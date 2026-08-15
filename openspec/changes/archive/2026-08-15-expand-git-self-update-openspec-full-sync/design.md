## Context

当前 `git-self-update` 的 OpenSpec 模块默认围绕 `commands/opsx/` 和 `openspec-*` skills 编写，这只能覆盖基础子集，不能满足用户要求的“最全”集合。See `proposal.md - Why`。

同步链路实际分为三段：

- OpenSpec 在 `~/.claude/` 下生成权威 commands/skills
- 运行时副本同步到 `~/.agents/`
- 当前项目知识库再从 `~/.agents/` 接收同步

扩大同步范围后，最大风险不是复制动作本身，而是：

- profile 仍停留在基础配置，导致源头生成物本来就不全
- 全量覆盖 `commands/` 后丢失 `propose.md` / `apply.md` 的 hook 尾部
- 知识库同步把“从 `.claude` 实际生成什么”与“项目内要保留什么”混为一谈

## Goals / Non-Goals

**Goals:**

- 明确“最全”以当前启用 profile 在 `~/.claude` 下实际生成的文件集合为准
- 在 skill 中补充先切到更完整 profile、再同步完整 commands/skills 的流程
- 保持 hook 恢复逻辑在全量同步后仍可用
- 将完整集合继续同步到当前项目知识库，同时不删除知识库额外内容

**Non-Goals:**

- 不在本次设计中指定某个 OpenSpec 固定版本号
- 不硬编码某个固定 commands 或 skills 名单
- 不修改 `.claude` 权威源文件正文

## Decisions

### 1. “最全”采用运行时枚举，而不是硬编码名单

决定：以 `~/.claude/commands/` 与 `~/.claude/skills/` 下实际存在的内容作为同步源，不再限定为 `opsx/` 或 `openspec-*` 子集。

原因：OpenSpec 的生成物会随 profile、版本、工具集变化，硬编码目录或文件名会再次过时。

备选方案：

- 继续只同步 `commands/opsx/` 和 `openspec-*`
  - 放弃原因：这正是当前问题来源，无法满足“最全”要求。

### 2. profile 切换单独作为前置步骤表达

决定：在 skill 中明确“如当前不是目标 profile，先切 profile，再 init/update，再同步”。

原因：如果 profile 不完整，后续同步做得再对，拿到的仍是基础集合。

备选方案：

- 只在同步阶段检查缺文件
  - 放弃原因：这会把问题滞后到结果阶段，用户无法在前置步骤中一次性纠正环境。

### 3. Hook 恢复保持 append-only

决定：全量同步 `commands/` 后，仍只在 `.agents` 与项目知识库中的 `propose.md` / `apply.md` 末尾恢复 Hook A/B，不反向改 `.claude`。

原因：`.claude` 是权威源；hook 是运行时附加约束，不能污染上游正文。

备选方案：

- 直接把 hook 写入 `.claude`
  - 放弃原因：会破坏上游权威源与后续 update 的一致性。

## Risks / Trade-offs

- [Risk] 全量同步范围扩大后，知识库改动量明显增大
  → Mitigation: 明确不加 `--delete`，并通过 `git status --short` 仅汇总报告，由用户自行审查提交

- [Risk] profile 名称或切换命令未来变化
  → Mitigation: skill 中强调先查看当前可用 profile/配置，而不是写死 profile 名称

- [Risk] commands 全量覆盖后 hook 再次丢失
  → Mitigation: 将 hook 恢复写成同步后的固定步骤，并校验 `propose.md` / `apply.md` 两个文件

## Migration Plan

1. 更新 `git-self-update` skill 对 profile 与全量同步的说明
2. 更新任务清单，覆盖完整 commands/skills 与知识库同步规则
3. 同步修复后的 skill 到当前项目知识库
4. 由用户在下一次实际执行 `/git-self-update` 时验证新规则
