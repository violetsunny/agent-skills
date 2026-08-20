---
name: opsx-workflow-hooks
description: |
  Post-command hooks for the opsx workflow.
  - Trigger A: immediately after /opsx/propose finishes generating all
    artifacts - enters an iterative refinement loop, asking the user if they
    have new ideas and updating proposal artifacts until the user is satisfied.
  - Trigger B: immediately after /opsx/apply completes ALL tasks (state:
    all_done) - runs a workstream-aware review and verification pass, fixes
    critical issues, then runs /opsx/archive to archive the change. Does NOT
    trigger when apply is paused mid-way.
  Use when "/opsx/propose is done", "proposal artifacts created", "all tasks
  complete after apply", "apply finished", or "implementation complete".
---

# OPSX Workflow Hooks

Post-completion behavior injected after `/opsx/propose` and `/opsx/apply`.

## Runtime Entry Points

- Trigger A - after `/opsx/propose`, read and follow `references/hook-a-after-propose.md`.
- Trigger B - after `/opsx/apply` reaches `state: "all_done"`, read and follow `references/hook-b-after-apply.md`.
- If apply is paused mid-way, Hook B does nothing.

## Change Discipline

- Keep `~/.agents/skills/opsx-workflow-hooks/` and `agent-skills/skills/opsx-workflow-hooks/` in sync.
- Use the minimum effective skill set for the active workstream; do not load adjacent skills just in case.
- Hook A is planning-only. Never edit project code there.

## References

- Operational instructions: `references/hook-a-after-propose.md`, `references/hook-b-after-apply.md`
- Design rationale: `references/design-decisions.md`, `references/phase-map-rationale.md`
