---
description: "执行 OpenSpec 变更的实施任务，完成后自动进入 Review/测试/验证/归档流程。/opsx-apply [变更名或需求描述]"
allowed-tools: Bash(openspec:*)
---

Implement tasks from an OpenSpec change, then run a mandatory review, test, verification, and archive sequence before the user spends time on manual validation.

**Store selection:** If the user names a store or the work lives in one, run `openspec store list --json` to discover registered store ids, then pass `--store <id>` on commands that read or write specs and changes. Once selected, treat `--store <id>` as sticky for the rest of the workflow.

**Input**: Optionally specify a change name (e.g., `/opsx-apply add-auth`) or a requirement description. A requirement description is analyzed and matched against active changes; if nothing matches, the workflow stops and suggests `/opsx-propose` instead of implementing. If omitted, check if it can be inferred from conversation context. If vague or ambiguous, prompt for available changes.

$ARGUMENTS

---

## Phase 1: Implement Tasks

### Step 1 — Select the change

If an argument is provided, first check whether it is an existing change name:

- **Matches an existing change** → use it.
- **Does not match any change** → treat it as a requirement description and analyze it:
  - Run `openspec list --json` to enumerate active changes.
  - Match the requirement semantically against each change's name and proposal summary.
  - Candidate found → present the match reasoning and ask the user to confirm which change to apply.
  - No candidate → do NOT implement; report that no matching change exists and suggest running `/opsx-propose <requirement description>` to create planning artifacts first.

If no argument is provided:
- Infer from conversation context if the user mentioned a change
- Auto-select if only one active change exists
- If ambiguous, run `openspec list --json` to get available changes and ask the user to select one

Always announce: "Using change: <name>" and how to override (e.g., `/opsx-apply <other>`).

### Step 2 — Check status to understand the schema

```bash
openspec status --change "<name>" --json
```

Parse the JSON to understand:
- `schemaName`: The workflow being used
- `planningHome`, `changeRoot`, and `actionContext`: planning scope and edit constraints
- Which artifact contains the tasks

### Step 3 — Get apply instructions

```bash
openspec instructions apply --change "<name>" --json
```

This returns:
- `contextFiles`: artifact ID → array of concrete file paths
- Progress (total, complete, remaining)
- Task list with status
- Dynamic instruction based on current state
- Optional `context`: required prompt-level project instruction input
- Optional `operationGuidance`: advisory guidance for apply

**Handle states:**
- If `state: "blocked"` (missing artifacts): show message, suggest using `/opsx-continue` or `openspec instructions <artifact-id>`
- If `state: "all_done"`: congratulate, suggest archive (proceed to Phase 2)
- Otherwise: proceed to implementation

Treat `context` as required prompt-level input — read and apply relevant conventions. Treat `operationGuidance` as optional additive advice. Both are prompt-level behavior contracts, not enforceable checks — they are NOT evidence of task completion, do not replace the built-in instruction, and do not permit bypassing a blocked state. If context conflicts with the built-in instruction, an explicit user choice, or a CLI-controlled value, report the conflict and preserve the controlling value.

### Step 4 — Read context files

Read every file path listed under `contextFiles` from the apply instructions output. Do not copy `context` or `operationGuidance` verbatim into implementation files.

### Step 5 — Show current progress

Display:
- Schema being used
- Progress: "N/M tasks complete"
- Remaining tasks overview
- Dynamic instruction from CLI

### Step 6 — Implement tasks (loop until done or blocked)

For each pending task:
- Show which task is being worked on
- Make the code changes required
- Keep changes minimal and focused
- Mark task complete in the tasks file: `- [ ]` → `- [x]`
- Continue to next task

**Pause if:**
- Task is unclear → ask for clarification
- Implementation reveals a design issue → suggest updating artifacts
- A task needs work beyond what the spec describes → surface the added scope and ask; do not absorb it silently
- Error or blocker encountered → report and wait for guidance
- User interrupts

### Step 7 — On completion or pause, show status

Display:
- Tasks completed this session
- Overall progress: "N/M tasks complete"
- If all done: proceed to Phase 2
- If paused: explain why and wait for guidance

