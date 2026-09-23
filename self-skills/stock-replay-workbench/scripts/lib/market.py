from __future__ import annotations

from datetime import date
from datetime import timedelta

from .common import clean_symbol
from .common import em_json_get
from .common import failure
from .common import format_hhmmss
from .common import full_symbol
from .common import normalize_date
from .common import safe_float
from .common import safe_int
from .common import source
from .common import success
from .quote import quote_history
from .quote import quote_realtime


EASTMONEY_UT = "7eea3edcaed734bea9cbfc24409ed989"
A_STOCK_FS = "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23"
INDEXES = [
    ("000001", "上证指数"),
    ("399001", "深证成指"),
    ("399006", "创业板指"),
    ("000300", "沪深300"),
    ("000688", "科创50"),
    ("899050", "北证50"),
]
RANK_FIELDS = "f12,f13,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f15,f16,f17,f18,f20,f21,f23"


def _parse_rank_row(row: dict, rank: int) -> dict:
    code = str(row.get("f12") or "").strip()
    return {
        "rank": rank,
        "symbol": full_symbol(code) if code else None,
        "code": code,
        "name": row.get("f14"),
        "latest": safe_float(row.get("f2")),
        "change_ratio": safe_float(row.get("f3")),
        "change": safe_float(row.get("f4")),
        "volume": safe_float(row.get("f5")),
        "amount": safe_float(row.get("f6")),
        "amplitude": safe_float(row.get("f7")),
        "turnover_ratio": safe_float(row.get("f8")),
        "pe": safe_float(row.get("f9")),
        "volume_ratio": safe_float(row.get("f10")),
        "high": safe_float(row.get("f15")),
        "low": safe_float(row.get("f16")),
        "open": safe_float(row.get("f17")),
        "previous_close": safe_float(row.get("f18")),
        "total_market_cap": safe_float(row.get("f20")),
        "float_market_cap": safe_float(row.get("f21")),
        "pb": safe_float(row.get("f23")),
    }


def _parse_pool_row(row: dict, rank: int) -> dict:
    code = str(row.get("c") or "").strip()
    price_raw = safe_float(row.get("p"))
    stat = row.get("zttj") if isinstance(row.get("zttj"), dict) else {}
    return {
        "rank": rank,
        "symbol": full_symbol(code) if code else None,
        "code": code,
        "name": row.get("n"),
        "latest": round(price_raw / 1000, 3) if price_raw is not None else None,
        "change_ratio": safe_float(row.get("zdp")),
        "amount": safe_float(row.get("amount")),
        "turnover_ratio": safe_float(row.get("hs")),
        "board_count": safe_int(row.get("lbc")),
        "first_limit_time": format_hhmmss(row.get("fbt")),
        "last_limit_time": format_hhmmss(row.get("lbt")),
        "sealed_fund": safe_float(row.get("fund")),
        "break_count": safe_int(row.get("zbc")),
        "sector": row.get("hybk"),
        "limit_stat_days": stat.get("days"),
        "limit_stat_count": stat.get("ct"),
    }


def _market_breadth() -> dict:
    payload = em_json_get(
        "https://push2.eastmoney.com/api/qt/ulist.np/get",
        {
            "fltt": 2,
            "fields": "f104,f105,f106,f3,f6",
            "secids": "1.000001,0.399001,0.399006",
        },
    )
    rows = payload.get("data", {}).get("diff") or []
    return {
        "up": sum(
            safe_int(row.get("f104")) or 0 for row in rows if isinstance(row, dict)
        ),
        "down": sum(
            safe_int(row.get("f105")) or 0 for row in rows if isinstance(row, dict)
        ),
        "flat": sum(
            safe_int(row.get("f106")) or 0 for row in rows if isinstance(row, dict)
        ),
    }


