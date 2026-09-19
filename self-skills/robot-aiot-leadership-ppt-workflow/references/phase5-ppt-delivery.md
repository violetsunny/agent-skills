# Phase 5: PPT 生成与交付验证

Phase 5 负责将母稿、图表 XML/HTML、逐页 HTML 一并移交给 `ppt-master`，生成最终 PPTX。

## 移交前校验

1. 所有数据与数据池一致
2. `~` 前缀一致，快照/累计标记清晰
3. 无零宽空格等不可见字符
4. Markdown 表格列数与分隔行一致
5. 所有图表 XML 已生成对应 HTML，且通过保真校验
6. 每页四要素齐全
7. 每页已生成对应 HTML，图表 HTML / 页面 HTML 全部完成后才可启动 PPT 阶段
8. 图表 HTML 与页面 HTML 配色同属一个体系，间距遵循统一基线
9. `doc-ppt/assets/midea-logo.png` 已就位，封面与页脚引用正确
10. 若启用轻量 MD3 规范化，图表 HTML 与页面 HTML 的 token 语义一致，且未引入新的结构漂移

## Sub Agent 建议

1. 交付前结构验证、数据验证、视觉验证可拆给独立 sub agents 并行检查
2. 主线程汇总各 sub agent 发现后统一修正，再决定是否调用 `ppt-master`
3. `ppt-master` 调用和最终“可交付”判断只能由主线程执行

## 调用 ppt-master 时提供

1. `doc-ppt/<项目>_PPT母稿.md`
2. `doc-ppt/flow/<图表名>.xml`
3. `doc-ppt/flow/<图表名>.html`
4. `doc-ppt/pages/*.html`
5. `doc-ppt/assets/midea-logo.png`
6. 页数与页面结构说明
7. 风格说明：配色统一、布局多样，不要所有页面都复制首页风格

三类输入职责固定：

1. MD：内容语义源
2. XML：图表真源
3. HTML：直接视觉约束输入

## 可编辑 PPTX 硬规则（最高优先，违反即交付失败）

1. **PPTX 必须可编辑**：所有标题/正文/标签/表格文字 = 原生文本框，卡片/色块/分隔线/几何图形 = 原生形状（AUTO_SHAPE/FREEFORM/连接线/原生 table）。PICTURE 仅允许两类：素材照片（平台截图等佐证图）、flow 图表的渲染 PNG——即"引用的图片文件"本身。
2. **禁止整页光栅贴图**：任何接近整页尺寸的 PICTURE（宽 > 10,000,000 EMU，或名为 page-fullbleed 之类）一律判失败。禁止把页面 HTML 截图后作为一页贴入。
3. **禁止用一张图代替一个内容区块**：页面里每个语义单元（结论条、卡片、表格行、chip、图注）都必须有对应原生元素。
4. **交付前形状构成验证（必做）**：用 python-pptx 递归展开每页所有形状（含 GROUP），统计 TEXT_BOX/AUTO_SHAPE/FREEFORM/TABLE/PICTURE 数量；断言每页 TEXT_BOX ≥ 8 且无超尺寸 PICTURE。验证不通过不得交付，回到生成层修复。
5. 若 ppt-master 任一路线的产物违反上述条款（如输出整页图片），判该次生成失败：不得交付，改用原生重建（python-pptx 按页面 HTML 逐页重建，风格对齐既有合格页）。

## HTML→PPTX 转换保真（书写侧硬约束与排版陷阱）

「可编辑 PPTX 硬规则」约束 PPTX 产物侧；本节约束逐页 HTML 书写侧：`doc-ppt/pages/*.html` 与 `doc-ppt/flow/*.html` 按本节规则书写，ppt-master 才可能产出合格产物；硬规则第 5 条失败回退的 python-pptx 原生重建路线，同样按本节的换算与标注约定执行。产物侧判定标准此处不重复。

### 书写侧 4 硬约束

