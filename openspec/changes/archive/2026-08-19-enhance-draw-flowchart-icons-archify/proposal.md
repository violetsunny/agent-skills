## Why

实际使用 robot-aiot-draw-flowchart 画图时暴露两个能力缺口：(1) `references/robot-icons.md` 现有图标均为简笔风格，缺少 draw.io「Smart Home / IoT Devices」形状库中那种精细产品插画风格的扫地机器人（用户截图样式：浅灰机身、白色内盘、绿色电源键、蓝色 LDS 塔、蓝色回充键、黑色三叉边刷、灰尘粒子），用户希望该样式可复用；(2) 本 SKILL 仅输出 draw.io XML，缺少 archify SKILL 提供的高保真 HTML/SVG 输出、暗/亮主题切换、多格式导出与布局校验能力，图的专业度和交付形态受限。

## What Changes

- 在 `references/robot-icons.md` 新增「产品插画风格（详细俯视）」图标变体：纯 draw.io 矢量 mxCell 组合（不依赖 PNG/base64），复刻截图中的机身、内盘、LDS、控制键、边刷、灰尘粒子等视觉元素，并附使用提示
- 新增 `references/archify-integration.md`：定义 draw.io XML 与 archify HTML/SVG 两种输出路径的选型指南、图表类型到 archify 五种渲染模式（architecture/workflow/sequence/dataflow/lifecycle）的映射、Mermaid 输入方言的委托方式
- 将 archify 的布局叙事原则（单一主路径、少标签边、短侧分支、细节入卡片）与自审清单思想，适配为 draw.io XML 的布局与交付前检查规范，纳入 SKILL.md
- 更新 SKILL.md：核心能力与工作流程中暴露 archify 高保真输出路径，版本升级
- 源文件（`~/.agents/skills/`）修改后同步至项目知识库副本（`agent-skills/skills/`），不执行 git 操作

## Capabilities

### New Capabilities
- `robot-icon-library`: 机器人图标库能力—— standardized 矢量图标变体集合，含产品插画风格详细俯视图标的结构、配色与使用约束
- `diagram-output-paths`: 图表输出路径能力—— draw.io XML 与 archify HTML/SVG 双输出选型、模式映射、布局叙事原则与交付前自审规范

### Modified Capabilities
（无既有 specs，留空）

## Impact

- 文件：`references/robot-icons.md`（新增图标节）、`references/archify-integration.md`（新建）、`SKILL.md`（能力/工作流/版本）、知识库副本同步
- 依赖：archify SKILL 作为外部委托目标（不 vendor 其代码），关系类似现有 robot-aiot-xml-html-bridge
- 无 BREAKING 变更：现有图标 1-9 与 draw.io XML 主路径保持不变
