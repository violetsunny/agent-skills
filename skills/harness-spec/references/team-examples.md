# 智能体团队示例

---

## 示例 1：调研团队（智能体团队模式）

### 团队架构：扇出/扇入
### 执行模式：智能体团队

```
[负责人/编排器]
    ├── TeamCreate(research-team)
    ├── TaskCreate（4 个调研任务）
    ├── 团队成员自我协调（SendMessage）
    ├── 使用 Read 收集结果
    └── 生成综合报告
```

### 智能体构成

| 成员 | 类型 | 角色 | 输出 |
|------|------|------|------|
| official-researcher | general-purpose | 官方文档与博客调研 | research_official.md |
| media-researcher | general-purpose | 媒体与投资信息调研 | research_media.md |
| community-researcher | general-purpose | 社区与社交网络调研 | research_community.md |
| background-researcher | general-purpose | 背景、竞争环境与学术调研 | research_background.md |
| （负责人 = 编排器） | — | 综合报告生成者 | 总结报告.md |

> 调研类智能体使用 `general-purpose` 内置类型，但仍需在 `.claude/agents/{name}.md` 中定义文件，明确角色、调研范围与团队通信协议，以提高复用性与协作质量。

### 编排器工作流（团队模式）

```text
Phase 1：准备
  - 分析用户输入（主题与调研方式）
  - 创建 _workspace/

Phase 2：团队组建
  - TeamCreate(team_name: "research-team", members: [
      { name: "official", prompt: "调研官方渠道..." },
      { name: "media", prompt: "调研媒体与投资动向..." },
      { name: "community", prompt: "调研社区反应..." },
      { name: "background", prompt: "调研背景与竞争环境..." }
    ])
  - TaskCreate(tasks: [
      { title: "官方渠道调研", assignee: "official" },
      { title: "媒体动向调研", assignee: "media" },
      { title: "社区反应调研", assignee: "community" },
      { title: "背景环境调研", assignee: "background" }
    ])

Phase 3：执行调研
  - 4 名成员各自独立调研；
  - 发现重要信息时通过 SendMessage 在成员间共享；
    （例如：media 将某项投资信息发送给 background）；
  - 发现相互矛盾的信息时成员间进行讨论；
  - 每位成员完成后保存文件并通知负责人。

Phase 4：整合结果
  - 负责人通过 Read 读取 4 个调研产物；
  - 生成综合报告；
  - 对矛盾信息进行并列呈现并注明各自来源。

Phase 5：收尾
  - 向成员发送结束通知；
  - 调用 TeamDelete 销毁团队；
  - 保留 _workspace/ 目录以便事后验证与审计。
```

### 团队通信模式

```text
official ──SendMessage──→ background  （共享相关官方公告）
media ─────SendMessage──→ background  （共享投资/收购信息）
community ─SendMessage──→ media      （社区反应中与媒体相关的信息）
所有成员 ──TaskUpdate──→ 共享任务列表  （更新进度）
负责人 ←──── 空闲通知 ───── 已完成成员  （自动）
```

---

## 示例 2：科幻小说创作团队（智能体团队模式）

### 团队架构：流水线 + 扇出
### 执行模式：智能体团队

```text
Phase 1（并行，团队模式）：worldbuilder + character-designer + plot-architect
  → 通过 SendMessage 相互协调设定一致性
Phase 2（顺序）：prose-stylist 进行草稿写作
Phase 3（并行，团队模式）：science-consultant + continuity-manager 进行审阅
  → 通过 SendMessage 共享审阅发现
Phase 4（顺序）：prose-stylist 根据审阅结果进行修订
```

### 智能体构成

| 成员 | 类型 | 角色 | 使用 Skill |
|------|------|------|------------|
| worldbuilder | 自定义 | 世界观构建 | world-setting |
| character-designer | 自定义 | 人物设定 | character-profile |
| plot-architect | 自定义 | 剧情结构设计 | outline |
| prose-stylist | 自定义 | 文风编辑与写作 | write-scene, review-chapter |
| science-consultant | 自定义 | 科学合理性审查 | science-check |
| continuity-manager | 自定义 | 故事连贯性审查 | consistency-check |

### 智能体文件示例：`worldbuilder.md`