1. **画布尺寸映射**：逐页 HTML 画布固定 1920×1080px（与 Phase 4 scale-to-fit 壳一致，1920×1080 视口下 scale=1），对应 PPTX 画布 960pt×540pt（16:9 标准，13.333in×7.5in），换算比 2:1；继承甲方模板时画布跟模板走（见「甲方模板继承」）。
2. **文字必须原生文本框**：所有上屏文字必须落在段落级元素（`<p>`、`<h1>`-`<h6>`、`<li>`）内，`<div>` 里禁止裸文字；`<span>` 只能夹在段落级元素内做局部样式（加粗/变色），不得承载主文字。原因：PPTX 文字必须存在于 text frame，裸 div 没有对应文本容器，生成层要么丢字要么整块光栅化。
3. **图形必须原生形状**：背景/边框/圆角只能写在容器 `<div>` 上，不得写在文字标签上；禁止 CSS 渐变，只用纯色或多个纯色子块分段；`<div>` 禁止 `background-image`，图片一律用 `<img>` 标签并显式给定宽高。原因：PPTX 里 shape 与 text frame 是两个对象，段落级元素只翻译成 text frame，容器 div 才翻译成 shape；`background-image` 不会被生成层解析为图片对象。
4. **禁止整页光栅贴图**：页面 HTML 不得出现任何“截图代替内容区块”的写法；`<img>` 仅限素材照片与 flow 图表渲染 PNG（与硬规则第 1 条 PICTURE 白名单一致），不得把 CSS 渐变降级成整页背景图来绕过约束 3（见「六排版陷阱」第 6 条）。

### 画布换算：1920×1080px → 960×540pt

1. 换算关系 2:1：`pt = px ÷ 2`。960pt×540pt = 13.333in×7.5in，即 PowerPoint 16:9 宽屏标准版面。
2. 字号同比例换算：`font-size: 48px` → 24pt，`28px` → 14pt；结果按 0.5pt 取整。
3. 间距与坐标（margin/padding/top/left/width/height）一律 `px ÷ 2`，同一页面不得混用两套数值。
4. 边框线宽：`border: 2px` → 1pt；border-radius 换算见「六排版陷阱」第 4 条。
5. 不要把 HTML 画布尺寸当分辨率：PPTX 是矢量文档，画布决定物理尺寸而非清晰度；超大画布不会让文字更清晰，只会让字号相对画布变小，投影反而更差。
6. 继承甲方模板时本节换算不适用，缩放比 = 模板幻灯片宽 pt ÷ HTML 画布宽 px（见「甲方模板继承」）。

python-pptx 重建路线新建画布时按如下设定：

```python
from pptx import Presentation
from pptx.util import Emu

prs = Presentation()
prs.slide_width = Emu(12192000)   # 13.333in = 960pt
prs.slide_height = Emu(6858000)   # 7.5in = 540pt
```

### data-pptx-merge：文本框合并标注

默认每个 `<p>`/`<h1>`-`<h6>` 在 PPTX 里是独立文本框，卡片内多段文字无法整段连续编辑。在容器 div 上标注 `data-pptx-merge="true"`，容器内全部段落级元素合并为一个可编辑文本框，段间保留段落分隔符。该属性标注在逐页 HTML 上、由 PPTX 生成层消费；python-pptx 原生重建回退路线必须读取该属性决定文本框粒度。

属性清单：

| 属性 | 允许值 | 缺省（未标注） | 效果 |
|---|---|---|---|
| `data-pptx-merge` | `"true"` | 每个 `<p>`/`<h*>` 独立文本框 | 容器内全部段落级元素合并为一个文本框 |

清单外不要自造其他 `data-pptx-*` 标注表达分组/层级——生成层不解析，分组与层级由 DOM 嵌套顺序和元素先后顺序决定。

合并样式规则：

1. 逐段保留（写入 run 级样式）：`font-size`、`color`、`font-family`、`font-weight`（bold）、`font-style`（italic）、`text-decoration: underline`，以及 `<b>/<i>/<u>/<strong>/<em>/<span>` 的内联样式
2. 取自第一段、整框统一：`text-align`、`line-height`——PowerPoint 的对齐与行距是段落/框级别，一框只能有一种对齐；多段对齐不同时不要用 merge，让各段独立成框
3. 容器自身的 `background`/`border`/`box-shadow`/`border-radius` 照常渲染为 shape，即“形状 + 文本框”两层结构不变，只是文本层从多框塌缩为一框

限制：

1. `data-pptx-merge` 不能嵌套
2. 容器不能用 `background-image`（同书写侧硬约束 3）
3. 容器内不要再放带 `background`/`border` 的子 div——它们仍会渲染为独立 shape，但其中文字已被合并走，产生视觉错位

