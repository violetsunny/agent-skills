---
name: robot-aiot-web-presentation-workflow
version: 3.1.0
description: >
  交互式Web演示页面制作工作流。用户指定源文件后分析并一次性反问（页数/汇报对象/汇报范围/场景/交付形态），
  产出Web演示母稿（用户确认门），按需调用 robot-aiot-arch-diagram 生成 flow/ 架构图/流程图（用户确认门），
  图表回写母稿对应页后，逐页交互动画特效HTML（可翻页、带动画、数据动效，纯原生零依赖双击即用）
  委派 robot-aiot-interactive-html-author 编写。交付形态含单文件 deck（默认）、多页形态、竖版社交 deck、滚动叙事页。
  当用户要求"做交互演示""生成Web演示""做动态汇报""可翻页演示""带动画的汇报""Web版汇报""竖版社交演示""滚动叙事页"时触发。
  也适用于用户描述了需要将技术项目数据转化为可交互浏览器演示的场景。
---

# Robot AIoT 交互式 Web 演示工作流

将用户指定的源文件转化为可在浏览器直接运行的交互式演示页面，核心原则：
**让受众在浏览器中获得沉浸式体验** — 每页有业务价值结论 + 数据支撑 + 交互动效，
不讲代码实现，双击即可运行。

主链路（两道用户确认门 + 一次图表回写，顺序不可调换）：

```
源文件（用户指定） → 分析+反问 → Web演示母稿 → [G1 用户确认母稿]
→ flow/ 图表生成 → [G2 用户确认图表] → 图表回写母稿对应页
→ 逐页交互动画 HTML（robot-aiot-interactive-html-author）
```

本技能覆盖从源文件到最终交互 HTML 的全链路编排，涉及两个兄弟技能调用：
- **robot-aiot-arch-diagram** — 生成架构图/流程图（SVG/HTML 格式）（Phase 3）
- **robot-aiot-interactive-html-author** — 逐页交互动画特效 HTML 编写与单文件合并（Phase 4）

本技能本身只负责编排与补充：阶段切换、母稿分页、确认门、图表调度与回写、跨阶段一致性、验收与交付。

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

用户指定的源文件（必需，未指定时先向用户索取，不得自行假设），至少包含：
1. 项目名称和背景
2. 核心指标或成果数据
3. 技术架构或业务流程描述

Markdown 知识文档为主；存量 `.pptx` 先跑 `scripts/extract_pptx.py` 提取后并入分析。汇报对象和要求可从源文件推断，推断结果须经 Phase 1 反问确认。

## 输出目录约定

默认放在当前运行项目的 `doc-web/` 目录下；**用户可指定其他输出目录**（如项目已有演示资产目录），指定后所有产物路径随之替换，Phase 1 必须确认并记录。完整目录结构（单文件/多页形态、flow/、assets/、_gen/、test-run/ 等输出/生成/验证/读取/临时五类登记）以根目录 [`env-config.md`](env-config.md) 为唯一真源；新增目录或修改路径只改 env-config.md，本文件与 references/ 仅引用登记项，不另行定义目录结构。

---

## 工作流总览

```
Phase 1: 源文件分析   → 用户指定源文件；完整读取；一次性反问（页数/汇报对象/汇报范围/场景/交付形态）；盘点既有资产
Phase 2: Web演示母稿  → 按 Web 母稿规范分页产出母稿 + lint 清零 → 【确认门 G1】用户确认母稿不需要调整
Phase 3: 图表生成     → 仅按已确认母稿的图表需求清单，调用 robot-aiot-arch-diagram 生成 flow/ SVG/HTML → 【确认门 G2】用户确认图表无误
Phase 3.5: 图表回写   → 图表产物路径与确认状态回写母稿对应页，母稿成为"整体准备好"的完整内容源
Phase 4: 交互HTML     → 委派 robot-aiot-interactive-html-author 逐页编写，合并单文件（默认）/ 产出 INDEX+pages（多页形态）
```

每个阶段产出是下一阶段的输入，逐级收敛；G1/G2 是阻塞门，未确认不得推进。每个环节结束后除确认门外，还须跑 `scripts/check_phase_handoff.py <输出目录> --phase N --write` 做交接（handoff）校验并落盘 `_gen/handoff-phaseN.md`：校验本环节产物存在、确认门状态已记录、下一环节输入齐备；FAIL 阻塞，不得进入下一环节。

