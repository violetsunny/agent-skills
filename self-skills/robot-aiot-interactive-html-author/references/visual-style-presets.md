# 视觉风格预设库

## 定位

deck 换肤素材库。每套预设 = 一组语义 token 覆盖集，直接覆盖 `design-system-standards.md` 定义的 `--primary-color` / `--surface-color` / `--text-primary` 等变量，不另造 token 体系。
选用流程：受众 + 情绪 → §1 mood 路由表 → 锁定一套 → 全套 deck 只用一套，不混用。
字体一律系统栈（零依赖单文件 HTML 不外链字体）；动效一律 CSS `cubic-bezier` / `steps()`，不依赖外部动画库。

## 1. mood→风格路由表

| 情绪 / 受众 | 推荐预设 | 备选 |
|---|---|---|
| 数据驱动 · 分析 · 技术汇报 | blue-professional | cobalt-grid, code-editorial |
| 高级 · 企业 · 奢华品牌 | biennale-yellow | cartesian, editorial-forest |
| 粗粝 · 朋克 · 叛逆宣言 | broadside | creative-mode |
| 高燃 · 喧闹 · 产品发布 | bold-poster | coral |
| AI · ML · 未来科技 | cobalt-grid | blue-professional |
| 人文 · 温暖 · 个人叙事 | capsule | editorial-forest |
| 文化 · 趣味 · 消费大众 | blockframe | daisy-days |
| 黑暗 · 戏剧 · 紧张氛围 | coral | broadside |
| 机构 · 董事会 · 克制严肃 | signal | blue-professional |
| 学术 · 白皮书 · 安静单色场 | vellum | cartesian |
| 极简 · 全墨 · 留白慷慨 | monochrome | cartesian |
| 商务 · 杂志封面 · 高饱和自信 | emerald-editorial | editorial-forest |
| 时装 · 三色轮换 · 编辑感 | editorial-tri-tone | capsule |
| 深夜 · 奢华 · 单焦点 | pink-script | coral |
| 宣言 · 高压 · 二元反转 | studio | broadside |
| 像素 · 街机 · 复古游戏 | 8-bit-orbit | cobalt-grid |
| 复古 OS · 桌面隐喻 · 怀旧 | retro-windows | creative-mode |
| 高密度 · 网格 · 新粗野 | neo-grid-bold | blockframe |
| 粗野 · 路演 · 零装饰 | raw-grid | bold-poster |
| 行动 · 海报 · 大众动员 | peoples-platform | bold-poster |
| 自然 · 有机 · 安静克制 | grove | editorial-forest |
| 材质 · 中世纪 · 刻意静止 | mat | code-editorial |
| 档案 · 田野手册 · 色块轮换 | stencil-tablet | creative-mode |
| 手工 · 田野笔记 · 拼贴 | pin-and-paper | daisy-days |
| 工作坊 · 头脑风暴 · 便利贴 | scatterbrain | capsule |
| 油印 · 独立出版 · 拼贴 | retro-zine | bold-poster |
| 日式 · 复古目录 · 多色轮换 | sakura-chroma | daisy-days |
| 独立 · 暖调 · 顽皮 | playful | capsule |
| 社群 · 餐饮 · 账本诚实 | long-table | editorial-forest |
| 文学 · 柔和 · 杂志感 | soft-editorial | biennale-yellow |
| 冷静 · 瓷白 · 学术期刊感 | porcelain-indigo | blue-professional |
| 怀旧 · 牛皮纸 · 人文手账 | kraft-journal | long-table |
| 瑞士 · 灰白底 · 皇家蓝单锚 | swiss-ultramarine | monochrome |
| 瑞士 · 灰白底 · 柠檬黄活力 | swiss-lemon | neo-grid-bold |
| 瑞士 · 灰白底 · 荧光绿未来 | swiss-lime | studio |
| 瑞士 · 灰白底 · 安全橙工业警示 | swiss-safety | broadside |

路由表只给正向推荐；锁定预设后必须过 §2「预设标注四字段 · 负向场合」的排除匹配，命中排除项回表重选。

## 2. 四十一套设计系统预设

> 每套格式：look（一句话视觉）/ pick-when（一句话适用）/ 核心 token（覆盖变量 hex）/ 字体·形状 / 签名动效（entry·exit·ambient 缓动 + 时长）/ 页型配方要点（cover·stat-grid·quote·timeline·closing 各 1 行特有做法）。

> 预设未显式给出 `on-primary` 时按 `design-system-standards.md` §1 配对规则推导：取白 / 近黑中与 `--primary-color` 按 WCAG 公式实算 ≥ 4.5:1 的那个；主色填充块上的文字一律用推导结果，不硬编码 `#fff`/`#000`。

> 预设标注四字段——选型与交付审查时对选定预设补齐以下四个判断（判断方法，不改写四十一套条目原文）：
>
> - **温度（暖/冷）**：把条目 `--primary-color` 与 `--surface-color` 的 hex 转 HSL 按色相判——H ∈ [345°, 90°]（红/品红/橙/黄）或底色偏奶油/牛皮/羊皮纸 = 暖；H ∈ [180°, 300°]（青/蓝/紫）或底色偏灰蓝/瓷白 = 冷；[90°, 180°]（黄绿/绿）与 [300°, 345°]（洋红/粉紫）为过渡扇区，按底色偏暖灰还是偏冷灰判。用途：§1 路由表锁定预设后做二次校验——受众情绪温度与预设温度冲突（如"人文·温暖"锁了冷瓷套）时回路由表重选，或向用户摆出冲突理由；禁止同页混用暖/冷两套预设元素。
> - **还原度（屏幕↔打印差异）**：本库默认屏幕演示；用户要 PDF 导出/印刷时按三档标注预期差异并给降级方案——高：平面实底 + 发丝线 + 纯排版（monochrome、cartesian、porcelain-indigo、swiss 四套），屏幕 ≈ 打印，直接导；中：大面积高饱和 accent 或双色实底（emerald-editorial、bold-poster、peoples-platform），印刷整体压暗约一档，accent 先加深一档再导；低：暗底 + 霓虹/辉光/grain/扫描线（8-bit-orbit、pink-script、studio、retro-windows），印刷必失真——出降级版（底色改纸白、霓虹改同色相深墨、去辉光与扫描线），并在交付说明标注哪些页做了降级，不假装是原版。
> - **字体平替（无网络字体时的系统栈回退）**：本库条目"字体·形状"行已是零外链系统栈，平替字段记录两件事——① 跨平台落点与再回退：展示 serif `"Songti SC"`(macOS) → `"SimSun"`(Windows) → Georgia → serif；正文 sans `"PingFang SC"`(macOS) → `"Microsoft YaHei"`(Windows) → system-ui → sans-serif；数据 mono `ui-monospace` → `"SF Mono"`(macOS) → Consolas(Windows) → monospace；手写面 `"Kaiti SC"`(macOS) → `"KaiTi"/"STKaiti"`(Windows) → cursive；Linux 无头导出环境统一再回退 `"Noto Serif CJK SC"` / `"Noto Sans CJK SC"` / `"DejaVu Sans Mono"`。② 签名特征降级：预设签名依赖字体特征而落点字体不具备时用 CSS 逼近——condensed 缺 `"Arial Narrow"` 用字距 −0.02em + 收窄容器宽模拟窄体感；200 超轻档缺失回退 300 并在交付说明标注；像素感不用普通字体硬凑，保留方块装饰与 `steps()` 阶梯动画的块状视觉语言。
> - **负向场合（avoid-when）**：pick-when 是正向信号，锁定前再做一次负向匹配，排除"气质对但场合错"的预设。高危组合表：严肃金融披露/医疗患教/监管汇报排除顽皮与复古游戏系（8-bit-orbit、playful、scatterbrain、daisy-days、retro-windows）；传统奢侈品/高端品牌排除粗粝粗野系（broadside、raw-grid、neo-grid-bold、retro-zine）；庄重场合/危机沟通排除高饱和庆典系（bold-poster、peoples-platform、sakura-chroma）；高密度数据白皮书排除装饰手写系（pin-and-paper、kraft-journal、stencil-tablet）。锁定后自问一句"这个 deck 的场合在该套的排除清单里吗"，命中即回 §1 路由表重选；用户明确要求冲突组合时落档用户原话后照办。

### 2.1 biennale-yellow

- **look**: 文学编辑目录风——暖羊皮纸底、单一深靛蓝墨、太阳黄作径向晕染 / 色板 / 瓷砖底印，严格矩形 0 圆角，1px 发丝线作唯一边框，无阴影。
- **pick-when**: 自信 / 氛围感 / 克制；想要博物馆目录式优雅与编辑权威的产品。
- **核心 token**: `--surface-color:#E9E5DB` `--surface-muted:#DCD6C4` `--text-primary:#1B2566` `--text-secondary:#1B2566`（降 opacity 至 60%） `--primary-color:#F1EE2E` `--secondary-color:#E26B4A` `--tertiary-color:#F0DA7C` `--outline-color:#1B2566`（20% 软发丝）
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（400，紧行高负字距）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px；密度低（55-60% 留白，账本页唯一密集）；阴影无。
- **签名动效**: entry `cubic-bezier(0.445,0.05,0.55,0.95)` 1.2s / exit `cubic-bezier(0.55,0.085,0.68,0.53)` 1.5s / ambient `cubic-bezier(0.445,0.05,0.55,0.95)` 3.0s 循环。
- **页型配方要点**:
  - cover: 羊皮纸底 + 太阳黄径向晕染（42-70% 画幅，偏心）+ 深靛蓝 2 行斜体展示标题左对齐 + 底部 4 列元数据条。
  - stat-grid: 账本式 4 列表格（mono 日期 · serif 标题 · sans 场馆 · mono 时长），1px 发丝线分隔，全套唯一密集页。
  - quote: 居中斜体 serif 大字 + 超大 serif 引号 + 居中太阳黄晕染，留白 60%。
  - timeline: 编号编辑列表（serif 序号 + serif 标题 + sans 正文），发丝软线分隔。
  - closing: 全幅太阳黄色板 + 靛蓝标题压顶（ink-on-yellow 签名做法，色板直接接纸面无边框）。

### 2.2 blockframe

- **look**: 极繁新粗野主义——4px 黑边框、8px 硬偏移阴影、五种糖果粉彩、大写特粗展示体、方角、倾斜装饰。
- **pick-when**: 大胆 / 冲击 /  playful-loud；想要自信且图形化的产品。
- **核心 token**: `--surface-color:#FFFDF5` `--surface-muted:#FFDC8B` `--text-primary:#000000` `--text-secondary:#000000`（60%） `--primary-color:#FE90E8` `--secondary-color:#C0F7FE` `--tertiary-color:#99E885` `--outline-color:#000000`（4px 边框）；额外 accent `#F7CB46`。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（900，uppercase）/ 正文同栈（700）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px；密度中；阴影 8px 硬偏移无模糊。
- **签名动效**: entry `cubic-bezier(0.34,1.56,0.64,1)` 0.5s / exit 用 `@keyframes` 多段回弹近似（或降级 `cubic-bezier(0.34,1.56,0.64,1)`）0.8s / ambient `cubic-bezier(0.445,0.05,0.55,0.95)` 1.5s。
- **页型配方要点**:
  - cover: 4px 黑边大标题块 + 8px 硬偏移阴影 + 倾斜装饰元素 + 糖果色底。
  - stat-grid: 糖果色块网格，每块 4px 黑边 + 硬阴影，数字特粗大写。
  - quote: 倾斜装饰 + 大写粗体引文 + 黑边框。
  - timeline: 糖果色节点 + 4px 黑边连线 + 硬阴影卡片。
  - closing: 黑底板（Closing Plate）+ 糖果色文字 + 倾斜装饰。

### 2.3 blue-professional

