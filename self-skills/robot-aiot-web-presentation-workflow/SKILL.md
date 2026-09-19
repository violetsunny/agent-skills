---
name: robot-aiot-web-presentation-workflow
version: 2.6.0
description: >
  交互式Web演示页面制作工作流。根据知识文档生成分页汇报母稿，按需制作架构图/流程图，
  逐页交互HTML（可翻页、带动画、数据动效，纯原生零依赖双击即用）委派 robot-aiot-interactive-html-author 编写。
  交付形态含单文件 deck（默认）、多页形态、竖版社交 deck、滚动叙事页。
  当用户要求"做交互演示""生成Web演示""做动态汇报""可翻页演示""带动画的汇报""Web版汇报""竖版社交演示""滚动叙事页"时触发。
  也适用于用户描述了需要将技术项目数据转化为可交互浏览器演示的场景。
---

# Robot AIoT 交互式 Web 演示工作流

将技术项目数据转化为可在浏览器直接运行的交互式演示页面，核心原则：
**让受众在浏览器中获得沉浸式体验** — 每页有业务价值结论 + 数据支撑 + 交互动效，
不讲代码实现，双击即可运行。

本技能覆盖从原始知识文档到最终交互 HTML 的全链路编排，涉及两个兄弟技能调用：
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

默认放在当前运行项目的 `doc-web/` 目录下；**用户可指定其他输出目录**（如项目已有演示资产目录），指定后所有产物路径随之替换，Phase 1 必须确认并记录。

```
doc-web/
├── assets/                     — 品牌静态资源（Logo、素材图压缩副本等）
│   └── midea-logo.png          — 美的品牌 Logo
├── flow/                       — 图表类产物统一目录
│   ├── <chart-name>.svg        — 图表 SVG（Phase 3，供 Phase 4 内嵌）
│   └── <chart-name>.html       — 图表 HTML（Phase 3，可独立预览）
├── <project>_演示母稿.md        — 母稿（Phase 2）
└── <project>-presentation.html — 最终交互演示文件（Phase 4，单文件多页，默认形态）
```

多页形态（用户指定时，覆盖单文件 deck 的文件形态）：

```
doc-web/
├── INDEX.html                  — 总纲页，承载全场导航
└── pages/
    ├── p01-<slug>.html         — 每页独立 HTML，带"上一页/下一页"跳转控件
    └── ...                     — 末页可返回 INDEX
```

---

## 工作流总览