建议执行方式：每个阶段先由 sub agent 在干净上下文中完成本阶段分析/起草/审查，再回到主线程做统一落盘和阶段阻塞检查，避免 Phase 1-4 信息互相污染。

---

## Phase 1: 源文件分析

详细规则见 `references/phase1-content-analysis.md`。

入口约束：
1. 源文件必须由用户指定；完整读取，提取关键信息，禁止抽样阅读
2. 一次性列齐反问清单向用户批量确认：**页面总数、汇报对象（领导层/技术同行/外部客户/大众，未指定默认领导层）、汇报范围（源文件哪些部分进 deck、哪些排除）、场景（年度总结/项目验收/方案评审/培训分享）、交付形态（单文件 deck 默认/多页/竖版/滚动叙事）**；能推断的先推断并标注依据，不一来一回
3. 识别核心结论和数据支撑点
4. 标记需要图表辅助说明的内容
5. 确认输出目录与页面规模
6. 盘点输出目录既有资产：素材截图、品牌 Logo、既有页面配色 token、旧图表/旧页面（旧产物默认只作内容参考，不直接复用；与新结构冲突时请用户确认归档或覆盖）

产物：内容分析报告，包含汇报定位（含结构形态与汇报范围）、核心信息清单、图表需求列表、素材图清单。

阻塞条件：源文件未指定、内容分析未完成不得进入 Phase 2。

交接（handoff）：本环节结束跑 `scripts/check_phase_handoff.py <输出目录> --phase 1 --write`，校验分析报告五章节齐备并落盘 `_gen/handoff-phase1.md`；FAIL 阻塞，不得进入 Phase 2。

---

## Phase 2: Web演示母稿

详细规则与 Web 母稿规范见 `references/phase2-pagination.md`。

入口约束：
1. 基于 Phase 1 分析报告进行分页
2. 每页必须定义四要素：标题、结论、上屏内容、话术；**外加"动效与交互备注"节（母稿每页必备）**
3. 每页标记是否需要图表及图表类型（架构图/流程图/数据图/拓扑图/映射图/泳道图/循环图/生命周期图/脑图/分流汇聚图/对比图/层级图/时序图/无 等，开放枚举），并标注配套素材图（图表与素材图并举）
4. 页面总数以 Phase 1 反问答案为准（默认 5-15 页）；用户明确要求扩充时可突破上限，须做节奏校验并在母稿记录扩充理由
5. 上屏内容必须从源文件持续提炼填满（概念与示例成对出现），不得只写标题级骨架；上屏文字按 Web 规范克制（文字是视觉锚点，叙事由动画分步承载）
6. 章节/阶段之间的过渡论证独立成页（为什么从上一章进入下一章），主体章节页数占比与其分量匹配
7. **Web 母稿规范**（最终产出浏览器运行的动画特效 HTML）：母稿须含主题节奏表（单色系 light/dark + hero）、能量段位表（四段位运镜输入）、逐页动效与交互备注（入场/转场/数据动效/交互点/DOM 预算）；图表槽位按可动画 SVG 内嵌规划；素材图按压缩缩略图 + lightbox 点击放大规划；规范细则见 `references/phase2-pagination.md`

产物：`doc-web/<project>_演示母稿.md`，以 `templates/deck-manuscript.md` 为骨架填充（含图表需求总表、素材图映射表、主题节奏表、能量段位表），填充后必须跑 `scripts/lint_manuscript.py` 且 `[MS-FAIL]` 清零。

**【确认门 G1，阻塞】**：母稿 lint 清零后向用户出示完整母稿，用户确认"不需要调整"后才能进入 Phase 3；用户提出修改 → 修订母稿重跑 lint 重新送审；G1 未过就绘图按阻塞项处理。G1 确认后母稿冻结为图表与页面的唯一内容源，后续内容变更须修订母稿并重新过 G1。G1 通过后先产两页 showcase 样张供用户确认风格基调（细化见 `references/phase2-pagination.md`"两页 showcase 确认门"），确认通过后再进 Phase 3 图表阶段。

交接（handoff）：G1 通过、母稿冻结后，主线程把母稿头部「确认状态」字段更新为「G1 已通过（日期）」，再跑 `scripts/check_phase_handoff.py <输出目录> --phase 2 --write`，校验母稿存在 + G1 已通过 + 图表需求总表存在，落盘 `_gen/handoff-phase2.md`；FAIL 阻塞，不得进入 Phase 3。

