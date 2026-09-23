from __future__ import annotations

import numpy as np
import requests

from .common import (
    TENCENT_USER_AGENT,
    clean_symbol,
    em_json_get,
    em_market_code,
    failure,
    full_symbol,
    normalize_date,
    safe_float,
    source,
    success,
    tencent_code,
)


def _fetch_kline_with_turnover_em(
    symbol: str, limit: int, end: str = "20500101"
) -> list[dict]:
    """东财 push2his 日K（前复权），f61 为换手率(%)。一次拿齐 OHLC+换手。
    end 为截止日 YYYYMMDD（历史回放传 as_of，默认取到最新）。"""
    payload = em_json_get(
        "https://push2his.eastmoney.com/api/qt/stock/kline/get",
        params={
            "secid": f"{em_market_code(symbol)}.{clean_symbol(symbol)}",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",
            "fqt": "1",
            "end": end,
            "lmt": str(max(1, limit)),
        },
    )
    klines = ((payload.get("data") or {}).get("klines")) or []
    rows = []
    for line in klines:
        parts = str(line).split(",")
        if len(parts) < 11:
            continue
        rows.append(
            {
                "date": parts[0],
                "close": safe_float(parts[2]),
                "high": safe_float(parts[3]),
                "low": safe_float(parts[4]),
                "turnover_rate": safe_float(parts[10]),
            }
        )
    return rows


def _fetch_kline_turnover_estimated(
    symbol: str, limit: int, end: str | None = None
) -> tuple[list[dict], str]:
    """备胎：腾讯日K（无换手率字段）+ 实时行情流通市值估算换手率。
    估算假设窗口内流通股本不变，股本变动大的票（增发/解禁）会有偏差。
    end 为截止日 YYYY-MM-DD（历史回放传 as_of）。"""
    quote_response = requests.get(
        f"https://qt.gtimg.cn/q={tencent_code(symbol)}",
        headers={"User-Agent": TENCENT_USER_AGENT},
        timeout=10,
    )
    quote_response.raise_for_status()
    quote_parts = quote_response.text.split('="', 1)[1].rsplit('";', 1)[0].split("~")
    latest_price = safe_float(quote_parts[3] if len(quote_parts) > 3 else None)
    float_cap_yi = safe_float(quote_parts[44] if len(quote_parts) > 44 else None)
    if not latest_price or not float_cap_yi:
        raise ValueError("腾讯实时行情缺少现价或流通市值，无法估算换手率")
    float_shares = float_cap_yi * 1e8 / latest_price

    kline_response = requests.get(
        "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get",
        params={
            "param": f"{tencent_code(symbol)},day,,{end or ''},{max(1, limit)},qfq"
        },
        headers={"User-Agent": TENCENT_USER_AGENT},
        timeout=10,
    )
    kline_response.raise_for_status()
    body = kline_response.json().get("data", {}).get(tencent_code(symbol), {})
    raw_items = body.get("qfqday", body.get("day", []))
    rows = []
    for item in raw_items:
        if len(item) < 6:
            continue
        volume = safe_float(item[5])
        close = safe_float(item[2])
        turnover_rate = None
        if volume is not None and close:
            turnover_rate = volume * 100 / float_shares * 100
        rows.append(
            {
                "date": item[0],
                "close": close,
                "high": safe_float(item[3]),
                "low": safe_float(item[4]),
                "turnover_rate": turnover_rate,
            }
        )
    return rows, (
        "换手率为估算值：腾讯日K不含换手率，按当前流通股本回推，"
        "窗口内如有增发/解禁等股本变动会有偏差。"
    )


