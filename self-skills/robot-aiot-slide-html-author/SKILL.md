---
name: robot-aiot-slide-html-author
description: >
  为领导汇报类 PPT/母稿生成固定画布的逐页 HTML 页面：支持静态版（PPT 单页真源）和交互版（可翻页、带动画、数据动效、特效演示，纯原生零依赖双击即用）。执行时引用 `ui-ux-pro-max` 的设计系统与审查能力，标准上内化语义化设计 token、清晰/克制/层次原则与高级感设计标准。适用于"PPT 母稿转单页 HTML""领导汇报页落成 HTML""逐页生成 slide HTML""给 ppt-master 准备逐页 HTML""修复汇报页布局/样式/信息层级""把图表 HTML 嵌入汇报页""生成交互演示版""带动画的汇报页""可翻页演示 HTML"等场景。当图表 HTML 存在问题时，可调用 `robot-aiot-xml-html-bridge` 进行审查和修复。
---

# Robot AIoT Slide HTML Author

本技能负责把汇报母稿或页面草图落成可审查、可交付给 `ppt-master` 的逐页 HTML。
它在执行上引用 `ui-ux-pro-max` 的能力，在标准上把语义化设计 token、清晰/克制/层次原则与反模板化高级感标准直接重写为汇报页专用规则：

1. 用内容优先和可读性驱动版面，而不是追求花哨样式
2. 用语义化 token、字级、间距和容器层次做统一治理
3. 用克制的深度、留白和视觉节奏强化领导视角的信息获取效率
4. 用设计解读、一致性锁定和 AI 痕迹清单消除模板感，让页面具备高级感

设计规范已全部内化到本技能 `references/` 下（`design-system-standards.md`、`premium-design-standards.md`、`premium-review-fix.md`），运行时不再额外依赖任何外部设计规范技能。`ui-ux-pro-max` 作为执行能力依赖保留。

## 执行前依赖检查

开始执行前，先检查依赖 skill 是否已安装在运行时 `~/.agents/skills/`：

```bash
for s in ui-ux-pro-max robot-aiot-xml-html-bridge ppt-master; do
  [ -d "$HOME/.agents/skills/$s" ] || printf '[DEP-MISSING] %s\n' "$s"
done
```

| 依赖 skill | 级别 | 用途 |
|------|------|------|
| ui-ux-pro-max | 必需 | 执行时引用其设计系统与审查能力 |
| robot-aiot-xml-html-bridge | 可选 | 图表 HTML 存在问题时用于审查和修复 |
| ppt-master | 可选 | 下游消费方：逐页 HTML 交付其生成 PPTX |

- 必需依赖存在 → 略过，进入主流程；可选依赖缺失 → 提示但不阻塞
- 必需依赖出现 `[DEP-MISSING]` → **暂停执行**，列出缺失清单并提示用户手动安装（本技能不私自安装），安装完成后再继续

## 上游工作流定位

本技能位于图表转换的下游，分工如下：

1. `robot-aiot-draw-flowchart`：绘制图表 XML（图表真源）
2. `robot-aiot-xml-html-bridge`：把 XML 转换为图表 HTML（前置工作，先画图再转 HTML）
3. 本技能：以图表 HTML 为冻结输入，负责页面级 HTML 的绘制和优化
4. 产出交付 `ppt-master` 生成 PPT

本技能不做图表 XML→HTML 转换，只引用上游产出的图表 HTML 做页面编排；页面壳层的绘制、配色、排版、留白和高级感优化全部由本技能负责。

## 输入

优先读取以下材料，再开始写页面：

1. 母稿或页面大纲：至少包含标题、页面结论、上屏内容、汇报话术
2. 图表 HTML：来自 `robot-aiot-xml-html-bridge` 的冻结真源
3. 品牌资源：如 `doc-ppt/assets/midea-logo.png`
4. 页面类型与约束：见 `references/page-authoring-rules.md` 与 `references/page-html-template.md`

## 输出

### 静态版（默认）

输出必须满足：

1. 一页一个 HTML 文件，路径通常为 `doc-ppt/pages/<页码>-<slug>.html`
2. 固定 `1920x1080` 画布，作为 PPT 单页真源
3. 页面主题单一，30 秒内可读懂核心结论
4. 图表优先引用既有图表 HTML，不重画事实表达

