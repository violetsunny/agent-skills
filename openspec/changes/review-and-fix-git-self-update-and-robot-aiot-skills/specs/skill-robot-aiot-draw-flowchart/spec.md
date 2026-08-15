## Purpose

定义 robot-aiot-draw-flowchart skill 的独立/被调用场景行为区分、文档内容准确性和跨 skill 兼容缺口标注的行为契约。

## MODIFIED Requirements

### Requirement: FAQ 编号顺序正确
SKILL.md「常见问题」章节 SHALL 按 Q1→Q2→Q3→Q4→Q5→Q6 的顺序排列，不得存在编号乱序。

#### Scenario: FAQ 顺序无误
- **WHEN** 读者按顺序阅读 FAQ
- **THEN** 编号从 Q1 连续递增到 Q6，无跳号或乱序

### Requirement: 独立使用与被工作流调用场景行为有区分
步骤 5（文件保存/上传）和验证清单中的 OSS 上传项 SHALL 区分"独立使用"和"被 robot-aiot-leadership-ppt-workflow 调用"两种场景的不同行为。

#### Scenario: 被工作流调用时跳过 OSS 上传
- **WHEN** draw-flowchart 被 leadership-ppt-workflow 调用
- **THEN** 步骤 5 说明跳过 OSS 上传，直接返回本地 doc-ppt/*.xml 路径

#### Scenario: 独立使用时执行 OSS 上传
- **WHEN** draw-flowchart 独立使用
- **THEN** 步骤 5 执行 OSS 上传并返回链接，验证清单要求上传完成

### Requirement: description 定位准确
SKILL.md frontmatter 的 description 字段 SHALL 反映实际使用场景（机器人/IoT 业务图表），不得使用过窄的"扫地机器人"定位。

#### Scenario: description 触发范围准确
- **WHEN** skill 路由系统匹配"领导汇报架构图"场景
- **THEN** 该 skill 被正确触发，description 不会因过窄定位而被排除

### Requirement: PPT 场景默认色显式对齐声明
references/color-schemes.md SHALL 标注 PPT 领导汇报场景的默认主色与 page-html-template.md 的 `--primary-color` 对齐。

#### Scenario: 配色对齐有文档依据
- **WHEN** 读者查阅 PPT 场景配色
- **THEN** color-schemes.md 中有明确声明"PPT 场景默认主色 #0078D4 与 page-html-template.md CSS 变量对齐"

### Requirement: mxgraph.flowchart.* 形状兼容缺口已标注
SKILL.md 和 flowchart-patterns.md 中涉及 `mxgraph.flowchart.*` 命名空间形状的位置 SHALL 标注该系列形状在 robot-aiot-xml-html-bridge 映射表中无对应 CSS 的已知缺口。

#### Scenario: 兼容缺口有文档警告
- **WHEN** 读者使用并行流程图（含 merge_or_storage 形状）后进行 XML→HTML 转换
- **THEN** 已提前被文档告知此类形状会触发未映射属性警告，是已知缺口

### Requirement: HTML 输出需通过 xml-html-bridge + MD3 规范
如需将图表 XML 转为 HTML，SHALL 通过 robot-aiot-xml-html-bridge 进行转换，且最终 HTML 须符合 Material Design 3 规范。

#### Scenario: 图表转 HTML 走规范路径
- **WHEN** 上游工作流需要将 draw-flowchart 输出转为 HTML
- **THEN** 文档说明必须经由 xml-html-bridge 转换，且结果须符合 MD3 规范