何时用：内容会在 PPT 里反复编辑的页面必须加；一次性导出归档可不加。生成路线不识别该标注时，文本框粒度以实际产物为准，可编辑性验收仍按「可编辑 PPTX 硬规则」第 4 条执行。

示例（1920×1080px 画布写法，换算见上节）：

```html
<div class="card" data-pptx-merge="true"
     style="position: absolute; top: 260px; left: 120px; width: 800px;
            background: #1A4A8A; border-radius: 16px; padding: 40px 48px;">
  <h2 style="font-size: 48px; color: #FFFFFF;">结论标题（换算后 24pt）</h2>
  <p style="font-size: 28px; color: #DDEEFF;">第一段正文，换算后 14pt。</p>
  <p style="font-size: 28px; color: #FFD166;">第二段：换颜色作强调，同一文本框连续编辑。</p>
</div>
```

### 原生重建文本单元解析（python-pptx 回退路线）

重建脚本从页面 HTML 收集上屏文字时按下列规则划分「文本单元」（run/文本框映射的最小文字块）。实测把 `<span>` 一律划入内联排除集，单页 16 个叶子 span 文字全丢、TEXT_BOX 计数断言击穿：

1. **叶子 span 即单元**：`<span>` 有直接文本且子节点全为内联元素（`b/i/u/strong/em/span/br`）时整体作为一个文本单元；内联排除集只排除「无直接文本的纯样式包装」
2. **交错保序**：段落级元素的直接文本与内联子元素交错（`文字<span>…</span>文字`）时，按 DOM 文档顺序（事件流）收集拼接进同一文本框，run 边界跟随元素边界，禁止重排或合并丢字
3. **粒度对接 data-pptx-merge**：标注 merge 的容器内各单元按文档序合并为一个文本框；未标注时每个段落级元素/叶子单元独立成框
4. **计数断言先于比对**：重建完成先跑「可编辑 PPTX 硬规则」第 4 条的每页 TEXT_BOX 计数断言，再进机械校验文字逐字比对——span 丢失是计数级缺陷，计数断言必须先于渲染目检暴露它

书写侧硬约束 2（span 不得承载主文字）不变；本节是解析侧兜底——遇到违规写法照单元解析、不丢字，问题回书写侧修。

### 六排版陷阱（成因 + 规避）

1. **字体回退**
   - 成因：页面 HTML 使用了目标机器没有的字体（web font、甲方规范指定但本机未装和商业字体如微软雅黑），浏览器预览与 PPTX 打开时都会 fallback 到替代字体，字体度量变化导致换行点漂移、末字掉行、文字溢出容器。
   - 规避：排版字体与交付字体分离——HTML/PDF 预览用本机真实安装的字体（中文正文用系统字体 PingFang SC / Microsoft YaHei），PPTX 文本框写甲方规范指定的字体名（对方机器上有）。分离前提是中文全角等宽：换字体不改变每行字数与换行位置，差异只在西文和标点；西文占比高的页面须逐行另行验证。禁止正文依赖 woff/@font-face 网络字体。
2. **行高漂移**
   - 成因：CSS line-height 是视觉行距倍数，而 HTML 量到的是字体行盒高度、大于实际视觉行距（实测 185 vs 148），照抄成 PPTX 精确行距会把文字整体下压；PowerPoint 行距是段落级，同一容器内多字号共用一个行距时小字被撑开、大字被压扁，相邻两行直接叠压。
   - 规避：行距按倍数换算，不按绝对值（`line-height: 1.5` → PPTX 150% 倍数行距）；单行段落不设精确行距，交给 PowerPoint 按字号自然排；不同字号的行用 `<br>` 或容器拆成独立文本框，各用各的行高。
3. **文本框 autofit**
   - 成因：flex 收缩包裹的容器宽度等于文字实际宽度、零余量，换到 PowerPoint 字体度量稍差最后一个字就被挤到下一行（实测“了”“力”等单字掉行）；PowerPoint 文本框默认自动适应（溢出时缩字或改形状尺寸）会进一步放大字号与位置漂移。
   - 规避：HTML 里确认本来就是单行的文字，生成文本框时直接关自动换行（python-pptx：`tf.word_wrap = False`），从根上不可能折行；统一关自动适应（`tf.auto_size = MSO_AUTO_SIZE.NONE`，枚举来自 `pptx.enum.text`）；多行文本框宽度预留至少半个中文字符余量，并逐页比对折行位置。
