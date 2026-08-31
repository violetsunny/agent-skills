# 模块 5：更新 `docs/skills-overview.md`

> 共享规则见 `modules/shared.md`

**目的**：在所有 skills 同步完成后，更新当前项目中的 `/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/docs/skills-overview.md`，形成统一的技能总览文档，分别展示 `~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/` 三个目录下的技能名称和说明。

### 输出要求

- 文档固定路径：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/docs/skills-overview.md`
- 文档必须分为三部分：
  - **第一部分**：`~/.agents/skills/` 下的技能和说明
  - **第二部分**：`agent-skills/skills/` 下的技能和说明（外部 skill 副本）
  - **第三部分**：`agent-skills/self-skills/` 下的技能和说明（用户自写 skill 真源）
- 每部分至少包含：
  - 扫描目录说明
  - skill 总数
  - 技能名称与简要说明表格
- 技能名称优先读取 `SKILL.md` frontmatter 中的 `name:`；若缺失，再退回 skill 根目录名
- 技能说明优先读取 `description:`；若为空，写 `（无描述）`

### 扫描范围

- 第一部分扫描：`/Users/kangll13/.agents/skills/`
- 第二部分扫描：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`
- 第三部分扫描：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`
- 三部分都应递归查找 `SKILL.md`，兼容存在分类目录的情况
- 只读取各自目录内部的 `SKILL.md`，不得跨目录混扫

### 同步规则

- 模块 5 在模块 2、模块 3、模块 4 全部完成后执行
- 模块 5 只更新 `docs/skills-overview.md` 文档，不修改任何 skill 源目录
- 生成文档时允许整体重写 `docs/skills-overview.md`，但**不得**删除 `~/.agents/`、`agent-skills/skills/` 或 `agent-skills/self-skills/` 中任何文件
- 如果某个 `SKILL.md` frontmatter 缺少 `name` 或 `description`，在文档中按兜底规则展示，并在汇总中计入“缺失字段数量”

### 建议生成步骤

1. 递归扫描三个目录下所有 `SKILL.md`
2. 解析每个文件的 frontmatter，提取 `name` 和 `description`
3. 分别按技能名排序
4. 生成三部分 Markdown 文档并写入 `docs/skills-overview.md`
5. 报告总技能数、缺失描述数、写入路径

### Sub Agent 建议

1. 用 fresh sub agent 递归扫描三个目录下的 `SKILL.md`，提取 `name` / `description` 并折叠多行描述
2. 若技能较多，可并行 sub agents 分别扫描 `~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/`
3. 主线程负责写入 `docs/skills-overview.md` 并给出最终统计，避免扫描上下文与写入上下文混杂

### 建议文档结构

```md
# 技能总览

本文档汇总三个技能目录：`~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/`。

## 第一部分：`~/.agents/skills/`

扫描目录：`/Users/kangll13/.agents/skills/`

共 N 个技能。

| 技能 | 说明 |
|------|------|
| `foo` | ... |

## 第二部分：`agent-skills/skills/`

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`

共 N 个技能。

| 技能 | 说明 |
|------|------|
| `bar` | ... |

## 第三部分：`agent-skills/self-skills/`（用户自写）

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`

共 N 个技能。

| 技能 | 说明 |
|------|------|
| `baz` | ... |
```

### 注意事项

- 若技能较多，应保持文档为单文件，但避免引入与技能分组强耦合的手工分类，优先采用稳定、可重复生成的格式
- 多行 `description` 应在文档中折叠为单行摘要，去除多余换行
- 文档内容以实际扫描结果为准，不依赖人工维护的静态技能列表
