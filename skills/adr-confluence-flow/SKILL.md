---
name: adr-confluence-flow
description: >
  技术方案端到端工作流：需求收敛 → 深度追问澄清 → 方案发散/权衡 → 生成结构化文档 →
  架构评审 → 合规校验 → 发布到 Confluence。支持三种模板：ADR标准格式、技术提案格式、
  简报格式。融合 to-spec（需求收敛）、grilling（设计树追问）、brainstorming（方案发散）、
  adr-generator（模板生成）、architecture-review（架构评审）、confluence-cli（Confluence发布）
  六者的能力。
  当用户需要"写技术方案"、"生成ADR"、"架构决策记录发布Confluence"、"技术提案发Confluence"、
  "方案归档到Confluence"、"写架构文档并发布"、"技术选型方案输出"时触发。
  也适用于"决策简报"、"向上汇报方案"、"1页方案"、"决策评审材料"等简报场景。
  也适用于用户描述了技术选型/架构设计需求并希望输出文档到 Confluence 的场景。
---

# ADR-Confluence-Flow

技术方案端到端工作流技能。将需求收敛、深度追问、方案发散、结构化文档生成、架构评审、
合规校验和 Confluence 发布融为一体，从模糊想法到线上发布一站式完成。

## 能力概览

| 阶段 | 能力 | 来源融合 |
|------|------|---------|
| 需求收敛 | 把粗粒度想法压实为目标、边界、验收条件 | to-spec |
| 追问澄清 | 设计树驱动的逐轮深度追问，确保方案无遗漏 | grilling |
| 方案发散 | 在多个可行路径之间展开对比和取舍 | brainstorming |
| 文档生成 | 三种模板：ADR标准 / 技术提案 / 简报 | adr-generator |
| 架构评审 | 在成文前检查方案完整性、边界、权衡与风险 | architecture-review |
| 合规校验 | 完整性检查、格式校验、必填章节验证 | 本 skill 原创 + architecture-review |
| Confluence发布 | Markdown→Storage XML，支持Mermaid/LaTeX/折叠块等富文本 | confluence-cli |

## 工作流总览

```
用户触发 → 信息评估 → [需求收敛(可选)] → [追问阶段(可选)] → [方案发散(可选)] → 模板选择 → 文档生成 → 架构评审 → 合规校验 → Confluence发布
```

---

### Phase 0：信息评估

收到用户需求后，先评估信息完整度。

**必须收集的信息：**
1. 核心问题/业务痛点
2. 候选方案（至少2个）
3. 最终选定方案
4. 作者/团队名称

**可选信息（缺失时追问或合理推断）：**
- 技术栈约束、性能指标、工期
- 状态（Proposed / Accepted）
- 文档编号
- 预期模板类型
- 目标 Confluence 页面（父页面ID或页面ID）—仅发布阶段需要

**评估规则：**
- 信息充分 → 直接进入 Phase 2（生成）
- 用户输入只有模糊目标、缺少边界/验收条件 → 先用 `to-spec` 收敛需求，再决定是否追问
- 信息不足 → 建议进入 Phase 1（追问），用户可跳过
- 存在多个可行方案且权衡未定 → 先用 `brainstorming` 展开方案比较，再进入生成
- 用户明确说"直接生成" → 跳过追问，缺信息时用 `[待补充]` 标注

---

### Phase 1：追问阶段（可选）

采用**设计树 + 逐轮追问**方法，将技术方案拆解为决策树，逐轮澄清未定问题。

**追问流程：**
1. 将方案拆解为决策树：每个决策点分叉出依赖它的子决策
2. 计算**前沿**（所有前置依赖已确定的决策点）——即当前可以提问的问题
3. 每轮提问所有前沿问题，格式：
   ```
   ❓ **Q1** - **问题标题**: 问题描述（含推荐选项）
   ➡️ 推荐答案
   ```
4. 用户回答后重新计算前沿，进入下一轮
5. 前沿为空时追问结束，总结已达成的共识

**事实查找委托：**
当前沿问题需要从环境中获取事实（文件系统、工具版本、现有代码模式等）时，
使用搜索工具自行查找，不要向用户提问本可自行获取的信息。
正在进行的查找视为未确定的前置依赖，仅下游问题等待其结果，其余前沿问题照常提问。

**追问覆盖维度：**
- **上下文**：业务背景、技术约束、性能要求、团队规模、工期压力
- **决策**：为什么选这个方案、具体实现方式、明确不做的边界
- **后果**：正面/负面影响、可量化指标
- **替代方案**：每个方案的优缺点、淘汰原因
- **撤销条件**：什么情况下需要推翻重来

**用户可随时说"跳过追问"或"直接生成"进入下一阶段。**

