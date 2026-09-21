---
name: robot-aiot-interactive-html-author
version: 1.12.0
description: >
  交互式动画特效 HTML 编写能力。纯原生零依赖产出浏览器可直接运行的交互页面/多页 deck：
  翻页系统（键盘+点击+触摸滑动+View Transition+#/N/M 深链）、演讲者模式（S 键弹窗：
  当前页/下一页像素级预览+话术提词+计时器，双窗口同步，可编辑备注 localStorage 持久化）、
  总览网格（O 键）、话术抽屉（N 键）、内联文本编辑（E 键切换+localStorage 持久化+Ctrl+S 导出）、
  页内分步揭示（fragment）、分支序列与内容热点、
  元素入场（data-enter-order）、数据动效（数字滚动/进度条填充/图表逐步绘制）、
  交互图表（hover/tooltip/展开）、关键帧动画与动效接缝、相机飞行过渡、
  页面级运镜与分镜规划（运镜预算制/对数时长/相机层/能量骨架/分镜卡）、
  UI 演示与画廊展示编排（八式帧级参数/画廊墙 render(t)/?seek ?autoplay）、
  多版本并行设计与选优（三方向硬门/6 视角 5 维评审/4 Pass 收敛/调参面板）、
  动效画布生命周期管理、41 套视觉风格预设（mood 路由+五维旋钮+72 组配色+单一主色推导）、
  登记版式系统（瑞士风 S01-S25 × 杂志风 M01-M10 版式锁定+deck 排版阶梯+中文排印细则）、
  扩展动画特效目录（49 种 CSS 入场动画 + 21 种 canvas FX，仅用户明确要求时路由启用）、
  Mermaid/PlantUML 图表构建期渲染嵌入（headless Chrome→PNG/SVG，失败降级不静默丢图）、
  自包含单文件/多页 INDEX 构建、衍生交付形态（文档 PDF A4/落地页 1440px）、
  高级感设计（品味六维/视觉密度/3 米测试）与交付前审查（高级感评分/终局三问）。
  当用户要求"写交互动画页""给 HTML 加翻页/动画/动效""交互图表动效""单文件交互演示页"
  "演讲者模式/提词器/双屏演示""分步揭示/分支导航/内容热点""风格预设/deck 换肤"
  "瑞士风/杂志风 deck/登记版式""多版本对比/方向选优""运镜/分镜/镜头语言""UI 演示编排"
  "品牌主色推导套色""落地页/文档 PDF 衍生形态""浏览器内直接改文字/内联编辑"，
  或上层 workflow 委派页面编写时触发。
---

# Robot AIoT 交互式动画特效 HTML 编写

只负责"把一页或多页内容写成交互动画特效 HTML"这一能力：token 体系、画布、翻页、
入场、数据动效、交互图表、动效接缝、单文件合并、设计标准与交付前审查。

不负责：知识文档分析、分页母稿、图表调度与阶段编排 —— 这些属于上层 workflow
的职责；被委派时只接收调用方给出的页面四要素、图表 HTML 与主色基调。

## 执行前依赖检查

必需依赖（运行时部署，执行前检查齐备）：

| 依赖 skill | 用途 |
|------|------|
| ui-ux-pro-max | 设计数据资产检索（search.py 查询风格/调色板库；字体库受硬约束 11 限制仅用系统字体栈） |

```bash
bash "$HOME/.agents/skills/robot-aiot-interactive-html-author/scripts/precheck_deps.sh"
```

执行第一个动作即跑此脚本：exit≠0（任一 [MISS]）立即中止并如实告知用户依赖不全，不得静默降级或假装可用。被上层 workflow 委派时输出存档批次 `_gen/precheck-robot-aiot-interactive-html-author.txt`。设计规则权威在本技能 `references/`；检索结果仅为数据建议，不得覆盖内化规则。

## 输入

1. 页面内容：四要素（标题、结论、上屏内容、话术）或母稿片段
2. 图表 HTML/SVG（可选，由调用方产出；内联其 SVG，不改节点坐标与数据语义）；Mermaid/PlantUML 源码输入时按 `references/diagram-embed-rendering.md` 构建期渲染为 PNG/SVG 后嵌入
3. 主色基调（可选；缺省时按 `references/design-system-standards.md` 派生）

## 输出

完整可运行交互 HTML：单页或单文件多页 deck，纯原生零依赖，双击即可运行，无外部请求。

