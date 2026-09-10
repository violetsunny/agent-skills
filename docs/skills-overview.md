# 技能总览

本文档汇总三个技能目录：`~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/`，根据各目录下实际存在的 `SKILL.md` 递归生成。技能名称优先读取 frontmatter `name`（缺失回退目录名）；说明为基于原始 `description` 提炼的中文摘要（≤500 字，简洁概括用途与触发场景）。

## 第一部分：`~/.agents/skills/`

扫描目录：`/Users/kangll13/.agents/skills/`（运行时技能目录）

共 **111** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `academy-guide` | `academy-guide` | 回答关于如何使用 Claude 或其产品的问题前，先查阅本 skill——它推荐 Claude Academy（academy.claude.com，Anthropic 学习中心）的匹配课程、教程和用例。触发：how do I、getting started with、what can Claude do、teach me、learn to use；关于 artifacts、projects、skills、plugins、connectors、MCP 的问题；团队/班级/组织推广 Claude 的请求；索要培训材料、上手内容或学习资源。适用于用户在学习功能用法时，而非任务进行中只想完成任务。可与其他 skill 组合：查阅产品文档回答功能原理后，也来这里找匹配课程，文档答案与 Academy 推荐应一起给出。仅在强匹配时推荐，绝不编造 Academy 内容。 |
| `algorithmic-art` | `algorithmic-art` | 用 p5.js 创作算法艺术，支持种子随机和交互式参数探索。当用户要求用代码创作艺术、生成艺术、算法艺术、流场或粒子系统时使用；创作原创算法艺术，不抄袭现有艺术家作品以避免版权问题。 |
| `api-contract-review` | `api-contract-review` | 审查 REST API 契约：HTTP 语义、版本管理、向后兼容性和响应一致性。适用于用户说 review API、check endpoints、REST review，或 API 变更发布前。 |
| `api-tester` | `api-tester` | 依据真实 OpenAPI、路由实现和现有测试生成并验证 API 测试。用于用户要求测试接口、补集成测试、验证 API 契约、生成回归用例或排查接口兼容性时；区分"生成测试"和"执行请求"的授权，不猜测状态码、响应结构或 SLA，不在未确认环境中发送写请求。 |
| `archify` | `robot-aiot-draw-flowchart/archify` | 创建精致且经过校验的架构图、工作流图、时序图、数据流图和生命周期/状态图，输出为可交互的独立 HTML（内联 SVG），支持深色/浅色主题、可选轨迹动画，以及 PNG/JPEG/WebP/SVG/WebM 导出。接受自然语言需求或粘贴的 Mermaid flowchart、sequenceDiagram、stateDiagram 输入；图表需反映真实代码时会检查仓库证据。适用于用户要求可视化系统架构、基础设施、云/安全/网络拓扑、技术工作流、API 调用时序、请求生命周期、数据管道、ETL/ELT、数据血缘、状态机，或转换/美化 Mermaid 时。 |
| `architecture-review` | `architecture-review` | 从宏观层面分析 Java 项目架构：包结构、模块边界、依赖方向、分层。当用户要求 review architecture、check structure、package organization，或评估代码库是否遵循 clean architecture 原则时使用。 |
| `ask-matt` | `ask-matt` | 询问哪个 skill 或流程适合当前情况，是本仓库 skills 的路由器。适用于不确定该用哪个 skill 时。 |
| `banner-design` | `banner-design` | 为社交媒体、广告、网站主视觉、创意素材和印刷品设计 Banner，提供多种艺术方向选项，可用生成或用户提供的视觉素材。动作：设计、创建、生成 Banner。平台：Facebook、Twitter/X、LinkedIn、YouTube、Instagram、Google Display、网站 Hero 区、印刷品。风格：极简、渐变、粗体排版、照片、插画、几何、复古、玻璃拟态、3D、霓虹、双色调、编辑风、拼贴。 |
| `baoyu-image-gen` | `baoyu-image-gen` | AI 图像生成，支持 OpenAI GPT Image 2.5、Azure OpenAI、Google、OpenRouter、DashScope、Z.AI GLM-Image、MiniMax、Jimeng、Seedream、Replicate 和 Agnes 等 API。支持文生图、参考图、宽高比设置和从已保存 prompt 文件批量生成。默认顺序生成；当用户已有多个 prompt 或需要稳定的多图吞吐时用并行批量生成。当用户要求生成、创建或绘制图像时使用。 |
| `brand` | `brand` | 品牌语音、视觉标识、信息框架、资产管理和品牌一致性。适用于品牌化内容、语气风格、营销素材、品牌合规、风格指南等场景。 |
| `brand-guidelines` | `brand-guidelines` | 把 Anthropic 官方品牌色和字体应用到各类产出物，使其具备 Anthropic 视觉风格。当涉及品牌色、样式指南、视觉格式化或公司设计标准时使用。 |
| `canvas-design` | `canvas-design` | 运用设计理念创作精美的视觉艺术，输出 .png 和 .pdf 文档。当用户要求创建海报、艺术作品、设计稿或其他静态作品时使用；创作原创视觉设计，不抄袭现有艺术家作品以避免版权问题。 |
| `changelog-generator` | `changelog-generator` | 从 git 提交生成 changelog。当用户说"generate changelog""update changelog""what changed since last release"，或准备新版本发布前使用。 |
| `claude-handoff` | `claude-handoff` | 把当前对话交接给一个全新的后台 agent，由其立即接手继续工作。 |
| `clean-code` | `clean-code` | Clean Code 原则（DRY、KISS、YAGNI）、命名、函数设计与可读性。适用于代码难读、方法过长、命名不清、重复代码或嵌套过深时。类职责划分与依赖方向问题请改用 solid-principles。 |
| `code-review` | `code-review` | 从固定基点（commit、分支、tag 或 merge-base）开始审查变更，沿两条轴线：Standards（代码是否遵循仓库成文编码规范）和 Spec（代码是否符合原始 issue/规格要求）。两个审查在并行子 agent 中运行并排汇报。适用于用户想审查分支、PR、进行中的改动，或说 review since X 时。 |
| `codebase-design` | `codebase-design` | 设计深模块（deep module）的共享词汇。当用户想设计或改进模块接口、寻找深化机会、决定 seam 的位置、让代码更可测试或更易被 AI 导航，或其他 skill 需要深模块词汇时使用。 |
| `concurrency-review` | `concurrency-review` | 审查 Java 并发代码的线程安全、竞态条件、死锁及现代模式（Virtual Threads、CompletableFuture、@Async）。当用户说"check thread safety""concurrency review""async code review"，或审查多线程代码时使用。 |
| `design` | `design` | 综合设计技能：品牌标识、设计 token、UI 样式、Logo 生成（55 种风格，支持 Gemini、Atlas Cloud 或 MuAPI AI）、企业形象 CIP（50 项交付物与样机）、HTML 演示文稿（Chart.js）、Banner 设计（22 种风格，覆盖社交/广告/网页/印刷）、图标设计（15 种风格，SVG，Gemini 3.1 Pro）、社交图片（HTML 转截图，多平台）。动作包括设计 Logo、创建 CIP、生成样机、制作幻灯片、设计 Banner、生成图标、创建社交媒体图片、品牌标识与设计系统。平台覆盖 Facebook、Twitter、LinkedIn、YouTube、Instagram、Pinterest、TikTok、Threads、Google Ads。 |
| `design-patterns` | `design-patterns` | 常见设计模式及 Java 示例（Factory、Builder、Strategy、Observer、Decorator 等）。当用户说"implement pattern""use factory""strategy pattern"，或设计可扩展组件时使用。 |
| `design-system` | `design-system` | 设计 token 架构、组件规格与幻灯片生成：三层 token（primitive→semantic→component）、CSS 变量、间距/字体比例、组件规范、策略性幻灯片制作。用于设计 token、系统化设计、符合品牌规范的演示文稿。 |
| `dev-paradigm-matt` | `dev-paradigm-matt` | 面向日常工程开发的分层工作流路由 skill：按任务所处阶段，把需求澄清、规格设计、架构规划、实现、调试、审查、交接和长期维护路由到合适的 matt-skills，而非强迫所有任务走同一条固定流水线。适用于"这个需求该怎么推进""从需求到代码怎么分阶段""该先 grill 还是 to-spec""Bug/重构/新功能分别怎么走""完整开发流程怎么编排""开发范式""dev-paradigm-matt"（曾用名 dev-paradigm）等场景；也是接手陌生项目时先做 setup、领域建模、票据拆分、实现收尾或长期维护规划的统一入口。 |
| `diagnosing-bugs` | `diagnosing-bugs` | 疑难 bug 和性能回归的诊断循环。适用于用户说 diagnose、debug this，或报告某功能损坏/抛异常/失败/变慢时。 |
| `discernment-nudge` | `discernment-nudge` | 在给出用户可能据以行动的实质性回答或草稿（建议、目标/计划/提案/邮件等草稿、估算、数据分析、事实断言、多步论证）之后、最终定稿之前调用：若适用，追加 2-3 个简短的跟进问题，每个都针对刚产出内容中的具体点，帮助用户核查关键事实、审视推理假设、发现缺失上下文。每次对话最多用一次。琐碎操作类问题、纯教学解释、格式转换、用户自己运行的代码、创意写作或闲聊、用户已要求复核/引用/审查时跳过。 |
| `doc-coauthoring` | `doc-coauthoring` | 引导用户通过结构化工作流共同撰写文档。适用于写文档、提案、技术规格、决策文档等结构化内容；帮助高效传递上下文、迭代打磨内容并验证文档对读者有效。用户提到写文档、创建提案、起草规格等任务时触发。 |
| `docx` | `docx` | 创建、读取、编辑或操作 Word 文档（.docx）和 Word 模板（.dotx）。触发词：Word doc、.docx、.dotx，或要求生成带目录、标题、页码、信头等格式的专业文档；也适用于提取/重组文档内容、插入替换图片、查找替换、处理修订和批注、把内容转成精排 Word 文档。用户要 Word 格式的 report、memo、letter、template 等交付物时使用。不适用于 PDF、电子表格、Google Docs 或与文档生成无关的编码任务。 |
| `domain-modeling` | `domain-modeling` | 构建并打磨项目的领域模型。适用于讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 架构决策记录等场景。 |
| `frontend-design` | `frontend-design` | 在构建新 UI 或重塑现有 UI 时，提供独特、有意图的视觉设计指导。帮助确定美学方向、字体排印，做出不像模板默认值的设计选择。 |
| `git-commit` | `git-commit` | 为 Java 项目生成规范化 commit 提交说明。适用于用户说 commit、create commit、commit changes，或代码改动完成需要提交时。 |
| `git-guardrails-claude-code` | `git-guardrails-claude-code` | 配置 Claude Code 钩子，在执行前拦截危险 git 命令（push、reset --hard、clean、branch -D 等）。适用于用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中拦截 git push/reset 时。 |
| `grill-me` | `grill-me` | 通过不留情面的连续追问，打磨计划或设计方案。 |
| `grill-with-docs` | `grill-with-docs` | 通过不留情面的访谈式追问打磨计划或设计，过程中同步产出文档（ADR 和术语表）。 |
| `grilling` | `grilling` | 就某个计划、决策或想法对用户进行不留情面的追问。当用户想对自己的思路做压力测试，或使用任何 grill 触发短语时使用。 |
| `handoff` | `handoff` | 把当前对话压缩成交接文档，供另一个 agent 接手继续工作。适用于会话过长需要转移上下文时。 |
| `humanizer` | `humanizer` | 在不改变原意的前提下，把 AI 腔文本改写为像作者本人写的。用于编辑或审查文章中的 AI 痕迹：not-X-but-Y 对比、一句话收尾、程式化开场、强行三段排比、满篇破折号、夸大表述、营销话术、AI 高频词、加粗标签或填充词。基于 Wikipedia 的 Signs of AI writing。 |
| `implement` | `implement` | 基于 spec 或一组 ticket 实现一项工作。 |
| `implement-spec` | `implement-spec` | 把一份规格说明（specification）实现为代码。 |
| `improve-codebase-architecture` | `improve-codebase-architecture` | 扫描代码库找出可做深模块化改进的机会，以可视化 HTML 报告呈现，然后针对用户选中的那一项进行连环追问打磨。适用于想系统性改进代码库架构时。 |
| `internal-comms` | `internal-comms` | 一套帮助撰写各类内部沟通材料的资源，采用公司惯用格式。当被要求写内部沟通内容时使用：状态报告、领导层更新、3P 更新、公司简报、FAQ、事故报告、项目进展等。 |
| `issue-triage` | `issue-triage` | 对 GitHub issue 做分诊并打优先级标签。当用户说"triage issues""check issues""review open issues"，或例行维护 GitHub issue 积压时使用。 |
| `java-code-review` | `java-code-review` | Java 系统化代码审查：空指针安全、异常处理、并发、性能检查。当用户说 review code、check this PR、code review，或合并变更前使用。 |
| `java-migration` | `java-migration` | Java 大版本升级指南（8→11→17→21→25）。当用户说 upgrade Java、migrate to Java 25、update Java version，或需要现代化改造遗留项目时使用。 |
| `jpa-patterns` | `jpa-patterns` | JPA/Hibernate 模式与常见陷阱（N+1、懒加载、事务、查询）。当用户遇到 JPA 性能问题、LazyInitializationException，或询问实体关系与抓取策略时使用。 |
| `logging-patterns` | `logging-patterns` | Java 日志最佳实践：SLF4J、结构化日志（JSON）和用于请求追踪的 MDC，包含便于 Claude Code 调试的 AI 友好日志格式。当用户询问日志、调试应用流程或分析日志时使用。 |
| `loop-me` | `loop-me` | 针对用户想在本工作区构建的工作流，就其规格进行连环追问拷问，帮助澄清需求。适用于动手前需要把 spec 问清楚的场景。 |
| `maven-dependency-audit` | `maven-dependency-audit` | 审计 Maven 依赖的过期版本、安全漏洞和冲突。当用户说 check dependencies、audit dependencies、outdated deps，或发布前检查时使用。 |
| `mcp-builder` | `mcp-builder` | 创建高质量 MCP (Model Context Protocol) 服务器的指南，让 LLM 通过良好设计的工具与外部服务交互。构建 MCP 服务器集成外部 API 或服务时使用，支持 Python (FastMCP) 和 Node/TypeScript (MCP SDK)。 |
| `migrate-to-shoehorn` | `migrate-to-shoehorn` | 把测试文件中的 as 类型断言迁移到 @total-typescript/shoehorn。当用户提到 shoehorn、想替换测试里的 as，或需要部分测试数据时使用。 |
| `openspec-apply-change` | `openspec-apply-change` | 实施 OpenSpec change 中的任务。适用于用户想开始实现、继续实现或逐项完成 change 任务时。 |
| `openspec-archive-change` | `openspec-archive-change` | 在实验性工作流中归档已完成的 change。当用户想在实现完成后收尾并归档某个 change 时使用。 |
| `openspec-bulk-archive-change` | `openspec-bulk-archive-change` | 一次性批量归档多个已完成的 change。当需要归档多个并行 change 时使用。 |
| `openspec-continue-change` | `openspec-continue-change` | 通过创建下一个 artifact 来继续推进 OpenSpec change。当用户想推进自己的 change、创建下一个 artifact 或继续工作流时使用。 |
| `openspec-explore` | `openspec-explore` | 进入 OpenSpec 探索模式：作为思考伙伴探索想法、调查问题、澄清需求。适用于用户想在 change 之前或过程中把某件事想清楚时。 |
| `openspec-ff-change` | `openspec-ff-change` | 快速推进 OpenSpec 工件创建。当用户想一次性快速创建实现所需的全部工件、而不逐个走流程时使用。 |
| `openspec-new-change` | `openspec-new-change` | 用实验性 artifact 工作流启动一个新的 OpenSpec change。当用户想以结构化分步方式创建新功能、修复或改动时使用。 |
| `openspec-onboard` | `openspec-onboard` | OpenSpec 引导式入门：带讲解地走完一个完整工作流循环，并在真实代码库中实操。 |
| `openspec-propose` | `openspec-propose` | 一步生成全部 artifact 来提议新 change。当用户想快速描述要构建的内容，并获得包含设计、specs 和任务、可直接进入实现的完整提案时使用。 |
| `openspec-sync-specs` | `openspec-sync-specs` | 把 change 中的 delta specs 同步到主 specs。当用户想用 delta spec 的变更更新主 specs、但不归档该 change 时使用。 |
| `openspec-update-change` | `openspec-update-change` | 更新 OpenSpec change：修订其现有规划 artifact 并保持彼此一致。当用户想修改某个 change 的计划、把新决策并入其中，或编辑后对齐各 artifact 时使用。绝不修改代码。 |
| `openspec-verify-change` | `openspec-verify-change` | 验证实现与 OpenSpec change 产物一致。适用于用户想在归档前确认实现完整、正确、连贯时。 |
| `opsx-workflow-hooks` | `opsx-workflow-hooks` | opsx 工作流的命令后钩子。触发 A：/opsx/propose 生成全部 artifact 后立即进入迭代打磨循环，询问用户是否有新想法并更新提案 artifact，直到用户满意；非平凡的 artifact 分析或起草用全新 sub agent，再回主线程验证并呈现结果。触发 B：/opsx/apply 到达实现完成交接点（所有任务完成，或仅剩 SIT/UAT/人工检查等用户侧验证）时，在用户花时间人工验证前先跑审查/测试/验证，修复关键问题，仅在所有任务真正完成时才归档；审查验证尽量在干净 sub agent 中跑，再回主线程做决策、修复和归档。普通实现中途暂停不触发。适用于"/opsx/propose is done""proposal artifacts created""all tasks complete after apply""apply finished""implementation complete"等场景。 |
| `pdf` | `pdf` | 用户想对 PDF 文件做任何操作时使用：读取或提取文本/表格、合并多个 PDF、拆分、旋转页面、加水印、创建新 PDF、填写表单、加密/解密、提取图片、对扫描版 PDF 做 OCR 使其可搜索。用户提到 .pdf 文件或要求产出 PDF 时用此 skill。 |
| `performance-smell-detection` | `performance-smell-detection` | 检测 Java 代码层面的潜在性能坏味道：stream、集合、装箱、正则、对象创建。提供的是风险意识而非绝对结论，优化前务必先测量。JPA/数据库性能问题请改用 jpa-patterns。 |
| `ppt-master` | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑 PPTX 与幻灯片、重建页面视觉、创建可复用的 Brand/Style/Layout/Deck 工作区、填充原生 PPTX 模板、增强已完成的 PPTX。当用户要求创建、生成、重建、美化、重设计、模板化、填充或增强 presentation/PPT/PPTX/幻灯片/课件（含添加旁白或动画），或要求制作演示文稿风格的旁白/自播放视频，或提到 ppt-master 时使用。 |
| `pptx` | `pptx` | 只要涉及 .pptx 或 .potx 文件（作为输入、输出或两者）就使用此 skill，包括：创建幻灯片、路演 deck 或演示文稿；读取、解析或提取其中文本（即使内容将用于邮件或摘要等其他用途）；编辑、修改或更新现有演示文稿；合并或拆分幻灯片文件；处理模板（.potx）、版式、演讲者备注或批注。当用户提到"deck""slides""presentation"或引用 .pptx/.potx 文件名时即触发，无论后续打算如何使用内容。 |
| `prototype` | `prototype` | 构建一次性原型来回答设计问题。当用户想快速验证某个状态模型或逻辑是否合理，或探索 UI 应该长什么样时使用。 |
| `refactor-advisor` | `refactor-advisor` | 重构顾问：识别代码坏味道并提供重构方案。适用于需要评估代码质量、找出坏味道并制定重构策略时。 |
| `research` | `research` | 针对问题进行调研，基于高可信度的一手资料来源查证，并把结论写成仓库内的 Markdown 文件。适用于用户想研究某个主题、收集文档或 API 事实，或把查阅资料的工作委托给后台 agent 时。 |
| `resolving-merge-conflicts` | `resolving-merge-conflicts` | 当需要解决正在进行中的 git merge/rebase 冲突时使用。 |
| `retro` | `retro` | 复盘与回顾 skill：把一次开发、排障、交付或协作过程整理成可执行的复盘结论，输出做得好的地方、问题与根因、改进动作和后续跟踪项。用于用户要求"复盘""回顾这次开发""总结问题和经验""postmortem""retrospective""总结这次哪里做得好/不好"等场景；也适用于任务刚完成、需要沉淀流程改进点、防止同类问题再次发生时。 |
| `robot-aiot-adr-confluence` | `robot-aiot-adr-confluence` | 技术方案文档端到端工作流：先做信息评估，再按需做需求收敛、追问澄清和方案比较，最后生成 ADR、技术提案或决策简报，并在需要时发布到 Confluence。适用于"写技术方案""生成 ADR""输出技术提案""写决策简报""架构决策记录发 Confluence""方案归档到 Confluence""技术选型文档输出"等场景。用户只要文档时可停在 Markdown 草稿；明确要求发布时才进入 Confluence 发布阶段。 |
| `robot-aiot-adr-generator` | `robot-aiot-adr-generator` | 生成并校验 ADR 架构决策记录：先根据业务/技术需求产出标准 ADR 文档，再按需对其中可外部验证的关键技术断言执行验证链核查。适用于生成 ADR、写架构决策记录、输出技术选型归档、ADR 发布前审稿、校验版本/兼容性/性能说法等场景。输出优先服务技术决策归档，而非通用技术文章写作。 |
| `robot-aiot-commit` | `robot-aiot-commit` | 为本项目生成统一格式的中文提交说明，并在用户明确要求时配合 Git 流程执行 commit。适用于生成 commit message、按规范提交、总结 diff、写提交说明、提交代码、根据分支提取 JIRA、按 FEAT/FIX/ENH/DOC/CHORE 分类提交等场景。输出优先服务本项目提交规范，而非通用 Conventional Commits 模板。 |
| `robot-aiot-docs-sync` | `robot-aiot-docs-sync` | 扫描当前项目并创建或更新一套可溯源的项目文档：AGENTS.md、README.md、CHANGELOG.md、docs/project-map.md、docs/architecture.md。适用于"更新项目文档""同步文档""更新 README""更新 AGENTS.md""生成 changelog""生成项目地图""补齐架构说明"等场景。吸收 changelog、中文文档、README 和 Diataxis 文档分层能力，仅在上述 5 个文件内做结构化增强，不修改源代码、配置文件或测试文件。 |
| `robot-aiot-draw-flowchart` | `robot-aiot-draw-flowchart` | 机器人/IoT 业务图表绘制能力。三条输出路径：draw.io XML（可编辑主路径）、直绘 SVG/HTML（汇报级展示）、archify 内置渲染（主题切换+导出）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑、时间线、Agent/记忆架构等 40+ 图表类型；内置机器人视觉语言、12 套 SVG 风格皮肤与品牌 token 定制、几何/构图校验、PNG/GIF 导出与 drawio/Mermaid 导入重绘。 |
| `robot-aiot-knowledge-expert` | `robot-aiot-knowledge-expert` | 物联网全栈技术专家回答规范。当用户问 IoT/AIOT 架构设计、协议选型、平台集成、边云协同、性能调优、故障排查等问题时使用。触发词包括：物联网、IoT、AIOT、MQTT、Modbus、BACnet、OPC UA、EMQX、物模型、边云协同、设备影子、OTA、JetLinks、ThingsBoard、感认行。 |
| `robot-aiot-leadership-ppt-workflow` | `robot-aiot-leadership-ppt-workflow` | 将项目数据和技术分析转化为结构化的领导汇报 PPT，覆盖全链路五阶段工作流：建立数据池 → 技术明细版+领导汇报版文档分层 → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML → 调用 robot-aiot-xml-html-bridge 将 XML 稳定转 HTML 并保留原样式 → 调用 robot-aiot-slide-html-author 完成 PPT 母稿逐页 HTML 化 → 调用 ppt-master 依据每页 HTML 样式生成最终 PPTX。当用户要求"写领导汇报PPT""出PPT母稿""做汇报材料""汇报方案""写PPT""领导汇报""生成汇报PPT"时触发；也适用于需要把技术项目数据转化为管理层可读汇报格式的场景。 |
| `robot-aiot-self-skill-sync` | `robot-aiot-self-skill-sync` | 批量同步 self 目录下所有 git 项目与 skill 库。模块 1 递归三层扫描嵌套 git 仓库批量更新，处理网络重试与冲突；模块 2 管理 OpenSpec：运行 openspec init/update，把 opsx/ 命令与 openspec-* skills 同步到 ~/.agents；模块 3 外部 skill 为 npx 管理型（superpowers 等 7 个），用 npx skills@latest update 更新，失败按本地克隆 rsync 兜底；模块 3.3/3.4 对 self-skills/ 自写 skill 与命令按文件级比对双向同步（真源新则部署，运行时新则回写），只更新不新增；模块 4 把 ~/.agents/skills/ 同步到个人知识库（排除自写）；模块 5 更新 docs/skills-overview.md。核心原则：只增改不删除；同步先比对内容+mtime，严禁旧覆盖新，目标端更新标 [NEWER-TARGET] 跳过；用户维护的代码禁止回滚或自动冲突处理，异常直接提示并跳过。 |
| `robot-aiot-slide-html-author` | `robot-aiot-slide-html-author` | 为领导汇报类 PPT/母稿生成固定画布（1920x1080）的逐页 HTML：执行时引用 ui-ux-pro-max 的设计系统与审查能力，内化语义化设计 token、清晰/克制/层次原则与高级感标准（反模板化排版、色彩/形状一致性锁定、AI 痕迹清单、审查修复工作流）。适用于 PPT 母稿转单页 HTML、领导汇报页落成 HTML、逐页生成 slide HTML、给 ppt-master 准备逐页 HTML、修复汇报页布局/样式/信息层级、把图表 HTML 嵌入汇报页；也适用于已有 Markdown 母稿、页面草图或图表 HTML、需保持图表真源与页面视觉体系一致的任务。图表 HTML 有问题时可调用 robot-aiot-xml-html-bridge 审查修复。 |
| `robot-aiot-xml-html-bridge` | `robot-aiot-xml-html-bridge` | 把 robot-aiot-draw-flowchart 或其他 draw.io / mxGraph XML 图表稳定转换为 HTML 预览稿，尽可能保留原始样式、布局、层级、配色、尺寸比例与文本关系。触发：XML转HTML、draw.io转HTML、mxGraph转HTML、图表转网页预览、先转HTML再转PPT、保留原样式输出HTML。也适用于领导汇报 PPT 工作流中，在 PPT 生成前先落一层 HTML 作为页面主约束的场景。 |
| `scaffold-exercises` | `scaffold-exercises` | 创建练习目录结构，包含章节、题目、答案和讲解，且能通过 lint。当用户想搭建练习脚手架、创建练习模板或建立新课程章节时使用。 |
| `security-audit` | `security-audit` | Java 安全检查清单，覆盖 OWASP Top 10、输入校验、注入防护和安全编码，适用于 Spring、Quarkus、Jakarta EE 和纯 Java。当审查代码安全性、发布前检查，或用户询问漏洞时使用。 |
| `setup-matt-pocock-skills` | `setup-matt-pocock-skills` | 为本仓库配置工程类 skills 的运行环境：设置 issue 跟踪器、triage 标签词汇和领域文档布局。在首次使用其他工程 skills 之前运行一次。 |
| `setup-pre-commit` | `setup-pre-commit` | 在当前仓库配置 Husky pre-commit 钩子，集成 lint-staged（Prettier）、类型检查和测试。适用于用户想添加 pre-commit 钩子、配置 Husky 或 lint-staged、在提交时执行格式化/类型检查/测试时。 |
| `setup-ts-deep-modules` | `setup-ts-deep-modules` | 在 TypeScript 仓库中接入 dependency-cruiser，让每个 package 成为深模块：实现隐藏在子文件夹中，只能通过入口文件访问。由用户主动调用。 |
| `skill-creator` | `skill-creator` | 创建新 skill、修改和改进现有 skill、度量 skill 性能。当用户想从零创建 skill、编辑或优化现有 skill、运行 evals 测试 skill、做基准测试和方差分析，或优化 skill 描述以提高触发准确度时使用。 |
| `slack-gif-creator` | `slack-gif-creator` | 创建针对 Slack 优化的动画 GIF 的知识和工具，提供尺寸约束、校验工具和动画概念。当用户要求制作 Slack 用动画 GIF（如"make me a GIF of X doing Y for Slack"）时使用。 |
| `slides` | `slides` | 创建有策略性的 HTML 演示文稿，涵盖 Chart.js 图表、design tokens、响应式布局、文案公式和按上下文选择的幻灯片策略。 |
| `solid-principles` | `solid-principles` | SOLID 原则检查清单，附 Java 示例。适用于类职责过多、抽象泄漏、依赖方向错误，以及用户询问单一职责、开闭、里氏替换、接口隔离或依赖倒置原则时。命名、重复和方法长度问题请改用 clean-code。 |
| `spring-boot-patterns` | `spring-boot-patterns` | Spring Boot 最佳实践与模式。适用于创建 controller、service、repository，或用户询问 Spring Boot 分层、装配、配置、异常处理时。JPA 和 Hibernate 行为请改用 jpa-patterns。 |
| `tdd` | `tdd` | 测试驱动开发。当用户想以测试先行的方式开发功能或修 bug、提到 red-green-refactor，或需要集成测试时使用。 |
| `teach` | `teach` | 在当前工作区内教用户一项新技能或新概念。 |
| `test-quality` | `test-quality` | 用 AssertJ 断言编写高质量 JUnit 5 测试。适用于用户说 add tests、write tests、improve test coverage，或为 Java 代码审查/创建测试类时。 |
| `theme-factory` | `theme-factory` | 为产物（幻灯片、文档、报告、HTML 落地页等）套用主题样式的工具包。内置 10 套预设主题（配色/字体），可应用到任何已创建的产物，也可即时生成新主题。 |
| `to-questionnaire` | `to-questionnaire` | 把自己无法完全回答的决策转化为问卷，交给他人填写。适用于需要向干系人收集信息以推进决策时。 |
| `to-spec` | `to-spec` | 把当前对话整理成 spec 并发布到项目 issue tracker；不做额外访谈，只综合已讨论的内容。 |
| `to-tickets` | `to-tickets` | 把计划、规格或当前对话拆解为一组曳光弹式工单，每个工单声明其阻塞依赖边，并发布到配置的跟踪器（本地模式为每工单一个文件、依赖边写成文本；真实跟踪器则用原生 blocking 链接）。 |
| `triage` | `triage` | 让 issue 和外部 PR 经过一套 triage 角色状态机流转：分类、验证、必要时质询打磨，并产出 agent 可直接执行的 brief。 |
| `ui-styling` | `ui-styling` | 用 shadcn/ui 组件（基于 Radix UI + Tailwind）、Tailwind CSS 原子化样式和 canvas 视觉设计创建美观、无障碍的用户界面。适用于构建 UI、实现设计系统、创建响应式布局、添加无障碍组件（对话框、下拉菜单、表单、表格）、定制主题配色、实现深色模式、生成视觉设计和海报，或建立跨应用一致的样式规范。 |
| `ui-ux-pro-max` | `ui-ux-pro-max` | 面向 Web、移动端和桌面的 UI/UX 设计智能库。适用于设计、构建、审查或修复界面，涵盖页面、组件、设计系统、无障碍、交互、响应式布局、排版、配色、图表和技术栈相关的 UI 实现。内置可搜索的本地数据：79 种风格（50 种启用）、192 套产品配色与推理档案、74 组字体搭配、119 条 UX 准则、105 个图标、17 个 GSAP 预设、25 种图表类型、22 个技术栈。 |
| `wait-what` | `wait-what` | 叫停信号：上一条消息没有传达清楚，需要重新表述。适用于用户表示没看懂、困惑或信息未落地时。 |
| `wayfinder` | `wayfinder` | 把超出单个 agent 会话容量的大型工作规划为 issue 跟踪器上的决策工单共享地图，逐个解决，直到通往目标的路径清晰。适用于规模过大、需要先拆解决策再执行的项目规划。 |
| `web-artifacts-builder` | `web-artifacts-builder` | 用现代前端技术（React、Tailwind CSS、shadcn/ui）创建复杂多组件 claude.ai HTML artifacts 的工具套件。用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifact；简单单文件 HTML/JSX artifact 不适用。 |
| `webapp-testing` | `webapp-testing` | 用 Playwright 交互和测试本地 Web 应用的工具集。支持验证前端功能、调试 UI 行为、截取浏览器截图和查看浏览器日志。 |
| `wizard` | `wizard` | 生成交互式 bash 向导，引导人类完成只有人能执行的步骤。适用于基础设施开通、配置凭据或 CI secret、操作不熟悉的第三方控制台、执行一次性迁移或切换。agent 自己能完成的步骤不要调用此 skill。 |
| `writing-beats` | `writing-beats` | 写作技法（exploit 方向）：把原始素材组织成 beats 旅程，在每个 beat 依赖某术语之前先铺垫解释该术语。 |
| `writing-for-agents` | `writing-for-agents` | 为 agent 编写文档的规范。适用于创建或编辑 skill，或修改 AGENTS.md、CLAUDE.md 时。 |
| `writing-fragments` | `writing-fragments` | 写作探索阶段：挖掘原始素材片段，尚不做结构化。 |
| `writing-shape` | `writing-shape` | 写作利用阶段：把原始素材逐段塑造成文章。 |
| `xlsx` | `xlsx` | 凡以电子表格文件为主要输入或输出的任务都用此 skill：打开、读取、编辑或修复现有 .xlsx、.xlsm、.xltx、.csv、.tsv 文件（加列、算公式、格式化、做图表、清洗脏数据）；从零或其他数据源创建新表格；表格格式互转。用户按名称或路径提到表格文件（哪怕随口说"下载目录里的 xlsx"）并要求处理或产出时尤其要触发；也适用于把杂乱表格数据（畸形行、错位表头、垃圾数据）清洗重构为规范表格。交付物必须是电子表格文件。主要交付物是 Word 文档、HTML 报告、独立 Python 脚本、数据库管道或 Google Sheets API 集成时不触发，即使涉及表格数据。 |
| `zh-code-reviewer` | `zh-code-reviewer` | 中文代码审查专家：生成详细的中文代码审查报告。适用于需要中文输出的代码评审场景。 |

