---
name: robot-aiot-ppt-presentation-workflow
version: 4.2.0
description: >
  将用户指定的源文件转化为面向目标受众的结构化汇报PPT（汇报对象与受众由用户指定：领导层/技术同行/外部客户/大众，未指定默认领导层），覆盖全链路六阶段工作流：
  源文件分析与反问澄清（页数/汇报对象/汇报范围/演讲时长） → PPT演示母稿（用户确认门） → 调用 robot-aiot-draw-flowchart 生成 flow/ 图表XML并完成XML→HTML桥接（用户确认门） → 图表回写母稿对应页并逐页HTML化 → 调用 ppt-master 生成最终PPTX文件。
  当用户要求"写PPT"、"出PPT母稿"、"做汇报材料"、"汇报方案"、"生成汇报PPT"、
  "领导汇报PPT"、"领导汇报"时触发。也适用于用户描述了需要将技术项目数据
  转化为目标受众可读的汇报格式的场景。
---

# Robot AIoT PPT 演示工作流

将用户指定的源文件转化为面向目标受众的 PPT 汇报。汇报对象与受众由用户指定
（领导层/技术同行/外部客户/大众），未指定时默认领导层。核心原则：
**让目标受众一目了然，一眼看懂** — 每页必须有业务价值结论 + 数据支撑，
不讲代码实现。

主链路（两道用户确认门 + 一次图表回写，顺序不可调换）：

```
源文件（用户指定） → 分析+反问 → PPT演示母稿 → [G1 用户确认母稿]
→ flow/ 图表生成+桥接 → [G2 用户确认图表] → 图表回写母稿对应页
→ 逐页 HTML → ppt-master 生成 PPTX
```

本技能覆盖从源文件到最终 PPTX 的全链路，涉及两个外部技能调用：
- **robot-aiot-draw-flowchart** — 生成分层架构图/流程图 XML，并完成 XML→HTML 桥接转换与静态页面 HTML 生成
- **ppt-master** — 读取逐页 HTML/MD 生成最终 PPTX 文件

Sub agent 原则：
- 非 trivial 的阶段分析、分层提炼、图表规划、页面草拟、交叉校验，优先交给 fresh sub agent 执行，保持上下文干净
- 主线程只做总控：阶段切换、用户确认、真实文件落盘、跨阶段一致性校验、外部技能调用与最终交付判断
- tiny wording tweak、单页局部小改、局部格式修正可直接在主线程完成，不必起 sub agent

强制中间层原则：
- **母稿先行**：PPT 演示母稿是图表与页面的唯一内容源，母稿未经用户确认（G1）不得开始绘图
- **XML 先转 HTML**：凡是由 `robot-aiot-draw-flowchart` 生成的图表 XML，在进入页面阶段前必须先通过 `robot-aiot-draw-flowchart` 的 XML→HTML 桥接能力转成 HTML 预览文件
- **图表先回写母稿**：图表经用户确认（G2）后，必须先把产物路径与确认状态回写母稿对应页，再开始逐页 HTML
- **母稿逐页转 HTML**：在调用 `ppt-master` 之前，必须通过 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力把 PPT 母稿的每一页都落成单页 HTML
- **按 HTML 转 PPT**：ppt-master 读取逐页 HTML/MD 生成 PPTX，HTML 是 ppt-master 的直接输入格式
- **没有 HTML 不得生成 PPT**：只要图表 HTML 或页面 HTML 未完成，PPT 生成阶段不得开始

---

## 执行前依赖检查

开始执行前，先检查依赖 skill 是否已安装在运行时 `~/.agents/skills/`：

```bash
for s in robot-aiot-draw-flowchart ppt-master; do
  [ -d "$HOME/.agents/skills/$s" ] || printf '[DEP-MISSING] %s\n' "$s"
done
```

| 依赖 skill | 级别 | 用途 |
|------|------|------|
| robot-aiot-draw-flowchart | 必需 | Phase 3 绘制图表 XML、Phase 3.5 XML→HTML 桥接转换、Phase 4 静态页面 HTML 生成 |
| ppt-master | 必需 | Phase 5 依据逐页 HTML 生成 PPTX |

