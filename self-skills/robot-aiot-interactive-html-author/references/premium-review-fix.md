# 高级感审查与修复工作流

本文件定义对已生成或既有汇报页 HTML 的审查、诊断与修复流程。
标准来自主文件 `premium-design-standards.md`；本文件只管怎么查、怎么修、按什么顺序修。

## 适用场景

1. 每页生成后的交付前审查
2. 用户明确要求"修复汇报页布局/样式/信息层级"
3. 既有页面 HTML 的高级感升级（不改内容语义）

## 三步流程

### 第一步：扫描

1. 读页面 HTML：确认画布、token 变量、定位方式、引用的图表 HTML
2. 读母稿对应段落：确认标题、结论、上屏内容、话术四要素
3. 修复既有页面时，先盘点再动手：现有 token、版式家族、图表引用、品牌资产

### 第二步：诊断（逐项审计）

按以下清单列出全部问题，先出诊断清单，再动手修：

#### 排版

- 标题是否超过 2 行；字级梯度是否清晰（相邻差 ≥ 2px）
- 正文行高是否在 `1.3-1.6`；单行是否过长
- 数字是否 `tabular-nums`；同列数字是否对齐
- 眉标是否超量（整套汇报每 3 页最多 1 个）
- 是否有竖排旋转文字、装饰分隔线

#### 色彩

- 强调色是否唯一；是否出现 AI 紫/霓虹渐变
- 灰阶是否冷暖混用；是否用了纯黑/纯白
- 阴影是否为纯黑硬阴影
- 单页是否出现深浅底反转
- 页面配色是否与图表真源冲突（冲突时以图表为准）

#### 布局

- 元素是否重叠、溢出画布
- 是否出现"三个等大功能卡片横排"默认版式（数据 KPI 指标卡不受此限）
- Bento 格子数是否等于内容条目数；有无空格子
- 同一版式家族是否重复超过限制
- 区块间距是否落在 `24/32/48px` 基线；是否过挤
- 卡片是否滥用（能用留白/分隔线替代的）

#### 形状与容器

- 圆角是否落在统一档位；有无混用
- 徽章/标签是否超过每页 2 个
- 图片上是否叠加了标签胶囊

#### 内容真实性

- 是否存在无来源的精确数字（未标注"示意"）
- 是否有 AI 套话、占位名称、残留技术名词
- 文案是否语法通顺、指代明确
- 是否命中 `premium-design-standards.md` 第 9 节 AI 痕迹清单任一项

#### 完整性

- 页面数是否与母稿一致；有无占位注释或未完成区块
- 每页 HTML 是否完整可独立运行
- 图表引用是否指向真源文件且未被替换重绘

#### Web 可访问性与语义

- 文本对比度：正文 ≥ 4.5:1，大文字 ≥ 3:1；仅靠颜色传达语义的区块是否有形状/图标/文字辅助
- 语义化标签：标题层级 h1-h6 是否连续不跳级；列表是否用 ol/ul/dl 而非纯 div；表格数据是否用 table/th/td
- 图片与媒体：img 是否有 alt；装饰性图片是否 alt=""；svg 图标是否 aria-hidden="true" 或有 title
- 交互元素：按钮/链接是否有可识别文本或 aria-label；focus 样式是否可见（即使汇报页无键盘操作，保留基础 focus outline 不影响视觉）
- 色彩独立性：状态指示（成功/警告/错误）是否同时有非颜色线索（图标、文字、边框样式）
- 字体回退：font-family 是否包含通用族（sans-serif/serif/monospace）作为 fallback

### 第三步：修复（按优先级）

按以下顺序修，风险从低到高，修到满足标准即停：

1. 色彩清理：统一强调色、去霓虹、统一灰阶、修阴影色调
2. 排版修正：字级梯度、行高、数字对齐、删多余眉标
3. 布局整理：消除重叠溢出、替换等大卡片版式、对齐间距基线
4. 形状统一：圆角档位收口、删多余徽章
5. 内容净化：重写问题文案、删 AI 痕迹、标注示意数据
6. 版式重构：仅当以上手段无法挽救时才动版式骨架；重构不改页面契约（标题/结论/上屏内容/话术）