---

## Phase 3: 图表生成与确认门 G2

详细规则见 `references/phase3-chart-generation.md`。

入口约束：
1. 仅生成 **G1 已确认母稿** 图表需求总表中标记的图表，不得自行加图、减图或改动图表语义
2. 调用 `robot-aiot-arch-diagram` 生成 SVG/HTML 格式图表
3. **默认全部新绘，不复用历史图表产物**（其他工作流目录的旧图表仅作内容参考）；确需复用必须用户明确同意
4. 首页架构图确定全局主色基调，后续页面保持配色统一；输出目录已有既有页面/品牌色时，直接沿用其配色 token 锁定主色，无需等首页产出
5. 图表产出直接输出 SVG/HTML，不经过 XML 中间格式
6. 数据统计图表（饼图/箱线图/热力图/网络拓扑等）按 `robot-aiot-arch-diagram` 的数据图表规则路由；页面需要嵌入 Mermaid/PlantUML 源码图时，Phase 4 由 `robot-aiot-interactive-html-author` 构建期渲染嵌入
7. 图表数量多（>6 张）时：先锁定全局风格 token（皮肤/主色/箭头语义/viewBox/网格/数据标注纪律），再分批派发并行 sub agent 生成，避免风格漂移
8. 委派前置落盘：进入 Phase 3 前跑 `robot-aiot-arch-diagram` 与 `robot-aiot-interactive-html-author` 各自的 `scripts/precheck_deps.sh`，输出存产出目录 `_gen/precheck-<skill名>.txt`；exit≠0 中止；批次无记录视同未执行前置检查

产物：`doc-web/flow/<chart-name>.svg`（供 Phase 4 内嵌）+ `doc-web/flow/<chart-name>.html`（独立预览），每个图表两个文件；图表类产物一律落 `flow/` 子目录，不与母稿、页面混放。

**【确认门 G2，阻塞】**：全部图表产出并通过校验后，向用户逐张出示（浏览器打开 `flow/<chart-name>.html`），附图表清单（图表名/类型/服务的母稿页码/核心信息），用户确认"图表无误"后才能进入 Phase 3.5；用户提出修改 → 重新生成 → 重新送审；修改波及母稿内容 → 回 Phase 2 修订母稿并重过 G1。

阻塞条件：母稿中需要的图表未全部生成或未过 G2，不得进入 Phase 3.5/4。

交接（handoff）：G2 通过后，主线程把母稿头部「确认状态」字段更新为「G2 已通过（日期）」，再跑 `scripts/check_phase_handoff.py <输出目录> --phase 3 --write`，校验 flow/ SVG↔HTML 配对 + G2 已通过，落盘 `_gen/handoff-phase3.md`；FAIL 阻塞，不得进入 Phase 3.5。

---

## Phase 3.5: 图表回写母稿

1. G2 通过后，把每张图表的产物路径（`flow/<chart-name>.svg` / `.html`）与确认状态回写到母稿"图表需求总表"对应行，并在对应 `## Page N` 块的图表需求节补"产物路径"字段
2. 回写完整性校验：图表需求总表中类型非"无"的行必须有产物路径与确认状态；任何页缺图表路径、或路径指向不存在/未确认的产物，不得进入 Phase 4
3. 回写只做登记，不得借机改动母稿的标题/结论/上屏内容/话术/动效备注；发现内容问题回 Phase 2 修订母稿并重过 G1
4. 回写完成后母稿即"整体准备好"的完整内容源，Phase 4 只消费该母稿

阻塞条件：回写未完成不得进入 Phase 4。

交接（handoff）：回写完成后跑 `scripts/check_phase_handoff.py <输出目录> --phase 3.5 --write`，校验图表需求总表回写完整（类型非「无」行的产物路径指向存在的 flow 文件、确认状态列已填），落盘 `_gen/handoff-phase3.5.md`；FAIL 阻塞，不得进入 Phase 4。

---

## Phase 4: 逐页交互 HTML（委派编写）

编写能力委派给 `robot-aiot-interactive-html-author`：加载该 skill 并按其编写契约与审查流程执行；本阶段只提供输入与验收。

