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
from lib.market import limit_pool, market_snapshot, rank
from lib.quote import quote_history, quote_realtime
from lib.replay_builder import build_replay
from lib.sector import sector
from render_replay_markdown import render_report


def _render_replay(input_path: str, output_path: str | None) -> dict:
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    markdown = render_report(payload)
    if output_path:
        Path(output_path).write_text(markdown, encoding="utf-8")
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


def _build_replay(trade_date: str | None, limit: int, output_path: str | None) -> dict:
    payload = build_replay(trade_date=trade_date, limit=limit)
    if output_path:
        Path(output_path).write_text(
            json.dumps(payload["data"], ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return payload


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

    subparsers.add_parser("market-snapshot", help="Fetch market snapshot")

    rank_parser = subparsers.add_parser("rank", help="Fetch market rank list")
    rank_parser.add_argument(
        "--kind",
        default="change_percent",
        choices=["change_percent", "turnover", "amount", "volume"],
    )
    rank_parser.add_argument("--limit", default=20, type=int)

    pool_parser = subparsers.add_parser("limit-pool", help="Fetch limit pool")
    pool_parser.add_argument("--pool", default="up", choices=["up", "down", "break"])
    pool_parser.add_argument("--limit", default=20, type=int)

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
    replay_parser.add_argument("--output")

    build_replay_parser = subparsers.add_parser(
        "build-replay", help="Build replay draft JSON"
    )
    build_replay_parser.add_argument("--trade-date")
    build_replay_parser.add_argument("--limit", default=5, type=int)
    build_replay_parser.add_argument("--output")

    return parser


def dispatch(args: argparse.Namespace) -> dict:
    if args.subcommand == "quote-realtime":
        return quote_realtime(args.symbol)
    if args.subcommand == "quote-history":
        return quote_history(args.symbol, args.period, args.adjust, args.limit)
    if args.subcommand == "market-snapshot":
        return market_snapshot()
    if args.subcommand == "rank":
        return rank(args.kind, args.limit)
    if args.subcommand == "limit-pool":
        return limit_pool(args.pool, args.limit)
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