## 修复红线

1. 不修改图表真源：图表节点、连线、数据、图例的问题不在页面层修，走 `robot-aiot-arch-diagram` 重新生成图表
2. 不改页面契约语义：修复是视觉治理，不是改写结论
3. 不引入响应式、媒体查询、滚动动画
4. 不跨页漂移：修复单页时不得破坏整套汇报的基调、强调色、圆角档位一致性
5. 每次修复可追溯到诊断清单中的具体条目

## 交付前预检清单

每页交付前逐项确认，任一不过则不交付：

### 阻塞项

- [ ] 画布 `1920x1080`，内容不溢出，元素不重叠
- [ ] scale-to-fit 视口自适应壳生效：任意窗口尺寸下画布等比缩放居中、无滚动条
- [ ] 素材图区无滚动条、无拉伸变形、无裸 `<img>`
- [ ] 标题 ≤ 2 行，结论区为第二视觉焦点
- [ ] 四要素完整：标题、结论、上屏内容、话术
- [ ] 图表引用真源，未被替换重绘，事实未被改写
- [ ] 无伪造精确数字；示意数据已显式标注
- [ ] 无残留技术名词（表名、类名、API 路径、未解释缩写）
- [ ] 页面 HTML 完整可运行，无占位注释
- [ ] 强调色、圆角档位、灰阶基调与整套汇报一致
- [ ] 主色填充块上的文字/图标走成对 `on-primary`，无硬编码 `#fff`/`#000`，与主色实算对比度 ≥ 4.5:1（高危组合：近黑主色配深色字，必须实算不目测）

### 非阻塞项（记录 `[UI-WARN]`）

- [ ] 强调色唯一且饱和度 < 80%
- [ ] 无 AI 紫/霓虹渐变、无纯黑硬阴影
- [ ] 无"三个等大功能卡片"、无空 Bento 格子（KPI 指标卡除外）
- [ ] 眉标每 3 页 ≤ 1 个；无编号眉标、无装饰状态点
- [ ] 数字 `tabular-nums` 且对齐
- [ ] 区块间距落在 `24/32/48px` 基线
- [ ] 文案自查完成，无 AI 套话
- [ ] AI 痕迹清单（设计标准第 9 节）零命中
- [ ] 对比度达标、语义标签正确、色彩不独立传达语义

## 交互版专属审查项

仅当交付物为交互版时执行以下检查：

### 阻塞项

- [ ] 纯原生 HTML/CSS/JS，零外部依赖，双击可运行
- [ ] 键盘翻页（←→/Space/PageUp/PageDown/Home/End）全部可用
- [ ] lightbox 可打开且可关闭（Esc 键/点击遮罩）：打不开或关不掉均为阻塞
- [ ] `prefers-reduced-motion` 适配：检测到后所有动画降级为即时切换
- [ ] 动画属性仅限 `transform`、`opacity`、`filter`（进度条 `width` 除外）
- [ ] 数字滚动/图表动画仅触发一次，不循环（animation-fx-catalog 的 canvas FX 除外，但须随页启停、离页销毁）
- [ ] 非活跃页面无残留定时器或事件监听
- [ ] 话术与演讲者专用文字只存在于 `.notes` 容器，可见区域零暴露
- [ ] 含演讲场景时：S 键演讲者窗口可弹出，预览/话术/计时器卡可用，双窗口翻页同步

### 非阻塞项（记录 `[UI-WARN]`）

- [ ] 过渡时长在 `400ms - 600ms` 范围内
- [ ] 入场动画总时长 ≤ 2s
- [ ] 背景特效未使用禁止类型（视频/高频闪烁/3D旋转）
- [ ] hover/focus 状态样式可见且符合 token
- [ ] 单页 DOM 节点数 ≤ 500
- [ ] O 键总览、`#/N/M` 深链、触摸滑动翻页可用
- [ ] 持续动效画布（如有）随页启停，翻离后 rAF 已停止

