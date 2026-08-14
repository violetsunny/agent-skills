## MODIFIED Requirements

### Requirement: 配色体系统一

页面 HTML 的配色 SHALL 参照首页架构图确立的视觉基调，并通过 `ui-ux-pro-max` 设计系统补充辅助色和间距系统。后续页面在保持配色体系统一的前提下，可采用多种数据可视化样式。

#### Scenario: 配色继承

- **WHEN** 首页架构图使用科技蓝 (#0078D4) 为主色
- **THEN** 后续页面的标题区、强调色、图表主色 MUST 使用同一色系或其衍生色

#### Scenario: 设计系统注入配色

- **WHEN** `ui-ux-pro-max --design-system` 返回配色方案和字体配对
- **THEN** 页面 HTML 模板的 `:root` CSS 变量 MUST 使用设计系统输出的值作为初始值，首页架构图主色优先覆盖 `--primary-color`

#### Scenario: 间距系统注入

- **WHEN** `ui-ux-pro-max` 设计系统返回间距系统（spacing scale）
- **THEN** 页面 HTML 的区域间距和内边距 MUST 参照该间距系统，不使用随意值