4. **形状圆角**
   - 成因：CSS border-radius 是绝对值（px），PPTX 圆角矩形（ROUNDED_RECTANGLE）的圆角半径是相对调整值（占短边一半的比例，范围 0-0.5），直接照抄数值会失真：大卡片圆角过圆，或被生成层忽略成直角。
   - 规避：按公式换算 `adj = radius_pt ÷ (min(w_pt, h_pt) ÷ 2)`。例：HTML `border-radius: 16px` → 8pt，卡片 400×200pt，adj = 8 ÷ 100 = 0.08；python-pptx 写法 `shape.adjustments[0] = 0.08`。
5. **阴影丢失**
   - 成因：CSS box-shadow 的模糊/偏移/多重阴影在 PPTX 里没有一一对应（PPTX 用 effectLst 的 outerShdw，模糊半径口径不同），多数 HTML→PPTX 生成路径直接忽略阴影，卡片层次感瞬间丢失。
   - 规避：不让阴影承载信息层级——页面 HTML 用 1-2pt 实线描边或底色差区分卡片与页面底色，书写侧就完成降级，不依赖生成层保真；视觉验收不把阴影列为必检项。
6. **渐变降级**
   - 成因：CSS 任意角度的 linear-gradient/radial-gradient 超出 PPTX shape fill 的预设渐变能力，生成路径普遍只映射纯色填充；硬转的结果要么整块变错色纯色，要么被直接丢弃。
   - 规避：页面 HTML 书写层禁用 CSS 渐变（书写侧硬约束 3），已有渐变必须在进入 Phase 5 前改为纯色或多个纯色块分段；不得把渐变降级成整页 PNG 贴图——那会触发「可编辑 PPTX 硬规则」第 2 条整页光栅判失败。

### 甲方模板继承

触发条件：用户提供甲方 PPT 模板并要求“必须用我们的模板”。此时不得从零新建文件，必须以模板 `.pptx` 为基底重建；甲方要的是两件具体的事：logo 是模板里的最新版，且他们改母版时这些页面要跟着整体变。

继承规则：

1. 用 `Presentation(甲方模板.pptx)` 打开，删掉模板自带示例页，母版/版式/主题/色板一律不动
2. 每页 `add_slide(官方版式)`，并把版式带到页面上的空占位符删掉
3. logo 等公共元素由版式提供，不画进 HTML 内容层（渲染时跳过 logo 类元素）；这样甲方改母版/版式，全部页面整体跟着变。该路线下「移交前校验」第 9 条的 `midea-logo.png` 页脚引用不再执行，避免双 logo
4. 画布尺寸跟模板走，「画布换算」一节的 960×540pt 不适用；缩放比 = 模板幻灯片宽 pt ÷ HTML 画布宽 px，1920px 画布配 1920pt 模板时该比为 1.0（1 CSS px = 1 pt）
5. 版式里可能藏一个铺满全屏的纯色矩形遮罩（与版式底色同色同尺寸），留着会挡住内容层元素，重建时删除，删除不改变版式外观

基底重建脚本（落 `projects/<任务名>/`；首次运行先看打印出的版式名清单，再回头改 LAYOUT_INDEX）：

```python
from pptx import Presentation

TEMPLATE = "甲方模板.pptx"   # 换成用户提供的甲方模板路径
LAYOUT_INDEX = 1             # 换成版式名清单里选定的内页版式序号

prs = Presentation(TEMPLATE)

sld_id_lst = prs.slides._sldIdLst
for sld_id in list(sld_id_lst):
    prs.part.drop_rel(sld_id.rId)
    sld_id_lst.remove(sld_id)

for i, layout in enumerate(prs.slide_layouts):
    print(i, layout.name)

layout = prs.slide_layouts[LAYOUT_INDEX]
for sp in list(layout.shapes):
    if (sp.width and sp.height
            and sp.width >= prs.slide_width * 0.99
            and sp.height >= prs.slide_height * 0.99):
        print("删除全屏遮罩:", sp.shape_id, sp.name)
        sp._element.getparent().remove(sp._element)

slide = prs.slides.add_slide(layout)
for ph in list(slide.placeholders):
    ph._element.getparent().remove(ph._element)

prs.save("base_from_template.pptx")
print("画布 pt:", prs.slide_width / 12700, "x", prs.slide_height / 12700)
```

## 生成过程产物目录（硬性）

