# PPT AI图像生成与封面设计

## 定位

为汇报 PPT（目标受众由用户指定，默认领导层）生成高质量配图、封面图和插图，增强视觉表达力。

## AI 图像生成

### Provider 自动选择优先级

Google → OpenAI → Azure → OpenRouter → DashScope → Z.AI → MiniMax → Replicate → Jimeng → Seedream → Agnes

codex-cli 永不自动选择。

### Quality 预设

- **normal** = 1K 快速预览
- **2k** = 2K 封面/插图（默认）

### 核心规则

- Reference-Image 身份保持：用简短硬编码语言，禁止长描述
- prompt 不含文字/字母，文案在后期叠加
- Batch 模式优先，每图最多 3 次重试
- Model 解析优先级：CLI > EXTEND.md > env > built-in default

## Banner/封面设计

### 5步工作流

1. **Gather Requirements** — 尺寸、平台、受众、核心信息
2. **Research & Art Direction** — 确定视觉方向
3. **Design & Generate** — HTML/CSS 构建 + AI 生图补充
4. **Export to Images** — 导出 PNG
5. **Present & Iterate** — 用户反馈迭代

### HTML/CSS 优先原则

Banner/封面用 HTML/CSS 构建，精确控制尺寸和排版：

- 安全区：核心内容居中 70-80%
- 最多 2 字体
- 单 CTA
- 文字对比度 ≥ 4.5:1
- 广告文字比 < 20%

### 视觉源优先级

用户提供素材 > CSS 构建视觉（渐变/几何/排版）> AI 图像生成

### 导出命名

`{style}-{width}x{height}.png`，kebab-case

### 22种 Art Direction 风格

Minimalist / Bold Typography / Gradient Flow / Geometric Abstract / Photo-driven / Illustration-led / Dark Mode / Light & Airy / Tech Grid / Organic Shapes / Retro / Futuristic / Duotone / Collage / Isometric / Flat Design / 3D Render / Neon Glow / Watercolor / Editorial / Motion-Ready / Data Visualization

## PPT 场景适配

| 页面类型 | 推荐方式 | 说明 |
|---------|---------|------|
| 封面 | HTML/CSS + AI 背景图 | 品牌色+标题+AI生成的氛围背景 |
| 章节分隔 | CSS 纯色/渐变 | 简洁过渡，不需AI生图 |
| 数据页 | SVG/HTML 图表 | 程序化生成，不用AI |
| 案例/故事 | AI 插图 | 具象化场景辅助理解 |
| 结尾/CTA | HTML/CSS | 联系方式+行动指令 |

## 无 API Key 降级策略

当环境中未配置任何图像生成 API Key 时：

1. **不阻塞主流程** — AI 图像生成是可选增强能力，缺失时自动降级
2. **封面降级为 CSS 构建** — 用 CSS 渐变、几何图形、品牌色块+排版构建封面，不依赖外部服务
3. **配图降级为程序化图表** — 调用 `robot-aiot-draw-flowchart` 的 SVG/PNG 导出管线替代
4. **提示用户** — 输出 `[NO-AI-IMAGE] 未检测到图像生成 API Key，封面/配图已降级为 CSS/程序化渲染`
5. **不尝试调用脚本** — 跳过 AI 生图步骤，直接进入 CSS/程序化路径

检测方式：检查环境变量中是否存在以下任一 Key：`GEMINI_API_KEY`、`OPENAI_API_KEY`、`AZURE_OPENAI_API_KEY`、`DASHSCOPE_API_KEY`、`MINIMAX_API_KEY`、`REPLICATE_API_TOKEN`。全部缺失即触发降级。

## 约束

1. AI 生成的图片不得承载事实数据，仅作视觉增强
2. 封面图必须包含品牌标识且不得遮挡标题
3. 所有配图需人工校验与内容的相关性
4. 用户未明确要求时不主动使用 AI 生图
5. PPT 静态版不使用动效，交互版按需添加
6. 无 API Key 时必须降级，不得虚构生成结果或静默跳过

## 截图取景与配图 Prompt 的母稿流程应用

本节定义截图素材与 AI 配图如何进入 PPT 母稿流程（Phase 1 素材盘点 → Phase 4 页面 HTML）。分工与交叉引用：

- 取景 7 参数完整定义、风格映射、prompt 模板全文（类型 1-7 / 瑞士风 1-5）、原生 SVG 静态地图规则 → `robot-aiot-interactive-html-author/references/content-imagery-and-infographic.md`
- 图片上屏原语（`.img-frame` 容器、contain/cover 选型、素材平铺与体积控制、scrim 边界）→ `robot-aiot-draw-flowchart/references/slide-image-framing.md`
- 本节只写 PPT 流程衔接点与 PPT 特有差异，不重复以上两处内容

### 截图资产化链路

1. **Phase 1 盘点**：素材图清单记录来源路径、内容类型（网页 / App / 代码 / dashboard / 设计稿）、处理目标（保真 / 统一美化 / 再设计）
2. **Phase 4 前合成**：逐张确定取景 7 参数 → 程序化合成（目标比例画布 + 统一背景 + 截图等比放入）→ 落 `doc-ppt/assets/`，命名 `{页号}-{语义}.png`
3. **上屏**：按 `slide-image-framing.md` 走 `.img-frame` 容器；截图 / UI / 文字密集图一律 contain，场景照片与 AI 氛围图 cover
4. **母稿联动**：合成产物写回母稿素材图映射表（页面 | 素材图 | 用途）；Phase 4 按表盘点，表中素材必须上屏，不得静默忽略

