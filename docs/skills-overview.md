# 技能总览

本文档汇总三个技能目录：`~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/`，根据各目录下实际存在的 `SKILL.md` 递归生成。技能名称优先读取 frontmatter `name`（缺失回退目录名）；说明为基于原始 `description` 提炼的中文摘要（≤500 字，简洁概括用途与触发场景）。

## 第一部分：`~/.agents/skills/`

扫描目录：`/Users/kangll13/.agents/skills/`（运行时技能目录）

共 **127** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `academy-guide` | `academy-guide` | 回答 Claude 产品使用类问题前必查：从 Claude Academy（academy.claude.com）推荐匹配的课程、教程与用例。触发于“how do I”“getting started”“what can Claude do”“teach me”等学习类提问、artifacts/skills/MCP 相关问题、团队培训或入门材料请求。与文档回答配合使用；仅强匹配时推荐，不杜撰课程内容。 |
| `algorithmic-art` | `algorithmic-art` | 用 p5.js 结合种子随机与交互参数探索创作算法艺术。用户要求代码艺术、生成艺术、流场、粒子系统时使用。须创作原创作品，不得复制现有艺术家以防侵权。 |
| `api-contract-review` | `api-contract-review` | 审查 REST API 契约：HTTP 语义、版本管理、向后兼容与响应一致性。用户说 "review API""check endpoints""REST review"，或发布 API 变更前使用。 |
| `api-tester` | `api-tester` | 依据真实 OpenAPI、路由实现与现有测试生成并验证 API 测试。用于测试接口、补集成测试、验证 API 契约、生成回归用例或排查接口兼容性；区分“生成测试”与“执行请求”的授权，不猜测状态码、响应结构或 SLA，不在未确认环境发送写请求。 |
| `archify` | `archify` | 生成经过校验的架构图、工作流图、时序图、数据流图、生命周期/状态机图，输出可交互独立 HTML（内联 SVG、深/浅主题、可选轨迹动画，支持 PNG/JPEG/WebP/SVG/WebM 导出）。接受自然语言需求或 Mermaid 输入，可检查代码仓库证据。用于系统架构、云/安全/网络拓扑、API 调用时序、数据管道、ETL/ELT、数据血缘等可视化，以及 Mermaid 转换美化。 |
| `architecture-review` | `architecture-review` | 宏观分析 Java 项目架构：包结构、模块边界、依赖方向与分层。触发于“review architecture”“check structure”“package organization”等，或评估代码库是否符合整洁架构原则。 |
| `ask-matt` | `ask-matt` | 技能路由器：当你不确定该用哪个 skill 或流程时，询问当前处境并推荐仓库中最合适的技能。 |
| `banner-design` | `banner-design` | 为社交媒体、广告、网站 hero、创意资产和印刷品设计 banner，提供多种艺术方向选项，可用生成或自带视觉素材。触发：design/create/generate banner；平台覆盖 Facebook、Twitter/X、LinkedIn、YouTube、Instagram、Google Display、网站 hero、印刷；风格含极简、渐变、粗字体、照片、插画、几何、复古、玻璃拟态、3D、霓虹、双色调、编辑风、拼贴。 |
| `brand` | `brand` | 品牌语调、视觉识别、信息框架、资产管理与品牌一致性。涉及品牌内容、语气设定、营销资产、品牌合规、风格指南时启用。 |
| `brand-guidelines` | `brand-guidelines` | 将 Anthropic 官方品牌配色与字体应用于各类产出物。用于需要 Anthropic 视觉风格、品牌规范、视觉格式或公司设计标准的场景。 |
| `canvas-design` | `canvas-design` | 用设计哲学在 .png 和 .pdf 文档中创作视觉艺术。用户要求海报、艺术品、设计或其他静态作品时使用。须原创设计，不得复制现有艺术家以防侵权。 |
| `changelog-generator` | `changelog-generator` | 从 git commits 生成 changelog。用户说 generate changelog、update changelog、what changed since last release，或准备新版本发布前使用。 |
| `claude-handoff` | `claude-handoff` | 把当前对话移交给一个全新的后台 agent，立即接手继续工作。 |
| `clean-code` | `clean-code` | Clean Code 原则（DRY、KISS、YAGNI）、命名、函数设计与可读性。代码难读、方法过长、命名不清、重复或深嵌套时使用；类职责划分与依赖方向问题改用 solid-principles。 |
| `code-review` | `code-review` | 从固定基点（commit、branch、tag 或 merge-base）起沿两条轴审查变更：Standards（代码是否符合仓库成文编码标准）与 Spec（是否符合原始 issue/规格要求）。以并行 subagent 运行两项审查并排汇报。审查分支、PR、进行中的改动，或用户要求 "review since X" 时使用。 |
| `codebase-design` | `codebase-design` | 深模块设计的共享词汇。用于设计或改进模块接口、寻找深化机会、决定接缝位置、提升代码可测试性与 AI 可导航性，或其他 skill 需要深模块词汇时。 |
| `concurrency-review` | `concurrency-review` | 审查 Java 并发代码的线程安全、竞态条件、死锁和现代模式（Virtual Threads、CompletableFuture、@Async）。用户要求 check thread safety、concurrency review、async code review 或审查多线程代码时使用。 |
| `design` | `design` | 综合设计能力：品牌识别、design tokens、UI 样式、logo 生成（55 种风格，支持 Gemini/Atlas Cloud/MuAPI AI）、CIP 企业形象方案（50 项交付物）、HTML 演示（Chart.js）、banner 设计（22 种风格）、图标设计（15 种风格 SVG）、社交配图（HTML→截图，多平台）。触发：设计 logo、生成 mockup、做 slide、banner、图标、社媒图片、品牌识别、设计系统；覆盖 Facebook/Twitter/LinkedIn/YouTube/Instagram/Pinterest/TikTok 等平台。 |
| `design-patterns` | `design-patterns` | 常见设计模式的 Java 示例（Factory、Builder、Strategy、Observer、Decorator 等）。用户要求实现某模式或设计可扩展组件时使用。 |
| `design-system` | `design-system` | 设计 token 架构、组件规格与幻灯片生成：三层 token（primitive→semantic→component）、CSS 变量、间距/字体比例、组件规格与策略性幻灯片创建。用于设计 token、系统化设计与品牌合规演示。 |
| `dev-paradigm-matt` | `dev-paradigm-matt` | 分层工作流路由 skill：按任务阶段把需求澄清、规格设计、架构规划、实现、调试、审查、交接和长期维护路由到合适的 matt-skills，而非所有任务走同一条流水线。适用于「这个需求该怎么推进」「该先 grill 还是 to-spec」「Bug/重构/新功能分别怎么走」、接手陌生项目、setup、领域建模、票据拆分等场景的统一入口。 |
| `diagnosing-bugs` | `diagnosing-bugs` | 面向疑难 bug 与性能回退的诊断循环。用户说 "diagnose""debug this"，或报告某功能损坏/抛错/失败/变慢时使用。 |
| `diagram-design` | `diagram-design` | 生成品牌化架构图、流程图、时序图、状态机、ER/数据模型、时间线、泳道、雷达图、甘特图、桑基图、鱼骨图、Wardley map、UML 类图、数据库 schema 等 40+ 类图表，输出独立 HTML/SVG/PNG；可重绘 .drawio、Mermaid .mmd、.excalidraw 源文件，从网站提取品牌 token，支持语义标注、无障碍动效与手绘风格。 |
| `discernment-nudge` | `discernment-nudge` | 在给出用户可能据以行动的实质性回答或草稿（建议推荐、目标/计划/proposal/邮件草稿、估算预测、数据分析解读、可依赖的事实断言、多步论证）后、定稿前调用：追加 2-3 个针对所产内容具体点的追问，帮助用户核查关键事实、检验推理与假设、发现缺失上下文；每次对话最多一次。简单查询、纯教学解释、格式转换、用户自己运行的代码、创意写作、闲聊，或用户已要求复查引用时跳过。 |
| `django-patterns` | `django-patterns` | Django 架构模式、DRF REST API 设计、ORM 最佳实践、缓存、signals、middleware 及生产级应用。构建或审查 Django 应用、DRF API、ORM 查询或缓存时使用。 |
| `django-security` | `django-security` | Django 安全最佳实践：认证、授权、CSRF 防护、SQL 注入与 XSS 防护、安全部署配置。审查 Django 认证授权、输入处理或部署设置时使用。 |
| `django-tdd` | `django-tdd` | 基于 pytest-django 的 Django 测试策略与 TDD 方法：factory_boy、mocking、覆盖率与 DRF API 测试。用于编写 Django/DRF 测试或测试先行开发功能。 |
| `django-verification` | `django-verification` | Django 项目发布或提 PR 前的验证循环：migrations、linting、带覆盖率的测试、安全扫描与部署就绪检查。 |
| `doc-coauthoring` | `doc-coauthoring` | 引导用户走结构化的文档共著流程。用户想写文档、proposal、技术规格、决策文档等结构化内容时使用；帮助高效传递上下文、迭代打磨内容，并验证文档对读者有效。 |
| `docx` | `docx` | 创建、读取、编辑、操作 Word 文档（.docx）与模板（.dotx）。触发于 Word 文档相关请求：目录、标题、页码、信头等专业格式，提取/重组内容，插入替换图片，查找替换，修订与批注，或要求以 Word 交付报告、备忘录、信函、模板。不适用于 PDF、表格或与文档生成无关的编码任务。 |
| `domain-modeling` | `domain-modeling` | 构建和打磨项目领域模型。讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。 |
| `fastapi-patterns` | `fastapi-patterns` | FastAPI 最佳实践：项目结构、Pydantic v2 schemas、依赖注入、async handlers、认证授权、事务服务层、httpx 与 pytest 测试。构建或审查 FastAPI 应用时使用。 |
| `frontend-design` | `frontend-design` | 构建或改造 UI 时的视觉设计指导：确定美学方向与字体排印，做出有辨识度的设计选择，避免模板化默认观感。 |
| `git-commit` | `git-commit` | 为 Java 项目生成 conventional commit 提交信息。用户说 "commit""create commit""commit changes" 或代码改动完成需要提交时使用。 |
| `git-guardrails-claude-code` | `git-guardrails-claude-code` | 配置 Claude Code hooks，在危险 git 命令（push、reset --hard、clean、branch -D 等）执行前拦截。用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中封禁 git push/reset 时使用。 |
| `grill-me` | `grill-me` | 通过毫不留情的追问打磨方案或设计。 |
| `grill-with-docs` | `grill-with-docs` | 通过持续追问打磨计划或设计，过程中同步产出 ADR 和术语表文档。 |
| `grilling` | `grilling` | 就方案、决策或想法对用户穷追不舍地拷问。用于用户想压力测试自己的思考，或说出 grill 类触发语时。 |
| `handoff` | `handoff` | 把当前对话压缩成交接文档，供另一个 agent 接手继续。 |
| `humanizer` | `humanizer` | 重写 AI 腔文本，使其读起来像真人作者且不改变原意。针对“不是X而是Y”排比、结尾金句、套路化开场、强行三段式、滥用破折号、夸张宣传语等 AI 痕迹，基于 Wikipedia 的“Signs of AI writing”。 |
| `i-have-adhd` | `i-have-adhd` | 为 ADHD 读者塑造输出形态：先给下一步动作、多步任务编号、跨轮重述进度状态、抑制跑题、给具体时间估计、让成果可见。用 /i-have-adhd 调用，说 "stop adhd mode" 关闭。 |
| `implement` | `implement` | 根据 spec 或一组 tickets 实现具体工作。 |
| `implement-spec` | `implement-spec` | 将规格说明（spec）实现为代码。 |
| `improve-codebase-architecture` | `improve-codebase-architecture` | 扫描代码库寻找模块深化（deepening）机会，生成可视化 HTML 报告，并对选中的机会进行追问深挖。 |
| `internal-comms` | `internal-comms` | 撰写各类公司内部沟通材料的资源集：状态报告、领导层更新、3P updates、公司 newsletter、FAQ、事故报告、项目进展等。被要求写内部沟通时使用。 |
| `issue-triage` | `issue-triage` | 给 GitHub issue 分诊并打优先级标签。用户说 triage issues、check issues、review open issues 或例行维护 issue 积压时使用。 |
| `java-code-review` | `java-code-review` | Java 系统化代码审查：空安全、异常处理、并发与性能检查。触发于“review code”“check this PR”“code review”或合并变更前。 |
| `java-migration` | `java-migration` | Java 项目大版本升级指南（8→11→17→21→25）。触发于“upgrade Java”“migrate to Java 25”等诉求或老旧项目现代化改造。 |
| `jpa-patterns` | `jpa-patterns` | JPA/Hibernate 模式与常见陷阱（N+1、懒加载、事务、查询）。用户遇到 JPA 性能问题、LazyInitializationException，或询问实体关系与抓取策略时使用。 |
| `logging-patterns` | `logging-patterns` | Java 日志最佳实践：SLF4J、JSON 结构化日志、MDC 请求追踪，含面向 Claude Code 调试的 AI 友好日志格式。用于编写日志、调试应用流程或分析日志。 |
| `loop-me` | `loop-me` | 在当前 workspace 内，就我想构建的工作流规格对我进行严格追问（grill）。 |
| `maven-dependency-audit` | `maven-dependency-audit` | 审计 Maven 依赖的过时版本、安全漏洞与冲突。触发于“check dependencies”“audit dependencies”“outdated deps”或发布前检查。 |
| `mcp-builder` | `mcp-builder` | 创建高质量 MCP（Model Context Protocol）服务器的指南，通过设计良好的 tools 让 LLM 与外部服务交互。用于以 Python（FastMCP）或 Node/TypeScript（MCP SDK）构建 MCP 服务器集成外部 API。 |
| `migrate-to-shoehorn` | `migrate-to-shoehorn` | 将测试文件中的 as 类型断言迁移到 @total-typescript/shoehorn。触发于提及 shoehorn、想替换测试中的 as、或需要部分测试数据时。 |
| `openspec-apply-change` | `openspec-apply-change` | 实现 OpenSpec change 中的任务。用户想开始实现、继续实现或逐项推进任务时使用。 |
| `openspec-archive-change` | `openspec-archive-change` | 在实验性工作流中归档已完成的 change。实现完成后用户想收尾归档时使用。 |
| `openspec-bulk-archive-change` | `openspec-bulk-archive-change` | 一次性归档多个已完成的 OpenSpec 变更，用于批量归档并行变更。 |
| `openspec-continue-change` | `openspec-continue-change` | 继续推进 OpenSpec 变更，创建下一个 artifact。用于用户想推进变更进度或延续工作流时。 |
| `openspec-explore` | `openspec-explore` | 进入 explore 模式——探索想法、调查问题、澄清需求的思考伙伴。用户想在变更开始前或进行中梳理思路时使用。 |
| `openspec-ff-change` | `openspec-ff-change` | 快进式创建 OpenSpec 变更所需的全部 artifacts，跳过逐个生成的步骤。用于用户想快速备齐实施材料时。 |
| `openspec-new-change` | `openspec-new-change` | 用 OpenSpec 实验性 artifact 工作流启动新的 change。用户想以结构化分步方式创建新功能、修复或修改时使用。 |
| `openspec-onboard` | `openspec-onboard` | OpenSpec 引导式入门：带讲解走完一个完整工作流周期，并结合真实代码库实际操作。 |
| `openspec-propose` | `openspec-propose` | 一步生成 OpenSpec 变更的全部 artifacts（design、specs、tasks）。用于用户想快速描述需求并获得可直接实施的完整提案。 |
| `openspec-sync-specs` | `openspec-sync-specs` | 将变更中的 delta spec 同步到主 specs，但不归档变更。用于用户想用增量更新主 specs 时。 |
| `openspec-update-change` | `openspec-update-change` | 通过修订 OpenSpec change 的现有 planning artifacts 并保持彼此一致来更新 change。用于修订计划、纳入新决策、编辑后对齐 artifacts。从不编辑代码。 |
| `openspec-verify-change` | `openspec-verify-change` | 校验实现与 OpenSpec change 产物一致。用户想在归档前验证实现完整、正确且连贯时使用。 |
| `opsx-workflow-hooks` | `opsx-workflow-hooks` | opsx 工作流的后置命令钩子。触发 A：/opsx/propose 生成全部 artifacts 后进入迭代打磨循环，询问用户新想法并更新提案直到满意，非平凡分析用全新 sub agent。触发 B：/opsx/apply 达到实现完成交接后，在用户人工验证（SIT/UAT）前运行 review/test/verification、修复关键问题，全部任务真正完成才归档。普通实现中暂停不触发。 |
| `pdf` | `pdf` | 处理 PDF 文件的一切任务：读取/提取文本表格、合并、拆分、旋转页面、加水印、创建 PDF、填表单、加密解密、提取图片、扫描件 OCR。用户提及 .pdf 文件或要求产出 PDF 时使用。 |
| `performance-smell-detection` | `performance-smell-detection` | 检测 Java 代码级性能坏味道：streams、集合、装箱、正则、对象创建。仅提供风险提示而非定论，优化前务必实测；JPA/数据库性能问题改用 jpa-patterns。 |
| `ppt-master` | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑 PPTX 幻灯片、重建页面视觉、创建可复用 Brand/Style/Layout/Deck 工作区、填充原生 PPTX 模板、美化成品文件。触发于创建/重建/美化/模板化/填充 PPT、PPTX、幻灯片或课件，含添加旁白动画或生成演示视频。 |
| `pptx` | `pptx` | 任何涉及 .pptx 或 .potx 文件的任务都用它：创建 slide deck、pitch deck、演示文稿；读取、解析、提取文本（即使内容用于邮件或摘要等其他用途）；编辑修改现有演示；合并拆分 slide 文件；处理模板、layout、speaker notes、comments。用户提到 deck、slides、presentation 或相关文件名时触发。 |
| `prototype` | `prototype` | 构建一次性原型来回答设计问题。用于验证状态模型或逻辑是否合理，或探索 UI 应该长什么样。 |
| `python-patterns` | `python-patterns` | Python 惯用写法、PEP 8 规范、类型提示与最佳实践。用于编写或审查 Python 代码，或讨论惯用结构、typing、PEP 8 时。 |
| `python-testing` | `python-testing` | Python 测试策略：pytest、TDD 方法论、fixtures、mocking、参数化与覆盖率要求。编写 pytest 测试（fixtures、mocks、参数化、覆盖率）时使用。 |
| `pytorch-lightning` | `pytorch-lightning` | PyTorch Lightning 深度学习框架指南：将 PyTorch 代码组织为 LightningModule，配置 Trainer 支持多 GPU/TPU，构建数据管道、callbacks 与日志（W&B、TensorBoard、MLflow），实现 DDP/FSDP/DeepSpeed 分布式训练，用于可扩展的神经网络训练。 |
| `pytorch-patterns` | `pytorch-patterns` | PyTorch 深度学习模式与最佳实践，构建稳健、高效、可复现的训练管线、模型架构与数据加载。编写或审查 PyTorch 训练循环、模型架构、数据加载，或实验无法复现时使用。 |
| `refactor-advisor` | `refactor-advisor` | 重构顾问，识别代码坏味道并提供重构方案。 |
| `research` | `research` | 调研类能力：针对高可信一手来源调查问题，把发现整理成 Markdown 文件存入仓库。用户想调研主题、收集文档或 API 事实、或把阅读工作交给后台 agent 时使用。 |
| `resolving-merge-conflicts` | `resolving-merge-conflicts` | 需要解决进行中的 git merge/rebase 冲突时使用。 |
| `retro` | `retro` | 复盘与回顾 skill：把一次开发、排障、交付或协作过程整理成可执行的复盘结论，输出做得好的地方、问题与根因、改进动作和后续跟踪项。用户要求「复盘」「回顾这次开发」「总结问题和经验」postmortem、retrospective 等场景，或任务完成后沉淀流程改进、防止同类问题复发时使用。 |
| `robot-aiot-adr-confluence` | `robot-aiot-adr-confluence` | 技术方案文档端到端工作流：信息评估 → 需求收敛、追问澄清、方案比较 → 生成 ADR、技术提案或决策简报，需要时发布到 Confluence。适用于「写技术方案」「生成 ADR」「架构决策记录发 Confluence」「技术选型文档输出」等场景。只要文档可停在 Markdown 草稿，明确要求发布才进 Confluence 阶段。 |
| `robot-aiot-adr-generator` | `robot-aiot-adr-generator` | 生成并校验 ADR 架构决策记录：先按业务/技术需求产出标准 ADR 文档，再按需对可外部验证的关键技术断言执行验证链核查。适用于"生成 ADR""写架构决策记录""输出技术选型归档""ADR 发布前审稿"等场景，输出服务技术决策归档而非通用技术文章。 |
| `robot-aiot-arch-diagram` | `robot-aiot-arch-diagram` | 架构图/技术可视化绘制能力。两条输出路径：直绘 SVG/HTML（主路径，编辑级设计系统+工程制图管线，含几何校验与构图契约）、archify 运行时渲染（主题切换+导出）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑等 40+ 图表类型；内置 12 套 SVG 风格皮肤与品牌 token 定制、PNG/GIF 导出，支持 drawio/Mermaid/Excalidraw 导入重绘与 .excalidraw/SVG/PNG 三件套离线导出，含数据统计图表绘制规则、深色主题直绘与出版级迭代流程。非 PPT 场景专用。触发：绘制架构图/技术可视化。 |
| `robot-aiot-bash-code-review` | `robot-aiot-bash-code-review` | 审查 skill 文档（.md）中 bash 代码块的语法、功能正确性与模式匹配准确性。创建或更新含 bash 代码块的 skill、要求验证文档 bash 代码、编辑涉及 bash 块的 skill 文档后触发。触发词：review bash、verify code blocks、bash 验证、代码块审查。 |
| `robot-aiot-commit` | `robot-aiot-commit` | 为本项目生成统一格式的中文提交说明，用户明确要求时执行 Git commit。适用于「生成 commit message」「按规范提交」「总结 diff」「按 FEAT/FIX/ENH/DOC/CHORE 分类提交」「根据分支提取 JIRA」等场景，遵循本项目提交规范而非通用 Conventional Commits 模板。 |
| `robot-aiot-docs-sync` | `robot-aiot-docs-sync` | 扫描项目并创建或更新可溯源文档：AGENTS.md、README.md、CHANGELOG.md、docs/project-map.md、docs/architecture.md。适用于「更新项目文档」「同步文档」「生成 changelog」「生成项目地图」等场景，仅对这 5 个文件做结构化增强，不修改源代码、配置或测试。 |
| `robot-aiot-draw-flowchart` | `robot-aiot-draw-flowchart` | 机器人/IoT 业务图表绘制与页面化能力：draw.io XML 图表生成（可编辑主路径）+ XML→HTML 稳定桥接转换 + 领导汇报静态页面 HTML（1920x1080 画布）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑等 39+ 图表类型；内置机器人视觉语言、配色与样式一致性体系、几何/构图校验，PNG/GIF 导出与 drawio/Mermaid 导入重绘，支持 Mermaid 源码写作与 .excalidraw/SVG/PNG 三件套离线导出、数据统计图表绘制、深色主题直绘与出版级迭代流程。 |
| `robot-aiot-interactive-html-author` | `robot-aiot-interactive-html-author` | 交互式动画特效 HTML 编写能力。纯原生零依赖产出浏览器可直接运行的交互页面/多页 deck：翻页系统（键盘+点击+触摸滑动+View Transition+#/N 深链）、演讲者模式（S 键弹窗：像素级预览+提词+计时器，双窗口同步）、总览网格（O 键）、话术抽屉（N 键）、元素入场、数据动效（数字滚动/进度条填充/图表逐步绘制）、交互图表、关键帧动画与动效接缝、扩展特效目录（27 种 CSS 入场动画 + 20 种 canvas FX，仅明确要求时启用）、Mermaid/PlantUML 构建期渲染嵌入（headless Chrome→PNG/SVG，失败降级不静默丢图）、自包含单文件构建与交付前审查。用户要求写交互动画页、加翻页/动画/动效、演讲者模式/提词器/双屏演示，或 robot-aiot-web-presentation-workflow 委派 Phase 4 编写时触发。 |
| `robot-aiot-knowledge-expert` | `robot-aiot-knowledge-expert` | 物联网全栈技术专家回答规范。用户问 IoT/AIOT 架构设计、协议选型、平台集成、边云协同、性能调优、故障排查时使用。触发词：物联网、IoT、MQTT、Modbus、BACnet、OPC UA、EMQX、物模型、边云协同、设备影子、OTA、JetLinks、ThingsBoard、感认行。 |
| `robot-aiot-leadership-ppt-workflow` | `robot-aiot-leadership-ppt-workflow` | 把项目数据和技术分析转化为领导汇报 PPT，五阶段全链路：数据池建立 → 技术明细版加目标受众汇报版文档分层 → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML 并完成 XML→HTML 桥接 → 调用 ppt-master 生成最终 PPTX。用户要求「写领导汇报PPT」「出PPT母稿」「做汇报材料」时触发。受众由用户指定，默认领导层。 |
| `robot-aiot-self-skill-sync` | `robot-aiot-self-skill-sync` | 批量更新 self 目录下所有 git 项目并同步 skills 的五模块工作流：统一更新 npx 管理型外部 skill（失败按 self/skills/ 本地克隆 rsync 兜底）、OpenSpec profile 升级并将 opsx/ 命令与 openspec-* skills 同步到 ~/.agents、self-skills/ 与 ~/.agents/skills/ 及 commands/ 按内容+mtime 文件级双向同步（严禁旧覆盖新）、~/.agents/skills/ 全量同步到知识库 agent-skills/skills/（不加 --delete）、最后更新 docs/skills-overview.md。核心原则：只允许新增和修改，禁止删除与 git push；self-skills/ 是自写 skill 唯一真源，禁止从非运行时来源写入。触发词：更新self、同步skills、更新skills、拉取self 等。 |
| `robot-aiot-web-presentation-workflow` | `robot-aiot-web-presentation-workflow` | 交互式 Web 演示页面制作工作流：根据知识文档生成分页汇报母稿，按需制作架构图/流程图，逐页交互 HTML（可翻页、带动画、数据动效，纯原生零依赖双击即用）委派 robot-aiot-interactive-html-author 编写。触发于“做交互演示”“生成Web演示”“做动态汇报”“可翻页演示”“带动画的汇报”“Web版汇报”，或将技术项目数据转化为可交互浏览器演示的场景。 |
| `scaffold-exercises` | `scaffold-exercises` | 创建通过 lint 的练习目录结构，含 sections、problems、solutions、explainers。用于搭建练习脚手架、创建练习 stub 或新建课程章节。 |
| `security-audit` | `security-audit` | Java 安全检查清单，覆盖 OWASP Top 10、输入校验、注入防护与安全编码，适用于 Spring、Quarkus、Jakarta EE 及原生 Java。用于代码安全审查、发布前检查或用户询问漏洞时。 |
| `setup-matt-pocock-skills` | `setup-matt-pocock-skills` | 为仓库配置工程技能：设置 issue tracker、triage 标签词表与领域文档布局。首次使用其他工程技能前运行一次。 |
| `setup-pre-commit` | `setup-pre-commit` | 在当前仓库配置 Husky pre-commit 钩子，含 lint-staged（Prettier）、类型检查与测试。用户想添加 pre-commit 钩子、配置 Husky/lint-staged 或提交时格式化/类型检查/测试时使用。 |
| `setup-ts-deep-modules` | `setup-ts-deep-modules` | 把 dependency-cruiser 接入 TypeScript 仓库，使每个 package 成为深模块——实现隐藏在子文件夹中，只能通过入口文件访问。用户手动调用。 |
| `skill-creator` | `skill-creator` | 创建新 skill、修改改进现有 skill、测量 skill 性能。用于从零创建 skill、编辑或优化现有 skill、跑 evals 测试、带方差分析的基准测试、优化描述的触发准确性。 |
| `slack-gif-creator` | `slack-gif-creator` | 创建为 Slack 优化的动画 GIF 的知识与工具集，提供约束、验证工具和动画概念。用户要求做某个 Slack 动画 GIF 时使用。 |
| `slides` | `slides` | 用 Chart.js、design tokens、响应式布局、文案公式和场景化 slide 策略创建策略型 HTML 演示。 |
| `solid-principles` | `solid-principles` | SOLID 原则清单（附 Java 示例）。类职责过多、抽象泄漏、依赖方向错误，或用户问及单一职责、开闭、里氏替换、接口隔离、依赖倒置时使用；命名、重复与方法长度问题改用 clean-code。 |
| `spring-boot-patterns` | `spring-boot-patterns` | Spring Boot 最佳实践与模式。创建 controller/service/repository，或用户问及 Spring Boot 分层、装配、配置、异常处理时使用；JPA 与 Hibernate 行为改用 jpa-patterns。 |
| `tdd` | `tdd` | 测试驱动开发。用于测试先行构建功能或修复 bug、提及 red-green-refactor、或需要集成测试时。 |
| `teach` | `teach` | 在当前工作区内向用户教授新技能或概念。 |
| `test-quality` | `test-quality` | 用 JUnit 5 加 AssertJ 断言编写高质量 Java 测试。用户说 add tests、write tests、improve test coverage，或审查/创建 Java 测试类时使用。 |
| `theme-factory` | `theme-factory` | 为产物（slide、docs、报告、HTML landing page 等）套用主题的样式工具包。内置 10 套预设配色/字体主题，可直接应用到已创建的产物，也可即时生成新主题。 |
| `to-questionnaire` | `to-questionnaire` | 把你无法完全回答的决策转成问卷，交给他人填写。 |
| `to-spec` | `to-spec` | 把当前对话综合成 spec 并发布到项目 issue tracker，无需访谈，直接提炼已讨论内容。 |
| `to-tickets` | `to-tickets` | 把计划、规格或当前对话拆解为一组 tracer-bullet 工单，每张声明自己的阻塞依赖，发布到配置的 tracker（本地为每工单一文件的文本记录，或在真实 tracker 上用原生 blocking 链接）。 |
| `triage` | `triage` | 让 issue 和外部 PR 走分诊角色状态机：分类、验证、必要时追问，并写出 agent-ready 简报。 |
| `ui-styling` | `ui-styling` | 用 shadcn/ui 组件（基于 Radix UI + Tailwind）、Tailwind CSS 原子化样式与 canvas 视觉设计构建美观、可访问的界面。构建 UI、实现设计系统、响应式布局、无障碍组件（对话框、下拉、表单、表格）、主题配色定制、暗黑模式、生成视觉海报或建立跨应用统一样式规范时使用。 |
| `ui-ux-pro-max` | `ui-ux-pro-max` | Web/移动/桌面 UI/UX 设计智能。设计、构建、审查或修复界面（页面、组件、设计系统、无障碍、交互、响应式布局、字体、配色、图表及各技术栈 UI 实现）时使用。内置可检索本地数据：79 种风格（50 个启用）、192 套产品配色、74 组字体搭配、119 条 UX 准则、105 个图标、17 个 GSAP 预设、25 种图表、22 个技术栈。 |
| `vercel-optimize` | `vercel-optimize` | 对已部署项目做 Vercel 成本与性能优化，尤其 Next.js、SvelteKit、Nuxt 及有限支持的 Astro。先收集 metrics、用量、项目配置和代码扫描结果，只调查有指标支撑的候选项，基于已验证文件和版本感知的 Vercel/框架文档给出排序建议。用于降低 Vercel 账单、慢或贵的路由、缓存机会、Function Invocations、Build Minutes、Fast Data Transfer、Core Web Vitals、Bot Management、Fluid compute、成本分解等请求。 |
| `vercel-react-native-skills` | `vercel-react-native-skills` | React Native 与 Expo 最佳实践，构建高性能移动应用。构建 RN 组件、优化列表性能、实现动画或使用原生模块时使用；涉及 React Native、Expo、移动性能、原生平台 API 的任务均触发。 |
| `vercel-react-view-transitions` | `vercel-react-view-transitions` | 用 React View Transition API（<ViewTransition> 组件、addTransitionType、CSS view transition 伪元素）实现原生流畅动画。用于页面转场、路由切换动画、共享元素动画、组件进出动画、列表重排、方向性导航动画，或在 Next.js 中集成 view transitions；不依赖第三方动画库。用户提到 startViewTransition、ViewTransition 或 React UI 状态间动画时触发。 |
| `wait-what` | `wait-what` | 当上一条消息未有效传达到位时，停下来重新组织表达再讲一遍。 |
| `wayfinder` | `wayfinder` | 把超出单个 agent 会话容量的大型工作规划为 issue tracker 上的决策工单共享地图，逐个解决，直到通往目标的路径清晰。 |
| `web-artifacts-builder` | `web-artifacts-builder` | 用现代前端技术（React、Tailwind CSS、shadcn/ui）构建复杂多组件 claude.ai HTML artifacts 的工具集。适用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifact，不用于简单单文件 HTML/JSX。 |
| `web-design-guidelines` | `web-design-guidelines` | 按 Web Interface Guidelines 审查 UI 代码。用户要求 "review my UI""check accessibility""audit design""review UX" 或按最佳实践检查站点时使用。 |
| `webapp-testing` | `webapp-testing` | 基于 Playwright 的本地 Web 应用交互与测试工具集。用于验证前端功能、调试 UI 行为、截取浏览器截图、查看浏览器日志。 |
| `wizard` | `wizard` | 生成交互式 bash 向导，引导人工完成只有人才能做的步骤。适用于基础设施开通、凭据或 CI secrets 配置、操作陌生的第三方控制台、一次性迁移或切换。agent 自己能完成的步骤不要用它。 |
| `writing-beats` | `writing-beats` | 写作技法：将原始素材组织为由节拍（beats）推进的叙事旅程，确保每个术语在节拍依赖它之前先做铺垫解释。 |
| `writing-for-agents` | `writing-for-agents` | 为 agent 撰写文档。创建或编辑 skill、修改 AGENTS.md 或 CLAUDE.md 时使用。 |
| `writing-fragments` | `writing-fragments` | 写作探索阶段：挖掘原始写作片段，暂不做结构化。 |
| `writing-shape` | `writing-shape` | 写作成形阶段：逐段把原始素材塑造成文章。 |
| `xlsx` | `xlsx` | 表格文件为主输入或输出的任务都用它：打开/读取/编辑/修复 .xlsx、.xlsm、.xltx、.csv、.tsv（加列、公式、格式、图表、清洗脏数据）、从零创建表格、表格格式转换。用户按名字或路径提及表格文件时触发。交付物必须是表格文件；主交付物为 Word、HTML、独立脚本、数据库管道或 Google Sheets API 集成时不触发。 |
| `zh-code-reviewer` | `zh-code-reviewer` | 中文代码审查专家，生成详细的中文代码审查报告。 |

