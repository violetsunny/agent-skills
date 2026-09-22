# 导出 block 注册表（`--registry`）

为可追溯 block 分解图的 `data-block-*` 元数据产出机器可读的 `.registry.json` sidecar。**仅限用户明确要求——绝不主动执行，且只在 `--registry` 时执行。**

## 触发条件

以下情况加载本文件：

- 用户要求导出图表 HTML 文件的 block registry——导出请求的 `--registry` 形式（单独使用，或与 `--svg-only`/`--png-only`/`--scale`/`--output` 组合）。
- 用户用自然语言索要可追溯 block 分解图（见 [`semantic-patterns.md` § 8](semantic-patterns.md)）背后的 block 元数据、ID 列表、registry 或可追溯数据，且要结构化数据而非图片。

本文件只管辖 `--registry`。SVG/PNG 光栅化是独立流程——见 [`export.md`](export.md)。两者可在同一次命令调用中运行，但不共享任何逻辑；把本流程当作独立流程，不是那个流程的扩展。

## 范围

registry 只捕获源 HTML `data-block-*` 属性中已书写的内容（定义见 [`semantic-patterns.md` § 8](semantic-patterns.md)）——不多不少。它是**投影，不是第二真源**：JSON 中每个值都必须能追溯到文件中字面存在的属性值。本流程绝不从图表文本、节点位置或自身判断去推断、概括或补充 block 记录。

只适用于使用可追溯 block 分解模式的图（携带 `data-block-id` 的 Tree 节点）。其他任何图——包括未用该模式的普通 Tree 图——没有 block 可提取；见*边界情况*。

## JSON schema

```json
{
  "source": "example-tree-block-decomposition.html",
  "blocks": [
    {
      "id": "PAY-001",
      "name": "Payment Gateway",
      "output": "Settled transaction record",
      "constraint": "Every transaction reaches exactly one terminal state",
      "impl": "src/payments/gateway/"
    },
    {
      "id": "PAY-001-01",
      "parent": "PAY-001",
      "name": "Card Authorization",
      "input": "Raw card details from checkout",
      "output": "Authorization token or decline",
      "constraint": "Never persists a raw card number",
      "assumption": "Runs behind the PCI-scoped boundary",
      "impl": "src/payments/authorization/"
    }
  ]
}
```

- `source` — 生成 registry 所用 HTML 文件的 basename。
- `blocks` — 每个携带 `data-block-id` 的节点一条，按文档顺序：即匹配节点在源文件中出现的顺序，绝不按 parent 重排。逐行书写的树（先全部 Tier 1 节点，再全部 Tier 2 节点）按该行序导出；只有深度优先书写的树才按深度优先导出。
- `id`、`name` — 恒存在；该模式要求每个 block 都有这两个属性。
- `parent` — 仅非根 block 存在，与 `data-block-parent` 自身"缺省即根"的约定一致。根 block 省略该键，绝不写 `null`。
- `input`、`output`、`constraint`、`assumption`、`impl` — 仅当节点上存在对应 `data-block-*` 属性时才出现。整键省略，而不是写空字符串。

不允许其他键，也不写生成时间戳：registry 的设计用途是按需重生成并在版本控制中 diff，实时时钟字段会让相同源的两次运行产出不同结果。出处与日期来自 git 历史，不来自文件自身内容。

## 流程

1. 读取源 HTML 文件。
2. 找出所有携带 `data-block-id` 属性的元素。没有该属性的节点不属于本模式——静默跳过，包括在模式与非模式 Tree 节点混用的图中。
3. 对每个匹配节点，读取 `data-block-id`、`data-block-parent`、`data-block-name`、`data-block-input`、`data-block-output`、`data-block-constraint`、`data-block-assumption`、`data-block-impl`——存在哪个读哪个。`data-block-name` 映射为 JSON 键 `name`；其余去掉 `data-block-` 前缀映射。
4. 属性值原样保留——除首尾空白外不 trim、不改大小写、不重排 `impl` 路径格式。
5. 按上文 *JSON schema* 定义，以文档顺序组装 `blocks` 数组。
6. 写入源文件同目录的 `<basename>.registry.json`（如 `example-tree-block-decomposition.html` → `example-tree-block-decomposition.registry.json`）。用户给父级导出命令传了显式 `--output` 路径则遵从。

## 边界情况

- **源中没有任何 `data-block-id` 属性**：拒绝并告知用户；不要写空的 `{"blocks": []}` 文件。这很可能是对根本未用该模式的图请求了 `--registry`——照实说。
- **`data-block-id` 值重复**：按文档顺序输出每条匹配项；不去重、不择一。重复 ID 是 `scripts/verify-block-registry.py` 要抓的正确性问题，不该由导出静默消化。
- **`data-block-parent` 指向文件中不存在的 ID，或 parent 成环**：按书写原样输出，包括坏引用或环。理由同重复 ID——导出镜像源；`scripts/verify-block-registry.py` 才是结构检查，运行它是独立的显式步骤，`--registry` 本身不隐含它。
- **源为多图 gallery HTML**（多图 gallery 源，用户源文件，不随 skill 分发）：拒绝，同 SVG/PNG 路径的处理——询问用户具体指哪个图表文件。
- **`--registry` 与 `--svg-only` 或 `--png-only` 组合**：输出相互独立——在请求的光栅/矢量格式之外额外产出 registry JSON。`--registry` 与 `--scale` 无交互；它不产出图像。

## 绝不做的事

- 校验 ID 唯一性、parent 可解析性或环。那是 `scripts/verify-block-registry.py` 的职责——作为独立步骤运行，导出不隐含它。
- 把 block 元数据与其绘制位置或连线几何做关联。完全在 registry 范围之外，不是"暂缓"——JSON 是元数据投影，不是几何审计。
- 写生成时间戳、工具版本，或任何非字面来源于 `data-block-*` 属性的字段。
- 修改源 HTML。
- 未显式传 `--registry` 时自动产出 `.registry.json`。与 SVG/PNG 导出一样，每次都必须用户明确要求。
