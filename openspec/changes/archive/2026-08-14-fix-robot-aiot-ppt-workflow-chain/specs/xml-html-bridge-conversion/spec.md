## Purpose

将 draw.io / mxGraph XML 图表确定性转换为固定画布 HTML 预览稿，保留原始样式、坐标布局和视觉层级，作为 PPT 生成前的视觉约束层。

## ADDED Requirements

### Requirement: XML 结构识别与拒绝

系统 SHALL 在转换前验证输入 XML 是否包含 `mxfile`/`diagram`/`mxGraphModel`/`root`/`mxCell` 结构。若不满足，系统 MUST 拒绝转换并返回明确的拒绝原因。

#### Scenario: 标准 draw.io XML 输入

- **WHEN** 输入 XML 包含 `mxfile > diagram > mxGraphModel > root > mxCell` 结构
- **THEN** 系统接受输入并进入转换流程

#### Scenario: 不兼容的 XML 输入

- **WHEN** 输入 XML 不包含 `mxGraphModel` 或 `mxCell` 结构
- **THEN** 系统拒绝转换并返回"不支持的 XML 结构"错误，不生成任何 HTML 文件

### Requirement: mxCell 样式到 CSS 的确定性映射

系统 SHALL 将 draw.io mxCell 的 style 属性确定性映射为 CSS 属性。映射规则 MUST 在 `references/xml-html-mapping.md` 中定义且不可由 agent 即兴发挥。

#### Scenario: 填充色映射

- **WHEN** mxCell style 包含 `fillColor=#0078D4`
- **THEN** 对应 HTML 元素的 CSS `background-color` 为 `#0078D4`

#### Scenario: 透明度映射

- **WHEN** mxCell style 包含 `opacity=60`
- **THEN** 对应 HTML 元素的 CSS `opacity` 为 `0.6`

#### Scenario: 虚线样式映射

- **WHEN** mxCell style 包含 `dashed=1`
- **THEN** 对应 HTML 元素的 CSS `border-style` 为 `dashed`

#### Scenario: 未知样式属性

- **WHEN** mxCell style 包含映射表中未定义的属性
- **THEN** 系统跳过该属性并在校验报告中记录警告，不阻塞转换

### Requirement: 坐标驱动布局

系统 SHALL 使用 mxGeometry 中的 x/y/width/height 值作为 HTML 元素的绝对定位坐标。HTML 画布尺寸 MUST 固定，不可使用响应式布局。

#### Scenario: 节点定位

- **WHEN** mxCell 的 mxGeometry 为 `x=100 y=200 width=120 height=60`
- **THEN** 对应 HTML 元素的 CSS 为 `position:absolute; left:100px; top:200px; width:120px; height:60px`

#### Scenario: 画布尺寸固定

- **WHEN** mxGraphModel 的 pageWidth=1600 pageHeight=1100
- **THEN** HTML 画布容器的 CSS 尺寸固定为 `1600px x 1100px`，不使用 `max-width` 或百分比

### Requirement: 连线等价表达

系统 SHALL 将 mxCell edge 元素等价表达为 HTML 中的视觉连线。连线方向、箭头关系和标签 MUST 保留。

#### Scenario: 带箭头连线

- **WHEN** XML 中存在 edge 元素，source 和 target 分别指向两个 vertex
- **THEN** HTML 中 MUST 存在从 source 位置到 target 位置的视觉连线表示（SVG line 或等价 CSS），且方向正确

#### Scenario: 连线标签保留

- **WHEN** edge 元素的 value 属性非空
- **THEN** HTML 中 MUST 在连线中点或附近显示该标签文本

### Requirement: 容器与泳道层级保留

系统 SHALL 保留 XML 中的 parent-child 容器关系和泳道/分层边界。容器嵌套层级在 HTML 中 MUST 通过视觉边界（边框/背景色）等价表达。

#### Scenario: 分层容器

- **WHEN** XML 中存在多层容器（如分层架构图的 L1~L5）
- **THEN** HTML 中 MUST 存在对应的分层视觉区块，每层有独立的背景色和边框

#### Scenario: 泳道边界

- **WHEN** XML 中存在泳道结构
- **THEN** HTML 中 MUST 存在对应的泳道分隔线和泳道标签

### Requirement: 保真校验

系统 SHALL 在生成 HTML 后执行保真校验，比对 XML 和 HTML 的关键视觉属性。校验不通过时 MUST 阻塞后续流程。

#### Scenario: 节点数量一致

- **WHEN** XML 中有 N 个 vertex 类型 mxCell
- **THEN** HTML 中 MUST 有 N 个对应的定位元素，校验通过

#### Scenario: 节点缺失阻塞

- **WHEN** HTML 中的定位元素数量少于 XML 中的 vertex 数量
- **THEN** 校验失败，系统返回"节点缺失"错误，不允许进入 PPT 阶段

#### Scenario: 关键标签一致

- **WHEN** XML 中某 mxCell 的 value 为"设备接入层"
- **THEN** HTML 中对应的元素文本内容 MUST 包含"设备接入层"

### Requirement: 真源与重生规则

系统 SHALL 声明 XML 为图表真源，HTML 为桥接约束层。XML 变更后 HTML MUST 整稿重生，不允许只手改 HTML。

#### Scenario: XML 变更触发重生

- **WHEN** 图表 XML 文件被修改
- **THEN** 对应的 HTML 文件 MUST 重新生成，不接受手工修改 HTML 来同步变更