### 交互版（用户明确要求时生成）

当用户要求"交互版""演示版""带动画""可翻页"等时，额外生成交互版 HTML：

1. 路径为 `doc-ppt/interactive/<页码>-<slug>.html`，与静态版并行存在
2. 同样固定 `1920x1080` 画布，但支持键盘/点击翻页、过渡动画、元素入场、数据动效、交互图表、背景与按钮特效
3. 纯原生 HTML/CSS/JS，零外部依赖，双击即可在浏览器运行
4. 所有页面合并为单个 HTML 文件（多页幻灯片模式），或按用户要求逐页生成
5. 设计 token、配色、排版与静态版完全一致，仅增加交互层
6. 完整规则见 `references/interactive-mode-rules.md`

## 执行流程

### 1. 先引用 `ui-ux-pro-max` 能力

逐页 HTML 化前，先用 `skill` 工具加载 `ui-ux-pro-max`，把它作为能力层输入，而不是规范真源。

优先借用它完成：

1. 页面级设计系统草案：配色候选、字体配对、间距系统、反模式建议
2. 布局与可读性复核：扫描路径、信息密度、视觉主次、可访问性风险
3. 页面交付前审查：是否存在装饰过度、对比不足、仅依赖颜色传达语义等问题

若 `ui-ux-pro-max` 的建议与本技能已内化的设计标准冲突，以本技能规则和首页图表真源约束为准。

### 2. 先做设计解读，再定风格基调

动手前按 `references/premium-design-standards.md` 完成：

1. 输出一行设计解读：页面类型、受众、视觉语气、风格基调
2. 设定三档刻度：DESIGN_VARIANCE（4-5）、MOTION_INTENSITY（1，静态页）、VISUAL_DENSITY（4-6）
3. 锁定风格基调：克制商务 / 深底科技 / 暖调编辑，三选一并保持整套汇报一致

### 3. 先定页面契约，再写样式

每页先固定四要素：

1. 标题：这一页讲什么
2. 结论：领导应该带走什么判断
3. 上屏内容：图表、表格、关键数字、流程或案例
4. 话术：解释含义、风险、动作，不复述屏幕文字

如果四要素不完整，先补语义，不要直接开始摆版。

### 4. 先建 token，再落绝对定位

页面样式先抽成变量，再放坐标：

1. 主色来自首页架构图或当前图表的主语义色
2. 其他颜色落到 `primary / secondary / tertiary / surface / outline / text` 等语义角色
3. 间距以 `8 / 16 / 24 / 32 / 48px` 为主
4. 圆角以 `8 / 12 / 16 / 24 / full` 为主
5. 深度优先用明度层级和容器对比，不依赖重阴影

### 5. 保持固定画布和内容优先

页面是 PPT 单页，不是响应式网页：

1. 使用固定画布和绝对定位
2. 先确定结构区块，再补视觉增强
3. 标题、结论、主数字和图表必须形成清晰扫描路径
4. UI 壳层服务内容，不与内容争抢注意力

### 6. 图表真源冻结与审查修复

图表区遵守以下边界：

1. 优先引用 `doc-ppt/<chart>.html`
2. 不修改图表节点坐标、结构关系和数据语义
3. 只允许调整页面容器、留白、标题、说明文字和外层 token
4. 若页面配色与图表主色冲突，以图表主色为准

**图表 HTML 审查与修复**：

当发现引用的图表 HTML 存在以下问题时，应调用 `robot-aiot-xml-html-bridge` 进行审查和修复：

1. 节点缺失、连线语义丢失、图例或数据锚点缺失
2. 分层或泳道边界消失
3. 页面比例明显变化、主色/边框色/字体层级漂移
4. 未映射样式属性导致视觉异常

调用方式：使用 `skill` 工具加载 `robot-aiot-xml-html-bridge`，让其执行保真校验和修复流程。修复完成后，`robot-aiot-slide-html-author` 继续基于修复后的图表 HTML 进行页面编排。

**边界**：`robot-aiot-slide-html-author` 负责页面级 HTML，不直接修改图表内部结构；图表级审查修复由 `robot-aiot-xml-html-bridge` 负责。