def market_snapshot() -> dict:
    warnings: list[str] = []
    indexes = []
    source_chain: list[dict] = []
    partial = False
    for code, label in INDEXES:
        payload = quote_realtime(code)
        indexes.append({"symbol": code, "name": label, **payload["data"]})
        source_chain.extend(payload.get("source_chain", []))
        warnings.extend(payload.get("warnings", []))
        if payload["data"].get("latest_price") is None:
            partial = True
    try:
        breadth = _market_breadth()
        source_chain.append(source("eastmoney_market_breadth", True))
    except Exception as exc:
        breadth = {"up": 0, "down": 0, "flat": 0}
        source_chain.append(source("eastmoney_market_breadth", False, str(exc)))
        warnings.append(f"市场宽度公开源失败，已降级到 0 值占位: {exc}")
    if partial:
        warnings.append("部分指数快照未取到实时价格，已保留结构化降级结果。")
    return success(
        "market_snapshot",
        {"indexes": indexes, "breadth": breadth},
        source_chain,
        warnings,
    )


def rank(kind: str = "change_percent", limit: int = 20) -> dict:
    fid = {
        "change_percent": "f3",
        "amount": "f6",
        "volume": "f5",
        "turnover": "f8",
    }.get(kind, "f3")
    warnings: list[str] = []
    source_chain: list[dict] = []
    try:
        payload = em_json_get(
            "https://push2.eastmoney.com/api/qt/clist/get",
            {
                "pn": 1,
                "pz": max(1, min(limit, 200)),
                "po": 1,
                "np": 1,
                "ut": EASTMONEY_UT,
                "fltt": 2,
                "invt": 2,
                "fid": fid,
                "fs": A_STOCK_FS,
                "fields": RANK_FIELDS,
            },
        )
        rows = payload.get("data", {}).get("diff") or []
        items = [
            _parse_rank_row(row, index + 1)
            for index, row in enumerate(rows)
            if isinstance(row, dict)
        ]
        source_chain.append(source("eastmoney_clist", True))
        if not items:
            warnings.append("榜单公开源返回空列表，可能是非交易时段或接口波动。")
        return success(
            "rank",
            {
                "kind": kind,
                "limit": limit,
                "items": items,
                "returned_count": len(items),
            },
            source_chain,
            warnings,
        )
    except Exception as exc:
        source_chain.append(source("eastmoney_clist", False, str(exc)))
        warnings.append(f"榜单公开源失败，已返回空列表: {exc}")
        return success(
            "rank",
            {"kind": kind, "limit": limit, "items": [], "returned_count": 0},
            source_chain,
            warnings,
            source_status={"eastmoney_clist": "fallback"},
        )


def limit_pool(pool: str = "up", limit: int = 20) -> dict:
    endpoint = {
        "up": "getTopicZTPool",
        "down": "getTopicDTPool",
        "break": "getTopicZBPool",
        "yesterday-up": "getYesterdayZTPool",
    }.get(pool, "getTopicZTPool")
    sort = {
        "up": "fbt:asc",
        "break": "fbt:asc",
        "down": "fbt:asc",
        "yesterday-up": "zs:desc",
    }.get(pool, "fbt:asc")
    warnings: list[str] = []
    source_chain: list[dict] = []
    try:
        payload = None
        data = {}
        items: list[dict] = []
        query_dates = [None]
        today = date.today()
        # offset 从 1 起：offset=0 与首查 None（默认今天）重复，白白多打一次节流请求
        query_dates.extend(
            (today - timedelta(days=offset)).strftime("%Y%m%d")
            for offset in range(1, 9)
        )
        for query_date in query_dates:
            params = {
                "ut": EASTMONEY_UT,
                "dpt": "wz.ztzt",
                "Pageindex": 0,
                "pagesize": max(1, min(limit, 200)),
                "sort": sort,
            }
            if query_date:
                params["date"] = query_date
            payload = em_json_get(
                f"https://push2ex.eastmoney.com/{endpoint}",
                params,
                referer="https://quote.eastmoney.com/ztb/detail",
            )
            data = payload.get("data") or {}
            items = [
                _parse_pool_row(row, index + 1)
                for index, row in enumerate(data.get("pool") or [])
                if isinstance(row, dict)
            ]
            if items:
                if query_date:
                    warnings.append(f"涨跌停池回退到最近可用交易日 {query_date}。")
                break
        source_chain.append(source(f"eastmoney_{endpoint}", True))
        if not items:
            warnings.append("涨跌停池公开源返回空列表，可能是非交易日。")
        return success(
            "limit_pool",
            {
                "pool": pool,
                "trade_date": str(data.get("qdate") or ""),
                "items": items,
                "returned_count": len(items),
            },
            source_chain,
            warnings,
        )
    except Exception as exc:
        source_chain.append(source(f"eastmoney_{endpoint}", False, str(exc)))
        warnings.append(f"涨跌停池公开源失败，已返回空列表: {exc}")
        return success(
            "limit_pool",
            {"pool": pool, "items": [], "returned_count": 0},
            source_chain,
            warnings,
            source_status={endpoint: "fallback"},
        )


