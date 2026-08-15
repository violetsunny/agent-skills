## Why

当前 `git-self-update` 只同步了 `commands/opsx/` 和 `openspec-*` skills，这对应的是一部分 OpenSpec 生成物，而不是用户要的“最全”集合。用户明确要求先切到更完整的 OpenSpec profile，再把该 profile 实际生成的全部 commands 和 skills 同步到 `.agents` 与当前项目知识库，避免只拿到基础命令和基础技能。

## What Changes

- 调整 `git-self-update` 的 OpenSpec 模块：先切换到更完整的 OpenSpec profile，而不是停留在基础/核心最小集合
- 将同步范围从 `commands/opsx/` + `openspec-*` skills 扩大为 OpenSpec init/update 在 `~/.claude/commands/` 与 `~/.claude/skills/` 下生成的完整集合
- 明确“最全”的判定方式：以当前已启用 profile 在 `~/.claude` 目录下实际生成的文件集为准，而不是硬编码目录名或仅同步 opsx
- 保留 Hook A / Hook B 的 append-only 恢复规则，避免全量覆盖后丢失本地运行时 hook
- 同步后的完整 commands/skills 继续同步到当前项目 `agent-skills/commands/` 与 `agent-skills/skills/`

## Capabilities

### New Capabilities

（无新能力）

### Modified Capabilities

- `skill-git-self-update`: 扩展 OpenSpec profile 选择与全量生成物同步规则，使 skill 能同步完整 commands/skills 集合，而非仅基础 opsx 和 openspec-* 子集

## Impact

- `~/.agents/skills/git-self-update/SKILL.md`
- `agent-skills/skills/git-self-update/`
- `~/.agents/commands/`
- `agent-skills/commands/`
- `~/.agents/skills/`
- `agent-skills/skills/`
