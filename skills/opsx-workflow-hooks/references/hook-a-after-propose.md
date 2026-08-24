# Hook A - After `/opsx/propose`

## Trigger

`/opsx/propose` has finished and all `applyRequires` artifacts are written to disk.

## Purpose

The first proposal is rarely final. This hook keeps the user in a fast iteration loop so the proposal converges before any implementation starts, while using the right planning skills for the current workstream:

- backend code writing
- frontend code auto-generation
- technical-solution or knowledge-content writing

Use sub agents for any non-trivial artifact analysis or drafting so the planning pass stays context-clean. The main thread owns the user loop and the final artifact write/validation.

## Steps

1. **Ask for feedback**

   Use the AskUserQuestion tool (open-ended, no preset options) to ask:

   > "Proposal complete. Do you have any new ideas, changes, or concerns you'd like to incorporate before moving to implementation? If helpful, here are one or two optional proposal prompts to react to: (1) add a missing edge case or acceptance condition, (2) simplify one implementation step or split an oversized task. Enter your thoughts, or say 'looks good' / 'no' to proceed."

2. **Evaluate the response**

   - **If the user signals satisfaction** (for example: "looks good", "no", "proceed", "go ahead", blank/empty, or affirmative with no actionable content):
     - Print: `Proposal locked. Run /opsx:apply when ready to implement.`
     - Stop. Do not loop.

   - **If the user provides new ideas or concerns:**
     - Acknowledge the input briefly in one sentence.
      - First decide whether this is a **tiny artifact change** that can bypass the normal artifact-refinement loop.
      - **Tiny change shortcut**: if the request can be completed as a very small, local planning-artifact adjustment (`<= 5` changed lines), in one artifact file, with no new function, API, schema, task breakdown, design change, or cross-file behavior impact, apply it directly to the affected planning artifact and do a lightweight validation/check only. Do not edit project code and do not load the full workstream skill set for this case.
      - If requirement understanding is still materially incomplete, or the user is choosing between competing directions, load `grill-me` before editing artifacts so the uncertainty is resolved first.
      - Only if the request is **not** a tiny artifact change, determine **one primary workstream** before editing artifacts, then use a fresh sub agent to analyze or draft the needed artifact changes before the main thread writes them.

3. **Use sub agents as the default non-trivial planning worker**

   - Launch a fresh sub agent when any of the following is true:
     - the change affects more than one planning artifact
     - the request changes scope, acceptance criteria, design, or task structure
     - competing interpretations must be compared before editing
     - substantial drafting is needed for proposal/design/tasks
   - Give the sub agent one narrow job: classify the request, propose exact artifact deltas, or draft replacement text for the affected sections.
   - After the sub agent returns, the main thread must review the result, write the actual artifact files, run `openspec status --change "<name>" --json`, and summarize the update to the user.
   - Do not let a sub agent directly close the user loop or declare the proposal locked.

4. **Route to the minimum effective planning skills**

   - **Backend code writing** (for example Java/Python services, APIs, scheduling, persistence, data flow, integration logic): start with `codebase-design` to shape module boundaries and interfaces. Add `spring-boot-patterns`, `design-patterns`, `jpa-patterns`, or `api-contract-review` only when they are directly relevant to the requested artifact update.
   - **Frontend code auto-generation** (for example HTML/CSS/Vue, generated pages/components, interactive flows, responsive UI): load `ui-ux-pro-max` first and keep it active throughout artifact refinement. Add `frontend-design` only when the change materially affects visual direction or layout language. Add `ui-styling` only when stack-specific component or layout constraints need to be reflected in the plan. Do not load `web-artifacts-builder` in Hook A; this hook is planning-only.
   - **Technical-solution or knowledge-content writing** (for example design docs, ADRs, technical proposals, knowledge notes, tutorials, internal guidance): load `doc-coauthoring` first for structure and reader clarity. Add `domain-modeling` when terminology or concept boundaries are part of the change. Add `research` only for fact-heavy claims. Add `teach` only for tutorial or instructional content. Add `internal-comms` only for stakeholder-facing or internal update formats.

