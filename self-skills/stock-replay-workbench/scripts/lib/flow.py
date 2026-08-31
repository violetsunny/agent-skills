from __future__ import annotations

from .common import (
    clean_symbol,
    detect_exchange,
    em_json_get,
    em_market_code,
    format_hhmmss,
    safe_float,
    safe_int,
    source,
    success,
)
from .sector import sector


def _market_flow_from_akshare(limit: int) -> tuple[dict, dict]:
    import akshare as ak  # type: ignore

    frame = ak.stock_market_fund_flow()
    rows = frame.to_dict("records")
    if not rows:
        raise ValueError("akshare market money flow returned empty rows")
    items = []
    # reversed() puts the most-recent row first (items[0] = latest).
    # Callers must use items[0] for the latest entry, not items[-1].
    for index, row in enumerate(reversed(rows[-max(1, min(limit, 20)) :]), start=1):
        trade_date = row.get("日期")
        items.append(
            {
                "rank": index,
                "date": str(trade_date) if trade_date is not None else None,
                "sh_close": safe_float(row.get("上证-收盘价")),
                "sh_change_percent": safe_float(row.get("上证-涨跌幅")),
                "sz_close": safe_float(row.get("深证-收盘价")),
                "sz_change_percent": safe_float(row.get("深证-涨跌幅")),
                "main_net_inflow": safe_float(row.get("主力净流入-净额")),
                "main_net_inflow_percent": safe_float(row.get("主力净流入-净占比")),
                "super_large_net_inflow": safe_float(row.get("超大单净流入-净额")),
                "super_large_net_inflow_percent": safe_float(
                    row.get("超大单净流入-净占比")
                ),
                "large_net_inflow": safe_float(row.get("大单净流入-净额")),
                "large_net_inflow_percent": safe_float(row.get("大单净流入-净占比")),
                "medium_net_inflow": safe_float(row.get("中单净流入-净额")),
                "medium_net_inflow_percent": safe_float(row.get("中单净流入-净占比")),
                "small_net_inflow": safe_float(row.get("小单净流入-净额")),
                "small_net_inflow_percent": safe_float(row.get("小单净流入-净占比")),
            }
        )
    latest = items[0]
    return (
        {
            "scope": "market",
            "symbol": None,
            "limit": limit,
            "items": items,
            "summary": {
                "date": latest.get("date"),
                "main_net_inflow": latest.get("main_net_inflow"),
                "main_net_inflow_percent": latest.get("main_net_inflow_percent"),
                "sh_close": latest.get("sh_close"),
                "sz_close": latest.get("sz_close"),
            },
        },
        source("akshare_stock_market_fund_flow", True),
    )


def _parse_stock_kline(line: str) -> dict | None:
    parts = line.split(",")
    if len(parts) < 6:
        return None
    return {
        "date": parts[0],
        "main_net_inflow": safe_float(parts[1]),
        "small_net_inflow": safe_float(parts[2]),
        "medium_net_inflow": safe_float(parts[3]),
        "large_net_inflow": safe_float(parts[4]),
        "super_large_net_inflow": safe_float(parts[5]),
    }


def _stock_flow_from_eastmoney(symbol: str, limit: int) -> tuple[dict, dict]:
    code = clean_symbol(symbol)
    market = em_market_code(code)
    payload = em_json_get(
        "https://push2his.eastmoney.com/api/qt/stock/fflow/kline/get",
        params={
            "lmt": str(max(limit, 5)),
            "klt": "101",
            "secid": f"{market}.{code}",
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56",
            "ut": "b2884a393a59ad64002292a3e90d46a5",
        },
    )
    data = payload.get("data") or {}
    rows = [_parse_stock_kline(line) for line in data.get("klines") or []]
    items = [row for row in rows if row][-max(1, min(limit, 20)) :]
    if not items:
        raise ValueError("eastmoney stock money flow returned empty rows")
    summary = {
        "main_net_inflow": sum(item.get("main_net_inflow") or 0 for item in items),
        "small_net_inflow": sum(item.get("small_net_inflow") or 0 for item in items),
        "medium_net_inflow": sum(item.get("medium_net_inflow") or 0 for item in items),
        "large_net_inflow": sum(item.get("large_net_inflow") or 0 for item in items),
        "super_large_net_inflow": sum(
            item.get("super_large_net_inflow") or 0 for item in items
        ),
        "window": len(items),
    }
    return (
        {
            "scope": "stock",
            "symbol": code,
            "name": data.get("name"),
            "limit": limit,
            "items": items,
            "summary": summary,
        },
        source("eastmoney_stock_money_flow", True),
    )