- **look**: 咨询级克制——暖奶油画布、单一饱和钴蓝 #1e2bfa accent、软色调卡片（4% 填充 / 20% 边框 / 10-14px 圆角）无阴影、pill chrome（100px）、3 阶灰字梯、钴蓝进度条。
- **pick-when**: 沉稳 / 高管可读 / 高级信号；想要投资研究级严谨与精致克制的产品。
- **核心 token**: `--surface-color:#fdfae7` `--surface-muted:#fdfae7`（卡片 4% 钴蓝填充） `--text-primary:#111111` `--text-secondary:#6b6b6b` `--primary-color:#1e2bfa` `--secondary-color:#059669` `--tertiary-color:#dc2626` `--outline-color:#1e2bfa`（20% 边框）；辅助灰 `#9a9a9a`。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（700）/ 正文同栈（400-500）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 pill 100px / 卡片 10-14px；密度中；阴影无。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 暖奶油底 + 单一钴蓝 accent + pill chrome（100px 圆角标签）。
  - stat-grid: Dashboard 软色调卡片（4% 填充 / 20% 边框 / 10-14px 圆角）+ 无阴影 + 钴蓝进度条。
  - quote: Pull Quote 钴蓝强调 + 3 阶灰字梯（#111111 / #6b6b6b / #9a9a9a）。
  - timeline: Bar Ranking 钴蓝条形排名 + 灰字标签。
  - closing: Closing/CTA pill 按钮（100px）+ 钴蓝填充。

### 2.4 bold-poster

- **look**: 民粹编辑海报——展示体倾斜 −6°..+2°、serif 正文、四色限定（白 / 棕黑墨 / 番茄红 / 米白）、双层边框网格（3px+1.5px）、红色左边栏卡片、红色破折号项目符、红色展示体堆叠 text-shadow、方角。
- **pick-when**: 有力 / 印刷感 / 克制；想要编辑权威与复古厚重的产品。
- **核心 token**: `--surface-color:#FFFFFF` `--surface-muted:#F5F2EF` `--text-primary:#1C1410` `--text-secondary:#1C1410`（60%） `--primary-color:#D8000F` `--secondary-color:#1C1410` `--tertiary-color:#F5F2EF` `--outline-color:#1C1410`（双层 3px+1.5px）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（倾斜 −6°..+2°）/ 正文 `"Songti SC","SimSun",Georgia,serif` / 数据 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`；圆角 0px；密度中；阴影红色展示体堆叠 text-shadow。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.3s / exit `cubic-bezier(0.34,1.56,0.64,1)` 0.4s / ambient `cubic-bezier(0.165,0.84,0.44,1)` 0.8s。
- **页型配方要点**:
  - cover: Hero Stack 倾斜展示体（−6°..+2°）+ 双层边框（3px+1.5px）。
  - stat-grid: Financial Grid 双层边框网格 + 红色左边栏卡片。
  - quote: Pull Quote 红色破折号项目符 + serif 正文。
  - timeline: Editorial Cards 红色左边栏 + 倾斜标题。
  - closing: Closing Statement 红色展示体 + 堆叠 text-shadow。

### 2.5 broadside

- **look**: 抗议海报系统——双色调平面（墨黑 / 火橙）、巨型小写特粗展示体作图形原语、mono chrome（uppercase，0.14em）、火橙唯一 accent、1px 发丝线、锐角、无阴影。
- **pick-when**: 大胆 / 排版驱动 / 宣言式；想要存在感与权威的产品。
- **核心 token**: `--surface-color:#F0ECE5` `--surface-muted:#1A1A18` `--text-primary:#111111` `--text-secondary:#888880` `--primary-color:#E85D26` `--secondary-color:#111111` `--tertiary-color:#282826` `--outline-color:#282826`（1px 发丝）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（900，lowercase 作图形）/ 正文同栈 / 数据 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase，0.14em）；圆角 0px；密度中；阴影无。
- **签名动效**: entry `cubic-bezier(0.36,1.7,0.66,1)` 0.3s / exit `steps(8)` 0.5s / ambient 用 `@keyframes` 多段回弹近似 1.0s。
- **页型配方要点**:
  - cover: 双色调平面（墨黑 / 火橙）+ 巨型小写特粗展示体作图形原语。
  - stat-grid: 1px 发丝线网格 + 火橙唯一 accent + 无阴影。
  - quote: 巨型小写展示体 + 火橙强调。
  - timeline: Fadelist 渐隐列表 + 1px 发丝线。
  - closing: Statement 火橙底板 + 墨黑文字。

### 2.6 capsule

- **look**:  playful 编辑风——每个容器都是 pill（2px 墨描边）、奶油画布、九种糖果 accent、serif 展示体 + sans 正文、软偏移阴影、浮动 pill 壁纸。
- **pick-when**: 友好 / 柔和 / 编辑感；想要温暖与亲和的产品。
- **核心 token**: `--surface-color:#F5F5F0` `--surface-muted:#FFFFFF` `--text-primary:#1A1A1A` `--text-secondary:#1A1A1A`（60%） `--primary-color:#E85D4E` `--secondary-color:#C4D94E` `--tertiary-color:#C5B5E0` `--outline-color:#1E1E1E`（2px 描边）；额外 accent `#8BB4F7` `#A06CE8` `#F2D160` `#F5B895` `#A8E6CF`。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif` / 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 pill 9999px / 卡片 2rem；密度中；阴影软偏移。
- **签名动效**: entry `cubic-bezier(0.445,0.05,0.55,0.95)` 1.0s / exit `cubic-bezier(0.455,0.03,0.515,0.955)` 1.5s / ambient `cubic-bezier(0.445,0.05,0.55,0.95)` 3.0s。
- **页型配方要点**:
  - cover: 奶油底 + 浮动 pill 壁纸 + 2px 墨描边 pill 标题。
  - stat-grid: Pillar Cards 胶囊卡片 + 九糖果 accent + 软偏移阴影。
  - quote: Pull Quote serif 展示体 + 胶囊框。
  - timeline: Orbit 轨道式胶囊节点。
  - closing: Closing Plate 胶囊板 + 糖果色。

### 2.7 cartesian

- **look**: 博物馆目录编辑风——1px 灰褐发丝网格、五暖石色板、serif 展示体 + sans 正文、锐角、圆规绘制几何环、零阴影零填充。
- **pick-when**: 稀疏 / 文学 / 克制；想要安静权威与编辑严谨的产品。
- **核心 token**: `--surface-color:#EDE8E0` `--surface-muted:#E2DBD1` `--text-primary:#1A1A1A` `--text-secondary:#5A5A5A` `--primary-color:#8A8178` `--secondary-color:#B8B0A4` `--tertiary-color:#5A5A5A` `--outline-color:#B8B0A4`（1px 发丝）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（400）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px；密度低；阴影无、填充无。
- **签名动效**: entry `cubic-bezier(0.445,0.05,0.55,0.95)` 1.2s / exit `cubic-bezier(0.55,0.085,0.68,0.53)` 1.5s / ambient `cubic-bezier(0.445,0.05,0.55,0.95)` 3.0s。
- **页型配方要点**:
  - cover: 暖石色底 + 1px 灰褐发丝网格 + 圆规几何环。
  - stat-grid: 发丝网格 + 零填充零阴影。
  - quote: Pull Quote serif 展示体 + 发丝框。
  - timeline: 发丝线 + 几何环节点。
  - closing: Closing Plate 暖石色 + 发丝网格。

### 2.8 cobalt-grid

- **look**: 现代主义双色 risograph——奶油纸、电光钴蓝墨、永久方格纸网格（10% 钴蓝）、顶底钴蓝发丝线、serif 展示体 + sans 正文 + mono 数据、0° 角、像素故障列 + QR 块补丁。
- **pick-when**: 克制 / 系统感 / 编辑风；想要清晰与沉稳权威的产品。
- **核心 token**: `--surface-color:#F0EBDE` `--surface-muted:#E6E0CE` `--text-primary:#1F2BE0` `--text-secondary:#4650D6`（奶油底实测 5.2:1，达 AA） `--primary-color:#1F2BE0` `--secondary-color:#4650D6` `--tertiary-color:rgba(31,43,224,0.10)` `--outline-color:#1F2BE0`（10% 网格）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（400）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px；密度中；阴影无。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 奶油纸 + 钴蓝墨 + 永久方格纸网格（10% 钴蓝）+ 顶底钴蓝发丝线。
  - stat-grid: Data Frame 方格纸网格 + 像素故障列 + QR 块补丁。
  - quote: Manifesto serif 展示体 + 钴蓝。
  - timeline: Index Ledger 账本式 + 方格网格。
  - closing: Colophon 方格纸 + 钴蓝发丝线。

### 2.9 code-editorial

- **look**: 暖编辑品牌书——暖奶油纸（非纯白）、陶土珊瑚红 #CC785C 作稀疏电压、发丝墨抬升（无重阴影）、serif 展示体 + sans 正文 + mono 索引 / 代码于暖 navy 代码面、sentence-case 展示体、✱ 珊瑚红尖峰。
- **pick-when**: 深思 / 文学 / 面向开发者；想要编辑 calm 与一流代码面的代码变更、发布或文档。
- **核心 token**: `--surface-color:#FAF9F5` `--surface-muted:#EFE9DE` `--text-primary:#141413` `--text-secondary:#141413`（60%） `--primary-color:#CC785C` `--secondary-color:#181715` `--tertiary-color:#ECE3D4` `--outline-color:#141413`（20%）；代码面 navy `#181715` / `#1F1E1B` / `#252320`。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（sentence-case）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 6/8/12px；密度中；阴影发丝墨抬升无重阴影。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 暖奶油纸（非纯白）+ serif sentence-case 展示体 + 珊瑚红 ✱ 尖峰。
  - stat-grid: Number/Impact 发丝墨抬升 + 珊瑚红稀疏强调。
  - quote: Pull-quote serif 展示体 + 珊瑚红。
  - timeline: Code Surface 暖 navy 代码面 + mono。
  - closing: Closing/CTA 珊瑚红 + 发丝抬升。

### 2.10 coral

- **look**: 大胆编辑杂志——三色实底（珊瑚火 / 墨黑 / 暖奶油）硬边相接、珊瑚上 45° 斜纹、condensed 展示体 + tracked caps 正文、零阴影零圆角（圆形 50%）、超大壁纸数字与巨型标记。
- **pick-when**: 大胆 / 结构主义 / 编辑风；想要图形自信与硬边自信的产品。
- **核心 token**: `--surface-color:#F5F0E8` `--surface-muted:#E8E0D4` `--text-primary:#1A1A1A` `--text-secondary:#6B6B6B` `--primary-color:#E85D5D` `--secondary-color:#D44A4A` `--tertiary-color:#B0B0B0` `--outline-color:#1A1A1A`。
- **字体·形状**: 展示体 `"Arial Narrow","PingFang SC",system-ui,sans-serif`（condensed，tracked caps）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px（圆形 50%）；密度中；阴影无。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.3s / exit `cubic-bezier(0.34,1.56,0.64,1)` 0.4s / ambient `cubic-bezier(0.165,0.84,0.44,1)` 0.8s。
- **页型配方要点**:
  - cover: Region-Split 三色实底（珊瑚火 / 墨黑 / 暖奶油）硬边相接 + 45° 斜纹。
  - stat-grid: Feature Stat 超大壁纸数字 + 珊瑚红斜纹。
  - quote: Quote Layout 巨型标记 + tracked caps。
  - timeline: 硬边色块 + 圆形节点（50%）。
  - closing: Closing Plate 珊瑚红底板 + 斜纹。

### 2.11 creative-mode

- **look**: 新粗野编辑风——奶油画布、4px 墨边框、硬偏移阴影（无模糊）、四 accent 限量 2-3 个、特粗大写展示体（0.92 行高）、mono 分类、sans 正文、方角除唯一 pill chip。
- **pick-when**: 稀疏 / 图形 / punchy-restrained；想要编辑存在感与几何自信的产品。
- **核心 token**: `--surface-color:#EFE9D9` `--surface-muted:#E4DCC4` `--text-primary:#0F0F0F` `--text-secondary:#2A2A2A` `--primary-color:#1F8A4C` `--secondary-color:#F06CA8` `--tertiary-color:#E85A1F` `--outline-color:#0F0F0F`（4px 边框）；额外 accent `#F5C518`。
- **字体·形状**: 展示体 `"Arial Narrow","PingFang SC",system-ui,sans-serif`（900，uppercase，0.92 行高）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px（唯一 pill chip 9999px）；密度中；阴影硬偏移无模糊。
- **签名动效**: entry `cubic-bezier(0.36,1.7,0.66,1)` 0.3s / exit `steps(8)` 0.5s / ambient 用 `@keyframes` 多段回弹近似 1.0s。
- **页型配方要点**:
  - cover: Wordmark 奶油底 + 4px 墨边 + 特粗大写展示体（0.92 行高）。
  - stat-grid: 硬偏移阴影（无模糊）+ 四 accent 限量 2-3 个。
  - quote: Big Claim 特粗大写 + 墨边。
  - timeline: Comparison Ledger 账本式 + mono 分类。
  - closing: Closing Plate 唯一 pill chip + 硬阴影。