### Phase 1.5：需求收敛 / 方案发散（可选）

当用户提供的是一句方向、一个松散主题，或者多个候选方案还没有形成明确取舍时，优先借助项目内 skill 做预处理，而不是直接硬写文档。

**引入规则：**
- **`to-spec`**：适用于“我要做个 X 方案”“帮我出个技术选型文档”这类粗粒度输入。目标是先收敛出清晰的问题定义、范围边界、验收条件、约束。
- **`brainstorming`**：适用于多个候选方案都可能成立、但权衡点还没说清的场景。目标是把方案空间、优缺点、适用边界和淘汰理由摊开。

**使用顺序：**
- 需求太粗 → 先 `to-spec`
- 方向很多、取舍不清 → 再 `brainstorming`
- 方向已经明确 → 跳过这一步，直接生成文档

**产出要求：**
- 只提炼决策所需的信息，不把这两个 skill 的完整过程原样塞进最终文档
- 最终文档中只保留收敛后的问题定义、候选方案、决策依据、边界和风险

---

### Phase 2：模板选择与文档生成

#### 模板选择

| 模板 | 适用场景 | 输出长度 | 特点 |
|------|---------|---------|------|
| ADR标准 | 单一架构决策记录 | 1-3页 | 聚焦一个决策，6章节固定结构 |
| 技术提案 | 综合技术方案设计 | 5-15页 | 含架构图/时序图/接口/风险/排期 |
| 简报 | 决策评审/向上汇报 | 1页 | 问题→方案→风险→成本→决策 |

**选择规则：**
- 用户明确指定 → 按指定模板
- 单一技术选型决策 → ADR标准
- 涉及多模块/系统级设计 → 技术提案
- 需要快速决策评审 → 简报
- 不确定时询问用户

#### 文档生成

读取对应模板并填充内容：
- ADR标准 → 读取 `references/adr-standard-template.md`
- 技术提案 → 读取 `references/tech-proposal-template.md`
- 简报 → 读取 `references/brief-template.md`

**生成要求：**
- 所有章节必须填充，不允许空章节
- 缺失信息用 `[待补充]` 标注并提醒用户
- 代码块标注语言（python / java / sql / yaml 等）
- 架构图使用 Mermaid 语法（`flowchart`、`sequenceDiagram` 等）
- 表格使用 Markdown 标准格式
- 使用 `[EXPAND 标题]...[/EXPAND]` 折叠次要内容
- 使用 `- [ ]` / `- [x]` 任务列表标注待办事项
- 需要保留 Confluence 原生宏时使用 `confluence-storage` 围栏

---

### Phase 3：架构评审

文档初稿生成后，在发布前先引入 `architecture-review` 做一次架构级审视，避免把
明显缺边界、缺权衡、缺风险闭环的方案直接送去 Confluence。

**适用时机：**
- ADR、技术提案、决策简报三种模板都适用
- 尤其适合涉及技术选型、系统边界、模块拆分、依赖关系、性能容量、可靠性、迁移路径的内容

**评审目标：**
- 决策是否真的回应了核心问题，而不是只给实现细节
- 备选方案是否充分，淘汰理由是否成立
- 方案边界、非目标、约束、风险、回滚条件是否明确
- 是否缺少关键视角：容量、性能、可用性、安全、可运维性、扩展性、迁移成本
- 文档中的架构图、时序图、接口说明、实施计划是否相互一致

**执行规则：**
- 初稿完成后，先用 `architecture-review` 对文档内容进行评审
- 如果评审发现关键缺口，先修正文档，再进入下一阶段
- 如果只是轻微表达问题，可直接修正措辞后继续
- 如果用户明确要求“快速出稿、不做深评审”，可弱化该阶段，但仍需至少执行一次快速自检

**评审输出要求：**
- 用简洁结论列出关键问题，不展开成长篇代码级实现分析
- 优先指出：缺失决策依据、边界不清、风险遗漏、验收标准失真、图文不一致
- 评审通过后，再进入 Phase 4

---

### Phase 4：合规校验

生成文档并完成架构评审后，按模板类型执行校验清单。各模板自带完整校验清单，Phase 4 以下为快速参考；
完整校验以模板文件中的清单为准。

**ADR标准校验（完整清单见 `references/adr-standard-template.md`）：**
- [ ] 编号从 0001 递增，保持唯一
- [ ] 状态为 Proposed / Accepted / Deprecated / Superseded 之一
- [ ] 后果至少2条正面 + 2条负面
- [ ] 替代方案至少2个，每个含优缺点 + 淘汰原因
- [ ] 撤销条件至少3条
- [ ] 变更历史首行已填充