def _stock_flow_from_rank(symbol: str, limit: int) -> tuple[dict, dict]:
    code = clean_symbol(symbol)
    payload = em_json_get(
        "https://push2delay.eastmoney.com/api/qt/clist/get",
        params={
            "fid": "f62",
            "po": "1",
            "pz": "100",
            "pn": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "ut": "b2884a393a59ad64002292a3e90d46a5",
            "fs": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2",
            "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f124",
        },
    )
    rows = (payload.get("data") or {}).get("diff") or []
    matched = next((row for row in rows if str(row.get("f12")) == code), None)
    if not isinstance(matched, dict):
        raise ValueError(f"eastmoney rank money flow missing {code}")
    item = {
        "symbol": code,
        "name": matched.get("f14"),
        "latest": safe_float(matched.get("f2")),
        "change_percent": safe_float(matched.get("f3")),
        "main_net_inflow": safe_float(matched.get("f62")),
        "main_net_inflow_percent": safe_float(matched.get("f184")),
        "super_large_net_inflow": safe_float(matched.get("f66")),
        "super_large_net_inflow_percent": safe_float(matched.get("f69")),
        "large_net_inflow": safe_float(matched.get("f72")),
        "large_net_inflow_percent": safe_float(matched.get("f75")),
        "medium_net_inflow": safe_float(matched.get("f78")),
        "medium_net_inflow_percent": safe_float(matched.get("f81")),
        "small_net_inflow": safe_float(matched.get("f84")),
        "small_net_inflow_percent": safe_float(matched.get("f87")),
        "timestamp": format_hhmmss(matched.get("f124")),
    }
    return (
        {
            "scope": "stock",
            "symbol": code,
            "name": matched.get("f14"),
            "limit": limit,
            "items": [item],
            "summary": {
                "main_net_inflow": item["main_net_inflow"],
                "main_net_inflow_percent": item["main_net_inflow_percent"],
                "latest": item["latest"],
                "change_percent": item["change_percent"],
                "timestamp": item["timestamp"],
            },
            "source_note": "个股明细接口失败后回退到东方财富排行快照",
        },
        source("eastmoney_stock_money_flow_rank", True),
    )


def _stock_flow_from_akshare(symbol: str, limit: int) -> tuple[dict, dict]:
    import akshare as ak  # type: ignore

    code = clean_symbol(symbol)
    market = detect_exchange(code).lower()
    frame = ak.stock_individual_fund_flow(stock=code, market=market)
    rows = frame.to_dict("records")
    items = []
    for row in rows[-max(1, min(limit, 20)) :]:
        items.append(
            {
                "date": row.get("日期"),
                "close": safe_float(row.get("收盘价")),
                "change_percent": safe_float(row.get("涨跌幅")),
                "main_net_inflow": safe_float(row.get("主力净流入-净额")),
                "main_net_inflow_percent": safe_float(row.get("主力净流入-净占比")),
                "super_large_net_inflow": safe_float(row.get("超大单净流入-净额")),
                "super_large_net_inflow_percent": safe_float(
                    row.get("超大单净流入-净占比")
                ),
                "large_net_inflow": safe_float(row.get("大单净流入-净额")),
                "large_net_inflow_percent": safe_float(row.get("大单净流入-净占比")),
                "medium_net_inflow": safe_float(row.get("中单净流入-净额")),
                "medium_net_inflow_percent": safe_float(row.get("中单净流入-净占比")),
                "small_net_inflow": safe_float(row.get("小单净流入-净额")),
                "small_net_inflow_percent": safe_float(row.get("小单净流入-净占比")),
            }
        )
    if not items:
        raise ValueError("akshare stock money flow returned empty rows")
    return (
        {
            "scope": "stock",
            "symbol": code,
            "limit": limit,
            "items": items,
            "summary": {
                "main_net_inflow": sum(
                    item.get("main_net_inflow") or 0 for item in items
                ),
                "main_net_inflow_percent": items[-1].get("main_net_inflow_percent"),
                "close": items[-1].get("close"),
                "date": items[-1].get("date"),
            },
        },
        source("akshare_stock_individual_fund_flow", True),
    )


