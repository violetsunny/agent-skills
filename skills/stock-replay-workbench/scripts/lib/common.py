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

try:
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    _EM_RETRY = Retry(
        total=3,
        connect=3,
        backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    EM_SESSION.mount("https://", HTTPAdapter(max_retries=_EM_RETRY))
    EM_SESSION.mount("http://", HTTPAdapter(max_retries=_EM_RETRY))
except Exception:
    _EM_RETRY = None


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


SH_INDEX_CODES = {
    "000001",
    "000016",
    "000300",
    "000905",
    "000688",
    "000852",
    "000010",
}
SZ_INDEX_CODES = {"399001", "399006"}
MARKET_CODES = ("SH", "SZ", "BJ")


def parse_symbol(symbol: str) -> tuple[str, str | None]:
    """解析受支持写法为 (纯6位代码, 显式市场标识或None)。

    支持 600519 / SH600519 / 600519.SH（前后缀二选一）。
    市场标识矛盾或代码非法时抛 ValueError，绝不静默路由到另一只标的。
    """
    value = str(symbol).strip().upper()
    prefix = value[:2] if value[:2] in MARKET_CODES else None
    if prefix:
        value = value[2:]
    suffix = None
    if "." in value:
        head, tail = value.split(".", 1)
        value = head
        if tail in MARKET_CODES:
            suffix = tail
    if prefix and suffix and prefix != suffix:
        raise ValueError(f"{symbol!r} 市场标识自相矛盾：前缀 {prefix} vs 后缀 {suffix}")
    if not value.isdigit() or len(value) != 6:
        raise ValueError(f"无法把 {symbol!r} 解析为 6 位股票代码")
    return value, prefix or suffix


def _default_exchange(code: str) -> str:
    if code in SH_INDEX_CODES:
        return "SH"
    if code in SZ_INDEX_CODES:
        return "SZ"
    if code == "899050" or code.startswith("92"):
        return "BJ"
    if code.startswith(("5", "6", "9")):
        return "SH"
    if code.startswith(("4", "8")):
        return "BJ"
    if code.startswith(("0", "1", "2", "3")):
        return "SZ"
    return "SH"


def detect_exchange(symbol: str) -> str:
    code, market = parse_symbol(symbol)
    if not market:
        return _default_exchange(code)
    if code.startswith("000"):
        if market == "BJ":
            raise ValueError(f"{symbol!r}：000xxx 号段不属北交所")
        return market
    natural = _default_exchange(code)
    if market != natural:
        raise ValueError(
            f"{symbol!r} 市场标识与号段矛盾：{code} 属 {natural} 市，不是 {market} 市"
        )
    return market


def clean_symbol(symbol: str) -> str:
    try:
        code, _ = parse_symbol(symbol)
        return code
    except ValueError:
        value = str(symbol).strip().upper()
        if value[:2] in MARKET_CODES:
            value = value[2:]
        if "." in value:
            value = value.split(".", 1)[0]
        return value


def full_symbol(symbol: str) -> str:
    code = clean_symbol(symbol)
    try:
        exchange = detect_exchange(symbol)
    except ValueError:
        exchange = _default_exchange(code)
    return f"{code}.{exchange}"


def tencent_code(symbol: str) -> str:
    return f"{detect_exchange(symbol).lower()}{clean_symbol(symbol)}"


def em_market_code(symbol: str) -> int:
    """东财 secid 市场号：沪=1，深/北=0。

    不要用 startswith('6') 之类判市场——沪市 ETF(51x)、科创板 ETF(588x)、
    沪 B 股(900x) 会错判，北交所 920xxx 以 9 开头也会误判为沪。
    """
    return 1 if detect_exchange(symbol) == "SH" else 0


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
