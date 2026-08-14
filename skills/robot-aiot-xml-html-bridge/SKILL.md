---
name: robot-aiot-xml-html-bridge
description: >
  将 robot-aiot-draw-flowchart 或其他 draw.io / mxGraph XML 图表稳定转换为 HTML 预览稿，
  并尽可能保留原始样式、布局、层级、配色、尺寸比例与文本关系。
  当用户要求"XML转HTML"、"draw.io转HTML"、"mxGraph转HTML"、"图表转网页预览"、
  "先转HTML再转PPT"、"保留原样式输出HTML"时触发。也适用于领导汇报 PPT 工作流中，
  需要在 PPT 生成前先落一层 HTML 作为页面主约束的场景。
---

# Robot AIoT XML 到 HTML 桥接工作流

本技能的目标不是"重新设计一张网页"，而是把既有 XML 图表稳定落成 HTML 预览稿，
让后续 PPT 生成有一个**可检查、可对比、可冻结**的视觉约束层。

核心原则：

1. **先保真，后可用**：HTML 首先要忠实表达 XML 的视觉结果，而不是追求网页感
2. **HTML 是桥接层，不是二次设计稿**：不能借转换之名改风格、改结构、改信息层级
3. **无稳定转换就不继续**：如果当前路径只能"近似画一个差不多的网页"，则必须阻塞，而不是带着漂移结果进入 PPT 阶段

---

## 适用输入

- `robot-aiot-draw-flowchart` 生成的 `.xml`
- 标准 draw.io / diagrams.net `mxfile` XML
- 其他结构兼容的 `mxGraphModel` 图表 XML

## 标准输出

每个输入 XML 至少对应两个输出物：

1. `doc-ppt/<name>.xml`：原始真源，不可被 HTML 反向覆盖
2. `doc-ppt/<name>.html`：HTML 预览稿，作为后续页面编排和 PPT 还原的视觉约束输入

如需页面级整合，可继续由上游 workflow 把多个图表 HTML 嵌入到 `doc-ppt/pages/*.html`。

---

## 不变式

转换过程中必须保留以下属性：

1. 节点相对位置
2. 容器层级关系
3. 主色、边框色、文字色
4. 文字内容、强调关系、字号层级
5. 连线方向、箭头关系、泳道/分层边界
6. 图例、数据锚点、标签位置
7. 宽高比例、留白关系、整体信息密度

以下行为默认禁止：

1. 把 XML 图表改造成新的卡片式网页布局
2. 擅自增删节点、文案、数值、图例、连接线
3. 因为 HTML 不好实现就删掉特殊样式或退化成普通文本列表
4. 手工调整 HTML 但不回写变更来源，造成 XML/HTML 漂移

---

## 工作流

### Phase 1: 识别 XML 结构

先确认输入是否为可稳定转换的 draw.io / mxGraph XML：

- 是否存在 `mxfile`
- 是否存在 `diagram`
- 是否存在 `mxGraphModel`
- 是否存在 `root` / `mxCell`

如果不满足，先告诉调用方这不是本技能支持的 XML 结构，不要盲目生成 HTML。

### Phase 2: 选择稳定转换路径

优先级如下：

1. **确定性渲染路径**：使用 `scripts/xml_to_html.py` 脚本执行转换，配合 `references/xml-html-mapping.md` 中的样式映射表。这是默认首选路径——脚本用标准库 `xml.etree.ElementTree` 解析 XML，按映射表确定性生成坐标驱动 HTML，不依赖 AI 即兴发挥
2. **手工映射降级路径**：若目标环境无 Python，agent 可按 `references/xml-html-mapping.md` 中的映射规则手工将 mxCell 样式翻译为 CSS，但必须逐项对照映射表，不可跳过或自创规则
3. **人工近似路径禁止直接放行**：如果只能"肉眼照着重画"，该结果不能作为 PPT 主约束输入

调用脚本示例：
```bash
python3 scripts/xml_to_html.py doc-ppt/<图表名>.xml -o doc-ppt/<图表名>.html
```

选择原则：

- 只要存在确定性脚本路径，就不要使用人工重排路径
- 若无稳定路径，必须明确阻塞，并说明缺少哪种解析/渲染能力

### Phase 3: 生成 HTML 桥接稿

#### 步骤 0: 加载 UI 设计参考

在执行样式映射前，先加载以下 UI 设计规范作为补充参考：

1. **加载 `ui-ux-pro-max` 准则**：读取 `ui-ux-pro-max` 的 `references/quick-reference.md` 中 §6（Typography & Color）和 §10（Charts & Data）准则，作为配色对比度和图表可读性的补充约束
2. **加载 `material-3` MD3 配色角色**：读取 `material-3/references/color-system.md`，参考 MD3 的 primary/secondary/tertiary 配色角色定义来理解图表中的色彩层级关系
3. **加载 `material-3` MD3 字体梯度**：读取 `material-3/references/typography-and-shape.md`，参考 MD3 Type Scale（Display/Headline/Title/Body/Label 五类）来理解字体层级梯度标准

这些参考不改变 `xml-html-mapping.md` 中的确定性映射规则，仅作为 Phase 4 保真校验中 UI 规范补充检查的依据。如参考文件路径不可用，agent 可跳过此步骤，不影响确定性转换流程。

#### 步骤 1: 生成 HTML 结构

HTML 桥接稿推荐具备以下结构：

