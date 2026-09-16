# 内容AI图像生成与信息图

## 定位

为 Web 演示页面生成内容配图、信息图和社交媒体风格的可视化卡片，增强信息的视觉传达力。

## 内容配图规则

### 何时需要配图

1. 抽象概念需要具象化（如"边缘计算"→设备+云的示意图）
2. 数据关系需要空间表达（如对比、流程、层级）
3. 纯文字段落超过 5 行且包含可视觉化的信息
4. 页面需要视觉节奏变化（打破纯文字的单调感）

### 配图风格选择

| 内容类型 | 推荐风格 | 说明 |
|---------|---------|------|
| 技术架构 | 等距/扁平图标 | 与架构图风格一致 |
| 数据对比 | 信息图卡片 | 大数字+标签+趋势 |
| 流程说明 | 步骤图/时间线 | 编号+图标+简述 |
| 概念解释 | 隐喻插图 | 用日常事物类比 |
| 案例展示 | 场景图/截图 | 真实或模拟的使用场景 |

## 信息图布局（21种）

按数据类型选择：

| 数据类型 | 推荐布局 |
|---------|---------|
| 单一指标 | Big Number / Metric Card |
| 多指标对比 | Dashboard Grid / Comparison Bar |
| 时间序列 | Timeline / Milestone Strip |
| 层级关系 | Pyramid / Nested Circles / Tree |
| 占比构成 | Donut / Treemap / Stacked Bar |
| 流程/步骤 | Step Flow / Swimlane / Pipeline |
| 地理分布 | Map Overlay / Region Cards |
| 评分/雷达 | Radar / Score Matrix |
| 列表/排名 | Ranked List / Leaderboard |
| 引用/证言 | Quote Card / Testimonial |

## 社交媒体图片样式（小红书/微信风格）

当演示需要导出为社交分享图时：

### 12种预设样式

Cover / Carousel / Quote / Data Card / Checklist / Tutorial / Comparison / Timeline / Profile / Event / Product / Minimal

### 尺寸规范

- 小红书：1080×1440（3:4）或 1080×1080（1:1）
- 微信公众号封面：900×383（2.35:1）
- 朋友圈：1080×1080（1:1）

### 配色方案

支持 3 种 palette 预设 + 自定义，确保与演示主色一致。

## AI 图像生成集成

### Provider 优先级

Google → OpenAI → Azure → OpenRouter → DashScope → Z.AI → MiniMax → Replicate → Jimeng → Seedream → Agnes

codex-cli 永不自动选择。

### 使用边界

- AI 生图仅用于氛围/背景/隐喻插图
- 数据图表必须程序化生成，不用 AI
- prompt 不含文字，文案后期叠加
- 用户未要求时不主动使用

## 无 API Key 降级策略

当环境中未配置任何图像生成 API Key 时：

1. **不阻塞主流程** — AI 图像生成是可选增强能力，缺失时自动降级
2. **配图降级为 SVG/CSS 构建** — 用内联 SVG 图标、CSS 渐变、几何图形组合替代 AI 插图
3. **信息图保持程序化** — 信息图本身即为 HTML/CSS/SVG 构建，不受影响
4. **提示用户** — 输出 `[NO-AI-IMAGE] 未检测到图像生成 API Key，配图已降级为 SVG/CSS 构建`
5. **不尝试调用外部服务** — 跳过 AI 生图步骤，直接使用程序化方案

检测方式：检查环境变量中是否存在以下任一 Key：`GEMINI_API_KEY`、`OPENAI_API_KEY`、`AZURE_OPENAI_API_KEY`、`DASHSCOPE_API_KEY`、`MINIMAX_API_KEY`、`REPLICATE_API_TOKEN`。全部缺失即触发降级。

## 约束

1. 配图服务于内容理解，不是装饰
2. 信息图数据必须来自 Phase 1 数据池，可溯源
3. 社交图片是演示的衍生输出，不是主要交付物
4. 所有配图需通过高级感审查（`premium-review-fix.md`）
5. 无 API Key 时必须降级，不得虚构生成结果或静默跳过