## 硬约束（编写契约）

1. 不使用响应式断点、媒体查询或 `max-width` 页面思维；固定 `1920x1080` 设计画布，画布外必须包 scale-to-fit 视口自适应壳（等比缩放居中，任意窗口尺寸下无滚动条完整可见），实现见 `references/interactive-html-authoring.md`
2. 不直接复用应用型 dashboard 套壳覆盖图表真源
3. 不在组件里散落硬编码颜色，优先引用根变量
4. 正文默认不小于 `16px`，说明/标签默认不小于 `12px`
5. 可选视觉增强不得改动已验证的布局坐标
6. 不伪造精确数字；占位数据必须显式标注"示意"
7. 不使用 AI 紫/霓虹渐变、纯黑硬阴影、纯黑大面积背景（品牌色本身为紫色时例外）
8. 不出现编号眉标、装饰状态点、版本号页脚等 AI 痕迹
9. 每页 HTML 必须完整可运行，禁止占位注释和"同上"省略
10. 最终交付物为自包含 HTML、双击即可完整运行：单页形态为单个文件；上层 workflow 要求多页形态时交付 `INDEX.html` + `pages/` 目录，每页独立自包含且导航链接真实存在
11. 纯原生零依赖，禁止 CDN、npm 包、外部字体
12. 尊重 `prefers-reduced-motion`，检测到时所有动画降级为即时切换
13. 话术与一切演讲者专用文字只进 `display:none` 的 `.notes` 容器，禁止出现在页面可见区域
14. 持续动效画布与扩展特效目录（49 种 CSS 入场动画 + 21 种 canvas FX）仅在用户明确要求时启用，按 `references/animation-fx-catalog.md` 路由选型；FX 必须随页启停（见 `references/generative-art-and-canvas.md` 生命周期契约）
15. 素材图（截图/照片佐证）上屏：原图高清落盘（禁止降分辨率/降质，压的是格位占位空间不是图片）、固定格位网格平铺（区内无滚动条、不拉伸变形、`object-fit` 归一）、点击放大 lightbox（纯原生零依赖，Esc/遮罩关闭，放大图 `contain` 不超视口、用原图），规则见 `references/interactive-html-authoring.md` 素材图节

## 编写流程

1. 核对输入：四要素/图表/主色是否齐备，缺失先问清再动手
2. 建 token 体系与画布骨架（`:root` 语义 token，安全边距 32-48px）
3. 逐页编写：结构 → `.notes` 话术容器（有演讲场景时）→ 素材图网格+lightbox（有素材图映射时）→ `data-enter-order` 入场 → 数据动效 → 交互图表（仅当有明细数据）
4. 多页时合并单文件：CSS 并入 `<style>`、JS 并入 `<script>`、图表 SVG 内联，接翻页系统与演讲者模式/总览/深链（上层 workflow 明确要求 INDEX + pages/ 多文件形态时除外）
5. 按 `references/premium-review-fix.md` 逐项审查（含交互版专属审查项），阻塞项修复后交付

## 验收自检

- 键盘翻页全键位可用（←→/Space/PageUp/PageDown/Home/End/F/B/Esc）；点击热区不遮挡可交互内容
- 内联编辑模式默认内置：E 键/左上角热区可切换、点上屏文字可改、localStorage 自动存、Ctrl+S 导出改动后 HTML（锁定版/仅导出版除外，规则见 `references/interactive-mode-rules.md`）
- 触摸滑动翻页可用且与点击热区不双触发；`#/N/M` 深链加载直达对应页与步
- 含话术输入时：S 键演讲者窗口可弹出，四卡（当前页/下一页/话术/计时器）可用，双窗口翻页同步；话术卡可编辑且刷新后保留；N 键抽屉、O 键总览可用
- 含 fragment/分支/热点时：步序无跳号、热点 target 真实存在、分支可导航栈回退（审查细则见 `references/premium-review-fix.md` deck 结构 lint）
- `prefers-reduced-motion` 降级为即时切换、数字直显终值、入场跳过、背景特效关闭
- 动画属性仅限 transform/opacity/filter；数字滚动/图表动画仅触发一次；非活跃页面无残留定时器与 rAF
- scale-to-fit 壳生效：任意窗口尺寸画布等比缩放居中、无滚动条；含素材图时网格无滚动、lightbox 可开可关（Esc/遮罩）
- 单页 DOM ≤ 500；最终文件零外部请求
- headless 自检按 `references/interactive-html-authoring.md` headless 验证方法论：reduced-motion 确定性交互断言、`#/N/M` 截图矩阵目检、rpartition 注入断言
- 多页形态豁免：S 演讲者窗、O 总览网格、`#/N/M` 深链、Home/End 键、触摸滑动为单文件 deck 专属能力；`INDEX.html` + `pages/` 多页形态不适用上述各项，不判 FAIL（多页形态翻页以 INDEX 与页间真实链接为准）

