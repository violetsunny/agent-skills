---
name: opsx-workflow-hooks
description: |
  Post-command hooks for the opsx workflow.
  - Trigger A: immediately after /opsx/propose finishes generating all
    artifacts — runs requirement clarification and proposal refinement across
    grill-me, brainstorming, and writing-plans before locking the change.
  - Trigger B: immediately after /opsx/apply completes ALL tasks (state:
    all_done) — runs /review first, then code-review and java-code-review as
    needed, verifies the change, and archives it. Does NOT trigger when apply
    is paused mid-way.
  Use when "/opsx/propose is done", "proposal artifacts created", "all tasks
  complete after apply", "apply finished", or "implementation complete".
---

# OPSX Workflow Hooks

Post-completion behavior injected after `/opsx/propose` and `/opsx/apply`.

## Bootstrap

When invoked directly, first verify that the OPSX command files still contain
the callback hooks that re-enter this skill after OpenSpec commands complete.
OpenSpec updates may overwrite those command files.

### Bootstrap Steps

1. Read these files as two synchronized pairs:
   - Project source: `agent-skills/commands/opsx/propose.md`
   - Runtime copy: `~/.agents/commands/opsx/propose.md`
   - Project source: `agent-skills/commands/opsx/apply.md`
   - Runtime copy: `~/.agents/commands/opsx/apply.md`
2. Check whether both `propose.md` copies contain all of:
   - `OPSX IMMUTABLE BOUNDARY`
   - `**Post-completion hook**`
   - `opsx-workflow-hooks`
   - `Hook A`
3. Check whether both `apply.md` copies contain all of:
   - `OPSX IMMUTABLE BOUNDARY`
   - `**Post-completion hook**`
   - `opsx-workflow-hooks`
   - `Hook B`
4. If a copy is missing the full tail marker set, repair only the Hook tail:
   - No hook yet: append the full Hook A / Hook B tail.
   - Hook exists but boundary is missing: rewrite the existing Hook tail so the
     boundary marker appears immediately before `**Post-completion hook**`.
   The original command body is immutable; only the appended Hook A / Hook B
   tail section may be created, extended, or revised. The boundary marker
   belongs inside the two command files only, never inside this skill file.
5. After hook presence is confirmed, diff each source/runtime pair. If the pair
   is not byte-identical, treat that as a stale-copy problem and sync the stale
   side by restoring the matching Hook tail. Do not continue until both pairs
   match.

### Initialization Payload

If `propose.md` is missing Hook A, append this block exactly once:

```md
<!-- OPSX IMMUTABLE BOUNDARY: original command content above this line must not be modified -->

**Post-completion hook**

After all artifacts are created and the final status is shown, use the **Skill tool** to invoke the `opsx-workflow-hooks` skill (Hook A). Do this automatically — do not wait for the user to ask.
```

If `apply.md` is missing Hook B, append this block exactly once:

```md
<!-- OPSX IMMUTABLE BOUNDARY: original command content above this line must not be modified -->

**Post-completion hook**

After the final task is marked complete, re-run `openspec instructions apply
--change "<name>" --json`. Only when that command returns
`state: "all_done"`, immediately use the **Skill tool** to invoke the
`opsx-workflow-hooks` skill (Hook B). Do not finish with a suggestion to archive
manually.

If apply is paused mid-way, do NOT invoke the hook. Wait for the user to resume.
```

### Bootstrap Guardrails

- This initialization is idempotent: never add the same hook block twice.
- Only the Hook tail may be rewritten. Never rewrite, replace, reorder, or
  insert into the original command body above the boundary marker.
- The immutable area is the original command content that appears before the
  appended boundary marker.
- The mutable area is only the appended Hook A / Hook B tail section that comes
  after the boundary marker.
- Future fixes may revise Hook A / Hook B content, but must not change any text
  above the boundary marker.
- After patching, re-read both source/runtime pairs and confirm the hook
  markers are present in all four files.
