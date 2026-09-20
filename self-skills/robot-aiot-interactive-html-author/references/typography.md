# 演示 Deck 排版阶梯

## 定位与分工

1. 本文件管演示 deck 专用的字号双约束、字重阶梯、中文大标题分档与最小字号下限
2. `design-system-standards.md` 管语义 token、汇报页字级体系与 CJK 排版通则（§15）；本文件不重复其内容，只给 deck 专用阶梯
3. `web-slide-strategies.md` 管密度模式二分（演讲型/阅读型）与文案公式；登记版式（S/M 系，见 `swiss-layout-system.md`）默认属演讲型大屏场景
4. 画布锚定：固定 1920×1080，1vw≡19.2px，1vh≡10.8px；本文件所有推导公式仅用于推导与校验新档位，代码一律写 px
5. 同一文本元素同时命中多档下限时，全部满足、取最严

## 一、字号双约束与画布推荐值

大字号必须限高，否则在内容多的页溢出画布。推导公式 `min(Xvw, Yvh)` 要求 Y ≥ X × 1.6：16:9 屏上 1vw:1vh ≈ 1.78，Y 太严（如 min(7vw,10vh)）会让字号被高度上限截断、不再受宽度主导，整体显小。固定画布下直接取 px：

| 用途 | 推导公式 | 画布值 |
|---|---|---|
| 封面巨字 / 宣言 | min(11.6vw, 19vh) | 205px |
| 章节标题 | min(7vw, 12vh) ~ min(7.4vw, 13vh) | 130-140px |
| 巨号 KPI | min(8.4vw, 14vh) | 151px |
| 收束宣言巨字 | min(8vw, 14vh) | 151px |
| 中数字 / 编号 | min(4.6vw, 8.5vh) ~ min(5.6vw, 10vh) | 88-107px |
| 账单巨数（限高防溢出） | min(13vw, 16vh) | 173px |

新档位按公式推导后取整为 px；禁止在代码里直接写 vw/vh 字号。

## 二、字重阶梯（越大越细，越小越粗）

"越大越细、越小越粗"是硬阶梯，不是感性描述：

| 字号区间 | 字重 | 典型场景 |
|---|---|---|
| ≥154px | 200 ExtraLight | 封面大字、巨号 KPI、statement |
| 77-152px | 200-300 | 章节标题、大编号 |
| 35-75px | 300-400 | 中型标题、takeaway 标题（≈35px）、中号数字 |
| 16-33px | 400-500 | 正文段落、卡片描述、说明文字 |
| 14-15px | 500-600 | meta、kicker、角标、图表标签、caption 强调 |

硬规则：

1. 同一页内，字号越小的元素字重必须 ≥ 字号越大的元素——不允许 16px 正文用 300 而 35px 标题用 500
2. 16px 左右小字拒绝 weight 300（太细不可读），最低 400，推荐 500
3. 大标题保持轻字重（200/300），重点词/数字 300；不因样式 helper 残留 700-900 而加粗
4. 反白大标题内强调字：拉丁可用 `italic + weight 300`（不用 accent 色——accent 压 accent 看不见）；中文禁伪斜体（§15 条 6），降级为字重或颜色区分

**系统栈诚实声明**：不引外部字体（SKILL.md 硬约束 11）。拉丁无衬线 `system-ui / Helvetica Neue / Arial`，mono `ui-monospace / SFMono-Regular / Menlo / Consolas`，衬线金句用系统衬线（Songti SC / SimSun / serif），中文沿用全局系统栈（见 `web-slide-strategies.md` 双语规则第 4 条）。200/300 细字重依赖字体自带字重族：macOS PingFang SC 有 Ultralight/Thin、Windows 微软雅黑有 Light；平台缺对应档时用系统可得的最细档，不用 `-webkit-text-stroke`/text-shadow 伪造细度，不为字重引外部字体。mono 数字 `font-feature-settings:"tnum"`；数据数字按 §15 条 8 用西文数字 + `tabular-nums`。

## 三、中文大标题分档

中文方块字视觉面积比拉丁重，不能直接套拉丁 hero 字号。生成前先按中文标题长度降级：

| 中文标题形态 | 字号 |
|---|---|
| 1 行，≤8 个中文字符 | 121px |
| 2 行，每行 ≤8 个中文字符 | 110px |
| 2 行，任一行 9-12 个中文字符 | 99px |
| 3 行或更长 | 先改写标题缩短；实在不能改时 88px |

规则：

