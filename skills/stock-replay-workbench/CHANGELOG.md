# Changelog

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
