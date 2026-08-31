from __future__ import annotations

from datetime import date
from datetime import timedelta

from .common import em_json_get
from .common import format_hhmmss
from .common import full_symbol
from .common import safe_float
from .common import safe_int
from .common import source
from .common import success
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
        query_dates.extend(
            (today - timedelta(days=offset)).strftime("%Y%m%d")
            for offset in range(0, 8)
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