1. 中文标题优先改短，其次降字号；不要让标题挤占下方图文区域（章节级标题-卡片间距 ≥97px）
2. 英文、数字型 hero 可以更大（205px 档），中文方法论页必须更克制
3. 中文巨标题字距归零、行高 1.15-1.25（§15 条 3/4）；拉丁巨字才可收紧至 letter-spacing -.025em ~ -.05em、line-height 0.9-1.0

## 四、最小字号下限

演示 deck 不是网页说明页，投屏时不能出现 10-12px 注释字。登记版式内屏上任何文字的下限：

| 文本类型 | 下限 |
|---|---|
| 正文段落 / 主要说明 | 18px |
| 卡片描述 / 列表 / 时间线说明 / caption / 图注 | 16px |
| meta / kicker / mono label / 图表标签 | 14px |

三层下限关系（作用域不同、并存，同一元素取所有适用档中最严）：

1. **本表 18/16/14px**：登记版式（S/M 系）屏上任何文字的底限
2. **演讲大屏必读档 ≥40px**：密度模式选"演讲型"时，观众必读文字（标题、核心结论、关键数字）的下限，见 `web-slide-strategies.md` 密度模式二分；次要文字（caption、meta、注释）不受必读档约束，但必须守住本表下限
3. **全局底线 16/12px**：SKILL.md 硬约束 4，任何形态的正文/说明标签绝对底线

内容过多时先压缩文案、拆页或更换登记版式；禁止靠降低小字字号解决拥挤。图注、时间线说明、KPI 注释、底部脚注尤其要守住下限。

## 五、中文排印细则与字体配对

本节管中文字体性格分类、中西文配对、正文与数字排印细则、webfont 体积闸，适用于演示 deck 与汇报页，不改变第一至四节的 deck 专用阶梯。分工：CJK 排版通则的权威来源是 `design-system-standards.md` §15（中文排版十条），本节只做细化与交叉引用，不复制条文；西文展示字体禁用清单与配对张力规则见 `premium-design-standards.md` §4 条 12/13。

### 5.1 中文字体性格分类

按"系"选字：先定页面情绪，再定字体，不凭感觉挑名字。

| 系 | 情绪 | 适用页型 | 代表字体（系统栈或开源可捆绑） |
|---|---|---|---|
| 宋体系 | 出版正统、文气、庄重 | 封面宣言、文化叙事、年报引文、章节题页 | 系统：Songti SC（macOS）、SimSun（Win）；可捆绑：Noto Serif SC / 思源宋体（OFL，7 字重，Heavy 可当 display）、汇文明朝体、京华老宋体（免费商用） |
| 黑体系 | 现代、中性、工程感 | 数据看板、架构图、技术汇报、正文兜底 | 系统：PingFang SC（macOS）、Microsoft YaHei（Win）；可捆绑：Noto Sans SC / 思源黑体、未来荧黑 Glow Sans SC、霞鹜新晰黑（均 OFL） |
| 楷体系 | 手写温度、公文庄重 | 引文块、教育人文页、传统风汇报、贺词 | 系统：Kaiti SC（macOS）、KaiTi（Win）；可捆绑：霞鹜文楷 LXGW WenKai（OFL） |
| 圆体系 | 圆润亲和、童趣 | 消费/教育向、游戏化页、亲和活动页 | 系统：Yuanti SC（仅 macOS）；Windows 无系统圆体，跨平台必须捆绑；严肃数据页不用 |
| 手写系 | 个人化、随性、手账感 | 小面积批注、彩蛋、生活化场景强调 | 系统：Hannotate SC、HanziPen SC、Xingkai SC（均仅 macOS）；Windows 基本缺位，无法捆绑就跨平台不用 |

使用纪律：

1. 正文只在宋/黑/楷三系里选；圆体/手写系只做点缀，整段使用是阅读阻力
2. display 个性字体（得意黑 Smiley Sans、老宋、明朝体）只上标题；得意黑是中文罕见的原生斜黑体，运动感强，正文用它会晕
3. 一页最多两个中文字体家族：中文字体单文件全量 5-15MB，超过两族同时毁加载与统一性
4. 宋体细横笔画在 18px 以下开始发糊断笔，宋体正文下限 18px（与第四节正文下限一致）；更小的字回黑体
5. 跨平台交付（Win/macOS 都可能打开的 HTML）不赌单平台系统字体：要么捆绑开源体（过 5.7 体积闸），要么写双平台 fallback 栈（如 `"Songti SC", "SimSun", serif`）
6. 繁体内容选繁体字形变体（如 Noto Serif TC / 思源宋体 TC），不用简体字体硬排繁体，反之同理——两岸字形差异（"骨""直""门"）会被读者一眼识别为不专业

