## Why

git-self-update 技能的模块 2（OpenSpec 更新）在实际执行中发现 5 个问题：OpenSpec v1.9.0 现在为 8 个工具生成文件（.claude/.agents/.codebuddy/.cursor/.gemini/.github/.lingma/.trae），但模块 2 只同步 `.claude → .agents`；`.codex/` 拋留文件警告无处理指引；`custom profile is missing 1 core workflow: update` 警告未处理；`openspec update` 删除的 deselect 文件未在汇总中报告；Codex "uses skills" 特殊行为未文档化。

## What Changes

- **新增多工具目录同步指引**：模块 2 在 `openspec init/update` 后，除 `.claude → .agents` 同步外，需检查并报告其他工具目录（.codebuddy/.cursor/.gemini/.github/.lingma/.trae）的生成状态
- **新增 `.codex/` 拋留文件处理指引**：当输出 `Left N files in .codex/ that differ` 时，提示用户比对 `.codex/` 与 `.agents/` 副本并删除拋留文件
- **新增 profile 完整性检查**：当输出 `custom profile is missing N core workflow(s)` 时，运行 `openspec config profile core` 或提示用户手动切换
- **新增 deselect 文件跟踪**：当 `openspec update` 输出 `Removed: N command files` / `Removed: N skill directories` 时，在汇总中报告被删除的文件数和 workflow 名称
- **文档化 Codex 特殊行为**：在模块 2 中注明 Codex 使用 skills 而非 commands（`Commands skipped for: codex (uses skills)`），这不是错误

## Capabilities

### New Capabilities
- `git-self-update`: git-self-update 技能的 OpenSpec 更新模块行为规范——多工具目录同步、拋留文件处理、profile 完整性检查、deselect 文件跟踪、Codex 特殊行为

### Modified Capabilities
<!-- 无现有 spec 需要修改 -->

## Impact

- **受影响文件**：`~/.agents/skills/git-self-update/modules/module2-openspec.md`、`~/.agents/skills/git-self-update/modules/summary.md`、`~/.agents/skills/git-self-update/modules/shared.md`
- **同步目标**：`.claude/skills/git-self-update/`、`agent-skills/skills/git-self-update/`
- **无破坏性变更**：不改变模块 1/3/3.5/4 的行为，仅增强模块 2 的 OpenSpec 更新处理逻辑
- **外部依赖**：OpenSpec v1.9.0（已安装）