### 2.12 daisy-days

- **look**: 欢快绘本风——3px 炭描边、6/4px 硬偏移阴影（无模糊）、九种阳光花园粉彩、圆体展示体 + 圆体正文、慷慨圆角（20-50px）、手绘 SVG 装饰层（雏菊 / 星星 / 太阳 / 云 / 彩虹）。
- **pick-when**:  playful / 孩子气 / 贴纸表 kawaii；想要温暖与奇趣的产品。
- **核心 token**: `--surface-color:#F5F0E6` `--surface-muted:#FFFFFF` `--text-primary:#2D2D2D` `--text-secondary:#6B6B6B` `--primary-color:#F8635F` `--secondary-color:#7ECDC0` `--tertiary-color:#F7C8D4` `--outline-color:#2D2D2D`（3px 炭描边）；额外粉彩 `#FDE68A` `#A8E6CF` `#D4A5E8` `#FFCBA4` `#A8D8F0`。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（700，圆角感）/ 正文同栈（500）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 20-50px；密度中；阴影 6/4px 硬偏移无模糊。
- **签名动效**: entry `cubic-bezier(0.34,1.56,0.64,1)` 0.5s / exit 用 `@keyframes` 多段回弹近似（或降级 `cubic-bezier(0.34,1.56,0.64,1)`）0.8s / ambient `cubic-bezier(0.445,0.05,0.55,0.95)` 1.5s。
- **页型配方要点**:
  - cover: 奶油底 + 3px 炭描边 + 手绘 SVG 装饰（雏菊 / 星星 / 太阳）。
  - stat-grid: Info Cards 九园艺粉彩 + 6/4px 硬阴影 + 20-50px 圆角。
  - quote: 圆体展示体 + 炭描边 + 手绘装饰。
  - timeline: Process Steps 粉彩节点 + 硬阴影。
  - closing: Framed Section 炭框 + 手绘装饰。

### 2.13 editorial-forest

- **look**: serif 主导文学编辑风——绿 / 粉 / 奶油编辑三色、serif 展示体（weight 500 opsz）+ mono uppercase chrome（weight 500）、平面纸感深度（无阴影）、2px 发丝线、6/8px 卡片圆角、monogram 圆章。
- **pick-when**: 宽敞 / 克制 / 编辑风；想要安静自信与文学语调的产品。
- **核心 token**: `--surface-color:#efe7d4` `--surface-muted:#e6dcc4` `--text-primary:#1a1a17` `--text-secondary:#1a1a17`（60%） `--primary-color:#2e4a2a` `--secondary-color:#e89cb1` `--tertiary-color:#3a5a36` `--outline-color:#1a1a17`（20%，2px 发丝）；深色变体 `#243a21` `#d27e96`。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（500）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase，500）；圆角 6/8px；密度低；阴影无（平面纸感）。
- **签名动效**: entry `cubic-bezier(0.445,0.05,0.55,0.95)` 1.2s / exit `cubic-bezier(0.55,0.085,0.68,0.53)` 1.5s / ambient `cubic-bezier(0.445,0.05,0.55,0.95)` 3.0s。
- **页型配方要点**:
  - cover: 绿 / 粉 / 奶油三色 + serif 展示体（w500）+ monogram 圆章。
  - stat-grid: KPI Stat 2px 发丝线 + 6/8px 圆角 + 平面纸感无阴影。
  - quote: Statement serif 展示体 + 发丝线。
  - timeline: Step Framework 发丝线 + 圆角卡片。
  - closing: Chart 平面纸感 + 三色。

### 2.14 8-bit-orbit

- **look**: 像素街机夜空风——深海军蓝星域底、40px 低透明网格、青/粉/黄三霓虹 accent、4/8px 堆叠硬偏移零模糊阴影、CRT 扫描线 + grain + 暗角三件套常驻、全方角。
- **pick-when**: 顽皮 / 复古游戏 / 科技狂欢；想要街机存在感与像素怀旧的产品。
- **核心 token**: `--surface-color:#0F1B3D` `--surface-muted:#0A0E27` `--text-primary:#FFFFFF` `--text-secondary:#E2D5F2` `--primary-color:#5EDCF4` `--secondary-color:#F0A6CA` `--tertiary-color:#F4D03F` `--outline-color:#5EDCF4`（40px 网格，低透明度）；on-primary `#0F1B3D`（显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（900，像素几何感）/ 正文同栈（400）/ 数据与标签 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase）；圆角 0px（导航点亦方形）；密度中；阴影 4/8px 堆叠硬偏移零模糊（三步 navy L 形 / 六步霓虹 cascade / 双层 text-shadow）。
- **签名动效**: entry `cubic-bezier(0.22,1,0.36,1)` 0.8s translateY / exit 同缓动 0.8s / ambient 星域闪烁 3s + 像素粒子 8s 循环。
- **页型配方要点**:
  - cover: 星域壁纸 + 像素堆叠阴影大标题 + CRT 三件套常驻（扫描线 / grain / 暗角，z 49-51）。
  - stat-grid: 青色玻璃 stat-block + L 形角括号 + 霓虹 cascade 阴影数字。
  - quote: 黄色短线 + navy 偏移引文卡。
  - timeline: 方形像素节点 + 虚线轨道连线。
  - closing: 六步堆叠阴影 pixel-button + 星域收底。

### 2.15 editorial-tri-tone

- **look**: 时装三色编辑风——全系统仅 3 个 hex（粉 / 奶油黄 / 勃艮第），三色逐页轮换作表面、serif 斜体强调面、pill + 大圆角卡片、零阴影。
- **pick-when**: 时髦 / 编辑感 / 三色轮换；想要时装杂志封面感与色块自信的产品。
- **核心 token**: `--surface-color:#F2D86A` `--surface-muted:#F2B6C6` `--text-primary:#7A1F35` `--text-secondary:#7A1F35`（60%） `--primary-color:#F2B6C6` `--secondary-color:#F2D86A` `--tertiary-color:#7A1F35` `--outline-color:#7A1F35`（深面上 25-30% opacity 发丝）；on-primary `#7A1F35`（显式）。三色皆可作页面底色轮换（粉 / 黄 / 勃艮第）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（700-800，负字距）/ 强调面 `"Songti SC","SimSun",Georgia,serif`（斜体：章节数 / 引文 / 年份 / 签名；CJK 无斜体→勃艮第色替代）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase 标签）；圆角 pill 999px / 卡片 28px / 图表卡 32px / 标题 0；密度中；阴影无。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 三色大色块硬边分割 + sans 特粗标题内嵌 serif 斜体 `<em>` 切换。
  - stat-grid: 四系列单画布 SVG 图表（三色轮换系列）+ 28px 圆角图表卡。
  - quote: serif 斜体大引文 + 勃艮第短线。
  - timeline: pill 节点 + 三色轮换阶段色块。
  - closing: footer 8px 圆点页进度（30%/100% 两态）+ 三色收底带。

### 2.16 emerald-editorial

- **look**: 杂志封面商务风——翡翠绿大色底、燕麦纸变体面、深海军 Didone 风特粗 serif 标题、全矩形零圆角、零阴影零渐变（深度 = 色块反转 + 4px 墨规线）。
- **pick-when**: 商务 / 杂志感 / 高饱和自信；想要封面级视觉冲击与编辑权威的产品。
- **核心 token**: `--surface-color:#3CD896`（深档 `#2DC684`/`#25B377`） `--surface-muted:#F1E9D6` `--text-primary:#0F1A5C` `--text-secondary:#0F1A5C`（60%） `--primary-color:#0F1A5C` `--secondary-color:#F1E9D6` `--tertiary-color:#25B377` `--outline-color:#0F1A5C`；on-primary `#3CD896`（inverse-tile 墨底翡翠字，显式）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（900，Didone 风特粗）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（500-800，uppercase）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px 全矩形；密度中偏满居中；阴影无渐变无（深度 = 色块反转 + 4px 墨规线）。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 翡翠绿全幅底 + 深海军特粗 serif 刊头 + double-rule ornament（双 4px 规线夹居中 serif 词）。
  - stat-grid: 460px jumbo 数字全幅墨底 panel（反转）。
  - quote: 燕麦纸面 + 海军 serif 引文 + 4px 墨规线上下夹。
  - timeline: agenda-row 三列 4px 顶边条。
  - closing: 色块反转收底（墨底翡翠字）+ double-rule ornament。

### 2.17 grove

- **look**: 自然有机安静风——深林绿底、陶土珊瑚唯一 accent、羊皮纸浅色变体面、serif 400 永不加粗、1px 发丝线 + 三级文字透明度、18vw 水印数字、零阴影零渐变。
- **pick-when**: 自然 / 有机 / 安静克制；想要植物园目录式沉静与材质诚实的产品。
- **核心 token**: `--surface-color:#192B1B` `--surface-muted:#1E3221` `--text-primary:#D4CFBF` `--text-secondary:#D4CFBF`（58%/30% 三级透明度） `--primary-color:#C8524A` `--secondary-color:#E8E4D6`（羊皮纸浅色变体面） `--tertiary-color:#1E3221` `--outline-color:#D4CFBF`（12% 发丝）；on-primary 按 §2 推导规则（珊瑚仅作文字 / 规线，不作填充）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（400，永不加粗）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（300）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（300，uppercase，0.12-0.2em）；圆角 0px；密度低；阴影无渐变无（深度 = 1px 发丝线 + 三级文字透明度 + 水印数字）。
- **签名动效**: entry `cubic-bezier(0.16,1,0.3,1)` 错峰 / exit（翻页）`cubic-bezier(0.77,0,0.175,1)` 0.9s / ambient 无。
- **页型配方要点**:
  - cover: 深林绿底 + 36px 珊瑚短线 + serif 400 标题 + 18vw 6% serif 水印数字。
  - stat-grid: grove-stat 无底纹发丝统计卡（数字珊瑚或羊皮纸色）。
  - quote: 珊瑚 em-dash 项目符引文 + 发丝线上下夹。
  - timeline: 发丝竖轴 + 珊瑚小点节点 + mono uppercase 阶段标签。
  - closing: 羊皮纸浅色变体面反转 + 36px 珊瑚短线收底。

### 2.18 long-table

- **look**: 单墨账本风——暖纸底、赤陶红棕唯一墨色以 78%/50%/32% 透明度作层次、serif 斜体正文、480px 级斜体巨数字、点纸纹常驻、零阴影。
- **pick-when**: 社群 / 餐饮 / 账本式诚实；想要手记感与单墨克制的产品。
- **核心 token**: `--surface-color:#FAF1E2` `--surface-muted:#F2E5CF` `--text-primary:#B53D2A` `--text-secondary:#B53D2A`（78%/50%/32% 三级透明度） `--primary-color:#B53D2A` `--secondary-color:#8E2D1F` `--tertiary-color:#E8D7B6` `--outline-color:#B53D2A`（1.5px）；on-primary `#FAF1E2`（显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（700-800，uppercase）/ 正文 `"Songti SC","SimSun",Georgia,serif`（400-600，默认斜体；CJK 无斜体→颜色 / 字重替代）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 pill 999px / 圆形徽章 / 方角 rect-tag；密度中偏高；阴影无（4px 径向点纸纹 10% 常驻）。
- **签名动效**: entry 280ms 透明度淡入 / exit 280ms 淡出 / ambient 无。
- **页型配方要点**:
  - cover: 暖纸底 + 480px 级斜体 serif edition 巨数字 + sans uppercase 主标。
  - stat-grid: ledger-row 多栏账本行（1.5px 墨规线分栏）。
  - quote: serif 斜体大引文 + 圆形徽章落款。
  - timeline: ledger-row 变体时间线（日期栏 mono + 事件栏 serif）。
  - closing: 导航提示 + 斜体页码 + pill 收底标签。

