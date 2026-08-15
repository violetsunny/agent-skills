## Context

git-self-update 技能的模块 2（`modules/module2-openspec.md`）当前只处理 `.claude → .agents` 的单向同步。OpenSpec v1.9.0 实际为 8 个工具生成文件，并在 init/update 输出中包含多个新类型的信息（拋留文件、profile 警告、deselect 删除、Codex 特殊行为），模块 2 未覆盖这些场景。参见 proposal.md 了解问题动机。

当前模块 2 的结构：
1. 确认 profile 并切换
2. `openspec init`（如需要）
3. `npm install -g @fission-ai/openspec@latest` + `openspec --version`
4. `openspec update`
5. 根据输出判定结果
6. `rsync -r --delete ~/.claude/commands/ ~/.agents/commands/`
7. 逐 skill 同步 `.claude/skills/ → .agents/skills/`
8. 运行 `/opsx-workflow-hooks` 恢复 hooks

需要增强的是步骤 5（输出判定）和步骤 6-7 之后（新增检查项），以及汇总报告模板。

## Goals / Non-Goals

**Goals:**
- 增强模块 2 的输出判定逻辑，覆盖 5 个新场景
- 增强汇总报告，包含多工具状态、拋留文件、profile 完整性、deselect 删除、Codex 特殊行为
- 保持 `.claude` 作为权威源不变

**Non-Goals:**
- 不修改模块 1/3/3.5/4 的行为
- 不自动同步其他工具目录（.codebuddy/.cursor 等）到 `.agents`——这些由 OpenSpec 直接管理
- 不自动删除 `.codex/` 拋留文件——仅提示用户
- 不修改 OpenSpec CLI 本身

## Decisions

### 1. 多工具目录：仅报告，不同步

**决策**：模块 2 在 init/update 后检查输出中所有工具的状态，在汇总中报告，但不自动同步其他工具目录到 `.agents`。

**理由**：OpenSpec 为每个工具生成的是该工具特有的格式（如 Codex 用 skills 而非 commands），直接同步到 `.agents` 没有意义。`.agents` 是 workspace-cli 的运行时目录，`.claude` 是 OpenSpec 的权威源，这个关系不变。

**替代方案**：同步所有工具目录到 `.agents`——否决，因为不同工具的文件格式不同，混在一起会冲突。

### 2. `.codex/` 拋留文件：提示用户处理，不自动删除

**决策**：检测到 `Left N files in .codex/` 时，在汇总中标记 `[CODEX-LEFTOVER]` 并提示用户比对后删除。

**理由**：拋留文件可能是用户自定义的内容，自动删除可能丢失用户定制。与保护目录规则一致——不确定时不自动操作。

### 3. Profile 缺失 workflow：自动切换到 core

**决策**：检测到 `custom profile is missing N core workflow(s)` 时，自动执行 `openspec config profile core` 切换到 core profile，然后重新 `openspec update`。

**理由**：当前技能已要求「切换到更完整的 profile」，core profile 包含所有 core workflows，是最完整的选择。用户之前的 custom profile 可能是历史遗留。

**替代方案**：仅提示用户手动切换——否决，因为技能的目标是自动化批量更新，手动步骤会中断流程。

### 4. Deselect 文件：仅在汇总中报告

**决策**：检测到 `Removed: N command files/skill directories` 时，在汇总中记录数量并提示原因。

**理由**：这些是 OpenSpec 主动删除的（workflow 被 deselect），是预期行为而非异常。只需在汇总中让用户知晓。

### 5. Codex 特殊行为：文档化为正常行为

**决策**：在模块 2 中注明 `Commands skipped for: codex (uses skills)` 是正常行为，不视为错误。

**理由**：避免后续执行者误判 Codex 的 commands 跳过为同步失败。

## Risks / Trade-offs

- **[风险] `openspec config profile core` 可能丢失用户自定义 profile 配置** → 缓解：切换前在汇总中报告原 profile 名称，用户可参考恢复
- **[风险] 新增检查项增加模块 2 执行时间** → 缓解：所有检查仅读取已有输出文本，无额外网络请求或文件 I/O
- **[风险] OpenSpec 未来版本输出格式变化** → 缓解：匹配模式使用关键字而非固定格式，降低格式依赖
