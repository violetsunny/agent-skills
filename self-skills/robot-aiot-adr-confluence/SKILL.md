---
name: robot-aiot-adr-confluence
description: >
  技术方案文档端到端工作流：先做信息评估，再按需做需求收敛、追问澄清和方案比较，
  最后生成 ADR、技术提案或决策简报，并在需要时发布到 Confluence。
  适用于“写技术方案”“生成 ADR”“输出技术提案”“写决策简报”“架构决策记录发 Confluence”
  “方案归档到 Confluence”“技术选型文档输出”等场景。
  如用户只要文档，可停在 Markdown 草稿；如用户明确要求发布，再进入 Confluence 发布阶段。
---

# ADR-Confluence-Flow

将模糊方案收敛成结构化文档，并在需要时发布到 Confluence。

## 核心定位

本技能整合了四类能力：

1. 决策准备：需求收敛、逐轮追问、方案发散
2. 文档成文：ADR 标准、技术提案、简报三类模板
3. 发布前质量控制：架构评审、验证链核查、模板校验、格式校验
4. 发布执行：在本地存在发布脚本时推送到 Confluence

说明：

1. `to-spec`、`grilling`、`brainstorming`、`architecture-review` 是可借用的上游能力
2. 当目标文档是 ADR 时，优先按 `robot-aiot-adr-generator` 的规则生成和核查；技术提案与简报仍由本 skill 自带模板完成
3. Confluence 发布依赖本地可用的 `confluence-cli` 脚本；没有脚本时只输出 Markdown，不报错硬失败

## 工作流总览

```text
信息评估
→ 决策准备（按需：需求收敛 / 追问 / 方案发散）
→ 模板选择
→ 文档生成
→ 架构评审
→ 验证链核查（按需）
→ 合规校验
→ Confluence 发布（仅用户要求且环境就绪时）
```

## Phase 0: 信息评估

信息评估、最低输入要求、模板阻塞项和“直接生成”规则见 `references/intake-and-routing.md`。

主文件只保留关键判断：

1. 文档生成和 Confluence 发布的阻塞信息不同，不能混为一谈
2. 用户要求“直接生成”时可跳过追问，但缺口必须显式标注为 `[待补充]`
3. 对 ADR 和简报，若连推荐方案都没有，只能输出草稿，不能宣称已定稿

## Phase 1: 决策准备

追问、事实查找、需求收敛和方案发散见 `references/discovery-and-decision-shaping.md`。

入口原则：

1. 能从代码、配置、环境中查到的事实，优先自行获取
2. 只把收敛后的结论写入最终文档，不把中间推演过程整段复制进去
3. 用户可随时跳过追问，但不能因此掩盖信息缺口

## Phase 2-4: 生成、评审、验证、校验

模板选择、生成要求、架构评审和通用格式校验见 `references/generation-and-review.md`。

模板文件：

1. `references/adr-standard-template.md`
2. `references/tech-proposal-template.md`
3. `references/brief-template.md`

ADR 优先入口：

1. 用户要 ADR 时，优先复用 `robot-aiot-adr-generator` 的输入约束、生成顺序和验证链核查逻辑
2. 只有在当前上下文明确要求继续走 Confluence 发布链路时，才在 ADR 生成后回到本 skill 后续阶段

主文件保留三条硬约束：

1. 所有章节都必须填充；不能确认的内容用 `[待补充]`
2. 先做架构评审；若文档含较多可验证技术断言，再做验证链核查；最后做发布前格式校验
3. 验证链只核查版本、兼容性、性能数据、公共产品能力边界等可外部验证事实，不替代架构判断本身
4. 任何格式校验不通过时，都不得进入发布阶段

## Phase 5: Confluence 发布

依赖定位、降级策略、dry-run、正式发布和发布后验证见 `references/confluence-publish.md`。

主文件保留发布原则：

1. 发布是可选阶段，不是所有请求都要走到 Confluence
2. 没有 `confluence-cli` 脚本时，优雅降级为本地 Markdown 交付
3. 若本轮需要验证链核查，则发布前必须确认已完成核查或已记录跳过原因
4. 只要进入发布路径，dry-run 就是必做项

## 结果约束

1. 文档默认中文输出；用户要求英文时再切换
2. 已 Accepted 的 ADR 不直接改写其决策结论；需要变更时优先新增 ADR 并标记旧者为 `Superseded`
3. 若最终只交付草稿，应明确说明哪些字段仍待补充，不能伪装成可直接发布的定稿
4. 若跳过验证链核查，应明确写出跳过原因，例如“仅含内部决策判断”“无联网核查条件”或“用户要求跳过”