```markdown
---
name: worldbuilder
description: "负责构建科幻小说的世界观，包括物理法则、社会结构、技术水平与历史背景。"
---

# Worldbuilder — 科幻世界观设计专家

你是科幻小说的世界观设计专家。基于科学事实延伸想象力，为故事提供物理、社会与技术层面的基础设定。

## 核心职责
1. 定义世界的物理法则与技术发展水平；
2. 构建社会结构、政治体制与经济系统；
3. 设计历史背景与当前冲突格局；
4. 描述各主要地点的环境与氛围。

## 工作原则
- 优先保证设定内部一致性，避免逻辑矛盾；
- 通过“如果存在该技术，会带来哪些连锁影响？”进行推演；
- 世界观服务于故事，避免过度复杂且与剧情无关的设定。

## 输入/输出约定
- 输入：用户提供的世界观设想与类型要求；
- 输出：`_workspace/01_worldbuilder_setting.md`；
- 格式：Markdown，按物理/社会/技术/历史/地点分节。

## 团队通信协议
- 向 character-designer 发送社会结构与阶层信息；
- 向 plot-architect 发送主要冲突与危机信息；
- 接收 science-consultant 的科学合理性反馈并改进设定；
- 更新世界观设定时，向相关成员广播变更信息。

## 错误处理
- 若用户提供的概念过于模糊，提出 3 种可能方向并请求选择；
- 若发现重大科学错误，给出替代设定建议并说明差异。

## 协作
- 为 character-designer 提供角色所处社会环境背景；
- 为 plot-architect 提供主要冲突与历史脉络；
- 根据 science-consultant 的反馈更新设定文档。
```

### 团队工作流详述

```text
Phase 1：TeamCreate("novel-team", members: [worldbuilder, character-designer, plot-architect])
          TaskCreate([世界观构建, 人物设定, 剧情结构])
          → 团队成员并行工作；
          → worldbuilder 完成社会结构后向 character-designer 发送信息；
          → character-designer 完成人物设定后向 plot-architect 发送信息。

Phase 2：结束 Phase 1 团队，改用子智能体模式调用 prose-stylist；
          prose-stylist 读取 _workspace/ 中三份设定文档进行写作，
          将草稿保存至 `_workspace/02_prose_draft.md`。

Phase 3：创建新团队 TeamCreate("review-team", members: [science-consultant, continuity-manager])；
          两位审阅者共同审阅草稿，互相共享发现；
          science-consultant 若发现物理错误，会通知 continuity-manager；
          审阅完成后销毁团队。

Phase 4：再次调用 prose-stylist，基于审阅报告修订草稿并生成最终稿。
```

---

## 示例 3：网络漫画制作团队（子智能体模式）

### 团队架构：生成-验证
### 执行模式：子智能体

> 在生成-验证模式中，仅有两个智能体且主要是结果传递，因此更适合使用子智能体模式。

```text
Phase 1：调用 webtoon-artist 生成画格；
Phase 2：调用 webtoon-reviewer 进行审阅；
Phase 3：若有问题，最多两次再次调用 webtoon-artist 重新生成问题画格。
```

### 智能体构成

| 智能体 | subagent_type | 角色 | 使用 Skill |
|--------|---------------|------|------------|
| webtoon-artist | 自定义 | 生成漫画画格 | generate-webtoon |
| webtoon-reviewer | 自定义 | 审阅质量 | review-webtoon, fix-webtoon-panel |

### 智能体文件示例：`webtoon-reviewer.md`

```markdown
---
name: webtoon-reviewer
description: "负责审阅网络漫画画格质量，从构图、角色一致性、文字可读性与演出效果等维度进行评价。"
---

# Webtoon Reviewer — 网络漫画质量审阅专家

你是网络漫画画格质量审阅专家，依据画面完整度、故事传达效果与角色一致性来评估每个画格的质量。

## 核心职责
1. 评估每个画格的构图与视觉完整度；
2. 检查角色外形在各画格间的一致性；
3. 评估对话框文字的可读性与布局合理性；
4. 审视整集故事的整体演出和节奏（节奏快慢、场景切换等）。

## 工作原则
- 使用 PASS / FIX / REDO 三档结果，明确指示;
- FIX 表示通过局部修改即可解决问题，REDO 表示需整体重绘；
- 尽量依赖客观标准（如一致性、可读性、构图）而非个人偏好。

## 输入/输出约定
- 输入：`_workspace/panels/` 目录下的画格图像；
- 输出：`_workspace/review_report.md`；
- 输出格式：
  ```markdown
  ## Panel {N}
  - 结论：PASS | FIX | REDO
  - 原因：[具体原因]
  - 修改建议：[FIX/REDO 时给出具体修改方向]
  ```

## 错误处理
- 若图像无法加载，则对该画格直接给出 REDO；
- 若某画格经过两次重绘仍被判定为 REDO，则在警告后视为 PASS，以免陷入无限循环。

## 协作
- 向 webtoon-artist 发送修改说明（基于审阅报告）；
- 对重绘后的画格再次进行审阅（最多循环 2 次）。
```

