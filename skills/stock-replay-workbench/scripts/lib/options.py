from __future__ import annotations

import re

import requests

from .common import clean_symbol, safe_float, source, success


_SINA_OPTION_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://stock.finance.sina.com.cn/",
}

_UNDERLYING_TO_CATE = {
    "510050": "50ETF",
    "510300": "300ETF",
    "588000": "科创50ETF",
    "510500": "500ETF",
}


def _strip_js_var_payload(text: str) -> list[str]:
    match = re.search(r'="(.*)"', text)
    if not match:
        return []
    return match.group(1).split(",")


def _sina_option_list(node: str) -> list[str]:
    response = requests.get(
        f"https://hq.sinajs.cn/list={node}",
        headers=_SINA_OPTION_HEADERS,
        timeout=10,
    )
    response.encoding = "gbk"
    return _strip_js_var_payload(response.text)


def option_codes(underlying: str = "510050") -> dict:
    code = clean_symbol(underlying)
    cate = _UNDERLYING_TO_CATE.get(code, _UNDERLYING_TO_CATE["510050"])
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: dict[str, dict[str, list[str]]] = {}
    try:
        response = requests.get(
            "https://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName",
            params={"exchange": "null", "cate": cate},
            headers=_SINA_OPTION_HEADERS,
            timeout=10,
        )
        payload = response.json()
        months = ((payload.get("result") or {}).get("data") or {}).get(
            "contractMonth"
        ) or []
        for month in months[1:]:
            normalized_month = str(month).replace("-", "")[2:]
            call_codes = [
                value.replace("CON_OP_", "")
                for value in _sina_option_list(f"OP_UP_{code}{normalized_month}")
                if value.startswith("CON_OP_")
            ]
            put_codes = [
                value.replace("CON_OP_", "")
                for value in _sina_option_list(f"OP_DOWN_{code}{normalized_month}")
                if value.startswith("CON_OP_")
            ]
            if call_codes or put_codes:
                items[normalized_month] = {"call": call_codes, "put": put_codes}
        if not items:
            warnings.append("ETF期权公开源返回空列表，已保留结构化空样本。")
        source_chain.append(source("sina_option_codes", True))
    except Exception as exc:
        warnings.append(f"ETF期权公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("sina_option_codes", False, str(exc)))

    return success(
        "option_codes",
        {
            "underlying": code,
            "items": items,
            "returned_count": sum(
                len(bucket.get("call", [])) + len(bucket.get("put", []))
                for bucket in items.values()
            ),
        },
        source_chain,
        warnings,
    )


def option_tquote(code: str) -> dict:
    option_code = clean_symbol(code)
    warnings: list[str] = []
    source_chain: list[dict] = []
    item: dict[str, object] = {}
    try:
        values = _sina_option_list(f"CON_OP_{option_code}")
        if len(values) >= 43:
            item = {
                "code": option_code,
                "bid_vol": safe_float(values[0]),
                "bid": safe_float(values[1]),
                "last": safe_float(values[2]),
                "ask": safe_float(values[3]),
                "ask_vol": safe_float(values[4]),
                "open_interest": safe_float(values[5]),
                "pct": safe_float(values[6]),
                "strike": safe_float(values[7]),
                "prev_close": safe_float(values[8]),
                "open": safe_float(values[9]),
                "limit_up": safe_float(values[10]),
                "limit_down": safe_float(values[11]),
                "name": values[37],
                "amplitude": safe_float(values[38]),
                "high": safe_float(values[39]),
                "low": safe_float(values[40]),
                "volume": safe_float(values[41]),
                "amount": safe_float(values[42]),
            }
        else:
            warnings.append("ETF期权公开源返回空列表，已保留结构化空样本。")
        source_chain.append(source("sina_option_tquote", True))
    except Exception as exc:
        warnings.append(f"ETF期权公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("sina_option_tquote", False, str(exc)))

    return success(
        "option_tquote",
        {
            "code": option_code,
            "item": item,
            "returned_count": 1 if item else 0,
        },
        source_chain,
        warnings,
    )


def option_greeks(code: str) -> dict:
    option_code = clean_symbol(code)
    warnings: list[str] = []
    source_chain: list[dict] = []
    item: dict[str, object] = {}
    try:
        raw = _sina_option_list(f"CON_SO_{option_code}")
        if len(raw) >= 16:
            values = [raw[0]] + raw[4:]
            item = {
                "code": option_code,
                "name": values[0],
                "volume": safe_float(values[1]),
                "delta": safe_float(values[2]),
                "gamma": safe_float(values[3]),
                "theta": safe_float(values[4]),
                "vega": safe_float(values[5]),
                "iv": safe_float(values[6]),
                "high": safe_float(values[7]),
                "low": safe_float(values[8]),
                "trade_code": values[9],
                "strike": safe_float(values[10]),
                "last": safe_float(values[11]),
                "theory": safe_float(values[12]),
            }
        else:
            warnings.append("ETF期权公开源返回空列表，已保留结构化空样本。")
        source_chain.append(source("sina_option_greeks", True))
    except Exception as exc:
        warnings.append(f"ETF期权公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("sina_option_greeks", False, str(exc)))

    return success(
        "option_greeks",
        {
            "code": option_code,
            "item": item,
            "returned_count": 1 if item else 0,
        },
        source_chain,
        warnings,
    )
