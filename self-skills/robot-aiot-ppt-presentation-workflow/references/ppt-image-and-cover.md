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

本节定义截图素材与 AI 配图如何进入 PPT 母稿流程（Phase 1 素材盘点 → Phase 4 页面 HTML）。

- 图片上屏原语（`.img-frame` 容器、contain/cover 选型、素材平铺与体积控制、scrim 边界）→ `robot-aiot-draw-flowchart/references/slide-image-framing.md`
- 截图取景规范与配图 Prompt 模板由本文件自包含，见下方各节

### 截图资产化链路

1. **Phase 1 盘点**：素材图清单记录来源路径、内容类型（网页 / App / 代码 / dashboard / 设计稿）、处理目标（保真 / 统一美化 / 再设计）
2. **Phase 4 前合成**：逐张确定取景 7 参数 → 程序化合成（目标比例画布 + 统一背景 + 截图等比放入）→ 落 `doc-ppt/assets/`，命名 `{页号}-{语义}.png`
3. **上屏**：按 `slide-image-framing.md` 走 `.img-frame` 容器；截图 / UI / 文字密集图一律 contain，场景照片与 AI 氛围图 cover
4. **母稿联动**：合成产物写回母稿素材图映射表（页面 | 素材图 | 用途）；Phase 4 按表盘点，表中素材必须上屏，不得静默忽略

### 取景 7 参数定义

每张截图处理前先确定：

| 参数 | 可选值 | 判断方式 |
|---|---|---|
| `ratio` | 21:9 / 16:10 / 16:9 / 4:3 / 1:1 | 跟随页面版式图片槽位，不跟随原截图比例 |
| `background` | plain / gradient / wallpaper / blurred / grid / paper | 跟随母稿头部锁定的风格基调 |
| `padding` | compact / standard / spacious | 普通截图 standard；文字密集或高图 spacious；小图组 compact |
| `inset` | none / subtle / balanced | 截图需从背景中浮出用 balanced；瑞士风预设多用 none/subtle |
| `shadow` | none / soft / editorial | 杂志风预设可 soft/editorial；瑞士风预设默认 none |
| `corners` | square / small / medium | 瑞士风预设 square；杂志风预设 small/medium |
| `alignment` | center / top-left / top-right / bottom-left / bottom-right | 跟随页面构图，不永远居中 |

### 风格映射（两种风格预设）

**杂志风预设**：背景 paper / blurred / 低饱和 gradient；纸张、墨水、胶片颗粒、暖白、低对比质感；截图可小圆角 + 轻微阴影，但不做成 SaaS 营销卡片。推荐语义：

```text
ratio:16:10, background:paper, padding:standard, inset:balanced, shadow:editorial, corners:small, alignment:center
```

**瑞士风预设**：背景 plain / grid / dot-matrix；accent 只允许极低占比，无大面积亮色块；截图直角、无阴影、无圆角，少量 hairline 或顶部 accent 线。推荐语义：

```text
ratio:21:9, background:grid, padding:standard, inset:subtle, shadow:none, corners:square, alignment:center
```

### 背景强度规则

截图背景是托底，不是主视觉：

1. `alignment` 不确定时，背景中心与四角都必须安静；截图放某角时该角不得有强色块
2. accent 只做 5%-8% 视觉占比的淡线、点阵或极浅几何场；禁高亮色条、大色块、霓虹渐变
3. 背景不得含文字、logo、图标、人物、设备、边框、明显主体或方向性构图
4. 背景必须 crop-safe：裁成 21:9 / 16:10 / 4:3 / 1:1 都不暴露被裁痕迹
5. 背景资产按 1920×1080 级 16:9 预生成后程序化 cover 裁到各槽位；同一 PPT 复用同一套背景，不每张截图临时生成

### 7 参数 PPT 默认值速查

| 参数 | PPT 默认 | 差异说明 |
|---|---|---|
| `ratio` | 由页面版式槽位决定（见下方适配表） | 页面画布恒 16:9，槽位比例 ≠ 页面比例 |
| `background` | 品牌色浅场 / paper / grid，全 PPT 统一一套 | 取自品牌资产（`brand-assets.md`）与母稿头部锁定的风格基准，预生成复用 |
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

### PPT 交付纪律

1. 静态交付：截图不加任何交互（无 lightbox、无 hover 放大）
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
| 概念性 UI 情景图 | AI 再设计（本文件类型 6 / 瑞士 3 模板） |

### 配图 Prompt 应用

1. 类型选择跟随页面类型（模板全文见下方"配图 Prompt 模板"）：

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