**技术提案校验（完整清单见 `references/tech-proposal-template.md`）：**
- [ ] 背景与目标清晰可量化
- [ ] 至少1张架构图（Mermaid flowchart）
- [ ] 核心流程至少1张时序图（Mermaid sequenceDiagram）
- [ ] 方案对比含对比表格
- [ ] 风险评估含风险等级和应对措施
- [ ] 实施计划含时间线和负责人
- [ ] 验收标准可量化

**简报校验（完整清单见 `references/brief-template.md`）：**
- [ ] 问题陈述 ≤3句话
- [ ] 推荐方案 ≤5个要点
- [ ] 主要风险 ≤3条
- [ ] 成本估算含开发+资源+运维
- [ ] 决策需求明确具体
- [ ] 整体可1页内展示

**通用格式校验（发布到 Confluence 前必须通过）：**
- [ ] 无原始 HTML（使用 `confluence-storage` 围栏替代）
- [ ] emoji 仅使用 confluence-cli 支持的20个名称（`smile` `sad` `cheeky` `laugh` `wink` `thumbs-up` `thumbs-down` `information` `tick` `cross` `warning` `plus` `minus` `question` `light-on` `light-off` `yellow-star` `red-star` `green-star` `blue-star`）
- [ ] Mermaid 节点标签不含 `(` `)` `|` 字符（会导致渲染失败）
- [ ] Block 公式 `$$` 必须独占行首
- [ ] 有序列表中插入图片时改用加粗编号（`**1**`、`**2**`），避免列表被截断重编号

校验不通过 → 修正后重新校验。校验通过 → 进入发布阶段。

---

### Phase 5：Confluence 发布

发布阶段依赖 `confluence-cli` skill 的脚本。如果用户未安装该 skill，**不报错中断**，
而是优雅降级：输出已生成的 Markdown 文件路径，并提示用户安装 confluence-cli 后自行发布。

#### 5.0 定位 confluence-cli 脚本（发布前必须执行）

confluence-cli 的脚本路径因 agent 平台而异，按以下优先级搜索：

1. 环境变量 `CONFLUENCE_CLI_SCRIPTS` 指向的 scripts 目录（用户显式覆盖）
2. 当前项目目录下的 `.agents/skills/confluence-cli/scripts/`
3. 全局 `~/.agents/skills/confluence-cli/scripts/`（workspace-cli 约定）
4. 全局 `~/.claude/skills/confluence-cli/scripts/`（Claude Code 约定）

```bash
# 按优先级搜索 confluence_cli.py（环境变量指向目录，其余路径直接指向文件）
CONFLUENCE_CLI=""
for candidate in \
  "${CONFLUENCE_CLI_SCRIPTS:+$CONFLUENCE_CLI_SCRIPTS/confluence_cli.py}" \
  ".agents/skills/confluence-cli/scripts/confluence_cli.py" \
  "$HOME/.agents/skills/confluence-cli/scripts/confluence_cli.py" \
  "$HOME/.claude/skills/confluence-cli/scripts/confluence_cli.py"; do
  [ -n "$candidate" ] && [ -f "$candidate" ] && CONFLUENCE_CLI="$candidate" && break
done
```

**如果 `CONFLUENCE_CLI` 为空（所有路径都未找到）**：
1. 告知用户："Confluence 发布需要 confluence-cli skill，当前未安装。"
2. 提示安装方式："可通过 skill_marketplace 搜索 confluence-cli 并安装。如已安装在其他位置，请设置环境变量 `CONFLUENCE_CLI_SCRIPTS` 指向其 scripts 目录。"
3. 将已生成的 Markdown 保存到用户指定路径（默认 `/tmp/adr-confluence-output.md`）
4. 告知用户："文档已保存到 {路径}，安装 confluence-cli 后可用以下命令发布："
   并打印发布命令模板（将 `$CONFLUENCE_CLI` 替换为实际路径）供用户复制
5. 结束发布流程，不继续执行后续步骤

**如果找到**：`CONFLUENCE_CLI` 变量保存了脚本完整路径，后续所有命令用它替代写死路径。继续执行 5.1

#### 5.1 环境检查

```bash
uv --version
```

如果 `uv` 不可用，提示用户安装（`curl -LsSf https://astral.sh/uv/install.sh | sh`）。

#### 5.2 保存文档到本地

将生成的 Markdown 内容保存为本地 `.md` 文件（如 `/tmp/adr-confluence-output.md`）。

#### 5.3 试运行（发布前必须执行）

```bash
uv run --script "$CONFLUENCE_CLI" page publish-markdown \
  --parent-id <父页面ID> --title "<文档标题>" --markdown-path /tmp/adr-confluence-output.md --dry-run
```

