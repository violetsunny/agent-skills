# 风格→图表类型适配指南

并非所有风格对所有图表类型效果等同。用本指南选最合适的风格。

## 风格文件索引

| # | 风格 | Reference 文件 |
|---|---|---|
| 1 | Flat Icon（默认） | [`style-1-flat-icon.md`](style-1-flat-icon.md) |
| 2 | Dark Terminal | [`style-2-dark-terminal.md`](style-2-dark-terminal.md) |
| 3 | Blueprint | [`style-3-blueprint.md`](style-3-blueprint.md) |
| 4 | Notion Clean | [`style-4-notion-clean.md`](style-4-notion-clean.md) |
| 5 | Glassmorphism | [`style-5-glassmorphism.md`](style-5-glassmorphism.md) |
| 6 | Claude Official | [`style-6-claude-official.md`](style-6-claude-official.md) |
| 7 | OpenAI Official | [`style-7-openai.md`](style-7-openai.md) |
| 8 | Dark Luxury | [`style-8-dark-luxury.md`](style-8-dark-luxury.md) |
| 9 | C4 Review Canvas | [`style-9-c4-review-canvas.md`](style-9-c4-review-canvas.md) |
| 10 | Cloud Fabric | [`style-10-cloud-fabric.md`](style-10-cloud-fabric.md) |
| 11 | Event Transit | [`style-11-event-transit.md`](style-11-event-transit.md) |
| 12 | Ops Pulse | [`style-12-ops-pulse.md`](style-12-ops-pulse.md) |

## 工程优先风格（9–12）

风格 9–12 把一套视觉语言与一份可执行语义契约绑定，是刻意的专用风格而非通用皮肤。

| Style | 必需证据 | 视觉指纹 | 提示词线索 | Fallback | 绝不混用 |
|---|---|---|---|---|---|
| 9 C4 Review Canvas | 一个已声明的 C4 层级、职责、技术、带标签协议 | 暖色评审板、C4 类型页眉、虚线评审戳、确定性铅笔回声 | `C4 review board`、`C4 评审画布`、`ADR 评审图` | 无证据时退回风格 1–7 通用架构 | Region/VPC 带、事件站点、实时指标 chip |
| 10 Cloud Fabric | Region/网络/负载归属与命名的跨边界机制 | 云网格、嵌套归属脊线、中性 manifest 字形、部署模式戳 | `deployment topology`、`多区域部署图`、`Region/VPC 归属图` | 缺部署事实时退回风格 1–7 | C4 抽象标签、站点编号、黄金信号卡片 |
| 11 Event Transit | Topic、有序处理器、消费组、junction、DLQ/状态 | 细地铁轨、编号站点、固定箭头、角色专属 terminal | `event metro map`、`事件地铁图`、`Kafka 拓扑图` | 缺流证据时退回通用流程风格 | 云嵌套、C4 卡片、SRE 仪表盘 |
| 12 Ops Pulse | 固定窗口、四个黄金信号、状态、一条关键路径与 trace | 实时戳、状态轨、指标窗口、编号 hop、trace 标尺 | `reliability pulse`、`事故排查视图`、`黄金信号追踪图` | 缺实测证据时退回通用架构 | 部署归属、事件轨道隐喻、C4 评审标记 |

风格 9–12 遵循 `showcase` 构图契约：节点间距至少 40px、容器 gutter 20px、零 bridge 交叉、每条边至多两个拐弯、语义边不为视觉效果重复。

## Architecture Diagram（架构图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 默认选择；彩色节点填充、层次清晰 |
| 2 Dark Terminal | Excellent | 开发博客流行款；深底上用彩色描边 |
| 3 Blueprint | Excellent | 正式架构文档绝配 |
| 4 Notion Clean | Good | 极简，适合行内文档 |
| 5 Glassmorphism | Good | 演示与产品页抢眼 |
| 6 Claude Official | Good | 暖色美学，Anthropic 风格演示 |
| 7 OpenAI Official | Good | 干净、精确；细边框、品牌绿 accent |
| 8 Dark Luxury | Excellent | 高端编辑风；黑底金字层次在架构文档中突出 |

## Class Diagram / ER Diagram（类图 / ER 图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Good | 按类类目着色页眉 |
| 2 Dark Terminal | Good | 代码感图表高对比 |
| 3 Blueprint | Excellent | 正式 UML 文档最佳 |
| 4 Notion Clean | Excellent | 干净极简；Notion 内嵌图首选 |
| 5 Glassmorphism | Poor | 玻璃效果干扰结构内容 |
| 6 Claude Official | Excellent | 温暖易读；适合文档 |
| 7 OpenAI Official | Excellent | 极简美学匹配 UML 精确性 |
| 8 Dark Luxury | Fair | UML 用非标准深底；仅限高端编辑场景 |

## Sequence Diagram（时序图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Good | 生命线清晰；activation 框可见 |
| 2 Dark Terminal | Good | 适合开发文章；虚线生命线可见 |
| 3 Blueprint | Excellent | 正式技术文档 |
| 4 Notion Clean | Excellent | Notion 内嵌时序图最佳 |
| 5 Glassmorphism | Poor | 玻璃效果让生命线难读 |
| 6 Claude Official | Excellent | 暖色高对比 |
| 7 OpenAI Official | Excellent | 极简、精确；API 文档首选 |
| 8 Dark Luxury | Good | 戏剧性对比；深色生命线适合开发博客与高端技术文档 |

