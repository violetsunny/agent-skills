# `~/.agents/skills/` 技能总览

本文档根据 `~/.agents/skills/*/SKILL.md` 的名称、描述和触发条件整理，覆盖当前安装的 127 个技能。技能名称是实际调用时使用的标识；用途是便于选型的简要摘要，具体规则以对应 `SKILL.md` 为准。

## 快速选型

| 工作类型 | 优先考虑的技能 |
| --- | --- |
| OpenSpec 变更规划与实施 | `openspec-propose`、`openspec-apply-change`、`openspec-verify-change`、`openspec-archive-change` |
| Java/Spring 后端 | `spring-boot-patterns`、`java-code-review`、`jpa-patterns`、`test-quality` |
| Python/通用代码 | `clean-code`、`code-review`、`tdd`、`systematic-debugging` |
| HTML/CSS/Vue/前端 | `ui-ux-pro-max`、`frontend-design`、`webapp-testing`、`ui-styling` |
| 技术方案和文档 | `doc-coauthoring`、`writing-plans`、`domain-modeling`、`chinese-documentation` |
| 测试和验证 | `tdd`、`test-driven-development`、`test-quality`、`verification-before-completion` |
| 物联网/机器人 | `robot-aiot-knowledge-expert`、`robot-aiot-draw-flowchart`、`robot-aiot-docs-sync` |
| PPT、图表和视觉材料 | `ppt-master`、`pptx`、`slides`、`theme-factory`、`design` |
| 调试和故障排查 | `systematic-debugging`、`diagnosing-bugs`、`quantum-debugger` |

## OpenSpec 与工作流

| 技能 | 主要用途 |
| --- | --- |
| `openspec-propose` | 一次性创建 OpenSpec 变更及 proposal、spec、design、tasks 等规划产物。 |
| `openspec-new-change` | 创建新的 OpenSpec 变更骨架。 |
| `openspec-continue-change` | 继续 OpenSpec 变更并生成下一个规划产物。 |
| `openspec-ff-change` | 快速生成实现所需的全部 OpenSpec 产物。 |
| `openspec-explore` | 在正式建变更前探索想法、问题和需求。 |
| `openspec-update-change` | 更新并协调已有变更的规划文档，不修改代码。 |
| `openspec-apply-change` | 按 OpenSpec tasks 执行实现。 |
| `openspec-verify-change` | 验证实现是否符合变更文档。 |
| `openspec-archive-change` | 归档已完成的 OpenSpec 变更。 |
| `openspec-bulk-archive-change` | 批量归档多个已完成变更。 |
| `openspec-sync-specs` | 将变更中的 delta spec 同步到主 spec。 |
| `openspec-onboard` | 引导完成 OpenSpec 全流程。 |
| `opsx-workflow-hooks` | 在 propose/apply 完成后自动执行方案迭代、技能增强、测试审查、UI/UX 审查和归档流程。 |

## Java、后端与代码质量

| 技能 | 主要用途 |
| --- | --- |
| `spring-boot-patterns` | Spring Boot 的 Controller、Service、Repository、REST、异常和 JPA 设计。 |
| `java-code-review` | Java 空安全、异常、并发、性能和结构化代码审查。 |
| `architecture-review` | Java 项目模块边界、分层、包结构和依赖方向审查。 |
| `jpa-patterns` | JPA/Hibernate 的 N+1、懒加载、事务、查询和实体关系问题。 |
| `concurrency-review` | Java 并发、竞态、死锁、虚拟线程、CompletableFuture 和异步代码审查。 |
| `security-audit` | Java/Spring/Quarkus/Jakarta 的 OWASP、输入校验和安全编码审计。 |
| `performance-smell-detection` | Java 集合、Stream、装箱、正则和对象创建等性能异味识别。 |
| `maven-dependency-audit` | Maven 依赖过期、漏洞、冲突和版本审计。 |
| `logging-patterns` | Java SLF4J、结构化 JSON 日志和 MDC 链路追踪规范。 |
| `java-migration` | Java 8/11/17/21/25 版本升级和迁移。 |
| `design-patterns` | Factory、Builder、Strategy、Observer、Decorator 等设计模式。 |
| `solid-principles` | SOLID 原则和 Java 类设计审查。 |
| `clean-code` | DRY、KISS、YAGNI、命名、函数设计和重构。 |
| `codebase-design` | 深模块、接口边界、测试 seam 和可维护模块设计。 |
| `improve-codebase-architecture` | 扫描代码库寻找架构深化机会，并生成可视化 HTML 报告。 |
| `code-review` | 按规范和需求双轴审查分支、PR 或工作区变更。 |
| `chinese-code-review` | 中文代码 Review 话术、分级和常见反模式沟通。 |
| `git-commit` | Java 项目的 Conventional Commit 信息生成。 |
| `chinese-commit-conventions` | 中文 commit、commitlint、husky 和 changelog 约定。 |
| `changelog-generator` | 根据 Git 提交生成或更新 changelog。 |