- **Full sync verification**: hook-marker presence alone is insufficient. Diff
  the project-source copy (`agent-skills/`) and runtime copy (`~/.agents/`) for
  both `propose.md` and `apply.md`, and require them to be byte-identical
  before continuing. If they diverge, treat the older side as stale and repair
  it by restoring the matching Hook tail.
- Never assume runtime is canonical. A stale project-source copy is equally
  dangerous because a later sync can overwrite a healthy runtime file.
- Only after bootstrap succeeds should the skill continue into Hook A or Hook B.

### Bootstrap Reliability Enhancement

Hook injection presence does not guarantee hook execution after a long apply
session. The reliability fix must also stay inside the mutable Hook B tail
section: add or revise reminder text only below the immutable boundary marker,
without changing the original state handling or output template above it.

---

## Phase Map

Use this skill as the orchestration layer across a seven-stage workflow:

| Phase | Goal | Primary tools | Exit standard |
| --- | --- | --- | --- |
| 0 | Requirement clarification and boundary alignment | `grill-me` | Clear scope, non-scope, and acceptance criteria |
| 1 | Spec solidification and change creation | `to-spec`, OpenSpec propose artifacts | `proposal` / `design` / `tasks` / schema-required spec artifacts are aligned |
| 2 | Architecture decisions and task atomization | `brainstorming`, `writing-plans` | Tasks fully cover specs with no gaps or speculative extras |
| 3 | Implementation execution and process control | `/opsx:apply`, Superpowers execution patterns | Code and tests implemented task by task |
| 4 | Boundary strengthening via tests | TDD + Java-specific edge-case checks | Extreme-path and failure-path tests are present where needed |
| 5 | Layered code review | `/review`, `code-review`, `java-code-review` | Design and code-quality issues are separated and resolved |
| 6 | Verification and archive handoff | `/opsx:verify`, `/opsx:archive` | Change is verified, archived, and traceable |

Hook A primarily governs phases 0-2. Hook B primarily governs phases 5-6 after
phase 3-4 implementation is complete.

---

## Hook A — After `/opsx/propose`

**Trigger:** `/opsx/propose` has finished and all `applyRequires` artifacts are
written to disk.

### Purpose

Sharpen requirements, lock boundaries, and refine task granularity before
implementation starts.

### Summary Format

Use this exact structure whenever Hook A asks the user for feedback or reprints
the updated proposal summary:

```
## Proposal Change Summary: <change-name>

### Need To Fix
- <this round needs to add/change/remove what>

### Current Problem
- <what is unclear, missing, conflicting, or risky in the current proposal>

### Fix Logic
- <how the proposal/design/tasks should be adjusted conceptually>

### Affected Scope
- <artifact/module/API/data-flow/behavior scope that will be affected>

### Still Need Confirmation
- <open question or dependency>; write `None` when there is no blocker

### Acceptance Checks
- [ ] <observable behavior or completion condition>
```

Keep the summary at proposal/design/task level. Do not dump code blocks, long
file inventories, or method-by-method logic. Mention concrete files only when
they are already certain and materially help the user understand scope.

### Steps

1. **Produce a Proposal Change Summary, then ask for feedback**

   `/opsx/propose` usually generates a long context. Before asking the user for
   feedback, first summarize the proposal in a compact form that highlights the
   change itself, the current problem, the fix logic, and any remaining open
   questions.

   Read these files for the current change:
   - `<change-dir>/proposal.md`
   - `<change-dir>/design.md`
   - `<change-dir>/tasks.md`

   Print the **Proposal Change Summary** using the format above.

   - If the artifacts are still too vague to summarize the problem and fix
     logic, ask a focused clarification question before asking for feedback.

   Then use the **AskUserQuestion tool** (open-ended, no preset options) to ask:

   > "Proposal complete. Do you have any new ideas, changes, or concerns you'd
   > like to incorporate before moving to implementation? If helpful, here are
   > one or two optional proposal prompts to react to: (1) add a missing edge
   > case or acceptance condition, (2) simplify one implementation step or split
   > an oversized task. Enter your thoughts, or say 'looks good' / 'no' to proceed."