## 第二部分：`agent-skills/skills/`

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`（外部 skill 副本库）

共 **665** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `a-stock-data` | `a-stock-data` | 需要写代码实际获取 A 股数据时使用：行情/K线（mootdx+腾讯+百度）、研报（东财+同花顺+iwencai）、信号（热点/北向/龙虎榜/解禁/行业）、资金面（融资融券/大宗/股东户数/分红/资金流）、新闻、财务三表/F10、公告（巨潮）、打板（涨停池/连板/炸板率/重点监控池/日内异动）、ETF期权（T型报价/希腊字母/IV）、舆情互动（互动易/热榜/人气榜）、筹码分布、复权因子、估值历史（PE/PB/PS+换手率+ST）、申万行业变迁史、宏观（社融/PMI）。十一层数据源、54 端点（含 3 官方备胎）、内嵌全部可运行代码，自包含零外部依赖；优先通达信（mootdx）/腾讯（不封 IP），东财接口内置限流防封，主源被封可查「备用源速查」降级。仅取数时加载：A股概念解释、投资观点讨论、策略问答等无需取数的话题不要用本 skill。 |
| `academy-guide` | `academy-guide` | 回答关于如何使用 Claude 或其产品的问题前，先查阅本 skill——它推荐 Claude Academy（academy.claude.com，Anthropic 学习中心）的匹配课程、教程和用例。触发：how do I、getting started with、what can Claude do、teach me、learn to use；关于 artifacts、projects、skills、plugins、connectors、MCP 的问题；团队/班级/组织推广 Claude 的请求；索要培训材料、上手内容或学习资源。适用于用户在学习功能用法时，而非任务进行中只想完成任务。可与其他 skill 组合：查阅产品文档回答功能原理后，也来这里找匹配课程，文档答案与 Academy 推荐应一起给出。仅在强匹配时推荐，绝不编造 Academy 内容。 |
| `accessibility` | `accessibility` | 基于 WCAG 2.2 Level AA 设计、实现和审计包容性数字产品。构建或审计须满足 WCAG 2.2 AA 的 UI，或审查改动的键盘、对比度、屏幕阅读器支持时使用；可为 Web 生成语义化 ARIA，为 Web 和原生平台（iOS/Android）生成无障碍 trait。 |
| `adaptyv` | `adaptyv` | Adaptyv Bio Foundry API 与 Python SDK 的使用方法：蛋白质实验设计、提交和结果获取。当用户提到 Adaptyv、Foundry API、蛋白结合实验、蛋白筛选实验、BLI/SPR 实验、热稳定性实验，或想提交蛋白序列做实验表征时触发；代码 import adaptyv、adaptyv_sdk、FoundryClient 或引用 foundry-api-public.adaptyvbio.com 时也触发。 |
| `aeon` | `aeon` | 时间序列机器学习任务：分类、回归、聚类、预测、异常检测、分割和相似性搜索。处理时序数据、序列模式或时间索引观测且需要超越标准 ML 方法的专门算法时使用；尤其适合单变量与多变量时间序列分析，API 兼容 scikit-learn。 |
| `agent-reach` | `agent-reach` | 用户想在互联网上调研/research/搜索/查/找内容时必须使用，如全网调研 X、查一下 X、看看大家怎么评价 X、research this topic；提到任何平台或分享 URL 时也必须使用：小红书/xhs、Twitter/推特/X、B站/bilibili、Reddit、Facebook、Instagram、V2EX、LinkedIn/领英/求职、YouTube、GitHub 代码搜索、小宇宙播客、雪球/股票行情、RSS 或任意网页链接。覆盖 15 个平台，多后端路由（OpenCLI / 各平台 CLI / API），6 渠道零配置；agent-reach doctor --json 可查看各平台当前后端。不适用于：写报告/数据分析/翻译等内容加工（只负责获取内容）；发帖/评论/点赞等写操作；已有专门 skill 的平台。SKILL.md 含路由表和常用命令，复杂场景按需读对应分类 references/*.md；分类：search / social / career / dev / web / video / finance。 |
| `agent-tui` | `agent-tui` | 主 agent 不要直接使用此 skill；如需测试 TUI 应调用 tui_tester 子代理。以编程方式驱动终端 UI（TUI）应用，用于测试、自动化和检查。适用于：自动化 CLI/TUI 交互、终端应用回归测试、验证交互行为；用户询问 agent-tui 是什么、能做什么、要求演示或想看实际效果时也触发。 |
| `ai-video-script` | `ai-video-script` | AI 视频脚本生成器：根据主题/关键词生成完整视频脚本，含分镜描述、画面提示词、配音文案；适用于短视频创作者、AI 视频制作者、内容营销人员；触发词：视频脚本、分镜、AI视频、短视频文案、视频策划。 |
| `algorithmic-art` | `algorithmic-art` | 用 p5.js 创作算法艺术，支持种子随机和交互式参数探索。当用户要求用代码创作艺术、生成艺术、算法艺术、流场或粒子系统时使用；创作原创算法艺术，不抄袭现有艺术家作品以避免版权问题。 |
| `analytical-method-validation` | `analytical-method-validation` | 在 ICH Q2(R2)/Q14、USP <1220>/<1225>/<1226>、ICH M10 生物分析、CLSI EP 或 ISO/IEC 17025 框架下规划、执行和记录分析方法的验证、确认与转移。适用于 HPLC、LC-MS/MS、GC、CE、ICP-MS、溶出、qNMR、qPCR、NIR、配体结合或细胞实验，凡涉及"方法是否适用于其预期用途"的问题。触发词包括 method validation、AMV、acceptance criteria、linearity、accuracy and precision、repeatability、recovery、LOD、LOQ、specificity、robustness、method transfer、Deming、Passing-Bablok、Bland-Altman、equivalence testing、OOS investigation、ICH Q2/Q14、USP 1225、ISR，以及任何要求证明分析方法有效的请求。 |
| `anndata` | `anndata` | 单细胞分析中标注矩阵的数据结构 AnnData：处理 .h5ad 文件或对接 scverse 生态时使用。本 skill 只管数据格式；分析流程用 scanpy，概率模型用 scvi-tools，群体规模查询用 cellxgene-census。 |
| `api-contract-review` | `api-contract-review` | 审查 REST API 契约：HTTP 语义、版本管理、向后兼容性和响应一致性。适用于用户说 review API、check endpoints、REST review，或 API 变更发布前。 |
| `api-design` | `api-design` | 生产级 REST API 设计模式，含资源命名、状态码、分页、过滤、错误响应、版本化和限流。适用于设计或评审 REST 端点、资源名、状态码、分页或版本化时。 |
| `api-sculptor` | `api-sculptor` | 设计并实现 API：REST、GraphQL、gRPC、WebSocket。产出 OpenAPI 3.1 规范、GraphQL SDL schema、Protocol Buffer 定义和可运行的服务端实现。触发：用户问 API 设计、端点结构、schema 定义、版本策略、分页、认证、限流或任何 API 实现工作，也响应“design an API for”、“write an OpenAPI spec”、“create a GraphQL schema”、“set up gRPC”、“REST API best practices”，以及“I need endpoints for my app”、“how should I structure my API”这类随口请求。 |
| `api-tester` | `api-tester` | 依据真实 OpenAPI、路由实现和现有测试生成并验证 API 测试。用于用户要求测试接口、补集成测试、验证 API 契约、生成回归用例或排查接口兼容性时；区分"生成测试"和"执行请求"的授权，不猜测状态码、响应结构或 SLA，不在未确认环境中发送写请求。 |
| `apple-hig-designer` | `Apple-Hig-Designer` | 按 Human Interface Guidelines 设计 Apple 风格 iOS/macOS 界面：创建符合 HIG 的组件，使用 SF Symbols、San Francisco 字体和正确的无障碍支持，可选现代视觉效果。设计 Apple 风格 UI、iOS/macOS 界面、HIG 合规组件或实现设计系统规范时使用。 |
| `arbor` | `arbor` | 基于 Arbor 论文的 Hypothesis Tree Refinement（HTR）方法，围绕目标函数与评估器自主迭代改进真实产物（代码、训练配方、agent harness、数据管道、prompt），避免过拟合开发集。触发场景：提升模型评测分数、改进 agent/harness、调优管道、超越基准 baseline、多方案搜索择优、MLE-bench/Kaggle 式优化，或任何长周期反复实验-评估、分支探索、担心 dev/test 差距的任务，即使用户未提 Arbor 或 hypothesis tree。以 Claude 为协调者，子 agent 在隔离 git worktree 中执行；独立 arbor CLI 见 references/arbor-upstream.md。 |
| `arboreto` | `arboreto` | 用可扩展算法（GRNBoost2、GENIE3）从基因表达数据推断基因调控网络（GRN）。在分析转录组数据（bulk RNA-seq、单细胞 RNA-seq）以识别转录因子-靶基因关系和调控相互作用时使用，支持大规模数据集的分布式计算。 |
| `archify` | `archify` | 创建精致且经过校验的架构图、工作流图、时序图、数据流图和生命周期/状态图，输出为可交互的独立 HTML（内联 SVG），支持深色/浅色主题、可选轨迹动画，以及 PNG/JPEG/WebP/SVG/WebM 导出。接受自然语言需求或粘贴的 Mermaid flowchart、sequenceDiagram、stateDiagram 输入；图表需反映真实代码时会检查仓库证据。适用于用户要求可视化系统架构、基础设施、云/安全/网络拓扑、技术工作流、API 调用时序、请求生命周期、数据管道、ETL/ELT、数据血缘、状态机，或转换/美化 Mermaid 时。 |
| `architecture-decision-records` | `architecture-decision-records` | 将 Claude Code 会话中的架构决策记录为结构化 ADR：自动识别决策时刻，记录背景、备选方案和理由，维护 ADR 日志，让后续开发者理解代码库为何如此设计。 |
| `architecture-review` | `architecture-review` | 从宏观层面分析 Java 项目架构：包结构、模块边界、依赖方向、分层。当用户要求 review architecture、check structure、package organization，或评估代码库是否遵循 clean architecture 原则时使用。 |
| `article-writing` | `article-writing` | 按给定范例或品牌指引提炼出的独特文风，撰写文章、指南、博客、教程、newsletter 等长文。适用于用户需要超过一段的成稿内容，尤其在意文风一致性、结构和可信度时。 |
| `ask-matt` | `ask-matt` | 询问哪个 skill 或流程适合当前情况，是本仓库 skills 的路由器。适用于不确定该用哪个 skill 时。 |
| `ask-matt` | `engineering/ask-matt` | 询问哪个 skill 或流程适合当前情况，是本仓库 skills 的路由器。适用于不确定该用哪个 skill 时。 |
| `astropy` | `astropy` | 天文学与天体物理工作流的核心 Python 库，涉及 Astropy API：单位/物理量、坐标、FITS I/O、表格、时间系统、WCS 和宇宙学。用 Astropy 实现或调试天文数据分析代码时使用。 |
| `async-pr-review` | `async-pr-review` | 用户想发起异步 PR 审查、对 PR 跑后台检查，或查询此前发起的异步 PR 审查状态时触发本 skill。 |
| `auth-architect` | `auth-architect` | 设计和实现认证与身份系统：OAuth2/OIDC 流程（授权码、PKCE、客户端凭证）、JWT 设计（RS256 vs HS256、密钥轮换、token 黑名单、refresh token 策略）、RBAC 与 ABAC 建模、SSO（Google、GitHub、SAML 2.0）、会话管理、magic link、MFA（TOTP、短信、硬件密钥）和 API key 管理。触发词：implement OAuth2、JWT refresh token rotation、set up SSO with Google、design RBAC for multi-tenant、implement magic link auth、is my JWT secure、add login to my app、session management strategy、API key auth。 |
| `autoplan` | `gstack-autoplan` | 自动评审流水线：从磁盘读取 CEO、design、eng、DX 四个评审 skill 并按序执行，用 6 条决策原则自动决策，把品味类决策（相近方案取舍、边界范围、codex 分歧）留到最终审批门。一条命令产出完整评审过的计划。触发：“auto review”、“autoplan”、“run all reviews”、“review this plan automatically”、“make the decisions for me”；用户已有计划文件又不想回答 15-30 个中间问题时主动建议。语音别名：“auto plan”、“automatic review”。 |
| `autoskill` | `autoskill` | 通过 screenpipe 观察用户屏幕，识别重复出现的科研工作流，与现有 scientific-agent-skills 匹配，为尚未覆盖的模式起草新 skill 或串联现有 skill 的组合配方。触发：用户要求分析近期工作并据实际行为提议 skill。需要本地 3030 端口运行 screenpipe daemon（https://github.com/screenpipe/screenpipe），无其他数据源，连不上就拒绝运行。检测全程本地执行，只有脱敏后的聚类摘要送给 LLM。 |
| `backtest-expert` | `backtest-expert` | 交易系统化回测的专家指导。开发、测试、压力测试或验证量化交易策略时使用。覆盖 beating ideas to death 方法论、参数稳健性测试、滑点建模、偏差防范和回测结果解读。适用于用户询问回测、策略验证、稳健性测试、避免过拟合或系统化交易开发。 |
| `banner-design` | `banner-design` | 为社交媒体、广告、网站首屏、创意素材和印刷品设计横幅，提供多个艺术方向选项并配 AI 生成视觉。动作：设计、创建、生成 banner。平台：Facebook、Twitter/X、LinkedIn、YouTube、Instagram、Google Display、网站首屏、印刷。风格：极简、渐变、粗体排版、照片、插画、几何、复古、玻璃拟态、3D、霓虹、双色调、编辑风、拼贴。调用 ui-ux-pro-max、frontend-design、ai-artist、ai-multimodal 等技能。 |
| `baoyu-article-illustrator` | `baoyu-article-illustrator` | 分析文章结构，识别需要配图的位置，用 Type × Style × Palette 三维方法生成插图。当用户要求 illustrate article、add images、generate images for article 或为文章配图时使用。 |
| `baoyu-comic` | `baoyu-comic` | 知识漫画创作，支持多种画风和基调，创作原创教育漫画，具备详细分镜布局和批量图像生成能力。触发词：知识漫画、教育漫画、biography comic、tutorial comic、Logicomix-style comic。 |
| `baoyu-compress-image` | `baoyu-compress-image` | 压缩图片为 WebP（默认）或 PNG，自动选择压缩工具。触发场景：用户要求 compress image、optimize image、convert to webp 或减小图片文件体积。 |
| `baoyu-cover-image` | `baoyu-cover-image` | 生成文章封面图：按 5 个维度（类型、配色、渲染风格、文字、情绪）组合，含 11 种配色和 7 种渲染风格；支持电影宽幅 2.35:1、宽屏 16:9、方形 1:1。触发：generate cover image、create article cover、make cover、生成封面图。 |
| `baoyu-danger-gemini-web` | `baoyu-danger-gemini-web` | 通过逆向工程的 Gemini Web API 生成图像和文本：支持文本生成、按提示词生成图像、以参考图做视觉输入、多轮对话。触发：其他 skill 需要图像生成后端，或用户要求 generate image with Gemini、Gemini text generation，或需要具备视觉能力的 AI 生成。 |
| `baoyu-danger-x-to-markdown` | `baoyu-danger-x-to-markdown` | 把 X（Twitter）推文和文章转换为带 YAML front matter 的 markdown，使用逆向工程 API，需用户明确同意。触发场景：用户提到 X to markdown、tweet to markdown、save tweet，或提供 x.com/twitter.com 链接要求转换。 |
| `baoyu-diagram` | `baoyu-diagram` | 创建专业深色主题 SVG 图表，任意类型：架构图、流程图、时序图、结构图、思维导图、时间线、示意/概念图等。当用户要求任何技术或概念图表、系统/流程/数据流/组件关系/网络拓扑/决策树/组织架构图/状态机的可视化，或任何结构、逻辑、流程的视觉呈现时使用。用户说画个图、画一个架构图、diagram、flowchart、sequence diagram、draw me a ...，或上传内容要求可视化时也触发。输出始终是独立 .svg 文件。 |
| `baoyu-electron-extract` | `baoyu-electron-extract` | 从任何已安装的 Electron 应用（.asar 包）提取资源和 JavaScript：有 .js.map 时还原原始源码，否则用 Prettier 格式化压缩代码；跳过 node_modules，支持 macOS 和 Windows。触发：extract Electron app、decompile Electron、get the source code of <app>、inspect app.asar、看 Electron 应用源码、提取 .asar，或询问某桌面 Electron 应用如何实现。 |
| `baoyu-format-markdown` | `baoyu-format-markdown` | 为纯文本或 markdown 文件添加格式化：frontmatter、标题、摘要、各级 heading、加粗、列表和代码块。触发场景：用户要求 format markdown、美化文章、添加格式或改进排版。输出到 {filename}-formatted.md。 |
| `baoyu-image-gen` | `baoyu-image-gen` | AI 图像生成，支持 OpenAI GPT Image 2、Azure OpenAI、Google、OpenRouter、DashScope、Z.AI GLM-Image、MiniMax、即梦、Seedream、Replicate 和 Agnes API。支持文生图、参考图、宽高比和从已保存 prompt 文件批量生成。默认顺序生成；用户已有多个 prompt 或需要稳定多图吞吐时用批量并行。当用户要求生成、创建或绘制图像时使用。 |
| `baoyu-infographic` | `baoyu-infographic` | 生成专业信息图，提供 21 种布局和 22 种视觉风格。自动分析内容、推荐布局×风格组合，产出可发布级信息图。当用户要求创建"infographic""信息图""visual summary""可视化"或"高密度信息大图"时使用。 |
| `baoyu-markdown-to-html` | `baoyu-markdown-to-html` | 将 Markdown 转换为带微信兼容主题的样式化 HTML。支持代码高亮、数学公式、Mermaid（经 headless Chrome 渲染为 PNG）、PlantUML、脚注、alerts、信息图，以及外链可选转底部引用。当用户要求 markdown to html、convert md to html、md 转 html、微信外链转底部引用，或需要从 markdown 生成样式化 HTML 时使用。 |
| `baoyu-post-to-wechat` | `baoyu-post-to-wechat` | 通过 API 或 Chrome CDP 发布内容到微信公众号。支持文章发布（HTML、markdown 或纯文本输入）和贴图发布（多图，原称图文）；markdown 文章流程默认把普通外链转为底部引用，输出对微信友好。触发：发布公众号、post to wechat、微信公众号、贴图/图文/文章。 |
| `baoyu-post-to-weibo` | `baoyu-post-to-weibo` | 发布内容到微博。支持含文字、图片、视频的普通博文，以及通过 Chrome CDP 以 Markdown 输入的头条文章。适用于用户要求 post to Weibo、发微博、发布微博、publish to Weibo、share on Weibo、写微博或微博头条文章时。 |
| `baoyu-post-to-x` | `baoyu-post-to-x` | 把内容和文章发布到 X（Twitter）：支持带图片/视频的普通帖子和 X Articles（长文 Markdown）。在 Codex 中，用户明确要求 Codex Chrome 插件/@chrome 时走 Chrome 扩展流程；否则优先用 Chrome Computer Use，仅在允许时回退到真实 Chrome CDP 脚本。触发词：post to X、tweet、publish to Twitter、share on X。 |
| `baoyu-slide-deck` | `baoyu-slide-deck` | 从内容生成专业幻灯片图像：先创建带风格说明的大纲，再逐页生成幻灯片图像。当用户要求 create slides、make a presentation、generate deck、slide deck 或 PPT 时使用。 |
| `baoyu-translate` | `baoyu-translate` | 用户要求翻译时使用，触发词：translate、翻译、精翻、translate article、translate to Chinese、translate to English、改成中文、改成英文、convert to Chinese、localize、本地化、refined translation、精细翻译、proofread translation、快速翻译、快翻、这篇文章翻译一下，或提供带翻译意图的 URL/文件。支持三种模式（quick/normal/refined）和自定义术语表。 |
| `baoyu-url-to-markdown` | `baoyu-url-to-markdown` | 用 baoyu-fetch CLI（Chrome CDP 加站点专用适配器）抓取任意 URL 并转为 markdown；内置 X/Twitter、YouTube 字幕、Hacker News 帖子适配器，通用页面用 Defuddle；通过交互等待模式处理登录/CAPTCHA；适用于用户想把网页保存为 markdown。 |
| `baoyu-wechat-summary` | `baoyu-wechat-summary` | 用本地 wx-cli 二进制把微信群聊精华总结成结构化摘要。默认生成普通版摘要，毒舌（roast）版需显式选择；跨运行维护每群历史（history.json + history-digests.jsonl）、每用户画像和每群事实记忆（memory.md），内置隐私防护。触发：总结群聊、群聊精华、群聊摘要、summarize group chat、group chat digest、提到微信群名加时间范围、帮我看看 XX 群最近聊了什么、XX 群有什么值得看的、回溯画像、初始化画像、backfill profiles；用户说毒舌版、roast 版、再来个毒舌的时追加毒舌版本。 |
| `baoyu-xhs-images` | `baoyu-xhs-images` | 生成信息图卡片系列，含 12 种视觉风格、8 种版式和 3 种配色，把内容拆成 1-10 张卡通风格图片卡片，针对社交媒体互动优化。适用于用户提到小红书图片、小红书种草、小绿书、微信图文、微信贴图、image cards、图片卡片、baoyu-xhs-images，或想要社交媒体信息图系列时。 |
| `baoyu-youtube-transcript` | `baoyu-youtube-transcript` | 按 URL 或视频 ID 下载 YouTube 视频字幕/转录文本和封面图，支持多语言、翻译、章节、说话人识别，缓存原始数据便于快速重新格式化。触发："get YouTube transcript"、"download subtitles"、"get captions"、"YouTube字幕"、"YouTube封面"、"视频封面"、"video thumbnail"，或用户给出 YouTube 链接想提取字幕文本或封面图。 |
| `behavioral-evals` | `behavioral-evals` | 行为评估（behavioral evaluations）的创建、运行、修复和晋升指导。适用于验证 agent 决策逻辑、调试评估失败、调试提示词引导效果、为 workspace 添加回归测试。 |
| `benchling-integration` | `benchling-integration` | Benchling Python SDK 与 REST API 集成：注册实体、库存、ELN 记录、工作流、Benchling Apps 及 Data Warehouse 查询。用 benchling-sdk 或 v2 API 自动化实验室数据时使用。 |
| `benchmark` | `gstack-benchmark` | 用 browse daemon 做性能回归检测：为页面加载时间、Core Web Vitals、资源体积建立基线，在每个 PR 上对比前后变化并跟踪长期性能趋势。触发词：performance、benchmark、page speed、lighthouse、web vitals、bundle size、load time；语音触发：speed test、check performance。(gstack) |
| `benchmark-models` | `gstack-benchmark-models` | gstack skill 的跨模型基准测试：同一 prompt 并行跑 Claude、GPT（经 Codex CLI）和 Gemini，比较延迟、token、成本，可选 LLM judge 评质量，用数据回答哪个模型最适合该 skill。区别于测网页性能的 /benchmark。触发场景：benchmark models、compare models、which model is best for X、跨模型对比、model shootout，含语音转文字别名。（gstack） |
| `bgpt-paper-search` | `bgpt-paper-search` | 通过 BGPT MCP server 搜索科学论文并获取从全文研究中提取的结构化实验数据，每篇论文返回 25+ 字段，包括方法、结果、样本量、质量评分和结论；适用于文献综述、证据综合，以及查找摘要中没有的实验细节。 |
| `bids` | `bids` | 处理 Brain Imaging Data Structure (BIDS) 数据集时使用：组织神经科学与生物医学数据（MRI、EEG、MEG、iEEG、PET、显微成像、NIRS、动作捕捉、EMG、MR 波谱、行为数据），查询 BIDS 布局、校验合规性、DICOM 转 BIDS、编写元数据 sidecar 或创建 BIDS 衍生物。 |
| `biopython` | `biopython` | 综合分子生物学工具包。用于序列操作、文件解析（FASTA/GenBank/PDB）、系统发育和程序化访问 NCBI/PubMed（Bio.Entrez）。最适合批处理、自定义生物信息流水线、BLAST 自动化。快速查询用 gget，多服务集成用 bioservices。 |
| `bioservices` | `bioservices` | 40+ 生物信息学服务的统一 Python 接口，用一致的 API 在单一流程中查询多个数据库（UniProt、KEGG、ChEMBL、Reactome）。最适合跨库分析和跨服务 ID 映射；单库快速查询用 gget，序列/文件操作用 biopython。 |
| `brainstorming` | `brainstorming` | 在任何创造性工作之前必须使用此技能：创建功能、构建组件、添加功能或修改行为。在实现之前先探索用户意图、需求和设计。 |
| `brand` | `brand` | 品牌语音、视觉标识、信息框架、资产管理和品牌一致性。适用于品牌化内容、语气风格、营销素材、品牌合规、风格指南等场景。 |
| `brand-guidelines` | `brand-guidelines` | 把 Anthropic 官方品牌色和字体应用到各类产出物，使其具备 Anthropic 视觉风格。当涉及品牌色、样式指南、视觉格式化或公司设计标准时使用。 |
| `brandkit` | `brandkit` | 高端品牌套件图像生成：制作品牌指南板、logo 系统、identity deck 和视觉世界演示；擅长极简、电影感、编辑风、暗色科技、奢侈、文化、安全、游戏、开发者工具、消费应用等品牌体系；优化 logo 概念设计、精致构图、稀疏排版、强符号意义、高级 mockup、艺术指导图像和灵活网格布局。 |
| `breadth-chart-analyst` | `breadth-chart-analyst` | 分析市场宽度图表，特别是 S&P 500 Breadth Index（基于 200 日均线）和美股上涨股票占比图。触发：用户提供宽度图图片要求分析、请求市场宽度评估、仓位策略建议，或想基于宽度指标理解中期战略与短期战术展望。没有图片时也可直接从公开源抓 CSV 数据分析。分析与输出均用英文。 |
| `breakout-trade-planner` | `breakout-trade-planner` | 从 VCP 筛选器输出生成 Minervini 风格突破交易计划：最坏情况风险计算、组合热度（portfolio heat）管理、Alpaca 兼容订单模板（预挂单用 stop-limit bracket，确认后用 limit bracket）。用户已有 VCP 筛选结果、想要含入场/止损/目标位和仓位大小的可执行交易计划时使用。 |
| `browse` | `gstack-browse` | 用于 QA 测试和站点自测的快速无头浏览器：访问任意 URL、与元素交互、验证页面状态、对比操作前后差异、截取带标注截图、检查响应式布局、测试表单和上传、处理对话框、断言元素状态，单命令约 100ms。需要测试功能、验证部署、自测用户流程或带证据提 bug 时使用；触发语：open in browser、test the site、take a screenshot、dogfood this。(gstack) |
| `browser-qa` | `browser-qa` | 功能部署后使用浏览器自动化进行视觉测试和 UI 交互验证。 |
| `bulk-rnaseq` | `bulk-rnaseq` | 端到端 bulk RNA-seq 编排器：从原始 FASTQ 经 QC 与修剪（FastQC、fastp/Trim Galore）、比对与定量（STAR、Salmon、featureCounts），组装基因级计数矩阵，再交接给差异表达（pydeseq2）、通路/GSEA 富集（pathway-enrichment）和出版级图表（scientific-visualization）。当用户有 bulk RNA-seq 读段或定量输出、想要完整可复现的差异表达流程时使用，如 analyze my RNA-seq、FASTQ to DESeq2、run nf-core/rnaseq、STAR/Salmon quantification、build a counts matrix for DESeq2。在 nf-core/rnaseq（Nextflow）路径与独立 STAR/Salmon 路径间路由，覆盖实验设计、链特异性和 QC 门。单细胞 RNA-seq 请改用 scanpy 技能。 |
| `canary` | `gstack-canary` | 部署后金丝雀监控：用 browse daemon 监视线上应用的控制台错误、性能退化和页面故障；定期截图并与部署前基线对比，异常时告警。触发词：monitor deploy、canary、post-deploy check、watch production、verify deploy。(gstack) |
| `canslim-screener` | `canslim-screener` | 用 William O'Neil 的 CANSLIM 成长股方法论筛选美股。适用于：用户请求 CANSLIM 选股、成长股分析、动量股识别，或想按 O'Neil 投资体系寻找盈利和价格动量强劲的股票。 |
| `canvas-design` | `canvas-design` | 运用设计理念创作精美的视觉艺术，输出 .png 和 .pdf 文档。当用户要求创建海报、艺术作品、设计稿或其他静态作品时使用；创作原创视觉设计，不抄袭现有艺术家作品以避免版权问题。 |
| `careful` | `gstack-careful` | 破坏性命令的安全护栏。在 rm -rf、DROP TABLE、force-push、git reset --hard、kubectl delete 等危险操作前发出警告，用户可逐项覆盖。适用于操作生产环境、调试线上系统、在共享环境中工作。触发：“be careful”、“safety mode”、“prod mode”、“careful mode”。 |
| `cavecrew` | `cavecrew` | 委派 caveman 风格子代理的决策指南。告诉主线程何时生成 cavecrew-investigator（定位代码）、cavecrew-builder（1-2 个文件的编辑）或 cavecrew-reviewer（diff 审查），而不是内联完成工作或使用普通 Explore。子代理输出经 caveman 压缩，注入回主上下文的工具结果小约 60%，长会话中主上下文更持久。触发词：delegate to subagent、use cavecrew、spawn investigator/builder/reviewer、save context、compressed agent output。 |
| `caveman` | `caveman` | 超压缩沟通模式：以穴居人式说话削减 65% 输出 token（实测），同时保持完整技术准确性。支持强度级别：lite、full（默认）、ultra、wenyan-lite、wenyan-full、wenyan-ultra。触发词：caveman mode、talk like caveman、use caveman、less tokens、be brief 或 /caveman；用户要求 token 效率时也会自动触发。 |
| `caveman-commit` | `caveman-commit` | 超压缩 commit 信息生成器：去除噪音同时保留意图与推理，Conventional Commits 格式；主题行不超过 50 字符，仅在 why 不明显时写正文。触发词：write a commit、commit message、generate commit、/commit 或 /caveman-commit；暂存变更时自动触发。 |
| `caveman-compress` | `caveman-compress` | 把自然语言记忆文件（CLAUDE.md、todos、偏好设置）压缩成 caveman 格式以节省输入 token，保留全部技术实质、代码、URL 和结构。压缩版覆盖原文件，人类可读备份存为 FILE.original.md。触发方式：/caveman-compress FILEPATH 或"compress memory file"。 |
| `caveman-discover` | `caveman-discover` | 扫描当前仓库中所有 LLM 调用工作流并逐一打标，让 Caveman Cloud 按实际用途（如 support-reply、nightly-digest）分组统计花费，而非归入匿名桶。触发场景：用户粘贴 Caveman discovery 提示词、说 discover workflows、或要求按工作流拆分 LLM 开销。前提是仓库已通过 Caveman gateway 路由（由 caveman-setup skill 完成）。 |
| `caveman-evidence-review` | `caveman-evidence-review` | 只读审查 Caveman Cloud 证据：成本、Cave Score、Cave Plan、工作流、trace、延迟、错误、压缩、路由、已验证节省。当用户问 Caveman 发现了什么、LLM 开销去向、成本或质量为何变化、哪些工作流需关注，或要求 trace/分析审查时使用。优先用 Caveman MCP 工具，回退到 CLI JSON。 |
| `caveman-explore` | `caveman-explore` | 只读代码库探索器。主动用于冷启动探索、跨文件大范围定位，或直接搜索失败需要找目标位置时。若问题已指明确切文件或符号，或上一轮已给出可用的 file:line 证据则跳过。只返回紧凑的 path:line 引用，其读取和 grep 过程不进入主对话上下文。 |
| `caveman-help` | `caveman-help` | caveman 全部模式、skill 和命令的速查卡，一次性展示，非持久模式。触发：/caveman-help、"caveman help"、"what caveman commands"、"how do I use caveman"。 |
| `caveman-learn` | `caveman-learn` | 完成 Caveman learn 报告的闭环——审查排序后的 token 消耗大户，并在逐项确认同意的前提下应用降成本修复（精简配置、把反复出现的上下文卸载到 cavemem）。适用于用户运行 caveman learn、想降低 agent token 成本、想精简臃肿的 CLAUDE.md、或想把每次会话都重复粘贴的上下文卸载到 cavemem 时。 |
| `caveman-manage` | `caveman-manage` | 检查 Caveman Cloud 受评估门控的实验生命周期，并阻止不安全执行。触发：用户要求启动、批准、取消、晋升或回滚 Caveman 实验，或询问某实验的证据支持什么操作。先读证据；在服务端权威状态转换和证据门控上线前，不执行生命周期变更操作。 |
| `caveman-optimize` | `caveman-optimize` | 把 Caveman 只读报告里的仓库观测项，转成由操作者选定的优化候选，并做基线/候选配对评估。触发：用户要求查看某条优化观测、评估候选改动，或对当前 Caveman 优化报告采取行动。需要已登录的 Caveman CLI 连接和明确批准；绝不从 profile 推断金额或执行动作。 |
| `caveman-review` | `caveman-review` | 超压缩代码评审意见：去除 PR 反馈噪音，保留可执行信号，每条评论一行，含位置、问题、修复方案。当用户说"review this PR""code review""review the diff""/review"或调用 /caveman-review 时使用，评审 pull request 时自动触发。 |
| `caveman-setup` | `caveman-setup` | 把当前仓库接入 Caveman Cloud gateway，对每个 LLM 请求计量成本、token、延迟，且不改变原有行为。触发：用户粘贴 Caveman setup prompt、说“set up caveman”，或想给应用加 LLM 花费可观测性。需要 gateway URL 和 Cave API key（setup prompt 自带这两项）。 |
| `caveman-stats` | `caveman-stats` | 显示当前会话的真实 token 用量和估算节省，直接读取 Claude Code 会话日志，非 AI 估算。由 /caveman-stats 触发。输出由 mode-tracker hook 注入，模型本身不计算数字。 |
| `cellxgene-census` | `cellxgene-census` | 以编程方式查询 CZ CELLxGENE Census，获取带版本的公共单细胞和空间转录组数据。适用于：群体级细胞元数据、基因表达切片、Census 汇总计数、源 H5AD URI/下载、embeddings、空间 Census 数据，或跨物种、组织、疾病、检测方式、细胞类型的参考图谱对比。分析自己的本地单细胞数据请用 scanpy、anndata 或 scvi-tools。 |
| `changelog-gen` | `changelog-gen` | Changelog 生成器：从 Git 历史自动生成 CHANGELOG。 |
| `changelog-generator` | `changelog-generator` | 从 git 提交生成 changelog。当用户说"generate changelog""update changelog""what changed since last release"，或准备新版本发布前使用。 |
| `chinese-code-review` | `chinese-code-review` | 中文代码评审沟通参考：话术模板、分级标注（必须修复/建议修改/仅供参考）、国内团队常见反模式的应对方式。仅在用户显式输入 /chinese-code-review 时调用，不要根据上下文自动触发。 |
| `chinese-commit-conventions` | `chinese-commit-conventions` | 中文 commit 与 changelog 配置参考：Conventional Commits 中文适配、commitlint/husky/commitizen 中文模板、conventional-changelog 中文配置。仅在用户显式 /chinese-commit-conventions 时调用，不根据上下文自动触发。 |
| `chinese-documentation` | `chinese-documentation` | 中文文档排版参考：中英文空格、全半角标点、术语保留、链接格式、中文文案排版指北约定。仅在用户显式输入 /chinese-documentation 时调用，不根据上下文自动触发。 |
| `chinese-git-workflow` | `chinese-git-workflow` | 国内 Git 平台配置参考——Gitee、Coding.net、极狐 GitLab、CNB 的 SSH/HTTPS/凭据/CI 接入差异与镜像同步配置。仅在用户显式调用 /chinese-git-workflow 时使用，不根据上下文自动触发。 |
| `ci` | `ci` | 面向 Gemini CLI 的专用技能：高性能、快速失败的 GitHub Actions workflow 监控，并对 CI 失败做本地自动验证。自动发现 run，只需提供分支名。 |
| `cirq` | `cirq` | Google 量子计算框架。适用于：面向 Google Quantum AI 硬件、设计噪声感知电路，或运行量子表征实验。最适合 Google 硬件、噪声建模和底层电路设计。IBM 硬件用 qiskit；带自动微分的量子机器学习用 pennylane；物理仿真用 qutip。 |
| `citation-management` | `citation-management` | 学术研究的全流程引文管理：在 OpenAlex、PubMed、Google Scholar 检索论文，提取准确元数据，校验引文，生成格式规范的 BibTeX 条目。适用于查找论文、核实引用信息、DOI 转 BibTeX、确保科学写作中参考文献准确。 |
| `claude` | `gstack-claude` | 面向非 Claude 宿主的 Claude Code CLI 包装器，三种模式。Review：通过 claude -p 做独立 diff 审查；Challenge：对抗式失败模式审查；Consult：以只读文件工具向 Claude 询问仓库相关问题。触发词：claude review、claude challenge、ask claude、second opinion from claude、outside voice。（gstack） |
| `claude-api` | `claude-api` | Claude API / Anthropic SDK 参考：模型 id、定价、参数、流式、tool use、MCP、agents、缓存、token 计数、模型迁移。触发（打开目标文件前先读，勿因看似一行改动而跳过）：提示词提到 Claude/Anthropic 任一形式（Opus、Sonnet、Haiku、anthropic、@anthropic-ai、claude-*、us.anthropic.*）；用户问 LLM 定价/模型选择/限制/缓存（勿凭记忆回答）；任务属 LLM 形态但未指明提供商（agent/MCP/RAG/LLM-judge/computer-use，生成/摘要/抽取/分类/改写/对话，调试拒答/截断/流式/tool call/token）。仅当用其他提供商时跳过：查询点名 OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama，或项目 grep openai\|langchain_openai\|google.generativeai\|genai\|mistralai\|cohere\|ollama 命中（未点名时先 grep 再读文件）。 |
| `claude-handoff` | `in-progress/claude-handoff` | 把当前对话交接给一个全新的后台 agent，由其立即接手继续工作。 |
| `claude-handoff` | `claude-handoff` | 把当前对话交接给一个全新的后台 agent，由其立即接手继续工作。 |
| `clean-code` | `clean-code` | Clean Code 原则（DRY、KISS、YAGNI）、命名、函数设计与可读性。适用于代码难读、方法过长、命名不清、重复代码或嵌套过深时。类职责划分与依赖方向问题请改用 solid-principles。 |
| `cleanddd-coach` | `cleanddd-coach` | 交互式 CleanDDD 教练技能，循序讲解 CleanDDD 核心原则与方法并与用户互动练习；包含微课、测验与检查清单，可承接到需求分析/建模/代码实现技能。 |
| `cleanddd-dotnet-coding` | `cleanddd-dotnet-coding` | CleanDDD 项目中落地已建模需求的编码指南，覆盖聚合、命令、查询、API 端点（Endpoints）、事件、仓储、配置、测试；用于编写或修改业务功能、端点与数据访问时。 |
| `cleanddd-dotnet-init` | `cleanddd-dotnet-init` | 初始化 CleanDDD dotnet 项目（netcorepal-web 模板）。在创建新项目或为客户演示快速拉起解决方案时使用，可直接调用 dotnet new 或包装脚本。 |
| `cleanddd-modeling` | `cleanddd-modeling` | 基于 cleanddd-requirements-analysis 的结果，输出符合 CleanDDD 的聚合、命令、事件、查询、API 端点（Endpoints）和定时任务模型；用于从已拆解的需求快速得到建模蓝图。 |
| `cleanddd-requirements-analysis` | `cleanddd-requirements-analysis` | 需求澄清与拆解，识别干系人并将需求条目标注所属对象与业务实体；仅产出结构化需求描述，不做建模定义，可作为后续建模输入。 |
| `clickhouse-io` | `clickhouse-io` | ClickHouse 数据库模式、查询优化、分析与数据工程最佳实践，面向高性能分析型负载。适用于编写 ClickHouse schema 或查询，或分析查询过慢时。 |
| `clinical-decision-support` | `clinical-decision-support` | 准备并校验仅限研究用途的临床决策支持产物：评估、证据画像、队列、生存分析、生物标志物/模型、隐私与治理文档。适用于聚合或合成数据的研究文档与可追溯性；不用于患者诊疗或线上临床操作。 |
| `clinical-reports` | `clinical-reports` | 为临床病例、诊断、试验、安全性和汇总研究报告生成带安全边界的草稿结构，并运行本地确定性检查。仅适用于合成、去标识化或汇总数据输入及已验证的来源事实清单；所有输出都需合格人员审查。 |
| `cobrapy` | `cobrapy` | 基于约束的代谢建模（COBRA）。提供 FBA、FVA、基因敲除、通量采样、SBML 模型处理，用于系统生物学和代谢工程分析。 |
| `code-review` | `code-review` | 从固定基点（commit、分支、tag 或 merge-base）开始审查变更，沿两条轴线：Standards（代码是否遵循仓库成文编码规范）和 Spec（代码是否符合原始 issue/规格要求）。两个审查在并行子 agent 中运行并排汇报。适用于用户想审查分支、PR、进行中的改动，或说 review since X 时。 |
| `code-review` | `engineering/code-review` | 从固定基点（commit、分支、tag 或 merge-base）起沿两个维度审查变更：Standards（是否符合仓库文档化的编码规范）和 Spec（是否符合原始 issue/spec 要求）；两个审查在并行子 agent 中运行并排报告；适用于审查分支、PR、进行中的变更，或用户要求 review since X。 |
| `code-reviewer` | `code-reviewer` | 代码审查技能。支持本地变更（已暂存或工作区）和远程 Pull Request（按 ID 或 URL），关注正确性、可维护性和项目规范遵循。 |
| `codebase-design` | `codebase-design` | 设计深模块（deep module）的共享词汇。当用户想设计或改进模块接口、寻找深化机会、决定 seam 的位置、让代码更可测试或更易被 AI 导航，或其他 skill 需要深模块词汇时使用。 |
| `codebase-design` | `engineering/codebase-design` | 设计深模块（deep module）的共享词汇。当用户想设计或改进模块接口、寻找深化机会、决定 seam 的位置、让代码更可测试或更易被 AI 导航，或其他 skill 需要深模块词汇时使用。 |
| `codebase-onboarding` | `codebase-onboarding` | 分析陌生代码库并生成结构化上手指南：架构图、关键入口点、约定和入门 CLAUDE.md。加入新项目或首次在仓库中配置 Claude Code 时使用。 |
| `coding-standards` | `coding-standards` | 跨项目的基线编码约定，涵盖命名、可读性、不可变性与代码质量审查。框架相关的模式请用专门的前端或后端技能。适用于审查代码质量或命名，且没有适用的框架专属技能时。 |
| `concurrency-review` | `concurrency-review` | 审查 Java 并发代码的线程安全、竞态条件、死锁及现代模式（Virtual Threads、CompletableFuture、@Async）。当用户说"check thread safety""concurrency review""async code review"，或审查多线程代码时使用。 |
| `confluence-cli` | `confluence-cli` | 提供 Confluence CLI 基础能力：环境检查、uv 安装、命令调用方式、参数说明、页面/附件/搜索等通用操作，以及 Markdown 发布的基础转换规则。适用于查询、检索、读取、发布 Confluence 页面，或确认 CLI 用法与环境是否正确的场景。 |
| `consciousness-council` | `consciousness-council` | 对任何问题、决策或创意挑战开展多视角 Mind Council（心智议会）审议。触发：用户需要多元观点、要帮忙做艰难决定、要求 council/panel/board 式讨论、想从多个角度探索问题、要魔鬼代言人分析；或说 what would different experts think about this、help me think through this from all sides、council mode、mind council、deliberate on this；用户面临两难、权衡取舍或没有明显答案的复杂选择时也应触发。 |
| `context-budget` | `context-budget` | 审计 Claude Code 上下文窗口消耗：跨 agent、skill、MCP server 和 rules 识别膨胀与冗余组件，产出按优先级排序的 token 节省建议；适用于上下文窗口消耗过快、需要定位是哪些组件占用时。 |
| `context-restore` | `gstack-context-restore` | 恢复 /context-save 之前保存的工作上下文，加载最近一次保存状态（默认跨所有分支），从中断处继续工作，支持跨 Conductor 工作区交接。触发词：resume、restore context、where was I、pick up where I left off。与 /context-save 配对使用；原名 /checkpoint resume，因 Claude Code 将 /checkpoint 视为原生 rewind 别名而改名。（gstack） |
| `context-save` | `gstack-context-save` | 保存工作上下文：捕获 git 状态、已做决策和剩余工作，让任何后续会话无缝接续。触发词：save progress、save state、context save、save my work。与 /context-restore 配对恢复。原名 /checkpoint，因 Claude Code 将 /checkpoint 作为原生回退别名会遮蔽此 skill 而改名。(gstack) |
| `continuous-learning-v2` | `continuous-learning-v2` | 基于本能（instinct）的学习系统：通过 hooks 观察会话，创建带置信度评分的原子本能，并将其演化为 skills/commands/agents。v2.1 新增项目级本能，防止跨项目污染。适用于从会话中提炼经验教训、管理本能，或把本能提升为 skill、命令或 agent。 |
| `contract-first` | `contract-first` | 契约优先（contract-first）：当多个消费方与提供方需要共同演进 API 或事件 schema，且必须避免字段漂移、集成意外或单方悄悄重定义接口时使用。 |
| `contrarian-setup-gate` | `contrarian-setup-gate` | 通过 fail-closed 优先级状态机，把 Jason Shapiro 逆向流水线的三项判定（COT 拥挤度、新闻反应失效、周线价格行为确认）合成为单个可执行的 setup_status。纯离线合成：无网络、无 API key，除校验和优先级判定外无其他计算。 |
| `cot-contrarian-detector` | `cot-contrarian-detector` | 检测 CFTC 期货市场的拥挤投机头寸（COT 报告分析），用 Jason Shapiro 方法论寻找逆向交易设置。通过 FMP Commitment of Traders API 筛选 65 个期货市场（股指、利率、外汇、金属、能源、加密货币）的大投机者（non-commercial）净头寸，计算每个市场的 3 年期和 26 周 COT 指数，把极端值分类为 CROWDED_LONG / CROWDED_SHORT。当用户问及 COT 报告分析、拥挤头寸、谁被套牢、投机头寸极端、逆向期货设置或想跑 Jason Shapiro 式分析时使用。只自动化拥挤检测（5 步中的第 1 步），本身不生成交易信号。 |
| `crypto-regime-analyzer` | `crypto-regime-analyzer` | 用免费的无 key 公开数据（CoinGecko + Binance 资金费率）量化加密市场状态健康度，生成跨 6 个分量的 0-100 综合评分（100 = risk-on）并给出仓位建议。无需 API key。适用于用户询问加密市场状况、是否进入山寨季、BTC 主导率、加密 risk-on 与 risk-off、资金费率，或是否应增减加密敞口时。 |
| `cso` | `gstack-cso` | 首席安全官模式，基础设施优先的安全审计：secrets 考古、依赖供应链、CI/CD 管道安全、LLM/AI 安全、skill 供应链扫描，加 OWASP Top 10、STRIDE 威胁建模和主动验证；两种模式：daily（零噪音，8/10 置信门槛）和 comprehensive（月度深扫，2/10 门槛），跨审计运行跟踪趋势；触发词：security audit、threat model、pentest review、OWASP、CSO review，语音别名 see-so、security review 等。(gstack) |
| `dashboard-builder` | `dashboard-builder` | 为 Grafana、SigNoz 及类似平台构建能回答运维真实问题的监控仪表盘。当需要把指标变成可用的工作仪表盘而非摆设看板时使用。 |
| `dask` | `dask` | 面向超出内存的 pandas/NumPy 工作流的分布式计算。适用于需要把现有 pandas/NumPy 代码扩展到内存之外或跨集群运行时，最适合并行文件处理、分布式机器学习、与现有 pandas 代码集成。单机核外分析用 vaex；内存内提速用 polars。 |
| `data-quality-checker` | `data-quality-checker` | 发布前校验市场分析文档和博客文章的数据质量。检查价格量级不一致（ETF 与期货）、证券代码记法错误、日期与星期不匹配、配置比例合计错误、单位不一致；支持英文和日文内容。咨询模式：问题以警告形式标出供人工复核，不作阻断。 |
| `data-throughput-accelerator` | `data-throughput-accelerator` | 当大规模数据摄取、回填、导出、ETL、数仓加载、manifest 追赶或表同步需要在保证数据正确性的前提下大幅提速时触发。 |
| `database-lookup` | `database-lookup` | 查询有文档的公开数据库 API，明确端点、过滤条件、分页和数据来源。当科学、监管、金融或其他数据库支撑的事实必须从具名来源可复现地获取、而非依赖通用知识推断时使用。 |
| `database-migrations` | `database-migrations` | 数据库迁移最佳实践：schema 变更、数据迁移、回滚和零停机部署，覆盖 PostgreSQL、MySQL 及常见 ORM（Prisma、Drizzle、Kysely、Django、TypeORM、golang-migrate）。适用于编写 schema 或数据迁移、规划回滚或追求零停机部署。 |
| `datamol` | `datamol` | RDKit 的 Pythonic 封装，接口简化、默认值合理。标准药物发现首选：SMILES 解析、标准化、描述符、指纹、聚类、3D 构象、并行处理。返回原生 rdkit.Chem.Mol 对象。需要高级控制或自定义参数时直接用 rdkit。 |
| `db-migrator` | `db-migrator` | 数据库迁移助手：Schema 对比、迁移脚本生成。 |
| `db-whisperer` | `db-whisperer` | 诊断和改进应用层数据库：Postgres、MySQL、SQLite、MongoDB。覆盖 EXPLAIN ANALYZE、慢查询检测、索引策略、N+1 检测、带 up/down 脚本的 schema 迁移、连接池、复制配置、vacuum/analyze 操作。当用户说"这个查询很慢""加个索引""新列的迁移""ORM 的 N+1""解释这个查询计划""复制延迟""优化我的数据库""查询超时""连接池耗尽"时使用。 |
| `deep-research` | `deep-research` | 通用深度研究 agent 团队：13 个 agent 的流水线，对任意主题做严谨学术研究。8 种模式：完整研究、快速简报、论文评审、文献综述、事实核查、三段式文献扫描、苏格拉底式引导研究对话、系统性综述（可选 meta 分析）。覆盖研究问题构建、苏格拉底式指导、方法学设计、系统性文献检索、来源核验、跨源综合、偏倚风险评估、meta 分析、APA 7.0 报告编纂、编辑审查、魔鬼代言人质询、伦理审查和研究后文献追踪。触发词：research、deep research、literature review、systematic review、meta-analysis、PRISMA、evidence synthesis、fact-check、WHY HOW WHAT papers、3W literature scan、guide my research、help me think through、研究、深度研究、文獻回顧、文獻探討、系統性回顧、後設分析、事實查核、三段式文獻掃描、引導我的研究、幫我釐清、幫我想想、我不確定要研究什麼、研究方向、研究主題。 |
| `deep-research-ecc` | `deep-research-ecc` | 使用 firecrawl 和 exa MCP 做多源深度研究：搜索网络、综合发现、产出带来源归属和引用的报告。当用户需要对任意主题做有证据和引用的深入研究时使用。 |
| `deepchem` | `deepchem` | 分子机器学习，提供多样化特征化器和预置数据集。适用于：用传统 ML 或 GNN 做性质预测（ADMET、毒性），且需要丰富特征化选项和 MoleculeNet 基准时。最适合用预训练模型快速实验和多样分子表示。图优先的 PyTorch 工作流用 torchdrug；基准数据集用 pytdc。 |
| `deepspot-m` | `deepspot-m` | 用 DeepSpot-M 从 H&E 组织病理切片生成全转录组虚拟空间转录组数据。适用场景：需要约 20 倍镜下 224x224 图块（tile）的 log1p-CPM 空间基因表达；想按基因符号查询蛋白编码基因而非固定 panel；或用 histolab 切块后对整张切片（whole slide）跑预测。 |
| `deeptools` | `deeptools` | NGS 分析工具包：BAM 转 bigWig、质控（相关性、PCA、fingerprint）、热图/剖面图（TSS、peaks），用于 ChIP-seq、RNA-seq、ATAC-seq 可视化。 |
| `dep-auditor` | `dep-auditor` | 审计 Node.js、Python、Go、Rust、JVM、Ruby 项目的依赖漏洞、版本健康度与许可证事实；当用户要求检查 package.json、lockfile、requirements、go.mod、Cargo.toml、pom.xml、Gemfile.lock，或生成不改依赖的中文审计报告时使用。 |
| `deploy-ninja` | `deploy-ninja` | 处理零停机部署：蓝绿、金丝雀发布、滚动更新和 feature flag 灰度。覆盖 Kubernetes、Docker、Cloudflare Workers、Terraform 和 CI/CD 流水线搭建。当用户要部署应用、搭建部署流水线、实现金丝雀发布、配置滚动更新、管理 feature flag 或任何发布自动化时使用。触发语：deploy to production、set up CI/CD、blue-green deployment、canary release、rolling update、zero-downtime deploy、rollback，以及 push this to prod、how do I safely release this 等口语请求。 |
| `deployment-patterns` | `deployment-patterns` | Web 应用的部署工作流、CI/CD 流水线模式、Docker 容器化、健康检查、回滚策略和生产就绪清单。适用于：搭建 CI/CD、应用容器化，或发布前检查生产就绪状态。 |
| `depmap` | `depmap` | 查询 Cancer Dependency Map（DepMap）：癌细胞系基因依赖评分（CRISPR Chronos）、药物敏感性数据和基因效应谱；适用于识别癌症特异性脆弱点、合成致死相互作用和验证肿瘤药物靶点。 |
| `design` | `design` | 综合设计 skill：品牌识别、设计 token、UI 样式、logo 生成（55 种风格，Gemini AI）、企业形象方案 CIP（50 项交付物与样机）、HTML 演示文稿（Chart.js）、横幅设计（22 种风格，社交/广告/网页/印刷）、图标设计（15 种风格，SVG，Gemini 3.1 Pro）、社交图片（HTML 转截图，多平台）。动作：设计 logo、创建 CIP、生成样机、做幻灯片、设计横幅、生成图标、创建社交媒体图片、品牌识别、设计系统。覆盖 Facebook、Twitter、LinkedIn、YouTube、Instagram、Pinterest、TikTok、Threads、Google Ads 等平台。 |
| `design-consultation` | `gstack-design-consultation` | 设计咨询：理解产品、调研行业现状、提出完整设计系统（美学、字体、色彩、布局、间距、动效），并生成字体加配色预览页，创建 DESIGN.md 作为项目设计唯一真源。已有站点改用 /plan-design-review 反推设计系统。触发："design system"、"brand guidelines"、"create DESIGN.md"；新项目 UI 起步且无设计系统或 DESIGN.md 时应主动建议。(gstack) |
| `design-html` | `gstack-design-html` | 设计定稿：生成生产级 Pretext 原生 HTML/CSS。可基于 /design-shotgun 的已批准样机、/plan-ceo-review 的 CEO 方案、/plan-design-review 的设计评审上下文，或用户描述从零开始。文本真实回流、高度自动计算、布局动态，30KB 开销零依赖，智能 API 路由按设计类型选择 Pretext 模式。触发："finalize this design"、"turn this into HTML"、"build me a page"、"implement this design"，或任何规划类 skill 之后；用户已批准设计或方案就绪时应主动建议。语音别名："build the design"、"code the mockup"、"make it real"。(gstack) |
| `design-patterns` | `design-patterns` | 常见设计模式及 Java 示例（Factory、Builder、Strategy、Observer、Decorator 等）。当用户说"implement pattern""use factory""strategy pattern"，或设计可扩展组件时使用。 |
| `design-review` | `gstack-design-review` | 设计师视角的 QA：找出视觉不一致、间距问题、层级问题、AI 味模式和慢交互并修复。在源码中迭代修复，每个修复原子提交，并用前后截图复验。计划阶段的设计评审请用 /plan-design-review。触发：“audit the design”、“visual QA”、“check if it looks good”、“design polish”；用户提到视觉不一致或想打磨线上站点观感时主动建议。 |
| `design-shotgun` | `gstack-design-shotgun` | 设计散弹枪：生成多个 AI 设计变体、打开对比板、收集结构化反馈并迭代，是可随时运行的独立设计探索。当用户说"explore designs""show me options""design variants""visual brainstorm"或"我不喜欢现在的样子"时使用；用户描述了 UI 功能但还没见过可能的样子时主动建议。(gstack) |
| `design-system` | `design-system` | 设计 token 架构、组件规格与幻灯片生成：三层 token（primitive→semantic→component）、CSS 变量、间距/字体比例、组件规范、策略性幻灯片制作。用于设计 token、系统化设计、符合品牌规范的演示文稿。 |
| `design-system-ecc` | `design-system-ecc` | 生成或审查设计系统、检查视觉一致性、审查涉及样式的 PR。在生成或审计设计系统、检查视觉一致性或审查触及样式的 PR 时使用。 |
| `design-taste-frontend` | `taste-skill` | 反 slop 前端技能，用于落地页、作品集和重设计。agent 阅读 brief、推断正确的设计方向，交付不像模板的界面。适用时使用真实设计系统，重设计先审计，执行严格的 pre-flight 检查。 |
| `design-taste-frontend-v1` | `taste-skill-v1` | 原始 v1 版 taste-skill，为依赖其精确行为的项目保留。当前默认是 design-taste-frontend（v2 实验版，大幅重写）。仅在需要精确向后兼容时使用此 v1 安装名。 |
| `devex-review` | `gstack-devex-review` | 实时开发者体验审计：用 browse 工具实际测试 DX——浏览文档、尝试入门流程、计时 TTHW、截图错误信息、评估 CLI 帮助文本，产出带证据的 DX 记分卡；若存在 /plan-devex-review 分数则对比（回旋镖效应：计划说 3 分钟，实际 8 分钟）。触发词：test the DX、DX audit、developer experience test、try the onboarding；发布面向开发者的功能后可主动建议。语音触发：dx audit、test the developer experience、try the onboarding、developer experience test。（gstack） |
| `dhdna-profiler` | `dhdna-profiler` | 从任意文本提取认知模式和思维指纹。当用户想分析某人如何思考、理解认知风格、画像写作或言语模式、比较多人思维风格，或问 what's my thinking style、analyze how this person reasons、cognitive profile、thinking pattern、DHDNA、digital DNA，或想理解文本背后的心智时使用。用户提供文本并希望深入了解作者的推理模式、决策风格或认知签名时也触发。 |
| `diagnosing-bugs` | `diagnosing-bugs` | 疑难 bug 和性能回归的诊断循环。适用于用户说 diagnose、debug this，或报告某功能损坏/抛异常/失败/变慢时。 |
| `diagnosing-bugs` | `engineering/diagnosing-bugs` | 疑难 bug 和性能回归的诊断循环。适用于用户说 diagnose、debug this，或报告某功能损坏/抛异常/失败/变慢时。 |
| `diagram` | `gstack-diagram` | 把英文描述（或 mermaid 源码）转成图表三件套：源码、可在 excalidraw.com 打开的可编辑 .excalidraw 文件、渲染好的 SVG + PNG（干净的 mermaid 风格；.excalidraw 保留手绘质感）。完全离线运行。触发：“make a diagram”、“draw the architecture”、“create a flowchart”、“diagram this”、“visualize this flow”。 |
| `diagram-design` | `diagram-design` | 创建品牌化图表并输出独立 HTML/SVG/PNG：架构图、IT 现状图、流程图、时序图、状态机、ER/数据模型、时间线、泳道图、象限图、雷达/蜘蛛图、极坐标图、循环/飞轮图、嵌套图、树图、组织架构图、层级堆叠图、Venn 图、金字塔/漏斗、treemap、柱状图、折线图、Gantt 图、散点图、高层图、过程图、medallion、数据流、DP 集成、DP 安全矩阵、Sankey 图、鱼骨图、Wardley map、看板、用户旅程、部署图、依赖图、UML 类图、故事地图、数据库 schema 图。可按指定尺寸/细节重绘 .drawio/.drawio.png/.drawio.svg 或 Mermaid .mmd 源文件；从网站提取品牌 token；添加语义图案、标注、无障碍动效或手绘风格。 |
| `diffdock` | `diffdock` | DiffDock 与 DiffDock-L 分子对接：从 PDB 或序列加 SMILES/SDF/MOL2 预测蛋白-小分子结合构象，支持批量对接、虚拟筛选和构象置信度解读。不适用于结合亲和力预测。 |
| `discernment-nudge` | `discernment-nudge` | 在给出用户可能据以行动的实质性回答或草稿（建议、目标/计划/提案/邮件等草稿、估算、数据分析、事实断言、多步论证）之后、最终定稿之前调用：若适用，追加 2-3 个简短的跟进问题，每个都针对刚产出内容中的具体点，帮助用户核查关键事实、审视推理假设、发现缺失上下文。每次对话最多用一次。琐碎操作类问题、纯教学解释、格式转换、用户自己运行的代码、创意写作或闲聊、用户已要求复核/引用/审查时跳过。 |
| `dispatching-parallel-agents` | `dispatching-parallel-agents` | 当面对 2 个以上可独立进行、无共享状态或顺序依赖的任务时使用，并行派发 agent 处理。 |
| `dividend-growth-pullback-screener` | `dividend-growth-pullback-screener` | 筛选处于临时回调中的高质量股息增长股：年股息增长率 12% 以上、股息率 1.5% 以上，且 RSI 超卖（RSI≤40）。结合股息基本面分析与技术择时指标，在强势股息增长股短期走弱时识别买入机会。 |
| `dnanexus-integration` | `dnanexus-integration` | 在 DNAnexus 上用 dx CLI、dxpy、apps/applets、原生 workflow、dxCompiler 和 Nextflow 构建并运维可复现的基因组学负载；适用于数据传输、dxapp.json 开发、执行监控、workflow 导入和项目自动化。 |
| `doc-coauthoring` | `doc-coauthoring` | 引导用户通过结构化工作流共同撰写文档。适用于写文档、提案、技术规格、决策文档等结构化内容；帮助高效传递上下文、迭代打磨内容并验证文档对读者有效。用户提到写文档、创建提案、起草规格等任务时触发。 |
| `docker-patterns` | `docker-patterns` | Docker 与 Docker Compose 模式：本地开发、加固的 CLI 安装器测试框架、容器安全、网络、卷、多服务编排。创建或审查 Dockerfile 与 Compose 服务、跨 Linux 发行版测试安装器、规划准确的 macOS/Windows 原生验证时使用。 |
| `docs-changelog` | `docs-changelog` | 基于提供的版本号和原始 changelog 数据，为新版本生成并格式化 changelog 文件。 |
| `docs-writer` | `docs-writer` | 当任务涉及编写、审查或编辑 /docs 目录中的文件或仓库中任何 .md 文件时，始终使用此 skill。 |
| `document-generate` | `gstack-document-generate` | 为功能、模块或整个项目从零生成缺失文档，用 Diataxis 框架（tutorial/how-to/reference/explanation）产出完整结构化文档；可独立调用，也可被 /document-release 在发现覆盖缺口时调用；触发词：write docs、generate documentation、document this feature、create a tutorial、explain this module。(gstack) |
| `document-release` | `gstack-document-release` | 发布后的文档更新：读取全部项目文档并与 diff 交叉核对，构建 Diataxis 覆盖图（reference/how-to/tutorial/explanation），更新 README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md 使其与已发布内容一致，检测架构图漂移，用 sell-test 评分标准润色 CHANGELOG 文风，清理 TODO，可选更新 VERSION；在 PR 正文中列出文档欠债。触发：update the docs、sync documentation、post-ship docs；PR 合并或代码发布后应主动建议。（gstack 套件） |
| `documentation-lookup` | `documentation-lookup` | 通过 Context7 MCP 获取最新的库和框架文档，替代训练数据中的过时知识。触发场景：环境搭建问题、API 参考、代码示例，或用户提到具体框架（如 React、Next.js、Prisma）时。 |
| `docx` | `docx` | 创建、读取、编辑或操作 Word 文档（.docx）和 Word 模板（.dotx）。触发词：Word doc、.docx、.dotx，或要求生成带目录、标题、页码、信头等格式的专业文档；也适用于提取/重组文档内容、插入替换图片、查找替换、处理修订和批注、把内容转成精排 Word 文档。用户要 Word 格式的 report、memo、letter、template 等交付物时使用。不适用于 PDF、电子表格、Google Docs 或与文档生成无关的编码任务。 |
| `domain-modeling` | `domain-modeling` | 构建并打磨项目的领域模型。适用于讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 架构决策记录等场景。 |
| `domain-modeling` | `engineering/domain-modeling` | 构建并打磨项目的领域模型。适用于讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 架构决策记录等场景。 |
| `downtrend-duration-analyzer` | `downtrend-duration-analyzer` | 分析历史下跌趋势的持续时间，生成交互式 HTML 直方图，按板块和市值展示典型回调长度。 |
| `drawdown-circuit-breaker` | `drawdown-circuit-breaker` | 基于 trader-memory-core 状态评估账户级回撤熔断规则，决定今天是否允许新的交易风险。使用已实现盈亏、连败冷却、周/月回撤限制，不调用任何外部 API。 |
| `ds-mapper` | `ds-mapper` | 项目目录结构地图：生成带说明的可视化目录树，快速理解任意代码库。 |
| `dual-axis-skill-reviewer` | `dual-axis-skill-reviewer` | 用双轴法评审任意项目里的 skill：一是确定性的代码检查（结构、脚本、测试、执行安全），二是 LLM 深度评审结论。适用于需要给 skills/*/SKILL.md 做可复现的质量打分、用分数阈值（如 90+）卡合并、或为低分 skill 列出具体改进项。通过 --project-root 跨项目工作。 |
| `e2e-testing` | `e2e-testing` | Playwright E2E 测试模式：Page Object Model、配置、CI/CD 集成、产物管理和不稳定测试（flaky test）应对策略。适用于：编写 Playwright 测试、组织 page object 结构，或修复 CI 中不稳定的 E2E 运行。 |
| `earnings-calendar` | `earnings-calendar` | 通过 Financial Modeling Prep（FMP）API 获取美股即将公布的财报日程。适用于用户请求财报日历数据、想知道下周哪些公司发布财报、或需要每周财报回顾时。聚焦市值 20 亿美元以上、对市场影响显著的中盘及以上公司，按日期和时间以清晰的 markdown 表格组织数据。支持多种环境（CLI、Desktop、Web）和灵活的 API key 管理。 |
| `earnings-trade-analyzer` | `earnings-trade-analyzer` | 用 5 因子评分体系（缺口大小、财报前趋势、成交量趋势、MA200 位置、MA50 位置）分析近期财报后股票，打分 0-100 并给出 A/B/C/D 评级；适用于财报交易分析、财报后动量筛选、财报缺口评分或寻找近期最佳财报反应。 |
| `economic-calendar-fetcher` | `economic-calendar-fetcher` | 用 FMP API 获取即将发生的经济事件和数据发布：央行决议、就业报告、通胀数据、GDP 发布及其他影响市场的经济指标，支持指定日期范围（默认未来 7 天）。脚本输出原始 JSON 或文本，由助手筛选、评估影响并生成 Markdown 报告。 |
| `edge-candidate-agent` | `edge-candidate-agent` | 从 EOD（每日收盘）观察生成并排序美股多头方向的 edge 研究工单，导出可直接进流水线的候选规格，供 trade-strategy-pipeline Phase I 使用。当用户要求把假设/异常转化为可复现的研究工单、把已验证的想法转成 strategy.yaml + metadata.json，或在跑流水线回测前预检接口兼容性（edge-finder-candidate/v1）时使用。 |
| `edge-concept-synthesizer` | `edge-concept-synthesizer` | 在策略设计/导出之前，把 detector 工单和提示抽象为可复用的 edge 概念，包含论点（thesis）、失效信号（invalidation signals）和策略 playbook。 |
| `edge-hint-extractor` | `edge-hint-extractor` | 从每日市场观察和新闻反应中提取 edge 线索，可选用 LLM 做构思，输出规范的 hints.yaml 供下游概念合成与自动检测使用。 |
| `edge-pipeline-orchestrator` | `edge-pipeline-orchestrator` | 编排完整的 edge 研究流水线：从候选检测到策略设计、评审、修订和导出；适用于端到端协调多阶段 edge 研究工作流。 |
| `edge-signal-aggregator` | `edge-signal-aggregator` | 聚合并排序多个找优势技能（edge-candidate-agent、theme-detector、sector-analyst、institutional-flow-tracker）的信号，通过加权评分、去重和矛盾检测，产出按优先级排列的信念度仪表盘。 |
| `edge-strategy-designer` | `edge-strategy-designer` | 将抽象的 edge 概念转化为策略草案变体，并可选生成可导出的 ticket YAML，供 edge-candidate-agent 导出与验证。 |
| `edge-strategy-reviewer` | `edge-strategy-reviewer` | 对 edge-strategy-designer 产出的策略草稿做批判性评审，检查优势可信度、过拟合风险、样本量充分性与执行现实性。当 strategy_drafts/*.yaml 存在且需要在导出到 pipeline 前过质量关时使用，输出 PASS/REVISE/REJECT 结论及置信度评分。 |
| `email-ops` | `email-ops` | ECC 的证据优先邮箱工作流：分诊、起草、发送验证与已发送邮件安全跟进。适用于用户想整理邮件、通过真实邮件界面起草或发送、或需要证明确有邮件进入 Sent 时。 |
| `embedded-captions` | `embedded-captions` | 为已有的单主体口播（talking-head）视频添加字幕，不剪辑原素材。适用于普通逐字字幕、嵌入主体身后的电影感字幕、VFX 字幕、炸/特效/酷炫字幕，或 35 种风格目录中的具名风格。按视觉风格路由而非后端引擎。安静的 anchor 轨道是默认；仅当用户明确要全电影感处理时才逐词嵌入。工作流全程本地运行（含转写和主体抠像）；多镜头素材需先切分再应用。 |
| `env-manager` | `env-manager` | 环境变量管理器：扫描、校验、同步 .env 文件，生成安全配置模板。 |
| `error-handling` | `error-handling` | TypeScript、Python、Go 的健壮错误处理模式：类型化错误、错误边界、重试、熔断器、面向用户的错误消息。设计错误类型、重试、熔断或用户可见的失败提示时使用。 |
| `error-translator` | `error-translator` | 编程错误消息翻译专家：将英文错误消息翻译成中文，解释原因并提供修复方案。 |
| `eslint-fix` | `eslint-fix` | 安全诊断并修复 ESLint error、warning 和配置兼容问题；适用于用户要求运行 lint、解释 ESLint 报错、限定范围自动修复或迁移 ESLint 配置；优先使用项目锁定的包管理器与版本，先预检再修改，不自动下载最新版或批量改写无关源码。 |
| `esm` | `esm` | 在直接使用 esm Python SDK、ESM3 或 ESMC 模型 ID、Forge/Biohub 推理客户端，或 ESMFold2 折叠工作流时使用。 |
| `etetoolkit` | `etetoolkit` | 用 ETE 4 分析、操作、比较、注释和可视化系统发育或其他层次树：Newick/Nexus 树读写、拓扑编辑与模式匹配、Robinson-Foulds 比较、基因树进化事件与 reconciliation、NCBI/GTDB 分类、SmartView 探索和出版级渲染；不用于从原始序列推断树，需先比对序列并推断出树。 |
| `exa-search` | `exa-search` | 由 Exa 驱动的网络工具包，针对科学和技术内容调优。触发：用户需要搜索网页或抓取/提取 URL 内容。覆盖网页搜索（语义查找、研究、实时信息，可选 research-paper 类别和学术域名过滤）和 URL 提取（批量抓取页面、文章、学术 PDF）。当用户想要高质量搜索或通过 category=research paper 做学术过滤时使用；对搜索、查询、抓取页面、提取文章的请求均触发。 |
| `executing-plans` | `executing-plans` | 当你有一份书面实现计划需要在单独的会话中执行，并设有审查检查点时使用。 |
| `experimental-design` | `experimental-design` | 在收集数据之前设计实验和研究：选择设计类型、随机化、区组划分、安排处理组合，确保结果可解释。适用于规划研究、分配受试对象/样本到分组，或提到随机化、区组、分层、对照、因子/部分因子设计、DOE、多因素筛选、响应面优化、交叉/重复测量/裂区设计、整群随机化、拉丁方、孔板布局、批次/运行顺序效应、重复与伪重复、序贯/自适应设计等场景；口语化提问如"这个实验该怎么设计""如何避免混杂""怎么测这 6 个因素""把这些小鼠分组"也触发。选定设计后的样本量/功效计算用 statistical-power，分析已收集数据用 statistical-analysis。 |
| `exploratory-data-analysis` | `exploratory-data-analysis` | 对明确支持的科学文件做有界的本地探索性分析。适用于脱敏的 CSV/TSV/JSON 剖析；可选的 NumPy、HDF5、FASTA/FASTQ 及基础图像元数据检查；缺失值与数据泄漏审计；离群点与变换敏感性；以及严谨的 EDA 报告骨架。其他领域格式仅供参考，未知格式一律失败关闭。 |
| `exposure-coach` | `exposure-coach` | 整合市场宽度（breadth）、宏观状态（regime）和资金流（flow）分析 skill 的信号，生成一页纸 Market Posture 摘要：净敞口上限、成长 vs 价值偏向、参与广度、允许新开仓 vs 现金优先的建议。 |
| `faceless-explainer` | `faceless-explainer` | 把任意文本（文章、笔记、主题、简报）转成无人出镜的讲解视频；没有网站或素材可抓取，每个场景的画面需自行创作（排版、抽象图形、示意图、数据可视化）。适用于主题讲解、概念拆解、教程、清单类内容。不适用于基于网站制作的视频（做宣传或导览用 /product-launch-video）。不确定时用 /hyperframes。 |
| `fastapi-patterns` | `fastapi-patterns` | FastAPI 最佳实践，覆盖项目结构、Pydantic v2 schema、依赖注入、异步处理器、认证、授权、事务性服务层，以及用 httpx 和 pytest 做测试。适用于构建或评审 FastAPI 应用——Pydantic schema、依赖、异步处理器、认证或测试。 |
| `figma` | `figma` | 将 Figma 内容导入 HyperFrames 合成：渲染资产、品牌 token、组件、故事板分段→重建动效（frame 按状态而非幻灯片读取）（REST/CLI），可用时借助 connector 辅助动效，以及来自 connector 或原生导出的 shader。适用于：用户粘贴 figma.com 链接，或要求把 Figma 设计、frame、logo、品牌或动画带入视频/合成。 |
| `find-skills` | `find-skills` | 帮助用户发现和安装 agent skill。触发：用户问 how do I do X、find a skill for X、is there a skill that can...，或表达想扩展能力的意愿；当用户在寻找可能以可安装 skill 形式存在的功能时使用。 |
| `finishing-a-development-branch` | `finishing-a-development-branch` | 当实现完成、所有测试通过、需要决定如何集成这份工作时使用。 |
| `finviz-screener` | `finviz-screener` | 根据自然语言请求构建并打开 FinViz 选股器 URL。触发场景：用户想筛选股票、按基本面或技术面条件过滤、或要求带条件打开 FinViz。支持日文和英文输入（如高股息成长小型股、超卖高 ROE 大盘股）。 |
| `fireworks-tech-graph` | `fireworks-tech-graph` | 创建技术图表：软件架构、数据流、流程图、时序图、C4 评审、云部署、事件流、可观测性排查、agent/记忆系统、UML、ER、网络拓扑、时间线和技术概念图，可导出 SVG、PNG、聚焦语义的 SVG-to-GIF 动图或离线交互 HTML。直接的 GIF 生成请求（Generate a GIF、生成 GIF、制作 GIF）视为动图需求；用户要求可视化系统或工程概念时使用。不适用于照片、位图艺术或定量数据图表。 |
| `fireworks-tech-graph` | `fireworks-tech-graph/skills/fireworks-tech-graph` | 创建技术图表：软件架构、数据流、流程图、时序图、C4 评审、云部署、事件流、可观测性排查、agent/记忆系统、UML、ER、网络拓扑、时间线和技术概念图，可导出 SVG、PNG、聚焦语义的 SVG-to-GIF 动图或离线交互 HTML。直接的 GIF 生成请求（Generate a GIF、生成 GIF、制作 GIF）视为动图需求；用户要求可视化系统或工程概念时使用。不适用于照片、位图艺术或定量数据图表。 |
| `flowio` | `flowio` | 用 FlowIO 读取、检查和写入 Flow Cytometry Standard (FCS) 2.0、3.0、3.1 文件。用于底层 FCS 元数据和通道检查、NumPy 事件提取、多数据集文件、表格导出和 FCS 3.1 创建；补偿、流式变换、门控或 FlowJo 工作区请用 FlowKit。 |
| `fluidsim` | `fluidsim` | 规划、配置、检查、重启和分析有界的 FluidSim 计算流体力学模拟，带显式数值有效性和 HPC 安全检查。用于 FluidSim 求解器选择、参数审查、FFT/MPI 设置、输出诊断或重启兼容性。 |
| `freestocklineskill` | `freestocklineskill` | 面向 OpenClaw 和 Hermes 的免费无 API Key A 股生态数据查询技能。当用户查询 A股、沪深京股票、指数、ETF/LOF、可转债、行业/概念板块、实时行情、K线、涨跌排行、涨停/跌停/炸板、资金流、财务估值、公告、龙虎榜、大宗交易、融资融券、新闻快讯、筹码等公开数据，且不想填 API Key、Token、Cookie 或使用付费账号时使用。 |
| `freeze` | `gstack-freeze` | 会话内将文件编辑限制在指定目录，阻止对允许路径之外的 Edit 和 Write；适用于调试时防止误改无关代码，或想把改动限定在一个模块；触发词如 freeze、restrict edits、only edit this folder、lock down edits。(gstack) |
| `frontend-a11y` | `frontend-a11y` | React 和 Next.js 无障碍（a11y）模式：语义化 HTML、ARIA 属性、表单标签、键盘导航、焦点管理、屏幕阅读器支持。构建任何交互式 UI 组件或表单时使用。 |
| `frontend-design` | `frontend-design` | 在构建新 UI 或重塑现有 UI 时，提供独特、有意图的视觉设计指导。帮助确定美学方向、字体排印，做出不像模板默认值的设计选择。 |
| `frontend-patterns` | `frontend-patterns` | 前端开发模式：React、Next.js、状态管理、性能优化和 UI 最佳实践。构建或审查 React 或 Next.js 组件、状态或渲染性能时使用。 |
| `frontend-slides` | `frontend-slides` | 从零创建或转换 PowerPoint 文件，生成动画丰富的精美 HTML 演示文稿。当用户想制作演示、把 PPT/PPTX 转成网页版、或为演讲/路演做幻灯片时使用。通过视觉探索而非抽象选择，帮助非设计师找到自己的审美方向。 |
| `ftd-detector` | `ftd-detector` | 用 William O'Neil 方法论检测 Follow-Through Day（FTD）信号以确认市场底部：双指数跟踪（S&P 500 + NASDAQ），状态机管理反弹尝试、FTD 有效性判定与 FTD 后健康监测。当用户询问市场底部信号、follow-through day、反弹尝试、回调后再入场时机或能否加大股票敞口时使用；与 market-top-detector（防守型）互补，本技能是进攻型（底部确认）。 |
| `full-output-enforcement` | `output-skill` | 覆盖 LLM 默认的截断行为。强制完整生成代码，禁止占位符模式，并干净地处理 token 上限拆分。适用于任何需要详尽、不删减输出的任务。 |
| `futures-position-sizer` | `futures-position-sizer` | 根据方向、入场价和止损价计算按合约计的期货仓位大小，使用经核实的每品种合约规格（乘数、tick size、tick value）。触发：用户问该交易多少手期货合约、想为期货仓位定量（ES、NQ、ZB、GC、CL、6E/E6、VX、BT 等），或交接 contrarian-setup-gate 的 READY_FOR_PLAN 方向/失效价位用于仓位计算。纯离线计算，无需 API key 和网络。 |
| `fxmacrodata-calendar` | `fxmacrodata-calendar` | 获取 FXMacroData 官方宏观发布日历事件，用于交易计划、宏观状态检查和事件风险过滤。在 CPI、NFP、GDP、PCE、零售销售、PMI 及央行决议窗口之前使用。 |
| `general-video` | `general-video` | 在没有专门工作流可用、或 BRIEF.md 设了 flow: companion 时，编写或修改自定义 HyperFrames composition。适用于较长或多场景作品、品牌与宣传片、蒙太奇、静态循环、静态标题卡、素材混剪和自由构建。短的、无旁白、以动效为主的作品（含动画标题）改用 motion-graphics。全新创作应先走 hyperframes 再用本 skill。 |
| `generate-image` | `generate-image` | 通过 OpenRouter Image API（Gemini、Seedream、Recraft、GPT-Image、Riverflow）用 AI 模型生成或编辑图像。用于照片、插画、艺术创作、概念图、视觉素材、logo，以及基于参考图的图像编辑或合成。流程图、电路、通路等技术图表请改用 scientific-schematics 技能。 |
| `geniml` | `geniml` | 用 Geniml 做可审计的本地基因组区间工作流：校验 BED 和 universe 契约、规划 Region2Vec 或 scEmbed 运行、检查模型/tokenizer 兼容性、评估共识 universe。 |
| `genomic-coordinates` | `genomic-coordinates` | 在不同坐标约定间转换基因组区间，规范并比较变异表示，在装配或 contig 命名不匹配污染分析前将其检出。适用于坐标跨越格式、工具或装配边界的场景：BED、GFF/GTF、VCF、SAM/BAM、WIG、PSL、genePred、Picard interval_list、区域字符串之间的转换；调和 0-based 半开区间与 1-based 闭区间；indel 左对齐或修剪；判断两条变异记录是否描述同一变化；基因组位置到转录本、CDS 或蛋白位置的映射；审计 BED/GTF/VCF 的约定违规；诊断 GRCh37 vs hg19 vs GRCh38 vs T2T、chr 前缀和 liftover 问题。触发词：off by one、0-based、1-based、half-open、coordinate system、left-align、normalize variant、bcftools norm、chr prefix、wrong genome build、liftover、REF mismatch、HGVS。 |
| `genomic-intelligence` | `genomic-intelligence` | 用 Genomic Intelligence 托管的 transformer DNA 语言模型，直接从 DNA 序列预测调控特征、基因结构和表达，无需本地 GPU 或模型权重。通过 REST API 和托管 MCP server（无 key 的公开 demo）提供六类任务：启动子区域、剪接供体/受体位点、增强子活性、染色质状态、序列到表达（log TPM）、从头基因注释，外加“先找基因再预测表达”的组合工作流。触发：用户有基因符号、基因组区域或 DNA/FASTA 序列并想要上述预测，或提到 Genomic Intelligence、genomicintelligence.ai、api.genomicintelligence.ai、mcp.genomicintelligence.ai。 |
| `geomaster` | `geomaster` | 综合地理空间科学技能，覆盖遥感、GIS、空间分析、地球观测机器学习及 30 多个科学领域。支持卫星影像处理（Sentinel、Landsat、MODIS、SAR、高光谱）、矢量与栅格数据操作、空间统计、点云处理、网络分析、云原生工作流（STAC、COG、Planetary Computer），以及 8 种编程语言（Python、R、Julia、JavaScript、C++、Java、Go、Rust）和 500 多个代码示例。适用于遥感工作流、GIS 分析、空间机器学习、地球观测数据处理、地形分析、水文建模、海洋空间分析、大气科学及任何地理空间计算任务。 |
| `geopandas` | `geopandas` | 为直接使用 GeoPandas GeoSeries、GeoDataFrame、空间操作或矢量数据 I/O 的 Python 工作流提供指导和本地审计工具。 |
| `get-available-resources` | `get-available-resources` | 当用户要求资源感知规划，或在明显资源敏感的本地负载开始前，检测主机清单及有效的 CPU、内存、磁盘、调度器、容器和加速器限制。产出脱敏的 JSON 快照和保守的规划辅助信息，不做压力测试，也不假设可见的主机硬件都可用。 |
| `gget` | `gget` | gget：对 20+ 生物信息学数据库的快速 CLI/Python 查询，适合基因信息、BLAST/BLAT、病毒序列下载、AlphaFold 结构、富集分析、OpenTargets、COSMIC、CELLxGENE 及 8cube 小鼠特异性/表达数据的即时查询与交互式探索。批量处理或高级 BLAST 用 biopython；多库 Python 工作流用 bioservices。 |
| `ghost-scraper` | `ghost-scraper` | 从网站提取结构化数据：静态 HTML、JS 渲染的 SPA、分页列表和 API 支撑的页面；具备反爬检测意识、限速和 robots.txt 合规处理。触发：用户想抓取网站、从 URL 提取数据、拉取商品列表、采集结构化数据、逆向站点 API 或处理动态 JS 渲染内容；也触发于 get me data from this site、extract prices from、crawl these pages 及任何网页数据提取请求，包括 can you pull info from this URL 这类随口一问。 |
| `ginkgo-cloud-lab` | `ginkgo-cloud-lab` | 在 Ginkgo Bioworks Cloud Lab（cloud.ginkgo.bio）提交和管理 protocol，该平台通过 Reconfigurable Automation Carts（RACs）自主执行实验；适用于蛋白表达纯化（cell-free、E. coli、Pichia）、HiBiT/A280/LabChip 定量、IVT mRNA/circRNA 合成、热漂移/可开发性检测、Echo-MS 酶或分析物方法、SPR 靶点接入、荧光像素艺术等；覆盖 protocol 选择、输入准备、定价和下单流程。 |
| `git-commit` | `git-commit` | 为 Java 项目生成规范化 commit 提交说明。适用于用户说 commit、create commit、commit changes，或代码改动完成需要提交时。 |
| `git-guardrails-claude-code` | `misc/git-guardrails-claude-code` | 配置 Claude Code 钩子，在执行前拦截危险 git 命令（push、reset --hard、clean、branch -D 等）。适用于用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中拦截 git push/reset 时。 |
| `git-guardrails-claude-code` | `git-guardrails-claude-code` | 配置 Claude Code 钩子，在执行前拦截危险 git 命令（push、reset --hard、clean、branch -D 等）。适用于用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中拦截 git push/reset 时。 |
| `git-workflow` | `git-workflow` | 安全处理 Git 状态检查、提交信息、commit、分支、push、PR 和 rebase。当用户要求检查改动、生成或创建提交、管理分支、推送、发起 PR 或整理历史时使用；严格区分每个动作的授权，并保护工作树中已有和无关的修改。 |
| `git-workflow-ecc` | `git-workflow-ecc` | Git 工作流模式：分支策略、提交规范、merge 与 rebase 取舍、冲突解决、各规模团队协作开发最佳实践。选择分支策略、编写提交规范、决定 merge 还是 rebase、解决冲突时使用。 |
| `github-actions-gen` | `github-actions-gen` | 分析真实项目并生成或修订安全、可验证的 GitHub Actions workflow。当用户要求创建 CI、测试矩阵、构建、Release、部署、缓存、Secrets、OIDC、PR 自动化，或排查 workflow 配置时使用。 |
| `github-issue-creator` | `github-issue-creator` | 当被要求创建 GitHub issue 时使用：按仓库模板处理不同 issue 类型（bug、feature 等），并确保正确打标签。 |
| `global-stock-data` | `global-stock-data` | 美股港股全栈数据工具包，官方源优先，十三层架构、30+ 端点、11 个数据源、全部零鉴权。在行情/K线/技术指标(MA/MACD/RSI/KDJ/布林带)/基本面/资金面/期权/SEC Filing/工具八层之上，新增 CBOE 官方期权链（完整希腊字母+IV+0DTE 流+异动识别）、FINRA 全市场每日空头成交量、SEC EDGAR 申报事件流（Form4 内部人/8-K/13F 机构持仓）、EDGAR 全市场横截面筛选、美债收益率曲线/CFTC COT/财报日历。每个数据源标注合规级别与条款原文，内嵌全部调用代码，自包含零外部依赖。适用于美股港股个股分析、全市场筛选、财报解读、期权与 0DTE 策略、做空数据追踪、SEC 文件检索、资金流与机构持仓分析。 |
| `glycoengineering` | `glycoengineering` | 分析与工程化改造蛋白质糖基化：扫描序列中的 N-糖基化位点（N-X-S/T sequon）、预测 O-糖基化热点，并提供精选糖工程工具（NetOGlyc、GlycoShield、GlycoWorkbench）。适用于糖蛋白工程、治疗性抗体优化和疫苗设计。 |
| `google-workspace-ops` | `google-workspace-ops` | 把 Google Drive、Docs、Sheets、Slides 当作统一的工作流面来操作计划、追踪表、演示文稿和共享文档。适用于用户需要查找、总结、编辑、迁移或清理 Google Workspace 资产，而不想退化到裸工具调用的场景。 |
| `gpt-taste` | `gpt-tasteskill` | 顶级 UX/UI 与高级 GSAP 动效工程师：强制用 Python 驱动真随机化实现布局变化、严格 AIDA 页面结构、宽幅编辑式排版（禁止 6 行折行）、无缝 bento 网格、严格 GSAP ScrollTrigger（pinning、堆叠、scrubbing）、内联微图像、超大区块间距。 |
| `grill-me` | `grill-me` | 通过不留情面的连续追问，打磨计划或设计方案。 |
| `grill-me` | `productivity/grill-me` | 通过不留情面的连续追问，打磨计划或设计方案。 |
| `grill-with-docs` | `grill-with-docs` | 通过不留情面的访谈式追问打磨计划或设计，过程中同步产出文档（ADR 和术语表）。 |
| `grill-with-docs` | `engineering/grill-with-docs` | 通过不留情面的访谈式追问打磨计划或设计，过程中同步产出文档（ADR 和术语表）。 |
| `grilling` | `grilling` | 就某个计划、决策或想法对用户进行不留情面的追问。当用户想对自己的思路做压力测试，或使用任何 grill 触发短语时使用。 |
| `grilling` | `productivity/grilling` | 就某个计划、决策或想法对用户进行不留情面的追问。当用户想对自己的思路做压力测试，或使用任何 grill 触发短语时使用。 |
| `gstack` | `gstack` | gstack skill 套件的路由器：把任意 gstack 请求分发到正确的 skill（规划、评审、QA、发布、调试、文档、安全、设计）；浏览器/QA 和 dogfooding 场景指向 /browse。触发：调用 gstack 但未指定具体 skill，或询问哪个 gstack skill 适合当前任务。（gstack 套件） |
| `gstack-upgrade` | `gstack-upgrade` | 升级 gstack 到最新版：自动检测全局安装还是 vendored 安装，执行升级并展示更新内容。触发：upgrade gstack、update gstack、get latest version；语音转文字别名：upgrade the tools、update the tools、gee stack upgrade、g stack upgrade。 |
| `gtars` | `gtars` | 用 Gtars 做本地基因组区间模型与集合代数、重叠与计数、consensus 与覆盖度、tokenization、fragment 处理，以及 refget/BEDbase 规划，覆盖 Python、Rust 和 CLI 三种入口。 |
| `guard` | `gstack-guard` | 完整安全模式：破坏性命令警告 + 目录范围编辑限制。组合 /careful（rm -rf、DROP TABLE、force-push 等执行前警告）与 /freeze（阻止指定目录外的编辑）。接触生产环境或调试线上系统需要最高安全性时使用。触发："guard mode"、"full safety"、"lock it down"、"maximum safety"。(gstack) |
| `handoff` | `handoff` | 把当前对话压缩成交接文档，供另一个 agent 接手继续工作。适用于会话过长需要转移上下文时。 |
| `handoff` | `productivity/handoff` | 把当前对话压缩成交接文档，供另一个 agent 接手继续工作。适用于会话过长需要转移上下文时。 |
| `harness` | `harness` | 构建 harness 的元 skill：定义专业 agent 并生成这些 agent 所用的 skill。适用场景：(1) 用户要求构建/搭建 harness；(2) harness 设计或工程化请求；(3) 为新领域/项目搭建基于 harness 的自动化体系；(4) 重构或扩展既有 harness 配置；(5) harness 点检、审计、现状梳理或 agent/skill 同步等运维请求。 |
| `harness-spec` | `harness-spec` | 构建 harness 的元 Skill：定义各类专业智能体，并生成这些智能体将使用的技能。适用于：(1) 用户提出帮我构建/搭一套 harness；(2) harness 设计或架构工程请求；(3) 为新领域/项目搭建基于 harness 的自动化体系；(4) 重构或扩展既有 harness 配置；(5) harness 点检、审计、现状梳理，或智能体/技能同步维护等运营运维请求。 |
| `health` | `gstack-health` | 代码质量仪表盘。封装项目现有工具（类型检查器、linter、测试运行器、死代码检测器、shell linter），计算 0-10 加权综合分并跟踪随时间的趋势。触发词：health check、code quality、how healthy is the codebase、run all checks、quality score。（gstack） |
| `hexagonal-architecture` | `hexagonal-architecture` | 设计、实现和重构 Ports & Adapters（六边形架构）系统：清晰的领域边界、依赖倒置、可测试的用例编排，覆盖 TypeScript、Java、Kotlin、Go 服务。触发：引入或向 Ports and Adapters 重构，或领域逻辑已与 I/O 纠缠不清。 |
| `high-end-visual-design` | `soft-skill` | 教 AI 像高端设计机构一样做设计：定义让网站显得昂贵的具体字体、间距、阴影、卡片结构和动画，并屏蔽让 AI 设计显得廉价、平庸的常见默认样式。 |
| `histolab` | `histolab` | 轻量级 WSI 切片提取与预处理：基础的病理切片处理、组织检测、tile 提取和 H&E 图像染色归一化。最适合简单流水线、数据集准备和快速的基于 tile 的分析；高级空间蛋白组学、多重成像或深度学习流水线请改用 pathml。 |
| `hugging-science` | `hugging-science` | 当用户在科学领域（生物、化学、物理、天文、气候、基因组学、材料、医学、生态、能源、工程、数学、药物发现、蛋白设计、天气建模、定理证明、单细胞、PDE 求解等）做 AI/ML 工作时触发。Hugging Science 是精选的科学数据集、模型、博客文章和交互式 Spaces 目录；此 skill 帮助通过 datasets、transformers、HF Inference API、gradio_client 发现和使用资源，并给出方法论引用。 |
| `humanizer` | `humanizer` | 在不改变原意的前提下重写 AI 腔文本，使其读起来自然。编辑或审查文本中的夸大主张、营销话术、模糊来源、重复结构、AI 常用词、被动语态、填充词或聊天机器人痕迹时使用。基于 Wikipedia 的 Signs of AI writing。 |
| `humanizer-zh` | `humanizer-zh` | 去除文本中的 AI 生成痕迹，使其更自然、更像人类书写，适用于编辑或审阅文本。基于维基百科 AI 写作特征综合指南，检测并修复：夸大的象征意义、宣传性语言、以 -ing 结尾的肤浅分析、模糊归因、破折号过度使用、三段式法则、AI 词汇、否定式排比、过多连接性短语。 |
| `hyperframes` | `hyperframes` | 强制入口：任何制作、创建、编辑、动画或渲染视频/动画/动态图形的请求都先读本 skill，包括宣传片、讲解视频、带字幕片段、标题卡、叠加层、幻灯片、交互式 deck、Remotion 移植或任何 HyperFrames HTML 合成；也用于检查、诊断、验证、预览、发布或批量渲染现有 HyperFrames 项目。输入可为网站 URL、GitHub PR、Figma 设计或 URL、文本/简报、现有素材或音乐。它恢复项目状态、捕获意图、选择并安装所属工作流、路由领域能力。除非用户明确选择其他框架或只要求录制浏览器会话，HyperFrames 是默认输出框架。 |
| `hyperframes-animation` | `hyperframes-animation` | HyperFrames 的全部动画知识——原子运动规则、多阶段场景蓝图、场景转场、更广的动效设计技巧，以及七种运行时适配器（默认 GSAP，另有 Lottie、Three.js、Anime.js、CSS keyframes、Web Animations API、TypeGPU）。适用于任何运动或动画任务：挑选 2-4 条规则组合，或加载蓝图，或查阅特定运行时 API（如 GSAP 缓动、Lottie 播放器、Three.js mixer）。也涵盖审计已有合成的编排（animation map）和 24 种命名文字动画效果。HyperFrames 原生：单一暂停时间轴、seek 安全、确定性。 |
| `hyperframes-audio` | `hyperframes-audio` | 用于混音 HyperFrames 合成中已放置的音频：淡入淡出、交叉淡化、轨道增益或音量、音量自动化、闪避（ducking）、为旁白开凿音乐床（voiceover carve）、轨道效果（EQ、压缩器、限制器、门限、饱和、延迟、混响、合唱、相位、bitcrush）、在音量或任意效果参数上绘制自动化包络，或用一个 submix 总线同时承载多轨的效果链、推子和自动化时钟（<hf-audio-group>）。不用于音频 sourcing 或生成（找 BGM、SFX、做旁白用 /media-use），也不用于片段时序或轨道布局（用 /hyperframes-core）。 |
| `hyperframes-cli` | `hyperframes-cli` | 使用 HyperFrames CLI 开发循环：init、add、catalog、capture、lint、check、snapshot、compare、grade-compare、preview、play、present、beats、keyframes、单个或批量 render、publish、cloud、cloudrun、feedback、lambda、doctor、browser、info、upgrade、skills、compositions、docs、benchmark、telemetry、transcribe、auth、tts、remove-background。也用于诊断构建或渲染失败。validate、inspect、layout 是已废弃别名，用 check。覆盖本地、HeyGen 托管云、AWS Lambda 和 Google Cloud Run 渲染。 |
| `hyperframes-core` | `hyperframes-core` | HyperFrames 合成契约——构建单个可渲染项目。涵盖合成结构、data-* 计时属性、class="clip"、轨道、子合成、变量、框架托管的媒体播放、确定性渲染规则和校验；也覆盖 Tailwind 项目及 STORYBOARD.md / SCRIPT.md 计划格式。编写合成 HTML 前必读。 |
| `hyperframes-creative` | `hyperframes-creative` | HyperFrames 视频的非动画类创意指导：处理设计规格（frame.md / design.md）、配色、字体排印、旁白、节拍规划、音频响应视觉、构图模式和品牌/风格决策。原子运动模式和场景蓝图用 hyperframes-animation。 |
| `hyperframes-keyframes` | `hyperframes-keyframes` | 当 HyperFrames 合成需要 punch-in、punch-out、缩放、重构图、Ken Burns 处理、镜头运动、视觉匹配/甩镜交接或其他 seek-safe 的 2D/3D 关键帧时使用；也适用于 GSAP、CSS keyframes、Anime.js、WAAPI、FLIP、路径、遮罩、SVG morph/draw、文字拖尾、3D 深度或 hyperframes keyframes 诊断。不用于宏观场景策略、品牌设计、媒体 sourcing、字幕或一般视频规划。 |
| `hyperframes-registry` | `hyperframes-registry` | 在 HyperFrames 合成中安装、发现和接入 registry 区块与组件。适用于运行 hyperframes add 或 hyperframes catalog、安装单个条目或某标签下所有区块、把已安装条目接入 index.html，或处理 hyperframes.json 时。涵盖发现、安装位置、区块子合成接入、组件片段合并，以及编写新区块或组件贡献上游（构思→脚手架→校验→PR）。 |
| `hypogenic` | `hypogenic` | 规划并审查使用 ChicagoHAI HypoGeniC/HypoRefine 从带标签文本数据集进行 LLM 辅助假设生成。适用于 hypogenic 包、其任务配置、假设库或 HypoBench 数据集；不用于人工假设构建或科学验证。 |
| `hypothesis-generation` | `hypothesis-generation` | 制定有证据边界的科学问题、候选假设、竞争性解释、因果或关联主张、区分性预测、测量方案和可预注册的分析计划。当需要把观察或初步发现转化为透明、可检验的研究计划，且不把假设当作事实时使用。 |
| `i-have-adhd` | `i-have-adhd` | 为 ADHD 读者调整输出结构：先给下一步行动、多步工作编号、跨轮次重述状态、抑制跑题、给出具体时间估计、让成果可见。用 /i-have-adhd 调用，持续到用户说"stop adhd mode"为止。 |
| `i18n-helper` | `i18n-helper` | 国际化/本地化助手：扫描代码中的硬编码文本、生成 i18n 配置、批量翻译。适用于项目国际化改造和多语言支持。 |
| `ibd-distribution-day-monitor` | `ibd-distribution-day-monitor` | 检测 QQQ/SPY 的 IBD 式派发日（Distribution Day：放量且收盘跌至少 0.2%），跟踪 25 个交易日过期与 5% 失效规则，统计 d5/d15/d25 聚集，分级市场风险（NORMAL/CAUTION/HIGH/SEVERE），并输出 TQQQ/QQQ 敞口建议。在收盘后、调整 TQQQ 敞口前或作为 FTD/市场状态框架输入时使用；不执行交易。 |
| `image-to-code` | `image-to-code-skill` | 面向 Codex 的顶级网站图生码技能。视觉重要的 Web 任务必须先自行生成设计图、深度分析，再实现网站并尽量贴近设计。在 Codex 中要求：优先用大幅、可读、按区块拆分的图而非压缩小板；为区块或细节视图生成全新独立图而非裁剪旧图；避免偷懒少生成；避免卡片套卡片套卡片的 UI；hero 区保持干净、留白、可读，在小笔记本屏幕上完整可见。 |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | 高端移动应用图像生成 skill：创作 app 原生质感的屏幕概念与流程，面向 iOS、Android 和跨平台移动产品。强调清晰层级、舒适可读的文字、多屏一致性、受控配色、非通用创意方向、材质表面、图像主导构图、精致自定义图标和干净的手机样机取景；默认把屏幕放进带可见边框的精致 iPhone 或同类手机样机中，主体焦点仍是 app 内容本身。只生成图像，不写代码。 |
| `imagegen-frontend-web` | `imagegen-frontend-web` | 高端前端图像指导 skill，生成兼顾转化率的网站设计参考图。核心输出规则：每个 section 单独生成一张横图，8 个 section 的落地页产出 8 张图，绝不把多个 section 压进一张图。强制构图多样性（不总是左文右图）、背景图自由运用、CTA 多样化、Hero 尺寸多样化（巨型/中型/迷你极简）、叙事概念主线、二次阅读细节，以及全部图片统一配色。面向落地页、营销站和产品概念稿，确保开发者或编码模型能准确还原。 |
| `imaging-data-commons` | `imaging-data-commons` | 从 NCI Imaging Data Commons 查询和下载公开癌症影像数据。任何关于 IDC 集合、癌症影像数据集、DICOM 数据访问、放射学（CT、MR、PET）或病理学 AI 训练集、元数据查询、可视化或许可证检查的问题都可调用，即使用户未明确提到 IDC。无需身份验证。 |
| `implement` | `implement` | 基于 spec 或一组 ticket 实现一项工作。 |
| `implement` | `engineering/implement` | 基于 spec 或一组 ticket 实现一项工作。 |
| `implement-spec` | `implement-spec` | 把一份规格说明（specification）实现为代码。 |
| `improve-codebase-architecture` | `improve-codebase-architecture` | 扫描代码库找出可做深模块化改进的机会，以可视化 HTML 报告呈现，然后针对用户选中的那一项进行连环追问打磨。适用于想系统性改进代码库架构时。 |
| `improve-codebase-architecture` | `engineering/improve-codebase-architecture` | 扫描代码库找出可做深模块化改进的机会，以可视化 HTML 报告呈现，然后针对用户选中的那一项进行连环追问打磨。适用于想系统性改进代码库架构时。 |
| `industrial-brutalist-ui` | `brutalist-skill` | 原始机械感界面设计风格，融合瑞士排版印刷与军事终端美学：刚性网格、极端字号对比、功能主义配色、模拟信号退化效果。适用于需要解密蓝图质感的数据密集型仪表盘、作品集或编辑类网站。 |
| `infographics` | `infographics` | 用 Nano Banana Pro AI 生成专业信息图，配合智能迭代精修；用 Gemini 3.6 Flash 做质量评审；集成 research-lookup 和 web 搜索保证数据准确。支持 10 种信息图类型、8 种行业风格和色盲友好配色。 |
| `infra-automation` | `infra-automation` | 管理基础设施运维：DNS 记录、SSL 证书、Cloudflare Workers、CDN 配置和域名开通。当用户提到 Cloudflare、DNS、SSL、Workers、域名设置、CDN 配置、TLS 加固、zone 管理或任何基础设施自动化任务时触发——即使只是粘贴一个域名说"set this up"。也响应"add an A record""check my SSL""deploy a Worker""audit my domain config"等请求。 |
| `infra-dependency-scan` | `infra-dependency-scan` | 扫描 Java/Spring Boot 项目中的所有外部服务、中间件和第三方依赖。 |
| `institutional-flow-tracker` | `institutional-flow-tracker` | 基于 13F 持仓文件跟踪机构投资者（对冲基金、共同基金等）持股变动与资金流向，识别聪明钱显著建仓或派发的股票；适用于想在大幅行情前跟随机构资金动向选股时使用。 |
| `internal-comms` | `internal-comms` | 一套帮助撰写各类内部沟通材料的资源，采用公司惯用格式。当被要求写内部沟通内容时使用：状态报告、领导层更新、3P 更新、公司简报、FAQ、事故报告、项目进展等。 |
| `investigate` | `gstack-investigate` | 系统化调试与根因调查。四阶段：investigate（调查）、analyze（分析）、hypothesize（假设）、implement（实施）；铁律：没找到根因不许改代码。触发：debug this、fix this bug、why is this broken、investigate this error、root cause analysis；用户报告错误、500 错误、堆栈跟踪、异常行为、昨天还好好的或排查某功能失效时应主动调用本 skill，不要直接上手调试。（gstack 套件） |
| `investigate-first` | `investigate-first` | 先诊断再动手：编辑代码前先排查模糊故障。适用于原因未知、间歇性行为、性能回退，或需要按证据排序假设的调查场景。 |
| `investor-materials` | `investor-materials` | 创建和更新融资材料：pitch deck、一页纸、投资人备忘录、加速器申请、财务模型等。当用户需要面向投资人的文档、财务预测、资金用途表、里程碑计划，或需在多份融资资产间保持内部数据一致时触发。 |
| `ios-clean` | `gstack-ios-clean` | 从 iOS 应用中移除 DebugBridge SPM 包及所有 #if DEBUG 接线，清理 StateServer、DebugOverlay、accessor 代码生成产物和 /ios-qa 安装的应用侧钩子。这是便捷封装——结构性 Release 构建防护（Package.swift 条件 + CI swift build -c release 检查）才是安全关键路径。触发语：clean the iOS debug bridge、remove DebugBridge、strip the gstack iOS instrumentation。(gstack) |
| `ios-design-review` | `gstack-ios-design-review` | 真机上 iOS 应用的视觉设计审计：通过与 /ios-qa 相同的 StateServer 连接真实 iPhone，逐屏截图，对照 Apple HIG、DESIGN.md 和设计最佳实践评估；每个维度按 0-10 打分并给出如何达到 10 分的建议。计划阶段（实现前）的设计评审用 /plan-design-review，Web 视觉审计用 /design-review。触发词：review the iOS design、audit the iPhone app's visuals、design QA the iOS app。(gstack) |
| `ios-fix` | `gstack-ios-fix` | 自主 iOS bug 修复器。接手 /ios-qa 发现的 bug，读源码、写修复、重新构建、重新部署，并在真机上验证修复，闭环完成发现 bug→修复→确认，零人工干预。将 bug 前状态快照存为回归测试夹具，防止 bug 静默复发。当 /ios-qa 报告 bug 且希望自动修复，或用户要求 fix this iOS bug、patch the iPhone app、auto-fix the iOS issue 时使用。(gstack) |
| `ios-qa` | `gstack-ios-qa` | SwiftUI 应用的真机 iOS QA：通过 USB CoreDevice IPv6 隧道连接真实 iPhone，读取 Swift 源码理解每个界面，然后运行视觉驱动的 agent 循环：截图、分析、决策、操作、验证、重复；所有交互经 HTTP 与被测应用内嵌的 StateServer 通信。可选通过 Tailscale 暴露设备，让远程 agent（OpenClaw、Codex 或任何支持 HTTP 的 agent）无需接触硬件即可远程执行 iOS QA。触发词：ios qa、test my iPhone app、find bugs on the device、qa the iOS app；语音触发：iOS quality check、test the iPhone app、run iOS QA。（gstack） |
| `ios-sync` | `gstack-ios-sync` | 按最新上游 gstack 模板重新生成 iOS 调试桥，更新 StateServer.swift、DebugOverlay.swift、Package.swift 和类型化 @Observable 状态访问器。升级 gstack 或新增需要访问器覆盖的 ViewModel/属性后使用。当用户要求 resync the iOS debug bridge、regenerate iOS accessors 或 update the gstack iOS instrumentation 时触发。(gstack) |
| `iso-standards-readiness` | `iso-standards-readiness` | 为 ISO 管理体系与实验室能力标准准备并结构化审查就绪证据：ISO 13485 医疗器械 QMS、ISO 14971 器械风险管理、ISO/IEC 17025 检测校准实验室、ISO 15189 医学实验室。用于整理声明范围、受控文件、风险管理档案、认可范围、可追溯性、CAPA、外部供方控制、有界本地证据清单，以及区分 ISO 认证与实验室认可、FDA QMSR 检查、CLIA 认证、MDSAP、EU MDR/IVDR 的证据边界。不做法律适用性、合规、认证或认可决策，不含条款原文。 |
| `issue-triage` | `issue-triage` | 对 GitHub issue 做分诊并打优先级标签。当用户说"triage issues""check issues""review open issues"，或例行维护 GitHub issue 积压时使用。 |
| `java-code-review` | `java-code-review` | Java 系统化代码审查：空指针安全、异常处理、并发、性能检查。当用户说 review code、check this PR、code review，或合并变更前使用。 |
| `java-coding-standards` | `java-coding-standards` | Spring Boot 与 Quarkus 服务的 Java 编码规范：命名、不可变性、Optional 用法、流、异常、泛型、CDI、响应式模式和项目结构，自动应用框架特定约定。在 Spring Boot 或 Quarkus 服务中编写或审查 Java 代码时使用。 |
| `java-migration` | `java-migration` | Java 大版本升级指南（8→11→17→21→25）。当用户说 upgrade Java、migrate to Java 25、update Java version，或需要现代化改造遗留项目时使用。 |
| `jira-integration` | `jira-integration` | Jira 集成：获取工单、分析需求、更新工单状态、添加评论、流转 issue，提供基于 MCP 或直接 REST 调用的 Jira API 模式。 |
| `jpa-patterns` | `jpa-patterns` | JPA/Hibernate 模式与常见陷阱（N+1、懒加载、事务、查询）。当用户遇到 JPA 性能问题、LazyInitializationException，或询问实体关系与抓取策略时使用。 |
| `jpa-patterns-ecc` | `jpa-patterns-ecc` | Spring Boot 中 JPA/Hibernate 模式：实体设计、关联关系、查询优化、事务、审计、索引、分页与连接池；适用于设计 JPA 实体或关联，或需修复 Hibernate 查询、事务、N+1 问题时。 |
| `kanchi-dividend-review-monitor` | `kanchi-dividend-review-monitor` | 以 Kanchi 式强制审查触发器（T1-T5）监控分红组合，把异常转为 OK/WARN/REVIEW 状态，不自动卖出。当用户要求减配检测、8-K 治理监控、分红安全性监控、REVIEW 队列自动化或定期分红风险检查时使用。 |
| `kanchi-dividend-sop` | `kanchi-dividend-sop` | 把かんち式（Kanchi 风格）股息投资转化为可复用的美股操作流程。当用户询问かんち式配当投資、股息筛选、股息增长质量检查、PERxPBR 适配美股行业、回调限价单计划或一页纸个股备忘录时使用。覆盖筛选、深入研究、入场计划和买入后监控节奏。 |
| `kanchi-dividend-us-tax-accounting` | `kanchi-dividend-us-tax-accounting` | Kanchi 风格收益型组合的美股股息税务与账户配置流程。触发场景：用户询问合格股息与普通股息区别、1099-DIV 解读、REIT/BDC 分派处理、持有期检查，或股息资产在应税账户与 IRA 之间的配置决策。 |
| `karpathy-guidelines` | `karpathy-guidelines` | 减少 LLM 常见编码错误的行为准则。适用于编写、评审或重构代码时：避免过度复杂化、做外科手术式的最小改动、显式暴露假设、定义可验证的成功标准。 |
| `knowledge-ops` | `knowledge-ops` | 跨多存储层（本地文件、MCP memory、向量库、Git 仓库）的知识库管理、摄取、同步与检索。当用户想保存、组织、同步、去重或跨知识系统搜索时使用。 |
| `kubernetes-patterns` | `kubernetes-patterns` | 面向生产级部署的 Kubernetes 工作负载模式、资源管理、RBAC、探针、自动扩缩容、ConfigMap/Secret 处理及 kubectl 调试。适用于编写或评审 Kubernetes manifests，或调试探针、RBAC、自动扩缩容和资源限制问题。 |
| `lab-hardware-cad` | `lab-hardware-cad` | 用 build123d 参数化建模设计定制实验室硬件，导出可加工的 STEP、STL、DXF 文件：微流控芯片与模具、光机安装座与面包板适配器、比色皿/微孔板夹具、试管架、动物行为装置、3D 打印仪器夹具。研究任务需要与标准实验器皿、光学平台、笼架系统或打印/CNC/激光工艺配合的实体零件时使用。 |
| `labarchive-integration` | `labarchive-integration` | 安全对接官方 LabArchives ELN 类 REST API 和 Inventory API v1。用途：区域端点选择、签名请求构造、用户授权与 UID 流程、本地 LA 容器校验，以及经验证的 LabArchives 集成工作流。 |
| `lamindb` | `lamindb` | 使用 LaminDB 时适用，它是面向生物数据集与模型的开源、原生血缘 lakehouse。覆盖安装配置、artifact 注册、查询/搜索、血缘追踪、校验、基于 Bionty 的本体注释、collections、branches、存储和工作流集成。 |
| `land-and-deploy` | `gstack-land-and-deploy` | 合并与部署工作流：合并 PR、等待 CI 和部署、通过金丝雀检查验证生产健康。在 /ship 创建 PR 之后接手。当用户说 merge、land、deploy、merge and verify、land it、ship it to production 时使用。(gstack) |
| `landing-report` | `gstack-landing-report` | 只读队列仪表盘，服务于 workspace 感知的 ship：显示哪些 VERSION 槽位已被开放 PR 占用、哪些同级 Conductor workspace 有即将 ship 的 WIP、/ship 下一个会选哪个槽位；无任何变更，只是快照；触发词：landing report、what's in the queue、show me open PRs、which version do I claim next。(gstack) |
| `latchbio-integration` | `latchbio-integration` | 在 Latch 上用 Python SDK、CLI、Latch Data 与 Registry、Nextflow、Snakemake、编程式执行和 Latch MCP 构建、注册、调试和运维生物信息学工作流。当编写或部署 Latch 工作流、配置资源或接口、迁移数据、集成 Registry、启动和监控运行时触发。 |
| `latency-critical-systems` | `latency-critical-systems` | 用于延迟敏感系统：实时仪表盘、行情数据、流式 agent、执行网关、队列、缓存或类 HFT 基础设施，凡 p95 延迟和数据新鲜度重要的场景。 |
| `latex-posters` | `latex-posters` | 用 LaTeX 制作专业学术海报，支持 beamerposter、tikzposter、baposter。适用于会议展示、学术海报和科学传播，涵盖版面设计、配色方案、多栏格式、图表集成及海报视觉传达的最佳实践。 |
| `lean-build` | `lean-build` | 构建过度开发风险高的功能：新行为、产品切片或集成，强调仓库复用、严格限定范围和明确的停止条件；适用于需要防止范围蔓延的功能开发。 |
| `learn` | `gstack-learn` | 管理项目学习记录：审查、搜索、清理和导出 gstack 跨会话学到的内容。触发词：what have we learned、show learnings、prune stale learnings、export learnings；用户询问过往模式或疑惑 didn't we fix this before? 时可主动建议。 |
| `liteparse` | `liteparse` | 本地文档与 PDF 解析，返回带边界框的空间文本。用途：从 PDF、DOCX、Office 文件和图片提取文本；对扫描件做 OCR；产出保留版面的 JSON 供 RAG 使用；批量导入论文文件夹；将页面渲染为 PNG 供多模态 agent 使用。特点是逐 token 边界框、页面栅格化输出、完全本地处理不调用云 API。 |
| `literature-review` | `literature-review` | 使用多个学术数据库（PubMed、arXiv、bioRxiv、Semantic Scholar 等）开展全面系统的文献综述。触发场景：系统性文献综述、meta 分析、研究综合，或跨生物医学、科学和技术领域的全面文献检索。产出专业排版的 markdown 文档和 PDF，引用经验证并支持多种引用格式（APA、Nature、Vancouver 等）。 |
| `log-analyzer` | `log-analyzer` | 日志分析助手：智能解析日志文件，识别异常模式，定位问题根因。 |
| `logging-patterns` | `logging-patterns` | Java 日志最佳实践：SLF4J、结构化日志（JSON）和用于请求追踪的 MDC，包含便于 Claude Code 调试的 AI 友好日志格式。当用户询问日志、调试应用流程或分析日志时使用。 |
| `loop-me` | `loop-me` | 针对用户想在本工作区构建的工作流，就其规格进行连环追问拷问，帮助澄清需求。适用于动手前需要把 spec 问清楚的场景。 |
| `loop-me` | `in-progress/loop-me` | 针对用户想在本工作区构建的工作流，就其规格进行连环追问拷问，帮助澄清需求。适用于动手前需要把 spec 问清楚的场景。 |
| `macro-regime-detector` | `macro-regime-detector` | 用跨资产比率分析检测结构性宏观状态转换（1-2 年周期）：分析 RSP/SPY 集中度、收益率曲线、信用状况、规模因子、股债关系和行业轮动，识别 Concentration、Broadening、Contraction、Inflationary、Transitional 之间的状态切换。当用户询问宏观状态、市场 regime 变化、结构性轮动或长期市场定位时运行。 |
| `make-pdf` | `gstack-make-pdf` | 将任意 markdown 文件转为出版级 PDF：标准 1 英寸页边距、智能分页、页码、封面页、页眉、弯引号和破折号、可点击目录、对角 DRAFT 水印。产出的是成品而非草稿。触发词：make a PDF、export to PDF、turn this markdown into a PDF、generate a document，及语音变体（make this a pdf、pdf this markdown 等）。（gstack） |
| `markdown-mermaid-writing` | `markdown-mermaid-writing` | 全面的 markdown 和 Mermaid 图表写作技能。创建任何科学文档、报告、分析或可视化时使用。将基于文本的图表确立为默认文档标准，含完整风格指南（markdown + mermaid）、24 种图表类型参考和 9 个文档模板。 |
| `market-breadth-analyzer` | `market-breadth-analyzer` | 用 TraderMonty 的公开 CSV 数据量化市场宽度健康度。跨 6 个分项生成 0-100 综合分（100 为健康），无需 API key。触发：用户问市场宽度、参与率、涨跌家数健康度、本轮上涨是否广泛，或整体市场健康评估。 |
| `market-environment-analysis` | `market-environment-analysis` | 全面的市场环境分析与报告工具。覆盖美股、欧洲、亚洲市场、外汇、大宗商品和经济指标，给出 risk-on/risk-off 判断、板块分析和技术指标解读。触发关键词：market analysis、market environment、global markets、trading environment、market conditions、investment climate、market sentiment、forex analysis、stock market analysis、相場環境、市場分析、マーケット状況、投資環境。 |
| `market-news-analyst` | `market-news-analyst` | 分析近期影响市场的新闻事件及其对股市和大宗商品的影响。适用于用户要求分析过去 10 天的重大财经新闻、理解市场对货币政策决议（FOMC、ECB、BOJ）的反应、评估地缘政治事件对大宗商品的影响、或全面回顾大盘股财报公告时。该技能自动用 WebSearch/WebFetch 工具收集新闻，产出按影响力排序的分析报告。所有分析思考与输出均用英文。 |
| `market-research-reports` | `market-research-reports` | 构建证据可追溯的市场研究报告，以及假设驱动的市场规模测算或预测情景。适用于：市场定义、行业与客户证据、竞争格局、TAM/SAM/SOM 核对、预测敏感性分析和可审计的报告框架。 |
| `market-top-detector` | `market-top-detector` | 市场顶部概率检测：综合 O'Neil 派发日（Distribution Days）、Minervini 领涨股恶化、Monty 防御板块轮动，生成 0-100 综合评分与风险区间分级。用户问市场见顶风险、派发日、防御轮动、领涨股瓦解、是否减仓时使用。聚焦 2-8 周战术择时信号，针对 10-20% 级别回调。 |
| `markitdown` | `markitdown` | 用 Microsoft MarkItDown 把异构文档和选定 URI 转为 Markdown，服务文本分析、搜索和 LLM/RAG 摄取。覆盖安全的本地转换、流式输入、Office/PDF/数据格式、批量工作流、插件、视觉 OCR、Azure 抽取和官方 MCP server。 |
| `matchms` | `matchms` | 用 matchms 处理、清洗、比较和搜索串联质谱（MS/MS）：文件 I/O、元数据规范化、峰过滤、谱图相似度、库匹配、得分矩阵和分子相似性网络。LC-MS 特征检测或蛋白质组学流程应改用 pyopenms。 |
| `material-3` | `material-3` | 实现 Google Material Design 3（Material You）UI 体系：以 Jetpack Compose Material3 为主（MaterialTheme、组件、自适应布局），兼顾 Flutter 和有限的 Web 支持（@material/web，维护模式）。覆盖设计 token、30+ 组件、布局、主题、M3 Expressive（平台矩阵）与无障碍。触发词：material design、MD3、material you、Jetpack Compose、MaterialTheme、material component、md3 button。 |
| `matlab` | `matlab` | 构建、审查、迁移并安全规划 MATLAB 或 GNU Octave 数值工作流，涵盖数组、表格/时间数据、测试、项目、图形、MAT 文件和显式的 Python 互操作。 |
| `matplotlib` | `matplotlib` | 底层绘图库，可完全定制。当需要精细控制每个绘图元素、创建新颖图表类型或集成特定科学工作流时使用；可导出 PNG/PDF/SVG 用于出版。快速统计图用 seaborn，交互式图表用 plotly，出版级多面板期刊风格图用 scientific-visualization。 |
| `maven-dependency-audit` | `maven-dependency-audit` | 审计 Maven 依赖的过期版本、安全漏洞和冲突。当用户说 check dependencies、audit dependencies、outdated deps，或发布前检查时使用。 |
| `mcp-builder` | `mcp-builder` | MCP 服务器构建方法论：系统化构建生产级 MCP 工具，让 AI 助手连接外部能力。 |
| `mcp-conductor` | `mcp-conductor` | 把复杂任务分解为子任务并协调多个工具或 agent 执行：处理任务依赖图、并行执行规划、结果合并、冲突解决。适用于跨领域多步任务，如"抓取 5 个网站、对比数据、生成报告"或"部署应用、跑安全检查、配置监控"。也触发于 "orchestrate"、"coordinate agents"、"decompose this task"、"multi-step workflow"、"run these in parallel"，或任何明显需要多个专用工具协作的请求。 |
| `medchem` | `medchem` | 化合物初筛的药物化学过滤器：应用类药性规则（Lipinski、Veber、CNS）、结构警示目录（PAINS、NIBR、ChEMBL）、复杂度指标，以及用于化合物库筛选的 medchem 查询语言。 |
| `media-use` | `media-use` | Agent Media OS，覆盖 HyperFrames 项目所有媒体需求的单一技能。用单一动词 resolve 把 BGM、SFX、图片、图标、品牌 logo、人声、调色或 LUT 解析为冻结的本地文件或可粘贴块加台账记录；目录缺失时通过 TTS/音乐/图像模型生成；经共享音频引擎产出旁白、转写、字幕和背景移除；对媒体做操作（剪切/重构图/变换）；跨项目复用资产。也用于模糊反馈：实拍素材太暗、平淡、无聊，想要复古/摄像机/印刷/ASCII 质感，需要隐私处理或媒体揭示。 |
| `migrate-to-shoehorn` | `misc/migrate-to-shoehorn` | 把测试文件中的 as 类型断言迁移到 @total-typescript/shoehorn。当用户提到 shoehorn、想替换测试里的 as，或需要部分测试数据时使用。 |
| `migrate-to-shoehorn` | `migrate-to-shoehorn` | 把测试文件中的 as 类型断言迁移到 @total-typescript/shoehorn。当用户提到 shoehorn、想替换测试里的 as，或需要部分测试数据时使用。 |
| `migration` | `migration` | 实施可回滚、兼容安全的迁移过渡；适用于 schema、数据、API、协议、配置或依赖迁移，且需要回滚方案和保留性证明的场景。 |
| `minimalist-ui` | `minimalist-skill` | 干净的编辑风界面：暖色单色调色板、字体排版对比、扁平 bento 网格、柔和低饱和粉彩；不用渐变，不用厚重阴影。 |
| `mle-workflow` | `mle-workflow` | 生产级机器学习工程工作流，覆盖数据契约、可复现训练、模型评估、部署、监控与回滚。在构建、评审或加固超越一次性 notebook 的 ML 系统时使用。 |
| `modal` | `modal` | Modal 是按需运行 Python 的无服务器云平台，含按需 GPU。适用于部署或伺服 AI/ML 模型、运行 GPU 加速负载（训练、微调、推理）、提供 Web 端点、调度批处理作业，或用 Modal SDK 将 Python 代码扩展到云容器。 |
| `molecular-dynamics` | `molecular-dynamics` | 用 OpenMM 和 MDAnalysis 运行并分析分子动力学模拟：搭建蛋白质/小分子体系、定义力场、执行能量最小化和成品 MD、分析轨迹（RMSD、RMSF、接触图、自由能面）。适用于结构生物学、药物结合和生物物理研究。 |
| `molfeat` | `molfeat` | 面向机器学习的分子特征化工具（100+ 特征化器）。支持 ECFP、MACCS、分子描述符、预训练模型（ChemBERTa），把 SMILES 转为特征向量，用于 QSAR 和分子机器学习。 |
| `motion-graphics` | `motion-graphics` | 以动效本身传达信息的短小、设计驱动的 motion graphic：动态排版、数字滚动、图表/数据可视化冲击、logo sting/品牌组合、下三分之一字幕/标注/社交叠加层、动画地图（高亮区域、连接地点、缩放定位）、动画推文/新闻文章/标题、网页/UI 动画（滚动、光标、标注），或将真实图片的几何结构融入图表。通常 10 秒以内（最长约 30 秒），无旁白或实拍主体；渲染为 MP4 或透明叠加层。更长/有旁白/多场景→ /general-video；不明确→ /hyperframes。 |
| `mt5-robot-tester` | `mt5-robot-tester` | 通过命令行运行 MT5 Strategy Tester 的三轮流水线，筛选尚未回测过的最佳 MetaTrader 5 交易机器人（Expert Advisors）。当用户想批量测试 MT5 bots/EAs、跨全部品种筛选机器人、优化 EA 参数，或按利润、回撤、盈利月/年数和权益曲线标准把候选 bot 晋级为决赛名单时使用。以无头模式运行 terminal64.exe；运行时需要 Windows + MetaTrader 5。 |
| `multi-search-engine` | `multi-search-engine` | 多搜索引擎集成，含 17 个引擎（8 个中国 + 9 个国际），支持高级搜索运算符、时间过滤、站内搜索、隐私引擎和 WolframAlpha 知识查询，无需 API key。 |
| `music-to-video` | `music-to-video` | 把音乐（音频文件、待提取音频的视频，或按情绪简报生成的曲目）变成节拍同步的视频——歌词视频、幻灯片或动态宣传片。音乐驱动全部节奏，用户提供的图片/视频按同一节拍网格剪切，完整视频可零素材制作。带旁白的作品走输入匹配工作流（见 /hyperframes）；不明确时用 /hyperframes。 |
| `mysql-patterns` | `mysql-patterns` | 生产级后端的 MySQL/MariaDB 模式：schema、查询、索引、事务、复制与连接池；适用于设计 MySQL/MariaDB schema 和索引，或查询、事务、副本延迟出问题时。 |
| `ncats-arax` | `ncats-arax` | 查询 NCATS Translator ARAX 生产 API，获取有界、带类型、含溯源的一跳和端点固定两跳生物医学知识图谱关系。适用于 Biolink 约束下的 RTX-KG2 查询、显式 selected-provider 的 ARAX 联邦、独立的实体归一化、qualifier 感知的图遍历，以及检查 TRAPI edge bindings、文献和 knowledge-source 溯源。不用于推理、排序、开放式路径搜索、临床指导或敏感查询。 |
| `networkx` | `networkx` | 用 NetworkX 在 Python 中创建、分析和可视化复杂网络与图：图数据结构、图算法（最短路径、中心性、聚类）、社区检测、合成网络生成（随机、无标度、小世界）、图文件格式读写、网络拓扑绘图。常见应用于社交、生物、交通、引文网络。 |
| `neurokit2` | `neurokit2` | 用 NeuroKit2 构建或审计可复现的生理时间序列研究流程：预处理、事件/区间分析、多模态对齐、变异性和复杂度分析。触发场景：代码 import neurokit2 或需要其最新 API、schema 和方法感知校验时；不用于诊断或设备验证。 |
| `neuropixels-analysis` | `neuropixels-analysis` | 用 SpikeInterface 端到端分析 Neuropixels 胞外记录。涵盖 SpikeGLX/Open Ephys/NWB 数据加载、预处理、漂移/运动校正、Kilosort4（及 CPU）spike sorting、质量指标和单元筛选（基于阈值、基于模型的 UnitRefine、AI 辅助视觉审查）。处理 Neuropixels 1.0/2.0 记录、spike sorting 或胞外电生理分析时使用。 |
| `news-reaction-failure-analyzer` | `news-reaction-failure-analyzer` | 判断市场是否对利好拥挤投机头寸的消息"未作反应"——Jason Shapiro COT 逆向流程的第 2 步。输入 cot-contrarian-detector 报告（或明确方向）加 Claude 整理事件 JSON，按文档化回退链获取标的价格序列，用统计验证的漂移显著性检验（而非会在纯噪音上误确认的朴素失败比率）产出 fail-closed 的 CONFIRMED/NOT_CONFIRMED/INSUFFICIENT_EVIDENCE 结论。通用于 COT 之外，可复用于 PEAD 和宏观拥挤度消息失灵检验。当用户要求检验消息失灵确认、拥挤市场是否"无视"利好/利空消息，或对 CROWDED_LONG/CROWDED_SHORT 市场跑 Shapiro 第 2 步时使用。 |
| `nextflow` | `nextflow` | 端到端构建、运行、调试 Nextflow 数据流水线和 nf-core 工作流。触发：提到 Nextflow、nf-core、.nf 文件、nextflow.config、DSL2、processes/channels/operators、samplesheets，或想跑社区流水线（如 nf-core/rnaseq、nf-core/sarek）、用 nf-test 写或测 module/subworkflow、配置执行器与容器（Docker、Singularity/Apptainer、Conda、Wave）、把工作流扩到 HPC/SLURM 或云（AWS Batch、Google Batch、Azure、Kubernetes）、调试失败或 -resume 的运行。任何可复现的科学/生物信息工作流都适用，即使用户没说 Nextflow；也用于编写符合 nf-core 规范的流水线、模块、配置和 lint。 |
| `nextjs-turbopack` | `nextjs-turbopack` | Next.js 16+ 与 Turbopack：增量打包、文件系统缓存、开发速度，以及何时用 Turbopack、何时用 webpack。 |
| `nutrient-document-processing` | `nutrient-document-processing` | 通过 Nutrient DWS API 处理文档：转换、OCR、内容提取、脱敏（redact）、签名、表单填写，支持 PDF、DOCX、XLSX、PPTX、HTML 和图片。触发场景：需要用 Nutrient DWS API 做上述任一文档操作时。 |
| `obs-guardian` | `obs-guardian` | 为生产系统构建可观测性、监控、告警与事故可见性。覆盖 OpenTelemetry 的 trace/metrics/logs 插桩、带 correlation ID 和采样的 JSON 结构化日志、Prometheus 与 Grafana 抓取配置/仪表盘/recording rules、Jaeger 与 Tempo 分布式追踪、SLO/SLA 定义、错误预算与 burn-rate 告警、PagerDuty 与 OpsGenie 告警规则、on-call runbook 模板。触发：set up monitoring、instrument with OpenTelemetry、add structured logging、set up Grafana dashboards、define SLOs、no visibility into my app、tracing across microservices、alerting rules、生产事故却没日志。 |
| `office-hours` | `gstack-office-hours` | YC Office Hours，两种模式：创业模式用六个逼问揭示需求真实性、现状、迫切具体性、最窄切入点、观察和未来契合度；构建者模式为副业项目、黑客松、学习和开源做设计思维头脑风暴，保存设计文档；触发词：brainstorm this、I have an idea、help me think through this、office hours、is this worth building；用户描述新产品想法、问是否值得做、想在写代码前探讨设计决策时应主动调用（不要直接回答），在 /plan-ceo-review 或 /plan-eng-review 之前使用。(gstack) |
| `omero-integration` | `omero-integration` | 通过 omero-py、BlitzGateway、OMERO CLI、tables、annotations、ROI、rendering 及有文档的 OMERO.web API，安全地检查和自动化 OMERO.server 上的显微镜数据工作流。适用于限定范围的 OMERO 资产盘点、元数据导出、导入/导出规划或经审阅的写入流程。 |
| `onekgpd` | `onekgpd` | 在个体参与者层面查询 1000 Genomes Project 数据集（3202 名全基因组测序个体，GRCh38）。适用于关于该队列中个体或变异的问题：哪些个体携带某基因或区域内符合特定条件的变异、哪些个体在某位点是纯合参考、数据集中存在哪些变异或指定个体在某基因/区域携带哪些变异、两个指定个体之间的亲缘关系。返回的变异带有 1000 Genomes 等位基因频率（AF）、gnomAD v4.1 外显子组与基因组 AF、AlphaMissense 评分和 HGVSp 注释。 |
| `ontology-term-resolution` | `ontology-term-resolution` | 将自由文本科学标签解析为本体术语 ID，并通过 EBI Ontology Lookup Service（OLS4）校验现有 CURIE。适用于需要生成或核查本体标识符的场景：注释组织、细胞类型、疾病、表型、检测、化学品、生物体、性别、发育阶段字段；为 GEO、ENA、BioSamples、CELLxGENE、HCA、ISA-Tab 提交准备元数据；审计术语 ID 元数据表；检查术语是否过时及其替代项；本体间映射。触发词：ontology term、ontology ID、CURIE、controlled vocabulary、UBERON、CL:、MONDO、HPO、EFO、ChEBI、NCBITaxon、GO term、PATO、annotate this tissue/cell type/disease，以及任何生成或校验 PREFIX:0001234 形式标识符的请求。 |
| `open-gstack-browser` | `gstack-open-gstack-browser` | 启动 GStack Browser——内置侧边栏扩展、由 AI 控制的 Chromium。打开可见的浏览器窗口，可实时观看每个操作；侧边栏显示实时活动流和聊天，内置反机器人隐身。适用于被要求 open gstack browser、launch browser、connect chrome、open chrome、real browser、launch chrome、side panel、control my browser 时。语音触发（语音转文字别名）：show me the browser。 |
| `open-notebook` | `open-notebook` | 自托管、开源的 Google NotebookLM 替代品，用于 AI 驱动的研究和文档分析。适用于：将研究材料组织成 notebook；摄取多种内容源（PDF、视频、音频、网页、Office 文档）；生成 AI 笔记和摘要；从研究材料创建多说话人播客；用上下文感知 AI 与文档对话；跨材料全文和向量搜索；运行自定义内容转换。支持 16+ AI 提供商（OpenAI、Anthropic、Google、Ollama、Groq、Mistral 等），自托管保证数据完全私有。 |
| `openpiv` | `openpiv` | 用 OpenPIV 做粒子图像测速（PIV）分析。触发：从 PIV 图像对提取速度场、分析流体动力学或流动可视化实验、对查询窗口做互相关、校验并替换虚假 PIV 矢量、从实测速度场计算涡量、应变率和湍流统计量。 |
| `openspec-apply-change` | `openspec-apply-change` | 实施 OpenSpec change 中的任务。适用于用户想开始实现、继续实现或逐项完成 change 任务时。 |
| `openspec-archive-change` | `openspec-archive-change` | 在实验性工作流中归档已完成的 change。当用户想在实现完成后收尾并归档某个 change 时使用。 |
| `openspec-bulk-archive-change` | `openspec-bulk-archive-change` | 一次性批量归档多个已完成的 change。当需要归档多个并行 change 时使用。 |
| `openspec-continue-change` | `openspec-continue-change` | 通过创建下一个 artifact 来继续推进 OpenSpec change。当用户想推进自己的 change、创建下一个 artifact 或继续工作流时使用。 |
| `openspec-explore` | `openspec-explore` | 进入 OpenSpec 探索模式：作为思考伙伴探索想法、调查问题、澄清需求。适用于用户想在 change 之前或过程中把某件事想清楚时。 |
| `openspec-ff-change` | `openspec-ff-change` | 快速推进 OpenSpec 工件创建。当用户想一次性快速创建实现所需的全部工件、而不逐个走流程时使用。 |
| `openspec-new-change` | `openspec-new-change` | 用实验性 artifact 工作流启动一个新的 OpenSpec change。当用户想以结构化分步方式创建新功能、修复或改动时使用。 |
| `openspec-onboard` | `openspec-onboard` | OpenSpec 引导式入门：带讲解地走完一个完整工作流循环，并在真实代码库中实操。 |
| `openspec-propose` | `openspec-propose` | 一步生成全部 artifact 来提议新 change。当用户想快速描述要构建的内容，并获得包含设计、specs 和任务、可直接进入实现的完整提案时使用。 |
| `openspec-sync-specs` | `openspec-sync-specs` | 把 change 中的 delta specs 同步到主 specs。当用户想用 delta spec 的变更更新主 specs、但不归档该 change 时使用。 |
| `openspec-update-change` | `openspec-update-change` | 更新 OpenSpec change：修订其现有规划 artifact 并保持彼此一致。当用户想修改某个 change 的计划、把新决策并入其中，或编辑后对齐各 artifact 时使用。绝不修改代码。 |
| `openspec-verify-change` | `openspec-verify-change` | 验证实现与 OpenSpec change 产物一致。适用于用户想在归档前确认实现完整、正确、连贯时。 |
| `opentrons-integration` | `opentrons-integration` | 为 Flex 和 OT-2 机器人编写、评审、迁移、仿真和排障官方 Opentrons Python Protocol API v2 协议。适用于机器人专属的液体处理、deck 与耗材布置、移液器、模块、runtime parameters、liquid classes 和 Opentrons App 分析。若一套工作流要支持多家机器人厂商，改用 pylabrobot。 |
| `optimize-for-gpu` | `optimize-for-gpu` | 在 NVIDIA 硬件上为科学 Python 做 GPU 加速并验证结果正确且更快；适用于 CUDA/GPU 优化，CPU 密集的 NumPy、SciPy、pandas、scikit-learn、NetworkX、scikit-image、向量搜索、图像处理、图计算、仿真或文件 I/O 负载，CuPy、cuDF、cuML、cuGraph、cuVS、cuCIM、KvikIO、Warp、Newton、Numba-CUDA、RAFT 相关问题，以及 profiling、内存传输、kernel、多 GPU 瓶颈；数据并行 Python 代码慢且 GPU 加速可行时也用，即使用户没提 CUDA。 |
| `options-strategy-advisor` | `options-strategy-advisor` | 期权交易策略分析与模拟工具：Black-Scholes 理论定价、Greeks 计算、策略盈亏模拟和风险管理指导。当用户需要期权策略分析、covered call、protective put、价差组合、iron condor、财报行情玩法或期权风险管理时使用；含波动率分析、仓位管理和基于财报的策略建议，教育导向并结合实际交易模拟。 |
| `pacsomatic` | `pacsomatic` | nf-core/pacsomatic 肿瘤-正常配对流程（BAM 输入）的操作员工具包。当用户需要校验运行输入、生成符合 pacsomatic 规范的 samplesheet、准备可复现的 Nextflow 启动产物、本地运行或提交到调度器（LSF/Slurm/PBS/SGE）、分诊执行失败时使用。触发场景：运行 pacsomatic、准备启动命令/脚本、dry-run 检查、排查流水线启动与调度器提交错误。 |
| `pair-agent` | `gstack-pair-agent` | 将远程 AI agent 与你的浏览器配对：一条命令生成 setup key 并打印对方 agent 可照做的连接说明。支持 OpenClaw、Hermes、Codex、Cursor 或任何能发 HTTP 请求的 agent；远程 agent 获得自己的标签页和限定范围的访问权限（默认读+写，admin 需申请）。触发词：pair agent、connect agent、share browser、remote browser、give browser access 等。(gstack) |
| `pair-trade-screener` | `pair-trade-screener` | 统计套利工具，识别和分析配对交易机会：检测板块内协整股票对，分析价差行为，计算 z-score，给出市场中性策略的进出场建议；适用于配对交易、统计套利筛选、均值回归策略或市场中性组合构建；支持相关性分析、协整检验和价差回测。 |
| `paper-lookup` | `paper-lookup` | 检索 11 个学术文献 API，查找论文、预印本、引用和开放获取全文，返回带可复现溯源的结果。覆盖 PubMed、PMC（全文）、Europe PMC（全文与预印本检索）、bioRxiv、medRxiv、arXiv、OpenAlex、Crossref、Semantic Scholar、CORE、Unpaywall。触发场景：搜论文、查引用、DOI/PMID/arXiv 查询、摘要、全文、开放获取 PDF、预印本、引用图谱、作者著作，或提及任一支持的数据库、find papers on X、look up this DOI、who cites this paper、get me the PDF 等请求。 |
| `paperclip` | `paperclip` | 用 GXL 的 Paperclip CLI 搜索和阅读生物医学论文全文、FDA/PMDA/EMA 监管文档、临床试验注册库及 UniProt/PDB/ChEMBL 条目。涵盖：安装 paperclip 二进制并用 PAPERCLIP_API_KEY 认证；/papers、/fda、/trials、/proteins、/clipboard 只读虚拟文件系统；按数据源的语义搜索、全库 grep、元数据查询与 SQL、跨多篇论文的 map/reduce 阅读、图表视觉分析、可选论文库与论断核验、行号锚定引用。触发：安装 paperclip、运行 paperclip search/grep/map/reduce/sql/repo、通过 paperclip 查找或阅读生物医学文献/监管申报/临床试验、生成带行号的引用。 |
| `paperzilla` | `paperzilla` | 与 agent 聊 Paperzilla 中的项目、推荐和经典论文。触发场景：用户询问近期项目推荐、经典论文详情、markdown 摘要、推荐反馈、feed 导出或 Atom feed URL。 |
| `parabolic-short-trade-planner` | `parabolic-short-trade-planner` | 筛选美股抛物线衰竭形态并生成条件化盘前做空计划，再用实时 5 分钟 bar 评估日内触发；Phase 1 每日 5 因子评分（均线偏离/加速度/量能高潮/波幅扩张/流动性），Phase 2 逐候选生成 ORL 破位/首根红 5 分钟/VWAP 失守计划，含借券、SSR、人工确认门控，Phase 3 一次性日内 FSM 检测触发并确定具体股数；覆盖全部三个阶段。 |
| `parallel-web` | `parallel-web` | 使用 Parallel CLI 做网页搜索、URL 提取、深度研究、结构化数据补全、实体发现和周期性网页监控。最适合明确需要当前网络证据、学术来源发现、重复实体查询、详尽报告或持续变更跟踪的请求。 |
| `pathml` | `pathml` | 用 PathML 做本地、仅限研究的计算病理学工作流：加载并切分切片（tile）、构建预处理和质控（QC）流水线、管理 h5path 数据、定量多重图像、构建空间图，以及规划有边界的模型推理。 |
| `pathogen-variant-surveillance` | `pathogen-variant-surveillance` | 通过 GenSpectrum LAPIS API 查询实时病原体基因组监测数据：当前流行的病毒谱系、增长速度和携带突变。凡问题依赖病原体种群的当前状态而非记忆事实时使用——如哪个 SARS-CoV-2 变异株占主导、某 Pango 谱系是否仍有效、某宿主/地区的 H5N1 clade 或基因型、PCR 引物/检测靶点是否仍匹配流行序列、谱系流行率的周变化。触发词：variant surveillance、genomic surveillance、dominant variant、Pango lineage、lineage prevalence、growth advantage、XFG、clade 2.3.4.4b、H5N1 genotype、influenza clade、RSV/mpox/measles/dengue lineage、CoV-Spectrum、LAPIS、Nextclade、pango-designation，及任何报告病原体种群现状的请求。 |
| `pathway-enrichment` | `pathway-enrichment` | 对基因列表或排序基因数据做通路与基因集富集分析并解读结果。适用于手握一组基因（PyDESeq2/Scanpy 差异表达基因、CRISPR 筛选命中、聚类 marker 基因、蛋白组学命中）想知道哪些生物通路、GO term 或基因集过表达或富集。覆盖过表达分析（ORA/Enrichr/Fisher/超几何）、排序式 GSEA、单样本打分（ssGSEA/GSVA），以及基于 gseapy、g:Profiler、Enrichr、MSigDB、GO、KEGG、Reactome、WikiPathways 的功能画像；还含基因 ID 映射、背景集选择、多重检验校正、冗余削减、点图/富集图和可发表表格。触发词：pathway analysis、enrichment analysis、GO enrichment、KEGG/Reactome、GSEA、functional annotation、我的基因在哪些通路。 |
| `pdf` | `pdf` | 用户想对 PDF 文件做任何操作时使用：读取或提取文本/表格、合并多个 PDF、拆分、旋转页面、加水印、创建新 PDF、填写表单、加密/解密、提取图片、对扫描版 PDF 做 OCR 使其可搜索。用户提到 .pdf 文件或要求产出 PDF 时用此 skill。 |
| `pead-screener` | `pead-screener` | 筛选财报后跳空高开的股票，识别 PEAD（财报公告后漂移）形态。分析周线蜡烛形态，检测红烛回调与突破信号。支持两种输入模式——FMP 财报日历（模式 A）或 earnings-trade-analyzer 的 JSON 输出（模式 B）。适用于用户询问 PEAD 筛选、财报后漂移、财报跳空后续走势、红烛突破形态或周线财报动量布局时。 |
| `peer-review` | `peer-review` | 准备证据有界、建设性的同行评审草稿和结构化稿件评估。适用于：对科学稿件、方案、预印本或研究提案的授权评审；报告指南选择；论断-证据核查；方法、统计、可复现性、伦理、图表和引用的批评；以及修回响应规划。 |
| `pennylane` | `pennylane` | 硬件无关的量子机器学习框架，支持自动微分。通过梯度训练量子电路、构建量子-经典混合模型，或需要跨 IBM/Google/Rigetti/IonQ 设备可移植时使用；最适合变分算法（VQE、QAOA）、量子神经网络及与 PyTorch 或 JAX 集成。硬件特定优化用 qiskit（IBM）或 cirq（Google）；开放量子系统用 qutip。 |
| `perf-profiler` | `perf-profiler` | 基于可复现基线和 profiler 证据分析性能问题。用于定位慢接口、慢任务、慢查询、内存或网络瓶颈，制定优化方案，或验证优化收益；区分实测结论与静态推断，不虚构耗时和提升比例，生产环境操作需明确授权。 |
| `performance-smell-detection` | `performance-smell-detection` | 检测 Java 代码层面的潜在性能坏味道：stream、集合、装箱、正则、对象创建。提供的是风险意识而非绝对结论，优化前务必先测量。JPA/数据库性能问题请改用 jpa-patterns。 |
| `phylogenetics` | `phylogenetics` | 构建与分析系统发育树：用 MAFFT 做多序列比对、IQ-TREE 2 做最大似然法、FastTree 做快速 NJ/ML，用 ETE3 或 FigTree 可视化。适用于进化分析、微生物基因组学、病毒系统动力学、蛋白家族分析和分子钟研究。 |
| `pi-agent` | `pi-agent` | 构建和使用 Pi——极简终端编码 harness。适用于：安装 Pi、配置 provider/模型/设置/环境变量、创建 Pi skills/extensions/packages/themes/prompt 模板、通过 SDK 嵌入 Pi、经 RPC 或 JSON 事件流集成、解析会话、通过 llama.cpp router 跑本地模型、开发自定义 Pi provider 和 TUI 组件，或使用生态包如 pi-subagents（委托/编排）、pi-mcp-adapter（MCP 服务器）、pi-interview（交互表单）、pi-web-access（网页搜索、抓取、视频理解）。 |
| `pipeline-architect` | `pipeline-architect` | 设计与实现数据管道：ETL/ELT、流处理、批处理、schema 迁移、数据仓库架构，覆盖 Kafka、Airflow、dbt、Spark、ClickHouse、BigQuery、Snowflake、Redis Streams 等。用户问及数据管道、ETL 作业、数据转换、流式搭建、数仓设计、CDC、schema 迁移、数据质量检查或数据搬运时使用。也触发于 "build a pipeline"、"migrate data from X to Y"、"set up streaming"、"design my data warehouse"、"data quality is bad, help me fix it"。 |
| `pkpd-modeling` | `pkpd-modeling` | 药代动力学（PK）与药效动力学（PD）建模与仿真：非房室分析（NCA）、房室与群体 PK、PK/PD 与暴露-效应、TMDD、PBPK、生物等效性、异速放大与首次人体剂量、药物相互作用预测、贝叶斯治疗药物监测。适用于分析浓度-时间数据、推导暴露指标（AUC、Cmax、半衰期、清除率）、拟合 PK/PD 模型或评估给药方案。触发词：pharmacokinetics、PK/PD、NCA、popPK、NONMEM、nlmixr2、exposure-response、TMDD、PBPK、bioequivalence、DDI、MIPD、dosing regimen。 |
| `plan-canvas` | `plan-canvas` | 在本地浏览器画布中打开计划和 HTML 工件，人可以直接在页面上标注元素、聊天、批准或要求修改，无需离开页面。展示计划供审查，或移动这个、改那个之类的反馈指着说比打字更容易时使用。 |
| `plan-ceo-review` | `gstack-plan-ceo-review` | CEO/创始人视角的计划评审。重新思考问题、寻找十星级产品、挑战前提，在能做出更好产品时扩大范围。四种模式：SCOPE EXPANSION（大胆设想）、SELECTIVE EXPANSION（保持范围并精选扩展）、HOLD SCOPE（最大化严谨度）、SCOPE REDUCTION（剥离至核心）。适用于被要求 think bigger、expand scope、strategy review、rethink this、is this ambitious enough 时。当用户质疑计划的范围或野心，或计划看起来可以想得更宏大时主动建议。（gstack） |
| `plan-design-review` | `gstack-plan-design-review` | 设计师视角的计划评审，交互式，类似 CEO 与 Eng 评审。给每个设计维度打 0-10 分，说明怎样能到 10 分，然后修改计划达成。工作在 plan mode。线上站点视觉审计请用 /design-review。触发：“review the design plan”、“design critique”；用户的计划含 UI/UX 部分且应在实现前评审时主动建议。 |
| `plan-devex-review` | `gstack-plan-devex-review` | 交互式开发者体验（DX）计划评审：探索开发者画像、对标竞品、设计 magical moment、追踪摩擦点后评分；三种模式：DX EXPANSION（竞争优势）、DX POLISH（打磨每个触点）、DX TRIAGE（只修关键缺口）；触发词：DX review、developer experience audit、devex review、API design review；用户有面向开发者产品（API、CLI、SDK、库、平台、文档）的计划时应主动建议。(gstack) |
| `plan-eng-review` | `gstack-plan-eng-review` | 工程经理模式的计划评审：锁定执行计划——架构、数据流、图表、边界情况、测试覆盖、性能，以交互式方式过问题并给出有立场的建议。当被要求"review the architecture""engineering review""lock in the plan"时使用；用户有计划或设计文档且即将开始编码时主动建议，以在实现前发现架构问题。(gstack) 语音触发别名："tech review""technical review""plan engineering review"。 |
| `plan-tune` | `gstack-plan-tune` | gstack 的问题敏感度与开发者心理画像自调优（v1 为观察式）。可回顾各 gstack skill 触发的 AskUserQuestion 提示、为每个问题设置偏好（从不问/总是问/仅对不可逆操作问）、查看双轨画像（你声明的偏好 vs 行为推断的偏好）、开关问题调优。对话式界面，无需 CLI 语法。触发词：tune questions、stop asking me that、too many questions、show my profile、what questions have I been asked、show my vibe、developer profile、turn off question tuning；当同一 gstack 问题重复出现或用户第 N 次明确推翻建议时应主动建议使用。(gstack) |
| `polars` | `polars` | 高性能 Python DataFrame 库，用于 ETL、分析和 pandas 迁移。适用于基于表达式的数据操作，支持惰性查询优化、并行执行、流式核外处理、Arrow 互操作和可选 GPU 执行。 |
| `polars-bio` | `polars-bio` | 基于 Polars DataFrame 的高性能基因组区间操作和生物信息文件 I/O：对 BED/VCF/BAM/GFF 区间做 overlap、nearest、merge、coverage、complement、subtract。流式、云原生，比 bioframe 更快的替代方案。 |
| `ponytail` | `ponytail` | 强制采用真正可行的最懒、最简、最短、最小子方案。扮演见惯一切的资深开发者：先质疑任务是否有存在必要（YAGNI），标准库优先于自写代码，平台原生特性优先于新依赖，一行优先于五十行。支持强度档位：lite、full（默认）、ultra。适用于任何编码任务：写、加、重构、修、评审、设计代码及选择库或依赖；用户说 ponytail、be lazy、lazy mode、simplest solution、minimal solution、yagni、do less、shortest path，或抱怨过度工程、臃肿、样板代码、不必要依赖时也触发。不用于非编码请求（常识问答、散文、翻译、摘要、菜谱）。 |
| `ponytail-audit` | `ponytail-audit` | 全仓库过度工程审计。类似 ponytail-review，但扫描整个代码库而非 diff：给出按优先级排序的清单，指出该删除、简化或换成标准库/原生等价物的地方。触发：“audit this codebase”、“audit for over-engineering”、“what can I delete from this repo”、“find bloat”、“ponytail-audit”、“/ponytail-audit”。一次性报告，不落地修复。 |
| `ponytail-debt` | `ponytail-debt` | 收集代码库中所有 ponytail: 注释生成债务台账，让 ponytail 刻意留下的捷径和延期项被跟踪，而不是烂尾成以后再说等于永不做。触发词：ponytail debt、/ponytail-debt、what did ponytail defer、list the shortcuts、ponytail ledger、what did we mark to do later。一次性报告，不修改任何代码。 |
| `ponytail-gain` | `ponytail-gain` | 以紧凑记分板展示 ponytail 的实测效果：更少代码、更低成本、更快速度，数据来自基准测试中位数。一次性展示，非持久模式，也非按仓库统计的数字。触发：/ponytail-gain、ponytail gain、what does ponytail save、show ponytail impact、ponytail scoreboard。 |
| `ponytail-help` | `ponytail-help` | ponytail 全部模式、skill 和命令的速查卡，一次性展示，非持久模式。触发：/ponytail-help、ponytail help、what ponytail commands、how do I use ponytail。 |
| `ponytail-review` | `ponytail-review` | 只关注过度工程的代码评审，找出可删除的东西：重复造轮子的标准库功能、不必要的依赖、投机性抽象、死板的灵活性。每条发现一行：位置、删什么、用什么替代。触发词：review for over-engineering、what can we delete、is this over-engineered、simplify review，或调用 /ponytail-review。与正确性评审互补，本 skill 只猎杀复杂度。 |
| `portfolio-manager` | `portfolio-manager` | 全面的投资组合分析：通过 Alpaca MCP Server 集成拉取持仓和头寸，分析资产配置、风险指标、个股仓位、分散度，并生成再平衡建议。触发：用户要求对券商账户做组合审查、仓位分析、风险评估、绩效评估或再平衡建议。 |
| `position-sizer` | `position-sizer` | 计算做多股票交易的基于风险的仓位大小。当用户询问仓位管理、买多少股、单笔风险、Kelly 准则、基于 ATR 的仓位、碎股仓位或组合风险分配时使用。支持止损距离计算、波动率缩放和行业集中度检查。 |
| `postgres-patterns` | `postgres-patterns` | PostgreSQL 数据库模式，涵盖查询优化、schema 设计、索引与安全，基于 Supabase 最佳实践。适用于设计 PostgreSQL schema、索引、RLS 策略，或查询过慢时。 |
| `ppt-master` | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑 PPTX 与幻灯片、重建页面视觉、创建可复用的 Brand/Style/Layout/Deck 工作区、填充原生 PPTX 模板、增强已完成的 PPTX。当用户要求创建、生成、重建、美化、重设计、模板化、填充或增强 presentation/PPT/PPTX/幻灯片/课件（含添加旁白或动画），或要求制作演示文稿风格的旁白/自播放视频，或提到 ppt-master 时使用。 |
| `pptx` | `pptx` | 只要涉及 .pptx 或 .potx 文件（作为输入、输出或两者）就使用此 skill，包括：创建幻灯片、路演 deck 或演示文稿；读取、解析或提取其中文本（即使内容将用于邮件或摘要等其他用途）；编辑、修改或更新现有演示文稿；合并或拆分幻灯片文件；处理模板（.potx）、版式、演讲者备注或批注。当用户提到"deck""slides""presentation"或引用 .pptx/.potx 文件名时即触发，无论后续打算如何使用内容。 |
| `pptx-posters` | `pptx-posters` | 从作者认可的本地内容和素材出发，创建并审计可编辑的无宏 PowerPoint（.pptx）科研海报。适用于交付物是 PowerPoint 研究/会议海报，且需要精确的物理尺寸、打印机、无障碍、素材溯源和包安全检查时。 |
| `pr-address-comments` | `pr-address-comments` | 帮用户处理 Gemini CLI 当前分支上的 GitHub PR 评论。触发：用户要求协助回应 PR comments。依赖 gh CLI 工具。 |
| `pr-creator` | `pr-creator` | 当被要求创建 Pull Request（PR）时使用，确保所有 PR 遵循仓库既定的模板和标准。 |
| `pr-to-video` | `pr-to-video` | 把 GitHub pull request（PR URL、owner/repo#N 或已检出仓库中的"this PR"）变成代码变更讲解视频——基于 diff、commits 和文件构建 changelog、功能发布、修复或重构讲解；输入是代码变更而非网站。不做产品宣传（用 /product-launch-video）或无 PR 的主题讲解（用 /faceless-explainer）；不明确时用 /hyperframes。 |
| `pre-trade-discipline-gate` | `pre-trade-discipline-gate` | 手动下单前执行本地交易前检查清单，拦截无计划、超仓位、报复性交易风险、市场状态受限或熔断受限的入场，并把决策记入日志供 trader-memory-core 复盘。 |
| `prediction-alpha` | `prediction-alpha` | 分析预测市场：Polymarket、Manifold Markets、Kalshi。计算隐含概率、检测跨平台套利、算期望值和 Kelly 仓位比例。触发：提到 prediction markets、Polymarket、Manifold、Kalshi、odds analysis、套利检测、市场概率、event contracts，或问“is there edge on this market”、“compare odds across platforms”、“analyze this prediction market”、“what are the current odds for”、“find arbitrage opportunities”，以及任何关于市场隐含概率的问题。 |
| `primekg` | `primekg` | 查询精准医学知识图谱（PrimeKG），获取基因、药物、疾病、表型等多尺度生物数据。 |
| `product-launch-video` | `product-launch-video` | 把产品或营销 URL、粘贴的脚本或简报制作成产品发布/宣传视频：SaaS 促销、功能揭晓、产品演示、应用与公司发布。当用户想营销、发布、推广或揭晓产品时使用，是任何商业 URL 的默认选择；网站导览/展示类需求也走此流程（简报承载如实展示的意图）。意图不明确时用 /hyperframes。 |
| `production-audit` | `production-audit` | 基于本地证据的生产就绪度审计，用于已交付应用、上线前评审、合并后检查，以及生产环境会出什么问题这类提问，且不把仓库数据发送到外部审计服务。适用于上线前、合并后审计生产就绪度，或被问及生产环境会出什么问题时。 |
| `project-flow-ops` | `project-flow-ops` | 在 GitHub 与 Linear 之间操作执行流：分诊 issue 和 PR、关联进行中的工作，保持 GitHub 面向公众、Linear 作为内部执行层。适用于：backlog 管控、PR 分诊、GitHub 到 Linear 的协调。 |
| `prompt-forge` | `prompt-forge` | 为 LLM 设计和优化提示词：system prompt、few-shot 示例、思维链结构、agent 人设与评估框架。适用于编写或改进 system prompt、设计 few-shot 示例、创建 agent 人设、优化提示词效果、搭建提示词评估或模板系统；触发短语如 write a system prompt、optimize this prompt、create an agent prompt、few-shot examples for、prompt engineering，以及 this prompt isn't working well、make my AI agent better 等口语化请求。 |
| `protocolsio-integration` | `protocolsio-integration` | 按当前官方 REST/MCP 契约读取、校验和安全导出 protocols.io 数据，或创建不执行的变更计划。内置客户端仅对官方主机做有界 GET 请求，写操作需显式 --execute。仅用于明确针对 protocols.io 或其精确协议版本的任务。 |
| `prototype` | `prototype` | 构建一次性原型来回答设计问题。当用户想快速验证某个状态模型或逻辑是否合理，或探索 UI 应该长什么样时使用。 |
| `prototype` | `engineering/prototype` | 构建一次性原型来回答设计问题。当用户想快速验证某个状态模型或逻辑是否合理，或探索 UI 应该长什么样时使用。 |
| `pufferlib` | `pufferlib` | PufferLib 强化学习环境的版本感知指导：向量化、策略、PuffeRL 训练、评估和安全 checkpoint 审查；适用于将 Gymnasium/PettingZoo 环境适配到已发布的 PufferLib 3.0.0，或使用重新设计的原生 4.0 源码线。 |
| `pydeseq2` | `pydeseq2` | 用 PyDESeq2 做 bulk RNA-seq 差异基因表达分析，包括公式化实验设计、Wald 检验、FDR 校正、LFC 收缩和结果可视化。 |
| `pydicom` | `pydicom` | 用 pydicom 读取、检查、写入、转换本地 DICOM 数据集和像素数据，并做安全预检。覆盖 DICOM 元数据、传输语法、压缩插件、帧、私有元素、JSON 导出和有边界的去标识化审查。 |
| `pyhealth` | `pyhealth` | 用 PyHealth 构建临床/医疗深度学习流水线：加载 EHR/信号/影像数据集（MIMIC-III/IV、eICU、OMOP、SleepEDF、ChestXray14、EHRShot），定义任务（死亡率、再入院、住院时长、药物推荐、睡眠分期、ICD 编码、EEG 事件），实例化模型（Transformer、RETAIN、GAMENet、SafeDrug、MICRON、StageNet、AdaCare、CNN/RNN/MLP），用 PyHealth Trainer 训练并计算临床指标，使用医疗代码工具（ICD/ATC/NDC/RxNorm 查询与交叉映射）。触发：用户提到 PyHealth、MIMIC、eICU、OMOP、EHR 建模、临床预测、药物推荐、睡眠分期、医疗代码映射、ICD/ATC 码，或任何符合数据集→任务→模型→训练器→指标模式的医疗 ML 流水线（即使未明确提到 PyHealth）。 |
| `pylabrobot` | `pylabrobot` | 开发和审查 PyLabRobot 实验室自动化资源、液体处理方案、离线仿真及受支持设备的集成。用于 PyLabRobot 协议或 API 问题；物理执行必须置于明确的操作员安全门之后。 |
| `pymatgen` | `pymatgen` | 用当前 pymatgen API 分析、校验、转换材料结构和计算材料数据，包括本地相图、对称性敏感性、电子结构 I/O，以及显式有界的 Materials Project 查询。 |
| `pymc` | `pymc` | PyMC 贝叶斯建模：构建分层模型、MCMC（NUTS）、变分推断、LOO/WAIC 模型比较、后验检查，用于概率编程与统计推断。 |
| `pymoo` | `pymoo` | 多目标优化框架 pymoo：NSGA-II、NSGA-III、MOEA/D、Pareto 前沿、约束处理、基准测试（ZDT、DTLZ），用于工程设计和优化问题。 |
| `pyopenms` | `pyopenms` | 完整的质谱分析平台，用于蛋白质组和代谢组工作流：特征检测、肽/蛋白鉴定、非标记与同位素标记定量、加合物/精确质量注释及复杂 LC-MS/MS 流水线，支持大量文件格式和算法。简单谱图对比和小分子库匹配请用 matchms。 |
| `pysam` | `pysam` | 基于 Python/HTSlib 的基因组文件工作流：用 pysam 读取、查询、过滤或写入 SAM/BAM/CRAM、VCF/BCF、FASTA/FASTQ、tabix 数据，包括 pileup、覆盖度、索引和 CRAM 参考序列处理。 |
| `pytdc` | `pytdc` | 通过 PyTDC Python 包使用 Therapeutics Data Commons：注册表发现、获批数据集访问、任务感知数据划分、评估器指标、基准测试组，以及有边界的分子 oracle 工作流。 |
| `python-patterns` | `python-patterns` | Pythonic 惯用法、PEP 8 规范、类型标注和最佳实践，构建健壮高效可维护的 Python 应用；适用于编写或评审 Python 代码，涉及惯用结构、typing 或 PEP 8 时。 |
| `python-testing` | `python-testing` | Python 测试策略：pytest、TDD 方法论、fixture、mock、参数化、覆盖率要求。编写 pytest 测试（fixture、mock、参数化、覆盖率）时使用。 |
| `pytorch-lightning` | `pytorch-lightning` | 深度学习框架（PyTorch Lightning / lightning 包）：把 PyTorch 代码组织为 LightningModule，配置 Trainer 支持多 GPU/TPU，实现数据管道、callbacks、日志（W&B、TensorBoard、MLflow）和分布式训练（DDP、FSDP、DeepSpeed），用于可扩展的神经网络训练。 |
| `pytorch-patterns` | `pytorch-patterns` | PyTorch 深度学习模式与最佳实践：构建健壮、高效、可复现的训练管道、模型架构和数据加载。编写或审查 PyTorch 训练循环、模型架构、数据加载，或训练无法复现时使用。 |
| `pyzotero` | `pyzotero` | 用 pyzotero Python 客户端操作 Zotero 文献管理库：通过 Zotero Web API v3 检索、创建、更新、删除条目、集合、标签和附件。在程序化管理 Zotero 库、管理参考文献、导出引用、搜索库内容、上传 PDF 附件或构建集成 Zotero 的科研自动化工作流时使用。 |
| `qa` | `gstack-qa` | 系统化 QA 测试 Web 应用并修复发现的 bug：先跑测试，再迭代修复源码，每个修复原子化提交并重新验证。触发词：qa、test this site、find bugs、test and fix、fix what's broken；用户说功能可测试或问 does this work? 时可主动建议。三档深度：Quick（仅严重/高）、Standard（+中）、Exhaustive（+外观），输出前后健康分、修复证据和发布就绪摘要。仅报告模式用 /qa-only。语音触发：quality check、test the app、run QA。（gstack） |
| `qa-only` | `gstack-qa-only` | 只出报告的 QA 测试。系统化测试 Web 应用，产出含健康评分、截图和复现步骤的结构化报告，但绝不修复任何问题。适用于被要求 just report bugs、qa report only、test but don't fix 时。需要完整的测试-修复-验证闭环请用 /qa。当用户想要 bug 报告但不改任何代码时主动建议。（gstack）语音触发（语音转文字别名）：bug report、just check for bugs。 |
| `qiskit` | `qiskit` | 用 Qiskit 和 IBM Quantum Runtime 构建、模拟、转译和执行量子电路：Qiskit 2.x 电路与算符、V2 Sampler/Estimator 原语、目标感知转译、本地或含噪模拟、IBM QPU 执行、Runtime session 或 batch、误差缓解及 Qiskit 生态包。 |
| `quantum-debugger` | `quantum-debugger` | 调试复杂难复现问题：竞态条件、内存泄漏、死锁、性能回退、heisenbug、崩溃分析。采用科学调试方法：生成假设、系统化测试、隔离根因。用户报告间歇性崩溃、性能下降、内存泄漏、线程安全问题、死锁或难复现 bug 时使用。也触发于 "debug this"、"why is this crashing"、"performance regression"、"memory leak"、"race condition"、"segfault"、"service hangs intermittently"、"this works on my machine but not in production"。 |
| `quarkus-patterns` | `quarkus-patterns` | Quarkus 3.x LTS 架构模式，含 Camel 消息、RESTful API 设计、CDI 服务、Panache 数据访问和异步处理。适用于事件驱动架构的 Java Quarkus 后端工作，尤其构建或评审带 Camel 消息或 Panache 数据访问的 Quarkus 服务时。 |
| `quarkus-security` | `quarkus-security` | Quarkus 安全最佳实践：认证、授权、JWT/OIDC、RBAC、输入校验、CSRF、密钥管理与依赖安全。触发场景：审查 Quarkus 的 authn/authz、JWT、OIDC、RBAC、校验或密钥相关代码时。 |
| `quarkus-tdd` | `quarkus-tdd` | Quarkus 3.x LTS 的测试驱动开发：使用 JUnit 5、Mockito、REST Assured、Camel 测试和 JaCoCo。适用于为事件驱动服务添加功能、修复 bug 或重构。 |
| `quarkus-verification` | `quarkus-verification` | Quarkus 项目的验证闭环：构建、静态分析、带覆盖率的测试、安全扫描、native 编译，以及发布或提 PR 前的 diff 评审。 |
| `qutip` | `qutip` | 用 QuTiP 5 模拟和审计封闭与开放量子系统模型，涵盖确定性、轨迹、稳态、谱分析和相空间工作流。适用于需要显式说明物理假设、维度和数值收敛的本地量子动力学工作。 |
| `rdkit` | `rdkit` | 用于精细分子控制的化学信息学工具包：SMILES/SDF 解析、描述符（MW、LogP、TPSA）、指纹、子结构搜索、2D/3D 结构生成、相似性、反应处理。标准工作流建议用接口更简单的 datamol（RDKit 封装）；需要高级控制、自定义 sanitization 或专门算法时用 rdkit。 |
| `react-patterns` | `react-patterns` | React 18/19 模式：hooks 纪律、server/client 组件边界、Suspense + error boundaries、form actions、数据获取、状态管理决策树、无障碍优先的组合方式。编写或审查 React 组件时使用。 |
| `react-performance` | `react-performance` | React 与 Next.js 性能优化模式，改编自 Vercel Engineering 的 React Best Practices。按 8 个优先级类别组织 70+ 条规则：瀑布流、bundle 体积、服务端、客户端数据获取、重渲染、渲染、JS 微优化、高级技巧。在编写、评审或重构 React/Next.js 代码以优化性能时使用。 |
| `react-testing` | `react-testing` | React 组件测试：React Testing Library、Vitest/Jest、MSW 网络 mock、axe 无障碍断言，以及组件测试与 Playwright/Cypress 端到端测试的边界决策。适用于编写或修复 React 组件、hooks 或页面的测试。 |
| `receiving-code-review` | `receiving-code-review` | 收到代码审查反馈后、实施建议之前使用，尤其当反馈不明确或技术上有疑问时——需要技术严谨性和验证，而非敷衍附和或盲目执行。 |
| `redesign-existing-projects` | `redesign-skill` | 将现有网站和应用升级为高端品质：审计当前设计、识别千篇一律的 AI 模式，在不破坏功能的前提下应用高端设计标准；适配任何 CSS 框架或纯 CSS。 |
| `redis-patterns` | `redis-patterns` | Redis 数据结构模式、缓存策略、分布式锁、限流、发布订阅与连接管理，面向生产应用。适用于用 Redis 添加缓存、分布式锁、限流或 pub/sub，或需要审查 key 设计时。 |
| `refactor-advisor` | `refactor-advisor` | 重构顾问：识别代码坏味道并提供重构方案。适用于需要评估代码质量、找出坏味道并制定重构策略时。 |
| `relsa-severity-assessment` | `relsa-severity-assessment` | 实验动物研究的多变量严重程度评估与人道终点预测，基于 RELSA（相对严重程度评估）评分和 ARIMA 预测。适用场景：将体重/失重、体温、临床或筑巢评分、生物标志物、活动量、心率、掘穴、跑轮等福利指标合成每只动物每天的单一严重程度评分；判断哪些动物有达到人道终点的风险及何时达到；用核密度估计在严重程度量表上定义注意区/危险区阈值；3Rs、refinement、动物福利或 EU Directive 2010/63/EU 严重程度评估报告。覆盖方向性（turned）变量、基线归一化、参考集、RELSA 权重、ARIMA 预测区间及 RMSE/PICP/MPIW 评估。 |
| `remotion-to-hyperframes` | `remotion-to-hyperframes` | 把现有 Remotion (React) 合成的源码移植为 HyperFrames HTML。仅在用户明确要求 port/convert/migrate/translate Remotion 源码时使用——单向、仅限 Remotion。顺带提到 Remotion、仅作参考的代码、或 make something like my Remotion video 属于全新构建（走 /general-video）。不明确时用 /hyperframes。 |
| `requesting-code-review` | `requesting-code-review` | 完成任务、实现重要功能或合并前使用，用于验证工作成果是否符合要求。 |
| `research` | `research` | 针对问题进行调研，基于高可信度的一手资料来源查证，并把结论写成仓库内的 Markdown 文件。适用于用户想研究某个主题、收集文档或 API 事实，或把查阅资料的工作委托给后台 agent 时。 |
| `research` | `engineering/research` | 针对问题进行调研，基于高可信度的一手资料来源查证，并把结论写成仓库内的 Markdown 文件。适用于用户想研究某个主题、收集文档或 API 事实，或把查阅资料的工作委托给后台 agent 时。 |
| `research-grants` | `research-grants` | 为 NSF、NIH、DOE、DARPA 和台湾 NSTC 撰写有竞争力的科研申请书。覆盖各机构专属格式、评审标准、预算编制、broader impacts、significance 陈述、创新叙事和提交要求合规。 |
| `research-lookup` | `research-lookup` | 为科学论文或研究简报汇编最新学术证据。用户明确要求收集文献、参考文献、背景证据、竞争性发现或论文研究资料包时使用。默认用 Parallel Search，来源核验用 Parallel Extract，明确的深度/穷尽任务用 Parallel Research，Parallel Chat 需显式指定，Perplexity 仅在用户要求或允许作为失败回退时使用。 |
| `residual-edge-analyzer` | `residual-edge-analyzer` | 将策略收益序列分解为声明的基线敞口与残余 edge，采用基于收益的 OLS 归因、HAC 推断、滚动稳定性、替代基线敏感性和市场状态分解。适用于：评估回测、样本外或实盘收益是否含超越市场、等权、动量、板块或用户提供因子的独立 alpha；解释回撤来自基线敞口还是策略特有行为；回测后需要归因质量门。不适用于基于持仓的 Brinson 归因、特征级 Shapley 解释，或无带日期收益序列、仅凭汇总指标的分析。 |
| `resolving-merge-conflicts` | `resolving-merge-conflicts` | 当需要解决正在进行中的 git merge/rebase 冲突时使用。 |
| `resolving-merge-conflicts` | `engineering/resolving-merge-conflicts` | 当需要解决正在进行中的 git merge/rebase 冲突时使用。 |
| `retro` | `gstack-retro` | 每周工程复盘：分析提交历史、工作模式和代码质量指标，带持久化历史与趋势追踪；支持团队维度，按人拆分贡献并给出表扬与成长点。触发场景：用户要求 weekly retro、问这周交付了什么、或要工程回顾；也可在工作周或 sprint 结束时主动建议。（gstack） |
| `retro` | `retro` | 复盘与回顾 skill：把一次开发、排障、交付或协作过程整理成可执行的复盘结论，输出做得好的地方、问题与根因、改进动作和后续跟踪项。用于用户要求"复盘""回顾这次开发""总结问题和经验""postmortem""retrospective""总结这次哪里做得好/不好"等场景；也适用于任务刚完成、需要沉淀流程改进点、防止同类问题再次发生时。 |
| `review` | `gstack-review` | 合并前的 PR 评审。对比 base 分支分析 diff，检查 SQL 安全、LLM 信任边界违规、条件分支副作用等结构性问题。触发：“review this PR”、“code review”、“pre-landing review”、“check my diff”；用户即将合并或落地代码改动时主动建议。 |
| `review-duplication` | `review-duplication` | 代码审查时使用：主动排查代码库中的重复功能、重复造轮子、以及未复用项目既有最佳实践和共享工具的情况。 |
| `robot-aiot-slide-html-author` | `robot-aiot-slide-html-author` | 为领导汇报类 PPT/母稿生成固定画布（1920x1080）的逐页 HTML：执行时引用 ui-ux-pro-max 的设计系统与审查能力，内化语义化设计 token、清晰/克制/层次原则与高级感标准（反模板化排版、色彩/形状一致性锁定、AI 痕迹清单、审查修复工作流）。适用于 PPT 母稿转单页 HTML、领导汇报页落成 HTML、逐页生成 slide HTML、给 ppt-master 准备逐页 HTML、修复汇报页布局/样式/信息层级、把图表 HTML 嵌入汇报页；也适用于已有 Markdown 母稿、页面草图或图表 HTML、需保持图表真源与页面视觉体系一致的任务。图表 HTML 有问题时可调用 robot-aiot-xml-html-bridge 审查修复。 |
| `rowan` | `rowan` | Rowan：云原生分子建模与药物化学工作流平台，提供 Python API。适用于 pKa 和 macropKa 预测、构象与互变异构体集合、对接和类似物对接、蛋白-配体 cofolding、MSA 生成、分子动力学、透性、描述符工作流及相关小分子或蛋白建模任务。适合程序化批量筛选、多步化学流水线，以及否则需要自维护本地 HPC/GPU 基础设施的工作流。 |
| `safe-refactor` | `safe-refactor` | 在保持行为不变的前提下重构代码。适用于提取、合并、所有权迁移或清理等结构性编辑，且必须在编辑前后用验证手段包裹确认行为一致的场景。 |
| `scaffold-exercises` | `misc/scaffold-exercises` | 创建练习目录结构，包含章节、题目、答案和讲解，且能通过 lint。当用户想搭建练习脚手架、创建练习模板或建立新课程章节时使用。 |
| `scaffold-exercises` | `scaffold-exercises` | 创建练习目录结构，包含章节、题目、答案和讲解，且能通过 lint。当用户想搭建练习脚手架、创建练习模板或建立新课程章节时使用。 |
| `scanpy` | `scanpy` | 标准单细胞 RNA-seq 分析流程：QC、归一化、降维（PCA/UMAP/t-SNE）、聚类、差异表达、可视化，以及把 R 侧单细胞格式（Seurat、SingleCellExperiment 的 RDS 文件）转成 h5ad 供 Scanpy 使用。适合有成熟工作流的探索性 scRNA-seq 分析；深度学习模型用 scvi-tools，数据格式问题用 anndata。 |
| `scenario-analyzer` | `scenario-analyzer` | 从新闻标题分析 18 个月情景：用 scenario-analyst agent 跑主分析，再用 strategy-reviewer agent 获取第二意见，生成完整英文报告，覆盖一阶/二阶/三阶影响、推荐股票和批判性评审。示例：/scenario-analyzer "Fed raises rates by 50bp"。触发场景：新闻分析、情景分析、18 个月展望、中长期投资策略。 |
| `scholar-evaluation` | `scholar-evaluation` | 对学术著作提供定性优先、证据可追溯的发展性评审，并审计低风险研究评估量表（可选本地质量控制）。绝不用于给人排名或做重大利害决策。 |
| `scientific-brainstorming` | `scientific-brainstorming` | 证据感知的科学头脑风暴：独立生成想法、结构化讨论、显式假设、透明评估、对抗性评审、决策日志。用于早期研究构思或候选方向优先级排序；实证验证、研究设计、伦理/监管审查、临床问题交给相应专家或 skill。 |
| `scientific-critical-thinking` | `scientific-critical-thinking` | 评估科学论断与证据质量。适用于评判实验设计有效性、识别偏倚与混杂因素、应用证据分级框架（GRADE、Cochrane Risk of Bias）、教授批判性分析。最适合理解证据质量和找出缺陷；撰写正式同行评审请改用 peer-review。 |
| `scientific-schematics` | `scientific-schematics` | 用 Nano Banana 2 AI 创建出版级科学示意图，带智能迭代精修，使用 Gemini 3.6 Flash 做质量审查，仅当质量低于对应文档类型阈值时才重新生成。专长于神经网络架构图、系统图、流程图、生物通路及复杂科学可视化。 |
| `scientific-slides` | `scientific-slides` | 为研究演讲制作幻灯片：PowerPoint 幻灯片、会议报告、研讨会演讲、研究展示、论文答辩幻灯片等科学演讲。提供幻灯片结构、设计模板、时间建议和视觉校验，支持 PowerPoint 和 LaTeX Beamer。 |
| `scientific-visualization` | `scientific-visualization` | 用 Matplotlib、Seaborn 或 Plotly 创建并审查真实、无障碍、可发表的科学图表。适用于图表设计、多面板布局、不确定性与缺失数据展示、颜色/对比度审查、图像元数据校验和期刊导出规划。 |
| `scientific-writing` | `scientific-writing` | 起草、修改和审核科学论文或报告，强调证据溯源、报告规范覆盖、作者责任、保密控制和本地一致性检查。适用于对科学准确性和可追溯性有要求的稿件章节、参考文献、声明、表格、图片或投稿准备。 |
| `scikit-bio` | `scikit-bio` | scikit-bio 生物数据工具包：序列分析、比对、系统发育树、多样性指标（alpha/beta、UniFrac）、排序分析（PCoA）、PERMANOVA、FASTA/Newick I/O，适用于微生物组分析。 |
| `scikit-learn` | `scikit-learn` | 用 scikit-learn 做 Python 机器学习：监督学习（分类、回归）、无监督学习（聚类、降维）、模型评估、超参调优、预处理和 ML pipeline 构建；提供算法、预处理技术、pipeline 和最佳实践的完整参考文档。 |
| `scikit-survival` | `scikit-survival` | 用 scikit-survival 构建、评估和审计右删失或竞争风险生存分析流程：防泄漏预处理、模型选择、概率预测、考虑删失的评估指标。 |
| `scrape` | `gstack-scrape` | 从网页抓取数据。新意图首次调用通过 $B 原语原型化流程并返回 JSON，后续同意图调用路由到已固化的 browser-skill，约 200ms 返回。只读；写操作（表单填写、点击、提交）用 /automate。当用户要求 scrape、get data from、pull、extract from 或问页面上有什么时触发。(gstack) |
| `scvelo` | `scvelo` | 用 scVelo 做 RNA 速度分析：从未剪接/已剪接 mRNA 动态估计细胞状态转变，推断轨迹方向，计算潜时间（latent time），识别单细胞 RNA-seq 数据中的驱动基因。与 Scanpy/scVI-tools 互补，用于轨迹推断。 |
| `scvi-tools` | `scvi-tools` | 单细胞组学的深度生成模型。用于概率式批次校正（scVI）、迁移学习、带不确定性的差异表达、多模态整合（TOTALVI、MultiVI）。最适合高级建模、批次效应和多模态数据。标准分析流水线用 scanpy。 |
| `seaborn` | `seaborn` | 与 pandas 集成的统计可视化，默认样式美观，适合快速探索分布、关系和分类对比，最擅长箱线图、小提琴图、pair plot、热力图，基于 matplotlib 构建。交互式图表用 plotly，出版级样式用 scientific-visualization。 |
| `search-first` | `search-first` | 先调研后编码的工作流：写自定义代码前先搜索现有工具、库和模式，调用 researcher agent。 |
| `sector-analyst` | `sector-analyst` | 分析板块轮动模式与市场周期定位。从 CSV 获取板块上升趋势数据（无需 API key），可选接受图表图片做补充分析。适用于用户请求板块轮动分析、周期股与防御股评估、超买超卖识别或市场周期阶段估计时。所有分析与输出均用英文。 |
| `security-audit` | `security-audit` | Java 安全检查清单，覆盖 OWASP Top 10、输入校验、注入防护和安全编码，适用于 Spring、Quarkus、Jakarta EE 和纯 Java。当审查代码安全性、发布前检查，或用户询问漏洞时使用。 |
| `security-review` | `security-review` | 安全审查清单与模式。在添加认证、处理用户输入、使用密钥/机密、创建 API 端点或实现支付等敏感功能时触发。 |
| `security-scan` | `security-scan` | 用 AgentShield 扫描 Claude Code 配置（.claude/ 目录）中的安全漏洞、错误配置和注入风险，检查 CLAUDE.md、settings.json、MCP servers、hooks 和 agent 定义。适用于：审计 .claude/ 目录的安全性。 |
| `security-sentinel` | `security-sentinel` | 执行安全审计、漏洞评估、SSL/TLS 加固、DNSSEC 配置和合规检查。覆盖 OWASP Top 10、CIS Benchmarks、邮件安全（SPF/DKIM/DMARC）和网络侦察。触发：用户要求安全审计、漏洞扫描、渗透测试、SSL 加固、DNSSEC 配置、合规检查或安全态势评估，也响应“is my site secure”、“check for vulnerabilities”、“harden my server”、“audit my domain”、“set up DNSSEC”，以及任何安全评估请求，包括“I'm worried about my site's security.”这类模糊表述。 |
| `setup-browser-cookies` | `gstack-setup-browser-cookies` | 把真实 Chromium 浏览器的 cookie 导入无头浏览会话，打开交互式选择器 UI 供选择要导入的 cookie 域。在 QA 测试需登录页面之前使用；触发词：import cookies、login to the site、authenticate the browser。（gstack） |
| `setup-deploy` | `gstack-setup-deploy` | 为 /land-and-deploy 配置部署设置。检测部署平台（Fly.io、Render、Vercel、Netlify、Heroku、GitHub Actions、自定义）、生产 URL、健康检查端点和部署状态命令，将配置写入 CLAUDE.md 使后续部署自动化。触发词：setup deploy、configure deployment、set up land-and-deploy、how do I deploy with gstack、add deploy config。 |
| `setup-gbrain` | `gstack-setup-gbrain` | 为当前 coding agent 配置 gbrain：安装 CLI、初始化本地 PGLite 或 Supabase brain、注册 MCP、记录按 remote 的信任策略；一条命令从零到 gbrain 运行且 agent 可调用。触发词：setup gbrain、connect gbrain、start gbrain、install gbrain、configure gbrain for this machine。(gstack) |
| `setup-matt-pocock-skills` | `setup-matt-pocock-skills` | 为本仓库配置工程类 skills 的运行环境：设置 issue 跟踪器、triage 标签词汇和领域文档布局。在首次使用其他工程 skills 之前运行一次。 |
| `setup-matt-pocock-skills` | `engineering/setup-matt-pocock-skills` | 为本仓库配置工程类 skills 的运行环境：设置 issue 跟踪器、triage 标签词汇和领域文档布局。在首次使用其他工程 skills 之前运行一次。 |
| `setup-pre-commit` | `misc/setup-pre-commit` | 在当前仓库配置 Husky pre-commit 钩子，集成 lint-staged（Prettier）、类型检查和测试。适用于用户想添加 pre-commit 钩子、配置 Husky 或 lint-staged、在提交时执行格式化/类型检查/测试时。 |
| `setup-pre-commit` | `setup-pre-commit` | 在当前仓库配置 Husky pre-commit 钩子，集成 lint-staged（Prettier）、类型检查和测试。适用于用户想添加 pre-commit 钩子、配置 Husky 或 lint-staged、在提交时执行格式化/类型检查/测试时。 |
| `setup-ts-deep-modules` | `setup-ts-deep-modules` | 在 TypeScript 仓库中接入 dependency-cruiser，让每个 package 成为深模块：实现隐藏在子文件夹中，只能通过入口文件访问。由用户主动调用。 |
| `setup-ts-deep-modules` | `in-progress/setup-ts-deep-modules` | 在 TypeScript 仓库中接入 dependency-cruiser，使每个 package 成为深模块：实现隐藏在子目录中，只能通过入口文件访问。需用户显式调用。 |
| `shap` | `shap` | 用 SHAP 解释和审计机器学习预测：选择 SHAP explainer 与 masker、计算并验证特征归因、处理多输出解释、生成局部或全局 SHAP 可视化。 |
| `ship` | `gstack-ship` | Ship 工作流：检测并合并 base 分支、运行测试、审查 diff、升级 VERSION、更新 CHANGELOG、提交、推送、创建 PR。触发词：ship、deploy、push to main、create a PR、merge and push、get it deployed。当用户表示代码就绪、询问部署、想推送代码或要求创建 PR 时，主动调用此 skill（不要直接 push/PR）。（gstack） |
| `short-term-stock-picker` | `short-term-stock-picker` | 基于 AKShare 数据的短线股票筛选工具。筛选条件：流通市值≤150亿、近20交易日有涨停、非ST、大A/深证/创业板/科创板、近3日主力净流入估算、换手率≤10%。触发场景：用户问帮我选短线股、短线炒股、找强势股、筛选股票；需要按条件筛选A股短线机会；执行选股策略时。 |
| `signal-postmortem` | `signal-postmortem` | 记录并分析 edge pipeline 及其他 skill 生成信号的交易后表现：跟踪误报、错失机会和市场状态错配，把结果反馈给 edge-signal-aggregator 的权重和 skill 改进待办清单。 |
| `simpy` | `simpy` | 用 SimPy 构建、检查、测试和分析有界的基于进程的离散事件仿真，涵盖事件、资源、中断、监控、多次重复运行、预热期和可复现的输出分析。 |
| `skill-creator` | `skill-creator` | 创建新 skill、修改和改进现有 skill、度量 skill 性能。当用户想从零创建 skill、编辑或优化现有 skill、运行 evals 测试 skill、做基准测试和方差分析，或优化 skill 描述以提高触发准确度时使用。 |
| `skill-curator` | `skill-curator` | 中文 Skill 收录评估器。核验 GitHub 上的 Claude Code、Codex、Agent Skills、Plugin、MCP、CLI 或 Agent 工作流是否值得加入精选列表；检查真实资产、安装方式、活跃度、重复项和安全边界，并生成分类、中文描述与可追溯证据。 |
| `skill-designer` | `skill-designer` | 从结构化的创意规格设计新的 Claude skill。当 skill 自动生成流水线需要产出 Claude CLI 提示词、以按仓库约定创建完整 skill 目录（SKILL.md、references、scripts、tests）时使用。 |
| `skill-idea-miner` | `skill-idea-miner` | 从 Claude Code 会话日志中挖掘 skill 创意候选。适用于：运行每周 skill 生成流水线时，从近期编码会话中提取、评分并将新 skill 想法纳入 backlog。 |
| `skill-integration-tester` | `skill-integration-tester` | 校验 CLAUDE.md 中定义的多 skill 工作流：检查 skill 是否存在、skill 间数据契约（JSON schema 兼容性）、文件命名约定和交接完整性。适用于新增工作流、修改 skill 输出或发布前验证流水线健康度。 |
| `skillify` | `gstack-skillify` | 把最近一次成功的 /scrape 流程固化为磁盘上的永久 browser-skill；之后相同意图的 /scrape 调用直接运行固化脚本（约 200ms），不再重新驱动页面。会回溯对话、生成 script.ts + script.test.ts + fixture，在临时目录运行测试，提交前询问确认。触发词：skillify、codify、save this scrape、make this permanent。(gstack) |
| `slack-gif-creator` | `slack-gif-creator` | 创建针对 Slack 优化的动画 GIF 的知识和工具，提供尺寸约束、校验工具和动画概念。当用户要求制作 Slack 用动画 GIF（如"make me a GIF of X doing Y for Slack"）时使用。 |
| `slides` | `slides` | 创建有策略性的 HTML 演示文稿，涵盖 Chart.js 图表、design tokens、响应式布局、文案公式和按上下文选择的幻灯片策略。 |
| `slideshow` | `slideshow` | 创作 HyperFrames 幻灯片：演示文稿、路演 deck 或交互式 deck，支持离散页面、片段渐显、分支、热点导航和带演讲者备注的演示模式，也可把现有页面转为 deck；输出是可导航的 deck 而非渲染的 MP4；用户未明确要求幻灯片时需先确认，不明确时用 /hyperframes。 |
| `solid-principles` | `solid-principles` | SOLID 原则检查清单，附 Java 示例。适用于类职责过多、抽象泄漏、依赖方向错误，以及用户询问单一职责、开闭、里氏替换、接口隔离或依赖倒置原则时。命名、重复和方法长度问题请改用 clean-code。 |
| `spec` | `gstack-spec` | 分五个阶段把模糊意图变成精确可执行的规格说明。创建 issue，可选在全新 worktree 中启动 Claude Code agent，并让 /ship 在合并时关闭源 issue。适用于被要求 spec this out、file an issue、write up a ticket、make this a GitHub issue、turn this into a backlog item 时。（gstack） |
| `spring-boot-patterns` | `spring-boot-patterns` | Spring Boot 最佳实践与模式。适用于创建 controller、service、repository，或用户询问 Spring Boot 分层、装配、配置、异常处理时。JPA 和 Hibernate 行为请改用 jpa-patterns。 |
| `springboot-patterns` | `springboot-patterns` | Spring Boot 架构模式：REST API 设计、分层服务、数据访问、缓存、异步处理、日志。构建或审查 Spring Boot 后端（REST 层、service、数据访问、缓存、异步任务）等 Java 后端工作时使用。 |
| `springboot-security` | `springboot-security` | Spring Security 最佳实践，覆盖 Java Spring Boot 服务中的认证/授权、校验、CSRF、密钥、响应头、限流与依赖安全。适用于审查 Spring Security 的认证授权、校验、CSRF、密钥、响应头或限流时。 |
| `springboot-tdd` | `springboot-tdd` | Spring Boot 测试驱动开发，使用 JUnit 5、Mockito、MockMvc、Testcontainers 和 JaCoCo；适用于添加功能、修复 bug 或重构。 |
| `springboot-verification` | `springboot-verification` | Spring Boot 项目的验证循环：构建、静态分析、带覆盖率的测试、安全扫描，以及发布或提 PR 前的 diff 评审。 |
| `stable-baselines3` | `stable-baselines3` | 生产级强化学习算法库（PPO、SAC、DQN、TD3、DDPG、A2C），scikit-learn 风格 API。适用于标准 RL 实验、快速原型和文档完善的算法实现，最适合配合 Gymnasium 环境的单智能体 RL；高性能并行训练、多智能体系统或自定义向量化环境请改用 pufferlib。 |
| `stanley-druckenmiller-investment` | `stanley-druckenmiller-investment` | Druckenmiller 策略综合器：整合 8 个上游 skill 输出（市场宽度、上升趋势、市场顶部、宏观状态、FTD 检测、VCP 筛选、主题检测、CANSLIM 筛选）为统一确信度分数（0-100）、模式分类和仓位配置建议；适用于询问整体市场确信度、组合定位、资产配置、策略综合或 Druckenmiller 式分析；触发如 What is my conviction level?、How should I position?、Run the strategy synthesizer、確信度スコア等。 |
| `statistical-analysis` | `statistical-analysis` | 面向科研数据的引导式统计分析：检验方法选择、前提假设检查、效应量、功效分析、贝叶斯替代方法及 APA 格式报告。触发场景：组间比较、假设检验、实验或问卷数据分析、统计假设检查、样本量计算、结果撰写，即使用户未指明具体检验方法。覆盖 t 检验、ANOVA、卡方、相关、回归、非参数与贝叶斯方法；底层模型 API 见 statsmodels 和 pymc skill。 |
| `statistical-power` | `statistical-power` | 研究规划的样本量与统计功效计算；适用于问需要多少受试者/样本/重复、事前功效分析、最小可检测效应（MDE）、功效曲线，或为基金申请、IRB 方案、预注册论证样本量；覆盖 t 检验、ANOVA、比例、相关、卡方、回归的闭式功效，以及 logistic/Poisson 回归、混合模型、整群随机、生存分析、交互作用等无公式设计的 Monte Carlo 模拟功效；即使只提到效应量、alpha 或 80% power 也应使用；研究布局用 experimental-design，已收集数据的分析报告用 statistical-analysis。 |
| `statsmodels` | `statsmodels` | Python 统计建模库。需要具体模型类（OLS、GLM、混合模型、ARIMA）及详细诊断、残差和推断时使用；最适合计量经济学、时间序列和带系数表的严谨推断。需要引导式统计检验选择和 APA 报告请用 statistical-analysis。 |
| `stitch-design-taste` | `stitch-skill` | 面向 Google Stitch 的语义化设计系统技能。生成对 agent 友好的 DESIGN.md 文件，强制执行高端、反同质化的 UI 标准——严格排版、校准色彩、非对称布局、持续微动效与硬件加速性能。 |
| `stock-analysis` | `stock-analysis-skill` | 股票智能分析技能。输入股票代码（A股/港股/美股），自动完成：获取实时行情和历史K线数据；计算技术指标（MA/MACD/RSI/量能/乖离率）；综合评分（100分制）加买卖信号；搜索最新新闻消息面；AI 综合分析并输出决策看板。触发场景：用户提供股票代码要求分析、问某只股票怎么样、要求看盘分析等。示例输入：「分析下 TSLA PLTR」「600519怎么样」「帮我看看HK00700」。 |
| `stock-analyst` | `stock-analyst` | 美股/港股盘前分析框架。抓取五大观测指标（VIX/IGV/MAGS/MEME/布油）、个股实时价格、期权隐含波动率，生成结构化盘前简报；含量化模块：粒子滤波概率追踪、期权蒙卡定价、Copula VaR；支持持仓 JSON 格式管理与实时浮盈亏计算。 |
| `stockbee-20pct-study` | `stockbee-20pct-study` | 构建并维护 Stockbee 风格的美股每日 20% 异动研究：扫描 +20%/-20% 异动股，分类催化剂与形态背景，更新后续走势，归纳同类模式。触发场景：用户要求跑每日 20% 研究、回填历史 20% 异动、寻找可复现的 edge 模式，或建立爆发性行情案例库。 |
| `stockbee-episodic-pivot-analyzer` | `stockbee-episodic-pivot-analyzer` | 分析 Stockbee 风格的 Day 1 Episodic Pivot（EP）候选：财报、上调指引、并购、FDA/监管批准、分析师行动、重大合同、产品发布、逼空催化剂或主题/叙事事件；综合评分催化剂质量、跳空/波幅扩张、成交量冲击、被忽视/重估背景、流动性及 EP 日低点风险。触发场景：用户要 EP 候选、episodic pivot、Day 1 催化剂交易、颠覆性新闻反应、延迟 EP 观察清单，或交接给 PEAD 监控。 |
| `stockbee-exhaustion-hammer-screener` | `stockbee-exhaustion-hammer-screener` | 按 Stockbee 风格筛选美股的卖方力竭锤子形态：依据前期动量、回调深度、跌破后收复（undercut/reclaim）、长下影线几何、收盘位置、成交量确认、质量/流动性门槛和风险距离评分。触发：用户提到 Stockbee、Pradeep Bonde、exhaustion setup、selling exhaustion、hammer reversal、undercut reclaim、尾盘反转候选，或在高质量机构持仓股中找回调买点。 |
| `stockbee-momentum-burst-screener` | `stockbee-momentum-burst-screener` | 筛选美股中 Stockbee 风格的短线 Momentum Burst 设置，使用 4% 突破、美元成交额突破、波幅扩张、成交量扩张、前期波幅收缩、收盘位置、失败过滤器和风险距离评分。触发词：Stockbee、Pradeep Bonde、momentum burst、4% breakout、range expansion、dollar breakout、短线波段动量候选、3-5 天爆发设置复盘。 |
| `stockbee-setup-fluency-trainer` | `stockbee-setup-fluency-trainer` | 从动量爆发（momentum-burst）筛选候选中构建 Stockbee 风格的形态模型手册，随后用 MFE/MAE、止损触发状态、结果标签和分组统计更新 3 日与 5 日前瞻结果。适用于用户想研究 Stockbee Momentum Burst 案例、跟踪失败候选、培养形态识别熟练度、复盘 A/B 形态质量，或把筛选输出转成学习闭环而非即时交易信号时。 |
| `strategic-compact` | `strategic-compact` | 建议在逻辑断点处手动压缩上下文，以任务阶段作为自然压缩点来保留上下文，而非依赖任意的自动压缩。当会话接近上下文限制且任务阶段适合压缩时触发。 |
| `strategy-pivot-designer` | `strategy-pivot-designer` | 检测回测迭代停滞，在参数调优陷入局部最优时生成结构上不同的策略转向（pivot）提案。 |
| `string-reviewer` | `string-reviewer` | 当被要求审查代码库中的文本和面向用户的字符串时使用，确保这些字符串符合清晰、有用、简洁和风格方面的规则。 |
| `subagent-driven-development` | `subagent-driven-development` | 在当前会话中执行包含独立任务的实现计划时使用，通过 subagent 驱动开发。 |
| `surgical-patch` | `surgical-patch` | 在最窄的责任层修 bug 和做小范围行为改动。适用于需要回归证据、保持周边行为不变、并补上与任务相关测试的场景。 |
| `sympy` | `sympy` | 需要在 Python 中做精确符号数学时使用——代数、微积分、方程求解、符号线性代数，或通过 lambdify/LaTeX 生成代码。若浮点近似已足够，优先用 NumPy 或 SciPy。 |
| `sync-gbrain` | `gstack-sync-gbrain` | 让 gbrain 与本仓库代码保持同步，并刷新 CLAUDE.md 中的 agent 搜索指南。封装 gstack-gbrain-sync 编排器，含状态探测、原生代码面注册、能力检查和结论块。可重复运行、幂等。触发词：sync gbrain、refresh gbrain、re-index this repo、gbrain search isn't finding things。（gstack） |
| `systematic-debugging` | `systematic-debugging` | 遇到任何 bug、测试失败或异常行为时使用，须在提出修复方案之前执行。 |
| `talking-head-recut` | `talking-head-recut` | 为已有的口播/访谈/播客视频叠加定时设计的图形卡片——动态标题、下三分之一字幕条、数据标注、引言、侧边面板、画中画——与转录文本同步，可选 16:9/9:16/4:5 画布；原视频在底层不做改动。触发词：graphic overlays、on-screen graphics、包装/美化我的视频。不是普通字幕（用 /embedded-captions）。不确定时用 /hyperframes。 |
| `tamarind` | `tamarind` | 通过 REST API 或 MCP server 访问 Tamarind Bio 平台上的开源分子设计与结构生物学工具集，无需本地 GPU。涵盖结构预测（AlphaFold、Boltz、Chai、ESMFold）、蛋白/结合子/从头设计（RFdiffusion、ProteinMPNN、BoltzGen）、抗体与纳米抗体设计及可开发性、蛋白-配体对接（DiffDock、Autodock Vina）、结合亲和力预测、MSA 生成和分子动力学。当用户提到 Tamarind 或 tamarind.bio、想在云端运行这些开源工具、引用 app.tamarind.bio/api 或 x-api-key header，或需批量提交序列做结构或生物物理表征时使用。 |
| `tdd` | `tdd` | 测试驱动开发。当用户想以测试先行的方式开发功能或修 bug、提到 red-green-refactor，或需要集成测试时使用。 |
| `tdd` | `engineering/tdd` | 测试驱动开发。当用户想以测试先行的方式开发功能或修 bug、提到 red-green-refactor，或需要集成测试时使用。 |
| `tdd-workflow` | `tdd-workflow` | 编写新功能、修复 bug 或重构代码时使用：强制执行测试驱动开发，要求 80% 以上覆盖率，涵盖单元、集成和 E2E 测试。 |
| `teach` | `teach` | 在当前工作区内教用户一项新技能或新概念。 |
| `teach` | `productivity/teach` | 在当前工作区内教用户一项新技能或新概念。 |
| `technical-analyst` | `technical-analyst` | 周线价格图表技术分析。适用于股票、股指、加密货币或外汇；当用户提供图表图片并要求技术分析、趋势识别、支撑/阻力位、情景规划或概率评估时触发；仅基于图表数据，不考虑新闻或基本面因素。 |
| `test-driven-development` | `test-driven-development` | 测试驱动开发：实现任何功能或修复 bug 时，在编写实现代码之前先写测试。 |
| `test-generator` | `test-generator` | 依据真实代码契约生成并验证单元测试或集成测试。用于用户要求为函数、类、接口或缺陷补测试、提高覆盖率、生成回归用例或完善测试策略时；先读取现有测试与调用方，不猜测空值、异常或超时行为，不自动安装框架或访问生产依赖。 |
| `test-quality` | `test-quality` | 用 AssertJ 断言编写高质量 JUnit 5 测试。适用于用户说 add tests、write tests、improve test coverage，或为 Java 代码审查/创建测试类时。 |
| `theme-detector` | `theme-detector` | 检测并分析跨板块的市场热门主题。适用于：用户询问当前市场主题、热门板块、板块轮动、主题投资、哪些主题热或冷，或想识别看多/看空的市场叙事并做生命周期分析。 |
| `theme-factory` | `theme-factory` | 为产物（幻灯片、文档、报告、HTML 落地页等）套用主题样式的工具包。内置 10 套预设主题（配色/字体），可应用到任何已创建的产物，也可即时生成新主题。 |
| `tiledbvcf` | `tiledbvcf` | 用 TileDB 高效存储和检索基因组变异数据：可扩展的 VCF/BCF 摄入、增量添加样本、压缩存储、并行查询，以及面向群体基因组学的导出能力。 |
| `timesfm-forecasting` | `timesfm-forecasting` | 用 Google TimesFM 基础模型做零样本时间序列预测。适用于任何单变量时间序列（销量、传感器、能耗、生命体征、天气），无需训练自定义模型。支持 CSV/DataFrame/数组输入，输出点预测和预测区间。含 preflight 系统检查脚本，首次使用前验证 RAM/GPU。 |
| `to-questionnaire` | `to-questionnaire` | 把自己无法完全回答的决策转化为问卷，交给他人填写。适用于需要向干系人收集信息以推进决策时。 |
| `to-questionnaire` | `productivity/to-questionnaire` | 把自己无法完全回答的决策转化为问卷，交给他人填写。适用于需要向干系人收集信息以推进决策时。 |
| `to-spec` | `to-spec` | 把当前对话整理成 spec 并发布到项目 issue tracker；不做额外访谈，只综合已讨论的内容。 |
| `to-spec` | `engineering/to-spec` | 把当前对话综合为一份 spec 并发布到项目 issue tracker；不做访谈，只提炼已讨论的内容。 |
| `to-tickets` | `to-tickets` | 把计划、规格或当前对话拆解为一组曳光弹式工单，每个工单声明其阻塞依赖边，并发布到配置的跟踪器（本地模式为每工单一个文件、依赖边写成文本；真实跟踪器则用原生 blocking 链接）。 |
| `to-tickets` | `engineering/to-tickets` | 把计划、spec 或当前对话拆解为一组 tracer-bullet ticket，每个声明其阻塞边，发布到配置的 tracker：本地为每 ticket 一个文件用文本描述边，真实 tracker 上用原生 blocking 链接。 |
| `torch-geometric` | `torch-geometric` | PyTorch Geometric（PyG）图神经网络：节点/链接/图分类、消息传递（GCN、GAT、GraphSAGE、GIN）、异构图、邻居采样和自定义数据集。触发场景：使用 torch_geometric 时；不适用于一般 NetworkX 分析或非图类 PyTorch 模型。 |
| `torchdrug` | `torchdrug` | 构建和排查 TorchDrug 0.2.1 工作流：分子图、性质预测、自监督预训练、分子生成、逆合成、蛋白表示学习和知识图谱推理。当代码 import torchdrug 或需要其数据集、模型、任务或 Engine 时使用。 |
| `trade-hypothesis-ideator` | `trade-hypothesis-ideator` | 从市场数据、交易日志和日记片段生成可证伪的交易策略假设。当已有结构化输入包、需要带排名的假设卡（含实验设计、kill 标准）并可选导出兼容 edge-finder-candidate/v1 的 strategy.yaml 时使用。 |
| `trade-performance-coach` | `trade-performance-coach` | 复盘已平仓交易、部分退出和月度交易汇总，评估流程遵守度、风险纪律、执行质量及基于证据的交易行为模式。触发场景：trader-memory-core 和 signal-postmortem 已产出记录后，或用户要求交易后教练、风控式复盘、规则遵守审查、下一交易日操作规则、心理层面的交易行为反馈。不提供买卖建议、心理治疗或券商执行。 |
| `trader-memory-core` | `trader-memory-core` | 跟踪投资论点的全生命周期——从筛选想法到平仓复盘。可从筛选器输出登记论点，管理状态流转，附加仓位规模与复盘到期日，并生成含盈亏与 MAE/MFE 分析的复盘报告。触发词：register thesis、track this idea、thesis status、review due、close position、postmortem、trading journal。 |
| `trading-skills-navigator` | `trading-skills-navigator` | 从自然语言目标推荐合适的交易工作流、技能组合、API 档位和上手路径。作为入口使用：用户表达交易或投资目标、想知道该用哪个 skill/工作流、从哪开始、或某些功能是否不需要付费 API key 时，例如“where do I start”、“which skill should I use”、“I want to swing trade only when the market is favorable”、“what works without API keys”、“どれを使えばいい”、“API キー無しで 使えるものは”。只做路由和解释，从不执行交易或自动运行其他 skill；没有已交付的工作流时会如实说明。 |
| `transformers` | `transformers` | Hugging Face Transformers：加载 Hub 模型、运行 pipeline 推理、文本生成和 Trainer 微调，覆盖 NLP、视觉、音频和多模态任务。适用于使用 AutoModel、pipelines、tokenizers 或 TrainingArguments 的场景；不适用于 Transformers 库之外的一般机器学习。 |
| `treatment-plans` | `treatment-plans` | 在临床决策已由持证专业人员提供并核实之后，对本地治疗方案文档做格式化与结构校验。适用于来源可追溯性、临床医师撰写的干预记录、目标与检查点、共同决策记录、交接核对与发布门禁；不用于临床决策本身。 |
| `triage` | `triage` | 让 issue 和外部 PR 经过一套 triage 角色状态机流转：分类、验证、必要时质询打磨，并产出 agent 可直接执行的 brief。 |
| `triage` | `engineering/triage` | 让 issue 和外部 PR 走 triage 角色状态机：分类、验证、必要时盘问（grill），并撰写 agent 可直接执行的 brief。 |
| `tui-tester` | `tui-tester` | 用终端自动化测试 Gemini CLI 行为和视觉输出的专家指导。 |
| `ui-styling` | `ui-styling` | 用 shadcn/ui 组件（基于 Radix UI + Tailwind）、Tailwind CSS 原子化样式和 canvas 视觉设计创建美观、无障碍的用户界面。适用于构建 UI、实现设计系统、创建响应式布局、添加无障碍组件（对话框、下拉菜单、表单、表格）、定制主题配色、实现深色模式、生成视觉设计和海报，或建立跨应用一致的样式规范。 |
| `ui-to-vue` | `ui-to-vue` | 将 UI 截图或设计稿批量转换为 Vue 3 组件，尤其配合 Vant、Element Plus、Ant Design Vue 等组件库时使用。 |
| `ui-ux-pro-max` | `ui-ux-pro-max` | 面向 Web、移动端和桌面的 UI/UX 设计智能库。适用于设计、构建、审查或修复界面，涵盖页面、组件、设计系统、无障碍、交互、响应式布局、排版、配色、图表和技术栈相关的 UI 实现。内置可搜索的本地数据：79 种风格（50 种启用）、192 套产品配色与推理档案、74 组字体搭配、119 条 UX 准则、105 个图标、17 个 GSAP 预设、25 种图表类型、22 个技术栈。 |
| `umap-learn` | `umap-learn` | 使用 UMAP-learn 做非线性降维、2D/3D 嵌入、聚类预处理，以及有监督/半监督 UMAP、DensMAP、AlignedUMAP、Parametric UMAP 工作流。 |
| `uncertainty-and-units` | `uncertainty-and-units` | 用 pint 和 uncertainties 在科学计算中跟踪物理单位并传播测量不确定度。适用于单位换算与量纲检查、GUM 不确定度预算、A 类和 B 类评定、包含因子与扩展不确定度、Monte Carlo 传播、有效数字与正负号报告、曲线拟合的误差传播、CODATA 常数、审计 Python 代码中丢失单位或不确定度传播断裂的问题，以及用无量纲数（Reynolds、Peclet、Damkohler、Knudsen、Biot、Womersley）、特征尺度（如扩散时间、Debye 长度）和观测数量级范围做量级合理性检查。当用户问这个数物理上合理吗、检查这些单位、这个流动处于什么流态，或结果看起来偏差数个数量级时触发。 |
| `unfreeze` | `gstack-unfreeze` | 清除 /freeze 设置的冻结边界，恢复对所有目录的编辑权限。用于在不结束会话的情况下扩大编辑范围。触发词：unfreeze、unlock edits、remove freeze、allow all edits。（gstack） |
| `unified-memory` | `unified-memory` | 通过本地 ECC Memory Vault 在 Claude、Codex、Hermes、Cursor、OpenCode 等 agent 间共享持久、可检查的上下文与交接。当 agent 需要保存工作状态、转移上下文、接续其他 agent 的任务或搜索共享项目知识时使用。 |
| `uptrend-analyzer` | `uptrend-analyzer` | 用 Monty's Uptrend Ratio Dashboard 数据分析市场广度，诊断当前市场环境。从 5 个成分（广度、板块参与度、轮动、动量、历史背景）生成 0-100 综合评分。当询问市场广度、上升趋势比率，或市场环境是否支持股票敞口时使用。无需 API key。 |
| `us-market-bubble-detector` | `us-market-bubble-detector` | 用修订版 Minsky/Kindleberger 框架 v2.1 通过量化数据驱动分析评估市场泡沫风险。优先采用客观指标（Put/Call、VIX、保证金债务、市场广度、IPO 数据）而非主观印象；具备严格的定性调整标准并防止确认偏差；以强制数据收集和机械化评分支持实际投资决策。适用于：用户询问泡沫风险、估值担忧或止盈时机。 |
| `us-stock-analysis` | `us-stock-analysis` | 全面的美股分析：基本面分析（财务指标、业务质量、估值）、技术面分析（指标、图表形态、支撑/阻力）、个股对比和投资报告生成。当用户要求分析美股代码（如"analyze AAPL""compare TSLA vs NVDA""给我一份微软的报告"）、评估财务指标、技术图表分析或美股投资建议时使用。 |
| `usfiscaldata` | `usfiscaldata` | 查询美国财政部 Fiscal Data REST API 获取联邦金融数据，无需 API key。适用于国家债务（Debt to the Penny）、Daily/Monthly Treasury Statements、国债拍卖、利率、汇率、储蓄债券及美国政府收支统计。 |
| `using-git-worktrees` | `using-git-worktrees` | 当需要开始与当前工作区隔离的功能开发，或在执行实现计划之前使用——通过原生工具或 git worktree 回退机制确保隔离工作区存在。 |
| `using-superpowers` | `using-superpowers` | 在开始任何对话时使用：确立如何查找和使用技能，要求在任何响应（包括澄清性问题）之前先调用 Skill 工具。 |
| `vaex` | `vaex` | 处理和分析超出可用内存的大型表格数据集（数十亿行）。Vaex 擅长核外 DataFrame 操作、惰性求值、快速聚合、大数据高效可视化和大数据集机器学习。适用于用户需要处理大型 CSV/HDF5/Arrow/Parquet 文件、对海量数据做快速统计、创建大数据可视化，或构建无法装入内存的 ML 流水线时。 |
| `value-dividend-screener` | `value-dividend-screener` | 筛选美股高质量分红标的，结合价值特征（P/E 低于 20、P/B 低于 2）、有吸引力的股息率（3% 以上）和持续增长（分红/营收/EPS 三年趋势向上）。支持两阶段筛选：先用 FINVIZ Elite API 高效预筛，再用 FMP API 做详细分析。触发：用户要求分红股筛选、收益型组合思路，或基本面强劲的优质价值股。 |
| `vcp-screener` | `vcp-screener` | 在标普 500 中筛选 Mark Minervini 的波动收缩形态（VCP），并检测单只股票历史价格路径中出现过的 VCP。识别处于 Stage 2 上升趋势、在突破临界点附近形成紧凑底部且波动收缩的股票；历史单股模式会遍历多年历史，输出每个形成的 VCP 及前瞻结果统计（突破/触发止损/超时）。适用于用户请求 VCP 筛选、Minervini 风格形态、紧凑底部形态、波动收缩突破候选、Stage 2 动量股扫描，或对特定股票（如 FIX、TSLA）做历史 VCP 形态研究时。 |
| `venue-templates` | `venue-templates` | 使用目标 venue（期刊/会议等）的格式指南和内置 LaTeX 脚手架，准备期刊稿件、会议论文、学术海报和基金申请文档。适用于选择官方模板、核对当前页数或匿名规则、把学术写作适配到目标 venue，或检查投稿 PDF。 |
| `verification-before-completion` | `verification-before-completion` | 在宣称工作完成、已修复或测试通过之前使用，也在提交或创建 PR 之前使用；必须运行验证命令并确认输出后才能声称成功，始终用证据支撑断言。 |
| `verification-loop` | `verification-loop` | 面向 Claude Code 会话的综合验证系统。在宣称会话工作完成之前，用于验证其产出时使用。 |
| `verify-and-stop` | `verify-and-stop` | 在不扩大范围的前提下证明既有工作满足验收条件。适用于纯验证任务、完成度检查、聚焦的门禁运行和最后一公里证明。 |
| `verify-chain` | `verify-chain` | 角色对抗式技术文章交叉验证：写完 IT 文章后，Critic 提取关键断言并生成核查问题，多个 Verifier SubAgent 在独立上下文联网验证，Repairer 自动修复。用于规避 AI 幻觉、知识过时、信息遗漏。 |
| `vite-patterns` | `vite-patterns` | Vite 构建工具模式：配置、插件、HMR、环境变量、代理设置、SSR、库模式、依赖预构建和构建优化。处理 vite.config.ts、Vite 插件或基于 Vite 的项目时激活。 |
| `vue-patterns` | `vue-patterns` | Vue.js 3 Composition API 模式、组件架构、响应式最佳实践、Pinia 状态管理、Vue Router 导航和 Nuxt SSR 模式。在 Vue、Nuxt、Vite 或 Pinia 项目中激活。构建或审查 Vue 3、Nuxt、Pinia 代码，涉及 Composition API、响应式或路由导航时使用。 |
| `wait-what` | `wait-what` | 叫停信号：上一条消息没有传达清楚，需要重新表述。适用于用户表示没看懂、困惑或信息未落地时。 |
| `wait-what` | `productivity/wait-what` | 停下。上一条消息没有传达清楚——重新表述一遍。 |
| `wayfinder` | `wayfinder` | 把超出单个 agent 会话容量的大型工作规划为 issue 跟踪器上的决策工单共享地图，逐个解决，直到通往目标的路径清晰。适用于规模过大、需要先拆解决策再执行的项目规划。 |
| `wayfinder` | `engineering/wayfinder` | 把超出单个 agent 会话容量的大块工作规划为 issue tracker 上的决策 ticket 共享地图，逐个解决直到通往目标的路径清晰。 |
| `waypoint-bio` | `waypoint-bio` | 使用 Outpost Bio 开源微生物组基础模型时适用：Waypoint 检查点（Waypoint-6m/45m/170m）、Atlas 预训练语料、Compass 八任务基准，以及 waypoint-bio 包的 waypoint CLI。覆盖微生物组样本嵌入、在分类丰度数据上微调、在 Compass 上评测检查点、用丰度谱预训练 GPT-2 模型，以及把 MetaPhlAn、Kraken2、QIIME 2、MGnify 丰度表转换为 waypoint 格式。 |
| `web-artifacts-builder` | `web-artifacts-builder` | 用现代前端技术（React、Tailwind CSS、shadcn/ui）创建复杂多组件 claude.ai HTML artifacts 的工具套件。用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifact；简单单文件 HTML/JSX artifact 不适用。 |
| `web-recorder` | `web-recorder` | 把网页上的重复操作录下来，之后让 AI 自动执行。例如每天导出数据、每周提交报表、批量处理单据；录一次，以后说帮我运行即可。触发词：录制网页、录脚本、帮我录、自动化、重复操作、导出数据脚本、网页自动化、RPA、录操作、录制浏览器、录制网页操作、帮我录一个XXX脚本、录制一个自动化流程、生成网页脚本、录制RPA、录制自动化、网页操作录制、浏览器录制、录制流程、把手动操作变成自动脚本、录制一次以后自动跑。支持 SSO 登录、API 分析、选择器验证、下载类型自动识别。不适用于：简单网页数据爬取（用爬虫技能）、单次网页操作（用 browser 工具）。 |
| `webapp-testing` | `webapp-testing` | 用 Playwright 交互和测试本地 Web 应用的工具集。支持验证前端功能、调试 UI 行为、截取浏览器截图和查看浏览器日志。 |
| `weekly-performance-digest` | `weekly-performance-digest` | 从已平仓的 trader-memory-core 论点生成每周绩效摘要：胜率、期望值、盈亏因子、R 倍数、MAE/MFE，以及按来源技能、退出原因、论点类型、板块和机制的胜负模式分析。无需 API，纯本地计算。 |
| `what-if-oracle` | `what-if-oracle` | 运行结构化 What-If 情景分析，做 4-6 个分支可能性探索（最佳、可能、最差、意外、逆向、二阶效应）。适用于：用户就不确定未来、战略分岔、应急预案提出推测性 what-if 问题，或想在承诺前对决策做压力测试。 |
| `wizard` | `wizard` | 生成交互式 bash 向导，引导人类完成只有人能执行的步骤。适用于基础设施开通、配置凭据或 CI secret、操作不熟悉的第三方控制台、执行一次性迁移或切换。agent 自己能完成的步骤不要调用此 skill。 |
| `wizard` | `engineering/wizard` | 生成交互式 bash 向导，引导人类完成只有人能执行的步骤。适用于基础设施开通、配置凭据或 CI secret、操作不熟悉的第三方控制台、执行一次性迁移或切换。agent 自己能完成的步骤不要调用此 skill。 |
| `workflow-runner` | `workflow-runner` | 在 Claude Code / OpenClaw / Cursor 中直接运行 agency-orchestrator YAML 工作流，无需 API key，使用当前会话的 LLM 作为执行引擎。当用户提供 .yaml 工作流文件或要求多角色协作完成任务时触发。 |
| `wps-excel` | `wps-excel` | WPS 表格智能助手，通过自然语言操控 Excel，解决公式编写、数据清洗、图表创建等痛点问题。 |
| `wps-office` | `wps-office` | WPS Office 跨应用智能助手，统一管理 Excel、Word、PPT 三大应用，处理跨应用操作和通用功能。 |
| `wps-ppt` | `wps-ppt` | WPS 演示智能助手，通过自然语言操控 PPT，解决排版美化、内容生成、动画设置等痛点问题。 |
| `wps-word` | `wps-word` | WPS 文字智能助手，通过自然语言操控 Word 文档，解决排版、格式、内容编辑等痛点问题。 |
| `writing-beats` | `in-progress/writing-beats` | 写作利用阶段（exploit）：把原始素材组装成由节拍（beats）构成的叙事旅程，在每个节拍依赖某术语之前先铺垫解释该术语。 |
| `writing-beats` | `writing-beats` | 写作技法（exploit 方向）：把原始素材组织成 beats 旅程，在每个 beat 依赖某术语之前先铺垫解释该术语。 |
| `writing-for-agents` | `writing-for-agents` | 为 agent 编写文档的规范。适用于创建或编辑 skill，或修改 AGENTS.md、CLAUDE.md 时。 |
| `writing-for-agents` | `productivity/writing-for-agents` | 为 agent 编写文档的规范。适用于创建或编辑 skill，或修改 AGENTS.md、CLAUDE.md 时。 |
| `writing-fragments` | `in-progress/writing-fragments` | 写作探索阶段（explore）：挖掘原始素材片段，暂不组织结构。 |
| `writing-fragments` | `writing-fragments` | 写作探索阶段：挖掘原始素材片段，尚不做结构化。 |
| `writing-great-skills` | `writing-great-skills` | 编写和编辑优质技能的参考——让技能行为可预测的词汇与原则。 |
| `writing-plans` | `writing-plans` | 当你有规格说明或需求用于多步骤任务时，在动手写代码之前使用。 |
| `writing-shape` | `in-progress/writing-shape` | 写作利用阶段（exploit）：把原始素材逐段塑造成文章。 |
| `writing-shape` | `writing-shape` | 写作利用阶段：把原始素材逐段塑造成文章。 |
| `writing-skills` | `writing-skills` | 在创建新技能、编辑现有技能或部署前验证技能是否有效时使用。 |
| `xlsx` | `xlsx` | 凡以电子表格文件为主要输入或输出的任务都用此 skill：打开、读取、编辑或修复现有 .xlsx、.xlsm、.xltx、.csv、.tsv 文件（加列、算公式、格式化、做图表、清洗脏数据）；从零或其他数据源创建新表格；表格格式互转。用户按名称或路径提到表格文件（哪怕随口说"下载目录里的 xlsx"）并要求处理或产出时尤其要触发；也适用于把杂乱表格数据（畸形行、错位表头、垃圾数据）清洗重构为规范表格。交付物必须是电子表格文件。主要交付物是 Word 文档、HTML 报告、独立 Python 脚本、数据库管道或 Google Sheets API 集成时不触发，即使涉及表格数据。 |
| `zarr-python` | `zarr-python` | Zarr-Python 3：面向云存储的分块 N 维数组。支持压缩数组、并行 I/O、经 fsspec 访问 S3/GCS，兼容 NumPy/Dask/Xarray，适用于大规模科学计算流水线。 |
| `zh-code-reviewer` | `zh-code-reviewer` | 中文代码审查专家：生成详细的中文代码审查报告。适用于需要中文输出的代码评审场景。 |
| `zh-docgen` | `zh-docgen` | 中文文档生成器：从代码库自动生成中文技术文档。 |
| `zh-readme` | `zh-readme` | 中文 README 生成器：先分析项目结构与代码，再生成面向中文开发者的高质量中文 README。适用于为项目新建或重写中文说明文档。 |

## 第三部分：`agent-skills/self-skills/`（用户自写）

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`（用户自写 skill 真源）

