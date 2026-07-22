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
   > like to incorporate before moving to implementation? (Enter your thoughts,
   > or say 'looks good' / 'no' to proceed.)"

2. **Evaluate the response**

   - **If the user signals satisfaction** (e.g., "looks good", "no", "proceed",
     "go ahead", blank/empty, affirmative with no actionable content):
     - Print: "Proposal locked. Run `/opsx:apply` when ready to implement."
     - **Stop. Do not loop.**

   - **If the user provides new ideas or concerns:**
     - Acknowledge the input briefly (one sentence).
     - Identify which artifacts are affected:
       - Scope/goal changes → `proposal.md`
       - Architecture/approach changes → `design.md`
       - Task breakdown changes → `tasks.md`
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

- Never start implementation during this hook — that is `/opsx/apply`'s job.
- If the user's input is ambiguous (could be a question or a change request),
  treat it as a change request and propose an update, then ask for confirmation.
- Surgical edits only: change exactly what the user asked for, nothing more.
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

   Use the **Skill tool** to load and execute a review skill. The Skill tool
   loads the skill's instructions into the current context so you can perform
   the review inline — this is the only reliable way to trigger review
   automatically from within a skill.

   **Skill selection priority:**

   1. **`gstack-review`** — the standard code review skill, covers logic,
      security, and structural issues.
   2. **`java-code-review`** — use IN ADDITION to `gstack-review` for
      Java/Spring projects (load both, run `java-code-review` first per
      project convention).
   3. **Other review skills** — if neither above is available, use the most
      specific review skill present in the workspace.
   4. **Manual inspection** — if no review skill exists at all, read every
      file modified during apply, cross-check each against `proposal.md` and
      `design.md`, and document what was checked.

   **Why not `/review` slash command?** Slash commands require user input to
   trigger; a skill cannot invoke another slash command programmatically.
   Using the Skill tool achieves the same result without interrupting the
   automated flow.

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
      - After fixing, re-run the same review method (built-in, skill, or manual)
        scoped to the affected files only.
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
