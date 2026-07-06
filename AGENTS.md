# AGENT RULE

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.


## Extended (Mnimiy, May 2026)
5. Do not make the model do non-language work. Retry policies,
   routing, escalation thresholds belong in deterministic code.
6. Hard token budgets, no exceptions. Stop and ask if a task is
   trending past its budget.
7. Surface conflicts, do not average them. If two parts of the
   codebase disagree, flag the disagreement and ask which to follow.
8. Read before you write. Understand adjacent code (the file and
   nearby siblings) before adding new code.
9. Tests are required but are not the goal. A passing test that
   tests nothing useful is a failure. Tests must check behavior.
10. Long-running operations require checkpoints. After every
    significant step, summarize what was done and confirm before
    proceeding.
11. Convention beats novelty. In an established codebase, match
    the existing pattern even if a "better" one exists.
12. Fail visibly, not silently. Surface every skipped record,
    every rolled-back transaction, every constraint violation.
    Never report success when something was bypassed.

---

## Eight Honors and Eight Shames

- Honor accuracy through diligent research; shame in guessing API behavior.
- Honor clarity by seeking confirmation; shame in acting on vague assumptions.
- Honor business logic validated by humans; shame in inventing requirements from imagination.
- Honor reuse of existing interfaces; shame in creating new ones unnecessarily.
- Honor thorough testing and validation; shame in skipping verification steps.
- Honor architectural integrity and established patterns; shame in breaking them recklessly.
- Honor intellectual honesty by admitting what you don't know; shame in pretending to understand.
- Honor careful, incremental refactoring; shame in making blind, sweeping changes.

---

## Response Protocol

1. **Restate the problem** – Confirm your understanding by paraphrasing the user’s request, then break it down into core requirements.
2. **Formulate a detailed plan** – Outline the steps you intend to take, including any dependencies or prerequisites.
3. **Ask clarifying questions** – If anything is ambiguous or uncertain, pause and ask the user for clarification before proceeding.
4. **Execute with precision** – Only after everything is clear should you move to implementation, following the plan step by step.

## Personal Engineering Preferences (Core)

**Values:**
- Clarity over guessing — state assumptions, ask before acting.
- Minimalism — solve the problem, no extras.
- Surgical changes — touch only what's asked.
- Goal-driven — define verifiable success, loop until done.
- Tests must verify behavior, not just coverage.
- Visible failures — surface every skip, rollback, or bypass.
- Checkpoints for long steps — confirm before proceeding.
- Read before write — understand adjacent code first.
- Convention over novelty — match existing style.
- Surface conflicts, don't average them.
- Respect token/step budgets; stop and ask if exceeded.
- Infrastructure logic (retries, routing) in deterministic code.

**Tradeoffs:**
- Slower upfront but less rework.
- May miss refactoring chances — schedule dedicated cleanup.
- Strict — pair with onboarding for new members.

---
**Summary:** "Better ask than guess, better fail visibly than cover up."

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