### 5.2 中西文配对规则

中文为主体、西文为点缀（拉丁字符、数字、kicker、展示大字），按六条执行：

1. **fallback 链顺序：西文在前、中文在后**。`font-family` 逐字符匹配，西文字体不含 CJK 码位，汉字自动穿透到后面的中文字体；反过来写（中文在前），拉丁字符全被中文字体自带的呆板西文吃掉，等于白配

```css
/* 黑体场景：西文 → 中文 → 系统中文 → 泛型 */
font-family: "Geist", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
/* 宋体场景 */
font-family: "Newsreader", "Noto Serif SC", "Songti SC", "SimSun", serif;
```

2. **字号补偿**：同字号下西文小写视觉偏小（x-height 只占字身一半，汉字占满字身）。系统解法 `font-size-adjust: from-font`（较新特性，不支持时自动忽略）；经验解法选 x-height 高的西文体（Geist / Newsreader / Work Sans 都高），或对西文 span 字号 +8% 起步再目测校准
3. **字重对齐**：中文可用字重档比西文粗疏（Microsoft YaHei 仅 Light/Regular/Bold），西文 300 配中文 400 会出现视觉重量跳变；同一行内中西字重差 ≤100，西文展示体只有单一细字重档时（如 Cormorant），中文同步取轻档
4. **基线对齐**：中西 baseline 不一致的症状是西文单词在中文行里"下沉"。优先换 x-height 更高的西文体；仅 display 大字场景允许对西文 span 用 `vertical-align: -0.02em ~ -0.06em` 微调，正文不这么修（维护成本大于收益）
5. **数字一律走西文字体**：fallback 链首位的西文体接住全部拉丁与数字（§15 条 8 西文数字）；中文字体自带数字是重灾区，数据页不允许中文字体的数字出场
6. **西文展示体选择纪律**：先过 `premium-design-standards.md` §4 条 12 禁用清单（17 个）与条 13 张力论证（年代反差 / 软硬反差 / 宽度反差，说不出理由就退回单字族加减字重）；中文黑体正文 × 西文 serif 展示是最安全的跨类结构；选定的西文体必须随稿捆绑或确认渲染环境可用（§4 条 1），不可得时退回系统拉丁（Helvetica Neue / Arial / Georgia）

中英之间的空格按 §15 条 1（盘古之白）执行，冲突声明见 5.8。

### 5.3 推荐配对表

表中中文字体全部为系统栈或开源可捆绑，西文字体全部为 OFL 开源可捆绑，且已逐一核对 `premium-design-standards.md` §4 条 12 禁用清单（17 个），无一命中；西文无法捆绑时按 5.2 条 6 退回系统拉丁。

| # | 中文字体 | 西文字体 | 适用场景 | 情绪关键词与配对逻辑 |
|---|---|---|---|---|
| 1 | Noto Serif SC / Songti SC、SimSun | EB Garamond | 文化叙事封面、年报引文、书籍感章节页 | 古典文气；年代反差——老宋体 × 16 世纪法国老衬线；Garamond x-height 低，同行混排西文 span +8% 补偿 |
| 2 | Noto Serif SC Heavy | Cormorant Garamond | 画廊式大字页、奢侈感 statement、时尚/文化展封面 | 高反差奢侈；粗细反差——Cormorant 极细 × 宋体极重同屏；Cormorant 须 ≥40px 才成立，小字号笔画会断 |
| 3 | PingFang SC / Microsoft YaHei / Noto Sans SC | Geist | 科技架构汇报、数据看板、产品能力页 | 精密工程感；同族咬合——Geist 高 x-height 与黑体天然齐，零翻车兜底组合（§4 条 1 既定示例） |
| 4 | PingFang SC / Noto Sans SC | Newsreader | 暖调编辑叙事页、调研报告长文、方法论页 | 安静出版感；形式对比——屏显优化的过渡衬线 × 中性黑体 |
| 5 | 霞鹜文楷 LXGW WenKai | Lora | 引文块、教育人文页、个人化叙事 | 温暖文气；软硬反差——楷体是中文的"引用语气"，Lora 笔刷感衬线呼应手写温度 |
| 6 | 得意黑 Smiley Sans | Archivo（Expanded/Black） | 发布大字报、活动主视觉、运动/宣言页 | 大胆动感；宽度反差——原生斜黑 × 超粗宽体西文；两者都是 display 专用，禁上正文 |
| 7 | 汇文明朝体 / 京华老宋体 | Source Serif 4 | 复古出版、报头感标题、文化展、数据人文题材 | 铅字旧书感；年代反差——旧字形明朝体当 display，正文交给现代屏显衬线 |
| 8 | 未来荧黑 Glow Sans SC | Schibsted Grotesk | 现代品牌页、行业趋势页、窄长 display | 几何现代；未来荧黑 Compressed 宽度可做窄长大字，Schibsted 带报业血统 |
| 9 | Noto Sans SC / PingFang SC | JetBrains Mono / Geist Mono | 技术文档页、架构标注标签、编号与代码展示 | 终端感；等宽当主角——mono 只用于标签/编号/代码，整段正文用等宽行长膨胀约 30% |
| 10 | Kaiti SC / KaiTi | Work Sans | 公文风汇报批注、传统风文档引文、政企页 | 公文庄重 × 中性西文；软硬反差——Work Sans 平稳不抢楷体笔意 |

