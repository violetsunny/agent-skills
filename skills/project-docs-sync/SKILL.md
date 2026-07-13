---
name: project-docs-sync
description: |
  Scans the current project and creates or updates two key documentation files:
  AGENTS.md (project index for AI assistants / workspace tools) and README.md
  (technical and business overview for developers). If an /init command exists
  in the project's commands directory, it is invoked first to bootstrap AGENTS.md.
  Use when asked to "update project docs", "sync documentation", "update AGENTS.md",
  "update README", "refresh project index", or "document this project".
  Also triggers on: "更新项目文档", "项目文档更新", "更新项目索引", "同步文档".
license: MIT
metadata:
  author: workspace
  version: "1.0"
---

# Project Docs Sync

Keeps `AGENTS.md` and `README.md` current with what the project actually does.

**AGENTS.md** — the project index read by AI assistants (Workspace, Claude Code, Cursor).
It tells the agent what the project does, how it's structured, and what conventions to follow.

**README.md** — the human-readable overview: what the project is, why it exists, how to install
and use it, and how to contribute.

---

## Step 0: Locate project root and detect init command

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
echo "PROJECT_ROOT: $_ROOT"
```

Check for a project-level init command that bootstraps AGENTS.md:

```bash
# Common locations for init commands
_INIT_CMD=""
for _candidate in \
    "$_ROOT/.agents/commands/init.md" \
    "$_ROOT/commands/init.md" \
    "$_ROOT/.claude/commands/init.md"; do
  if [ -f "$_candidate" ]; then
    _INIT_CMD="$_candidate"
    echo "INIT_COMMAND_FOUND: $_INIT_CMD"
    break
  fi
