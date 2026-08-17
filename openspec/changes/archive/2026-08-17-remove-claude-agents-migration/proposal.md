## Why

实际验证表明，`robot-aiot-self-skill-sync` 仍需要把 OpenSpec 在 `~/.claude/commands/` 与 `~/.claude/skills/` 生成的内容迁移到 `.agents` 运行时目录。当前问题不在于要不要迁移，而在于文档中对 profile/workflow 完整性、多工具目录状态、异常记录，以及模块 4 回写边界的描述已经和现状混杂，容易误导后续维护。

## What Changes

- 保留模块 2 中 `~/.claude/commands/ -> ~/.agents/commands/` 与 `~/.claude/skills/ -> ~/.agents/skills/` 的迁移要求，并明确这是运行时所需步骤。
- 调整模块 2 的目录检查逻辑：区分“OpenSpec 直接生成的多工具目录状态”和“`.claude -> .agents` 的额外迁移步骤”，两者都要记录。
- 保留模块 4 中 `~/.agents/skills/ -> ~/.claude/skills/` 的备份同步要求，不改动该行为边界。
- 更新汇总与告警口径，明确 profile/workflow 数量、各工具目录生成状态、迁移执行结果、异常与 skipped 信息，避免把“生成状态”和“迁移状态”混为一谈。

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `robot-aiot-self-skill-sync`: 修正 OpenSpec 相关模块的规划说明，保留 `.claude -> .agents` 迁移与模块 4 备份同步，同时强化 profile/workflow、工具目录状态与异常记录要求。

## Impact

- Affected docs: `skills/robot-aiot-self-skill-sync/modules/module2-openspec.md`, `modules/module4-knowledge-base.md`, `modules/shared.md`, `modules/summary.md`
- Affected spec: `openspec/specs/robot-aiot-self-skill-sync/spec.md`
- Affected runtime behavior: OpenSpec 更新后的检查、`.claude -> .agents` 迁移记录、知识库同步边界
- No project code implementation in this change; planning only
