---
name: robot-aiot-leadership-ppt-workflow
description: >
  将项目数据和技术分析转化为结构化的领导汇报PPT，覆盖全链路五阶段工作流：
  数据池建立 → 技术明细版+领导汇报版文档分层 → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图XML →
  调用 robot-aiot-xml-html-bridge 将XML稳定转HTML并保留原样式 → PPT母稿逐页HTML化 → 调用 ppt-master 依据每页HTML样式生成最终PPTX文件。
  当用户要求"写领导汇报PPT"、"出PPT母稿"、"做汇报材料"、"汇报方案"、"写PPT"、
  "领导汇报"、"生成汇报PPT"时触发。也适用于用户描述了需要将技术项目数据
  转化为管理层可读的汇报格式的场景。
---

# Robot AIoT 领导汇报 PPT 工作流

将技术项目数据转化为领导可读的 PPT 汇报，核心原则：
**让领导一目了然，一眼看懂** — 每页必须有业务价值结论 + 数据支撑，
不讲代码实现。

本技能覆盖从原始数据到最终 PPTX 的全链路，涉及三个外部技能调用：
- **robot-aiot-draw-flowchart** — 在文档分层完成后，生成分层架构图/流程图 XML
- **robot-aiot-xml-html-bridge** — 在 XML 生成后，稳定转换为 HTML 预览稿，作为 PPT 前的主约束
- **ppt-master** — 在母稿逐页 HTML 化后，读取逐页 HTML/MD 生成最终 PPTX 文件

Sub agent 原则：
- 非 trivial 的阶段分析、分层提炼、图表规划、页面草拟、交叉校验，优先交给 fresh sub agent 执行，保持上下文干净
- 主线程只做总控：阶段切换、用户确认、真实文件落盘、跨阶段一致性校验、外部技能调用与最终交付判断
- tiny wording tweak、单页局部小改、局部格式修正可直接在主线程完成，不必起 sub agent

强制中间层原则：
- **XML 先转 HTML**：凡是由 `robot-aiot-draw-flowchart` 生成的图表 XML，在进入 PPT 阶段前必须先通过 `robot-aiot-xml-html-bridge` 转成 HTML 预览文件
- **母稿逐页转 HTML**：在调用 `ppt-master` 之前，必须把 PPT 母稿的每一页都落成单页 HTML
- **按 HTML 转 PPT**：ppt-master 读取逐页 HTML/MD 生成 PPTX，HTML 是 ppt-master 的直接输入格式
- **没有 HTML 不得生成 PPT**：只要图表 HTML 或页面 HTML 未完成，PPT 生成阶段不得开始

---

## 输出目录约定

所有输出产物统一放在当前运行项目的 `doc-ppt/` 目录下，不散落到其他位置。

```
doc-ppt/
├── assets/                     — 品牌静态资源（Logo 等）
│   └── midea-logo.png          — 美的品牌 Logo（从 skill assets/ 复制）
├── <chart-name>.xml            — 图表 XML（Phase 3，robot-aiot-draw-flowchart 产出）
├── <chart-name>.html           — 图表 HTML（Phase 3.5，robot-aiot-xml-html-bridge 产出）
├── <project>_PPT母稿.md        — 母稿（Phase 4）
├── pages/                      — 逐页 HTML（Phase 4）
│   ├── 01-cover.html
│   ├── 02-overview.html
│   └── ...
└── <project>.pptx              — 最终 PPTX（Phase 5，ppt-master 产出）
```

---

## 品牌资源（静态资产）

输出目录、Logo 复制方式、尺寸建议和配色协调规则见 `references/brand-assets.md`。
主文件只保留入口约束：

1. 所有产物统一落在 `doc-ppt/`
2. Phase 4 开始前把 `assets/midea-logo.png` 复制到 `doc-ppt/assets/`
3. 封面页与内容页页脚必须嵌入 Logo，且不得遮挡标题、结论或关键数据

---

## 工作流总览

