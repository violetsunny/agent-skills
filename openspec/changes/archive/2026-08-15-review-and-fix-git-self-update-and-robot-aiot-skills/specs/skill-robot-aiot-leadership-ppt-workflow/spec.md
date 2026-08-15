## Purpose

定义 robot-aiot-leadership-ppt-workflow skill 的执行路径无歧义、跨 skill 调用边界清晰、HTML 生成强制规范的行为契约。

## MODIFIED Requirements

### Requirement: Phase 5 执行路径唯一
leadership-ppt-workflow 的 Phase 5 SHALL 描述唯一的 ppt-master 调用路径（以逐页 HTML/MD 为输入），不得同时存在"agent 手写 SVG"和"ppt-master 读 MD"两种矛盾说法。

#### Scenario: Phase 5 无歧义路径
- **WHEN** agent 执行到 Phase 5
- **THEN** 文档中有且仅有一条执行路径描述，agent 无需判断走哪条

### Requirement: 技术命名检查通用化
Phase 4 的技术命名过滤规则 SHALL 使用通用描述，不得硬编码具体业务表名。

#### Scenario: 检查规则不含硬编码表名
- **WHEN** agent 执行 Phase 4 技术命名检查
- **THEN** 检查对象为通用技术命名类别（数据库表名、Java 类名、内部 API 路径等），而非特定表名

### Requirement: 不越界描述被调用 skill 的落盘行为
leadership-ppt-workflow 调用 draw-flowchart 时，对其文件输出路径的描述 SHALL 以引用方式注明来源（"见 draw-flowchart SKILL.md 步骤 5"），不得在本 skill 中重复规定对方的落盘路径。

#### Scenario: 路径描述以引用为准
- **WHEN** 读者查阅 Phase 3 中的文件落盘说明
- **THEN** 描述为"由 robot-aiot-draw-flowchart 输出（见其 SKILL.md 步骤 5）"而非直接规定路径

### Requirement: HTML 生成强制走 ui-ux-pro-max + MD3
所有逐页 HTML 生成 SHALL 通过 ui-ux-pro-max skill 驱动，并严格符合 Material Design 3 规范，不得绕过。

#### Scenario: Phase 4 HTML 生成入口有强制声明
- **WHEN** agent 进入 Phase 4 逐页 HTML 生成环节
- **THEN** 文档在步骤入口处有明确的强制声明，包含 ui-ux-pro-max 和 MD3 规范要求

### Requirement: ui-ux-pro-max 调用方式有说明
Phase 4 设计系统生成步骤 SHALL 说明如何触发 `ui-ux-pro-max --design-system`（使用 Skill 工具加载）。

#### Scenario: 首次执行 agent 知道如何触发
- **WHEN** agent 首次执行 Phase 4 设计系统生成步骤
- **THEN** 文档中有明确的触发方式说明，不产生"这是什么工具"的歧义

### Requirement: 重生链触发机制有操作说明
「真源与重生顺序」中的每个重生步骤 SHALL 包含触发方式说明。

#### Scenario: XML 重生步骤有操作说明
- **WHEN** 读者查阅重生链中的"图表 XML 重生"步骤
- **THEN** 文档说明该步骤的触发方式为"再次调用 robot-aiot-draw-flowchart"

### Requirement: 多图表场景有循环调用说明
Phase 3.5 SHALL 说明当 PPT 含多张图表时，xml-html-bridge 需被依次调用。

#### Scenario: 多图表场景有明确处理说明
- **WHEN** PPT 包含多张图表
- **THEN** Phase 3.5 文档说明"对每个 .xml 文件依次调用 robot-aiot-xml-html-bridge"

### Requirement: 封面页底部总结例外已文档化
page-html-template.md 中"底部总结不可隐藏"规则 SHALL 标注封面页例外说明。

#### Scenario: 封面页规则无矛盾
- **WHEN** 读者查阅可隐藏区域规则
- **THEN** 规则中明确说明封面页（cover 类型）不含底部总结蓝条，此规则仅适用于内容页