## 测试、调试与交付验证

| 技能 | 主要用途 |
| --- | --- |
| `tdd` | 红-绿-重构、行为测试、测试 seam 和测试反模式。 |
| `test-driven-development` | 实现功能或修复 Bug 前先写失败测试，再做最小实现。 |
| `test-quality` | Java JUnit 5、AssertJ、AAA 结构和可维护测试。 |
| `verification-before-completion` | 在宣称完成、通过、提交或合并前提供新鲜验证证据。 |
| `systematic-debugging` | 按证据、复现、定位、验证和回归流程排查问题。 |
| `diagnosing-bugs` | 复杂 Bug 和性能回退的诊断循环。 |
| `quantum-debugger` | 深层次、非确定性或复杂系统故障调试。 |
| `requesting-code-review` | 完成任务或合并前请求代码审查。 |
| `receiving-code-review` | 严谨分析并处理代码审查反馈。 |
| `finishing-a-development-branch` | 实现完成且测试通过后决定合并、提交或收尾方式。 |
| `executing-plans` | 按已有实现计划分阶段执行并设置检查点。 |
| `implement` | 根据 spec 或 tickets 执行一项工作。 |
| `using-git-worktrees` | 为隔离开发创建并管理 Git worktree。 |
| `resolving-merge-conflicts` | 处理 Git merge/rebase 冲突。 |
| `subagent-driven-development` | 将独立实现任务交给并行子代理执行。 |
| `dispatching-parallel-agents` | 分派两个或以上可并行的独立任务。 |

## 前端、UI/UX 与视觉设计

| 技能 | 主要用途 |
| --- | --- |
| `ui-ux-pro-max` | UI/UX、无障碍、交互、响应式、排版、颜色和组件设计审查。 |
| `frontend-design` | 构建具有明确视觉方向、排版和个性的前端界面。 |
| `ui-styling` | shadcn/ui、Radix、Tailwind、响应式和无障碍组件样式。 |
| `web-artifacts-builder` | 构建复杂多组件 HTML/React/Tailwind/shadcn Web artifact。 |
| `webapp-testing` | 使用 Playwright 对浏览器端行为做自动化验证。 |
| `design-system` | 设计 token、组件规格、CSS 变量、间距和排版系统。 |
| `theme-factory` | 为幻灯片、文档、报告和 HTML artifact 应用主题。 |
| `design` | 品牌、设计 token、Logo、图标、HTML 演示和视觉资产。 |
| `brand` | 品牌声音、视觉识别、营销信息和品牌一致性。 |
| `brand-guidelines` | 应用 Anthropic 官方品牌颜色和字体规范。 |
| `banner-design` | 社交媒体、广告、网站 Hero 和印刷 Banner 设计。 |
| `canvas-design` | 使用设计原则生成 PNG/PDF 静态视觉艺术。 |
| `algorithmic-art` | 使用 p5.js 和随机种子创建算法艺术、粒子和流场。 |
| `slack-gif-creator` | 创建符合 Slack 约束的动画 GIF。 |

## 文档、方案、研究与沟通

| 技能 | 主要用途 |
| --- | --- |
| `doc-coauthoring` | 通过上下文收集、结构迭代和读者测试共同编写文档。 |
| `writing-plans` | 在修改代码前根据 spec 或需求编写多步实施计划。 |
| `writing-for-agents` | 编写 skill、AGENTS.md、CLAUDE.md 等供 Agent 使用的文档。 |
| `writing-skills` | 创建、编辑和验证技能文件。 |
| `writing-great-skills` | 技能触发、结构、指令和可预测性写作参考。 |
| `chinese-documentation` | 中文技术文档中英文空格、标点、术语和排版规范。 |
| `internal-comms` | 状态报告、领导汇报、3P、FAQ、事故和项目沟通材料。 |
| `research` | 基于高可信一手资料研究并写入 Markdown。 |
| `deep-research` | 多代理深度研究、文献综述、事实核查和证据综合。 |
| `prompt-forge` | 设计和优化系统提示词、Agent 人设、few-shot 和提示词评测。 |
| `domain-modeling` | 梳理项目领域模型、术语、CONTEXT.md 和 ADR。 |
| `grill-me` | 通过高强度提问打磨方案或设计。 |
| `grill-with-docs` | 通过提问打磨方案并同步生成 ADR 和术语表。 |
| `grilling` | 压力测试计划、决策或想法。 |
| `humanizer-zh` | 改善中文表达，降低机械化和 AI 腔。 |
| `teach` | 在当前工作区内讲解技能或技术概念。 |
| `to-questionnaire` | 将无法直接回答的决策整理成问卷。 |
| `to-spec` | 将当前对话整理成 spec 并发布到项目 issue tracker。 |
| `to-tickets` | 将计划或 spec 拆成带依赖边的 tracer-bullet tickets。 |
| `handoff` | 将当前会话压缩成便于其他 Agent 接手的交接文档。 |
| `wayfinder` | 将超出单次会话的大型工作拆成共享决策地图和 tickets。 |
| `prediction-alpha` | 预测和分析类任务的专业工作流。 |

