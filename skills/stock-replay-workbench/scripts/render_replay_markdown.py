#!/usr/bin/env python3
"""Render a replay markdown report from structured JSON.

Input JSON example:
{
  "trade_date": "2026-06-26",
  "summary": "市场缩量分化，主线集中在 AI 硬件与消费电子。",
  "market_overview": [
    {"metric": "上证指数", "value": "+0.31%", "comment": "震荡收红"}
  ],
  "themes": {
    "main": ["AI 硬件", "消费电子"],
    "secondary": ["机器人"],
    "sentiment": "涨停家数尚可，但炸板率偏高",
    "divergence": "高位股午后分歧加大"
  },
  "sectors": [
    {"name": "消费电子", "performance": "强", "leaders": "立讯精密", "catalyst": "苹果链催化"}
  ],
  "leaders": [
    {"symbol": "300750", "status": "震荡走强", "fact": "成交额居前", "role": "中军"}
  ],
  "capital_and_events": {
    "capital": ["主力净流入集中在 AI 硬件"],
    "special": ["龙虎榜机构净买入偏向消费电子"],
    "catalysts": ["多家公司披露订单与回购进展"]
  },
  "watchlist": ["观察 AI 硬件是否继续扩散"],
  "risks": ["高位股分歧可能继续扩大"],
  "source_chain": ["freestocklineskill smart-query", "腾讯财经", "东方财富"],
  "timestamp": "2026-06-26 15:12:00",
  "warnings": ["部分资金流字段为 best-effort"]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _format_number(value, digits: int = 2) -> str:
    if value in (None, "", "-", "--"):
        return "-"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:,.{digits}f}"
    return str(value)


def _format_percent(value) -> str:
    if value in (None, "", "-", "--"):
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:.2f}%"
    return str(value)


def _table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "|" + "|".join(["---"] * len(headers)) + "|"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, sep_line, *body])


def _normalized_event_text_variants(text: str) -> set[str]:
    value = text.strip()
    variants = {value}
    trimmed = value.rstrip("。；;:：")
    if trimmed:
        variants.add(trimmed)
    prefix = "："
    if prefix in trimmed:
        variants.add(trimmed.split(prefix, 1)[1].strip())
    ascii_prefix = ":"
    if ascii_prefix in trimmed:
        variants.add(trimmed.split(ascii_prefix, 1)[1].strip())

    expanded = set(variants)
    for item in list(variants):
        for separator in ("；", ";"):
            if separator not in item:
                continue
            for part in item.split(separator):
                piece = part.strip().rstrip("。；;:：")
                if piece:
                    expanded.add(piece)
    return {item for item in expanded if item}


def _collect_event_texts(bucket: dict | None) -> list[str]:
    if not isinstance(bucket, dict):
        return []

    texts: list[str] = []
    seen: set[str] = set()
    for item in _ensure_list(bucket.get("summary")):
        text = str(item).strip()
        variants = _normalized_event_text_variants(text)
        if text and not (variants & seen):
            seen.update(variants)
            texts.append(text)

    for item in _ensure_list(bucket.get("evidence")):
        if isinstance(item, dict):
            for key in ("title", "名称", "证券简称"):
                value = str(item.get(key, "")).strip()
                variants = _normalized_event_text_variants(value)
                if value and not (variants & seen):
                    seen.update(variants)
                    texts.append(value)
                    break
        else:
            text = str(item).strip()
            variants = _normalized_event_text_variants(text)
            if text and not (variants & seen):
                seen.update(variants)
                texts.append(text)
    return texts


def _dedupe_event_texts(items: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = str(item).strip()
        variants = _normalized_event_text_variants(text)
        if text and not (variants & seen):
            seen.update(variants)
            deduped.append(text)
    return deduped


def _format_security_label(name, symbol) -> str:
    name_text = str(name or "").strip()
    symbol_text = str(symbol or "").strip()
    if name_text and symbol_text:
        return f"{name_text}({symbol_text})"
    return name_text or symbol_text or "-"


def _split_labelled_event_text(text: str) -> tuple[str, str]:
    value = str(text or "").strip()
    if "：" not in value:
        return "", value
    label, content = value.split("：", 1)
    return label.strip(), content.strip()


def render_report(payload: dict) -> str:
    trade_date = payload.get("trade_date", "未知交易日")
    summary = payload.get("summary", "暂无总结")

    lines = [f"## {trade_date} A股复盘", "", "### 一句话结论", summary, ""]

    overview_rows = []
    for item in payload.get("market_overview", []):
        overview_rows.append(
            [
                str(item.get("metric", "")),
                str(item.get("value", "")),
                str(item.get("comment", "")),
            ]
        )
    if overview_rows:
        lines.extend(
            ["### 市场总览", _table(["指标", "数值", "说明"], overview_rows), ""]
        )

    themes = payload.get("themes", {})
    if themes:
        lines.extend(
            [
                "### 主线与情绪",
                f"- 主线题材: {', '.join(_ensure_list(themes.get('main'))) or '暂无'}",
                f"- 次主线: {', '.join(_ensure_list(themes.get('secondary'))) or '暂无'}",
                f"- 情绪强度: {themes.get('sentiment', '暂无')}",
                f"- 退潮或分歧点: {themes.get('divergence', '暂无')}",
                "",
            ]
        )

    market_regime = payload.get("market_regime") or {}
    if market_regime:
        lines.append("### 市场结构判断")
        lines.append(f"- Regime: {market_regime.get('label', 'unknown')}")
        lines.append(f"- 结论: {market_regime.get('summary', '暂无')}")
        for item in _ensure_list(market_regime.get("signals")):
            lines.append(f"- 信号: {item}")
        lines.append("")

    limit_sentiment = payload.get("limit_sentiment")
    if isinstance(limit_sentiment, dict) and limit_sentiment:
        lines.extend(
            [
                "### 打板情绪",
                f"- 涨停家数: {_format_number(limit_sentiment.get('up_count'), 0)}",
                f"- 炸板家数: {_format_number(limit_sentiment.get('break_count'), 0)}",
                f"- 跌停家数: {_format_number(limit_sentiment.get('down_count'), 0)}",
                f"- 昨涨停家数: {_format_number(limit_sentiment.get('yesterday_up_count'), 0)}",
                f"- 炸板率: {_format_percent(limit_sentiment.get('break_rate'))}",
                f"- 昨涨停晋级率: {_format_percent(limit_sentiment.get('advance_rate'))}",
                f"- 昨涨停赚钱效应: {_format_percent(limit_sentiment.get('earning_rate'))}",
                f"- 连板高度: {_format_number(limit_sentiment.get('max_height'), 0)}",
                "",
            ]
        )

    sector_rows = []
    for item in payload.get("sectors", []):
        sector_rows.append(
            [
                str(item.get("name", "")),
                str(item.get("performance", "")),
                str(item.get("leaders", "")),
                str(item.get("catalyst", "")),
            ]
        )
    if sector_rows:
        lines.extend(
            [
                "### 关键板块",
                _table(["板块", "表现", "领涨股", "资金/事件催化"], sector_rows),
                "",
            ]
        )

    sector_money_flow = payload.get("sector_money_flow", {})
    industry_flow = _ensure_list(sector_money_flow.get("industry"))
    concept_flow = _ensure_list(sector_money_flow.get("concept"))
    flow_rows = []
    for scope, items in (("行业", industry_flow), ("概念", concept_flow)):
        for item in items:
            if not isinstance(item, dict):
                continue
            flow_rows.append(
                [
                    scope,
                    str(item.get("name", "")),
                    _format_percent(item.get("change_percent")),
                    _format_number(item.get("main_net_inflow")),
                    _format_percent(item.get("main_net_inflow_percent")),
                    str(item.get("leader", "-") or "-"),
                ]
            )
    if flow_rows:
        lines.extend(
            [
                "### 板块资金流",
                _table(
                    ["类型", "板块", "涨跌幅", "主力净流入", "净占比", "代表股"],
                    flow_rows,
                ),
                "",
            ]
        )

    leader_rows = []
    for item in payload.get("leaders", []):
        leader_rows.append(
            [
                str(item.get("symbol", "")),
                str(item.get("status", "")),
                str(item.get("fact", "")),
                str(item.get("role", "")),
            ]
        )
    if leader_rows:
        lines.extend(
            [
                "### 强势股与关键个股",
                _table(["标的", "状态", "关键事实", "角色判断"], leader_rows),
                "",
            ]
        )

    fundamental_rows = []
    for item in _ensure_list(payload.get("fundamental_snapshots")):
        if not isinstance(item, dict):
            continue
        fundamental_rows.append(
            [
                _format_security_label(item.get("name"), item.get("symbol")),
                f"PE {_format_number(item.get('pe'))} / PB {_format_number(item.get('pb'))}",
                f"ROE {_format_percent(item.get('roe'))} / 毛利率 {_format_percent(item.get('gross_margin'))}",
                (
                    f"营收 {_format_number(item.get('revenue'))} / 净利 {_format_number(item.get('net_profit'))}"
                    f" / 资产负债率 {_format_percent(item.get('asset_liability_ratio'))}"
                    f" / 净利率 {_format_percent(item.get('net_margin'))}"
                    f" / 每股净资产 {_format_number(item.get('book_value_per_share'))}"
                ),
            ]
        )
    if fundamental_rows:
        lines.extend(
            [
                "### 重点标的基本面",
                _table(["标的", "估值", "盈利能力", "财务摘要"], fundamental_rows),
                "",
            ]
        )

    event_snapshots = payload.get("event_snapshots", {})
    market_events = (
        event_snapshots.get("market", {}) if isinstance(event_snapshots, dict) else {}
    )
    market_event_lines = []
    for key in ("announcements", "news", "dragon_tiger", "margin_trading"):
        market_event_lines.extend(_collect_event_texts(market_events.get(key)))
    market_event_lines = _dedupe_event_texts(market_event_lines)
    if market_event_lines:
        lines.append("### 事件快照")
        for item in market_event_lines:
            lines.append(f"- {item}")
        lines.append("")

    focus_events = (
        event_snapshots.get("focus", []) if isinstance(event_snapshots, dict) else []
    )
    focus_sections = []
    focus_catalyst_variants: set[str] = set()
    for item in _ensure_list(focus_events):
        if not isinstance(item, dict):
            continue
        focus_name = str(item.get("name") or item.get("symbol") or "重点股").strip()
        focus_lines = []
        for key in ("announcements", "news", "dragon_tiger", "margin_trading"):
            focus_lines.extend(_collect_event_texts(item.get(key)))
        focus_lines = _dedupe_event_texts(focus_lines)
        if focus_lines:
            for focus_line in focus_lines:
                focus_catalyst_variants.update(
                    _normalized_event_text_variants(focus_line)
                )
            focus_sections.append((focus_name, focus_lines))
    if focus_sections:
        lines.append("### 重点股事件催化")
        for focus_name, focus_lines in focus_sections:
            lines.append(f"- {focus_name}: {'；'.join(focus_lines)}")
        lines.append("")

    cap = payload.get("capital_and_events", {})
    if cap:
        lines.append("### 资金与事件")
        for item in _ensure_list(cap.get("capital")):
            lines.append(f"- 资金面: {item}")
        for item in _ensure_list(cap.get("special")):
            lines.append(f"- 龙虎榜/大宗/两融: {item}")
        for item in _ensure_list(cap.get("catalysts")):
            _, content = _split_labelled_event_text(item)
            if _normalized_event_text_variants(content) & focus_catalyst_variants:
                continue
            lines.append(f"- 公告/新闻/研报催化: {item}")
        lines.append("")

    watchlist = _ensure_list(payload.get("watchlist"))
    if watchlist:
        lines.append("### 明日观察点")
        for idx, item in enumerate(watchlist, 1):
            lines.append(f"{idx}. {item}")
        lines.append("")

    risks = _ensure_list(payload.get("risks"))
    if risks:
        lines.append("### 风险提示")
        for item in risks:
            lines.append(f"- {item}")
        lines.append("")

    disclaimers = _ensure_list(payload.get("disclaimers"))
    if disclaimers:
        lines.append("### 免责声明")
        for item in disclaimers:
            lines.append(f"- {item}")
        lines.append("")

    provenance = payload.get("analysis_provenance") or {}
    if provenance:
        lines.append("### 数据来源与降级说明")
        lines.append(f"- 来源模式: {provenance.get('mode', 'unknown')}")
        primary_sources = (
            ", ".join(_ensure_list(provenance.get("primary_sources"))) or "无"
        )
        fallback_sources = (
            ", ".join(_ensure_list(provenance.get("fallback_sources"))) or "无"
        )
        degradation_flags = (
            ", ".join(_ensure_list(provenance.get("degradation_flags"))) or "无"
        )
        lines.append(f"- 主源: {primary_sources}")
        lines.append(f"- 回退源: {fallback_sources}")
        lines.append(f"- 降级域: {degradation_flags}")
        lines.append("")

    source_chain = payload.get("source_chain", [])
    warnings = payload.get("warnings", [])
    lines.extend(
        [
            f"> 数据来源: {', '.join(_ensure_list(source_chain)) or '未提供'}",
            f"> 数据时间: {payload.get('timestamp', '未提供')}",
            f"> Warnings: {'; '.join(_ensure_list(warnings)) or '无'}",
            f"> Confidence: {payload.get('confidence', '未评定')}",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render replay markdown from JSON")
    parser.add_argument("--input", required=True, help="Path to replay JSON payload")
    parser.add_argument(
        "--output",
        help="Optional output markdown path. Missing parent directories are created automatically",
    )
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    markdown = render_report(payload)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