### 2.19 mat

- **look**: 中世纪材质风——深苔绿底、暖橙内联强调、奶油 info-card 材质对比、右下木棕径向辉光常驻、全 0s 即时翻页（刻意无动画）、零阴影。
- **pick-when**: 材质 / 中世纪 / 安静温度；想要家居展厅式触感与刻意静止的产品。
- **核心 token**: `--surface-color:#232E26` `--surface-muted:#2E3D30` `--text-primary:#F0E8D2` `--text-secondary:#F0E8D2`（58%/30%） `--primary-color:#C07030` `--secondary-color:#EDE6D0`（奶油浅色变体） `--tertiary-color:#7A4E24`（辉光） `--outline-color:#F0E8D2`（12% 发丝）；on-primary 按 §2 推导规则（暖橙仅作内联强调，不作大面积填充）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（800，混合大小写，禁全大写）/ 正文同栈（400）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（400，uppercase）；圆角 0px；密度中偏疏；阴影无（深度 = 右下木棕径向辉光 55%×70% 常驻 + 发丝线 + 奶油 info-card 材质对比）。
- **签名动效**: entry 0s / exit 0s（全即时翻页，刻意无动画）/ ambient 无（辉光为静态径向渐变，非动画）。
- **页型配方要点**:
  - cover: 深苔绿底 + sans 800 混合大小写标题 + 暖橙 em-dash 项目符前言 + 右下木棕辉光。
  - stat-grid: stat-cell 竖分隔统计格（发丝竖线，数字奶油色）。
  - quote: info-card 奶油嵌入块（浅底深字材质反转）+ 暖橙强调词。
  - timeline: 发丝横轴 + 方角节点 + mono uppercase 年份。
  - closing: 奶油 info-card 收底面 + 暖橙短线。

### 2.20 monochrome

- **look**: 全墨极简风——奶油底、墨黑字、零彩色（primary = accent = 墨黑）、sans 200 超轻展示 + serif 斜体仅引文、8vw 页边距全库最慷慨、零阴影零渐变零纹理。
- **pick-when**: 极简 / 全墨 / 留白慷慨；想要瑞士排印式安静与字体自信的产品。
- **核心 token**: `--surface-color:#FAFADF`（近同三奶油 `#F2F2D2`/`#F0F0D4`/`#F5F0E4`） `--surface-muted:#F2F2D2` `--text-primary:#1A1A16` `--text-secondary:#5E5E54` `--primary-color:#1A1A16` `--secondary-color:#5E5E54` `--tertiary-color:#8A8A80` `--outline-color:#1A1A16`（1px）；on-primary `#FAFADF`（显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（200 超轻；CJK 用 Ultralight 字重档）/ 正文同栈（300）/ 引文面 `"Songti SC","SimSun",Georgia,serif`（斜体，仅引文与 insight 卡）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase）；圆角 0px（唯一例外 insight 卡 16px）；密度低（8vw 页边距）；阴影无渐变无纹理无。
- **签名动效**: entry 错峰 8 档延迟 0-0.96s / exit（翻页）0.9s / ambient 无。
- **页型配方要点**:
  - cover: 奶油底 + sans 200 超轻大标题 + 36px 短线标点。
  - stat-grid: 墨黑数字 + 发丝线网格 + 三级灰字梯（#1A1A16/#5E5E54/#8A8A80）。
  - quote: serif 斜体引文 + 16px 圆角 insight 卡（全库唯一圆角）。
  - timeline: 穿环黑点时间线（发丝线穿环形节点中心）。
  - closing: 金字塔 color-mix 墨阶收底（同相墨黑逐级提亮）。

### 2.21 neo-grid-bold

- **look**: 新粗野网格风——浅灰底、霓虹柠檬黄唯一 accent、12×8 网格填满（留白 = 坏）、`<mark>` 黄块标题强调、240-320px 巨型数字、零阴影（深度 = 色块邻接）。
- **pick-when**: 高密度 / 网格 / 新粗野；想要信息极大化与图形张力的产品。
- **核心 token**: `--surface-color:#ECECE8` `--surface-muted:#F5F4EF` `--text-primary:#0A0A0A` `--text-secondary:#8A8A85` `--primary-color:#E6FF3D` `--secondary-color:#0A0A0A` `--tertiary-color:#8A8A85` `--outline-color:#0A0A0A`（表格 1.5px / 图表轴 2px）；on-primary `#0A0A0A`（柠檬卡上墨字，显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（700，uppercase，负字距）/ 正文同栈（400-500）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase，0.08-0.12em）；圆角 0px 全元素；密度高（12×8 网格填满）；阴影无（深度 = 色块邻接）。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 网格底 + `<mark>` 黄块强调标题 + 2×2 blockmark 块戳 + 左下常驻页码 `01 / 12`。
  - stat-grid: 240-320px 巨型数字占格 + 1.5px 墨表格线。
  - quote: 黄块 mark 引文 + sans 700 uppercase 落款。
  - timeline: 网格行时间线 + 三态对比 pill（墨 / 柠檬 / 描边）。
  - closing: 柠檬黄全幅底 + 墨黑收底声明 + corner-mark 块戳。

### 2.22 peoples-platform

- **look**: 行动主义海报风——米白底、电光钴蓝 / 琥珀橙双 accent、热红仅作阴影色不作填充、slab 特粗 uppercase + 手写体小注旋转 2-5°、6px 重边、红色双层堆叠 text-shadow、grain 叠印。
- **pick-when**: 行动 / 海报 / 大众动员；想要公共事业海报式力量与手工丝印感的产品。
- **核心 token**: `--surface-color:#F5F2EA` `--surface-muted:#F4E9D6` `--text-primary:#0E0E14` `--text-secondary:#0E0E14`（60%） `--primary-color:#2C2CDC`（深 `#1B1BB0`） `--secondary-color:#F2A03A`（深 `#E89321`） `--tertiary-color:#E83A2A`（热红仅作阴影色不作填充，深 `#B7281C`） `--outline-color:#0E0E14`（6px 重边）；on-primary `#F4E9D6`（蓝底奶油字，显式）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（900，slab 风特粗 uppercase）/ 手写面 `"Kaiti SC","Bradley Hand","Segoe Script",cursive`（小写，旋转 2-5°）/ 正文 `"Arial Narrow","PingFang SC",system-ui,sans-serif` / 数据 `ui-monospace,"SF Mono",Consolas,monospace`（24px，0.18-0.22em）；圆角结构 0（pill 999 / 圆 50% / 菱形 4px 转 45°）；密度中高；阴影红色双层堆叠 text-shadow（3px→12px/24px 按字号四档）+ 6-8px 红硬偏移 + grain 叠印。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: slab uppercase 海报大标题 + 红色堆叠 text-shadow + 橙色底部 ribbon。
  - stat-grid: 6px 重边卡片 + circular stamp 圆章角标 + diamond bullet。
  - quote: 手写体旋转注解引文 + slab uppercase 落款。
  - timeline: 菱形节点时间线 + 橙色 ribbon 阶段带。
  - closing: 钴蓝全幅底 + 6px 奶油 inset frame + 奶油字收底。

### 2.23 pin-and-paper

- **look**: 手工田野笔记风——便签黄底、深钴蓝墨、手绘别针 + 朱砂红印章、卡片交替旋转 0.6-1.5°、5-6px 硬墨蓝偏移零模糊、分形噪声 grain 0.35 multiply 必选。
- **pick-when**: 手工 / 田野笔记 / 拼贴；想要剪贴簿式真实感与文具质感的产品。
- **核心 token**: `--surface-color:#EFE56A`（层次 `#F5ECA0`/`#E8D85A`/`#FBE6A4`/kraft `#C9A66B`） `--surface-muted:#F8F1D6` `--text-primary:#1F3A8A` `--text-secondary:#2D4FB8`（线色 `#3457C4` / 深 `#0E1430`） `--primary-color:#1F3A8A` `--secondary-color:#C2342B` `--tertiary-color:#6B7A2E` `--outline-color:#1F3A8A`（1.5px）；on-primary `#EFE56A`（墨底纸黄字，显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（700）/ 手写面 `"Kaiti SC","Bradley Hand","Segoe Script",cursive`（600-700）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（500，档案标签）；圆角卡片 4px 微 / pill 999 / 印章 0；密度中高（每页 3-6 卡）；阴影 5-6px 硬墨蓝偏移零模糊 + 分形噪声 grain 0.35 multiply 必选。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 便签黄底 + safety-pin 手绘别针标题卡（旋转 −6..−12°）+ mono 档案标签。
  - stat-grid: number-script 手写步骤号卡片 + 硬墨蓝偏移 + 交替微旋转。
  - quote: 朱砂红印章（−4°）落款 + 手写面引文。
  - timeline: 手绘连线 + 别针节点 + kraft 纸阶段色带。
  - closing: 三声部字体收底（sans 标题 + 手写签名 + mono 日期）+ 印章封缄。

### 2.24 pink-script

- **look**: 深夜奢华风——径向暖黑底（左上打光）、热紫红唯一 accent、serif 400 展示 32-600px 无第二展示面、1px 纸白内框 inset 36px 常驻、film grain 8% screen、零 box-shadow。
- **pick-when**: 深夜 / 奢华 / 单焦点；想要舞台追光式聚焦与高级时装夜感的产品。
- **核心 token**: `--surface-color:#060507`（径向暖黑椭圆左上打光） `--surface-muted:#0F0D11` `--text-primary:#F5EDF1` `--text-secondary:#F5EDF1`（55%） `--primary-color:#ED3D8C`（浅 `#FF66A8` / 深 `#B81D67` / 线 32%） `--secondary-color:#FF66A8` `--tertiary-color:#B81D67` `--outline-color:#F5EDF1`（14% 纸白发丝）；on-primary `#060507`（pill-solid 粉底深墨字，显式）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（400，32-600px，唯一展示面）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（300）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase，0.08em+）；圆角 0px（"pill"亦矩形）；密度低中单焦点；阴影零 box-shadow（深度 = 径向表面 + film grain 8% screen + 粉色 halo text-shadow 80-120px blur）。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 暖黑径向底 + serif 大标题 em 切换粉色 + 1px 纸白内框（inset 36px 常驻）。
  - stat-grid: stat-row 无框统计（粉色数字 + 纸白标签）+ matrix-cell 32% 粉行线。
  - quote: serif 大引文 + 粉色 halo text-shadow。
  - timeline: 1px 纸白发丝轴 + 粉色方节点。
  - closing: qr-tile 唯一大浅色块（纸白底深墨字）+ serif 收底。

### 2.25 playful

- **look**: 独立暖调顽皮风——桃陶底、炭黑单色系统、双线描边偏移（3px 实线 + 6-8px ghost）、有机不对称圆角与鹅卵石形、±0.5-3° 微旋转、2px stroke SVG 涂鸦、零 web 阴影。
- **pick-when**: 独立 / 暖调 / 顽皮；想要手绘海报式温度与图形幽默的产品。
- **核心 token**: `--surface-color:#F0C8A0`（alt `#E8B88E` / 浅 `#F7DEC6`） `--surface-muted:#F7DEC6` `--text-primary:#1A1A1A` `--text-secondary:#1A1A1A`（60%） `--primary-color:#1A1A1A`（单色系统，墨即主色） `--secondary-color:#E8B88E` `--tertiary-color:#F7DEC6` `--outline-color:#1A1A1A`（3px）；on-primary `#F0C8A0`（filled-block 炭黑底桃字，显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（800，负字距）/ 正文同栈（400-500）；圆角 0 / 50% / 有机不对称（`40% 60% 70% 30% / 40% 50% 60% 50%`）/ 鹅卵石（`255px 15px 225px 15px / ...`）——禁中间档；密度中低单主导元素；阴影零 web 阴影（深度 = 双线描边偏移 3px 实线 + 6-8px ghost ::before、±0.5-3° 旋转、ghost-blob 0.08 壁纸、2px stroke SVG 涂鸦）。
- **签名动效**: entry 0.6s 透明度淡入 / exit 0.6s 淡出 / ambient 底部 4px 进度条。
- **页型配方要点**:
  - cover: 桃陶底 + rough-box 双线描边大标题 + 2px stroke 涂鸦角饰。
  - stat-grid: filled-block 炭黑底桃字数字块 + 有机不对称圆角卡。
  - quote: 展示体大引文 + 鹅卵石形边框。
  - timeline: step-node-circle 圆形节点 + 双线描边连线。
  - closing: vertical-text 90° 书脊装饰 + filled-block 收底。

