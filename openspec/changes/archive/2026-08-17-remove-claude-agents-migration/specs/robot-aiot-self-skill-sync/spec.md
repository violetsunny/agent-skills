## MODIFIED Requirements

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
