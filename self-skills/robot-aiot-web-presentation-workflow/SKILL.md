---
name: robot-aiot-web-presentation-workflow
version: 2.0.0
description: >
  交互式Web演示页面制作工作流。根据知识文档生成分页汇报母稿，按需制作架构图/流程图，
  逐页交互HTML（可翻页、带动画、数据动效，纯原生零依赖双击即用）委派 robot-aiot-interactive-html-author 编写。
  当用户要求"做交互演示""生成Web演示""做动态汇报""可翻页演示""带动画的汇报""Web版汇报"时触发。
  也适用于用户描述了需要将技术项目数据转化为可交互浏览器演示的场景。
---

# Robot AIoT 交互式 Web 演示工作流

将技术项目数据转化为可在浏览器直接运行的交互式演示页面，核心原则：
**让受众在浏览器中获得沉浸式体验** — 每页有业务价值结论 + 数据支撑 + 交互动效，
不讲代码实现，双击即可运行。

本技能覆盖从原始知识文档到最终交互 HTML 的全链路编排，涉及两个外部技能调用：
- **robot-aiot-arch-diagram** — 生成架构图/流程图（SVG/HTML 格式）（Phase 3）
- **robot-aiot-interactive-html-author** — 逐页交互动画特效 HTML 编写与单文件合并（Phase 4）

本技能本身只负责编排与补充：阶段切换、母稿分页、图表调度、跨阶段一致性、验收与交付。

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
[ -d "$HOME/.agents/skills/robot-aiot-interactive-html-author" ] || printf '[DEP-MISSING] robot-aiot-interactive-html-author\n'
```

| 依赖 skill | 级别 | 用途 |
|------|------|------|
| robot-aiot-arch-diagram | 必需 | Phase 3 绘制架构图/流程图（SVG/HTML） |
| robot-aiot-interactive-html-author | 必需 | Phase 4 逐页交互动画特效 HTML 编写与单文件合并 |

- 必需 skill 存在 → 略过，进入主流程
- 必需 skill 缺失 → **暂停执行**，提示用户手动安装（本技能不私自安装）

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
Phase 4: 交互HTML    → 委派 robot-aiot-interactive-html-author 逐页编写并合并单文件
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

## Phase 4: 逐页交互 HTML（委派编写）

编写能力委派给 `robot-aiot-interactive-html-author`：加载该 skill 并按其编写契约与审查流程执行；本阶段只提供输入与验收。

入口约束：
1. 向编写 skill 传递页面四要素、图表 HTML 与主色基调
2. 编写 skill 产出单文件多页 deck：`doc-web/<project>-presentation.html`
3. 验收自检（编排侧抽查）：
   - 翻页键位全可用、`prefers-reduced-motion` 降级即时切换
   - 零外部请求、固定 1920x1080、单页 DOM ≤ 500
   - 母稿四要素与图表数据语义无缺页、无篡改

阻塞条件：所有页面生成完毕且通过编写 skill 的交付前审查才算完成。

---

## 设计标准

设计与编写标准已全部内化在 `robot-aiot-interactive-html-author` 的 `references/` 下，
由编写 skill 在 Phase 4 执行；本技能不重复存放，仅按验收自检抽查。

---

## 硬约束（交付契约）

1. 最终交付物为单个 HTML 文件，双击即可在浏览器完整运行，纯原生零依赖（禁 CDN/npm/外部字体）
2. 固定 `1920x1080` 画布，不使用响应式断点
3. 尊重 `prefers-reduced-motion`，检测到时降级为即时切换
4. 不伪造精确数字；占位数据必须显式标注"示意"
5. 编写期细则（token、字级、AI 痕迹、动画属性、DOM 预算等）以 `robot-aiot-interactive-html-author` 编写契约为准

## 何时读取引用文档

### 核心工作流
1. 需要内容分析规则时，读 `references/phase1-content-analysis.md`
2. 需要分页策略和母稿模板时，读 `references/phase2-pagination.md`
3. 需要图表生成调用规则时，读 `references/phase3-chart-generation.md`

### 外部委派
4. 需要绘制架构图/流程图（Phase 3）时，加载 `robot-aiot-arch-diagram`
5. 需要逐页交互动画特效 HTML 编写（Phase 4）时，加载 `robot-aiot-interactive-html-author`

## 交付口径

输出给用户时，优先报告：

1. 生成了哪些文件（母稿、图表、最终演示 HTML）
2. 采用了哪套主色/语义 token 规则
3. 页面总数和交互功能清单
4. 是否存在仍需人工确认的布局或内容风险
5. 高级感审查结论（汇总自 `robot-aiot-interactive-html-author` 审查）：阻塞项是否全部通过、`[UI-WARN]` 列表