共 **16** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `archify` | `robot-aiot-draw-flowchart/archify` | 创建精致且经过校验的架构图、工作流图、时序图、数据流图和生命周期/状态图，输出为可交互的独立 HTML（内联 SVG），支持深色/浅色主题、可选轨迹动画，以及 PNG/JPEG/WebP/SVG/WebM 导出。接受自然语言需求或粘贴的 Mermaid flowchart、sequenceDiagram、stateDiagram 输入；图表需反映真实代码时会检查仓库证据。适用于用户要求可视化系统架构、基础设施、云/安全/网络拓扑、技术工作流、API 调用时序、请求生命周期、数据管道、ETL/ELT、数据血缘、状态机，或转换/美化 Mermaid 时。 |
| `dev-paradigm-matt` | `dev-paradigm-matt` | 面向日常工程开发的分层工作流路由 skill：按任务所处阶段，把需求澄清、规格设计、架构规划、实现、调试、审查、交接和长期维护路由到合适的 matt-skills，而非强迫所有任务走同一条固定流水线。适用于"这个需求该怎么推进""从需求到代码怎么分阶段""该先 grill 还是 to-spec""Bug/重构/新功能分别怎么走""完整开发流程怎么编排""开发范式""dev-paradigm-matt"（曾用名 dev-paradigm）等场景；也是接手陌生项目时先做 setup、领域建模、票据拆分、实现收尾或长期维护规划的统一入口。 |
| `easy-crawler` | `easy-crawler` | 可独立部署的网页抓取 skill。统一处理通用网页抓取、社媒平台抓取专项优化和反爬/浏览器自动化场景。用户提到抓网页、抓列表页/详情页、抓社媒搜索/评论/创作者主页，或需要浏览器自动化、代理、登录态复用、反爬边界说明时触发。优先给出统一任务契约、可观测输出和显式失败，不把未实现的平台逆向能力伪装成已支持。 |
| `mac-safe-storage-cleaner` | `mac-safe-storage-cleaner` | 安全检查并清理当前 macOS 机器上的缓存、日志、临时文件、下载目录安装包和受控的 Workspace 历史目录。用户提到清理系统缓存、清理文件占用、清理 Workspace 占用、清理日志、磁盘空间不够、删除临时文件、清理 Downloads、清理 IDEA 日志、清理 Workspace 历史、查看可删文件、分析占用、磁盘瘦身时触发。也适用于复查清理规则、验证保护目录、确认是否会误删，以及执行先分析、再确认、最后决定是否删除的交互流程。 |
| `opsx-workflow-hooks` | `opsx-workflow-hooks` | opsx 工作流的命令后钩子。触发 A：/opsx/propose 生成全部 artifact 后立即进入迭代打磨循环，询问用户是否有新想法并更新提案 artifact，直到用户满意；非平凡的 artifact 分析或起草用全新 sub agent，再回主线程验证并呈现结果。触发 B：/opsx/apply 到达实现完成交接点（所有任务完成，或仅剩 SIT/UAT/人工检查等用户侧验证）时，在用户花时间人工验证前先跑审查/测试/验证，修复关键问题，仅在所有任务真正完成时才归档；审查验证尽量在干净 sub agent 中跑，再回主线程做决策、修复和归档。普通实现中途暂停不触发。适用于"/opsx/propose is done""proposal artifacts created""all tasks complete after apply""apply finished""implementation complete"等场景。 |
| `robot-aiot-adr-confluence` | `robot-aiot-adr-confluence` | 技术方案文档端到端工作流：先做信息评估，再按需做需求收敛、追问澄清和方案比较，最后生成 ADR、技术提案或决策简报，并在需要时发布到 Confluence。适用于"写技术方案""生成 ADR""输出技术提案""写决策简报""架构决策记录发 Confluence""方案归档到 Confluence""技术选型文档输出"等场景。用户只要文档时可停在 Markdown 草稿；明确要求发布时才进入 Confluence 发布阶段。 |
| `robot-aiot-adr-generator` | `robot-aiot-adr-generator` | 生成并校验 ADR 架构决策记录：先根据业务/技术需求产出标准 ADR 文档，再按需对其中可外部验证的关键技术断言执行验证链核查。适用于生成 ADR、写架构决策记录、输出技术选型归档、ADR 发布前审稿、校验版本/兼容性/性能说法等场景。输出优先服务技术决策归档，而非通用技术文章写作。 |
| `robot-aiot-commit` | `robot-aiot-commit` | 为本项目生成统一格式的中文提交说明，并在用户明确要求时配合 Git 流程执行 commit。适用于生成 commit message、按规范提交、总结 diff、写提交说明、提交代码、根据分支提取 JIRA、按 FEAT/FIX/ENH/DOC/CHORE 分类提交等场景。输出优先服务本项目提交规范，而非通用 Conventional Commits 模板。 |
| `robot-aiot-docs-sync` | `robot-aiot-docs-sync` | 扫描当前项目并创建或更新一套可溯源的项目文档：AGENTS.md、README.md、CHANGELOG.md、docs/project-map.md、docs/architecture.md。适用于"更新项目文档""同步文档""更新 README""更新 AGENTS.md""生成 changelog""生成项目地图""补齐架构说明"等场景。吸收 changelog、中文文档、README 和 Diataxis 文档分层能力，仅在上述 5 个文件内做结构化增强，不修改源代码、配置文件或测试文件。 |
| `robot-aiot-draw-flowchart` | `robot-aiot-draw-flowchart` | 机器人/IoT 业务图表绘制能力。三条输出路径：draw.io XML（可编辑主路径）、直绘 SVG/HTML（汇报级展示）、archify 内置渲染（主题切换+导出）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑、时间线、Agent/记忆架构等 40+ 图表类型；内置机器人视觉语言、12 套 SVG 风格皮肤与品牌 token 定制、几何/构图校验、PNG/GIF 导出与 drawio/Mermaid 导入重绘。 |
| `robot-aiot-knowledge-expert` | `robot-aiot-knowledge-expert` | 物联网全栈技术专家回答规范。当用户问 IoT/AIOT 架构设计、协议选型、平台集成、边云协同、性能调优、故障排查等问题时使用。触发词包括：物联网、IoT、AIOT、MQTT、Modbus、BACnet、OPC UA、EMQX、物模型、边云协同、设备影子、OTA、JetLinks、ThingsBoard、感认行。 |
| `robot-aiot-leadership-ppt-workflow` | `robot-aiot-leadership-ppt-workflow` | 将项目数据和技术分析转化为结构化的领导汇报 PPT，覆盖全链路五阶段工作流：建立数据池 → 技术明细版+领导汇报版文档分层 → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML → 调用 robot-aiot-xml-html-bridge 将 XML 稳定转 HTML 并保留原样式 → 调用 robot-aiot-slide-html-author 完成 PPT 母稿逐页 HTML 化 → 调用 ppt-master 依据每页 HTML 样式生成最终 PPTX。当用户要求"写领导汇报PPT""出PPT母稿""做汇报材料""汇报方案""写PPT""领导汇报""生成汇报PPT"时触发；也适用于需要把技术项目数据转化为管理层可读汇报格式的场景。 |
| `robot-aiot-self-skill-sync` | `robot-aiot-self-skill-sync` | 批量同步 self 目录下所有 git 项目与 skill 库。模块 1 递归三层扫描嵌套 git 仓库批量更新，处理网络重试与冲突；模块 2 管理 OpenSpec：运行 openspec init/update，把 opsx/ 命令与 openspec-* skills 同步到 ~/.agents；模块 3 外部 skill 为 npx 管理型（superpowers 等 7 个），用 npx skills@latest update 更新，失败按本地克隆 rsync 兜底；模块 3.3/3.4 对 self-skills/ 自写 skill 与命令按文件级比对双向同步（真源新则部署，运行时新则回写），只更新不新增；模块 4 把 ~/.agents/skills/ 同步到个人知识库（排除自写）；模块 5 更新 docs/skills-overview.md。核心原则：只增改不删除；同步先比对内容+mtime，严禁旧覆盖新，目标端更新标 [NEWER-TARGET] 跳过；用户维护的代码禁止回滚或自动冲突处理，异常直接提示并跳过。 |
| `robot-aiot-slide-html-author` | `robot-aiot-slide-html-author` | 为领导汇报类 PPT/母稿生成固定画布（1920x1080）的逐页 HTML：执行时引用 ui-ux-pro-max 的设计系统与审查能力，内化语义化设计 token、清晰/克制/层次原则与高级感标准（反模板化排版、色彩/形状一致性锁定、AI 痕迹清单、审查修复工作流）。适用于 PPT 母稿转单页 HTML、领导汇报页落成 HTML、逐页生成 slide HTML、给 ppt-master 准备逐页 HTML、修复汇报页布局/样式/信息层级、把图表 HTML 嵌入汇报页；也适用于已有 Markdown 母稿、页面草图或图表 HTML、需保持图表真源与页面视觉体系一致的任务。图表 HTML 有问题时可调用 robot-aiot-xml-html-bridge 审查修复。 |
| `robot-aiot-xml-html-bridge` | `robot-aiot-xml-html-bridge` | 把 robot-aiot-draw-flowchart 或其他 draw.io / mxGraph XML 图表稳定转换为 HTML 预览稿，尽可能保留原始样式、布局、层级、配色、尺寸比例与文本关系。触发：XML转HTML、draw.io转HTML、mxGraph转HTML、图表转网页预览、先转HTML再转PPT、保留原样式输出HTML。也适用于领导汇报 PPT 工作流中，在 PPT 生成前先落一层 HTML 作为页面主约束的场景。 |
| `stock-replay-workbench` | `stock-replay-workbench` | 当用户要求 A股盘后复盘、收盘简报、主线题材梳理、强势股/观察池、个股为何走强、题材与资金联动、龙虎榜/公告/研报/财务交叉分析，或股票查询需从简单行情扩展为含任务路由、来源优先级、时间戳、警示和分层结论的结构化工作流时触发。覆盖打板情绪（涨停/炸板/跌停/昨涨停四池+连板分析+涨停揭秘）、ETF期权（T型报价+希腊字母+IV）、舆情互动（热榜/人气榜/互动易）等能力；多股对比和多维复盘通过 sub-agent 并行编排，深度报告强制经 cross-check-reviewer 第二意见复查校对。 |
