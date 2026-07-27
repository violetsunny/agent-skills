---
name: opsx-workflow-hooks
description: |
  Post-command hooks for the opsx workflow.
  - Trigger A: immediately after /opsx/propose finishes generating all
    artifacts — enters an iterative refinement loop, asking the user if they
    have new ideas and updating proposal artifacts until the user is satisfied.
  - Trigger B: immediately after /opsx/apply completes ALL tasks (state:
    all_done) — runs gstack-review to check code and logic for issues, fixes
    any critical problems found, then runs /opsx/archive to archive the change.
    Does NOT trigger when apply is paused mid-way.
  Use when "/opsx/propose is done", "proposal artifacts created", "all tasks
  complete after apply", "apply finished", or "implementation complete".
---

# OPSX Workflow Hooks

Post-completion behavior injected after `/opsx/propose` and `/opsx/apply`.

## Bootstrap

When this skill is invoked directly, first verify that the global OPSX command
files still contain the callback hooks that re-enter this skill after OpenSpec
commands complete. OpenSpec updates may overwrite those command files.

### Bootstrap Steps

1. Read these files:
   - `~/.agents/commands/opsx/propose.md`
   - `~/.agents/commands/opsx/apply.md`
2. Check whether `propose.md` contains all of:
   - `**Post-completion hook**`
   - `opsx-workflow-hooks`
   - `Hook A`
3. Check whether `apply.md` contains all of:
   - `**Post-completion hook**`
   - `opsx-workflow-hooks`
   - `Hook B`
4. If either hook block is missing, initialize it immediately before doing
   anything else.

### Initialization Payload

If `propose.md` is missing Hook A, append this block exactly once:

```md
**Post-completion hook**

After all artifacts are created and the final status is shown, use the **Skill tool** to invoke the `opsx-workflow-hooks` skill (Hook A). Do this automatically — do not wait for the user to ask.
```

If `apply.md` is missing Hook B, append this block exactly once:

```md
**Post-completion hook**

When all tasks are done (`state: "all_done"`), use the **Skill tool** to invoke the `opsx-workflow-hooks` skill (Hook B). Do this automatically — do not wait for the user to ask.

If apply is paused mid-way, do NOT invoke the hook. Wait for the user to resume.
```

### Bootstrap Guardrails

- This initialization is idempotent: never add the same hook block twice.
- Prefer patching only the missing block; do not rewrite unrelated command text.
- After patching, re-read both files and confirm the hook markers are present.
- Only after bootstrap succeeds should the skill continue into Hook A or Hook B.

---

## Hook A — After `/opsx/propose`

**Trigger:** `/opsx/propose` has finished and all `applyRequires` artifacts are
written to disk.

### Purpose

The first proposal is rarely final. This hook keeps the user in a fast
iteration loop so the proposal converges before any implementation starts.

### Steps

1. **Ask for feedback**

   Use the **AskUserQuestion tool** (open-ended, no preset options) to ask:

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
     - If the new input changes intent, constraints, acceptance criteria, or
       reveals unclear assumptions, use `grill-me` first to sharpen requirement
       understanding before deciding how to update the proposal.
     - If the new input exposes multiple possible solution paths, unresolved
       product tradeoffs, or a design direction that still feels under-specified,
       use `brainstorming` to refine the proposal collaboratively before editing
       the artifacts.
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
     - Identify which artifacts are affected:
       - Scope/goal changes → `proposal.md`
       - Architecture/approach changes → `design.md`
       - Task breakdown changes → `tasks.md`
     - If the proposal is conceptually stable but `tasks.md` is still too coarse
       to execute confidently, use `writing-plans` to sharpen the implementation
       breakdown before finalizing the updated tasks.
     - Update only the affected artifact files. Do NOT rewrite unaffected files.
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
     - **Return to Step 1** (ask again).

3. **Loop until the user is satisfied.**

   There is no forced exit. Keep iterating until the user explicitly signals
   they are done or says to proceed.

### Guardrails

- Default to artifact iteration during this hook; only bypass `/opsx:apply` for
  a tiny implementation change that meets the strict threshold above.
- Use `grill-me` only when requirement understanding is materially incomplete;
  do not turn every minor wording tweak into a long clarification session.
- Use `brainstorming` only for genuine design or tradeoff ambiguity; once the
  direction is already clear, update the artifacts directly.
- Use `writing-plans` only when task granularity is the real gap; do not force
  a full planning pass for a small artifact edit.
- If the user's input is ambiguous (could be a question or a change request),
  treat it as a change request and propose an update, then ask for confirmation.
- Surgical edits only: change exactly what the user asked for, nothing more.
- The optional proposal prompts are aids only; they must stay within the current
  proposal's scope and must not invent new product requirements.
- If the user's request contradicts an existing artifact constraint, surface the
  conflict and ask which takes priority — do NOT silently average them.

---

## Hook B — After `/opsx/apply`

**Trigger:** `/opsx/apply` has finished AND `state: "all_done"` — every task is
checked off. **Do NOT trigger if apply paused mid-way** (`state: "paused"` or
partial progress); in that case, wait for the user to resume and complete apply.

### Purpose

Implementation can introduce subtle logic errors or missed edge cases. This hook
enforces a mandatory review-then-archive sequence so nothing lands without a
final check.

### Steps

1. **Run the review**

   Announce: "Implementation complete. Running review before archiving…"

   Review in this order, stopping when the current layer is sufficient:

   **Review selection priority:**

   1. **Agent built-in `/review` capability** — try this first whenever the
      current runtime can invoke it successfully.
   2. **`code-review`** — primary fallback for completed `/opsx:apply` work.
      Use it when you can identify a fixed point for the implementation diff.
      Review along both axes: repo standards and spec alignment.
   3. **`java-code-review`** — for Java/Spring projects, run this after
      `code-review` when you need an additional Java-focused pass on null
      safety, exceptions, concurrency, and performance. Also use it as the
      direct fallback when `/review` or `code-review` cannot run cleanly.
   4. **Other review skills** — if none of the above is available, use the most
      specific review skill present in the workspace.
   5. **Manual inspection** — if no review skill exists at all, read every file
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

3. **Archive**

   Announce: "Review passed. Archiving change…"

   Execute `/opsx/archive` for the same change name already known from the
   apply session. Do NOT ask the user for the change name again.

   The archive command will handle: delta-spec sync check, task completion
   check, directory move, and summary output. Let it run to completion.

4. **Confirm completion**

   Print the archive summary from `/opsx/archive`, then append:

   ```
   Workflow complete: propose → apply → review → archive
   ```

### Guardrails

- Only trigger when `state: "all_done"`. If apply is paused, do nothing.
- Never skip the review step, even if the implementation looks clean.
- Never archive with unresolved CRITICAL issues.
- WARNING-level issues require a user decision — do not silently ignore or
  silently fix them.
- If `/opsx/archive` fails (e.g., archive already exists), surface the error
  and options to the user; do not force-proceed.
