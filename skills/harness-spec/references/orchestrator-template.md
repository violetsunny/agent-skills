# 编排器技能模板

编排器（Orchestrator）是负责协调整个团队的上层 Skill。根据执行模式提供 3 种模板：

- **模板 A：智能体团队模式（默认）** —— 在两名以上智能体协作时的首选模式
- **模板 B：子智能体模式（备选）** —— 在不需要团队通信时使用
- **模板 C：混合模式** —— 在不同 Phase 混合使用多种模式

---

## 模板 A：智能体团队模式（默认，优先选择）

当有 2 名以上智能体协作时，这是 **必须优先考虑的默认模式**。通过 `TeamCreate` 组建团队，通过共享任务列表与 `SendMessage` 进行协调。

```markdown
---
name: {domain}-orchestrator
description: "用于协调 {领域} 智能体团队的编排器。初始执行关键词：{初始执行关键词}。后续工作：当用户提出 {领域} 结果修改、部分重执行、更新、补充、再次执行、基于既有结果进行改进等请求时，也必须使用此技能。"
---

# {Domain} Orchestrator

负责协调 {领域} 智能体团队，生成 {最终产物} 的综合 Skill。

## 执行模式：智能体团队

## 智能体构成

| 成员 | 类型 | 角色 | 使用技能 | 输出 |
|------|------|------|----------|------|
| {teammate-1} | {自定义或内置} | {角色} | {skill} | {output-file} |
| {teammate-2} | {自定义或内置} | {角色} | {skill} | {output-file} |
| ... | | | | |

## 工作流

### Phase 0：上下文检查（支持后续工作）

通过检查是否存在既有产物来决定执行模式：

1. 检查 `_workspace/` 目录是否存在。
2. 根据结果决定执行模式：
   - **`_workspace/` 不存在** → 视为首次执行，进入 Phase 1。
   - **`_workspace/` 存在 且 用户请求部分修改** → 部分重执行。仅重新调用相关智能体，并只覆盖需修改部分的产物。
   - **`_workspace/` 存在 且 用户提供新输入** → 全新执行。先将旧 `_workspace/` 重命名为 `_workspace_{YYYYMMDD_HHMMSS}/`，再进入 Phase 1。
3. 在部分重执行模式下：需在智能体提示中加入旧产物路径，使智能体读取历史结果并基于反馈进行修正。

### Phase 1：准备阶段

1. 分析用户输入 —— 明确 {需要识别的内容}。
2. 在工作目录中创建 `_workspace/`：
   - **首次执行**：直接创建新的 `_workspace/`。
   - **全新执行**：在将旧 `_workspace/` 迁移至 `_workspace_{YYYYMMDD_HHMMSS}/` 后，重新创建新的 `_workspace/`。
3. 将输入数据保存至 `_workspace/00_input/`。

### Phase 2：团队组建

1. 创建团队：

```markdown
TeamCreate(
  team_name: "{domain}-team",
  members: [
    { name: "{teammate-1}", agent_type: "{type}", model: "opus", prompt: "{角色说明与任务指示}" },
    { name: "{teammate-2}", agent_type: "{type}", model: "opus", prompt: "{角色说明与任务指示}" },
    ...
  ]
)
```

2. 注册任务：

```markdown
TaskCreate(tasks: [
  { title: "{任务1}", description: "{说明}", assignee: "{teammate-1}" },
  { title: "{任务2}", description: "{说明}", assignee: "{teammate-2}" },
  { title: "{任务3}", description: "{说明}", depends_on: ["{任务1}"] },
  ...
])
```

> 单个成员建议分配 5–6 个任务。存在依赖关系的任务需通过 `depends_on` 显式标注。

### Phase 3：主要工作阶段（如：调研/生成/分析）

**执行策略：** 由团队成员自我协调。

- 成员从共享任务列表中领取（claim）任务并独立执行；
- 负责人监控整体进度并在必要时介入。

**团队通信规则：**
- {teammate-1} 通过 SendMessage 向 {teammate-2} 传递 {信息类型}；
- {teammate-2} 完成工作后保存结果文件并通知负责人；
- 当成员需要其他成员的结果时，通过 SendMessage 发起请求。

**产物保存规则：**

| 成员 | 输出路径 |
|------|----------|
| {teammate-1} | `_workspace/{phase}_{teammate-1}_{artifact}.md` |
| {teammate-2} | `_workspace/{phase}_{teammate-2}_{artifact}.md` |

**负责人监控要点：**
- 成员空闲时自动收到通知；
- 成员遇到阻塞时，通过 SendMessage 下达指令或重新分配任务；
- 使用 TaskGet 查看整体进度与任务状态。

### Phase 4：后续工作（如：验证/整合）

1. 等待所有成员完成任务（通过 TaskGet 确认状态）；
2. 使用 Read 收集各成员产物；
3. 执行 {整合/验证逻辑}；
4. 生成最终产物：`{output-path}/{filename}`。

### Phase 5：收尾

1. 向团队成员发送结束通知（SendMessage）；
2. 调用 TeamDelete 销毁团队；
3. 保留 `_workspace/` 目录（不删除中间产物，用于事后验证与审计）。
4. 向用户汇报结果摘要。

> **当需要重新组建团队时：** 如果各个 Phase 需要不同专家组合，应先通过 TeamDelete 清理当前团队，再通过新的 TeamCreate 为下一 Phase 组建新团队。之前团队产物仍保存在 `_workspace/` 中，新团队可通过 Read 使用。

## 数据流

```
[负责人] → TeamCreate → [成员-1] ←SendMessage→ [成员-2]
                         │                              │
                         ↓                              ↓
                   artifact-1.md                  artifact-2.md
                         │                              │
                         └───────── Read ───────────────┘
                                    ↓
                             [负责人：整合]
                                    ↓
                             最终产物输出