2. **Evaluate the response**

   - **If the user signals satisfaction** (e.g., "looks good", "no", "proceed",
     "go ahead", blank/empty, affirmative with no actionable content):
     - Print: "Proposal locked. Run `/opsx:apply` when ready to implement."
     - **Stop. Do not loop.**

    - **If the user provides new ideas or concerns:**
      - Acknowledge the input briefly (one sentence).
      - Before using any other skill or editing any artifact, update and reprint
        the **Proposal Change Summary** using the format above. Treat it as the
        working contract for the rest of Hook A; do not rely on the preceding
        conversation as the source of truth.
      - If the user request is still too ambiguous to identify even the affected
        scope or the intended fix logic, stop and ask a focused clarification
        question before editing.
      - If the new input changes intent, constraints, acceptance criteria, or
        reveals unclear assumptions, use `grill-me` first to sharpen requirement
        understanding before deciding how to update the proposal. This is the
        default phase 0 tool.
      - If the new input exposes multiple possible solution paths, unresolved
        product tradeoffs, or a design direction that still feels under-specified,
        use `brainstorming` to refine the proposal collaboratively before editing
        the artifacts. This is the default phase 2 tool for architectural
        ambiguity.
      - First classify the request:
        - **Tiny implementation change** — can be completed with a very small,
          local code edit (`<= 5` changed lines), in one file, with no new
          function, API, schema, task breakdown, or design change.
        - **Artifact-level change** — anything that changes scope, design,
          acceptance criteria, task structure, cross-file behavior, or needs more
          than the tiny-edit threshold above.

   - **If it is a tiny implementation change:**
     - Make the small code change directly.
     - Do NOT run `/opsx:apply` for this case.
     - Immediately enter the review flow even for this direct-execution path.
     - First try the agent's built-in `/review` capability for the touched
       file(s).
     - If `/review` cannot be used from the current execution context, fall back
       to `java-code-review` for the touched file(s).
     - Stop after review completes. Do NOT archive and do NOT mark apply tasks
       complete.
     - Report the result clearly:
       ```
       Applied tiny change directly — updated <file>
       Review complete — no major issues found
       ```
     - Return to Step 1 and ask if the user has any other ideas.

    - **If it is an artifact-level change:**
      - Reprint the final **Proposal Change Summary** immediately before editing
        artifacts. It must reflect any conclusions from `grill-me`, `to-spec`,
        `brainstorming`, or `writing-plans`.
      - If the updated idea is still rough and not yet concrete enough for
        OpenSpec artifact edits, use `to-spec` first to turn it into a crisp
        requirement statement before touching the artifacts. This is the phase 1
        bridge into OpenSpec.
      - Identify which artifacts are affected:
        - Scope/goal changes → `proposal.md`
        - Architecture/approach changes → `design.md`
        - Task breakdown changes → `tasks.md`
        - Requirement/spec wording changes → schema-required spec artifacts
      - If the proposal is conceptually stable but `tasks.md` is still too coarse
        to execute confidently, use `writing-plans` to sharpen the implementation
        breakdown before finalizing the updated tasks. This is the default phase
        2 tool for task atomization.
      - Update only the affected artifact files. Do NOT rewrite unaffected files.
      - **Artifact edit strategy**: if one artifact needs multiple dependent
        edits, prefer reading the full file and doing one comprehensive `write`
        rather than several surgical `edit` calls. This matters most for
        `tasks.md`, where renumbering and task reshaping make later `old_string`
        matches stale. For localized `proposal.md` or `design.md` edits,
        surgical `edit` is usually fine.
      - After writing, verify the artifact is recognized by running:
        ```bash
        openspec status --change "<name>" --json
        ```
        Confirm the updated artifact still shows `status: "done"`. If it does
        not (e.g., template validation fails), fix the file and re-check.
      - After confirming, print a brief diff summary:
        ```
        Updated proposal.md — added X, revised Y
        Updated tasks.md   — split task 3 into two steps
        ```
      - Append a **Post-Edit Summary** using this exact structure:
        ```
        ## Post-Edit Summary: <change-name>

        ### Fixed This Round
        - <what was changed in proposal/design/tasks/specs>

        ### Problem Resolved
        - <what ambiguity, gap, or conflict was resolved>

        ### Final Fix Logic
        - <the final agreed solution logic>

        ### Still Open
        - <remaining question or follow-up>; write `None` when nothing remains
        ```
      - **Return to Step 1** (ask again).

