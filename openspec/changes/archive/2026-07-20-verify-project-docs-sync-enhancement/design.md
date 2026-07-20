## Context

`skills/project-docs-sync/SKILL.md` is a single-file skill that an AI agent executes step-by-step. The v1.0 skill instructed the agent to write `AGENTS.md` and `README.md` only. Four separate skills existed for related documentation tasks but were never integrated:

- `changelog-gen` — Git-history-driven CHANGELOG
- `zh-readme` — Chinese-first README quality framework
- `zh-docgen` — Architecture docs with Mermaid diagrams
- `ds-mapper` — Visual directory tree with annotations

The enhancement consolidates all four into a revised `project-docs-sync/SKILL.md` (v2.0), keeping a single skill file as the unit of delivery.

## Goals / Non-Goals

**Goals:**
- Merge changelog, project-map, and architecture-doc generation into the existing skill workflow
- Upgrade README generation to zh-readme quality standard (30-second value judgment, no empty words, self-check)
- Preserve all original trigger phrases and backward compatibility of AGENTS.md generation
- Keep the skill as a **single SKILL.md file** — no additional assets

**Non-Goals:**
- Replacing or deprecating the original four source skills
- Changing the skill's trigger mechanism or frontmatter `name` field
- Auto-publishing or pushing documentation to external systems
- Modifying any project source code (skill scope: documentation only)

## Decisions

### D1: Flat merge into one SKILL.md (not multi-file)
**Decision**: All logic lives in one `SKILL.md`.
**Rationale**: The skill system executes a single markdown file. Splitting into includes or partials is not supported. Consolidation is the only viable approach.
**Alternative considered**: Create separate sub-skills and chain them — rejected because it would require the caller to invoke multiple skills manually, defeating the "one-pass" goal.

### D2: Step numbering — insert new steps after existing scan, before report
**Decision**: Steps 5 (CHANGELOG), 6 (docs/) are inserted between the existing README step (4) and the final report (7).
**Rationale**: Natural dependency order — the scan (Step 2) provides all data needed for all outputs; CHANGELOG needs Git data gathered in Step 0; docs/ needs structure data from Step 2.

### D3: CHANGELOG edit strategy — prepend, not overwrite
**Decision**: When `CHANGELOG.md` already exists, new version blocks are prepended; existing history is preserved.
**Rationale**: CHANGELOG is append-only by convention (Keep a Changelog). Overwriting would destroy release history.
**Alternative**: Always regenerate full history — rejected as destructive and computationally expensive.

### D4: README — Edit tool for existing files, Write tool only for new
**Decision**: Explicit guardrail that `Edit` (not `Write`) must be used when README already has content.
**Rationale**: Prevents accidental erasure of manually-maintained sections (badges, screenshots, detailed usage docs) that the agent can't infer from code alone.

### D5: Chinese-first for human-facing docs, English-first for AGENTS.md
**Decision**: README, project-map, and architecture docs use Chinese prose; AGENTS.md stays English.
**Rationale**: AGENTS.md is consumed by AI agents (language-agnostic, but English is the lingua franca of AI tooling). README and docs/ are consumed by Chinese-speaking developer teams.

### D6: docs/ subdirectory for project-map and architecture
**Decision**: New files go to `docs/project-map.md` and `docs/architecture.md`, not project root.
**Rationale**: Keeps the project root clean; `docs/` is the conventional location for supplementary documentation.

## Risks / Trade-offs

- **[Risk] CHANGELOG generation quality depends on commit discipline** → If the repo uses ad-hoc commit messages (not Conventional Commits), classification degrades to "other changes". Mitigation: guardrail explicitly handles non-conforming commits by placing them in a "其他变更" bucket rather than silently dropping them.

- **[Risk] Mermaid diagram in architecture.md may be inaccurate for complex projects** → The agent infers architecture from file structure, not runtime behaviour. Mitigation: template instructs agent to write "TODO: verify" where inference is uncertain; guardrail "No invented content" applies.

- **[Risk] Edit tool precision for large README files** → If an existing README has many sections, finding exact `oldString` matches may fail. Mitigation: guardrail says "if information is not enough, write TODO: verify" and the agent can fall back to section-by-section editing.

- **[Trade-off] More output files = longer execution time** → A single run now creates up to 5 files instead of 2. This is acceptable since the skill is explicitly invoked (not auto-triggered) and the user expects a comprehensive documentation pass.

- **[Trade-off] docs/ creation may conflict with existing docs/** → If a project already has `docs/project-map.md` or `docs/architecture.md` with custom content, the skill will read-then-edit. The "Edit over Write" guardrail protects existing content, but section-level conflicts require human review.
