## Purpose

将 `ui-ux-pro-max` 技能的设计规范和 `material-3` 的 MD3 参考规范集成到 PPT 工作流的 HTML 生成环节，确保图表 HTML 和页面 HTML 在视觉专业性上达到 UI/UX 标准。

## ADDED Requirements

### Requirement: 设计系统注入

在生成页面 HTML 前，系统 SHALL 调用 `ui-ux-pro-max` 的 `--design-system` 搜索能力，生成与汇报主题匹配的设计系统（配色方案、字体配对、间距系统），并将输出注入页面 HTML 模板的 CSS 变量中。

#### Scenario: 生成设计系统

- **WHEN** agent 进入 Phase 4 逐页 HTML 化阶段
- **THEN** 系统 MUST 先调用 `ui-ux-pro-max --design-system "<项目描述> <行业> <风格关键词>"` 获取设计系统输出

#### Scenario: 注入 CSS 变量

- **WHEN** `ui-ux-pro-max` 返回设计系统（含 primary color、accent color、font pairing、spacing scale）
- **THEN** 页面 HTML 模板的 `:root` CSS 变量 MUST 使用设计系统输出的值，而非硬编码默认值

#### Scenario: 设计系统与首页架构图配色冲突

- **WHEN** `ui-ux-pro-max` 推荐的主色与首页架构图 XML 确立的主色不一致
- **THEN** 首页架构图的主色 MUST 优先，`ui-ux-pro-max` 的配色作为补充色和辅助色使用

### Requirement: 图表 HTML 视觉规范

`robot-aiot-xml-html-bridge` 在转换 XML 到 HTML 时，SHALL 加载 `ui-ux-pro-max` 的配色对比度、字体层级和图表可读性准则，作为样式映射的补充约束。

#### Scenario: 配色对比度校验

- **WHEN** 转换后的图表 HTML 中某节点文字色与背景色对比度低于 4.5:1
- **THEN** 系统 MUST 在校验报告中标记警告，建议调整文字色或背景色以满足 WCAG 标准

#### Scenario: 字体层级一致性

- **WHEN** 图表 HTML 中存在多个文字层级（标题、标签、数据锚点）
- **THEN** 各层级的 font-size MUST 形成清晰的梯度（如 20px / 16px / 12px），不出现相邻层级差值小于 2px 的情况

#### Scenario: 图表可读性

- **WHEN** 图表 HTML 中包含数据表格或看板卡片
- **THEN** 表格行高 MUST 不低于 32px，卡片内边距 MUST 不低于 12px，确保信息可读

### Requirement: MD3 参考规范加载

在生成 HTML 前，系统 SHALL 加载 `material-3/references/` 中的 MD3 设计规范作为补充参考，包括配色角色（color-system.md）、字体梯度（typography-and-shape.md）和间距系统（layout-and-responsive.md 的 8dp token）。`material-3` 不作为技能调用，仅作为参考文档加载。

#### Scenario: 加载 MD3 配色角色

- **WHEN** agent 进入 HTML 生成环节
- **THEN** agent MUST 读取 `material-3/references/color-system.md`，参考 MD3 的 primary/secondary/tertiary 配色角色定义来组织配色体系

#### Scenario: 加载 MD3 字体梯度

- **WHEN** agent 定义页面 HTML 或图表 HTML 的字体层级
- **THEN** agent MUST 参考 `material-3/references/typography-and-shape.md` 中的 MD3 Type Scale（Display/Headline/Title/Body/Label 五类），确保字体梯度有清晰的类别区分

#### Scenario: 加载 MD3 间距系统

- **WHEN** agent 定义页面 HTML 的区域间距和内边距
- **THEN** agent MUST 参考 `material-3/references/layout-and-responsive.md` 中的 8dp 间距 token 系统，间距值尽量对齐 8dp 倍数（8/16/24/32/48px）

### Requirement: UI 规范校验

两个技能的验证清单 SHALL 包含 UI 规范校验项，在保真校验通过后额外检查视觉规范性。

#### Scenario: 配色一致性校验

- **WHEN** 图表 HTML 和页面 HTML 都已生成
- **THEN** 两者的主色、强调色 MUST 来自同一色系，不出现完全不同的配色体系

#### Scenario: 间距规范校验

- **WHEN** 页面 HTML 的五区域布局已填充内容
- **THEN** 区域间距 MUST 不低于 16px，内边距 MUST 不低于 20px，不出现零间距或负间距
