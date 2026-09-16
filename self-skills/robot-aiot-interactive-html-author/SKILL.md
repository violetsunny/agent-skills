---
name: robot-aiot-interactive-html-author
version: 1.1.0
description: >
  交互式动画特效 HTML 编写能力。纯原生零依赖产出浏览器可直接运行的交互页面/多页 deck：
  翻页系统（键盘+点击+View Transition）、元素入场（data-enter-order）、数据动效（数字滚动/
  进度条填充/图表逐步绘制）、交互图表（hover/tooltip/展开）、关键帧动画与动效接缝、
  Mermaid/PlantUML 图表构建期渲染嵌入（headless Chrome→PNG/SVG，失败降级不静默丢图）、
  自包含单文件构建、高级感设计与交付前审查。
  当用户要求"写交互动画页""给 HTML 加翻页/动画/动效""交互图表动效""单文件交互演示页"，
  或 robot-aiot-web-presentation-workflow 委派 Phase 4 编写时触发。
---

# Robot AIoT 交互式动画特效 HTML 编写

只负责"把一页或多页内容写成交互动画特效 HTML"这一能力：token 体系、画布、翻页、
入场、数据动效、交互图表、动效接缝、单文件合并、设计标准与交付前审查。

不负责：知识文档分析、分页母稿、图表调度与阶段编排 —— 这些属于
`robot-aiot-web-presentation-workflow` 的职责；被委派时只接收其给出的页面四要素、
图表 HTML 与主色基调。

## 输入

1. 页面内容：四要素（标题、结论、上屏内容、话术）或母稿片段
2. 图表 HTML/SVG（可选，由 robot-aiot-arch-diagram 产出；内联其 SVG，不改节点坐标与数据语义）；Mermaid/PlantUML 源码输入时按 `references/diagram-embed-rendering.md` 构建期渲染为 PNG/SVG 后嵌入
3. 主色基调（可选；缺省时按 `references/design-system-standards.md` 派生）

## 输出

完整可运行交互 HTML：单页或单文件多页 deck，纯原生零依赖，双击即可运行，无外部请求。

## 硬约束（编写契约）

1. 不使用响应式断点、媒体查询或 `max-width` 页面思维；固定 `1920x1080` 画布
2. 不直接复用应用型 dashboard 套壳覆盖图表真源
3. 不在组件里散落硬编码颜色，优先引用根变量
4. 正文默认不小于 `16px`，说明/标签默认不小于 `12px`
5. 可选视觉增强不得改动已验证的布局坐标
6. 不伪造精确数字；占位数据必须显式标注"示意"
7. 不使用 AI 紫/霓虹渐变、纯黑硬阴影、纯黑大面积背景（品牌色本身为紫色时例外）
8. 不出现编号眉标、装饰状态点、版本号页脚等 AI 痕迹
9. 每页 HTML 必须完整可运行，禁止占位注释和"同上"省略
10. 最终交付物为单个 HTML 文件，双击即可在浏览器完整运行
11. 纯原生零依赖，禁止 CDN、npm 包、外部字体
12. 尊重 `prefers-reduced-motion`，检测到时所有动画降级为即时切换

## 编写流程

1. 核对输入：四要素/图表/主色是否齐备，缺失先问清再动手
2. 建 token 体系与画布骨架（`:root` 语义 token，安全边距 32-48px）
3. 逐页编写：结构 → `data-enter-order` 入场 → 数据动效 → 交互图表（仅当有明细数据）
4. 多页时合并单文件：CSS 并入 `<style>`、JS 并入 `<script>`、图表 SVG 内联，接翻页系统
5. 按 `references/premium-review-fix.md` 逐项审查（含交互版专属审查项），阻塞项修复后交付

## 验收自检

- 键盘翻页全键位可用（←→/Space/PageUp/PageDown/Home/End/F/Esc）；点击热区不遮挡可交互内容
- `prefers-reduced-motion` 降级为即时切换、数字直显终值、入场跳过、背景特效关闭
- 动画属性仅限 transform/opacity/filter；数字滚动/图表动画仅触发一次；非活跃页面无残留定时器
- 单页 DOM ≤ 500；最终文件零外部请求

## 何时读取引用文档

1. 翻页/过渡/入场/交互图表模式完整规则：`references/interactive-mode-rules.md`
2. 逐页编写实现（结构/token/画布/翻页/入场/数据动效/合并）：`references/interactive-html-authoring.md`
3. 关键帧动画与动效接缝（Seam Gate、缓动选择、时长预算）：`references/keyframe-animation.md`
4. 自包含 HTML 构建（零依赖、资源内联、性能约束）：`references/self-contained-html.md`
5. 语义 token、字级、圆角、层次体系：`references/design-system-standards.md`
6. 反模板化、高级感、AI 痕迹清单：`references/premium-design-standards.md`
7. 反 AI 模板感设计规则（两遍工作流、token 系统、signature 元素）：`references/anti-ai-slop-design.md`
8. 交付前审查与修复流程：`references/premium-review-fix.md`
9. 内容 AI 图像生成与信息图（21 种信息图布局、社交图片样式）：`references/content-imagery-and-infographic.md`
10. 生成艺术与数据可视化动效（p5.js/Canvas API、种子随机性）：`references/generative-art-and-canvas.md`
11. Web 演示布局策略与文案公式（25 种布局、叙事策略）：`references/web-slide-strategies.md`
12. Mermaid/PlantUML 图表构建期渲染嵌入（headless Chrome 流程、嵌入策略、失败降级）：`references/diagram-embed-rendering.md`

运行时可选协作：

| 协作 skill | 级别 | 用途 |
|------|------|------|
| ui-ux-pro-max | 可选 | 设计系统建议与页面审查补充（内化规则优先） |

设计标准以本技能内化规则为准，`ui-ux-pro-max` 仅提供补充建议。
