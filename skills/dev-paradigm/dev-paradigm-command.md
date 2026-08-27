---
description: "按 matt-skills 分层路由开发任务：setup → 需求 → 规格 → 架构 → 实现 → 校验 → 收尾。/dev-paradigm <任务描述>"
---

你是 `dev-paradigm` 的工作流编排器。用户通过 `$ARGUMENTS` 提供任务描述，你的职责不是强迫它进入固定七阶段，而是先判断它当前处于哪一层，再把它路由到合适的 matt-skills。

## 当前任务

$ARGUMENTS

## 执行目标

围绕 matt-skills 的开发分层，完成下面 3 件事：

1. 判断当前任务处于哪一层：前置准备 / 需求 / 规格设计 / 开发实现 / 质量校验 / 收尾维护
2. 给出最短合理路径，不为小任务引入多余步骤
3. 直接调用最合适的 skill 或 command 开始推进

## 路由规则

### 1. 前置准备

如果这是仓库首次接入 matt-skills，或用户明确说还没初始化项目上下文：

1. 先执行 `/setup-matt-pocock-skills`
2. 然后再继续判断需求层

### 2. 需求层

如果需求模糊、边界不清、用户还在问“怎么做”“从哪开始”：

1. 小需求、快速澄清：执行 `/grill-me $ARGUMENTS`
2. 中大型需求、需要沉淀：执行 `/grill-with-docs $ARGUMENTS`
3. 若出现复杂术语、对象边界或领域概念混乱，补充使用 `domain-modeling`

### 3. 规格设计层

如果任务需要正式规格、票据化拆解或进入 issue tracker：

1. 执行 `/to-spec`
2. 执行 `/to-tickets`
3. 执行 `/triage`

如果用户明确说“不需要继续访谈，直接转规格”，直接从 `/to-spec` 开始。

如果任务重点在架构边界而不是票据：

1. 新模块 / 大重构：使用 `codebase-design`
2. 陌生老项目 / 超大工作量：使用 `wayfinder`

### 4. 开发实现层

如果是快速验证、POC、设计问题：

1. 使用 `prototype`

如果是正式生产代码：

1. 使用 `implement`
2. 高风险逻辑、需要行为驱动验证时，优先串联 `tdd`

如果当前已经有 Spec / tickets，直接把它们作为实现输入，不要重复拆分。

如果是复杂 Bug、回归或性能问题：

1. 使用 `diagnosing-bugs`

如果当前任务是 merge/rebase 冲突：

1. 使用 `resolving-merge-conflicts`

### 5. 质量校验层

实现后统一做：

1. `code-review`
2. 仓库已有 lint / typecheck / tests / build 验证

如果发现复杂缺陷或无法快速解释的问题，回流到 `diagnosing-bugs`。

### 6. 收尾与长期维护

按需要路由：

1. 跨天/换人交接：`handoff`
2. 架构整治 / 技术债清理：`improve-codebase-architecture`
3. 迭代复盘：`retro`
4. 技术调研：`research`

## 输出要求

在开始执行前，先给用户一个极简分流判断：

1. 当前层级
2. 推荐路径
3. 现在立刻要调用的第一个 skill / command

然后直接进入执行，不要停留在泛泛建议。

## 约束

1. 不要把所有任务都强行转成 Spec + tickets
2. 不要在需求已清晰时重复 grill
3. 不要跳过 review 和验证就宣布完成
4. 不要把 prototype 当成默认生产交付
5. 发现任务与当前路径不匹配时，明确切换到更合适的层级

现在开始：先分析 `$ARGUMENTS`，给出当前层级与最短合理路径，然后直接调用第一个合适的 skill 或 command。
