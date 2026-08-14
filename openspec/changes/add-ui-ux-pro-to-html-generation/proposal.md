## Why

当前 `robot-aiot-leadership-ppt-workflow` 和 `robot-aiot-xml-html-bridge` 在生成 HTML 时没有 UI/UX 设计规范约束——图表 HTML 只做坐标驱动的保真转换，页面 HTML 只做五区域布局，两者都缺少配色一致性、字体层级、间距系统、图表可读性等方面的专业 UI 规范。`ui-ux-pro-max` 技能正好提供了 84 种样式、192 套配色、74 套字体配对、25 种图表类型和 98 条 UX 准则的可搜索数据库，将其引入 HTML 生成环节可以让汇报图表和页面在视觉质量上从"能看"提升到"专业"。

## What Changes

- **在 `robot-aiot-xml-html-bridge` 中引入 `ui-ux-pro-max` + `material-3` 参考规范**：在 Phase 3 生成 HTML 桥接稿前，先加载 `ui-ux-pro-max` 的配色、字体、图表设计规范，同时加载 `material-3/references/` 的 MD3 配色角色、字体梯度、8dp 间距系统作为补充参考，确保转换后的图表 HTML 在视觉专业性上达标
- **在 `robot-aiot-leadership-ppt-workflow` 中引入 `ui-ux-pro-max` + `material-3` 参考规范**：在 Phase 4 逐页 HTML 化前，先调用 `ui-ux-pro-max` 的 `--design-system` 生成设计系统，同时加载 `material-3/references/` 的布局和间距规范作为补充参考，将配色方案、字体配对、间距系统注入页面 HTML 模板的 CSS 变量中
- **更新 `page-html-template.md`**：模板的配色变量从硬编码默认值改为引用 `ui-ux-pro-max` 设计系统输出，间距系统参考 MD3 的 8dp 间距 token
- **新增 UI 规范校验项**：在两个技能的验证清单中增加配色一致性、字体层级、间距规范的校验

## Capabilities

### New Capabilities
- `ui-ux-html-integration`: 将 `ui-ux-pro-max` 设计规范和 `material-3` MD3 参考规范集成到 PPT 工作流 HTML 生成环节的能力，包括图表 HTML 的样式规范约束和页面 HTML 的设计系统注入

### Modified Capabilities
- `xml-html-bridge-conversion`: 新增 UI 规范约束要求——转换后的 HTML 须符合 `ui-ux-pro-max` 的配色对比度、字体层级和图表可读性准则，并参考 `material-3` 的 MD3 配色角色和字体梯度
- `leadership-ppt-page-template`: 页面 HTML 模板的配色变量从硬编码改为引用 `ui-ux-pro-max` 设计系统输出，间距系统参考 MD3 8dp 间距 token

## Impact

- **`~/.agents/skills/robot-aiot-xml-html-bridge/SKILL.md`**：Phase 3 新增加载 `ui-ux-pro-max` + `material-3` 参考步骤，验证清单新增 UI 规范校验项
- **`~/.agents/skills/robot-aiot-leadership-ppt-workflow/SKILL.md`**：Phase 4 新增调用 `ui-ux-pro-max --design-system` + 加载 `material-3` 参考步骤，模板引用改为动态注入
- **`~/.agents/skills/robot-aiot-leadership-ppt-workflow/references/page-html-template.md`**：配色变量定义改为引用设计系统输出，间距系统参考 MD3 8dp token
- **`~/.agents/skills/robot-aiot-xml-html-bridge/references/xml-html-mapping.md`**：新增 UI 规范映射补充说明
- **不修改 `ui-ux-pro-max` 和 `material-3` 本身**：只调用其搜索能力 / 加载其参考文档，不改变其内部结构