### 7 参数 PPT 默认值速查

| 参数 | PPT 默认 | 差异说明 |
|---|---|---|
| `ratio` | 由页面版式槽位决定（见下方适配表） | 页面画布恒 16:9，槽位比例 ≠ 页面比例 |
| `background` | 品牌色浅场 / paper / grid，全 PPT 统一一套 | 取自品牌资产（`brand-assets.md`）与 Phase 2 确认的风格基调，预生成复用 |
| `padding` | standard（网格图 compact、高图 spacious） | — |
| `inset` | subtle | 静态导出形态，浮起感靠背景对比即可 |
| `shadow` | soft（浅色风格预设）/ none（瑞士风预设） | 跟随受众→风格基调映射结果 |
| `corners` | 跟随风格预设：直角预设 square、圆角预设 small | — |
| `alignment` | center 为主，图文分栏页跟随文字列贴角 | — |

### PPT 页面尺寸适配

页面画布固定 1920×1080（scale-to-fit 壳，见 `phase4-page-authoring.md`）；槽位比例从页面布局换算：

| PPT 布局（`slide-layout-strategies.md` / `slide-image-framing.md` §3） | 图片槽位比例 | 取景要点 |
|---|---|---|
| 截图展示（设备框 + 标注） | 16:10 或 4:3 | 标注用静态 HTML/SVG 叠加层，不烧进像素 |
| 图文分栏（50/50 或 60/40） | 16:10 / 4:3 | alignment 跟随文字列，图与正文区顶对齐 |
| 全出血封面 / banner | 16:9 或 21:9 | cover 裁切须用户允许；标题侧走 scrim 规则 |
| 多图网格（单页 ≤4 张） | 同组统一比例 | 同组同背景、同边距、同格位尺寸 |
| 对比版式（改造前后 / 方案 A/B） | 两侧同尺寸同比例 | 7 参数两侧完全一致 |

### PPT 特有差异（相对 Web deck）

1. 静态交付：截图不加任何交互（无 lightbox、无 hover 放大）；交互形态规则由交互编写技能承载
2. 投影可读性：合成后按 50% 缩放自检，截图内关键文字必须可读；不可读时截关键区域做局部放大或拆面板，不整图硬缩
3. 敏感信息：账号、头像、项目名等在合成前遮盖——用实色块 + hairline 描边，不用模糊渐变
4. 导出链路：合成产物是 PNG 资产，随页面 HTML 被截图/转 PPT 消费，路径必须相对可解析

### 截图类型决策（PPT 简表）

| 素材 | 处理 |
|---|---|
| 平台/系统截图（素材图映射表内） | 程序化合成 + contain 上屏，不重画 |
| 长网页截图 | 截关键区域或拆 2-3 张同尺寸面板，单页素材 ≤4 张 |
| 极窄/极高截图 | spacious + 侧向 alignment；仍不可用再 AI 再设计 |
| 代码/配置截图 | 浅底合成，50% 缩放做文字可读性自检 |
| 概念性 UI 情景图 | AI 再设计（author 侧类型 6 / 瑞士 3 模板） |

### 配图 Prompt 应用

1. 类型选择跟随页面类型（模板编号与全文见 author 侧 `content-imagery-and-infographic.md`）：

| PPT 页面类型 | 模板选择 |
|---|---|
| 封面氛围背景 | 瑞士 1 / 类型 1（纪实照片），文字区域留白由 HTML 叠加标题 |
| 案例/故事页 | 类型 1（杂志风预设）或瑞士 1（瑞士风预设），按风格基调二选一 |
| 方案/功能页隐喻插图 | 类型 6 / 瑞士 3（UI 情景图）或隐喻插图 |
| 章节分隔 | 不生图——CSS 纯色/渐变（本文件既有规则） |
| 数据页 | 不用 AI 生图——程序化 SVG/HTML 图表走 Phase 3 管线（本文件既有规则） |

2. 后缀规格约束（比例、不画页面外壳、同组一致）每张必带；图内文字语言跟随 deck 语言
3. 封面配图遵循本文件"HTML/CSS 优先原则"：AI 只生成氛围背景图，标题 / CTA / 品牌标识由 HTML 叠加，不画进图
4. 信息承载类图（信息图 / 流程 / 对比）默认程序化构建；AI 整图生成模板仅在用户明确要求时使用

### 降级与审查联动

1. 截图合成是程序化环节，不依赖生图 API：无 API Key 时仅"截图再设计 / AI 配图"按本文件降级策略走 CSS/程序化路径，合成链路照常执行
2. 合成产物与配图随 Phase 4 页面审查：裸 img、截图被 cover 裁剪、同页混用容器比例 → 按 `robot-aiot-draw-flowchart/references/slide-premium-review.md` 口径判定阻塞项
3. Phase 5 交付清单核对：母稿素材图映射表引用的图片全部存在于 `doc-ppt/assets/`，页面相对路径可解析