3. **Loop until the user is satisfied.**

   There is no forced exit. Keep iterating until the user explicitly signals
   they are done or says to proceed.

### Guardrails

- Default to artifact iteration during this hook; only bypass `/opsx:apply` for
  a tiny implementation change that meets the strict threshold above.
- Even when Hook A allows a tiny change to be executed directly, it must still
  go through the `/review`-first review path before the hook can continue.
- Use `grill-me` only when requirement understanding is materially incomplete;
  do not turn every minor wording tweak into a long clarification session.
- Use `to-spec` only to sharpen rough requirement language into spec-ready form;
  once the requirement is already precise, edit the OpenSpec artifacts directly.
- Use `brainstorming` only for genuine design or tradeoff ambiguity; once the
  direction is already clear, update the artifacts directly.
- Use `writing-plans` only when task granularity is the real gap; do not force
  a full planning pass for a small artifact edit.
- Before leaving Hook A, the intended implementation scope, non-scope, and
  acceptance criteria must be explainable without hand-waving.
- Never edit an artifact before printing the complete Proposal Change Summary.
- The summary should explain the fix in terms of problem, scope, and logic, not
  code dump or exhaustive file inventory.
- Mention concrete files only when they are already certain and necessary for
  understanding; otherwise stay at artifact/module/API/behavior level.
- After every artifact edit, report the final resolved problem, final fix logic,
  and any remaining open questions.
- If the user's input is ambiguous (could be a question or a change request),
  treat it as a change request and propose an update, then ask for confirmation.
- Surgical edits only: change exactly what the user asked for, nothing more.
- The optional proposal prompts are aids only; they must stay within the current
  proposal's scope and must not invent new product requirements.
- If the user's request contradicts an existing artifact constraint, surface the
  conflict and ask which takes priority — do NOT silently average them.

---

## Hook B — After `/opsx/apply`

**Trigger:** The apply command has re-run
`openspec instructions apply --change "<name>" --json` after the final task and
the result contains `state: "all_done"`. The apply command must invoke this
skill immediately after that confirmation. A checkbox count or a
`N/M tasks complete` message is not sufficient evidence. **Do NOT trigger if
the re-check returns any other state**; wait for the user to resume or resolve
the blocker.

### Purpose

Enforce layered review, explicit verification, and only then archival.

### Steps

