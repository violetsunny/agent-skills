# Changelog

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