### 2.26 raw-grid

- **look**: 粗野创始人路演风——纯白底、纯黑 3px 重边即布局（格间无缝相接）、黑色硬偏移阴影、双粉彩（腮粉 / 鼠尾草绿）仅作区域填充不作文字色、低透明巨数字壁纸、零 web 字体原生栈。
- **pick-when**: 粗野 / 路演 / 零装饰；想要结构诚实与原始图形力的产品。
- **核心 token**: `--surface-color:#FFFFFF` `--surface-muted:#F5F5F5` `--text-primary:#0A0A0A` `--text-secondary:#333333` `--primary-color:#0A0A0A`（结构墨黑） `--secondary-color:#F2D4CF`（腮粉） `--tertiary-color:#E5EDD6`（鼠尾草绿；二粉彩仅作区域填充不作文字色） `--outline-color:#0A0A0A`（3px）；on-primary `#FFFFFF`（显式）。
- **字体·形状**: 展示体 `system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif`（900，uppercase；零 web 字体原生栈）/ 正文同栈（500）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px（唯一 donut 50%）；密度中；阴影 `6px 6px 0`/`4px 4px 0` 纯黑硬偏移零模糊。
- **签名动效**: entry 0s / exit 0s（即时切换无过渡）/ ambient 无。
- **页型配方要点**:
  - cover: 3px 黑边网格分割 + 900 uppercase 大标题 + 低透明巨数字壁纸（0.15-0.35）。
  - stat-grid: 黑边格间无缝相接 + 粉彩区域填充 + 黑硬偏移。
  - quote: `→` 箭头 ::before 前缀引文 + 黑底白字 label。
  - timeline: 3px 黑边节点格 + 粉彩交替填充。
  - closing: 黑全幅底 + 白字 900 uppercase 收底 + 巨数字壁纸。

### 2.27 retro-windows

- **look**: 复古 OS 风——`#D4D0C8` 系统灰底、navy 渐变标题栏 + `_ □ X` 窗控、双色不对称 bevel 边框（白左上 / 黑右下）、Tahoma 系统字、CRT 扫描线 3px 周期 3%、marquee 走马灯 ambient。
- **pick-when**: 复古 / OS 怀旧 / 高密度信息；想要桌面系统隐喻与像素怀旧的产品。
- **核心 token**: `--surface-color:#D4D0C8`（btn-face） `--surface-muted:#C0C0C0` `--text-primary:#222222` `--text-secondary:#555555` `--primary-color:#000080`（navy） `--secondary-color:#1084D0` `--tertiary-color:#008000`（复古绿；语义状态色红 `#800000` 黄 `#808000` 青 `#008080`） `--outline-color:#000000`（bevel 白左上 / 黑右下 / `#404040`）；on-primary `#FFFFFF`（navy 标题栏白字，显式）。
- **字体·形状**: 展示体 `Tahoma,"Segoe UI",system-ui,sans-serif`（700；MS Sans Serif 近似）/ 正文同栈（400）/ 数据与终端 `ui-monospace,"SF Mono",Consolas,monospace`（像素 / 终端点缀）；圆角 0px 全系统；密度高；阴影零模糊（深度 = 双色不对称边框 bevel 凸起 / 凹陷 + inset + 白灰色块 + CRT 扫描线 3px 周期 3% 黑）。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient marquee 14s linear 循环。
- **页型配方要点**:
  - cover: win-window 大窗口（navy 渐变标题栏 + `_ □ X` + 文件名式标题 `AGENDA.TXT`）+ CRT 扫描线。
  - stat-grid: panel-sunken 白井统计区 + group-box 分组 + navy 进度条。
  - quote: group-box 引文框 + bevel 凸起落款条。
  - timeline: tree-item 文件夹/文档字形树状时间线（navy 选中态反转）。
  - closing: btn-retro 按压反转 bevel 按钮 + marquee 告别滚动条。

### 2.28 retro-zine

- **look**: 独立油印 zine 风——卡其纸底、深林绿 accent、condensed uppercase 宽字距展示体、绿块 12px 纸叠纸偏移、±5-8° 旋转拼贴 + 半透明胶带、SVG grain 0.07 常驻。
- **pick-when**: 油印 / 独立出版 / 拼贴；想要复印 zine 式粗粝与 DIY 精神的产品。
- **核心 token**: `--surface-color:#C8B99A`（深 `#B8A98A`） `--surface-muted:#B8A98A` `--text-primary:#1A1A1A` `--text-secondary:#1A1A1A`（60%） `--primary-color:#008F4D`（浅 `#00A85D`） `--secondary-color:#F4EFE6`（奶白） `--tertiary-color:#00A85D` `--outline-color:#000000`（3px 结构 / 2px 子区域 / 1.5px 格线）；on-primary `#F4EFE6`（绿 ribbon 奶白字，显式）。
- **字体·形状**: 展示体 `"Arial Narrow","PingFang SC",system-ui,sans-serif`（condensed，uppercase，宽字距）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（300-500）/ 手写面 `"Kaiti SC","Bradley Hand","Segoe Script",cursive`；圆角 0px 全系统；密度中高；阴影零 web 阴影（深度 = 绿块 12px 纸叠纸偏移 ::before、±5-8° 旋转、SVG grain 0.07 常驻、半透明胶带）。
- **签名动效**: entry 淡入 + 20px 上浮（非活跃页 `opacity:0;translateY(20px)`，时序 `cubic-bezier(0.19,1,0.22,1)` 0.4s）/ exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 导航提示 0.4s。
- **页型配方要点**:
  - cover: 卡其纸底 + condensed uppercase 大标题 + 绿色 drop cap + 半透明胶带角饰。
  - stat-grid: ledger-row + chip 标签组合（1.5px 格线）+ 绿块 12px 纸叠偏移。
  - quote: inline-highlight 马克笔强调引文 + 手写面注解。
  - timeline: collage + tape 拼贴式节点（±5-8° 旋转）。
  - closing: stamp-mark −8° 印章 + 绿 ribbon 收底带。

### 2.29 sakura-chroma

- **look**: 日式复古目录风——骨白底、暖棕墨字、六原色轮换（红粉橙绿蓝黄）、condensed 900 负字距展示体、8px 棕墨硬偏移、4px 周期半调点纸纹 16% 必选、星爆印章。
- **pick-when**: 日式 / 复古目录 / 多色轮换；想要昭和印刷目录式密度与原色能量的产品。
- **核心 token**: `--surface-color:#F1E6CB`（深 `#E5D6B0`） `--surface-muted:#E5D6B0` `--text-primary:#3A2516` `--text-secondary:#3A2516`（60%） `--primary-color:#E5392A` `--secondary-color:#3F8BC4` `--tertiary-color:#F0BC2A`（六原色轮换：红 `#E5392A` 粉 `#E54489` 橙 `#F09131` 绿 `#3D9F47` 蓝 `#3F8BC4` 黄 `#F0BC2A`） `--outline-color:#3A2516`（1.5px）；on-primary `#F1E6CB`（红章奶油字，显式）。
- **字体·形状**: 展示体 `"Arial Narrow","PingFang SC",system-ui,sans-serif`（900，负字距）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（400-700）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（规格行）；圆角 0px（花瓣 50% 正圆 / 印章 32 角星 clip-path）；密度中高；阴影 `8px 8px 0` 棕墨硬偏移（仅引文框）+ 4px 周期半调点纸纹 16% 必选。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 骨白底 + condensed 900 大标题 + petals-cluster 4-5 叠圆 + 斜向五色 ribbon ±22°。
  - stat-grid: card-product 目录卡 + mono 规格行 + bar-eq 均衡器 VU 表条。
  - quote: red-stamp −3° 印章落款 + 8px 棕墨偏移引文框。
  - timeline: nb-checkbox 方格勾选节点 + 六原色轮换阶段色。
  - closing: rosette-seal 星爆章 + 五色 ribbon 收底。

### 2.30 scatterbrain

- **look**: 工作坊白板风——暖白底（软木 / 网格纸 / 暖渐变三底纹变体每页选一）、七色便利贴轮换（各带深档）、图钉径向渐变 3D 珠 + 半透明胶带、便利贴 ±1-5° 旋转、全库唯一允许软模糊阴影。
- **pick-when**: 工作坊 / 头脑风暴 / 便利贴拼贴；想要白板会议式自发感与协作感的产品。
- **核心 token**: `--surface-color:#FAF8F3`（三底纹变体：软木 / 网格纸 / 暖渐变） `--surface-muted:#F7F5F0` `--text-primary:#2D2A26` `--text-secondary:#5C5750` `--primary-color:#FFE066`（便利贴黄） `--secondary-color:#A5D8FF`（蓝） `--tertiary-color:#FFC9C9`（粉；七色轮换各带深档：黄 `#FFD43B` 橙 `#FFCC80` 紫 `#D0BFFF` 绿 `#B2F2BB`） `--outline-color:#2D2A26`（白便签 2px 边）；on-primary `#2D2A26`（所有粉彩上墨字不反转，显式）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（900，chunky 装饰 serif 近似）/ 正文 `"Songti SC","SimSun",Georgia,serif`（400，slab）/ 手写面 `"Kaiti SC","Bradley Hand","Segoe Script",cursive`；圆角便签 0 / 图标图钉 50% / 图表条 3px；密度中（1-4 便签 + 1-2 装饰）；阴影全库唯一允许软模糊：`2px 3px 15px rgba(45,42,38,0.15), 0 1px 3px rgba(45,42,38,0.25)`。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无（滚轮 700ms 锁）。
- **页型配方要点**:
  - cover: 软木底纹 + 主便签卡（±1-3°）+ 图钉 3D 珠 + doodle 0.15 角饰。
  - stat-grid: 七色便利贴网格（浮动卡 ±5-15° 旋转）+ 软模糊阴影。
  - quote: 大号便利贴 + 手写面引文 + 胶带角饰。
  - timeline: 虚线二次贝塞尔连线（凹凸交替 + 三角箭头）+ 便利贴节点。
  - closing: 网格纸底纹 + 图钉自定义光标彩蛋 + 手写收底。

### 2.31 signal

- **look**: 机构董事会汇报风——navy 与奶油双表面逐页互换、古金唯一 accent（仅规线 / 标题内斜体强调 / 统计数字三用途）、serif 展示 9.5vw 行高 0.96、单页填充 ≤50% 不对称留白、零阴影零渐变。
- **pick-when**: 机构 / 董事会 / 克制严肃；想要董事会材料式权威与编辑精度的产品。
- **核心 token**: 双表面——navy `#1C2644`（alt `#232F55`）与奶油 `#F0ECE3`（alt `#E6E0D4`）逐页互换；navy 面 `--text-primary:#E2DCD0` `--text-secondary:#8A96A8`（三级 `#4E5A6E`），奶油面 `--text-primary:#1A2030` `--text-secondary:#5A6270`（三级 `#9AA0A8`）；`--primary-color:#C8A870`（古金唯一 accent） `--outline-color:#2E3D5C`（深面）/`#CAC4B4`（浅面）；on-primary 不适用（金从不作填充）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（600-700；display 9.5vw 行高 0.96 负字距）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（400）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（500，uppercase，0.14-0.22em）；圆角 0px（唯一 donut 50% / 时间线点 9px / 图例 2px）；密度中低不对称（单页填充 ≤50%）；阴影无渐变无（仅全幅图底 scrim）；暗页 80px 网格纹理 3% 白指纹。
- **签名动效**: entry `cubic-bezier(0.16,1,0.3,1)` 0.5-0.85s 错峰（delay 0-6）/ exit（翻页）`cubic-bezier(0.77,0,0.175,1)` / ambient 无。
- **页型配方要点**:
  - cover: navy 面 + serif 大标题内嵌古金斜体 `<em>`（Signal moment；CJK 降级为仅颜色替代）+ 36px 金短线。
  - stat-grid: stat-card 古金 serif 数字 5.5vw 600 −0.02em + 发丝分隔。
  - quote: chromeless 声明页（serif 声明居中裸面，无卡片）。
  - timeline: vt-spine 1px 竖发丝 + 9px 金点 + em-dash 金 mono 项目符。
  - closing: pyramid band 3px 金左边 + color-mix 递减 + 双表面反转收底。

