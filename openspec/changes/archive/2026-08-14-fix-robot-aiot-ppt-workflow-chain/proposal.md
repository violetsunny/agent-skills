## Why

robot-aiot-leadership-ppt-workflow 链路存在两个高严重度能力断裂：
1. `robot-aiot-xml-html-bridge` 只有方法论，无实际转换机制——"确定性渲染路径"是空话，没有 scripts/ 或 references/，agent 执行时无法落地
2. `ppt-master` 没有 HTML 输入路由（其生成路线是 SVG-based），但 leadership workflow 声称"逐页 HTML 是 PPT 还原的第一参照物"，导致 Phase 5 依赖一个不存在的能力

这两个断裂意味着当前 workflow 从 Phase 3.5 到 Phase 5 无法稳定执行。

## What Changes

- **新增 `robot-aiot-xml-html-bridge` 的 `references/` 转换规范**：定义 draw.io mxCell 样式到 CSS 的映射规则、坐标驱动 HTML 的生成方法、连线/泳道/分层容器的 HTML 等价表达方式，让"结构映射路径"从空话变成可执行步骤
- **新增 `robot-aiot-xml-html-bridge` 的 `scripts/` 转换脚本**：提供确定性 XML→HTML 转换脚本，解析 mxfile/mxGraphModel，输出固定画布尺寸的坐标驱动 HTML
- **修正 `robot-aiot-leadership-ppt-workflow` Phase 5 的 ppt-master 交接契约**：明确 HTML 是"视觉参照"而非 ppt-master 的直接输入格式；定义 agent 如何将页面 HTML 映射为 ppt-master 支持的 SVG 页面设计
- **补充 `robot-aiot-leadership-ppt-workflow` Phase 4 的页面 HTML 模板**：在 references/ 中提供单页 HTML 模板，固定 16:9 画布、标题区/结论区/图表区/数据区/备注区布局比例，减少 agent 手写 HTML 时的不确定性
- **定义单一真源与重生顺序规则**：明确数据变更时的重生链——母稿 MD 改动 → 图表 XML 重生 → 图表 HTML 重生 → 页面 HTML 重生，不允许跳步或只手改下游产物
- **修正 `robot-aiot-draw-flowchart` 标题**：从"扫地机器人业务流程图绘制 Skill"改为通用表述，与 description 中"通用技术能力"保持一致

## Capabilities

### New Capabilities
- `xml-html-bridge-conversion`: draw.io/mxGraph XML 到 HTML 的确定性转换能力，包括样式映射、坐标驱动布局、保真校验
- `leadership-ppt-page-template`: 领导汇报 PPT 逐页 HTML 模板规范，固定画布比例和区域布局

### Modified Capabilities
（无现有 spec 需要修改——这些 skill 目录下目前没有 openspec/specs/ 中的既有 capability spec）

## Impact

- **`~/.agents/skills/robot-aiot-xml-html-bridge/`**：新增 `references/xml-html-mapping.md` 和 `scripts/xml_to_html.py`
- **`~/.agents/skills/robot-aiot-leadership-ppt-workflow/`**：修正 Phase 5 交接契约，新增 `references/page-html-template.md`，补充真源重生顺序规则
- **`~/.agents/skills/robot-aiot-draw-flowchart/SKILL.md`**：标题修正（低优先级）
- **不改动 `ppt-master`**：本 change 不修改 ppt-master 技能本身，只修正 leadership workflow 对其能力的假设和交接方式
