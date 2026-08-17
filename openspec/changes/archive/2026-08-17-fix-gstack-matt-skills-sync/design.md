## Context

See `proposal.md` for motivation. 当前 gstack 被错误放在模块 3（同步到 `~/.agents/skills/` 运行时），但 gstack 的 skill 应直接同步到知识库 `agent-skills/skills/`，属于模块 4 的职责。matt-skills 当前标记为 `[NPX-MANUAL]` 要求用户手动执行 npx 命令，但用户希望自动执行。

## Goals / Non-Goals

**Goals:**
- gstack 从模块 3 移除，在模块 4 步骤 4.1A 中新增 `.agents/skills/` 目录结构处理
- matt-skills 从 `[NPX-MANUAL]` 改为自动执行，失败时记录错误不中断

**Non-Goals:**
- 不修改其他项目（superpowers、claude-code-java 等）的同步方式
- 不修改模块 1 的 git pull 逻辑
- 不修改模块 4 的备份同步步骤 4.4

## Decisions

### 1. gstack 放在模块 4 而非模块 3

gstack 的 54 个 skill 是知识库内容，不需要运行时加载。放在模块 4 步骤 4.1A 中，扩展遍历逻辑以识别 `.agents/skills/` 目录结构。

备选方案：保留在模块 3 但改同步目标为知识库。

不采用原因：模块 3 的职责是同步到 `~/.agents/skills/` 运行时目录，混入知识库同步会破坏模块边界。

### 2. matt-skills 自动执行 npx

直接在模块 3 中自动执行 `npx skills@latest add mattpocock/skills`，不再输出 `[NPX-MANUAL]` 提示。npx 是交互式命令，但可以通过管道或 `--yes` 标志实现非交互执行。

备选方案：保留手动模式但增加重试提示。

不采用原因：用户明确要求自动执行，不希望自己手动操作。

### 3. 模块 4 步骤 4.1A 扩展第三种目录结构

当前 4.1A 只处理两种结构：`SKILL.md` 直接结构和 `skills/` 二级结构。新增第三种：`.agents/skills/` 结构，专门用于 gstack。

## Risks / Trade-offs

- [风险] npx 交互式命令在非交互环境中可能挂起 → Mitigation: 设置超时，超时后标记 `[NPX-FAILED]` 并继续
- [风险] gstack 的 `.agents/skills/` 路径与其他项目冲突 → Mitigation: 只在 gstack 项目名下检查此路径，不泛化
- [风险] 4.1A 脚本新增第三种结构增加复杂度 → Mitigation: 保持按项目名精确匹配，不做模糊推断
