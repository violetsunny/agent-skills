# 技能总览

本文档汇总三个技能目录：`~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/`，根据各目录下实际存在的 `SKILL.md` 递归生成。技能名称优先读取 frontmatter `name`（缺失回退目录名）；说明为基于原始 `description` 提炼的中文摘要（≤500 字，简洁概括用途与触发场景）。


## 第一部分：`~/.agents/skills/`

扫描目录：`/Users/kangll13/.agents/skills/`（运行时技能目录）

共 **130** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `academy-guide` | `academy-guide` | 回答关于如何使用 Claude 或 Claude 产品的问题前先检查此 skill——它推荐来自 Claude Academy（academy.claude.com）的匹配课程/教程/用例。触发条件：how do I/how can I/getting started with/what can Claude do/teach me/learn to use；关于 artifacts/projects/skills/plugins/connectors/MCP 的问题；向团队/班级/组织推广 Claude 的请求；培训材料/入门内容/学习资源的请求。适用于用户正在学习如何使用功能或产品时，而非正在执行任务只想完成任务时。与其他 skill 组合使用：查阅产品文档回答 Claude 功能用法后，也检查此处是否有匹配课程或教程。仅在强匹配时推荐，绝不虚构 Academy 内容。 |
| `algorithmic-art` | `algorithmic-art` | 使用 p5.js 创作算法艺术，支持种子随机性和交互式参数探索。适用于用户要求用代码创作艺术、生成艺术、算法艺术、流场或粒子系统时。创作原创算法艺术，避免复制现有艺术家作品以防侵权。 |
| `api-contract-review` | `api-contract-review` | 审查 REST API 契约的 HTTP 语义、版本管理、向后兼容性和响应一致性。适用于用户要求 review API、check endpoints、REST review 或发布 API 变更前。 |
| `api-tester` | `api-tester` | 依据真实 OpenAPI、路由实现和现有测试生成并验证 API 测试。适用于测试接口、补集成测试、验证 API 契约、生成回归用例或排查接口兼容性时；区分生成测试和执行请求的授权，不猜测状态码/响应结构/SLA，不在未确认环境中发送写请求。 |
| `archify` | `robot-aiot-draw-flowchart/archify` | 创建精美的架构、工作流、时序、数据流和生命周期/状态图，输出为可交互的独立 HTML（内联 SVG），支持深色/浅色主题、可选轨迹动画及 PNG/JPEG/WebP/SVG/WebM 导出。接受自然语言需求或粘贴的 Mermaid flowchart/sequenceDiagram/stateDiagram 输入；当图表需反映真实代码时检查仓库证据。适用于可视化系统架构、基础设施、云/安全/网络拓扑、技术工作流、API 调用序列、请求生命周期、数据管道、ETL/ELT、数据血缘、状态机，或转换/美化 Mermaid 图表。 |
| `architecture-review` | `architecture-review` | 宏观层面分析 Java 项目架构：包结构、模块边界、依赖方向和分层。适用于用户要求 review architecture/check structure/package organization 或评估代码库是否遵循整洁架构原则时。 |
| `ask-matt` | `ask-matt` | 询问哪个 skill 或流程适合当前情况。本仓库 skill 的路由器。 |
| `banner-design` | `banner-design` | 设计社交媒体、广告、网站 Hero、创意素材及印刷品 Banner。提供多种艺术方向可选配生成或提供的视觉素材。支持 Facebook/Twitter-X/LinkedIn/YouTube/Instagram/Google Display/网站 Hero/印刷品等平台，涵盖极简、渐变、粗体排版、摄影、插画、几何、复古、玻璃拟态、3D、霓虹、双色调、编辑风、拼贴等风格。 |
| `baoyu-image-gen` | `baoyu-image-gen` | AI 图像生成，支持 OpenAI GPT Image 2.5/Azure OpenAI/Google/OpenRouter/DashScope/Z.AI GLM-Image/MiniMax/Jimeng/Seedream/Replicate/Agnes API。支持文生图、参考图、宽高比和从保存的 prompt 文件批量生成。默认顺序执行；用户已有多个 prompts 或需要稳定的多图吞吐时使用批量并行生成。适用于用户要求生成/创建/绘制图像时。 |
| `brand` | `brand` | 品牌声音、视觉识别、消息框架、资产管理与品牌一致性。适用于品牌内容、语调、营销素材、品牌合规、风格指南等场景。 |
| `brand-guidelines` | `brand-guidelines` | 将 Anthropic 官方品牌配色和排版应用于任何可受益于 Anthropic 外观的制品。适用于品牌配色/风格指南/视觉格式/公司设计标准适用时。 |
| `canvas-design` | `canvas-design` | 使用设计理念在 .png 和 .pdf 文档中创建精美视觉艺术。适用于用户要求创建海报、艺术品、设计或其他静态作品时。创作原创视觉设计，避免复制现有艺术家作品以防侵权。 |
| `captions-overlay` | `captions-overlay` | embedded-captions 工作流的叠加规则：定义字幕模型（drop/rail/embed）及字幕作为 OVERLAY 合成在影片上方（而非预留底部安全区）的原则。适用于为出镜视频或发布视频添加字幕、决定短语丢弃/保留/升级为嵌入高潮、布局带字幕的构图（禁止预留 keep-out band）、在字幕下以真实帧中心对齐构图时加载。 |
| `changelog-generator` | `changelog-generator` | 从 git commits 生成 changelog。适用于用户说 generate changelog/update changelog/what changed since last release 或准备新版本发布前。 |
| `changelog-video` | `changelog-video` | 将每周 changelog .md 转为成品品牌 changelog 视频（正方形 1080、约 45-60 秒、Annie VO、动画品牌背景、模拟 UI 可视化、低调字幕）。适用于用户提供 changelog/digest markdown 并想要每周视频或说 changelog video 时。自包含——字体、背景、词典和脚本均内置于此 skill。 |
| `claude-handoff` | `claude-handoff` | 将当前对话交接给新的后台 agent 立即接续工作。 |
| `clean-code` | `clean-code` | Clean Code 原则（DRY/KISS/YAGNI）、命名、函数设计与可读性。适用于代码难读、方法过长、命名不清、重复或嵌套过深时。类职责拆分和依赖方向请用 solid-principles。 |
| `code-review` | `code-review` | 从固定点（commit/branch/tag/merge-base）起沿两个维度审查变更：Standards（是否符合仓库编码规范）和 Spec（是否匹配原始 issue/spec 要求）。并行子 agent 运行两项审查并并列报告。适用于审查分支、PR、进行中变更或用户要求 review since X 时。 |
| `codebase-design` | `codebase-design` | 设计 deep module 的共享词汇表。适用于用户想设计或改进模块接口、寻找深化机会、决定接缝位置、使代码更易测试或 AI 导航，或其他 skill 需要 deep-module 词汇时。 |
| `concurrency-review` | `concurrency-review` | 审查 Java 并发代码的线程安全、竞态条件、死锁和现代模式（Virtual Threads/CompletableFuture/@Async）。适用于用户要求 check thread safety/concurrency review/async code review 或审查多线程代码时。 |
| `cut-the-curve` | `cut-the-curve` | 技术目录：五种速度匹配的 SEAMS（zoom-through/INVERSE zoom-through/cut-the-curve/waterfall cut/rack-focus blur-cut）加两种场景内技术——waterfall ENTRY（标题卡/段落开头的交错到达级联）和 nudge curve（慢-快-慢三阶段群组滑动）。涵盖约 12% 画幅的部分行程速度匹配（镜像 power4 缓动）、Z scale-sign 规则、尺寸缩放模糊（10px 文字/18-20px 全帧）、逐词交错剪切、按元素权重的级联节奏和 10/65/25 滑动比例。编写任何转场、文字节拍交接、动态文字入场或群组重定位前阅读。 |
| `design` | `design` | 综合设计能力：品牌识别、设计 token、UI 样式、Logo 生成（55 种风格）、企业形象方案 CIP（50 项交付物）、HTML 演示文稿（Chart.js）、Banner 设计（22 种风格）、图标设计（15 种风格 SVG）、社交媒体图片（HTML→截图多平台适配）。支持 Facebook/Twitter/LinkedIn/YouTube/Instagram/Pinterest/TikTok/Threads/Google Ads 等平台。 |
| `design-patterns` | `design-patterns` | 常见设计模式及 Java 示例（Factory/Builder/Strategy/Observer/Decorator 等）。适用于用户要求 implement pattern/use factory/strategy pattern 或设计可扩展组件时。 |
| `design-system` | `design-system` | Token 架构、组件规范和幻灯片生成。三层 tokens（primitive→semantic→component）、CSS 变量、间距/排版比例、组件规范、战略幻灯片创建。适用于设计 tokens、系统化设计、品牌合规演示文稿。 |
| `dev-paradigm-matt` | `dev-paradigm-matt` | 面向日常工程开发的分层工作流路由：根据任务阶段将需求澄清、规格设计、架构规划、实现、调试、审查、交接和长期维护路由到合适的 matt-skills。适用于这个需求怎么推进、从需求到代码怎么分阶段、该先 grill 还是 to-spec、Bug/重构/新功能分别怎么走、完整开发流程编排、接手陌生项目需 setup/领域建模/票据拆分/实现收尾/长期维护规划等场景。 |
| `diagnosing-bugs` | `diagnosing-bugs` | 疑难 bug 和性能回退的诊断循环。适用于用户说 diagnose/debug this 或报告某些东西坏了/抛异常/失败/变慢时。 |
| `diagram-design` | `diagram-design` | 创建品牌化的架构/IT 现状/流程图/时序/状态机/ER 数据模型/时间线/泳道/象限/雷达蜘蛛/极坐标/循环飞轮/嵌套/树形/组织/层叠/韦恩/金字塔漏斗/矩形树图/柱状/瀑布/折线/甘特/散点/高层/流程/勋章/数据流/DP 集成/DP 安全矩阵/Sankey/鱼骨/Wardley map/看板/用户旅程/部署/依赖图/UML 类/故事地图/数据库 schema 图等独立 HTML/SVG/PNG。可按指定尺寸/细节重绘 .drawio/.drawio.png/.drawio.svg/Mermaid .mmd/Excalidraw .excalidraw 源；从网站接入品牌 token；添加语义图案/标注/无障碍动画/手绘风格。 |
| `discernment-nudge` | `discernment-nudge` | 在给出实质性回答或草稿（建议、方案、计划、提案、邮件、估算、数据分析、事实陈述、多步论证）后、最终发送前触发，追加 2-3 个简短跟进问题，帮助用户核查关键事实、探查推理假设、发现缺失上下文。每次对话最多一次。简单 how-to、纯教育解释、格式转换、代码执行、创意写作、闲聊或已要求复核/引用/审查时跳过。 |
| `doc-coauthoring` | `doc-coauthoring` | 引导用户通过结构化工作流协同撰写文档。适用于写文档、提案、技术规范、决策文档等结构化内容。帮助用户高效传递上下文、迭代精炼内容并验证文档对读者的有效性。用户提及写文档、创建提案、起草规范等任务时触发。 |
| `docx` | `docx` | 当用户想创建/读取/编辑/操作 Word 文档（.docx）或 Word 模板（.dotx）时使用。触发条件：提及 Word doc/word document/.docx/.dotx 或要求生成带目录/标题/页码/信头等格式的专业文档。也适用于从 .docx/.dotx 提取或重组内容、插入/替换图片、查找替换、处理修订/批注或将内容转为精美 Word 文档。不适用于 PDF/表格/Google Docs 或与文档生成无关的编码任务。 |
| `domain-modeling` | `domain-modeling` | 构建和打磨项目领域模型。适用于讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。 |
| `embedded-captions` | `embedded-captions` | 为单人出镜视频添加字幕，无需剪辑原片。支持逐字字幕、电影级嵌入主体后方字幕、VFX 特效字幕及 35 种风格目录中的指定样式。按视觉风格路由而非后端引擎。默认使用静默 anchor rail；仅在用户明确要求全电影级处理时才嵌入每个词。全流程本地运行（含转录和主体抠像），多镜头素材需先拆分再处理。 |
| `faceless-explainer` | `faceless-explainer` | 将任意文本（文章、笔记、主题、简报）转为无真人出镜的解释视频：无网站或实拍素材，每场景独立生成视觉（排版、抽象图形、图表、数据可视化）。适用于主题解释、概念拆解、教程、列表类内容。非网站推广视频（用 /product-launch-video）。不确定时用 /hyperframes。 |
| `frontend-design` | `frontend-design` | 构建新 UI 或重塑现有 UI 时的独特、有意图的视觉设计指导。帮助确定美学方向、排版选择和避免模板化默认外观。 |
| `general-video` | `general-video` | 当没有专门工作流适用或 BRIEF.md 设置 flow: companion 时，编写或编辑自定义 HyperFrames 组合。适用于较长或多场景作品、品牌和 sizzle reels、蒙太奇、静态循环、静态标题卡、素材混剪和自由构建。短小无旁白运动优先单元（含动画标题）请用 motion-graphics。新创作请先通过 hyperframes 路由。 |
| `git-commit` | `git-commit` | 为 Java 项目生成 Conventional Commit 提交信息。适用于用户说 commit、create commit、commit changes 或完成代码变更后需要提交时。 |
| `git-guardrails-claude-code` | `git-guardrails-claude-code` | 设置 Claude Code hooks 阻止危险 git 命令（push/reset --hard/clean/branch -D 等）在执行前被拦截。适用于用户想防止破坏性 git 操作、添加 git 安全钩子或在 Claude Code 中阻止 git push/reset 时。 |
| `grill-me` | `grill-me` | 对计划、决策或想法进行 relentless 追问式压力测试。适用于用户想压力测试自己的思考或使用任何 grill 触发短语时。 |
| `grill-with-docs` | `grill-with-docs` |  relentless 追问式访谈以锐化计划或设计，同时在过程中创建文档（ADR 和术语表）。 |
| `grilling` | `grilling` | 对用户的计划、决策或想法进行 relentless 追问。适用于用户想压力测试思考或使用任何 grill 触发短语时。 |
| `handoff` | `handoff` | 将当前对话压缩为交接文档供另一个 agent 接续工作。 |
| `humanizer` | `humanizer` | 改写 AI 味文本使其读起来像作者本人所写而不改变含义。适用于编辑或审查散文中的 AI 痕迹：not-X-but-Y 对比、单行结尾、staged 开场、强制三段式、到处破折号、夸大主张、销售语言、AI 常用词、粗体标签或填充词。基于 Wikipedia 的 Signs of AI writing。 |
| `implement` | `implement` | 基于规格或一组 tickets 实施一项工作。 |
| `implement-spec` | `implement-spec` | 将规格以代码实现。 |
| `improve-codebase-architecture` | `improve-codebase-architecture` | 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，然后对你选择的任一机会进行深入追问。 |
| `internal-comms` | `internal-comms` | 帮助撰写各类内部沟通内容的资源集，使用公司偏好的格式。适用于被要求撰写状态报告、领导层更新、3P 更新、公司通讯、FAQ、事件报告、项目更新等内部沟通内容时。 |
| `issue-triage` | `issue-triage` | 对 GitHub issues 进行分诊和分类并标记优先级标签。适用于用户说 triage issues/check issues/review open issues 或定期维护 GitHub issue backlog 时。 |
| `java-code-review` | `java-code-review` | Java 系统化代码审查：空安全、异常处理、并发和性能检查。适用于用户说 review code/check this PR/code review 或合并变更前。 |
| `java-migration` | `java-migration` | Java 项目大版本升级指南（8→11→17→21→25）。适用于用户说 upgrade Java/migrate to Java 25/update Java version 或现代化遗留项目时。 |
| `jpa-patterns` | `jpa-patterns` | JPA/Hibernate 模式与常见陷阱（N+1/懒加载/事务/查询）。适用于 JPA 性能问题、LazyInitializationException 或询问实体关系和抓取策略时。 |
| `logging-patterns` | `logging-patterns` | Java 日志最佳实践：SLF4J、结构化日志（JSON）和 MDC 请求追踪。包含 AI 友好的日志格式便于 Claude Code 调试。适用于用户询问日志、调试应用流程或分析日志时。 |
| `loop-me` | `loop-me` | 在当前工作区内就待构建的工作流规格对我进行追问式审查。 |
| `maven-dependency-audit` | `maven-dependency-audit` | 审计 Maven 依赖的过期版本、安全漏洞和冲突。适用于用户说 check dependencies/audit dependencies/outdated deps 或发布前。 |
| `mcp-builder` | `mcp-builder` | 创建高质量 MCP（Model Context Protocol）服务器的指南，使 LLM 能通过精心设计的工具与外部服务交互。适用于构建 MCP 服务器集成外部 API 或服务，支持 Python（FastMCP）或 Node/TypeScript（MCP SDK）。 |
| `media-use` | `media-use` | Agent Media OS：HyperFrames 项目中所有媒体需求的统一 skill。将 BGM/SFX/图像/图标/品牌 Logo/语音/调色/LUT 解析为冻结本地文件或粘贴就绪块+台账记录（一个动词 resolve）；目录缺失时通过 TTS/音乐/图像模型生成；通过共享音频引擎制作旁白/转录/字幕/背景移除；对媒体执行剪切/重构/变换；跨项目复用资产。也适用于实拍素材显得暗/平/无聊/需要复古/摄像机/印刷/ASCII 感觉/需要隐私/需要媒体揭示等模糊反馈。 |
| `migrate-to-shoehorn` | `migrate-to-shoehorn` | 将测试文件从 as 类型断言迁移到 @total-typescript/shoehorn。适用于用户提及 shoehorn、想替换测试中的 as 或需要部分测试数据时。 |
| `motion-graphics` | `motion-graphics` | 以运动为核心信息的短设计驱动动态图形：动态排版、数据统计递增、图表/数据可视化命中、Logo sting/品牌锁定、Lower-third/标注/社交叠加、动画地图（高亮区域/连接地点/缩放定位）、动画推文/新闻文章/标题、网页/UI 动画（滚动/光标/标注）或将真实图像几何融入图表。通常 10 秒以内（最长约 30 秒），无旁白或真人主体；渲染为 MP4 或透明叠加。更长/有旁白/多场景请用 /general-video。不确定时用 /hyperframes。 |
| `openspec-apply-change` | `openspec-apply-change` | 实施 OpenSpec change 中的任务。适用于用户要开始实施、继续实施或逐步完成任务时。 |
| `openspec-archive-change` | `openspec-archive-change` | 在实验性工作流中归档已完成的 change。适用于用户想在实现完成后终结并归档 change 时。 |
| `openspec-bulk-archive-change` | `openspec-bulk-archive-change` | 一次性归档多个已完成的 changes。适用于并行归档多个 changes 时。 |
| `openspec-continue-change` | `openspec-continue-change` | 通过创建下一个 artifact 继续 OpenSpec change。适用于用户想推进 change、创建下一个 artifact 或继续工作流时。 |
| `openspec-explore` | `openspec-explore` | 进入探索模式：作为思考伙伴探索想法、调查问题和澄清需求。适用于用户在变更之前或期间想要深入思考某事时。 |
| `openspec-ff-change` | `openspec-ff-change` | 快速推进 OpenSpec artifact 创建。适用于用户想快速创建实施所需的所有 artifacts 而无需逐步操作时。 |
| `openspec-new-change` | `openspec-new-change` | 使用实验性 artifact 工作流启动新的 OpenSpec change。适用于用户想用结构化分步方法创建新功能、修复或修改时。 |
| `openspec-onboard` | `openspec-onboard` | OpenSpec 引导式入门：带解说和真实代码库操作走完一个完整工作流周期。 |
| `openspec-propose` | `openspec-propose` | 一步生成所有 artifacts 提出新 change。适用于用户想快速描述要构建的内容并获得包含设计/规格/任务的完整提案以供实施时。 |
| `openspec-sync-specs` | `openspec-sync-specs` | 将 change 的 delta specs 同步到主 specs。适用于用户想用 delta spec 的变更更新主 specs 但不归档 change 时。 |
| `openspec-update-change` | `openspec-update-change` | 通过修订现有规划 artifacts 并保持彼此一致来更新 OpenSpec change。适用于用户想修改 change 计划、纳入新决策或在编辑后协调 artifacts 时。不编辑代码。 |
| `openspec-verify-change` | `openspec-verify-change` | 验证实现是否匹配 change artifacts。适用于用户想在归档前确认实现完整、正确且一致时。 |
| `opsx-workflow-hooks` | `opsx-workflow-hooks` | opsx 工作流的 Post-command hooks。Trigger A：/opsx/propose 完成所有 artifacts 后立即进入迭代精炼循环，询问用户是否有新想法并更新提案 artifacts 直到满意。Trigger B：/opsx/apply 达到实现完成的交接点后（所有任务完成或仅剩用户/外部验证如 SIT/UAT/手动检查），在用户花时间手动验证前运行审查/测试/验证，修复关键问题，仅在所有任务真正完成后归档。不在普通实现中途暂停时触发。 |
| `oversized-cursor` | `oversized-cursor` | HyperFrames 发布视频中的超大 macOS 光标风格技术。适用于场景涉及光标或指针引导动作、启动 UI 场景、用点击点燃 morph/transition/typing 运行、或场景显得静态呆板需要低成本高收益的运动源来引导视线并打破停滞感时。涵盖光标尺寸外观（含品牌图案光标）、屏外入场法则、尖端定位与点击敲击、点击点燃下一节拍、退出/跨场景交接。 |
| `pdf` | `pdf` | 处理 PDF 文件的通用能力：读取/提取文本表格、合并/拆分 PDF、旋转页面、加水印、创建新 PDF、填写表单、加密解密、提取图片、OCR 扫描件使其可搜索。用户提及 .pdf 文件或要求生成 PDF 时使用。 |
| `performance-smell-detection` | `performance-smell-detection` | 检测 Java 代码级性能异味：streams、collections、装箱、正则、对象创建。提供意识提醒而非绝对结论，优化前务必度量。JPA/数据库性能请用 jpa-patterns。 |
| `ppt-master` | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑 PPTX 幻灯片、重建页面视觉、创建可复用 Brand/Style/Layout/Deck 工作区、填充原生 PPTX 模板和增强成品 PPTX。适用于用户要求创建/生成/重建/重新生成/美化/重新设计/模板化/填充/增强演示文稿/PPT/PPTX/幻灯片/课件（含添加旁白或动画）、请求演示文稿生成的旁白/自播放视频或提及 ppt-master 时。 |
| `pptx` | `pptx` | 当 .pptx 或 .potx 文件以任何方式涉及（输入/输出/两者）时使用。包括创建幻灯片/演示文稿、读取/解析/提取 .pptx/.potx 文本、编辑/修改/更新现有演示文稿、合并/拆分幻灯片、处理模板/布局/演讲者备注/批注。用户提及 deck/slides/presentation 或引用 .pptx/.potx 文件名时触发，无论后续如何处理内容。 |
| `pr-to-video` | `pr-to-video` | 将 GitHub PR（URL、owner/repo#N 或已检出仓库中的 this PR）转为代码变更解释视频——基于 diff、commits 和文件构建变更日志、功能展示、修复或重构演练。输入是代码变更而非网站。非产品推广（用 /product-launch-video）或无 PR 的主题解释（用 /faceless-explainer）。不确定时用 /hyperframes。 |
| `product-launch-video` | `product-launch-video` | 将产品或营销 URL、粘贴的脚本或简报转为产品发布/推广视频——SaaS 推广、功能展示、产品演示、应用和公司发布。适用于用户想营销/发布/推广/展示产品时；任何商业 URL 的默认选择。网站巡览/展示也路由至此。不确定时用 /hyperframes。 |
| `prototype` | `prototype` | 构建一次性原型以回答设计问题。适用于用户想验证状态模型或逻辑是否合理，或探索 UI 应该长什么样时。 |
| `refactor-advisor` | `refactor-advisor` | 重构顾问：识别代码坏味道并提供重构方案。 |
| `research` | `research` | 针对高可信一手信源调研问题并将结果以 Markdown 写入仓库。适用于用户要求调研主题、收集文档或 API 事实、将阅读工作委派给后台 agent 的场景。 |
| `resolving-merge-conflicts` | `resolving-merge-conflicts` | 解决进行中的 git merge/rebase 冲突时使用。 |
| `retro` | `retro` | 复盘与回顾：将一次开发/排障/交付/协作过程整理为可执行的复盘结论，输出做得好的地方、问题与根因、改进动作和后续跟踪项。适用于用户要求复盘/回顾这次开发/总结问题和经验/postmortem/retrospective 等场景；也适用于任务刚完成需沉淀流程改进点防止同类问题再发生时。 |
| `robot-aiot-adr-confluence` | `robot-aiot-adr-confluence` | 技术方案文档端到端工作流：信息评估→按需需求收敛/追问澄清/方案比较→生成 ADR/技术提案/决策简报，需要时发布到 Confluence。适用于写技术方案、生成 ADR、输出技术提案、写决策简报、架构决策记录发 Confluence、方案归档到 Confluence、技术选型文档输出等场景。仅需文档可停在 Markdown 草稿；明确要求发布才进入 Confluence 阶段。 |
| `robot-aiot-adr-generator` | `robot-aiot-adr-generator` | 生成并校验 ADR 架构决策记录：根据业务/技术需求产出标准 ADR 文档，按需对关键技术断言执行验证链核查。适用于生成 ADR、写架构决策记录、输出技术选型归档、ADR 发布前审稿等场景。 |
| `robot-aiot-commit` | `robot-aiot-commit` | 为本项目生成统一格式中文提交说明，并在用户明确要求时配合 Git 提交流程执行 commit。适用于生成 commit message、按规范提交、总结 diff、写提交说明、提交代码、根据分支提取 JIRA、按 FEAT/FIX/ENH/DOC/CHORE 分类提交等场景。 |
| `robot-aiot-docs-sync` | `robot-aiot-docs-sync` | 扫描当前项目并创建或更新一套可溯源的项目文档：AGENTS.md、README.md、CHANGELOG.md、docs/project-map.md、docs/architecture.md。适用于更新项目文档、同步文档、更新 README/AGENTS.md、生成 changelog/项目地图/架构说明等场景。吸收 changelog、中文文档、README 和 Diataxis 文档分层能力，仅在上述 5 个文件内做结构化增强，不修改源代码/配置/测试文件。 |
| `robot-aiot-draw-flowchart` | `robot-aiot-draw-flowchart` | 机器人/IoT 业务图表绘制：三条输出路径（draw.io XML 可编辑主路径、直绘 SVG/HTML 汇报级展示、archify 内置渲染支持主题切换+导出）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑、时间线、Agent/记忆架构等 40+ 图表类型；内置机器人视觉语言、12 套 SVG 风格皮肤与品牌 token 定制、几何/构图校验、PNG/GIF 导出与 drawio/Mermaid 导入重绘。 |
| `robot-aiot-knowledge-expert` | `robot-aiot-knowledge-expert` | 物联网全栈技术专家回答规范。适用于 IoT/AIOT 架构设计、协议选型、平台集成、边云协同、性能调优、故障排查等问题。触发词：物联网/IoT/AIOT/MQTT/Modbus/BACnet/OPC UA/EMQX/物模型/边云协同/设备影子/OTA/JetLinks/ThingsBoard/感认行。 |
| `robot-aiot-leadership-ppt-workflow` | `robot-aiot-leadership-ppt-workflow` | 将项目数据和技术分析转化为结构化领导汇报 PPT，覆盖五阶段全链路：数据池建立→技术明细版+领导汇报版文档分层→调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML→调用 robot-aiot-xml-html-bridge 将 XML 稳定转 HTML 并保留原样式→调用 robot-aiot-slide-html-author 完成 PPT 母稿逐页 HTML 化→调用 ppt-master 生成最终 PPTX。用户要求写领导汇报 PPT/出 PPT 母稿/做汇报材料/汇报方案/写 PPT/领导汇报/生成汇报 PPT 时触发。 |
| `robot-aiot-self-skill-sync` | `robot-aiot-self-skill-sync` | 批量更新 self 目录下所有 git 项目与 skill/command 同步工具。模块 3 外部 skill 通过 npx skills@latest update 统一更新，失败则用本地 git 克隆 rsync 兜底；递归扫描嵌套 git 仓库；~/.agents/ 与 agent-skills/ 只允许新增和修改禁止删除；文件级同步先比对新旧严禁旧覆盖新；self-skills/ 为用户自写 skill 唯一真源可双向同步；commands/ 自写命令同样双向定向同步；模块 4 将 ~/.agents/skills/ 全量同步到个人知识库（排除自写 skill）；模块 5 更新 docs/skills-overview.md 汇总。 |
| `robot-aiot-slide-html-author` | `robot-aiot-slide-html-author` | 为领导汇报类 PPT/母稿生成 1920x1080 固定画布的逐页 HTML 页面。引用 ui-ux-pro-max 的设计系统与审查能力，内化语义化设计 token、清晰/克制/层次原则与高级感设计标准（反模板化排版、色彩/形状一致性锁定、AI 痕迹清单、审查修复工作流）。适用于 PPT 母稿转单页 HTML/领导汇报页落成 HTML/逐页生成 slide HTML/给 ppt-master 准备逐页 HTML/修复汇报页布局样式信息层级/把图表 HTML 嵌入汇报页等场景。图表 HTML 有问题时可调用 robot-aiot-xml-html-bridge 审查修复。 |
| `robot-aiot-xml-html-bridge` | `robot-aiot-xml-html-bridge` | 将 robot-aiot-draw-flowchart 或其他 draw.io/mxGraph XML 图表稳定转换为 HTML 预览稿，尽可能保留原始样式/布局/层级/配色/尺寸比例/文本关系。适用于 XML 转 HTML/draw.io 转 HTML/mxGraph 转 HTML/图表转网页预览/先转 HTML 再转 PPT/保留原样式输出 HTML 等场景。也适用于领导汇报 PPT 工作流中在 PPT 生成前先落一层 HTML 作为页面主约束的场景。 |
| `scaffold-exercises` | `scaffold-exercises` | 创建包含章节、题目、解答和说明的练习目录结构并通过 lint。适用于用户想搭建练习脚手架、创建练习模板或设置新课程章节时。 |
| `seam-craft` | `seam-craft` | HyperFrames 发布视频中场景间接缝的渲染正确性原则——使转场在主时间线上正确合成的前提条件。适用于组装主时间线/index.html、剪切或交叉淡入淡出接缝处出现白闪（尤其暗色影片）、分析转场透明度下降穿透原因、或验证重叠场景包装器混合的渲染侧机制时。涵盖不透明舞台底色（#root 背景）白闪防护及注入器如何重叠包装器、保持最终帧、乒乓轨道和在主时间线上打印 lint-clean 模板代码。不包含逐转场目录，请参见 transition registry。 |
| `security-audit` | `security-audit` | Java 安全检查清单，覆盖 OWASP Top 10、输入验证、注入防护和安全编码。支持 Spring/Quarkus/Jakarta EE 和纯 Java。适用于审查代码安全、发布前或用户询问漏洞时。 |
| `setup-matt-pocock-skills` | `setup-matt-pocock-skills` | 为当前仓库配置工程技能体系：设置 issue tracker、分诊标签词汇和领域文档布局。首次使用其他工程技能前运行一次。 |
| `setup-pre-commit` | `setup-pre-commit` | 在当前仓库配置 Husky pre-commit hooks，集成 lint-staged（Prettier）、类型检查和测试。适用于用户想添加 pre-commit hooks、配置 Husky/lint-staged 或在提交时自动格式化/类型检查/测试时。 |
| `setup-ts-deep-modules` | `setup-ts-deep-modules` | 将 dependency-cruiser 接入 TypeScript 仓库，使每个包成为 deep module，实现隐藏在子文件夹中且仅通过入口文件可达。由用户手动触发。 |
| `skill-creator` | `skill-creator` | 创建新 skill、修改和改进现有 skill、衡量 skill 性能。适用于用户想从零创建 skill、编辑或优化现有 skill、运行 evals 测试 skill、基准方差分析或优化 skill 描述以提高触发准确率时。 |
| `slack-gif-creator` | `slack-gif-creator` | 创建针对 Slack 优化的动画 GIF 的知识与工具集。提供约束、验证工具和动画概念。适用于用户请求为 Slack 制作动画 GIF 时。 |
| `slides` | `slides` | 使用 Chart.js、设计 token、响应式布局、文案公式和上下文幻灯片策略创建战略性 HTML 演示文稿。 |
| `slideshow` | `slideshow` | 编写 HyperFrames slideshow——具有离散幻灯片、片段揭示、分支、热点导航和内置演讲者模式（含演讲者备注）的演示文稿/路演/交互式 deck；也可将现有页面转为 deck。输出是可导航的 deck 而非渲染的 MP4。用户未明确要求 slideshow 时先确认。不确定时用 /hyperframes。 |
| `solid-principles` | `solid-principles` | SOLID 原则清单及 Java 示例。适用于类职责过多、抽象泄漏、依赖方向错误，以及用户询问单一职责/开闭/里氏替换/接口隔离/依赖倒置时。命名、重复和方法长度请用 clean-code。 |
| `spring-boot-patterns` | `spring-boot-patterns` | Spring Boot 最佳实践与模式。适用于创建 controller/service/repository 或用户询问 Spring Boot 分层、装配、配置或异常处理时。JPA/Hibernate 行为请用 jpa-patterns。 |
| `tdd` | `tdd` | 测试驱动开发。适用于用户想以测试优先方式构建功能或修复 bug、提及 red-green-refactor 或想要集成测试时。 |
| `teach` | `teach` | 在当前工作区内教授用户新技能或概念。 |
| `test-quality` | `test-quality` | 使用 AssertJ 断言编写高质量 JUnit 5 测试。适用于用户说 add tests/write tests/improve test coverage 或审查/创建 Java 测试类时。 |
| `theme-factory` | `theme-factory` | 为幻灯片、文档、报告、HTML 落地页等制品应用主题样式的工具集。内置 10 套预设主题（配色/字体），也可即时生成新主题。 |
| `to-questionnaire` | `to-questionnaire` | 将无法完全回答的决策转化为问卷让他人填写。 |
| `to-spec` | `to-spec` | 将当前对话转为规格并发布到项目 issue tracker：不做访谈，仅综合已讨论内容。 |
| `to-tickets` | `to-tickets` | 将计划、规格或当前对话拆分为一组 tracer-bullet tickets，每个声明阻塞边，发布到配置的 tracker（本地每票一文件含文本边，或真实 tracker 的原生阻塞链接）。 |
| `triage` | `triage` | 通过分诊角色状态机推进 issue 和外部 PR：分类、验证、必要时追问，并编写 agent-ready briefs。 |
| `ui-styling` | `ui-styling` | 使用 shadcn/ui 组件（Radix UI + Tailwind）、Tailwind CSS utility-first 样式和 canvas 视觉设计创建美观、无障碍的用户界面。适用于构建 UI、实现设计系统、创建响应式布局、添加无障碍组件（对话框/下拉菜单/表单/表格）、自定义主题颜色、实现暗色模式、生成视觉设计和海报，或建立跨应用一致的样式模式。 |
| `ui-ux-pro-max` | `ui-ux-pro-max` | Web/移动端/桌面端 UI/UX 设计智能：覆盖页面、组件、设计系统、无障碍、交互、响应式布局、排版、配色、图表及各技术栈 UI 实现。内置 79 种可搜索风格、192 套产品调色板、74 组字体搭配、119 条 UX 准则、105 个图标、17 个 GSAP 预设、25 种图表类型和 22 个技术栈数据。适用于设计、构建、审查或修复界面时触发。 |
| `vercel-cli-with-tokens` | `vercel-cli-with-tokens` | 使用基于 token 的身份验证在 Vercel 上部署和管理项目。适用于使用 access token 而非交互式登录操作 Vercel CLI 的场景，如 deploy to vercel/set up vercel/add environment variables to vercel。 |
| `vercel-optimize` | `vercel-optimize` | Vercel 已部署项目的成本和性能优化，尤其 Next.js/SvelteKit/Nuxt 和部分 Astro 应用。先收集 Vercel 指标/用量/项目配置/代码扫描结果；仅调查有指标支撑的候选项；产出基于已验证文件和版本感知 Vercel/框架文档的排序建议。适用于 Vercel 账单缩减、慢/贵路由、缓存机会、Function Invocations/Build Minutes/Fast Data Transfer/Core Web Vitals/Bot Management/Fluid compute 或成本分解请求。 |
| `vercel-react-native-skills` | `vercel-react-native-skills` | React Native 和 Expo 构建高性能移动应用的最佳实践。适用于构建 RN 组件、优化列表性能、实现动画或使用原生模块时。涉及 React Native/Expo/移动性能/原生平台 API 的任务触发。 |
| `vercel-react-view-transitions` | `vercel-react-view-transitions` | 使用 React View Transition API（<ViewTransition> 组件、addTransitionType、CSS view transition 伪元素）实现流畅原生感动画的指南。适用于添加页面过渡、动画路由切换、共享元素动画、组件进出动画、列表重排动画、方向性（前进/后退）导航动画或在 Next.js 中集成 view transitions 时。用户提及 view transitions/startViewTransition/ViewTransition/transition types 或询问不使用第三方动画库在 React 中动画化 UI 状态切换时也触发。 |
| `wait-what` | `wait-what` | 暂停并重述：上一条消息未传达清楚时重新表达。 |
| `wayfinder` | `wayfinder` | 将超出单次 agent 会话承载量的大型工作规划为 issue tracker 上的共享决策票据地图，逐个解决直至路径清晰。 |
| `web-artifacts-builder` | `web-artifacts-builder` | 使用现代前端技术（React/Tailwind CSS/shadcn/ui）创建复杂多组件 claude.ai HTML artifacts 的工具套件。适用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifacts，不适用于简单单文件 HTML/JSX artifacts。 |
| `web-design-guidelines` | `web-design-guidelines` | 按 Web Interface Guidelines 审查 UI 代码。适用于被要求 review my UI、check accessibility、audit design、review UX 或 check my site against best practices 时。 |
| `webapp-testing` | `webapp-testing` | 使用 Playwright 与本地 Web 应用交互和测试的工具集。支持验证前端功能、调试 UI 行为、截取浏览器截图和查看浏览器日志。 |
| `wizard` | `wizard` | 生成交互式 bash 向导，引导人类完成只有他们才能执行的步骤。适用于配置基础设施、设置凭证或 CI secrets、走查不熟悉的第三方面板、执行一次性迁移或切换。agent 自己能做的步骤不要调用此 skill。 |
| `writing-beats` | `writing-beats` | 写作利用阶段：将原始素材组装成节拍旅程，在每个术语被节拍依赖前先确立其基础。 |
| `writing-for-agents` | `writing-for-agents` | 为 agent 编写文档。适用于创建或编辑 skill、修改 AGENTS.md 或 CLAUDE.md 时。 |
| `writing-fragments` | `writing-fragments` | 写作探索阶段：挖掘原始片段，尚无结构。 |
| `writing-shape` | `writing-shape` | 写作利用阶段：将原始素材逐段塑造成文章。 |
| `xlsx` | `xlsx` | 当电子表格文件是主要输入或输出时使用。包括打开/读取/编辑/修复 .xlsx/.xlsm/.xltx/.csv/.tsv 文件（加列、计算公式、格式化、图表、清洗脏数据）；从零或其他数据源创建新表格；在表格文件格式间转换。用户按名称或路径提及表格文件并要求操作时也触发。交付物必须是表格文件。主要交付物为 Word/HTML/Python 脚本/数据库管道/Google Sheets API 集成时不触发。 |
| `zh-code-reviewer` | `zh-code-reviewer` | 中文代码审查专家：生成详细的中文代码审查报告。 |

