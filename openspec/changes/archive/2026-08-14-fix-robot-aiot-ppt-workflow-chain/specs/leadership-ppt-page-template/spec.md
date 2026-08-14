## Purpose

为领导汇报 PPT 工作流提供逐页 HTML 页面模板规范，固定 16:9 画布比例和标题区/结论区/图表区/数据区/备注区的布局，减少 agent 手写 HTML 时的不确定性，确保每页 HTML 可直接映射到 PPT 幻灯片。

## ADDED Requirements

### Requirement: 固定画布比例

页面 HTML 模板 SHALL 使用固定 16:9 画布尺寸（1280x720px），不允许响应式布局。每个 HTML 文件只表达一页幻灯片内容。

#### Scenario: 画布尺寸固定

- **WHEN** agent 使用页面 HTML 模板生成单页 HTML
- **THEN** HTML 画布容器的 CSS 尺寸 MUST 为 `1280px x 720px`，不使用 `max-width`、`width:100%` 或媒体查询

### Requirement: 五区域布局

页面 HTML 模板 SHALL 定义五个固定区域：标题区、结论区、图表区、数据区、备注区。每个区域的位置和尺寸比例 MUST 在模板中预定义。

#### Scenario: 标题区位置

- **WHEN** agent 填充页面 HTML 模板
- **THEN** 标题区 MUST 位于画布顶部，高度占比不超过画布的 15%

#### Scenario: 图表区与数据区共存

- **WHEN** 页面同时包含图表和数据表
- **THEN** 图表区和数据区 MUST 左右分列或上下分层，各有独立边界，不重叠

#### Scenario: 备注区位置

- **WHEN** 页面包含汇报话术
- **THEN** 备注区 MUST 位于画布底部，高度占比不超过画布的 10%，且文字大小小于正文

### Requirement: 图表嵌入约束

页面 HTML 中的图表区域 SHALL 引用 `robot-aiot-xml-html-bridge` 生成的图表 HTML，不允许在页面 HTML 中重新绘制一份不同风格的图表。

#### Scenario: 引用图表 HTML

- **WHEN** 页面需要展示分层架构图
- **THEN** 图表区 MUST 嵌入或引用 `doc-ppt/<图表名>.html` 的内容，不自造替代图表

#### Scenario: 禁止风格偏离

- **WHEN** 图表 HTML 使用科技蓝主题色
- **THEN** 页面 HTML 中嵌入的图表 MUST 保持科技蓝主题色，不改为其他配色

### Requirement: 配色体系统一

页面 HTML 的配色 SHALL 参照首页架构图确立的视觉基调。后续页面在保持配色体系统一的前提下，可采用多种数据可视化样式。

#### Scenario: 配色继承

- **WHEN** 首页架构图使用科技蓝 (#0078D4) 为主色
- **THEN** 后续页面的标题区、强调色、图表主色 MUST 使用同一色系或其衍生色

### Requirement: 数据一致性锚定

页面 HTML 中的所有数据值 SHALL 与母稿 MD 中的数据池完全一致。页面 HTML 不得包含数据池中不存在的数字。

#### Scenario: 数据池引用

- **WHEN** 母稿数据池中"设备规模"为 85.8万台
- **THEN** 页面 HTML 中该指标显示值 MUST 为"85.8万台"，不得为其他数值

#### Scenario: 估算值标记保留

- **WHEN** 数据池中某值为估算值（带 `~` 前缀）
- **THEN** 页面 HTML 中该值 MUST 保留 `~` 前缀标记
