from __future__ import annotations

from datetime import date

from .common import now_iso, success
from .events import announcement, dragon_tiger, margin_trading, news, sentiment_heat
from .flow import money_flow
from .fundamental import fundamental
from .market import limit_pool, market_snapshot, rank
from .sector import sector


_STATIC_DISCLAIMER_WARNINGS = {
    "融资融券为交易所公开源 best-effort 数据，深沪字段可能不完全一致。"
}

_STATIC_DISCLAIMER_SUBSTRINGS = ("为公开源 best-effort 数据。",)


def limit_sentiment(limit: int = 50) -> dict:
    up_payload = limit_pool("up", limit)
    break_payload = limit_pool("break", limit)
    down_payload = limit_pool("down", limit)
    yesterday_up_payload = limit_pool("yesterday-up", limit)

    warnings: list[str] = []
    source_chain: list[dict] = []
    for payload in (up_payload, break_payload, down_payload, yesterday_up_payload):
        _extend_chain(source_chain, payload)
        _extend_warnings(warnings, payload)

    up_count = up_payload.get("data", {}).get("returned_count", 0)
    break_count = break_payload.get("data", {}).get("returned_count", 0)
    yesterday_up_items = yesterday_up_payload.get("data", {}).get("items", [])
    advance_count = sum(
        1 for item in yesterday_up_items if (item.get("change_ratio") or 0) >= 9.8
    )
    earning_count = sum(
        1 for item in yesterday_up_items if (item.get("change_ratio") or 0) > 0
    )
    yesterday_up_count = yesterday_up_payload.get("data", {}).get("returned_count", 0)

    return success(
        "limit_sentiment",
        {
            "limit": limit,
            "up_count": up_count,
            "break_count": break_count,
            "down_count": down_payload.get("data", {}).get("returned_count", 0),
            "break_rate": round(break_count / (up_count + break_count) * 100, 1)
            if (up_count + break_count)
            else 0.0,
            "yesterday_up_count": yesterday_up_count,
            "advance_count": advance_count,
            "advance_rate": round(advance_count / yesterday_up_count * 100, 1)
            if yesterday_up_count
            else 0.0,
            "earning_rate": round(earning_count / yesterday_up_count * 100, 1)
            if yesterday_up_count
            else 0.0,
            "max_height": max(
                [
                    item.get("board_count") or 0
                    for item in up_payload.get("data", {}).get("items", [])
                ]
                or [0]
            ),
        },
        source_chain,
        warnings,
    )


def _extend_chain(target: list[dict], payload: dict) -> None:
    target.extend(payload.get("source_chain", []))


def _extend_warnings(target: list[str], payload: dict) -> None:
    for item in payload.get("warnings", []):
        text = str(item).strip()
        if text:
            target.append(text)


def _unique_strings(items: list[str], limit: int | None = None) -> list[str]:
    unique: list[str] = []
    for item in items:
        text = str(item).strip()
        if text and text not in unique:
            unique.append(text)
    return unique if limit is None else unique[:limit]


def _split_disclaimers(items: list[str]) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    disclaimers: list[str] = []
    for item in _unique_strings(items):
        if item in _STATIC_DISCLAIMER_WARNINGS or any(
            marker in item for marker in _STATIC_DISCLAIMER_SUBSTRINGS
        ):
            disclaimers.append(item)
        else:
            warnings.append(item)
    return warnings, disclaimers


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


def _empty_event_bucket() -> dict:
    return {"summary": [], "evidence": []}


def _empty_market_event_snapshots() -> dict:
    return {
        "announcements": _empty_event_bucket(),
        "news": _empty_event_bucket(),
        "dragon_tiger": _empty_event_bucket(),
        "margin_trading": _empty_event_bucket(),
    }


def _first_present(row: dict, keys: tuple[str, ...]) -> object:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _event_evidence(
    rows: list[dict], keys: tuple[str, ...], limit: int = 3
) -> list[dict]:
    evidence: list[dict] = []
    for row in rows[:limit]:
        item = {key: row.get(key) for key in keys if row.get(key) not in (None, "")}
        if item:
            evidence.append(item)
    return evidence


def _event_rows(payload: dict) -> list[dict]:
    items = payload.get("data", {}).get("items") or []
    return [item for item in items if isinstance(item, dict)]


