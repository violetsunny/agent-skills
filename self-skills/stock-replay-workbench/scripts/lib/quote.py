from __future__ import annotations

import json

import requests

from .common import (
    TENCENT_USER_AGENT,
    clean_symbol,
    full_symbol,
    guess_name,
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


def _parse_tencent_quote(text: str, symbol: str) -> dict:
    body = text.split('="', 1)[1].rsplit('";', 1)[0]
    parts = body.split("~")
    latest_price = _safe_float(parts[3] if len(parts) > 3 else None)
    prev_close = _safe_float(parts[4] if len(parts) > 4 else None)
    volume = _safe_int(parts[6] if len(parts) > 6 else None)
    is_stale = (
        latest_price is not None
        and prev_close is not None
        and volume == 0
        and latest_price == prev_close
    )
    return {
        "symbol": clean_symbol(symbol),
        "full_symbol": full_symbol(symbol),
        "name": parts[1] or guess_name(symbol),
        "latest_price": latest_price,
        "prev_close": prev_close,
        "open": _safe_float(parts[5] if len(parts) > 5 else None),
        "volume": volume,
        "turnover": _safe_float(parts[37] if len(parts) > 37 else None),
        "change": _safe_float(parts[31] if len(parts) > 31 else None),
        "change_percent": _safe_float(parts[32] if len(parts) > 32 else None),
        "high": _safe_float(parts[33] if len(parts) > 33 else None),
        "low": _safe_float(parts[34] if len(parts) > 34 else None),
        "timestamp": parts[30] if len(parts) > 30 else None,
        "is_stale": is_stale,
        "stale_reason": "成交量为0且最新价等于昨收，疑似已迁移废码或停牌（僵尸报价）"
        if is_stale
        else None,
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
                "turnover": None,
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
        source_chain.append(source("tencent_kline", True))
        return success(
            "quote_history",
            {
                "symbol": code,
                "full_symbol": full_symbol(symbol),
                "period": period,
                "adjust": adjust,
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
                "candles": [],
                "latest_snapshot": None,
            },
            source_chain,
            warnings,
            source_status={"tencent_kline": "fallback"},
        )