```

## 错误处理

| 场景 | 策略 |
|------|------|
| 单个成员失败/中止 | 负责人发现后，通过 SendMessage 获取状态 → 重启或创建替代成员 |
| 多数成员失败 | 通知用户并确认是否继续执行 |
| 超时 | 使用当前已收集的部分结果，终止未完成成员 |
| 成员间数据冲突 | 保留所有冲突数据并注明来源，不删除任何一方 |
| 任务状态延迟 | 负责人通过 TaskGet 检查状态并手动通过 TaskUpdate 校正 |

## 测试场景

### 正常流程

1. 用户提供 {输入}；
2. Phase 1 生成 {分析结果}；
3. Phase 2 组建团队（{N} 名成员，{M} 个任务）；
4. Phase 3 中团队成员自我协调完成任务；
5. Phase 4 整合产物生成最终结果；
6. Phase 5 收尾并销毁团队；
7. 预期产物：生成 `{output-path}/{filename}`。

### 错误流程

1. Phase 3 中 {teammate-2} 因错误中止；
2. 负责人收到空闲通知；
3. 通过 SendMessage 查询状态并尝试重启；
4. 若重启失败，将 {teammate-2} 的任务重新分配给 {teammate-1}；
5. 使用剩余结果执行 Phase 4；
6. 在最终报告中注明“{teammate-2} 范围内部分内容缺失”。
```

---

## 模板 B：子智能体模式（备选）

当团队通信开销不必要时，使用此模式。通过 `Agent` 工具直接调用子智能体，并用返回值收集结果。

```markdown
---
name: {domain}-orchestrator
description: "用于协调 {领域} 智能体的编排器。{初始执行关键词}。包含后续工作关键词。"
---

## 执行模式：子智能体

## 智能体构成

| 智能体 | subagent_type | 角色 | 使用技能 | 输出 |
|--------|---------------|------|----------|------|
| {agent-1} | {内置或自定义} | {角色} | {skill} | {output-file} |
| {agent-2} | ... | ... | ... | ... |

## 工作流

### Phase 0：上下文检查

与模板 A 相同——根据 `_workspace/` 是否存在进行分支。

### Phase 1：准备

1. 分析输入；
2. 创建 `_workspace/`（在首次运行或旧 `_workspace/` 迁移之后）。

### Phase 2：并行执行

在同一消息中并行调用多个 Agent 工具：

| 智能体 | 输入 | 输出 | model | run_in_background |
|--------|------|------|-------|-------------------|
| {agent-1} | {数据来源} | `_workspace/{phase}_{agent}_{artifact}.md` | opus | true |
| {agent-2} | {数据来源} | `_workspace/{phase}_{agent}_{artifact}.md` | opus | true |

### Phase 3：结果整合

1. 收集各智能体的返回值；
2. 使用 Read 收集基于文件的产物；
3. 应用整合逻辑生成最终产物。

### Phase 4：收尾

1. 保留 `_workspace/`；
2. 向用户汇报结果。

## 错误处理

- 单个智能体失败：重试一次，若仍失败则在报告中标明缺失部分并继续执行；
- 多数智能体失败：通知用户并确认是否继续执行；
- 超时：使用现有部分结果继续执行。
```