### 2.32 soft-editorial

- **look**: 文学杂志柔和风——暖纸底、五粉彩互换无固定语义（尘粉 / 柠檬 / 鼠尾草 / blush / lilac）、serif roman/italic 混排、chrome 永不用 mono 永不 uppercase、半透明白卡透纸色、零阴影、全库无方角。
- **pick-when**: 文学 / 柔和 / 杂志感；想要文学期刊式温和与纸面透光感的产品。
- **核心 token**: `--surface-color:#F2EEDF`（2 `#ECE6D2`） `--surface-muted:#ECE6D2` `--text-primary:#2A241B` `--text-secondary:#5C5345` `--primary-color:#E1A4C2`（尘粉） `--secondary-color:#D6DD63`（柠檬） `--tertiary-color:#B7C7A8`（鼠尾草；五粉彩互换无固定语义：加 blush `#E8C9B6`、lilac `#C9BEDC`） `--outline-color:rgba(42,36,27,0.18)`（主分隔 0.35）；卡片填充 `rgba(255,255,255,0.55)`；on-primary `#2A241B`（所有粉彩填充上墨字永不反转，显式）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（500，roman/italic 混排；斜体短语降 400）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（400-500）；永不用 mono、永不 uppercase（chrome 用斜体 serif + 普通 sans）；圆角 pill 999px / 卡 22-36px / 小件 14-18px（无方角）；密度卡内中高卡间慷慨；阴影无（深度 = 半透明白卡透纸色 + 圆角 + 色块，卡不叠卡）。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 暖纸底 + serif 500 标题 + swatch-dot 色点行（五粉彩预览）。
  - stat-grid: 半透明白卡（0.55 透纸色）+ 22-36px 圆角 + 粉彩数字。
  - quote: 132px drop cap 开篇 + 斜体 serif 大引文。
  - timeline: marker-rule 虚线签注时间线 + pill 节点。
  - closing: action-bar 柠檬行动条 + 斜体 serif 双栏页脚。

### 2.33 stencil-tablet

- **look**: 档案田野手册风——骨白底、纯黑字、七色轮换 accent（洋红 / 青 / 芥末 / 赭 / 橙 / 蓝 / 橄榄）、stencil 风展示体（重 condensed 900 uppercase 近似 + 背景色细横条模拟 ink-break 断口）、色块铺满画布、零阴影零渐变。
- **pick-when**: 档案 / 田野手册 / 色块轮换；想要标本目录式系统感与模板印刷质感的产品。
- **核心 token**: `--surface-color:#E2DCC9`（骨白） `--surface-muted:#F4EFE0`（纸） `--text-primary:#0A0A0A` `--text-secondary:#0A0A0A`（60%） `--primary-color:#C73B7A`（洋红） `--secondary-color:#2D7E73`（青） `--tertiary-color:#D8A93B`（芥末；七色轮换：加赭 `#A06A3C` 橙 `#EE7A2E` 蓝 `#3F73B7` 橄榄 `#6F7A2E`） `--outline-color:#0A0A0A`；on-primary `#E2DCC9`（黑底骨字；色块卡上按 §2 推导规则实算）。
- **字体·形状**: 展示体 `"Arial Narrow","PingFang SC",system-ui,sans-serif`（900，uppercase；stencil 无系统平替→叠背景色细横条模拟 ink-break 断口）/ chrome 同栈（600-800，uppercase，0.06-0.14em）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（400，唯一 sentence case）；圆角 pill 999 / tablet 26px / 卡 22px / 时间线条 18px / cover mark 14px / 图表框 0；密度高（色块铺满画布）；阴影无渐变无（深度 = 色块邻接 + 圆角 tablet；暗 agenda 页 organic blob SVG 底）。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: 骨白底 + 540px 级分节巨数字 + stencil 风主标（ink-break 横条）+ cover mark 14px 圆角。
  - stat-grid: 220px tablet 色块统计卡（每卡不同 accent）+ 160px stat 数字。
  - quote: matrix 头行反转（黑底骨字）+ 芥末 action-bar 行动条。
  - timeline: process-node 每步不同 accent + 18px 圆角时间线条。
  - closing: 七色轮换收底色块 + stencil 风收底词。

### 2.34 studio

- **look**: 高压工作室宣言风——近黑与酸黄二元反转（或反之）、次级色用同色透明度档不用灰、sans 900 uppercase 负字距 12vw 封面、1px 发丝 chrome + 2px stat 顶规、零阴影零渐变。
- **pick-when**: 宣言 / 高压 / 二元反转；想要设计工作室式攻击性自信的产品。注意：深底 + 酸色属 Lazy Defaults 限制区，仅用户明确点名或有品牌理由时使用，且整套一致、不混用、霓虹不进正文。
- **核心 token**: 二元反转——近黑 `#1C1C1C`（alt `#242422`）底 + 酸黄 `#F5D200`（alt `#F0CC00`）字，或反之；深面 `--text-secondary:rgba(245,210,0,0.58)`（三级 0.32），浅面 `--text-secondary:rgba(28,28,28,0.62)`（三级 0.35）——同色透明度档不用灰；`--primary-color:#F5D200` `--outline-color:#2E2E2C`（深面）/`rgba(28,28,28,0.18)`（浅面）；on-primary `#1C1C1C`（黄底近黑字，显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（900，uppercase，负字距 −0.01..−0.03em；12vw 封面 / 7.5vw 声明）/ 正文同栈（400/500）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（500，仅元数据）；圆角 0px；密度低刻意稀疏；阴影无渐变无（深度 = 双表面反转 + 1px 发丝 chrome / 2px stat 顶规与图表基线 + 900 字重质量）。
- **签名动效**: entry `cubic-bezier(0.16,1,0.3,1)` 0.5s / exit（翻页）`cubic-bezier(0.77,0,0.175,1)` 0.75s（比 signal 更短更锐）/ ambient 无。
- **页型配方要点**:
  - cover: 近黑底 + 12vw sans 900 uppercase 大标题 + 三栏 mono 元数据 footer（工作室 × 客户 / 标题 / 工作室名）。
  - stat-grid: stat-card 2px 顶规 + 酸黄大数字 + 发丝分隔。
  - quote: 7.5vw 声明页（表面反转：黄底黑字）。
  - timeline: 发丝轴 + 方角节点 + em-dash 随表面 accent 色。
  - closing: 二元反转收底 + mono 元数据 footer 重现。

### 2.35 vellum

- **look**: 学术单色场风——长春花蓝紫 `#2A3870` 全 deck 无反转、暖黄绿文字三档透明度、serif 斜体 400 全场景（斜体即人格）、每页左下青色 mono 注记、全 0s 刻意静止、零阴影零渐变。
- **pick-when**: 学术 / 白皮书 / 单色场静止；想要学术期刊式庄重与排印一致性的产品。
- **核心 token**: `--surface-color:#2A3870`（对比板 `#1F2858`/`#34407A`/alt `#343F80`，全 deck 无反转） `--surface-muted:#1F2858` `--text-primary:#E8D85C` `--text-secondary:#E8D85C`（62%/32% 三档） `--primary-color:#E8D85C` `--secondary-color:#3A7878`（尘青：引号形 / kicker / 28px 短线 / 列表计数） `--tertiary-color:#F5E168`（强调黄，`<em>` 专用） `--outline-color:#E8D85C`（20% 黄发丝）；on-primary 不适用（黄 / 青仅作文字不作填充）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（斜体 400 全场景；斜体即人格，CJK 无斜体→颜色 / 字重替代）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（400）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（400-500，打字机注记声）；圆角 0px；密度低居中（内容宽 55-80%）；阴影无渐变无（深度 = 蓝紫双档对比板 + 黄三档透明度 + 20% 黄发丝）。
- **签名动效**: entry 0s / exit 0s（全即时翻页、无入场动画，刻意静止）/ ambient 无。
- **页型配方要点**:
  - cover: 蓝紫单色场底 + serif 斜体居中大标题 + 左下 pin-note 青色 mono 注记（每页常驻）。
  - stat-grid: pin-stat 竖排居中统计（黄色数字三档透明度）。
  - quote: 7vw 青色 serif 斜体引号形居中 + 斜体引文。
  - timeline: CSS counter 编号列表 + 28px 青色短线阶段标。
  - closing: 单色场收底 + pin-note 注记重现 + 强调黄 `<em>` 收底词。

### 2.36 porcelain-indigo

- **look**: 冷瓷学术杂志风——瓷白冷底、深靛蓝单墨（墨即主题色），暗靛反转页（墨底瓷字）作节奏，1px 靛蓝发丝线分栏，serif 展示 + mono 栏目标签 chrome，零彩色零阴影零渐变。
- **pick-when**: 冷静 / 理性 / 深度内容；想要学术期刊式克制与工程文化气质的科技研究、数据分享、技术发布产品。锁定 M 系登记版式（M01-M10），不与 S 系混用。
- **核心 token**: `--surface-color:#F1F3F5` `--surface-muted:#E4E8EC` `--text-primary:#0A1F3D` `--text-secondary:#0A1F3D`（降 opacity 至 60%） `--primary-color:#0A1F3D`（双色单墨，墨即主色） `--secondary-color:#152A4A` `--tertiary-color:#E4E8EC` `--outline-color:#0A1F3D`（20% 软发丝）；on-primary `#F1F3F5`（墨底瓷字，显式）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（400-600，紧行高）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（400）/ 数据与栏目标签 `ui-monospace,"SF Mono",Consolas,monospace`（uppercase，0.1-0.16em）；圆角 0px；密度中低（两段式页标题-内容间距 65-86px）；阴影无渐变无（深度 = 墨/纸反转页 + 发丝线）。
- **签名动效**: entry `cubic-bezier(0.19,1,0.22,1)` 0.4s / exit `cubic-bezier(0.755,0.05,0.855,0.06)` 0.6s / ambient 无。
- **页型配方要点**:
  - cover: M01 开场封面——深靛 hero-dark 底 + 瓷白 serif 巨字（192px 档）+ mono kicker（场合·主讲人），页眉不写页码。
  - stat-grid: M03 数据大字报——瓷白底 3×2 六格统计卡，数字深靛，卡间 1px 靛蓝发丝线，数字过长用 K/M 简写。
  - quote: M08 大引用页——dark 优先（靛底瓷字），serif 金句 111px 档逐句揭示 + 出处 lead 65% 透明度。
  - timeline: M06 两列流水线——mono 靛蓝步骤编号 + fragment 分步点亮；旧/新范式对照改 M09（左列 55% 透明度弱化）。
  - closing: M07 悬念问题页——靛蓝 hero-dark + 巨字三行断在语义处；多幕 deck 用 M02 幕封收束（hero dark/light 交替呼吸）。

### 2.37 kraft-journal

