## Context

模块 2 的 `.claude/skills/ → .agents/skills/` 同步是 OpenSpec 生成的 commands 和 skills 的单向同步。模块 3 从 `self/skills/` 项目更新 `.agents/skills/` 中的部分 skill，也在模块 2 之后执行。模块 4 将 `.agents/skills/` 同步到知识库 `agent-skills/skills/`。当前流程中 `.claude/skills/` 在模块 3 更新后不是最新的，用户希望在模块 4 末尾增加一步备份同步。参见 proposal.md 了解问题动机。

数据流（单向 + 模块4备份）：
```
OpenSpec update → .claude/skills/ →(模块2)→ .agents/skills/
                                              ↑
self/skills/     →(模块3 rsync -r --delete)→ .agents/skills/  (覆盖模块2的旧版本)
                                                      ↓
                                        模块4 → agent-skills/skills/
                                        模块4 → .claude/skills/  (备份同步)
```

## Goals / Non-Goals

**Goals:**
- 模块 4 末尾增加备份同步 `.agents/skills/ → .claude/skills/`
- 在模块 2 中注明同步范围和权威源关系
- 保持模块 2/3 数据流单向不变

**Non-Goals:**
- 不在模块 3 中新增反向同步
- 不修改模块 2 的 `.claude/ → .agents/` 同步逻辑本身
- 不改变模块 1/3.5 的行为
- 不修改 OpenSpec CLI 的行为

## Decisions

### 1. 备份同步放在模块 4 末尾

**决策**：在模块 4 完成知识库同步后，增加一步 `rsync -r ~/.agents/skills/ ~/.claude/skills/` 作为运行时备份。

**理由**：模块 4 是最后一个模块，此时 `.agents/skills/` 已包含所有模块的最终更新结果。备份同步确保 `.claude/skills/` 与运行时一致。放在模块 4 而非模块 3，是因为模块 3 只更新部分 skill，而模块 4 备份是全量的。

**替代方案**：在模块 3 中反向同步 → 否决，用户要求单向数据流，备份放模块 4。

### 2. 备份同步不使用 --delete

**决策**：备份同步使用 `rsync -r`（不加 `--delete`），保留 `.claude/skills/` 中可能存在的额外文件。

**理由**：`.claude/skills/` 可能有 OpenSpec 直接生成的文件，不应该被删除。备份只覆盖和新增，不删除。

### 3. 模块 2 注明同步范围

**决策**：在模块 2 的同步段落中注明「模块 3 维护的 skills 的最新性由模块 3 保证，`.claude/skills/` 的运行时备份由模块 4 保证」。

**理由**：不改变任何同步逻辑，只补充文档说明，让执行者理解数据流关系。

## Risks / Trade-offs

- **[风险] 备份同步可能覆盖 `.claude/skills/` 中 OpenSpec 刚生成的内容** → 不会：备份在模块 4（最后），此时 `.agents/skills/` 已包含 OpenSpec 的最新内容（模块 2 同步的）+ 模块 3 的最新内容，备份的是最终状态
- **[风险] 下次 `openspec update` 覆盖备份内容** → 这是预期行为：OpenSpec 是权威源，有权覆盖；备份只是运行时快照
- **[风险] 备份同步增加模块 4 执行时间** → 缓解：rsync 只传输有差异的文件，通常差异不大
