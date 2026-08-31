#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.bond import bond
from lib.common import emit, failure, success
from lib.events import (
    announcement,
    block_trade,
    dragon_tiger,
    margin_trading,
    news,
    sentiment_heat,
)
from lib.flow import money_flow
from lib.fundamental import fundamental
from lib.irm import irm_qa
from lib.market import limit_pool, market_snapshot, rank
from lib.options import option_codes, option_greeks, option_tquote
from lib.quote import quote_history, quote_realtime
from lib.replay_builder import build_replay, classify_market_regime, limit_sentiment
from lib.sector import sector
from render_replay_markdown import render_report


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / ".analysis"
CORE_ACCEPTANCE_PATH = (
    Path(__file__).resolve().parents[1] / "evals" / "core-acceptance-stocks.json"
)
ANALYSIS_LAYERS = ["facts", "signals", "judgment", "risks"]
HIGH_VOLATILITY_KEYWORDS = (
    "芯片",
    "半导体",
    "封装",
    "封测",
    "科创",
    "AI",
    "存储",
    "算力",
    "成长",
)
DEFENSIVE_KEYWORDS = ("银行", "电力", "高股息", "公用事业", "运营商")


def _resolve_output_path(output_path: str) -> Path:
    output = Path(output_path)
    if output.is_absolute():
        return output
    if output.parent == Path("."):
        return DEFAULT_OUTPUT_DIR / output.name
    return output


def _render_replay(input_path: str, output_path: str | None) -> dict:
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    markdown = render_report(payload)
    if output_path:
        output = _resolve_output_path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
    return success(
        "render_replay",
        {
            "input": input_path,
            "output": output_path,
            "markdown": markdown,
        },
        source_chain=[{"source": "render_replay_markdown", "ok": True}],
        warnings=[],
        trade_date=payload.get("trade_date"),
    )


