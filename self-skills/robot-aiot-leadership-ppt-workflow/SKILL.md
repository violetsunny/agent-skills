---
name: robot-aiot-leadership-ppt-workflow
version: 3.3.0
description: >
  将项目数据和技术分析转化为结构化的领导汇报PPT，覆盖全链路五阶段工作流：
  数据池建立 → 技术明细版+目标受众汇报版文档分层（受众由用户指定，默认领导层） → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图XML并完成XML→HTML桥接与静态页面HTML化 → 调用 ppt-master 依据每页HTML样式生成最终PPTX文件。
  当用户要求"写领导汇报PPT"、"出PPT母稿"、"做汇报材料"、"汇报方案"、"写PPT"、
  "领导汇报"、"生成汇报PPT"时触发。也适用于用户描述了需要将技术项目数据
  转化为管理层可读的汇报格式的场景。
---

# Robot AIoT 领导汇报 PPT 工作流

将技术项目数据转化为领导可读的 PPT 汇报，核心原则：
**让领导一目了然，一眼看懂** — 每页必须有业务价值结论 + 数据支撑，
不讲代码实现。

本技能覆盖从原始数据到最终 PPTX 的全链路，涉及两个外部技能调用：
- **robot-aiot-draw-flowchart** — 生成分层架构图/流程图 XML，并完成 XML→HTML 桥接转换与静态页面 HTML 生成
- **ppt-master** — 读取逐页 HTML/MD 生成最终 PPTX 文件

Sub agent 原则：
- 非 trivial 的阶段分析、分层提炼、图表规划、页面草拟、交叉校验，优先交给 fresh sub agent 执行，保持上下文干净
- 主线程只做总控：阶段切换、用户确认、真实文件落盘、跨阶段一致性校验、外部技能调用与最终交付判断
- tiny wording tweak、单页局部小改、局部格式修正可直接在主线程完成，不必起 sub agent

强制中间层原则：
- **XML 先转 HTML**：凡是由 `robot-aiot-draw-flowchart` 生成的图表 XML，在进入 PPT 阶段前必须先通过 `robot-aiot-draw-flowchart` 的 XML→HTML 桥接能力转成 HTML 预览文件
- **母稿逐页转 HTML**：在调用 `ppt-master` 之前，必须通过 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力把 PPT 母稿的每一页都落成单页 HTML
- **按 HTML 转 PPT**：ppt-master 读取逐页 HTML/MD 生成 PPTX，HTML 是 ppt-master 的直接输入格式
- **没有 HTML 不得生成 PPT**：只要图表 HTML 或页面 HTML 未完成，PPT 生成阶段不得开始

---

## 执行前依赖检查

开始执行前，先检查依赖 skill 是否已安装在运行时 `~/.agents/skills/`：

```bash
for s in robot-aiot-draw-flowchart ppt-master; do
  [ -d "$HOME/.agents/skills/$s" ] || printf '[DEP-MISSING] %s\n' "$s"
done
```

| 依赖 skill | 级别 | 用途 |
|------|------|------|
| robot-aiot-draw-flowchart | 必需 | 阶段三绘制图表 XML、XML→HTML 桥接转换、静态页面 HTML 生成 |
| ppt-master | 必需 | 阶段五依据逐页 HTML 生成 PPTX |

- 全部存在 → 略过，进入主流程
- 出现 `[DEP-MISSING]` → **暂停执行**，列出缺失清单并提示用户手动安装（本技能不私自安装），安装完成后再继续

## 输出目录约定

所有输出产物统一放在当前运行项目的 `doc-ppt/` 目录下，不散落到其他位置。

