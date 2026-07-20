## Why

The v2.0 enhancement of `project-docs-sync` introduced several embedded Markdown template blocks inside the SKILL.md. A structural review found that some of these templates contain **nested triple-backtick fenced code blocks**, which break Markdown rendering (inner fences close the outer block prematurely). Additional minor issues include interactive checkbox syntax in the self-check list, a redundant Git command in Step 0, and a few template/spec alignment gaps. These need to be fixed so the skill renders correctly and is easy to maintain.

## What Changes

- **Fix nested fenced code blocks** in three templates (AGENTS.md template, README.md template, project-map template): replace outer triple-backtick fences with quadruple-backtick fences so inner code blocks don't prematurely close the outer one
- **Fix README self-check checkboxes**: replace `- [ ]` GFM task-list syntax with plain `[ ]` text bullets to avoid confusion with task tracking tools (e.g. openspec)
- **Remove redundant Git commands from Step 0**: the `git tag` and `git log` calls in Step 0 produce output but don't assign variables used later; remove or annotate them clearly as informational-only
- **Align architecture.md template with spec**: add brief inline notes for the three extra sections (`## 依赖关系`, `## 扩展点`, `## 已知限制`) so readers understand they're optional extensions, not required by spec

## Capabilities

### New Capabilities
- (none — this is a structural fix, no new behavioural capabilities)

### Modified Capabilities
- `skill-markdown-structure`: correctness and rendering quality of SKILL.md's embedded template blocks (structural fix, not a behavioural spec change — no delta spec needed)

## Impact

- **Affected file**: `skills/project-docs-sync/SKILL.md` only
- No behavioural changes to the skill's execution logic
- No breaking changes to trigger phrases, step numbering, or output files
- Fixes will make the skill render correctly in all Markdown renderers (GitHub, VS Code preview, workspace-cli UI)