### Phase 1 Guardrails

- Keep going through tasks until done or blocked
- Always read context files before starting
- If task is ambiguous, pause and ask before implementing
- Keep code changes minimal and scoped to each task
- Update task checkbox immediately after completing each task
- Only mark a task `- [x]` when its specified behavior is fully implemented
- When a task needs work beyond what the spec describes, surface the added scope and pause

---

## Phase 2: Review, Test, Verification, and Archive (Hook B)

**Trigger:** Phase 1 has reached an implementation-complete handoff — either `state: "all_done"` (every task checked off) or the only remaining tasks are user/external verification (SIT/UAT/manual checks).

Do NOT trigger Phase 2 for ordinary mid-implementation pauses, blockers, or partial progress where agent-completable work remains.

Announce: `Implementation pass complete. Running review and automated verification before user validation or archive...`

### Step 1 — Classify the handoff and load the right skills

Classify into one of two paths:
- **Archive-ready path**: all tasks complete (`state: "all_done"`)
- **Manual-validation handoff path**: implementation complete, remaining tasks are only user/external verification

Classify the completed work into one primary workstream for orchestration, then run the main review/verification pass in fresh sub agents. If the change touches other workstreams, add matching secondary review passes for each affected workstream.

### Step 2 — Use sub agents as the default non-trivial review worker

Launch fresh sub agents for the main review/verification pass whenever the handoff includes meaningful code, UI, tests, content, or multiple changed files.

Each sub agent should have one narrow responsibility: workflow verification, standards/spec review, UI review, browser verification, test-quality review, or content-quality review.

Prefer parallel sub agents when checks are independent. After sub agents return, the main thread aggregates findings, decides whether CRITICAL issues exist, applies fixes, re-runs checks, and decides whether archive is allowed.

Tiny follow-up checks on a one-line/local change may stay in the main thread.

### Step 3 — Route to the minimum effective post-apply skills

- **Backend code writing**
  - Execution/fix: `implement` for minimal follow-up fixes required by critical findings.
  - Verification baseline: `openspec-verify-change` only on the archive-ready path. Skip on manual-validation handoff path.
  - Code review: `java-code-review` for Java/Spring work. Add `code-review` only when a broader standards/spec diff review adds signal.
  - Testing: `tdd` and `test-quality` when changed behavior needs regression coverage. Add `api-tester` when API contracts changed.
  - Optional: `codebase-design`, `spring-boot-patterns`, `design-patterns`, `jpa-patterns`, `api-contract-review` only when findings point there.

- **Frontend code auto-generation**
  - Execution/fix: `implement` for minimal follow-up fixes.
  - Verification baseline: `openspec-verify-change` only on the archive-ready path.
  - UI review: `ui-ux-pro-max` is mandatory for HTML/CSS/UI work.
  - Testing: `webapp-testing` for rendered browser behavior.
  - Add `frontend-design` only when review reveals a visual-direction problem.
  - Add `ui-styling` only when stack uses component-level styling systems.
  - Add `code-review` only when a broader code-bearing diff review adds signal beyond UI.

- **Technical-solution or knowledge-content writing**
  - Execution/fix: `implement` only when findings require direct file fixes.
  - Verification baseline: `openspec-verify-change` only on the archive-ready path.
  - Document quality baseline: `doc-coauthoring`.
  - Add `research` only for fact-heavy claims.
  - Add `domain-modeling` when terminology or concept boundaries matter.
  - Add `teach` only for tutorial content.
  - Add `internal-comms` only for stakeholder-facing formats.

### Step 4 — Run the review and verification pass

- **Archive-ready path:** include `openspec-verify-change` in the gate.
- **Manual-validation handoff path:** skip `openspec-verify-change`, rely on workstream-specific review/test gate.