1. PPT 生成的一切过程产物（工作区、脚本、中间渲染图、验证报告）放本次交付目录下的 `projects/`（如 `doc-ppt/test-run/projects/<任务名>/`）。
2. 禁止写入 `~/.agents/projects` 或任何全局目录；发现遗留时迁回交付目录 `projects/_legacy/` 归档。
3. 调用 ppt-master 时显式指定项目工作区为该路径。

## 路由与确认门禁

1. 路由按 ppt-master 的 `workflows/routing.md` 判定：本移交形态（MD 语义源 + HTML 视觉约束、无光栅页框、无既有 PPTX）落 Generate PPTX 普通 Default；仅当同时具备光栅页框清单与 Codex 时才走 image-to-pptx，勿误路由。
2. ppt-master Stage-1/Stage-2 为 ⛔ 两阶段确认门禁：交互场景暂停等待用户显式确认；端到端授权执行场景按显式委托处理（agent 做决策、安装并派生 Stage 2，决策后出示一份完整摘要，不伪造 UI 回执）。
3. 会话 token 预算不足以走完 Step 4-7 时，停在路由定义的 ✅ Checkpoint 干净断点，记录恢复指针（项目路径 + 下一步编号），不得半程产出残缺 PPTX。
4. **用户显式指令优先**：用户明确 skip 某默认步骤（如目检/校验）时，遵从用户指令，不因默认路由强行执行；但须在交付说明中记录被 skip 的项，不得静默省略。

## 交付后验证

结构验证：

1. 页数与母稿一致
2. 每页标题与母稿一致
3. PPT 布局与对应 HTML 基本一致

数据验证：

1. 数据表数值与母稿一致
2. 图表渲染与图表 HTML / 原始 XML 一致
3. 跨页同一指标保持一致

视觉验证：

1. Logo 已正确嵌入封面页和页脚
2. 配色体系无漂移
3. 字号层级清晰
4. 无乱码或格式错位
5. 轻量 MD3 规范化仅体现在容器、字体、间距和语义色层级，不影响图表事实表达

质量收敛通常需要 2-3 轮，每轮只聚焦一个层面。

## 验证工具可信度（先验证验证工具）

结构/数据/视觉三层验证项见「交付后验证」；本节约束验证工具本身：同一个 PPTX，不同渲染器给出的结果可以完全不同，工具不可信时后面每一步都在给假绿灯。在相信任何渲染结论之前，先确认这个渲染器本身能正确渲染。

### 对照实验法（必做）

1. 选样：取一个已知正确的同类文件——甲方模板原件，或上一轮已验收通过的 PPTX
2. 用与待验产物完全相同的工具与参数渲染该样本
3. 判定：已知正确样本同样出现缺陷（中文全变豆腐块、字体整体丢失）→ 是环境/工具问题，不是本次产物问题；样本正常而产物异常 → 才进入产物排查
4. 该步骤必须排在产物排查之前，能省掉数小时在错误方向上的排查

### 可信度排序（macOS）

| 工具 | 结论 | 适用场景 |
|---|---|---|
| Keynote + AppleScript 导 PDF | ✅ 可终审 | 本机唯一能全自动且可信的渲染验证，真演示引擎排版；导 PDF 后逐页出图，与页面 HTML 并排比对 |
| WPS / PowerPoint 人工打开 | ✅ 可终审 | 甲方多半用这一类，交付前人工逐页确认 |
| python-pptx 结构验证 | ✅ 可信（结构层） | 递归展开形状构成、文字逐字比对、尺寸断言；不经渲染器、骗不过计数，但发现不了“看起来重叠”类视觉问题 |
| LibreOffice headless | ⚠️ 版面可信，中文可能全丢 | 取不到 macOS 系统中文字体，渲出豆腐块甚至空白；中文丢失时先做对照实验判定是否环境问题 |
| qlmanage -t 缩略图 | ⚠️ 仅封面 | 见下方局限注记 |

### qlmanage 局限注记

1. `qlmanage -t` 只生成封面（第一张幻灯片）缩略图，内页完全看不到，更不能验证内页可编辑性
2. 它走简化渲染路径，对行距的处理比真 PowerPoint 宽容得多——实测放过 4 个会导致文字重叠的 bug：20 页缩略图逐页看全对，用户在 WPS 里一打开就是文字压文字
3. 适用边界：仅用于快速确认文件可打开、封面版式大体正确；不得作为内页、排版保真或可编辑性的验收依据
4. 「无 LibreOffice 环境的替代目检」第 1 条的 qlmanage 目检受本边界约束：缩略图通过后，仍必须执行「可编辑 PPTX 硬规则」第 4 条的 python-pptx 递归展开验证与本节文字逐字比对