def _filter_event_payload(payload: dict, symbol: str | None) -> dict:
    if not symbol:
        return payload

    symbol_text = str(symbol)
    rows = [
        row
        for row in _event_rows(payload)
        if symbol_text
        in {
            str(value)
            for key, value in row.items()
            if key in ("代码", "证券代码", "symbol", "code") and value not in (None, "")
        }
    ]
    filtered = dict(payload)
    data = dict(payload.get("data") or {})
    data["symbol"] = symbol_text
    data["items"] = rows
    data["returned_count"] = len(rows)
    filtered["data"] = data
    return filtered


def _summarize_market_news(news_payload: dict, themes: dict) -> dict:
    rows = _top_items(news_payload, 3)
    bucket = _empty_event_bucket()
    bucket["evidence"] = _event_evidence(
        rows, ("title", "source", "published_at", "url"), limit=3
    )
    titles = [str(row.get("title", "")) for row in rows if row.get("title")]
    if titles:
        bucket["summary"].append(f"市场资讯前排聚焦：{'; '.join(titles[:2])}。")
    theme_hits = []
    for label in (themes.get("main") or []) + (themes.get("secondary") or []):
        if any(str(label) in title for title in titles):
            theme_hits.append(str(label))
    if theme_hits:
        bucket["summary"].append(
            f"新闻流与当前主线存在重合，相关方向包括 {'、'.join(_unique_strings(theme_hits, 3))}。"
        )
    bucket["summary"] = _unique_strings(bucket["summary"], 2)
    return bucket


def _summarize_market_dragon_tiger(payload: dict) -> dict:
    rows = _top_items(payload, 3)
    bucket = _empty_event_bucket()
    bucket["evidence"] = _event_evidence(
        rows,
        ("代码", "名称", "解读", "收盘价", "涨跌幅", "成交额", "净买额"),
        limit=3,
    )
    count = payload.get("data", {}).get("returned_count", 0)
    if count:
        bucket["summary"].append(
            f"当日龙虎榜样本 {count} 条，活跃资金仍在前排强势股中博弈。"
        )
    names = [
        str(_first_present(row, ("名称", "股票简称", "代码")))
        for row in rows
        if _first_present(row, ("名称", "股票简称", "代码"))
    ]
    if names:
        bucket["summary"].append(
            f"龙虎榜前排样本包括 {'、'.join(_unique_strings(names, 3))}。"
        )
    bucket["summary"] = _unique_strings(bucket["summary"], 2)
    return bucket


def _summarize_market_margin_trading(payload: dict) -> dict:
    rows = _top_items(payload, 3)
    bucket = _empty_event_bucket()
    bucket["evidence"] = _event_evidence(
        rows,
        ("证券代码", "证券简称", "融资余额", "融资买入额", "融资偿还额", "融券余量"),
        limit=3,
    )
    count = payload.get("data", {}).get("returned_count", 0)
    if count:
        bucket["summary"].append(
            f"两融样本返回 {count} 条，可作为资金博弈的 best-effort 旁证。"
        )
    names = [
        str(_first_present(row, ("证券简称", "名称", "证券代码")))
        for row in rows
        if _first_present(row, ("证券简称", "名称", "证券代码"))
    ]
    if names:
        bucket["summary"].append(
            f"两融前排样本关注 {'、'.join(_unique_strings(names, 3))}。"
        )
    bucket["summary"] = _unique_strings(bucket["summary"], 2)
    return bucket


def _summarize_focus_announcements(payload: dict) -> dict:
    rows = _top_items(payload, 3)
    bucket = _empty_event_bucket()
    bucket["evidence"] = _event_evidence(
        rows, ("title", "announcement_time", "pdf_url"), limit=3
    )
    titles = [str(row.get("title", "")) for row in rows if row.get("title")]
    if titles:
        bucket["summary"].append(f"公告侧有新增披露：{'; '.join(titles[:2])}。")
    return bucket


def _summarize_focus_news(payload: dict) -> dict:
    rows = _top_items(payload, 3)
    bucket = _empty_event_bucket()
    bucket["evidence"] = _event_evidence(
        rows, ("title", "source", "published_at", "url"), limit=3
    )
    titles = [str(row.get("title", "")) for row in rows if row.get("title")]
    if titles:
        bucket["summary"].append(f"个股新闻跟踪到：{'; '.join(titles[:2])}。")
    return bucket


def _summarize_focus_dragon_tiger(payload: dict) -> dict:
    rows = _top_items(payload, 3)
    bucket = _empty_event_bucket()
    bucket["evidence"] = _event_evidence(
        rows,
        ("代码", "名称", "解读", "收盘价", "涨跌幅", "净买额"),
        limit=3,
    )
    if rows:
        bucket["summary"].append("该标的命中龙虎榜样本，可作为席位活跃度旁证。")
    return bucket