def _triangular_weights(
    grid: np.ndarray, low: float, high: float, avg: float
) -> np.ndarray:
    """当日筹码在价格网格上的三角分布权重（峰值在均价，面积归一）。"""
    weights = np.zeros_like(grid)
    if not np.isfinite([low, high, avg]).all() or high < low:
        return weights
    if high - low < 1e-9:  # 一字板：全部堆在一个价位
        weights[np.argmin(np.abs(grid - low))] = 1.0
        return weights
    avg = min(max(avg, low), high)  # 均价必须落在当日区间内
    left = (grid >= low) & (grid <= avg)
    right = (grid > avg) & (grid <= high)
    if avg - low > 1e-9:
        weights[left] = (grid[left] - low) / (avg - low)
    else:
        weights[left] = 1.0
    if high - avg > 1e-9:
        weights[right] = (high - grid[right]) / (high - avg)
    else:
        weights[right] = 1.0
    total = weights.sum()
    if total > 0:
        return weights / total
    # 兜底：当日振幅窄于网格步长时权重全为 0，若跳过该日会连换手衰减一起丢失，
    # 低波动标的+长窗口下累积成大偏差。映射到最近网格点。
    weights[np.argmin(np.abs(grid - avg))] = 1.0
    return weights


def _compute_chip_distribution(
    rows: list[dict], grid_size: int = 300, decay: float = 1.0
) -> tuple[dict, list[str]]:
    data = [
        row
        for row in rows
        if row.get("high")
        and row.get("low")
        and row.get("close")
        and row.get("turnover_rate") is not None
        and row["high"] > 0
    ]
    if not data:
        raise ValueError("有效行数为 0（检查是否全是停牌日，或换手率字段缺失）")
    # 换手衰减是有方向的时序递推，倒序会静默算错，强制按日期升序。
    data.sort(key=lambda row: str(row["date"]))

    lo = min(float(row["low"]) for row in data)
    hi = max(float(row["high"]) for row in data)
    pad = (hi - lo) * 0.02 or max(lo * 0.02, 0.01)
    grid = np.linspace(lo - pad, hi + pad, grid_size)

    # 初始筹码必须播种成「首日全部流通盘」，不能从全零开始：
    # 从零起步等于假设窗口之前没有任何持仓，会把窗口内少量换手归一化成 100%。
    chips: np.ndarray | None = None
    for row in data:
        turnover = min(max(float(row["turnover_rate"]) / 100.0 * decay, 0.0), 1.0)
        avg = (float(row["high"]) + float(row["low"]) + float(row["close"])) / 3.0
        weights = _triangular_weights(grid, float(row["low"]), float(row["high"]), avg)
        if weights.sum() <= 0:
            continue
        if chips is None:
            chips = weights.copy()
            continue
        chips = chips * (1.0 - turnover) + weights * turnover
    if chips is None:
        raise RuntimeError("所有交易日的价格区间都无效，无法构建分布")

    total = chips.sum()
    if total <= 0:
        raise RuntimeError("筹码总量为 0，无法计算指标")
    chips = chips / total

    price = float(data[-1]["close"])
    cum = np.cumsum(chips)

    def price_at(q: float) -> float:
        return float(np.interp(q, cum, grid))

    p05, p15, p85, p95 = (price_at(q) for q in (0.05, 0.15, 0.85, 0.95))
    peak_index = int(np.argmax(chips))
    profit_ratio = float(chips[grid <= price].sum())
    avg_cost = float((grid * chips).sum())
    concentration_90 = (p95 - p05) / (p95 + p05) if p95 + p05 else None
    concentration_70 = (p85 - p15) / (p85 + p15) if p85 + p15 else None

    # 硬约束自检（违反说明算法或输入有问题，必须显式告警）
    self_check: list[str] = []
    if not 0.0 <= profit_ratio <= 1.0:
        self_check.append(f"获利比例 {profit_ratio} 超出 [0,1]，结果不可信")
    if not float(grid[0]) <= avg_cost <= float(grid[-1]):
        self_check.append(f"平均成本 {avg_cost} 超出网格范围，结果不可信")
    if not (p05 <= p15 and p85 <= p95):
        self_check.append("90% 成本区间未包含 70% 成本区间，结果不可信")
    if (
        concentration_90 is not None
        and concentration_70 is not None
        and concentration_90 <= concentration_70
    ):
        self_check.append("90% 集中度未大于 70% 集中度，结果不可信")

    result = {
        "price": price,
        "profit_ratio": profit_ratio,
        "avg_cost": avg_cost,
        "cost_90": [p05, p95],
        "cost_70": [p15, p85],
        "concentration_90": concentration_90,
        "concentration_70": concentration_70,
        "peak_price": float(grid[peak_index]),
        "window_days": len(data),
        "histogram": [
            [round(float(point), 4), round(float(weight), 6)]
            for point, weight in zip(grid, chips)
            if weight > 1e-6
        ],
    }
    return result, self_check