入口约束：
1. 向编写 skill 传递页面四要素、动效与交互备注、已回写母稿的图表 SVG/HTML、素材图映射与主色基调；委派前核对 `_gen/precheck-robot-aiot-interactive-html-author.txt` 存在，缺失先补跑 Phase 3 入口约束 8
2. 默认形态：编写 skill 产出单文件多页 deck `doc-web/<project>-presentation.html`；多页形态（Phase 1 确认）：产出 `INDEX.html` 总纲 + `pages/` 逐页 HTML，每页必须有"上一页/下一页"跳转控件，末页可返回 INDEX
3. 验收自检（编排侧抽查）：
   - 翻页键位全可用（多页形态为导航链接全可用）、`prefers-reduced-motion` 降级即时切换
   - 零外部请求、1920x1080 设计画布 + scale-to-fit 视口自适应（任意窗口无滚动条完整可见）、单页 DOM ≤ 500
   - 母稿四要素、动效备注与图表数据语义无缺页、无篡改
    - 母稿素材图映射表中该页有素材时必须已上屏（压缩缩略图 + 网格平铺无滚动 + 点击放大 lightbox）
   - 用户无风格偏好时：三标题页预览已出并经用户定稿，全套锁定无混用
   - 多页批次：源页（旧源拷贝或新制）入批前必须先单页过 `scripts/lint_deck_html.py`；批次终验一次调用 `scripts/check_deck_batch.py`（静态硬约束 + lint 全量检查含 SVG 线/箭头契约 #8 + 导航链闭合：中间页 prev/next 顺序指向相邻页、首末页禁用）+ `scripts/check_notes_hidden.py`（话术容器隐藏断言）+ `scripts/shoot_anim.py`（t100/t6000 双时间点动画触发截图）+ 逐图目检全过；母稿登记的静态页以 `--static-pages` 传入 `check_deck_batch.py` 与 `shoot_anim.py` 豁免动画触发检查；验证产物落盘 `test-run/<批次>/` 不删除

阻塞条件：所有页面生成完毕且通过编写 skill 的交付前审查才算完成。

交接（handoff）：交付前跑 `scripts/check_phase_handoff.py <输出目录> --phase 4 --write`，校验最终 HTML 存在（单文件 deck 或 INDEX+pages），落盘 `_gen/handoff-phase4.md`；质量验收另跑 lint_deck_html/check_deck_batch（见上验收自检），handoff 只校验交付产物存在。

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
1. 需要源文件分析与反问清单规则时，读 `references/phase1-content-analysis.md`；产物骨架用 `templates/content-analysis-report.md`
2. 需要分页策略、Web 母稿规范与 G1 确认门规则时，读 `references/phase2-pagination.md`；产物骨架用 `templates/deck-manuscript.md`，填充后跑 `scripts/lint_manuscript.py`
3. 需要图表生成调用与 G2 确认门规则时，读 `references/phase3-chart-generation.md`
4. Phase 4 编写页面 shell/动画或批次验收时，读 `references/phase4-style-lock.md`（deck 级风格基线，优先于编写契约的 deck 级取舍）
5. 存量 `.pptx` 作内容源时，跑 `scripts/extract_pptx.py`；Phase 4 交付 HTML 验收跑 `scripts/lint_deck_html.py`
6. 每个环节结束做交接（handoff）校验、落盘 `_gen/handoff-phaseN.md` 时，跑 `scripts/check_phase_handoff.py --phase N`
7. 需要交叉校验清单、真源重生链、handoff 治理、迭代与协作链路规则时，读 `references/governance-and-iteration.md`
8. 需要目录结构与路径登记（输出/生成/验证/读取/临时）时，读 `env-config.md`（唯一真源）

### 外部委派
1. 需要绘制架构图/流程图（Phase 3）时，加载 `robot-aiot-arch-diagram`
2. 需要逐页交互动画特效 HTML 编写（Phase 4）时，加载 `robot-aiot-interactive-html-author`

## 交付口径

输出给用户时，优先报告：

1. 生成了哪些文件（母稿、图表、最终演示 HTML；多页形态时报告 INDEX.html + pages/ 页面清单）
2. 采用了哪套主色/语义 token 规则
3. 页面总数和交互功能清单
4. 两道确认门（G1 母稿 / G2 图表）的确认记录与图表回写状态
5. 是否存在仍需人工确认的布局或内容风险
6. 高级感审查结论（汇总自 `robot-aiot-interactive-html-author` 审查）：阻塞项是否全部通过、`[UI-WARN]` 列表