- **look**: 牛皮纸手账人文杂志风——深牛皮底、深棕单墨、暖米 tint 区块作层次，棕墨发丝规线分栏，serif 引文 + sans 正文，零阴影零渐变，全库最暖的纸面色位。
- **pick-when**: 怀旧 / 人文 / 老笔记本；想要牛皮信封式温度与年代感的书评、文学历史、手作品牌、生活方式产品。锁定 M 系登记版式（M01-M10），不与 S 系混用。
- **核心 token**: `--surface-color:#EEDFC7` `--surface-muted:#E0D0B6` `--text-primary:#2A1E13` `--text-secondary:#2A1E13`（60%） `--primary-color:#2A1E13`（双色单墨，墨即主色） `--secondary-color:#3A2A1D` `--tertiary-color:#E0D0B6` `--outline-color:#2A1E13`（25% 软发丝）；on-primary `#EEDFC7`（棕底牛皮字，显式）。
- **字体·形状**: 展示体 `"Songti SC","SimSun",Georgia,serif`（400-700）/ 引文面同栈斜体（CJK 无斜体→字重 / 颜色替代）/ 正文 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（400）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`；圆角 0px；密度中；阴影无渐变无（深度 = 牛皮双档色块 + 棕墨发丝线）。
- **签名动效**: entry `cubic-bezier(0.445,0.05,0.55,0.95)` 1.0s / exit `cubic-bezier(0.55,0.085,0.68,0.53)` 1.5s / ambient 无。
- **页型配方要点**:
  - cover: M01 开场封面——牛皮底 + 深棕 serif 巨字 + mono meta 行（作者·身份），卷次文案强化年代语义（如"Vol.03 · 秋"式）。
  - stat-grid: M03 数据大字报——六格卡牛皮双档（#EEDFC7/#E0D0B6）交替，数字深棕 serif 大字。
  - quote: M08 大引用页——深棕 hero-dark 反转（棕底牛皮字）+ 斜体引文 + meta 出处行。
  - timeline: M06 两列流水线——mono 棕编号步骤行 + 发丝分隔线分步点亮；多案例图片实证改 M05（281px 固定高网格）。
  - closing: M07 悬念问题页——牛皮底巨字居中三行 + 棕短线收底；或 M02 幕封式收束。

### 2.38 swiss-ultramarine

- **look**: 瑞士国际主义皇家蓝锚点——高级灰白底（非纯白）+ 统一三档灰阶，深皇家蓝单一高饱和 accent，16 列网格 + 1px 发丝线，巨字 200 超轻 / 重点数字 300 / 小标 600，直角纯色不透明，零渐变零阴影零圆角。
- **pick-when**: 冷静 / 理性 / 学术感；想要单锚点色瑞士克制的商业发布、科技产品、设计领域分享。锁定 S 系登记版式（S01-S25）；高密度黄块填满改 neo-grid-bold，全墨零彩色改 monochrome。
- **核心 token**: `--surface-color:#FAFAF8` `--surface-muted:#F0F0EE`（灰底卡） `--text-primary:#0A0A0A` `--text-secondary:#737373` `--primary-color:#002FA7`（皇家蓝唯一 accent） `--secondary-color:#0A0A0A`（ink 反转块） `--tertiary-color:#D4D4D2` `--outline-color:#D4D4D2`（1px 发丝）；on-primary `#FFFFFF`（显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（200 巨字，拉丁字距 −0.04em 行高 0.9-0.94；中文巨标题字距归零行高 1.15-1.25）/ 正文同栈（300）/ 小标同栈（600）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（`font-feature-settings:"tnum"`）；圆角 0px 全元素；密度中（16 列网格 gap 16px）；阴影无渐变无（accent 不加阴影 / 圆角 / 透明度）。
- **签名动效**: entry expressive `cubic-bezier(0,0,0.3,1)` 0.4-0.7s（每页一个语义化 recipe 与图形耦合：数字 scale 弹入 / bar scaleY 拉起 / 圆环 stroke-dashoffset 描线）/ exit productive `cubic-bezier(0.2,0,0.38,0.9)` 0.24s / ambient 无。
- **页型配方要点**:
  - cover: S01 目录封面——皇家蓝 accent 满屏 + 三行 cover-row（mono 编号 + 巨字 205px/200）；调性不合时改左 ink 右纸白对开变体。
  - stat-grid: S06 KPI 塔（bar 高度数据驱动、皇家蓝 bar）/ 4-6 行账单改 S20 / 规格 benchmark 改 S21。
  - quote: S03 分屏陈述（左半皇家蓝反白巨字 / 右半灰底解释栏）/ 中段宣言改 S12 ink 通栏。
  - timeline: S11 横向（8×8 直角方块节点，无数据）/ 带数据演化改 S02 / 闭环改 S14。
  - closing: S10 分屏收束——左半皇家蓝满屏巨字宣言 + 右半纸白 3 条 takeaway，第 3 条穿蓝完成缝合。蓝色只做 KPI 数字与单焦点卡，满屏蓝即掉档；黑底页上蓝色反白同样克制。

### 2.39 swiss-lemon

- **look**: 瑞士风柠檬黄锚点——高级灰白底 + 统一三档灰阶，金柠檬黄单一高饱和 accent，块戳 / 下划线 / 单字符高亮为主要武器，16 列网格 + 1px 发丝线，直角纯色不透明，零渐变零阴影。
- **pick-when**: 年轻 / 活力 / 消费零售；想要鲜亮图形能量的运动、消费品、活力主题发布。锁定 S 系登记版式；高密度黄块填满的新粗野改 neo-grid-bold（金柠檬 vs 酸霓虹，色相与系统均不同）。
- **核心 token**: `--surface-color:#FAFAF8` `--surface-muted:#F0F0EE` `--text-primary:#0A0A0A` `--text-secondary:#737373` `--primary-color:#FFD500`（金柠檬黄唯一 accent） `--secondary-color:#0A0A0A`（ink 反转块） `--tertiary-color:#D4D4D2` `--outline-color:#D4D4D2`（1px 发丝）；on-primary `#0A0A0A`（浅色 accent——黄块上墨字，禁白字，显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（200 巨字，拉丁字距 −0.04em 行高 0.9-0.94；中文巨标题字距归零行高 1.15-1.25）/ 正文同栈（300）/ 小标同栈（600）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（`font-feature-settings:"tnum"`）；圆角 0px 全元素；密度中（16 列网格 gap 16px）；阴影无渐变无。
- **签名动效**: entry expressive `cubic-bezier(0,0,0.3,1)` 0.4-0.7s（每页一个语义化 recipe：数字 scale 弹入 / 节点序列点亮）/ exit productive `cubic-bezier(0.2,0,0.38,0.9)` 0.24s / ambient 无。
- **页型配方要点**:
  - cover: S01 目录封面——纸白底三行 cover-row + 柠檬黄块戳 accent；或黄满屏变体（黄底墨字）。
  - stat-grid: S15 矩阵 + 巨数（12 格灰底卡填满、强调项单独一张柠檬黄 accent 卡，单焦点法则）/ 6 项快讯改 S16 微卡。
  - quote: S09 点阵陈述——巨字三行宣言 + 柠檬黄单字符高亮（mark 式黄块），点阵 mask 从左推到右。
  - timeline: S11 横向——8×8 柠檬黄方块节点左→右依次点亮（220ms/节点）。
  - closing: S10 分屏收束——左半柠檬黄满屏 + 墨黑巨字宣言（黄底墨字），右半纸白 takeaway 第 3 条穿黄。

### 2.40 swiss-lime

- **look**: 瑞士风荧光柠檬绿锚点——高级灰白底 + 统一三档灰阶，荧光黄绿单一 accent，屏幕显色自带发光感，16 列网格 + 1px 发丝线，直角纯色不透明，零渐变零阴影。
- **pick-when**: 生态 / 未来 / 新兴；想要当代感的可持续、健康、Z 世代品牌、AI 创业项目。锁定 S 系登记版式；深底酸黄二元反转改 studio（本套是浅底单锚点，结构不同）。
- **核心 token**: `--surface-color:#FAFAF8` `--surface-muted:#F0F0EE` `--text-primary:#0A0A0A` `--text-secondary:#737373` `--primary-color:#C5E803`（荧光柠檬绿唯一 accent） `--secondary-color:#0A0A0A`（ink 反转块） `--tertiary-color:#D4D4D2` `--outline-color:#D4D4D2`（1px 发丝）；on-primary `#0A0A0A`（浅色 accent——绿块上墨字，禁白字，显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（200 巨字，拉丁字距 −0.04em 行高 0.9-0.94；中文巨标题字距归零行高 1.15-1.25）/ 正文同栈（300）/ 小标同栈（600）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（`font-feature-settings:"tnum"`）；圆角 0px 全元素；密度中（16 列网格 gap 16px）；阴影无渐变无。
- **签名动效**: entry expressive `cubic-bezier(0,0,0.3,1)` 0.4-0.7s（圆环 stroke-dashoffset 描线 / 节点序列点亮）/ exit productive `cubic-bezier(0.2,0,0.38,0.9)` 0.24s / ambient 无。
- **页型配方要点**:
  - cover: S01 目录封面——灰白底 + 荧光绿 mono 编号列 + 巨字 205px/200；或左 ink 右纸白对开变体（ink 块上一条绿线）。
  - stat-grid: S06 KPI 塔（荧光绿 bar，高度数据驱动，最小 65px 最大 389px）/ 层级架构与生态地图改 S17 同心圆（引线绿色、标签 HTML）。
  - quote: S03 分屏陈述——左半 ink 底反白巨字 + 荧光绿强调词，右半灰底解释栏错峰升入。
  - timeline: S14 闭环流程——同心圆环荧光绿 stroke-dashoffset 描线 + 灰底直角节点序列点亮。
  - closing: S10 分屏收束——左半荧光绿满屏 + 墨黑巨字（绿底墨字），右半 takeaway 第 3 条穿绿。

### 2.41 swiss-safety

- **look**: 瑞士风安全橙锚点——高级灰白底 + 统一三档灰阶，安全橙单一 accent 承担工业紧迫感与视觉锚点感，只做局部高亮不做满屏，16 列网格 + 1px 发丝线，直角纯色，零渐变零阴影。
- **pick-when**: 工业 / 警示 / 转折点；想要锚点级紧迫感的制造业、汽车、施工安全、"警告 / 决策"主题内容。锁定 S 系登记版式；墨黑/火橙双色调抗议海报改 broadside（本套是灰白底单锚点，结构不同）。
- **核心 token**: `--surface-color:#FAFAF8` `--surface-muted:#F0F0EE` `--text-primary:#0A0A0A` `--text-secondary:#737373` `--primary-color:#FF6B35`（安全橙唯一 accent） `--secondary-color:#0A0A0A`（ink 反转块） `--tertiary-color:#D4D4D2` `--outline-color:#D4D4D2`（1px 发丝）；on-primary `#FFFFFF`（橙为中明度 accent——橙底白字必须 ≥600 字重才达对比度，显式）。
- **字体·形状**: 展示体 `"PingFang SC","Microsoft YaHei",system-ui,sans-serif`（200 巨字，拉丁字距 −0.04em 行高 0.9-0.94；中文巨标题字距归零行高 1.15-1.25）/ 正文同栈（300）/ 小标同栈（600）/ 数据 `ui-monospace,"SF Mono",Consolas,monospace`（`font-feature-settings:"tnum"`）；圆角 0px 全元素；密度中（16 列网格 gap 16px）；阴影无渐变无。
- **签名动效**: entry expressive `cubic-bezier(0,0,0.3,1)` 0.4-0.7s（条宽 0→目标 / 中线 scaleY 先拉开）/ exit productive `cubic-bezier(0.2,0,0.38,0.9)` 0.24s / ambient 无。
- **页型配方要点**:
  - cover: S01 目录封面——左 ink 右纸白对开变体（ink 块上一条橙规线），橙不满屏。
  - stat-grid: S07 横向条形（1px 橙条 0→目标宽 + 末端数字 count-up，必须真实数据）/ 4-6 行账单改 S20（巨数橙）。
  - quote: S12 宣言 + ink 通栏——上半橙短线 + 大字 4 行宣言，下半 ink 通栏 scaleX 铺开 + 反白短句。
  - timeline: S08 双轨对照——中线 1px 纵线 scaleY 0→1 先拉开，旧/新两列镜像入场，新列橙强调。
  - closing: S10 分屏收束——经典 ink 双半屏变体（左 ink 巨字 / 右纸白 takeaway），第 3 条橙收口。

## 3. 主题五维旋钮

预设锁定后，用五维旋钮微调，不另选预设：

| 维度 | 选项 | 说明 |
|---|---|---|
| **theme** | Dark / Light / Palette | Dark `#0e0e0e` 底 `#eee` 字；Light `#f5f3ef` 底 `#1a1a1a` 字；Palette 用 §4 配色色 |
| **corners** | 0px / 4px / 12px | Sharp / Slight / Rounded；覆盖预设圆角档 |
| **density** | Tight / Normal / Generous | Tight padding 8-12px gap 8-12px；Normal padding 16-24px gap 16-20px；Generous padding 32-48px gap 28-40px |
| **depth** | Flat / Subtle / Layered | Flat 无阴影；Subtle 淡阴影；Layered 光晕 + 层次 |
| **ease** | Confident / Snappy / Gentle / Bouncy / Elastic / Sharp | `cubic-bezier(0.165,0.84,0.44,1)` / `cubic-bezier(0.19,1,0.22,1)` / `cubic-bezier(0.445,0.05,0.55,0.95)` / `cubic-bezier(0.34,1.56,0.64,1)` / `@keyframes` 多段回弹 / `cubic-bezier(0.755,0.05,0.855,0.06)` |

