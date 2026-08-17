# robot-aiot-self-skill-sync Specification

## Purpose
规范 robot-aiot-self-skill-sync 技能模块 2 在执行 OpenSpec init/update 后对多工具目录同步、拋留文件处理、profile 完整性检查、deselect 文件跟踪和 Codex 特殊行为处理的要求。

## Requirements

### Requirement: 多工具目录生成状态检查

模块 2 在 `openspec init` 或 `openspec update` 完成后，SHALL 检查 OpenSpec 为所有已配置工具生成的目录状态，不仅限于 `.claude` 和 `.agents`。其中 `.claude` 仍 SHALL 作为 OpenSpec 更新后的迁移来源，`.agents` 仍 SHALL 作为运行时目标目录；其他工具目录仅记录生成状态，不参与 `.agents` 迁移。

#### Scenario: 所有工具目录同步成功

- **WHEN** `openspec init` 或 `openspec update` 输出 `Setup complete for <tool>` 或 `Updated <tool>` 对所有已配置工具
- **THEN** 模块 2 SHALL 在汇总中列出所有已配置工具名称及其状态（成功/跳过/失败）
- **AND** SHALL 在 OpenSpec 更新完成后继续执行 `~/.claude/commands/ -> ~/.agents/commands/` 与 `~/.claude/skills/ -> ~/.agents/skills/` 的迁移

#### Scenario: 检测到未同步的工具目录

- **WHEN** `openspec init` 或 `openspec update` 的输出中包含除 `.claude` 和 `.agents` 之外的工具目录（如 `.codebuddy`、`.cursor`、`.gemini`、`.github`、`.lingma`、`.trae`）
- **THEN** 模块 2 SHALL 在汇总中报告这些目录的存在和生成状态，但不 SHALL 自动同步这些目录到 `.agents`（这些目录由 OpenSpec 直接管理）
- **AND** SHALL 仅对 `.claude -> .agents` 执行迁移，其他工具目录不参与迁移

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

模块 2 的结果汇总 SHALL 包含所有新增检查项的汇总信息，并明确区分 `.claude` 与其他工具目录的生成状态，以及 `.claude -> .agents` 迁移步骤的执行结果。

#### Scenario: 完整汇总报告

- **WHEN** 模块 2 执行完毕
- **THEN** 汇总 SHALL 包含以下字段：CLI 升级前后版本、当前 profile 及其完整性状态、已配置工具列表及各自状态、`.claude -> .agents` 的 commands/skills 迁移结果、`[OVERWRITE]` 覆盖的 skills 列表、`[CODEX-LEFTOVER]` 拋留文件数、deselected 删除的 command/skill 文件数、Codex 特殊状态
- **AND** SHALL 在汇总中说明其他工具目录仅记录生成状态，不参与 `.agents` 迁移

### Requirement: 模块 4 备份同步到 .claude/skills/

模块 4 在完成所有同步步骤后，SHALL 继续将 `~/.agents/skills/` 全量同步到 `~/.claude/skills/` 作为运行时备份，确保 `.claude/skills/` 与 `.agents/skills/` 保持一致。该备份步骤 SHALL 保留，但其结果需要与模块 2 的 `.claude -> .agents` 迁移步骤分开记录。

#### Scenario: 模块 4 末尾备份同步

- **WHEN** 模块 4 完成步骤 4.1-4.3（知识库同步和变更报告）
- **THEN** SHALL 执行 `rsync -r ~/.agents/skills/ ~/.claude/skills/` 将 `.agents/skills/` 全量同步到 `.claude/skills/`
- **AND** SHALL NOT 使用 `--delete`（保留 `.claude/skills/` 中可能存在的额外文件）
- **AND** SHALL 在汇总中报告备份同步的 skill 数量
- **AND** SHALL 在汇总中说明该步骤是模块 4 的备份同步，而不是 OpenSpec 直接生成动作

#### Scenario: 备份同步不影响模块 2 权威性

- **WHEN** 下次模块 2 执行 `openspec update` → `.claude/skills/ → .agents/skills/`
- **THEN** OpenSpec SHALL 有权覆盖 `.claude/skills/` 中的任何内容（OpenSpec 仍是 OpenSpec 生成 skills 的权威源）
- **AND** 备份同步的目的是保持 `.claude/skills/` 与运行时 `.agents/skills/` 一致，不改变权威源关系

#### Scenario: 模块 2 同步范围注明

- **WHEN** 模块 2 执行 `.claude/skills/ → .agents/skills/` 同步
- **THEN** 该同步 SHALL 覆盖 `~/.claude/skills/` 中所有已存在的 skill 到 `~/.agents/skills/`
- **AND** SHALL 在段落中注明：模块 3 维护的 skills 的最新性由模块 3 保证，`.claude/skills/` 的运行时备份由模块 4 保证

### Requirement: matt-skills 自动安装

模块 3 在处理 matt-skills 时，SHALL 自动执行 `npx skills@latest add mattpocock/skills` 安装到 `~/.agents/skills/`，不再要求用户手动操作。安装失败时 SHALL 记录错误并继续执行后续项目，不中断整体流程。

#### Scenario: 自动安装成功

- **WHEN** 模块 3 执行到 matt-skills 项目
- **THEN** SHALL 自动执行 `npx skills@latest add mattpocock/skills`
- **AND** SHALL 在汇总中标记 `[NPX-AUTO]` 并报告安装的 skill 数量

#### Scenario: 自动安装失败

- **WHEN** `npx skills@latest add mattpocock/skills` 执行失败（网络超时、npm 错误等）
- **THEN** SHALL 在汇总中标记 `[NPX-FAILED]` 并记录错误信息
- **AND** SHALL NOT 中断后续项目的同步
- **AND** SHALL 提示用户稍后可手动重试 `npx skills@latest add mattpocock/skills`

### Requirement: gstack 知识库同步

模块 4 SHALL 将 `self/skills/gstack/.agents/skills/` 下的所有 skill 同步到知识库 `agent-skills/skills/`。gstack 的 skill 源路径为项目内的 `.agents/skills/` 目录（完整路径 `/Users/kangll13/aiot/java-code/self/skills/gstack/.agents/skills/`），不是常见的 `skills/` 目录，需在步骤 4.1A 的遍历逻辑中明确处理此路径结构。

#### Scenario: gstack 同步到知识库

- **WHEN** 模块 4 步骤 4.1A 遍历 `self/skills/` 下的项目
- **AND** 项目为 gstack 且 `self/skills/gstack/.agents/skills/` 目录存在
- **THEN** SHALL 遍历 `.agents/skills/` 下所有子目录，分别同步到 `agent-skills/skills/{skill_name}/`
- **AND** SHALL 使用 `rsync -r`（不加 `--delete`），只覆盖已有文件和新增文件
- **AND** SHALL 在汇总中报告 gstack 同步的 skill 数量

#### Scenario: gstack 不在模块 3 中同步

- **WHEN** 模块 3 执行 skill 同步到 `~/.agents/skills/`
- **THEN** SHALL NOT 包含 gstack 项目
- **AND** gstack 的同步职责完全由模块 4 承担