配对自查：每组必须说出一条张力理由（年代 / 形式 / 软硬 / 宽度反差），说不出就退回单中文字族加减字重（§4 条 13）；全套汇报最多两个字体族（§4 条 1），表中"中文 + 西文"合计即两族——数据页需要 mono 数字时，mono 占用该套的西文名额，不另加第三族。

### 5.4 中文大标题分档补充

分档表（121/110/99/88px）与"优先改短、其次降字号"见第三节，此处不重复；本节补竖排标题、换行禁则、字距微调三项。

**竖排标题（中文独有的 display 手段）**

```css
.vertical-title {
  writing-mode: vertical-rl;
  text-orientation: upright;   /* 汉字保持直立，不是躺倒旋转 */
  letter-spacing: 0.06em;      /* 竖排时字距即呼吸，取 0.04-0.1em */
  line-height: 1.3;            /* 竖排时行高即列间距 */
}
.vertical-title .num { text-combine-upright: all; } /* 两位以内数字/字母合体直立 */
```

```html
<h1 class="vertical-title">年度技术<span class="num">Q3</span>回顾</h1>
```

1. 仅限封面书脊式标题、诗词引文、目录页；每页最多一处竖排
2. 竖排字号沿用第三节对应分档；竖排块高度不超过画布高的约 2/3（≈720px），上下留呼吸
3. 竖排中的西文与数字：两位以内用 `text-combine-upright: all` 合体直立；更长的编号、单词拆出竖排块单独横排，不逐字硬立
4. 与 `premium-design-standards.md` §4 条 8 的边界：该条禁的是"旋转文字"（`transform: rotate()` / 字形躺倒的侧排）与装饰性竖排西文标签；字形直立的中文竖排是承载内容的排布手段，不在禁列，但无内容的纯装饰竖排文字仍然禁止

**标题换行禁则**

1. 固定画布（1920×1080）优先在语义单元边界手动 `<br>`，不赌自动换行——自动换行位置随渲染引擎与字体回退漂移，跨机演示不可控
2. 不可拆行：词内部、专有名词/产品名、数字+单位（3.5 GHz）、数字+量词（320 万元）、百分号结构（92%）
3. 禁孤字：任何一行不允许只剩 1 个字；两行标题两行字数差 ≤3 字，上行略长于下行比下行更长更稳
4. 标题含顿号时在顿号后断行；展示标题不带句号（§15 条 10）
5. 自动换行兜底用 `text-wrap: balance`（≤6 行的标题，均衡各行长度、消灭孤字行）

**标题字距微调**

1. 默认归零（第三节规则 3、§15 条 3），此条不变
2. 121px 及以上封面巨字档，笔画密的字（如"鑫""睿"）显挤时可收 -0.01em ~ -0.02em：作用于整行而非个别字，不得超过 -0.02em——汉字满格设计，再负笔画相撞
3. 暗底按 `premium-design-standards.md` §4 条 9 补偿 +0.01em（浅字深底视觉膨胀）
4. 中西混排标题：负字距只作用于拉丁 span（§15 条 3），中文 span 保持归零
5. 禁止给中文标题加正字距"显高级"：0.05em 以上标题松垮像临时占位；宽字距（0.08-0.2em）只属于混排中的拉丁 uppercase kicker（§15 条 3）

### 5.5 正文排印细则

行高、字距、标点、伪斜体通则见 §15 条 2/3/4/6/7，此处只给落地细则：

