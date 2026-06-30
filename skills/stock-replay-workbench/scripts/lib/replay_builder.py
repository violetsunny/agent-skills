from __future__ import annotations

from datetime import date

from .common import now_iso, success
from .flow import money_flow
from .fundamental import fundamental
from .market import limit_pool, market_snapshot, rank
from .sector import sector


def _extend_chain(target: list[dict], payload: dict) -> None:
    target.extend(payload.get("source_chain", []))


def _extend_warnings(target: list[str], payload: dict) -> None:
    target.extend(payload.get("warnings", []))


def _top_items(payload: dict, count: int) -> list[dict]:
    items = payload.get("data", {}).get("items") or []
    return [item for item in items if isinstance(item, dict)][:count]


def _pool_leader_symbols(pool_payload: dict, count: int) -> list[str]:
    symbols: list[str] = []
    for item in _top_items(pool_payload, count):
        symbol = item.get("code") or item.get("symbol")
        if symbol:
            symbols.append(str(symbol).split(".", 1)[0])
    return symbols


def _rank_leader_symbols(rank_payload: dict, count: int) -> list[str]:
    symbols: list[str] = []
    for item in _top_items(rank_payload, count):
        symbol = item.get("code") or item.get("symbol")
        if symbol:
            symbols.append(str(symbol).split(".", 1)[0])
    return symbols


def _pick_focus_symbols(
    pool_payload: dict, rank_payload: dict, count: int
) -> list[str]:
    chosen = _pool_leader_symbols(pool_payload, count) or _rank_leader_symbols(
        rank_payload, count
    )
    unique: list[str] = []
    for symbol in chosen:
        if symbol not in unique:
            unique.append(symbol)
    return unique[:count]


def _build_market_overview(
    snapshot_payload: dict, limit_up_payload: dict
) -> list[dict]:
    overview: list[dict] = []
    indexes = snapshot_payload.get("data", {}).get("indexes") or []
    breadth = snapshot_payload.get("data", {}).get("breadth") or {}
    for item in indexes[:3]:
        overview.append(
            {
                "metric": item.get("name") or item.get("symbol"),
                "value": (
                    f"{item.get('change_percent'):.2f}%"
                    if isinstance(item.get("change_percent"), (int, float))
                    else "-"
                ),
                "comment": f"最新价 {item.get('latest_price') or '-'}",
            }
        )
    overview.append(
        {
            "metric": "涨跌家数",
            "value": f"{breadth.get('up', 0)} / {breadth.get('down', 0)} / {breadth.get('flat', 0)}",
            "comment": "上涨 / 下跌 / 平盘",
        }
    )
    overview.append(
        {
            "metric": "涨停池",
            "value": str(limit_up_payload.get("data", {}).get("returned_count", 0)),
            "comment": "涨停池样本数",
        }
    )
    return overview


def _build_themes(
    industry_rank_payload: dict,
    concept_rank_payload: dict,
    industry_flow_payload: dict,
    concept_flow_payload: dict,
    warnings: list[str],
) -> dict:
    main = []
    secondary = []
    for payload in (industry_flow_payload, concept_flow_payload):
        for item in _top_items(payload, 2):
            name = item.get("name")
            if name and name not in main:
                main.append(str(name))
    for payload in (industry_rank_payload, concept_rank_payload):
        for item in _top_items(payload, 2):
            name = item.get("name")
            if name and name not in main and name not in secondary:
                secondary.append(str(name))
    return {
        "main": main[:2],
        "secondary": secondary[:2],
        "sentiment": "涨停池和板块前排仍有活跃度" if main else "情绪信号偏弱",
        "divergence": "公开源存在 best-effort 字段，请结合次日盘面确认"
        if warnings
        else "当前未见明显结构性回落信号",
    }