1. **Run the review**

   Announce: "Implementation complete. Running review before archiving…"

    Review in this order, stopping when the current layer is sufficient:

   1. **Agent built-in `/review` capability** — try this first whenever the
      current runtime can invoke it successfully. If it is exposed as a slash
      command, use the **Task tool** with `/review` as the complete prompt;
      do not merely print `/review` as text.
   2. **`code-review`** — primary fallback for completed `/opsx:apply` work.
      Use it when you can identify a fixed point for the implementation diff.
      Review along both axes: repo standards and spec alignment.
   3. **`java-code-review`** — for Java/Spring projects, run this after
      `code-review` when you need an additional Java-focused pass on null
      safety, exceptions, concurrency, and performance. Also use it as the
      direct fallback when `/review` or `code-review` cannot run cleanly.
   4. **`security-audit`** — for security-sensitive Java/Spring work such as
      authentication, authorization, input handling, external callbacks, file
      upload, or any internet-facing endpoint, run this after the general review
      layers to catch OWASP and secure-coding issues.
   5. **Other review skills** — if none of the above is available, use the most
      specific review skill present in the workspace.
   6. **Manual inspection** — if no review skill exists at all, read every file
      modified during apply, cross-check each against `proposal.md` and
      `design.md`, and document what was checked.

   If the built-in `/review` capability is not reachable from this execution
   path, do not block the workflow on it; fall through to the skill-based review
   options immediately.

   When using `code-review`, choose a fixed point that isolates the apply
   implementation cleanly (for example the pre-apply HEAD, the change branch
   base, or another resolved merge-base). If no trustworthy fixed point is
   available, fall back to `java-code-review`.

   For Java/Spring projects, prefer a chained review when feasible:
   `/review` → `code-review` → `java-code-review`.
   If the earlier layer already finds blocking issues, fix them first before
   running the next layer.

   For Java/Spring projects that touch security-sensitive flows, extend the
   chain to:
   `/review` → `code-review` → `java-code-review` → `security-audit`.

    The review must cover:

   - **Logic correctness** — does the implementation match the intent in
     `proposal.md` and `design.md`?
   - **Edge cases** — are obvious failure paths handled?
   - **Task completeness** — does every checked-off task have corresponding code?
   - **No regressions** — do existing tests still pass (run the project's test
     command if one is available)?

   Present findings in this format:

   ```
   ## Review: <change-name>

   ### Findings
   - [CRITICAL] <issue description>   ← must fix before archiving
   - [WARNING]  <issue description>   ← should fix, ask user
   - [INFO]     <observation>         ← informational only

   ### Summary
   <overall assessment — one or two sentences>
   ```

2. **Act on findings**

   - **No CRITICAL issues:**
     - If there are WARNINGs, list them and ask the user whether to fix them
       now or proceed.
     - Once the user decides, continue to Step 3.

   - **One or more CRITICAL issues:**
     - Do NOT proceed to archive.
     - Report each critical issue with its location (`file_path:line_number`
       where applicable).
     - Fix them now (minimal code change only — no scope creep).
     - After fixing, re-run the same review method (`/review`, `code-review`,
       `java-code-review`, other skill, or manual) scoped to the affected files
       only.
     - Once no CRITICAL issues remain, continue to Step 3.

3. **Verify the change**

    Announce: "Review passed. Verifying change before archive…"

    Use the **Task tool** to execute `/opsx:verify <name>` for the same change.
    Do not merely print the command as text. Verification must confirm the
    change artifacts and implementation still line up before archival.

   If verification reports drift, missing spec updates, or incomplete task
   closure, stop, fix the issue, and re-run verification before continuing.

4. **Archive**

    Announce: "Review passed. Archiving change…"

    Use the **Task tool** to execute `/opsx:archive <name>` for the same change
    name already known from the apply session. Do NOT ask the user for the
    change name again or merely print the command as a suggestion.

   The archive command will handle: delta-spec sync check, task completion
   check, directory move, and summary output. Let it run to completion.

5. **Confirm completion**

   Print the archive summary from `/opsx/archive`, then append:

   ```
Workflow complete: propose → apply → review → verify → archive
   ```

### Guardrails

- Trust only the post-task CLI re-check supplied by `/opsx/apply`; never infer
  `all_done` from task checkboxes or the final progress text.
- Only proceed when that re-check explicitly contains `state: "all_done"`.
- If the re-check is missing or contains another state, stop and report that
  Hook B was not run; do not review or archive.
- Never skip the review step, even if the implementation looks clean.
- Never skip verification before archive.
- Never archive with unresolved CRITICAL issues.
- WARNING-level issues require a user decision — do not silently ignore or
  silently fix them.
- If `/opsx/archive` fails (e.g., archive already exists), surface the error
  and options to the user; do not force-proceed.
