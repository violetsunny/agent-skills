---
name: robot-aiot-web-presentation-workflow
version: 2.0.0
description: >
  交互式Web演示页面制作工作流。根据知识文档生成分页汇报母稿，按需制作架构图/流程图，
  逐页生成交互HTML（可翻页、带动画、数据动效，纯原生零依赖双击即用）。
  当用户要求"做交互演示""生成Web演示""做动态汇报""可翻页演示""带动画的汇报""Web版汇报"时触发。
  也适用于用户描述了需要将技术项目数据转化为可交互浏览器演示的场景。
---

# Robot AIoT 交互式 Web 演示工作流

将技术项目数据转化为可在浏览器直接运行的交互式演示页面，核心原则：
**让受众在浏览器中获得沉浸式体验** — 每页有业务价值结论 + 数据支撑 + 交互动效，
不讲代码实现，双击即可运行。

本技能覆盖从原始知识文档到最终交互 HTML 的全链路，涉及一个外部技能调用：
- **robot-aiot-arch-diagram** — 生成架构图/流程图（SVG/HTML 格式）

与 `robot-aiot-leadership-ppt-workflow` 的关键区别：
- 产出是单个可运行 HTML 文件，不是 PPTX
- 图表由 `robot-aiot-arch-diagram` 直接生成 SVG/HTML，不需要 XML→HTML 桥接
- 支持翻页、过渡动画、元素入场、数据动效、交互图表
- 输出目录为 `doc-web/`，区别于 PPT 的 `doc-ppt/`

Sub agent 原则：
- 非 trivial 的阶段分析、内容提炼、图表规划、页面草拟、交叉校验，优先交给 fresh sub agent 执行，保持上下文干净
- 主线程只做总控：阶段切换、用户确认、真实文件落盘、跨阶段一致性校验、外部技能调用与最终交付判断
- tiny wording tweak、单页局部小改、局部格式修正可直接在主线程完成，不必起 sub agent

---

## 执行前依赖检查

开始执行前，先检查依赖 skill 是否已安装在运行时 `~/.agents/skills/`：

```bash
[ -d "$HOME/.agents/skills/robot-aiot-arch-diagram" ] || printf '[DEP-MISSING] robot-aiot-arch-diagram\n'
```

| 依赖 skill | 级别 | 用途 |
|------|------|------|
| robot-aiot-arch-diagram | 必需 | Phase 3 绘制架构图/流程图（SVG/HTML） |
| ui-ux-pro-max | 可选 | 设计系统建议与页面审查能力（内化规则优先） |

- 必需 skill 存在 → 略过，进入主流程
- 必需 skill 缺失 → **暂停执行**，提示用户手动安装（本技能不私自安装）
- 可选 skill 缺失 → 使用内化设计规则，不影响核心功能

## 输入

Markdown 知识文档，至少包含：
1. 项目名称和背景
2. 核心指标或成果数据
3. 技术架构或业务流程描述
4. 汇报对象和要求（可选）

## 输出目录约定

所有输出产物统一放在当前运行项目的 `doc-web/` 目录下。

```
doc-web/
├── assets/                     — 品牌静态资源（Logo 等）
│   └── midea-logo.png          — 美的品牌 Logo
├── <chart-name>.html           — 图表 HTML（Phase 3，robot-aiot-arch-diagram 产出）
├── <project>_演示母稿.md        — 母稿（Phase 2）
└── <project>-presentation.html — 最终交互演示文件（Phase 4，单文件多页）
```

---

## 工作流总览

```
Phase 1: 内容分析     → 读取知识文档，明确汇报对象和要求
Phase 2: 母稿分页     → 按内容结构分页，每页定义四要素和图表需求
Phase 3: 图表生成     → 调用 robot-aiot-arch-diagram 生成 SVG/HTML 图表
Phase 4: 交互HTML    → 基于母稿和图表，逐页生成交互HTML，合并为单文件
```

每个阶段产出是下一阶段的输入，逐级收敛。

建议执行方式：每个阶段先由 sub agent 在干净上下文中完成本阶段分析/起草/审查，再回到主线程做统一落盘和阶段阻塞检查，避免 Phase 1-4 信息互相污染。

---

## Phase 1: 内容分析

详细规则见 `references/phase1-content-analysis.md`。

入口约束：
1. 完整读取知识文档，提取关键信息
2. 明确汇报对象（领导/技术团队/客户）和场景（内部汇报/外部展示/培训）
3. 识别核心结论和数据支撑点
4. 标记需要图表辅助说明的内容

产物：内容分析报告，包含汇报定位、核心信息清单、图表需求列表。

阻塞条件：内容分析未完成不得进入 Phase 2。

---

## Phase 2: 母稿分页

详细规则见 `references/phase2-pagination.md`。

入口约束：
1. 基于 Phase 1 分析报告进行分页
2. 每页必须定义四要素：标题、结论、上屏内容、话术
3. 每页标记是否需要图表及图表类型（架构图/流程图/数据图/无）
4. 页面总数控制在 5-15 页，超出需拆分或合并

产物：`doc-web/<project>_演示母稿.md`，结构化分页文档。

阻塞条件：母稿未完成不得进入 Phase 3。

---

## Phase 3: 图表生成

详细规则见 `references/phase3-chart-generation.md`。

