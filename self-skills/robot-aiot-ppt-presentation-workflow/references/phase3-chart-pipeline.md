# Phase 3-3.5: 图表生成、桥接转换与确认门 G2

图表链路分三步：按已确认母稿产出 XML 真源 → 产出 HTML 桥接稿 → 用户确认（G2）。

前置条件：Phase 2 确认门 G1 已通过，母稿已冻结。仅生成母稿"图表需求总表"中标记的图表，不得自行加图、减图或改动图表语义。

## Phase 3: 调用 robot-aiot-draw-flowchart

### 选型

1. 分层架构图：系统架构展示、多模块分层说明，推荐用作首页主视觉
2. 泳道流程图：多角色协作流程
3. 线性/分支流程图：单链路流程
4. 循环流程图：重试机制、治理闭环

### 执行要求

1. 使用 `skill` 工具加载 `robot-aiot-draw-flowchart`
2. 按需读取其 `references/layered-architecture.md` 或 `references/flowchart-patterns.md`
3. 图表表达的是业务能力和治理闭环，不是底层技术部署拓扑
4. 图表底部补 2-3 个数据锚点，保持与数据池一致
5. 图表为**静态呈现**：不含动画、交互、hover 效果（PPT 母稿规范，见 `phase2-manuscript.md`）
6. 首页架构图确立全局主色系，后续页面在统一配色下允许展示风格多样性

### Sub Agent 建议

1. 先用 fresh sub agent 按母稿图表需求总表规划图表类型、节点分层、数据锚点和页面用途，再由主线程正式调用 `robot-aiot-draw-flowchart`
2. XML→HTML 桥接后的保真校验也优先交给独立 sub agent 扫描，避免页面写作上下文干扰图表审查
3. 主线程负责判定图表 HTML 是否通过、是否允许发起 G2 确认

### 产物

输出到 `doc-ppt/flow/`（图表类产物统一落 `flow/` 子目录）：

```markdown
- 图表真源：`doc-ppt/flow/<图表文件名>.xml`
- 图表状态：Phase 3 已完成，待进入 Phase 3.5 转换
```

## Phase 3.5: XML→HTML 桥接 + 确认门 G2

### 桥接执行要求

1. 继续使用已加载的 `robot-aiot-draw-flowchart`，调用其 XML→HTML 桥接能力
2. 对每个 `.xml` 生成对应 `.html`
3. 校验 HTML 保留 XML 的样式、布局、层级、比例和关键标签关系

### 确认门 G2（阻塞性）

1. 全部图表 HTML 产出并通过保真校验后，向用户逐张出示（浏览器直接打开 `flow/<chart-name>.html`），附图表清单：图表名 / 类型 / 服务的母稿页码 / 核心信息
2. 用户确认"图表无误" → 进入 Phase 4 回写；确认前不得开始回写与逐页 HTML
3. 用户提出修改 → 改 XML 真源 → 该图表 HTML 整稿重生 → 重新送审；禁止只改 HTML 不改 XML
4. 修改波及母稿内容（图表表达的结论/数据变化）→ 回 Phase 2 修订母稿并重过 G1
5. 用户明确要求跳过 G2 时：把用户的明确指令记入母稿头部后方可继续，不得静默跳过

### 阻塞规则

1. G1 未过，不允许开始 Phase 3
2. 没有完成图表 HTML，不允许发起 G2
3. G2 未过，不允许进入 Phase 4（回写与逐页 HTML）
4. 图表 HTML 与 XML 视觉不一致，不允许进入 Phase 5
5. XML 改动后，关联图表 HTML 必须整稿重生，且重新过 G2

### 产物

```markdown
- 图表真源：`doc-ppt/flow/<图表文件名>.xml`
- 图表 HTML：`doc-ppt/flow/<图表文件名>.html`
- 确认状态：G2 已通过（待 Phase 4 回写母稿图表需求总表）
```

页面 HTML 落 `doc-ppt/pages/`，页面引用图表用 `../flow/<图表文件名>.html` 相对路径。
