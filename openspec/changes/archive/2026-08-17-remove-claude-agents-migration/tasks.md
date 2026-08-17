## 1. Update OpenSpec Planning Artifacts

- [x] 1.1 Update `openspec/specs/robot-aiot-self-skill-sync/spec.md` to preserve `.claude -> .agents` migration and separate it from direct tool generation status
- [x] 1.2 Revise `proposal.md` and `design.md` so they reflect the validated runtime model instead of removing migration

## 2. Revise Skill Documentation

- [x] 2.1 Update `skills/robot-aiot-self-skill-sync/modules/module2-openspec.md` to keep `.claude -> .agents` command and skill sync steps while clarifying workflow/profile and tool-state reporting
- [x] 2.2 Update `skills/robot-aiot-self-skill-sync/modules/module4-knowledge-base.md` to keep `.agents -> .claude` backup sync behavior and describe it separately from OpenSpec generation
- [x] 2.3 Update `skills/robot-aiot-self-skill-sync/modules/shared.md` and `modules/summary.md` so reporting distinguishes direct OpenSpec output status, migration results, warnings, and exceptions

## 3. Validate Documentation Consistency

- [x] 3.1 Review the `robot-aiot-self-skill-sync` skill docs for statements that incorrectly remove or weaken the required `.claude -> .agents` migration
- [x] 3.2 Verify the final wording matches the current OpenSpec workflow/profile model and the validated need to migrate runtime files into `.agents`
