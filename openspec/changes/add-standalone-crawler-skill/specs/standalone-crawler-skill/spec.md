## Purpose

定义一个名为 easy-crawler 的可独立部署行动型 crawler skill，使调用方能够通过统一任务契约执行通用网页抓取、社媒专项优化抓取以及反爬/浏览器自动化抓取，并获得一致的可观测输出与失败边界。

## ADDED Requirements

### Requirement: Skill SHALL be independently deployable

The skill SHALL be deliverable as a self-contained skill directory that can be copied or synced without depending on hidden repository state.

#### Scenario: Complete standalone delivery structure exists
- **WHEN** the skill is added to the repository
- **THEN** it SHALL include a skill definition, script entrypoints, configuration examples, examples, and references required to understand and run the skill

#### Scenario: Skill can be understood without repository-specific tribal knowledge
- **WHEN** a user reads the skill directory contents
- **THEN** the run prerequisites, expected inputs, outputs, and dependency boundaries SHALL be explicitly documented inside the skill directory

### Requirement: Skill SHALL support a normative task syntax

The skill SHALL define a single task syntax that describes crawl targets, page intent, execution mode, output preferences, and optional browser, login, and proxy controls.

#### Scenario: Generic web crawl task is declared
- **WHEN** a caller provides a task targeting one or more URLs with list/detail extraction intent
- **THEN** the syntax SHALL support declaring the target, extraction goal, output format, and run mode in a consistent structure

#### Scenario: Social-media crawl task is declared
- **WHEN** a caller provides a task targeting a social-media flow such as search, creator timeline, comments, or replies
- **THEN** the syntax SHALL support platform-oriented fields without breaking the same top-level task contract

#### Scenario: Browser and anti-bot options are declared
- **WHEN** a caller requires browser automation, login reuse, proxy routing, or challenge handling
- **THEN** the syntax SHALL support those options as explicit fields rather than undocumented free-form instructions

### Requirement: Skill SHALL support generic web extraction workflows

The skill SHALL define behavior for generic web extraction flows including page access, list traversal, detail extraction, pagination traversal, aggregation, and structured output generation.

#### Scenario: List and detail workflow is requested
- **WHEN** a task describes a list page with downstream detail pages
- **THEN** the skill SHALL support a workflow that records list extraction, follows detail targets, and aggregates the resulting records

#### Scenario: Pagination workflow is requested
- **WHEN** a task describes paginated or scroll-driven collections
- **THEN** the skill SHALL define how repeated page traversal is represented and how outputs are aggregated across traversal steps

### Requirement: Skill SHALL provide social-media-specific optimization behaviors

The skill SHALL define social-media-oriented optimization behaviors for dynamic rendering, login-state reuse, comment graph extraction, search flows, and creator-home flows.

#### Scenario: Login-dependent social-media page is targeted
- **WHEN** a task requires authenticated access to a social-media page
- **THEN** the skill SHALL support an explicit login-state reuse path and report when login state is unavailable or insufficient

#### Scenario: Comment and reply extraction is requested
- **WHEN** a task requests comments and nested replies from a social-media target
- **THEN** the skill SHALL describe outputs that preserve parent-child relationships rather than flattening them silently

#### Scenario: Dynamic social-media content requires rendering
- **WHEN** a target requires client-side rendering to expose posts, search results, or comment threads
- **THEN** the skill SHALL support rendering-aware execution behavior and report that behavior in the run summary

### Requirement: Skill SHALL support anti-bot and browser automation execution modes

The skill SHALL define both lightweight HTTP execution and browser automation execution, including the observable boundary between them.

#### Scenario: HTTP mode is sufficient
- **WHEN** a target can be accessed and extracted without a browser runtime
- **THEN** the skill SHALL allow a lightweight HTTP execution path and report that the run stayed in HTTP mode

#### Scenario: Browser mode is required
- **WHEN** a target requires JavaScript execution, login interaction, scroll automation, or challenge-page handling
- **THEN** the skill SHALL support a browser automation path and report that the run used browser mode

#### Scenario: Anti-bot controls are needed
- **WHEN** a task requires proxy use, stealth settings, real-browser attachment, or challenge handling
- **THEN** the skill SHALL support explicit anti-bot-related options in its task contract and runtime reporting

### Requirement: Skill SHALL define observable outputs and run artifacts

The skill SHALL define a consistent output structure for successful, partial, and failed runs.

#### Scenario: Run completes successfully
- **WHEN** a run finishes with extracted records
- **THEN** the skill SHALL produce a structured result payload and a run summary describing targets, mode, and output locations

#### Scenario: Run partially fails
- **WHEN** some targets or steps fail while others succeed
- **THEN** the skill SHALL surface a partial-result structure together with an explicit error summary instead of implying full success

#### Scenario: Debug artifacts are produced
- **WHEN** the run captures diagnostic artifacts such as snapshots, traces, HTML dumps, or screenshots
- **THEN** the skill SHALL expose their locations through a documented debug-artifact section

### Requirement: Skill SHALL fail visibly with explicit boundaries

The skill SHALL declare unsupported scenarios and missing prerequisites explicitly rather than degrading silently.

#### Scenario: Unsupported platform-specific reverse engineering is required
- **WHEN** a task depends on proprietary signing logic or platform-specific reverse engineering not implemented by the skill
- **THEN** the skill SHALL report the task as unsupported or requiring dedicated adaptation

#### Scenario: Required runtime dependency is missing
- **WHEN** a task requires a browser, proxy, or login-state dependency that is not available
- **THEN** the skill SHALL terminate visibly with a corrective hint instead of silently skipping the missing capability

### Requirement: Skill SHALL be extensible without breaking the task contract

The skill SHALL allow future platform adapters or execution backends to be added without breaking the documented task syntax and output contract.

#### Scenario: New platform optimization is added later
- **WHEN** a future implementation adds a new platform-specific adapter
- **THEN** existing task structures and documented output sections SHALL remain backward compatible

#### Scenario: New execution backend is added later
- **WHEN** a future implementation adds another crawl backend or browser engine
- **THEN** the externally documented task fields and result sections SHALL remain stable unless a separate spec change is introduced