```
doc-ppt/
├── assets/                     — 品牌静态资源（Logo、素材图压缩副本等）
│   └── midea-logo.png          — 美的品牌 Logo（从 skill assets/ 复制）
├── flow/                       — 图表类产物统一目录
│   ├── <chart-name>.xml        — 图表 XML（Phase 3，robot-aiot-draw-flowchart 产出）
│   └── <chart-name>.html       — 图表 HTML（Phase 3.5，robot-aiot-draw-flowchart XML→HTML 桥接产出）
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
Phase 2: 受众分层     → 技术明细版MD + 目标受众汇报版MD（受众由用户指定，默认领导层；同一数据，不同表达）
Phase 3: 图表生成     → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML
Phase 3.5: 桥接转换  → 调用 robot-aiot-draw-flowchart 的 XML→HTML 桥接能力，将 XML 稳定转 HTML 并保留原样式
Phase 4: PPT母稿     → 调用 robot-aiot-draw-flowchart 的静态页面 HTML 能力，按页结构化：标题→结论→数据→话术，并将每页落成 HTML 页面样式
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

## Phase 2: 受众分层 — 技术明细版 + 目标受众汇报版

文档结构、受众→表达策略映射、术语映射模板和业务化翻译规则见 `references/phase2-audience-layering.md`。

入口约束：

1. 先确认目标受众（用户指定：领导层/技术同行/外部客户/大众；未指定默认领导层），受众决定表达策略与 Phase 4 风格基调
2. 先写技术明细版，再按受众表达策略提炼汇报版
3. 两份文档共用同一数据池
4. 面向领导层/外部客户/大众时，汇报版不得直接暴露表名、类名、API 路径或无解释缩写（技术同行受众豁免）

---

## Phase 3 / 3.5: 图表生成与桥接转换

图表类型选择、XML/HTML 产物、阻塞规则与协作边界见 `references/phase3-chart-pipeline.md`。

主文件保留五条硬约束：

1. Phase 3 先调用 `robot-aiot-draw-flowchart` 生成图表 XML 真源
2. Phase 3.5 必须调用 `robot-aiot-draw-flowchart` 的 XML→HTML 桥接能力为每个 XML 生成对应 HTML
3. 没有图表 HTML，不得进入 Phase 4
4. 首页架构图确定全局主色基调，后续页面保持配色统一但允许版式多样
5. 允许在 Phase 3.5 和 Phase 4 做轻量 Material 3 规范化，但只能整理 token、字体层级、间距和容器语义，不能改图表结构和数据语义
6. 数据统计图表（饼图/箱线图/热力图/网络拓扑等）与 Mermaid 源导入重绘（含 pie/mindmap/timeline 等扩展类型）按 `robot-aiot-draw-flowchart` 的数据图表与导入规则路由；需要可编辑 `.excalidraw` 三件套产物时走其导出规则

---

## Phase 4: PPT母稿 — 按页结构化

Phase 4 的逐页 HTML 编写能力已内化到 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力中。本工作流负责阶段编排、阻塞校验、产物衔接，以及页面策略层增强。

### 页面策略增强

布局模式选择、Deck叙事策略、文案公式详见 `references/slide-layout-strategies.md`：

1. 按页面类型选择 17 种布局模式中最匹配的一种，相邻两页不得使用相同布局
2. 按汇报场景选择 11 种 Deck 策略确定叙事弧线；演讲时长按页数换算（30 分钟 = 8-12 页）
3. 用 8 个文案公式框架组织每页文案（PAS/AIDA/FAB/3W 等）
4. 每页话术按逐字稿三铁律写作：提示信号（关键词加粗）、150-300 字/页、口语化；话术只进母稿话术栏与页面 `.notes` 容器，不得上屏

### 配图与封面图

需要高质量配图或封面图时，规则见 `references/ppt-image-and-cover.md`：

1. 封面推荐 HTML/CSS + AI 背景图组合
2. 案例/故事页可用 AI 插图具象化场景
3. 数据页用程序化图表，不用 AI 生图
4. AI 图片不承载事实数据，仅作视觉增强

### 阻塞性要求

1. 逐页 HTML 生成必须调用 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力
2. **仅使用静态版**：禁止生成交互版（翻页/动画/特效），ppt-master 只消费静态 HTML；scale-to-fit 视口自适应壳不属于交互版特性，必须保留（1920x1080 视口下 scale=1，不影响 ppt-master 消费）
3. 每页必须满足"标题 / 结论 / 上屏内容 / 话术"四要素；话术写入页面 `display:none` 的 `.notes` 容器，出现在可见区域按阻塞项处理
4. 每页对应一个独立 HTML 文件，且图表优先引用 Phase 3.5 输出的图表 HTML（`flow/` 目录）
5. 母稿含素材图映射的页面必须把素材图以原图高清落盘、网格平铺上屏（只压格位占位空间不压图片分辨率，区内无滚动条、不拉伸变形），素材图规则由 `robot-aiot-draw-flowchart` 的 `references/slide-image-framing.md` 承载；母稿未指定但资源目录存在可用素材时，Phase 4 开始前盘点并向用户确认选配，不得静默忽略
6. `robot-aiot-draw-flowchart` 的布局审查清单 10 项全部通过，才允许进入 Phase 5
7. 页面允许做轻量语义化规范化，但不得破坏首页图表确立的主色语义与图表 HTML 的冻结约束

---

## Phase 5: PPT生成 — 调用 ppt-master

移交前校验、输入清单和交付后三层验证见 `references/phase5-ppt-delivery.md`。

主文件保留五条硬约束：

1. `ppt-master` 的直接视觉输入是逐页 HTML，XML 只负责图表真源追溯，MD 负责语义来源
2. 风格一致性指配色体系统一，不等于所有页面复用同一种版式
3. 若采用轻量语义化规范化，必须贯穿图表 HTML 与页面 HTML，而不是只在某几页单独套新风格
4. **PPTX 必须可编辑**：文字=原生文本框、图形=原生形状；PICTURE 仅限素材照片与 flow 图表渲染图；禁止整页光栅贴图（任何超尺寸整页 PICTURE 判交付失败）；交付前必须用 python-pptx 递归展开做形状构成验证，细则见 `references/phase5-ppt-delivery.md`
5. **过程产物目录**：PPT 生成的一切工作区/脚本/中间产物放本次交付目录下 `projects/`，禁止写入 `~/.agents/projects` 等全局目录

---

## 何时读取引用文档

### 核心工作流
1. 需要数据池建立规则时，读 `references/phase1-data-pool.md`
2. 需要受众分层规则时，读 `references/phase2-audience-layering.md`
3. 需要图表生成与桥接转换规则时，读 `references/phase3-chart-pipeline.md`
4. 需要逐页 HTML 编写规则时，读 `references/phase4-page-authoring.md`
5. 需要 PPT 交付校验规则时，读 `references/phase5-ppt-delivery.md`

### 品牌与页面
6. 需要品牌资源使用规则时，读 `references/brand-assets.md`
7. 需要页面 HTML 模板骨架时，读 `references/page-html-template.md`

### 增强能力
8. 需要布局策略/Deck叙事/文案公式时，读 `references/slide-layout-strategies.md`
9. 需要AI图像生成/封面设计规则时，读 `references/ppt-image-and-cover.md`

### 治理
10. 需要交叉校验/重生链/协作关系时，读 `references/governance-and-iteration.md`

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