## 何时读取引用文档

1. 翻页/过渡/入场/交互图表模式完整规则：`references/interactive-mode-rules.md`
2. 逐页编写实现（结构/token/画布/翻页/入场/数据动效/合并、多页 INDEX+pages 形态、概览墙三硬约束、禁用 emoji→Unicode/内联 SVG）：`references/interactive-html-authoring.md`
3. 关键帧动画与动效接缝（Seam Gate、缓动选择、时长预算、相机 rig 元素级接口、counter-transform、放大防糊栅格化）：`references/keyframe-animation.md`
4. 自包含 HTML 构建（零依赖、资源内联、性能约束）：`references/self-contained-html.md`
5. 语义 token、字级、圆角、层次体系：`references/design-system-standards.md`
6. 反模板化、高级感、AI 痕迹清单、品味六维、视觉密度上下限、3 米测试、品位锚点：`references/premium-design-standards.md`
7. 反 AI 模板感设计规则（两遍工作流、token 系统、signature 元素、data/quote slop、bento 用烂、CSS 神器过度清单）：`references/anti-ai-slop-design.md`
8. 交付前审查与修复流程、高级感评分与终局三问：`references/premium-review-fix.md`
9. 内容 AI 图像生成与信息图（21 种信息图布局、社交图片样式、真图诚实性测试、文档 PDF A4/落地页 1440px 衍生形态）：`references/content-imagery-and-infographic.md`
10. 生成艺术与数据可视化动效（p5.js/Canvas API、种子随机性、render(t) canvas 纯函数契约、程序化纸纹 fractalNoise）：`references/generative-art-and-canvas.md`
11. Web 演示布局策略与文案公式（25 种布局、叙事策略、hero 字号 180-240px、视觉主角轮换）：`references/web-slide-strategies.md`
12. Mermaid/PlantUML 图表构建期渲染嵌入（headless Chrome 流程、嵌入策略、失败降级）：`references/diagram-embed-rendering.md`
13. 演讲者模式（S 键弹窗/磁吸卡片/双窗口同步/激光笔圈选/自动翻页/演前检查）、话术 .notes 承载、总览网格、深链、触摸翻页、主题审阅、预览 iframe 三坑防护、?seek/?autoplay 联动、调参面板联动：`references/presenter-mode.md`
14. 用户明确要求动画特效时的扩展目录与路由（49 CSS 入场 + 21 canvas FX + 5 页面级编排 recipe、打字机两场景、预算硬限、clip-path 例外条款）：`references/animation-fx-catalog.md`
15. 视觉风格预设（41 套设计系统预设、mood 路由表、先预览再定稿选型流程、五维旋钮、72 组配色库、预设标注四字段、单一主色推导三步法）：`references/visual-style-presets.md`
16. 登记版式系统（瑞士风 S01-S25 × 杂志风 M01-M10 版式锁定、结构骨架 px 锚定、选择索引、内容-数据类型匹配、禁止清单）：`references/swiss-layout-system.md`
17. 演示 deck 排版阶梯（字号双约束与画布推荐值、字重阶梯、中文大标题分档、最小字号三层下限、中文排印细则与字体配对）：`references/typography.md`
18. 多版本并行设计与选优（三方向硬门、7 Phase 工作流、6 视角 5 维评审、选择无效铁律、4 Pass 收敛、调参面板）：`references/multi-version-selection.md`
19. 页面级运镜与分镜规划（运镜预算制、动机表、对数时长公式、相机层结构、镜间三分律、能量骨架、分镜卡、thumbnail pass）：`references/camera-storyboard.md`
20. UI 演示与画廊展示编排（演示即叙事公理、八式帧级参数、画廊墙 render(t)、Gallery Ripple、Dashboard Overlay、?seek/?autoplay/?speed、iframe 三坑）：`references/ui-demo-choreography.md`