- 全部存在 → 略过，进入主流程
- 出现 `[DEP-MISSING]` → **暂停执行**，列出缺失清单并提示用户手动安装（本技能不私自安装），安装完成后再继续

## 输入

用户指定的源文件（必需，未指定时先向用户索取，不得自行假设）：
- Markdown 知识文档 / 技术方案 / 总结报告
- 存量 `.pptx`（先提取内容再分析）
- 多个源文件时全部列出，由用户确认取舍与优先级

## 输出目录约定

所有输出产物统一放在当前运行项目的 `doc-ppt/` 目录下，不散落到其他位置。完整目录结构（输出/生成/验证/读取/临时五类，含 assets/、flow/、pages/、projects/、test-run/、_gen/ 登记）以根目录 [`env-config.md`](env-config.md) 为唯一真源；新增目录或修改路径只改 env-config.md，本文件与 references/ 仅引用登记项，不另行定义目录结构。

---

## 品牌资源（静态资产）

输出目录、Logo 复制方式、尺寸建议和配色协调规则见 `references/brand-assets.md`。
主文件只保留入口约束：

1. 所有产物统一落在 `doc-ppt/`
2. Phase 2 开始前把 `assets/midea-logo.png` 复制到 `doc-ppt/assets/`
3. 封面页与内容页页脚必须嵌入 Logo，且不得遮挡标题、结论或关键数据

---

## 工作流总览

```
Phase 1: 源文件分析   → 用户指定源文件；建立数据池；一次性反问（页数/汇报对象/汇报范围/演讲时长）；受众分层提炼
Phase 2: PPT演示母稿  → 按 PPT 母稿规范产出母稿 → 【确认门 G1】用户确认母稿不需要调整
Phase 3: 图表生成     → 仅按已确认母稿的图表需求清单，调用 robot-aiot-draw-flowchart 生成 flow/ 图表 XML
Phase 3.5: 桥接+确认  → XML→HTML 桥接保留原样式 → 【确认门 G2】用户确认图表无误
Phase 4: 回写+页面    → 图表产物路径与确认状态回写母稿对应页；调用静态页面 HTML 能力逐页落 HTML（含两页 showcase 门）
Phase 5: PPT生成      → 调用 ppt-master，读取逐页 HTML/MD 生成最终 PPTX
```

每个阶段产出是下一阶段的输入，逐级收敛；G1/G2 是阻塞门，未确认不得推进。每个环节结束后除确认门外，还须跑 `scripts/check_phase_handoff.py <输出目录> --phase N --write` 做交接（handoff）校验并落盘 `_gen/handoff-phaseN.md`：校验本环节产物存在、确认门状态已记录、下一环节输入齐备；FAIL 阻塞，不得进入下一环节。Phase 5 的交接即移交 ppt-master 前的 `scripts/precheck_handoff.py`（已有），不另设 --phase 5。

建议执行方式：每个阶段先由 sub agent 在干净上下文中完成本阶段分析/起草/审查，再回到主线程做统一落盘和阶段阻塞检查，避免 Phase 1-5 信息互相污染。

---

## Phase 1: 源文件分析 — 数据池与反问澄清

详细规则、反问清单、单/多数据源模板、受众分层与估算值口径见 `references/phase1-source-analysis.md`。

执行时只抓四件事：

1. 源文件必须由用户指定；完整读取后先建唯一数据池，再写任何页面，每个数字都能追溯来源，估算值显式加 `~`
2. 一次性列齐反问清单向用户批量确认：**页面总数、汇报对象（领导层/技术同行/外部客户/大众，默认领导层）、汇报范围（源文件哪些部分进 deck、哪些排除）、演讲时长**；能推断的先推断并标注依据，不一来一回
3. 受众决定表达策略与 Phase 2 母稿风格基调；先做技术明细理解，再按受众提炼汇报表达
4. 多数据源先统一口径，再进入后续阶段

产物：内容分析结论 + `doc-ppt/<project>_数据池.md` + 反问答案记录（写入分析报告头部）。

