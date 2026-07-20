## ADDED Requirements

### Requirement: Embedded Markdown templates render correctly in all standard parsers
The SKILL.md file SHALL use 4-backtick outer fences (` ```` `) wherever an embedded template block contains inner triple-backtick fenced code blocks, so that the outer fence is never prematurely closed by an inner one.

#### Scenario: Nested fences in AGENTS.md template render as a single code block
- **WHEN** the SKILL.md is rendered in a CommonMark-compatible Markdown viewer (GitHub, VS Code, workspace-cli)
- **THEN** the entire AGENTS.md template block from opening to closing outer fence SHALL appear as one continuous code block with no content leaking into prose

#### Scenario: Nested fences in README.md template render as a single code block
- **WHEN** the SKILL.md is rendered in a CommonMark-compatible Markdown viewer
- **THEN** the entire README.md template block SHALL appear as one continuous code block, including all embedded bash examples

#### Scenario: Nested fences in project-map template render as a single code block
- **WHEN** the SKILL.md is rendered in a CommonMark-compatible Markdown viewer
- **THEN** the entire project-map template block SHALL appear as one continuous code block, including the ASCII directory tree block

### Requirement: README self-check list items are not parsed as GFM task list items
The SKILL.md self-check list in Step 4 SHALL use a non-GFM-task-list syntax (e.g. Unicode ballot box `☐`) so that task-tracking tools scanning the file do not interpret these items as pending tasks.

#### Scenario: Self-check items not counted as open tasks by openspec
- **WHEN** openspec or another task-tracking tool scans the SKILL.md for `- [ ]` patterns
- **THEN** the self-check checklist items SHALL NOT appear as pending tasks

#### Scenario: Self-check items remain visually distinct as a checklist
- **WHEN** the SKILL.md is read by a human or AI agent
- **THEN** the self-check items SHALL be visually recognisable as a checklist (using `☐` prefix or equivalent)

### Requirement: Step 0 contains only state-detection commands with no unreferenced output
Step 0 of the SKILL.md SHALL contain only bash commands whose output is either: (a) assigned to a variable used in a later step, or (b) annotated as informational with an explicit comment.

#### Scenario: No stray git commands produce unassigned output in Step 0
- **WHEN** an agent executes the Step 0 bash blocks
- **THEN** every line of output SHALL correspond to a labelled variable (e.g. `PROJECT_ROOT:`, `INIT_COMMAND_FOUND:`, `HAS_AGENTS_MD:`) or be explicitly marked `# informational`
