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