### 配图 Prompt 模板

#### 使用边界（先读）

1. 信息承载类图（信息图、流程图、关系图、数据图）默认程序化 SVG/HTML 构建——走 Phase 3 图表管线；AI 生图默认只做氛围照片、隐喻插图、UI 情景图
2. 信息承载类整图 AI 生成仅在用户明确要求时使用；此时图内文字必须短标签，并在 prompt 中指定语言
3. 走 AI 生图时下方通用规则与后缀约束必带

#### 通用规则

- 先判定 deck 风格预设：杂志风预设（纸张质感、胶片颗粒、暖白低对比）/ 瑞士风预设（12/16 列网格、无衬线气质、单一高饱和 accent、直角纯色、发丝线、极大留白）
- 瑞士风预设配图只用黑白灰 + 主题唯一 accent，禁渐变、阴影、圆角、霓虹、3D、卡通；21:9 图核心主体落在中央 70% 安全区
- 图内文字语言跟随 deck 语言：中文 deck 用中文，英文 deck 用英文
- 不生成卡通、3D、霓虹科技感、SaaS 模板感、过度装饰、假 logo
- 给标题/正文留可叠加空间，不满屏堆细节；同组图必须同比例、同视觉缩放、同边距密度
- 配图是嵌入素材不是独立页面：不生成页眉、页脚、页码、标题栏、角标、署名、装饰边框等页面外壳
- 生成图落 `doc-ppt/assets/`，命名 `{页号}-{语义}.{ext}`，不外链

#### 后缀约束（每张必带）

```text
输出必须是[16:9/16:10/4:3/3:2]横向构图，主体居中但保留边距，画面密度中等，与同组图片保持相同视觉缩放和边距。只保留核心图形/画面本身，不要生成页眉、页脚、标题、页码、角标、署名、装饰边框、超长条、竖图或不规则比例。
```

同页多图时追加：

```text
这是一组图片中的一张，请保持与同组图片相同的画面比例、元素大小、边距、线条粗细和标注密度。
```

#### 类型 1 · 人文纪实照片（现场感、真实世界锚点）

```text
生成一张横向纪实摄影配图，主题是：[页面概念]。经典胶片纪实摄影质感：自然光、低饱和、轻微颗粒、真实工作或生活现场，克制有人文温度。适合杂志风页面，留出标题空间。不要商业摆拍、科幻界面、AI 机器人、logo 或水印。[接后缀约束]
```

#### 类型 6 · 截图再设计 / UI 情景图

```text
生成一张横向 UI 情景图，把[截图/界面/工作区内容]再设计成适合杂志风页面的视觉。保留真实产品工作流的感觉，使用纸张底色、细线框、网格、少量标注和克制阴影。图中文字使用[中文/英文]，短而清晰。不要真实品牌 logo、花哨 dashboard、霓虹渐变或过度拟物。输出必须是 16:10 横向构图。[接后缀约束]
```

#### 瑞士 1 · 纪实照片 / 案例主图（顶部横幅）

```text
生成一张 21:9 超宽横向纪实摄影配图，主题是：[页面概念]。Swiss editorial documentary 风格：高对比、低饱和、冷静克制、真实办公/城市/产品使用场景，构图有大量负空间，主体位于中央 70% 安全区，适合瑞士国际主义页面顶部横幅。不要 AI 机器人、科幻界面、商业摆拍、logo、水印或文字。只保留核心照片本身，不要页面外壳。
```

#### 瑞士 3 · 截图再设计 / UI 情景图

```text
生成一张横向 UI 情景图，把[截图/界面/工作区内容]再设计成 Swiss International Typographic Style。极简 dashboard/workspace 结构，直角面板、发丝线、12 列网格、少量[主题 accent]强调色，无阴影无圆角。图中文字使用[中文/英文]，短而清晰，不要真实品牌 logo。输出必须是 16:10 横向构图，视觉密度中等，适合 contain 展示。只保留核心 UI 画面本身，不要页面外壳。
```

### 降级与审查联动

1. 截图合成是程序化环节，不依赖生图 API：无 API Key 时仅"截图再设计 / AI 配图"按本文件降级策略走 CSS/程序化路径，合成链路照常执行
2. 合成产物与配图随 Phase 4 页面审查：裸 img、截图被 cover 裁剪、同页混用容器比例 → 按 `robot-aiot-draw-flowchart/references/slide-premium-review.md` 口径判定阻塞项
3. Phase 5 交付清单核对：母稿素材图映射表引用的图片全部存在于 `doc-ppt/assets/`，页面相对路径可解析