done
[ -z "$_INIT_CMD" ] && echo "INIT_COMMAND_FOUND: none"
```

Check existing documentation state:

```bash
_HAS_AGENTS=$([ -f "$_ROOT/AGENTS.md" ] && echo "yes" || echo "no")
_HAS_README=$([ -f "$_ROOT/README.md" ] && echo "yes" || echo "no")
echo "HAS_AGENTS_MD: $_HAS_AGENTS"
echo "HAS_README_MD: $_HAS_README"
```

---

## Step 1: Handle init command (if found)

If `INIT_COMMAND_FOUND` is **not** `none` AND `HAS_AGENTS_MD` is `no`:

Read the init command file, then execute its instructions to bootstrap `AGENTS.md`.
The init command is a project-specific slash command — treat it as an instruction document
and follow its steps to create the initial `AGENTS.md`.

After execution: verify `AGENTS.md` exists at project root. If it does, print:
`AGENTS_MD_BOOTSTRAPPED: yes` and proceed to Step 3 (skip Step 2's creation logic,
but still update/enrich it in Step 3).

If the init command fails or produces no output file, fall through to Step 2 to
generate AGENTS.md from scratch.

---

## Step 2: Scan project structure

Gather evidence about what the project actually does. Do NOT skip or abbreviate this step —
the quality of the documentation is proportional to how well you understand the code.

### 2a. File inventory

```bash
find "$_ROOT" -type f \
  ! -path "*/.git/*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.venv/*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  ! -path "*/.next/*" \
  ! -path "*/.idea/*" \
  | sort | head -300
```

### 2b. Project metadata files

Read ALL of the following that exist (use the Read tool, not bash):

- `package.json` / `pyproject.toml` / `pom.xml` / `build.gradle` / `Cargo.toml` / `go.mod`
- `requirements.txt` / `setup.py` / `setup.cfg`
- `.env.example` / `config.yaml` / `config.example.yml`
- Existing `README.md` (if present — to preserve factual content)
- Existing `AGENTS.md` (if present — to preserve agent-specific rules)
- `CLAUDE.md` / `CONTRIBUTING.md` / `CHANGELOG.md`
- Main entry files: `main.py`, `app.py`, `index.ts`, `index.js`, `main.go`, `Main.java`,
  `src/main.rs`, `cmd/main.go`

### 2c. Architecture inference

From the file inventory, identify:

```
LANGUAGE: [primary language(s)]
FRAMEWORK: [detected frameworks/libraries]
PROJECT_TYPE: [web-app / cli-tool / library / service / monorepo / data-pipeline / other]
ENTRY_POINTS: [main files or commands]
KEY_DIRS: [src/, lib/, cmd/, services/, etc. — with one-line purpose each]
TEST_FRAMEWORK: [jest / pytest / go test / etc.]
BUILD_TOOL: [npm / cargo / gradle / make / etc.]
PACKAGE_MANAGER: [npm / pip / cargo / go / etc.]
```

### 2d. Business purpose extraction

Answer these questions from the code and config:
- What problem does this project solve?
- Who is the target user / caller?
- What are the main features or capabilities?
- What does it NOT do (scope boundaries)?

---

## Step 3: Write or update AGENTS.md

`AGENTS.md` is read by AI assistants. Its purpose: give an agent enough context to work
effectively in the project without reading every file.

**If `HAS_AGENTS_MD` is `yes`:** Read the existing file first. Preserve any existing rules,
conventions, or agent-specific sections. Update factual sections (structure, entry points,
commands) to match the current codebase. Add new sections if the existing file is missing
key context.

**If `HAS_AGENTS_MD` is `no`:** Create from the template below.

### AGENTS.md template

```markdown
# AGENTS.md — Project Index

> Auto-generated by project-docs-sync. Update manually for project-specific rules.

## Project Overview

**Name:** <project name from package.json / pyproject.toml / directory name>
**Type:** <PROJECT_TYPE>
**Language:** <LANGUAGE>
**Framework:** <FRAMEWORK>

One-paragraph description: what the project does, who uses it, and what problem it solves.

## Repository Structure

```
<key directories and files with one-line purpose each>
```

## Entry Points

| Command / File | Purpose |
|---|---|
| `<entry>` | <purpose> |

## Development Setup

```bash
# Install dependencies
<install command>

# Run locally
<dev/run command>

# Run tests
<test command>

# Build
<build command>
```

## Key Conventions

- <coding conventions observed in the codebase>
- <naming patterns>
- <file organization rules>

## Architecture Notes

<How the main components fit together. Data flow. Key design decisions visible in code.>

## Agent Guidelines

<!-- Rules for AI assistants working in this project -->

- Read `<main entry file>` before making changes to understand current structure.
- Run `<test command>` after any changes.
- Match existing code style: <observed style notes>.
- <Any project-specific rules from existing AGENTS.md>
```

Write the completed file to `$_ROOT/AGENTS.md`.

---

## Step 4: Write or update README.md

`README.md` is read by humans: developers, users, contributors.

**If `HAS_README_MD` is `yes`:** Read the existing file first. Preserve structure and
existing content where accurate. Update sections that are stale (wrong commands, outdated
descriptions, missing features). Do NOT use the Write tool — use Edit with exact strings
to preserve existing content that is still valid.

**If `HAS_README_MD` is `no`:** Create from the template below.

### README.md template

```markdown
# <Project Name>

<One-sentence tagline: what it does and for whom.>

## Overview

<2-4 paragraphs: problem it solves, how it solves it, who it's for.
Business context goes here — not just technical description.>

## Features

- <Feature 1>
- <Feature 2>
- <Feature 3>

## Requirements

- <Runtime/platform requirement>
- <Version requirement>

## Installation

```bash
<install steps>
```

## Quick Start

```bash
<minimal working example>
```

## Usage

<More detailed usage examples. Cover the main use cases.>

## Configuration

| Option | Default | Description |
|---|---|---|
| `<key>` | `<default>` | <description> |

## Development

```bash
# Clone and install
<setup commands>

# Run tests
<test command>

# Build
<build command>
```

## Contributing

<Brief contribution guide or link to CONTRIBUTING.md>

## License
```
<License type> — see [LICENSE](LICENSE) for details.
```

**For existing README.md:** Use Edit to update only the sections that are stale.
Never rewrite the whole file if it has substantial existing content.

Write or update the file at `$_ROOT/README.md`.

---

## Step 5: Report

Print a brief summary of what was done:

```
AGENTS_MD: [created|updated|bootstrapped-then-updated]  (<N> sections)
README_MD:  [created|updated|unchanged]  (<N> sections updated)

Key changes:
- <one-line per significant change>

Review these files:
  $_ROOT/AGENTS.md
  $_ROOT/README.md
```

If any critical information could not be inferred (e.g., business purpose is unclear,
no entry point found), list what needs manual review.

---

## Guardrails

- **Read before write.** Always read existing files before updating them.
- **Preserve project-specific rules.** Any existing `## Agent Guidelines` or
  `## Conventions` sections in AGENTS.md are treated as authoritative — do not
  overwrite them, only append if adding new information.
- **No invented content.** Every claim in both files must be traceable to an actual
  file, config, or code pattern in the project. If unsure, write "TODO: verify."
- **Edit over Write for existing files.** When README.md already has content, use
  Edit with exact string matches rather than Write (which would overwrite the whole file).
- **Init command takes precedence.** If an `/init` command bootstrapped AGENTS.md,
  treat that output as the base and only add/update, never replace.
- **Scope is documentation only.** This skill does not modify source code, configs,
  or tests. Only `AGENTS.md` and `README.md` are written.
