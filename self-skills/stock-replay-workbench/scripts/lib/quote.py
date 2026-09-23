from __future__ import annotations

import json

import requests

from .common import (
    TENCENT_USER_AGENT,
    clean_symbol,
    full_symbol,
    guess_name,
    normalize_date,
    source,
    success,
    tencent_code,
)


HEADERS = {"User-Agent": TENCENT_USER_AGENT}


def _safe_float(value: str | None) -> float | None:
    if value in (None, "", "-", "--"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _safe_int(value: str | None) -> int | None:
    if value in (None, "", "-", "--"):
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def _detect_stale(
    latest_price: float | None, prev_close: float | None, volume: int | None
) -> tuple[bool, str | None]:
    if (
        latest_price is not None
        and prev_close is not None
        and volume == 0
        and latest_price == prev_close
    ):
        return True, "成交量为0且最新价等于昨收，疑似已迁移废码或停牌（僵尸报价）"
    return False, None


def _parse_tencent_quote(text: str, symbol: str) -> dict:
    body = text.split('="', 1)[1].rsplit('";', 1)[0]
    parts = body.split("~")
    latest_price = _safe_float(parts[3] if len(parts) > 3 else None)
    prev_close = _safe_float(parts[4] if len(parts) > 4 else None)
    volume = _safe_int(parts[6] if len(parts) > 6 else None)
    is_stale, stale_reason = _detect_stale(latest_price, prev_close, volume)
    return {
        "symbol": clean_symbol(symbol),
        "full_symbol": full_symbol(symbol),
        "name": parts[1] or guess_name(symbol),
        "latest_price": latest_price,
        "prev_close": prev_close,
        "open": _safe_float(parts[5] if len(parts) > 5 else None),
        "volume": volume,
        # parts[37]=成交额(万元)，parts[38]=换手率(%)。旧版误把 parts[37] 命名为 turnover。
        "amount": _safe_float(parts[37] if len(parts) > 37 else None),
        "amount_unit": "万元",
        "turnover_rate": _safe_float(parts[38] if len(parts) > 38 else None),
        "change": _safe_float(parts[31] if len(parts) > 31 else None),
        "change_percent": _safe_float(parts[32] if len(parts) > 32 else None),
        "high": _safe_float(parts[33] if len(parts) > 33 else None),
        "low": _safe_float(parts[34] if len(parts) > 34 else None),
        "timestamp": parts[30] if len(parts) > 30 else None,
        "is_stale": is_stale,
        "stale_reason": stale_reason,
    }


def quote_realtime(symbol: str) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    code = clean_symbol(symbol)
    try:
        response = requests.get(
            f"https://qt.gtimg.cn/q={tencent_code(symbol)}",
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        parsed = _parse_tencent_quote(response.text, symbol)
        source_chain.append(source("tencent_quote", True))
        if parsed.get("latest_price") is None:
            warnings.append("腾讯行情返回成功，但关键价格字段缺失。")
        if parsed.get("is_stale"):
            warnings.append(
                "疑似僵尸报价（成交量为0且价格未变）：可能是北交所已迁移废码或停牌标的，不要用于估值。"
            )
        return success("quote_realtime", parsed, source_chain, warnings)
    except Exception as exc:
        warnings.append(f"实时行情降级为本地最小结果: {exc}")
        source_chain.append(source("tencent_quote", False, str(exc)))
        return success(
            "quote_realtime",
            {
                "symbol": code,
                "full_symbol": full_symbol(symbol),
                "name": guess_name(symbol),
                "latest_price": None,
                "prev_close": None,
                "open": None,
                "volume": None,
                "amount": None,
                "amount_unit": "万元",
                "turnover_rate": None,
                "change": None,
                "change_percent": None,
                "high": None,
                "low": None,
                "timestamp": None,
            },
            source_chain,
            warnings,
            source_status={"tencent_quote": "fallback"},
        )


def quote_history(
    symbol: str,
    period: str = "day",
    adjust: str = "qfq",
    limit: int = 60,
    as_of: str | None = None,
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    code = clean_symbol(symbol)
    try:
        response = requests.get(
            "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get",
            params={"param": f"{tencent_code(symbol)},{period},,,{limit},{adjust}"},
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        body = payload.get("data", {}).get(tencent_code(symbol), {})
        api_key = "qfqday" if adjust == "qfq" else period
        raw_items = body.get(api_key, body.get(period, []))
        candles = []
        for item in raw_items:
            if len(item) < 6:
                continue
            candles.append(
                {
                    "date": item[0],
                    "open": _safe_float(item[1]),
                    "close": _safe_float(item[2]),
                    "high": _safe_float(item[3]),
                    "low": _safe_float(item[4]),
                    "volume": _safe_int(item[5]),
                }
            )
        # is not None 而非 truthy：空串 as_of 也要走非法值 warning，
        # 与 chip.py/market.py 的硬校验口径一致（此处为软校验分层设计）。
        if as_of is not None:
            as_of_iso = normalize_date(as_of)
            if not as_of_iso:
                warnings.append(
                    f"as_of={as_of!r} 不是合法日期（需 YYYY-MM-DD 或 YYYYMMDD），"
                    "已忽略截断——返回的是未截断数据，历史复盘时不得直接使用。"
                )
            if as_of_iso:
                before = len(candles)
                candles = [
                    candle
                    for candle in candles
                    if str(candle.get("date") or "") <= as_of_iso
                ]
                if len(candles) < before:
                    warnings.append(
                        f"已按 as_of={as_of_iso} 截断 {before - len(candles)} 根后续K线"
                        "（未来函数防护：历史复盘不得使用该日之后的数据）。"
                    )
        source_chain.append(source("tencent_kline", True))
        return success(
            "quote_history",
            {
                "symbol": code,
                "full_symbol": full_symbol(symbol),
                "period": period,
                "adjust": adjust,
                "as_of": as_of,
                "candles": candles,
                "latest_snapshot": candles[-1] if candles else None,
            },
            source_chain,
            warnings,
        )
    except Exception as exc:
        warnings.append(f"历史行情暂未拉取到公开源数据: {exc}")
        source_chain.append(source("tencent_kline", False, str(exc)))
        return success(
            "quote_history",
            {
                "symbol": code,
                "full_symbol": full_symbol(symbol),
                "period": period,
                "adjust": adjust,
                "as_of": as_of,
                "candles": [],
                "latest_snapshot": None,
            },
            source_chain,
            warnings,
            source_status={"tencent_kline": "fallback"},
        )