DD_DOWN_THRESHOLD = 0.002  # IBD: 收盘较昨收跌 >= 0.2%
DD_EXPIRY_SESSIONS = 25  # 超过 25 个交易日过期
DD_INVALIDATION_GAIN = 0.05  # DD 后指数涨 5% 失效
DD_EXPOSURE_POLICY = {
    "NORMAL": (100, "HOLD_OR_FOLLOW_BASE_STRATEGY"),
    "CAUTION": (75, "AVOID_NEW_ADDS"),
    "HIGH": (50, "REDUCE_EXPOSURE"),
    "SEVERE": (25, "CLOSE_OR_HEDGE"),
    # 数据不足分级：风险工具禁止 fail-open（K线缺失时输出 NORMAL=满仓信号
    # 会把「不知道」伪装成「安全」），cap=None 表示无法给出仓位上限。
    "UNKNOWN": (None, "DATA_INSUFFICIENT_MANUAL_REVIEW"),
}


def _ema(values: list[float], span: int) -> float | None:
    if len(values) < span:
        return None
    factor = 2.0 / (span + 1)
    ema = values[0]
    for value in values[1:]:
        ema = value * factor + ema * (1 - factor)
    return ema


def distribution_days(
    symbol: str = "000001", limit: int = 120, as_of: str | None = None
) -> dict:
    """IBD 派发日计数 + 风险分级（移植自 claude-trading-skills
    ibd-distribution-day-monitor，规则原文见 references/market-regime-playbook.md）。

    DD 判定：收盘较昨收跌 >= 0.2% 且成交量放大。
    DD 失效：超过 25 个交易日，或 DD 后指数最高价较 DD 收盘涨 >= 5%（当日 DD 不立即失效）。
    分级：NORMAL(d25<=2) / CAUTION(d25>=3) / HIGH(d25>=5 或 d15>=3 或 d5>=2)
         / SEVERE(d25>=6 或 d15>=4 或 (跌破21EMA或50MA 且 d25>=5))。
    as_of：历史回放截止日（YYYY-MM-DD / YYYYMMDD），K线截断到该日，防未来函数。
    """
    warnings: list[str] = []
    source_chain: list[dict] = []
    code = clean_symbol(symbol) if symbol else "000001"
    as_of_iso = None
    if as_of is not None:
        as_of_iso = normalize_date(as_of)
        if not as_of_iso:
            return failure(
                "distribution_days",
                "invalid_input",
                f"as_of={as_of!r} 不是合法日期（需 YYYY-MM-DD 或 YYYYMMDD）",
            )
    # clean_symbol 后再查前缀，防 "SH510300" 带市场前缀绕过；50=沪市 LOF/封基
    if code[:2] in ("50", "51", "56", "58", "15", "16"):
        warnings.append(
            "标的为 ETF/LOF 且使用不复权价：除权除息日的跳空会被误判为派发日，分级结果失真。"
        )
    history_payload = quote_history(
        code, "day", "none", max(limit, 80), as_of=as_of_iso
    )
    source_chain.extend(history_payload.get("source_chain") or [])
    warnings.extend(history_payload.get("warnings") or [])
    candles = (history_payload.get("data") or {}).get("candles") or []

    closes = [c.get("close") for c in candles]
    highs = [c.get("high") for c in candles]
    volumes = [c.get("volume") for c in candles]
    dates = [c.get("date") for c in candles]
    if len(candles) < 30:
        warnings.append(
            f"K线仅 {len(candles)} 根（<30），派发日计数与均线过滤不可靠，"
            "分级已降级为 UNKNOWN（数据不足，禁止按 NORMAL 消费）。"
        )
    valid_closes = [c for c in closes if c is not None]

    raw: list[dict] = []
    for index in range(1, len(candles)):
        close, prev_close = closes[index], closes[index - 1]
        volume, prev_volume = volumes[index], volumes[index - 1]
        if close is None or prev_close is None or not prev_close:
            continue
        if volume is None or prev_volume is None:
            continue
        pct = (close - prev_close) / prev_close
        if pct <= -DD_DOWN_THRESHOLD and volume > prev_volume:
            raw.append(
                {
                    "date": dates[index],
                    "index": index,
                    "close": close,
                    "change_percent": round(pct * 100, 3),
                }
            )

    last_index = len(candles) - 1
    active: list[dict] = []
    for record in raw:
        age = last_index - record["index"]
        if age > DD_EXPIRY_SESSIONS:
            continue
        tail_highs = [high for high in highs[record["index"] + 1 :] if high is not None]
        high_since = max(tail_highs) if tail_highs else None
        invalidated = (
            high_since is not None
            and record["close"]
            and high_since >= record["close"] * (1 + DD_INVALIDATION_GAIN)
        )
        if invalidated:
            continue
        active.append(
            {
                "date": record["date"],
                "close": record["close"],
                "change_percent": record["change_percent"],
                "age_sessions": age,
                "high_since": high_since,
            }
        )

    d5 = sum(1 for item in active if item["age_sessions"] <= 5)
    d15 = sum(1 for item in active if item["age_sessions"] <= 15)
    d25 = len(active)

    ema21 = _ema(valid_closes, 21)
    sma50 = (
        sum(valid_closes[-50:]) / len(valid_closes[-50:])
        if len(valid_closes) >= 50
        else None
    )
    latest_close = valid_closes[-1] if valid_closes else None
    below_ma: bool | None = None
    if latest_close is not None and (ema21 is not None or sma50 is not None):
        below_ma = (ema21 is not None and latest_close < ema21) or (
            sma50 is not None and latest_close < sma50
        )

    if len(candles) < 30:
        classification = "UNKNOWN"
    elif d25 >= 6 or d15 >= 4 or (below_ma and d25 >= 5):
        classification = "SEVERE"
    elif d25 >= 5 or d15 >= 3 or d5 >= 2:
        classification = "HIGH"
    elif d25 >= 3:
        classification = "CAUTION"
    else:
        classification = "NORMAL"
    exposure_cap, action = DD_EXPOSURE_POLICY[classification]

    warnings.append(
        "IBD 派发日规则移植自美股（QQQ/SPY 口径），用于 A 股指数时成交量口径与波动结构有差异，"
        "分级结果仅作参考输入，不构成交易指令。"
    )
    return success(
        "distribution_days",
        {
            "symbol": code,
            "full_symbol": full_symbol(code),
            "as_of": as_of_iso,
            "classification": classification,
            "d5_count": d5,
            "d15_count": d15,
            "d25_count": d25,
            "below_21ema_or_50ma": below_ma,
            "ema21": ema21,
            "sma50": sma50,
            "latest_close": latest_close,
            "active_distribution_days": active,
            "exposure_cap_pct": exposure_cap,
            "action": action,
        },
        source_chain,
        warnings,
    )