The review must cover:
- **Logic correctness** — does implementation match `proposal.md` and `design.md`?
- **Edge cases** — are obvious failure paths handled?
- **Task completeness** — does every checked-off task have corresponding implementation?
- **Backend/API correctness** (when backend code changed) — API contracts, persistence, transaction boundaries, error paths
- **Regression coverage** — for each new behavior or fix, is there a corresponding automated test?
- **No regressions** — do existing tests still pass?
- **Test quality** — are new tests behavior-focused and exercising public seams?
- **UI/UX quality** (when HTML/CSS involved) — accessibility, responsive layout, typography, contrast, interaction patterns
- **Rendered UI verification** (when browser-facing behavior changes) — Playwright or browser-level checks
- **Content quality** (when deliverable is technical/knowledge content) — structure, audience fit, terminology consistency
- **Fact validation** (when deliverable contains technical claims) — checked against project context or reliable sources

Present findings in this format:

```
## Review: <change-name>

### Findings
- [CRITICAL] <issue description>
- [WARNING] <issue description>
- [INFO] <observation>

### Summary
<overall assessment — one or two sentences>
```

### Step 5 — Act on findings

- **No CRITICAL issues:**
  - If there are WARNINGs, list them and ask the user whether to fix now or proceed.
  - Once the user decides, continue to Step 6.

- **One or more CRITICAL issues:**
  - Do not proceed to archive.
  - Report each critical issue with its location (`file_path:line_number` where applicable).
  - Fix them now using the minimum scoped file change needed.
  - If the critical issue is missing test coverage, add or improve the smallest meaningful automated test before re-running review.
  - After fixing, re-run the same verification path:
    - archive-ready path → re-run `openspec-verify-change` plus workstream-specific review/testing
    - manual-validation handoff path → re-run workstream-specific review/testing only
  - Once no CRITICAL issues remain, re-run Step 4 for fresh evidence, then confirm the gate is clean before continuing.

### Step 6 — Choose the correct post-review outcome

- **If remaining tasks are only user/external verification:**
  - Do not archive yet.
  - State clearly that the implementation has passed the automated gate and the next step is manual/external verification.
  - Tell the user to resume the workflow after SIT/UAT/manual validation is complete.
  - Print: `Automated review complete: proceed with SIT/UAT/manual verification`

- **If all tasks are complete (`state: "all_done"`):**
  - Announce: `Review passed. Archiving change...`
  - Execute `/opsx/archive` (the existing nested archive command) for the same change name. Do not ask the user for the change name again.
  - Let the archive command run to completion (delta-spec sync, task completion check, directory move, summary).

### Step 7 — Confirm the handoff or completion

Use a summary skill only when it improves the handoff:
- **Code-dominant changes** — use `changelog-generator` for a concise code change summary.
- **Cross-functional or content-heavy changes** — use `handoff` for a structured completion note.

- **If archiving now:**
  - Print the archive summary from `/opsx/archive`, then append:
    ```
    Workflow complete: propose → apply → review → archive
    ```

- **If handing off to user/external verification:**
  - Summarize the automated review/test result briefly, then append:
    ```
    Automated review complete: proceed with SIT/UAT/manual verification
    ```

### Phase 2 Guardrails

- Trigger Phase 2 before the user spends time on SIT/UAT/manual verification when implementation is already complete.
- Do not trigger Phase 2 for ordinary paused mid-way implementation states.
- Never skip the review step, even if the implementation looks clean.
- For non-trivial review/testing/verification work, prefer fresh sub agents.
- The main thread is the only place that may decide severity, apply fixes, ask about WARNINGs, or archive.
- `openspec-verify-change` is the workflow-alignment baseline before archive, but skip it for the manual-validation handoff path.
- When implementation involves HTML/CSS styling, `ui-ux-pro-max` is mandatory.
- When behavior changes, do not treat existing green tests as automatically sufficient — verify targeted coverage.
- When tests are added or changed, review their quality; avoid placeholder or tautological tests.
- Never claim verification passed without fresh evidence from the relevant test, build, browser-level command, or OpenSpec verification pass.
- Use the minimum effective skill set for the active workstream.
- A primary workstream is only an orchestration aid — if multiple workstreams are affected, each must receive workstream-appropriate review coverage.
- Do not send the user to manual verification while obvious automated review/test failures are still unresolved.
- Never archive with unresolved CRITICAL issues.
- WARNING-level issues require a user decision — do not silently ignore or silently fix them.
- If `/opsx/archive` fails (e.g., archive already exists), surface the error and options to the user.
