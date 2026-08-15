## ADDED Requirements

### Requirement: 模块 4 备份同步到 .claude/skills/

模块 4 在完成所有同步步骤后，SHALL 将 `~/.agents/skills/` 全量同步到 `~/.claude/skills/` 作为运行时备份，确保 `.claude/skills/` 与 `.agents/skills/` 保持一致。

#### Scenario: 模块 4 末尾备份同步

- **WHEN** 模块 4 完成步骤 4.1-4.3（知识库同步和变更报告）
- **THEN** SHALL 执行 `rsync -r ~/.agents/skills/ ~/.claude/skills/` 将 `.agents/skills/` 全量同步到 `.claude/skills/`
- **AND** SHALL NOT 使用 `--delete`（保留 `.claude/skills/` 中可能存在的额外文件）
- **AND** SHALL 在汇总中报告备份同步的 skill 数量

#### Scenario: 备份同步不影响模块 2 权威性

- **WHEN** 下次模块 2 执行 `openspec update` → `.claude/skills/ → .agents/skills/`
- **THEN** OpenSpec SHALL 有权覆盖 `.claude/skills/` 中的任何内容（OpenSpec 仍是 OpenSpec 生成 skills 的权威源）
- **AND** 备份同步的目的是保持 `.claude/skills/` 与运行时 `.agents/skills/` 一致，不改变权威源关系

#### Scenario: 模块 2 同步范围注明

- **WHEN** 模块 2 执行 `.claude/skills/ → .agents/skills/` 同步
- **THEN** 该同步 SHALL 覆盖 `~/.claude/skills/` 中所有已存在的 skill 到 `~/.agents/skills/`
- **AND** SHALL 在段落中注明：模块 3 维护的 skills 的最新性由模块 3 保证，`.claude/skills/` 的运行时备份由模块 4 保证
