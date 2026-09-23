from __future__ import annotations

import json
import math
import os
import random
import time
from datetime import date, datetime, timezone

# akshare 内部用 tqdm 输出进度条到 stderr，调用方 2>&1 合并时会污染 CLI JSON 输出。
os.environ.setdefault("TQDM_DISABLE", "1")

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
except (ImportError, OSError):
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
    """尽力提取6位代码，非法输入返回去前缀/后缀后的原始字符串。

    与 parse_symbol 的严格校验不同，本函数为"best-effort"语义：
    当输入无法通过 parse_symbol 校验时，仍尝试剥离市场标识返回纯文本，
    供下游做模糊匹配或日志展示。若需严格校验请使用 parse_symbol。
    """
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


def normalize_date(value: str | None) -> str | None:
    """把 YYYYMMDD / YYYY-MM-DD 归一为 YYYY-MM-DD；非法输入返回 None。"""
    if not value:
        return None
    text = str(value).replace("-", "")
    if len(text) != 8 or not text.isdigit():
        return None
    try:
        return date(int(text[:4]), int(text[4:6]), int(text[6:8])).isoformat()
    except ValueError:
        return None


def is_historical_date(trade_date: str | None) -> bool:
    normalized = normalize_date(trade_date)
    if not normalized:
        return False
    return date.fromisoformat(normalized) < date.today()


def snapshot_notice(trade_date: str | None) -> str:
    return (
        f"未来函数警示：{normalize_date(trade_date)} 是历史日期，但实时/快照类接口"
        "（实时行情、资金流、热榜、涨停池等）返回的是当前数据，无法回溯截断，"
        "不得当作该历史日的事实使用。"
    )


def collect_missing(data: dict, required_paths: list[str]) -> list[str]:
    """按点分路径检查 data 中缺失/为空的关键字段，返回缺失路径列表。
    用于报告顶部显式告警，禁止静默省略数据缺口。"""
    missing: list[str] = []
    for path in required_paths:
        node: object = data
        for key in path.split("."):
            if not isinstance(node, dict):
                node = None
                break
            node = node.get(key)
        if node is None or node == [] or node == {}:
            missing.append(path)
    return missing


def _em_throttle() -> None:
    global _EM_LAST_CALL
    wait = EM_MIN_INTERVAL - (time.time() - _EM_LAST_CALL)
    if wait > 0:
        time.sleep(wait + random.uniform(0.1, 0.4))
    # 请求发起前就打点：网络异常时同样消耗了风控配额，
    # 若在成功后才打点，连续失败期间会退化成不限流连打。
    _EM_LAST_CALL = time.time()


def em_get(
    url: str,
    params: dict | None = None,
    timeout: int = 15,
    referer: str = "https://quote.eastmoney.com/",
) -> requests.Response:
    _em_throttle()
    response = EM_SESSION.get(
        url,
        params=params,
        timeout=timeout,
        headers={"Referer": referer},
    )
    response.raise_for_status()
    return response


def em_post(
    url: str,
    json_body: dict | None = None,
    timeout: int = 15,
    referer: str = "https://quote.eastmoney.com/",
) -> requests.Response:
    """东财 POST 请求（emappdata 等人气榜端点），与 em_get 共享同一节流预算。
    ponytail: 仅覆盖 JSON body 场景；如需 form 表单再加 data 参数。"""
    _em_throttle()
    response = EM_SESSION.post(
        url,
        json=json_body,
        timeout=timeout,
        headers={"Referer": referer},
    )
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
