from __future__ import annotations

import json
import math
import random
import time
from datetime import datetime, timezone

import requests


LOCAL_SYMBOL_NAMES = {
    "000001": "上证指数",
    "000300": "沪深300",
    "000688": "科创50",
    "300750": "宁德时代",
    "399001": "深证成指",
    "399006": "创业板指",
    "600519": "贵州茅台",
    "899050": "北证50",
}

EM_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
TENCENT_USER_AGENT = "Mozilla/5.0 stock-replay-workbench/0.2"
EM_MIN_INTERVAL = 1.0
EM_SESSION = requests.Session()
EM_SESSION.headers.update(
    {
        "User-Agent": EM_USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }
)
_EM_LAST_CALL = 0.0


def now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def meta(trade_date: str | None = None, source_status: dict | None = None) -> dict:
    return {
        "generated_at": now_iso(),
        "trade_date": trade_date,
        "source_status": source_status or {},
    }


def source(source: str, ok: bool, note: str | None = None) -> dict:
    item = {"source": source, "ok": ok}
    if note:
        item["note"] = note
    return item


def success(
    intent: str,
    data: dict,
    source_chain: list[dict] | None = None,
    warnings: list[str] | None = None,
    trade_date: str | None = None,
    source_status: dict | None = None,
) -> dict:
    return {
        "ok": True,
        "intent": intent,
        "data": data,
        "source_chain": source_chain or [],
        "warnings": warnings or [],
        "meta": meta(trade_date=trade_date, source_status=source_status),
    }


def failure(
    intent: str,
    error_type: str,
    message: str,
    data: dict | None = None,
    source_chain: list[dict] | None = None,
    warnings: list[str] | None = None,
    trade_date: str | None = None,
    source_status: dict | None = None,
) -> dict:
    return {
        "ok": False,
        "intent": intent,
        "data": data,
        "source_chain": source_chain or [],
        "warnings": warnings or [],
        "error": {"type": error_type, "message": message},
        "meta": meta(trade_date=trade_date, source_status=source_status),
    }


def emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def clean_symbol(symbol: str) -> str:
    value = symbol.strip().upper()
    if "." in value:
        value = value.split(".", 1)[0]
    return value


def detect_exchange(symbol: str) -> str:
    value = clean_symbol(symbol)
    if value in {"000001", "000300", "000688"}:
        return "SH"
    if value in {"399001", "399006"}:
        return "SZ"
    if value == "899050":
        return "BJ"
    if value.startswith(("5", "6", "9")):
        return "SH"
    if value.startswith(("0", "1", "2", "3", "4", "8")):
        return "SZ"
    return "SH"


def full_symbol(symbol: str) -> str:
    value = symbol.strip().upper()
    if "." in value:
        return value
    return f"{clean_symbol(value)}.{detect_exchange(value)}"


def tencent_code(symbol: str) -> str:
    code = clean_symbol(symbol)
    exchange = detect_exchange(symbol).lower()
    if exchange == "bj":
        exchange = "bj"
    return f"{exchange}{code}"


def guess_name(symbol: str) -> str | None:
    return LOCAL_SYMBOL_NAMES.get(clean_symbol(symbol))


def safe_float(value: object) -> float | None:
    if value in (None, "", "-", "--"):
        return None
    try:
        number = float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def safe_int(value: object) -> int | None:
    number = safe_float(value)
    if number is None:
        return None
    return int(number)


def pick(row: dict, keys: list[str]) -> object:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def format_hhmmss(value: object) -> str | None:
    number = safe_int(value)
    if number is None:
        return None
    text = f"{number:06d}"
    return f"{text[0:2]}:{text[2:4]}:{text[4:6]}"


def em_get(
    url: str,
    params: dict | None = None,
    timeout: int = 15,
    referer: str = "https://quote.eastmoney.com/",
) -> requests.Response:
    global _EM_LAST_CALL
    wait = EM_MIN_INTERVAL - (time.time() - _EM_LAST_CALL)
    if wait > 0:
        time.sleep(wait + random.uniform(0.1, 0.4))
    response = EM_SESSION.get(
        url,
        params=params,
        timeout=timeout,
        headers={"Referer": referer},
    )
    _EM_LAST_CALL = time.time()
    response.raise_for_status()
    return response


def em_json_get(
    url: str,
    params: dict | None = None,
    timeout: int = 15,
    referer: str = "https://quote.eastmoney.com/",
) -> dict:
    payload = em_get(url, params=params, timeout=timeout, referer=referer).json()
    if not isinstance(payload, dict):
        raise ValueError("eastmoney response is not a JSON object")
    return payload
