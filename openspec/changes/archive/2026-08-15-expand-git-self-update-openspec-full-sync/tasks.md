## 1. 扩展 OpenSpec profile 与生成物规则

- [x] 1.1 在 `git-self-update` SKILL.md 中补充“最全”以当前启用 profile 在 `~/.claude/commands/` 与 `~/.claude/skills/` 下实际生成内容为准的规则
- [x] 1.2 在 `git-self-update` SKILL.md 中补充：若当前不是目标完整 profile，先切换到更完整 profile，再继续 init/update

## 2. 扩展同步范围到完整 commands / skills 集合

- [x] 2.1 将 OpenSpec commands 同步说明从仅 `commands/opsx/` 扩展为同步 `~/.claude/commands/` 下实际生成的完整集合到 `~/.agents/commands/`
- [x] 2.2 将 OpenSpec skills 同步说明从仅 `openspec-*` 扩展为同步 `~/.claude/skills/` 下实际生成的完整集合到 `~/.agents/skills/`
- [x] 2.3 保留并更新 hook 恢复说明，明确全量覆盖 `commands/` 后仍需 append-only 恢复 `propose.md` / `apply.md` hooks

## 3. 扩展知识库同步范围

- [x] 3.1 在模块 4 中补充将 `.agents/commands/` 的完整集合同步到 `agent-skills/commands/`
- [x] 3.2 在模块 4 中补充将 `.agents/skills/` 的完整集合同步到 `agent-skills/skills/`
- [x] 3.3 将修复后的 `git-self-update` skill 同步到当前项目知识库，并重新报告 `git status --short`