5. **Reflect the chosen workstream in the planning artifacts**

   Update the artifacts indirectly through the workstream lens:

   - `proposal.md` - user-visible goals, acceptance criteria, and scope
   - `design.md` - architecture, UI/content structure, trade-offs, and risks
   - `tasks.md` - execution order plus the matching review, test, and validation tasks

   If a request spans multiple areas, keep one primary workstream and add only the minimum secondary skills needed to avoid scope creep.

6. **Classify the edit path**

   - **Tiny artifact change** - use the shortcut path above.
   - **Artifact-level change** - anything that changes scope, design, acceptance criteria, task structure, cross-file behavior, or needs more than the tiny-edit threshold above.

7. **Apply the chosen path**

   - **If it is a tiny artifact change:**
     - Update the small planning artifact directly.
     - Do not edit implementation files and do not run `/opsx:apply` during this hook.
     - Run only a lightweight check/validation appropriate to the touched artifact file. Do not invoke the full Hook B workflow. Do not archive and do not mark apply tasks complete.
     - Report the result clearly:

       ```
       Applied tiny artifact update directly - updated <file>
       Lightweight validation complete - no major issues found
       ```

     - Return to Step 1 and ask if the user has any other ideas.

   - **If it is an artifact-level change:**
     - Identify which artifacts are affected:
       - Scope/goal changes -> `proposal.md`
       - Architecture/approach changes -> `design.md`
       - Task breakdown changes -> `tasks.md`
     - Update only the affected artifact files. Do not rewrite unaffected files.
     - After writing, verify the artifact is recognized by running:

       ```bash
       openspec status --change "<name>" --json
       ```

     - Confirm the updated artifact still shows `status: "done"`. If it does not (for example, template validation fails), fix the file and re-check.
     - After confirming, print a brief diff summary:

       ```
       Updated proposal.md - added X, revised Y
       Updated tasks.md - split task 3 into two steps
       ```

     - Return to Step 1 and ask again.

8. **Loop until the user is satisfied**

   There is no forced exit. Keep iterating until the user explicitly signals they are done or says to proceed.

## Guardrails

- Default to artifact iteration during this hook; only bypass the normal artifact-refinement loop for a tiny planning-artifact change that meets the strict threshold above.
- Tiny changes should be detected before workstream routing. Do not send a one-file micro-fix through the full proposal/design/tasks refinement loop.
- This hook is still planning-only: never edit project code here, even when the user asks for a tiny fix. Route implementation to `/opsx:apply` instead.
- For non-trivial planning work, prefer a fresh sub agent over doing all reasoning in the main thread. Clean-context drafting is the default, not an exception.
- The main thread remains the control plane: only it talks to the user, writes artifacts, runs OpenSpec status checks, and decides whether to loop or stop.
- Use the minimum effective skill set for the active workstream. Do not load every nearby planning skill just because it could apply.
- `grill-me` is for materially incomplete requirements or unresolved trade-offs, not routine wording tweaks.
- Hook A may proactively load supporting skills for backend, frontend, or technical/knowledge writing work, but only to improve the current planning artifacts. Do not let skill usage introduce new product scope or speculative features.
- Choose one primary workstream per iteration. Add secondary skills only when they directly support the same request.
- Ensure `tasks.md` records the matching review, test, and validation work for the selected workstream rather than leaving those steps implicit.
- If the user's input is ambiguous (could be a question or a change request), treat it as a change request and propose an update, then ask for confirmation.
- Surgical edits only: change exactly what the user asked for, nothing more.
- The optional proposal prompts are aids only; they must stay within the current proposal's scope and must not invent new product requirements.
- If the user's request contradicts an existing artifact constraint, surface the conflict and ask which takes priority. Do not silently average them.