**选项设计规则——14px swatch 可辨**：任何配色 / 主题选项必须在 14px swatch 尺寸下可分辨。两个选项若背景明度相同且 accent 色相近似，删一个。

**用户无风格偏好时——先预览再定稿**：不默默选，走五步：

1. **三阶收敛读文件**：先只读 §1 路由表按情绪 / 受众圈出 3-5 套 → 再只读候选条目的 look / pick-when → 仅对进入预览的一套读条目全文；不通读四十一套。
2. **出 3 个真实标题页**：1 个安全款（最贴受众的一套）+ ≥1 个 bold 款（高张力套）+ 1 个 wildcard 款（跨情绪套），用 deck 真实标题与真实数据，合并为单文件双击可翻页浏览。
3. **预览真实性铁律**：预览页只出现将真实上屏的内容，禁止内部工作流词汇（预设名、token 名、旋钮档位）上屏。
4. **定稿后全套锁定**：用户选定一套即锁定，后续微调只走 §3 五维旋钮；禁止中途换预设或混用两套元素。
5. **定稿后迭代纪律**：新增页面元素只从锁定预设的既有原语（组件 / 圆角档 / 动效档）派生；禁止引入第二 accent、新圆角档、预设外动效；需求确实越界时回到选型流程重锁。

候选间差异必须 14px swatch 可辨。

## 4. 配色库（9 类 72 组）

按类分组，每组一行：序号 + hex（多数 5 色，非 5 色组注明实际色数）。不编造 hex，全部来自源配色文件。

### 单一主色推导三步法

用户只给一个主色（品牌色 / logo 吸色）时，从主色推导整套 token，不直接套 72 组色板。OKLCH 空间的派生与 chroma 阶梯规则见 `anti-ai-slop-design.md` §OKLCH 单色相派色板，本节不重复；本节给 hex token 工作流的 HSL 可运行实现。

1. **定基调**：主色转 HSL，记录 H（色相）与 S（饱和度）。按 H 扇区判暖/冷（判法见 §2 预设标注四字段·温度）；S 按用途封顶——大面积底色 S ≤ 12%、中性/文字层 S ≤ 30%、主色本身 S ≤ 72%（防屏幕荧光感）。主色 S/L 极端（近黑、近白、荧光）时先修正到可推导区间再走后续两步。
2. **算明度阶梯**：固定 H，L 走 97% → 92% → 82% → 42% → 14% 五档生成 surface / surface-muted / outline / text-secondary / text-primary。同 H 保证整套色温天然一致；中性色不是纯灰，带主色 8-14% 饱和度。暗底预设把阶梯反转（surface 取 14% 档、text 取 92% 档），accent 取高 L 档。
3. **配强调色**：secondary 取 (H+150)° % 360、tertiary 取 (H+210)° % 360 的分裂互补位，S 为主色的 0.6-0.8 倍，L 与主色同档或提亮一档；强调色只作小面积点睛。语义状态色（成功/警告/危险）用固定红黄绿，不从主色偏移推导——偏移位落不到正确语义色相上。

可运行推导函数（零依赖，输入主色 hex，输出 token 对象；`on-primary` 不在推导内，仍按 §2 白/近黑实算规则配对）：

```js
function derivePalette(hex) {
  const n = parseInt(hex.slice(1), 16);
  const r = ((n >> 16) & 255) / 255;
  const g = ((n >> 8) & 255) / 255;
  const b = (n & 255) / 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
  let h = 0;
  if (d !== 0) {
    if (max === r) h = ((g - b) / d) % 6;
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h = Math.round(h * 60);
    if (h < 0) h += 360;
  }
  const l = (max + min) / 2;
  const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1));
  const toHex = (hh, ss, ll) => {
    const a = ss * Math.min(ll, 1 - ll);
    const f = (k) => {
      const x = (k + hh / 30) % 12;
      const v = ll - a * Math.max(-1, Math.min(x - 3, 9 - x, 1));
      return Math.round(255 * v).toString(16).padStart(2, "0");
    };
    return "#" + f(0) + f(8) + f(4);
  };
  const sBase = Math.min(s, 0.72);
  const sNeutral = Math.min(sBase, 0.14);
  return {
    "--primary-color": toHex(h, sBase, l),
    "--surface-color": toHex(h, Math.min(sNeutral, 0.12), 0.97),
    "--surface-muted": toHex(h, sNeutral, 0.92),
    "--outline-color": toHex(h, sNeutral, 0.82),
    "--text-secondary": toHex(h, Math.min(sBase, 0.20), 0.42),
    "--text-primary": toHex(h, Math.min(sBase, 0.30), 0.14),
    "--secondary-color": toHex((h + 150) % 360, sBase * 0.8, l),
    "--tertiary-color": toHex((h + 210) % 360, sBase * 0.6, Math.min(l + 0.15, 0.85))
  };
}
```

推导后自检：① `--text-primary` 对 `--surface-color` 对比度实算 ≥ 4.5:1，不足把 text 的 L 压到 0.10 重算；② 交付说明写一句"为什么是这个色"（主色来源：品牌 logo / 内容真图 / 主题文化语境），写不出 = 在抽签，回 §1 路由表重选；③ 推导色板与下方 72 组是两条平行路径——有主色走推导，无主色从色板组选，同一 deck 不混用两条路径的产物。

canonical 数据：`assets/palettes.json`（下方 72 组与该 JSON 同源，程序化消费读 JSON，修改时两处同步）

### bold-energetic（8 组）

1. `#FFBE0B #FB5607 #FF006E #8338EC #3A86FF`
2. `#F72585 #7209B7 #3A0CA3 #4361EE #4CC9F0`
3. `#EF476F #FFD166 #06D6A0 #118AB2 #073B4C`
4. `#FF595E #FFCA3A #8AC926 #1982C4 #6A4C93`
5. `#9B5DE5 #F15BB5 #FEE440 #00BBF9 #00F5D4`
6. `#390099 #9E0059 #FF0054 #FF5400 #FFBD00`
7. `#3D348B #7678ED #F7B801 #F18701 #F35B04`
8. `#FFBC42 #D81159 #8F2D56 #218380 #73D2DE`

### clean-corporate（8 组）

1. `#FFFCF2 #CCC5B9 #403D39 #252422 #EB5E28`
2. `#22223B #4A4E69 #9A8C98 #C9ADA7 #F2E9E4`
3. `#3D5A80 #98C1D9 #E0FBFC #EE6C4D #293241`
4. `#2B2D42 #8D99AE #EDF2F4 #EF233C #D90429`
5. `#353535 #3C6E71 #FFFFFF #D9D9D9 #284B63`
6. `#E7ECEF #274C77 #6096BA #A3CEF1 #8B8C89`
7. `#CFDBD5 #E8EDDF #F5CB5C #242423 #333533`
8. `#2F6690 #3A7CA5 #D9DCD6 #16425B #81C3D7`

### dark-premium（8 组）

1. `#000000 #14213D #FCA311 #E5E5E5 #FFFFFF`
2. `#000814 #001D3D #003566 #FFC300 #FFD60A`
3. `#0D1B2A #1B263B #415A77 #778DA9 #E0E1DD`
4. `#0D1321 #1D2D44 #3E5C76 #748CAB #F0EBD8`
5. `#011627 #FDFFFC #2EC4B6 #E71D36 #FF9F1C`
6. `#0B090A #161A1D #660708 #A4161A #E5383B`
7. `#001427 #708D81 #F4D58D #BF0603 #8D0801`
8. `#001524 #15616D #FFECD1 #FF7D00 #78290F`

### jewel-rich（8 组）

1. `#5F0F40 #9A031E #FB8B24 #E36414 #0F4C5C`
2. `#780000 #C1121F #FDF0D5 #003049 #669BBC`
3. `#10002B #240046 #3C096C #5A189A #7B2CBF`
4. `#355070 #6D597A #B56576 #E56B6F #EAAC8B`
5. `#6F1D1B #BB9457 #432818 #99582A #FFE6A7`
6. `#231942 #5E548E #9F86C0 #BE95C4 #E0B1CB`
7. `#461220 #8C2F39 #B23A48 #FCB9B2 #FED0BB`
8. `#780116 #F7B538 #DB7C26 #D8572A #C32F27`

### monochrome（8 组）

1. `#F8F9FA #E9ECEF #DEE2E6 #CED4DA #ADB5BD #6C757D #495057 #343A40 #212529`（9 色）
2. `#0466C8 #0353A4 #023E7D #002855 #001233`
3. `#012A4A #013A63 #01497C #2A6F97 #468FAF #89C2D9`（6 色）
4. `#582F0E #7F4F24 #936639 #A68A64 #C2C5AA`
5. `#463F3A #8A817C #BCB8B1 #F4F3EE #E0AFA0`
6. `#03071E #370617 #6A040F #9D0208 #DC2F02 #F48C06 #FFBA08`（7 色）
7. `#590D22 #800F2F #A4133C #FF4D6D #FF8FA3 #FFCCD5`（6 色）
8. `#220901 #621708 #941B0C #BC3908 #F6AA1C`

### nature-earth（8 组）

1. `#606C38 #283618 #FEFAE0 #DDA15E #BC6C25`
2. `#DAD7CD #A3B18A #588157 #3A5A40 #344E41`
3. `#386641 #6A994E #A7C957 #F2E8CF #BC4749`
4. `#CAD2C5 #84A98C #52796F #354F52 #2F3E46`
5. `#F0EAD2 #DDE5B6 #ADC178 #A98467 #6C584C`
6. `#132A13 #31572C #4F772D #90A955 #ECF39E`
7. `#6B9080 #A4C3B2 #CCE3DE #EAF4F4 #F6FFF8`
8. `#233D4D #FE7F2D #FCCA46 #A1C181 #619B8A`

### neon-electric（8 组）

1. `#F72585 #B5179E #7209B7 #560BAD #3A0CA3`
2. `#70D6FF #FF70A6 #FF9770 #FFD670 #E9FF70`
3. `#7400B8 #6930C3 #5E60CE #5390D9 #48BFE3`
4. `#0B132B #1C2541 #3A506B #5BC0BE #6FFFE9`
5. `#540D6E #EE4266 #FFD23F #3BCEAC #0EAD69`
6. `#2D00F7 #6A00F4 #8900F2 #A100F2 #F20089`
7. `#FF6D00 #FF7900 #FF8500 #FF9100 #240046`
8. `#BBFBFF #8DD8FF #4E71FF #5409DA`（4 色）

### pastel-soft（8 组）

1. `#CDB4DB #FFC8DD #FFAFCC #BDE0FE #A2D2FF`
2. `#CCD5AE #E9EDC9 #FEFAE0 #FAEDCD #D4A373`
3. `#FFD6FF #E7C6FF #C8B6FF #B8C0FF #BBD0FF`
4. `#FFA69E #FAF3DD #B8F2E6 #AED9E0 #5E6472`
5. `#EDAFB8 #F7E1D7 #DEDBD2 #B0C4B1 #4A5759`
6. `#555B6E #89B0AE #BEE3DB #FAF9F9 #FFD6BA`
7. `#006D77 #83C5BE #EDF6F9 #FFDDD2 #E29578`
8. `#0081A7 #00AFB9 #FDFCDC #FED9B7 #F07167`

### warm-editorial（8 组）

1. `#264653 #2A9D8F #E9C46A #F4A261 #E76F51`
2. `#335C67 #FFF3B0 #E09F3E #9E2A2B #540B0E`
3. `#F4F1DE #E07A5F #3D405B #81B29A #F2CC8F`
4. `#F6BD60 #F7EDE2 #F5CAC3 #84A59D #F28F3B`
5. `#003049 #D62828 #F77F00 #FCBF49 #EAE2B7`
6. `#588B8B #FFFFFF #FFD5C2 #F28F3B #C8553D`
7. `#283D3B #197278 #EDDDD4 #C44536 #772E25`
8. `#0D3B66 #FAF0CA #F4D35E #EE964B #F95738`
