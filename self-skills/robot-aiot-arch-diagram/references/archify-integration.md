# Archify 运行时渲染器（路径 C）

archify 渲染引擎由**运行时部署**的 archify skill 提供（`~/.agents/skills/archify`，仅需 node ≥ 18），本 SKILL 不内嵌引擎副本。

约定：`$SKILL_ROOT` = 本 SKILL 目录；`$ARCHIFY_ROOT` = `$HOME/.agents/skills/archify`；`$ARCHIFY` = `$ARCHIFY_ROOT/bin/archify.mjs`。

## 输出路径选型指南

本 SKILL 有两条输出路径：直绘 SVG/HTML（B，主路径，见 SKILL.md「生成工作流 · 路径 B」）、archify 运行时渲染（C）；不含可编辑 draw.io XML 路径（路径 A）。B/C 对比表与决策规则以 SKILL.md「输出路径选型」为唯一权威，此处不复述。

archify 产物为自包含 HTML（内联 SVG），带暗/亮主题切换（localStorage + prefers-color-scheme）与导出菜单（PNG 剪贴板、PNG/JPEG/WebP 最高 4x、双主题 SVG），交付前必须通过 archify fail-fast 校验（重叠/标签碰撞/越界）。

## 图表类型 → archify 类型路由

| 本 SKILL 图表类型 | archify 类型 | 说明 |
| --- | --- | --- |
| 分层架构图 | architecture | 层容器 → boundaries(region)，组件 → components |
| 线性/分支/循环/并行/泳道流程图 | workflow | 泳道 → lanes，阶段 → phases，并行 → groups |
| 调用链/交互序列 | sequence | 角色 → participants，消息 → messages |
| 数据管道/ETL/数据流 | dataflow | 阶段 → stages，流 → flows（含 classification） |
| 状态机/OTA 生命周期 | lifecycle | 状态 → states（start/active/waiting/success/failure） |

## 快速创作流程（6 步）

1. **定类型**：按上表路由；不确定时 `node $ARCHIFY guide <场景> --lang zh`。
2. **读契约**：读 `$ARCHIFY_ROOT/schemas/<type>.schema.json` + `$ARCHIFY_ROOT/schemas/common.schema.json` + 至少一个 `$ARCHIFY_ROOT/examples/*.<type>.json`。
3. **写候选**：产出 `<name>.<type>.json`。主节点 ≤ 12；`quality_profile: "showcase"`；布局遵循布局预算与叙事原则；语言与用户一致；品牌图标显式声明（`node $ARCHIFY brands <关键词>` 查询）。
4. **校验**：每次编辑后必跑 `node $ARCHIFY validate <type> <候选.json> --quality showcase --json`。showcase 档 = 9 项产物检查，必须 0 errors 0 warnings；失败按输出的 Suggested fix 修正 JSON 重跑，**不得手改渲染器或生成的 HTML**。
5. **交付**：`node $ARCHIFY deliver <type> <候选.json> <输出.html> --json`（冻结 spec 快照、原子写入、输出 SHA-256 回执）。非零退出不得声称成功。
6. **视觉检查**：`node $ARCHIFY visual-check <输出.html> --json`。退出码：0=通过，1=溢出/截图失败，2=无 Chromium（跳过）。恒报 `visualReview: "pending"`——工具不做视觉裁决，向用户如实报告。

## 创作不变量摘要

- `visual_preset`、`subtitle`、`legend` 默认省略，确有需要才加
- 关系标签是语义数据（描述流向/协议/因果），不是装饰
- 组件类型：frontend / backend / database / cloud / security / messagebus / external；变体：default / emphasis / security / dashed
- 自动布线端点遵循侧契约（top/bottom/left/right），避免连线交叉
- 增量修改用 `node $ARCHIFY compare architecture <base.json> <head.json>` 生成差异视图

## Mermaid 输入方言映射

用户粘贴 Mermaid 代码时，不机械解析，读取其拓扑与语义后按类型路由重排：
- `flowchart/graph` → workflow（组件图则 architecture）；`subgraph` → lane/region；`{}` 菱形 → 决策节点
- `sequenceDiagram` → sequence；`-->>` → return 变体；`Note` → message note
- `stateDiagram` → lifecycle；`[*]` → start/terminal
- 丢弃 Mermaid 样式（classDef/style），仅保留拓扑与语义

## 主题兼容约束（仅限手工改模板的降级路径，硬性）

正常流程产物由 `deliver` 生成，无需手改。仅当用户明确要求手工调整模板时才适用：

1. **CSS class 颜色系统** — SVG 形状一律使用 `c-<type>` / `t-<type>` class，不得硬编码 `fill="#…"` / `stroke="#…"`（模板自身 defs 除外）
2. **双矩形模式** — 每个 `c-<type>` 矩形前必须有同几何的 `c-mask` 不透明矩形
3. **箭头先于组件** — 文档顺序中箭头在组件矩形之前绘制
4. **保留交互块** — `.toolbar`、`<script>`、`:root` / `[data-theme]` CSS 不得改动（即主题切换与导出菜单本体）
5. 交付前按自审清单核对：viewBox 余量 ≥20px、图例在所有 boundary 之下

## 环境自检与降级

- 自检：`node $ARCHIFY doctor`；示例一览：`node $ARCHIFY examples`；本地演示：`node $ARCHIFY demo <目录>`
- node 不可用或 doctor 失败时：降级为直绘 SVG/HTML（B），并如实告知用户降级原因；需要可编辑 XML 时如实告知本 SKILL 不具备该能力

## 如实交付报告

交付后向用户报告：产物路径、SHA-256 回执、validate 结果（0 errors/0 warnings）、visual-check 状态（通过/跳过/待人工复核）。不得隐瞒跳过的检查。
