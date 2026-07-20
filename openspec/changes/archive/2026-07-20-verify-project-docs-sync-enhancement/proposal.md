## Why

The `project-docs-sync` skill (v1.0) only generated two files — `AGENTS.md` and `README.md` — leaving critical documentation gaps: no CHANGELOG, no visual project map, no architecture reference, and a README that lacked the "30-second value judgment" structure that helps developers quickly evaluate a project. The enhancement merges four complementary skills (`changelog-gen`, `zh-readme`, `zh-docgen`, `ds-mapper`) into a single, cohesive documentation suite that covers the full lifecycle of project documentation in one pass.

## What Changes

- **Expanded output scope**: From 2 files to 5 files per run (`AGENTS.md`, `README.md`, `CHANGELOG.md`, `docs/project-map.md`, `docs/architecture.md`)
- **README quality upgrade**: Adopts zh-readme's "30-second value judgment" framework — mandatory value proposition, target audience, shortest-possible install command; bans empty marketing words; adds a self-check checklist
- **CHANGELOG generation** (new): Reads Git history, classifies commits via Conventional Commits, applies SemVer versioning rules, emits Keep-a-Changelog format; handles repos with and without tags
- **Project structure map** (new): `docs/project-map.md` — ASCII directory tree with Chinese inline annotations, module responsibility table, entry-point guide; max 3 levels deep
- **Architecture document** (new): `docs/architecture.md` — Mermaid diagram, data-flow description, core module table, FAQ section
- **Chinese-first documentation**: README, project-map, and architecture docs use Chinese prose with English-preserved technical terms
- **Step numbering restructured**: Steps 0–7 replacing the original 0–5, with new Step 5 (CHANGELOG), Step 6 (docs/), Step 7 (report)
- **Guardrails strengthened**: Edit-over-Write rule for CHANGELOG and README, empty-section omission rule for CHANGELOG, explicit Chinese-first principle

## Capabilities

### New Capabilities
- `changelog-generation`: Auto-generate CHANGELOG.md from Git history using Conventional Commits classification and SemVer versioning strategy
- `project-structure-map`: Generate `docs/project-map.md` — annotated ASCII directory tree with module explanations and entry-point guide
- `architecture-doc`: Generate `docs/architecture.md` — Mermaid architecture diagram, data flow, module table, and FAQ

### Modified Capabilities
- `readme-generation`: README.md template and workflow upgraded to zh-readme standard (30-second value judgment, self-check checklist, Chinese-first prose, no empty marketing language)

## Impact

- **Affected file**: `skills/project-docs-sync/SKILL.md` (sole file in the skill)
- **No breaking changes** to existing trigger phrases — all original triggers preserved; new triggers added
- **Output contract change**: callers expecting only `AGENTS.md` + `README.md` will now also receive `CHANGELOG.md`, `docs/project-map.md`, `docs/architecture.md` — additive, not destructive
- **Version bump**: `1.0` → `2.0` in skill frontmatter