## 第二部分：`agent-skills/skills/`

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`（外部 skill 副本库）

共 **676** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `a-stock-data` | `a-stock-data` | 当任务需要写代码实际获取 A 股数据时使用——拉取行情 K 线(mootdx+腾讯+百度)/研报(东财+同花顺+iwencai)/信号(热点/北向/龙虎榜/解禁/行业)/资金面(融资融券/大宗/股东户数/分红/资金流)/新闻/财务三表 F10/公告(巨潮)/打板(涨停池/连板/炸板率/重点监控池/日内异动)/ETF 期权(T 型报价/希腊字母/IV)/舆情互动(互动易/热榜/人气榜)/筹码分布(获利比例/成本区间)/复权因子/估值历史(PE/PB/PS+换手率+ST)/申万行业变迁史/宏观(社融/PMI)等真实数据。十一层数据源 54 端点含 3 官方备胎，内嵌全部可运行代码自包含零依赖外部文件；优先通达信(mootdx)/腾讯(不封 IP)，东财已内置限流防封，主源被封可查备用源速查降级。仅在需要调用数据接口取数时使用：A 股概念解释/投资观点讨论/策略问答等无需取数的话题不要加载。 |
| `academy-guide` | `academy-guide` | 回答关于如何使用 Claude 或 Claude 产品的问题前先检查此 skill——它推荐来自 Claude Academy（academy.claude.com）的匹配课程/教程/用例。触发条件：how do I/how can I/getting started with/what can Claude do/teach me/learn to use；关于 artifacts/projects/skills/plugins/connectors/MCP 的问题；向团队/班级/组织推广 Claude 的请求；培训材料/入门内容/学习资源的请求。适用于用户正在学习如何使用功能或产品时，而非正在执行任务只想完成任务时。与其他 skill 组合使用：查阅产品文档回答 Claude 功能用法后，也检查此处是否有匹配课程或教程。仅在强匹配时推荐，绝不虚构 Academy 内容。 |
| `accessibility` | `accessibility` | 使用 WCAG 2.2 Level AA 设计、实现和审计无障碍数字产品。构建或审计需满足 WCAG 标准的 UI、审查键盘/对比度/屏幕阅读器支持时触发。生成语义 ARIA 和 Web/Native 无障碍特性。 |
| `adaptyv` | `adaptyv` | Adaptyv Bio Foundry API 和 Python SDK 使用指南，用于蛋白质实验设计、提交和结果获取。当用户提及 Adaptyv/Foundry API/蛋白质结合实验/BLI/SPR/热稳定性实验或提交蛋白质序列进行实验表征时触发。代码导入 adaptyv/adaptyv_sdk/FoundryClient 或引用 foundry-api-public.adaptyvbio.com 时也触发。 |
| `aeon` | `aeon` | 时间序列机器学习技能，涵盖分类、回归、聚类、预测、异常检测、分割和相似性搜索。适用于需要专用算法的单变量和多变量时间序列分析，兼容 scikit-learn API。 |
| `agent-reach` | `agent-reach` | 全网调研/搜索技能，覆盖小红书、Twitter/X、B站、Reddit、Facebook、Instagram、V2EX、LinkedIn、YouTube、GitHub、雪球等 15 个平台。用户提到任何平台名或 URL 时必须使用。仅负责获取内容，不做加工或写操作。 |
| `agent-tui` | `agent-tui` | 编程驱动终端 UI (TUI) 应用进行测试、自动化和检查。主 agent 不直接使用，需通过 tui_tester subagent 调用。也可用于了解 agent-tui 的功能和工作方式。 |
| `ai-video-script` | `ai-video-script` | AI 视频脚本生成器，根据主题/关键词生成完整视频脚本（分镜描述、画面提示词、配音文案）。适用于短视频创作者、AI 视频制作者和内容营销人员。 |
| `algorithmic-art` | `algorithmic-art` | 使用 p5.js 创作算法艺术，支持种子随机性和交互式参数探索。适用于用户要求用代码创作艺术、生成艺术、算法艺术、流场或粒子系统时。创作原创算法艺术，避免复制现有艺术家作品以防侵权。 |
| `analytical-method-validation` | `analytical-method-validation` | 在ICH Q2(R2)/Q14、USP <1220>/<1225>/<1226>、ICH M10、CLSI EP或ISO/IEC 17025框架下规划、执行和记录分析方法的验证、确认和转移。适用于HPLC/LC-MS/MS/GC/CE/ICP-MS/溶出/qNMR/qPCR/NIR/配体结合/细胞法等方法适用性评估，覆盖线性、准确度、精密度、LOD/LOQ、专属性、耐用性、方法转移、Deming/Passing-Bablok/Bland-Altman、等效性检验、OOS调查等。 |
| `anndata` | `anndata` | 单细胞分析中标注矩阵的数据结构。适用于处理 .h5ad 文件或与 scverse 生态集成时。这是数据格式 skill——分析工作流用 scanpy；概率模型用 scvi-tools；群体规模查询用 cellxgene-census。 |
| `api-contract-review` | `api-contract-review` | 审查 REST API 契约的 HTTP 语义、版本管理、向后兼容性和响应一致性。适用于用户要求 review API、check endpoints、REST review 或发布 API 变更前。 |
| `api-design` | `api-design` | REST API设计模式：资源命名、状态码、分页、过滤、错误响应、版本控制和速率限制。适用于设计或审查REST端点、资源名、状态码、分页或版本控制。 |
| `api-sculptor` | `api-sculptor` | 设计和实现API（REST/GraphQL/gRPC/WebSocket）：生成OpenAPI 3.1 spec、GraphQL SDL schema、Protocol Buffer定义和可用服务端实现。适用于API设计、端点结构、schema定义、版本策略、分页、认证、限流或任何API实现工作。 |
| `api-tester` | `api-tester` | 依据真实 OpenAPI、路由实现和现有测试生成并验证 API 测试。适用于测试接口、补集成测试、验证 API 契约、生成回归用例或排查接口兼容性时；区分生成测试和执行请求的授权，不猜测状态码/响应结构/SLA，不在未确认环境中发送写请求。 |
| `apple-hig-designer` | `Apple-Hig-Designer` | 遵循 Human Interface Guidelines 设计 Apple 风格 iOS/macOS 界面。创建符合 HIG 的组件，使用 SF Symbols/San Francisco 排版和正确的无障碍支持。支持可选的现代效果。适用于设计 Apple 风格 UI/iOS macOS 界面/HIG 合规组件或实现设计规范时。 |
| `arbor` | `arbor` | 使用Arbor论文的Hypothesis Tree Refinement(HTR)自主优化真实artifact（代码/训练recipe/agent harness/数据pipeline/prompt），针对目标和评估器在多实验中迭代改进而不过拟合。适用于"get eval score up""improve agent/harness""tune pipeline""beat baseline"或长期"make artifact better且不memorize dev set"任务。以Claude为协调者、隔离git worktree中的subagent执行。 |
| `arboreto` | `arboreto` | 使用可扩展算法（GRNBoost2、GENIE3）从基因表达数据推断基因调控网络(GRN)。适用于bulk/scRNA-seq转录组数据分析转录因子-靶基因关系和调控互作，支持大规模数据集分布式计算。 |
| `archify` | `archify` | 创建精美的架构、工作流、时序、数据流和生命周期/状态图，输出为可交互的独立 HTML（内联 SVG），支持深色/浅色主题、可选轨迹动画及 PNG/JPEG/WebP/SVG/WebM 导出。接受自然语言需求或粘贴的 Mermaid flowchart/sequenceDiagram/stateDiagram 输入；当图表需反映真实代码时检查仓库证据。适用于可视化系统架构、基础设施、云/安全/网络拓扑、技术工作流、API 调用序列、请求生命周期、数据管道、ETL/ELT、数据血缘、状态机，或转换/美化 Mermaid 图表。 |
| `architecture-decision-records` | `architecture-decision-records` | 将 Claude Code 会话中做出的架构决策捕获为结构化 ADR。自动检测决策时刻、记录上下文/考虑的备选方案和理由。维护 ADR 日志以便未来开发者理解代码库为何如此塑造。 |
| `architecture-review` | `architecture-review` | 宏观层面分析 Java 项目架构：包结构、模块边界、依赖方向和分层。适用于用户要求 review architecture/check structure/package organization 或评估代码库是否遵循整洁架构原则时。 |
| `article-writing` | `article-writing` | 撰写文章、指南、博客、教程、newsletter等长篇内容，从提供的范例或品牌指导中衍生独特文风。适用于需要超过一段的精炼书面内容，尤其是文风一致性、结构和可信度重要的场景。 |
| `ask-matt` | `ask-matt` | 询问哪个 skill 或流程适合当前情况。本仓库 skill 的路由器。 |
| `ask-matt` | `engineering/ask-matt` | 询问哪个 skill 或流程适合当前情况。本仓库 skill 的路由器。 |
| `astropy` | `astropy` | 天文和天体物理核心 Python 库，涵盖 Astropy 单位/量、坐标、FITS I/O、表、时间系统、WCS 和宇宙学。实现或调试天文数据分析代码时使用。 |
| `async-pr-review` | `async-pr-review` | 当用户想启动异步 PR 审查/对 PR 运行后台检查/检查先前启动的异步 PR 审查状态时触发。 |
| `auth-architect` | `auth-architect` | 设计和实现认证与身份系统：OAuth2/OIDC 流程（授权码/PKCE/客户端凭证）、JWT 设计（RS256/HS256/密钥轮换/token 黑名单/刷新策略）、RBAC/ABAC 建模、SSO（Google/GitHub/SAML 2.0）、会话管理、magic link、MFA（TOTP/SMS/硬件密钥）和 API key 管理。 |
| `autoplan` | `gstack-autoplan` | 自动评审pipeline：从磁盘读取完整的CEO/design/eng/DX评审skill并按6条决策原则依次自动执行。在最终审批门控处暴露品味决策（接近的方案、边界scope、codex分歧）。一条命令完成全面评审。适用于"auto review""autoplan""run all reviews"或用户有plan文件想跳过中间问答时主动建议。 |
| `autoskill` | `autoskill` | 通过screenpipe观察用户屏幕，检测重复研究工作流，匹配现有scientific-agent-skills，为未覆盖的模式起草新skill或组合recipe。需要本地运行screenpipe daemon(port 3030)。所有检测在本地运行，仅脱敏聚类摘要发送给LLM。 |
| `backtest-expert` | `backtest-expert` | 系统化回测交易策略的专家指导。适用于开发/测试/压力测试/验证量化交易策略。覆盖 beating ideas to death 方法论、参数稳健性测试、滑点建模、偏差预防和解读回测结果。适用于用户询问 backtesting/strategy validation/robustness testing/avoiding overfitting/systematic trading development 时。 |
| `banner-design` | `banner-design` | 设计社交媒体/广告/网站 Hero/创意素材/印刷品 Banner。多种艺术方向可选配 AI 生成视觉素材。支持 Facebook/Twitter-X/LinkedIn/YouTube/Instagram/Google Display/网站 Hero/印刷品。风格：极简/渐变/粗体排版/摄影/插画/几何/复古/玻璃拟态/3D/霓虹/双色调/编辑风/拼贴。使用 ui-ux-pro-max/frontend-design/ai-artist/ai-multimodal skills。 |
| `baoyu-article-illustrator` | `baoyu-article-illustrator` | 分析文章结构，识别需配图位置，按类型×风格×配色三维度生成插图。用户说"为文章配图""illustrate article"时触发。 |
| `baoyu-comic` | `baoyu-comic` | 知识漫画创作工具，支持多种画风和语调，可生成带详细分镜布局的教育类原创漫画并批量出图。当用户要求创建知识漫画、教育漫画、传记漫画、教程漫画或 Logicomix 风格漫画时使用。 |
| `baoyu-compress-image` | `baoyu-compress-image` | 压缩图片为WebP（默认）或PNG，自动选择工具。适用于"compress image""optimize image""convert to webp"或减小图片文件大小。 |
| `baoyu-cover-image` | `baoyu-cover-image` | 生成文章封面图，5维度（类型/调色板/渲染/文字/情绪）组合11种配色和7种渲染风格。支持电影宽幅(2.35:1)、宽屏(16:9)和方形(1:1)。触发词包括"generate cover image""create article cover""make cover"。 |
| `baoyu-danger-gemini-web` | `baoyu-danger-gemini-web` | 通过逆向工程的Gemini Web API生成图片和文本：支持文本生成、prompt图片生成、参考图vision输入和多轮对话。适用于其他skill需要图片生成后端，或用户请求Gemini图片/文本生成及vision-capable AI生成。 |
| `baoyu-danger-x-to-markdown` | `baoyu-danger-x-to-markdown` | 将X(Twitter)推文和文章转换为带YAML front matter的markdown。使用逆向工程API，需用户同意。适用于"X to markdown""tweet to markdown""save tweet"或提供x.com/twitter.com URL进行转换。 |
| `baoyu-diagram` | `baoyu-diagram` | 创建专业深色主题 SVG 图表（架构图、流程图、时序图、思维导图等）。用户说"画个图""diagram""flowchart"或上传内容要求可视化时触发，输出独立 .svg 文件。 |
| `baoyu-electron-extract` | `baoyu-electron-extract` | 从已安装的Electron应用（.asar包）中提取资源和JavaScript，有.js.map时恢复原始源码，否则用Prettier格式化压缩代码。跳过node_modules，支持macOS和Windows。触发词包括"extract Electron app""decompile Electron""看Electron应用源码""提取.asar"等。 |
| `baoyu-format-markdown` | `baoyu-format-markdown` | 格式化纯文本或markdown文件：添加frontmatter、标题、摘要、heading、粗体、列表和代码块。适用于"format markdown""beautify article""add formatting"或改善文章排版。输出到{filename}-formatted.md。 |
| `baoyu-image-gen` | `baoyu-image-gen` | AI 图像生成，支持 OpenAI GPT Image 2/Azure OpenAI/Google/OpenRouter/DashScope/Z.AI GLM-Image/MiniMax/Jimeng/Seedream/Replicate/Agnes API。支持文生图、参考图、宽高比及从保存提示文件批量生成。默认顺序执行；用户已有多个提示或需稳定多图吞吐时使用批量并行。触发词：generate/create/draw images。 |
| `baoyu-infographic` | `baoyu-infographic` | 生成专业信息图，支持21种布局和22种视觉风格。分析内容后推荐布局×风格组合，生成可直接发布的信息图。触发词包括"infographic""信息图""visual summary""可视化""高密度信息大图"。 |
| `baoyu-markdown-to-html` | `baoyu-markdown-to-html` | 将 Markdown 转为带样式的 HTML，兼容微信主题。支持代码高亮、数学公式、Mermaid（通过 headless Chrome 渲染为 PNG）、PlantUML、脚注、警告框、信息图及可选外链转底部引用。触发词：markdown to html、convert md to html、md 转 html、微信外链转底部引用。 |
| `baoyu-post-to-wechat` | `baoyu-post-to-wechat` | 通过API或Chrome CDP发布内容到微信公众号。支持HTML/Markdown/纯文本输入的文章发布和多图贴图发布。Markdown文章工作流默认将外部链接转为底部引用以适配微信。触发词包括"发布公众号""post to wechat""微信公众号""贴图/图文/文章"。 |
| `baoyu-post-to-weibo` | `baoyu-post-to-weibo` | 通过Chrome CDP发布内容到微博，支持带文字/图片/视频的普通微博和Markdown输入的头条文章。触发词包括"发微博""发布微博""微博头条文章"等。 |
| `baoyu-post-to-x` | `baoyu-post-to-x` | 向 X（Twitter）发布内容和文章。支持带图片/视频的常规帖子及 X Articles（长文 Markdown）。Codex 环境中优先使用 Chrome Extension 工作流，否则用 Chrome Computer Use，仅在允许时回退到 Chrome CDP 脚本。触发词：post to X、tweet、publish to Twitter、share on X。 |
| `baoyu-slide-deck` | `baoyu-slide-deck` | 从内容生成专业幻灯片图像。先创建带风格指令的大纲，再生成单张幻灯片图像。触发词：create slides、make a presentation、generate deck、slide deck、PPT。 |
| `baoyu-translate` | `baoyu-translate` | 翻译技能，支持快翻/普通/精翻三种模式和自定义术语表。用户说"翻译""translate""精翻""本地化"或提供含翻译意图的 URL/文件时触发。 |
| `baoyu-url-to-markdown` | `baoyu-url-to-markdown` | 使用 baoyu-fetch CLI（Chrome CDP + 站点适配器）抓取任意 URL 并转为 markdown。内置 X/Twitter、YouTube、Hacker News 适配器，支持登录/CAPTCHA 交互等待。 |
| `baoyu-wechat-summary` | `baoyu-wechat-summary` | 使用本地wx-cli将微信群聊精华总结为结构化摘要。默认生成正常版，可选毒舌版。跨运行维护每群历史、用户画像和群事实记忆，内置隐私护栏。触发词包括"总结群聊""群聊精华""group chat digest""回溯画像"等。 |
| `baoyu-xhs-images` | `baoyu-xhs-images` | 生成信息图卡片系列：12 种视觉风格/8 种布局/3 种配色。将内容拆分为 1-10 张卡通风格图片卡片，优化社交媒体参与度。在用户提及小红书图片/小红书种草/小绿书/微信图文/微信贴图/image cards/图片卡片/baoyu-xhs-images 或想要社交媒体信息图系列时触发。 |
| `baoyu-youtube-transcript` | `baoyu-youtube-transcript` | 通过 URL 或视频 ID 下载 YouTube 视频字幕/封面图。支持多语言/翻译/章节/说话人识别。缓存原始数据以便快速重新格式化。适用于 get YouTube transcript/download subtitles/get captions/YouTube字幕/YouTube封面/视频封面/video thumbnail/video cover image 或提供 YouTube URL 并想提取字幕文本或封面图时。 |
| `behavioral-evals` | `behavioral-evals` | 创建、运行、修复和提升behavioral evaluation的指导。适用于验证agent决策逻辑、调试失败、调试prompt steering或添加workspace回归测试。 |
| `benchling-integration` | `benchling-integration` | Benchling Python SDK 和 REST API 集成：注册实体/库存/ELN 条目/工作流/Benchling Apps/Data Warehouse 查询。适用于使用 benchling-sdk 或 v2 API 自动化实验室数据时。 |
| `benchmark` | `gstack-benchmark` | 基于 browse daemon 的性能回归检测。建立页面加载时间、Core Web Vitals 和资源大小的基线，每次 PR 对比前后变化，跟踪性能趋势。触发词：performance、benchmark、page speed、lighthouse、web vitals、bundle size、load time、speed test、check performance。 |
| `benchmark-models` | `gstack-benchmark-models` | gstack skill跨模型benchmark：同一prompt通过Claude/GPT(Codex CLI)/Gemini并行运行，比较延迟/token/成本，可选LLM judge评质量。用数据回答"which model is best for this skill?"。区别于测量网页性能的/benchmark。触发词包括"benchmark models""compare models""model shootout"。 |
| `bgpt-paper-search` | `bgpt-paper-search` | 通过 BGPT MCP 服务器搜索科学论文并检索全文提取的结构化实验数据（25+ 字段含方法、结果、样本量、质量评分）。用于文献综述、证据综合和获取摘要之外的实验细节。 |
| `bids` | `bids` | 处理Brain Imaging Data Structure(BIDS)数据集：组织神经科学和生物医学数据（MRI/EEG/MEG/iEEG/PET/显微镜/NIRS/运动捕捉/EMG/MRS/行为数据）、查询BIDS布局、验证合规性、DICOM转BIDS、编写metadata sidecar、创建BIDS derivatives。 |
| `biopython` | `biopython` | 综合分子生物学工具包：序列操作、文件解析（FASTA/GenBank/PDB）、系统发育和编程化NCBI/PubMed访问（Bio.Entrez）。适用于批处理、自定义生信pipeline、BLAST自动化。快速查找用gget，多服务集成用bioservices。 |
| `bioservices` | `bioservices` | 统一的Python接口访问40+生信服务。适用于单个工作流中查询多个数据库（UniProt/KEGG/ChEMBL/Reactome）并保持API一致。最适合跨数据库分析和ID映射。单库快速查找用gget，序列/文件操作用biopython。 |
| `brainstorming` | `brainstorming` | 创造性工作前置技能。在创建功能、构建组件、添加特性或修改行为之前必须先使用，在实现前先探索用户意图、需求和设计方案。 |
| `brand` | `brand` | 品牌声音、视觉识别、消息框架、资产管理与品牌一致性。适用于品牌内容、语调、营销素材、品牌合规、风格指南等场景。 |
| `brand-guidelines` | `brand-guidelines` | 将 Anthropic 官方品牌配色和排版应用于任何可受益于 Anthropic 外观的制品。适用于品牌配色/风格指南/视觉格式/公司设计标准适用时。 |
| `brandkit` | `brandkit` | 高端品牌套件图像生成技能，创作品牌指南板、logo 系统、身份识别套件和视觉世界演示。针对极简、电影感、编辑风、暗科技、奢侈品等品牌系统优化。 |
| `breadth-chart-analyst` | `breadth-chart-analyst` | 分析市场宽度图表：S&P 500 Breadth Index（200日均线）和美股上升趋势股票比率图表。适用于用户提供宽度图表进行分析、请求市场宽度评估、定位策略建议或基于宽度指标理解中期战略和短期战术展望。也可不带图表直接从公共源获取CSV数据分析。所有分析和输出使用英文。 |
| `breakout-trade-planner` | `breakout-trade-planner` | 从 VCP screener 输出生成 Minervini 风格突破交易计划，含最坏情况风险计算/组合热度管理/Alpaca 兼容订单模板（预下单 stop-limit bracket/确认后 limit bracket）。适用于用户有 VCP screener 结果并想要带入场/止损/目标位和仓位大小的可执行交易计划时。 |
| `browse` | `gstack-browse` | 快速无头浏览器用于 QA 测试和站点自检。导航任意 URL、与元素交互、验证页面状态、diff 前后操作、截取带注释截图、检查响应式布局、测试表单和上传、处理对话框、断言元素状态。每命令约 100ms。适用于测试功能、验证部署、自检用户流程或用证据提交 bug。被要求 open in browser/test the site/take a screenshot/dogfood this 时使用。 |
| `browser-qa` | `browser-qa` | 部署功能后使用浏览器自动化进行视觉测试和 UI 交互验证。 |
| `bulk-rnaseq` | `bulk-rnaseq` | 端到端 bulk RNA-seq 编排：从原始 FASTQ 经 QC/trimming（FastQC/fastp）、比对定量（STAR/Salmon/featureCounts）、基因计数矩阵组装，到差异表达（pydeseq2）、通路富集（GSEA）和出版级图表。支持 nf-core/rnaseq 和独立路径。 |
| `canary` | `gstack-canary` | 部署后金丝雀监控：使用 browse daemon 监视线上应用的控制台错误、性能退化和页面故障，定期截图并与部署前基线对比，异常时告警。 |
| `canslim-screener` | `canslim-screener` | 使用William O'Neil的CANSLIM成长股方法论筛选美股。适用于CANSLIM选股、成长股分析、动量股识别或按O'Neil投资系统寻找盈利和价格动量强劲的标的。 |
| `canvas-design` | `canvas-design` | 使用设计理念在 .png 和 .pdf 文档中创建精美视觉艺术。适用于用户要求创建海报、艺术品、设计或其他静态作品时。创作原创视觉设计，避免复制现有艺术家作品以防侵权。 |
| `careful` | `gstack-careful` | 破坏性命令的安全护栏：在rm -rf、DROP TABLE、force-push、git reset --hard、kubectl delete等操作前警告。用户可逐项覆盖。适用于接触prod、调试线上系统或共享环境。触发词包括"be careful""safety mode""prod mode"。 |
| `cavecrew` | `cavecrew` | caveman 风格子代理委派决策指南。指导主线程何时派生 cavecrew-investigator（定位代码）、cavecrew-builder（1-2 文件编辑）或 cavecrew-reviewer（diff 审查），而非内联执行或使用普通 Explore。子代理输出经 caveman 压缩后回注主上下文，体积减少约 60%，延长长会话的主上下文寿命。触发词：delegate to subagent、use cavecrew、spawn investigator/builder/reviewer、save context、compressed agent output。 |
| `caveman` | `caveman` | 超压缩通信模式，实测减少 65% 输出 token，保持完整技术准确性。支持 lite/full/ultra/wenyan-lite/wenyan-full/wenyan-ultra 强度级别。用户说"caveman mode""less tokens"或调用 /caveman 时触发。 |
| `caveman-commit` | `caveman-commit` | 超压缩 commit 消息生成器，去除噪音保留意图和推理，Conventional Commits 格式。标题≤50 字符，仅在"why"不明显时加正文。暂存变更时自动触发。 |
| `caveman-compress` | `caveman-compress` | 将自然语言记忆文件（CLAUDE.md、todos、preferences）压缩为caveman格式以节省input token。保留所有技术内容、代码、URL和结构。压缩版覆盖原文件，人类可读备份保存为FILE.original.md。触发：/caveman-compress FILEPATH或"compress memory file"。 |
| `caveman-discover` | `caveman-discover` | 发现当前仓库中所有LLM工作流并标记，使Caveman Cloud按代码实际功能（support-reply/nightly-digest）而非匿名桶分组支出。适用于粘贴Caveman discovery prompt、说"discover workflows"或要求按工作流分解LLM支出。仓库应已通过caveman-setup接入gateway。 |
| `caveman-evidence-review` | `caveman-evidence-review` | 只读审查 Caveman Cloud 证据：成本/Cave Score/Cave Plan/工作流/traces/延迟/错误/压缩/路由和已验证节省。适用于用户询问 Caveman 发现了什么/LLM 支出去向/成本或质量为何变化/哪些工作流需关注/请求 trace 或分析审查时。优先使用 Caveman MCP 工具；回退到 CLI JSON。 |
| `caveman-explore` | `caveman-explore` | 只读仓库探索器。主动用于冷启动探索/广泛跨文件定位/或直接搜索失败需要找到某物所在位置时。当 issue 已指明确切文件或符号或前一轮已返回可用的 file:line 证据时跳过。仅返回紧凑 path:line 引用；其读取和 grep 不进入主对话。 |
| `caveman-help` | `caveman-help` | 所有 caveman 模式/skills/commands 的快速参考卡。一次性显示，非持久模式。触发：/caveman-help/caveman help/what caveman commands/how do I use caveman。 |
| `caveman-learn` | `caveman-learn` | 完结 Caveman learn 报告——审查排名的 token 消耗大户并应用降低成本修复（精简 config/将重复上下文卸载到 cavemem），每次编辑需同意。适用于用户运行 caveman learn/要求降低 agent token 成本/想精简过重的 CLAUDE.md/想把每次会话重复粘贴的上下文卸载到 cavemem 时。 |
| `caveman-manage` | `caveman-manage` | 检查Caveman Cloud的eval-gated实验生命周期并阻止不安全执行。适用于启动、批准、取消、提升或回滚Caveman实验，或询问实验证据支持的操作。先读证据，在服务端权威转换和证据门控上线前不执行生命周期变更。 |
| `caveman-optimize` | `caveman-optimize` | 将Caveman仅报告模式的仓库观察转化为用户选定的优化候选，配套baseline/candidate评估。适用于检查优化观察、评估候选变更或对当前Caveman优化报告采取行动。需要已登录Caveman CLI连接和明确批准；不从profile推断资金或执行。 |
| `caveman-review` | `caveman-review` | 超压缩代码审查评论，去除PR反馈噪音保留可操作信号。每条评论一行：位置+问题+修复。触发词包括"review this PR""code review""/review"等，PR审查时自动触发。 |
| `caveman-setup` | `caveman-setup` | 将当前仓库接入Caveman Cloud gateway，使每个LLM请求都被度量（成本/token/延迟），零行为变更。适用于用户粘贴Caveman setup prompt、说"set up caveman"或想为应用添加LLM支出可观测性。需要gateway URL和Cave API key。 |
| `caveman-stats` | `caveman-stats` | 显示当前会话的真实 token 用量和预估节省量。直接从 Claude Code 会话日志读取，非 AI 估算。由 mode-tracker hook 注入输出，模型本身不计算数字。触发：/caveman-stats。 |
| `cellxgene-census` | `cellxgene-census` | 编程查询 CZ CELLxGENE Census 获取版本化公共单细胞和空间转录组数据：群体级细胞元数据、基因表达切片、摘要计数、H5AD URI/下载、嵌入、空间数据和参考图谱比较。分析自有本地数据用 scanpy/anndata/scvi-tools。 |
| `changelog-gen` | `changelog-gen` | Changelog 生成器：从 Git 历史自动生成 CHANGELOG。 |
| `changelog-generator` | `changelog-generator` | 从 git commits 生成 changelog。适用于用户说 generate changelog/update changelog/what changed since last release 或准备新版本发布前。 |
| `chinese-code-review` | `chinese-code-review` | 中文review沟通参考：话术模板、分级标注（必须修复/建议修改/仅供参考）、国内团队常见反模式应对。仅在用户显式调用/chinese-code-review时使用，不根据上下文自动触发。 |
| `chinese-commit-conventions` | `chinese-commit-conventions` | 中文 commit 与 changelog 配置参考：Conventional Commits 中文适配、commitlint/husky/commitizen 中文模板、conventional-changelog 中文配置。仅在用户显式调用 /chinese-commit-conventions 时触发。 |
| `chinese-documentation` | `chinese-documentation` | 中文文档排版参考：中英文空格、全半角标点、术语保留、链接格式、中文文案排版指北约定。仅在用户显式调用/chinese-documentation时使用，不根据上下文自动触发。 |
| `chinese-git-workflow` | `chinese-git-workflow` | 国内Git平台配置参考：Gitee、Coding.net、极狐GitLab、CNB的SSH/HTTPS/凭据/CI接入差异与镜像同步配置。仅在用户显式调用/chinese-git-workflow时使用，不根据上下文自动触发。 |
| `ci` | `ci` | Gemini CLI专用skill，提供GitHub Actions workflow的高性能快速失败监控及CI失败的本地自动验证。只需提供分支名即可自动发现run。 |
| `cirq` | `cirq` | Google 量子计算框架 Cirq。适用于 Google Quantum AI 硬件、噪声感知电路设计及量子表征实验。针对 Google 硬件、噪声建模和底层电路设计；IBM 硬件用 qiskit，量子 ML 自动微分用 pennylane，物理仿真用 qutip。 |
| `citation-management` | `citation-management` | 学术研究综合引用管理：搜索OpenAlex/PubMed/Google Scholar论文、提取准确元数据、验证引用、生成格式化BibTeX条目。适用于查找论文、验证引用信息、DOI转BibTeX或确保科学写作中参考文献准确性。 |
| `claude` | `gstack-claude` | 非Claude host的Claude Code CLI封装，三种模式。Review：通过claude -p独立diff审查。Challenge：对抗性失败模式审查。Consult：只读文件工具向Claude询问仓库问题。适用于"claude review""claude challenge""ask claude""second opinion from claude""outside voice"。 |
| `claude-api` | `claude-api` | Claude API/Anthropic SDK参考：模型ID、定价、参数、streaming、tool use、MCP、agents、缓存、token计数、模型迁移。当prompt提及Claude/Anthropic、用户询问LLM相关问题（定价/模型选择/限制/缓存）、或任务为LLM相关且provider未指定时触发。若项目使用其他provider（OpenAI/Gemini/Llama等）则跳过。 |
| `claude-handoff` | `in-progress/claude-handoff` | 将当前对话交接给新的后台 agent 立即接续工作。 |
| `claude-handoff` | `claude-handoff` | 将当前对话交接给新的后台 agent 立即接续工作。 |
| `clean-code` | `clean-code` | Clean Code 原则（DRY/KISS/YAGNI）、命名、函数设计与可读性。适用于代码难读、方法过长、命名不清、重复或嵌套过深时。类职责拆分和依赖方向请用 solid-principles。 |
| `cleanddd-coach` | `cleanddd-coach` | 交互式 CleanDDD 教练技能，循序讲解并与用户互动练习 CleanDDD 核心原则与方法，包含微课、测验与检查清单，可承接到需求分析/建模/代码实现技能。 |
| `cleanddd-dotnet-coding` | `cleanddd-dotnet-coding` | 在 CleanDDD 项目中落地已建模需求（聚合/命令/查询/API Endpoints/事件/仓储/配置/测试）的编码指南。适用于编写或修改业务功能、端点与数据访问时。 |
| `cleanddd-dotnet-init` | `cleanddd-dotnet-init` | 初始化CleanDDD dotnet项目（netcorepal-web模板）。在创建新项目或为客户演示快速拉起解决方案时使用，可直接调用dotnet new或包装脚本。 |
| `cleanddd-modeling` | `cleanddd-modeling` | 基于 cleanddd-requirements-analysis 结果，输出符合 CleanDDD 的聚合、命令、事件、查询、API 端点、定时任务模型，从已拆解需求快速得到建模蓝图。 |
| `cleanddd-requirements-analysis` | `cleanddd-requirements-analysis` | 需求澄清与拆解，识别干系人并将需求条目标注所属对象与业务实体，仅产出结构化需求描述，可作为后续建模输入。 |
| `clickhouse-io` | `clickhouse-io` | ClickHouse 数据库模式/查询优化/分析/高性能分析工作负载的数据工程最佳实践。适用于编写 ClickHouse schemas 或查询或分析查询太慢时。 |
| `clinical-decision-support` | `clinical-decision-support` | 准备和验证仅用于研究的临床决策支持评估、证据profile、队列、生存、biomarker/模型、隐私和治理artifact。适用于聚合或合成研究文档和追溯——不用于患者护理或实时临床操作。 |
| `clinical-reports` | `clinical-reports` | 为临床病例、诊断、试验、安全及聚合研究报告创建安全有界的草案结构并运行本地确定性检查。仅使用合成、去标识化或聚合输入及经验证的源事实清单；所有输出需经合格人员审查。 |
| `cobrapy` | `cobrapy` | 约束型代谢建模(COBRA)：FBA、FVA、基因敲除、通量采样、SBML模型，用于系统生物学和代谢工程分析。 |
| `code-review` | `code-review` | 从固定点（commit/branch/tag/merge-base）起沿两个维度审查变更：Standards（是否符合仓库编码规范）和 Spec（是否匹配原始 issue/spec 要求）。并行子 agent 运行两项审查并并列报告。适用于审查分支、PR、进行中变更或用户要求 review since X 时。 |
| `code-review` | `engineering/code-review` | 从固定点（commit/branch/tag/merge-base）审查变更，沿两个轴并行：标准（是否符合仓库编码规范）和规格（是否匹配原始 issue/spec 要求）。用于审查分支、PR 或进行中变更。 |
| `code-reviewer` | `code-reviewer` | 代码审查技能。支持本地变更（暂存区或工作树）和远程 PR（按 ID 或 URL），聚焦正确性、可维护性及项目标准合规性。 |
| `codebase-design` | `codebase-design` | 设计 deep module 的共享词汇表。适用于用户想设计或改进模块接口、寻找深化机会、决定接缝位置、使代码更易测试或 AI 导航，或其他 skill 需要 deep-module 词汇时。 |
| `codebase-design` | `engineering/codebase-design` | 设计 deep module 的共享词汇表。适用于用户想设计或改进模块接口、寻找深化机会、决定接缝位置、使代码更易测试或 AI 导航，或其他 skill 需要 deep-module 词汇时。 |
| `codebase-onboarding` | `codebase-onboarding` | 分析陌生代码库并生成结构化上手指南，包含架构地图、关键入口、约定和初始 CLAUDE.md。加入新项目或首次配置 Claude Code 时使用。 |
| `coding-standards` | `coding-standards` | 跨项目通用编码规范基线，涵盖命名、可读性、不可变性和代码质量审查。无框架特定skill时用于代码质量或命名审查；框架特定模式请用对应前后端skill。 |
| `concurrency-review` | `concurrency-review` | 审查 Java 并发代码的线程安全、竞态条件、死锁和现代模式（Virtual Threads/CompletableFuture/@Async）。适用于用户要求 check thread safety/concurrency review/async code review 或审查多线程代码时。 |
| `confluence-cli` | `confluence-cli` | Confluence CLI 基础能力，包括环境检查、uv 安装、命令调用方式、参数说明、页面/附件/搜索等通用操作及 Markdown 发布转换规则。适用于查询、检索、读取、发布 Confluence 页面或确认 CLI 用法与环境。 |
| `consciousness-council` | `consciousness-council` | 对任何问题、决策或创意挑战运行多视角Mind Council审议。适用于需要多元观点、艰难决策帮助、council/panel讨论、多角度探索、devil's advocate分析，或面临无明显答案的两难/权衡/复杂选择时。 |
| `context-budget` | `context-budget` | 审计 Claude Code 上下文窗口消耗（agents/skills/MCP servers/rules），识别膨胀和冗余组件，产出优先级排序的 token 节省建议。上下文窗口填充过快时使用。 |
| `context-restore` | `gstack-context-restore` | 恢复之前 /context-save 保存的工作上下文，加载最近保存的状态（默认跨所有分支），即使跨 Conductor 工作区交接也能续接。与 /context-save 配对使用。 |
| `context-save` | `gstack-context-save` | 保存工作上下文。捕获 git 状态、已做决策和剩余工作，使未来会话可无缝接续。触发词：save progress、save state、context save、save my work。配合 /context-restore 恢复。原名 /checkpoint，因与 Claude Code 原生 rewind 别名冲突而更名。 |
| `continuous-learning-v2` | `continuous-learning-v2` | 基于直觉的学习系统 v2.1，通过 hooks 观察会话，创建带置信度评分的原子直觉，并将其演化为技能/命令/代理。新增项目级直觉防止跨项目污染。用于从会话中捕获经验教训、管理直觉或将其提升为技能/命令/代理。 |
| `contract-first` | `contract-first` | 当多个consumer和provider必须协同演进API或事件schema而不出现字段漂移、集成意外或一方静默重定义接口时使用。 |
| `contrarian-setup-gate` | `contrarian-setup-gate` | 合成 Jason Shapiro 反向交易管线三项裁决（COT 拥挤度、新闻反应失败、周线价格行为确认）为可操作的 setup_status，采用故障关闭优先级状态机。纯离线合成，无需网络、API key 或额外计算。 |
| `cot-contrarian-detector` | `cot-contrarian-detector` | 基于 CFTC COT 报告检测期货市场拥挤投机头寸，寻找反向交易机会（Jason Shapiro 方法论）。通过 FMP API 扫描 65 个期货市场的大投机者净持仓，计算 3 年和 26 周 COT Index，将极端值分类为 CROWDED_LONG/CROWDED_SHORT。仅自动化拥挤检测（5 步中的第 1 步），不单独生成交易信号。 |
| `crypto-regime-analyzer` | `crypto-regime-analyzer` | 利用免费公开数据（CoinGecko+Binance funding）量化加密市场regime健康度，生成0-100综合评分（100=risk-on）及仓位建议。无需API key。适用于加密市场状况、alt season、BTC dominance、risk-on/off判断及仓位调整决策。 |
| `cso` | `gstack-cso` | 首席安全官模式：基础设施优先的安全审计，含密钥考古、依赖供应链、CI/CD 安全、LLM/AI 安全、OWASP Top 10、STRIDE 威胁建模和主动验证。日常模式（零噪音）和综合模式（月度深扫）。 |
| `dashboard-builder` | `dashboard-builder` | 为Grafana、SigNoz等平台构建能回答运维实际问题的监控dashboard，而非虚荣指标面板。适用于将metrics转化为可用dashboard的场景。 |
| `dask` | `dask` | Dask分布式计算，用于超出内存限制的pandas/NumPy工作流或跨集群扩展。适用于并行文件处理、分布式ML、与现有pandas代码集成。单机out-of-core分析用vaex，内存加速用polars。 |
| `data-quality-checker` | `data-quality-checker` | 在发布前验证市场分析文档和博客文章的数据质量。检查价格尺度不一致（ETF vs期货）、标的符号错误、日期/星期不匹配、配置总和错误和单位不匹配。支持英文和日文内容。咨询模式——标记问题为警告供人工审查，不作为阻断。 |
| `data-throughput-accelerator` | `data-throughput-accelerator` | 大规模数据导入、回填、导出、ETL、数仓加载、manifest 追赶或表同步需要大幅提速且保持数据正确性时使用。 |
| `database-lookup` | `database-lookup` | 查询有文档的公共数据库API，提供明确的端点、过滤器、分页和来源追溯。适用于需要从指定来源可复现地检索科学、监管、金融或其他数据库事实，而非从一般知识推断。 |
| `database-migrations` | `database-migrations` | 数据库迁移最佳实践，涵盖 PostgreSQL/MySQL 及常见 ORM（Prisma/Drizzle/Kysely/Django/TypeORM/golang-migrate）的 schema 变更、数据迁移、回滚及零停机部署。用于编写 schema 或数据迁移、规划回滚或追求零停机部署。 |
| `datamol` | `datamol` | RDKit的Pythonic封装，简化接口和合理默认值。首选用于标准药物发现：SMILES解析、标准化、描述符、指纹、聚类、3D构象、并行处理。返回原生rdkit.Chem.Mol对象。需高级控制或自定义参数时直接用rdkit。 |
| `db-migrator` | `db-migrator` | 数据库迁移助手，提供 Schema 对比和迁移脚本生成功能。 |
| `db-whisperer` | `db-whisperer` | 诊断和优化应用层数据库（Postgres/MySQL/SQLite/MongoDB）：EXPLAIN ANALYZE、慢查询检测、索引策略、N+1检测、带up/down脚本的schema迁移、连接池、复制设置、vacuum/analyze操作。适用于"query is slow""add an index""N+1""explain query plan""replication lag""connection pool exhausted"等场景。 |
| `deep-research` | `deep-research` | 通用深度研究agent团队，13-agent pipeline用于任何主题的严谨学术研究。8种模式：完整研究、快速简报、论文评审、文献综述、事实核查、三段式文献扫描、苏格拉底引导研究对话、系统综述+可选meta分析。覆盖研究问题构建、方法论设计、系统文献检索、来源验证、跨源综合、偏倚风险评估、APA 7.0报告、编辑审查、devil's advocate、伦理审查和后研究文献监控。 |
| `deep-research-ecc` | `deep-research-ecc` | 使用firecrawl和exa MCP进行多源深度研究，搜索网络、综合发现并交付带来源归属的引用报告。适用于需要对任何主题进行带证据和引用的深入研究。 |
| `deepchem` | `deepchem` | DeepChem 分子机器学习工具，提供多样化特征化器和预置数据集。用于 ADMET/毒性等性质预测（传统 ML 或 GNN），适合快速实验预训练模型和多种分子表示。图优先 PyTorch 工作流用 torchdrug，基准数据集用 pytdc。 |
| `deepspot-m` | `deepspot-m` | 使用 DeepSpot-M 从 H&E 组织学切片生成全转录组虚拟空间转录组。适用于需要 224x224 tiles 约 20x 下 log1p-CPM 空间基因表达、按基因符号查询蛋白编码基因而非固定 panel、或用 histolab 切片后在全切片上运行预测时。 |
| `deeptools` | `deeptools` | NGS分析工具包：BAM转bigWig、QC（相关性/PCA/fingerprints）、热力图/profile（TSS/peaks），用于ChIP-seq/RNA-seq/ATAC-seq可视化。 |
| `dep-auditor` | `dep-auditor` | 审计 Node.js/Python/Go/Rust/JVM/Ruby 项目的依赖漏洞、版本健康度与许可证事实。适用于检查 package.json/lockfile/requirements/go.mod/Cargo.toml/pom.xml/Gemfile.lock 或生成不改依赖的中文审计报告时。 |
| `deploy-ninja` | `deploy-ninja` | 零停机部署：蓝绿/金丝雀/滚动更新/Feature Flag 灰度发布。覆盖 Kubernetes/Docker/Cloudflare Workers/Terraform 和 CI/CD pipeline 搭建。适用于部署应用/搭建部署 pipeline/实现金丝雀发布/配置滚动更新/管理 feature flags/任何发布自动化。也在 deploy to production/set up CI/CD/blue-green deployment/canary release/rolling update/zero-downtime deploy/rollback/push this to prod/how do I safely release this 时触发。 |
| `deploy-to-vercel` | `deploy-to-vercel` | 将应用和网站部署到 Vercel。适用于用户请求部署操作如 deploy my app/deploy and give me the link/push this live/create a preview deployment 时。 |
| `deployment-patterns` | `deployment-patterns` | 部署工作流、CI/CD pipeline模式、Docker容器化、健康检查、回滚策略和生产就绪检查清单。适用于搭建CI/CD、容器化应用或发布前检查生产就绪状态。 |
| `depmap` | `depmap` | 查询 Cancer Dependency Map (DepMap) 获取癌细胞系基因依赖性评分（CRISPR Chronos）、药物敏感性数据和基因效应谱。用于识别癌症特异性脆弱性、合成致死相互作用和验证肿瘤药物靶点。 |
| `design` | `design` | 综合设计能力：品牌识别/设计 token/UI 样式/Logo 生成（55 种风格 Gemini AI）/企业形象方案 CIP（50 项交付物）/HTML 演示文稿（Chart.js）/Banner 设计（22 种风格）/图标设计（15 种风格 SVG Gemini 3.1 Pro）/社交媒体图片（HTML→截图多平台）。支持 Facebook/Twitter/LinkedIn/YouTube/Instagram/Pinterest/TikTok/Threads/Google Ads。 |
| `design-consultation` | `gstack-design-consultation` | 设计咨询：理解你的产品、研究行业现状、提出完整设计系统（美学/排版/配色/布局/间距/动效）并生成字体+配色预览页。创建 DESIGN.md 作为项目设计唯一真相源。现有站点请用 /plan-design-review 推断系统。适用于被要求 design system/brand guidelines/create DESIGN.md 时。新项目 UI 无现有设计系统或 DESIGN.md 时主动建议。 |
| `design-html` | `gstack-design-html` | 设计定稿：生成生产质量的 Pretext-native HTML/CSS。可与 /design-shotgun 批准的 mockup/CEO 计划/设计审查上下文配合使用，或从用户描述从头开始。文本真正回流/高度计算/布局动态。30KB 开销零依赖。智能 API 路由：为每种设计类型选择合适的 Pretext 模式。适用于 finalize this design/turn this into HTML/build me a page/implement this design 或任何规划 skill 之后。用户已批准设计或有现成计划时主动建议。 |
| `design-patterns` | `design-patterns` | 常见设计模式及 Java 示例（Factory/Builder/Strategy/Observer/Decorator 等）。适用于用户要求 implement pattern/use factory/strategy pattern 或设计可扩展组件时。 |
| `design-review` | `gstack-design-review` | 设计师视角QA：发现视觉不一致、间距问题、层级问题、AI slop模式和慢交互，然后修复。在源码中迭代修复，每次原子提交并用前后截图重新验证。Plan-mode设计审查用/plan-design-review。适用于"audit the design""visual QA""design polish"或用户提到视觉不一致时主动建议。 |
| `design-shotgun` | `gstack-design-shotgun` | Design shotgun：生成多个AI设计变体、打开对比面板、收集结构化反馈并迭代。独立的设计探索工具。适用于"explore designs""show me options""design variants""visual brainstorm"或用户对UI外观不满意时。当用户描述UI功能但未见过效果时主动建议。 |
| `design-system` | `design-system` | Token 架构、组件规范和幻灯片生成。三层 tokens（primitive→semantic→component）、CSS 变量、间距/排版比例、组件规范、战略幻灯片创建。适用于设计 tokens、系统化设计、品牌合规演示文稿。 |
| `design-system-ecc` | `design-system-ecc` | 生成或审计设计系统、检查视觉一致性、审查涉及样式的 PR。适用于设计系统构建、样式变更评审场景。 |
| `design-taste-frontend` | `taste-skill` | 反模板化前端技能，用于落地页、作品集和重设计。读取需求推断设计方向，交付不像模板的界面；重设计优先审计，严格预检。 |
| `design-taste-frontend-v1` | `taste-skill-v1` | 原始 v1 taste-skill，保留给依赖其精确行为的项目。当前默认为 design-taste-frontend（v2 实验版），是大幅重写版。仅在需要精确向后兼容时使用此 v1 安装名。 |
| `devex-review` | `gstack-devex-review` | 实时开发者体验审计：用浏览工具实际测试 DX，导航文档、尝试入门流程、计时 TTHW、截图错误信息、评估 CLI 帮助文本。产出带证据的 DX 记分卡。 |
| `dhdna-profiler` | `dhdna-profiler` | 从任意文本提取认知模式和思维指纹。用于分析某人如何思考、理解认知风格、分析写作或言语模式、比较不同人的思维风格。触发词：thinking style、analyze reasoning、cognitive profile、thinking pattern、DHDNA、digital DNA，或提供文本希望深入了解作者的推理模式、决策风格或认知签名。 |
| `diagnosing-bugs` | `diagnosing-bugs` | 疑难 bug 和性能回退的诊断循环。适用于用户说 diagnose/debug this 或报告某些东西坏了/抛异常/失败/变慢时。 |
| `diagnosing-bugs` | `engineering/diagnosing-bugs` | 疑难 bug 和性能回退的诊断循环。适用于用户说 diagnose/debug this 或报告某些东西坏了/抛异常/失败/变慢时。 |
| `diagram` | `gstack-diagram` | 将英文描述（或mermaid源码）转为图表三件套：源码、可在excalidraw.com打开编辑的.excalidraw文件、渲染的SVG+PNG。完全离线。适用于"make a diagram""draw the architecture""create a flowchart""diagram this""visualize this flow"。 |
| `diagram-design` | `diagram-design` | 创建各类品牌化图表（架构、流程、时序、ER、泳道、Wardley map、UML 类等），输出独立 HTML/SVG/PNG。支持重绘 .drawio/.mmd 源、导入品牌 token、添加语义模式和手绘风格。 |
| `diffdock` | `diffdock` | DiffDock和DiffDock-L分子对接：从PDB或序列+SMILES/SDF/MOL2进行蛋白-小分子pose预测、批量对接、虚拟筛选和pose置信度解读。不用于结合亲和力预测。 |
| `discernment-nudge` | `discernment-nudge` | 在给出实质性回答或草稿（建议、方案、计划、提案、邮件、估算、数据分析、事实陈述、多步论证）后、最终发送前触发，追加 2-3 个简短跟进问题，帮助用户核查关键事实、探查推理假设、发现缺失上下文。每次对话最多一次。简单 how-to、纯教育解释、格式转换、代码执行、创意写作、闲聊或已要求复核/引用/审查时跳过。 |
| `dispatching-parallel-agents` | `dispatching-parallel-agents` | 面对2个以上可独立进行、无共享状态或顺序依赖的任务时使用，分派并行agent执行。 |
| `dividend-growth-pullback-screener` | `dividend-growth-pullback-screener` | 筛选高质量股息增长股（年股息增长12%+、收益率1.5%+）中经历暂时回调的标的，通过RSI超卖条件（RSI≤40）识别。结合基本面股息分析与技术择时指标，在短期弱势中发现强势股息成长股的买入机会。 |
| `dnanexus-integration` | `dnanexus-integration` | 在 DNAnexus 上构建和运行可复现基因组学工作负载，使用 dx CLI/dxpy/apps/applets/dxCompiler/Nextflow。覆盖数据传输、dxapp.json 开发、执行监控、工作流导入和项目自动化。 |
| `doc-coauthoring` | `doc-coauthoring` | 引导用户通过结构化工作流协同撰写文档。适用于写文档、提案、技术规范、决策文档等结构化内容。帮助用户高效传递上下文、迭代精炼内容并验证文档对读者的有效性。用户提及写文档、创建提案、起草规范等任务时触发。 |
| `docker-patterns` | `docker-patterns` | Docker 和 Docker Compose 模式：本地开发/加固 CLI 安装器 harness/容器安全/网络/volumes/多服务编排。适用于创建或审查 Dockerfiles 和 Compose services/跨 Linux 发行版测试安装器/规划准确的 macOS 和 Windows 原生验证。 |
| `docs-changelog` | `docs-changelog` | 根据提供的版本号和原始变更数据生成并格式化新版本 changelog 文件。 |
| `docs-writer` | `docs-writer` | 文档编写技能。当任务涉及 /docs 目录下的文件或仓库中任何 .md 文件的撰写、审查或编辑时，始终使用此技能。 |
| `document-generate` | `gstack-document-generate` | 从零生成功能、模块或整个项目的缺失文档，使用 Diataxis 框架（tutorial/how-to/reference/explanation）产出完整结构化文档。可独立调用或由 /document-release 在发现覆盖缺口时调用。 |
| `document-release` | `gstack-document-release` | 发版后文档更新：读取所有项目文档、交叉引用diff、构建Diataxis覆盖图（reference/how-to/tutorial/explanation）、更新README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md以匹配已发布内容、检测架构图漂移、用sell-test rubric润色CHANGELOG语气、清理TODOS、可选bump VERSION。在PR body中暴露文档债务。适用于"update the docs""sync documentation""post-ship docs"，PR合并或代码发布后主动建议。 |
| `documentation-lookup` | `documentation-lookup` | 通过Context7 MCP使用最新的库和框架文档代替训练数据。适用于setup问题、API参考、代码示例或用户提及框架名（React/Next.js/Prisma等）时激活。 |
| `docx` | `docx` | 当用户想创建/读取/编辑/操作 Word 文档（.docx）或 Word 模板（.dotx）时使用。触发条件：提及 Word doc/word document/.docx/.dotx 或要求生成带目录/标题/页码/信头等格式的专业文档。也适用于从 .docx/.dotx 提取或重组内容、插入/替换图片、查找替换、处理修订/批注或将内容转为精美 Word 文档。不适用于 PDF/表格/Google Docs 或与文档生成无关的编码任务。 |
| `domain-modeling` | `domain-modeling` | 构建和打磨项目领域模型。适用于讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。 |
| `domain-modeling` | `engineering/domain-modeling` | 构建和打磨项目领域模型。适用于讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。 |
| `downtrend-duration-analyzer` | `downtrend-duration-analyzer` | 分析历史下跌趋势持续时间，生成交互式 HTML 直方图，按板块和市值展示典型回调长度。 |
| `drawdown-circuit-breaker` | `drawdown-circuit-breaker` | 从trader-memory-core状态评估账户级回撤熔断规则，决定今日是否允许新交易风险。使用已实现P&L、连败冷却和周/月回撤限制，无需外部API。 |
| `ds-mapper` | `ds-mapper` | 项目目录结构地图：生成带说明的可视化目录树，快速理解任意代码库。 |
| `dual-axis-skill-reviewer` | `dual-axis-skill-reviewer` | 双轴方法审查skill：(1)确定性代码检查（结构/脚本/测试/执行安全）和(2)LLM深度审查发现。适用于skills/*/SKILL.md的可复现质量评分、以分数阈值（如90+）gate merge或为低分skill提供具体改进项。支持--project-root跨项目。 |
| `e2e-testing` | `e2e-testing` | Playwright E2E 测试模式，涵盖 Page Object Model、配置、CI/CD 集成、产物管理及 flaky test 策略。用于编写 Playwright 测试、构建页面对象或修复 CI 中不稳定的 E2E 运行。 |
| `earnings-calendar` | `earnings-calendar` | 使用 Financial Modeling Prep（FMP）API 获取美股即将发布的财报公告。适用于用户请求 earnings calendar 数据/想知道下周哪些公司发布财报/需要每周财报回顾时。聚焦市值 20 亿美元以上的中大盘公司，按日期和时间组织为干净的 markdown 表格。支持多环境（CLI/Desktop/Web）和灵活的 API key 管理。 |
| `earnings-trade-analyzer` | `earnings-trade-analyzer` | 使用 5 因子评分系统（缺口大小、财报前趋势、成交量趋势、MA200 位置、MA50 位置）分析近期财报后股票，评分 0-100 并划分 A/B/C/D 等级。用于财报交易分析和动量筛选。 |
| `economic-calendar-fetcher` | `economic-calendar-fetcher` | 通过 FMP API 获取未来经济事件和数据发布（央行决议、就业报告、通胀、GDP 等），默认查未来 7 天，助手筛选评估影响并生成 Markdown 报告。 |
| `edge-candidate-agent` | `edge-candidate-agent` | 从 EOD 观测生成并排序美股多头边缘研究工单，导出管线就绪的候选规格供 trade-strategy-pipeline Phase I 使用。用于将假设/异常转化为可复现研究工单、将验证过的想法转为 strategy.yaml + metadata.json，或在运行管线回测前预检接口兼容性（edge-finder-candidate/v1）。 |
| `edge-concept-synthesizer` | `edge-concept-synthesizer` | 将detector tickets和hints抽象为可复用的edge concepts，包含thesis、invalidation signals和strategy playbooks，用于策略设计/导出前。 |
| `edge-hint-extractor` | `edge-hint-extractor` | 从每日市场观察和新闻反应中提取edge hints，可选LLM辅助生成，输出标准hints.yaml供下游概念合成与自动检测使用。 |
| `edge-pipeline-orchestrator` | `edge-pipeline-orchestrator` | 编排完整的 edge 研究流水线：从候选检测到策略设计、审查、修订和导出。用于端到端协调多阶段 edge 研究工作流。 |
| `edge-signal-aggregator` | `edge-signal-aggregator` | 聚合和排序来自多个edge-finding skill（edge-candidate-agent、theme-detector、sector-analyst、institutional-flow-tracker）的信号，生成带加权评分、去重和矛盾检测的优先级conviction dashboard。 |
| `edge-strategy-designer` | `edge-strategy-designer` | 将抽象 edge 概念转化为策略草案变体和可选的可导出 ticket YAML，供 edge-candidate-agent 导出/验证。 |
| `edge-strategy-reviewer` | `edge-strategy-reviewer` | 对edge-strategy-designer生成的策略草案进行关键审查，评估edge合理性、过拟合风险、样本量充分性和执行可行性。当strategy_drafts/*.yaml存在且需在pipeline导出前通过质量门时使用，输出PASS/REVISE/REJECT判定及置信度评分。 |
| `email-ops` | `email-ops` | ECC 的证据优先邮箱分诊/起草/发送验证/已发送邮件安全跟进工作流。适用于用户想组织邮件/通过真实邮件界面起草或发送/证明已发送到 Sent 时。 |
| `embedded-captions` | `embedded-captions` | 为单人出镜视频添加字幕，无需剪辑原片。支持逐字字幕、电影级嵌入主体后方字幕、VFX 特效字幕及 35 种风格目录中的指定样式。按视觉风格路由而非后端引擎。默认使用静默 anchor rail；仅在用户明确要求全电影级处理时才嵌入每个词。全流程本地运行（含转录和主体抠像），多镜头素材需先拆分再处理。 |
| `env-manager` | `env-manager` | 环境变量管理器：扫描、校验、同步.env文件，生成安全配置模板。 |
| `error-handling` | `error-handling` | TypeScript/Python/Go 的健壮错误处理模式。覆盖类型化错误/error boundaries/重试/熔断器/面向用户的错误消息。适用于在 TypeScript/Python/Go 中设计错误类型/重试/熔断器/面向用户的失败消息时。 |
| `error-translator` | `error-translator` | 编程错误消息翻译专家：将英文错误消息翻译成中文，解释原因并提供修复方案。 |
| `eslint-fix` | `eslint-fix` | 安全诊断并修复 ESLint error/warning 和配置兼容问题。优先使用项目锁定的包管理器与版本，先预检再修改，不自动下载最新版或批量改写无关源码。 |
| `esm` | `esm` | 直接使用esm Python SDK、ESM3/ESMC模型ID、Forge/Biohub推理客户端或ESMFold2折叠工作流时使用。 |
| `etetoolkit` | `etetoolkit` | 使用 ETE 4 分析、操作、比较、注释和可视化系统发育树或层级树。支持 Newick/Nexus I/O、拓扑编辑、Robinson-Foulds 比较、基因树进化事件、NCBI/GTDB 分类学和出版渲染。不用于从原始序列推断树。 |
| `exa-search` | `exa-search` | 基于Exa的网络工具包，专为科技内容调优。覆盖网页搜索（语义查找/研究/时事信息，可选research paper分类和学术域过滤）和URL提取（批量获取页面/文章/学术PDF）。适用于需要高质量搜索或学术过滤的网络任务。 |
| `executing-plans` | `executing-plans` | 当有一份书面实现计划需要在单独会话中执行并设有审查检查点时使用。 |
| `experimental-design` | `experimental-design` | 在数据收集前设计实验和研究：选择设计方案、随机化、区组、处理组合布局以确保结果可解释。适用于研究规划、分组分配、随机化、分层、对照、因子设计、DOE、响应面优化、交叉/重复测量/裂区设计、拉丁方、批次效应、复制vs伪复制、序贯/自适应设计等。样本量计算用statistical-power，已收集数据分析用statistical-analysis。 |
| `exploratory-data-analysis` | `exploratory-data-analysis` | 对明确支持的科学文件执行有界本地探索性分析：CSV/TSV/JSON脱敏profile，可选NumPy/HDF5/FASTA/FASTQ及基础图像元数据检查；缺失值/泄漏审计；异常值和变换敏感性分析；严格的EDA报告脚手架。其他领域格式仅供参考，未知格式安全失败。 |
| `exposure-coach` | `exposure-coach` | 整合 breadth/regime/flow 分析技能的信号，生成一页 Market Posture 摘要：净敞口上限、成长vs价值偏好、参与广度、允许新开仓vs现金优先建议。 |
| `faceless-explainer` | `faceless-explainer` | 将任意文本（文章、笔记、主题、简报）转为无真人出镜的解释视频：无网站或实拍素材，每场景独立生成视觉（排版、抽象图形、图表、数据可视化）。适用于主题解释、概念拆解、教程、列表类内容。非网站推广视频（用 /product-launch-video）。不确定时用 /hyperframes。 |
| `fastapi-patterns` | `fastapi-patterns` | FastAPI最佳实践：项目结构、Pydantic v2 schema、依赖注入、async handler、认证授权、事务性service层、httpx+pytest测试。适用于构建或审查FastAPI应用。 |
| `figma` | `figma` | 将Figma内容导入HyperFrames组合：渲染资产、brand tokens、components、storyboard sections→重建动效（frames读为states非slides）。支持REST/CLI、connector辅助动效和shader。适用于粘贴figma.com链接或将Figma设计/frame/logo/品牌/动画导入视频/组合。 |
| `find-skills` | `find-skills` | 帮助用户发现和安装agent skill，当用户问"how do I do X""find a skill for X""is there a skill that can..."或表达扩展能力兴趣时使用。 |
| `finishing-a-development-branch` | `finishing-a-development-branch` | 当实现完成、所有测试通过、需要决定如何集成这份工作时使用。 |
| `finviz-screener` | `finviz-screener` | 从自然语言请求构建并打开FinViz screener URL。适用于筛选股票、按条件查找股票、按基本面或技术面过滤或用特定条件打开FinViz。支持日文和英文输入。 |
| `fireworks-tech-graph` | `fireworks-tech-graph` | 创建技术图表：软件架构、数据流、流程图、序列图、C4、云部署、事件流、可观测性调查、agent/memory系统、UML/ER、网络拓扑、时间线和技术概念图。导出SVG/PNG/语义SVG-to-GIF动效或离线交互式HTML。"Generate GIF"等请求视为动效需求。不用于照片、栅格艺术或定量数据图表。 |
| `fireworks-tech-graph` | `fireworks-tech-graph/skills/fireworks-tech-graph` | 创建技术图表：软件架构、数据流、流程图、序列图、C4、云部署、事件流、可观测性调查、agent/memory系统、UML/ER、网络拓扑、时间线和技术概念图。导出SVG/PNG/语义SVG-to-GIF动效或离线交互式HTML。"Generate GIF"等请求视为动效需求。不用于照片、栅格艺术或定量数据图表。 |
| `flowio` | `flowio` | 使用 FlowIO 读写 FCS 2.0/3.0/3.1 流式细胞术文件，支持元数据检查、NumPy 事件提取、多数据集处理和表导出。补偿、转换、门控用 FlowKit。 |
| `fluidsim` | `fluidsim` | 规划、配置、检查、重启和分析有界的FluidSim CFD模拟，包含明确的数值有效性和HPC安全检查。适用于FluidSim求解器选择、参数审查、FFT/MPI设置、输出诊断或重启兼容性。 |
| `freestocklineskill` | `freestocklineskill` | 免费无需API Key的A股生态数据查询skill，覆盖沪深京股票、指数、ETF/LOF、可转债、行业/概念板块、实时行情、K线、涨跌排行、涨停/跌停/炸板、资金流、财务估值、公告、龙虎榜、大宗交易、融资融券、新闻快讯、筹码等公开数据。 |
| `freeze` | `gstack-freeze` | 将会话中的文件编辑限制到指定目录，阻止允许路径外的 Edit 和 Write。调试时防止意外修改无关代码，或限定变更范围到一个模块时使用。 |
| `frontend-a11y` | `frontend-a11y` | React 和 Next.js 的无障碍模式：语义化 HTML/ARIA 属性/表单标签/键盘导航/焦点管理和屏幕阅读器支持。适用于构建任何交互式 UI 组件或表单时。 |
| `frontend-design` | `frontend-design` | 构建新 UI 或重塑现有 UI 时的独特、有意图的视觉设计指导。帮助确定美学方向、排版选择和避免模板化默认外观。 |
| `frontend-patterns` | `frontend-patterns` | React/Next.js 前端开发模式，涵盖状态管理、性能优化和 UI 最佳实践。构建或审查 React/Next.js 组件、状态或渲染性能时使用。 |
| `frontend-slides` | `frontend-slides` | 从零创建或转换 PowerPoint 文件为精美动画 HTML 演示文稿。当用户想构建演示文稿、将 PPT/PPTX 转为网页或为演讲/路演创建幻灯片时使用。帮助非设计师通过视觉探索而非抽象选择发现自己的审美风格。 |
| `ftd-detector` | `ftd-detector` | 使用 William O'Neil 方法检测 Follow-Through Day (FTD) 信号确认市场底部。双指数跟踪（S&P 500 + NASDAQ）含状态机监测反弹尝试、FTD 资格和后续健康度。与市场顶部检测器互补。 |
| `full-output-enforcement` | `output-skill` | 覆盖LLM默认截断行为，强制完整代码生成、禁止占位符模式、干净处理token上限分割。适用于任何需要详尽无删减输出的任务。 |
| `futures-position-sizer` | `futures-position-sizer` | 根据方向、入场价和止损计算基于合约的期货仓位大小，使用经验证的每品种合约规格（乘数/tick size/tick value）。适用于询问期货交易合约数量、期货仓位 sizing（ES/NQ/ZB/GC/CL/6E/VX/BT等）或承接contrarian-setup-gate的READY_FOR_PLAN信号。纯离线计算，无需API key和网络。 |
| `fxmacrodata-calendar` | `fxmacrodata-calendar` | 获取FXMacroData官方宏观发布日历事件，用于交易规划、宏观regime检查和事件风险过滤。适用于CPI/NFP/GDP/PCE/零售/PMI/央行决议窗口前使用。 |
| `general-video` | `general-video` | 当没有专门工作流适用或 BRIEF.md 设置 flow: companion 时，编写或编辑自定义 HyperFrames 组合。适用于较长或多场景作品、品牌和 sizzle reels、蒙太奇、静态循环、静态标题卡、素材混剪和自由构建。短小无旁白运动优先单元（含动画标题）请用 motion-graphics。新创作请先通过 hyperframes 路由。 |
| `generate-image` | `generate-image` | 通过 OpenRouter Image API（Gemini/Seedream/Recraft/GPT-Image/Riverflow）生成或编辑图像。用于照片、插画、艺术品、概念艺术、视觉资产、logo 及基于参考图的图像编辑/合成。流程图/电路图/通路图等技术图表用 scientific-schematics。 |
| `geniml` | `geniml` | 使用Geniml进行经审计的本地基因组区间工作流：验证BED和universe契约、规划Region2Vec或scEmbed运行、检查模型/tokenizer兼容性、评估共识universe。 |
| `genomic-coordinates` | `genomic-coordinates` | 在坐标约定间转换基因组区间、归一化和比较变异表示、检测assembly或contig命名不匹配。适用于跨格式/工具/assembly边界的坐标转换（BED/GFF/GTF/VCF/SAM/BAM/WIG/PSL/genePred/Picard interval_list/region string）、0-based半开与1-based包含的对齐、indel左对齐/trimming、检查两个变异记录是否描述同一变化、基因组到转录本/CDS/蛋白位置映射、BED/GTF/VCF约定违规审计、GRCh37/hg19/GRCh38/T2T/chr-prefix/liftover问题诊断。 |
| `genomic-intelligence` | `genomic-intelligence` | 通过Genomic Intelligence托管的transformer DNA语言模型直接从DNA序列预测调控特征、基因结构和表达，无需本地GPU或模型权重。REST API和托管MCP server（免key公开demo）支持六项任务：启动子区域、剪接供体/受体位点、增强子活性、染色质状态、序列到表达(log TPM)和从头基因注释，及组合工作流find-genes-then-predict-expression。 |
| `geomaster` | `geomaster` | 综合地理空间科学 skill：遥感/GIS/空间分析/地球观测机器学习/30+ 科学领域。支持卫星影像处理（Sentinel/Landsat/MODIS/SAR/高光谱）/矢量和栅格数据操作/空间统计/点云处理/网络分析/云原生工作流（STAC/COG/Planetary Computer）/8 种编程语言（Python/R/Julia/JavaScript/C++/Java/Go/Rust）含 500+ 代码示例。适用于遥感工作流/GIS 分析/空间 ML/地球观测数据处理/地形分析/水文建模/海洋空间分析/大气科学/任何地理空间计算任务。 |
| `geopandas` | `geopandas` | Python GeoPandas工作流的指导和当地审计工具，覆盖GeoSeries、GeoDataFrame、空间操作和矢量数据I/O。 |
| `get-available-resources` | `get-available-resources` | 检测主机资源清单及有效CPU、内存、磁盘、调度器、容器和加速器上限，用于资源感知规划或资源敏感的本地负载前评估。输出脱敏JSON快照和保守规划辅助信息，不做压力测试，不假设可见硬件均可用。 |
| `gget` | `gget` | 快速CLI/Python查询20+生信数据库：基因信息、BLAST/BLAT、病毒序列下载、AlphaFold结构、富集分析、OpenTargets、COSMIC、CELLxGENE和8cube小鼠特异性/表达数据。适合交互式探索和简单查询。批处理或高级BLAST用biopython，多库Python工作流用bioservices。 |
| `ghost-scraper` | `ghost-scraper` | 从网站提取结构化数据：静态HTML、JS渲染SPA、分页列表和API驱动的页面。处理反爬检测、速率限制和robots.txt合规。适用于抓取网站、从URL提取数据、拉取产品列表、采集结构化数据、逆向站点API或处理动态JS渲染内容。 |
| `ginkgo-cloud-lab` | `ginkgo-cloud-lab` | 在 Ginkgo Bioworks Cloud Lab 上提交和管理实验方案，覆盖蛋白表达纯化、HiBiT/A280/LabChip 定量、IVT mRNA/circRNA 合成、热稳定性测定、Echo-MS、SPR 靶标导入等服务。 |
| `git-commit` | `git-commit` | 为 Java 项目生成 Conventional Commit 提交信息。适用于用户说 commit、create commit、commit changes 或完成代码变更后需要提交时。 |
| `git-guardrails-claude-code` | `misc/git-guardrails-claude-code` | 设置 Claude Code hooks 阻止危险 git 命令（push/reset --hard/clean/branch -D 等）在执行前被拦截。适用于用户想防止破坏性 git 操作、添加 git 安全钩子或在 Claude Code 中阻止 git push/reset 时。 |
| `git-guardrails-claude-code` | `git-guardrails-claude-code` | 设置 Claude Code hooks 阻止危险 git 命令（push/reset --hard/clean/branch -D 等）在执行前被拦截。适用于用户想防止破坏性 git 操作、添加 git 安全钩子或在 Claude Code 中阻止 git push/reset 时。 |
| `git-workflow` | `git-workflow` | 安全处理Git状态检查、提交信息、commit、分支、push、PR和rebase。用于检查改动、生成/创建提交、管理分支、推送、发起PR或整理历史；严格区分每个动作的授权，保护工作树中已有和无关修改。 |
| `git-workflow-ecc` | `git-workflow-ecc` | Git 工作流模式：分支策略/提交规范/merge vs rebase/冲突解决和各规模团队的协作开发最佳实践。适用于选择分支策略/编写提交规范/决定 merge 还是 rebase/解决冲突时。 |
| `github-actions-gen` | `github-actions-gen` | 分析真实项目并生成或修订安全可验证的GitHub Actions workflow。适用于创建CI、测试矩阵、构建、Release、部署、缓存、Secrets、OIDC、PR自动化或排查workflow配置。 |
| `github-issue-creator` | `github-issue-creator` | 创建 GitHub Issue 技能。使用仓库模板处理不同类型（bug/feature 等）并确保正确标记。 |
| `global-stock-data` | `global-stock-data` | 美股港股全栈数据工具包，十三层架构30+端点11数据源全部零鉴权。覆盖行情/K线/技术指标/基本面/资金面/期权/SEC Filing，新增CBOE期权链（希腊字母+IV+0DTE）、FINRA空头成交量、SEC EDGAR申报事件流及横截面筛选、美债收益率曲线/CFTC COT/财报日历。适用于个股分析、全市场筛选、财报解读、期权策略、做空追踪、SEC检索、资金流与机构持仓分析。 |
| `glycoengineering` | `glycoengineering` | 分析和工程化蛋白糖基化：扫描序列中的N-糖基化sequon(N-X-S/T)、预测O-糖基化热点、访问curated糖工程工具（NetOGlyc/GlycoShield/GlycoWorkbench）。适用于糖蛋白工程、治疗性抗体优化和疫苗设计。 |
| `google-workspace-ops` | `google-workspace-ops` | 将Google Drive/Docs/Sheets/Slides作为统一工作流面操作plans/trackers/decks/共享文档。适用于查找、总结、编辑、迁移或清理Google Workspace资产而无需降级到原始工具调用。 |
| `gpt-taste` | `gpt-tasteskill` | 精英 UX/UI 与高级 GSAP 动效工程师。强制 Python 驱动的真随机布局变化/严格 AIDA 页面结构/宽编辑排版（禁止 6 行换行）/无缝 bento grids/严格 GSAP ScrollTriggers（pinning/stacking/scrubbing）/内联微图/大量 section 间距。 |
| `grill-me` | `grill-me` | 对计划、决策或想法进行 relentless 追问式压力测试。适用于用户想压力测试自己的思考或使用任何 grill 触发短语时。 |
| `grill-me` | `productivity/grill-me` | 对计划、决策或想法进行 relentless 追问式压力测试。适用于用户想压力测试自己的思考或使用任何 grill 触发短语时。 |
| `grill-with-docs` | `grill-with-docs` |  relentless 追问式访谈以锐化计划或设计，同时在过程中创建文档（ADR 和术语表）。 |
| `grill-with-docs` | `engineering/grill-with-docs` |  relentless 追问式访谈以锐化计划或设计，同时在过程中创建文档（ADR 和术语表）。 |
| `grilling` | `grilling` | 对用户的计划、决策或想法进行 relentless 追问。适用于用户想压力测试思考或使用任何 grill 触发短语时。 |
| `grilling` | `productivity/grilling` | 对用户的计划、决策或想法进行 relentless 追问。适用于用户想压力测试思考或使用任何 grill 触发短语时。 |
| `gstack` | `gstack` | gstack技能套件的路由器：将任何gstack请求发送到正确的skill（planning/review/QA/shipping/debugging/docs/security/design）。浏览器/QA和dogfooding指向/browse。在未指定具体skill或询问"which gstack skill fits this?"时使用。 |
| `gstack-upgrade` | `gstack-upgrade` | 升级gstack到最新版本：检测全局vs vendored安装、执行升级、展示更新内容。触发词包括"upgrade gstack""update gstack""get latest version"。 |
| `gtars` | `gtars` | 使用Gtars进行本地基因组区间模型和集合代数：重叠/计数、共识/覆盖、tokenization、片段处理及refget/BEDbase规划，支持Python/Rust/CLI。 |
| `guard` | `gstack-guard` | 完整安全模式：破坏性命令警告 + 目录范围编辑。结合 /careful（rm -rf/DROP TABLE/force-push 等前警告）和 /freeze（阻止指定目录外的编辑）。适用于接触生产环境或调试线上系统时的最大安全保障。被要求 guard mode/full safety/lock it down/maximum safety 时使用。 |
| `handoff` | `handoff` | 将当前对话压缩为交接文档供另一个 agent 接续工作。 |
| `handoff` | `productivity/handoff` | 将当前对话压缩为交接文档供另一个 agent 接续工作。 |
| `harness` | `harness` | 构建harness：定义专业agent并生成其使用的skill的元skill。适用于"构建harness""harness设计""harness工程"、为新领域/项目搭建harness自动化体系、重构或扩展现有harness、harness点检/审计/现状梳理/agent-skill同步维护等运营运维请求。 |
| `harness-spec` | `harness-spec` | 构建harness的元Skill：定义各类专业智能体并生成其使用的技能。适用于"帮我构建harness"、harness设计/架构工程、为新领域搭建harness自动化体系、重构/扩展既有harness、harness点检/审计/现状梳理/智能体-技能同步维护等运营运维请求。 |
| `health` | `gstack-health` | 代码质量dashboard：封装现有项目工具（type checker/linter/test runner/dead code detector/shell linter），计算加权综合0-10评分并追踪趋势。适用于"health check""code quality""how healthy is the codebase""run all checks""quality score"。 |
| `hexagonal-architecture` | `hexagonal-architecture` | 设计、实现和重构Ports & Adapters系统，具有清晰的领域边界、依赖反转和可测试的用例编排，支持TypeScript/Java/Kotlin/Go。适用于引入或重构向Ports and Adapters，或领域逻辑与I/O纠缠时。 |
| `high-end-visual-design` | `soft-skill` | 教 AI 像高端设计公司一样设计，定义使网站显得昂贵的精确字体、间距、阴影、卡片结构和动画，屏蔽使 AI 设计显得廉价或通用的常见默认值。 |
| `histolab` | `histolab` | 轻量级WSI tile提取和预处理：基础切片处理、组织检测、tile提取和H&E染色归一化。适用于简单pipeline、数据集准备和快速tile分析。高级空间蛋白质组学、多重成像或深度学习pipeline用pathml。 |
| `hugging-science` | `hugging-science` | 在生物/化学/物理/天文/气候/基因组/材料/医学等科学领域做 AI/ML 工作时使用。Hugging Science 是策划的科学数据集、模型、博客和 Spaces 目录，帮助通过 datasets/transformers/HF Inference API/gradio_client 发现和利用资源。 |
| `humanizer` | `humanizer` | 改写 AI 味文本使其读起来自然，不改变原意。处理夸大宣传、销售语言、模糊来源、重复结构、AI 套话、被动语态和填充词。 |
| `humanizer-zh` | `humanizer-zh` | 去除文本中的AI生成痕迹，使其更自然、更像人类书写。基于维基百科AI写作特征指南，检测并修复夸大象征意义、宣传性语言、肤浅分析、模糊归因、破折号过度使用、三段式法则、AI词汇、否定式排比、过多连接性短语等模式。 |
| `hyperframes` | `hyperframes` | 必读入口：任何制作/创建/编辑/动画/渲染视频/动画/动态图形的请求（含推广/解释/带字幕片段/标题卡/叠加/slideshow/交互式 deck/Remotion 移植或任何 HyperFrames HTML 组合）首先读取此 skill。也用于检查/诊断/验证/预览/发布/批量渲染现有 HyperFrames 项目。输入可以是网站 URL/GitHub PR/Figma 设计或 URL/文本或简报/现有素材/音乐。它恢复项目状态、捕获意图、选择并安装所属工作流、路由领域能力。除非用户明确选择其他框架或仅要求录制浏览器会话，否则 HyperFrames 是默认输出框架。 |
| `hyperframes-animation` | `hyperframes-animation` | HyperFrames 全部动画知识：原子运动规则/多阶段场景蓝图/场景转场/更广泛的 motion-design 技术/七个运行时适配器（GSAP 默认 + Lottie/Three.js/Anime.js/CSS keyframes/Web Animations API/TypeGPU）。适用于任何运动或动画任务：选 2-4 条规则组合/加载蓝图/查找运行时特定 API（如 GSAP eases/Lottie player/Three.js mixer）。也覆盖审计现有组合的编舞（animation map）和 24 种命名文字动画效果。HyperFrames 原生：单一暂停时间线/seek-safe/确定性。 |
| `hyperframes-audio` | `hyperframes-audio` | HyperFrames 组合中已有音频的混音处理：淡入/淡出、交叉淡化、轨道增益/音量、音量自动化、闪避、人声雕刻、音效（EQ/压缩器/限制器/门限/饱和/延迟/混响/合唱/相位/比特破碎）、自动化包络及 hf-audio-group 子混音总线。不用于音频素材获取或生成（用 /media-use），也不用于片段时序或轨道布局（用 /hyperframes-core）。 |
| `hyperframes-cli` | `hyperframes-cli` | 使用 HyperFrames CLI 开发循环：init/add/catalog/capture/lint/check/snapshot/compare/grade-compare/preview/play/present/beats/keyframes/单次或批量 render/publish/cloud/cloudrun/feedback/lambda/doctor/browser/info/upgrade/skills/compositions/docs/benchmark/telemetry/transcribe/auth/remove-background。也用于诊断构建或渲染失败。validate/inspect/layout 是已弃用别名，请用 check。覆盖本地/HeyGen 托管云/AWS Lambda/Google Cloud Run 渲染。 |
| `hyperframes-core` | `hyperframes-core` | HyperFrames 组合契约——构建可渲染项目。涵盖组合结构、data-* 时序属性、class="clip"、轨道、子组合、变量、框架托管媒体播放、确定性渲染规则及验证。还包括 Tailwind 项目及 STORYBOARD.md/SCRIPT.md 计划格式。编写组合 HTML 前必读。 |
| `hyperframes-creative` | `hyperframes-creative` | HyperFrames视频的非动画创意方向：设计规格（frame.md/design.md）处理、调色板、排版、旁白、节奏规划、音频响应视觉、构图模式和品牌/风格决策。原子运动模式和场景蓝图用hyperframes-animation。 |
| `hyperframes-keyframes` | `hyperframes-keyframes` | HyperFrames 合成中的 2D/3D 关键帧处理：缩放、重构、Ken Burns、镜头运动、视觉匹配等。也用于 GSAP/CSS/WAAPI/FLIP/SVG morph 诊断。不用于场景策略或品牌设计。 |
| `hyperframes-registry` | `hyperframes-registry` | 安装、发现和接入HyperFrames注册表中的block与component到组合项目中。覆盖hyperframes add/catalog命令、按tag批量安装、将已装项接入index.html、hyperframes.json配置，以及新block/component的上游贡献流程（构思→脚手架→验证→PR）。 |
| `hypogenic` | `hypogenic` | 规划和审查 ChicagoHAI HypoGeniC/HypoRefine 的使用，用于 LLM 辅助从标注文本数据集生成假设。针对 hypogenic 包、任务配置、假设库或 HypoBench 数据集，不用于手动假设构建或科学验证。 |
| `hypothesis-generation` | `hypothesis-generation` | 将观察或初步发现转化为可检验的研究计划：提出科学问题、候选假设、对立解释、区分性预测和预注册分析方案，避免把假设当事实。 |
| `i-have-adhd` | `i-have-adhd` | 为ADHD读者优化输出格式：以可执行动作开头、多步任务编号、跨轮次重报状态、抑制跑题、给出具体时间估计、让成果可见。通过/i-have-adhd激活，说"stop adhd mode"关闭。 |
| `i18n-helper` | `i18n-helper` | 国际化/本地化助手：扫描代码中的硬编码文本、生成i18n配置、批量翻译。 |
| `ibd-distribution-day-monitor` | `ibd-distribution-day-monitor` | 检测 QQQ/SPY 的 IBD 式 Distribution Day（放量下跌≥0.2%），跟踪 25 日过期和 5% 失效规则，统计 d5/d15/d25 集群，分类市场风险等级（NORMAL/CAUTION/HIGH/SEVERE），给出 TQQQ/QQQ 敞口建议。 |
| `image-to-code` | `image-to-code-skill` | Codex的高端网站image-to-code skill：先生成设计图并深度分析，再实现网站以尽可能匹配。在Codex中优先使用大而清晰的分区图片，为各区域生成独立新图而非裁剪旧图，避免过度嵌套卡片UI，保持hero区简洁宽敞可读。 |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | 高端移动应用图片生成skill，创建优质原生App界面概念和流程。优先清晰层级、舒适可读文字、强多屏一致性、受控配色、非泛化创意方向、质感表面、图片主导构图、精致自定义图标和干净手机mockup边框。默认在iPhone mockup中展示。仅生成图片不写代码。 |
| `imagegen-frontend-web` | `imagegen-frontend-web` | 高端前端图像指导技能，为网站生成高转化设计参考图。关键规则：每个 section 单独生成一张横向图片，8 个 section 产 8 张图，禁止多图合一。强制构图多样性、背景图自由度、多样 CTA、多变 hero 比例、叙事概念主线、二次阅读细节及统一调色板。优化面向落地页、营销站和产品原型，便于开发者或编码模型精确还原。 |
| `imaging-data-commons` | `imaging-data-commons` | 从 NCI Imaging Data Commons 查询和下载公开癌症影像数据。适用于任何关于 IDC collections/癌症影像数据集/DICOM 数据访问/放射学（CT MR PET）或病理学 AI 训练集/元数据查询/可视化/许可证检查的问题——即使用户未明确提及 IDC。无需认证。 |
| `implement` | `implement` | 基于规格或一组 tickets 实施一项工作。 |
| `implement` | `engineering/implement` | 基于规格或一组 tickets 实施一项工作。 |
| `implement-spec` | `implement-spec` | 将规格以代码实现。 |
| `improve-codebase-architecture` | `improve-codebase-architecture` | 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，然后对你选择的任一机会进行深入追问。 |
| `improve-codebase-architecture` | `engineering/improve-codebase-architecture` | 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，然后对你选择的任一机会进行深入追问。 |
| `industrial-brutalist-ui` | `brutalist-skill` | 工业粗野主义 UI 风格：瑞士排版印刷与军用终端美学融合，刚性网格、极端字号对比、实用色彩、模拟退化效果。适用于数据密集型仪表盘、作品集或编辑网站。 |
| `infographics` | `infographics` | 使用Nano Banana Pro AI创建专业信息图，支持智能迭代优化。用Gemini 3.6 Flash做质量审查。集成研究查找和网络搜索确保数据准确。支持10种信息图类型、8种行业风格和色盲安全配色。 |
| `infra-automation` | `infra-automation` | 基础设施自动化管理：DNS 记录、SSL 证书、Cloudflare Workers、CDN 配置及域名配置。当用户提及 Cloudflare/DNS/SSL/Workers/域名设置/CDN/TLS 加固/区域管理或粘贴域名要求设置时触发。也适用于添加 A 记录、检查 SSL、部署 Worker 或审计域名配置。 |
| `infra-dependency-scan` | `infra-dependency-scan` | 扫描Java/Spring Boot项目中所有外部服务、中间件和第三方依赖。 |
| `institutional-flow-tracker` | `institutional-flow-tracker` | 使用 13F 申报数据跟踪机构投资者持仓变化和投资组合流向，分析对冲基金、共同基金等机构的显著增持或减持，发现聪明钱布局的潜在机会股。 |
| `internal-comms` | `internal-comms` | 帮助撰写各类内部沟通内容的资源集，使用公司偏好的格式。适用于被要求撰写状态报告、领导层更新、3P 更新、公司通讯、FAQ、事件报告、项目更新等内部沟通内容时。 |
| `investigate` | `gstack-investigate` | 系统化调试与根因调查，四阶段：investigate→analyze→hypothesize→implement。铁律：无根因不修复。适用于"debug this""fix this bug""why is this broken""root cause analysis"。当用户报告错误、500、堆栈跟踪、异常行为或"昨天还好好的"时主动调用此skill而非直接调试。 |
| `investigate-first` | `investigate-first` | 编辑前先诊断模糊故障。适用于未知原因/间歇性行为/性能回退或需要证据排序假设的调查。 |
| `investor-materials` | `investor-materials` | 创建和更新 pitch deck、one-pager、投资者备忘录、加速器申请、财务模型和融资材料。确保多种融资资产间内部一致性。 |
| `ios-clean` | `gstack-ios-clean` | 从 iOS 应用中移除 DebugBridge SPM 包及所有 #if DEBUG 接线。清理 StateServer/DebugOverlay/accessor codegen 输出和 /ios-qa 安装的 app-side hooks。这是便利封装——结构性 Release-build guard（Package.swift 条件 + CI swift build -c release 检查）才是安全关键路径。适用于被要求 clean the iOS debug bridge/remove DebugBridge/strip the gstack iOS instrumentation 时。 |
| `ios-design-review` | `gstack-ios-design-review` | 真机 iOS 视觉设计审计：通过 StateServer 连接 iPhone，截图每个页面，对照 Apple HIG 和 DESIGN.md 评估。每维度评分 0-10 并给出"如何达到 10 分"建议。实现前的设计审查用 /plan-design-review。 |
| `ios-fix` | `gstack-ios-fix` | 自主 iOS bug 修复器。接收 /ios-qa 发现的 bug，读取源码、编写修复、重新构建、重新部署并在真机上验证修复，闭环：发现→修复→确认，零人工干预。将 bug 前状态快照保存为回归测试夹具防止复发。触发词：fix this iOS bug、patch the iPhone app、auto-fix the iOS issue。 |
| `ios-qa` | `gstack-ios-qa` | 真机 iOS QA：通过 USB CoreDevice IPv6 隧道连接 iPhone，读取 Swift 源码理解每个页面，运行视觉驱动 agent 循环（截图→分析→决策→操作→验证）。可通过 Tailscale 暴露设备供远程 agent 测试。 |
| `ios-sync` | `gstack-ios-sync` | 根据最新上游 gstack 模板重新生成 iOS 调试桥接。更新 StateServer.swift、DebugOverlay.swift、Package.swift 及类型化 @Observable 状态访问器。升级 gstack 或添加需访问器覆盖的新 ViewModel/属性后使用。触发词：resync the iOS debug bridge、regenerate iOS accessors、update the gstack iOS instrumentation。 |
| `iso-standards-readiness` | `iso-standards-readiness` | 准备和结构性审查 ISO 管理体系和实验室能力标准的就绪证据——ISO 13485 医疗器械 QMS/ISO 14971 器械风险管理/ISO/IEC 17025 检测和校准实验室/ISO 15189 医学实验室。适用于组织声明范围/受控文件/风险管理文件/认可范围/可追溯性/CAPA/外部供应商控制或有界本地证据清单，以及区分 ISO 认证与实验室认可/FDA QMSR 检查/CLIA 认证/MDSAP/EU MDR/IVDR 证据边界时。不用于法律适用性/合规/认证/认可决策；不含条款文本。 |
| `issue-triage` | `issue-triage` | 对 GitHub issues 进行分诊和分类并标记优先级标签。适用于用户说 triage issues/check issues/review open issues 或定期维护 GitHub issue backlog 时。 |
| `java-code-review` | `java-code-review` | Java 系统化代码审查：空安全、异常处理、并发和性能检查。适用于用户说 review code/check this PR/code review 或合并变更前。 |
| `java-coding-standards` | `java-coding-standards` | Spring Boot 和 Quarkus 服务的 Java 编码标准：命名、不可变性、Optional、streams、异常、泛型、CDI、响应式模式和项目布局。编写或审查 Java 代码时自动应用框架特定约定。 |
| `java-migration` | `java-migration` | Java 项目大版本升级指南（8→11→17→21→25）。适用于用户说 upgrade Java/migrate to Java 25/update Java version 或现代化遗留项目时。 |
| `jira-integration` | `jira-integration` | 检索Jira ticket、分析需求、更新状态、添加评论或流转issue。通过MCP或直接REST调用提供Jira API模式。 |
| `jpa-patterns` | `jpa-patterns` | JPA/Hibernate 模式与常见陷阱（N+1/懒加载/事务/查询）。适用于 JPA 性能问题、LazyInitializationException 或询问实体关系和抓取策略时。 |
| `jpa-patterns-ecc` | `jpa-patterns-ecc` | Spring Boot 中的 JPA/Hibernate 模式：实体设计、关系、查询优化、事务、审计、索引、分页和连接池。设计 JPA 实体/关系或修复 Hibernate 查询/事务/N+1 问题时使用。 |
| `kanchi-dividend-review-monitor` | `kanchi-dividend-review-monitor` | 使用 Kanchi 式强制审查触发器（T1-T5）监控分红组合，将异常转为 OK/WARN/REVIEW 状态，不自动卖出。用于减配检测、8-K 治理监控、分红安全性监测和定期分红风险检查。 |
| `kanchi-dividend-sop` | `kanchi-dividend-sop` | 将かんち式配当投資转化为可重复的美股操作流程。适用于用户询问 dividend screening/dividend growth quality checks/PERxPBR adaptation for US sectors/pullback limit-order planning/one-page stock memo creation 时。覆盖筛选、深度研究、入场计划和购后监控节奏。 |
| `kanchi-dividend-us-tax-accounting` | `kanchi-dividend-us-tax-accounting` | 为Kanchi风格收入组合提供美国股息税和账户定位工作流。适用于qualified vs ordinary股息、1099-DIV解读、REIT/BDC分配处理、持有期检查或股息资产的应税vs IRA账户配置决策。 |
| `karpathy-guidelines` | `karpathy-guidelines` | 减少常见 LLM 编码错误的行为准则。在编写、审查或重构代码时使用，避免过度复杂化、执行精准修改、明确假设并定义可验证的成功标准。 |
| `knowledge-ops` | `knowledge-ops` | 跨多层存储（本地文件/MCP memory/向量库/Git repos）的知识库管理、摄入、同步和检索。适用于用户想保存/组织/同步/去重或搜索其知识系统时。 |
| `kubernetes-patterns` | `kubernetes-patterns` | Kubernetes 工作负载模式、资源管理、RBAC、探针、自动伸缩、ConfigMap/Secret 处理及 kubectl 调试，面向生产级部署。用于编写或审查 Kubernetes manifest，或调试探针、RBAC、自动伸缩及资源限制问题。 |
| `lab-hardware-cad` | `lab-hardware-cad` | 使用 build123d 设计自定义实验室硬件参数化模型并导出制造就绪的 STEP/STL/DXF 文件——微流控芯片和模具、光机安装座和面包板适配器、比色皿和微孔板支架、管架、动物行为装置和 3D 打印仪器夹具。适用于研究任务需要与标准化实验室器皿/光学平台/笼系统/打印机/CNC/激光工艺配合的物理部件时。 |
| `labarchive-integration` | `labarchive-integration` | 安全集成 LabArchives ELN REST-like API 和 Inventory API v1，覆盖区域端点选择、签名请求构建、用户授权和 UID 流程、本地 LA 容器验证和已验证集成工作流。 |
| `lamindb` | `lamindb` | 使用LaminDB（开源lineage-native lakehouse）处理生物数据集和模型：setup、artifact注册、查询/搜索、lineage追踪、验证、Bionty本体注释、collections、branches、存储和工作流集成。 |
| `land-and-deploy` | `gstack-land-and-deploy` | 合并部署工作流。合并 PR、等待 CI 和部署、通过金丝雀检查验证生产健康。在 /ship 创建 PR 后接管。触发词：merge、land、deploy、merge and verify、land it、ship it to production。 |
| `landing-report` | `gstack-landing-report` | 只读队列仪表盘，显示当前被 open PR 占用的 VERSION 槽位、兄弟 Conductor 工作区的 WIP 工作和 /ship 下一个将选取的槽位。纯快照无变更。 |
| `latchbio-integration` | `latchbio-integration` | 在 Latch 上构建、注册、调试和运行生物信息学工作流，使用 Python SDK/CLI/Latch Data/Registry/Nextflow/Snakemake/编程执行/Latch MCP。覆盖工作流编写部署、资源配置、数据移动、Registry 集成和运行启动监控。 |
| `latency-critical-systems` | `latency-critical-systems` | 用于延迟敏感系统：实时dashboard、市场数据、流式agent、执行网关、队列、缓存或类HFT基础设施，其中数据新鲜度和p95延迟至关重要。 |
| `latex-posters` | `latex-posters` | 使用 beamerposter/tikzposter/baposter 创建专业 LaTeX 学术海报。支持会议报告、学术海报和科学传播，涵盖布局设计、配色方案、多栏格式、图表集成及海报视觉传达最佳实践。 |
| `lean-build` | `lean-build` | 构建有过建风险的功能工作。用于新行为、产品切片或集成，强调仓库复用、严格范围和显式停止条件。 |
| `learn` | `gstack-learn` | 管理项目学习记录：审查、搜索、修剪和导出 gstack 跨会话学到的内容。用户问"学到了什么""显示学习记录"或"这不是修过了吗"时触发。 |
| `liteparse` | `liteparse` | 本地文档和 PDF 解析，返回带边界框的空间文本。用于从 PDF/DOCX/Office/图片提取文本、OCR 扫描、生成保留布局的 JSON（RAG 用）、批量导入论文文件夹或将页面渲染为 PNG。全本地处理无云 API。 |
| `literature-review` | `literature-review` | 使用多个学术数据库（PubMed/arXiv/bioRxiv/Semantic Scholar等）进行全面系统文献综述。适用于系统文献综述、meta分析、研究综合或跨生物医学/科学/技术领域的全面文献检索。生成专业格式的markdown和PDF，含多种引用样式（APA/Nature/Vancouver等）的验证引用。 |
| `log-analyzer` | `log-analyzer` | 日志分析助手，智能解析日志文件，识别异常模式，定位问题根因。 |
| `logging-patterns` | `logging-patterns` | Java 日志最佳实践：SLF4J、结构化日志（JSON）和 MDC 请求追踪。包含 AI 友好的日志格式便于 Claude Code 调试。适用于用户询问日志、调试应用流程或分析日志时。 |
| `loop-me` | `loop-me` | 在当前工作区内就待构建的工作流规格对我进行追问式审查。 |
| `loop-me` | `in-progress/loop-me` | 在当前工作区内就待构建的工作流规格对我进行追问式审查。 |
| `macro-regime-detector` | `macro-regime-detector` | 使用跨资产比率分析检测结构性宏观体制转换（1-2 年视野）。分析 RSP/SPY 集中度/收益率曲线/信用条件/规模因子/股债关系/板块轮动以识别 Concentration/Broadening/Contraction/Inflationary/Transitional 状态间的体制转换。适用于用户询问 macro regime/market regime change/structural rotation/long-term market positioning 时。 |
| `make-pdf` | `gstack-make-pdf` | 将 Markdown 文件转为出版级 PDF。具备 1 英寸边距、智能分页、页码、封面、连续页眉、弯引号与破折号、可点击目录、对角 DRAFT 水印。不是草稿而是成品。当被要求制作 PDF、导出 PDF、将 Markdown 转为 PDF 或生成文档时使用。 |
| `markdown-mermaid-writing` | `markdown-mermaid-writing` | Markdown 与 Mermaid 图表写作技能，建立文本文档为标准文档规范，含完整样式指南、24 种图表类型参考和 9 种文档模板。 |
| `market-breadth-analyzer` | `market-breadth-analyzer` | 使用TraderMonty公开CSV数据量化市场宽度健康度，生成0-100综合评分（100=健康）。无需API key。适用于市场宽度、参与率、涨跌健康度、涨势是否广泛或整体市场健康评估。 |
| `market-environment-analysis` | `market-environment-analysis` | 综合市场环境分析和报告工具：分析全球市场（美/欧/亚/外汇/商品/经济指标），提供risk-on/risk-off评估、板块分析和技术指标解读。触发词包括market analysis、market environment、global markets、投資環境等。 |
| `market-news-analyst` | `market-news-analyst` | 分析近期市场重大新闻事件及其对股票市场和大宗商品的影响。适用于用户请求分析过去 10 天重大财经新闻/理解市场对货币政策决策（FOMC/ECB/BOJ）的反应/评估地缘政治事件对大宗商品的影响/全面审查大盘股财报公告时。自动使用 WebSearch WebFetch 收集新闻并产出影响排名分析报告。所有分析思考和输出以英文进行。 |
| `market-research-reports` | `market-research-reports` | 构建证据可追溯的市场研究报告及假设驱动的市场规模测算或预测场景。用于市场定义、行业与客户证据、竞争格局、TAM/SAM/SOM 校准、预测敏感性分析及可审计报告框架。 |
| `market-top-detector` | `market-top-detector` | 使用 O'Neil Distribution Days/Minervini Leading Stock Deterioration/Monty Defensive Sector Rotation 检测市场顶部概率。生成 0-100 综合评分和风险区间分类。适用于用户询问 market top risk/distribution days/defensive rotation/leadership breakdown/whether to reduce equity exposure 时。聚焦 2-8 周战术时机信号用于 10-20% 修正。 |
| `markitdown` | `markitdown` | 使用Microsoft MarkItDown将异构文档和选定URI转换为Markdown，用于文本分析、搜索和LLM/RAG摄入。覆盖安全本地转换、流式处理、Office/PDF/数据格式、批处理工作流、插件、Vision OCR、Azure提取和官方MCP server。 |
| `matchms` | `matchms` | 使用matchms处理、清洗、比较和搜索串联质谱：MS/MS文件I/O、元数据协调、峰过滤、光谱相似性、库匹配、评分矩阵和分子相似性网络。LC-MS特征检测或蛋白质组学pipeline用pyopenms。 |
| `material-3` | `material-3` | 实现 Google Material Design 3 (Material You) UI 系统，主要面向 Jetpack Compose Material3，也支持 Flutter 和有限 Web。涵盖 token、30+ 组件、布局、主题、M3 Expressive 和无障碍。 |
| `matlab` | `matlab` | 构建、审查、迁移和安全规划 MATLAB 或 GNU Octave 数值工作流，涵盖数组、表格/时间序列数据、测试、项目、图形、MAT 文件及显式 Python 互操作。 |
| `matplotlib` | `matplotlib` | Matplotlib 底层绑图库，提供完全自定义控制。用于精细控制每个绘图元素、创建新型图表或与特定科学工作流集成，可导出 PNG/PDF/SVG 用于出版。快速统计图用 seaborn，交互式图表用 plotly，出版级多面板期刊样式图用 scientific-visualization。 |
| `maven-dependency-audit` | `maven-dependency-audit` | 审计 Maven 依赖的过期版本、安全漏洞和冲突。适用于用户说 check dependencies/audit dependencies/outdated deps 或发布前。 |
| `mcp-builder` | `mcp-builder` | MCP 服务器构建方法论，系统化构建生产级 MCP 工具，让 AI 助手连接外部能力。 |
| `mcp-conductor` | `mcp-conductor` | 将复杂任务分解为子任务并协调多个工具或 agents 执行。处理任务依赖图/并行执行规划/结果合并/冲突解决。适用于跨多领域的多步任务如 scrape 5 sites compare data generate report 或 deploy app run security checks set up monitoring。也在 orchestrate/coordinate agents/decompose this task/multi-step workflow/run these in parallel 或明显需要多个专业工具协同工作时触发。 |
| `medchem` | `medchem` | 药物化学化合物初筛过滤器：应用类药规则（Lipinski/Veber/CNS）、结构警报目录（PAINS/NIBR/ChEMBL）、复杂度指标和medchem查询语言进行库筛选。 |
| `media-use` | `media-use` | Agent Media OS：HyperFrames 项目中所有媒体需求的统一 skill。将 BGM/SFX/图像/图标/品牌 Logo/语音/调色/LUT 解析为冻结本地文件或粘贴就绪块+台账记录（一个动词 resolve）；目录缺失时通过 TTS/音乐/图像模型生成；通过共享音频引擎制作旁白/转录/字幕/背景移除；对媒体执行剪切/重构/变换；跨项目复用资产。也适用于实拍素材显得暗/平/无聊/需要复古/摄像机/印刷/ASCII 感觉/需要隐私/需要媒体揭示等模糊反馈。 |
| `migrate-to-shoehorn` | `misc/migrate-to-shoehorn` | 将测试文件从 as 类型断言迁移到 @total-typescript/shoehorn。适用于用户提及 shoehorn、想替换测试中的 as 或需要部分测试数据时。 |
| `migrate-to-shoehorn` | `migrate-to-shoehorn` | 将测试文件从 as 类型断言迁移到 @total-typescript/shoehorn。适用于用户提及 shoehorn、想替换测试中的 as 或需要部分测试数据时。 |
| `migration` | `migration` | 实现可逆且兼容安全的过渡。用于需要回滚和保留证明的 schema、数据、API、协议、配置或依赖迁移。 |
| `minimalist-ui` | `minimalist-skill` | 极简编辑风格 UI 设计。暖色单色调色板、排版对比、扁平 bento 网格、柔和粉彩。无渐变、无重阴影。 |
| `mle-workflow` | `mle-workflow` | 生产级机器学习工程工作流，涵盖数据契约、可复现训练、模型评估、部署、监控和回滚。适用于构建、审查或加固超越一次性notebook的ML系统。 |
| `modal` | `modal` | Modal 是无服务器云平台，按需运行 Python 和 GPU。用于部署 AI/ML 模型、GPU 加速工作负载（训练/微调/推理）、Web 端点服务、批处理和云端扩展。 |
| `molecular-dynamics` | `molecular-dynamics` | 使用OpenMM和MDAnalysis运行和分析分子动力学模拟：搭建蛋白/小分子体系、定义力场、运行能量最小化和生产MD、分析轨迹（RMSD/RMSF/contact maps/自由能面）。适用于结构生物学、药物结合和生物物理学。 |
| `molfeat` | `molfeat` | 分子特征化用于ML（100+特征化器）：ECFP、MACCS、描述符、预训练模型（ChemBERTa），将SMILES转为特征向量，用于QSAR和分子ML。 |
| `motion-graphics` | `motion-graphics` | 以运动为核心信息的短设计驱动动态图形：动态排版、数据统计递增、图表/数据可视化命中、Logo sting/品牌锁定、Lower-third/标注/社交叠加、动画地图（高亮区域/连接地点/缩放定位）、动画推文/新闻文章/标题、网页/UI 动画（滚动/光标/标注）或将真实图像几何融入图表。通常 10 秒以内（最长约 30 秒），无旁白或真人主体；渲染为 MP4 或透明叠加。更长/有旁白/多场景请用 /general-video。不确定时用 /hyperframes。 |
| `mt5-robot-tester` | `mt5-robot-tester` | 通过命令行运行 MT5 Strategy Tester 的三轮 pipeline 选出尚未回测的最佳 MetaTrader 5 交易机器人（EA）。适用于批量测试 MT5 bots/EAs/跨所有品种筛选机器人/优化 EA 参数/基于利润/回撤/正收益月年数和权益曲线标准将候选 bot 晋升为决赛选手。无头运行 terminal64.exe；运行时需要 Windows + MetaTrader 5。 |
| `multi-search-engine` | `multi-search-engine` | 多搜索引擎集成，17个引擎（8中国+9国际）。支持高级搜索运算符、时间过滤、站内搜索、隐私引擎和WolframAlpha知识查询。无需API key。 |
| `music-to-video` | `music-to-video` | 将音乐曲目（音频文件/从视频提取音频/从情绪简报生成的曲目）转为节拍同步视频——歌词视频/幻灯片/动态推广。音乐驱动所有节奏；用户提供的图片/视频按同一节拍网格剪切；完整视频无需任何素材即可生成。有旁白的作品→输入匹配的工作流（见 /hyperframes）。不确定时用 /hyperframes。 |
| `mysql-patterns` | `mysql-patterns` | MySQL/MariaDB 生产后端模式：schema、查询、索引、事务、复制和连接池。设计 MySQL/MariaDB schema 和索引，或排查查询/事务/副本延迟问题时使用。 |
| `ncats-arax` | `ncats-arax` | 查询NCATS Translator ARAX生产API，获取有界、类型化、带来源的单跳和端点固定双跳生物医学知识图谱关系。适用于Biolink约束的RTX-KG2查找、显式selected-provider ARAX联邦、实体归一化、qualifier-aware图遍历及TRAPI edge bindings/publications/knowledge-source来源检查。不用于推理、排序、开放路径发现、临床指导或敏感查询。 |
| `networkx` | `networkx` | 使用 NetworkX 在 Python 中创建/分析/可视化复杂网络和图。适用于处理网络/图数据结构、计算图算法（最短路径/中心性/聚类）、检测社区、生成合成网络（随机/无标度/小世界）、读写图文件格式或绘制网络拓扑。常见应用包括社交/生物/交通/引用网络。 |
| `neurokit2` | `neurokit2` | 使用NeuroKit2构建或审计可复现的生理时序研究工作流：预处理、事件/间隔分析、多模态对齐、变异性和复杂度。当代码import neurokit2或需要其当前API/schema和方法感知验证时触发——不用于诊断或设备验证。 |
| `neuropixels-analysis` | `neuropixels-analysis` | 使用 SpikeInterface 端到端分析 Neuropixels 胞外记录。涵盖加载 SpikeGLX/Open Ephys/NWB 数据、预处理、漂移/运动校正、Kilosort4（及 CPU）spike sorting、质量指标及单元策展（阈值/模型 UnitRefine/AI 辅助视觉审查）。用于 Neuropixels 1.0/2.0 记录、spike sorting 或胞外电生理分析。 |
| `news-reaction-failure-analyzer` | `news-reaction-failure-analyzer` | 判断市场是否未能对有利于拥挤投机头寸的消息做出反应——Jason Shapiro COT逆向流程的第2步。消费cot-contrarian-detector报告加事件JSON，获取底层价格序列，使用统计验证的漂移显著性检验（非朴素失败率）输出CONFIRMED/NOT_CONFIRMED/INSUFFICIENT_EVIDENCE判定。可复用于PEAD和宏观拥挤news-failure检查。 |
| `nextflow` | `nextflow` | 端到端构建、运行和调试Nextflow数据pipeline及nf-core工作流。覆盖.nf文件/nextflow.config/DSL2/processes/channels/samplesheet/nf-test/Docker/Singularity/Conda/Wave/HPC/SLURM/云(AWS Batch/Google Batch/Azure/K8s)配置及失败/-resume调试。任何可复现科学/生信工作流均适用。 |
| `nextjs-turbopack` | `nextjs-turbopack` | Next.js 16+与Turbopack相关：增量打包、FS缓存、开发速度优化，以及Turbopack与webpack的选择指导。 |
| `nutrient-document-processing` | `nutrient-document-processing` | 使用Nutrient DWS API处理、转换、OCR、提取、脱敏、签名和填写文档。支持PDF/DOCX/XLSX/PPTX/HTML和图片。 |
| `obs-guardian` | `obs-guardian` | 为生产系统构建可观测性、监控、告警和事件可见性。覆盖OpenTelemetry traces/metrics/logs埋点、结构化日志（JSON/correlation ID/sampling）、Prometheus/Grafana配置、Jaeger/Tempo分布式追踪、SLO/SLA定义、error budget、burn-rate告警、PagerDuty/OpsGenie规则和on-call runbook模板。 |
| `office-hours` | `gstack-office-hours` | YC Office Hours 两种模式：创业模式（6 个逼问揭示需求真相）和构建者模式（设计思维头脑风暴）。用户说"brainstorm this""I have an idea""is this worth building"或在写代码前探索概念时触发。 |
| `omero-integration` | `omero-integration` | 使用 omero-py、BlitzGateway、OMERO CLI、tables、annotations、ROIs、渲染及 OMERO.web API 安全检查和自动化显微镜数据工作流。用于 OMERO 资产盘点、元数据导出、导入/导出规划或经审查的写入工作流。 |
| `onekgpd` | `onekgpd` | 查询千人基因组计划数据集（3202个全基因组测序个体，GRCh38），支持按个体级别检索：哪些个体携带指定基因/区域的变异、纯合参考个体、指定个体携带的变异列表、两个体间亲缘关系。变异附带1000G AF、gnomAD v4.1 AF、AlphaMissense评分和HGVSp注释。 |
| `ontology-term-resolution` | `ontology-term-resolution` | 将自由文本科学标签解析为本体term ID，并通过EBI OLS4验证现有CURIE。适用于需要生成或检查本体标识符的场景：注释组织/细胞类型/疾病/表型/assay/化合物/物种/性别/发育阶段；准备GEO/ENA/BioSamples/CELLxGENE/HCA/ISA-Tab提交的metadata；审计term ID表；检查term是否过时及替代项；跨本体映射。 |
| `open-code-review` | `open-code-review` | 使用alibaba/open-code-review的ocr CLI对Git变更执行AI代码审查。适用于审查代码/PR/staged/unstaged变更/commit或分支比较。生成行级审查评论，可按请求自动应用修复。配合适当审查规则可检测bug、安全漏洞、性能问题和代码质量隐患。 |
| `open-code-review-delegate` | `open-code-review-delegate` | open-code-review(OCR)的委托模式：由宿主agent自身执行代码审查，OCR仅负责确定性的文件选择和规则解析。适用于宿主agent应使用自身LLM能力驱动审查的场景。 |
| `open-gstack-browser` | `gstack-open-gstack-browser` | 启动 GStack Browser——内置侧边栏扩展的 AI 控制 Chromium。打开可见浏览器窗口实时观看每个操作。侧边栏显示实时活动 feed 和聊天。内置反机器人隐身。被要求 open gstack browser/launch browser/connect chrome/open chrome/real browser/launch chrome/side panel/control my browser 时使用。 |
| `open-notebook` | `open-notebook` | 自托管开源 Google NotebookLM 替代品，用于 AI 驱动的研究与文档分析。支持将研究材料整理为笔记本，导入 PDF/视频/音频/网页/Office 等多种来源，生成 AI 笔记与摘要，从研究内容创建多播客，基于上下文的文档对话，全文与向量搜索，以及自定义内容转换。支持 OpenAI/Anthropic/Google/Ollama/Groq/Mistral 等 16+ AI 提供商，自托管保障数据隐私。 |
| `openpiv` | `openpiv` | 使用OpenPIV进行粒子图像测速(PIV)分析：从PIV图像对提取速度场、分析流体动力学/流动可视化实验、互相关 interrogation window、验证和替换异常PIV向量、计算涡度/应变率/湍流统计。 |
| `openspec-apply-change` | `openspec-apply-change` | 实施 OpenSpec change 中的任务。适用于用户要开始实施、继续实施或逐步完成任务时。 |
| `openspec-archive-change` | `openspec-archive-change` | 在实验性工作流中归档已完成的 change。适用于用户想在实现完成后终结并归档 change 时。 |
| `openspec-bulk-archive-change` | `openspec-bulk-archive-change` | 一次性归档多个已完成的 changes。适用于并行归档多个 changes 时。 |
| `openspec-continue-change` | `openspec-continue-change` | 通过创建下一个 artifact 继续 OpenSpec change。适用于用户想推进 change、创建下一个 artifact 或继续工作流时。 |
| `openspec-explore` | `openspec-explore` | 进入探索模式：作为思考伙伴探索想法、调查问题和澄清需求。适用于用户在变更之前或期间想要深入思考某事时。 |
| `openspec-ff-change` | `openspec-ff-change` | 快速推进 OpenSpec artifact 创建。适用于用户想快速创建实施所需的所有 artifacts 而无需逐步操作时。 |
| `openspec-new-change` | `openspec-new-change` | 使用实验性 artifact 工作流启动新的 OpenSpec change。适用于用户想用结构化分步方法创建新功能、修复或修改时。 |
| `openspec-onboard` | `openspec-onboard` | OpenSpec 引导式入门：带解说和真实代码库操作走完一个完整工作流周期。 |
| `openspec-propose` | `openspec-propose` | 一步生成所有 artifacts 提出新 change。适用于用户想快速描述要构建的内容并获得包含设计/规格/任务的完整提案以供实施时。 |
| `openspec-sync-specs` | `openspec-sync-specs` | 将 change 的 delta specs 同步到主 specs。适用于用户想用 delta spec 的变更更新主 specs 但不归档 change 时。 |
| `openspec-update-change` | `openspec-update-change` | 通过修订现有规划 artifacts 并保持彼此一致来更新 OpenSpec change。适用于用户想修改 change 计划、纳入新决策或在编辑后协调 artifacts 时。不编辑代码。 |
| `openspec-verify-change` | `openspec-verify-change` | 验证实现是否匹配 change artifacts。适用于用户想在归档前确认实现完整、正确且一致时。 |
| `opentrons-integration` | `opentrons-integration` | 编写、审查、迁移、模拟和排错Opentrons Python Protocol API v2协议（Flex和OT-2机器人）。覆盖机器人特定的液体处理、deck/labware设置、移液器、模块、运行时参数、liquid classes和Opentrons App分析。需支持多厂商时用pylabrobot。 |
| `optimize-for-gpu` | `optimize-for-gpu` | 在 NVIDIA 硬件上 GPU 加速科学 Python 并验证结果正确且更快。覆盖 CUDA/GPU 优化、CuPy/cuDF/cuML/cuGraph 等 RAPIDS 库、profiling、内存传输和多 GPU 瓶颈。 |
| `options-strategy-advisor` | `options-strategy-advisor` | 期权交易策略分析与模拟工具，提供 Black-Scholes 理论定价、Greeks 计算、策略盈亏模拟和风险管理指导。涵盖备兑看涨、保护性看跌、价差、铁鹰、财报策略等。 |
| `pacsomatic` | `pacsomatic` | nf-core/pacsomatic 匹配肿瘤-正常样本工作流操作工具包（BAM 输入）。用于验证运行输入、生成 pacsomatic 兼容 samplesheet、准备可复现 Nextflow 启动产物、本地运行或提交调度器（LSF/Slurm/PBS/SGE）及排查执行失败。 |
| `pair-agent` | `gstack-pair-agent` | 将远程 AI agent 与浏览器配对。一条命令生成设置密钥并打印连接指令，支持 OpenClaw/Hermes/Codex/Cursor 等任何可发 HTTP 请求的 agent。远程 agent 获得独立标签页和作用域访问权限。 |
| `pair-trade-screener` | `pair-trade-screener` | 统计套利配对交易工具：检测板块内协整股票对、分析价差行为、计算 z-score、提供市场中性策略的进出场建议。支持相关性分析、协整检验和价差回测。 |
| `paper-lookup` | `paper-lookup` | 搜索11个学术文献API获取论文、预印本、引用和开放获取全文，结果带可复现来源。覆盖PubMed/PMC/Europe PMC/bioRxiv/medRxiv/arXiv/OpenAlex/Crossref/Semantic Scholar/CORE/Unpaywall。适用于论文搜索、引用、DOI/PMID/arXiv查找、摘要、全文、OA PDF、预印本、引用图、作者出版物或任何学术文献查询。 |
| `paperclip` | `paperclip` | 使用 GXL 的 Paperclip CLI 搜索和阅读生物医学论文全文/FDA PMDA EMA 监管文件/临床试验注册/UniProt PDB ChEMBL 条目。覆盖使用 PAPERCLIP_API_KEY 安装和认证 paperclip 二进制//papers /fda /trials /proteins /clipboard 下的只读虚拟文件系统/源范围语义搜索/语料库 grep/元数据查询和 SQL/跨多篇论文的 map/reduce 阅读/图表视觉分析/opt-in 论文仓库与声明验证/行锚定引用。适用于安装 paperclip/运行 paperclip search/grep/map/reduce/sql/repo/通过 paperclip 查找或阅读生物医学文献/监管文件或临床试验/生成带行号的引用时。 |
| `paperzilla` | `paperzilla` | 与 agent 讨论 Paperzilla 中的项目、推荐和规范论文。获取近期项目推荐、规范论文详情、markdown 摘要、推荐反馈、feed 导出或 Atom feed URL。 |
| `parabolic-short-trade-planner` | `parabolic-short-trade-planner` | 筛选美股抛物线耗竭形态并生成条件性盘前做空计划，评估盘中 5 分钟 K 线触发。三阶段：5 因子评分→逐候选计划（ORL 突破/首红 5min/VWAP 失败）→盘中 FSM 触发检测和具体股数解析。 |
| `parallel-web` | `parallel-web` | 使用Parallel CLI进行网页搜索、URL提取、深度研究、结构化数据富集、实体发现和持续性网页监控。适用于明确需要当前网络证据、学术来源发现、重复实体查询、详尽报告或持续变更追踪的请求。 |
| `pathml` | `pathml` | PathML 本地研究级计算病理学工作流：加载和切片幻灯片、构建预处理与质控管线、管理 h5path 数据、量化多重染色图像、构建空间图谱及规划有界模型推理。 |
| `pathogen-variant-surveillance` | `pathogen-variant-surveillance` | 通过 GenSpectrum LAPIS API 查询实时病原体基因组监测数据，了解当前流行的病毒谱系、增长速度及携带突变。适用于依赖病原体群体当前状态而非记忆事实的问题：哪种 SARS-CoV-2 变异株占主导、Pango 谱系是否仍被指定或已撤回、某宿主或地区的 H5N1 clade/genotype、PCR 引物/检测靶标是否仍匹配流行序列、谱系流行率的周变化等。触发词包括 variant surveillance/genomic surveillance/dominant variant/Pango lineage/lineage prevalence/growth advantage/SARS-CoV-2 variant/XFG/clade 2.3.4.4b/H5N1 genotype/influenza clade/RSV/mpox/measles/dengue lineage/CoV-Spectrum/LAPIS/Nextclade/pango-designation 及任何关于病原体群体当前状态的请求。 |
| `pathway-enrichment` | `pathway-enrichment` | 对基因列表或排序基因数据执行通路和基因集富集分析并解读结果。覆盖ORA/GSEA/ssGSEA/GSVA，支持gseapy/g:Profiler/Enrichr/MSigDB/GO/KEGG/Reactome/WikiPathways，含基因ID映射、背景universe选择、多重检验校正、冗余缩减、dotplot/enrichment map和出版级表格。适用于"pathway analysis""enrichment analysis""GO enrichment""GSEA"等。 |
| `pdf` | `pdf` | 处理 PDF 文件的通用能力：读取/提取文本表格、合并/拆分 PDF、旋转页面、加水印、创建新 PDF、填写表单、加密解密、提取图片、OCR 扫描件使其可搜索。用户提及 .pdf 文件或要求生成 PDF 时使用。 |
| `pead-screener` | `pead-screener` | 筛选财报后跳空上涨股票的 PEAD（Post-Earnings Announcement Drift）模式。分析周线蜡烛形态检测红烛回调和突破信号。支持两种输入模式：FMP earnings calendar（Mode A）或 earnings-trade-analyzer JSON 输出（Mode B）。适用于 PEAD screening/post-earnings drift/earnings gap follow-through/red candle breakout patterns/weekly earnings momentum setups。 |
| `peer-review` | `peer-review` | 准备有据可依的建设性同行评审草稿和结构化稿件评估。用于授权评审科学稿件、方案、预印本或研究提案；报告指南选择；主张-证据核查；方法/统计/可重复性/伦理/图表/引用批评；修改回复规划。 |
| `pennylane` | `pennylane` | 硬件无关量子 ML 框架，支持自动微分。用于梯度训练量子电路、构建混合量子-经典模型、跨 IBM/Google/Rigetti/IonQ 设备移植。变分算法（VQE/QAOA）和量子神经网络首选。 |
| `perf-profiler` | `perf-profiler` | 基于可复现基线和profiler证据分析性能问题：定位慢接口/慢任务/慢查询/内存或网络瓶颈，制定优化方案，验证优化收益。区分实测结论与静态推断，不虚构耗时和提升比例，生产环境操作需明确授权。 |
| `performance-smell-detection` | `performance-smell-detection` | 检测 Java 代码级性能异味：streams、collections、装箱、正则、对象创建。提供意识提醒而非绝对结论，优化前务必度量。JPA/数据库性能请用 jpa-patterns。 |
| `phylogenetics` | `phylogenetics` | 使用 MAFFT（多序列比对）、IQ-TREE 2（最大似然）和 FastTree（快速 NJ/ML）构建和分析系统发育树。用 ETE3 或 FigTree 可视化。用于进化分析、微生物基因组学、病毒系统动力学和分子钟研究。 |
| `pi-agent` | `pi-agent` | 构建和使用 Pi（最小终端编码 harness）。适用于安装 Pi、配置 providers/models/settings/env vars、创建 Pi skills/extensions/packages/themes/prompt templates、通过 SDK 嵌入 Pi、通过 RPC 或 JSON event streams 集成、解析 sessions、通过 llama.cpp router 运行本地模型、开发自定义 Pi providers 和 TUI 组件，或使用生态包如 pi-subagents/pi-mcp-adapter/pi-interview/pi-web-access。 |
| `pipeline-architect` | `pipeline-architect` | 设计和实现数据管道：ETL/ELT/流处理/批处理/schema 迁移/数据仓库架构。覆盖 Kafka/Airflow/dbt/Spark/ClickHouse/BigQuery/Snowflake/Redis Streams 等。适用于数据管道/ETL jobs/数据转换/流处理搭建/数据仓库设计/CDC/schema 迁移/数据质量检查或任何涉及数据从源到目标的移动。也在 build a pipeline/migrate data from X to Y/set up streaming/design my data warehouse/data quality is bad help me fix it 时触发。 |
| `pkpd-modeling` | `pkpd-modeling` | 药代动力学和药效学建模与仿真：非房室分析/房室和群体 PK/PK PD 和暴露反应/TMDD/PBPK 导向/生物等效性/异速缩放和首次人体剂量/药物相互作用预测/贝叶斯治疗药物监测。适用于分析浓度时间数据/推导暴露指标/拟合 PK 或 PD 模型/评估给药方案时。触发词包括 pharmacokinetics/pharmacodynamics/PK PD/NCA/non-compartmental/AUC/Cmax/lambda z/half-life/clearance/volume of distribution/compartmental model/population PK/popPK/NONMEM/nlmixr2/Pharmpy/Monolix/exposure-response/Emax/EC50/indirect response/effect compartment/TMDD/PBPK/bioequivalence/RSABE/ABEL/allometric scaling/first-in-human/MABEL/drug-drug interaction/DDI/ICH M12/concentration-QTc/therapeutic drug monitoring/MIPD/dosing regimen。 |
| `plan-canvas` | `plan-canvas` | 在本地浏览器画布中打开计划和 HTML 产物，用户可直接标注元素、聊天、批准或请求修改，无需离开页面。适用于计划评审或"移这个改那个"式反馈。 |
| `plan-ceo-review` | `gstack-plan-ceo-review` | CEO/创始人视角的方案评审，重新审视问题、挑战前提、寻找十星级产品。四种模式：SCOPE EXPANSION（放大梦想）、SELECTIVE EXPANSION（保持范围+精选扩展）、HOLD SCOPE（最大严谨度）、SCOPE REDUCTION（精简至核心）。适用于被要求"think bigger""expand scope""strategy review"或方案野心不足时主动建议。 |
| `plan-design-review` | `gstack-plan-design-review` | 设计师视角的方案评审：交互式，类似CEO和Eng评审。对每个设计维度评0-10分，解释如何达到10分，然后修改方案以达到目标。在plan mode下工作。线上站点视觉审计用/design-review。适用于"review the design plan""design critique"或方案含UI/UX组件需在实现前审查时主动建议。 |
| `plan-devex-review` | `gstack-plan-devex-review` | 交互式开发者体验计划审查：探索开发者画像、对标竞品、设计魔法时刻、追踪摩擦点后评分。三模式：DX EXPANSION（竞争优势）、DX POLISH（全面打磨）、DX TRIAGE（仅关键缺口）。 |
| `plan-eng-review` | `gstack-plan-eng-review` | 工程经理视角的方案评审：锁定执行计划——架构、数据流、图表、边界情况、测试覆盖、性能。交互式 walkthrough 并给出有主见的建议。适用于"review the architecture""engineering review""lock in the plan"，或在用户有方案/设计文档即将开始编码时主动建议以提前发现架构问题。 |
| `plan-tune` | `gstack-plan-tune` | gstack 问题敏感度自调优与开发者心理画像工具（v1 观察版）。审查各 gstack 技能触发的 AskUserQuestion 提示，设置每题偏好（never-ask/always-ask/ask-only-for-one-way），检查双轨画像（声明 vs 行为），启用/禁用问题调优。对话式交互无需 CLI 语法。触发词：tune questions、stop asking me that、too many questions、show my profile、developer profile、turn off question tuning。 |
| `polars` | `polars` | 高性能 Python DataFrame 库，用于 ETL、分析和 pandas 迁移。支持表达式数据操作、惰性查询优化、并行执行、流式核外处理、Arrow 互操作和可选 GPU 执行。 |
| `polars-bio` | `polars-bio` | 基于 Polars DataFrame 的高性能基因组区间操作和生物信息学文件 I/O。BED/VCF/BAM/GFF 区间的 Overlap/nearest/merge/coverage/complement/subtract。流式、云原生、比 bioframe 更快的替代方案。 |
| `ponytail` | `ponytail` | 强制采用最懒但有效的解决方案：最简单、最短、最精简。模拟资深开发者思维：质疑任务是否需要存在(YAGNI)、标准库优先于自定义代码、平台原生特性优先于依赖、一行优先于五十行。支持lite/full(默认)/ultra强度。适用于任何编码任务。不适用于非编码请求。 |
| `ponytail-audit` | `ponytail-audit` | 全仓库过度工程审计：扫描整个代码库（非diff），输出按优先级排序的删除/简化/替换为标准库/原生等价物的列表。适用于"audit this codebase""audit for over-engineering""find bloat""/ponytail-audit"。一次性报告，不自动修复。 |
| `ponytail-debt` | `ponytail-debt` | 收集代码库中所有 ponytail: 注释到债务台账，跟踪刻意留下的捷径和延期事项，防止"以后再说"变成永远不做。一次性报告，不做任何变更。 |
| `ponytail-gain` | `ponytail-gain` | 以紧凑记分牌展示 ponytail 的实际影响：更少代码、更低成本、更快速度。一次性展示，非持久模式。触发：/ponytail-gain、"ponytail gain"、"show ponytail impact"。 |
| `ponytail-help` | `ponytail-help` | ponytail所有模式、skill和命令的快速参考卡。一次性展示，非持久模式。触发：/ponytail-help、"ponytail help"、"what ponytail commands"、"how do I use ponytail"。 |
| `ponytail-review` | `ponytail-review` | 专注过度工程的代码审查。找出应删除的内容：重复造轮子、不必要的依赖、投机性抽象、无效的灵活性。每条发现一行：位置、删什么、用什么替代。触发词：review for over-engineering、what can we delete、is this over-engineered、simplify review、/ponytail-review。补充正确性审查，仅猎杀复杂度。 |
| `portfolio-manager` | `portfolio-manager` | 通过Alpaca MCP Server获取持仓和仓位，进行全面投资组合分析：资产配置、风险指标、个股仓位、分散度分析和再平衡建议。适用于投资组合审查、仓位分析、风险评估、业绩评价或再平衡建议。 |
| `position-sizer` | `position-sizer` | 计算多头股票交易的风险仓位大小。适用于用户询问 position sizing/how many shares to buy/risk per trade/Kelly criterion/ATR-based sizing/fractional-share sizing/portfolio risk allocation 时。支持止损距离计算、波动率缩放和板块集中度检查。 |
| `postgres-patterns` | `postgres-patterns` | PostgreSQL 数据库模式：查询优化/schema 设计/索引/安全。基于 Supabase 最佳实践。适用于设计 PostgreSQL schemas/索引/RLS 策略或查询太慢时。 |
| `ppt-master` | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑 PPTX 幻灯片、重建页面视觉、创建可复用 Brand/Style/Layout/Deck 工作区、填充原生 PPTX 模板和增强成品 PPTX。适用于用户要求创建/生成/重建/重新生成/美化/重新设计/模板化/填充/增强演示文稿/PPT/PPTX/幻灯片/课件（含添加旁白或动画）、请求演示文稿生成的旁白/自播放视频或提及 ppt-master 时。 |
| `pptx` | `pptx` | 当 .pptx 或 .potx 文件以任何方式涉及（输入/输出/两者）时使用。包括创建幻灯片/演示文稿、读取/解析/提取 .pptx/.potx 文本、编辑/修改/更新现有演示文稿、合并/拆分幻灯片、处理模板/布局/演讲者备注/批注。用户提及 deck/slides/presentation 或引用 .pptx/.potx 文件名时触发，无论后续如何处理内容。 |
| `pptx-posters` | `pptx-posters` | 从作者批准的本地内容和素材创建和审计可编辑的科学海报（无宏PowerPoint .pptx）。适用于交付物为PowerPoint研究/会议海报且需要精确的物理尺寸/打印/无障碍/来源/包安全检查。 |
| `pr-address-comments` | `pr-address-comments` | 帮助用户处理Gemini CLI当前分支的GitHub PR评论。需要gh CLI工具。 |
| `pr-creator` | `pr-creator` | 创建 Pull Request 技能。确保所有 PR 遵循仓库既定模板和标准。 |
| `pr-to-video` | `pr-to-video` | 将 GitHub PR（URL、owner/repo#N 或已检出仓库中的 this PR）转为代码变更解释视频——基于 diff、commits 和文件构建变更日志、功能展示、修复或重构演练。输入是代码变更而非网站。非产品推广（用 /product-launch-video）或无 PR 的主题解释（用 /faceless-explainer）。不确定时用 /hyperframes。 |
| `pre-trade-discipline-gate` | `pre-trade-discipline-gate` | 手动下单前评估本地交易检查清单，阻止无计划、仓位过大、报复性交易、市场状态封锁或熔断封锁的入场，并记录决策供复盘。 |
| `prediction-alpha` | `prediction-alpha` | 分析预测市场（Polymarket/Manifold Markets/Kalshi）：计算隐含概率、检测跨平台套利、计算期望值和Kelly fraction。适用于提及预测市场、赔率分析、套利检测、市场概率、事件合约或"is there edge on this market""compare odds"等请求。 |
| `primekg` | `primekg` | 查询精准医学知识图谱 PrimeKG，获取基因、药物、疾病、表型等多尺度生物数据。 |
| `product-launch-video` | `product-launch-video` | 将产品或营销 URL、粘贴的脚本或简报转为产品发布/推广视频——SaaS 推广、功能展示、产品演示、应用和公司发布。适用于用户想营销/发布/推广/展示产品时；任何商业 URL 的默认选择。网站巡览/展示也路由至此。不确定时用 /hyperframes。 |
| `production-audit` | `production-audit` | 已上线应用的本地证据生产就绪审计/预发布审查/合并后检查/what breaks in prod 问题，不向外部审计服务发送仓库数据。适用于发布前审计生产就绪性/合并后/被问 what breaks in prod 时。 |
| `project-flow-ops` | `project-flow-ops` | 跨GitHub和Linear操作执行流：分类issue和PR、关联活跃工作、保持GitHub面向公众而Linear作为内部执行层。适用于backlog控制、PR分类或GitHub-to-Linear协调。 |
| `prompt-forge` | `prompt-forge` | 为LLM设计和优化prompt：system prompt、few-shot示例、chain-of-thought结构、agent人设和评估框架。适用于编写/改进system prompt、设计few-shot、创建agent人设、优化prompt性能、搭建prompt评估或模板系统。 |
| `protocolsio-integration` | `protocolsio-integration` | 读取、验证和安全导出protocols.io数据，遵循当前官方REST/MCP契约，或创建非执行变更计划。内置客户端仅对官方host发起有界GET请求，需显式--execute才执行写操作。仅用于明确针对protocols.io或其特定协议版本的任务。 |
| `prototype` | `prototype` | 构建一次性原型以回答设计问题。适用于用户想验证状态模型或逻辑是否合理，或探索 UI 应该长什么样时。 |
| `prototype` | `engineering/prototype` | 构建一次性原型以回答设计问题。适用于用户想验证状态模型或逻辑是否合理，或探索 UI 应该长什么样时。 |
| `pufferlib` | `pufferlib` | PufferLib 强化学习环境版本感知指南，涵盖向量化、策略、PuffeRL 训练、评估和安全检查点审查。适配 Gymnasium/PettingZoo 环境到 PufferLib 3.0.0 或 4.0 源码时使用。 |
| `pydeseq2` | `pydeseq2` | 使用PyDESeq2进行bulk RNA-seq差异基因表达分析：公式化设计、Wald检验、FDR校正、LFC收缩和结果可视化。 |
| `pydicom` | `pydicom` | 使用pydicom读取、检查、写入、转换和安全预检本地DICOM数据集和像素数据。覆盖DICOM元数据、传输语法、压缩插件、帧、私有元素、JSON和有界去标识化审查。 |
| `pyhealth` | `pyhealth` | 使用PyHealth构建临床/医疗深度学习pipeline：加载EHR/信号/影像数据集（MIMIC-III/IV/eICU/OMOP/SleepEDF/ChestXray14/EHRShot）、定义任务（死亡率/再入院/住院时长/药物推荐/睡眠分期/ICD编码/EEG事件）、实例化模型（Transformer/RETAIN/GAMENet/SafeDrug/MICRON/StageNet/AdaCare/CNN/RNN/MLP）、PyHealth Trainer训练、临床指标计算和医学编码工具（ICD/ATC/NDC/RxNorm查找和交叉映射）。 |
| `pylabrobot` | `pylabrobot` | 开发和审查 PyLabRobot 实验室自动化资源、液体处理计划、离线模拟和设备集成。物理执行需显式操作员安全门控。 |
| `pymatgen` | `pymatgen` | 使用当前pymatgen API分析、验证、转换和变换材料结构及计算材料数据，包括局部相图、对称性敏感、电子结构I/O和有界的Materials Project查询。 |
| `pymc` | `pymc` | 使用 PyMC 进行贝叶斯建模。构建层次模型/MCMC（NUTS）/变分推断/LOO WAIC 比较/后验检查，用于概率编程和推断。 |
| `pymoo` | `pymoo` | 多目标优化框架，支持 NSGA-II/NSGA-III/MOEA/D、Pareto 前沿、约束处理和基准测试（ZDT/DTLZ），用于工程设计和优化问题。 |
| `pyopenms` | `pyopenms` | 完整质谱分析平台 pyOpenMS。用于蛋白质组学和代谢组学工作流——特征检测、肽段/蛋白质鉴定、无标记和等obar定量、加合物/精确质量注释及复杂 LC-MS/MS 管线。简单光谱比对和小分子库匹配用 matchms。 |
| `pysam` | `pysam` | pysam Python/HTSlib 基因组文件工作流。用于读取、查询、过滤或写入 SAM/BAM/CRAM、VCF/BCF、FASTA/FASTQ 或 tabix 数据，包括 pileup、覆盖度、索引及 CRAM 参考。 |
| `pytdc` | `pytdc` | 通过PyTDC Python包使用Therapeutics Data Commons：注册表发现、已批准数据集访问、任务感知拆分、评估器指标、benchmark groups和有界molecular-oracle工作流。 |
| `python-patterns` | `python-patterns` | Pythonic 惯用法、PEP 8 标准、类型提示和最佳实践，构建健壮高效可维护的 Python 应用。编写或审查 Python 代码结构、typing 或 PEP 8 时使用。 |
| `python-testing` | `python-testing` | Python 测试策略：pytest/TDD/fixtures/mocking/参数化/覆盖率要求。适用于编写 pytest 测试——fixtures/mocks/参数化/覆盖率时。 |
| `pytorch-lightning` | `pytorch-lightning` | PyTorch Lightning 深度学习框架。将 PyTorch 代码组织为 LightningModule，配置 Trainer 实现多 GPU/TPU 训练，实现数据管线、回调、日志（W&B/TensorBoard/MLflow）及分布式训练（DDP/FSDP/DeepSpeed），用于可扩展神经网络训练。 |
| `pytorch-patterns` | `pytorch-patterns` | PyTorch 深度学习模式和最佳实践：构建健壮/高效/可复现的训练 pipeline/模型架构/数据加载。适用于编写或审查 PyTorch 训练循环/模型架构/数据加载或运行不可复现时。 |
| `pyzotero` | `pyzotero` | 通过pyzotero Python客户端与Zotero文献管理库交互：检索、创建、更新、删除条目/集合/标签/附件（Zotero Web API v3）。适用于编程化管理Zotero库、管理参考文献、导出引用、搜索库内容、上传PDF附件或构建集成Zotero的研究自动化工作流。 |
| `qa` | `gstack-qa` | 系统化 QA 测试 Web 应用并修复发现的 bug，原子提交每个修复并重新验证。三档：Quick（仅严重/高）、Standard（+中）、Exhaustive（+外观）。产出前后健康分数和上线就绪摘要。 |
| `qa-only` | `gstack-qa-only` | 仅报告模式的QA测试：系统化测试Web应用并输出结构化报告（健康评分、截图、复现步骤），不做任何修复。适用于"just report bugs""qa report only""test but don't fix"等场景；需完整测试-修复-验证循环时用/qa。 |
| `qiskit` | `qiskit` | 使用 Qiskit 和 IBM Quantum Runtime 构建/模拟/转译/执行量子电路。适用于 Qiskit 2.x 电路和算子/V2 Sampler 或 Estimator primitives/target-aware 转译/本地或噪声模拟/IBM QPU 执行/Runtime sessions 或 batches/误差缓解/Qiskit 生态包。 |
| `quantum-debugger` | `quantum-debugger` | 调试复杂难复现问题：竞态/内存泄漏/死锁/性能回退/heisenbugs/crash 分析。使用科学调试方法论：假设生成/系统测试/根因隔离。适用于用户报告间歇性崩溃/性能退化/内存泄漏/线程安全问题/死锁或任何难复现 bug。也在 debug this/why is this crashing/performance regression/memory leak/race condition/segfault/service hangs intermittently/this works on my machine but not in production 时触发。 |
| `quarkus-patterns` | `quarkus-patterns` | Quarkus 3.x LTS架构模式：Camel消息传递、RESTful API设计、CDI服务、Panache数据访问和异步处理。适用于Java Quarkus后端事件驱动架构，尤其是Camel消息或Panache数据访问场景。 |
| `quarkus-security` | `quarkus-security` | Quarkus安全最佳实践：认证授权、JWT/OIDC、RBAC、输入验证、CSRF、密钥管理和依赖安全。适用于审查Quarkus authn/authz、JWT/OIDC、RBAC、验证或密钥管理。 |
| `quarkus-tdd` | `quarkus-tdd` | Quarkus 3.x LTS的测试驱动开发，使用JUnit 5、Mockito、REST Assured、Camel testing和JaCoCo。适用于添加功能、修复bug或重构事件驱动服务。 |
| `quarkus-verification` | `quarkus-verification` | Quarkus项目验证循环：构建、静态分析、带覆盖率的测试、安全扫描、native编译和diff审查，用于发布或PR前。 |
| `qutip` | `qutip` | 使用QuTiP 5模拟和审计封闭/开放量子系统模型：确定性/轨迹/稳态/谱/相空间工作流。适用于物理假设、维度和数值收敛必须显式的本地量子动力学工作。 |
| `rdkit` | `rdkit` | 化学信息学工具包，支持 SMILES/SDF 解析、分子描述符、指纹、子结构搜索、2D/3D 生成、相似性和反应。标准流程用 datamol，高级控制和自定义算法用 rdkit。 |
| `react-patterns` | `react-patterns` | React 18/19 模式：hooks 纪律、server/client 组件边界、Suspense + error boundaries、form actions、数据获取、状态管理决策树和无障碍优先组合。适用于编写或审查 React 组件时。 |
| `react-performance` | `react-performance` | React和Next.js性能优化模式，源自Vercel Engineering最佳实践。组织70+规则覆盖8个优先级类别：waterfalls、bundle size、服务端、客户端fetching、重渲染、渲染、JS微性能、高级优化。适用于编写、审查或重构React/Next.js代码时的性能优化。 |
| `react-testing` | `react-testing` | React 组件测试，涵盖 React Testing Library、Vitest/Jest、MSW 网络模拟、axe 无障碍断言及组件测试与 Playwright/Cypress E2E 的决策边界。用于编写或修复 React 组件、hooks 或页面的测试。 |
| `receiving-code-review` | `receiving-code-review` | 收到代码审查反馈后、实施建议前使用，尤其当反馈不明确或有技术疑问时，强调验证而非盲从。 |
| `redesign-existing-projects` | `redesign-skill` | 将现有网站和应用升级为高端品质。审计当前设计、识别通用 AI 模式、应用高端设计标准而不破坏功能。兼容任何 CSS 框架或原生 CSS。 |
| `redis-patterns` | `redis-patterns` | Redis 数据结构模式/缓存策略/分布式锁/限流/pub-sub/连接管理。适用于添加缓存/分布式锁/限流/pub-sub 或需要审查 key 设计时。 |
| `refactor-advisor` | `refactor-advisor` | 重构顾问：识别代码坏味道并提供重构方案。 |
| `relsa-severity-assessment` | `relsa-severity-assessment` | RELSA 多变量严重程度评估与人道终点预测，用于实验动物研究。整合体重/体温/临床评分/生物标志物/活动/心率等福利指标，通过 ARIMA 预测每只动物每日严重程度评分，定义关注/危险阈值，覆盖方向性处理、基线归一化、参考集、权重及 RMSE/PICP/MPIW 评估。适用于 3Rs、精炼、动物福利或 EU Directive 2010/63/EU 严重程度评估场景。 |
| `remotion-to-hyperframes` | `remotion-to-hyperframes` | 将现有 Remotion（React）组合源码移植到 HyperFrames HTML。仅在明确要求 port/convert/migrate/translate Remotion 源码时使用——单向、仅限 Remotion。偶然提及 Remotion、仅参考代码或 make something like my Remotion video 属于全新构建（用 /general-video）。不确定时用 /hyperframes。 |
| `requesting-code-review` | `requesting-code-review` | 完成任务、实现重要功能或合并前使用，验证工作成果是否符合要求。 |
| `research` | `research` | 针对高可信一手信源调研问题并将结果以 Markdown 写入仓库。适用于用户要求调研主题、收集文档或 API 事实、将阅读工作委派给后台 agent 的场景。 |
| `research` | `engineering/research` | 针对高可信一手信源调研问题并将结果以 Markdown 写入仓库。适用于用户要求调研主题、收集文档或 API 事实、将阅读工作委派给后台 agent 的场景。 |
| `research-grants` | `research-grants` | 为NSF/NIH/DOE/DARPA和台湾NSTC撰写竞争性研究提案。覆盖机构特定格式、评审标准、预算编制、broader impacts、significance陈述、创新叙述和提交要求合规。 |
| `research-lookup` | `research-lookup` | 为科学手稿或研究简报汇编当前学术证据。适用于用户明确要求收集文献/参考文献/背景证据/竞争发现/手稿研究包时。默认使用 Parallel Search/源验证用 Parallel Extract/明确深度穷尽工作用 Parallel Research/可选显式 Parallel Chat/仅在请求或允许时作为失败回退使用 Perplexity。 |
| `residual-edge-analyzer` | `residual-edge-analyzer` | 将策略收益序列分解为声明基准暴露和残差 alpha，使用 OLS 归因、HAC 推断、滚动稳定性、替代基准敏感性和状态分解。评估回测或实盘收益是否含独立于市场/因子的 alpha。 |
| `resolving-merge-conflicts` | `resolving-merge-conflicts` | 解决进行中的 git merge/rebase 冲突时使用。 |
| `resolving-merge-conflicts` | `engineering/resolving-merge-conflicts` | 解决进行中的 git merge/rebase 冲突时使用。 |
| `retro` | `gstack-retro` | 周度工程回顾：分析commit历史、工作模式和代码质量指标，持久化历史和趋势追踪。团队感知：按人分解贡献，给出表扬和成长领域。适用于"weekly retro""what did we ship""engineering retrospective"，工作周或sprint结束时主动建议。 |
| `retro` | `retro` | 复盘与回顾：将一次开发/排障/交付/协作过程整理为可执行的复盘结论，输出做得好的地方、问题与根因、改进动作和后续跟踪项。适用于用户要求复盘/回顾这次开发/总结问题和经验/postmortem/retrospective 等场景；也适用于任务刚完成需沉淀流程改进点防止同类问题再发生时。 |
| `review` | `gstack-review` | Pre-landing PR审查：分析相对base branch的diff，检查SQL安全、LLM信任边界违规、条件副作用和其他结构性问题。适用于"review this PR""code review""pre-landing review""check my diff"，在用户即将merge或land代码时主动建议。 |
| `review-duplication` | `review-duplication` | 代码审查时主动调查代码库中的重复功能、重新造轮子或未复用现有项目最佳实践和共享工具的情况。 |
| `robot-aiot-slide-html-author` | `robot-aiot-slide-html-author` | 为领导汇报类 PPT/母稿生成 1920x1080 固定画布的逐页 HTML 页面。引用 ui-ux-pro-max 的设计系统与审查能力，内化语义化设计 token、清晰/克制/层次原则与高级感设计标准（反模板化排版、色彩/形状一致性锁定、AI 痕迹清单、审查修复工作流）。适用于 PPT 母稿转单页 HTML/领导汇报页落成 HTML/逐页生成 slide HTML/给 ppt-master 准备逐页 HTML/修复汇报页布局样式信息层级/把图表 HTML 嵌入汇报页等场景。图表 HTML 有问题时可调用 robot-aiot-xml-html-bridge 审查修复。 |
| `rowan` | `rowan` | Rowan是云原生分子建模和药物化学工作流平台，提供Python API。支持pKa/macropKa预测、构象/互变异构集合、对接/analogue docking、蛋白-配体cofolding、MSA生成、分子动力学、渗透性、描述符工作流等。适用于编程化批量筛选、多步化学pipeline和替代本地HPC/GPU基础设施的工作流。 |
| `safe-refactor` | `safe-refactor` | 在保留行为的前提下重构代码：提取、合并、所有权迁移或清理，验证必须包围结构性编辑。 |
| `scaffold-exercises` | `misc/scaffold-exercises` | 创建包含章节、题目、解答和说明的练习目录结构并通过 lint。适用于用户想搭建练习脚手架、创建练习模板或设置新课程章节时。 |
| `scaffold-exercises` | `scaffold-exercises` | 创建包含章节、题目、解答和说明的练习目录结构并通过 lint。适用于用户想搭建练习脚手架、创建练习模板或设置新课程章节时。 |
| `scanpy` | `scanpy` | 标准单细胞 RNA-seq 分析流程：QC、标准化、降维（PCA/UMAP/t-SNE）、聚类、差异表达、可视化，以及将 Seurat/SingleCellExperiment RDS 转为 h5ad。深度学习用 scvi-tools。 |
| `scenario-analyzer` | `scenario-analyzer` | 从新闻标题分析18个月情景展望。使用scenario-analyst agent做主分析，strategy-reviewer agent给第二意见。生成涵盖一/二/三阶影响、推荐标的和关键审查的综合英文报告。触发词包括news analysis、scenario analysis、18-month outlook等。 |
| `scholar-evaluation` | `scholar-evaluation` | 对学术作品进行定性优先、证据可追溯的发展性评审，审计低风险研究评估rubric，可选本地质量控制。绝不用于人员排名或后果性决策。 |
| `scientific-brainstorming` | `scientific-brainstorming` | 促进证据感知的科学构思：独立生成/结构化讨论/显式假设/透明评估/对抗性审查/决策日志。适用于早期研究头脑风暴或优先排序候选方向；实证验证/研究设计/伦理或法规审查/临床问题交给相应专家或 skill。 |
| `scientific-critical-thinking` | `scientific-critical-thinking` | 评估科学主张和证据质量：实验设计有效性、偏差和混杂因素识别、证据分级框架（GRADE/Cochrane Risk of Bias）、批判性分析教学。适用于理解证据质量和识别缺陷。正式同行评审写作使用peer-review。 |
| `scientific-schematics` | `scientific-schematics` | 使用Nano Banana 2 AI创建出版级科学示意图，支持智能迭代优化。用Gemini 3.6 Flash做质量审查，仅在低于文档类型阈值时重新生成。专长于神经网络架构、系统图、流程图、生物通路和复杂科学可视化。 |
| `scientific-slides` | `scientific-slides` | 构建学术报告幻灯片和演示文稿。用于制作 PowerPoint 幻灯片、会议报告、研讨会演讲、研究展示、答辩幻灯片或任何科学报告。提供幻灯片结构、设计模板、时间控制及视觉验证，支持 PowerPoint 和 LaTeX Beamer。 |
| `scientific-visualization` | `scientific-visualization` | 使用 Matplotlib/Seaborn/Plotly 创建和审查真实、无障碍、出版级科学图表。用于图表设计、多面板布局、不确定性与缺失数据展示、色彩/对比度审查、图像元数据验证及期刊导出规划。 |
| `scientific-writing` | `scientific-writing` | 起草、修订和审计科学稿件或报告，具备明确的证据来源、报告指南覆盖、作者责任、保密控制和本地一致性检查。适用于稿件章节、参考文献、声明、表格、图表或投稿准备中科学准确性和可追溯性重要的场景。 |
| `scikit-bio` | `scikit-bio` | 生物数据工具包：序列分析、比对、系统发育树、多样性指标(alpha/beta/UniFrac)、排序(PCoA)、PERMANOVA、FASTA/Newick I/O，用于微生物组分析。 |
| `scikit-learn` | `scikit-learn` | Python 机器学习库 scikit-learn，涵盖监督学习（分类/回归）、无监督学习（聚类/降维）、模型评估、超参数调优、预处理和 ML pipeline 构建。 |
| `scikit-survival` | `scikit-survival` | 使用 scikit-survival 构建/评估/审计右删失或竞争风险生存工作流，包括防泄漏预处理/模型选择/概率预测和删失感知指标。 |
| `scrape` | `gstack-scrape` | 从网页抓取数据。首次调用新意图时通过 $B 原语原型化流程并返回 JSON；后续匹配意图路由到已编码浏览器技能，约 200ms 返回。只读操作——表单填写/点击/提交等变更流程用 /automate。触发词：scrape、get data from、pull、extract from、what's on。 |
| `scvelo` | `scvelo` | scVelo RNA 速度分析。从 unspliced/spliced mRNA 动态估计细胞状态转变、推断轨迹方向、计算潜在时间并识别驱动基因。补充 Scanpy/scVI-tools 的轨迹推断能力。 |
| `scvi-tools` | `scvi-tools` | 单细胞组学的深度生成模型：概率批次校正(scVI)、迁移学习、带不确定性的差异表达、多模态整合(TOTALVI/MultiVI)。适用于高级建模、批次效应和多模态数据。标准分析pipeline用scanpy。 |
| `seaborn` | `seaborn` | 基于pandas集成的统计可视化，适合快速探索分布、关系和分类比较，默认样式美观。擅长箱线图、小提琴图、pair plot、热力图。基于matplotlib构建。交互式图表用plotly，出版级样式用scientific-visualization。 |
| `search-first` | `search-first` | 先研究再编码的工作流：编写自定义代码前先搜索现有工具、库和模式，调用 researcher agent。 |
| `sector-analyst` | `sector-analyst` | 分析板块轮动模式和市场周期定位。从 CSV 获取板块上升趋势数据（无需 API key），可选接受图表图片补充分析。适用于 sector rotation analysis/cyclical vs defensive assessment/overbought oversold identification/market cycle phase estimation。所有分析和输出以英文进行。 |
| `security-audit` | `security-audit` | Java 安全检查清单，覆盖 OWASP Top 10、输入验证、注入防护和安全编码。支持 Spring/Quarkus/Jakarta EE 和纯 Java。适用于审查代码安全、发布前或用户询问漏洞时。 |
| `security-review` | `security-review` | 添加认证、处理用户输入、操作密钥、创建 API 端点或实现支付/敏感功能时使用，提供全面的安全检查清单和模式。 |
| `security-scan` | `security-scan` | 使用AgentShield扫描Claude Code配置（.claude/目录）的安全漏洞、错误配置和注入风险。检查CLAUDE.md/settings.json/MCP servers/hooks/agent定义。适用于审计.claude/目录。 |
| `security-sentinel` | `security-sentinel` | 执行安全审计、漏洞评估、SSL/TLS加固、DNSSEC配置和合规检查。覆盖OWASP Top 10、CIS Benchmarks、邮件安全(SPF/DKIM/DMARC)和网络侦察。适用于安全审计、漏洞扫描、渗透测试、SSL加固、DNSSEC设置、合规检查或安全态势评估。 |
| `setup-browser-cookies` | `gstack-setup-browser-cookies` | 将真实 Chromium 浏览器的 cookie 导入无头浏览会话，交互式选择要导入的域名。QA 测试认证页面前使用，用户说"import cookies""login to the site"时触发。 |
| `setup-deploy` | `gstack-setup-deploy` | 为 /land-and-deploy 配置部署设置。自动检测部署平台（Fly.io/Render/Vercel/Netlify/Heroku/GitHub Actions/自定义）、生产 URL、健康检查端点和部署状态命令，将配置写入 CLAUDE.md 使后续部署自动化。触发词：setup deploy、configure deployment、set up land-and-deploy、add deploy config。 |
| `setup-gbrain` | `gstack-setup-gbrain` | 为编码 agent 设置 gbrain：安装 CLI、初始化本地 PGLite 或 Supabase brain、注册 MCP、捕获每远程信任策略。一条命令从零到"gbrain 运行中且 agent 可调用"。 |
| `setup-matt-pocock-skills` | `setup-matt-pocock-skills` | 为当前仓库配置工程技能体系：设置 issue tracker、分诊标签词汇和领域文档布局。首次使用其他工程技能前运行一次。 |
| `setup-matt-pocock-skills` | `engineering/setup-matt-pocock-skills` | 为当前仓库配置工程技能体系：设置 issue tracker、分诊标签词汇和领域文档布局。首次使用其他工程技能前运行一次。 |
| `setup-pre-commit` | `misc/setup-pre-commit` | 在当前仓库配置 Husky pre-commit hooks，集成 lint-staged（Prettier）、类型检查和测试。适用于用户想添加 pre-commit hooks、配置 Husky/lint-staged 或在提交时自动格式化/类型检查/测试时。 |
| `setup-pre-commit` | `setup-pre-commit` | 在当前仓库配置 Husky pre-commit hooks，集成 lint-staged（Prettier）、类型检查和测试。适用于用户想添加 pre-commit hooks、配置 Husky/lint-staged 或在提交时自动格式化/类型检查/测试时。 |
| `setup-ts-deep-modules` | `setup-ts-deep-modules` | 将 dependency-cruiser 接入 TypeScript 仓库，使每个包成为 deep module，实现隐藏在子文件夹中且仅通过入口文件可达。由用户手动触发。 |
| `setup-ts-deep-modules` | `in-progress/setup-ts-deep-modules` | 将dependency-cruiser接入TypeScript仓库，使每个package成为deep module——实现隐藏在子文件夹中，仅通过入口文件可达。用户手动调用。 |
| `shap` | `shap` | 使用 SHAP 解释和审计机器学习预测。适用于选择 SHAP explainers 和 maskers/计算和验证特征归因/处理多输出解释/生成本地或全局 SHAP 可视化。 |
| `ship` | `gstack-ship` | Ship工作流：检测+merge base branch、运行测试、审查diff、bump VERSION、更新CHANGELOG、commit、push、创建PR。适用于"ship""deploy""push to main""create a PR""merge and push""get it deployed"。当用户说代码就绪、询问部署、想push或创建PR时主动调用此skill而非直接push/PR。 |
| `short-term-stock-picker` | `short-term-stock-picker` | A 股短线选股工具（AKShare 数据），筛选条件：流通市值≤150 亿、近 20 日有涨停、非 ST、主板/深证/创业板/科创板、近 3 日主力净流入估算、换手率≤10%。用户问"帮我选短线股""找强势股"时触发。 |
| `signal-postmortem` | `signal-postmortem` | 记录和分析 edge pipeline 及其他技能生成的信号的交易后结果。追踪误报、错过机会和 regime 错配，将结果反馈给 edge-signal-aggregator 权重和技能改进待办事项。 |
| `simpy` | `simpy` | 使用 SimPy 构建、检查、测试和分析有界离散事件仿真，涵盖事件、资源、中断、监控、重复运行、预热期及可复现的输出分析。 |
| `skill-creator` | `skill-creator` | 创建新 skill、修改和改进现有 skill、衡量 skill 性能。适用于用户想从零创建 skill、编辑或优化现有 skill、运行 evals 测试 skill、基准方差分析或优化 skill 描述以提高触发准确率时。 |
| `skill-curator` | `skill-curator` | 中文 Skill 收录评估器，核验 GitHub 上的 Claude Code/Codex/Agent Skills/Plugin/MCP/CLI 工作流是否值得加入精选列表，检查真实资产、安装方式、活跃度、重复项和安全边界，生成分类、中文描述与可追溯证据。 |
| `skill-designer` | `skill-designer` | 从结构化创意规格设计新的 Claude 技能。当技能自动生成管线需要产出 Claude CLI 提示以创建完整技能目录（SKILL.md、references、scripts、tests）并遵循仓库规范时使用。 |
| `skill-idea-miner` | `skill-idea-miner` | 从Claude Code会话日志中挖掘skill idea候选。在周度skill生成pipeline中运行，从近期编码会话中提取、评分和backlog新skill想法。 |
| `skill-integration-tester` | `skill-integration-tester` | 验证 CLAUDE.md 中定义的多技能工作流，检查技能存在性、技能间数据契约（JSON schema 兼容性）、文件命名规范和交接完整性。在添加新工作流、修改技能输出或发布前验证管线健康时使用。 |
| `skillify` | `gstack-skillify` | 将最近成功的 /scrape 流程固化为永久浏览器技能。未来相同意图的 /scrape 调用直接运行固化脚本（约 200ms），无需重新驱动页面。回溯对话合成 script.ts + test + fixture，临时目录测试通过后询问再提交。 |
| `slack-gif-creator` | `slack-gif-creator` | 创建针对 Slack 优化的动画 GIF 的知识与工具集。提供约束、验证工具和动画概念。适用于用户请求为 Slack 制作动画 GIF 时。 |
| `slides` | `slides` | 使用 Chart.js、设计 token、响应式布局、文案公式和上下文幻灯片策略创建战略性 HTML 演示文稿。 |
| `slideshow` | `slideshow` | 编写 HyperFrames slideshow——具有离散幻灯片、片段揭示、分支、热点导航和内置演讲者模式（含演讲者备注）的演示文稿/路演/交互式 deck；也可将现有页面转为 deck。输出是可导航的 deck 而非渲染的 MP4。用户未明确要求 slideshow 时先确认。不确定时用 /hyperframes。 |
| `solid-principles` | `solid-principles` | SOLID 原则清单及 Java 示例。适用于类职责过多、抽象泄漏、依赖方向错误，以及用户询问单一职责/开闭/里氏替换/接口隔离/依赖倒置时。命名、重复和方法长度请用 clean-code。 |
| `spec` | `gstack-spec` | 将模糊意图转化为精确可执行的spec，分五阶段完成。自动创建issue，可选在新worktree中启动Claude Code agent，支持/ship在merge时关闭源issue。适用于"spec this out""file an issue""write up a ticket"等请求。 |
| `spring-boot-patterns` | `spring-boot-patterns` | Spring Boot 最佳实践与模式。适用于创建 controller/service/repository 或用户询问 Spring Boot 分层、装配、配置或异常处理时。JPA/Hibernate 行为请用 jpa-patterns。 |
| `springboot-patterns` | `springboot-patterns` | Spring Boot 架构模式/REST API 设计/分层服务/数据访问/缓存/异步处理/日志。适用于 Java Spring Boot 后端工作。构建或审查 Spring Boot 后端（REST 层/服务/数据访问/缓存/异步）时使用。 |
| `springboot-security` | `springboot-security` | Spring Security 最佳实践：authn authz/验证/CSRF/secrets/headers/限流/Java Spring Boot 服务中的依赖安全。适用于审查 Spring Security authn authz/验证/CSRF/secrets/headers/限流时。 |
| `springboot-tdd` | `springboot-tdd` | Spring Boot 测试驱动开发，使用 JUnit 5、Mockito、MockMvc、Testcontainers 和 JaCoCo。添加功能、修复 bug 或重构时使用。 |
| `springboot-verification` | `springboot-verification` | Spring Boot 项目验证循环：构建、静态分析、带覆盖率的测试、安全扫描及 diff 审查，用于发布或 PR 前。 |
| `stable-baselines3` | `stable-baselines3` | 生产级强化学习算法库（PPO/SAC/DQN/TD3/DDPG/A2C），scikit-learn 风格 API。适用于单智能体 Gymnasium 环境的标准 RL 实验和快速原型。高性能并行训练或多智能体用 pufferlib。 |
| `stanley-druckenmiller-investment` | `stanley-druckenmiller-investment` | Druckenmiller 策略合成器：整合 8 个上游技能输出（市场广度、上升趋势、市场顶部、宏观状态、FTD、VCP、主题、CANSLIM）为统一确信度评分（0-100）、模式分类和配置建议。 |
| `statistical-analysis` | `statistical-analysis` | 研究数据的引导式统计分析：检验选择、假设检验、效应量、功效分析、贝叶斯替代方案和APA格式报告。适用于组间比较、假设检验、实验/调查数据分析、统计假设检查、样本量计算或结果撰写。覆盖t检验/ANOVA/卡方/相关/回归/非参数/贝叶斯方法。 |
| `statistical-power` | `statistical-power` | 样本量和统计功效计算。覆盖 t 检验/ANOVA/比例/相关/卡方/回归的闭式功效，以及 logistic/Poisson/混合模型/整群随机/生存分析的 Monte Carlo 模拟功效。用于研究设计和样本量论证。 |
| `statsmodels` | `statsmodels` | Python 统计模型库，提供 OLS/GLM/混合模型/ARIMA 等模型类及详细诊断、残差和推断。适用于计量经济学、时间序列和严谨系数表推断。引导式统计检验用 statistical-analysis。 |
| `stitch-design-taste` | `stitch-skill` | 为Google Stitch生成语义化设计系统文件DESIGN.md，强制执行高端反模板UI标准：严格排版、校准配色、非对称布局、持续微动效、硬件加速性能。 |
| `stock-analysis` | `stock-analysis-skill` | 股票智能分析技能。输入 A股/港股/美股代码，自动获取实时行情与历史K线，计算 MA/MACD/RSI/量能/乖离率等技术指标，综合评分（百分制）并给出买卖信号，搜索最新新闻消息面，AI 综合分析输出决策看板。用户提供股票代码要求分析、询问某只股票情况或要求看盘分析时触发。 |
| `stock-analyst` | `stock-analyst` | 美股/港股盘前分析框架：抓取五大观测指标（VIX/IGV/MAGS/MEME/布油）、个股实时价格、期权隐含波动率，生成结构化盘前简报。含量化模块（粒子滤波概率追踪、期权蒙卡定价、Copula VaR），支持持仓JSON管理和实时浮盈亏计算。 |
| `stockbee-20pct-study` | `stockbee-20pct-study` | 构建和维护Stockbee风格每日20%异动研究：扫描+20%/-20%异动股、分类催化剂和setup背景、更新前瞻结果、总结队列模式。适用于运行每日20% study、回填历史20%异动、发现重复edge模式或构建爆发式市场运动model book。 |
| `stockbee-episodic-pivot-analyzer` | `stockbee-episodic-pivot-analyzer` | 分析Stockbee风格Day 1 Episodic Pivot候选：财报/指引上调/并购/FDA审批/分析师行动/重大合同/产品发布/轧空催化剂/主题事件。综合评分催化剂质量、gap/range扩张、成交量冲击、忽视/重估背景、流动性和EP日低点风险。适用于EP候选/episodic pivots/Day 1 catalyst trades/game-changing news reactions/delayed EP watchlists或转入PEAD监控。 |
| `stockbee-exhaustion-hammer-screener` | `stockbee-exhaustion-hammer-screener` | 筛选符合Stockbee风格卖出耗竭锤子形态的美股：基于前期动量、回调深度、undercut/reclaim、长下影线几何、收盘位置、成交量确认、质量/流动性门槛和风险距离评分。适用于Stockbee/exhaustion setup/hammer reversal/undercut reclaim/pullback entry等请求。 |
| `stockbee-momentum-burst-screener` | `stockbee-momentum-burst-screener` | Stockbee 风格短期动量爆发选股筛选器。使用 4% 突破、美元突破、区间扩张、成交量扩张、前期区间收缩、收盘位置、失败过滤及风险距离评分筛选美股。触发词：Stockbee、Pradeep Bonde、momentum burst、4% breakout、range expansion、dollar breakout、短期波段动量候选、3-5 天爆发设置回顾。 |
| `stockbee-setup-fluency-trainer` | `stockbee-setup-fluency-trainer` | 从 momentum-burst screener 候选构建 Stockbee 风格 setup model book，然后用 MFE MAE/止损触发状态/结果标签/队列统计更新 3 天和 5 天前向结果。适用于用户想研究 Stockbee Momentum Burst 示例/跟踪失败候选/建立 setup 熟练度/审查 A B setup 质量/将 screener 输出转化为学习循环而非即时交易信号时。 |
| `strategic-compact` | `strategic-compact` | 在逻辑间隔建议手动上下文压缩，按任务阶段而非任意自动压缩来保留上下文。会话接近上下文限制且任务阶段是自然压缩点时使用。 |
| `strategy-pivot-designer` | `strategy-pivot-designer` | 检测回测迭代停滞，当参数调优陷入局部最优时生成结构性不同的策略转向提案。 |
| `string-reviewer` | `string-reviewer` | 审查代码库中的文本和用户面向字符串，确保遵循清晰度、有用性、简洁性和风格规则。 |
| `subagent-driven-development` | `subagent-driven-development` | 在当前会话中执行包含独立任务的实现计划时使用，通过 subagent 驱动开发。 |
| `surgical-patch` | `surgical-patch` | 在最窄的合理层面修复bug和小行为变更。适用于需要回归证明、保留周围行为和任务相关测试的场景。 |
| `sympy` | `sympy` | 在 Python 中需要精确符号数学时使用——代数/微积分/方程求解/符号线性代数/通过 lambdify LaTeX 代码生成。浮点近似足够时优先用 NumPy 或 SciPy。 |
| `sync-gbrain` | `gstack-sync-gbrain` | 保持gbrain与当前仓库代码同步并刷新CLAUDE.md中的agent搜索指引。封装gstack-gbrain-sync编排器，含状态探测、原生代码面注册、能力检查和判定块。可重跑、幂等。适用于"sync gbrain""refresh gbrain""re-index this repo""gbrain search isn't finding things"。 |
| `systematic-debugging` | `systematic-debugging` | 遇到任何 bug/测试失败/异常行为时使用，在提出修复方案之前先执行系统化调试。 |
| `talking-head-recut` | `talking-head-recut` | 为现有出镜/访谈/播客视频打包定时设计的 GRAPHIC OVERLAY 卡片——动态标题/lower-thirds/数据标注/引用/侧面板/画中画——与字幕同步，在你选择的 16:9/9:16/4:5 画布上；底层片段不受影响地播放。在 graphic overlays/on-screen graphics/package dress up my video 时触发。非纯字幕（用 /embedded-captions）。不确定时用 /hyperframes。 |
| `tamarind` | `tamarind` | Tamarind Bio 平台开源分子设计与结构生物学工具集，通过 REST API 或 MCP 服务器访问，无需本地 GPU。集成 AlphaFold/Boltz/Chai/ESMFold 结构预测、RFdiffusion/ProteinMPNN/BoltzGen 蛋白质设计、抗体/纳米抗体设计、DiffDock/Autodock Vina 对接、结合亲和力预测、MSA 生成及分子动力学。提及 Tamarind/tamarind.bio/app.tamarind.bio/api/x-api-key 或需云端批量提交序列时触发。 |
| `tdd` | `tdd` | 测试驱动开发。适用于用户想以测试优先方式构建功能或修复 bug、提及 red-green-refactor 或想要集成测试时。 |
| `tdd` | `engineering/tdd` | 测试驱动开发。适用于用户想以测试优先方式构建功能或修复 bug、提及 red-green-refactor 或想要集成测试时。 |
| `tdd-workflow` | `tdd-workflow` | 测试驱动开发工作流。在编写新功能、修复 bug 或重构代码时使用，强制执行 TDD 并确保 80%+ 覆盖率（含单元、集成和 E2E 测试）。 |
| `teach` | `teach` | 在当前工作区内教授用户新技能或概念。 |
| `teach` | `productivity/teach` | 在当前工作区内教授用户新技能或概念。 |
| `technical-analyst` | `technical-analyst` | 分析股票/指数/加密货币/外汇对的周线图。用户提供图表图片并要求技术分析、趋势识别、支撑阻力位、情景规划或概率评估时触发，纯基于图表数据不考虑新闻或基本面。 |
| `test-driven-development` | `test-driven-development` | 在实现任何功能或修复 bug 时使用，在编写实现代码之前先写测试。 |
| `test-generator` | `test-generator` | 依据真实代码契约生成并验证单元测试或集成测试。适用于为函数/类/接口或缺陷补测试/提高覆盖率/生成回归用例/完善测试策略时；先读取现有测试与调用方，不猜测空值/异常/超时行为，不自动安装框架或访问生产依赖。 |
| `test-quality` | `test-quality` | 使用 AssertJ 断言编写高质量 JUnit 5 测试。适用于用户说 add tests/write tests/improve test coverage 或审查/创建 Java 测试类时。 |
| `theme-detector` | `theme-detector` | 检测和分析跨行业的热门市场主题。当用户询问当前市场主题、热门板块、板块轮动、主题投资、哪些主题冷热，或希望识别多空市场叙事及生命周期分析时使用。 |
| `theme-factory` | `theme-factory` | 为幻灯片、文档、报告、HTML 落地页等制品应用主题样式的工具集。内置 10 套预设主题（配色/字体），也可即时生成新主题。 |
| `tiledbvcf` | `tiledbvcf` | 使用 TileDB 高效存储和检索基因组变异数据，支持可扩展 VCF/BCF 导入、增量样本添加、压缩存储、并行查询和群体基因组学导出。 |
| `timesfm-forecasting` | `timesfm-forecasting` | 使用Google TimesFM基础模型进行零样本时间序列预测。适用于任何单变量时序（销售/传感器/能源/生命体征/天气），无需训练自定义模型。支持CSV/DataFrame/array输入，提供点预测和预测区间。首次使用前含preflight系统检查脚本验证RAM/GPU。 |
| `to-questionnaire` | `to-questionnaire` | 将无法完全回答的决策转化为问卷让他人填写。 |
| `to-questionnaire` | `productivity/to-questionnaire` | 将无法完全回答的决策转化为问卷让他人填写。 |
| `to-spec` | `to-spec` | 将当前对话转为规格并发布到项目 issue tracker：不做访谈，仅综合已讨论内容。 |
| `to-spec` | `engineering/to-spec` | 将当前对话转化为规格并发布到项目 issue tracker，无需访谈，直接综合已讨论内容。 |
| `to-tickets` | `to-tickets` | 将计划、规格或当前对话拆分为一组 tracer-bullet tickets，每个声明阻塞边，发布到配置的 tracker（本地每票一文件含文本边，或真实 tracker 的原生阻塞链接）。 |
| `to-tickets` | `engineering/to-tickets` | 将计划、规格或当前对话拆分为 tracer-bullet ticket 集，每个声明阻塞边并发布到配置的 tracker。本地每票一文件含文本边，真实 tracker 用原生阻塞链接。 |
| `torch-geometric` | `torch-geometric` | PyTorch Geometric(PyG)图神经网络：节点/边/图分类、消息传递(GCN/GAT/GraphSAGE/GIN)、异构图、邻居采样和自定义数据集。适用于torch_geometric相关工作，非通用NetworkX分析或非图PyTorch模型。 |
| `torchdrug` | `torchdrug` | TorchDrug 0.2.1 工作流构建与排障，涵盖分子图、性质预测、自监督预训练、分子生成、逆合成、蛋白质表示学习及知识图谱推理。代码导入 torchdrug 或需其数据集/模型/任务/Engine 时使用。 |
| `trade-hypothesis-ideator` | `trade-hypothesis-ideator` | 从市场数据、交易日志和日记片段生成可证伪的交易策略假设，输出带实验设计和终止标准的排序假设卡片，可选导出兼容 edge-finder-candidate/v1 的 strategy.yaml。 |
| `trade-performance-coach` | `trade-performance-coach` | 审查已平仓交易、部分退出和月度汇总的流程遵守、风险纪律、执行质量和基于证据的交易行为模式。在trader-memory-core和signal-postmortem产出记录后使用，或用户请求post-trade coach/风控风格审查/规则遵守审查/下场操作规则/心理aware交易行为反馈时使用。不提供买卖建议、治疗或经纪执行。 |
| `trader-memory-core` | `trader-memory-core` | 跟踪投资论点的全生命周期——从筛选想法到平仓及事后分析。从 screener 输出注册论点/管理状态转换/附加仓位大小/审查到期日/生成含 P&L 和 MAE MFE 分析的事后报告。在 register thesis/track this idea/thesis status/review due/close position/postmortem/trading journal 时触发。 |
| `trading-skills-navigator` | `trading-skills-navigator` | 从自然语言目标推荐合适的交易工作流、技能集、API profile和入门路径。作为用户表达交易/投资目标时的入口，帮助确定使用哪个skill/workflow、从哪里开始、是否有无需付费API key的方案。仅路由和解释，不执行交易或自动运行其他skill。 |
| `transformers` | `transformers` | Hugging Face Transformers：加载Hub模型、pipeline推理、文本生成和Trainer微调，覆盖NLP/视觉/音频/多模态任务。适用于AutoModel/pipelines/tokenizers/TrainingArguments相关工作，非Transformers库外的通用ML。 |
| `treatment-plans` | `treatment-plans` | 在临床决策已由授权执业专业人员提供并验证后，格式化和结构验证本地治疗计划文档。适用于来源追溯、临床医生撰写的干预记录、目标和检查点、共同决策记录、交接核对和发布门控——不用于临床决策。 |
| `triage` | `triage` | 通过分诊角色状态机推进 issue 和外部 PR：分类、验证、必要时追问，并编写 agent-ready briefs。 |
| `triage` | `engineering/triage` | 通过分类→验证→质询的状态机处理 issue 和外部 PR，必要时深入质询并编写 agent 可用的简报。 |
| `tui-tester` | `tui-tester` | 使用终端自动化测试 Gemini CLI 行为和视觉输出的专家指导。 |
| `ui-styling` | `ui-styling` | 使用 shadcn/ui 组件（Radix UI + Tailwind）、Tailwind CSS utility-first 样式和 canvas 视觉设计创建美观、无障碍的用户界面。适用于构建 UI、实现设计系统、创建响应式布局、添加无障碍组件（对话框/下拉菜单/表单/表格）、自定义主题颜色、实现暗色模式、生成视觉设计和海报，或建立跨应用一致的样式模式。 |
| `ui-to-vue` | `ui-to-vue` | 当用户有 UI 截图或设计导出需要批量转换为 Vue 3 组件时使用，尤其配合 Vant/Element Plus/Ant Design Vue。 |
| `ui-ux-pro-max` | `ui-ux-pro-max` | Web/移动端/桌面端 UI/UX 设计智能：覆盖页面、组件、设计系统、无障碍、交互、响应式布局、排版、配色、图表及各技术栈 UI 实现。内置 79 种可搜索风格、192 套产品调色板、74 组字体搭配、119 条 UX 准则、105 个图标、17 个 GSAP 预设、25 种图表类型和 22 个技术栈数据。适用于设计、构建、审查或修复界面时触发。 |
| `umap-learn` | `umap-learn` | 使用 UMAP-learn 进行非线性降维/2D 3D 嵌入/聚类预处理/监督或半监督 UMAP/DensMAP/AlignedUMAP/Parametric UMAP 工作流。 |
| `uncertainty-and-units` | `uncertainty-and-units` | 使用 pint 和 uncertainties 追踪物理单位和测量不确定度，支持单位换算、量纲检查、GUM 不确定度评定、Monte Carlo 传播、无量纲群合理性检验。当质疑数值物理合理性或单位异常时触发。 |
| `unfreeze` | `gstack-unfreeze` | 清除/freeze设置的冻结边界，允许再次编辑所有目录。适用于想扩大编辑范围但不结束会话时。触发词包括"unfreeze""unlock edits""remove freeze""allow all edits"。 |
| `unified-memory` | `unified-memory` | 通过本地 ECC Memory Vault 在 Claude/Codex/Hermes/Cursor/OpenCode 和其他 agents 之间共享持久可检查的上下文和交接。适用于 agent 必须保存工作状态/转移上下文/恢复另一 agent 的任务/搜索共享项目知识时。 |
| `uptrend-analyzer` | `uptrend-analyzer` | 基于 Monty Uptrend Ratio Dashboard 数据分析市场广度，从广度、板块参与、轮动、动量、历史背景五维度生成 0-100 综合评分，判断市场环境是否适合持股。无需 API key。 |
| `us-market-bubble-detector` | `us-market-bubble-detector` | 使用修订版Minsky/Kindleberger框架v2.1通过量化数据驱动分析评估市场泡沫风险。优先客观指标（Put/Call/VIX/margin debt/breadth/IPO）而非主观印象。严格定性调整标准防确认偏差。支持带强制数据采集和机械评分的实际投资决策。适用于泡沫风险、估值担忧或获利了结时机。 |
| `us-stock-analysis` | `us-stock-analysis` | 全面的美股分析，包括基本面分析（财务指标、业务质量、估值）、技术分析（指标、图表形态、支撑/阻力）、股票对比和投资报告生成。适用于美股ticker分析、财务指标评估、技术图表分析或投资建议。 |
| `usfiscaldata` | `usfiscaldata` | 查询美国财政部 Fiscal Data REST API 获取联邦财务数据（国债、每日/每月财政报表、证券拍卖、利率、汇率、储蓄债券、收支统计），无需 API key。 |
| `using-git-worktrees` | `using-git-worktrees` | 当需要开始与当前工作区隔离的功能开发，或在执行实现计划之前使用——通过原生工具或 git worktree 回退机制确保隔离工作区存在。 |
| `using-superpowers` | `using-superpowers` | 在任何对话开始时使用，确立如何查找和使用技能，要求在任何响应（含澄清问题）之前先调用Skill工具。 |
| `vaex` | `vaex` | 处理和分析超出可用 RAM 的大型表格数据集（数十亿行）。Vaex 擅长核外 DataFrame 操作/惰性求值/快速聚合/大数据高效可视化/大数据集机器学习。适用于处理大型 CSV HDF5 Arrow Parquet 文件/海量数据集快速统计/大数据可视化/构建不适合内存的 ML pipeline 时。 |
| `value-dividend-screener` | `value-dividend-screener` | 筛选兼具价值特征（P/E<20、P/B<2）、高股息率（3%+）和持续增长（股息/营收/EPS三年趋势向上）的优质美股股息标的。支持两阶段筛选：FINVIZ Elite API预过滤+FMP API详细分析。适用于股息股筛选、收入组合思路或基本面扎实的价值股息股查找。 |
| `vcp-screener` | `vcp-screener` | 筛选标普500中符合Mark Minervini波动率收缩形态(VCP)的股票，或对单个标的历史价格路径检测所有VCP并统计突破/止损/超时结果。适用于VCP选股、Minervini式 setups、紧基底突破候选、Stage 2动量扫描及特定ticker历史VCP研究。 |
| `venue-templates` | `venue-templates` | 使用特定期刊/会议格式指导和捆绑 LaTeX 脚手架准备期刊稿件、会议论文、研究海报及基金申请文档。用于选择官方模板、检查页数或匿名规则、适配学术写作至特定场合或检查投稿 PDF。 |
| `vercel-cli-with-tokens` | `vercel-cli-with-tokens` | 使用基于 token 的身份验证在 Vercel 上部署和管理项目。适用于使用 access token 而非交互式登录操作 Vercel CLI 的场景，如 deploy to vercel/set up vercel/add environment variables to vercel。 |
| `vercel-composition-patterns` | `composition-patterns` | 可扩展的 React 组合模式。用于重构布尔 prop 泛滥的组件、构建灵活组件库或设计可复用 API，涵盖复合组件、render props、Context Provider 及组件架构，包含 React 19 API 变更。 |
| `vercel-optimize` | `vercel-optimize` | Vercel 已部署项目的成本和性能优化，尤其 Next.js/SvelteKit/Nuxt 和部分 Astro 应用。先收集 Vercel 指标/用量/项目配置/代码扫描结果；仅调查有指标支撑的候选项；产出基于已验证文件和版本感知 Vercel/框架文档的排序建议。适用于 Vercel 账单缩减、慢/贵路由、缓存机会、Function Invocations/Build Minutes/Fast Data Transfer/Core Web Vitals/Bot Management/Fluid compute 或成本分解请求。 |
| `vercel-react-best-practices` | `react-best-practices` | Vercel 工程团队的 React 和 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码以确保最优性能模式时使用，涵盖 React 组件、Next.js 页面、数据获取、包优化或性能改进。 |
| `vercel-react-native-skills` | `react-native-skills` | React Native 和 Expo 构建高性能移动应用的最佳实践。适用于构建 RN 组件、优化列表性能、实现动画或使用原生模块时。涉及 React Native/Expo/移动性能/原生平台 API 的任务触发。 |
| `vercel-react-view-transitions` | `react-view-transitions` | 使用 React View Transition API（<ViewTransition> 组件、addTransitionType、CSS view transition 伪元素）实现流畅原生感动画的指南。适用于添加页面过渡、动画路由切换、共享元素动画、组件进出动画、列表重排动画、方向性（前进/后退）导航动画或在 Next.js 中集成 view transitions 时。用户提及 view transitions/startViewTransition/ViewTransition/transition types 或询问不使用第三方动画库在 React 中动画化 UI 状态切换时也触发。 |
| `verification-before-completion` | `verification-before-completion` | 宣称工作完成、修复或测试通过前必须运行验证命令并确认输出，提交或创建 PR 前使用。始终用证据支撑断言。 |
| `verification-loop` | `verification-loop` | Claude Code 会话综合验证系统。在声称 Claude Code 会话工作完成之前使用。 |
| `verify-and-stop` | `verify-and-stop` | 证明现有工作满足验收条件而不扩大范围。适用于纯验证任务、完成检查、聚焦gate运行和最后里程证明。 |
| `verify-chain` | `verify-chain` | 验证链——角色对抗式技术文章交叉验证。写完 IT 文章后 Critic 提取关键断言并生成核查问题，多个 Verifier SubAgent 独立上下文联网验证，Repairer 自动修复。用于规避 AI 幻觉/知识过时/信息遗漏。 |
| `vite-patterns` | `vite-patterns` | Vite 构建工具模式，涵盖配置、插件、HMR、环境变量、代理、SSR、库模式、依赖预打包和构建优化。处理 vite.config.ts 或 Vite 项目时触发。 |
| `vue-patterns` | `vue-patterns` | Vue.js 3 Composition API 模式、组件架构、响应式最佳实践、Pinia 状态管理、Vue Router 导航及 Nuxt SSR 模式。Vue/Nuxt/Vite/Pinia 项目激活。用于构建或审查 Vue 3/Nuxt/Pinia 代码——Composition API、响应式或路由导航。 |
| `wait-what` | `wait-what` | 暂停并重述：上一条消息未传达清楚时重新表达。 |
| `wait-what` | `productivity/wait-what` | 停止。上一条消息没有传达清楚，重新表述。 |
| `wayfinder` | `wayfinder` | 将超出单次 agent 会话承载量的大型工作规划为 issue tracker 上的共享决策票据地图，逐个解决直至路径清晰。 |
| `wayfinder` | `engineering/wayfinder` | 将超出单个 agent 会话容量的大型工作规划为 issue tracker 上的共享决策票地图，逐个解决直到路径清晰。 |
| `waypoint-bio` | `waypoint-bio` | Outpost Bio 开放微生物组基础模型工具。涵盖 Waypoint 检查点（6m/45m/170m）、Atlas 预训练语料、Compass 八任务基准及 waypoint CLI。用于微生物组样本嵌入、分类丰度数据微调、Compass 基准测试、GPT-2 预训练及 MetaPhlAn/Kraken2/QIIME2/MGnify 丰度表转换为 waypoint 格式。 |
| `web-artifacts-builder` | `web-artifacts-builder` | 使用现代前端技术（React/Tailwind CSS/shadcn/ui）创建复杂多组件 claude.ai HTML artifacts 的工具套件。适用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifacts，不适用于简单单文件 HTML/JSX artifacts。 |
| `web-design-guidelines` | `web-design-guidelines` | 按 Web Interface Guidelines 审查 UI 代码。适用于被要求 review my UI、check accessibility、audit design、review UX 或 check my site against best practices 时。 |
| `web-recorder` | `web-recorder` | 将网页上的重复操作录制下来，以后让AI自动执行。适用于每天导出数据、每周提交报表、批量处理单据等场景。录一次后说"帮我运行"即可。支持SSO登录、API分析、选择器验证、下载类型自动识别。不用于简单爬取或单次操作。触发词包括"录制网页""录脚本""自动化""RPA"等。 |
| `webapp-testing` | `webapp-testing` | 使用 Playwright 与本地 Web 应用交互和测试的工具集。支持验证前端功能、调试 UI 行为、截取浏览器截图和查看浏览器日志。 |
| `weekly-performance-digest` | `weekly-performance-digest` | 从已关闭的 trader-memory-core 论点生成每周绩效摘要——胜率、期望值、利润因子、R 倍数、MAE/MFE 及按来源技能/退出原因/论点类型/板块/机制的胜负模式分析。纯本地计算，无需 API。 |
| `what-if-oracle` | `what-if-oracle` | 结构化假设情景分析工具，探索 4-6 个分支可能性（最佳、最可能、最差、意外、反向思维、二阶效应）。当用户提出关于不确定未来的推测性问题、战略分歧、应急规划或在决策前进行压力测试时使用。 |
| `wizard` | `wizard` | 生成交互式 bash 向导，引导人类完成只有他们才能执行的步骤。适用于配置基础设施、设置凭证或 CI secrets、走查不熟悉的第三方面板、执行一次性迁移或切换。agent 自己能做的步骤不要调用此 skill。 |
| `wizard` | `engineering/wizard` | 生成交互式 bash 向导，引导人类完成只有他们才能执行的步骤。适用于配置基础设施、设置凭证或 CI secrets、走查不熟悉的第三方面板、执行一次性迁移或切换。agent 自己能做的步骤不要调用此 skill。 |
| `workflow-runner` | `workflow-runner` | 在 Claude Code/OpenClaw/Cursor 中直接运行 agency-orchestrator YAML 工作流，无需 API key，使用当前会话 LLM 作为执行引擎。当用户提供 .yaml 工作流文件或要求多角色协作完成任务时触发。 |
| `wps-excel` | `wps-excel` | WPS 表格智能助手，通过自然语言操控 Excel，解决公式编写、数据清洗、图表创建等痛点。 |
| `wps-office` | `wps-office` | WPS Office 跨应用智能助手，统一管理 Excel、Word、PPT 三大应用，处理跨应用操作和通用功能。 |
| `wps-ppt` | `wps-ppt` | WPS 演示智能助手，通过自然语言操控 PPT，解决排版美化、内容生成、动画设置等痛点。 |
| `wps-word` | `wps-word` | WPS 文字智能助手，通过自然语言操控 Word 文档，解决排版、格式、内容编辑问题。 |
| `writing-beats` | `in-progress/writing-beats` | 写作开发阶段：将原始素材组装为beats旅程，在每个beat依赖术语前先奠定其基础。 |
| `writing-beats` | `writing-beats` | 写作利用阶段：将原始素材组装成节拍旅程，在每个术语被节拍依赖前先确立其基础。 |
| `writing-for-agents` | `writing-for-agents` | 为 agent 编写文档。适用于创建或编辑 skill、修改 AGENTS.md 或 CLAUDE.md 时。 |
| `writing-for-agents` | `productivity/writing-for-agents` | 为 agent 编写文档。适用于创建或编辑 skill、修改 AGENTS.md 或 CLAUDE.md 时。 |
| `writing-fragments` | `in-progress/writing-fragments` | 写作探索阶段：挖掘原始片段，尚无结构。 |
| `writing-fragments` | `writing-fragments` | 写作探索阶段：挖掘原始片段，尚无结构。 |
| `writing-great-skills` | `writing-great-skills` | 编写和编辑优质 skill 的参考：使 skill 可预测的词汇和原则。 |
| `writing-guidelines` | `writing-guidelines` | 按Writing Guidelines审查文档/散文。适用于"review my docs""check writing style""audit prose""review docs voice and tone"或"check this page against the writing handbook"。 |
| `writing-plans` | `writing-plans` | 当有规格说明或需求用于多步骤任务时，在动手写代码之前使用此技能制定计划。 |
| `writing-shape` | `in-progress/writing-shape` | 写作开发阶段：将原始素材逐段塑造成文章。 |
| `writing-shape` | `writing-shape` | 写作利用阶段：将原始素材逐段塑造成文章。 |
| `writing-skills` | `writing-skills` | 创建新技能、编辑现有技能或部署前验证技能有效性时使用。 |
| `xlsx` | `xlsx` | 当电子表格文件是主要输入或输出时使用。包括打开/读取/编辑/修复 .xlsx/.xlsm/.xltx/.csv/.tsv 文件（加列、计算公式、格式化、图表、清洗脏数据）；从零或其他数据源创建新表格；在表格文件格式间转换。用户按名称或路径提及表格文件并要求操作时也触发。交付物必须是表格文件。主要交付物为 Word/HTML/Python 脚本/数据库管道/Google Sheets API 集成时不触发。 |
| `zarr-python` | `zarr-python` | Zarr-Python 3 云端存储分块 N 维数组。支持压缩数组、并行 I/O、通过 fsspec 访问 S3/GCS，兼容 NumPy/Dask/Xarray，用于大规模科学计算管线。 |
| `zh-code-reviewer` | `zh-code-reviewer` | 中文代码审查专家：生成详细的中文代码审查报告。 |
| `zh-docgen` | `zh-docgen` | 中文文档生成器：从代码库自动生成中文技术文档。 |
| `zh-readme` | `zh-readme` | 中文README生成器：先分析项目，再生成面向中文开发者的高质量README。 |

## 第三部分：`agent-skills/self-skills/`（用户自写）

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`（用户自写 skill 真源）

