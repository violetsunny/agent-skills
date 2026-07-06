# AGENTS.md

## What this is

**Independent skill project.** A-share post-market replay and structured analysis workbench (v0.3.0). Unified CLI for 19 subcommands covering market data, limit-up sentiment (当前已接入涨停/炸板/跌停/昨涨停四池 + 连板分析), capital flow, events, sectors, financials, ETF options (T 型报价 + 希腊字母 + IV), IRM Q&A, and derivatives.

## Current target

This project must become a **fully independent stock skill project**.

- Every capability promised by `SKILL.md` should eventually be implemented inside this directory.
- The preferred landing zone is local code under `scripts/lib/` plus a routed subcommand in `scripts/stock_replay_cli.py`.
- Sibling projects are references only. They must not become runtime dependencies for the workbench.
- Do not satisfy missing CLI coverage by shelling out to sibling projects or importing them directly.

## User-set preferences

- Prefer minimal independent transplantation and adaptation over wrappers.
- When `SKILL.md` promises a capability, bias toward implementing the local CLI rather than shrinking the promise.
- Keep project context and `AGENTS.md` aligned with the active build target before large implementation work.
- Analysis results must be written to the current skill project's root `./.analysis/` directory. If `.analysis/` does not exist, create it first.

## Commands

```bash
python3 scripts/stock_replay_cli.py <subcommand> [...args]

# Key subcommands
build-replay     # assemble replay draft JSON
render-replay    # render structured JSON to Markdown report
quote-realtime   # single-stock real-time quote
quote-history    # single-stock history
market-snapshot  # index snapshot + market breadth
rank             # market-wide rankings
limit-pool       # up/down/break/yesterday-up pools
limit-sentiment  # board-trading sentiment summary
sentiment-heat   # market heat summary
sector           # industry/concept rankings, stock block membership
money-flow       # market/stock/industry/concept fund flow
fundamental      # valuation, ROE, gross margin, cashflow summary
announcement     # disclosure list lookup
news             # stock or market news
dragon-tiger     # dragon tiger details
block-trade      # block trade records
margin-trading   # margin trading records
irm-qa           # investor relation Q&A
option-codes     # ETF option contract codes
option-tquote    # ETF option T-quote
option-greeks    # ETF option greeks and IV
bond             # convertible bond data
```

## Core workflow

```bash
# Generate replay draft, then render
python3 scripts/stock_replay_cli.py build-replay --limit 3 --output .analysis/YYYY-MM-DD-A股复盘.json
python3 scripts/stock_replay_cli.py render-replay --input .analysis/YYYY-MM-DD-A股复盘.json --output .analysis/YYYY-MM-DD-A股复盘.md
```

## Task routing (do this first)

| Type | Triggers | Approach |
|------|----------|----------|
| 快查 | `茅台最新价` | Direct API call |
| 深度分析 | `为什么强` | Build draft → supplement 3+ data domains |
| 短线筛选 | `找强势股` | Read `references/screening-playbook.md` → hard filter |
| 盘后复盘 | `复盘今天` | Read `references/replay-template.md` → build-replay + render-replay |

## Validation

```bash
python3 scripts/validate_skill.py
uv run pytest tests/test_stock_replay_workbench.py -q
```

## Key constraints

- Never ask for API keys or paid credentials.
- Eastmoney only for unique fields; serial calls, ≥1s interval + random jitter (via `em_get()`).
- mootdx must use `tdx_client()` helper (BESTIP empty-string crash fix); K-line param name is `frequency` (not `category`).
- Limit-up pools: price fields must be ÷1000.
- Output must separate fact, signal, judgment, risk.
- Persist generated analysis and replay artifacts under the current project root `.analysis/` directory; create the directory if missing.
- Reference projects can inform design, but the executable result must live in this project.
- Reference docs: `references/capability-registry.md`, `references/query-contracts.md`, `references/source-playbook.md`, `references/screening-playbook.md`, `references/replay-template.md`.
