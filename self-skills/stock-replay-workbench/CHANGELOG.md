# Changelog

## v0.4.1 - 2026-09-10

### Added

- 资金流备胎链（2026-09-10 东财 push2 对住宅 IP 间歇风控、akshare RemoteDisconnected 场景实测通过）：
  - `money-flow --scope market`：akshare 失败后直连东财 push2his 沪深两市资金流日K（`secid=1.000001&secid2=0.399001`，走 `em_get` 限流重试）。
  - `money-flow --scope industry/concept`：akshare 失败后直连东财 push2delay clist 板块资金流（按 f62 主力净额降序，leader 口径为领涨股并加 source_note），再失败才回退板块排行信号。
  - `money-flow --scope stock`：东财明细 → 东财排行 → akshare 之后新增新浪 `MoneyFlow.ssl_qsfx_zjlrqs` 日度备胎（独立风控面；主力=netamount、超大单=r0_net，占比由小数口径×100，无大/中/小单分档）。
- `margin-trading` 交易所官方备胎：akshare 失败或空返回时回退上交所 `queryMargin.do` + 深交所 `1837_xxpl` xlsx（金额单位元、上交所融券余额源值为空保留为空）；当日未发布自动回退最近可用交易日（最多 7 天）；单所有数据时 warning「不代表沪深全市场」。
- 新增 4 个离线单测：新浪备胎解析（含新→旧反转）、市场资金流东财 daykline 回退、上交所官方两融解析、两融回退含日期回退与单所 warning。

### Changed

- 深交所 xlsx 解析抑制 openpyxl `UserWarning`，避免污染 CLI JSON 输出。
- `SKILL.md` best-effort 边界与 `references/source-playbook.md` 资金域/事件域/能力表同步备胎链描述；记录 push2 与 push2his/push2delay 风控面不同的实测结论。

### Validation

- `python3 -m unittest discover -s tests` 63/63 通过。
- 真实接口实测（2026-09-10 盘中）：market 回退拿到 9/8~9/10 主力净流出（-82.0/-73.5/-315.8 亿）；industry 回退拿到 push2delay 板块资金流 TOP5；两融官方备胎回退到 9/9（沪 1999 行 + 深 2104 行）；新浪个股备胎 600519 三日数据与东财交叉一致。

## v0.4.0 - 2026-08-25

### Added

- Added `references/subagent-playbook.md`：sub-agent 并行编排与复查校对手册（借鉴 claude-trading-skills 的 orchestrator + second-opinion agent 模式）。
- Added 新任务类型「多标的 / 多维度并行」：≥3 只股票对比或复盘多维度时派发并行 sub-agent。
- Added 核心原则 7「多标的并行分析，交付前强制复查」：取数集中在主会话（防东财并发封 IP），sub-agent 只消费底稿；深度分析/复盘/筛选报告强制经 `cross-check-reviewer` 第二意见校对。
- Added 三个 sub-agent 角色定义：`symbol-analyst`（个股）、`domain-analyst`（行情维度）、`cross-check-reviewer`（复查校对，含事实核对/分层合规/偏差检测/僵尸报价与北交所老号段数据质量检查）。

### Changed

- Updated `SKILL.md` 任务路由表、核心工作流、失败处理与仓库内参考，纳入 sub-agent 编排路径；版本升至 0.4.0。

### Validation

- frontmatter 解析与引用文档完整性检查 -> passed
- `python3 scripts/validate_skill.py` 涉及实时取数，未在本次离线改动中重跑

## v0.3.0 - 2026-07-06

### Added

- Added `stock-diagnose` output improvements for more practical A-share analysis wording.
- Added `buy_plan.summary` so diagnosis results now include a concise trading-style summary tied to stance, support, pressure, and stop-loss context.
- Added stronger money-flow narration in layered analysis, translating `main_net_inflow` into readable inflow/outflow signals instead of only exposing raw status.
- Added a standalone `README.md` with installation, Quick Start, common commands, project structure, validation steps, and release-facing usage guidance.
- Added a release cleanup plan artifact at `docs/superpowers/plans/2026-07-06-independent-skill-release-cleanup.md`.

### Changed

- Standardized project documentation and examples around independent skill usage from the project root.
- Updated command examples from `python3 stock-replay-workbench/scripts/...` to `python3 scripts/...`.
- Standardized output directory wording to the project-root `./.analysis/` contract across CLI help and key docs.
- Updated `AGENTS.md` project positioning from repo-core wording to independent skill project wording.
- Kept the project aligned with an independent-release shape across `README.md`, `SKILL.md`, `AGENTS.md`, `INDEX.md`, and validation references.

### Fixed

- Fixed CLI help text for `build-replay` and `render-replay` so relative output paths are documented as writing under `./.analysis/`.
- Preserved six-stock runtime acceptance while improving diagnosis wording, keeping the validator green.
- Ensured documentation no longer implies runtime dependence on repo-relative sibling-project paths.

### Dependencies

- Removed clearly unrelated top-level packages from `requirements.txt`:
  - `Flask`
  - `openai`
  - `pytest`

### Validation

- `python3 scripts/validate_skill.py` -> passed
- `python3 scripts/stock_replay_cli.py --help` -> passed
- `python3 -m unittest tests.test_stock_replay_workbench -v` -> passed (`45` tests)

### Notes

- The project is now documented and packaged as an independently usable skill project.
- Runtime still depends on public data sources and third-party Python packages, which is an expected boundary and not treated as sibling-project coupling.