### 7. 做高级感交付前审查

每页完成后按 `references/premium-review-fix.md` 执行审查：

1. 基础检查：画布尺寸、布局不重叠、内容不溢出
2. 层级检查：标题层级、结论显著性、数字字号、页脚品牌位
3. 内容检查：页面不残留技术表名、类名、API 路径或未经解释的缩写
4. 图表检查：图表与页面 token 语义一致，但图表事实未被改写
5. 高级感预检：逐项过 `references/premium-review-fix.md` 的阻塞项与非阻塞项清单，输出审查报告

## 设计原则

以下原则的完整细则（token 角色配对、字级具体值、同心圆角、对比度判据）见 `references/design-system-standards.md`。

### 内容优先

1. 每个视觉元素都要为结论服务
2. 页面 chrome 保持克制，避免堆叠装饰
3. 大结论先于实现细节，业务影响先于技术名词

### 语义一致

1. 用语义色而不是散落的十六进制常量
2. 用 surface/container 层级表达主次关系
3. 用 headline/title/body/label 管理字级，不为每页重新发明字号

### 适度层次

1. 通过浅深背景、容器层级、轻阴影制造层次
2. 默认使用实色或轻渐变背景
3. 模糊玻璃效果只有在用户明确要求时才使用

### 一致又不单调

结合 `ui-ux-pro-max` 的页面审查能力：

1. 配色体系和字级体系统一
2. 页面版式允许变化，但不打断整体扫描节奏
3. 不依赖 hover，不用只靠颜色传达意义

### 反模板感

完整规则见 `references/premium-design-standards.md`：

1. 先做设计解读再动手，不做无意识的默认审美
2. 一致性锁定：强调色、圆角档位、灰阶基调、风格基调全套汇报统一
3. 消除 AI 痕迹：编号眉标、装饰状态点、假精确数字、三大卡片默认版式等一律禁止
4. 内容真实性：数据必须可溯源，文案禁止套话，交付前逐字自查

## 硬约束

1. 不使用响应式断点、媒体查询或 `max-width` 页面思维
2. 不直接复用应用型 dashboard 套壳覆盖图表真源
3. 不在组件里散落硬编码颜色，优先引用根变量
4. 正文默认不小于 `16px`，说明/标签默认不小于 `12px`
5. 可选视觉增强不得改动已验证的布局坐标
6. 静态版不做滚动动画、入场动画、循环动效；交互版动画规则见 `references/interactive-mode-rules.md`
7. 不伪造精确数字；占位数据必须显式标注"示意"
8. 不使用 AI 紫/霓虹渐变、纯黑硬阴影、纯黑大面积背景（品牌色本身为紫色时例外，且须整套汇报一致）
9. 不出现编号眉标、装饰状态点、版本号页脚等 AI 痕迹（完整清单见 `references/premium-design-standards.md` 第 9 节）
10. 每页 HTML 必须完整可运行，禁止占位注释和"同上"省略

## 何时读取引用文档

1. 需要完整页面编写规则时，读 `references/page-authoring-rules.md`
2. 需要页面类型、token 表、模板骨架和布局清单时，读 `references/page-html-template.md`
3. 需要运行时设计系统建议和页面审查能力时，加载 `ui-ux-pro-max`
4. 需要审查或修复图表 HTML 时，加载 `robot-aiot-xml-html-bridge`
5. 需要高级感设计标准（设计解读、刻度、风格基调、排版/色彩/布局纪律、AI 痕迹清单）时，读 `references/premium-design-standards.md`
6. 需要执行交付前审查或修复既有页面时，读 `references/premium-review-fix.md`
7. 需要设计系统细则（色彩角色配对、tonal surface 层次、字级、同心圆角、对比度判据）时，读 `references/design-system-standards.md`
8. 生成交互版时，读 `references/interactive-mode-rules.md`

## 交付口径

输出给上游工作流时，优先报告：

1. 生成了哪些页面 HTML
2. 采用了哪套主色/语义 token 规则
3. 哪些图表 HTML 被引用
4. 是否存在仍需人工确认的布局或内容风险
5. 高级感审查结论：阻塞项是否全部通过、`[UI-WARN]` 列表、风格基调与刻度声明
