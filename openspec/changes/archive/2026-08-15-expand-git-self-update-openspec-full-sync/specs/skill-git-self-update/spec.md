## Purpose

定义 `git-self-update` 在 OpenSpec 维度如何切换到更完整的 profile，并同步该 profile 实际生成的完整 commands 与 skills 集合。

## MODIFIED Requirements

### Requirement: OpenSpec profile 必须切换到更完整集合

`git-self-update` 在执行 OpenSpec 初始化与更新时 SHALL 不停留在基础/核心最小 profile。它 MUST 引导用户切换到更完整的 OpenSpec profile，并以该 profile 生成的 commands/skills 作为后续同步源。

#### Scenario: 当前 profile 不是最全

- **WHEN** 当前 OpenSpec profile 仅生成基础 commands 或基础 skills
- **THEN** `git-self-update` 会引导用户切换到更完整的 profile，再继续后续同步流程

#### Scenario: 当前 profile 已是目标 profile

- **WHEN** 当前 OpenSpec profile 已能生成用户要求的完整 commands/skills 集合
- **THEN** `git-self-update` 直接进入同步步骤，而不重复切换 profile

---

### Requirement: 同步范围以 `.claude` 实际生成的完整集合为准

完成 OpenSpec init/update 后，`git-self-update` SHALL 将 `~/.claude/commands/` 与 `~/.claude/skills/` 下由当前 profile 实际生成的完整集合视为权威源，而不是仅同步 `commands/opsx/` 与 `openspec-*` skills 子集。

#### Scenario: 同步完整 commands 集合

- **WHEN** `~/.claude/commands/` 下存在多个命令目录和命令文件
- **THEN** `git-self-update` 会把这些实际存在的 commands 全量同步到 `~/.agents/commands/`，而不是只同步 `commands/opsx/`

#### Scenario: 同步完整 skills 集合

- **WHEN** `~/.claude/skills/` 下存在多个由当前 profile 生成的 skills
- **THEN** `git-self-update` 会把这些实际存在的 skills 全量同步到 `~/.agents/skills/`，而不是只同步 `openspec-*` skills

---

### Requirement: Hook 恢复规则在全量同步后仍然成立

即使同步范围扩大到完整 commands 集合，`git-self-update` 仍 MUST 在同步后恢复并校验 `propose.md` / `apply.md` 的 Hook A / Hook B，且恢复方式 SHALL 保持 append-only，不得修改 `.claude` 权威源正文。

#### Scenario: 全量 commands 覆盖后恢复 hooks

- **WHEN** `~/.agents/commands/` 因全量同步被 `.claude` 覆盖
- **THEN** `git-self-update` 会立即恢复 `propose.md` 和 `apply.md` 的 hook 尾部，并校验恢复结果

---

### Requirement: 完整集合继续同步到当前项目知识库

`git-self-update` 在完成 `.claude -> .agents` 全量同步后 SHALL 继续把完整 commands/skills 集合同步到当前项目 `agent-skills/commands/` 和 `agent-skills/skills/`，同步时不得使用 `--delete` 删除知识库中额外内容。

#### Scenario: 完整 commands 集合同步到知识库

- **WHEN** `.agents/commands/` 更新后
- **THEN** 当前项目 `agent-skills/commands/` 会同步得到同样的完整 commands 集合，并保留知识库附加内容

#### Scenario: 完整 skills 集合同步到知识库

- **WHEN** `.agents/skills/` 更新后
- **THEN** 当前项目 `agent-skills/skills/` 会同步得到同样的完整 skills 集合，并保留知识库附加内容