def _sector_flow_from_akshare(scope: str, limit: int) -> tuple[dict, dict]:
    import akshare as ak  # type: ignore

    sector_type = "行业资金流" if scope == "industry" else "概念资金流"
    frame = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type=sector_type)
    rows = frame.to_dict("records")
    if not rows:
        raise ValueError(f"akshare {scope} money flow returned empty rows")
    items = []
    for index, row in enumerate(rows[: max(1, min(limit, 20))], start=1):
        items.append(
            {
                "rank": index,
                "name": row.get("名称"),
                "change_percent": safe_float(row.get("今日涨跌幅")),
                "main_net_inflow": safe_float(row.get("今日主力净流入-净额")),
                "main_net_inflow_percent": safe_float(row.get("今日主力净流入-净占比")),
                "super_large_net_inflow": safe_float(row.get("今日超大单净流入-净额")),
                "super_large_net_inflow_percent": safe_float(
                    row.get("今日超大单净流入-净占比")
                ),
                "large_net_inflow": safe_float(row.get("今日大单净流入-净额")),
                "large_net_inflow_percent": safe_float(
                    row.get("今日大单净流入-净占比")
                ),
                "medium_net_inflow": safe_float(row.get("今日中单净流入-净额")),
                "medium_net_inflow_percent": safe_float(
                    row.get("今日中单净流入-净占比")
                ),
                "small_net_inflow": safe_float(row.get("今日小单净流入-净额")),
                "small_net_inflow_percent": safe_float(
                    row.get("今日小单净流入-净占比")
                ),
                "leader": row.get("今日主力净流入最大股"),
            }
        )
    latest = items[0]
    return (
        {
            "scope": scope,
            "symbol": None,
            "limit": limit,
            "items": items,
            "summary": {
                "leader_sector": latest.get("name"),
                "leader_stock": latest.get("leader"),
                "main_net_inflow": latest.get("main_net_inflow"),
                "main_net_inflow_percent": latest.get("main_net_inflow_percent"),
            },
        },
        source(f"akshare_stock_sector_fund_flow_rank_{scope}", True),
    )


def _sector_flow_from_sector_signal(
    scope: str, limit: int
) -> tuple[dict, list[dict], list[str]]:
    action = "industry-rank" if scope == "industry" else "concept-rank"
    payload = sector(action, None, limit)
    rows = [
        item
        for item in (payload.get("data", {}).get("items") or [])
        if isinstance(item, dict)
    ]
    items = []
    for index, row in enumerate(rows[: max(1, min(limit, 20))], start=1):
        items.append(
            {
                "rank": index,
                "name": row.get("name") or row.get("板块名称"),
                "change_percent": safe_float(
                    row.get("change_percent")
                    if row.get("change_percent") is not None
                    else row.get("板块涨幅")
                ),
                "main_net_inflow": row.get("main_net_inflow"),
                "main_net_inflow_percent": row.get("main_net_inflow_percent"),
                "leader": row.get("leader") or row.get("领涨股票"),
                "signal_type": "sector_rank_fallback",
            }
        )
    if not items:
        raise ValueError(f"sector signal fallback returned empty rows for {scope}")
    latest = items[0]
    data = {
        "scope": scope,
        "symbol": None,
        "limit": limit,
        "items": items,
        "summary": {
            "leader_sector": latest.get("name"),
            "leader_stock": latest.get("leader"),
            "change_percent": latest.get("change_percent"),
            "source_note": f"{scope} 资金流主源失败后，已回退到板块排行信号。",
        },
        "source_note": f"{scope} 资金流当前为板块排行信号回退结果。",
    }
    return data, payload.get("source_chain", []), payload.get("warnings", [])