### deck 结构 lint（含 fragment / 分支 / 热点 / 多页 deck 时逐项过）

- [ ] sceneId 可解析：深链 `#/N/M` 的每段与页内真实序列一一对应，无死链
- [ ] hotspot 目标有序列：每个内容热点/分支入口的 target 指向真实存在的序列，无悬空
- [ ] fragment 落点在页内：每步索引不超过该页步数总量，揭示顺序无跳号
- [ ] 主线不重叠：进度/时间线类页面的多条主线语义不互相覆盖（同一事件不出现在两条主线）

### 动效审查（三法）

1. **瞬态/持续分级**：先给页内每个动效归类——瞬态（入场、数字滚动、sheen sweep，播完即止）或持续（ambient 呼吸、canvas FX、循环装饰）。瞬态不得循环播放；持续必须随页启停（翻离页 rAF 停止、定时器清除）
2. **sweep_static 静默扫查**：入场全部播完后（翻页后约 2-3s）检查整页是否完全静止。除刻意决策（高密度数据页、quote 页允许全静）外，保留一个低幅度活元素（ambient 呼吸 / 慢速 glow / 微幅 canvas）；全静且非刻意 = 记 `[UI-WARN]`
3. **对比度实测法**：对比度不目测，按 WCAG 相对亮度公式实算——sRGB 通道先 gamma 校正（`c <= 0.03928 ? c/12.92 : ((c+0.055)/1.055)^2.4`），亮度 `L = 0.2126R + 0.7152G + 0.0722B`，对比度 `= (L1 + 0.05) / (L2 + 0.05)`；渐变底/图片底上的小字取背景最暗点计算

## 登记版式专属校验（S/M 系 deck）

仅当交付物为登记版式 deck（每页 `<section>` 带 `data-layout="Sxx|Mxx"`，登记定义见 `swiss-layout-system.md`）时执行；其余单文件汇报页跳过本节。本节静态扫描四项全部计入阻塞项，任一不过则不交付。

### 静态扫描（机器可查项，先于目测全部跑完）

#### 1. data-layout 登记校验

- 每页 `<section>` 必须带 `data-layout`，值必须在 S01-S22 / M01-M10 登记范围内；未登记编号（S23、M11、自造名）= 阻塞
- 同一 deck S 系与 M 系不混用：下面两条计数同时 >0 即违规
- `<section>` 出现次数与 `data-layout` 出现次数必须相等，差值即漏登记页

```bash
grep -o 'data-layout="[^"]*"' index.html | sort | uniq -c   # 逐个值对照登记范围
grep -o '<section' index.html | wc -l                       # 应与下行相等
grep -o 'data-layout=' index.html | wc -l
grep -c 'data-layout="S' index.html                         # S/M 混用检查
grep -c 'data-layout="M' index.html
```

#### 2. 大标题居中拦截

登记版式禁则：顶部大标题禁止 `text-align:center`。例外仅限 S03/S09/S10（S 系陈述/分屏版式）与 M01/M02/M07/M08（M 系 hero 页）。

```bash
grep -nE 'text-align: ?center' index.html
```

命中行逐个确认所在页的 data-layout：非例外版式且命中元素是页级大标题（h1/h2 或标题字号档元素）= 阻塞，改为左对齐贴左上内容轴。卡片内部小元素居中、时间线 label 的 `translateX(-50%)` 居中不属于本项。

#### 3. SVG 可见文字拦截

SVG 只画几何线条/圆/路径/箭头，不写可见文字；所有文字标签用 HTML 放网格、卡片或 caption 里。

```bash
grep -n '<text' index.html
```

`<svg>` 内命中即阻塞：删除 `<text>`，标签改 HTML 元素按网格落位；引线保留在 SVG 里，标签文字一律 HTML。

#### 4. nav-safe 底部安全区校验