## Flowchart / Process Flow（流程图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 默认；彩色决策菱形 |
| 2 Dark Terminal | Good | 开发工作流图效果好 |
| 3 Blueprint | Good | 正式流程文档 |
| 4 Notion Clean | Good | SOP 与行内文档干净 |
| 5 Glassmorphism | Good | 产品演示抢眼 |
| 6 Claude Official | Good | 演示用暖色美学 |
| 7 OpenAI Official | Good | 干净极简 |
| 8 Dark Luxury | Good | 高端流程文档抢眼 |

## Mind Map / Concept Map（思维导图 / 概念图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 彩色分支、有吸引力 |
| 2 Dark Terminal | Good | 深底霓虹感分支 |
| 3 Blueprint | Poor | 蓝图网格与放射布局冲突 |
| 4 Notion Clean | Excellent | 头脑风暴文档首选 |
| 5 Glassmorphism | Excellent | 演示视觉效果惊艳 |
| 6 Claude Official | Good | 温暖易读 |
| 7 OpenAI Official | Good | 干净极简 |
| 8 Dark Luxury | Excellent | 黑底金色分支；放射布局在演示中突出 |

## Data Flow Diagram（数据流图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 按数据类型给箭头着色 |
| 2 Dark Terminal | Excellent | 深底发光数据路径 |
| 3 Blueprint | Excellent | 正式数据流文档 |
| 4 Notion Clean | Good | 极简、干净 |
| 5 Glassmorphism | Poor | 干扰流语义 |
| 6 Claude Official | Good | 易读 |
| 7 OpenAI Official | Good | 精确、极简 |
| 8 Dark Luxury | Excellent | 彩色数据路径在深黑上发亮；数据工程文档首选 |

## Use Case Diagram（用例图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Good | 彩色用例椭圆 |
| 2 Dark Terminal | Poor | 小人图标在深底上不够醒目 |
| 3 Blueprint | Excellent | 经典 UML 美学 |
| 4 Notion Clean | Excellent | 产品需求文档绝配 |
| 5 Glassmorphism | Poor | 多余视觉噪音 |
| 6 Claude Official | Excellent | 温暖、专业 |
| 7 OpenAI Official | Excellent | 干净、精确的 UML |
| 8 Dark Luxury | Fair | 小人图标在深黑上不够醒目；谨慎使用 |

## State Machine Diagram（状态机图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Good | 彩色状态 |
| 2 Dark Terminal | Good | 发光状态与迁移 |
| 3 Blueprint | Excellent | 正式 UML 状态机最佳 |
| 4 Notion Clean | Excellent | 文档用干净风格 |
| 5 Glassmorphism | Poor | 干扰状态迁移 |
| 6 Claude Official | Excellent | 易读 |
| 7 OpenAI Official | Excellent | 极简、精确 |
| 8 Dark Luxury | Good | 状态迁移高对比；编辑级品质 |

## Network Topology（网络拓扑）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 彩色设备图标 |
| 2 Dark Terminal | Excellent | 赛博朋克风网络图 |
| 3 Blueprint | Excellent | 基础设施文档首选 |
| 4 Notion Clean | Good | IT 文档干净风格 |
| 5 Glassmorphism | Good | 演示抢眼 |
| 6 Claude Official | Good | 专业网络图 |
| 7 OpenAI Official | Good | 干净的基础设施图 |
| 8 Dark Luxury | Excellent | 深黑基础设施经典款；金色拓扑线跳出 |

## Comparison / Feature Matrix（对比 / 特性矩阵）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 着色对勾 |
| 2 Dark Terminal | Good | 开发工具对比适用 |
| 3 Blueprint | Poor | 网格与表格布局冲突 |
| 4 Notion Clean | Excellent | Notion 内嵌表格绝配 |
| 5 Glassmorphism | Poor | 干扰表格数据 |
| 6 Claude Official | Excellent | 干净、温暖 |
| 7 OpenAI Official | Excellent | 极简、精确 |
| 8 Dark Luxury | Fair | 对比表用深底非标准；谨慎使用 |

## Timeline / Gantt（时间线 / 甘特图）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 按类目彩色条 |
| 2 Dark Terminal | Good | 开发路线图适用 |
| 3 Blueprint | Good | 正式项目计划 |
| 4 Notion Clean | Excellent | Notion 项目文档首选 |
| 5 Glassmorphism | Good | keynote 演示抢眼 |
| 6 Claude Official | Good | 温暖、专业 |
| 7 OpenAI Official | Good | 干净时间线 |
| 8 Dark Luxury | Good | 高端项目路线图与 keynote 演示 |

## Agent / Memory Architecture（Agent / 记忆架构）
| Style | Suitability | Notes |
|-------|-------------|-------|
| 1 Flat Icon | Excellent | 彩色层次、有吸引力 |
| 2 Dark Terminal | Excellent | AI/ML 博客文章流行款 |
| 3 Blueprint | Good | 正式 AI 系统文档 |
| 4 Notion Clean | Good | AI 研究笔记干净风格 |
| 5 Glassmorphism | Excellent | AI 产品演示惊艳 |
| 6 Claude Official | Excellent | Anthropic AI 美学 |
| 7 OpenAI Official | Excellent | OpenAI AI 美学 |
| 8 Dark Luxury | Excellent | 高端 AI 系统文档最佳；深黑配香槟金 |