## 第二部分：`agent-skills/skills/`

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`（外部 skill 副本库）

共 **696** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `a-stock-data` | `a-stock-data` | 需要写代码实际获取 A 股真实数据时使用——行情/K线(mootdx+腾讯+百度)、研报(东财+同花顺+iwencai)、信号(热点/北向/龙虎榜/解禁)、资金面(融资融券/大宗/分红/资金流)、新闻、财务三表/F10、公告(巨潮)、打板(涨停池/连板/炸板率)、ETF期权(T型报价/希腊字母/IV)、舆情互动(互动易/热榜)、筹码分布、复权因子、估值历史(PE/PB/PS)、申万行业变迁、宏观(社融/PMI)。十一层数据源·54 端点，内嵌全部可运行代码，零外部文件依赖；优先通达信(mootdx)/腾讯(不封IP)，东财已内置限流防封，主源被封可查「备用源速查」降级。仅在需调用接口取数时加载；概念解释、观点讨论、策略问答等无需取数的话题不要加载。 |
| `academy-guide` | `academy-guide` | 回答 Claude 产品使用类问题前必查：从 Claude Academy（academy.claude.com）推荐匹配的课程、教程与用例。触发于“how do I”“getting started”“what can Claude do”“teach me”等学习类提问、artifacts/skills/MCP 相关问题、团队培训或入门材料请求。与文档回答配合使用；仅强匹配时推荐，不杜撰课程内容。 |
| `accessibility` | `accessibility` | 按 WCAG 2.2 Level AA 设计、实现并审计无障碍产品：覆盖键盘操作、对比度、屏幕阅读器支持，为 Web 生成语义化 ARIA，为 Web/iOS/Android 生成无障碍特性。构建或审查需达标的 UI 时使用。 |
| `adaptyv` | `adaptyv` | 使用 Adaptyv Bio Foundry API 与 Python SDK 进行蛋白实验设计、提交与结果获取。触发：提到 Adaptyv、Foundry API、蛋白结合/筛选实验、BLI/SPR、热稳定性实验，或代码导入 adaptyv、adaptyv_sdk、FoundryClient，引用 foundry-api-public.adaptyvbio.com。 |
| `aeon` | `aeon` | 时间序列机器学习 skill，覆盖分类、回归、聚类、预测、异常检测、分割与相似性搜索。当数据为时间索引观测或顺序模式、需要超出常规 ML 的专门算法时使用；支持单变量与多变量分析，API 与 scikit-learn 兼容。 |
| `agent-reach` | `agent-reach` | 互联网调研统一入口：用户要求搜索/调研/查资料（全网调研 X、查一下、看看大家怎么评价），或提及平台、分享 URL 时必须使用。覆盖小红书、Twitter/X、B站、Reddit、V2EX、LinkedIn、YouTube、GitHub、小宇宙、雪球、RSS 等 15 个平台，多后端路由（OpenCLI/平台 CLI/API），用 `agent-reach doctor --json` 查看各平台后端状态。不负责写报告、翻译等内容加工，也不做发帖评论等写操作。 |
| `agent-tui` | `agent-tui` | 主 agent 不要直接使用本 skill，需测试 TUI 时调用 `tui_tester` subagent。以编程方式驱动终端 UI（TUI）应用，用于测试、自动化与检查。适用于 CLI/TUI 交互自动化、终端应用回归测试或验证交互行为；也用于回答"什么是 agent-tui""agent-tui 怎么工作""演示 agent-tui"等请求。 |
| `ai-video-script` | `ai-video-script` | AI 视频脚本生成器。根据输入主题/关键词生成完整视频脚本，含分镜描述、画面提示词与配音文案。适用于短视频创作者、AI 视频制作者与内容营销人员。触发词：视频脚本、分镜、AI 视频、短视频文案、视频策划。 |
| `algorithmic-art` | `algorithmic-art` | 用 p5.js 结合种子随机与交互参数探索创作算法艺术。用户要求代码艺术、生成艺术、流场、粒子系统时使用。须创作原创作品，不得复制现有艺术家以防侵权。 |
| `analytical-method-validation` | `analytical-method-validation` | 按 ICH Q2(R2)/Q14、USP <1220>/<1225>/<1226>、ICH M10、CLSI EP、ISO/IEC 17025 等框架规划、执行并记录分析方法的验证、确认与转移，适用于 HPLC、LC-MS/MS、GC、CE、ICP-MS、溶出、qNMR、qPCR、NIR 及配体结合/细胞 assay。触发：method validation、AMV、linearity、accuracy and precision、LOD/LOQ、specificity、robustness、method transfer、Bland-Altman、OOS investigation、ISR 等。 |
| `anndata` | `anndata` | 单细胞分析中带注释矩阵的数据结构。处理 .h5ad 文件或对接 scverse 生态时使用。这是数据格式 skill——分析工作流用 scanpy，概率模型用 scvi-tools，群体规模查询用 cellxgene-census。 |
| `api-contract-review` | `api-contract-review` | 审查 REST API 契约：HTTP 语义、版本管理、向后兼容与响应一致性。用户说 "review API""check endpoints""REST review"，或发布 API 变更前使用。 |
| `api-design` | `api-design` | 生产级 REST API 设计模式：资源命名、状态码、分页、过滤、错误响应、版本控制与限流。设计或评审 REST endpoint、资源命名、状态码、分页或版本控制时使用。 |
| `api-sculptor` | `api-sculptor` | 设计并实现 API：REST、GraphQL、gRPC 与 WebSocket，产出 OpenAPI 3.1 规范、GraphQL SDL schema、Protocol Buffer 定义及可运行的服务端实现。触发：API 设计、endpoint 结构、schema 定义、版本策略、分页、认证、限流，或 "design an API for"、"write an OpenAPI spec"、"create a GraphQL schema"、"set up gRPC" 及 "I need endpoints for my app" 等口语化请求。 |
| `api-tester` | `api-tester` | 依据真实 OpenAPI、路由实现与现有测试生成并验证 API 测试。用于测试接口、补集成测试、验证 API 契约、生成回归用例或排查接口兼容性；区分“生成测试”与“执行请求”的授权，不猜测状态码、响应结构或 SLA，不在未确认环境发送写请求。 |
| `apple-hig-designer` | `Apple-Hig-Designer` | 按 Human Interface Guidelines 设计 Apple 风格 iOS/macOS 界面。创建符合 HIG 的组件，使用 SF Symbols、San Francisco 字体与完善可访问性，支持可选现代特效。设计 Apple 风格 UI、iOS/macOS 界面、HIG 合规组件或落地设计系统规范时使用。 |
| `arbor` | `arbor` | 用 Arbor 论文的 Hypothesis Tree Refinement（HTR）方法，针对目标与评估器自主改进真实工件（代码、训练配方、agent harness、数据管道、prompt）。适用于多轮实验迭代优化且要防过拟合的场景，如 "get my model's eval score up"、"improve this agent/harness"、"beat the baseline on this benchmark"、MLE-bench / Kaggle 式优化，或任何长期“让工件更好且不是背 dev set”的任务。用户未提 "Arbor" 但描述了反复实验-评估循环、竞争思路分支探索或担心 dev/test 差距时也触发。由 Claude 本体作协调者、subagent 执行器跑在隔离 git worktree；独立 arbor CLI 工具见 references/arbor-upstream.md。 |
| `arboreto` | `arboreto` | 用可扩展算法（GRNBoost2、GENIE3）从基因表达数据推断基因调控网络（GRN）。触发：分析转录组数据（bulk RNA-seq、single-cell RNA-seq）以识别转录因子-靶基因关系与调控相互作用；支持大规模数据分布式计算。 |
| `archify` | `archify` | 生成经过校验的架构图、工作流图、时序图、数据流图、生命周期/状态机图，输出可交互独立 HTML（内联 SVG、深/浅主题、可选轨迹动画，支持 PNG/JPEG/WebP/SVG/WebM 导出）。接受自然语言需求或 Mermaid 输入，可检查代码仓库证据。用于系统架构、云/安全/网络拓扑、API 调用时序、数据管道、ETL/ELT、数据血缘等可视化，以及 Mermaid 转换美化。 |
| `architecture-decision-records` | `architecture-decision-records` | 把 Claude Code 会话中的架构决策捕获为结构化 ADR。自动检测决策时刻，记录背景、备选方案与理由，维护 ADR 日志，让后续开发者理解代码库为何如此成形。 |
| `architecture-review` | `architecture-review` | 宏观分析 Java 项目架构：包结构、模块边界、依赖方向与分层。触发于“review architecture”“check structure”“package organization”等，或评估代码库是否符合整洁架构原则。 |
| `article-writing` | `article-writing` | 以从给定示例或品牌指引提炼的独特声线撰写文章、指南、博客、教程、newsletter 等长文。需要超过一段篇幅的成稿内容，且重视声线一致性、结构与可信度时使用。 |
| `ask-matt` | `ask-matt` | 技能路由器：当你不确定该用哪个 skill 或流程时，询问当前处境并推荐仓库中最合适的技能。 |
| `ask-matt` | `engineering/ask-matt` | 技能路由器：当你不确定该用哪个 skill 或流程时，询问当前处境并推荐仓库中最合适的技能。 |
| `astropy` | `astropy` | 天文与天体物理工作流的核心 Python 库，覆盖单位/量纲（units/quantities）、坐标、FITS I/O、表格、时间系统、WCS 与宇宙学。用 Astropy 实现或调试天文数据分析代码时使用。 |
| `async-pr-review` | `async-pr-review` | 需要启动异步 PR review、对 PR 运行后台检查，或查询先前启动的异步 PR review 状态时使用。 |
| `auth-architect` | `auth-architect` | 设计并实现认证与身份系统。覆盖 OAuth2/OIDC 流程（authorization code、PKCE、client credentials）、JWT 设计（RS256 vs HS256、密钥轮换、token 黑名单、refresh token 策略）、RBAC/ABAC 建模、Google/GitHub/SAML 2.0 SSO、会话管理、magic link、MFA（TOTP/SMS/硬件密钥）与 API key 管理。用户说 "implement OAuth2"、"JWT refresh token rotation"、"set up SSO with Google"、"design RBAC"、"add login to my app" 等时触发。 |
| `autoplan` | `gstack-autoplan` | 自动评审流水线：从磁盘读取全部 CEO、设计、工程和 DX review 技能，按 6 条决策原则顺序执行并自动决策，仅在最终审批门呈现口味类决策（近似方案、边界范围、codex 分歧）。一条命令产出完整评审计划；用户有计划文件想免答 15-30 个中间问题时使用，触发 auto review、autoplan 等。 |
| `autoskill` | `autoskill` | 通过 screenpipe 观察用户屏幕，检测重复的研究工作流并与现有 scientific-agent-skills 匹配，为未覆盖的模式起草新技能或组合配方。需本地 3030 端口运行 screenpipe 守护进程，否则拒绝执行；检测全部本地运行，仅脱敏聚类摘要送 LLM。 |
| `backtest-expert` | `backtest-expert` | 量化交易策略系统化回测的专家指导。开发、测试、压力测试或验证策略时使用，覆盖"打死想法"方法论、参数稳健性测试、滑点建模、偏差防范与回测结果解读。触发：回测、策略验证、稳健性测试、避免过拟合、系统化交易开发。 |
| `banner-design` | `banner-design` | 为社交媒体、广告、网站 hero、创意素材和印刷品设计 banner，提供多个艺术方向选项与 AI 生成视觉。覆盖 Facebook、Twitter/X、LinkedIn、YouTube、Instagram、Google Display 等平台，支持极简、渐变、粗体字、3D、霓虹、双色调、玻璃拟态等多种风格。触发 design/generate banner、"图片卡片" 等需求。 |
| `baoyu-article-illustrator` | `baoyu-article-illustrator` | 分析文章结构、找出需配图的位置，用 Type × Style × Palette 三维度生成插图。用户说 "illustrate article"、"add images"、"为文章配图" 时使用。 |
| `baoyu-comic` | `baoyu-comic` | 知识漫画创作器，支持多种画风与基调，生成含精细分镜的原创教育漫画，支持批量生图。用户要求"知识漫画"、"教育漫画"、biography comic、tutorial comic 或 Logicomix 风格漫画时触发。 |
| `baoyu-compress-image` | `baoyu-compress-image` | 将图片压缩为 WebP（默认）或 PNG，自动选择工具。用户要求"压缩图片""优化图片""转 webp"或减小图片文件体积时使用。 |
| `baoyu-cover-image` | `baoyu-cover-image` | 生成文章封面图：5 个维度（类型、配色、渲染、文字、情绪）组合 11 套配色与 7 种渲染风格，支持 2.35:1 电影、16:9 宽屏、1:1 方形比例。触发："generate cover image"、"make cover" 等。 |
| `baoyu-danger-gemini-web` | `baoyu-danger-gemini-web` | 通过逆向工程的 Gemini Web API 生成图像与文本：文本生成、按提示词生图、参考图视觉输入和多轮对话。供其他技能作图像生成后端，或用户要求 generate image with Gemini、Gemini text generation 时使用。 |
| `baoyu-danger-x-to-markdown` | `baoyu-danger-x-to-markdown` | 将 X（Twitter）推文与文章转换为带 YAML front matter 的 markdown。使用逆向工程 API，需用户同意。用户说"X to markdown""tweet to markdown""保存推文"或提供 x.com/twitter.com 链接时触发。 |
| `baoyu-diagram` | `baoyu-diagram` | 创建专业深色主题 SVG 图表：架构图、流程图、时序图、结构图、思维导图、时间线、概念图等。用户要求任何技术/概念图表、系统或流程可视化、"画个图"、"画一个架构图"、"diagram"、"flowchart" 等时触发。输出为独立 .svg 文件。 |
| `baoyu-electron-extract` | `baoyu-electron-extract` | 从已安装的 Electron 应用（.asar 包）提取资源与 JavaScript：有 .js.map 时还原原始源码，否则用 Prettier 格式化压缩代码。触发："extract Electron app"、"decompile Electron"、"看 Electron 应用源码"、"提取 .asar" 等。跳过 node_modules，支持 macOS 与 Windows。 |
| `baoyu-format-markdown` | `baoyu-format-markdown` | 为纯文本或 markdown 文件排版：frontmatter、标题、摘要、各级标题、加粗、列表与代码块。用户要求"format markdown""美化文章"或改善排版时使用，输出到 {filename}-formatted.md。 |
| `baoyu-image-gen` | `baoyu-image-gen` | AI 图像生成，聚合 OpenAI GPT Image 2.5、Azure OpenAI、Google、OpenRouter、DashScope、Z.AI GLM-Image、MiniMax、Jimeng、Seedream、Replicate、Agnes 等 API。支持文生图、参考图、宽高比与基于已存 prompt 文件的批量生成；默认顺序执行，已有多个 prompt 或需要稳定多图吞吐时用批量并行。用户要求生成、创建或绘制图像时使用。 |
| `baoyu-infographic` | `baoyu-infographic` | 生成专业信息图：21 种布局类型 × 22 种视觉风格。分析内容、推荐 layout×style 组合，产出可出版级信息图。触发：用户要求 "infographic"、"信息图"、"visual summary"、"可视化"、"高密度信息大图"。 |
| `baoyu-markdown-to-html` | `baoyu-markdown-to-html` | 将 Markdown 转为带样式 HTML，提供微信兼容主题。支持代码高亮、数学公式、Mermaid（经 headless Chrome 渲染为 PNG）、PlantUML、脚注、告警、信息图，外链可选转底部引用。用户说 "markdown to html"、"md 转 html"、"微信外链转底部引用" 或需要带样式 HTML 输出时使用。 |
| `baoyu-post-to-wechat` | `baoyu-post-to-wechat` | 通过 API 或 Chrome CDP 向微信公众号发布内容：支持文章（HTML/markdown/纯文本）与多图贴图（原图文）；markdown 文章默认把外链转为文末引用以适配公众号。用户提到「发布公众号」「post to wechat」「微信公众号」「贴图/图文/文章」时使用。 |
| `baoyu-post-to-weibo` | `baoyu-post-to-weibo` | 通过 Chrome CDP 发布内容到微博（Weibo），支持含文字、图片、视频的普通博文，以及 Markdown 输入的头条文章。触发："post to Weibo"、"发微博"、"发布微博"、"publish to Weibo"、"share on Weibo"、"写微博"、"微博头条文章"。 |
| `baoyu-post-to-x` | `baoyu-post-to-x` | 将内容与文章发布到 X (Twitter)，支持带图片/视频的普通推文及 X Articles 长文（Markdown）。用户要求 post to X、tweet、publish to Twitter 或 share on X 时触发。Codex 中用户显式要求 Chrome 插件/@chrome 时走 Chrome Extension 工作流，否则优先 Chrome Computer Use，仅在允许时回退真实 Chrome CDP 脚本。 |
| `baoyu-slide-deck` | `baoyu-slide-deck` | 从内容生成专业 slide deck 图片：先创建带样式说明的大纲，再逐页生成幻灯片图片。用户要求 "create slides"、"make a presentation"、"generate deck"、"slide deck" 或 "PPT" 时使用。 |
| `baoyu-translate` | `baoyu-translate` | 翻译 skill：用户要求 translate、翻译、精翻、快翻、改成中文/英文、convert to Chinese、localize（本地化）、校对译文，或提供带翻译意图的 URL/文件时使用。支持 quick/normal/refined 三种模式与自定义术语表。 |
| `baoyu-url-to-markdown` | `baoyu-url-to-markdown` | 通过 baoyu-fetch CLI（基于 Chrome CDP 与站点专用适配器）抓取任意 URL 并转为 markdown。内置 X/Twitter、YouTube 字幕、Hacker News 讨论串及基于 Defuddle 的通用页面适配器，以交互等待模式处理登录/验证码。当用户想将网页保存为 markdown 时使用。 |
| `baoyu-wechat-summary` | `baoyu-wechat-summary` | 用本地 wx-cli 二进制总结微信群聊精华：默认普通摘要，可选毒舌版。跨次维护 per-group 历史（history.json + history-digests.jsonl）、per-user 画像与群事实记忆（memory.md），内置隐私护栏。触发："总结群聊"、"群聊精华"、"summarize group chat"、群名+时间范围、"回溯画像"/"backfill profiles"；"毒舌版" 加 roast 模式。 |
| `baoyu-xhs-images` | `baoyu-xhs-images` | 生成信息图图片卡片系列：12 种视觉风格、8 种版式、3 种配色，把内容拆为 1-10 张卡通风格图片卡，为社交媒体传播优化。触发"小红书图片"、"小红书种草"、"小绿书"、"微信图文"、"image cards" 或用户需要社交媒体信息图系列。 |
| `baoyu-youtube-transcript` | `baoyu-youtube-transcript` | 按 URL 或视频 ID 下载 YouTube 字幕/转录文本与封面图。支持多语言、翻译、章节与说话人识别，缓存原始数据以便快速重新格式化。用户要 "get YouTube transcript"、"download subtitles"、"YouTube字幕"、"YouTube封面"、video thumbnail/cover image，或提供 YouTube URL 想提取转录文本或封面时使用。 |
| `behavioral-evals` | `behavioral-evals` | 创建、运行、修复与晋升行为评测（behavioral evals）的指导。用于验证 agent 决策逻辑、调试失败与 prompt 引导问题，或为 workspace 添加回归测试。 |
| `benchling-integration` | `benchling-integration` | Benchling Python SDK 与 REST API 集成，覆盖 registry 实体、库存、ELN 条目、workflow、Benchling Apps 与 Data Warehouse 查询。用 benchling-sdk 或 v2 API 自动化实验数据时使用。 |
| `benchmark` | `gstack-benchmark` | 基于 browse daemon 的性能回归检测：为页面加载时间、Core Web Vitals 与资源大小建立基线，每个 PR 前后对比，跟踪长期性能趋势。触发词："performance"、"benchmark"、"page speed"、"lighthouse"、"web vitals"、"bundle size" 等。 |
| `benchmark-models` | `gstack-benchmark-models` | gstack skills 跨模型基准测试：同一 prompt 并行跑 Claude、GPT（via Codex CLI）、Gemini，比较延迟、token、成本及可选 LLM judge 质量评分，用数据回答"哪个模型最好"。触发词："benchmark models""compare models""model shootout"。与测网页性能的 /benchmark 是两回事。 |
| `bgpt-paper-search` | `bgpt-paper-search` | 通过 BGPT MCP server 检索科学论文，并获取从全文提取的结构化实验数据，每篇返回 25+ 字段，含方法、结果、样本量、质量评分与结论。用于文献综述、证据综合及获取摘要中查不到的实验细节。 |
| `bids` | `bids` | 处理 Brain Imaging Data Structure (BIDS) 数据集时使用：组织神经科学与生物医学数据（MRI、EEG、MEG、iEEG、PET、显微镜、NIRS、动作捕捉、EMG、MR 波谱、行为数据）、查询 BIDS layout、校验合规性、DICOM 转 BIDS、编写 metadata sidecar、创建 BIDS derivatives。 |
| `biopython` | `biopython` | 分子生物学综合工具库，用于序列操作、FASTA/GenBank/PDB 文件解析、系统发育分析，以及通过 Bio.Entrez 编程访问 NCBI/PubMed。最适合批处理、自定义生信流水线、BLAST 自动化。快速查询用 gget，多服务集成用 bioservices。 |
| `bioservices` | `bioservices` | 统一 Python 接口访问 40+ 生信数据库服务，适合单工作流中跨库查询（UniProt、KEGG、ChEMBL、Reactome）与跨服务 ID 映射；单库快查用 gget，序列/文件处理用 biopython。 |
| `brainstorming` | `brainstorming` | 任何创造性工作前必须使用——创建功能、构建组件、添加功能或修改行为时，在实现之前先探索用户意图、需求和设计。 |
| `brand` | `brand` | 品牌语调、视觉识别、信息框架、资产管理与品牌一致性。涉及品牌内容、语气设定、营销资产、品牌合规、风格指南时启用。 |
| `brand-guidelines` | `brand-guidelines` | 将 Anthropic 官方品牌配色与字体应用于各类产出物。用于需要 Anthropic 视觉风格、品牌规范、视觉格式或公司设计标准的场景。 |
| `brandkit` | `brandkit` | 高端品牌视觉图像生成，用于制作品牌规范板、logo 系统、品牌识别演示与视觉世界展示。擅长极简、电影感、编辑风、暗黑科技、奢华、文化、安全、游戏、开发者工具与消费级应用等品牌体系，注重 logo 概念构思、克制排版、强象征意义、高级 mockup 与灵活网格布局。 |
| `breadth-chart-analyst` | `breadth-chart-analyst` | 分析市场广度图表，特别是基于 200 日均线的 S&P 500 Breadth Index 与美股上升趋势股票比例图。用户提供广度图请求分析、要求广度评估与仓位策略建议，或想基于广度指标理解中长期战略与短期战术展望时使用；也可不带图片直接从公开源抓 CSV。输出全英文。 |
| `breakout-trade-planner` | `breakout-trade-planner` | 从 VCP 筛选器输出生成 Minervini 风格突破交易计划：最坏情况风险计算、组合热度管理、Alpaca 兼容订单模板（确认前用 stop-limit bracket 预挂，确认后用 limit bracket）。用户提供 VCP 筛选结果并需要入场/止损/目标位与仓位规模时使用。 |
| `browse` | `gstack-browse` | 无头浏览器 QA 测试与网站自用测试工具：导航任意 URL、交互元素、验证页面状态、对比操作前后差异、带标注截图、检查响应式布局、测试表单与上传、处理对话框、断言元素状态，约 100ms/命令。用于测试功能、验证部署、dogfood 用户流程或带证据提交 bug；触发于“open in browser”“test the site”“take a screenshot”“dogfood this”。 |
| `browser-qa` | `browser-qa` | 功能部署后用浏览器自动化执行视觉测试与 UI 交互验证。 |
| `bulk-rnaseq` | `bulk-rnaseq` | 端到端 bulk RNA-seq 编排：原始 FASTQ 经 QC 与剪切（FastQC、fastp/Trim Galore）、比对与定量（STAR、Salmon、featureCounts）生成基因级 counts 矩阵，再接差异表达（pydeseq2）、通路/GSEA 富集与出版级图表。在 nf-core/rnaseq（Nextflow）与独立 STAR/Salmon 两条路径间路由，覆盖实验设计与 QC 门槛；单细胞 RNA-seq 改用 scanpy。 |
| `bun-runtime` | `bun-runtime` | Bun 作为 runtime、包管理器、bundler 与 test runner。何时选 Bun 而非 Node、迁移要点与 Vercel 支持。 |
| `canary` | `gstack-canary` | 部署后金丝雀监控。通过 browse daemon 监控线上应用的 console 报错、性能回退与页面故障，周期性截图并与部署前基线对比，发现异常即告警。触发语："monitor deploy""canary""post-deploy check""watch production""verify deploy"。 |
| `canslim-screener` | `canslim-screener` | 用 William O'Neil 的 CANSLIM 成长股方法筛选美股。用户要求 CANSLIM 选股、成长股分析、动量股识别，或按 O'Neil 投资体系寻找盈利与股价动能强劲的股票时触发。 |
| `canvas-design` | `canvas-design` | 用设计哲学在 .png 和 .pdf 文档中创作视觉艺术。用户要求海报、艺术品、设计或其他静态作品时使用。须原创设计，不得复制现有艺术家以防侵权。 |
| `captions-overlay` | `captions-overlay` | embedded-captions 工作流的字幕叠加学说：字幕模型（drop / rail / embed）及"字幕是叠加在影片之上的 OVERLAY，绝不预留底部避让带"的规则。在给 talking-head 或发布视频加字幕、决定某句丢弃/走逐字 rail/升格为稀缺 embed 高潮、布局将承载字幕的 composition（不要预留 keep-out band）或按真实画面中心构图时加载。引用 embedded-captions 的 rail+embed 模型，叠加于其上适用。 |
| `careful` | `gstack-careful` | 破坏性命令安全护栏：在 rm -rf、DROP TABLE、force-push、git reset --hard、kubectl delete 等操作前发出警告，用户可逐条覆盖。接触生产环境、调试在线系统或共享环境时使用；用户说 be careful、safety mode、prod mode 时启用。 |
| `cavecrew` | `cavecrew` | 向 caveman 风格 subagent 分派的决策指南：何时派 cavecrew-investigator（定位代码）、cavecrew-builder（1-2 文件编辑）、cavecrew-reviewer（diff 审查），而非内联处理或用普通 Explore。subagent 输出经 caveman 压缩，回注主上下文约缩小 60%，延长长会话上下文寿命。触发："delegate to subagent"、"use cavecrew"、"save context" 等。 |
| `caveman` | `caveman` | 超压缩沟通模式：以原始人式表达削减 65% 输出 token（实测）且保持技术准确。支持 lite/full/ultra 三档强度及 wenyan 变体。用户说 caveman mode、be brief、要求省 token 或调用 /caveman 时触发。 |
| `caveman-commit` | `caveman-commit` | 超压缩 commit message 生成器：保留意图与理由、削减噪音，遵循 Conventional Commits，主题不超过 50 字符，仅在 why 不明显时写 body。用户要求写 commit 或暂存变更时自动触发。 |
| `caveman-compress` | `caveman-compress` | 将自然语言记忆文件（CLAUDE.md、todos、preferences）压缩为 caveman 格式以节省输入 token，保留技术实质、代码、URL 与结构；压缩版覆写原文件，另存 FILE.original.md 备份。触发：/caveman-compress FILEPATH 或 "compress memory file"。 |
| `caveman-discover` | `caveman-discover` | 找出当前仓库中所有 LLM 工作流并打标签，使 Caveman Cloud 按代码实际用途（如 support-reply、nightly-digest）归集花费，而非混入匿名桶。触发：用户粘贴 Caveman discovery prompt、说 "discover workflows" 或要求按工作流拆分 LLM 花费。前提是仓库已接入 Caveman gateway（caveman-setup skill 负责该步）。 |
| `caveman-evidence-review` | `caveman-evidence-review` | 只读审查 Caveman Cloud 证据：成本、Cave Score、Cave Plan、workflow、trace、延迟、错误、压缩、路由与已验证节省。用户问 Caveman 发现了什么、LLM 花费去向、成本或质量为何变化、哪些 workflow 需关注，或要求 trace/分析审查时使用。优先用 Caveman MCP 工具，回退 CLI JSON。 |
| `caveman-explore` | `caveman-explore` | 只读仓库探索器。冷启动探索、跨文件大范围定位或直接搜索失败时主动使用；问题已指明具体文件或符号、或上轮已有可用 file:line 证据时跳过。只返回紧凑的 path:line 引用，读取与 grep 结果不进入主对话。 |
| `caveman-help` | `caveman-help` | 所有 caveman 模式、skill 与命令的快速参考卡。一次性显示，非持久模式。触发：/caveman-help、"caveman help"、"what caveman commands"、"how do I use caveman"。 |
| `caveman-learn` | `caveman-learn` | 收尾 Caveman learn 报告：审查排名靠前的 token 消耗点并应用降本修复（精简配置、把重复上下文卸载到 cavemem），每次修改需用户确认。用户运行 "caveman learn"、想降低 agent token 成本、精简重型 CLAUDE.md 或把每次会话重复粘贴的上下文迁入 cavemem 时使用。 |
| `caveman-manage` | `caveman-manage` | 审查 Caveman Cloud 的 eval 门控实验生命周期并阻止不安全执行。用于启动、批准、取消、晋升、回滚实验，或询问实验证据支持何种动作。先读证据；在服务端权威状态转移与证据门控就绪前不执行生命周期变更。 |
| `caveman-optimize` | `caveman-optimize` | 把 Caveman 纯报告式的仓库观察结果转为操作者选定的优化候选，并做基线/候选配对评估。触发：查看某条优化观察、评估候选变更、对当前 Caveman 优化报告采取行动。需已登录 Caveman CLI 连接与明确批准，绝不从 profile 推断资金或执行动作。 |
| `caveman-review` | `caveman-review` | 超压缩代码评审评论：在保留可行动信号的同时砍掉 PR 反馈噪音。每条一行：位置、问题、修复。触发：用户说 "review this PR"、"code review"、"review the diff"、"/review" 或调用 /caveman-review；评审 pull request 时自动触发。 |
| `caveman-setup` | `caveman-setup` | 把当前仓库接入 Caveman Cloud 网关，以零行为改变度量每次 LLM 请求的成本、token 与延迟。用户粘贴 Caveman 配置提示、说 set up caveman，或想给应用加 LLM 花费可观测性时使用；需网关 URL 和 Cave API key（配置提示自带）。 |
| `caveman-stats` | `caveman-stats` | 显示当前会话的真实 token 用量与预估节省。直接读取 Claude Code 会话日志，无 AI 估算。触发 /caveman-stats。输出由 mode-tracker hook 注入，模型本身不计算数字。 |
| `cellxgene-census` | `cellxgene-census` | 以编程方式查询 CZ CELLxGENE Census 的版本化公共单细胞与空间转录组数据。用于获取群体规模细胞元数据、基因表达切片、Census 汇总计数、源 H5AD URI/下载、embeddings、空间数据，以及跨物种/组织/疾病/assay/细胞类型的参考图谱比较。分析本地单细胞数据请改用 scanpy、anndata 或 scvi-tools。 |
| `changelog-gen` | `changelog-gen` | 从 Git 历史自动生成 CHANGELOG 的生成器。 |
| `changelog-generator` | `changelog-generator` | 从 git commits 生成 changelog。用户说 generate changelog、update changelog、what changed since last release，或准备新版本发布前使用。 |
| `changelog-video` | `changelog-video` | 把每周 changelog .md 变成成品品牌更新视频（方形 1080、约 45-60 秒、Annie 配音、动画品牌背景、mock-UI 可视化、低调字幕）。触发：用户提供 changelog/摘要 markdown 并要每周视频，或说 "changelog video"。自包含——字体、背景、词库与脚本都在 skill 内。 |
| `chinese-code-review` | `chinese-code-review` | 中文 code review 沟通参考：话术模板、分级标注（必须修复/建议修改/仅供参考）与国内团队常见反模式的应对。仅在用户显式输入 /chinese-code-review 时调用，不要根据上下文自动触发。 |
| `chinese-commit-conventions` | `chinese-commit-conventions` | 中文 commit 与 changelog 配置参考：Conventional Commits 中文适配、commitlint/husky/commitizen 中文模板、conventional-changelog 中文配置。仅在用户显式输入 /chinese-commit-conventions 时调用，不随上下文自动触发。 |
| `chinese-documentation` | `chinese-documentation` | 中文文档排版参考：中英文空格、全半角标点、术语保留、链接格式等，遵循中文文案排版指北约定。仅在用户显式 /chinese-documentation 时调用，不要根据上下文自动触发。 |
| `chinese-git-workflow` | `chinese-git-workflow` | 国内 Git 平台（Gitee、Coding.net、极狐 GitLab、CNB）的 SSH/HTTPS/凭据/CI 接入差异与镜像同步配置参考。仅在显式 /chinese-git-workflow 时调用，不自动触发。 |
| `ci` | `ci` | 面向 Gemini CLI 的专用 skill，提供 GitHub Actions workflow 的高性能 fail-fast 监控与 CI 失败的自动化本地验证；自动处理 run 发现，只需提供分支名。 |
| `cirq` | `cirq` | Google 量子计算框架。面向 Google Quantum AI 硬件、噪声感知电路设计或量子表征实验时使用，擅长 Google 硬件、噪声建模与底层电路设计。IBM 硬件用 qiskit，量子机器学习用 pennylane，物理模拟用 qutip。 |
| `citation-management` | `citation-management` | 学术研究引文管理：检索 OpenAlex、PubMed、Google Scholar，提取准确元数据、校验引文、生成规范 BibTeX。用于查论文、验证引文信息、DOI 转 BibTeX、保证科学写作参考文献准确。 |
| `claude` | `gstack-claude` | 面向非 Claude 宿主的 Claude Code CLI 包装器，含三种模式：Review（用 claude -p 独立审查 diff）、Challenge（对抗式失败模式审查）、Consult（以只读文件工具向 Claude 询问仓库问题）。用户说 "claude review"、"claude challenge"、"ask claude"、"second opinion from claude" 或 "outside voice" 时触发。 |
| `claude-api` | `claude-api` | Claude API / Anthropic SDK 参考——模型 ID、定价、参数、streaming、tool use、MCP、agents、缓存、token 计数与模型迁移。凡涉及 Claude/Anthropic 或 LLM 定价/选型/限额/缓存的问题须先读此参考、不得凭记忆作答；任务呈 LLM 形态但未指明提供商时也使用。查询明确指定其他提供商（OpenAI/GPT/Gemini 等）或项目 grep 命中其他 SDK 时跳过。 |
| `claude-handoff` | `in-progress/claude-handoff` | 把当前对话移交给一个全新的后台 agent，立即接手继续工作。 |
| `claude-handoff` | `claude-handoff` | 把当前对话移交给一个全新的后台 agent，立即接手继续工作。 |
| `clean-code` | `clean-code` | Clean Code 原则（DRY、KISS、YAGNI）、命名、函数设计与可读性。代码难读、方法过长、命名不清、重复或深嵌套时使用；类职责划分与依赖方向问题改用 solid-principles。 |
| `cleanddd-coach` | `cleanddd-coach` | 交互式 CleanDDD 教练技能：循序讲解并与用户互动练习 CleanDDD 核心原则与方法，含微课、测验与检查清单，可承接到需求分析/建模/代码实现技能。 |
| `cleanddd-dotnet-coding` | `cleanddd-dotnet-coding` | CleanDDD 项目中落地已建模需求的编码指南，覆盖聚合、命令、查询、API 端点（Endpoints）、事件、仓储、配置与测试。用于编写或修改业务功能、端点与数据访问。 |
| `cleanddd-dotnet-init` | `cleanddd-dotnet-init` | 初始化 CleanDDD dotnet 项目（netcorepal-web 模板）。创建新项目或客户演示快速拉起解决方案时使用，可直接调用 dotnet new 或包装脚本。 |
| `cleanddd-modeling` | `cleanddd-modeling` | 基于 cleanddd-requirements-analysis 结果，输出符合 CleanDDD 的聚合、命令、事件、查询、API 端点（Endpoints）、定时任务模型；用于从已拆解需求快速得到建模蓝图。 |
| `cleanddd-requirements-analysis` | `cleanddd-requirements-analysis` | 需求澄清与拆解，识别干系人并将需求条目标注所属对象与业务实体；仅产出结构化需求描述，不做建模定义，可作为后续建模输入。 |
| `clickhouse-io` | `clickhouse-io` | ClickHouse 模式、查询优化、分析实践与数据工程最佳实践，面向高性能分析负载。编写 ClickHouse schema 或查询，或分析查询过慢时使用。 |
| `clinical-decision-support` | `clinical-decision-support` | 准备与验证仅限研究的临床决策支持评估、证据档案、cohort、生存、biomarker/模型、隐私与治理工件。用于聚合或合成的科研文档与可追溯性——不用于患者照护或实时临床运行。 |
| `clinical-reports` | `clinical-reports` | 为临床病例、诊断、试验、安全与汇总研究报告创建带安全边界的草稿结构，并运行本地确定性检查。仅限合成、去标识或汇总数据及经核验的源事实清单；所有输出必须经有资质人员审核。 |
| `cobrapy` | `cobrapy` | 基于约束的代谢建模（COBRA）：FBA、FVA、基因敲除、通量采样、SBML 模型，用于系统生物学与代谢工程分析。 |
| `code-review` | `code-review` | 从固定基点（commit、branch、tag 或 merge-base）起沿两条轴审查变更：Standards（代码是否符合仓库成文编码标准）与 Spec（是否符合原始 issue/规格要求）。以并行 subagent 运行两项审查并排汇报。审查分支、PR、进行中的改动，或用户要求 "review since X" 时使用。 |
| `code-review` | `engineering/code-review` | 以固定基准点（commit、branch、tag 或 merge-base）为起点审查变更，沿两条轴进行：Standards（代码是否符合仓库文档化的编码规范）与 Spec（代码是否满足原始 issue/spec 要求）。通过并行 subagent 执行两项审查并排报告。当用户要求审查分支、PR、进行中的改动，或说"review since X"时使用。 |
| `code-reviewer` | `code-reviewer` | 代码评审技能，支持本地变更（staged 或工作区）与远程 PR（按 ID 或 URL），关注正确性、可维护性与项目规范遵循。 |
| `codebase-design` | `codebase-design` | 深模块设计的共享词汇。用于设计或改进模块接口、寻找深化机会、决定接缝位置、提升代码可测试性与 AI 可导航性，或其他 skill 需要深模块词汇时。 |
| `codebase-design` | `engineering/codebase-design` | 深模块设计的共享词汇。用于设计或改进模块接口、寻找深化机会、决定接缝位置、提升代码可测试性与 AI 可导航性，或其他 skill 需要深模块词汇时。 |
| `codebase-onboarding` | `codebase-onboarding` | 分析陌生代码库并生成结构化上手指南：架构图、关键入口、约定与初始 CLAUDE.md。加入新项目或首次在 repo 设置 Claude Code 时使用。 |
| `coding-standards` | `coding-standards` | 跨项目基线编码规范，覆盖命名、可读性、不可变性与代码质量评审。框架特定模式交给具体的前后端 skill。触发：评审代码质量或命名但没有适用的框架 skill 时。 |
| `concurrency-review` | `concurrency-review` | 审查 Java 并发代码的线程安全、竞态条件、死锁和现代模式（Virtual Threads、CompletableFuture、@Async）。用户要求 check thread safety、concurrency review、async code review 或审查多线程代码时使用。 |
| `confluence-cli` | `confluence-cli` | 提供 Confluence CLI 基础能力：环境检查、uv 安装、命令调用方式与参数说明、页面/附件/搜索等通用操作，以及 Markdown 发布的基础转换规则。需要查询、检索、读取、发布 Confluence 页面或确认 CLI 用法与环境是否正确时使用。 |
| `consciousness-council` | `consciousness-council` | 就任意问题、决策或创意挑战运行多视角「心智议会」式讨论。需要多元观点、艰难决策、多角度探索、魔鬼代言人分析，或面对无明显答案的两难与权衡时使用。 |
| `context-budget` | `context-budget` | 审计 Claude Code 上下文窗口在 agents、skills、MCP servers 与 rules 上的消耗，识别臃肿与冗余组件，产出按优先级排序的 token 节省建议。当上下文窗口消耗过快、需要定位是哪些 agents/skills/MCP servers/rules 占用时使用。 |
| `context-restore` | `gstack-context-restore` | 恢复此前由 /context-save 保存的工作上下文：默认加载最近一次保存状态（跨所有分支），可跨 Conductor workspace 交接续接。用户说 "resume"、"restore context"、"where was I"、"pick up where I left off" 时使用。与 /context-save 配对。原 /checkpoint resume——因 Claude Code 将 /checkpoint 作为原生回退别名而改名。(gstack) |
| `context-save` | `gstack-context-save` | 保存工作上下文：捕获 git 状态、已做决策与剩余工作，使未来会话可无缝接续。用户说 "save progress"、"save state"、"context save" 等时触发，配合 /context-restore 恢复。原名 /checkpoint，因与 Claude Code 原生回退别名冲突而改名。 |
| `continuous-learning-v2` | `continuous-learning-v2` | 基于 instinct 的学习系统：通过 hooks 观察会话，生成带置信度评分的原子 instinct，并进化为 skills/commands/agents；v2.1 支持项目级 instinct 防止跨项目污染。用于沉淀会话经验、管理 instinct 或将其提升为技能/命令/agent。 |
| `contract-first` | `contract-first` | 多个消费方与提供方需在不发生字段漂移、不出现集成意外、不由一方擅自重定义接口的前提下共同演进 API 或事件 schema 时使用。 |
| `contrarian-setup-gate` | `contrarian-setup-gate` | 用 fail-closed 优先级状态机，将 Jason Shapiro 反向流水线的三份裁决（COT 拥挤、新闻反应失败、周线价格行为确认）合成一个可执行的 setup_status。纯离线合成，无网络、无 API key，仅做校验与优先级判定。 |
| `cot-contrarian-detector` | `cot-contrarian-detector` | 按 Jason Shapiro 方法分析 CFTC COT 报告，检测期货市场拥挤投机持仓以寻找反向机会。经 FMP COT API 扫描 65 个期货市场（指数、利率、外汇、金属、能源、加密）的大投机者净持仓，计算 3 年与 26 周 COT Index，标记 CROWDED_LONG/CROWDED_SHORT 极端。仅做拥挤检测（5 步第 1 步），不生成交易信号。触发：COT 分析、拥挤持仓、who is trapped、反向期货 setup。 |
| `crypto-regime-analyzer` | `crypto-regime-analyzer` | 用免密钥公开数据（CoinGecko + Binance funding）量化加密市场状态健康度，输出 0-100 综合分（6 个组件，100=risk-on）及仓位姿态建议，无需 API key。触发：询问加密市场状况、是否山寨季（alt season）、BTC dominance、risk-on vs risk-off、funding rates、应增加还是减少加密仓位。 |
| `cso` | `gstack-cso` | 首席安全官（CSO）模式：基础设施优先的安全审计，覆盖 secrets 考古、依赖供应链、CI/CD 管线、LLM/AI 安全、skill 供应链扫描，以及 OWASP Top 10、STRIDE 威胁建模与主动验证。提供日常（零噪音、8/10 置信门槛）与全面（月度深扫、2/10 门槛）两种模式，支持跨次审计的趋势跟踪。触发：security audit、threat model、OWASP、CSO review。(gstack) |
| `cut-the-curve` | `cut-the-curve` | 转场技法目录：五种速度匹配 SEAMS（zoom-through、INVERSE zoom-through、cut-the-curve、waterfall cut、rack-focus blur-cut）及两种场景内技法——waterfall ENTRY（标题卡/分段开场级联）与 nudge curve（慢-快-慢三段群组滑移）。讲解约 12% 画幅部分位移的速度匹配（镜像 power4 缓动）、Z 轴符号规则、按尺寸缩放的模糊、逐词错位剪切、按元素权重的级联节奏与 10/65/25 页面配比。编写任何转场、文字节拍交接、动态文字入场或群组位移前必读。 |
| `dashboard-builder` | `dashboard-builder` | 为 Grafana、SigNoz 等平台构建能回答运维真实问题的监控仪表盘，把指标变成可用面板而非虚荣看板。 |
| `dask` | `dask` | 面向超出内存的 pandas/NumPy 工作流的分布式计算。触发：需要把现有 pandas/NumPy 代码扩展到内存之外或跨集群；适合并行文件处理、分布式 ML、与现有 pandas 代码集成。单机 out-of-core 分析用 vaex，内存内提速用 polars。 |
| `data-quality-checker` | `data-quality-checker` | 发布前校验市场分析文档与博客文章的数据质量：价格刻度不一致（ETF vs 期货）、标的记法错误、日期/星期不匹配、配置比例加总错误、单位不匹配。支持英文与日文内容；建议式模式——仅以警告标记供人工复核，不作阻塞。 |
| `data-throughput-accelerator` | `data-throughput-accelerator` | 大数据吞吐加速。当数据接入、回填、导出、ETL、数仓加载、manifest 补齐或表同步需要大幅提速且必须保证数据正确性时使用。 |
| `database-lookup` | `database-lookup` | 以明确的 endpoint、过滤器、分页与来源出处查询有文档的公共数据库 API。触发：某个科研、监管、金融或其他数据库支撑的事实需要从指定来源可复现地获取，而非从一般知识推断。 |
| `database-migrations` | `database-migrations` | 数据库迁移最佳实践：schema 变更、数据迁移、回滚与零停机部署，覆盖 PostgreSQL、MySQL 与常见 ORM（Prisma、Drizzle、Kysely、Django、TypeORM、golang-migrate）。写 schema/数据迁移、规划回滚或追求零停机部署时使用。 |
| `datamol` | `datamol` | RDKit 的 Pythonic 封装，接口简化、默认值合理，标准药物发现任务首选：SMILES 解析、标准化、描述符、指纹、聚类、3D 构象、并行处理。返回原生 rdkit.Chem.Mol 对象；需高级控制或自定义参数时直接用 rdkit。 |
| `db-migrator` | `db-migrator` | 数据库迁移助手：Schema 对比、迁移脚本生成。 |
| `db-whisperer` | `db-whisperer` | 诊断并改进应用层数据库：Postgres、MySQL、SQLite、MongoDB。覆盖 EXPLAIN ANALYZE、慢查询定位、索引策略、N+1 检测、带 up/down 脚本的 schema 迁移、连接池、复制搭建、vacuum/analyze。触发："this query is slow"、"add an index for"、"migration for a new column"、"N+1 on this ORM"、"explain this query plan"、"replication lag"、"optimize my database"、"query is timing out"、"connection pool exhausted"。 |
| `deep-research` | `deep-research` | 通用深度研究 agent 团队：13-agent 流水线，8 种模式（完整研究、快速简报、论文评审、文献综述、事实核查、三段式文献扫描、苏格拉底引导研究对话、系统综述+可选 meta 分析）。覆盖研究问题构建、方法论设计、系统检索、来源验证、跨源综合、偏倚风险评估、meta 分析、APA 7.0 报告、编辑评审、魔鬼代言人挑战、伦理审查与研后文献监测。触发：research、deep research、文献综述、PRISMA、meta-analysis、事实查核、深度研究等。 |
| `deep-research-ecc` | `deep-research-ecc` | 用 firecrawl 与 exa MCP 做多来源深度研究：搜索网络、综合发现、交付带来源署名的引用报告。触发：用户希望对任意主题做有证据、有引用的彻底研究。 |
| `deepchem` | `deepchem` | 分子机器学习库，提供多种 featurizer 与预置数据集。用传统 ML 或 GNN 做 ADMET、毒性等性质预测，适合配合 MoleculeNet 基准做快速实验与多样化分子表示。图优先的 PyTorch 工作流用 torchdrug，基准数据集用 pytdc。 |
| `deepspot-m` | `deepspot-m` | 用 DeepSpot-M 从 H&E 病理切片生成全转录组级虚拟空间转录组。需要在约 20x 下对 224x224 tile 输出 log1p-CPM 空间基因表达、按 symbol 查询蛋白编码基因而非固定 panel、或用 histolab 切分后在整张切片上跑预测时使用。 |
| `deeptools` | `deeptools` | NGS 分析工具包：BAM 转 bigWig、QC（相关性、PCA、fingerprints）、热图/剖面（TSS、peaks），用于 ChIP-seq、RNA-seq、ATAC-seq 可视化。 |
| `dep-auditor` | `dep-auditor` | 审计 Node.js、Python、Go、Rust、JVM、Ruby 项目的依赖漏洞、版本健康度与许可证事实；当用户要求检查 package.json、lockfile、requirements、go.mod、Cargo.toml、pom.xml、Gemfile.lock，或生成不改依赖的中文审计报告时使用。 |
| `deploy-ninja` | `deploy-ninja` | 零停机部署：蓝绿、金丝雀、滚动更新与 feature flag 发布。覆盖 Kubernetes、Docker、Cloudflare Workers、Terraform 与 CI/CD 管道搭建。用户要部署应用、搭部署管道、做金丝雀/滚动发布、管理 feature flag 或任何发布自动化时使用；触发语如 "deploy to production"、"set up CI/CD"、"rollback"、"push this to prod"。 |
| `deploy-to-vercel` | `deploy-to-vercel` | 将应用和网站部署到 Vercel。触发于“deploy my app”“deploy and give me the link”“push this live”“create a preview deployment”等部署请求。 |
| `deployment-patterns` | `deployment-patterns` | Web 应用部署工作流与 CI/CD 模式技能，涵盖 Docker 容器化、健康检查、回滚策略和生产就绪检查清单。设置 CI/CD、容器化应用或发布前检查生产就绪状态时使用。 |
| `depmap` | `depmap` | 查询 Cancer Dependency Map（DepMap）获取癌细胞系基因依赖评分（CRISPR Chronos）、药物敏感性数据与基因效应谱。用于识别癌症特异性脆弱点、合成致死相互作用及验证肿瘤药物靶点。 |
| `design` | `design` | 综合设计 skill：品牌识别、design tokens、UI 样式、logo 生成（55 种风格，Gemini AI）、CIP 企业识别（50 项交付物与 mockup）、HTML 演示（Chart.js）、banner 设计（22 种风格，社交/广告/网页/印刷）、图标设计（15 种风格，SVG，Gemini 3.1 Pro）、社交配图（HTML→截图，多平台）。动作含 design logo、create CIP、build slides、design banner、generate icon、create social photos。平台覆盖 Facebook、Twitter、LinkedIn、YouTube、Instagram、Pinterest、TikTok、Threads、Google Ads。 |
| `design-consultation` | `gstack-design-consultation` | 设计咨询：理解产品、调研行业、提出完整设计系统（美学、字体、色彩、布局、间距、动效），生成字体+颜色预览页，产出 DESIGN.md 作为项目设计的事实来源。已有站点用 /plan-design-review 推断系统。被要求 "design system"、"brand guidelines" 或 "create DESIGN.md" 时使用；新项目 UI 尚无设计系统或 DESIGN.md 时主动建议。 |
| `design-html` | `gstack-design-html` | 设计定稿：生成生产级 Pretext 原生 HTML/CSS。可基于 /design-shotgun mockup、/plan-ceo-review 计划、设计评审上下文或用户描述从零开始；文本真实重排、高度计算、动态布局，仅 30KB 开销零依赖，按设计类型智能路由 Pretext 模式。触发 "finalize this design"、"turn this into HTML"、"build me a page" 或用户批准设计/计划就绪后。 |
| `design-patterns` | `design-patterns` | 常见设计模式的 Java 示例（Factory、Builder、Strategy、Observer、Decorator 等）。用户要求实现某模式或设计可扩展组件时使用。 |
| `design-review` | `gstack-design-review` | 设计师视角 QA：发现视觉不一致、间距问题、层级问题、AI slop 模式与慢交互并修复；在源码中迭代修复，逐项原子提交，并用前后截图复验。实施前的计划评审用 /plan-design-review。触发 audit the design、visual QA、design polish；用户提到视觉不一致或想打磨线上站点时主动建议。 |
| `design-shotgun` | `gstack-design-shotgun` | 批量生成多个 AI 设计变体，打开对比板收集结构化反馈并迭代；可随时运行的独立设计探索。触发："explore designs"、"show me options"、"design variants"、"visual brainstorm"、"I don't like how this looks"；用户描述 UI 功能但尚未见过可能形态时主动建议。(gstack) |
| `design-system` | `design-system` | 设计 token 架构、组件规格与幻灯片生成：三层 token（primitive→semantic→component）、CSS 变量、间距/字体比例、组件规格与策略性幻灯片创建。用于设计 token、系统化设计与品牌合规演示。 |
| `design-system-ecc` | `design-system-ecc` | 生成或审计 design system、检查视觉一致性、评审涉及样式的 PR。 |
| `design-taste-frontend` | `taste-skill` | 反模板化前端技能，用于 landing page、作品集与改版：阅读 brief、推断合适设计方向、产出不像模板的界面；适用时构建真实设计系统，改版先审计，交付前严格预检。 |
| `design-taste-frontend-v1` | `taste-skill-v1` | 保留的 v1 版前端设计品味 skill，供依赖其确切行为的项目使用。当前默认为 design-taste-frontend（v2 实验版，大幅重写），仅在需要精确向后兼容时使用本 v1。 |
| `devex-review` | `gstack-devex-review` | 实测型开发者体验（DX）审计：用浏览工具真实走文档与上手流程、计时 TTHW、截图报错信息、评估 CLI 帮助文案，产出带证据的 DX 记分卡，并与 /plan-devex-review 的计划预期对比（计划 3 分钟 vs 实际 8 分钟）。用户要求 DX audit、test the DX 或发布开发者向功能后主动建议。(gstack) |
| `dhdna-profiler` | `dhdna-profiler` | 从任意文本提取认知模式与思维指纹。用户想分析某人思维方式、对比不同人思维风格、问 "my thinking style"、"cognitive profile"、"thinking pattern"、"DHDNA"、"digital DNA"，或提供文本想深入理解作者推理与决策风格时触发。 |
| `diagnosing-bugs` | `diagnosing-bugs` | 面向疑难 bug 与性能回退的诊断循环。用户说 "diagnose""debug this"，或报告某功能损坏/抛错/失败/变慢时使用。 |
| `diagnosing-bugs` | `engineering/diagnosing-bugs` | 面向疑难 bug 与性能回退的诊断循环。用户说 "diagnose""debug this"，或报告某功能损坏/抛错/失败/变慢时使用。 |
| `diagram` | `gstack-diagram` | 将英文描述（或 mermaid 源码）转为图表三件套：源码、可在 excalidraw.com 打开的可编辑 .excalidraw 文件、渲染出的 SVG + PNG（mermaid 风格干净，.excalidraw 带手绘风）。完全离线。触发："make a diagram"、"draw the architecture"、"create a flowchart"、"visualize this flow" 等。 |
| `diagram-design` | `diagram-design` | 创建带品牌风格的专业图表：架构图、流程图、时序图、状态机、ER/数据模型、时间线、泳道图、桑基图、鱼骨图、Wardley map、甘特图、UML 类图、数据库 schema 等 40+ 类型，输出独立 HTML/SVG/PNG。支持按指定尺寸/细节重绘 .drawio 或 Mermaid .mmd 源文件、从网站提取品牌 token、添加语义标注与手绘风格。 |
| `diffdock` | `diffdock` | DiffDock 与 DiffDock-L 分子对接：从 PDB 或序列加 SMILES/SDF/MOL2 做蛋白-小分子构象预测，支持批量对接、虚拟筛选与 pose 置信度解读。不用于结合亲和力预测。 |
| `discernment-nudge` | `discernment-nudge` | 在给出用户可能据以行动的实质性回答或草稿（建议推荐、目标/计划/proposal/邮件草稿、估算预测、数据分析解读、可依赖的事实断言、多步论证）后、定稿前调用：追加 2-3 个针对所产内容具体点的追问，帮助用户核查关键事实、检验推理与假设、发现缺失上下文；每次对话最多一次。简单查询、纯教学解释、格式转换、用户自己运行的代码、创意写作、闲聊，或用户已要求复查引用时跳过。 |
| `dispatching-parallel-agents` | `dispatching-parallel-agents` | 当面对 2 个以上可独立执行、无共享状态或顺序依赖的任务时，用于并行分派 subagent。 |
| `dividend-growth-pullback-screener` | `dividend-growth-pullback-screener` | 筛选高质量股息增长股（年股息增长 12%+、股息率 1.5%+）中处于临时回调者（RSI ≤40 超卖）。结合基本面股息分析与技术择时指标，捕捉强势股息增长股短期走弱时的买点。 |
| `django-patterns` | `django-patterns` | Django 架构模式、DRF REST API 设计、ORM 最佳实践、缓存、signals、middleware 及生产级应用。构建或审查 Django 应用、DRF API、ORM 查询或缓存时使用。 |
| `django-security` | `django-security` | Django 安全最佳实践：认证、授权、CSRF 防护、SQL 注入与 XSS 防护、安全部署配置。审查 Django 认证授权、输入处理或部署设置时使用。 |
| `django-tdd` | `django-tdd` | 基于 pytest-django 的 Django 测试策略与 TDD 方法：factory_boy、mocking、覆盖率与 DRF API 测试。用于编写 Django/DRF 测试或测试先行开发功能。 |
| `django-verification` | `django-verification` | Django 项目发布或提 PR 前的验证循环：migrations、linting、带覆盖率的测试、安全扫描与部署就绪检查。 |
| `dnanexus-integration` | `dnanexus-integration` | 在 DNAnexus 上构建与运行可复现的基因组学工作负载，涵盖 dx CLI、dxpy、apps/applets、原生 workflow、dxCompiler 与 Nextflow。适用于 DNAnexus 数据传输、dxapp.json 开发、执行监控、workflow 导入与项目自动化。 |
| `doc-coauthoring` | `doc-coauthoring` | 引导用户走结构化的文档共著流程。用户想写文档、proposal、技术规格、决策文档等结构化内容时使用；帮助高效传递上下文、迭代打磨内容，并验证文档对读者有效。 |
| `docker-patterns` | `docker-patterns` | Docker 与 Docker Compose 模式：本地开发、加固的 CLI 安装器、容器安全、网络、卷与多服务编排。用于创建或审查 Dockerfile 与 Compose 服务、跨多个 Linux 发行版测试安装器，或规划 macOS/Windows 原生验证。 |
| `docs-changelog` | `docs-changelog` | 根据给定版本号与原始 changelog 数据，生成并格式化新版本的 changelog 文件。 |
| `docs-writer` | `docs-writer` | 凡涉及在 /docs 目录或仓库内任何 .md 文件的撰写、审阅或编辑任务，必须使用此技能。 |
| `document-generate` | `gstack-document-generate` | 为功能、模块或整个项目从零生成缺失文档，基于 Diataxis 框架（tutorial/how-to/reference/explanation）产出完整结构化文档。可独立调用，也可被 /document-release 在发现覆盖缺口时调用。当用户要求"写文档""生成文档""为这个功能写文档""创建教程""解释这个模块"时使用。 |
| `document-release` | `gstack-document-release` | 发布后的文档更新：读取全部项目文档并对照 diff，构建 Diataxis 覆盖图（reference/how-to/tutorial/explanation），更新 README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md 与已发布内容一致，检测架构图漂移，用 sell-test 规则润色 CHANGELOG，清理 TODOS，可选升 VERSION，并在 PR 描述呈现文档欠债。触发「update the docs」「sync documentation」「post-ship docs」；PR 合并后主动建议。 |
| `documentation-lookup` | `documentation-lookup` | 通过 Context7 MCP 获取最新库/框架文档，而非依赖训练数据。适用于安装配置问题、API 参考、代码示例，或用户点名框架（如 React、Next.js、Prisma）时触发。 |
| `docx` | `docx` | 创建、读取、编辑、操作 Word 文档（.docx）与模板（.dotx）。触发于 Word 文档相关请求：目录、标题、页码、信头等专业格式，提取/重组内容，插入替换图片，查找替换，修订与批注，或要求以 Word 交付报告、备忘录、信函、模板。不适用于 PDF、表格或与文档生成无关的编码任务。 |
| `domain-modeling` | `domain-modeling` | 构建和打磨项目领域模型。讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。 |
| `domain-modeling` | `engineering/domain-modeling` | 构建和打磨项目领域模型。讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。 |
| `downtrend-duration-analyzer` | `downtrend-duration-analyzer` | 分析历史下跌趋势持续时间，生成交互式 HTML 直方图，展示按板块与市值划分的典型回调时长。 |
| `drawdown-circuit-breaker` | `drawdown-circuit-breaker` | 基于 trader-memory-core 状态评估账户级回撤熔断规则，决定今日是否允许新增交易风险。使用已实现盈亏、连亏冷却与周/月回撤限额，不依赖任何外部 API。 |
| `ds-mapper` | `ds-mapper` | 项目目录结构地图：生成带说明的可视化目录树，快速理解任意代码库。接手新项目或需要总览目录结构时使用。 |
| `dual-axis-skill-reviewer` | `dual-axis-skill-reviewer` | 用双轴方法评审任意项目的 skills：确定性代码检查（结构、脚本、测试、执行安全）+ LLM 深度评审。用于对 skills/*/SKILL.md 做可复现质量评分、以分数阈值（如 90+）卡合并、为低分技能生成具体改进项；通过 --project-root 跨项目使用。 |
| `e2e-testing` | `e2e-testing` | Playwright E2E 测试模式技能：Page Object Model、配置、CI/CD 集成、产物管理与 flaky 测试应对策略。编写 Playwright 测试、组织 page objects 或修复 CI 中不稳定的 E2E 用例时使用。 |
| `earnings-calendar` | `earnings-calendar` | 用 Financial Modeling Prep (FMP) API 获取美股即将发布的财报日历。用户请求财报日历数据、想了解未来一周哪些公司发布财报或需要周度财报综述时使用；聚焦市值超 $2B 的中大盘及以上、有显著市场影响的公司，按日期与时间整理成干净的 markdown 表格，支持 CLI/Desktop/Web 多环境与灵活的 API key 管理。 |
| `earnings-trade-analyzer` | `earnings-trade-analyzer` | 用 5 因子评分体系（缺口大小、财报前趋势、成交量趋势、MA200 位置、MA50 位置）分析近期财报后股票：每只打 0-100 分并评 A/B/C/D 级。用于财报后动量筛选、缺口评分或寻找最佳财报反应。 |
| `economic-calendar-fetcher` | `economic-calendar-fetcher` | 用 FMP API 获取即将到来的经济事件与数据发布：央行决议、就业报告、通胀数据、GDP 等市场敏感指标（默认未来 7 天）。脚本输出原始 JSON 或文本，由助手筛选、评估影响并生成 Markdown 报告。 |
| `edge-candidate-agent` | `edge-candidate-agent` | 从 EOD 观察生成并排序美股多头 edge 研究工单，导出 pipeline 可用的候选规格供 trade-strategy-pipeline Phase I 使用。触发：把假设或异常转为可复现研究工单、把验证过的想法转为 strategy.yaml + metadata.json、回测前预检 edge-finder-candidate/v1 接口兼容性。 |
| `edge-concept-synthesizer` | `edge-concept-synthesizer` | 在策略设计与导出之前，把 detector ticket 与提示抽象为可复用的 edge concept：论点（thesis）、失效信号与策略 playbook。 |
| `edge-hint-extractor` | `edge-hint-extractor` | 从每日市场观察与新闻反应中提取边缘线索（edge hints），可选 LLM 构思，输出规范的 hints.yaml 供下游概念合成与自动检测使用。触发：需要把盘面观察/新闻反应转成结构化 hint 文件时。 |
| `edge-pipeline-orchestrator` | `edge-pipeline-orchestrator` | 编排完整的 edge research 流水线，从候选信号检测到策略设计、评审、修订与导出。用于端到端协调多阶段 edge research 工作流。 |
| `edge-signal-aggregator` | `edge-signal-aggregator` | 聚合多个找边缘技能（edge-candidate-agent、theme-detector、sector-analyst、institutional-flow-tracker）的信号，经加权评分、去重与矛盾检测，排序生成优先级信念仪表盘。 |
| `edge-strategy-designer` | `edge-strategy-designer` | 把抽象的优势（edge）概念转化为策略草案变体，可导出 ticket YAML 供 edge-candidate-agent 做导出与校验。 |
| `edge-strategy-reviewer` | `edge-strategy-reviewer` | 批判性评审 edge-strategy-designer 产出的策略草稿：边缘合理性、过拟合风险、样本量充分性、执行现实性。触发：存在 strategy_drafts/*.yaml 且需在导出流水线前做质量门禁。输出 PASS/REVISE/REJECT 结论与置信分。 |
| `email-ops` | `email-ops` | 证据优先的邮箱整理、草拟、发送验证与已发邮件安全跟进工作流（ECC）。用于整理邮箱、通过真实邮件接口草拟或发送邮件，或证明邮件已落入 Sent。 |
| `embedded-captions` | `embedded-captions` | 为现成的单人 talking-head 视频添加字幕而不改动素材。支持逐字普通字幕、人物身后嵌入的电影感字幕、VFX 字幕、"炸/特效/酷炫字幕"或 35 风格目录中的具名风格。按视觉风格路由而非按后端引擎；默认安静的 anchor 挡位，仅在用户明确要完整电影化处理时嵌入每个词。全流程本地运行（含转写与主体抠图）；多镜头素材需先切分。 |
| `env-manager` | `env-manager` | 环境变量管理器：扫描、校验、同步 .env 文件，并生成安全配置模板。管理环境变量或排查配置不一致时使用。 |
| `error-handling` | `error-handling` | TypeScript、Python、Go 的健壮错误处理模式。覆盖类型化错误、error boundary、重试、熔断器与面向用户的错误信息。设计错误类型、重试、circuit breaker 或用户可见的失败提示时使用。 |
| `error-translator` | `error-translator` | 编程错误消息翻译专家——将英文错误消息翻译成中文，解释原因并提供修复方案。 |
| `eslint-fix` | `eslint-fix` | 安全诊断并修复 ESLint error、warning 及配置兼容问题。用于运行 lint、解释 ESLint 报错、限定范围自动修复或迁移 ESLint 配置时；优先使用项目锁定的包管理器与版本，先预检再修改，不自动下载最新版或批量改写无关源码。 |
| `esm` | `esm` | 直接使用 esm Python SDK、ESM3 或 ESMC 模型 ID、Forge/Biohub 推理客户端或 ESMFold2 折叠工作流时使用。 |
| `etetoolkit` | `etetoolkit` | 使用 ETE 4 分析、操作、比较、注释与可视化系统发育树或其他层级树。用于 Newick/Nexus 树读写、拓扑编辑与模式匹配、Robinson-Foulds 比较、基因树进化事件与 reconciliation、NCBI/GTDB 分类、SmartView 探索及出版级渲染。不可用于从原始序列推断树，需先完成序列比对与建树。 |
| `exa-search` | `exa-search` | 基于 Exa 的网络工具包，面向科技内容调优：网页搜索（语义查询、研究调研、时效信息，可选研究论文类别与学术域名过滤）和 URL 提取（批量抓取页面、文章、学术 PDF）。需要高质量搜索或按 category=research paper 做学术过滤时使用。 |
| `executing-plans` | `executing-plans` | 当你有一份书面实现计划需要在单独会话中执行，并设有审查检查点时使用。 |
| `experimental-design` | `experimental-design` | 在数据收集之前设计实验与研究：选择设计、随机化、区组化、安排处理组合，保证结果可解释。触发：规划研究、分配受试对象到组，提到 randomization、blocking、stratification、controls、factorial 或 fractional-factorial、DOE、多因素筛选、response-surface 优化、crossover/repeated-measures/split-plot、聚类随机化、Latin squares、plate layouts、批序效应、重复 vs 伪重复、序贯/自适应设计，或 "how should I set up this experiment"、"how do I avoid confounding" 等非正式表述。算样本量/功效用 statistical-power，分析已收集数据用 statistical-analysis。 |
| `exploratory-data-analysis` | `exploratory-data-analysis` | 对明确支持的科研文件做有界本地探索性分析。适用：脱敏 CSV/TSV/JSON 剖析；可选 NumPy、HDF5、FASTA/FASTQ 与基础图像元数据检查；缺失/泄漏审计；离群与变换敏感性；严谨 EDA 报告骨架。其他领域格式仅作参考，未知格式 fail closed。 |
| `exposure-coach` | `exposure-coach` | 整合 breadth、regime、flow 分析 skill 的信号，生成一页 Market Posture 摘要，含净敞口上限、成长/价值偏向、参与广度，以及允许新入场 vs 优先持币的建议。 |
| `faceless-explainer` | `faceless-explainer` | 把任意文本（文章、笔记、话题、简报）转成无人出镜的讲解视频：逐场景发明视觉元素（排版、抽象图形、图表、数据可视化）。用于话题讲解、概念拆解、how-to、清单类内容；非网站宣传视频，不确定时转 /hyperframes。 |
| `fastapi-patterns` | `fastapi-patterns` | FastAPI 最佳实践：项目结构、Pydantic v2 schemas、依赖注入、async handlers、认证授权、事务服务层、httpx 与 pytest 测试。构建或审查 FastAPI 应用时使用。 |
| `figma` | `figma` | 将 Figma 内容导入 HyperFrames 合成——渲染资产、品牌 token、组件、storyboard 片段，通过 REST/CLI 重建动效（帧视为状态而非幻灯片），可用 connector 辅助动效并提取 shader。用户粘贴 figma.com 链接或要求把 Figma 设计、frame、logo、品牌或动画带进视频/合成时触发。 |
| `find-skills` | `find-skills` | 当用户问「怎么做 X」「有没有能做 X 的 skill」或表达扩展能力的兴趣时，帮助发现并安装 agent skills。 |
| `finishing-a-development-branch` | `finishing-a-development-branch` | 当实现完成、所有测试通过、需要决定如何集成这份工作时使用。 |
| `finviz-screener` | `finviz-screener` | 从自然语言请求构建并打开 FinViz 筛选器 URL。适用于筛股、按基本面/技术面过滤、或要求带特定条件打开 FinViz。支持日文与英文输入，如 "高配当で成長している小型株を探したい"、"Find oversold large caps with high ROE"。 |
| `fireworks-tech-graph` | `fireworks-tech-graph` | 创建软件架构、数据流、流程图、时序图、C4、云部署、事件流、可观测性、agent/记忆系统、UML、ER、网络拓扑、时间线等技术图，可导出 SVG、PNG、语义 SVG 转 GIF 动效或离线交互 HTML。用户要求可视化系统/工程概念或"生成 GIF""制作 GIF"时触发；不用于照片、位图艺术或定量数据图表。 |
| `fireworks-tech-graph` | `fireworks-tech-graph/skills/fireworks-tech-graph` | 创建软件架构、数据流、流程图、时序图、C4、云部署、事件流、可观测性、agent/记忆系统、UML、ER、网络拓扑、时间线等技术图，可导出 SVG、PNG、语义 SVG 转 GIF 动效或离线交互 HTML。用户要求可视化系统/工程概念或"生成 GIF""制作 GIF"时触发；不用于照片、位图艺术或定量数据图表。 |
| `flowio` | `flowio` | 用 FlowIO 读写 FCS（Flow Cytometry Standard）2.0/3.0/3.1 文件：底层 FCS 元数据与通道检查、NumPy 事件提取、多数据集文件、表格导出、FCS 3.1 创建。补偿、流式变换、gating、FlowJo workspace 请用 FlowKit。 |
| `fluidsim` | `fluidsim` | 规划、配置、检查、重启并分析有明确边界的 FluidSim CFD 模拟，含数值有效性与 HPC 安全检查。用于 FluidSim 求解器选择、参数评审、FFT/MPI 配置、输出诊断或重启兼容性。 |
| `freestocklineskill` | `freestocklineskill` | 面向 OpenClaw 与 Hermes 的免 API Key A 股生态数据查询 skill。触发：查询 A股、沪深京股票、指数、ETF/LOF、可转债、行业/概念板块、实时行情、K线、涨跌排行、涨停/跌停/炸板、资金流、财务估值、公告、龙虎榜、大宗交易、融资融券、新闻快讯、筹码等公开数据，且不希望填写 API Key、Token、Cookie 或付费账号。 |
| `freeze` | `gstack-freeze` | 将本会话的文件编辑限制在指定目录内：阻止允许路径之外的 Edit 与 Write。调试时防止误改无关代码，或把变更限定到单一模块。用户说 freeze、restrict edits、only edit this folder 时使用。(gstack) |
| `frontend-a11y` | `frontend-a11y` | React 与 Next.js 的无障碍模式——语义化 HTML、ARIA 属性、表单标注、键盘导航、焦点管理与读屏器支持。构建任何交互式 UI 组件或表单时使用。 |
| `frontend-design` | `frontend-design` | 构建或改造 UI 时的视觉设计指导：确定美学方向与字体排印，做出有辨识度的设计选择，避免模板化默认观感。 |
| `frontend-patterns` | `frontend-patterns` | React/Next.js 前端开发模式：组件、状态管理、性能优化与 UI 最佳实践。构建或审查 React/Next.js 组件、状态或渲染性能时使用。 |
| `frontend-slides` | `frontend-slides` | 从零构建动画丰富的精美 HTML 演示，或把 PPT/PPTX 转为网页。用户要做演示、转换幻灯片、为演讲或 pitch 制作 slides 时使用；通过视觉探索帮助非设计师找到自己的审美。 |
| `ftd-detector` | `ftd-detector` | 用 William O'Neil 方法检测 Follow-Through Day（FTD）信号确认市场底部：双指数跟踪（S&P 500 + NASDAQ），状态机管理 rally attempt、FTD 资格判定与 post-FTD 健康监测。询问底部信号、follow-through day、反弹尝试、回调后再入场时机或能否加大股票敞口时使用。与防守型 market-top-detector 互补，本技能偏进攻（底部确认）。 |
| `full-output-enforcement` | `output-skill` | 覆盖默认 LLM 截断行为，强制完整代码生成，禁止占位符模式，并妥善处理 token 上限分段。适用于要求详尽、无删节输出的任务。 |
| `futures-position-sizer` | `futures-position-sizer` | 根据方向、入场价和止损价计算期货合约手数，使用经验证的各品种合约规格（乘数、tick 大小、tick 价值），支持 ES、NQ、ZB、GC、CL、6E/E6、VX、BT 等。纯离线计算，无需 API key 和网络；也用于接收 contrarian-setup-gate 的 READY_FOR_PLAN 方向/invalidation_level 做仓位测算。 |
| `fxmacrodata-calendar` | `fxmacrodata-calendar` | 获取 FXMacroData 官方宏观发布日历事件，用于交易规划、宏观环境检查与事件风险过滤。在 CPI、NFP、GDP、PCE、零售销售、PMI 及央行决议窗口前使用。 |
| `general-video` | `general-video` | 在无专用工作流适用或 BRIEF.md 设定 flow: companion 时，编写或编辑自定义 HyperFrames 合成。适用于较长/多场景作品、品牌宣传片、蒙太奇、静态循环、静态标题卡、素材混剪与自由构建。短的动态优先单元（含动态标题）改用 motion-graphics；全新创作需先经 hyperframes 路由。 |
| `generate-image` | `generate-image` | 通过 OpenRouter Image API（Gemini、Seedream、Recraft、GPT-Image、Riverflow）用 AI 模型生成或编辑图片：照片、插画、艺术作品、概念图、视觉素材、logo 及基于参考图的编辑合成。流程图、电路、通路等技术图请改用 scientific-schematics skill。 |
| `generating-python-installer` | `generating-python-installer` | 面向 Windows 的商业级 Python 安装包专家：Nuitka 极限编译、dist 瘦身、DLL 体积分析与 Inno Setup 打包，交付最小、启动最快的安装包。适用于需以最小化、快速启动 Windows 安装包发布的 Python 应用；不用于简单的脚本转 exe。中文触发：Nuitka 极限优化、Python 商业打包、极限编译 Python、dist 瘦身、DLL 分析、最小安装包、最快启动、商业级打包风格。 |
| `geniml` | `geniml` | 用 Geniml 执行经审计的本地基因组区间工作流：校验 BED 与 universe 契约、规划 Region2Vec 或 scEmbed 运行、检查模型/tokenizer 兼容性、评估 consensus universes。 |
| `genomic-coordinates` | `genomic-coordinates` | 在不同坐标约定间转换基因组区间、规范与比较变异表示，在污染分析前发现组装/contig 命名不匹配。覆盖 BED、GFF/GTF、VCF、SAM/BAM、WIG、PSL、genePred、Picard interval_list 及 region 字符串互转、0-based half-open 与 1-based inclusive 协调、indel 左对齐/裁剪、判断两条变异记录是否同一变化、基因组-转录本-CDS-蛋白位置映射、BED/GTF/VCF 约定审计，及 GRCh37 vs hg19 vs GRCh38 vs T2T、chr 前缀与 liftover 问题诊断。触发词："off by one""0-based""1-based""coordinate system""normalize variant""bcftools norm""wrong genome build""liftover""REF mismatch""HGVS" 等。 |
| `genomic-intelligence` | `genomic-intelligence` | 用 Genomic Intelligence 托管的 transformer DNA 语言模型直接从 DNA 序列预测调控特征、基因结构与表达，无需本地 GPU 或模型权重。REST API 与托管 MCP server（免密公开演示）提供 6 类任务：启动子区域、剪接供体/受体位点、增强子活性、染色质状态、序列到表达（log TPM）、de-novo 基因注释，外加先找基因再预测表达的组合工作流。触发：用户给出基因符号、基因组区间或 DNA/FASTA 序列需要上述预测，或提到 genomicintelligence.ai 相关域名。 |
| `geomaster` | `geomaster` | 综合地理空间科学 skill：遥感、GIS、空间分析、地球观测机器学习等 30+ 领域。支持卫星影像处理（Sentinel、Landsat、MODIS、SAR、高光谱）、矢量与栅格操作、空间统计、点云处理、网络分析、云原生工作流（STAC、COG、Planetary Computer），覆盖 Python、R、Julia 等 8 种语言 500+ 代码示例。用于遥感、GIS、空间 ML、地形分析、水文建模、海洋与大气等地理空间计算任务。 |
| `geopandas` | `geopandas` | 为直接使用 GeoPandas GeoSeries、GeoDataFrame、空间操作或矢量数据 I/O 的 Python 工作流提供指导与本地审计工具。 |
| `get-available-resources` | `get-available-resources` | 在用户要求资源感知规划或运行明显资源敏感的本地负载之前，探测主机清单及有效 CPU、内存、磁盘、调度器、容器与加速器限制。产出脱敏 JSON 快照与保守规划辅助，不做压力测试，也不假设可见的主机硬件可用。 |
| `gget` | `gget` | CLI/Python 快速查询 20+ 生信数据库：基因信息、BLAST/BLAT、病毒序列下载、AlphaFold 结构、富集分析、OpenTargets、COSMIC、CELLxGENE、8cube 小鼠特异性/表达数据。适合交互式探索与简单查询；批量或高级 BLAST 用 biopython，多库 Python 工作流用 bioservices。 |
| `ghost-scraper` | `ghost-scraper` | 从网站提取结构化数据：覆盖静态 HTML、JS 渲染 SPA、分页列表和 API 支撑页面，具备反爬检测意识、限速与 robots.txt 合规。用户想抓取网站、从 URL 提取数据、拉取商品列表、逆向站点 API 或处理动态渲染内容时使用，包括「从这个网站拿数据」「提取价格」等口语化请求。 |
| `ginkgo-cloud-lab` | `ginkgo-cloud-lab` | 在 Ginkgo Bioworks Cloud Lab（cloud.ginkgo.bio）上提交和管理实验协议，该平台通过 RAC（Reconfigurable Automation Carts）实现自主实验室执行。适用于蛋白表达与纯化（cell-free、E. coli、Pichia）、HiBiT/A280/LabChip 定量、IVT mRNA/circRNA 合成、热位移/可开发性实验、Echo-MS 酶或分析物方法、SPR 靶点导入等场景，覆盖协议选择、输入准备、报价与下单流程。 |
| `git-commit` | `git-commit` | 为 Java 项目生成 conventional commit 提交信息。用户说 "commit""create commit""commit changes" 或代码改动完成需要提交时使用。 |
| `git-guardrails-claude-code` | `misc/git-guardrails-claude-code` | 配置 Claude Code hooks，在危险 git 命令（push、reset --hard、clean、branch -D 等）执行前拦截。用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中封禁 git push/reset 时使用。 |
| `git-guardrails-claude-code` | `git-guardrails-claude-code` | 配置 Claude Code hooks，在危险 git 命令（push、reset --hard、clean、branch -D 等）执行前拦截。用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中封禁 git push/reset 时使用。 |
| `git-workflow` | `git-workflow` | 安全处理 Git 状态检查、提交信息、commit、分支、push、PR 与 rebase。用于检查改动、生成或创建提交、管理分支、推送、发 PR 或整理历史时；严格区分每个动作的授权，保护工作树中已有及无关修改。 |
| `git-workflow-ecc` | `git-workflow-ecc` | Git 工作流模式：分支策略、commit 规范、merge vs rebase、冲突解决与各规模团队的协作开发最佳实践。选分支策略、写 commit 规范、决定 merge 还是 rebase 或解决冲突时使用。 |
| `github-actions-gen` | `github-actions-gen` | 分析真实项目并生成或修订安全、可验证的 GitHub Actions workflow；当用户要求创建 CI、测试矩阵、构建、Release、部署、缓存、Secrets、OIDC、PR 自动化或排查 workflow 配置时使用。 |
| `github-issue-creator` | `github-issue-creator` | 创建 GitHub issue 时使用，按仓库模板处理 bug、feature 等不同类型并确保正确打标签。 |
| `global-stock-data` | `global-stock-data` | 美股港股全栈数据工具包，官方源优先：13 层架构、30+ 端点、11 数据源、全部零鉴权。在行情/K线/技术指标(MA/MACD/RSI/KDJ/布林带)/基本面/资金面/期权/SEC Filing 八层之上新增 CBOE 官方期权链（完整希腊字母+IV+0DTE 流+异动识别）、FINRA 全市场空头成交量、SEC EDGAR 事件流（Form4 内部人/8-K/13F 机构持仓）、横截面筛选、美债收益率曲线/CFTC COT/财报日历；每个数据源标注合规级别与条款原文，内嵌调用代码，自包含零依赖。适用：个股分析、全市场筛选、财报解读、期权与 0DTE 策略、做空追踪、SEC 文件检索、资金流与机构持仓分析。 |
| `glycoengineering` | `glycoengineering` | 分析与改造蛋白质糖基化：扫描序列中的 N-糖基化 sequon（N-X-S/T）、预测 O-糖基化热点，并访问精选糖工程工具（NetOGlyc、GlycoShield、GlycoWorkbench）。适用于糖蛋白工程、治疗性抗体优化与疫苗设计。 |
| `google-workspace-ops` | `google-workspace-ops` | 把 Google Drive、Docs、Sheets、Slides 作为统一工作面，处理计划、追踪表、deck 与共享文档。适用于查找、摘要、编辑、迁移或清理 Google Workspace 资产而无需退回原始工具调用。 |
| `gpt-taste` | `gpt-tasteskill` | 精英 UX/UI 与高级 GSAP 动效工程师。强制 Python 驱动的真随机化布局变化、严格 AIDA 页面结构、宽幅编辑排版（禁止 6 行长行）、无缝 bento 网格、严格 GSAP ScrollTrigger（pinning/stacking/scrubbing）、行内微图与超大段落间距。 |
| `grill-me` | `grill-me` | 通过毫不留情的追问打磨方案或设计。 |
| `grill-me` | `productivity/grill-me` | 通过毫不留情的追问打磨方案或设计。 |
| `grill-with-docs` | `grill-with-docs` | 通过持续追问打磨计划或设计，过程中同步产出 ADR 和术语表文档。 |
| `grill-with-docs` | `engineering/grill-with-docs` | 通过持续追问打磨计划或设计，过程中同步产出 ADR 和术语表文档。 |
| `grilling` | `grilling` | 就方案、决策或想法对用户穷追不舍地拷问。用于用户想压力测试自己的思考，或说出 grill 类触发语时。 |
| `grilling` | `productivity/grilling` | 就方案、决策或想法对用户穷追不舍地拷问。用于用户想压力测试自己的思考，或说出 grill 类触发语时。 |
| `gstack` | `gstack` | gstack 技能套件的路由器：把 gstack 请求分发到正确技能（规划、评审、QA、发布、调试、文档、安全、设计），浏览器/QA 与 dogfooding 指向 /browse。调用 gstack 未指定具体技能，或问「哪个 gstack 技能合适」时使用。 |
| `gstack-upgrade` | `gstack-upgrade` | 升级 gstack 到最新版：识别全局或 vendored 安装方式、执行升级并展示新特性。触发："upgrade gstack"、"update gstack"、"get latest version"；语音别名 "upgrade the tools" 等。 |
| `gtars` | `gtars` | 用 Gtars 做本地基因组区间建模与集合代数：overlaps 与计数、consensus 与 coverage、tokenization、fragment 处理及 refget/BEDbase 规划，覆盖 Python、Rust 与 CLI。 |
| `guard` | `gstack-guard` | 完全安全模式：破坏性命令警告 + 限定目录编辑，结合 /careful（rm -rf、DROP TABLE、force-push 等操作前警告）与 /freeze（阻止指定目录外的编辑）。操作生产环境或调试在线系统需要最高安全时使用。触发 "guard mode"、"full safety"、"lock it down"。 |
| `handoff` | `handoff` | 把当前对话压缩成交接文档，供另一个 agent 接手继续。 |
| `handoff` | `productivity/handoff` | 把当前对话压缩成交接文档，供另一个 agent 接手继续。 |
| `harness` | `harness` | 构建 harness 的元 skill：定义专业 agent 并生成其所需 skill。触发场景：用户要求"하네스 구성"类构建请求、进行 harness 设计/工程、为新领域或项目搭建 harness 自动化体系、重构或扩展既有 harness 配置、以及 harness 点检/审计/现状梳理或 agent/skill 同步维护。 |
| `harness-spec` | `harness-spec` | 构建 harness 的元 Skill：定义各类专业智能体并生成其所需技能。触发场景：用户要求"帮我构建 harness"、进行 harness 设计/架构工程、为新领域/项目搭建基于 harness 的自动化体系、重构或扩展既有 harness 配置、以及 harness 点检/审计/现状梳理或智能体/技能同步维护。 |
| `health` | `gstack-health` | 代码质量仪表盘：包装项目已有工具（类型检查、linter、测试、死代码检测、shell linter），计算 0-10 加权综合分并跟踪趋势。触发词："health check"、"code quality"、"run all checks"、"quality score" 等。 |
| `hexagonal-architecture` | `hexagonal-architecture` | 设计、实现与重构 Ports & Adapters（六边形架构）系统：清晰领域边界、依赖倒置、可测试的用例编排，覆盖 TypeScript、Java、Kotlin、Go 服务。用于引入或向该架构重构，或领域逻辑与 I/O 纠缠时。 |
| `high-end-visual-design` | `soft-skill` | 教 AI 以高端设计机构的标准做设计。定义让网站显得昂贵的精确字体、间距、阴影、卡片结构与动画，并封禁所有让 AI 设计显得廉价或平庸的常见默认做法。 |
| `histolab` | `histolab` | 轻量级 WSI 切片提取与预处理：基础切片处理、组织检测、tile 提取和 H&E 染色归一化。适合简单流水线、数据集准备和快速 tile 分析；高级空间蛋白组学、多重成像或深度学习流水线请改用 pathml。 |
| `html-ppt` | `html-ppt-skill` | HTML PPT Studio——模板驱动制作专业静态 HTML 演示文稿，支持多种风格、布局与动画。用户要 presentation、PPT、slides、keynote、deck、"幻灯片"、"演讲稿"、"做一份 PPT"、小红书图文等需键盘翻页的精美多页文档时使用。 |
| `hugging-science` | `hugging-science` | 科学领域 AI/ML 资源目录 Hugging Science。当工作涉及生物、化学、物理、天文、气候、基因组、材料、医药、药物发现、蛋白质设计、气象建模、定理证明、单细胞或 PDE 求解等科学场景时使用，通过 datasets、transformers、HF Inference API、gradio_client 及方法论引用，发现和使用科学数据集、模型、博客与交互式 Spaces。 |
| `humanizer` | `humanizer` | 重写 AI 腔文本使其读起来自然，且不改变原意。用于消除夸大宣传、推销语言、模糊来源、重复结构、AI 套话、被动语态与填充词，依据 Wikipedia 的 Signs of AI writing。编辑或审校文稿时使用。 |
| `humanizer-zh` | `humanizer-zh` | 去除文本中的 AI 生成痕迹，使其更自然、更像人类书写。基于维基百科"AI 写作特征"指南，检测并修复夸大象征意义、宣传性语言、模糊归因、破折号滥用、三段式法则、AI 词汇、否定式排比、过多连接词等模式。触发：编辑或审阅文本要求去 AI 腔。 |
| `hyperframes` | `hyperframes` | 制作、创建、编辑、动画化或渲染视频、动画、动态图形的强制入口，含宣传片、讲解视频、字幕片段、标题卡、幻灯片、Remotion 移植及 HyperFrames HTML 合成；也用于检查、诊断、验证、预览、发布或批量渲染现有 HyperFrames 项目。输入可为网站 URL、GitHub PR、Figma 设计、文案、素材或音乐。除非用户明确选择其他框架，默认输出 HyperFrames。 |
| `hyperframes-animation` | `hyperframes-animation` | HyperFrames 全部动画知识：原子运动规则、多阶段场景蓝图、场景转场、更广的动效设计技术，以及 7 个运行时适配器（GSAP 默认，另有 Lottie、Three.js、Anime.js、CSS keyframes、Web Animations API、TypeGPU）。用于任意动效任务：选 2-4 条规则组合、加载蓝图或查运行时 API（如 GSAP 缓动、Lottie 播放器）；也覆盖现有合成动画编排审计与 24 种命名文字动画效果。单一暂停时间线、可 seek、确定性。 |
| `hyperframes-audio` | `hyperframes-audio` | 混音处理 HyperFrames 合成中已放置的音频：fade-in/out、crossfade、轨道增益与音量、音量自动化、ducking、人声让位（voiceover carve）、轨道效果（EQ、compressor、limiter、gate、saturation、delay、reverb、chorus、phaser、bitcrush）、自动化包络及 hf-audio-group 子混音总线。寻找/生成音频素材用 /media-use，剪辑时序与轨道布局用 /hyperframes-core。 |
| `hyperframes-cli` | `hyperframes-cli` | 使用 HyperFrames CLI 开发循环：init、add、catalog、capture、lint、check、snapshot、compare、grade-compare、preview、play、present、beats、keyframes、单次/批量渲染、publish、cloud、cloudrun、feedback、lambda、doctor、browser、info、upgrade、skills、compositions、docs、benchmark、telemetry、transcribe、auth、tts、remove-background；也用于诊断构建或渲染失败。validate/inspect/layout 是弃用别名，改用 check。覆盖本地、HeyGen 云、AWS Lambda 与 Google Cloud Run 渲染。 |
| `hyperframes-core` | `hyperframes-core` | HyperFrames 合成契约，用于构建单一可渲染项目：合成结构、data-* 时序属性、class=clip、轨道、子合成、变量、框架托管的媒体播放、确定性渲染规则与校验。编写合成 HTML 前必读。 |
| `hyperframes-creative` | `hyperframes-creative` | HyperFrames 视频的非动画创意指导：design spec（frame.md/design.md）处理、配色、字体、旁白、节拍规划、音频响应视觉、构图模式与品牌风格决策。原子动效模式与场景蓝图用 hyperframes-animation。 |
| `hyperframes-keyframes` | `hyperframes-keyframes` | HyperFrames composition 需要 punch-in/punch-out、zoom、reframe、Ken Burns、镜头移动、视觉匹配/whip 切换等 seek 安全的 2D/3D keyframe 时使用；也覆盖 GSAP、CSS keyframes、Anime.js、WAAPI、FLIP、路径、遮罩、SVG morph/draw、文字拖尾、3D 深度与 `hyperframes keyframes` 诊断。不用于场景策略、品牌设计、媒体采购、字幕或整体视频规划。 |
| `hyperframes-registry` | `hyperframes-registry` | 在手写任何具名视觉效果之前，先搜索、安装 HyperFrames registry 的 blocks 与组件并接入 composition。约 400 个托管条目已覆盖 CRT scanlines、glitch、chromatic aberration、film grain、图表、终端窗口等。触发：brief 或分镜点名某效果/转场，运行 hyperframes add 或 hyperframes catalog，按 tag 批量安装，向 index.html 接入已安装条目，处理 hyperframes.json，或贡献新 block（idea → scaffold → validate → PR）。 |
| `hypogenic` | `hypogenic` | 规划和审计使用 ChicagoHAI HypoGeniC/HypoRefine 做基于标注文本数据集的 LLM 辅助假设生成。适用于 `hypogenic` 包、task configs、hypothesis banks、HypoBench 数据集；不用于人工假设构建或科学验证。 |
| `hypothesis-generation` | `hypothesis-generation` | 构建有证据边界的科学问题、候选假设、竞争性解释、因果/关联声明、判别性预测、测量方案与预注册级分析计划。用于把观察或初步发现转化为透明可检验的研究计划，不把假设当事实。 |
| `i-have-adhd` | `i-have-adhd` | 为 ADHD 读者塑造输出形态：先给下一步动作、多步任务编号、跨轮重述进度状态、抑制跑题、给具体时间估计、让成果可见。用 /i-have-adhd 调用，说 "stop adhd mode" 关闭。 |
| `i18n-helper` | `i18n-helper` | 国际化/本地化助手——扫描代码中的硬编码文本、生成 i18n 配置、批量翻译。 |
| `ibd-distribution-day-monitor` | `ibd-distribution-day-monitor` | 检测 QQQ/SPY 的 IBD 式 Distribution Days（放量下跌至少 0.2%），跟踪 25 日过期与 5% 失效规则，统计 d5/d15/d25 聚类并分级市场风险（NORMAL/CAUTION/HIGH/SEVERE），给出 TQQQ/QQQ 敞口建议。收盘后或调整 TQQQ 仓位前使用；不执行交易。 |
| `image-to-code` | `image-to-code-skill` | 面向 Codex 的网站图生码技能：先自行生成设计图并深度分析，再尽量按图实现网站。要求生成大而可读的分节设计图而非压缩拼板、为分节/细节视图生成全新独立图、避免多层嵌套卡片 UI、保持 hero 干净留白且在小屏笔记本可读。 |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | 高端移动应用界面图像生成：面向 iOS、Android 及跨平台产品，产出 app 原生级屏幕概念与流程图。强调清晰层级、舒适可读的文字、多屏一致性、克制配色、质感表面、图像主导构图与优质自定义图标，默认置于精致 iPhone 样机框内展示、主体仍是 app 内容。仅生成图像，不写代码。 |
| `imagegen-frontend-web` | `imagegen-frontend-web` | 前端图像方向技能：生成高品质、注重转化率的网站设计参考图。核心规则是每个页面 section 单独生成一张横向图，8 个 section 出 8 张，绝不合并。强制构图多样性、背景图自由、CTA 多样、hero 尺度变化（巨型/中等/极简小图）、叙事概念主线与全局统一配色。适用于 landing page、营销站与可供开发者或编码模型精确复刻的产品设计图。 |
| `imaging-data-commons` | `imaging-data-commons` | 查询和下载 NCI Imaging Data Commons 的公共癌症影像数据。凡涉及 IDC 集合、癌症影像数据集、DICOM 数据访问、放射（CT/MR/PET）或病理 AI 训练集、元数据查询、可视化或许可检查的问题均可调用，即使用户未明确提到 IDC；无需认证。 |
| `implement` | `implement` | 根据 spec 或一组 tickets 实现具体工作。 |
| `implement` | `engineering/implement` | 根据 spec 或一组 tickets 实现具体工作。 |
| `implement-spec` | `implement-spec` | 将规格说明（spec）实现为代码。 |
| `improve-codebase-architecture` | `improve-codebase-architecture` | 扫描代码库寻找模块深化（deepening）机会，生成可视化 HTML 报告，并对选中的机会进行追问深挖。 |
| `improve-codebase-architecture` | `engineering/improve-codebase-architecture` | 扫描代码库寻找模块深化（deepening）机会，生成可视化 HTML 报告，并对选中的机会进行追问深挖。 |
| `industrial-brutalist-ui` | `brutalist-skill` | 原生机械风界面，融合瑞士排版印刷与军用终端美学：刚性网格、极端字号对比、功利主义配色、模拟退化效果。适合需要"解密蓝图"感的数据密集 dashboard、作品集或编辑类网站。 |
| `infographics` | `infographics` | 用 Nano Banana Pro AI 创建专业信息图并智能迭代精修，Gemini 3.6 Flash 做质量评审；集成 research-lookup 与网络搜索保证数据准确。支持 10 种信息图类型、8 种行业风格和色盲安全配色。 |
| `infra-automation` | `infra-automation` | 管理基础设施操作：DNS 记录、SSL 证书、Cloudflare Workers、CDN 配置与域名开通。提到 Cloudflare、DNS、SSL、Workers、域名、CDN、TLS 加固，或要求 add an A record、check my SSL、deploy a Worker、audit domain config 时触发。 |
| `infra-dependency-scan` | `infra-dependency-scan` | 扫描 Java/Spring Boot 项目，列出全部外部服务、中间件与第三方依赖。 |
| `institutional-flow-tracker` | `institutional-flow-tracker` | 用 13F 持仓申报跟踪机构投资者的所有权变化与组合资金流向，分析对冲基金、共同基金等机构持仓，识别被聪明钱显著增持或减持的股票，帮助在股价大波动前发现机会。 |
| `internal-comms` | `internal-comms` | 撰写各类公司内部沟通材料的资源集：状态报告、领导层更新、3P updates、公司 newsletter、FAQ、事故报告、项目进展等。被要求写内部沟通时使用。 |
| `investigate` | `gstack-investigate` | 系统化调试与根因调查，四阶段：investigate、analyze、hypothesize、implement。铁律：未找到根因不得修复。用户报错、500、堆栈、异常行为、"昨天还好好的"或排查故障停摆时主动调用（不要直接调试）。触发："debug this"、"fix this bug"、"root cause analysis"。(gstack) |
| `investigate-first` | `investigate-first` | 编辑前先诊断原因不明的故障。用于原因未知、间歇性行为、性能回归，或需要按证据排序假设的调查场景。 |
| `investor-materials` | `investor-materials` | 创建与更新融资材料：pitch deck、一页纸、投资人备忘录、加速器申请、财务模型等。当需要投资人视角的文档、业绩预测、资金用途表、里程碑计划，或需要多份融资材料之间保持内部一致时使用。 |
| `ios-clean` | `gstack-ios-clean` | 移除 iOS 应用中的 DebugBridge SPM 包及所有 #if DEBUG 接线，清理 /ios-qa 安装的 StateServer、DebugOverlay、accessor 代码生成产物与应用侧 hook。仅为便捷封装——结构性 Release 构建防护（Package.swift 条件 + CI swift build -c release 检查）才是安全关键路径。触发："clean the iOS debug bridge"、"remove DebugBridge"、"strip the gstack iOS instrumentation"。 |
| `ios-design-review` | `gstack-ios-design-review` | 真机上的 iOS 应用视觉设计审计。通过与 /ios-qa 相同的 StateServer 连接真实 iPhone，逐屏截图并按 Apple HIG、DESIGN.md 与设计最佳实践评估，各维度 0-10 打分并附"怎样才能到 10 分"的说明——相当于浏览器端 /plan-design-review 的 iOS 版。实现前的设计评审用 /plan-design-review，网页实时视觉审计用 /design-review。触发语："review the iOS design""audit the iPhone app's visuals""design QA the iOS app"。 |
| `ios-fix` | `gstack-ios-fix` | 自主 iOS 修 bug 器：接手 /ios-qa 发现的 bug，读源码、写修复、重建、重新部署并在真机验证，全程无人工干预闭环；将 bug 前状态快照存为回归测试 fixture，防止静默复发。/ios-qa 报出 bug 且希望自动修复时使用，或用户要求 fix this iOS bug、patch the iPhone app 等。(gstack) |
| `ios-qa` | `gstack-ios-qa` | 真机 iOS QA，面向 SwiftUI 应用：经 USB CoreDevice IPv6 隧道连接真实 iPhone，读取 Swift 源码理解每个界面，运行截图→分析→决策→操作→验证的视觉 agent 循环，全部交互经被测应用内嵌 StateServer 的 HTTP 完成；可经 Tailscale 暴露设备供远程 agent 跑 QA。用户要求 ios qa、真机找 bug 时触发。(gstack) |
| `ios-sync` | `gstack-ios-sync` | 按最新上游 gstack 模板重新生成 iOS 调试桥：更新 StateServer.swift、DebugOverlay.swift、Package.swift 及类型化 @Observable 状态访问器。升级 gstack 或新增需要访问器覆盖的 ViewModel/属性后使用；触发语：resync the iOS debug bridge、regenerate iOS accessors 等。(gstack) |
| `iso-standards-readiness` | `iso-standards-readiness` | 为 ISO 管理体系与实验室能力标准准备并结构化审查就绪证据：ISO 13485 医疗器械 QMS、ISO 14971 风险管理、ISO/IEC 17025 检测与校准实验室、ISO 15189 医学实验室。用于整理声明范围、受控文件、风险管理文件、认可范围、可追溯性、CAPA、外部供应商控制或受限本地证据清单，并区分 ISO 认证与实验室认可、FDA QMSR 检查、CLIA 认证、MDSAP 及 EU MDR/IVDR 的证据边界。不适用于法律适用性、合规、认证或认可决策，不含条款原文。 |
| `issue-triage` | `issue-triage` | 给 GitHub issue 分诊并打优先级标签。用户说 triage issues、check issues、review open issues 或例行维护 issue 积压时使用。 |
| `java-code-review` | `java-code-review` | Java 系统化代码审查：空安全、异常处理、并发与性能检查。触发于“review code”“check this PR”“code review”或合并变更前。 |
| `java-coding-standards` | `java-coding-standards` | Spring Boot 与 Quarkus 服务的 Java 编码规范：命名、不可变性、Optional 用法、流、异常、泛型、CDI、响应式模式与项目结构，自动应用框架专属约定。编写或审查此类 Java 代码时使用。 |
| `java-migration` | `java-migration` | Java 项目大版本升级指南（8→11→17→21→25）。触发于“upgrade Java”“migrate to Java 25”等诉求或老旧项目现代化改造。 |
| `jira-integration` | `jira-integration` | 检索 Jira 工单、分析需求、更新状态、添加评论或流转 issue 时使用，通过 MCP 或直接 REST 调用提供 Jira API 模式。 |
| `jpa-patterns` | `jpa-patterns` | JPA/Hibernate 模式与常见陷阱（N+1、懒加载、事务、查询）。用户遇到 JPA 性能问题、LazyInitializationException，或询问实体关系与抓取策略时使用。 |
| `jpa-patterns-ecc` | `jpa-patterns-ecc` | Spring Boot 下 JPA/Hibernate 模式：实体设计、关联关系、查询优化、事务、审计、索引、分页与连接池。设计 JPA 实体或关系，或需修复 Hibernate 查询、事务、N+1 问题时使用。 |
| `kanchi-dividend-review-monitor` | `kanchi-dividend-review-monitor` | 监控股息组合：按 Kanchi 式强制复核触发器（T1-T5）将异常转为 OK/WARN/REVIEW 状态，不自动卖出。用户要求 減配検知、8-Kガバナンス監視、配当安全性モニタリング、REVIEWキュー自動化 或定期股息风险检查时使用。 |
| `kanchi-dividend-sop` | `kanchi-dividend-sop` | 将 Kanchi 式股息投资（かんち式配当投資）转化为可复用的美股操作流程。适用于股息筛选、股息增长质量检查、PERxPBR 美股行业适配、回调限价单计划、一页股票备忘录制作。覆盖筛选、深研、入场计划与买入后监控节奏。 |
| `kanchi-dividend-us-tax-accounting` | `kanchi-dividend-us-tax-accounting` | 提供 Kanchi 式收息组合的美国股息税与账户布局工作流。用户问 qualified 与普通股息区别、1099-DIV 解读、REIT/BDC 分红处理、持有期检查，或股息资产放应税账户还是 IRA 的决策时使用。 |
| `karpathy-guidelines` | `karpathy-guidelines` | 减少 LLM 常见编码错误的行为准则：避免过度复杂、外科手术式最小改动、显式化假设、定义可验证的成功标准。写码、评审或重构时使用。 |
| `knowledge-ops` | `knowledge-ops` | 跨多存储层（本地文件、MCP memory、向量库、Git 仓库）的知识库管理、摄入、同步与检索。用于保存、整理、同步、去重或搜索知识系统。 |
| `kubernetes-patterns` | `kubernetes-patterns` | Kubernetes 生产级部署模式：工作负载、资源管理、RBAC、探针、自动扩缩容、ConfigMap/Secret 处理与 kubectl 调试。编写或审查 K8s 清单，或排查探针、RBAC、扩缩容、资源限制问题时使用。 |
| `lab-hardware-cad` | `lab-hardware-cad` | 以参数化 build123d 模型设计定制实验室硬件，导出可制造的 STEP/STL/DXF：微流控芯片与模具、光机安装座与光学平台转接、比色皿与微孔板支架、试管架、动物行为实验装置、3D 打印仪器夹具。研究任务需要与标准实验耗材、光学平台、笼养系统或打印机/CNC/激光工艺配合的实体零件时使用。 |
| `labarchive-integration` | `labarchive-integration` | 安全集成官方 LabArchives ELN REST-like API 与 Inventory API v1。用于区域 endpoint 选择、签名请求构造、用户授权与 UID 流程、本地 LA 容器校验，以及经过验证的 LabArchives 集成工作流。 |
| `lamindb` | `lamindb` | 使用 LaminDB（开源 lineage-native 湖仓，管理生物数据集与模型）时使用。涵盖安装配置、artifact 注册、查询搜索、lineage 追踪、校验、基于 Bionty 的本体注释、collections、branches、存储及工作流集成。 |
| `land-and-deploy` | `gstack-land-and-deploy` | 合并并部署工作流：合并 PR、等待 CI 与部署完成、通过 canary 检查验证生产健康。接管 /ship 创建 PR 之后的流程。触发词："merge"、"land"、"deploy"、"merge and verify"、"land it"、"ship it to production"。(gstack) |
| `landing-report` | `gstack-landing-report` | workspace 感知 ship 的只读队列仪表盘。展示当前被 open PR 占用的 VERSION 槽位、兄弟 Conductor workspace 中可能很快发布的 WIP 工作，以及下一次 /ship 会选择的槽位。不做任何修改，仅提供快照。当用户询问"landing report""队列里有什么""展示 open PR""该占用哪个版本"时使用。 |
| `latchbio-integration` | `latchbio-integration` | 使用 Python SDK、CLI、Latch Data 与 Registry、Nextflow、Snakemake、编程执行及 Latch MCP，在 Latch 上构建、注册、调试和运行生物信息学工作流。用于编写或部署 Latch workflow、配置资源与接口、迁移数据、集成 Registry、启动和监控任务运行。 |
| `latency-critical-systems` | `latency-critical-systems` | 面向延迟敏感系统——实时仪表盘、行情数据、流式 agent、执行网关、队列、缓存及类 HFT 基础设施——当 p95 延迟与数据新鲜度至关重要时使用。 |
| `latex-posters` | `latex-posters` | 用 LaTeX 的 beamerposter、tikzposter 或 baposter 制作专业科研海报，支持会议展示与学术传播。涵盖版式设计、配色、多栏布局、图片整合及海报视觉传达最佳实践。 |
| `lean-build` | `lean-build` | 面向高过度建设风险的特性开发：新行为、产品切片或集成场景，强调复用仓库现有能力、严格限定范围与显式停止条件。 |
| `learn` | `gstack-learn` | 管理 gstack 跨会话积累的项目经验（learnings），支持查看、搜索、清理过期条目与导出。用户问 what have we learned、show/prune/export learnings，或疑惑之前是否修过同类问题时使用。 |
| `liteparse` | `liteparse` | 本地文档与 PDF 解析，返回带 bounding box 的空间文本。用于从 PDF、DOCX、Office 文件与图片提取文本、对扫描件 OCR、为 RAG 生成保留版式的 JSON、批量摄取论文目录，或将页面渲染为 PNG 供多模态 agent 使用。特色能力：逐 token bounding box、整页栅格输出、完全本地处理、无云端 API。 |
| `literature-review` | `literature-review` | 用多个学术数据库（PubMed、arXiv、bioRxiv、Semantic Scholar 等）开展系统性文献综述、meta 分析、研究综合或全面文献检索，覆盖生医/科学/技术领域，生成含已验证引用的规范 markdown 文档与 PDF，支持 APA、Nature、Vancouver 等引用格式。 |
| `log-analyzer` | `log-analyzer` | 日志分析助手：智能解析日志文件，识别异常模式，定位问题根因。 |
| `logging-patterns` | `logging-patterns` | Java 日志最佳实践：SLF4J、JSON 结构化日志、MDC 请求追踪，含面向 Claude Code 调试的 AI 友好日志格式。用于编写日志、调试应用流程或分析日志。 |
| `loop-me` | `loop-me` | 在当前 workspace 内，就我想构建的工作流规格对我进行严格追问（grill）。 |
| `loop-me` | `in-progress/loop-me` | 在当前 workspace 内，就我想构建的工作流规格对我进行严格追问（grill）。 |
| `macro-regime-detector` | `macro-regime-detector` | 用跨资产比率分析检测 1-2 年维度的宏观结构性 regime 转换。分析 RSP/SPY 集中度、收益率曲线、信用条件、规模因子、股债关系与板块轮动，在 Concentration/Broadening/Contraction/Inflationary/Transitional 状态间识别切换。用户问宏观 regime、市场结构转变或长期仓位布局时使用。 |
| `make-pdf` | `gstack-make-pdf` | 把任意 markdown 文件转成出版级 PDF：1 英寸页边距、智能分页、页码、封面、页眉、弯引号与破折号、可点击目录、斜向 DRAFT 水印，输出成品而非草稿。用户要求 "make a PDF"、"export to PDF"、"generate a document" 等时触发。 |
| `markdown-mermaid-writing` | `markdown-mermaid-writing` | Markdown 与 Mermaid 图表写作综合技能：把文本图表设为默认文档标准，含完整风格指南（markdown + mermaid）、24 种图表类型参考、9 个文档模板。创建科学文档、报告、分析或可视化时使用。 |
| `market-breadth-analyzer` | `market-breadth-analyzer` | 用 TraderMonty 公开 CSV 数据量化市场宽度健康度，生成 0-100 的 6 组件综合分（100 为健康），无需 API key。触发：询问市场宽度、参与率、涨跌健康度、上涨是否普涨或整体市场健康评估。 |
| `market-environment-analysis` | `market-environment-analysis` | 综合市场环境分析与报告：覆盖美欧亚市场、外汇、大宗商品与经济指标，提供 risk-on/risk-off 评估、板块分析与技术指标解读。触发词：market analysis、global markets、trading environment、市場分析、投資環境等。 |
| `market-news-analyst` | `market-news-analyst` | 分析近期影响市场的新闻事件及其对股市和大宗商品的影响。用于分析过去 10 天重大财经新闻、货币政策决议（FOMC、ECB、BOJ）的市场反应、地缘事件对商品的影响或超大盘股财报综述；自动用 WebSearch/WebFetch 收集新闻并产出按影响排序的分析报告，分析思考与输出均为英文。 |
| `market-research-reports` | `market-research-reports` | 构建证据可追溯的市场研究报告及基于假设的市场规模测算或预测情景。覆盖市场定义、行业与客户证据、竞争格局、TAM/SAM/SOM 对账、预测敏感性及可审计的报告骨架。 |
| `market-top-detector` | `market-top-detector` | 用 O'Neil Distribution Days、Minervini Leading Stock Deterioration、Monty Defensive Sector Rotation 检测市场见顶概率，输出 0-100 综合评分与风险区间分类。用于询问市场见顶风险、派发日、防御性轮动、领涨股瓦解或是否减仓；聚焦 2-8 周战术时序信号，针对 10-20% 级别回调。 |
| `markitdown` | `markitdown` | 用 Microsoft MarkItDown 将异构文档与部分 URI 转为 Markdown，供文本分析、搜索与 LLM/RAG 摄入。覆盖安全本地转换、流式处理、Office/PDF/数据格式、批量工作流、插件、vision OCR、Azure 提取与官方 MCP server。 |
| `matchms` | `matchms` | 用 matchms 处理、清洗、比较与检索串联质谱：MS/MS 文件 I/O、元数据统一、峰过滤、谱相似度、库匹配、得分矩阵与分子相似度网络。LC-MS 特征检测或蛋白质组学流水线改用 pyopenms。 |
| `material-3` | `material-3` | 实现 Google Material Design 3（Material You）UI 体系：主用 Jetpack Compose Material3（MaterialTheme、组件、自适应布局），兼顾 Flutter 与受限 Web（@material/web，维护模式）。覆盖 token、30+ 组件、布局、主题化、M3 Expressive 与无障碍。触发词：material design、MD3、MaterialTheme、md3 button 等。 |
| `matlab` | `matlab` | 构建、审查、迁移并安全规划 MATLAB 或 GNU Octave 数值工作流，覆盖数组、表格/时间数据、测试、项目、图形、MAT 文件及显式 Python 互操作。 |
| `matplotlib` | `matplotlib` | 底层绘图库，可精细控制每个绘图元素，用于创造新图型或对接特定科学工作流，支持导出 PNG/PDF/SVG 出版。快速统计图用 seaborn，交互图用 plotly，期刊级多面板图用 scientific-visualization。 |
| `maven-dependency-audit` | `maven-dependency-audit` | 审计 Maven 依赖的过时版本、安全漏洞与冲突。触发于“check dependencies”“audit dependencies”“outdated deps”或发布前检查。 |
| `mcp-builder` | `mcp-builder` | MCP 服务器构建方法论——系统化构建生产级 MCP 工具，让 AI 助手连接外部能力。 |
| `mcp-conductor` | `mcp-conductor` | 把复杂任务分解为子任务并协调多个工具或 agent 执行。处理任务依赖图、并行执行计划、结果合并与冲突解决。适用于跨多领域的多步任务，如"抓取 5 个站点、对比数据、生成报告"或"部署应用、跑安全检查、配监控"；触发 "orchestrate"、"coordinate agents"、"run these in parallel" 等。 |
| `medchem` | `medchem` | 药物化学过滤器，用于化合物初筛：应用类药性规则（Lipinski、Veber、CNS）、结构警示目录（PAINS、NIBR、ChEMBL）、复杂度指标及 medchem 查询语言做化合物库过滤。 |
| `media-use` | `media-use` | HyperFrames 项目媒体统一入口：用 `resolve` 将 BGM、SFX、图片、图标、品牌 logo、配音、调色、LUT 解析为冻结的本地文件或即贴代码块+台账记录；目录缺失时经 TTS/音乐/图像模型生成；一个共享音频引擎产出配音、转写、字幕、去背景；支持媒体剪切/重构图/变换与跨项目资产复用。也处理模糊反馈（实拍偏暗、扁平、需复古/隐私/媒体揭示）。 |
| `migrate-to-shoehorn` | `misc/migrate-to-shoehorn` | 将测试文件中的 as 类型断言迁移到 @total-typescript/shoehorn。触发于提及 shoehorn、想替换测试中的 as、或需要部分测试数据时。 |
| `migrate-to-shoehorn` | `migrate-to-shoehorn` | 将测试文件中的 as 类型断言迁移到 @total-typescript/shoehorn。触发于提及 shoehorn、想替换测试中的 as、或需要部分测试数据时。 |
| `migration` | `migration` | 实现可回滚、兼容安全的迁移过渡：schema、数据、API、协议、配置或依赖迁移，要求具备回滚能力与数据保全证明。 |
| `minimalist-ui` | `minimalist-skill` | 极简编辑风界面设计：暖色单色调、字体排印对比、扁平 bento 网格、柔和粉彩色，不用渐变与重阴影。适用于需要干净杂志感 UI 的设计场景。 |
| `mle-workflow` | `mle-workflow` | 生产级机器学习工程工作流：数据契约、可复现训练、模型评估、部署、监控与回滚。触发：构建、评审或加固超越一次性 notebook 的 ML 系统时。 |
| `modal` | `modal` | Modal 无服务器云平台使用指南：按需运行 Python（含按需 GPU）。用于部署/服务 AI/ML 模型、GPU 训练与微调推理、Web endpoint、定时批处理任务，或用 Modal SDK 将 Python 代码弹性扩展到云端容器。 |
| `molecular-dynamics` | `molecular-dynamics` | 用 OpenMM 和 MDAnalysis 运行并分析分子动力学模拟：搭建蛋白/小分子体系、定义力场、能量最小化与生产 MD，分析轨迹（RMSD、RMSF、接触图、自由能面）。用于结构生物学、药物结合与生物物理。 |
| `molfeat` | `molfeat` | 面向机器学习的分子特征化（100+ featurizer）：ECFP、MACCS、描述符、预训练模型（ChemBERTa），将 SMILES 转为特征，服务 QSAR 与分子 ML。 |
| `motion-doctrine` | `motion-doctrine` | HyperFrames 动画/视频创作前必须最先加载的网关规则。定义高层运动法则，使多场景视频呈现为一个连续镜头而非独立幻灯片堆叠：矢量法则（退出方式决定进入方式，含 Z 轴 scale 符号规则）、载体元素、因果运动、Seam Gate 构建门禁、禁止无意义晃动（运动必须承载叙事）、高潮前静止与持续运动路线，并路由到 cut-the-curve（完整技法目录，含 waterfall entry 与 nudge curve）、oversized-cursor、seam-craft 等底层技法 skill。其规则优先于通用/上游运动指导。 |
| `motion-graphics` | `motion-graphics` | 短小、设计驱动的动态图形（motion graphic），以动效为表达核心：动态排版、数字滚动、图表数据动效、logo 演绎、字幕条/标注/社媒浮层、动画地图、动画推文/新闻标题、网页/UI 动画、实拍图片几何融入图表等。通常 10 秒内（最长约 30 秒），无旁白或实拍主体，渲染为 MP4 或透明叠加。更长/带旁白/多场景用 /general-video，不明确时用 /hyperframes。 |
| `mt5-robot-tester` | `mt5-robot-tester` | 通过命令行运行 MT5 Strategy Tester，用三轮流水线筛选尚未回测的 MetaTrader 5 EA（交易机器人）。用于批量测试 MT5 bot/EA、跨全部品种筛选、优化 EA 参数，按利润、回撤、盈利月/年数与净值曲线标准选出入围者。无头运行 terminal64.exe；运行时需 Windows + MetaTrader 5。 |
| `multi-search-engine` | `multi-search-engine` | 17 个搜索引擎集成（8 个国内 + 9 个国际），支持高级搜索运算符、时间过滤、站点搜索、隐私引擎与 WolframAlpha 知识查询，无需 API key。 |
| `music-to-video` | `music-to-video` | 将音乐曲目（音频文件、可提取音频的视频或按 mood brief 生成的曲目）转为卡点视频——歌词视频、幻灯片或动感宣传片。音乐驱动全部节奏；用户提供的图片/视频也切到同一节拍网格；零素材也能产出完整视频。解说类内容走 input-matched workflow（见 /hyperframes），不明确时也转 /hyperframes。 |
| `mysql-patterns` | `mysql-patterns` | MySQL/MariaDB 生产后端模式：schema 设计、查询、索引、事务、复制与连接池。设计 schema 与索引，或遇到查询、事务、副本延迟问题时使用。 |
| `ncats-arax` | `ncats-arax` | 查询 NCATS Translator ARAX 生产 API，获取有界、类型化、带溯源的单跳与端点固定的双跳生物医学知识图谱关系：Biolink 约束的 RTX-KG2 查询、显式选定 provider 的 ARAX 联邦、独立实体规范化、限定符感知图遍历，以及检查 TRAPI 边绑定、出版物与知识源溯源。不用于推理、排名、开放式寻路、临床建议或敏感查询。 |
| `nestjs-patterns` | `nestjs-patterns` | NestJS 架构模式：module、controller、provider、DTO 校验、guard、interceptor、config 与生产级 TypeScript 后端。构建或评审 NestJS 后端时使用。 |
| `netmiko-ssh-automation` | `netmiko-ssh-automation` | 用 Python Netmiko 安全自动化网络设备访问：只读采集、有界批量 SSH、TextFSM 解析、带防护的配置变更、超时与错误处理。适用于采集设备状态或推送受控配置变更的场景。 |
| `networkx` | `networkx` | 用 Python 的 NetworkX 创建、分析与可视化复杂网络和图。处理图数据结构、计算图算法（最短路径、中心性、聚类）、社区检测、生成合成网络（随机/无标度/小世界）、读写图文件格式或绘制网络拓扑时使用。常见应用：社交、生物、交通与引文网络。 |
| `neurokit2` | `neurokit2` | 用 NeuroKit2 构建或审计可复现的生理时间序列研究工作流：预处理、事件/区间分析、多模态对齐、变异性与复杂度。当代码 import neurokit2 或需要其当前 API、schema 及方法感知校验时触发——不用于诊断或设备验证。 |
| `neuropixels-analysis` | `neuropixels-analysis` | 用 SpikeInterface 端到端分析 Neuropixels 胞外电生理记录：加载 SpikeGLX/Open Ephys/NWB 数据、预处理、漂移/运动校正、Kilosort4（含 CPU 版）spike sorting、质量指标与 unit curation（阈值法、模型法 UnitRefine、AI 辅助视觉复核）。处理 Neuropixels 1.0/2.0 记录、spike sorting 或胞外电生理分析时使用。 |
| `news-reaction-failure-analyzer` | `news-reaction-failure-analyzer` | 判断市场是否未能对利好拥挤投机仓位的信息做出反应——Jason Shapiro COT 逆向流程第 2 步。输入 cot-contrarian-detector 报告（或明确方向）与 Claude 策展的事件 JSON，按有文档的回退链获取价格序列，用统计验证的漂移显著性检验（而非朴素失败率，避免对纯噪声误确认）产出 fail-closed 的 CONFIRMED / NOT_CONFIRMED / INSUFFICIENT_EVIDENCE 结论。可泛化用于 PEAD 与宏观拥挤的新闻失效检查。触发：检查 news-failure 确认、拥挤市场是否"无视"利好/利空，或对 CROWDED_LONG/CROWDED_SHORT 市场运行 Shapiro 第 2 步。 |
| `nextflow` | `nextflow` | 端到端构建、运行和调试 Nextflow 数据流水线与 nf-core 工作流：提及 Nextflow、nf-core、.nf、nextflow.config、DSL2、samplesheets，运行社区流水线（如 nf-core/rnaseq、nf-core/sarek），用 nf-test 编写/测试模块，配置执行器与容器（Docker、Singularity/Apptainer、Conda、Wave），扩展到 HPC/SLURM 或云，调试失败/-resume 运行。可复现科学/生信流水线工作均应使用。 |
| `nextjs-turbopack` | `nextjs-turbopack` | Next.js 16+ 与 Turbopack：增量打包、FS 缓存、开发速度，以及 Turbopack 与 webpack 的选型。 |
| `nodejs-keccak256` | `nodejs-keccak256` | 防止 JavaScript/TypeScript 中的 Ethereum 哈希错误：Node 的 sha3-256 是 NIST SHA3 而非 Ethereum Keccak-256，会静默破坏 selector、签名、storage slot 与地址推导。在 JS/TS 中做 Ethereum 哈希，或发现 selector/签名/storage slot/派生地址不对时使用。 |
| `nutrient-document-processing` | `nutrient-document-processing` | 通过 Nutrient DWS API 处理文档：转换、OCR、提取、涂黑（redact）、签名、填表，支持 PDF、DOCX、XLSX、PPTX、HTML 与图像。需要经该 API 做文档转换/OCR/提取/涂黑/签名/填表时使用。 |
| `nuxt4-patterns` | `nuxt4-patterns` | Nuxt 4 应用模式：hydration 安全、性能、route rules、懒加载，及 useFetch/useAsyncData 的 SSR 安全数据获取。用于构建或评审 Nuxt 4 应用，或排查 hydration 不匹配与数据获取问题。 |
| `obs-guardian` | `obs-guardian` | 为生产系统构建可观测性、监控、告警与事件可见性：OpenTelemetry 埋点（traces/metrics/logs）、JSON 结构化日志与关联 ID、Prometheus/Grafana 抓取配置与 recording rules、Jaeger/Tempo 分布式追踪、SLO/错误预算与 burn-rate 告警、PagerDuty/OpsGenie 告警规则及 on-call runbook 模板。触发："set up monitoring"、"add structured logging"、"no visibility into my app" 等。 |
| `office-hours` | `gstack-office-hours` | YC Office Hours，两种模式。创业模式：通过六个逼迫性问题检验需求真实性、现状、迫切具体性、最窄切入点、观察与未来适配性。Builder 模式：面向副业项目、黑客松、学习与开源的设计思维头脑风暴，并保存设计文档。当用户描述新产品想法、询问某想法是否值得做、想在写代码前探索概念或梳理设计决策时须主动调用（不要直接回答），也可在 /plan-ceo-review 或 /plan-eng-review 之前使用。触发语："brainstorm this""I have an idea""help me think through this""office hours"等。 |
| `omero-integration` | `omero-integration` | 用 omero-py、BlitzGateway、OMERO CLI 等安全检查和自动化 OMERO.server 显微镜数据工作流，覆盖 tables、annotations、ROIs、rendering 及有文档的 OMERO.web API。适用于范围化 OMERO 清点、元数据导出、导入/导出规划或受审查的写操作。 |
| `onekgpd` | `onekgpd` | 按参与者级别查询 1000 Genomes Project 数据集（3202 名全基因组测序个体，GRCh38）。触发：询问队列中的个体或变异——哪些个体携带符合基因/区域条件的变异、某位点纯合参考的个体、某变异是否存在或由指定个体携带、两个体间亲缘关系。返回 1000 Genomes AF、gnomAD v4.1 外显子/基因组 AF、AlphaMissense 评分与 HGVSp 注释。 |
| `ontology-term-resolution` | `ontology-term-resolution` | 将自由文本科学标签解析为本体 term ID，并对已有 CURIE 对照 EBI Ontology Lookup Service（OLS4）校验。用于标注组织/细胞类型/疾病/表型/试验/化学物质/物种等字段、准备 GEO/ENA/BioSamples/CELLxGENE/HCA/ISA-Tab 提交元数据、审计 term ID 表、检查 term 是否废弃及替代、跨本体映射。触发词："ontology term""CURIE""UBERON""MONDO""HPO""EFO""ChEBI""GO term" 等。 |
| `open-code-review` | `open-code-review` | 用 alibaba/open-code-review 的 `ocr` CLI 对 Git 变更做 AI 代码评审。用户要求 review 代码、PR、暂存/未暂存变更、单个 commit 或对比分支时触发；产出行级评审意见，可按需自动应用修复，配合评审规则可查出 bug、安全漏洞、性能与代码质量问题。 |
| `open-code-review-delegate` | `open-code-review-delegate` | open-code-review (OCR) 的委派模式：不由 OCR 调用 LLM 端点，而是指示宿主 agent 用自身 LLM 能力执行代码评审，OCR 仅负责确定性工程——文件选择与规则解析。触发：需要宿主 agent 主导评审时。 |
| `open-gstack-browser` | `gstack-open-gstack-browser` | 启动 GStack Browser：AI 控制的 Chromium（内置侧栏扩展），打开可见浏览器窗口实时观看每步操作，侧栏显示活动流与聊天，内置反爬隐身能力。触发 "open gstack browser"、"launch browser"、"connect chrome"、"control my browser" 等；语音别名 "show me the browser"。 |
| `open-notebook` | `open-notebook` | 自托管开源的 Google NotebookLM 替代品，用于 AI 研究与文档分析。支持将 PDF、视频、音频、网页、Office 文档组织进 notebook，生成 AI 笔记与摘要、多说话人播客、上下文感知文档对话、全文与向量检索及自定义内容转换。支持 OpenAI、Anthropic、Google、Ollama 等 16+ 提供商，自托管保证数据隐私。 |
| `openpiv` | `openpiv` | 用 OpenPIV 做粒子图像测速（PIV）分析：从 PIV 图像对提取速度场、做流体力学/流动可视化实验分析、interrogation window 互相关、校验与替换虚假 PIV 矢量、由实测速度场计算涡量、应变率与湍流统计。 |
| `openspec-apply-change` | `openspec-apply-change` | 实现 OpenSpec change 中的任务。用户想开始实现、继续实现或逐项推进任务时使用。 |
| `openspec-archive-change` | `openspec-archive-change` | 在实验性工作流中归档已完成的 change。实现完成后用户想收尾归档时使用。 |
| `openspec-bulk-archive-change` | `openspec-bulk-archive-change` | 一次性归档多个已完成的 OpenSpec 变更，用于批量归档并行变更。 |
| `openspec-continue-change` | `openspec-continue-change` | 继续推进 OpenSpec 变更，创建下一个 artifact。用于用户想推进变更进度或延续工作流时。 |
| `openspec-explore` | `openspec-explore` | 进入 explore 模式——探索想法、调查问题、澄清需求的思考伙伴。用户想在变更开始前或进行中梳理思路时使用。 |
| `openspec-ff-change` | `openspec-ff-change` | 快进式创建 OpenSpec 变更所需的全部 artifacts，跳过逐个生成的步骤。用于用户想快速备齐实施材料时。 |
| `openspec-new-change` | `openspec-new-change` | 用 OpenSpec 实验性 artifact 工作流启动新的 change。用户想以结构化分步方式创建新功能、修复或修改时使用。 |
| `openspec-onboard` | `openspec-onboard` | OpenSpec 引导式入门：带讲解走完一个完整工作流周期，并结合真实代码库实际操作。 |
| `openspec-propose` | `openspec-propose` | 一步生成 OpenSpec 变更的全部 artifacts（design、specs、tasks）。用于用户想快速描述需求并获得可直接实施的完整提案。 |
| `openspec-sync-specs` | `openspec-sync-specs` | 将变更中的 delta spec 同步到主 specs，但不归档变更。用于用户想用增量更新主 specs 时。 |
| `openspec-update-change` | `openspec-update-change` | 通过修订 OpenSpec change 的现有 planning artifacts 并保持彼此一致来更新 change。用于修订计划、纳入新决策、编辑后对齐 artifacts。从不编辑代码。 |
| `openspec-verify-change` | `openspec-verify-change` | 校验实现与 OpenSpec change 产物一致。用户想在归档前验证实现完整、正确且连贯时使用。 |
| `opentrons-integration` | `opentrons-integration` | 编写、评审、迁移、仿真和排障 Opentrons Python Protocol API v2 官方协议（Flex 与 OT-2 机器人）：液体处理、deck 与 labware 设置、移液器、模块、运行参数、液体类及 Opentrons App 分析。一个工作流需支持多厂商机器人时改用 pylabrobot。 |
| `optimize-for-gpu` | `optimize-for-gpu` | 在 NVIDIA 硬件上为科学计算 Python 提供 GPU 加速，并验证结果正确且更快。适用于 CUDA/GPU 优化；CPU 瓶颈的 NumPy、SciPy、pandas、scikit-learn、NetworkX、scikit-image、向量检索、图像处理、图计算、仿真或文件 I/O 负载；CuPy、cuDF、cuML、cuGraph、cuVS、KvikIO、Warp、Numba-CUDA、RAFT 等库问题；以及性能剖析、内存传输、kernel 或多 GPU 瓶颈排查。大数据并行 Python 代码慢且 GPU 加速可行时也可用，即使用户未提及 CUDA。 |
| `options-strategy-advisor` | `options-strategy-advisor` | 期权策略分析与模拟工具：Black-Scholes 理论定价、Greeks 计算、策略 P/L 模拟与风险管理指导。用户要求期权策略分析、covered calls、protective puts、spreads、iron condors、财报博弈或期权风险管理时使用；含波动率分析、仓位 sizing 与财报策略建议。教育定位，附实操模拟。 |
| `oversized-cursor` | `oversized-cursor` | HyperFrames 启动视频的超大 macOS 光标手法：凡涉及光标/指针主导动作、启动 UI 场景、点击引爆 morph/转场/打字连击，或场景显得静态死板、需要廉价高收益动效承载视线时加载。涵盖光标尺寸/外观（含品牌母题光标）、离屏入场法则、tip 瞄准与点击、click-ignites-next-beat、退出与跨场景交接。 |
| `pacsomatic` | `pacsomatic` | nf-core/pacsomatic 肿瘤-正常配对流程（BAM 输入）运维工具包：校验运行输入、生成合规 samplesheet、准备可复现的 Nextflow 启动产物、本地运行或提交 LSF/Slurm/PBS/SGE 调度器、排查执行失败。触发：运行 pacsomatic、准备启动脚本、dry-run 检查、排查流程启动与调度提交错误。 |
| `pair-agent` | `gstack-pair-agent` | 将远程 AI agent 配对到本地浏览器：一条命令生成 setup key 并打印连接说明，远程 agent（OpenClaw、Hermes、Codex、Cursor 等任何能发 HTTP 请求的 agent）获得独立 tab 与受限权限（默认读写，可申请 admin）。用户说 "pair agent"、"connect agent"、"share browser"、"remote browser" 等时触发。 |
| `pair-trade-screener` | `pair-trade-screener` | 统计套利工具，用于识别与分析配对交易机会。检测同行业内协整的股票对，分析价差行为、计算 z-score，为市场中性策略提供进出场建议。适用于配对交易筛选、统计套利、均值回归策略或市场中性组合构建，支持相关性分析、协整检验与价差回测。 |
| `paper-lookup` | `paper-lookup` | 检索 11 个学术 API（PubMed、Europe PMC、arXiv、OpenAlex、Crossref、Semantic Scholar、Unpaywall 等）查论文、预印本、引用与开放获取全文，返回带可复现来源的结果。触发场景：找论文、查 DOI/PMID/arXiv、摘要全文、开放获取 PDF、引用图谱、作者发表记录。 |
| `paperclip` | `paperclip` | 用 GXL 的 Paperclip CLI 搜索和阅读生物医学论文全文、FDA/PMDA/EMA 法规文件、临床试验注册库及 UniProt/PDB/ChEMBL 条目。涵盖安装并用 PAPERCLIP_API_KEY 认证 `paperclip`、/papers /fda /trials /proteins 等只读虚拟文件系统、语义搜索、全库 grep、SQL 元数据查询、map/reduce 批量阅读、图表视觉分析与带行号引用。要求安装 paperclip 或运行其 search/grep/map/reduce/sql/repo、查找文献并生成行号引用时使用。 |
| `paperzilla` | `paperzilla` | 与 agent 讨论 Paperzilla 中的项目、推荐与经典论文。适用于获取近期项目推荐、经典论文详情、markdown 摘要、推荐反馈、feed 导出或 Atom feed URL。 |
| `parabolic-short-trade-planner` | `parabolic-short-trade-planner` | 筛选美股抛物线衰竭形态并生成条件化盘前做空计划，再基于实时 5 分钟 K 线评估盘中触发。Phase 1 日线 5 因子评分（均线过度延伸/加速/成交量高潮/波幅扩张/流动性）；Phase 2 为候选股制定 ORL 破位/首根 5 分钟阴线/VWAP 失守计划，含借券/SSR/人工确认门控；Phase 3 一次性盘中 FSM 检测触发并确定具体股数。覆盖三个阶段。 |
| `parallel-web` | `parallel-web` | 用 Parallel CLI 做 Web 搜索、URL 抽取、深度研究、结构化数据富化、实体发现与周期性网页监控。适合明确需要当前网络证据、学术来源发现、重复实体查询、详尽报告或持续变更追踪的请求。 |
| `pathml` | `pathml` | 用 PathML 做本地、仅研究的计算病理工作流：加载与切片 slide、构建预处理与 QC 管线、管理 h5path 数据、定量多通道图像、构建空间图并规划有边界的模型推理。 |
| `pathogen-variant-surveillance` | `pathogen-variant-surveillance` | 通过 GenSpectrum LAPIS API 查询实时病原体基因组监测数据：当前流行毒株、增长速度与携带突变。用于依赖病原体群体当前状态而非记忆事实的问题，如 SARS-CoV-2 优势变异株、Pango 谱系指定状态、H5N1 分支/基因型、PCR 引物匹配性、谱系占比周变化等。触发词含 variant surveillance、dominant variant、Pango lineage、LAPIS、Nextclade、CoV-Spectrum 等。 |
| `pathway-enrichment` | `pathway-enrichment` | 对基因列表或排序基因数据做通路与基因集富集分析并解读。覆盖 ORA（Enrichr/Fisher/超几何）、排名型 GSEA、ssGSEA/GSVA，及 gseapy、g:Profiler、MSigDB、GO、KEGG、Reactome、WikiPathways；含基因 ID 映射、背景集选择、多重检验校正、冗余消减与出版级 dotplot/富集图。触发："pathway analysis"、"GSEA"、"GO enrichment" 等。 |
| `pdf` | `pdf` | 处理 PDF 文件的一切任务：读取/提取文本表格、合并、拆分、旋转页面、加水印、创建 PDF、填表单、加密解密、提取图片、扫描件 OCR。用户提及 .pdf 文件或要求产出 PDF 时使用。 |
| `pead-screener` | `pead-screener` | 筛选财报后跳空上涨股票的 PEAD（Post-Earnings Announcement Drift）模式：分析周线 K 线形态识别红K回调与突破信号。支持两种输入：FMP 财报日历（Mode A）或 earnings-trade-analyzer JSON 输出（Mode B）。用于 PEAD 筛选、财报跳空延续、红K突破形态、周线财报动量 setup 等查询。 |
| `peer-review` | `peer-review` | 生成证据有界、建设性的同行评审草稿与结构化稿件评估。用于获授权评审科学论文、协议、预印本或研究提案；选择报告规范、核查论断与证据、评估方法/统计/可复现性/伦理/图表/引用质量，以及规划 revision-response 回复。 |
| `pennylane` | `pennylane` | 硬件无关的量子机器学习框架，带自动微分。用于梯度训练量子线路、构建量子-经典混合模型，可跨 IBM/Google/Rigetti/IonQ 设备移植。擅长 VQE、QAOA、量子神经网络及 PyTorch/JAX 集成；硬件专属优化用 qiskit/cirq，开放量子系统用 qutip。 |
| `perf-profiler` | `perf-profiler` | 基于可复现基线和 profiler 证据分析性能问题。用于定位慢接口、慢任务、慢查询、内存或网络瓶颈、制定优化方案或验证优化收益；区分实测结论与静态推断，不虚构耗时和提升比例，生产环境操作需明确授权。 |
| `performance-smell-detection` | `performance-smell-detection` | 检测 Java 代码级性能坏味道：streams、集合、装箱、正则、对象创建。仅提供风险提示而非定论，优化前务必实测；JPA/数据库性能问题改用 jpa-patterns。 |
| `phylogenetics` | `phylogenetics` | 使用 MAFFT（多序列比对）、IQ-TREE 2（最大似然）与 FastTree（快速 NJ/ML）构建与分析系统发育树，用 ETE3 或 FigTree 可视化。适用于进化分析、微生物基因组学、病毒系统动力学、蛋白家族分析与分子钟研究。 |
| `pi-agent` | `pi-agent` | 构建和使用 Pi（极简终端编码 harness）。涵盖安装 Pi、配置 provider/model/环境变量、创建 Pi 的 skills/extensions/packages/themes/prompt 模板、通过 SDK 嵌入、RPC 或 JSON 事件流集成、解析 session、用 llama.cpp router 跑本地模型、开发自定义 provider 与 TUI 组件，以及使用生态包 pi-subagents（委派/编排）、pi-mcp-adapter（MCP server）、pi-interview（交互表单）、pi-web-access（网页搜索/抓取/视频理解）。 |
| `pipeline-architect` | `pipeline-architect` | 设计与实现数据管道：ETL/ELT、流式、批处理、schema 迁移与数仓架构。覆盖 Kafka、Airflow、dbt、Spark、ClickHouse、BigQuery、Snowflake、Redis Streams 等。用户问数据管道、ETL 作业、数据转换、流式搭建、数仓设计、CDC、schema 迁移、数据质量时使用；也触发 "build a pipeline"、"set up streaming"、"data quality is bad, help me fix it"。 |
| `pkpd-modeling` | `pkpd-modeling` | 药代动力学/药效学建模与仿真：NCA 非房室分析、房室与群体 PK（popPK）、PK/PD 与暴露-响应、TMDD、PBPK、生物等效性（RSABE/ABEL）、异速缩放与首次人体剂量（MABEL）、DDI 预测、贝叶斯治疗药物监测。用于分析浓度-时间数据、计算暴露指标、拟合 PK/PD 模型或评估给药方案；触发词含 pharmacokinetics、NCA、AUC、Cmax、NONMEM、nlmixr2、Monolix 等。 |
| `plan-canvas` | `plan-canvas` | 在本地浏览器画布打开 plan 与 HTML artifact，人工可标注元素、对话、批准或请求修改，无需离开页面。展示 plan 供评审，或"移这个改那个"类反馈用指点比打字更直观时使用。 |
| `plan-ceo-review` | `gstack-plan-ceo-review` | CEO/创始人视角的方案评审：重构问题、寻找 10 星级产品、挑战前提、在有益时扩大范围。四种模式：SCOPE EXPANSION（大胆扩展）、SELECTIVE EXPANSION（保持范围+精选扩展）、HOLD SCOPE（最大严谨）、SCOPE REDUCTION（精简到本质）。触发：用户要求 "think bigger"、"expand scope"、"strategy review"、"rethink this"、"is this ambitious enough"，或质疑方案范围/野心时主动建议。(gstack) |
| `plan-design-review` | `gstack-plan-design-review` | 设计师视角的计划评审：交互式进行（类似 CEO 与 Eng review），对每个设计维度 0-10 打分、解释如何达到 10 分，然后修订计划。工作于 plan 模式；线上站点视觉审计用 /design-review。用户有含 UI/UX 的计划需在实施前评审时使用。 |
| `plan-devex-review` | `gstack-plan-devex-review` | 交互式开发者体验（DX）计划评审。先探索开发者画像、对标竞品、设计 magic moment 并追踪摩擦点，再评分。三种模式：DX EXPANSION（竞争优势）、DX POLISH（打磨每个触点）、DX TRIAGE（仅关键缺口）。当用户有面向开发者的产品计划（API、CLI、SDK、库、平台、文档）时建议使用。触发语："DX review""developer experience audit""devex review""API design review"等。 |
| `plan-eng-review` | `gstack-plan-eng-review` | 工程经理模式评审并锁定执行计划——架构、数据流、图表、边界情况、测试覆盖、性能，交互式逐项给出明确建议。触发："review the architecture"、"engineering review"、"lock in the plan"；用户手握计划/设计文档即将开工时主动建议，在实现前发现架构问题。语音别名："tech review" 等。(gstack) |
| `plan-tune` | `gstack-plan-tune` | gstack 的自调节提问敏感度与开发者画像（v1 观察式）：回顾各 gstack skill 触发的 AskUserQuestion 提示，设置逐题偏好（never-ask / always-ask / ask-only-for-one-way），查看"声明 vs 行为"双轨画像并开关提问调优。纯对话式，无 CLI 语法。触发："tune questions"、"stop asking me that"、"show my profile" 等；用户反复遇到同一 gstack 提问或多次覆盖推荐时主动建议。 |
| `plankton-code-quality` | `plankton-code-quality` | 基于 Plankton 的写入时代码质量强制：通过 hooks 在每次文件编辑时自动格式化、lint 并用 Claude 修复。为文件编辑设置写入时格式化/lint/自动修复 hooks 时使用。 |
| `polars` | `polars` | 高性能 DataFrame 库，用于 Python ETL、数据分析与 pandas 迁移。表达式驱动的数据处理，支持惰性查询优化、并行执行、流式核外处理、Arrow 互操作与可选 GPU 执行。 |
| `polars-bio` | `polars-bio` | 在 Polars DataFrame 上做高性能基因组区间运算与生信文件 I/O：对 BED/VCF/BAM/GFF 区间执行 overlap、nearest、merge、coverage、complement、subtract。支持流式与云原生，是更快的 bioframe 替代品。 |
| `ponytail` | `ponytail` | 强制采用能工作的最懒方案——最简单、最短、最小化：先质疑任务是否该存在（YAGNI），标准库优先于自写代码、平台原生优先于依赖、一行优先于五十行。支持 lite/full/ultra 三档。用于任何编码任务（写、加、重构、修、评审、选型）；用户说 ponytail、be lazy、yagni 等，或抱怨过度设计、样板代码、多余依赖时触发；不用于非编码请求。 |
| `ponytail-audit` | `ponytail-audit` | 全仓库过度工程审计，类似 ponytail-review 但扫描整个代码库而非 diff：输出按优先级排序的清单——删什么、简化什么、换成标准库/原生等价物。触发："audit this codebase"、"audit for over-engineering"、"what can I delete from this repo"、"find bloat"、"/ponytail-audit"。一次性报告，不执行修复。 |
| `ponytail-debt` | `ponytail-debt` | 汇集代码库中所有 `ponytail:` 注释生成技术债台账，让刻意留下的简化与延后项被追踪，而不是烂尾成"以后再做"。用户说 "ponytail debt"、"/ponytail-debt"、"list the shortcuts"、"ponytail ledger" 等时触发。只输出一次性报告，不改动任何文件。 |
| `ponytail-gain` | `ponytail-gain` | 以紧凑记分板一次性展示 ponytail 的量化收益：更少代码、更低成本、更快速度，数据来自基准测试中位数。属一次性展示而非持久模式，也不是按仓库统计。触发：/ponytail-gain、ponytail gain、show ponytail impact 等。 |
| `ponytail-help` | `ponytail-help` | ponytail 全部模式、skill 与命令的速查卡片，一次性展示，非持久模式。触发：/ponytail-help、"ponytail help"、"what ponytail commands"。 |
| `ponytail-review` | `ponytail-review` | 专注过度工程的代码评审：只找该删的东西——重复造的标准库轮子、多余依赖、投机性抽象、死掉的灵活性。每条发现一行：位置、删什么、用什么替代。触发词：review for over-engineering、what can we delete、is this over-engineered、simplify review 或 /ponytail-review。与正确性评审互补，只猎复杂度。 |
| `portfolio-manager` | `portfolio-manager` | 基于 Alpaca MCP Server 拉取持仓与仓位做综合组合分析：资产配置、风险指标、个股仓位、分散度与再平衡建议。用户要求组合 review、仓位分析、风险评估、业绩评估或再平衡建议时使用。 |
| `position-sizer` | `position-sizer` | 为做多股票计算基于风险的仓位大小。适用于问仓位管理、买多少股、单笔风险、Kelly criterion、基于 ATR 的 sizing、碎股 sizing 或组合风险分配；支持止损距离计算、波动率缩放与行业集中度检查。 |
| `postgres-patterns` | `postgres-patterns` | PostgreSQL 模式：查询优化、schema 设计、索引与安全，基于 Supabase 最佳实践。设计 schema、索引或 RLS 策略，或查询过慢时使用。 |
| `ppt-master` | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑 PPTX 幻灯片、重建页面视觉、创建可复用 Brand/Style/Layout/Deck 工作区、填充原生 PPTX 模板、美化成品文件。触发于创建/重建/美化/模板化/填充 PPT、PPTX、幻灯片或课件，含添加旁白动画或生成演示视频。 |
| `pptx` | `pptx` | 任何涉及 .pptx 或 .potx 文件的任务都用它：创建 slide deck、pitch deck、演示文稿；读取、解析、提取文本（即使内容用于邮件或摘要等其他用途）；编辑修改现有演示；合并拆分 slide 文件；处理模板、layout、speaker notes、comments。用户提到 deck、slides、presentation 或相关文件名时触发。 |
| `pptx-posters` | `pptx-posters` | 基于作者批准的本地内容与素材，在无宏 PowerPoint（.pptx）中创建并审计可编辑的科学海报。交付物为 PowerPoint 研究/会议海报，且需精确的物理尺寸、打印、无障碍、来源与包安全检查时使用。 |
| `pr-address-comments` | `pr-address-comments` | 帮助处理 Gemini CLI 当前分支的 GitHub PR 评论。需要 gh CLI 工具。 |
| `pr-creator` | `pr-creator` | 创建 pull request (PR) 时使用，确保 PR 遵循仓库既定模板与规范。 |
| `pr-to-video` | `pr-to-video` | 把 GitHub pull request（PR URL、owner/repo#N 或已检出仓库中的 "this PR"）变成代码变更解说视频——基于 diff、commits 与文件构建 changelog、功能揭晓、修复或重构走读；输入是代码变更而非网站。不是产品宣传（/product-launch-video），也不是无 PR 的主题解说（/faceless-explainer）；意图不明确时用 /hyperframes。 |
| `pre-trade-discipline-gate` | `pre-trade-discipline-gate` | 手动下单前评估本地 pre-trade checklist，阻止无计划、超仓位、报复性、市场状态禁入或熔断禁入的开仓，并把决策记录到 trader-memory-core 供复盘。 |
| `prediction-alpha` | `prediction-alpha` | 分析预测市场（Polymarket、Manifold Markets、Kalshi）：计算隐含概率、检测跨平台套利、计算期望值与 Kelly 仓位比例。用户提到 prediction markets、Polymarket、Kalshi、赔率分析、套利检测、事件合约，或问「这个市场有优势吗」「当前赔率是多少」时使用。 |
| `primekg` | `primekg` | 查询精准医学知识图谱 PrimeKG，获取基因、药物、疾病、表型等多尺度生物学数据。 |
| `product-launch-video` | `product-launch-video` | 把产品或营销 URL、粘贴的脚本或 brief 转成产品发布/宣传视频——SaaS 推广、功能揭晓、产品演示、应用与公司发布。用户想营销、发布、推广或揭晓产品时使用；任何商业 URL 默认走此技能；网站游览/展示类需求也路由到这里。不明确时用 /hyperframes。 |
| `production-audit` | `production-audit` | 基于本地证据的生产就绪审计：已发布应用、上线前评审、合并后检查及"上线会坏什么"类问题，不向外部审计服务发送仓库数据。上线前、合并后审计或被问生产风险时使用。 |
| `project-flow-ops` | `project-flow-ops` | 跨 GitHub 与 Linear 运转执行流：分诊 issue 与 PR、关联进行中的工作，GitHub 保持对外公开、Linear 作为内部执行层。用户要做 backlog 控制、PR 分诊或 GitHub-to-Linear 协调时使用。 |
| `prompt-forge` | `prompt-forge` | 为 LLM 编写与优化 prompt：系统提示词、few-shot 示例、思维链结构、agent 人设与评估框架。用于写/改 system prompt、设计 few-shot、创建 agent persona、优化 prompt 性能、搭建评估体系或模板系统。触发："write a system prompt"、"prompt engineering"、"this prompt isn't working well" 等。 |
| `protocolsio-integration` | `protocolsio-integration` | 按当前官方 REST/MCP 契约读取、校验并安全导出 protocols.io 数据，或创建非执行型变更计划。内置客户端仅在显式 --execute 时对官方主机发起有界 GET 请求。仅用于明确针对 protocols.io 或精确协议版本的任务。 |
| `prototype` | `prototype` | 构建一次性原型来回答设计问题。用于验证状态模型或逻辑是否合理，或探索 UI 应该长什么样。 |
| `prototype` | `engineering/prototype` | 构建一次性原型来回答设计问题。用于验证状态模型或逻辑是否合理，或探索 UI 应该长什么样。 |
| `pufferlib` | `pufferlib` | 针对 PufferLib 强化学习的版本感知指导，覆盖环境适配、向量化、策略、PuffeRL 训练、评估与安全检查点审查。适用于将 Gymnasium/PettingZoo 环境迁移到已发布的 PufferLib 3.0.0，或使用重新设计的 4.0 原生源码线时。 |
| `pydeseq2` | `pydeseq2` | 用 PyDESeq2 做 bulk RNA-seq 差异表达分析，涵盖公式化设计、Wald 检验、FDR 校正、LFC 收缩与结果可视化。 |
| `pydicom` | `pydicom` | 用 pydicom 读取、检查、写入、转换本地 DICOM 数据集与像素数据并做安全预检。覆盖 DICOM 元数据、transfer syntax、压缩插件、frames、私有元素、JSON 及限定范围的脱敏审查。 |
| `pyhealth` | `pyhealth` | 用 PyHealth 构建临床/医疗深度学习管线：加载 EHR/信号/影像数据集（MIMIC-III/IV、eICU、OMOP、SleepEDF、ChestXray14 等），定义任务（死亡率、再入院、住院时长、用药推荐、睡眠分期、ICD 编码、EEG 事件），实例化模型（Transformer、RETAIN、SafeDrug 等）并用 PyHealth Trainer 训练、计算临床指标、做 ICD/ATC/NDC/RxNorm 编码查寻与跨映射。提到 PyHealth、MIMIC、EHR 建模或任何"数据集→任务→模型→训练→指标"模式的医疗 ML 需求即触发。 |
| `pylabrobot` | `pylabrobot` | 开发与评审 PyLabRobot 实验自动化资源、移液方案、离线模拟及支持的设备集成。用于 PyLabRobot protocol 或 API 问题；物理执行必须置于明确的操作员安全门之后。 |
| `pymatgen` | `pymatgen` | 用最新 pymatgen API 分析、校验、转换与变换材料结构及计算材料数据，含局域相图、对称性敏感性、电子结构 I/O 与显式限定范围的 Materials Project 查询。 |
| `pymc` | `pymc` | 用 PyMC 做贝叶斯建模：构建层次模型、MCMC（NUTS）采样、变分推断、LOO/WAIC 模型比较与后验检查，用于概率编程与推断。 |
| `pymoo` | `pymoo` | 多目标优化框架指导，涵盖 NSGA-II、NSGA-III、MOEA/D、Pareto 前沿、约束处理与基准测试（ZDT、DTLZ），用于工程设计与优化问题。 |
| `pyopenms` | `pyopenms` | 完整质谱分析平台，覆盖蛋白质组与代谢组工作流：feature 检测、肽/蛋白鉴定、label-free 与 isobaric 定量、加合物与精确质量注释、复杂 LC-MS/MS 流水线，支持多种文件格式与算法。简单谱图比对与小分子库匹配请用 matchms。 |
| `pysam` | `pysam` | 基于 Python/HTSlib 的基因组文件工作流。用 pysam 读取、查询、过滤或写出 SAM/BAM/CRAM、VCF/BCF、FASTA/FASTQ、tabix 数据时使用，含 pileup、覆盖度、索引与 CRAM 参考处理。 |
| `pytdc` | `pytdc` | 通过 PyTDC Python 包使用 Therapeutics Data Commons：数据集注册发现、已批准数据集访问、任务感知数据划分、评估指标、基准组以及有界的分子 oracle 工作流。 |
| `python-patterns` | `python-patterns` | Python 惯用写法、PEP 8 规范、类型提示与最佳实践。用于编写或审查 Python 代码，或讨论惯用结构、typing、PEP 8 时。 |
| `python-testing` | `python-testing` | Python 测试策略：pytest、TDD 方法论、fixtures、mocking、参数化与覆盖率要求。编写 pytest 测试（fixtures、mocks、参数化、覆盖率）时使用。 |
| `pytorch-lightning` | `pytorch-lightning` | PyTorch Lightning 深度学习框架指南：将 PyTorch 代码组织为 LightningModule，配置 Trainer 支持多 GPU/TPU，构建数据管道、callbacks 与日志（W&B、TensorBoard、MLflow），实现 DDP/FSDP/DeepSpeed 分布式训练，用于可扩展的神经网络训练。 |
| `pytorch-patterns` | `pytorch-patterns` | PyTorch 深度学习模式与最佳实践，构建稳健、高效、可复现的训练管线、模型架构与数据加载。编写或审查 PyTorch 训练循环、模型架构、数据加载，或实验无法复现时使用。 |
| `pyzotero` | `pyzotero` | 用 pyzotero Python 客户端通过 Zotero Web API v3 检索、创建、更新、删除条目、收藏、标签与附件。触发：编程方式管理 Zotero 文献库、管理参考文献、导出引用、搜索库内容、上传 PDF 附件，或构建与 Zotero 集成的科研自动化工作流。 |
| `qa` | `gstack-qa` | 对 web 应用系统性 QA 测试并修复发现的 bug：迭代修复源码，每个修复原子提交并复验。用户说 "qa"、"test this site"、"find bugs"、"test and fix"、"fix what's broken" 或问 "does this work?" 时使用。三档：Quick（仅 critical/high）、Standard（+medium）、Exhaustive（+cosmetic）；产出前后健康分、修复证据与 ship-readiness 总结。仅报告模式用 /qa-only。(gstack) |
| `qa-only` | `gstack-qa-only` | 仅报告型 QA 测试：系统化测试 Web 应用并产出含健康分、截图、复现步骤的结构化报告，但绝不修改代码。触发："just report bugs"、"qa report only"、"test but don't fix"；用户要 bug 报告而不要改动时主动建议。完整测试-修复-验证循环用 /qa。语音别名："bug report"、"just check for bugs"。(gstack) |
| `qiskit` | `qiskit` | 用 Qiskit 与 IBM Quantum Runtime 构建、模拟、transpile 并执行量子电路。用于 Qiskit 2.x 电路与算子、V2 Sampler/Estimator 原语、target-aware transpilation、本地或含噪模拟、IBM QPU 执行、Runtime session/batch、错误缓解及 Qiskit 生态包。 |
| `quantum-debugger` | `quantum-debugger` | 调试复杂难复现问题：竞态、内存泄漏、死锁、性能回退、heisenbug 与崩溃分析。用科学调试方法论——假设生成、系统测试、根因隔离。用户报间歇性崩溃、性能退化、内存泄漏、线程安全、死锁或任何难复现 bug 时使用；触发语如 "debug this"、"segfault"、"service hangs intermittently"、"works on my machine but not in production"。 |
| `quarkus-patterns` | `quarkus-patterns` | Quarkus 3.x LTS 架构模式：Camel 消息、RESTful API 设计、CDI 服务、Panache 数据访问与异步处理。构建或评审 Quarkus 服务（尤其 Camel 消息或 Panache 数据访问）的事件驱动后端时使用。 |
| `quarkus-security` | `quarkus-security` | Quarkus 安全最佳实践：认证授权、JWT/OIDC、RBAC、输入校验、CSRF、secrets 管理与依赖安全。评审 Quarkus authn/authz、JWT 或 OIDC、RBAC、校验或 secrets 时使用。 |
| `quarkus-tdd` | `quarkus-tdd` | 面向 Quarkus 3.x LTS 的测试驱动开发，使用 JUnit 5、Mockito、REST Assured、Camel testing 和 JaCoCo。添加功能、修 bug 或重构事件驱动服务时使用。 |
| `quarkus-verification` | `quarkus-verification` | Quarkus 项目验证闭环：构建、静态分析、带覆盖率的测试、安全扫描、native 编译，以及发布或 PR 前的 diff 审查。 |
| `qutip` | `qutip` | 用 QuTiP 5 模拟与审计闭/开量子系统模型，覆盖确定性演化、轨迹、稳态、谱分析与相空间工作流。适用于要求物理假设、维度与数值收敛显式化的本地量子动力学工作。 |
| `rdkit` | `rdkit` | 细粒度分子控制化学信息学工具：SMILES/SDF 解析、描述符（MW、LogP、TPSA）、分子指纹、子结构搜索、2D/3D 生成、相似度、反应。标准流程用更简单的 datamol（RDKit 封装）；需高级控制、自定义 sanitization、专用算法时用 rdkit。 |
| `react-patterns` | `react-patterns` | React 18/19 模式：hooks 纪律、Server/Client 组件边界、Suspense + error boundaries、form actions、数据获取、状态管理决策树与无障碍优先组合。用于编写或审查 React 组件。 |
| `react-performance` | `react-performance` | React 与 Next.js 性能优化模式，改编自 Vercel Engineering 的 React Best Practices。70+ 规则分 8 个优先级类别：waterfalls、bundle size、server-side、client fetching、re-render、rendering、JS 微优化、advanced。触发：编写、评审或重构 React/Next.js 代码涉及性能时。 |
| `react-testing` | `react-testing` | React 组件测试：React Testing Library、Vitest/Jest、MSW 网络模拟、axe 无障碍断言，以及组件测试与 Playwright/Cypress 端到端测试的边界。为 React 组件、hooks 或页面编写或修复测试时使用。 |
| `receiving-code-review` | `receiving-code-review` | 收到代码审查反馈后、实施建议之前使用，尤其当反馈不明确或技术上有疑问时——需要技术严谨性和验证，而非敷衍附和或盲目执行。 |
| `redesign-existing-projects` | `redesign-skill` | 将现有网站/应用升级到高端设计水准：审计当前设计、识别通用 AI 风格套路，应用高阶设计标准且不破坏功能，兼容任意 CSS 框架或原生 CSS。 |
| `redis-patterns` | `redis-patterns` | Redis 数据结构模式、缓存策略、分布式锁、限流、pub/sub 与连接管理。为生产应用添加缓存、分布式锁、限流或 pub/sub，或需审查 key 设计与连接管理时使用。 |
| `refactor-advisor` | `refactor-advisor` | 重构顾问，识别代码坏味道并提供重构方案。 |
| `relsa-severity-assessment` | `relsa-severity-assessment` | 实验动物研究的多变量严重度评估与 humane endpoint 预测：用 RELSA 分数融合体重/体温、临床或筑巢评分、生物标志物、活动、心率、burrowing 等福利指标，为每只动物每天计算单一严重度分，并用基于 ARIMA 的 foRcast 预测何时达到 humane endpoint。覆盖变量方向性、基线归一化、参考集、RELSA 权重、核密度阈值分区及 RMSE/PICP/MPIW 评估。适用于 3Rs、动物福利或 EU Directive 2010/63/EU 场景。 |
| `remotion-to-hyperframes` | `remotion-to-hyperframes` | 把现有 Remotion（React）composition 源码移植为 HyperFrames HTML。仅在明确要求 port/convert/migrate/translate Remotion 源码时使用，单向且仅限 Remotion；顺带提及 Remotion、仅参考代码或"做个类似我 Remotion 视频的东西"属于全新构建（/general-video）。不明确时转 /hyperframes。 |
| `repo-scan` | `repo-scan` | 引导安装外部 repo-scan 技能的 bootstrap 指针，从固定、可审查的 commit 安装。需在运行跨技术栈源码资产审计前先安装 repo-scan 时使用；此 ECC 指针本身不执行审计。 |
| `requesting-code-review` | `requesting-code-review` | 完成任务、实现重要功能或合并前使用，验证工作成果是否符合要求。 |
| `research` | `research` | 调研类能力：针对高可信一手来源调查问题，把发现整理成 Markdown 文件存入仓库。用户想调研主题、收集文档或 API 事实、或把阅读工作交给后台 agent 时使用。 |
| `research` | `engineering/research` | 调研类能力：针对高可信一手来源调查问题，把发现整理成 Markdown 文件存入仓库。用户想调研主题、收集文档或 API 事实、或把阅读工作交给后台 agent 时使用。 |
| `research-grants` | `research-grants` | 撰写有竞争力的科研基金申请书，覆盖 NSF、NIH、DOE、DARPA 与台湾 NSTC：机构特定格式、评审标准、预算编制、broader impacts、意义陈述、创新叙事与提交合规。 |
| `research-lookup` | `research-lookup` | 为科学手稿或研究简报汇编最新学术证据。用户明确要求收集文献、参考资料、背景证据、竞争性发现或研究资料包时使用；默认 Parallel Search，源验证用 Parallel Extract，明确要求深度工作时用 Parallel Research，Perplexity 仅在允许时作为兜底。 |
| `residual-edge-analyzer` | `residual-edge-analyzer` | 将策略收益序列分解为基准暴露与残差 alpha：基于收益的 OLS 归因、HAC 推断、滚动稳定性、替代基准敏感性与分市场状态分析。用于评估回测/实盘收益是否含市场、等权、动量、行业等因子之外的独立 alpha，或解释回撤来自基准暴露还是策略本身。不适用于持仓级 Brinson 归因或无带日期收益序列的汇总指标分析。 |
| `resolving-merge-conflicts` | `resolving-merge-conflicts` | 需要解决进行中的 git merge/rebase 冲突时使用。 |
| `resolving-merge-conflicts` | `engineering/resolving-merge-conflicts` | 需要解决进行中的 git merge/rebase 冲突时使用。 |
| `retro` | `gstack-retro` | 每周工程回顾：分析 commit 历史、工作模式与代码质量指标，带持久历史与趋势追踪。团队感知：按人拆分贡献，给出表扬与成长点。触发："weekly retro"、"what did we ship"、"engineering retrospective"；在周末或 sprint 结束时主动建议使用。(gstack) |
| `retro` | `retro` | 复盘与回顾 skill：把一次开发、排障、交付或协作过程整理成可执行的复盘结论，输出做得好的地方、问题与根因、改进动作和后续跟踪项。用户要求「复盘」「回顾这次开发」「总结问题和经验」postmortem、retrospective 等场景，或任务完成后沉淀流程改进、防止同类问题复发时使用。 |
| `review` | `gstack-review` | 合并前的 PR 评审：对照 base 分支分析 diff，检查 SQL 安全、LLM 信任边界违规、条件副作用等结构问题。被要求 review this PR、code review、pre-landing review、check my diff 时使用；即将合并代码时主动建议。 |
| `review-duplication` | `review-duplication` | 代码评审时主动排查代码库中的重复功能、重复造轮子，以及未复用项目既有最佳实践与共享工具的情况。 |
| `rowan` | `rowan` | 云原生分子建模与药物化学平台 Rowan（Python API）：pKa/macropKa 预测、构象与互变异构体系、对接与类似物对接、蛋白-配体共折叠、MSA 生成、分子动力学、渗透性与描述符工作流。适合程序化批量筛选、多步化学流水线，免维护本地 HPC/GPU。 |
| `safe-refactor` | `safe-refactor` | 在保持行为不变的前提下重构代码：提取、合并、所有权迁移或清理，且结构改动须有验证包裹。 |
| `scaffold-exercises` | `misc/scaffold-exercises` | 创建通过 lint 的练习目录结构，含 sections、problems、solutions、explainers。用于搭建练习脚手架、创建练习 stub 或新建课程章节。 |
| `scaffold-exercises` | `scaffold-exercises` | 创建通过 lint 的练习目录结构，含 sections、problems、solutions、explainers。用于搭建练习脚手架、创建练习 stub 或新建课程章节。 |
| `scanpy` | `scanpy` | 标准单细胞 RNA-seq 分析流水线：QC、归一化、降维（PCA/UMAP/t-SNE）、聚类、差异表达与可视化；并支持把 Seurat、SingleCellExperiment 等 R 友好格式转为 h5ad。适合既有工作流的探索性 scRNA-seq；深度学习用 scvi-tools，格式问题用 anndata。 |
| `scenario-analyzer` | `scenario-analyzer` | 从新闻标题做 18 个月情景分析：scenario-analyst agent 主分析，strategy-reviewer agent 给第二意见，产出英文报告，含一/二/三阶影响、推荐股票与批判性评审。示例：/scenario-analyzer "Fed raises rates by 50bp"。触发：news/scenario analysis、18 个月展望、中长期投资策略。 |
| `scholar-evaluation` | `scholar-evaluation` | 对学术成果做定性优先、证据可追溯的发展性评审，并审计低风险科研评估量表（可加本地质量控制）。不得用于人员排名或重大决策。 |
| `scientific-brainstorming` | `scientific-brainstorming` | 科学头脑风暴引导 skill：独立生成观点、结构化讨论、显式假设、透明评估、对抗性审查与决策日志。用于早期研究头脑风暴或候选研究方向排序；实证验证、研究设计、伦理或法规审查及临床问题应交给相应专家或 skill。 |
| `scientific-critical-thinking` | `scientific-critical-thinking` | 评估科学论断与证据质量：审查实验设计有效性、识别偏倚与混杂因素、应用证据分级框架（GRADE、Cochrane Risk of Bias）或教授批判性分析。正式同行评审写作请用 peer-review。 |
| `scientific-schematics` | `scientific-schematics` | 用 Nano Banana 2 AI 创建出版级科研示意图，支持智能迭代精修；用 Gemini 3.6 Flash 做质量评审，仅在质量低于当前文档类型阈值时重新生成。专注神经网络架构、系统图、流程图、生物通路与复杂科研可视化。 |
| `scientific-slides` | `scientific-slides` | 为科研演讲制作幻灯片：PowerPoint、会议演示、seminar、研究汇报、论文答辩等。提供幻灯结构、设计模板、时间分配与视觉校验，支持 PowerPoint 与 LaTeX Beamer。 |
| `scientific-visualization` | `scientific-visualization` | 用 Matplotlib、Seaborn 或 Plotly 创建并审计真实、可访问、达到出版质量的科研图表：图表设计、多面板布局、不确定性与缺失数据呈现、颜色/对比度审查、图像元数据校验与期刊导出规划。 |
| `scientific-writing` | `scientific-writing` | 起草、修订与审计科学论文或报告，带显式证据溯源、报告指南覆盖、作者署名问责、保密控制与本地一致性检查。适用于稿件章节、参考文献、声明、表格、图片或投稿准备，尤其当科学准确性与可追溯性重要时。 |
| `scikit-bio` | `scikit-bio` | 生物数据工具包：序列分析、比对、系统发育树、多样性指标（alpha/beta、UniFrac）、PCoA 排序、PERMANOVA 及 FASTA/Newick 读写，面向微生物组分析。 |
| `scikit-learn` | `scikit-learn` | Python 机器学习库 scikit-learn 的使用指导。适用于监督学习（分类、回归）、无监督学习（聚类、降维）、模型评估、超参数调优、预处理或构建 ML pipeline，提供算法、预处理技术、pipeline 与最佳实践的全面参考文档。 |
| `scikit-survival` | `scikit-survival` | 用 scikit-survival 构建、评估与审计右删失或竞争风险的生存分析工作流，包括防泄漏预处理、模型选择、概率预测与考虑删失的评估指标。 |
| `scrape` | `gstack-scrape` | 从网页拉取数据。新意图首次调用通过 $B 原语对流程做原型化并返回 JSON；匹配意图的后续调用路由到已固化的 browser-skill，约 200ms 返回。只读操作——表单、点击、提交等变更流程请用 /automate。触发：scrape、get data from、pull、extract from、what's on 等。(gstack) |
| `scvelo` | `scvelo` | 用 scVelo 做 RNA velocity 分析：由 unspliced/spliced mRNA 动力学估计细胞状态转换、推断轨迹方向、计算 latent time、识别 driver genes，适用于单细胞 RNA-seq，与 Scanpy/scVI-tools 互补。 |
| `scvi-tools` | `scvi-tools` | 面向单细胞组学的深度生成模型，用于概率式批次校正（scVI）、迁移学习、带不确定性的差异表达、多模态整合（TOTALVI、MultiVI）。适合高级建模、批次效应、多模态数据；标准分析流水线用 scanpy。 |
| `seaborn` | `seaborn` | 与 pandas 集成的统计可视化，默认样式美观，适合快速探索分布、关系与类别比较，最擅长箱线图、小提琴图、pair plot、热力图。基于 matplotlib；交互图用 plotly，出版级样式用 scientific-visualization。 |
| `seam-craft` | `seam-craft` | HyperFrames 发布视频中场景间接缝的渲染正确性规范——保证转场在 master timeline 上正确合成的先决条件。在组装 master timeline / index.html、切点或交叉淡入出现白闪（尤其暗色影片）、推理转场透明度下陷为何透出、或验证场景 wrapper 重叠混合的渲染机制时加载。涵盖不透明 stage-ground（#root 背景）白闪防护，以及 injector 的 wrapper 重叠、定格末帧、ping-pong 轨道与模板代码 stamping。不含逐个转场目录——单个转场条目见 transition registry。 |
| `search-first` | `search-first` | 先研究后编码的工作流。在编写自定义代码前先搜索现有工具、库与成熟模式，通过调用 researcher agent 完成。 |
| `sector-analyst` | `sector-analyst` | 分析板块轮动模式与市场周期定位。从 CSV 读取板块上升趋势数据（无需 API key），可选接收图表图片作补充分析。用于板块轮动分析、周期股 vs 防御股评估、超买超卖识别或市场周期阶段判断；分析与输出均为英文。 |
| `security-audit` | `security-audit` | Java 安全检查清单，覆盖 OWASP Top 10、输入校验、注入防护与安全编码，适用于 Spring、Quarkus、Jakarta EE 及原生 Java。用于代码安全审查、发布前检查或用户询问漏洞时。 |
| `security-review` | `security-review` | 实现安全相关功能时使用：新增认证、处理用户输入、操作密钥、创建 API endpoint 或实现支付/敏感功能。提供全面的安全检查清单与安全模式。 |
| `security-scan` | `security-scan` | 用 AgentShield 扫描 Claude Code 配置（.claude/ 目录）的安全漏洞、配置错误与注入风险，检查 CLAUDE.md、settings.json、MCP servers、hooks 及 agent 定义。审计 .claude/ 目录时触发。 |
| `security-sentinel` | `security-sentinel` | 执行安全审计、漏洞评估、SSL/TLS 加固、DNSSEC 配置与合规检查，覆盖 OWASP Top 10、CIS Benchmarks、邮件安全（SPF/DKIM/DMARC）与网络侦察。触发：安全审计、漏洞扫描、渗透测试、SSL 加固、"is my site secure"、"check for vulnerabilities"、"harden my server"、"set up DNSSEC" 等任何安全评估请求，含模糊表述。 |
| `setup-browser-cookies` | `gstack-setup-browser-cookies` | 把真实 Chromium 浏览器的 cookie 导入无头浏览会话，弹出交互式选择界面由用户勾选要导入的 cookie 域名。QA 测试需登录页面前使用；用户要求 import cookies、登录站点或认证浏览器时触发。(gstack) |
| `setup-deploy` | `gstack-setup-deploy` | 为 /land-and-deploy 配置部署设置：自动检测部署平台（Fly.io、Render、Vercel、Netlify、Heroku、GitHub Actions 或自定义）、生产 URL、健康检查端点与部署状态命令，并写入 CLAUDE.md 使后续部署自动化。触发："setup deploy"、"configure deployment" 等。 |
| `setup-gbrain` | `gstack-setup-gbrain` | 为当前编码 agent 配置 gbrain：安装 CLI、初始化本地 PGLite 或 Supabase brain、注册 MCP、捕获按 remote 的信任策略，一条命令从零到"gbrain 运行中且本 agent 可调用"。触发语："setup gbrain""connect gbrain""start gbrain""install gbrain""configure gbrain for this machine"。 |
| `setup-matt-pocock-skills` | `setup-matt-pocock-skills` | 为仓库配置工程技能：设置 issue tracker、triage 标签词表与领域文档布局。首次使用其他工程技能前运行一次。 |
| `setup-matt-pocock-skills` | `engineering/setup-matt-pocock-skills` | 为仓库配置工程技能：设置 issue tracker、triage 标签词表与领域文档布局。首次使用其他工程技能前运行一次。 |
| `setup-pre-commit` | `misc/setup-pre-commit` | 在当前仓库配置 Husky pre-commit 钩子，含 lint-staged（Prettier）、类型检查与测试。用户想添加 pre-commit 钩子、配置 Husky/lint-staged 或提交时格式化/类型检查/测试时使用。 |
| `setup-pre-commit` | `setup-pre-commit` | 在当前仓库配置 Husky pre-commit 钩子，含 lint-staged（Prettier）、类型检查与测试。用户想添加 pre-commit 钩子、配置 Husky/lint-staged 或提交时格式化/类型检查/测试时使用。 |
| `setup-ts-deep-modules` | `setup-ts-deep-modules` | 把 dependency-cruiser 接入 TypeScript 仓库，使每个 package 成为深模块——实现隐藏在子文件夹中，只能通过入口文件访问。用户手动调用。 |
| `setup-ts-deep-modules` | `in-progress/setup-ts-deep-modules` | 在 TypeScript 仓库接入 dependency-cruiser，使每个 package 成为深模块——实现藏在子文件夹、只能通过入口文件访问。用户手动调用。 |
| `shap` | `shap` | 用 SHAP 解释和审计机器学习预测：选择 explainer 与 masker、计算并验证特征归因、处理多输出解释、生成局部或全局 SHAP 可视化。 |
| `ship` | `gstack-ship` | 发布工作流：检测并合并基础分支、跑测试、审查 diff、bump VERSION、更新 CHANGELOG、commit、push、创建 PR。用户说 "ship"、"deploy"、"push to main"、"create a PR"、"merge and push" 等时触发；用户表示代码就绪、要部署或建 PR 时应主动调用此技能，而非直接 push/PR。 |
| `short-term-stock-picker` | `short-term-stock-picker` | 基于 AKShare 的 A 股短线选股工具。筛选条件：流通市值≤150亿、近20交易日有涨停、非 ST、沪深主板/创业板/科创板、近3日主力净流入估算、换手率≤10%。用户说"帮我选短线股""找强势股""筛选股票"或需按条件筛 A 股短线机会时触发。 |
| `signal-postmortem` | `signal-postmortem` | 记录并分析 edge pipeline 等技能所产生信号的事后交易结果：追踪假阳性、错失机会与 regime 错配，并将结论回馈到 edge-signal-aggregator 权重与技能改进 backlog。 |
| `simpy` | `simpy` | 用 SimPy 构建与检验有界过程式离散事件仿真：事件、资源、中断、监控、复现实验、预热期与可复现的输出分析。 |
| `skill-creator` | `skill-creator` | 创建新 skill、修改改进现有 skill、测量 skill 性能。用于从零创建 skill、编辑或优化现有 skill、跑 evals 测试、带方差分析的基准测试、优化描述的触发准确性。 |
| `skill-curator` | `skill-curator` | 中文 Skill 收录评估器：核验 GitHub 上的 Claude Code、Codex、Agent Skills、Plugin、MCP、CLI 或 Agent 工作流是否值得加入精选列表；检查真实资产、安装方式、活跃度、重复项与安全边界，输出分类、中文描述与可追溯证据。 |
| `skill-designer` | `skill-designer` | 从结构化 idea 规格设计新的 Claude skill。当 skill 自动生成管线需要产出一条 Claude CLI 提示、以创建符合仓库规范的完整 skill 目录（SKILL.md、references、scripts、tests）时使用。 |
| `skill-idea-miner` | `skill-idea-miner` | 从 Claude Code 会话日志挖掘 skill 创意候选。运行每周 skill 生成管线时使用，从近期编码会话中提取、评分并将新 skill 想法加入 backlog。 |
| `skill-integration-tester` | `skill-integration-tester` | 验证 CLAUDE.md 中定义的多 skill 工作流：检查 skill 存在性、skill 间数据契约（JSON schema 兼容性）、文件命名规范与交接完整性。新增工作流、修改 skill 输出或发布前验证管线健康时使用。 |
| `skillify` | `gstack-skillify` | 将最近一次成功的 /scrape 流程固化为磁盘上的永久 browser-skill，之后相同意图的 /scrape 直接运行已固化脚本（约 200ms），不再重新驱动页面。回顾对话生成 script.ts + script.test.ts + fixture，在临时目录跑测试，提交前先询问。用户说 "skillify"、"codify"、"save this scrape"、"make this permanent" 时触发。 |
| `slack-gif-creator` | `slack-gif-creator` | 创建为 Slack 优化的动画 GIF 的知识与工具集，提供约束、验证工具和动画概念。用户要求做某个 Slack 动画 GIF 时使用。 |
| `slides` | `slides` | 用 Chart.js、design tokens、响应式布局、文案公式和场景化 slide 策略创建策略型 HTML 演示。 |
| `slideshow` | `slideshow` | 用 HyperFrames 制作演示文稿/pitch deck/交互式 deck：离散分页、fragment 渐显、分支与热点导航、内置演讲者模式与讲者备注，也可把现有页面转为 deck；输出可导航 deck 而非 MP4。用户未明确要求 slideshow 时先确认。 |
| `solid-principles` | `solid-principles` | SOLID 原则清单（附 Java 示例）。类职责过多、抽象泄漏、依赖方向错误，或用户问及单一职责、开闭、里氏替换、接口隔离、依赖倒置时使用；命名、重复与方法长度问题改用 clean-code。 |
| `spec` | `gstack-spec` | 五阶段把模糊意图变成精确可执行的 spec，创建 GitHub issue，可选在全新 worktree 中拉起 Claude Code agent，合并时用 /ship 关闭源 issue。触发："spec this out"、"file an issue"、"write up a ticket"、"make this a GitHub issue"、"turn this into a backlog item"。(gstack) |
| `spring-boot-patterns` | `spring-boot-patterns` | Spring Boot 最佳实践与模式。创建 controller/service/repository，或用户问及 Spring Boot 分层、装配、配置、异常处理时使用；JPA 与 Hibernate 行为改用 jpa-patterns。 |
| `springboot-patterns` | `springboot-patterns` | Spring Boot 架构模式：REST API 设计、分层服务、数据访问、缓存、异步处理与日志。构建或审查 Spring Boot 后端（REST 层、服务层、数据访问、缓存或异步任务）时使用。 |
| `springboot-security` | `springboot-security` | Spring Security 最佳实践：认证授权、校验、CSRF、密钥管理、headers、限流与依赖安全。审查 Spring Boot 服务的 authn/authz、校验、CSRF、secrets、headers 或限流时使用。 |
| `springboot-tdd` | `springboot-tdd` | Spring Boot 测试驱动开发，使用 JUnit 5、Mockito、MockMvc、Testcontainers 与 JaCoCo。适用于新增功能、修复 bug 或重构时。 |
| `springboot-verification` | `springboot-verification` | Spring Boot 项目验证循环：构建、静态分析、带覆盖率的测试、安全扫描与 diff 评审，用于发布或 PR 前。 |
| `stable-baselines3` | `stable-baselines3` | 生产级强化学习算法（PPO、SAC、DQN、TD3、DDPG、A2C），scikit-learn 风格 API。适合标准 RL 实验、快速原型与文档完善的算法实现，最佳场景是 Gymnasium 单智能体 RL。高性能并行训练、多智能体或自定义向量化环境请用 pufferlib。 |
| `stanley-druckenmiller-investment` | `stanley-druckenmiller-investment` | Druckenmiller 策略综合器：整合 8 个上游 skill 输出（Market Breadth、Uptrend Analysis、Market Top、Macro Regime、FTD Detector、VCP Screener、Theme Detector、CANSLIM Screener）为统一确信度评分（0-100）、形态分类与资产配置建议。用户问整体市场确信度、仓位定位、配置建议或 Druckenmiller 式分析时使用。 |
| `statistical-analysis` | `statistical-analysis` | 研究数据的引导式统计分析：检验选择、假设前提检查、效应量、功效分析、贝叶斯替代与 APA 格式报告。触发：比较组间、检验假设、分析实验/问卷数据、检查统计假设、计算所需样本量或撰写结果——即使未点名具体检验。覆盖 t 检验、ANOVA、卡方、相关、回归、非参数与贝叶斯方法；底层模型 API 见 statsmodels 与 pymc skills。 |
| `statistical-power` | `statistical-power` | 研究计划的样本量与统计功效计算。凡问需要多少样本/受试者/重复、要做先验功效分析、最小可检测效应（MDE）、功效曲线，或为基金申请、IRB、预注册说明样本量时使用；覆盖 t 检验、ANOVA、比例、相关、卡方、回归的解析公式，及 logistic/Poisson 回归、混合模型、整群随机试验、生存分析等无公式设计的 Monte Carlo 模拟。仅提到效应量或 80% power 也应触发；研究设计布局用 experimental-design，已有数据分析用 statistical-analysis。 |
| `statsmodels` | `statsmodels` | Python 统计建模库：适合需要特定模型类（OLS、GLM、混合模型、ARIMA）及详细诊断、残差分析与系数推断的场景，擅长计量经济学、时间序列与严格统计推断。若需引导式检验选择与 APA 报告，用 statistical-analysis。 |
| `stitch-design-taste` | `stitch-skill` | 面向 Google Stitch 的语义设计系统 skill，生成 agent 友好的 DESIGN.md，强制高端、反模板化 UI 标准：严格字体排印、校准配色、非对称布局、持续微动效与硬件加速性能。 |
| `stock-analysis` | `stock-analysis-skill` | 股票智能分析：输入股票代码（A股/港股/美股），自动获取实时行情与历史 K 线，计算 MA/MACD/RSI/量能/乖离率等技术指标，输出 100 分制综合评分与买卖信号，搜索最新新闻做 AI 综合分析并生成决策看板。用户提供股票代码求分析或问某只股票怎么样时触发，如「分析下 TSLA PLTR」「600519怎么样」。 |
| `stock-analyst` | `stock-analyst` | 美股/港股盘前分析框架：抓取五大观测指标（VIX/IGV/MAGS/MEME/布油）、个股实时价格与期权隐含波动率，生成结构化盘前简报。包含量化模块：粒子滤波概率追踪、期权蒙卡定价、Copula VaR；支持持仓 JSON 格式管理与实时浮盈亏计算。 |
| `stockbee-20pct-study` | `stockbee-20pct-study` | 建立并维护美股每日 ±20% 涨跌幅研究：扫描异动股、分类催化与形态背景、更新后续走势、总结同类模式。用户要跑每日 20% 研究、回补历史异动、找复现优势模式或构建暴涨行情模型手册时使用。 |
| `stockbee-episodic-pivot-analyzer` | `stockbee-episodic-pivot-analyzer` | 分析 Stockbee 式 Day 1 Episodic Pivot 候选（财报、上调指引、并购、FDA/监管批准、分析师动作、大额合同、产品发布、逼空或题材事件），综合评分催化质量与跳空/量能冲击、忽视/重估背景、流动性及 EP 日低点风险。用户要 EP 候选、Day 1 催化交易或转 PEAD 监控时使用。 |
| `stockbee-exhaustion-hammer-screener` | `stockbee-exhaustion-hammer-screener` | 用 Stockbee 风格筛选美股卖出衰竭 hammer（锤形线）形态：结合前期动量、回调深度、undercut/reclaim、长下影线几何、收盘位置、成交量确认、质量/流动性门槛与风险距离打分。用户提到 Stockbee、Pradeep Bonde、exhaustion setup、hammer reversal、undercut reclaim 或在高质量机构持仓股中找回调买点时使用。 |
| `stockbee-momentum-burst-screener` | `stockbee-momentum-burst-screener` | 按 Stockbee 风格筛选美股短期 Momentum Burst setup：4% breakout、dollar breakout、range expansion、volume expansion、前区间收缩、收盘位置、failure 过滤与风险距离评分。触发词：Stockbee、Pradeep Bonde、momentum burst、4% breakout、3-5 天 burst 回顾等。 |
| `stockbee-setup-fluency-trainer` | `stockbee-setup-fluency-trainer` | 从 momentum-burst 筛选候选构建 Stockbee 风格 setup 模型手册，并回填 3 日与 5 日前瞻结果（MFE/MAE、止损命中状态、结果标签、分组统计）。用于研究 Stockbee Momentum Burst 案例、跟踪失败候选、建立 setup 熟练度、评审 A/B setup 质量，或把筛选输出转化为学习闭环而非即时交易信号。 |
| `strategic-compact` | `strategic-compact` | 在任务阶段的逻辑节点建议手动压缩上下文（compact），而非任意时点的自动压缩，以在任务各阶段间保留关键上下文。当会话接近上下文上限且当前任务阶段是自然的压缩点时使用。 |
| `strategy-pivot-designer` | `strategy-pivot-designer` | 检测回测迭代停滞，当参数调优到达局部最优时，生成结构性不同的策略转向提案。 |
| `string-reviewer` | `string-reviewer` | 评审代码库中的文本与面向用户的字符串，确保符合清晰、有用、简洁与风格规则。被要求 review 文案/字符串时使用。 |
| `subagent-driven-development` | `subagent-driven-development` | 执行包含多个独立任务的实现计划时使用，在当前会话中以 subagent 驱动方式推进。 |
| `surgical-patch` | `surgical-patch` | 在最小负责层修复 bug 与小行为变更。需要回归证明、保留周边行为和任务相关测试时使用。 |
| `sympy` | `sympy` | 需要 Python 精确符号数学时使用：代数、微积分、方程求解、符号线性代数，或经 lambdify/LaTeX 生成代码。浮点近似已足够时优先 NumPy 或 SciPy。 |
| `sync-gbrain` | `gstack-sync-gbrain` | 让 gbrain 与本仓库代码保持同步并刷新 CLAUDE.md 中的 agent 搜索指引。包装 gstack-gbrain-sync 编排器，含状态探测、原生代码面注册、能力检查与结论块，可重复执行且幂等。触发词："sync gbrain""refresh gbrain""re-index this repo""gbrain search isn't finding things"。（gstack） |
| `systematic-debugging` | `systematic-debugging` | 遇到任何 bug、测试失败或异常行为时使用，在提出修复方案之前先系统性定位根因。 |
| `talking-head-recut` | `talking-head-recut` | 为已有口播/访谈/播客视频叠加与转录同步的计时图文卡片：动态标题、下三分之一条、数据标注、引言侧栏、画中画等，可选 16:9/9:16/4:5 画布，原片画面不动。触发 "graphic overlays"、"package / dress up my video"；非普通字幕（/embedded-captions），不确定时转 /hyperframes。 |
| `tamarind` | `tamarind` | 通过 REST API 或 MCP server 使用 Tamarind Bio 平台的开源分子设计与结构生物学工具，无需本地 GPU：结构预测（AlphaFold、Boltz、Chai、ESMFold）、蛋白/binder/de novo 设计（RFdiffusion、ProteinMPNN、BoltzGen）、抗体与纳米抗体设计、分子对接（DiffDock、Autodock Vina）、亲和力预测、MSA 生成与分子动力学。提到 tamarind.bio 或需云端批量提交序列做结构/生物物理表征时使用。 |
| `tdd` | `tdd` | 测试驱动开发。用于测试先行构建功能或修复 bug、提及 red-green-refactor、或需要集成测试时。 |
| `tdd` | `engineering/tdd` | 测试驱动开发。用于测试先行构建功能或修复 bug、提及 red-green-refactor、或需要集成测试时。 |
| `tdd-workflow` | `tdd-workflow` | 写新功能、修 bug 或重构时使用，强制测试驱动开发，要求 80%+ 覆盖率，含单元、集成与 E2E 测试。 |
| `teach` | `teach` | 在当前工作区内向用户教授新技能或概念。 |
| `teach` | `productivity/teach` | 在当前工作区内向用户教授新技能或概念。 |
| `technical-analyst` | `technical-analyst` | 用于分析股票、股指、加密货币或外汇的周线图。当用户提供图表图像并要求纯基于图表数据的技术分析时使用，涵盖趋势识别、支撑/阻力位、情景推演与概率评估，不考虑新闻或基本面因素。 |
| `terminal-opener` | `terminal-opener` | 在可见终端窗口中打开可执行文件及其参数数组，提供可复用、无 shell 的启动计划，支持 dry-run、JSON、能力检测、detached 回退与独立恢复模式。当需要在新终端打开交互式 CLI、SSH 会话、本地开发进程、沙箱等 argv 命令，或诊断目标终端是否可用、给出不支持时的可行方案时使用。 |
| `terminal-ops` | `terminal-ops` | ECC 的证据优先仓库执行工作流：需要执行命令、检查仓库、调试 CI 失败或推送小修，并要求对实际执行与验证内容给出精确证据时使用。 |
| `test-driven-development` | `test-driven-development` | 实现任何功能或修复 bug 前，先写测试再写实现代码。 |
| `test-generator` | `test-generator` | 依据真实代码契约生成并验证单元测试或集成测试。用于为函数、类、接口或缺陷补测试、提高覆盖率、生成回归用例或完善测试策略；先读取现有测试与调用方，不猜测空值、异常或超时行为，不自动安装框架或访问生产依赖。 |
| `test-quality` | `test-quality` | 用 JUnit 5 加 AssertJ 断言编写高质量 Java 测试。用户说 add tests、write tests、improve test coverage，或审查/创建 Java 测试类时使用。 |
| `theme-detector` | `theme-detector` | 检测并分析各行业 trending 市场主题。用户问当前市场主题、热门板块、板块轮动、主题投资，或想识别多头/空头市场叙事并做生命周期分析时使用。 |
| `theme-factory` | `theme-factory` | 为产物（slide、docs、报告、HTML landing page 等）套用主题的样式工具包。内置 10 套预设配色/字体主题，可直接应用到已创建的产物，也可即时生成新主题。 |
| `tiledbvcf` | `tiledbvcf` | 基于 TileDB 高效存储与检索基因组变异数据：可扩展的 VCF/BCF 写入、增量添加样本、压缩存储、并行查询与导出，面向群体基因组学场景。 |
| `timesfm-forecasting` | `timesfm-forecasting` | 用 Google TimesFM 基础模型做零样本时间序列预测：任意单变量序列（销售、传感器、能源、生命体征、天气）无需训练自定义模型。支持 CSV/DataFrame/数组输入，输出点预测与预测区间；含首次使用前检查 RAM/GPU 的预检脚本。 |
| `to-questionnaire` | `to-questionnaire` | 把你无法完全回答的决策转成问卷，交给他人填写。 |
| `to-questionnaire` | `productivity/to-questionnaire` | 把你无法完全回答的决策转成问卷，交给他人填写。 |
| `to-spec` | `to-spec` | 把当前对话综合成 spec 并发布到项目 issue tracker，无需访谈，直接提炼已讨论内容。 |
| `to-spec` | `engineering/to-spec` | 将当前对话整理成 spec 并发布到项目 issue tracker——无需访谈，直接综合已讨论的内容。 |
| `to-tickets` | `to-tickets` | 把计划、规格或当前对话拆解为一组 tracer-bullet 工单，每张声明自己的阻塞依赖，发布到配置的 tracker（本地为每工单一文件的文本记录，或在真实 tracker 上用原生 blocking 链接）。 |
| `to-tickets` | `engineering/to-tickets` | 将计划、spec 或当前对话拆解为一组 tracer-bullet 工单并发布到配置的 tracker，每张工单声明其阻塞依赖——本地以每工单一文件中的文本边表示，或用真实 tracker 的原生阻塞链接。 |
| `torch-geometric` | `torch-geometric` | PyTorch Geometric（PyG）图神经网络技能：节点/边/图分类、消息传递（GCN、GAT、GraphSAGE、GIN）、异构图、邻居采样与自定义数据集。使用 torch_geometric 时触发，不适用于一般 NetworkX 分析或非图 PyTorch 模型。 |
| `torchdrug` | `torchdrug` | 构建与排障 TorchDrug 0.2.1 工作流：分子图、性质预测、自监督预训练、分子生成、逆合成、蛋白质表示学习、知识图谱推理。代码 import torchdrug 或需要其 datasets、models、tasks、Engine 时使用。 |
| `trade-hypothesis-ideator` | `trade-hypothesis-ideator` | 从市场数据、交易日志与笔记片段生成可证伪的交易策略假设，输出按优先级排序的假设卡片，附实验设计与 kill criteria，可导出兼容 edge-finder-candidate/v1 的 strategy.yaml。需有结构化输入。 |
| `trade-performance-coach` | `trade-performance-coach` | 复盘已平仓交易、部分离场与月度交易汇总，评估流程遵守、风险纪律、执行质量与有据可依的交易行为模式。在 trader-memory-core 与 signal-postmortem 产生记录后使用，或用户要求交易后教练式复盘、风险管理式评审、规则遵守评审、下次交易操作规则或心理层面的行为反馈。不提供买卖建议、心理治疗或券商执行。 |
| `trader-memory-core` | `trader-memory-core` | 全生命周期跟踪投资论点：从筛选出想法到平仓复盘。从筛选器输出注册论点、管理状态流转、附加仓位规模、审查到期日，并生成含盈亏与 MAE/MFE 分析的复盘报告。触发 "register thesis"、"thesis status"、"review due"、"close position"、"postmortem"、"trading journal"。 |
| `trading-skills-navigator` | `trading-skills-navigator` | 根据自然语言目标推荐合适的交易工作流、技能集、API 配置与上手路径。触发场景：用户表达交易/投资目标并询问从哪开始、该用哪个 skill、无付费 API key 时能做什么等（如 "where do I start"、"I want to swing trade only when the market is favorable"）。仅做路由与解释，不执行交易、不自动运行其他 skill；若尚无可用工作流会如实说明。 |
| `transformers` | `transformers` | Hugging Face Transformers 使用技能：从 Hub 加载模型、pipeline 推理、文本生成及 Trainer 微调，覆盖 NLP、视觉、音频与多模态任务。涉及 AutoModel、pipelines、tokenizers 或 TrainingArguments 时使用，不适用于 Transformers 库之外的一般机器学习。 |
| `treatment-plans` | `treatment-plans` | 在授权执业专业人员已给出并核实临床决策之后，对本地治疗计划文档做格式化与结构校验。用于来源可追溯、临床医师撰写的干预记录、目标与检查点、共同决策记录、交接与发布关卡——不用于临床决策本身。 |
| `triage` | `triage` | 让 issue 和外部 PR 走分诊角色状态机：分类、验证、必要时追问，并写出 agent-ready 简报。 |
| `triage` | `engineering/triage` | 以状态机方式推进 issue 与外部 PR 的分诊流程：分类、验证、必要时深度质询，并撰写 agent 可直接使用的简报。 |
| `tui-tester` | `tui-tester` | 用终端自动化测试 Gemini CLI 行为与视觉输出的专家指导。 |
| `ui-styling` | `ui-styling` | 用 shadcn/ui 组件（基于 Radix UI + Tailwind）、Tailwind CSS 原子化样式与 canvas 视觉设计构建美观、可访问的界面。构建 UI、实现设计系统、响应式布局、无障碍组件（对话框、下拉、表单、表格）、主题配色定制、暗黑模式、生成视觉海报或建立跨应用统一样式规范时使用。 |
| `ui-to-vue` | `ui-to-vue` | 用户有 UI 截图或设计稿导出、需批量转换为 Vue 3 组件时使用，尤其配合 Vant、Element Plus 或 Ant Design Vue。 |
| `ui-ux-pro-max` | `ui-ux-pro-max` | Web/移动/桌面 UI/UX 设计智能。设计、构建、审查或修复界面（页面、组件、设计系统、无障碍、交互、响应式布局、字体、配色、图表及各技术栈 UI 实现）时使用。内置可检索本地数据：79 种风格（50 个启用）、192 套产品配色、74 组字体搭配、119 条 UX 准则、105 个图标、17 个 GSAP 预设、25 种图表、22 个技术栈。 |
| `umap-learn` | `umap-learn` | 用 UMAP-learn 做非线性降维：2D/3D 嵌入、聚类预处理、监督或半监督 UMAP，以及 DensMAP、AlignedUMAP、Parametric UMAP 工作流。 |
| `uncertainty-and-units` | `uncertainty-and-units` | 用 pint 和 uncertainties 在科学计算中追踪物理单位并传播测量不确定度：单位换算与量纲检查、GUM 不确定度预算、A/B 类评定、扩展不确定度、Monte Carlo 传播、有效数字与±报告、曲线拟合误差传播、CODATA 常数，审计丢失单位或断裂的误差传播代码，并用 Reynolds、Peclet、Knudsen 等无量纲数做量级合理性检查。触发："is this number physically reasonable"、"sanity check these units"。 |
| `unfreeze` | `gstack-unfreeze` | 清除 /freeze 设置的冻结边界，恢复所有目录可编辑。想在不结束会话的前提下扩大编辑范围时使用；触发词："unfreeze""unlock edits""remove freeze""allow all edits"。（gstack） |
| `unified-memory` | `unified-memory` | 通过本地 ECC Memory Vault 在 Claude、Codex、Hermes、Cursor、OpenCode 等 agent 间共享持久、可检视的上下文与交接。agent 需要保存工作状态、传递上下文、恢复其他 agent 任务或搜索共享项目知识时使用。 |
| `uptrend-analyzer` | `uptrend-analyzer` | 基于 Monty's Uptrend Ratio Dashboard 数据分析市场宽度、诊断当前市场环境：由广度、板块参与、轮动、动量、历史背景 5 组件生成 0-100 综合分。询问市场宽度、uptrend ratio 或环境是否支持股票敞口时使用。无需 API key。 |
| `us-market-bubble-detector` | `us-market-bubble-detector` | 用修订版 Minsky/Kindleberger 框架 v2.1 做定量数据驱动的市场泡沫风险评估：优先客观指标（Put/Call、VIX、融资余额、市场广度、IPO 数据）而非主观印象，含严格定性调整标准与确认偏误防范，强制数据采集加机械评分，辅助实际投资决策。用户问泡沫风险、估值担忧或止盈时机时使用。 |
| `us-stock-analysis` | `us-stock-analysis` | 美股综合分析：基本面（财务指标、业务质量、估值）、技术面（指标、图表形态、支撑/阻力）、个股对比与投资报告生成。触发：用户要求分析美股代码（如 "analyze AAPL"、"compare TSLA vs NVDA"、"give me a report on Microsoft"）、评估财务指标、技术图表分析或美股投资建议。 |
| `usfiscaldata` | `usfiscaldata` | 查询 U.S. Treasury Fiscal Data REST API 获取联邦财政数据，无需 API key：国债（Debt to the Penny）、Daily/Monthly Treasury Statements、国债拍卖、利率、汇率、储蓄债券、政府收支统计。 |
| `using-git-worktrees` | `using-git-worktrees` | 需要开始与当前工作区隔离的功能开发，或在执行实现计划之前使用——通过原生工具或 git worktree 回退机制确保隔离工作区存在。 |
| `using-superpowers` | `using-superpowers` | 在任何对话开始时使用——确立如何查找和使用技能，要求在给出任何响应（包括澄清性提问）之前先调用 Skill 工具。 |
| `vaex` | `vaex` | 处理与分析超出内存的十亿行级表格数据集：Vaex 擅长 out-of-core DataFrame 操作、惰性求值、快速聚合、大数据可视化与大规模数据集上的机器学习。用于处理大型 CSV/HDF5/Arrow/Parquet 文件、海量数据快速统计、大数据可视化或内存装不下的 ML 管线。 |
| `value-dividend-screener` | `value-dividend-screener` | 美股高股息机会筛选：结合价值特征（P/E<20、P/B<2）、股息率不低于 3% 与持续增长（股息/营收/EPS 三年上行）。两阶段筛选：先用 FINVIZ Elite API 预过滤，再用 FMP API 细化分析。触发：股息股筛选、收益组合思路、基本面优质的价值股。 |
| `vcp-screener` | `vcp-screener` | 筛选 S&P 500 股票中的 Minervini 波动收缩形态（VCP），并在单只股票价格路径上检测历史 VCP。识别 Stage 2 上升趋势中形成紧密基底、波动收缩临近突破枢轴点的股票；历史单股模式遍历多年历史并输出每个 VCP 的前瞻结果统计（突破/止损/超时）。用于 VCP 筛选、Minervini 风格 setup、紧密基底、波动收缩突破候选、Stage 2 动量股扫描或特定股票历史 VCP 研究（如 FIX、TSLA）。 |
| `venue-templates` | `venue-templates` | 借助期刊/会议专属格式指南与内置 LaTeX 模板，准备期刊稿件、会议论文、研究海报与基金文档。用于选择官方模板、核查页数与匿名规则、按投稿场合调整学术写作、检查投稿 PDF。 |
| `vercel-cli-with-tokens` | `vercel-cli-with-tokens` | 用 token 认证在 Vercel 上部署和管理项目。适用于以 access token 而非交互式登录操作 Vercel CLI 的场景，如 "deploy to vercel"、"set up vercel"、为 Vercel 添加环境变量。 |
| `vercel-composition-patterns` | `composition-patterns` | 可扩展的 React 组合模式。重构布尔 prop 泛滥的组件、构建灵活组件库或设计可复用 API 时使用；涉及 compound components、render props、context providers 或组件架构的任务触发。含 React 19 API 变化。 |
| `vercel-optimize` | `vercel-optimize` | 对已部署项目做 Vercel 成本与性能优化，尤其 Next.js、SvelteKit、Nuxt 及有限支持的 Astro。先收集 metrics、用量、项目配置和代码扫描结果，只调查有指标支撑的候选项，基于已验证文件和版本感知的 Vercel/框架文档给出排序建议。用于降低 Vercel 账单、慢或贵的路由、缓存机会、Function Invocations、Build Minutes、Fast Data Transfer、Core Web Vitals、Bot Management、Fluid compute、成本分解等请求。 |
| `vercel-react-best-practices` | `react-best-practices` | 来自 Vercel Engineering 的 React 与 Next.js 性能优化准则。编写、审查或重构 React/Next.js 代码以保证最优性能模式时使用；涉及 React 组件、Next.js 页面、数据获取、bundle 优化或性能改进的任务触发。 |
| `vercel-react-native-skills` | `react-native-skills` | React Native 与 Expo 最佳实践，构建高性能移动应用。构建 RN 组件、优化列表性能、实现动画或使用原生模块时使用；涉及 React Native、Expo、移动性能、原生平台 API 的任务均触发。 |
| `vercel-react-view-transitions` | `react-view-transitions` | 用 React View Transition API（<ViewTransition> 组件、addTransitionType、CSS view transition 伪元素）实现原生流畅动画。用于页面转场、路由切换动画、共享元素动画、组件进出动画、列表重排、方向性导航动画，或在 Next.js 中集成 view transitions；不依赖第三方动画库。用户提到 startViewTransition、ViewTransition 或 React UI 状态间动画时触发。 |
| `verification-before-completion` | `verification-before-completion` | 宣称工作完成、已修复或测试通过之前使用，提交或创建 PR 之前——必须运行验证命令并确认输出后才能声称成功；始终用证据支撑断言。 |
| `verification-loop` | `verification-loop` | 面向 Claude Code 会话的综合验证系统，在声称工作完成之前验证会话产出。 |
| `verify-and-stop` | `verify-and-stop` | 只证明既有工作满足验收条件、不扩大范围。用于纯验证任务、完成度检查、聚焦的 gate 运行与最后一公里证明。 |
| `verify-chain` | `verify-chain` | 验证链——角色对抗式技术文章交叉验证。写完 IT 文章后，Critic 提取关键断言并生成核查问题，多个 Verifier SubAgent 在独立上下文联网验证，Repairer 自动修复。用于规避 AI 幻觉、知识过时、信息遗漏。 |
| `vite-patterns` | `vite-patterns` | Vite 构建工具模式：配置、插件、HMR、env 变量、proxy 设置、SSR、library mode、依赖预打包与构建优化。处理 vite.config.ts、Vite 插件或 Vite 项目时使用。 |
| `vue-patterns` | `vue-patterns` | Vue.js 3 Composition API 模式、组件架构、响应式最佳实践、Pinia 状态管理、Vue Router 导航与 Nuxt SSR 模式。Vue/Nuxt/Vite/Pinia 项目中编写或评审 Vue 3、Nuxt、Pinia 代码时激活。 |
| `wait-what` | `wait-what` | 当上一条消息未有效传达到位时，停下来重新组织表达再讲一遍。 |
| `wait-what` | `productivity/wait-what` | 中断指令：上一条回复没有说到点子上，停下来重新组织表达再说一遍。触发短语 "wait what"。 |
| `wayfinder` | `wayfinder` | 把超出单个 agent 会话容量的大型工作规划为 issue tracker 上的决策工单共享地图，逐个解决，直到通往目标的路径清晰。 |
| `wayfinder` | `engineering/wayfinder` | 将超出单个 agent 会话容量的超大工作量规划为 issue tracker 上的决策工单共享地图，逐个解决，直至通往目标的路径完全清晰。适用于大规模长期任务的拆解与推进。 |
| `waypoint-bio` | `waypoint-bio` | 用于 Outpost Bio 的开放微生物组基础模型：Waypoint 检查点（Waypoint-6m、Waypoint-45m、Waypoint-170m）、Atlas 预训练语料、Compass 八任务基准及 waypoint-bio 包的 waypoint CLI。覆盖微生物组样本嵌入、分类丰度数据微调、在 Compass 上基准测试检查点、GPT-2 预训练，以及 MetaPhlAn/Kraken2/QIIME 2/MGnify 丰度表转 waypoint 格式。 |
| `web-artifacts-builder` | `web-artifacts-builder` | 用现代前端技术（React、Tailwind CSS、shadcn/ui）构建复杂多组件 claude.ai HTML artifacts 的工具集。适用于需要状态管理、路由或 shadcn/ui 组件的复杂 artifact，不用于简单单文件 HTML/JSX。 |
| `web-design-guidelines` | `web-design-guidelines` | 按 Web Interface Guidelines 审查 UI 代码。用户要求 "review my UI""check accessibility""audit design""review UX" 或按最佳实践检查站点时使用。 |
| `web-recorder` | `web-recorder` | 把网页上的重复操作「录制」下来，之后让 AI 自动执行，如每日导出数据、每周提交报表、批量处理单据；支持 SSO 登录、API 分析、选择器验证、下载类型自动识别。触发词：录制网页、录脚本、网页自动化、RPA、帮我录等。不用于简单网页爬取（用爬虫技能）或单次网页操作（用 browser 工具）。 |
| `webapp-testing` | `webapp-testing` | 基于 Playwright 的本地 Web 应用交互与测试工具集。用于验证前端功能、调试 UI 行为、截取浏览器截图、查看浏览器日志。 |
| `weekly-performance-digest` | `weekly-performance-digest` | 从 trader-memory-core 已平仓论点生成绩效周报：胜率、期望值、profit factor、R-multiple、MAE/MFE，并按来源 skill、退出原因、论点类型、板块、机制做盈亏模式分析。无需 API，纯本地计算。 |
| `what-if-oracle` | `what-if-oracle` | 结构化 What-If 情景分析，展开 4-6 个分支可能性（最好、最可能、最坏、wild card、逆向、二阶影响）。用户就不确定的未来提假设性问题、面对战略分叉、做应急预案或决策前压力测试时使用。 |
| `wizard` | `wizard` | 生成交互式 bash 向导，引导人工完成只有人才能做的步骤。适用于基础设施开通、凭据或 CI secrets 配置、操作陌生的第三方控制台、一次性迁移或切换。agent 自己能完成的步骤不要用它。 |
| `wizard` | `engineering/wizard` | 生成交互式 bash 向导，引导人工完成只有人才能做的步骤。适用于基础设施开通、凭据或 CI secrets 配置、操作陌生的第三方控制台、一次性迁移或切换。agent 自己能完成的步骤不要用它。 |
| `workflow-runner` | `workflow-runner` | 在 Claude Code / OpenClaw / Cursor 中直接运行 agency-orchestrator YAML 工作流——无需 API key，以当前会话的 LLM 作为执行引擎。用户提供 .yaml 工作流文件或要求多角色协作完成任务时触发。 |
| `wps-excel` | `wps-excel` | WPS 表格智能助手，通过自然语言操控 Excel，解决公式编写、数据清洗、图表创建等痛点。 |
| `wps-office` | `wps-office` | WPS Office 跨应用智能助手，统一管理 Excel、Word、PPT 三大应用，处理跨应用操作与通用功能。 |
| `wps-ppt` | `wps-ppt` | WPS 演示智能助手：通过自然语言操控 PPT，解决排版美化、内容生成、动画设置等问题。 |
| `wps-word` | `wps-word` | WPS 文字智能助手，通过自然语言操控 Word 文档，解决排版、格式、内容编辑等痛点。 |
| `writing-beats` | `in-progress/writing-beats` | 写作·组装阶段：把素材编排成 beats（节拍）旅程，每个术语在被节拍依赖前先落实定义。 |
| `writing-beats` | `writing-beats` | 写作技法：将原始素材组织为由节拍（beats）推进的叙事旅程，确保每个术语在节拍依赖它之前先做铺垫解释。 |
| `writing-for-agents` | `writing-for-agents` | 为 agent 撰写文档。创建或编辑 skill、修改 AGENTS.md 或 CLAUDE.md 时使用。 |
| `writing-for-agents` | `productivity/writing-for-agents` | 为 agent 撰写文档。创建或编辑 skill、修改 AGENTS.md 或 CLAUDE.md 时使用。 |
| `writing-fragments` | `in-progress/writing-fragments` | 写作·探索阶段：挖掘原始素材片段，尚无结构。 |
| `writing-fragments` | `writing-fragments` | 写作探索阶段：挖掘原始写作片段，暂不做结构化。 |
| `writing-great-skills` | `writing-great-skills` | 编写与编辑 skill 的参考：让 skill 行为可预测所需的词汇与原则。 |
| `writing-guidelines` | `writing-guidelines` | 按 Writing Guidelines 审查文档/散文合规性。被要求 review my docs、check writing style、audit prose、review docs voice and tone，或对照写作手册检查页面时使用。 |
| `writing-plans` | `writing-plans` | 多步骤任务动工前使用：依据规格说明或需求编写实施计划，再开始写代码。 |
| `writing-shape` | `in-progress/writing-shape` | 写作·加工阶段：逐段将原始素材塑造成文章。 |
| `writing-shape` | `writing-shape` | 写作成形阶段：逐段把原始素材塑造成文章。 |
| `writing-skills` | `writing-skills` | 当创建新技能、编辑现有技能或在部署前验证技能是否有效时使用。 |
| `xlsx` | `xlsx` | 表格文件为主输入或输出的任务都用它：打开/读取/编辑/修复 .xlsx、.xlsm、.xltx、.csv、.tsv（加列、公式、格式、图表、清洗脏数据）、从零创建表格、表格格式转换。用户按名字或路径提及表格文件时触发。交付物必须是表格文件；主交付物为 Word、HTML、独立脚本、数据库管道或 Google Sheets API 集成时不触发。 |
| `zarr-python` | `zarr-python` | 面向云存储的分块 N 维数组（Zarr-Python 3）：压缩数组、并行 I/O、经 fsspec 访问 S3/GCS，兼容 NumPy/Dask/Xarray，用于大规模科学计算管线。 |
| `zh-code-reviewer` | `zh-code-reviewer` | 中文代码审查专家，生成详细的中文代码审查报告。 |
| `zh-docgen` | `zh-docgen` | 中文文档生成器——从代码库自动生成中文技术文档。 |
| `zh-readme` | `zh-readme` | 中文 README 生成器——先分析项目，再生成面向中文开发者的高质量 README。 |

## 第三部分：`agent-skills/self-skills/`（用户自写）

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`（用户自写 skill 真源）

