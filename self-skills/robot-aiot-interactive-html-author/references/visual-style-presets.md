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

## 2. 十三套设计系统预设

> 每套格式：look（一句话视觉）/ pick-when（一句话适用）/ 核心 token（覆盖变量 hex）/ 字体·形状 / 签名动效（entry·exit·ambient 缓动 + 时长）/ 页型配方要点（cover·stat-grid·quote·timeline·closing 各 1 行特有做法）。

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

**用户无风格偏好时**：生成 2-3 个候选主题（不同 theme + corners + density 组合）让用户挑选，不默默选。候选间差异必须 14px swatch 可辨。

## 4. 配色库（9 类 72 组）

按类分组，每组一行：序号 + hex（多数 5 色，非 5 色组注明实际色数）。不编造 hex，全部来自源配色文件。

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