阻塞条件：源文件未指定、或反问清单未获用户回答（可推断项已标注假设除外）时，不得进入 Phase 2。

交接（handoff）：本环节结束跑 `scripts/check_phase_handoff.py <输出目录> --phase 1 --write`，校验数据池 MD 存在并落盘 `_gen/handoff-phase1.md`；FAIL 阻塞，不得进入 Phase 2。

---

## Phase 2: PPT演示母稿 — 产出与确认门 G1

母稿结构、PPT 母稿规范、确认门流程见 `references/phase2-manuscript.md`；产物骨架用 `templates/ppt-manuscript.md`。

主文件保留硬约束：

1. 母稿按 `templates/ppt-manuscript.md` 骨架填充：头部元信息（含反问答案）→ 图表需求总表 → 素材图映射表 → 逐页 `## Page N` 块（标题/结论/上屏内容/话术 四要素 + 图表需求槽位）
2. **PPT 母稿规范**（最终由 ppt-master 消费为静态可编辑 PPTX）：
   - 静态呈现：母稿不得出现翻页/动画/动效/交互标注
   - 字数：上屏文字中等密度，结论一句话 + 数据支撑，正文条目化；话术 150-300 字/页只进话术栏
   - 版式：从 17 种布局模式选型，相邻两页不同版式；商务汇报风、品牌 Logo 页脚
   - 图表：静态图表槽位（XML 真源 → HTML 桥接），图表以静态引用嵌入页面
   - 素材图：原图高清落盘、网格平铺上屏，无 lightbox 交互
3. 每页话术按逐字稿三铁律写作：提示信号（关键词加粗）、150-300 字/页、口语化
4. **【确认门 G1，阻塞】**：母稿落盘后向用户出示完整母稿，用户确认"不需要调整"后才能进入 Phase 3；用户提出修改 → 修订母稿重新送审；G1 未过就绘图按阻塞项处理
5. G1 确认后母稿冻结为图表与页面的唯一内容源；后续任何内容变更走重生链（`references/governance-and-iteration.md`），不得只改下游

交接（handoff）：G1 通过、母稿冻结后，主线程把母稿头部「确认状态」字段更新为「G1 已通过（日期）」，再跑 `scripts/check_phase_handoff.py <输出目录> --phase 2 --write`，校验母稿存在 + G1 已通过 + 图表需求总表存在，落盘 `_gen/handoff-phase2.md`；FAIL 阻塞，不得进入 Phase 3。

---

## Phase 3 / 3.5: 图表生成、桥接转换与确认门 G2

图表类型选择、XML/HTML 产物、阻塞规则与协作边界见 `references/phase3-chart-pipeline.md`。

主文件保留硬约束：

1. 仅生成 **G1 已确认母稿** 图表需求总表中标记的图表，不得自行加图
2. Phase 3 先调用 `robot-aiot-draw-flowchart` 生成图表 XML 真源，落 `doc-ppt/flow/`
3. Phase 3.5 必须调用 `robot-aiot-draw-flowchart` 的 XML→HTML 桥接能力为每个 XML 生成对应 HTML
4. **【确认门 G2，阻塞】**：全部图表 HTML 产出后，向用户逐张出示（浏览器打开 `flow/<chart-name>.html`）并列出图表清单，用户确认"图表无误"后才能进入 Phase 4；用户提出修改 → 改 XML 真源 → 整稿重生 HTML → 重新送审
5. 首页架构图确定全局主色基调，后续页面保持配色统一但允许版式多样
6. 允许在 Phase 3.5 和 Phase 4 做轻量 Material 3 规范化，但只能整理 token、字体层级、间距和容器语义，不能改图表结构和数据语义
7. 数据统计图表（饼图/箱线图/热力图/网络拓扑等）与 Mermaid 源导入重绘（含 pie/mindmap/timeline 等扩展类型）按 `robot-aiot-draw-flowchart` 的数据图表与导入规则路由；需要可编辑 `.excalidraw` 三件套产物时走其导出规则
8. 委派前置落盘：Phase 3 调用 `robot-aiot-draw-flowchart` 前跑其 `scripts/precheck_deps.sh`，输出存产出目录 `_gen/precheck-robot-aiot-draw-flowchart.txt`；exit≠0 中止；批次无记录视同未执行前置检查

