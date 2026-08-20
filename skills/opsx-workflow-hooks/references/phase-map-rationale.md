# Phase Map Design Rationale

This document captures the reasoning behind the current workflow split encoded in `opsx-workflow-hooks`.

## Origin

The hook design still reflects the earlier phase-model idea:

| Phase | Core goal | Current binding |
| --- | --- | --- |
| 0 | Requirement clarification | Hook A, optionally `grill-me` |
| 1 | Proposal/spec solidification | Hook A artifact refinement |
| 2 | Architecture decisions and task shaping | Hook A workstream routing |
| 3 | Implementation execution | `/opsx:apply` |
| 4 | Test and edge-case strengthening | `/opsx:apply`, plus post-apply testing skills |
| 5 | Workstream-aware review | Hook B |
| 6 | Verification and archive | Hook B |

## Key decisions

### Hook A governs pre-implementation only

- Hook A exists to improve planning artifacts after `/opsx/propose`.
- The old idea of "tiny implementation change directly in Hook A" was removed because it violates the planning-only boundary from `openspec-propose`.
- The remaining tiny shortcut is limited to tiny planning-artifact edits.

### Hook A uses conditional skill escalation

- `grill-me` survives from the older model, but only for material ambiguity or unresolved trade-offs.
- Backend planning still centers on `codebase-design` plus narrowly relevant backend design skills.
- Frontend planning still centers on `ui-ux-pro-max`, with `frontend-design` or `ui-styling` only when the artifact change genuinely needs them.
- Content planning still centers on `doc-coauthoring`, with fact or terminology specialists loaded only when justified.

### Hook B now prefers workflow verification over generic review-first routing

- Older drafts prioritized `/review` and then `code-review`.
- The current design uses `openspec-verify-change` as the default workflow-alignment baseline because Hook B is an OpenSpec workflow closer, not a generic PR review assistant.
- `java-code-review` remains important for Java/Spring code quality.
- `code-review` remains available as a supplemental broader standards/spec pass.

### Deliberate exclusions

- `web-artifacts-builder` is not part of the default frontend Hook B route because it is artifact-build specific and too narrow for general UI review.
- `teach` and `internal-comms` are not part of the default content route because they match special output modes, not all technical documents.
- Missing older references such as `brainstorming` and `writing-plans` were not restored because they are unavailable here and the current planning route is already adequately covered by existing skills.

## Practical design rule

When changing this skill, preserve this bias:

1. Keep Hook A planning-only.
2. Keep Hook B verification-first.
3. Prefer replacing an over-broad default skill with a better-fitting one over adding another skill on top.