---

## 模板 C：混合模式

在不同 Phase 使用不同执行模式。每个 Phase 顶部必须标明 `**执行模式：{团队 | 子智能体}`。

```markdown
---
name: {domain}-orchestrator
description: "{领域} 混合模式编排器。{关键词}。包含后续工作关键词。"
---

## 执行模式：混合

| Phase | 模式 | 理由 |
|-------|------|------|
| Phase 2（并行收集） | 子智能体 | 只需独立收集数据，无需团队通信 |
| Phase 3（基于共识的整合） | 智能体团队 | 需要围绕冲突数据进行讨论与达成共识 |
| Phase 4（独立验证） | 子智能体 | 由单一 QA 智能体进行客观验证 |

## 工作流

### Phase 2：并行数据收集

**执行模式：子智能体**

在单一消息中并行调用多个 Agent 工具（`run_in_background: true`）。每个结果保存到 `_workspace/02_{agent}_raw.md`。

### Phase 3：基于共识的整合

**执行模式：智能体团队**

1. 使用 `TeamCreate` 组建整合团队（如 editor + fact-checker + synthesizer）；
2. 使用 `TaskCreate` 分配任务 —— 所有成员 Read `_workspace/02_*` 文件；
3. 成员之间通过 SendMessage 讨论冲突数据，并以文件为基础形成共识方案；
4. 生成统一整合稿 `_workspace/03_integrated.md`；
5. 使用 TeamDelete 销毁团队。

### Phase 4：独立验证

**执行模式：子智能体**

调用单一 QA 子智能体，以 `_workspace/03_integrated.md` 作为输入生成验证报告。
```

**混合模式切换规则：**

- 团队 → 子智能体：必须先通过 `TeamDelete` 清理团队，然后再调用 Agent 工具；
- 子智能体 → 团队：需将子智能体生成的文件产物路径传递给团队成员，作为 Read 输入；
- 团队 → 团队：先清理旧团队，再通过新的 `TeamCreate` 创建新团队（每个会话仅允许一个激活团队）。

---

## 编写原则

1. **先明确执行模式** —— 在编排器顶部声明 "智能体团队" / "子智能体" / "混合模式"。若为混合模式，则必须提供 Phase 与模式对应表。
2. **团队模式下必须具体说明 TeamCreate/SendMessage/TaskCreate 用法** —— 包括团队构成、任务注册、通信规则等。
3. **子智能体模式下必须完整标注 Agent 工具参数** —— 包括 name、subagent_type、prompt、run_in_background、model。
4. **文件路径必须明确** —— 使用 `_workspace/` 下的绝对式相对路径（避免模糊位置）。
5. **Phase 间依赖关系要清楚** —— 特别是在混合模式中，明确各 Phase 之间的产物流动与模式切换点。
6. **错误处理要贴近现实** —— 不假设“所有步骤都成功”。
7. **必须包含测试场景** —— 至少一个正常流程和一个错误流程。

## 在 description 中加入后续工作关键词

编排器的 description 若只包含首次执行关键词远远不够，必须加入以下后续工作表达：

- 再次执行/重新运行/更新/修改/补充；
- “仅重新执行 {领域} 的 {部分内容}”；
- “基于之前结果”“提升当前结果”；
- 与领域相关的日常请求表达（例如：用于“发布策略”的哈尼斯，应包含“发布”“宣传”“热度”等词）。

若缺少后续关键词，编排器在首次运行后将难以再次被触发，形同“死代码”。

## 实际编排器参考

扇出/扇入模式下编排器的典型结构为：准备 → Phase 0（上下文检查） → TeamCreate + TaskCreate → 多成员并行执行 → Read + 整合 → 收尾。

可参考 `references/team-examples.md` 中的调研团队示例。