交接（handoff）：
- Phase 3 结束跑 `scripts/check_phase_handoff.py <输出目录> --phase 3 --write`，校验 flow/ XML 真源存在，落盘 `_gen/handoff-phase3.md`；FAIL 阻塞，不得进入 Phase 3.5。
- Phase 3.5 G2 通过后，主线程把母稿头部「确认状态」字段更新为「G2 已通过（日期）」，再跑 `scripts/check_phase_handoff.py <输出目录> --phase 3.5 --write`，校验 flow/ XML↔HTML 配对 + G2 已通过，落盘 `_gen/handoff-phase3.5.md`；FAIL 阻塞，不得进入 Phase 4。

---

## Phase 4: 图表回写母稿 + 逐页 HTML

回写规则、逐页 HTML 编写入口与两页 showcase 门见 `references/phase4-page-authoring.md`。

### 图表回写（先于一切页面工作）

1. G2 通过后，把每张图表的产物路径（`flow/<chart-name>.xml` / `.html`）与确认状态回写到母稿"图表需求总表"对应行，并在对应 `## Page N` 块的图表需求节填入产物路径
2. 回写后母稿即"整体准备好"的完整内容源：任何页缺图表路径、或路径指向未确认产物，不得开始逐页 HTML
3. 回写只做登记，不得借机改动母稿的标题/结论/上屏内容/话术；发现内容问题回到 G1 流程修订

### 页面策略增强

布局模式选择、Deck叙事策略、文案公式详见 `references/slide-layout-strategies.md`：