共 **17** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `dev-paradigm-matt` | `dev-paradigm-matt` | 分层工作流路由 skill：按任务阶段把需求澄清、规格设计、架构规划、实现、调试、审查、交接和长期维护路由到合适的 matt-skills，而非所有任务走同一条流水线。适用于「这个需求该怎么推进」「该先 grill 还是 to-spec」「Bug/重构/新功能分别怎么走」、接手陌生项目、setup、领域建模、票据拆分等场景的统一入口。 |
| `easy-crawler` | `easy-crawler` | 可独立部署的网页抓取 skill，统一覆盖通用网页抓取、社媒平台专项优化及反爬/浏览器自动化。用户提到抓网页、列表页/详情页、社媒搜索/评论/创作者主页，或需浏览器自动化、代理、登录态复用、反爬边界说明时触发。输出统一任务契约、可观测结果与显式失败，不把未实现的平台逆向能力伪装成已支持。 |
| `mac-safe-storage-cleaner` | `mac-safe-storage-cleaner` | 安全检查并清理本机 macOS 的缓存、日志、临时文件、下载目录安装包及受控的 Workspace 历史目录。用户提到清理系统缓存/日志、清理 Workspace 占用、磁盘空间不足、删除临时文件、清理 Downloads/IDEA 日志、分析磁盘占用时触发；支持复查清理规则、验证保护目录、确认是否会误删，按"先分析、再确认、最后决定是否删除"的交互流程执行。 |
| `opsx-workflow-hooks` | `opsx-workflow-hooks` | opsx 工作流的后置命令钩子。触发 A：/opsx/propose 生成全部 artifacts 后进入迭代打磨循环，询问用户新想法并更新提案直到满意，非平凡分析用全新 sub agent。触发 B：/opsx/apply 达到实现完成交接后，在用户人工验证（SIT/UAT）前运行 review/test/verification、修复关键问题，全部任务真正完成才归档。普通实现中暂停不触发。 |
| `robot-aiot-adr-confluence` | `robot-aiot-adr-confluence` | 技术方案文档端到端工作流：信息评估 → 需求收敛、追问澄清、方案比较 → 生成 ADR、技术提案或决策简报，需要时发布到 Confluence。适用于「写技术方案」「生成 ADR」「架构决策记录发 Confluence」「技术选型文档输出」等场景。只要文档可停在 Markdown 草稿，明确要求发布才进 Confluence 阶段。 |
| `robot-aiot-adr-generator` | `robot-aiot-adr-generator` | 生成并校验 ADR 架构决策记录：先按业务/技术需求产出标准 ADR 文档，再按需对可外部验证的关键技术断言执行验证链核查。适用于"生成 ADR""写架构决策记录""输出技术选型归档""ADR 发布前审稿"等场景，输出服务技术决策归档而非通用技术文章。 |
| `robot-aiot-arch-diagram` | `robot-aiot-arch-diagram` | 架构图/技术可视化绘制能力。两条输出路径：直绘 SVG/HTML（主路径，编辑级设计系统+工程制图管线，含几何校验与构图契约）、archify 运行时渲染（主题切换+导出）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑等 40+ 图表类型；内置 12 套 SVG 风格皮肤与品牌 token 定制、PNG/GIF 导出，支持 drawio/Mermaid/Excalidraw 导入重绘与 .excalidraw/SVG/PNG 三件套离线导出，含数据统计图表绘制规则、深色主题直绘与出版级迭代流程。非 PPT 场景专用。触发：绘制架构图/技术可视化。 |
| `robot-aiot-bash-code-review` | `robot-aiot-bash-code-review` | 审查 skill 文档（.md）中 bash 代码块的语法、功能正确性与模式匹配准确性。创建或更新含 bash 代码块的 skill、要求验证文档 bash 代码、编辑涉及 bash 块的 skill 文档后触发。触发词：review bash、verify code blocks、bash 验证、代码块审查。 |
| `robot-aiot-commit` | `robot-aiot-commit` | 为本项目生成统一格式的中文提交说明，用户明确要求时执行 Git commit。适用于「生成 commit message」「按规范提交」「总结 diff」「按 FEAT/FIX/ENH/DOC/CHORE 分类提交」「根据分支提取 JIRA」等场景，遵循本项目提交规范而非通用 Conventional Commits 模板。 |
| `robot-aiot-docs-sync` | `robot-aiot-docs-sync` | 扫描项目并创建或更新可溯源文档：AGENTS.md、README.md、CHANGELOG.md、docs/project-map.md、docs/architecture.md。适用于「更新项目文档」「同步文档」「生成 changelog」「生成项目地图」等场景，仅对这 5 个文件做结构化增强，不修改源代码、配置或测试。 |
| `robot-aiot-draw-flowchart` | `robot-aiot-draw-flowchart` | 机器人/IoT 业务图表绘制与页面化能力：draw.io XML 图表生成（可编辑主路径）+ XML→HTML 稳定桥接转换 + 领导汇报静态页面 HTML（1920x1080 画布）。覆盖流程图、分层架构、时序、状态机、ER、UML 类/用例、网络拓扑等 39+ 图表类型；内置机器人视觉语言、配色与样式一致性体系、几何/构图校验，PNG/GIF 导出与 drawio/Mermaid 导入重绘，支持 Mermaid 源码写作与 .excalidraw/SVG/PNG 三件套离线导出、数据统计图表绘制、深色主题直绘与出版级迭代流程。 |
| `robot-aiot-interactive-html-author` | `robot-aiot-interactive-html-author` | 交互式动画特效 HTML 编写能力。纯原生零依赖产出浏览器可直接运行的交互页面/多页 deck：翻页系统（键盘+点击+触摸滑动+View Transition+#/N 深链）、演讲者模式（S 键弹窗：像素级预览+提词+计时器，双窗口同步）、总览网格（O 键）、话术抽屉（N 键）、元素入场、数据动效（数字滚动/进度条填充/图表逐步绘制）、交互图表、关键帧动画与动效接缝、扩展特效目录（27 种 CSS 入场动画 + 20 种 canvas FX，仅明确要求时启用）、Mermaid/PlantUML 构建期渲染嵌入（headless Chrome→PNG/SVG，失败降级不静默丢图）、自包含单文件构建与交付前审查。用户要求写交互动画页、加翻页/动画/动效、演讲者模式/提词器/双屏演示，或 robot-aiot-web-presentation-workflow 委派 Phase 4 编写时触发。 |
| `robot-aiot-knowledge-expert` | `robot-aiot-knowledge-expert` | 物联网全栈技术专家回答规范。用户问 IoT/AIOT 架构设计、协议选型、平台集成、边云协同、性能调优、故障排查时使用。触发词：物联网、IoT、MQTT、Modbus、BACnet、OPC UA、EMQX、物模型、边云协同、设备影子、OTA、JetLinks、ThingsBoard、感认行。 |
| `robot-aiot-leadership-ppt-workflow` | `robot-aiot-leadership-ppt-workflow` | 把项目数据和技术分析转化为领导汇报 PPT，五阶段全链路：数据池建立 → 技术明细版加目标受众汇报版文档分层 → 调用 robot-aiot-draw-flowchart 生成分层架构图/流程图 XML 并完成 XML→HTML 桥接 → 调用 ppt-master 生成最终 PPTX。用户要求「写领导汇报PPT」「出PPT母稿」「做汇报材料」时触发。受众由用户指定，默认领导层。 |
| `robot-aiot-self-skill-sync` | `robot-aiot-self-skill-sync` | 批量更新 self 目录下所有 git 项目并同步 skills 的五模块工作流：统一更新 npx 管理型外部 skill（失败按 self/skills/ 本地克隆 rsync 兜底）、OpenSpec profile 升级并将 opsx/ 命令与 openspec-* skills 同步到 ~/.agents、self-skills/ 与 ~/.agents/skills/ 及 commands/ 按内容+mtime 文件级双向同步（严禁旧覆盖新）、~/.agents/skills/ 全量同步到知识库 agent-skills/skills/（不加 --delete）、最后更新 docs/skills-overview.md。核心原则：只允许新增和修改，禁止删除与 git push；self-skills/ 是自写 skill 唯一真源，禁止从非运行时来源写入。触发词：更新self、同步skills、更新skills、拉取self 等。 |
| `robot-aiot-web-presentation-workflow` | `robot-aiot-web-presentation-workflow` | 交互式 Web 演示页面制作工作流：根据知识文档生成分页汇报母稿，按需制作架构图/流程图，逐页交互 HTML（可翻页、带动画、数据动效，纯原生零依赖双击即用）委派 robot-aiot-interactive-html-author 编写。触发于“做交互演示”“生成Web演示”“做动态汇报”“可翻页演示”“带动画的汇报”“Web版汇报”，或将技术项目数据转化为可交互浏览器演示的场景。 |
| `stock-replay-workbench` | `stock-replay-workbench` | A 股盘后复盘工作台。当用户要求收盘简报、主线题材梳理、强势股/观察池、个股走强原因、题材与资金联动、龙虎榜/公告/研报/财务交叉分析，或简单行情查询需扩展为带任务路由、来源优先级、时间戳、警告与分层结论的结构化流程时触发。覆盖打板情绪（涨停/炸板/跌停/昨涨停四池+连板分析+涨停揭秘）、ETF 期权（T型报价+希腊字母+IV）、舆情互动（热榜/人气榜/互动易）；多股对比经 sub-agent 并行编排，深度报告强制经 cross-check-reviewer 二次校对。 |