共 **16** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `archify` | `robot-aiot-draw-flowchart/archify` | 创建精美的架构、工作流、时序、数据流和生命周期/状态图，输出为可交互的独立 HTML（内联 SVG），支持深色/浅色主题、可选轨迹动画及 PNG/JPEG/WebP/SVG/WebM 导出。接受自然语言需求或粘贴的 Mermaid flowchart/sequenceDiagram/stateDiagram 输入；当图表需反映真实代码时检查仓库证据。适用于可视化系统架构、基础设施、云/安全/网络拓扑、技术工作流、API 调用序列、请求生命周期、数据管道、ETL/ELT、数据血缘、状态机，或转换/美化 Mermaid 图表。 |
| `dev-paradigm-matt` | `dev-paradigm-matt` | 面向日常工程开发的分层工作流路由：根据任务阶段将需求澄清、规格设计、架构规划、实现、调试、审查、交接和长期维护路由到合适的 matt-skills。适用于这个需求怎么推进、从需求到代码怎么分阶段、该先 grill 还是 to-spec、Bug/重构/新功能分别怎么走、完整开发流程编排、接手陌生项目需 setup/领域建模/票据拆分/实现收尾/长期维护规划等场景。 |
| `easy-crawler` | `easy-crawler` | 可独立部署的网页抓取 skill，统一处理通用网页抓取、社媒平台专项优化和反爬/浏览器自动化场景。优先给出统一任务契约、可观测输出和显式失败，不把未实现的逆向能力伪装成已支持。 |
| `mac-safe-storage-cleaner` | `mac-safe-storage-cleaner` | 安全检查并清理 macOS 机器上的缓存、日志、临时文件、Downloads 安装包及受控 Workspace 历史目录。触发：清理系统缓存/文件占用/Workspace 占用/日志/磁盘空间不够/删除临时文件/清理 IDEA 日志/查看可删文件/分析占用/磁盘瘦身。也适用于复查清理规则、验证保护目录、确认不会误删，及执行先分析再确认最后决定是否删除的交互流程。 |
| `opsx-workflow-hooks` | `opsx-workflow-hooks` | opsx 工作流的 Post-command hooks。Trigger A：/opsx/propose 完成所有 artifacts 后立即进入迭代精炼循环，询问用户是否有新想法并更新提案 artifacts 直到满意。Trigger B：/opsx/apply 达到实现完成的交接点后（所有任务完成或仅剩用户/外部验证如 SIT/UAT/手动检查），在用户花时间手动验证前运行审查/测试/验证，修复关键问题，仅在所有任务真正完成后归档。不在普通实现中途暂停时触发。 |
| `robot-aiot-adr-confluence` | `robot-aiot-adr-confluence` | 技术方案文档端到端工作流：信息评估→按需需求收敛/追问澄清/方案比较→生成 ADR/技术提案/决策简报，需要时发布到 Confluence。适用于写技术方案、生成 ADR、输出技术提案、写决策简报、架构决策记录发 Confluence、方案归档到 Confluence、技术选型文档输出等场景。仅需文档可停在 Markdown 草稿；明确要求发布才进入 Confluence 阶段。 |
| `robot-aiot-adr-generator` | `robot-aiot-adr-generator` | 生成并校验 ADR 架构决策记录：根据业务/技术需求产出标准 ADR 文档，按需对关键技术断言执行验证链核查。适用于生成 ADR、写架构决策记录、输出技术选型归档、ADR 发布前审稿等场景。 |
| `robot-aiot-commit` | `robot-aiot-commit` | 为本项目生成统一格式中文提交说明，并在用户明确要求时配合 Git 提交流程执行 commit。适用于生成 commit message、按规范提交、总结 diff、写提交说明、提交代码、根据分支提取 JIRA、按 FEAT/FIX/ENH/DOC/CHORE 分类提交等场景。 |
| `robot-aiot-docs-sync` | `robot-aiot-docs-sync` | 扫描当前项目并创建或更新一套可溯源的项目文档：AGENTS.md、README.md、CHANGELOG.md、docs/project-map.md、docs/architecture.md。适用于更新项目文档、同步文档、更新 README/AGENTS.md、生成 changelog/项目地图/架构说明等场景。吸收 changelog、中文文档、README 和 Diataxis 文档分层能力，仅在上述 5 个文件内做结构化增强，不修改源代码/配置/测试文件。 |
| `robot-aiot-draw-flowchart` | `robot-aiot-draw-flowchart` | 机器人/IoT 业务图表绘制：三条输出路径（draw.io XML 可编辑主路径、直绘 SVG/HTML 汇报级展示、archify 内置渲染支持主题切换+导出）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑、时间线、Agent/记忆架构等 40+ 图表类型；内置机器人视觉语言、12 套 SVG 风格皮肤与品牌 token 定制、几何/构图校验、PNG/GIF 导出与 drawio/Mermaid 导入重绘。 |
| `robot-aiot-knowledge-expert` | `robot-aiot-knowledge-expert` | 物联网全栈技术专家回答规范。适用于 IoT/AIOT 架构设计、协议选型、平台集成、边云协同、性能调优、故障排查等问题。触发词：物联网/IoT/AIOT/MQTT/Modbus/BACnet/OPC UA/EMQX/物模型/边云协同/设备影子/OTA/JetLinks/ThingsBoard/感认行。 |
| `robot-aiot-leadership-ppt-workflow` | `robot-aiot-leadership-ppt-workflow` | 将项目数据和技术分析转化为结构化领导汇报 PPT，覆盖五阶段全链路：数据池建立→技术明细版+领导汇报版文档分层→调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML→调用 robot-aiot-xml-html-bridge 将 XML 稳定转 HTML 并保留原样式→调用 robot-aiot-slide-html-author 完成 PPT 母稿逐页 HTML 化→调用 ppt-master 生成最终 PPTX。用户要求写领导汇报 PPT/出 PPT 母稿/做汇报材料/汇报方案/写 PPT/领导汇报/生成汇报 PPT 时触发。 |
| `robot-aiot-self-skill-sync` | `robot-aiot-self-skill-sync` | 批量更新 self 目录下所有 git 项目和外部 skill（npx 管理型 15 个统一更新，失败则本地 git 克隆 rsync 兜底）。递归扫描嵌套 git 仓库，处理网络重试和冲突。~/.agents/ 与 agent-skills/ 只允许新增和修改，禁止删除。文件级同步先比对新旧，严禁旧覆盖新。self-skills/ 与运行时双向同步，commands/ 同理。完成后同步知识库并更新 skills-overview.md。 |
| `robot-aiot-slide-html-author` | `robot-aiot-slide-html-author` | 为领导汇报类 PPT/母稿生成 1920x1080 固定画布的逐页 HTML 页面。引用 ui-ux-pro-max 的设计系统与审查能力，内化语义化设计 token、清晰/克制/层次原则与高级感设计标准（反模板化排版、色彩/形状一致性锁定、AI 痕迹清单、审查修复工作流）。适用于 PPT 母稿转单页 HTML/领导汇报页落成 HTML/逐页生成 slide HTML/给 ppt-master 准备逐页 HTML/修复汇报页布局样式信息层级/把图表 HTML 嵌入汇报页等场景。图表 HTML 有问题时可调用 robot-aiot-xml-html-bridge 审查修复。 |
| `robot-aiot-xml-html-bridge` | `robot-aiot-xml-html-bridge` | 将 robot-aiot-draw-flowchart 或其他 draw.io/mxGraph XML 图表稳定转换为 HTML 预览稿，尽可能保留原始样式/布局/层级/配色/尺寸比例/文本关系。适用于 XML 转 HTML/draw.io 转 HTML/mxGraph 转 HTML/图表转网页预览/先转 HTML 再转 PPT/保留原样式输出 HTML 等场景。也适用于领导汇报 PPT 工作流中在 PPT 生成前先落一层 HTML 作为页面主约束的场景。 |
| `stock-replay-workbench` | `stock-replay-workbench` | A 股盘后复盘工作台：收盘简报、主线题材梳理、强势股/观察池、个股走强原因、题材资金联动、龙虎榜/公告/研报/财务交叉分析。覆盖打板情绪、ETF 期权、舆情互动。多股对比通过 sub-agent 并行编排，深度报告强制 cross-check-reviewer 复查。 |