分页圆点 bottom 22px，登记版式统一预留底部 86px 安全区（规则见 `web-slide-strategies.md` nav-safe 节，此处只做机器查与实测，不重述）。

```bash
grep -nE 'align-items:end|align-self:end|margin-top:auto|bottom: ?0' index.html
```

命中处逐个确认：元素最低边缘距画布底 ≥86px，或所在版式已内置安全区。caption、脚注、时间线下 label、KPI 小字是最高发侵入点；手写贴底命中的页面必须再走下节实测拿 navSafeIntrusionPx 定论。

### 后验测量（先量再修，不目测猜）

溢出、底部空白、标题间距、安全区侵入一律实测，目测只做最终风格确认。入场动画稳定后（翻页约 2-3s）再量，不把动画中间态当溢出。

**方法一：headless Chrome 逐页截图**

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --window-size=1920,1080 \
  --virtual-time-budget=6000 \
  --screenshot=page-03.png "file://$PWD/index.html#/3"
```

多页 deck 按 `#/N` 深链逐页截图；Linux 环境用 `google-chrome --headless=new` 或 `chromium` 等价命令。截图逐页看：溢出、贴住、安全区侵入。

**方法二：getBoundingClientRect 四值实测**（比截图精确，控制台执行）

```js
document.querySelectorAll('section[data-layout]').forEach(sec => {
  const sr = sec.getBoundingClientRect();
  const k = sr.height / 1080;  // scale-to-fit 缩放系数，把实测值折回 1920x1080 画布 px
  let overflow = 0, maxBottom = 0;
  sec.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) return;
    overflow = Math.max(overflow, r.bottom - sr.bottom, r.right - sr.right);
    maxBottom = Math.max(maxBottom, r.bottom);
  });
  const title = sec.querySelector('h1,h2');
  const next = title && title.nextElementSibling;
  console.log(sec.dataset.layout, JSON.stringify({
    overflowPx: Math.round(overflow / k),                                   // >0 = 溢出
    bottomWhitespacePx: Math.round((sr.bottom - maxBottom) / k),            // 防"超出修成巨空"
    titleGapPx: next ? Math.round((next.getBoundingClientRect().top - title.getBoundingClientRect().bottom) / k) : null,
    navSafeIntrusionPx: Math.round(Math.max(0, maxBottom - (sr.bottom - 86 * k)) / k)  // >0 = 侵入安全区
  }));
});
```

隐藏页（display:none）rect 全 0，测量无效：逐页翻到当前页再量（控制台先执行 `location.hash = '#/3'`），或在 devtools 里临时移除非活跃页隐藏后整批量。

**修完反查**：修溢出后 bottomWhitespacePx 变大 = 修过头，恢复部分间距或放大最后一块再量；每轮只做一个档位的调整，改完重跑测量，不连改两轮再验。

### overflow 修正阶梯（按实测 overflowPx 分级处置）

| 实测溢出 | 处置 | 禁止动作 |
|---|---|---|
| 1-40px | 只微调：上移内容组，或收紧一处 gap/padding | 删内容 |
| 40-90px | 局部压缩 gap/padding，或降低一个模块高度，优先保内容 | 删内容、缩字号 |
| 90-160px | 轻微压标题档位或压缩一段正文，再考虑拆页 | 直接换版式 |
| 160px+ | 才允许：换更高容量登记版式、合并模块、删内容、拆页 | — |

- 禁止靠降低字号解决拥挤；字号下限按 `typography.md` 第四节（18/16/14px）守住
- 拆页/换版式必须回 `swiss-layout-system.md` 的 P0 匹配表重选登记版式，不临时发明未登记结构

### title gap 校验

- 两段式页面（顶部标题 + 下部长正文/引用/图表）：titleGapPx 实测 65-86px
- 章节级标题-卡片间距 ≥97px（S15/S16 矩阵与微卡页）
- titleGapPx <54px = 标题与正文贴住，阻塞
- titleGapPx >160px 且非刻意留白记 `[UI-WARN]`：多为修溢出的副产品，按修完反查处理

