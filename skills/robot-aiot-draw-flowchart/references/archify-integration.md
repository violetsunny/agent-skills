# Archify Integration Reference

## 输出路径选型指南

本 SKILL 有两条互补输出路径：

| 维度 | draw.io XML（主路径） | archify HTML/SVG（高保真路径） |
| --- | --- | --- |
| 产物 | .drawio / .xml 可编辑文件 | 自包含 HTML（内联 SVG） |
| 适用 | 需要二次编辑、进入 PPT 工作流（robot-aiot-xml-html-bridge）、团队协作修改 | 汇报展示、README 嵌入、需要主题切换或高分辨率导出 |
| 主题 | 无 | 暗/亮主题切换（localStorage + prefers-color-scheme） |
| 导出 | 依赖 draw.io | 内置菜单：PNG 剪贴板、PNG/JPEG/WebP（最高 4x）、双主题 SVG |
| 校验 | 本 SKILL §6 自审清单 | archify 渲染器 fail-fast 校验（重叠/标签碰撞/越界） |

**决策规则：**
1. 用户要求可编辑或进 PPT 工作流 → draw.io XML
2. 用户要求汇报展示/README/主题/导出 → 委托 archify
3. 未明确时默认 draw.io XML（主路径）

## 图表类型 → archify 渲染模式映射

| 本 SKILL 图表类型 | archify 模式 | 说明 |
| --- | --- | --- |
| 分层架构图 | architecture | 层容器 → boundaries(region)，组件 → components |
| 线性/分支/循环/并行/泳道流程图 | workflow | 泳道 → lanes，阶段 → phases，并行 → groups |
| 调用链/交互序列 | sequence | 角色 → participants，消息 → messages |
| 数据管道/ETL/数据流 | dataflow | 阶段 → stages，流 → flows（含 classification） |
| 状态机/OTA 生命周期 | lifecycle | 状态 → states（start/active/waiting/success/failure） |

## Mermaid 输入方言委托

用户粘贴 Mermaid 代码时，不机械解析，读取其拓扑与语义后按 archify 映射重排：
- `flowchart/graph` → workflow（组件图则 architecture）；`subgraph` → lane/region；`{}` 菱形 → 决策节点
- `sequenceDiagram` → sequence；`-->>` → return 变体；`Note` → message note
- `stateDiagram` → lifecycle；`[*]` → start/terminal
- 丢弃 Mermaid 样式（classDef/style），仅保留拓扑与语义

## 委托步骤

1. 按映射表确定 archify 模式，读取 archify 的 `schemas/<type>.schema.json` 与对应 `examples/*.<type>.json`
2. 编写 `<name>.<type>.json`（布局遵循 archify 布局预算与叙事原则）
3. 渲染：`node bin/archify.mjs render <type> <input>.json <output>.html`（路径相对 archify SKILL 目录）
4. 校验：`node bin/archify.mjs validate <type> <input>.json --json`；已有 HTML 用 `node bin/archify.mjs check <output>.html`
5. 校验失败时按输出的 Suggested fix 修正 JSON 后重跑，不得手改渲染器或生成的 HTML

**环境自检：** `node bin/archify.mjs doctor`；不可用时降级为 draw.io XML 主路径并告知用户。

## 主题兼容约束（硬性）

1. **CSS class 颜色系统** — SVG 形状一律使用 `c-<type>` / `t-<type>` class，不得硬编码 `fill="#…"` / `stroke="#…"`（模板自身 defs 除外）
2. **双矩形模式** — 每个 `c-<type>` 矩形前必须有同几何的 `c-mask` 不透明矩形
3. **箭头先于组件** — 文档顺序中箭头在组件矩形之前绘制
4. **保留交互块** — `.toolbar`、`<script>`、`:root` / `[data-theme]` CSS 不得改动（即主题切换与导出菜单本体）
5. 交付前按 archify 自审清单核对：viewBox 余量 ≥20px、图例在所有 boundary 之下
