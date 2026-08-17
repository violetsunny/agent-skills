## Why

模块 3 和模块 4 有两处同步方式写错，导致 gstack skill 无法正确同步到知识库，matt-skills 需要用户手动操作而非自动执行。

## What Changes

- **gstack**：从模块 3（同步到 `~/.agents/skills/` 运行时）移到模块 4（同步到 `agent-skills/skills/` 知识库）。gstack 的 skill 源路径为 `self/skills/gstack/.agents/skills/`，需在模块 4 步骤 4.1A 中新增对 `.agents/skills/` 目录结构的处理，明确完整路径避免歧义。
- **matt-skills**：从 `[NPX-MANUAL]`（提示用户手动执行）改为自动执行 `npx skills@latest add mattpocock/skills`，安装失败时记录错误并继续，不中断整体流程。
- 从模块 3 中移除 gstack 条目（3.7），因为它不属于运行时同步。

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `robot-aiot-self-skill-sync`: 修正模块 3 的 matt-skills 自动安装方式和模块 4 的 gstack 知识库同步路径。

## Impact

- Affected docs: `skills/robot-aiot-self-skill-sync/modules/module3-skill-sync.md`, `modules/module4-knowledge-base.md`, `modules/summary.md`
- Affected spec: `openspec/specs/robot-aiot-self-skill-sync/spec.md`
- No project code implementation in this change; planning only