```html
<html>
  <head>
    <style>
      /* 固定画布尺寸、颜色变量、节点/连线/标签样式 */
    </style>
  </head>
  <body>
    <div class="diagram-canvas">
      <!-- 容器 -->
      <!-- 节点 -->
      <!-- 标签 -->
      <!-- 连线或等价表示 -->
    </div>
  </body>
</html>
```

要求：

1. 使用固定画布尺寸，避免响应式改版导致布局漂移
2. 采用显式坐标或等价布局约束，保证节点位置稳定
3. 颜色、边框、字体、间距均来自 XML 样式映射，不自行换皮
4. 如原图存在分层区块、泳道、数据卡片、图例，必须逐项落地

### Phase 4: 保真校验

生成 HTML 后，必须做最少一轮保真校验。`scripts/xml_to_html.py` 的 `verify_fidelity()` 会自动执行以下校验并输出结构化报告：

1. **Vertex 数量校验**：HTML 中定位元素数量与 XML vertex 数量一致，不一致时非零退出
2. **Edge 数量校验**：HTML 中 SVG `<line>` 元素数量与 XML edge 数量一致，不一致时非零退出
3. **文本内容校验**：对每个 vertex 的 value 做 HTML 转义后检查是否出现在 HTML 输出中，缺失时标记 vertex ID 和预期文本
4. **未映射样式属性报告**：列出所有映射表未定义的 style 属性名和值，不阻塞转换但标记为需人工确认
5. 核对主要容器/泳道/层级数量是否一致
6. 核对主视觉配色是否一致
7. 核对整体相对布局是否一致

校验报告输出格式：
```
--- Fidelity Report ---
  Vertices: N
  Edges: M
  Text: all matched / N missing
  Unmapped: N
  Result: PASS / FAIL
```

如果发生以下情况，结果不能进入 PPT 阶段：

1. 节点缺失
2. 连线语义丢失
3. 图例或数据锚点缺失
4. 分层/泳道边界消失
5. 页面比例明显变化

#### UI 规范补充检查（非阻塞）

保真校验通过后，额外执行以下 UI 规范检查。这些检查基于 Phase 3 步骤 0 加载的 `ui-ux-pro-max` 准则和 `material-3` MD3 参考规范，不通过时标记 `[UI-WARN]` 警告，**不阻塞转换流程**（保真校验仍为唯一阻塞门）：

1. **配色对比度**：检查图表 HTML 中各节点文字色与背景色的对比度，低于 4.5:1（WCAG 标准）时标记 `[UI-WARN]`，建议调整文字色或背景色
2. **字体层级梯度**：检查图表 HTML 中多个文字层级（标题、标签、数据锚点）的 font-size 是否形成清晰梯度，相邻层级差值低于 2px 时标记 `[UI-WARN]`。参考 MD3 Type Scale 五类（Display/Headline/Title/Body/Label）的梯度划分
3. **图表可读性**：检查图表 HTML 中的数据表格或看板卡片，行高低于 32px 或卡片内边距低于 12px 时标记 `[UI-WARN]`

agent 看到 `[UI-WARN]` 警告后可自行决定是否调整，不影响 HTML 交付。

### Phase 5: 交付与冻结

交付时应明确：

1. XML 是图表真源
2. HTML 是 PPT 前的视觉约束层
3. 若 XML 后续变更，HTML 必须整稿重生，不能只手改 HTML

推荐在输出说明中附带：

```markdown
- 图表真源：doc-ppt/<name>.xml
- 图表 HTML：doc-ppt/<name>.html
- 状态：HTML 已完成，可进入 PPT 页面编排
```

---

## 与其他技能的协作关系

### 与 `robot-aiot-draw-flowchart`

- `robot-aiot-draw-flowchart` 负责产出图表 XML
- 本技能负责把 XML 转成 HTML 桥接稿
- 不要把 XML->HTML 能力写回 `robot-aiot-draw-flowchart`，避免边界混乱

### 与 `robot-aiot-leadership-ppt-workflow`

- 本技能处于 `draw-flowchart` 和 `ppt-master` 之间
- 没有完成 HTML，不允许进入 PPT 生成
- 页面级 `doc-ppt/pages/*.html` 可以引用本技能输出的图表 HTML

### 与 `ppt-master`

- 本技能不负责生成最终 PPTX
- 本技能只负责提供稳定、可审查、可冻结的 HTML 约束输入
- 若后续存在专门的 HTML->PPT 技能，则本技能的输出应作为其直接输入

---

## 验证清单

- [ ] 输入 XML 为支持的 draw.io / mxGraph 结构
- [ ] 输出 HTML 与 XML 一一对应
- [ ] Vertex 数量一致
- [ ] Edge 数量一致
- [ ] 文本内容一致
- [ ] 容器/泳道/层级结构一致
- [ ] 关键标签、图例、数据锚点一致
- [ ] 主色、边框色、字体层级未漂移
- [ ] 画布比例和相对布局未漂移
- [ ] 未映射样式属性已人工确认
- [ ] 配色对比度达标（文字与背景对比度 ≥ 4.5:1，不达标项已标记 `[UI-WARN]`）
- [ ] 字体层级梯度清晰（相邻层级 font-size 差值 ≥ 2px，参考 MD3 Type Scale 五类）
- [ ] 图表可读性达标（表格行高 ≥ 32px，卡片内边距 ≥ 12px，不达标项已标记 `[UI-WARN]`）
- [ ] 已声明 XML 为真源，HTML 为桥接约束层
- [ ] 若 XML 变更，HTML 需整稿重生的规则已声明

若以上任一关键项不满足，不要宣称"已可进入 PPT 阶段"。
