## ADDED Requirements

### Requirement: Generate annotated directory tree
The skill SHALL produce `docs/project-map.md` containing an ASCII directory tree with inline Chinese annotations for every significant directory and file.

#### Scenario: Standard project — tree up to 3 levels deep
- **WHEN** the project is a single-repo (not monorepo)
- **THEN** the skill SHALL render the directory tree to a maximum depth of 3 levels and annotate each directory with a one-line Chinese description

#### Scenario: Monorepo — separate trees per package
- **WHEN** the project contains a `packages/`, `apps/`, or `workspaces/` directory indicating a monorepo
- **THEN** the skill SHALL emit a separate tree section for each top-level package

#### Scenario: Noise directories are excluded
- **WHEN** generating the tree
- **THEN** the skill SHALL exclude `node_modules`, `.git`, `vendor`, `__pycache__`, `dist`, `build`, `.next`, `.venv` from the output

#### Scenario: Module responsibility table is included
- **WHEN** writing `docs/project-map.md`
- **THEN** the skill SHALL append a Markdown table listing each key directory, its responsibility in Chinese, and its most important files

#### Scenario: Entry-point guide is included
- **WHEN** writing `docs/project-map.md`
- **THEN** the skill SHALL include a "💡 入口建议" section listing the startup entry, documentation entry, config file, and test command

#### Scenario: docs/ directory is created if absent
- **WHEN** the project root does not contain a `docs/` directory
- **THEN** the skill SHALL create it before writing `docs/project-map.md`
