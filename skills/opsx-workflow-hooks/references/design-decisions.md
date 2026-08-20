# Design Decisions for opsx-workflow-hooks

## 2026-08-20 Session Decisions

### 1. Dual-path sync requirement
- Runtime path: `~/.agents/skills/opsx-workflow-hooks/`
- Project copy: `agent-skills/skills/opsx-workflow-hooks/`
- Both must be updated when changing this skill.
- Runtime behavior comes from `~/.agents/`, but the project copy is the durable editable source in this repo.

### 2. Hook instructions are split for readability
- `SKILL.md` stays short and points to the operational references.
- Hook A lives in `references/hook-a-after-propose.md`.
- Hook B lives in `references/hook-b-after-apply.md`.
- Historical reasoning stays in `references/design-decisions.md` and `references/phase-map-rationale.md`.

### 3. Planning boundary is strict in Hook A
- Hook A is planning-only because it runs after `/opsx/propose`.
- Tiny changes are allowed only as tiny planning-artifact edits, not direct project-code edits.
- Any real implementation work must wait for `/opsx:apply`.

### 4. Minimum effective skill set beats skill stacking
- Do not load every plausible skill for a workstream.
- Choose one primary workstream, then load only the smallest set that materially improves the current phase.
- This principle is stronger than historical "phase completeness" instincts from earlier drafts.

### 5. Reused planning-side capability from earlier references
- `grill-me` is still useful in Hook A, but only when requirement understanding or trade-offs are materially incomplete.
- It is not a default step for every wording tweak.

### 6. Updated post-apply verification baseline
- `openspec-verify-change` is now the default workflow-alignment baseline before archive.
- `java-code-review` remains the main Java-specific quality pass.
- `code-review` is now supplemental, not the default baseline for every backend or frontend change.
- Hook B runs before user/external validation when implementation is complete, so SIT/UAT is not the first line of bug discovery.
- On the manual-validation handoff path, skip `openspec-verify-change` rather than forcing incomplete user/external verification tasks through a pre-archive completeness gate.

### 7. Frontend route is intentionally narrower
- `ui-ux-pro-max` is the mandatory core skill for HTML/CSS/UI work.
- `frontend-design` and `ui-styling` are conditional helpers.
- `web-artifacts-builder` is excluded from the generic default route because it is specific to Claude HTML artifact builds, not normal apply-phase frontend review.

### 8. Content route is intentionally narrower
- `doc-coauthoring` is the default document-quality baseline.
- `research` and `domain-modeling` are conditional based on factual density or concept-boundary importance.
- `teach` and `internal-comms` are format-specific specialists, not default always-on content skills.
