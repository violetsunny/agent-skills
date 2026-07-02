# AGENTS.md

## What this is

**Core project of this repo.** A-share post-market replay and structured analysis workbench (v0.3.0). Unified CLI for 15+ subcommands covering market data, limit-up sentiment (涨停/炸板/跌停/昨涨停四池 + 连板分析), capital flow, events, sectors, financials, ETF options (T型报价 + 希腊字母 + IV), IRM Q&A, and derivatives.

## Commands

```bash
python3 stock-replay-workbench/scripts/stock_replay_cli.py <subcommand> [...args]

# Key subcommands
build-replay     # assemble replay draft JSON
render-replay    # render structured JSON to Markdown report
quote-realtime   # single-stock real-time quote
quote-history    # single-stock history
market-snapshot  # index snapshot + market breadth
rank             # market-wide rankings
limit-pool       # limit-up/down/broken pools
sector           # industry/concept rankings, stock block membership
money-flow       # market/stock/industry/concept fund flow
fundamental      # valuation, ROE, gross margin, cashflow summary
```

## Core workflow

```bash
# Generate replay draft, then render
python3 stock-replay-workbench/scripts/stock_replay_cli.py build-replay --limit 3 --output analysis/YYYY-MM-DD-A股复盘.json
python3 stock-replay-workbench/scripts/stock_replay_cli.py render-replay --input analysis/YYYY-MM-DD-A股复盘.json --output analysis/YYYY-MM-DD-A股复盘.md
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
python3 stock-replay-workbench/scripts/validate_skill.py
uv run pytest tests/test_stock_replay_workbench.py -q
```

## Key constraints

- Never ask for API keys or paid credentials.
- Eastmoney only for unique fields; serial calls, ≥1s interval + random jitter (via `em_get()`).
- mootdx must use `tdx_client()` helper (BESTIP empty-string crash fix); K-line param name is `frequency` (not `category`).
- Limit-up pools: price fields must be ÷1000.
- Output must separate fact, signal, judgment, risk.
- Reports auto-save to `analysis/` (gitignored).
- Reference docs: `references/capability-registry.md`, `references/query-contracts.md`, `references/source-playbook.md`, `references/screening-playbook.md`, `references/replay-template.md`.
