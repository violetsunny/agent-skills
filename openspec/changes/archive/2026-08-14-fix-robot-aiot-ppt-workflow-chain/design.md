## Context

当前 `robot-aiot-leadership-ppt-workflow` 链路依赖三个外部 skill：`robot-aiot-draw-flowchart`（产出 XML）、`robot-aiot-xml-html-bridge`（XML→HTML）、`ppt-master`（HTML→PPTX）。

审查发现两个高严重度断裂：
1. `robot-aiot-xml-html-bridge` 只有方法论无实际转换机制——"确定性渲染路径"是空话
2. `ppt-master` 没有 HTML 输入路由（其生成路线是 SVG-based `svg_output/`），但 leadership workflow 声称"逐页 HTML 是 PPT 还原的第一参照物"

See proposal.md - Why for motivation.

## Goals / Non-Goals

**Goals:**
- 让 `robot-aiot-xml-html-bridge` 具备可执行的 XML→HTML 转换能力（样式映射 + 坐标驱动 + 保真校验）
- 修正 leadership workflow 对 `ppt-master` 的交接契约，从"HTML 是直接输入"改为"HTML 是视觉参照，agent 负责将 HTML 映射为 ppt-master 支持的 SVG 页面"
- 提供逐页 HTML 模板规范，减少 Phase 4 的手写不确定性
- 定义单一真源与重生顺序规则

**Non-Goals:**
- 不修改 `ppt-master` 技能本身——它的 SVG-based 生成路线是稳定的，不需要新增 HTML 路由
- 不开发独立的 HTML→PPTX 引擎——PPT 生成仍由 `ppt-master` 承担
- 不修改 `robot-aiot-draw-flowchart` 的核心能力——它只产 XML，不产 HTML

## Decisions

### D1: XML→HTML 转换采用 Python 脚本 + 样式映射表

**选择**: 在 `robot-aiot-xml-html-bridge/scripts/` 中放一个 `xml_to_html.py` 脚本，配合 `references/xml-html-mapping.md` 中的样式映射表。

**理由**: 
- draw.io XML 是结构化的 mxCell 树，Python 的 `xml.etree.ElementTree` 可稳定解析
- 样式映射表（mxCell style → CSS）是确定性的，不需要 AI 即兴发挥
- 脚本化保证可重复执行，每次 XML 变更后可一键重生 HTML

**替代方案**:
- 用 JS/draw.io embed 渲染器：引入浏览器依赖，环境复杂
- 让 agent 手工逐节点翻译：不可重复，漂移风险高

### D2: HTML→PPT 交接改为"HTML 作为视觉参照，agent 手工映射为 SVG"

**选择**: 修正 leadership workflow Phase 5，从"逐页 HTML 是 PPT 还原的第一参照物"改为"逐页 HTML 是视觉参照，agent 依据 HTML 的布局、配色、内容层级手工编写 ppt-master 的 SVG 页面"。

**理由**:
- `ppt-master` 的生成路线是 SVG-based（`svg_output/`），不接受 HTML 作为直接输入
- 用户确认"HTML 再生成 PPT 效果非常好"——这说明 HTML 作为视觉参照层确实有效，但执行路径是 agent 看 HTML 写 SVG，而不是 ppt-master 直接读 HTML
- 这不改变 ppt-master 的能力边界，只改变 leadership workflow 对交接方式的描述

**替代方案**:
- 新增独立 HTML→PPTX skill：过度工程，ppt-master 的 SVG 路线已足够好
- 给 ppt-master 加 HTML 路由：改动量大，且 ppt-master 不是我们的技能

### D3: 逐页 HTML 模板放在 leadership-ppt-workflow 的 references/ 中

**选择**: 在 `robot-aiot-leadership-ppt-workflow/references/page-html-template.md` 中定义五区域布局模板和 CSS 基础样式。

**理由**:
- 页面 HTML 模板是 leadership workflow 专属的，不是通用能力
- 放在 references/ 而非 scripts/，因为它是布局规范而非可执行脚本
- agent 按模板填内容，不需要脚本生成

### D4: 单一真源与重生顺序

**选择**: 定义明确的重生链——

```
数据池 MD 改动 → 母稿 MD 更新 → 图表 XML 重生 → 图表 HTML 重生 → 页面 HTML 重生
```

不允许跳步或只手改下游产物。每次重生后必须重跑交叉校验。

**理由**: 三层产物共存时，没有明确重生顺序会导致漂移——母稿改了数字但页面 HTML 没刷，或图表 XML 更新了但嵌入页里的 HTML 还是旧版。

### D5: 输出产物统一目录

**选择**: 所有输出产物（XML、MD、HTML、PPTX）统一放在当前运行项目的 `doc-ppt/` 目录下，不散落到 `doc/`、根目录或其他位置。

目录结构：
```
doc-ppt/
├── <chart-name>.xml            — 图表 XML（Phase 3）
├── <chart-name>.html           — 图表 HTML（Phase 3.5）
├── <project>_PPT母稿.md        — 母稿（Phase 4）
├── pages/                      — 逐页 HTML（Phase 4）
│   ├── 01-cover.html
│   └── ...
└── <project>.pptx              — 最终 PPTX（Phase 5）
```

**理由**:
- 产物分散在 `doc/`、根目录等多个位置会导致"找不到文件"
- `doc-ppt/` 作为唯一输出根目录，一眼可见全部产物
- 与项目其他文档（`doc/`）分离，不混淆

**替代方案**:
- 继续用 `doc/`：与项目其他文档混放，产物不清晰
- 每个阶段独立目录：过度拆分，增加路径管理负担

## Risks / Trade-offs

- **[Python 脚本环境依赖]** → 脚本仅用标准库 `xml.etree.ElementTree`，不引入第三方依赖。若目标环境无 Python，agent 可按 `references/xml-html-mapping.md` 手工映射作为降级路径
- **[HTML→SVG 手工映射的主观性]** → agent 依据 HTML 写 SVG 时可能引入偏差。通过 Phase 5 移交后验证清单（每页 PPT 布局与对应 HTML 基本一致）来捕获偏差
- **[样式映射表不完整]** → draw.io style 属性可能存在映射表未覆盖的值。脚本 MUST 跳过未知属性并记录警告，不阻塞转换
- **[页面 HTML 模板可能过于刚性]** → 五区域固定布局可能不适合所有页面类型（如全图页、对比页）。模板 MUST 声明哪些区域可隐藏，允许 agent 按页面类型裁剪

## Open Questions

- `xml_to_html.py` 是否需要支持 draw.io 的 compressed XML 格式（`mxfile` 的 `compressed="true"` 属性）？当前假设输入是未压缩的明文 XML。若需要支持压缩格式，需引入 `deflate` 解压逻辑