```
Phase 1: 方案基础     → 提取真实指标，建立统一数据池（单一数据源）
Phase 2: 受众分层     → 技术明细版MD + 领导汇报版MD（同一数据，不同表达）
Phase 3: 图表生成     → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML
Phase 3.5: 桥接转换  → 调用 robot-aiot-xml-html-bridge 将 XML 稳定转 HTML 并保留原样式
Phase 4: PPT母稿     → 按页结构化：标题→结论→数据→话术，并将每页落成 HTML 页面样式
Phase 5: PPT生成     → 调用 ppt-master，读取逐页 HTML/MD 生成最终 PPTX
```

每个阶段产出是下一阶段的输入，逐级收敛。

建议执行方式：每个阶段先由 sub agent 在干净上下文中完成本阶段分析/起草/审查，再回到主线程做统一落盘和阶段阻塞检查，避免 Phase 1-5 信息互相污染。

---

## Phase 1: 方案基础 — 数据池建立

详细规则、单/多数据源模板、估算值和合并口径约束见 `references/phase1-data-pool.md`。

执行时只抓三件事：

1. 先建唯一数据源，再写任何页面
2. 每个数字都能追溯来源，估算值显式加 `~`
3. 多数据源先统一口径，再进入后续阶段

---

## Phase 2: 受众分层 — 技术明细版 + 领导汇报版

文档结构、术语映射模板和业务化翻译规则见 `references/phase2-audience-layering.md`。

入口约束：

1. 先写技术明细版，再提炼领导汇报版
2. 两份文档共用同一数据池
3. 领导汇报版不得直接暴露表名、类名、API 路径或无解释缩写

---

## Phase 3 / 3.5: 图表生成与桥接转换

图表类型选择、XML/HTML 产物、阻塞规则与协作边界见 `references/phase3-chart-pipeline.md`。

主文件保留五条硬约束：

1. Phase 3 先调用 `robot-aiot-draw-flowchart` 生成图表 XML 真源
2. Phase 3.5 必须调用 `robot-aiot-xml-html-bridge` 为每个 XML 生成对应 HTML
3. 没有图表 HTML，不得进入 Phase 4
4. 首页架构图确定全局主色基调，后续页面保持配色统一但允许版式多样
5. 允许在 Phase 3.5 和 Phase 4 做轻量 Material 3 规范化，但只能整理 token、字体层级、间距和容器语义，不能改图表结构和数据语义

---

## Phase 4: PPT母稿 — 按页结构化

母稿模板、逐页 HTML 规则、设计系统注入、布局审查和 CSS 分层见 `references/phase4-page-authoring.md`，页面模板细节见 `references/page-html-template.md`。

主文件只保留阻塞性要求：

1. 逐页 HTML 生成必须通过 `ui-ux-pro-max` 的设计系统能力驱动
2. 每页必须满足“标题 / 结论 / 上屏内容 / 话术”四要素
3. 每页对应一个独立 HTML 文件，且图表优先引用 Phase 3.5 输出的图表 HTML
4. `page-html-template.md` 第 5 节布局审查清单 10 项全部通过，才允许进入 Phase 5
5. 页面允许做轻量 MD3 规范化，但不得破坏首页图表确立的主色语义与图表 HTML 的冻结约束

---

## Phase 5: PPT生成 — 调用 ppt-master

移交前校验、输入清单和交付后三层验证见 `references/phase5-ppt-delivery.md`。

主文件保留三条原则：

1. `ppt-master` 的直接视觉输入是逐页 HTML，XML 只负责图表真源追溯，MD 负责语义来源
2. 风格一致性指配色体系统一，不等于所有页面复用同一种版式
3. 若采用轻量 MD3 规范化，必须贯穿图表 HTML 与页面 HTML，而不是只在某几页单独套新风格

---

## 治理与迭代

交叉校验、重生链、页面合并和协作关系见 `references/governance-and-iteration.md`。

本文件最后只保留执行顺序：

1. Phase 1 建唯一数据池
2. Phase 2 做受众分层并清理技术术语
3. Phase 3 生成图表 XML
4. Phase 3.5 生成图表 HTML
5. Phase 4 产出母稿与逐页 HTML
6. Phase 5 移交给 `ppt-master`
7. 任一上游变更后，按重生链逐级刷新下游产物