入口约束：
1. 仅生成母稿中标记需要图表的页面
2. 调用 `robot-aiot-arch-diagram` 生成 SVG/HTML 格式图表
3. 首页架构图确定全局主色基调，后续页面保持配色统一
4. 图表产出直接为 HTML，无需 XML→HTML 桥接

产物：`doc-web/<chart-name>.html`，每个图表一个文件。

阻塞条件：母稿中需要的图表未全部生成不得进入 Phase 4。

---

## Phase 4: 逐页交互 HTML

详细规则见 `references/phase4-interactive-html.md`。

入口约束：
1. 基于母稿和图表 HTML 逐页生成
2. 所有页面合并为单个 HTML 文件（多页幻灯片模式）
3. 必须实现翻页系统（键盘+点击）、过渡动画、元素入场
4. 数据密集页实现数字滚动、进度条填充等动效
5. 纯原生 HTML/CSS/JS，零外部依赖，双击即可运行
6. 尊重 `prefers-reduced-motion`，检测到时降级为即时切换
7. 固定 `1920x1080` 画布

交互 HTML 规范要点（完整规则见 `references/interactive-mode-rules.md`）：
- 翻页：←→/Space/PageUp/PageDown/Home/End/F/Esc
- 过渡：View Transition API 优先，降级 CSS transition
- 入场：按 `data-enter-order` 依次入场，总时长 ≤ 2s
- 数据动效：数字滚动、进度条填充、图表逐步绘制
- 交互图表：hover 高亮、tooltip、点击展开（仅当母稿提供明细数据）
- 性能：单页 DOM ≤ 500，动画仅限 transform/opacity/filter

产物：`doc-web/<project>-presentation.html`，单文件多页交互演示。

阻塞条件：所有页面生成完毕且通过交付前审查才算完成。

---

## 设计标准

设计规范已全部内化到本技能 `references/` 下：
- `design-system-standards.md` — 语义 token、字级、圆角、层次体系
- `premium-design-standards.md` — 反模板化、高级感、AI 痕迹清单
- `premium-review-fix.md` — 交付前审查与修复流程
- `anti-ai-slop-design.md` — 反 AI 模板感设计规则（两遍工作流、token 系统、signature 元素）
- `self-contained-html.md` — 自包含 HTML 构建规则（零依赖、资源内联、性能约束）
- `keyframe-animation.md` — 关键帧动画与动效接缝规则（Seam Gate、缓动选择、时长预算）
- `content-imagery-and-infographic.md` — 内容AI图像生成与信息图（21种信息图布局、社交图片样式、AI图像生成集成）
- `generative-art-and-canvas.md` — 生成艺术与数据可视化动效（p5.js/Canvas API、种子随机性、画布级图片）
- `web-slide-strategies.md` — Web 演示布局策略与文案公式（25种布局、叙事策略、文案公式）

运行时可选协作：

| 协作 skill | 级别 | 用途 |
|------|------|------|
| ui-ux-pro-max | 可选 | 设计系统建议与页面审查能力 |

```bash
[ -d "$HOME/.agents/skills/ui-ux-pro-max" ] && echo '[COLLAB] ui-ux-pro-max available' || echo '[INFO] ui-ux-pro-max not deployed, using internal design rules'
```

设计标准以本技能内化规则为准，`ui-ux-pro-max` 提供补充建议。

---

## 硬约束

1. 不使用响应式断点、媒体查询或 `max-width` 页面思维
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

## 何时读取引用文档

### 核心工作流
1. 需要内容分析规则时，读 `references/phase1-content-analysis.md`
2. 需要分页策略和母稿模板时，读 `references/phase2-pagination.md`
3. 需要图表生成调用规则时，读 `references/phase3-chart-generation.md`
4. 需要逐页交互 HTML 编写规则时，读 `references/phase4-interactive-html.md`
5. 需要交互模式完整规则时，读 `references/interactive-mode-rules.md`

### 设计标准
6. 需要设计系统细则时，读 `references/design-system-standards.md`
7. 需要高级感设计标准时，读 `references/premium-design-standards.md`
8. 需要执行交付前审查或修复时，读 `references/premium-review-fix.md`
9. 需要反 AI 模板感规则时，读 `references/anti-ai-slop-design.md`
10. 需要自包含 HTML 构建规则时，读 `references/self-contained-html.md`

### 视觉增强
11. 需要关键帧动画与动效接缝规则时，读 `references/keyframe-animation.md`
12. 需要内容AI图像生成与信息图规则时，读 `references/content-imagery-and-infographic.md`
13. 需要生成艺术与数据可视化动效时，读 `references/generative-art-and-canvas.md`
14. 需要 Web 演示布局策略与文案公式时，读 `references/web-slide-strategies.md`

### 外部协作
15. 需要运行时设计系统建议和页面审查能力时，加载 `ui-ux-pro-max`
16. 需要绘制架构图/流程图时，加载 `robot-aiot-arch-diagram`

## 交付口径

输出给用户时，优先报告：

1. 生成了哪些文件（母稿、图表、最终演示 HTML）
2. 采用了哪套主色/语义 token 规则
3. 页面总数和交互功能清单
4. 是否存在仍需人工确认的布局或内容风险
5. 高级感审查结论：阻塞项是否全部通过、`[UI-WARN]` 列表
