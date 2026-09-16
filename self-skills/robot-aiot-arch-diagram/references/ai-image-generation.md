# AI 图像生成能力

## 定位

当架构图/技术图表需要以 AI 生成的高清图片形式输出时，使用本规则。区别于 SVG/PNG 程序化导出，本能力通过 AI 图像模型生成具有设计感的视觉作品。

## 适用场景

1. 架构图需要作为封面图、Banner 或社交媒体配图
2. 需要将技术概念转化为具象化的视觉隐喻
3. 程序化渲染无法满足视觉品质要求时
4. 需要生成与架构图配套的插图/背景图

## Provider 自动选择优先级

Google → OpenAI → Azure → OpenRouter → DashScope → Z.AI → MiniMax → Replicate → Jimeng → Seedream → Agnes

codex-cli 永不自动选择。

## Quality 预设

- **normal** = 1K 快速预览
- **2k** = 2K 封面/插图（默认）

## 核心规则

### Reference-Image 身份保持

用简短硬编码语言："Use the person/object in the reference image(s) as the same identity"。禁止长描述导致模型合成新人物。

### Batch 模式

prompt 文件保存后优先 batch 而非 subagent；每图最多 3 次重试。

### Model 解析优先级

CLI > EXTEND.md > env > built-in default

### 脚本入口

- 单图：`{baseDir}/scripts/main.ts`
- Batch：`{baseDir}/scripts/build-batch.ts`

## 与程序化导出的区别

| 维度 | 程序化导出（PNG/SVG） | AI 图像生成 |
|------|---------------------|-----------|
| 精确性 | 像素级精确 | 风格化表达 |
| 可编辑性 | 可回溯修改 | 一次性产出 |
| 适用 | 技术文档、工程交付 | 封面、Banner、社交配图、视觉隐喻 |
| 数据保真 | 100% | 需人工校验 |

## 无 API Key 降级策略

当环境中未配置任何图像生成 API Key 时：

1. **不阻塞主流程** — AI 图像生成是可选增强能力，缺失时自动降级
2. **降级为程序化渲染** — 使用本 SKILL 已有的 SVG/PNG 导出管线（`generate-diagram.sh` / `png-export.md`）替代
3. **降级为 CSS 视觉构建** — 用 CSS 渐变、几何图形、排版组合构建封面/配图，不依赖外部服务
4. **提示用户** — 输出 `[NO-AI-IMAGE] 未检测到图像生成 API Key，已降级为程序化渲染/CSS 视觉构建`
5. **不尝试调用脚本** — `{baseDir}/scripts/main.ts` 等脚本在无 Key 时不可用，跳过而非报错

检测方式：检查环境变量中是否存在以下任一 Key：`GEMINI_API_KEY`、`OPENAI_API_KEY`、`AZURE_OPENAI_API_KEY`、`DASHSCOPE_API_KEY`、`MINIMAX_API_KEY`、`REPLICATE_API_TOKEN`。全部缺失即触发降级。

## 约束

1. AI 生成的图片不得替代程序化图表作为技术真源
2. 生成结果必须人工校验数据准确性
3. prompt 不含文字/字母，文案在后期叠加
4. 仅用于增强视觉表达，不承载事实信息
5. 用户未明确要求时不主动使用 AI 生图
6. 无 API Key 时必须降级，不得虚构生成结果或静默跳过

## 与出版级示意图迭代流程的分工

本文件约束风格化视觉输出（封面/Banner/插图/视觉隐喻）：prompt 不含文字、不承载事实信息、不替代程序化图表。需要带标签、承载事实、必须通过「生成 → 质量审查 → 低于阈值定向重生成」循环的出版级科学/技术示意图，按 `scientific-schematic-iteration.md` 执行；两套能力目标不同，不互相替代。