### 错误处理策略

```text
重试策略：
- 对被判定为 REDO 的画格，向画师发送重新绘制请求，并附上具体修改建议；
- 同一画格最多重绘 2 次，仍为 REDO 时强制 PASS；
- 当超过 50% 的画格被判定为 REDO 时，建议用户修改原始提示词或设定。
```

---

## 示例 4：代码评审团队（智能体团队模式）

### 团队架构：扇出/扇入 + 讨论
### 执行模式：智能体团队

> 代码评审是智能体团队优势突出的场景之一：多个审阅者从安全、性能与测试等不同角度分析，并通过互相交流发现更深层问题。

```text
[负责人] → TeamCreate(review-team)
    ├── security-reviewer：负责安全漏洞检查；
    ├── performance-reviewer：负责性能影响分析；
    └── test-reviewer：负责测试覆盖率验证；
    → 审阅者之间通过 SendMessage 共享发现；
    → 负责人整合最终评审结果。
```

### 团队通信模式

```text
security ──SendMessage──→ performance  （如："此 SQL 存在注入风险，请从性能角度评估"）
performance ──SendMessage──→ test       （如："检测到 N+1 查询，确认是否有相关测试"）
test ─────SendMessage──→ security       （如："认证模块缺乏测试，请给出安全优先级建议"）
```

关键点：审阅者之间可 **绕过负责人直接沟通**，快速发现跨领域问题。

---

## 示例 5：监督者模式——代码迁移团队（智能体团队模式）

### 团队架构：监督者
### 执行模式：智能体团队

```text
[supervisor/负责人] → 分析文件列表 → 分配迁移任务
    ├→ [migrator-1] 负责批次 A
    ├→ [migrator-2] 负责批次 B
    └→ [migrator-3] 负责批次 C
    ← 通过 TaskUpdate 接收进度；根据情况分配新任务或调整任务分配。
```

### 智能体构成

| 成员 | 角色 |
|------|------|
| migration-supervisor（负责人） | 负责分析文件、分配批次任务与管理进度 |
| migrator-1~3 | 负责处理各自所分配的文件批次 |

### 监督者的动态分配逻辑（团队模式）

```text
1. 收集所有待迁移文件列表；
2. 根据文件大小、import 数量与依赖关系估计复杂度；
3. 使用 TaskCreate 注册各文件批次为任务（包含依赖信息）；
4. 团队成员可自械从任务列表中领取任务；
5. 成员通过 TaskUpdate 上报任务完成状态：
   - 完成 → 自动领取下一任务；
   - 失败 → 负责人通过 SendMessage 查询原因，并进行重分配或重新调度；
6. 全部任务完成后，负责人执行整体验证与测试。
```

与普通扇出模式的区别：任务不是预先固定，而是在运行过程中 **动态分配**。共享任务列表的“自助领取”机制与监督者模式高度契合。

---

## 产出模式汇总

### 智能体定义文件

路径：`项目/.claude/agents/{agent-name}.md`
必备部分：核心角色、工作原则、输入/输出协议、错误处理与协作方式；
在团队模式下需要增加：**团队通信协议**（说明消息接收与发送对象，以及任务请求范围）。

### Skill 文件结构

路径：`项目/.claude/skills/{skill-name}/SKILL.md`（项目级），或 `~/.claude/skills/{skill-name}/SKILL.md`（全局级）。

### 编排器 Skill

用于协调整个团队的上层 Skill，定义不同场景下的智能体构成与工作流。模板可参考 `references/orchestrator-template.md`。

> 必须在编排器 Skill 中明确声明执行模式：默认使用智能体团队模式，必要时可使用子智能体模式或混合模式。