def _summarize_focus_margin_trading(payload: dict) -> dict:
    rows = _top_items(payload, 3)
    bucket = _empty_event_bucket()
    bucket["evidence"] = _event_evidence(
        rows,
        ("证券代码", "证券简称", "融资余额", "融资买入额", "融资偿还额", "融券余量"),
        limit=3,
    )
    if rows:
        bucket["summary"].append("该标的存在两融记录，可作为资金承接的补充观察。")
    return bucket


def _build_market_event_snapshots(
    trade_date: str | None, limit: int, themes: dict
) -> tuple[dict, dict[str, dict], list[dict], list[str]]:
    market = _empty_market_event_snapshots()
    source_chain: list[dict] = []
    warnings: list[str] = []

    news_payload = news(None, limit)
    dragon_payload = dragon_tiger(None, trade_date, limit)
    margin_payload = margin_trading(None, trade_date, limit)

    for payload in (news_payload, dragon_payload, margin_payload):
        _extend_chain(source_chain, payload)
        _extend_warnings(warnings, payload)

    market["news"] = _summarize_market_news(news_payload, themes)
    market["dragon_tiger"] = _summarize_market_dragon_tiger(dragon_payload)
    market["margin_trading"] = _summarize_market_margin_trading(margin_payload)
    payloads = {
        "news": news_payload,
        "dragon_tiger": dragon_payload,
        "margin_trading": margin_payload,
    }
    return market, payloads, source_chain, warnings


def _build_focus_event_snapshot(
    symbol: str,
    name: str | None,
    trade_date: str | None,
    limit: int,
    market_event_payloads: dict[str, dict] | None = None,
) -> tuple[dict, list[dict], list[str]]:
    source_chain: list[dict] = []
    warnings: list[str] = []

    announcement_payload = announcement(symbol, None, limit)
    news_payload = news(symbol, limit)
    reused_dragon_payload = (market_event_payloads or {}).get("dragon_tiger")
    reused_margin_payload = (market_event_payloads or {}).get("margin_trading")
    dragon_payload = _filter_event_payload(
        reused_dragon_payload or dragon_tiger(symbol, trade_date, limit), symbol
    )
    margin_payload = _filter_event_payload(
        reused_margin_payload or margin_trading(symbol, trade_date, limit), symbol
    )

    for payload in (announcement_payload, news_payload):
        _extend_chain(source_chain, payload)
        _extend_warnings(warnings, payload)

    if not reused_dragon_payload:
        _extend_chain(source_chain, dragon_payload)
        _extend_warnings(warnings, dragon_payload)
    if not reused_margin_payload:
        _extend_chain(source_chain, margin_payload)
        _extend_warnings(warnings, margin_payload)

    snapshot = {
        "symbol": symbol,
        "name": name,
        "announcements": _summarize_focus_announcements(announcement_payload),
        "news": _summarize_focus_news(news_payload),
        "dragon_tiger": _summarize_focus_dragon_tiger(dragon_payload),
        "margin_trading": _summarize_focus_margin_trading(margin_payload),
    }
    return snapshot, source_chain, warnings


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
        "divergence": "部分公开源查询失败或已降级，分歧判断需结合次日盘面确认"
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
        risks.append("部分公开源查询失败或已降级，复盘结论需结合次日盘口确认。")
    if limit_up_payload.get("warnings"):
        risks.append("涨停池存在交易日回退或空池风险，强势股样本可能不完整。")
    return _unique_strings(risks) or [
        "当前复盘为规则化底稿，事件归因仍需人工补充确认。"
    ]


