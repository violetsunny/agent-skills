# Hook B - After `/opsx/apply`

## Trigger

`/opsx/apply` has reached an implementation-complete handoff.

Trigger Hook B in either case:

1. `/opsx/apply` finished with `state: "all_done"` - every task is checked off.
2. `/opsx/apply` is pausing only because the remaining tasks are user/external verification steps after implementation is complete, such as SIT, UAT, manual exploratory checks, or environment-owned validation that the agent cannot perform.

Do not trigger Hook B for ordinary mid-implementation pauses, blockers, unresolved design questions, or partial progress where agent-completable implementation work still remains.
Only treat a remaining task as user/external verification when it inherently requires a human judgment, a user-owned credential, or an external system/environment that the agent cannot operate. If the agent can still move the work forward by changing code, adding tests, reading logs, or running accessible automated checks, this is not the manual-validation handoff path.

## Purpose

Implementation can introduce subtle logic errors, weak generated UI, missing validation, or low-quality written content. This hook enforces a mandatory workstream-aware execution-fix, review, verification, and archive-summary sequence before archive, and crucially before the user spends time on manual verification, so obvious bugs are caught first.

## Steps

1. **Classify the implementation-complete handoff and load the right skills**

   Announce: `Implementation pass complete. Running review and automated verification before user validation or archive...`

   First classify the handoff into one of two paths:

   - **Archive-ready path**: all tasks are complete (`state: "all_done"`).
   - **Manual-validation handoff path**: implementation work is complete, but the remaining tasks are only user/external verification.

   Use the Skill tool to load and execute review or verification skills inline. First classify the completed work into one primary workstream, then load the minimum effective execution, review, testing, and verification skills.

2. **Route to the minimum effective post-apply skills**

   - **Backend code writing**
     - Execution/fix: `implement` for minimal follow-up fixes required by critical findings.
     - Verification baseline: `openspec-verify-change` only on the archive-ready path. Skip it on the manual-validation handoff path because user/external verification tasks may remain intentionally unchecked.
     - Code review: `java-code-review` for Java/Spring work. Add `code-review` only when a broader standards/spec diff review would add signal.
     - Testing: `tdd` and `test-quality` when changed behavior needs meaningful regression coverage. Add `api-tester` when API contracts or integration behavior changed.
     - Optional structure context: `codebase-design`, `spring-boot-patterns`, `design-patterns`, `jpa-patterns`, or `api-contract-review` only when the findings point there.

   - **Frontend code auto-generation**
     - Execution/fix: `implement` for minimal follow-up fixes required by critical findings.
     - Verification baseline: `openspec-verify-change` only on the archive-ready path. Skip it on the manual-validation handoff path because user/external verification tasks may remain intentionally unchecked.
     - UI review: `ui-ux-pro-max` is mandatory for HTML/CSS/UI work.
     - Testing: `webapp-testing` for rendered browser behavior.
     - Add `frontend-design` only when the review reveals a visual-direction or layout-language problem that needs design-level guidance.
     - Add `ui-styling` only when the stack uses component-level styling systems such as Tailwind/shadcn or when styling constraints are implementation-critical.
     - Do not load `web-artifacts-builder` unless the deliverable is specifically a Claude HTML artifact build pipeline.
     - Add `code-review` only when a broader code-bearing diff review would add signal beyond UI and OpenSpec verification.

   - **Technical-solution or knowledge-content writing**
     - Execution/fix: `implement` only when findings require direct file fixes.
     - Verification baseline: `openspec-verify-change` only on the archive-ready path. Skip it on the manual-validation handoff path because user/external verification tasks may remain intentionally unchecked.
     - Document quality baseline: `doc-coauthoring`.
     - Add `research` only for fact-heavy claims.
     - Add `domain-modeling` when terminology, concept boundaries, or ADR consistency matter.
     - Add `teach` only for tutorial or instructional content.
     - Add `internal-comms` only for stakeholder-facing or internal update formats.
     - Do not pretend code-style checks alone are sufficient for content-heavy deliverables.

3. **Core skill selection priority**

   1. `openspec-verify-change` - the mandatory workflow-alignment baseline before archive on the archive-ready path only.
   2. `implement` - only when critical findings require minimal follow-up fixes.
   3. `java-code-review` - for Java/Spring code quality review.
   4. `ui-ux-pro-max` - mandatory for HTML/CSS/UI work.
   5. `webapp-testing` - for rendered browser verification.
   6. `api-tester` - for backend API behavior or contract changes.
   7. `tdd` and `test-quality` - when changed behavior or test updates need stronger regression evidence.
   8. `doc-coauthoring` - the default document-quality review baseline for content deliverables.
   9. `research` and `domain-modeling` - only when factual accuracy or concept boundaries are central to the findings.
   10. `code-review` - supplemental broad standards/spec diff review when it adds signal.
   11. `frontend-design`, `ui-styling`, `teach`, `internal-comms` - conditional specialists, not default always-on skills.
   12. Other review/testing skills - if none of the above is available, use the most specific skill present in the workspace.
   13. Manual inspection - if no review skill exists at all, read every file modified during apply, cross-check each against `proposal.md` and `design.md`, and document what was checked.

