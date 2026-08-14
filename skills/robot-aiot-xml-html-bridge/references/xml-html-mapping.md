# draw.io mxCell 样式到 CSS 映射表

本表定义 `xml_to_html.py` 在转换 draw.io / mxGraph XML 时使用的确定性样式映射规则。
所有映射必须严格按本表执行，不允许 agent 即兴发挥或自行扩展。

---

## 基础样式映射

| draw.io style 属性 | CSS 属性 | 转换规则 | 示例 |
|---|---|---|---|
| `fillColor` | `background-color` | 直接取色值 | `fillColor=#0078D4` → `background-color: #0078D4` |
| `strokeColor` | `border-color` | 直接取色值 | `strokeColor=#005A9E` → `border-color: #005A9E` |
| `fontColor` | `color` | 直接取色值 | `fontColor=#FFFFFF` → `color: #FFFFFF` |
| `opacity` | `opacity` | 除以 100 转为小数 | `opacity=60` → `opacity: 0.6` |
| `dashed` | `border-style` | `1` → `dashed`，`0` → `solid` | `dashed=1` → `border-style: dashed` |
| `rounded` | `border-radius` | `1` → `8px`，`0` → `0px` | `rounded=1` → `border-radius: 8px` |
| `shadow` | `box-shadow` | `1` → `2px 2px 4px rgba(0,0,0,0.2)`，`0` → `none` | `shadow=1` → `box-shadow: 2px 2px 4px rgba(0,0,0,0.2)` |
| `strokeWidth` | `border-width` | 取数值加 `px` | `strokeWidth=2` → `border-width: 2px` |

## 特殊值处理

| draw.io 特殊值 | 处理方式 |
|---|---|
| `fillColor=none` | 不生成 `background-color`，元素透明 |
| `strokeColor=none` | 不生成 `border-color`，设 `border: none` |
| `fontColor=none` | 不生成 `color`，使用继承色 |
| `opacity=0` | `opacity: 0`（完全透明，但仍占位） |
| `fillColor=#FFFFFF` 或未指定 | 默认白色背景 `background-color: #FFFFFF` |

## 字体样式映射

| draw.io style 属性 | CSS 属性 | 转换规则 |
|---|---|---|
| `fontSize` | `font-size` | 取数值加 `px` |
| `fontStyle=1` | `font-weight` | `bold` |
| `fontStyle=2` | `font-style` | `italic` |
| `fontStyle=4` | `text-decoration` | `underline` |
| `fontStyle=0` | 不生成额外字体样式 | — |
| `align=left` | `text-align` | `left` |
| `align=center` | `text-align` | `center` |
| `align=right` | `text-align` | `right` |
| `verticalAlign=top` | `display:flex; align-items` | `flex-start` |
| `verticalAlign=middle` | `display:flex; align-items` | `center` |
| `verticalAlign=bottom` | `display:flex; align-items` | `flex-end` |

## 形状映射

draw.io 的 `shape=` 属性决定节点的基本渲染形态：

| draw.io shape | HTML 等价表达 | 备注 |
|---|---|---|
| 无 shape 或 `rectangle` | `<div>` 矩形 | 默认矩形 |
| `rounded=1`（无 shape） | `<div>` 圆角矩形 | 通过 `border-radius` |
| `ellipse` | `<div>` 椭圆 | `border-radius: 50%` |
| `rhombus` | `<div>` 菱形 | `transform: rotate(45deg)` |
| `cylinder` | `<div>` 圆柱体 | `border-radius: 50% / 10%` |
| `swimlane` | `<div>` 泳道容器 | 带标题栏的容器 |
| `hexagon` | `<div>` 六边形 | `clip-path: polygon(...)` |
| `triangle` | `<div>` 三角形 | `clip-path: polygon(...)` |

## 连线样式映射（edge 元素）

| draw.io style 属性 | SVG/CSS 等价表达 | 转换规则 |
|---|---|---|
| `endArrow=classic` | `marker-end` | 标准 arrowhead marker |
| `endArrow=none` 或 `endArrow=0` | 无 `marker-end` | 不画箭头 |
| `startArrow=classic` | `marker-start` | 标准 arrowhead marker |
| `dashed=1`（edge） | `stroke-dasharray` | `stroke-dasharray: 8,4` |
| `strokeColor`（edge） | `stroke` | 直接取色值 |
| `strokeWidth`（edge） | `stroke-width` | 取数值 |
| `exitX/exitY` | 连线起点偏移 | `起点 = (src.abs_x + exitX × src.w, src.abs_y + exitY × src.h)` |
| `entryX/entryY` | 连线终点偏移 | `终点 = (tgt.abs_x + entryX × tgt.w, tgt.abs_y + entryY × tgt.h)` |

**连接点偏移计算说明**：

- `exitX/exitY` 是 source 节点上的连出点，值为 0~1 的比例：`0.0` = 左/上边缘，`0.5` = 中心，`1.0` = 右/下边缘
- `entryX/entryY` 是 target 节点上的连入点，比例同上
- 当 XML 中未指定偏移时，默认使用 `0.5`（即节点中心），保持向后兼容
- 示例：`exitX=0.5;exitY=1.0;entryX=0.5;entryY=0.0` 表示从 source 底部中心连到 target 顶部中心

## 未覆盖属性处理规则

当 `xml_to_html.py` 遇到映射表中未定义的 style 属性时：

1. **跳过该属性**，不生成对应 CSS
2. **打印警告到 stderr**：`[WARN] Unmapped style attribute: <attr>=<value>, skipped`
3. **不阻塞转换**，继续处理其余属性

此规则确保脚本对未知的 draw.io 属性具有前向兼容性。

---

## UI 规范补充说明

本映射表定义的是 `xml_to_html.py` 脚本使用的**确定性样式映射规则**（XML style 属性 → CSS 属性），不包含 UI/UX 视觉规范判断。

转换后的 HTML 在视觉质量上的补充约束来自以下两个来源：

1. **`ui-ux-pro-max` 的 `references/quick-reference.md`**：§6（Typography & Color）提供配色对比度准则，§10（Charts & Data）提供图表可读性准则
2. **`material-3` 的 MD3 参考文档**：`references/color-system.md` 提供配色角色定义（primary/secondary/tertiary），`references/typography-and-shape.md` 提供字体梯度标准（Display/Headline/Title/Body/Label 五类）

这些 UI 准则由 agent 在 Phase 4 保真校验后作为**补充检查**执行（标记 `[UI-WARN]` 警告，不阻塞流程），不改变本映射表中的确定性映射规则，也不修改 `xml_to_html.py` 脚本逻辑。