def _build_capital_and_events(
    industry_flow_payload: dict,
    concept_flow_payload: dict,
    warnings: list[str],
    event_snapshots: dict | None = None,
) -> dict:
    capital = []
    for payload in (industry_flow_payload, concept_flow_payload):
        first = (_top_items(payload, 1) or [{}])[0]
        if first.get("name"):
            capital.append(f"{first.get('name')} 处于板块资金流前排。")
    market_events = (event_snapshots or {}).get("market") or {}
    focus_events = (event_snapshots or {}).get("focus") or []

    special = []
    catalysts = []
    market_special = (
        (market_events.get("dragon_tiger") or {}).get("summary") or []
    ) + ((market_events.get("margin_trading") or {}).get("summary") or [])
    for item in _unique_strings(market_special):
        special.append(item)
    for focus in focus_events[:3]:
        for key in ("dragon_tiger", "margin_trading"):
            for item in (focus.get(key) or {}).get("summary") or []:
                label = focus.get("name") or focus.get("symbol") or "重点股"
                special.append(f"{label}：{item}")

    market_catalysts = ((market_events.get("news") or {}).get("summary") or []) + (
        (market_events.get("announcements") or {}).get("summary") or []
    )
    for item in _unique_strings(market_catalysts):
        catalysts.append(item)
    for focus in focus_events[:3]:
        for key in ("announcements", "news"):
            for item in (focus.get(key) or {}).get("summary") or []:
                label = focus.get("name") or focus.get("symbol") or "重点股"
                catalysts.append(f"{label}：{item}")

    return {
        "capital": capital or ["当前板块资金流以公开源 best-effort 结果为主。"],
        "special": _unique_strings(special, 3)
        or ["龙虎榜 / 两融暂无有效摘要，继续保留为旁证层。"],
        "catalysts": _unique_strings(catalysts, 3)
        or (
            ["如需公告 / 新闻催化，请在底稿基础上继续补事件域查询。"]
            if warnings
            else ["当前未提炼出明确事件催化摘要。"]
        ),
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
    return "低" if len(_unique_strings(warnings)) >= 4 else "中"


def build_replay(trade_date: str | None = None, limit: int = 5) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []

    snapshot_payload = market_snapshot()
    limit_up_payload = limit_pool("up", limit)
    limit_sentiment_payload = limit_sentiment(max(limit, 20))
    amount_rank_payload = rank("amount", limit)
    industry_rank_payload = sector("industry-rank", None, limit)
    concept_rank_payload = sector("concept-rank", None, limit)
    industry_flow_payload = money_flow("industry", None, limit)
    concept_flow_payload = money_flow("concept", None, limit)

    for payload in [
        snapshot_payload,
        limit_up_payload,
        limit_sentiment_payload,
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

    event_themes = _build_themes(
        industry_rank_payload,
        concept_rank_payload,
        industry_flow_payload,
        concept_flow_payload,
        warnings,
    )

    market_events, market_event_payloads, market_event_chain, market_event_warnings = (
        _build_market_event_snapshots(trade_date, limit, event_themes)
    )
    _extend_warnings(warnings, {"warnings": market_event_warnings})
    source_chain.extend(market_event_chain)

    sentiment_heat_payload = sentiment_heat(max(limit, 10))
    _extend_chain(source_chain, sentiment_heat_payload)

    focus_event_snapshots = []
    for snapshot in fundamental_snapshots:
        symbol = snapshot.get("symbol")
        if not symbol:
            continue
        focus_snapshot, focus_chain, focus_warnings = _build_focus_event_snapshot(
            str(symbol),
            snapshot.get("name"),
            trade_date,
            limit,
            market_event_payloads,
        )
        focus_event_snapshots.append(focus_snapshot)
        source_chain.extend(focus_chain)
        _extend_warnings(warnings, {"warnings": focus_warnings})

    warnings, disclaimers = _split_disclaimers(warnings)

    themes = _build_themes(
        industry_rank_payload,
        concept_rank_payload,
        industry_flow_payload,
        concept_flow_payload,
        warnings,
    )

    event_snapshots = {
        "market": market_events,
        "focus": focus_event_snapshots,
    }

    replay_data = {
        "trade_date": trade_date or date.today().isoformat(),
        "summary": _build_summary(
            snapshot_payload,
            industry_flow_payload,
            concept_flow_payload,
            limit_up_payload,
        ),
        "market_overview": _build_market_overview(snapshot_payload, limit_up_payload),
        "themes": themes,
        "sectors": _build_sectors(industry_rank_payload, concept_rank_payload, limit),
        "sector_money_flow": {
            "industry": industry_flow_payload.get("data", {}).get("items") or [],
            "concept": concept_flow_payload.get("data", {}).get("items") or [],
        },
        "leaders": _build_leaders(limit_up_payload, amount_rank_payload, limit),
        "limit_sentiment": limit_sentiment_payload.get("data", {}),
        "sentiment_heat": sentiment_heat_payload.get("data", {}),
        "fundamental_snapshots": fundamental_snapshots,
        "event_snapshots": event_snapshots,
        "capital_and_events": _build_capital_and_events(
            industry_flow_payload, concept_flow_payload, warnings, event_snapshots
        ),
        "watchlist": _build_watchlist(
            limit_up_payload, industry_flow_payload, concept_flow_payload
        ),
        "risks": _build_risks(warnings, limit_up_payload),
        "disclaimers": disclaimers,
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