```
Phase 1: 内容分析     → 读取知识文档，明确汇报对象和要求
Phase 2: 母稿分页     → 按内容结构分页，每页定义四要素和图表需求
Phase 3: 图表生成     → 调用 robot-aiot-arch-diagram 生成 SVG/HTML 图表
Phase 4: 交互HTML    → 委派 robot-aiot-interactive-html-author 逐页编写，合并单文件（默认）/ 产出 INDEX+pages（多页形态）
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
5. 与用户确认结构形态：单文件 deck（默认）/ 多页形态（INDEX 总纲 + 每页上一页下一页导航）；确认输出目录与页面规模
6. 盘点输出目录既有资产：素材截图、品牌 Logo、既有页面配色 token、旧图表/旧页面（旧产物默认只作内容参考，不直接复用；与新结构冲突时请用户确认归档或覆盖）

产物：内容分析报告，包含汇报定位（含结构形态）、核心信息清单、图表需求列表、素材图清单。

阻塞条件：内容分析未完成不得进入 Phase 2。

---

## Phase 2: 母稿分页

详细规则见 `references/phase2-pagination.md`。

入口约束：
1. 基于 Phase 1 分析报告进行分页
2. 每页必须定义四要素：标题、结论、上屏内容、话术
3. 每页标记是否需要图表及图表类型（架构图/流程图/数据图/拓扑图/映射图/泳道图/循环图/生命周期图/脑图/分流汇聚图/对比图/层级图/时序图/无 等，开放枚举），并标注配套素材图（图表与素材图并举）
4. 页面总数默认 5-15 页；用户明确要求扩充时可突破上限，须做节奏校验并在母稿记录扩充理由
5. 上屏内容必须从源文档持续提炼填满（概念与示例成对出现），不得只写标题级骨架
6. 章节/阶段之间的过渡论证独立成页（为什么从上一章进入下一章），主体章节页数占比与其分量匹配

产物：`doc-web/<project>_演示母稿.md`，结构化分页文档（含图表需求总表与素材图映射表）。

阻塞条件：母稿未完成不得进入 Phase 3。

---

## Phase 3: 图表生成

详细规则见 `references/phase3-chart-generation.md`。

入口约束：
1. 仅生成母稿中标记需要图表的页面
2. 调用 `robot-aiot-arch-diagram` 生成 SVG/HTML 格式图表
3. **默认全部新绘，不复用历史图表产物**（其他工作流目录的旧图表仅作内容参考）；确需复用必须用户明确同意
4. 首页架构图确定全局主色基调，后续页面保持配色统一；输出目录已有既有页面/品牌色时，直接沿用其配色 token 锁定主色，无需等首页产出
5. 图表产出直接为 HTML，无需 XML→HTML 桥接
6. 数据统计图表（饼图/箱线图/热力图/网络拓扑等）按 `robot-aiot-arch-diagram` 的数据图表规则路由；页面需要嵌入 Mermaid/PlantUML 源码图时，Phase 4 由 `robot-aiot-interactive-html-author` 构建期渲染嵌入
7. 图表数量多（>6 张）时：先锁定全局风格 token（皮肤/主色/箭头语义/viewBox/网格/数据标注纪律），再分批派发并行 sub agent 生成，避免风格漂移

产物：`doc-web/flow/<chart-name>.svg`（供 Phase 4 内嵌）+ `doc-web/flow/<chart-name>.html`（独立预览），每个图表两个文件；图表类产物一律落 `flow/` 子目录，不与母稿、页面混放。

阻塞条件：母稿中需要的图表未全部生成不得进入 Phase 4。

---

## Phase 4: 逐页交互 HTML（委派编写）

编写能力委派给 `robot-aiot-interactive-html-author`：加载该 skill 并按其编写契约与审查流程执行；本阶段只提供输入与验收。

入口约束：
1. 向编写 skill 传递页面四要素、图表 SVG/HTML、素材图映射与主色基调
2. 默认形态：编写 skill 产出单文件多页 deck `doc-web/<project>-presentation.html`；多页形态（Phase 1 确认）：产出 `INDEX.html` 总纲 + `pages/` 逐页 HTML，每页必须有"上一页/下一页"跳转控件，末页可返回 INDEX
3. 验收自检（编排侧抽查）：
   - 翻页键位全可用（多页形态为导航链接全可用）、`prefers-reduced-motion` 降级即时切换
   - 零外部请求、1920x1080 设计画布 + scale-to-fit 视口自适应（任意窗口无滚动条完整可见）、单页 DOM ≤ 500
   - 母稿四要素与图表数据语义无缺页、无篡改
   - 母稿素材图映射表中该页有素材时必须已上屏（压缩缩略图 + 网格平铺无滚动 + 点击放大 lightbox）
   - 用户无风格偏好时：三标题页预览已出并经用户定稿，全套锁定无混用

阻塞条件：所有页面生成完毕且通过编写 skill 的交付前审查才算完成。

---

## 设计标准

设计与编写标准已全部内化在 `robot-aiot-interactive-html-author` 的 `references/` 下，
由编写 skill 在 Phase 4 执行；本技能不重复存放，仅按验收自检抽查。

视觉风格选型走编写 skill 预设库的 mood 路由表与"先预览再定稿"流程：Phase 1 的汇报对象与场景作选型输入；用户无风格偏好时由编写 skill 出 3 个真实标题页供用户预览定稿后全套锁定。

---

## 硬约束（交付契约）

1. 默认交付物为单个 HTML 文件，双击即可在浏览器完整运行，纯原生零依赖（禁 CDN/npm/外部字体）；用户指定多页形态时，"单文件"被覆盖为 INDEX + pages/ 多文件，其余约束（零依赖、双击即用）不变
2. 固定 `1920x1080` 设计画布，不使用响应式断点；画布外包 scale-to-fit 视口自适应壳（等比缩放居中，任意窗口尺寸无滚动条完整可见）
3. 尊重 `prefers-reduced-motion`，检测到时降级为即时切换
4. 不伪造精确数字；占位数据必须显式标注"示意"
5. 编写期细则（token、字级、AI 痕迹、动画属性、DOM 预算等）以 `robot-aiot-interactive-html-author` 编写契约为准

## 何时读取引用文档

### 核心工作流
1. 需要内容分析规则时，读 `references/phase1-content-analysis.md`
2. 需要分页策略和母稿模板时，读 `references/phase2-pagination.md`
3. 需要图表生成调用规则时，读 `references/phase3-chart-generation.md`

### 外部委派
1. 需要绘制架构图/流程图（Phase 3）时，加载 `robot-aiot-arch-diagram`
2. 需要逐页交互动画特效 HTML 编写（Phase 4）时，加载 `robot-aiot-interactive-html-author`

## 交付口径

输出给用户时，优先报告：

1. 生成了哪些文件（母稿、图表、最终演示 HTML；多页形态时报告 INDEX.html + pages/ 页面清单）
2. 采用了哪套主色/语义 token 规则
3. 页面总数和交互功能清单
4. 是否存在仍需人工确认的布局或内容风险
5. 高级感审查结论（汇总自 `robot-aiot-interactive-html-author` 审查）：阻塞项是否全部通过、`[UI-WARN]` 列表
