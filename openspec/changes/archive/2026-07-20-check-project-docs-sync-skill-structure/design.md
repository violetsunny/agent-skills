## Context

`skills/project-docs-sync/SKILL.md` (v2.0) embeds multiple Markdown template blocks that illustrate what the generated output files should look like. When writing these templates, triple-backtick fenced code blocks were used as the outer container, while the template content itself also uses triple-backtick fences for bash/markdown examples. Standard CommonMark and GFM parsers treat the first matching closing ` ``` ` as the end of the outer fence — causing the rest of the template to render as prose rather than code. The skill is functional (agents read it as plain text), but it renders incorrectly in GitHub, VS Code preview, and workspace-cli's Markdown preview.

## Goals / Non-Goals

**Goals:**
- Fix all nested fenced code block rendering issues in SKILL.md
- Replace GFM `- [ ]` task-list syntax in the README self-check with plain text to avoid false task-tracking matches
- Remove or annotate the redundant Git commands in Step 0
- Add `<!-- optional -->` notes to the three extra sections in the `docs/architecture.md` template

**Non-Goals:**
- Changing any execution logic, step content, or guardrails
- Modifying trigger phrases or frontmatter
- Changing the `author` field (leave as-is; owner decision)

## Decisions

### D1: Use 4-backtick outer fences for templates containing inner code blocks
**Decision**: Wherever a template block contains its own ` ``` ` fences, wrap the outer block with ```` ```` ```` (4 backticks) instead of ` ``` `.
**Rationale**: CommonMark spec §4.5 states that a fenced code block can only be closed by a fence of equal or greater length. A 4-backtick outer fence cannot be closed by a 3-backtick inner fence.
**Affected locations**:
- AGENTS.md template (lines 154–214): contains a ` ``` ` code block for the directory tree and a `bash` block
- README.md template (lines 236–301): contains `bash` blocks for install, quickstart, dev
- project-map template (lines 436–477): contains a ` ``` ` block for the ASCII tree

**Alternative considered**: Use indented (4-space) code blocks for inner content — rejected because it makes the template harder to read and edit, and indented blocks don't support syntax highlighting hints.

### D2: Replace `- [ ]` checkboxes with `[ ]` plain text in README self-check
**Decision**: Change the 6 checklist items from `- [ ] ...` to `- [ ] ...` written as literal text using HTML entity or just keep bullet-only `- ...` prefix with a `[ ]` as part of the text (non-GFM-parsed).
**Rationale**: GFM task list checkboxes (`- [ ]`) are parsed by openspec's task tracker as pending tasks. If the skill file itself is scanned for tasks, these 6 items will appear as uncompleted work items, creating noise. Plain `- ...` or `- [ ]` written without the GFM trigger avoids this.
**Practical fix**: Change `- [ ]` to `- [ ]` by using `&#x5B;` HTML entity — or more simply, prefix with a non-GFM character. Simplest: change to `- ☐ ` (Unicode ballot box) which is visually equivalent and unambiguous.

### D3: Remove redundant Git commands from Step 0
**Decision**: Remove the `git tag ... | head -5` and `git log --oneline -20` lines from Step 0 (lines 69–71), since they don't assign variables and their output is never referenced again.
**Rationale**: Step 5 re-fetches Git history with proper variable assignment. The Step 0 commands produce ephemeral output that an agent may try to act on (or ignore), adding confusion. Removing them keeps Step 0 focused on state detection only.
**Alternative**: Keep them with an explicit comment `# informational only — output not used in later steps`. Accepted as an alternative if removal feels too aggressive.

### D4: Mark optional sections in `docs/architecture.md` template
**Decision**: Add `<!-- optional -->` inline comments after the `##` headings for `依赖关系`, `扩展点`, and `已知限制`.
**Rationale**: The `architecture-doc` spec only requires: overview, Mermaid diagram, data flow, module table, FAQ. The three extra sections are good practice but not required. Making them optional reduces agent uncertainty about whether to populate them.

## Risks / Trade-offs

- **[Risk] 4-backtick fences are less familiar** → Mitigation: CommonMark support for 4-backtick fences is universal; no real risk.
- **[Risk] Removing Step 0 Git commands may confuse existing users** → Mitigation: The commands are redundant; Step 5 covers Git history completely. If preferred, keep with annotation (see D3 alternative).
- **[Trade-off] Ballot box `☐` vs plain dash** → `☐` is visually cleaner but slightly less portable. Plain `- text` with no checkbox marker is safest but loses the visual checklist feel. Ballot box is the chosen balance.