1. **行高与行长联动**：§15 条 4 定 CJK 正文 1.75-1.85；细化——行长 <30 字/行取 1.7-1.75，30-38 字/行取 1.75-1.85 上沿，行越长回行越远、越需要大行距当"轨道"。`premium-design-standards.md` §4 条 5 的行高 1.3-1.6 是拉丁为主正文的值，中文正文以 §15 条 4 为准（`design-system-standards.md` 是细则权威来源）
2. **行长**：正文单行宽度见 `premium-design-standards.md` §4 条 5（约 32 个中文字），不重复数值
3. **段间距**：段落靠间距分隔，段间距 = 0.5-1 倍行高，按 8px 基线取 16-24px（`design-system-standards.md` §4.3 档位）；卡片内正文可降到 12-16px
4. **首行不缩进**：屏显正文 `text-indent: 0`；首行缩进（2em）只属于纸质长文，汇报页与 deck 不用；禁止"缩进 + 段间距"双重分隔
5. **标点悬挂**：`hanging-punctuation: first allow-end`（仅 Safari 支持）；跨浏览器兜底——段首开引号用 `text-indent: -0.5em` 把开引号悬挂出去，让左边缘对齐；行尾连续全角标点（如「）。」）的空洞用 `font-feature-settings: "halt" 1` 收窄
6. **避头尾**：`line-break: strict`（禁句号逗号出现在行首、开引号出现在行尾，中文排版底线）；`overflow-wrap: break-word`（长 URL、英文串不撑破容器）
7. **强调手段**：中文正文强调只用字重 / 颜色（§15 条 6/9）；着重号 `text-emphasis: dot` 是中文原生强调（Chromium / Safari 可用，Firefox 不支持时降级字重强调）；引文块可整段换楷体——楷体即中文的"引用语气"，段间换字体不违反 §15 条 9（该条禁的是一句话内切换）
8. **正文兜底**：`text-wrap: pretty`（消灭行尾孤词，西文效果明显、中文轻微，全局给正文无副作用）

> 规范副本：`templates/deck-skeleton.html` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```css
:root {
  line-break: strict;
  overflow-wrap: break-word;
  font-synthesis: none;   /* 禁合成斜体/加粗，§15 条 6 的保险丝 */
}
body {
  font-size: 18px;        /* 中文正文基准，守住第四节 18/16/14px 下限 */
  line-height: 1.8;
  text-indent: 0;
}
p { text-wrap: pretty; }
p + p { margin-top: 20px; }         /* 段间距替代首行缩进，取 16-24px 档 */
.quote-hang { text-indent: -0.5em; } /* 段首开引号悬挂兜底 */
.cjk-display { font-feature-settings: "halt" 1; } /* 展示大字全角标点挤压 */
```

### 5.6 数字与单位排印

西文数字 + `tabular-nums` 的通则见 §15 条 8、第二节与 `premium-design-standards.md` §4 条 6/11，细则：

| 项 | 规则 | 正例 | 反例 |
|---|---|---|---|
| 表格数字 | 数据表、KPI 列一律 `font-variant-numeric: tabular-nums`，否则 1 和 8 宽度不同、列边缘抖动 | 同列右对齐或小数点对齐 | 比例数字导致列参差 |
| 千分位 | ≥4 位整数用西文逗号分节；年份、页码、端口号、产品型号不分节 | 12,480 台 / 2026 / 8080 | 12480 台 / 2,026 |
| 大数 | ≥8 位改用中文计数单位，保留 1-2 位小数；同一列口径统一，不混用 | 1.2 亿 / 3,500 万 | 120,000,000；同列既写 3,500 万又写 1.2 亿 |
| 数字与拉丁单位 | 数字与拉丁单位符号之间加一个半角空格 | 3.5 GHz / 120 ms / 64 GB | 3.5GHz |
| 数字与符号 | %、‰、° 紧贴数字，不加空格 | 92% / 45° | 92 % |
| 数字与中文量词 | 按盘古之白（§15 条 1）加一个半角空格 | 部署 3 套 / 320 万元 | 部署3套 |
| 百分号 | 百分数与百分点严格区分语义 | 同比提升 2.3 个百分点 | 用"提升 2.3%"表述百分点差 |
| 货币符号 | ¥/$/€ 前置紧贴数字；中文货币词"元/万元/亿元"后置并按盘古之白加空格；数据表在列头标单位（万元），单元格纯数字不重复符号 | ¥1,200 / $4.2M / 4.2 万元 | 1,200¥ / 4.2万元 |
| 数值区间 | 区间符号全套统一（"～"或"至"选一），不与半角连字符混用 | 10～20 台 | 同稿混写 10-20 台 / 10～20 台 |