def chip_distribution(
    symbol: str,
    limit: int = 250,
    decay: float = 1.0,
    grid_size: int = 300,
    as_of: str | None = None,
) -> dict:
    """筹码分布本地推演（三角分布+换手衰减）。东财无公开 CYQ 接口，业界通行本地推演。
    decay=1.0 按真实换手率；1.5~2.0 加快历史筹码消散，可对齐同花顺口径。
    as_of：历史回放截止日（YYYY-MM-DD / YYYYMMDD），K线截断到该日，防未来函数。"""
    warnings: list[str] = []
    source_chain: list[dict] = []
    code = clean_symbol(symbol)
    as_of_iso = None
    if as_of is not None:
        as_of_iso = normalize_date(as_of)
        if not as_of_iso:
            return failure(
                "chip_distribution",
                "invalid_input",
                f"as_of={as_of!r} 不是合法日期（需 YYYY-MM-DD 或 YYYYMMDD）",
            )
    rows: list[dict] = []
    try:
        rows = _fetch_kline_with_turnover_em(
            symbol, limit, end=(as_of_iso or "9999-12-31").replace("-", "")
        )
        source_chain.append(source("eastmoney_kline_turnover", True))
        if not rows:
            raise ValueError("东财K线返回空列表")
    except Exception as exc:
        source_chain.append(source("eastmoney_kline_turnover", False, str(exc)))
        warnings.append(f"东财K线(含换手率)不可用，回退腾讯K线+换手率估算: {exc}")
    if not rows:
        try:
            rows, estimate_warning = _fetch_kline_turnover_estimated(
                symbol, limit, end=as_of_iso
            )
            source_chain.append(source("tencent_kline_estimated_turnover", True))
            warnings.append(estimate_warning)
            if as_of_iso:
                warnings.append(
                    f"历史回放(as_of={as_of_iso})下换手率按当前流通市值估算，"
                    "as_of 时至今的股本变动会造成偏差，且流通市值本身是当前值（未来函数风险）。"
                )
        except Exception as exc:
            source_chain.append(
                source("tencent_kline_estimated_turnover", False, str(exc))
            )
            warnings.append(f"筹码分布多源均失败: {exc}")
            return success(
                "chip_distribution",
                {"symbol": code, "full_symbol": full_symbol(symbol), "result": None},
                source_chain,
                warnings,
            )
    if as_of_iso:
        # 双保险：即使数据源忽略 end 参数，也在本地按日期截断，防未来函数
        before = len(rows)
        rows = [row for row in rows if str(row.get("date") or "") <= as_of_iso]
        if len(rows) < before:
            warnings.append(
                f"已按 as_of={as_of_iso} 截断 {before - len(rows)} 根后续K线。"
            )
        warnings.append(
            f"前复权基准锚定在取数日而非 as_of：{as_of_iso} 之后的除权除息会整体"
            "平移历史价格，result.price 等绝对价位不等于 as_of 当日真实收盘价；"
            "分布形状与获利比例内部自洽，跨除权日对比绝对价位时需注意。"
        )
    try:
        result, self_check = _compute_chip_distribution(rows, grid_size, decay)
    except (ValueError, RuntimeError) as exc:
        warnings.append(f"筹码分布计算失败: {exc}")
        return success(
            "chip_distribution",
            {"symbol": code, "full_symbol": full_symbol(symbol), "result": None},
            source_chain,
            warnings,
        )
    warnings.extend(self_check)
    warnings.append(
        "筹码分布为本地推演口径（三角分布+换手衰减），非同花顺/Level-2 官方口径；"
        "输入为前复权价。"
    )
    result.update(
        {
            "symbol": code,
            "full_symbol": full_symbol(symbol),
            "decay": decay,
            "as_of": as_of_iso,
        }
    )
    return success(
        "chip_distribution",
        {"symbol": code, "full_symbol": full_symbol(symbol), "result": result},
        source_chain,
        warnings,
    )