### 与现有流程的衔接

1. 本节静态扫描四项与 overflowPx >0、navSafeIntrusionPx >0、titleGapPx <54px 阈值全部计入"交付前预检清单 · 阻塞项"；阻塞项中"内容不溢出，元素不重叠"以本节实测值判定，不以目测判定
2. 未过项走第三步修复顺序处理；换版式骨架级修复仍遵守修复红线第 6 条——不改页面契约（标题/结论/上屏内容/话术）
3. 审查报告逐页附 overflowPx / bottomWhitespacePx / titleGapPx / navSafeIntrusionPx 四值；无测量记录的页面不算通过审查

## 高级感评分与终局三问（跨文件衔接）

本节管审校阶段怎么调用评分。五维打分本体（信息传达 / 视觉张力 / 品牌契合 / 技术稳健 / 受众适配）、受众权重表与一票否决在 `multi-version-selection.md` §5，本文件不复制；终局三问只在本节定义。

### 触发时机

1. 多版本并行场景：Phase 5 打分前触发——先过本文件合格门（交付前预检清单阻塞项＋交互版专属审查项＋登记版式专属校验），未过的版本回三步流程修完再打分，衔接细则见 `multi-version-selection.md` §9
2. 单版交付场景：交付前预检清单全过、且用户问"够不够高级/要不要再打磨"时触发；例行交付不强制评分
3. 既有页面高级感升级场景（适用场景 3）：修复前先跑一次终局三问留底，修复后再跑对比

### 五维打分的证据分工

1. 技术稳健维：直接取本文件阻塞项通过情况与四值实测结果，不另行打分
2. 可访问性视角：直接取本文件"Web 可访问性与语义"清单与动效审查第三法（对比度实测法）
3. 信息传达 / 视觉张力 / 品牌契合三维：按 `multi-version-selection.md` §5 表打分，证据取本文件第二步诊断清单与 `premium-design-standards.md` §12 品味六维的判定结果

### 终局三问（合格门通过后的总判，按套执行）

1. 截图传播：任意一页截图发到工作群，会让人停下来看吗——不会＝视觉张力只是模板级合格
2. 一句话记忆：看完能复述出整套汇报的主张吗——不能＝信息传达失败
3. 跨时代：5 年后回看会显得廉价吗——对照 `premium-design-standards.md` §9 AI 痕迹清单与 §12 品味六维总判

三问不打分，只记是/否与一句话依据，结果附入审查报告。

### 不通过的回退

1. 三问任一"否"：不阻塞交付（阻塞以交付前预检清单为准），记 `[UI-WARN]` 并给出可执行修复方向，回第三步修复顺序执行；修复仍守修复红线（不改页面契约、不动图表真源）
2. 每轮三问审查只改一类问题，改完重跑三问与四值实测，不连改两轮再验（对齐修完反查）
3. 评分与三问结论冲突（加权总分高但三问全"否"）：如实摆出冲突点与取舍让用户裁决，不平摊、不折中（对齐 `multi-version-selection.md` §6 选优决策规则）

## 审查报告格式

```text
--- 高级感审查: <页面文件> ---
  诊断: N 项（排版 a / 色彩 b / 布局 c / 形状 d / 内容 e / 完整性 f / Web语义 g）
  已修复: M 项
  阻塞项: 通过 / 未通过（列出）
  UI-WARN: K 项（列出）
  图表真源: 未触碰 / 需转 bridge 审查（说明原因）
  Web 可访问性: 通过 / 有问题（列出）
  交互版审查: 不适用 / 通过 / 有问题（列出）
  登记版式校验: 不适用 / 通过 / 有问题（列出 overflowPx / titleGapPx / navSafe 实测值）
  高级感评分: 不适用 / 加权总分 X.XX（三问: 传播 是|否 · 记忆 是|否 · 跨时代 是|否）
  结论: 可交付 / 需返工
```
