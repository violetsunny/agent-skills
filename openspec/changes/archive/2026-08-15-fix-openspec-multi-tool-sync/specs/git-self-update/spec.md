## Purpose

规范 git-self-update 技能模块 2 在执行 OpenSpec init/update 后对多工具目录同步、拋留文件处理、profile 完整性检查、deselect 文件跟踪和 Codex 特殊行为处理的要求。

## ADDED Requirements

### Requirement: 多工具目录生成状态检查

模块 2 在 `openspec init` 或 `openspec update` 完成后，SHALL 检查 OpenSpec 为所有已配置工具生成的目录状态，不仅限于 `.claude` 和 `.agents`。

#### Scenario: 所有工具目录同步成功

- **WHEN** `openspec init` 或 `openspec update` 输出 `Setup complete for <tool>` 或 `Updated <tool>` 对所有已配置工具
- **THEN** 模块 2 SHALL 在汇总中列出所有已配置工具名称及其状态（成功/跳过/失败）

#### Scenario: 检测到未同步的工具目录

- **WHEN** `openspec init` 或 `openspec update` 的输出中包含除 `.claude` 和 `.agents` 之外的工具目录（如 `.codebuddy`、`.cursor`、`.gemini`、`.github`、`.lingma`、`.trae`）
- **THEN** 模块 2 SHALL 在汇总中报告这些目录的存在和生成状态，但不 SHALL 自动同步这些目录到 `.agents`（这些目录由 OpenSpec 直接管理）

### Requirement: `.codex/` 拋留文件处理

当 `openspec init` 或 `openspec update` 输出 `Left N files in .codex/ that differ from the copy in .agents/` 时，模块 2 SHALL 提示用户比对并清理拋留文件。

#### Scenario: 检测到 .codex 拋留文件

- **WHEN** OpenSpec 输出包含 `Left N files in .codex/ that differ from the copy in .agents/. Nothing was overwritten`
- **THEN** 模块 2 SHALL 在汇总中标记 `[CODEX-LEFTOVER]` 并提示用户：「检测到 .codex/ 中有 N 个文件与 .agents/ 不同，请比对后删除 .codex/ 副本」
- **AND** 模块 2 SHALL NOT 自动删除 `.codex/` 中的文件

### Requirement: Profile 完整性检查

模块 2 在 `openspec update` 完成后，SHALL 检查输出中是否包含 profile 缺失 workflow 的警告，并在检测到时执行修复或提示用户。

#### Scenario: 检测到 profile 缺失 core workflow

- **WHEN** `openspec update` 输出包含 `Your custom profile is missing N core workflow(s): <workflow-name>` 或 `Run 'openspec config profile' to add it, or 'openspec config profile core' to use the core set.`
- **THEN** 模块 2 SHALL 执行 `openspec config profile core` 切换到 core profile
- **AND** 切换后 SHALL 重新执行 `openspec update` 确保所有 core workflows 的文件已生成
- **AND** 模块 2 SHALL 在汇总中报告 profile 切换前后状态

#### Scenario: 无 profile 警告

- **WHEN** `openspec update` 输出中不包含 profile 缺失警告
- **THEN** 模块 2 SHALL 跳过 profile 检查步骤，在汇总中标记 profile 状态为 `OK`

### Requirement: Deselected 文件跟踪

模块 2 SHALL 跟踪 `openspec update` 删除的 deselected workflow 文件，并在汇总中报告。

#### Scenario: 检测到删除的 command 文件

- **WHEN** `openspec update` 输出包含 `Removed: N command files (deselected workflows)`
- **THEN** 模块 2 SHALL 在汇总中记录被删除的 command 文件数量
- **AND** SHALL 在汇总中提示用户这些文件因 workflow 被 deselect 而被删除

#### Scenario: 检测到删除的 skill 目录

- **WHEN** `openspec update` 输出包含 `Removed: N skill directories (deselected workflows)`
- **THEN** 模块 2 SHALL 在汇总中记录被删除的 skill 目录数量
- **AND** SHALL 在汇总中提示用户这些目录因 workflow 被 deselect 而被删除

#### Scenario: 无删除

- **WHEN** `openspec update` 输出中不包含 `Removed:` 行
- **THEN** 模块 2 SHALL 在汇总中标记 deselected 文件数为 0

### Requirement: Codex 特殊行为文档化

模块 2 SHALL 文档化 Codex 工具使用 skills 而非 commands 的特殊行为，避免误判为错误。

#### Scenario: Codex commands 被跳过

- **WHEN** `openspec init` 或 `openspec update` 输出包含 `Commands skipped for: codex (uses skills)`
- **THEN** 模块 2 SHALL 在汇总中将 Codex 的 commands 状态标记为 `SKIPPED (uses skills)`，不视为错误

### Requirement: openspec update 汇总报告增强

模块 2 的结果汇总 SHALL 包含所有新增检查项的汇总信息。

#### Scenario: 完整汇总报告

- **WHEN** 模块 2 执行完毕
- **THEN** 汇总 SHALL 包含以下字段：CLI 升级前后版本、当前 profile 及其完整性状态、已配置工具列表及各自状态、`[OVERWRITE]` 覆盖的 skills 列表、`[CODEX-LEFTOVER]` 拋留文件数、deselected 删除的 command/skill 文件数、Codex 特殊状态
