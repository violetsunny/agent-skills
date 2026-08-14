# Phase Map Design Rationale

This document captures the reasoning behind the 7-phase workflow encoded in
`opsx-workflow-hooks`. Future sessions should consult this when considering
changes to the phase structure, tool bindings, or hook behavior.

## Origin

The 7-phase model was derived from a user-proposed table mapping stages to
primary tools and exit standards. The user's original framing:

| Phase | Core goal | Primary tools |
| --- | --- | --- |
| 0 | Requirement clarification | `grill-me` |
| 1 | Spec solidification | `to-spec`, OpenSpec |
| 2 | Architecture decisions & task atomization | `brainstorming`, `writing-plans` |
| 3 | Implementation execution | `/opsx:apply`, Superpowers |
| 4 | Test-driven boundary strengthening | TDD + edge-case checks |
| 5 | Layered code review | `/review`, `code-review`, `java-code-review` |
| 6 | Verification & archive | `/opsx:verify`, `/opsx:archive` |

## Key decisions

### Hook A governs phases 0-2 (pre-implementation)

- `grill-me` is the **default phase 0 tool** — only triggered when requirement
  understanding is materially incomplete, not for every minor wording tweak.
- `to-spec` is the **phase 1 bridge** — used only when raw user input is too
  rough for direct OpenSpec artifact edits.
- `brainstorming` is the **default phase 2 tool** for architectural ambiguity.
- `writing-plans` is the **phase 2 tool** for task atomization when tasks.md
  is too coarse to execute.
- Tiny changes (≤5 lines, single file, no structural impact) bypass the full
  `/opsx:apply` flow — they go directly to edit + review.

### Hook B governs phases 5-6 (post-implementation)

- Review priority: `/review` (built-in) → `code-review` → `java-code-review`
  → other review skills → manual inspection.
- For Java/Spring projects, a chained review is preferred when feasible.
- Verification (`/opsx:verify`) must pass before archive.
- CRITICAL issues block archive; WARNINGs require explicit user decision.

### What was deliberately excluded

- `subagent-driven-development` was considered for phase 3 but deemed beyond
  the current minimum scope.
- `requesting-code-review` was considered for phase 5 but adds orchestration
  complexity that isn't needed yet.
- `tdd` and `implement` (Matt skills) were noted as useful future integrations
  for phases 3-4 but not included in the current minimal set.
- The user explicitly said: "Don't stuff all superpowers/matt-skills in at once.
  Minimal and effective is better."

## Bootstrap necessity

OpenSpec updates can overwrite `~/.agents/commands/opsx/propose.md` and
`apply.md`, which erases the hook injection blocks. The bootstrap section
solves this by making the skill self-healing: when invoked directly, it checks
and re-injects the missing hooks before proceeding.

## Dual-path sync

Runtime reads from `~/.agents/` (commands + skills). Project source lives in
`agent-skills/`. **Both must be updated** when changing opsx commands or skills.
Forgetting to sync is the most common cause of "hooks not triggering."
