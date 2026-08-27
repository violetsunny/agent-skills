---
name: dev-paradigm
description: >
  面向日常工程开发的分层工作流路由 skill：根据任务所处阶段，把需求澄清、规格设计、架构规划、实现、调试、审查、交接和长期维护路由到合适的 matt-skills，而不是强迫所有任务走同一条固定流水线。适用于“这个需求该怎么推进”“从需求到代码怎么分阶段”“该先 grill 还是 to-spec”“Bug / 重构 / 新功能分别怎么走”“完整开发流程怎么编排”“开发范式”“dev-paradigm”等场景。也适用于接手陌生项目、需要先做 setup、领域建模、票据拆分、实现收尾或长期维护规划时的统一入口。
---

# Dev Paradigm

这是一个开发分层路由 skill，不是七阶段强制流水线。

目标只有两个：

1. 先判断任务当前处于哪一层
2. 再把工作路由到最合适的 matt-skills 组合

不要为了“走完整流程”而引入无意义步骤。任务小就走短路径，任务大才补齐规格、票据、架构和治理。

## 总图

```text
前置准备（每仓一次）
→ 需求层
→ 规格设计层
→ 开发实现层
→ 质量校验层
→ 收尾与长期维护
```

## 1. 前置准备

如果仓库还没建立 matt-skills 的项目上下文，先执行一次：

1. `setup-matt-pocock-skills`

预期出口：

1. `CONTEXT.md`
2. ADR 目录
3. issue / triage 标签与约定路径

只有在“每个仓库首次接入”或用户明确说还没初始化时才需要这一步，不要每次开发都重复跑。

## 2. 需求层

先判断需求是否清楚。

### 需求模糊

根据深度选择：

1. 快速澄清、小需求：`grill-me`
2. 中大型需求、需要沉淀文档：`grill-with-docs`

当出现术语混乱、边界不清、对象关系复杂时，补 `domain-modeling`。

出口：

1. 需求清晰
2. 核心术语统一
3. 边界、非目标、约束已显式化

### 需求已清晰

直接进入规格设计层，不重复访谈。

## 3. 规格设计层

这一层的重点不是写文档本身，而是决定是否需要正式规格、票据和架构边界。

### 需要正式规格

按顺序：

1. `to-spec`
2. `to-tickets`
3. `triage`

适用场景：

1. 中大型功能
2. 多人协作
3. 跨天推进
4. 需要进入 issue tracker

出口：

1. 正式 Spec
2. 带阻塞依赖的任务清单
3. 优先级与状态明确

### 需要架构设计

按场景分流：

1. 新模块或大规模重构：`codebase-design`
2. 接手陌生老项目或工作量超大：`wayfinder`
3. 需要补齐领域边界：`domain-modeling`

如果用户只是想把当前对话直接转成规格而不想继续访谈，优先 `to-spec`，不要重复 `grill`。

### 不需要正式规格

小改动、已有明确边界时，直接进入开发实现层。

## 4. 开发实现层

先判断是验证想法，还是正式生产代码。

### 快速验证 / POC

1. `prototype`

用于回答设计问题、验证状态机、验证交互或逻辑，不直接等同于可交付生产代码。

### 正式生产代码

1. `implement`

`implement` 是主入口。需要行为验证时，优先让它串联：

1. `tdd`
2. 实现
3. `code-review`

如果当前已有 Spec 或 tickets，默认直接以它们作为 `implement` 的输入，而不是重新拆解。

### Bug / 回归

1. 简单 Bug：直接修复，但仍要回到质量校验层
2. 复杂 Bug、棘手回归、性能问题：`diagnosing-bugs`

### 合并冲突

1. `resolving-merge-conflicts`

## 5. 质量校验层

实现完成后，统一进入验证收尾。

### 功能与规格符合度

1. 若有 Spec / tickets：逐项对照验收
2. 若无 Spec：对照用户已确认的需求边界验收

### 代码质量

1. `code-review`
2. Java 项目可叠加 `java-code-review`

重点检查两轴：

1. Standards：是否符合项目规范
2. Spec：是否忠实实现需求

### 验证执行

运行仓库已有的：

1. lint
2. typecheck
3. tests
4. build（如果这是交付门槛）

### 问题回流

发现问题后：

1. 一般缺陷回到 `implement`
2. 难复现或复杂根因问题回到 `diagnosing-bugs`

## 6. 收尾与长期维护

### 跨天或换人交接

1. `handoff`

### 定期架构整治 / 技术债清理

1. `improve-codebase-architecture`

### 迭代复盘

1. `retro`

### 技术选型 / 方案调研

1. `research`

## 路由规则

1. 需求模糊先澄清，不猜
2. 小任务默认短路径，不强行补 Spec / tickets
3. 多人协作、跨天推进、陌生领域或复杂依赖时，优先走规格化路径
4. 新模块先考虑 `codebase-design`，陌生老项目先考虑 `wayfinder`
5. 生产代码优先 `implement`，高风险逻辑优先 `tdd`
6. 复杂 Bug 优先 `diagnosing-bugs`，不要跳过复现和根因定位
7. 收尾至少做验收、review、验证；是否交接取决于是否需要跨人/跨天继续

## 推荐路径

### 路径 A：小需求 / 明确改动

1. 需求已清晰
2. 直接 `implement`
3. `code-review`
4. 跑验证

### 路径 B：中大型功能

1. `grill-with-docs`
2. `domain-modeling`（如有必要）
3. `to-spec`
4. `to-tickets`
5. `triage`
6. `implement`
7. `code-review`
8. 跑验证
9. `handoff`（如需）

### 路径 C：陌生项目 / 大规模重构

1. `setup-matt-pocock-skills`（若未初始化）
2. `wayfinder` 或 `codebase-design`
3. `to-spec` / `to-tickets`（若需多人协作）
4. `implement`
5. `code-review`
6. 跑验证
7. `improve-codebase-architecture`（可作为收尾）

### 路径 D：复杂 Bug / 回归

1. `diagnosing-bugs`
2. `code-review`
3. 跑验证
4. `handoff`（如需沉淀）

## 不要这样做

1. 不要把所有任务都强行走完整七阶段
2. 不要在需求已清晰时重复 grill
3. 不要在小修小补上硬拆 Spec 和 tickets
4. 不要跳过 review 和验证直接宣布完成
5. 不要把 `prototype` 产物默认当生产代码交付