### Keynote 自动化终审（可运行脚本）

```bash
PPTX="$PWD/doc-ppt/项目.pptx"
OUT="$PWD/doc-ppt/test-run/projects/verify"
mkdir -p "$OUT"
osascript <<EOF
tell application "Keynote"
  activate
  set d to open POSIX file "$PPTX"
  delay 4
  export d to POSIX file "$OUT/out.pdf" as PDF
  close d saving no
  quit
end tell
EOF
pdftoppm -png -r 54 "$OUT/out.pdf" "$OUT/page"
```

1. `pdftoppm` 来自 poppler，未安装先 `brew install poppler`；大文件 4 秒不够 Keynote 完成排版时增大 `delay`
2. 产出的 `$OUT/page-*.png` 与 `doc-ppt/pages/*.html` 原图逐页并排比对，重点核对「HTML→PPTX 转换保真」节六排版陷阱的 6 个条目
3. 禁止用 System Events 注入按键翻页截图——按键会打进用户当前正在输入的窗口；只用 Keynote `export` 这类文档级 API，或人工看
4. 本机未装 Keynote 时，退回排序表第 2 行的 WPS / PowerPoint 人工终审，不得改用 qlmanage 顶替

### 机械校验（不依赖渲染器，必做）

1. 形状构成验证：按「可编辑 PPTX 硬规则」第 4 条的 python-pptx 递归展开执行，本节不重复
2. 文字逐字比对：expected_text 抽取首选确定性脚本——headless 浏览器逐页加载 HTML，TreeWalker 按文档序收集上屏文字（跳过 `.notes` 话术容器与任何 `display:none` 内容），零 LLM 参与、可复现，单文件 deck 必用此路；脚本环境不可用才退回 sub agent 按同一口径抽取。落成 `projects/<任务名>/expected_text.txt`；生成层自动追加的页码/页脚文字按同一口径补进该文件，不得放宽为子串匹配来通过。比对脚本落 `projects/<任务名>/compare_text.py`：

```python
import re
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def iter_shapes(shapes):
    for sp in shapes:
        if sp.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_shapes(sp.shapes)
        else:
            yield sp


def pptx_text(path):
    prs = Presentation(path)
    chunks = []
    for slide in prs.slides:
        for sp in iter_shapes(slide.shapes):
            if sp.has_text_frame:
                chunks.append(sp.text_frame.text)
            if getattr(sp, "has_table", False) and sp.has_table:
                for row in sp.table.rows:
                    for cell in row.cells:
                        chunks.append(cell.text)
    return re.sub(r"\s+", "", "".join(chunks))


def main():
    actual = pptx_text(sys.argv[1])
    with open(sys.argv[2], encoding="utf-8") as f:
        expected = re.sub(r"\s+", "", f.read())
    if actual != expected:
        print("FAIL 文字逐字比对不一致")
        print("expected 字数:", len(expected), "actual 字数:", len(actual))
        sys.exit(1)
    print("PASS 文字逐字比对一致")


main()
```

运行方式：

```bash
python3 projects/<任务名>/compare_text.py doc-ppt/项目.pptx projects/<任务名>/expected_text.txt
```

3. 数量比对：图片数、形状数逐页对齐，由第 4 条递归展开统计覆盖，不另列

## 无 LibreOffice 环境的替代目检

渲染目检依赖 LibreOffice 不可用时，按以下替代方案验证，不得直接跳过验证：

1. macOS QuickLook：`qlmanage -t -s 1200 -o <输出目录> <文件.pptx>` 生成缩略图目检封面与版式；qlmanage 只渲染封面且走简化渲染路径，不得作为内页与可编辑性的验收依据，边界见「验证工具可信度」节 qlmanage 局限注记
2. 字节级验证：解压 pptx（`unzip <文件.pptx> -d <目录>`），比对 `ppt/media/` 内嵌媒体的 md5 与源截图/图表 PNG 的 md5（`md5 -q`），确认图片未丢失、未被替换降质
3. 替代目检通过后仍须在交付说明中注明"未经渲染目检，采用替代验证"