4. **Run the review and verification pass**

   - **Archive-ready path:** include `openspec-verify-change` in the gate.
   - **Manual-validation handoff path:** skip `openspec-verify-change` and rely on the workstream-specific review/test gate instead.

   The review must cover:

   - **Logic correctness** - does the implementation match the intent in `proposal.md` and `design.md`?
   - **Edge cases** - are obvious failure paths handled?
    - **Task completeness** - does every checked-off task have corresponding implementation or deliverable updates?
   - **Backend/API correctness** (when backend code changed) - are API contracts, persistence behavior, transaction boundaries, and error paths consistent with the plan?
   - **Regression coverage** - for each new behavior or bug fix, is there a corresponding automated test, or a clearly documented reason why one cannot be added?
   - **No regressions** - do existing tests still pass (run the project's test command if one is available)?
   - **Test quality** - are the new/updated tests behavior-focused, meaningful, and exercising public seams rather than implementation details?
   - **UI/UX quality** (when HTML/CSS is involved) - are accessibility, responsive layout, typography, color contrast, and interaction patterns validated per `ui-ux-pro-max` guidance?
   - **Rendered UI verification** (when browser-facing behavior changes) - was a suitable rendered verification performed, such as Playwright or browser-level checks, instead of relying only on static code inspection?
   - **Content quality** (when the deliverable is technical-solution or knowledge content) - are structure, audience fit, terminology consistency, and reader clarity strong enough for the intended readers?
   - **Fact validation** (when the deliverable contains technical or knowledge claims) - were key claims checked against project context or reliable sources instead of being left as unsupported assertions?

   Present findings in this format:

   ```
   ## Review: <change-name>

   ### Findings
   - [CRITICAL] <issue description>
   - [WARNING] <issue description>
   - [INFO] <observation>

   ### Summary
   <overall assessment - one or two sentences>
   ```

5. **Act on findings**

   - **No CRITICAL issues:**
     - If there are WARNINGs, list them and ask the user whether to fix them now or proceed.
     - Once the user decides, continue to Step 6.

   - **One or more CRITICAL issues:**
     - Do not proceed to archive.
     - Report each critical issue with its location (`file_path:line_number` where applicable).
     - Fix them now using the minimum scoped file change needed to resolve the issue.
      - If the critical issue is missing or inadequate test coverage, add or improve the smallest meaningful automated test before re-running review.
      - After fixing, re-run the same verification path that applied to this handoff:
        - archive-ready path -> re-run `openspec-verify-change` plus the same workstream-specific review/testing path
        - manual-validation handoff path -> re-run the same workstream-specific review/testing path only
      - Once no CRITICAL issues remain, continue to Step 6.

6. **Choose the correct post-review outcome**

    - **If remaining tasks are only user/external verification tasks:**
      - Do not archive yet.
      - Hand off to the user only after the automated review/test/verification pass is clean enough to proceed.
      - State clearly that the implementation has passed the automated gate and the next step is manual/external verification.
      - Tell the user to resume the workflow after SIT/UAT/manual validation is complete so the remaining tasks can be checked off and archive can proceed.
      - Do not treat those intentionally open user/external verification tasks as CRITICAL by themselves; only agent-completable implementation gaps or failing automated checks should block the handoff.

   - **If all tasks are complete (`state: "all_done"`):**
     - Announce: `Review passed. Archiving change...`
     - Execute `/opsx/archive` for the same change name already known from the apply session. Do not ask the user for the change name again.
     - The archive command will handle delta-spec sync check, task completion check, directory move, and summary output. Let it run to completion.

7. **Confirm the handoff or completion**

   Before the final message, use a summary skill only when it improves the archive handoff or the manual-validation handoff:

   - **Code-dominant changes** - use `changelog-generator` when a concise code change summary would make the archive easier to review.
   - **Cross-functional or content-heavy changes** - use `handoff` when a short, structured completion note would help the next reader understand scope, decisions, and follow-up context.

   - **If archiving now:**
     - Print the archive summary from `/opsx/archive`, then append:

       ```
       Workflow complete: propose -> apply -> review -> archive
       ```

   - **If handing off to user/external verification:**
     - Summarize the automated review/test result briefly, then append:

       ```
       Automated review complete: proceed with SIT/UAT/manual verification
       ```

## Guardrails

- Trigger Hook B before the user spends time on SIT/UAT/manual verification when implementation work is already complete and only external validation remains.
- Do not trigger Hook B for ordinary paused mid-way implementation states.
- Never skip the review step, even if the implementation looks clean.
- `openspec-verify-change` is the workflow-alignment baseline before archive, but skip it for the manual-validation handoff path where user/external verification tasks intentionally remain open.
- When the implementation involves HTML/CSS styling, `ui-ux-pro-max` is mandatory.
- When behavior changes, do not treat existing green tests as automatically sufficient - verify whether new or changed behavior has targeted coverage.
- When tests are added or changed, review their quality; avoid placeholder, tautological, or implementation-coupled tests.
- Never claim verification passed without fresh evidence from the relevant test, build, browser-level command, or OpenSpec verification pass.
- Use the minimum effective skill set for the active workstream. Do not load every adjacent review skill just because it exists.
- Backend, frontend, and technical/knowledge content must each use workstream-appropriate skills.
- For technical-solution or knowledge-content changes, do not pretend code review alone is sufficient - perform structure, fact, and reader-clarity checks.
- Do not send the user to manual verification while obvious automated review/test failures are still unresolved.
- Never archive with unresolved CRITICAL issues.
- WARNING-level issues require a user decision - do not silently ignore or silently fix them.
- If `/opsx/archive` fails (for example, archive already exists), surface the error and options to the user; do not force-proceed.