def _load_core_acceptance_standard(symbol: str) -> dict | None:
    if not CORE_ACCEPTANCE_PATH.exists():
        return None
    try:
        payload = json.loads(CORE_ACCEPTANCE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    for entry in payload.get("stocks", []):
        if str(entry.get("symbol", "")).strip() == str(symbol).strip():
            return entry
    return None


def _read_path(data: object, path: str) -> object:
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current.get(part)
    return current


def _append_unique(target: list[str], text: str | None) -> None:
    value = str(text or "").strip()
    if value and value not in target:
        target.append(value)


def _unique_strings(items: list[str]) -> list[str]:
    unique: list[str] = []
    for item in items:
        _append_unique(unique, item)
    return unique


def _warning_domains(
    warnings: list[str], payload_data: dict, missing_fields: list[str]
) -> list[str]:
    text = " ".join(str(item) for item in warnings)
    domains: list[str] = []
    if "资金流" in text or any(
        field.startswith("money_flow") for field in missing_fields
    ):
        domains.append("flow")
    if "板块" in text or any(
        field.startswith("sector_membership") for field in missing_fields
    ):
        domains.append("sector")
    if "行情" in text or any(field.startswith("realtime") for field in missing_fields):
        domains.append("market")
    if (
        "估值" in text
        or "财务" in text
        or any(field.startswith("fundamental") for field in missing_fields)
    ):
        domains.append("fundamental")
    if payload_data.get("market_context") in (None, {}, []):
        return domains
    if "market_context" in missing_fields:
        domains.append("market")
    return _unique_strings(domains)


def _build_provenance(source_chain: list[dict]) -> dict:
    primary_sources = [
        str(item.get("source"))
        for item in source_chain
        if isinstance(item, dict) and item.get("ok") is True and item.get("source")
    ]
    fallback_sources = [
        str(item.get("source"))
        for item in source_chain
        if isinstance(item, dict) and item.get("ok") is False and item.get("source")
    ]
    if primary_sources and fallback_sources:
        mode = "mixed"
    elif fallback_sources:
        mode = "fallback"
    else:
        mode = "primary"
    return {
        "mode": mode,
        "primary_sources": _unique_strings(primary_sources),
        "fallback_sources": _unique_strings(fallback_sources),
    }


def _build_market_regime(payload_data: dict, warnings: list[str]) -> dict:
    regime = classify_market_regime(payload_data.get("market_context") or {})
    if not (payload_data.get("market_context") or {}).get("indexes"):
        regime["signals"] = _unique_strings([*regime.get("signals", []), *warnings[:2]])
    return regime


def _classify_stock_role(payload_data: dict) -> dict:
    sector_names = " ".join(
        str(item.get("板块名称", ""))
        for item in (payload_data.get("sector_membership") or [])
        if isinstance(item, dict)
    )
    pe = _read_path(payload_data, "fundamental.pe")
    pb = _read_path(payload_data, "fundamental.pb")
    if any(keyword in sector_names for keyword in HIGH_VOLATILITY_KEYWORDS) or (
        isinstance(pe, (int, float)) and float(pe) >= 60
    ):
        return {
            "bucket": "high_volatility",
            "summary": "所属方向偏高弹性，波动和预期回撤都更敏感。",
        }
    if any(keyword in sector_names for keyword in DEFENSIVE_KEYWORDS) or (
        isinstance(pb, (int, float)) and float(pb) <= 2
    ):
        return {
            "bucket": "defensive",
            "summary": "更偏防御或稳定器属性，不宜在非系统性回撤里优先处理。",
        }
    return {
        "bucket": "trend_following",
        "summary": "更接近趋势跟随品种，优先级取决于市场环境和板块承接。",
    }


def _build_action_priority(payload_data: dict, market_regime: dict) -> list[dict]:
    role = _classify_stock_role(payload_data)
    regime_label = market_regime.get("label")
    priority = 2
    action = "observe"
    if regime_label in {"systemic_weakness", "structural_rotation"}:
        if role["bucket"] == "high_volatility":
            priority = 1
            action = "reduce_first"
        elif role["bucket"] == "defensive":
            priority = 3
            action = "hold_if_not_broken"
    summary = f"{market_regime.get('summary', '')} {role['summary']}"
    return [
        {
            "symbol": payload_data.get("symbol"),
            "bucket": role["bucket"],
            "priority": priority,
            "action": action,
            "summary": summary.strip(),
        }
    ]


def _build_market_context(limit: int) -> tuple[dict, list[dict], list[str]]:
    source_chain: list[dict] = []
    warnings: list[str] = []

    snapshot_payload = market_snapshot()
    sentiment_payload = limit_sentiment(max(limit, 20))
    industry_rank_payload = sector("industry-rank", None, limit)
    concept_rank_payload = sector("concept-rank", None, limit)

    for payload in (
        snapshot_payload,
        sentiment_payload,
        industry_rank_payload,
        concept_rank_payload,
    ):
        _extend_chain(source_chain, payload)
        _extend_warnings(warnings, payload)

    industry_items = (industry_rank_payload.get("data") or {}).get("items") or []
    concept_items = (concept_rank_payload.get("data") or {}).get("items") or []
    leaders = [
        str(item.get("name", "")).strip()
        for item in industry_items
        if isinstance(item, dict)
        and isinstance(item.get("change_percent"), (int, float))
        and float(item.get("change_percent")) > 0
        and str(item.get("name", "")).strip()
    ]
    laggards = [
        str(item.get("name", "")).strip()
        for item in concept_items
        if isinstance(item, dict)
        and isinstance(item.get("change_percent"), (int, float))
        and float(item.get("change_percent")) < 0
        and str(item.get("name", "")).strip()
    ]

    context = {
        "indexes": (snapshot_payload.get("data") or {}).get("indexes") or [],
        "breadth": (snapshot_payload.get("data") or {}).get("breadth") or {},
        "limit_sentiment": sentiment_payload.get("data") or {},
        "sector_context": {
            "leaders": _unique_strings(leaders)[:2],
            "laggards": _unique_strings(laggards)[:2],
        },
    }
    return context, source_chain, warnings


def _build_confidence_label(
    warnings: list[str], missing_fields: list[str], source_chain: list[dict]
) -> str:
    if missing_fields or any(
        item.get("ok") is False for item in source_chain if isinstance(item, dict)
    ):
        return "low"
    if warnings:
        return "medium"
    return "high"


def _build_layered_analysis(
    symbol: str,
    payload_data: dict,
    source_chain: list[dict],
    warnings: list[str],
) -> dict:
    standard = _load_core_acceptance_standard(symbol)
    if not standard:
        return {
            "thesis": None,
            "facts": [],
            "signals": [],
            "judgment": [],
            "risks": [],
            "conclusion_tags": [],
            "source_trace": source_chain,
            "rational": True,
        }

    facts: list[str] = []
    signals: list[str] = []
    judgment: list[str] = []
    risks: list[str] = []
    thesis = str(standard.get("thesis", "")).strip() or None

    latest_price = _read_path(payload_data, "realtime.latest_price")
    if latest_price is not None:
        _append_unique(facts, f"最新价为 {latest_price}。")
    pb = _read_path(payload_data, "fundamental.pb")
    if pb is not None:
        _append_unique(facts, f"PB 为 {pb}。")
    pe = _read_path(payload_data, "fundamental.pe")
    if pe is not None:
        _append_unique(facts, f"PE 为 {pe}。")

    memberships = payload_data.get("sector_membership") or []
    sector_names = [
        str(item.get("板块名称")).strip()
        for item in memberships
        if isinstance(item, dict) and str(item.get("板块名称", "")).strip()
    ]
    if sector_names:
        _append_unique(facts, f"所属板块包括：{'、'.join(sector_names[:3])}。")

    flow_summary = _read_path(payload_data, "money_flow.summary")
    if isinstance(flow_summary, dict):
        status = str(flow_summary.get("status", "")).strip()
        note = str(flow_summary.get("note", "")).strip()
        main_net_inflow = flow_summary.get("main_net_inflow")
        window = flow_summary.get("window")
        if status:
            text = f"资金流摘要状态为 {status}。"
            if note:
                text = f"{text} 备注：{note}。"
            _append_unique(signals, text)
        elif isinstance(main_net_inflow, (int, float)):
            amount_yi = abs(float(main_net_inflow)) / 100000000
            if float(main_net_inflow) > 0:
                direction = "净流入"
                suffix = "说明短线资金承接仍在，但持续性还需继续确认。"
            elif float(main_net_inflow) < 0:
                direction = "净流出"
                suffix = "说明短线资金分歧仍在，回踩承接需要继续观察。"
            else:
                direction = "基本平衡"
                suffix = "说明短线资金暂未形成明确方向。"
            prefix = (
                f"近{int(window)}日主力资金"
                if isinstance(window, (int, float)) and int(window) > 0
                else "主力资金"
            )
            _append_unique(
                signals,
                f"资金流方面，{prefix}{direction}约 {amount_yi:.2f} 亿元，{suffix}",
            )
        elif flow_summary:
            _append_unique(signals, "资金流摘要已有返回，可与估值和题材信号交叉验证。")

    if thesis:
        _append_unique(signals, f"当前样本主题聚焦：{thesis}")

    news_titles = payload_data.get("news_titles") or []
    if news_titles:
        _append_unique(facts, f"新闻样本包括：{news_titles[0]}。")
        _append_unique(signals, f"新闻样本显示：{news_titles[0]}。")

    if _read_path(payload_data, "money_flow.summary") in (None, [], {}):
        _append_unique(
            signals, "资金流字段当前缺失，相关信号只能按公开源 warning 处理。"
        )

    for warning in warnings:
        _append_unique(signals, f"公开源提示：{warning}")
        _append_unique(risks, f"数据链路风险：{warning}")

    tags = [
        str(tag).strip()
        for tag in (standard.get("expected_conclusion_tags") or [])
        if str(tag).strip()
    ]
    if thesis:
        _append_unique(
            judgment, f"当前分析按“{thesis}”框架展开，仅使用已确认字段组织结论。"
        )
    if tags:
        _append_unique(judgment, f"结论标签聚焦：{'、'.join(tags)}。")
        _append_unique(signals, f"标签信号涉及：{'、'.join(tags)}。")
        _append_unique(risks, f"需要警惕 {tags[0]} 主线下的估值与预期波动。")

    if flow_summary not in (None, [], {}):
        _append_unique(
            risks, "资金流字段虽已返回，但若公开源持续波动，资金流判断仍可能失真。"
        )

    missing_fields = [
        field
        for field in (standard.get("required_fields") or [])
        if _read_path(payload_data, str(field)) in (None, [], {})
    ]
    provenance = _build_provenance(source_chain)
    degradation_flags = _warning_domains(warnings, payload_data, missing_fields)
    market_regime = _build_market_regime(payload_data, warnings)
    action_priority = _build_action_priority(payload_data, market_regime)
    confidence = _build_confidence_label(warnings, missing_fields, source_chain)
    if missing_fields:
        _append_unique(risks, f"仍缺少关键字段：{', '.join(missing_fields)}。")
    else:
        _append_unique(judgment, "核心验收要求的关键字段已覆盖，可继续做分层判断。")
        _append_unique(
            risks, "关键字段当前已覆盖，但后续若公开源波动，结论稳定性仍可能下降。"
        )

    for layer in ANALYSIS_LAYERS:
        if locals()[layer] == []:
            if layer == "facts":
                _append_unique(facts, "当前仅保留已确认字段，未补写不可验证信息。")
            elif layer == "signals":
                _append_unique(
                    signals, "暂无新增市场信号，维持对现有公开数据的克制解读。"
                )
            elif layer == "judgment":
                _append_unique(
                    judgment, "当前判断仅作为结构化整理，不外推超出数据边界的结论。"
                )
            elif layer == "risks":
                _append_unique(risks, "若后续公开源继续缺失，结论稳定性会下降。")

    return {
        "thesis": thesis,
        "facts": facts,
        "signals": signals,
        "judgment": judgment,
        "risks": risks,
        "conclusion_tags": tags,
        "source_trace": source_chain,
        "provenance": provenance,
        "degradation_flags": degradation_flags,
        "market_regime": market_regime,
        "action_priority": action_priority,
        "confidence": confidence,
        "warnings": _unique_strings(warnings),
        "rational": True,
    }


def _build_replay(trade_date: str | None, limit: int, output_path: str | None) -> dict:
    payload = build_replay(trade_date=trade_date, limit=limit)
    if output_path:
        output = _resolve_output_path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload["data"], ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return payload


def _extend_chain(target: list[dict], payload: dict) -> None:
    target.extend(payload.get("source_chain", []))


def _extend_warnings(target: list[str], payload: dict) -> None:
    for item in payload.get("warnings", []):
        text = str(item).strip()
        if text:
            target.append(text)


def _round_price(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 2)


def _format_price_range(lower: float | None, upper: float | None) -> str | None:
    if lower is None or upper is None:
        return None
    return f"{lower:.2f}-{upper:.2f}"


def _build_buy_plan(
    latest_price: float | None,
    latest_close: float | None,
    recent_low: float | None,
    recent_high: float | None,
) -> dict:
    if None in (latest_price, latest_close, recent_low, recent_high):
        return {
            "stance": "insufficient_data",
            "trial_zone": {
                "range": None,
                "reason": "行情关键位不足，暂时无法生成买点区间。",
            },
            "buy_on_dip_zone": {
                "range": None,
                "reason": "缺少完整的最新价、收盘价或区间高低点。",
            },
            "pressure_levels": [],
            "stop_loss_note": "缺少关键行情数据，暂不提供止损参考。",
            "summary": "行情关键位不足，暂时无法给出可靠的试错区、低吸区和压力位结论。",
        }

    price_span = max(recent_high - recent_low, 0.01)
    trial_lower = _round_price(max(recent_low, latest_close - price_span * 0.1))
    trial_upper = _round_price(max(trial_lower, latest_close))
    dip_lower = _round_price(recent_low)
    dip_upper = _round_price(min(recent_high, recent_low + price_span * 0.1))
    first_pressure = _round_price(min(recent_high, latest_close + price_span * 0.1))
    second_pressure = _round_price(recent_high)

    position_ratio = (latest_price - recent_low) / price_span
    if position_ratio >= 0.8:
        stance = "avoid_chasing"
        trial_reason = "当前价已接近最近区间高位，追价性价比偏低，更适合等回踩。"
    elif position_ratio <= 0.35:
        stance = "try"
        trial_reason = "当前价已靠近短线支撑一侧，可用小仓位先试错。"
    else:
        stance = "wait"
        trial_reason = "当前价处于区间中段，追击和抄底都不占优，更适合等回踩确认。"

    stop_loss_note = (
        f"若有效跌破 {recent_low:.2f} 一带，说明短线支撑失守，应降低仓位或暂停试错。"
    )
    pressure_note = f"先留意 {first_pressure:.2f} 附近压力。"
    dip_range = _format_price_range(dip_lower, dip_upper)
    trial_range = _format_price_range(trial_lower, trial_upper)
    if stance == "try":
        summary = (
            f"当前更适合在 {trial_range} 一带小仓试错，若回踩到 {dip_range} 可继续观察低吸，"
            f"{pressure_note}{stop_loss_note}"
        )
    elif stance == "wait":
        summary = (
            f"当前更适合等待回踩到 {dip_range} 一带再确认，不建议在区间中段追价，"
            f"{pressure_note}{stop_loss_note}"
        )
    else:
        summary = (
            f"当前已接近区间高位，不建议追高，优先等回踩到 {dip_range} 一带再观察，"
            f"{pressure_note}{stop_loss_note}"
        )

    return {
        "stance": stance,
        "trial_zone": {
            "range": trial_range,
            "reason": trial_reason,
        },
        "buy_on_dip_zone": {
            "range": dip_range,
            "reason": "更贴近最近窗口低点，若缩量回踩不破，适合作为低吸观察区。",
        },
        "pressure_levels": [
            {
                "price": first_pressure,
                "reason": "接近最新收盘上方的第一道短线反压位，容易出现抛压。",
            },
            {
                "price": second_pressure,
                "reason": "最近窗口高点，若不能有效突破，通常仍按强压力位处理。",
            },
        ],
        "stop_loss_note": stop_loss_note,
        "summary": summary,
    }


def stock_diagnose(symbol: str, limit: int = 20) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []

    realtime_payload = quote_realtime(symbol)
    history_payload = quote_history(symbol, "day", "qfq", max(limit, 20))
    flow_payload = money_flow("stock", symbol, limit)
    sector_payload = sector("stock-membership", symbol, limit)
    fundamental_payload = fundamental(symbol)
    news_payload = news(symbol, limit)
    market_context, market_chain, market_warnings = _build_market_context(limit)

    for payload in (
        realtime_payload,
        history_payload,
        flow_payload,
        sector_payload,
        fundamental_payload,
        news_payload,
    ):
        _extend_chain(source_chain, payload)
        _extend_warnings(warnings, payload)
    source_chain.extend(market_chain)
    warnings.extend(market_warnings)

    realtime_data = realtime_payload.get("data") or {}
    history_data = history_payload.get("data") or {}
    flow_data = flow_payload.get("data") or {}
    sector_data = sector_payload.get("data") or {}
    fundamental_data = fundamental_payload.get("data") or {}
    news_items = (news_payload.get("data") or {}).get("items") or []
    candles = history_data.get("candles") or []
    recent_window = candles[-min(len(candles), max(2, limit)) :]

    recent_high = None
    recent_low = None
    if recent_window:
        highs = [
            item.get("high") for item in recent_window if item.get("high") is not None
        ]
        lows = [
            item.get("low") for item in recent_window if item.get("low") is not None
        ]
        recent_high = max(highs) if highs else None
        recent_low = min(lows) if lows else None

    latest_price = realtime_data.get("latest_price")
    latest_close = (history_data.get("latest_snapshot") or {}).get("close")
    buy_plan = _build_buy_plan(latest_price, latest_close, recent_low, recent_high)
    result_data = {
        "symbol": str(
            realtime_data.get("symbol") or fundamental_data.get("symbol") or symbol
        ),
        "name": realtime_data.get("name") or fundamental_data.get("name"),
        "realtime": realtime_data,
        "history": history_data,
        "support_resistance": {
            "recent_low": recent_low,
            "recent_high": recent_high,
            "latest_close": latest_close,
        },
        "buy_plan": buy_plan,
        "money_flow": flow_data,
        "sector_membership": sector_data.get("items") or [],
        "fundamental": fundamental_data,
        "market_context": market_context,
        "news_titles": [
            str(item.get("title")).strip()
            for item in news_items
            if isinstance(item, dict) and str(item.get("title", "")).strip()
        ][: min(limit, 5)],
    }
    result_data["analysis"] = _build_layered_analysis(
        result_data["symbol"], result_data, source_chain, warnings
    )

    return success(
        "stock_diagnose",
        result_data,
        source_chain,
        warnings,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="stock-replay-workbench unified CLI")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    realtime = subparsers.add_parser("quote-realtime", help="Fetch realtime quote")
    realtime.add_argument("--symbol", required=True, help="A-share symbol, e.g. 600519")

    history = subparsers.add_parser("quote-history", help="Fetch history quote")
    history.add_argument("--symbol", required=True)
    history.add_argument("--period", default="day", choices=["day", "week", "month"])
    history.add_argument("--adjust", default="qfq", choices=["qfq", "hfq", "none"])
    history.add_argument("--limit", default=60, type=int)

    diagnose = subparsers.add_parser(
        "stock-diagnose", help="Aggregate quote, flow, sector, fundamental, and news"
    )
    diagnose.add_argument("--symbol", required=True)
    diagnose.add_argument("--limit", default=20, type=int)

    subparsers.add_parser("market-snapshot", help="Fetch market snapshot")

    rank_parser = subparsers.add_parser("rank", help="Fetch market rank list")
    rank_parser.add_argument(
        "--kind",
        default="change_percent",
        choices=["change_percent", "turnover", "amount", "volume"],
    )
    rank_parser.add_argument("--limit", default=20, type=int)

    pool_parser = subparsers.add_parser("limit-pool", help="Fetch limit pool")
    pool_parser.add_argument(
        "--pool", default="up", choices=["up", "down", "break", "yesterday-up"]
    )
    pool_parser.add_argument("--limit", default=20, type=int)

    limit_sentiment_parser = subparsers.add_parser(
        "limit-sentiment", help="Fetch limit-up sentiment summary"
    )
    limit_sentiment_parser.add_argument("--limit", default=50, type=int)

    sector_parser = subparsers.add_parser("sector", help="Fetch sector info")
    sector_parser.add_argument(
        "--action",
        default="industry-rank",
        choices=["industry-rank", "concept-rank", "stock-membership"],
    )
    sector_parser.add_argument("--symbol")
    sector_parser.add_argument("--limit", default=20, type=int)

    flow_parser = subparsers.add_parser("money-flow", help="Fetch money flow")
    flow_parser.add_argument(
        "--scope",
        default="market",
        choices=["market", "stock", "industry", "concept"],
    )
    flow_parser.add_argument("--symbol")
    flow_parser.add_argument("--limit", default=20, type=int)

    fundamental_parser = subparsers.add_parser("fundamental", help="Fetch fundamentals")
    fundamental_parser.add_argument("--symbol", required=True)

    announcement_parser = subparsers.add_parser(
        "announcement", help="Fetch announcements"
    )
    announcement_parser.add_argument("--symbol")
    announcement_parser.add_argument("--keyword")
    announcement_parser.add_argument("--limit", default=20, type=int)

    news_parser = subparsers.add_parser("news", help="Fetch news")
    news_parser.add_argument("--symbol")
    news_parser.add_argument("--limit", default=20, type=int)

    dragon_parser = subparsers.add_parser(
        "dragon-tiger", help="Fetch dragon tiger list"
    )
    dragon_parser.add_argument("--symbol")
    dragon_parser.add_argument("--trade-date")
    dragon_parser.add_argument("--limit", default=20, type=int)

    block_parser = subparsers.add_parser("block-trade", help="Fetch block trades")
    block_parser.add_argument("--symbol")
    block_parser.add_argument("--trade-date")
    block_parser.add_argument("--limit", default=20, type=int)

    margin_parser = subparsers.add_parser("margin-trading", help="Fetch margin trading")
    margin_parser.add_argument("--symbol")
    margin_parser.add_argument("--trade-date")
    margin_parser.add_argument("--limit", default=20, type=int)

    sentiment_heat_parser = subparsers.add_parser(
        "sentiment-heat", help="Fetch sentiment heat summary"
    )
    sentiment_heat_parser.add_argument("--limit", default=20, type=int)

    irm_parser = subparsers.add_parser("irm-qa", help="Fetch investor relation Q&A")
    irm_parser.add_argument("--symbol", required=True)
    irm_parser.add_argument("--limit", default=20, type=int)

    option_codes_parser = subparsers.add_parser(
        "option-codes", help="Fetch ETF option contract codes"
    )
    option_codes_parser.add_argument("--underlying", default="510050")

    option_tquote_parser = subparsers.add_parser(
        "option-tquote", help="Fetch ETF option T-quote"
    )
    option_tquote_parser.add_argument("--code", required=True)

    option_greeks_parser = subparsers.add_parser(
        "option-greeks", help="Fetch ETF option greeks and IV"
    )
    option_greeks_parser.add_argument("--code", required=True)

    bond_parser = subparsers.add_parser("bond", help="Fetch bond data")
    bond_parser.add_argument(
        "--action", default="realtime", choices=["realtime", "rank", "history"]
    )
    bond_parser.add_argument("--symbol")
    bond_parser.add_argument("--limit", default=20, type=int)

    replay_parser = subparsers.add_parser(
        "render-replay", help="Render replay markdown"
    )
    replay_parser.add_argument("--input", required=True)
    replay_parser.add_argument(
        "--output",
        help=(
            "Optional markdown output path. Relative paths are written under "
            "./.analysis/"
        ),
    )

    build_replay_parser = subparsers.add_parser(
        "build-replay", help="Build replay draft JSON"
    )
    build_replay_parser.add_argument("--trade-date")
    build_replay_parser.add_argument("--limit", default=5, type=int)
    build_replay_parser.add_argument(
        "--output",
        help=(
            "Optional JSON output path. Relative paths are written under ./.analysis/"
        ),
    )

    return parser


def dispatch(args: argparse.Namespace) -> dict:
    if args.subcommand == "quote-realtime":
        return quote_realtime(args.symbol)
    if args.subcommand == "quote-history":
        return quote_history(args.symbol, args.period, args.adjust, args.limit)
    if args.subcommand == "stock-diagnose":
        return stock_diagnose(args.symbol, args.limit)
    if args.subcommand == "market-snapshot":
        return market_snapshot()
    if args.subcommand == "rank":
        return rank(args.kind, args.limit)
    if args.subcommand == "limit-pool":
        return limit_pool(args.pool, args.limit)
    if args.subcommand == "limit-sentiment":
        return limit_sentiment(args.limit)
    if args.subcommand == "sector":
        return sector(args.action, args.symbol, args.limit)
    if args.subcommand == "money-flow":
        return money_flow(args.scope, args.symbol, args.limit)
    if args.subcommand == "fundamental":
        return fundamental(args.symbol)
    if args.subcommand == "announcement":
        return announcement(args.symbol, args.keyword, args.limit)
    if args.subcommand == "news":
        return news(args.symbol, args.limit)
    if args.subcommand == "dragon-tiger":
        return dragon_tiger(args.symbol, args.trade_date, args.limit)
    if args.subcommand == "block-trade":
        return block_trade(args.symbol, args.trade_date, args.limit)
    if args.subcommand == "margin-trading":
        return margin_trading(args.symbol, args.trade_date, args.limit)
    if args.subcommand == "sentiment-heat":
        return sentiment_heat(args.limit)
    if args.subcommand == "irm-qa":
        return irm_qa(args.symbol, args.limit)
    if args.subcommand == "option-codes":
        return option_codes(args.underlying)
    if args.subcommand == "option-tquote":
        return option_tquote(args.code)
    if args.subcommand == "option-greeks":
        return option_greeks(args.code)
    if args.subcommand == "bond":
        return bond(args.action, args.symbol, args.limit)
    if args.subcommand == "render-replay":
        return _render_replay(args.input, args.output)
    if args.subcommand == "build-replay":
        return _build_replay(args.trade_date, args.limit, args.output)
    return failure(
        "unknown", "UnknownCommand", f"Unsupported subcommand: {args.subcommand}"
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    payload = dispatch(args)
    emit(payload)
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