检查终端输出的 Storage XML，确认：
- 标题层级正确（H1自动剥除，H2开始）
- 表格、列表、代码块格式正确
- Mermaid 图渲染为 SVG（检查有无 warning）
- 折叠块、任务列表、公式正确转换
- `confluence-storage` 围栏内容原样透传

#### 5.4 正式发布

```bash
# 方式一：发布到父页面（同名则创建/更新）
uv run --script "$CONFLUENCE_CLI" --json page publish-markdown \
  --parent-id <父页面ID> --title "<文档标题>" --markdown-path /tmp/adr-confluence-output.md

# 方式二：直接更新已知页面（推荐，更快更安全）
uv run --script "$CONFLUENCE_CLI" --json page publish-markdown \
  --parent-id <父页面ID> --page-id <页面ID> --title "<文档标题>" --markdown-path /tmp/adr-confluence-output.md
```

#### 5.5 发布后验证

```bash
uv run --script "$CONFLUENCE_CLI" --json page get \
  --page-id <页面ID> --body-format storage --expand body.storage,version --fresh
```

确认正文版本已更新、图片引用和宏正确渲染。

---

## Confluence 富文本格式支持

文档生成时可直接使用以下语法，发布时自动转换为 Confluence 原生格式：

| 格式 | 语法 | 说明 |
|------|------|------|
| Mermaid流程图 | ` ```mermaid` ... ` ``` ` | 自动渲染为SVG内联嵌入 |
| LaTeX公式 | `$...$`（行内）、`$$...$$`（块） | 块公式 `$$` 必须独占行首 |
| 折叠块 | `[EXPAND 标题]` ... `[/EXPAND]` | 可嵌套，内含完整Markdown |
| 任务列表 | `- [ ]` / `- [x]` | 转为Confluence原生复选框 |
| 代码自动折叠 | 代码块 > 200行自动折叠 | 无需手动操作 |
| Emoji | `:tick:` `:warning:` 等 | 仅支持20个内置名称 |
| @提及 | `@姓名` | 需配置 `CONFLUENCE_MENTION_MAP` 环境变量 |
| Storage直通 | ` ```confluence-storage` ... ` ``` ` | 原样透传 Confluence storage XML |
| 图片尺寸控制 | `![图](./a.png "confluence-width=1200")` | 通过 title 控制展示尺寸 |
| 信息宏 | 通过 `confluence-storage` 围栏嵌入 | `<ac:structured-macro ac:name="info">` |

> 完整格式规范参考 confluence-cli skill 的 SKILL.md。

---

## 交互流程示例

```
用户：帮我写一个缓存方案的技术提案，发到Confluence

技能：我需要确认几个信息：
  1. 核心痛点是什么？
  2. 候选方案有哪些？
  3. 最终选定哪个？
  4. 作者/团队？
  5. Confluence 父页面ID？
  6. 用哪种模板？（ADR标准 / 技术提案 / 简报）

用户：行情接口延迟高，候选Redis和Caffeine，选Redis Cluster，量化后端组，父页面3061931928，用技术提案

技能：信息充分。是否需要追问澄清细节？可以说"直接生成"跳过。

用户：直接生成

技能：[生成技术提案 Markdown] → [架构评审通过] → [合规校验通过] → [dry-run 确认格式] → [发布到 Confluence]
      → 返回页面链接
```

---

## 注意事项

1. **原 skill 保留**：本 skill 融合了 to-spec（需求收敛）、grilling（设计树追问方法）、brainstorming（方案发散）、adr-generator（模板结构）、architecture-review（架构评审）、confluence-cli（发布脚本）的能力，原 skill 不受影响，可独立使用。合规校验清单为本 skill 原创
2. **Confluence 发布依赖**：Phase 5 依赖 `confluence-cli` skill 的脚本。通过多路径搜索定位（环境变量 `CONFLUENCE_CLI_SCRIPTS` → 项目级 `.agents/skills/` → 全局 `~/.agents/skills/` → `~/.claude/skills/`），兼容不同 agent 平台。未找到时不报错，自动降级为仅输出 Markdown 文件并给出安装指引。追问、需求收敛、方案发散、文档生成和架构评审阶段不依赖任何外部发布脚本
3. **Mermaid 网络依赖**：Mermaid 渲染依赖 mermaid.ink 公网服务或 `MERMAID_INK_SERVER` 环境变量
4. **dry-run 必须执行**：发布前必须先 dry-run 确认格式，避免线上页面格式错误
5. **文档语言**：默认中文输出，用户可要求英文
6. **ADR 编号**：从 0001 开始递增，保持唯一性；已 Accepted 的 ADR 不应修改，如需变更应创建新 ADR 并标记旧者为 Superseded