1. 按页面类型选择 17 种布局模式中最匹配的一种，相邻两页不得使用相同布局
2. 按汇报场景选择 11 种 Deck 策略确定叙事弧线；演讲时长按页数换算（30 分钟 = 8-12 页）
3. 用 8 个文案公式框架组织每页文案（PAS/AIDA/FAB/3W 等）
4. 话术只进母稿话术栏与页面 `.notes` 容器，不得上屏；页内重组删改屏上文字后，notes/*.md 与 pages/*.html `.notes` 话术须双源同步更新（`check_notes.py --sync` 验证）

### 配图与封面图

需要高质量配图或封面图时，规则见 `references/ppt-image-and-cover.md`：

1. 封面推荐 HTML/CSS + AI 背景图组合
2. 案例/故事页可用 AI 插图具象化场景
3. 数据页用程序化图表，不用 AI 生图
4. AI 图片不承载事实数据，仅作视觉增强

### 阻塞性要求

1. 逐页 HTML 生成必须调用 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力
2. **仅使用静态版**：禁止动画与交互（翻页/动画/特效），ppt-master 只消费静态 HTML；scale-to-fit 视口自适应壳不属于交互动效，必须保留（1920x1080 视口下 scale=1，不影响 ppt-master 消费）
3. 每页必须满足"标题 / 结论 / 上屏内容 / 话术"四要素；话术写入页面 `display:none` 的 `.notes` 容器，出现在可见区域按阻塞项处理
4. 每页对应一个独立 HTML 文件，且图表只引用已回写母稿的图表 HTML（`flow/` 目录，相对路径 `../flow/<图表名>.html`）
5. 母稿含素材图映射的页面必须把素材图以原图高清落盘、网格平铺上屏（只压格位占位空间不压图片分辨率，区内无滚动条、不拉伸变形），素材图规则由 `robot-aiot-draw-flowchart` 的 `references/slide-image-framing.md` 承载；母稿未指定但资源目录存在可用素材时，Phase 4 开始前盘点并向用户确认选配，不得静默忽略
6. 逐页 HTML 全面铺开前必须过两页 showcase 门（封面 + 核心内容页，规则见 `references/phase4-page-authoring.md`）
7. `robot-aiot-draw-flowchart` 的布局审查清单 10 项全部通过，才允许进入 Phase 5
8. 页面允许做轻量语义化规范化，但不得破坏首页图表确立的主色语义与图表 HTML 的冻结约束

交接（handoff）：showcase 门通过后主线程把风格基准写入母稿头部、图表回写完成后，跑 `scripts/check_phase_handoff.py <输出目录> --phase 4 --write`，校验母稿回写完整 + pages/ 逐页 HTML 存在 + showcase 门已过（风格基准已锁定），落盘 `_gen/handoff-phase4.md`；FAIL 阻塞，不得进入 Phase 5。页数对齐/零宽字符/表格 GFM/logo 等移交前深度校验由 Phase 5 的 `precheck_handoff.py` 承担。

---

## Phase 5: PPT生成 — 调用 ppt-master

移交前校验、输入清单和交付后三层验证见 `references/phase5-ppt-delivery.md`。

主文件保留五条硬约束：

1. `ppt-master` 的直接视觉输入是逐页 HTML，XML 只负责图表真源追溯，MD 负责语义来源
2. 风格一致性指配色体系统一，不等于所有页面复用同一种版式
3. 若采用轻量语义化规范化，必须贯穿图表 HTML 与页面 HTML，而不是只在某几页单独套新风格
4. **PPTX 必须可编辑**：文字=原生文本框、图形=原生形状；PICTURE 仅限素材照片与 flow 图表渲染图；禁止整页光栅贴图（任何超尺寸整页 PICTURE 判交付失败）；交付前必须用 python-pptx 递归展开做形状构成验证，细则见 `references/phase5-ppt-delivery.md`
5. **过程产物目录**：PPT 生成的一切工作区/脚本/中间产物放本次交付目录下 `projects/`，禁止写入 `~/.agents/projects` 等全局目录

交接（handoff）：Phase 5 的交接即移交 ppt-master 前的最终校验，跑 `scripts/precheck_handoff.py <输出目录>`（零宽字符/表格 GFM/flow 配对/页数对齐/logo/输入清单）；FAIL 阻塞，不得调用 ppt-master。本环节不再另跑 check_phase_handoff.py。

---

## 何时读取引用文档

### 核心工作流
1. 需要源文件分析、反问清单与数据池规则时，读 `references/phase1-source-analysis.md`
2. 需要母稿结构、PPT 母稿规范与 G1 确认门规则时，读 `references/phase2-manuscript.md`
3. 需要图表生成、桥接转换与 G2 确认门规则时，读 `references/phase3-chart-pipeline.md`
4. 需要图表回写与逐页 HTML 编写规则时，读 `references/phase4-page-authoring.md`
5. 需要 PPT 交付校验规则时，读 `references/phase5-ppt-delivery.md`

### 品牌与页面
6. 需要品牌资源使用规则时，读 `references/brand-assets.md`

### 增强能力
7. 需要布局策略/Deck叙事/文案公式时，读 `references/slide-layout-strategies.md`
8. 需要AI图像生成/封面设计规则时，读 `references/ppt-image-and-cover.md`

### 治理
9. 需要交叉校验/重生链/协作关系时，读 `references/governance-and-iteration.md`
10. 每个环节结束做交接（handoff）校验、落盘 `_gen/handoff-phaseN.md` 时，跑 `scripts/check_phase_handoff.py --phase N`（Phase 5 交接走 `scripts/precheck_handoff.py`）
11. 需要目录结构与路径登记（输出/生成/验证/读取/临时）时，读 `env-config.md`（唯一真源）

## 治理与迭代

交叉校验、重生链、页面合并和协作关系见 `references/governance-and-iteration.md`。

本文件最后只保留执行顺序：

1. Phase 1 源文件分析：建唯一数据池 + 一次性反问（页数/汇报对象/汇报范围/时长）
2. Phase 2 产出 PPT 演示母稿 → **G1 用户确认母稿**
3. Phase 3 按母稿图表需求清单生成图表 XML
4. Phase 3.5 生成图表 HTML → **G2 用户确认图表**
5. Phase 4 图表回写母稿 → 逐页 HTML（showcase 门）
6. Phase 5 移交给 `ppt-master`
7. 任一上游变更后，按重生链逐级刷新下游产物；确认门涉及的产物变更后须重新过对应门