def _build_sectors(
    industry_rank_payload: dict, concept_rank_payload: dict, limit: int
) -> list[dict]:
    rows: list[dict] = []
    for payload in (industry_rank_payload, concept_rank_payload):
        for item in _top_items(payload, max(1, limit // 2 or 1)):
            rows.append(
                {
                    "name": item.get("name"),
                    "performance": item.get("change_percent"),
                    "leaders": item.get("leader"),
                    "catalyst": "来自板块排行前排",
                }
            )
    return rows[:limit]


def _build_leaders(
    limit_up_payload: dict, amount_rank_payload: dict, limit: int
) -> list[dict]:
    leaders: list[dict] = []
    for item in _top_items(limit_up_payload, limit):
        leaders.append(
            {
                "symbol": item.get("code") or item.get("symbol"),
                "status": "涨停池前排",
                "fact": item.get("sector") or "封板强度待继续跟踪",
                "role": "强势观察",
            }
        )
    if leaders:
        return leaders[:limit]
    for item in _top_items(amount_rank_payload, limit):
        leaders.append(
            {
                "symbol": item.get("code") or item.get("symbol"),
                "status": "成交额前排",
                "fact": f"成交额 {item.get('amount') or '-'}",
                "role": "中军观察",
            }
        )
    return leaders[:limit]


def _build_watchlist(
    limit_up_payload: dict,
    industry_flow_payload: dict,
    concept_flow_payload: dict,
) -> list[str]:
    items: list[str] = []
    for item in _top_items(limit_up_payload, 2):
        code = item.get("code") or item.get("symbol") or "未知标的"
        sector_name = item.get("sector") or "所属方向"
        items.append(f"观察 {code} 是否继续带动 {sector_name} 方向强度延续。")
    for payload in (industry_flow_payload, concept_flow_payload):
        first = (_top_items(payload, 1) or [{}])[0]
        leader = first.get("leader")
        name = first.get("name")
        if leader and name:
            items.append(f"观察 {leader} 能否继续维持 {name} 的资金承接。")
    unique: list[str] = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique[:3]


def _build_risks(warnings: list[str], limit_up_payload: dict) -> list[str]:
    risks = []
    if warnings:
        risks.append("部分公开源字段为 best-effort，复盘结论需结合次日盘口确认。")
    if limit_up_payload.get("warnings"):
        risks.append("涨停池存在交易日回退或空池风险，强势股样本可能不完整。")
    return risks or ["当前复盘为规则化底稿，事件归因仍需人工补充确认。"]


def _build_capital_and_events(
    industry_flow_payload: dict, concept_flow_payload: dict, warnings: list[str]
) -> dict:
    capital = []
    for payload in (industry_flow_payload, concept_flow_payload):
        first = (_top_items(payload, 1) or [{}])[0]
        if first.get("name"):
            capital.append(f"{first.get('name')} 处于板块资金流前排。")
    return {
        "capital": capital or ["当前板块资金流以公开源 best-effort 结果为主。"],
        "special": ["龙虎榜 / 大宗 / 两融尚未自动并入第一版底稿。"],
        "catalysts": ["如需公告 / 新闻催化，请在底稿基础上继续补事件域查询。"]
        if warnings
        else ["第一版底稿暂不自动归因公告与新闻事件。"],
    }


def _build_summary(
    snapshot_payload: dict,
    industry_flow_payload: dict,
    concept_flow_payload: dict,
    limit_up_payload: dict,
) -> str:
    indexes = snapshot_payload.get("data", {}).get("indexes") or []
    first_index = indexes[0] if indexes else {}
    index_name = first_index.get("name") or "市场"
    index_change = first_index.get("change_percent")
    trend = (
        f"{index_name} {index_change:.2f}%"
        if isinstance(index_change, (int, float))
        else "指数方向待确认"
    )
    industry_name = (
        ((_top_items(industry_flow_payload, 1) or [{}])[0]).get("name") or "行业前排"
    )
    concept_name = (
        ((_top_items(concept_flow_payload, 1) or [{}])[0]).get("name") or "概念前排"
    )
    pool_count = limit_up_payload.get("data", {}).get("returned_count", 0)
    return f"{trend}，涨停池样本 {pool_count} 只，板块资金流主要集中在 {industry_name} 和 {concept_name}。"


def _confidence(warnings: list[str]) -> str:
    return "低" if len(warnings) >= 4 else "中"


def build_replay(trade_date: str | None = None, limit: int = 5) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []

    snapshot_payload = market_snapshot()
    limit_up_payload = limit_pool("up", limit)
    amount_rank_payload = rank("amount", limit)
    industry_rank_payload = sector("industry-rank", None, limit)
    concept_rank_payload = sector("concept-rank", None, limit)
    industry_flow_payload = money_flow("industry", None, limit)
    concept_flow_payload = money_flow("concept", None, limit)

    for payload in [
        snapshot_payload,
        limit_up_payload,
        amount_rank_payload,
        industry_rank_payload,
        concept_rank_payload,
        industry_flow_payload,
        concept_flow_payload,
    ]:
        _extend_chain(source_chain, payload)
        _extend_warnings(warnings, payload)

    focus_symbols = _pick_focus_symbols(
        limit_up_payload, amount_rank_payload, min(limit, 3)
    )
    fundamental_snapshots = []
    for symbol in focus_symbols:
        payload = fundamental(symbol)
        _extend_chain(source_chain, payload)
        _extend_warnings(warnings, payload)
        data = payload.get("data") or {}
        if isinstance(data, dict):
            fundamental_snapshots.append(data)

    replay_data = {
        "trade_date": trade_date or date.today().isoformat(),
        "summary": _build_summary(
            snapshot_payload,
            industry_flow_payload,
            concept_flow_payload,
            limit_up_payload,
        ),
        "market_overview": _build_market_overview(snapshot_payload, limit_up_payload),
        "themes": _build_themes(
            industry_rank_payload,
            concept_rank_payload,
            industry_flow_payload,
            concept_flow_payload,
            warnings,
        ),
        "sectors": _build_sectors(industry_rank_payload, concept_rank_payload, limit),
        "sector_money_flow": {
            "industry": industry_flow_payload.get("data", {}).get("items") or [],
            "concept": concept_flow_payload.get("data", {}).get("items") or [],
        },
        "leaders": _build_leaders(limit_up_payload, amount_rank_payload, limit),
        "fundamental_snapshots": fundamental_snapshots,
        "capital_and_events": _build_capital_and_events(
            industry_flow_payload, concept_flow_payload, warnings
        ),
        "watchlist": _build_watchlist(
            limit_up_payload, industry_flow_payload, concept_flow_payload
        ),
        "risks": _build_risks(warnings, limit_up_payload),
        "source_chain": [
            item.get("source") for item in source_chain if item.get("source")
        ],
        "timestamp": now_iso().replace("T", " ").replace("Z", ""),
        "warnings": warnings,
        "confidence": _confidence(warnings),
    }
    return success(
        "build_replay",
        replay_data,
        source_chain,
        warnings,
        trade_date=replay_data["trade_date"],
    )
