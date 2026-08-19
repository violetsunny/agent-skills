# robot-icon-library Specification

## Purpose
提供标准化、可复用的扫地机器人矢量图标库，供 draw.io 图表直接引用，确保机器人/IoT 业务图表的视觉元素跨图一致，并覆盖从简笔到产品插画的不同精细度需求。

## Requirements

### Requirement: 产品插画风格图标以纯矢量形状提供
图标库 SHALL 提供「产品插画风格（详细俯视）」变体，且该变体 MUST 仅由 draw.io 矢量形状（ellipse / 圆角矩形 / text）组合而成，不得依赖外部图片 URL 或 base64 嵌入。

#### Scenario: 请求产品风格图标
- **WHEN** 用户请求智能家居产品风格的扫地机器人图标
- **THEN** SKILL 输出一段 mxCell XML 块，全部元素为矢量形状，无任何 image= 或 base64 属性

### Requirement: 产品插画图标包含规范视觉元素
该图标 MUST 包含以下视觉元素：外圈机身圆、同心内盘、带 LDS 标签的中心激光雷达塔、顶部控制行（绿色电源键 + 两侧点缀方块）、底部回充键、两个伸出机身外的多叉边刷、边刷附近灰尘粒子。

#### Scenario: 生成图标 XML
- **WHEN** 从 robot-icons.md 复制产品插画图标代码
- **THEN** XML 中包含机身、内盘、LDS 塔、控制行、回充键、双边刷、灰尘粒子七组元素，且层序为机身在下、控件在上

### Requirement: 图标配色服从色板
图标所有填充色与边框色 MUST 取自 references/color-schemes.md 色板，不得引入色板外颜色值。

#### Scenario: 校验图标颜色
- **WHEN** 检查产品插画图标的 style 属性
- **THEN** 每个 fillColor/strokeColor 均能在 color-schemes.md 色板中找到对应条目

### Requirement: 图标可整体分组与等比缩放
图标元素 MUST 使用统一坐标基准（有界包围盒内的相对坐标），使全部元素可被 Group 后整体移动，且等比缩放不失真。

#### Scenario: 在图中复用图标
- **WHEN** 用户将图标块粘贴进任意图表并执行 Group（Ctrl+G）后移动或缩放
- **THEN** 所有元素保持相对位置与圆形比例不变