## API、数据、基础设施与平台

| 技能 | 主要用途 |
| --- | --- |
| `api-sculptor` | 设计和实现 REST、GraphQL、gRPC、WebSocket API 及其契约。 |
| `api-contract-review` | 审查 REST HTTP 语义、版本兼容和响应一致性。 |
| `archify` | 生成架构、流程、时序、数据流和生命周期图，并输出可交互 HTML。 |
| `auth-architect` | 设计 OAuth2/OIDC、JWT、SSO、MFA、RBAC/ABAC 和 API Key 身份认证体系。 |
| `chinese-git-workflow` | Gitee、Coding、GitLab、CNB 的 SSH/HTTPS、凭据、CI 和镜像同步配置。 |
| `ghost-scraper` | 抓取静态或动态网站数据，识别分页、API 和反爬限制。 |
| `pipeline-architect` | 设计 ETL/ELT、流式、批处理、数据仓库和 CDC 管道。 |
| `infra-automation` | 基础设施自动化、环境编排和运维脚本。 |
| `deploy-ninja` | 部署、发布和上线相关工作流。 |
| `db-whisperer` | 数据库问题分析、查询和数据访问协助。 |
| `mcp-builder` | 构建高质量 MCP Server，支持 Python FastMCP 和 Node/TypeScript SDK。 |
| `mcp-conductor` | MCP 服务编排和多工具协同。 |
| `obs-guardian` | 可观测性、日志、指标、链路和告警治理。 |
| `security-sentinel` | 通用安全风险识别和安全防护审查。 |
| `workflow-runner` | 在 Claude Code、OpenClaw 或 Cursor 中执行 YAML 多角色工作流。 |
| `wizard` | 生成只引导人执行的 Bash 配置、凭据、CI 或切换向导。 |
| `harness-spec` | 设计 harness、专业 Agent、元技能及同步运维体系。 |
| `setup-matt-pocock-skills` | 初始化工程技能仓库的 issue tracker、标签和文档布局。 |
| `issue-triage` | GitHub issue 优先级分类和维护。 |
| `triage` | 按状态机流转 issue 和外部 PR，并产出 Agent brief。 |

## IoT、机器人与企业文档

| 技能 | 主要用途 |
| --- | --- |
| `robot-aiot-knowledge-expert` | IoT/AIOT 协议、边云、平台、物模型和性能问题专家回答。 |
| `robot-aiot-draw-flowchart` | 生成机器人/IoT 流程图、架构图和 draw.io XML。 |
| `robot-aiot-leadership-ppt-workflow` | 将 IoT 项目数据转成领导汇报文档、架构图和 PPT。 |
| `robot-aiot-docs-sync` | 机器人/IoT 项目文档同步和一致性维护。 |
| `robot-aiot-adr-confluence` | 机器人/IoT ADR 和 Confluence 技术决策文档。 |
| `robot-aiot-xml-html-bridge` | 将 draw.io XML 稳定转换为保留样式的 HTML。 |
| `robot-aiot-self-skill-sync` | 更新 self 下项目并同步技能、OpenSpec 和个人知识库。 |
| `stock-replay-workbench` | A 股盘后复盘、题材、资金、龙虎榜、ETF 期权和舆情分析。 |

## PPT、文件与数据资产

| 技能 | 主要用途 |
| --- | --- |
| `ppt-master` | 创建、重构、填充和增强可编辑 PPTX/PPT 演示文稿。 |
| `pptx` | 处理任意 PPTX/POTX 的创建、读取、编辑和转换。 |
| `slides` | 创建带 Chart.js、设计 token 和响应式布局的 HTML 演示。 |
| `pdf` | 读取、提取、合并、拆分、OCR、加水印和加密 PDF。 |
| `docx` | 创建、读取、编辑 Word 文档和模板。 |
| `xlsx` | 创建、读取、清洗和分析 Excel/CSV/TSV 表格。 |

## 技能管理、协作与通用辅助

| 技能 | 主要用途 |
| --- | --- |
| `skill-creator` | 创建、修改、优化技能并运行 eval/benchmark。 |
| `using-superpowers` | 会话开始时查找并调用合适技能。 |
| `ask-matt` | 根据问题在技能和工作流之间做路由。 |
| `brainstorming` | 创意、功能和行为修改前探索意图与需求。 |
| `prototype` | 创建一次性原型验证状态模型或设计问题。 |
| `cavecrew` | Cavecrew 相关协作工作流。 |
| `caveman` | Caveman 相关简化协作工作流。 |
| `wait-what` | 发现上一条消息未被正确理解时重新表述。 |

## 维护说明

- 本文档是用途索引，不替代具体技能文件；使用前应加载对应 `SKILL.md`。
- 技能描述和安装集合可能变化，建议在技能同步后重新生成本表。
- 部分技能的 frontmatter 描述为空或不完整，本文档根据技能名称和目录用途做了最小化概括。