```css
.data, table { font-variant-numeric: tabular-nums; }
```

### 5.7 webfont 体积闸

**启用前提**：默认一律系统栈——第二节系统栈诚实声明、SKILL.md 硬约束 11（禁 CDN 与外部字体）、`web-slide-strategies.md` 双语规则条 4；仅当用户明确要求个性字体且允许随稿捆绑时（`premium-design-standards.md` §4 条 1、`self-contained-html.md` 的 @font-face + base64 woff2 路径），本节才启用。外链 Google Fonts 一律禁止（硬约束 11）。

体积闸（任一超标即回退系统栈）：

| 项 | 闸值 | 说明 |
|---|---|---|
| 全量中文 webfont | 禁止嵌入 | 单文件 5-15MB，base64 全量内嵌毁首屏也毁文件体积 |
| display 字体子集 | ≤100KB | 按页面实际出现的字符裁剪（封面/章节页往往只有 20-200 字） |
| 正文字体子集 | ≤2MB（woff2） | 按常用 3500 字集裁剪；超标先减到正文实际用字，再超回退系统栈 |
| 全套字体族数 | ≤2 族 | §4 条 1，中文 + 西文合计 |

子集化与加载策略：

1. **按实际用字子集化**：display 字体按页面字符清单裁剪；正文字体按常用 3500 字 + 正文实际用字补裁。构建期用 `cn-font-split` 或 fonttools 的 `pyftsubset`（仅构建期工具，产物 HTML 保持零运行时依赖）；需要 unicode-range 分片时自托管分片文件并在 @font-face 中声明
2. **`font-display: swap`**：中文字体体积大下载慢，白屏等字体是最差体验；swap 先以系统栈渲染、字体就绪后替换，代价是一次文本闪换（FOUT），汇报页可接受
3. **3500ms 超时锁定**：swap 只解决"先显示"，不解决"迟迟不到"。3500ms 内 webfont 未就绪则给根元素加类锁定系统栈，防止字体迟到引发演讲中途回流：

```html
<style>
  @font-face {
    font-family: "LXGW WenKai";
    src: url("assets/lxgw-wenkai-subset.woff2") format("woff2");
    font-weight: 400;
    font-display: swap;
  }
  body { font-family: "LXGW WenKai", "Kaiti SC", "KaiTi", serif; }
  /* 超时锁定后即使 webfont 迟到也不再替换，防演讲中途回流 */
  html.font-timeout body { font-family: "Kaiti SC", "KaiTi", "PingFang SC", serif; }
</style>
<script>
  Promise.race([
    document.fonts.load('400 18px "LXGW WenKai"', '永字八法'),
    new Promise(function (_, reject) { setTimeout(reject, 3500); })
  ]).catch(function () {
    document.documentElement.classList.add('font-timeout');
  });
</script>
```

4. **捆绑方式**：自包含单文件交付用 base64 内嵌（体积按 1.33 倍计入上表闸值）；多文件交付用同目录 woff2 相对路径引用。捆绑后必须在 Windows 与 macOS 双端实测各一遍，确认 fallback 栈在字体缺失时正确触发

### 5.8 冲突处理声明

1. **盘古之白（主声明）**：有排印流派主张"中英之间不加空格"，理由是 fallback 链的字体自带留白已足够。该条与 `design-system-standards.md` §15 条 1（盘古之白：CJK 与拉丁/数字之间加一个半角空格）冲突。**处理：以 §15 条 1 为准，本章不采纳"不加空格"条**，本章全部中西混排示例按盘古之白书写。两者并不互斥：字体留白解决字形拥挤，盘古之白解决字符级分隔，后者是本技能硬规范
2. **竖排边界**：中文竖排与 `premium-design-standards.md` §4 条 8"禁止竖排旋转文字"的边界按 5.4 执行——字形直立、承载内容、每页一处的竖排允许；字形躺倒的旋转文字与装饰性竖排西文标签禁止
3. **双 sans 边界**：`premium-design-standards.md` §4 条 13"禁止双 sans"约束的是西文 display + body 双族结构；中文主体 + 西文点缀场景下的中文黑体 × 西文 grotesque（配对表 #3、#8）属 §4 条 1 的既定组合，不受该禁约束，但仍须给出张力理由，否则退回单字族加减字重
