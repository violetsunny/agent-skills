## Why

模块 2 用 `rsync -r --delete` 将 `.claude/skills/` 中所有 skill 同步到 `.agents/skills/`（OpenSpec 生成的 commands 和 skills）。模块 3 从 `self/skills/` 项目更新 `.agents/skills/` 中的部分 skill。数据流为单向，但模块 4 完成后 `.agents/skills/` 的最终状态没有备份到 `.claude/skills/`。需要在模块 4 末尾增加一步，将 `.agents/skills/` 作为运行时备份同步到 `.claude/skills/`。

## What Changes

- **明确模块 2 同步范围**：在模块 2 中注明 `.claude/skills/ → .agents/skills/` 同步是 OpenSpec 生成的 commands 和 skills 的同步，模块 3 维护的 skills 的最新性由模块 3 保证
- **模块 4 新增备份同步步骤**：在模块 4 末尾增加一步，将 `.agents/skills/` 全量同步到 `.claude/skills/` 作为运行时备份，确保 `.claude/skills/` 保持与 `.agents/skills/` 一致
- **明确数据流方向**：模块 2 和模块 3 的同步方向不变（单向），模块 4 的备份同步是额外的全量备份，不改变模块 2/3 的权威源关系

## Capabilities

### New Capabilities
<!-- 无新能力 -->

### Modified Capabilities
- `git-self-update`: 新增「模块 4 备份同步到 .claude/skills/」需求——模块 4 末尾 SHALL 将 `.agents/skills/` 全量同步到 `.claude/skills/` 作为运行时备份

## Impact

- **受影响文件**：`~/.agents/skills/git-self-update/modules/module2-openspec.md`（注明同步范围）、`~/.agents/skills/git-self-update/modules/module4-knowledge-base.md`（新增备份同步步骤）、`~/.agents/skills/git-self-update/modules/summary.md`（汇总新增备份同步报告）
- **同步目标**：`.claude/skills/git-self-update/`、`agent-skills/skills/git-self-update/`
- **无破坏性变更**：不改变模块 1/2/3/3.5 的行为；模块 4 仅新增一步备份同步
