# Org Chart / Responsibility Map（组织架构/职责图）

**最适合：** 人类团队、agent 团队、支持升级地图、角色归属、路由地图，以及任何读者需要知道*谁负责什么*而不只是父 → 子结构的层级。

当节点是人、agent、团队、角色或问责 owner 时，用 **Org Chart** 而非 **Tree**。树表达通用层级；org chart 表达职责、调用路径与覆盖缺口。

## 布局约定
- 根 owner 或"前门"位于顶部居中。用一个 coral 焦点节点标出接收模糊工作的人/团队/agent。
- 第 1 层节点是部门、pod、队列或主路由桶。保持水平对齐。
- 第 2 层节点是责任 owner 或专家。专家超过 8 个时，把他们分组到 pod 节点下，而不是排成一个巨型横排。
- 使用正交连接线：父节点垂直下探 → 水平总线 → 垂直下探到子节点。禁止斜线。
- 空间允许时，每个节点应回答三个问题：
  1. **Name**——人类可读的角色/人/agent，Geist sans。
  2. **How to invoke**——Slack handle、队列、issue 前缀或触发条件，Geist Mono。
  3. **Scope**——2–4 个简洁的职责词，不是一段话。
- 非 Slack / 尚未上线的 owner 用虚线 optional 样式展示，不要隐藏。缺失的路由在运维上是重要信息。
- 升级 / 审批规则放进小型侧注或页脚条，不作为额外的组织节点。

## 节点处理
- **前门 / 指挥中心：** focal 处理（`accent-tint` + `accent`）。
- **团队 / pod / 部门：** backend 处理（白 + `ink`）。
- **单个 agent / owner：** 视其在系统中是否活跃，用 store 或 external 处理。
- **缺口 / 待建立：** optional 虚线处理。
- **审批门：** security 处理，与汇报层级分开。

## 复杂度预算
- 最大可见组织节点：12。超出则做一张总览 org chart + 每个 pod 单独的细节图。
- 最大深度：4 层。
- 单个父节点下最大直接汇报数：5。超出则引入分组节点。
- 最大 coral 节点：1。org chart 的职责是清晰，不是处处高亮。
- 最大侧注数：2。

## 反模式
- 用户的真实问题是"谁做什么？"却用泳道图。泳道解释流程；org chart 解释职责归属。
- 每个人/agent 都画成一模一样的盒子。这会掩盖前门、专家、缺口与升级路径。
- 把完整岗位描述塞进节点。scope 短语保持简短，细节移到下方 summary cards。
- 把不可用 / 未接线的 agent 画成正常活跃 owner。用虚线 optional 样式让缺口可见。
- 节点子标签就能承载调用路径，却在正文段落里重复 Slack handle。
- 组织区域内漂浮的图例。用标准底部图例条。

## 示例
- minimal light
- minimal dark
- full editorial