def money_flow(
    scope: str = "market", symbol: str | None = None, limit: int = 20
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    cleaned_symbol = clean_symbol(symbol) if symbol else None

    if scope == "market":
        try:
            data, chain_item = _market_flow_from_akshare(limit)
            source_chain.append(chain_item)
            return success("money_flow", data, source_chain, warnings)
        except Exception as exc:
            warnings.append(f"市场资金流主源失败: {exc}")
            source_chain.append(
                source("akshare_stock_market_fund_flow", False, str(exc))
            )
            return success(
                "money_flow",
                {
                    "scope": "market",
                    "symbol": None,
                    "limit": limit,
                    "items": [],
                    "summary": {
                        "status": "unavailable",
                        "note": "市场资金流主源失败，当前返回空样本，请结合其他盘面指标交叉确认。",
                    },
                },
                source_chain,
                warnings,
                source_status={"market_money_flow": "fallback-empty"},
            )

    if scope in {"industry", "concept"}:
        try:
            data, chain_item = _sector_flow_from_akshare(scope, limit)
            source_chain.append(chain_item)
            return success("money_flow", data, source_chain, warnings)
        except Exception as exc:
            warnings.append(f"{scope} 资金流主源失败: {exc}")
            source_chain.append(
                source(f"akshare_stock_sector_fund_flow_rank_{scope}", False, str(exc))
            )
        try:
            data, fallback_chain, fallback_warnings = _sector_flow_from_sector_signal(
                scope, limit
            )
            source_chain.extend(fallback_chain)
            warnings.extend(fallback_warnings)
            warnings.append(f"{scope} 资金流已回退到板块排行信号。")
            return success("money_flow", data, source_chain, warnings)
        except Exception as exc:
            warnings.append(f"{scope} 板块信号回退失败: {exc}")
            return success(
                "money_flow",
                {
                    "scope": scope,
                    "symbol": None,
                    "limit": limit,
                    "items": [],
                    "summary": None,
                },
                source_chain,
                warnings,
                source_status={f"{scope}_money_flow": "fallback-empty"},
            )

    if cleaned_symbol is None:
        return success(
            "money_flow",
            {
                "scope": scope,
                "symbol": None,
                "limit": limit,
                "items": [],
                "summary": None,
            },
            [source("stock_money_flow", False, "symbol is required for stock scope")],
            ["个股资金流需要 symbol。"],
            source_status={"stock_money_flow": "invalid-request"},
        )

    try:
        data, chain_item = _stock_flow_from_eastmoney(cleaned_symbol, limit)
        source_chain.append(chain_item)
        return success("money_flow", data, source_chain, warnings)
    except Exception as exc:
        warnings.append(f"个股资金流明细主源失败，回退中: {exc}")
        source_chain.append(source("eastmoney_stock_money_flow", False, str(exc)))

    try:
        data, chain_item = _stock_flow_from_rank(cleaned_symbol, limit)
        source_chain.append(chain_item)
        warnings.append("个股资金流已回退到东方财富排行快照。")
        return success("money_flow", data, source_chain, warnings)
    except Exception as exc:
        warnings.append(f"个股资金流排行回退失败，继续尝试 akshare: {exc}")
        source_chain.append(source("eastmoney_stock_money_flow_rank", False, str(exc)))

    try:
        data, chain_item = _stock_flow_from_akshare(cleaned_symbol, limit)
        source_chain.append(chain_item)
        warnings.append("个股资金流为公开源 best-effort 数据。")
        return success("money_flow", data, source_chain, warnings)
    except Exception as exc:
        warnings.append(f"个股资金流公开源暂不可用: {exc}")
        source_chain.append(
            source("akshare_stock_individual_fund_flow", False, str(exc))
        )
        return success(
            "money_flow",
            {
                "scope": "stock",
                "symbol": cleaned_symbol,
                "limit": limit,
                "items": [],
                "summary": {
                    "status": "unavailable",
                    "note": "个股资金流公开源当前不可用，已返回空样本，请结合成交额、涨跌停和板块强度交叉确认。",
                },
            },
            source_chain,
            warnings,
            source_status={"stock_money_flow": "fallback-empty"},
        )
