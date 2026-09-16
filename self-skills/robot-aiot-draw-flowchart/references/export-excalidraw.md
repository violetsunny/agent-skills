# Mermaid → Excalidraw / SVG / PNG 离线三件套导出

从 Mermaid 源码（或图表描述先写成 Mermaid 源码）离线产出三件套交付物的完整流程规则。全程不依赖 CDN、不发起网络请求。

## 交付物定义

每次导出产出三件套，缺一即不算完成：

| 产物 | 用途 |
|---|---|
| `<slug>.mmd` | Mermaid 源码——机器友好的交换格式，**唯一事实源** |
| `<slug>.excalidraw` | 可编辑场景文件——在 excalidraw.com（File → Open）打开后可继续手工编辑 |
| `<slug>.svg` + `<slug>.png` | SVG 供文档嵌入（矢量清晰），PNG 供聊天/Issue/README（位图通用） |

## 硬约束

1. **离线契约**：渲染全程使用本地渲染页/本地依赖包。渲染环境缺失时停下报告构建/安装命令，**禁止退回 CDN 或在线服务**。
2. **不渲染不交付**：只有 `.mmd` 文件不构成图表交付。无法渲染时如实说明并停止，不交付未验证的产物。
3. **`.mmd` 是唯一事实源**：内容修改一律改 `.mmd` 后重渲染；`.excalidraw` 的手工编辑不回写 Mermaid。
4. **可编辑性边界**：Mermaid→Excalidraw 官方转换器只稳定支持 flowchart 类（`graph LR` / `graph TD` / `flowchart`）。sequenceDiagram、stateDiagram、gantt 等其他类型可正常渲染 SVG/PNG，但跳过 `.excalidraw` 产物，并必须明确告知用户："该类型可渲染但暂不可 excalidraw 编辑（上游转换器限制，flowchart 可以）。"

## Step 1 — 撰写 Mermaid 源码

- 语法与类型选择遵循 [mermaid-authoring.md](mermaid-authoring.md)。
- 目标是可编辑场景时优先 flowchart：管线/流向用 `graph LR`，层级用 `graph TD`。
- 节点标签短，细节放边标签；5–15 个节点是可读区间，超出就拆成多张图并说明原因。
- 输出目录：当前目录在 git 仓库内用 `./diagrams/`（产物可随仓库提交），否则用 `/tmp/diagrams/`。
- `<slug>` 从图表主题派生：kebab-case，≤40 字符。

## Step 2 — 准备离线渲染环境（每会话一次）

渲染环境是一个本地 HTML 渲染页，打包了 Mermaid、Mermaid→Excalidraw 转换器、SVG 序列化与光栅化工具，并向 `window` 暴露四个入口函数：

| 入口 | 签名 | 作用 |
|---|---|---|
| `__renderMermaid` | `(id, mermaidSrc) → Promise<svgString>` | Mermaid 源码 → SVG |
| `__rasterize` | `(svgString, widthPx) → Promise<pngBlob>` | SVG → 指定宽度 PNG |
| `__mermaidToExcalidraw` | `(mermaidSrc) → Promise<sceneJson>` | Mermaid 源码 → .excalidraw 场景 JSON |
| `__excalidrawToSvg` | `(sceneJson) → Promise<svgString>` | 编辑后的场景 → SVG（往返导出用） |

准备规则：

1. 按固定候选路径探测渲染页文件；找不到即输出 `BUNDLE_MISSING` 与构建命令，停止（见硬约束 1）。
2. 将渲染页复制为**内容寻址**的暂存副本（如 `/tmp/diagram-render-<sha256前16位>.html`）：哈希一致直接复用，不一致先写临时文件再原子 `mv`。并发会话与不同版本互不覆盖。
3. 用无头浏览器（或等价的本地浏览器自动化）打开暂存副本，等待页面就绪标记（如 `#done` 元素）后记录 tab 句柄。
4. 后续所有页面内 JS 调用、等待、关闭操作都必须显式带上该 tab 句柄，避免误中共享浏览器实例里的其他标签页。
5. 渲染 tab 在本轮图表工作全部结束后才关闭，不在两张图之间反复开关。

## Step 3 — 渲染三件套

先用写文件工具把 Mermaid 源码落到 `<outdir>/<slug>.mmd`，再驱动渲染页。

**源码传入必须走 base64**：渲染页无法读本地文件，把源码 base64 编码后在页面内 `atob()` 解码。禁止把文件内容直接拼进 JS 模板字符串——源码中的反引号、`${`、反斜杠会被解释执行并损坏内容。含中文/非 ASCII 标签时，`atob()` 得到的是 Latin-1，需用 `decodeURIComponent(escape(atob('…')))` 还原 UTF-8。

渲染顺序与产物：

1. **SVG（必出）**：`__renderMermaid('diagram-1', <解码后源码>)` → 结果写入 `<slug>.svg`。
2. **PNG（必出）**：`__rasterize(svg, 1950)` → 写入 `<slug>.png`。1950px = 6.5 英寸版面宽 @300dpi，保证打印与文档清晰。
3. **.excalidraw（仅 flowchart 类）**：`__mermaidToExcalidraw(<解码后源码>)` → 结果写入 `<slug>.excalidraw`，并核对返回 JSON 的 `elements` 数量 > 0。

错误处理：

- Mermaid 解析报错：把解析错误原样展示给用户，修正 `.mmd` 后重试；**不交付带解析错误的源码文件**。
- `__mermaidToExcalidraw` 对非 flowchart 类型失败：跳过 `.excalidraw`，交付 SVG+PNG 并附硬约束 4 的限制说明。
- 渲染页/浏览器不可用：报 BLOCKED，给出环境构建命令，不用其他方式凑产物。

## Step 4 — 展示与交付

1. 用读图工具内联展示 PNG，让用户直接看到结果。
2. 列出三件套完整路径。
3. 附一行可编辑性说明："`.excalidraw` 可在 excalidraw.com（File → Open）打开编辑；编辑后可从场景文件重新导出。"
4. 用户要改内容：改 `.mmd`，重跑 Step 3。

**编辑往返**（用户在 excalidraw.com 改完 `.excalidraw` 后要求重新出图）：不再经过 Mermaid，直接以场景文件为输入——同样走 base64 传输（场景 JSON 充满引号和反斜杠）——`__excalidrawToSvg(scene)` → SVG → `__rasterize` → PNG。

## .excalidraw JSON 结构要点

转换器输出的场景文件即标准 Excalidraw 场景格式。手工校验、修补或程序化生成时遵循以下结构。

### 顶层结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ... ],
  "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

`elements` 是唯一的图形内容数组；`appState` 只带最小视图状态；无嵌入图片时 `files` 为空对象。

### element 公共字段

每个元素都含：

| 字段 | 说明 |
|---|---|
| `id` | 唯一字符串 ID（随机 nanoid 风格） |
| `type` | `rectangle` / `ellipse` / `diamond` / `arrow` / `line` / `text` / `freedraw` / `image` / `frame` |
| `x`, `y` | 包围盒左上角坐标（arrow/line 为起点锚） |
| `width`, `height` | 包围盒尺寸 |
| `angle` | 旋转弧度，默认 0 |
| `strokeColor`, `backgroundColor` | 描边/填充色，如 `"#1e1e1e"`、`"transparent"` |
| `fillStyle` | `hachure`（手绘斜线）/ `cross-hatch` / `solid` |
| `strokeWidth`, `strokeStyle` | 线宽；`solid` / `dashed` / `dotted` |
| `roughness` | 0（干净）/ 1（手绘）/ 2（更糙） |
| `opacity` | 0–100 |
| `seed`, `versionNonce` | 随机整数，决定手绘抖动形态 |
| `version` | 整数版本号，每次修改递增 |
| `isDeleted`, `locked`, `link` | 默认 `false` / `false` / `null` |
| `groupIds`, `frameId` | 分组与画框归属，默认 `[]` / `null` |
| `boundElements` | 绑定到本元素的其他元素：`[{"type":"text","id":"…"},{"type":"arrow","id":"…"}]`，无绑定为 `null` |
| `roundness` | 圆角：矩形类 `{"type":3}`，线/箭头 `{"type":2}`，直角为 `null` |
| `updated` | 毫秒时间戳 |

### 节点与文字绑定

容器内文字是**两个元素 + 双向引用**：

- 容器（rectangle/diamond/ellipse）的 `boundElements` 含 `{"type":"text","id":"<文字元素id>"}`。
- 文字元素设 `containerId: "<容器id>"`，并带 `text`、`originalText`（两者一致）、`fontSize`（16/20 常用）、`fontFamily`（1 手写体 / 2 无衬线 / 3 等宽）、`textAlign: "center"`、`verticalAlign: "middle"`、`lineHeight: 1.25`。
- 文字元素的 `x/y/width/height` 由容器内居中计算；绑定关系建立后由 Excalidraw 自动维护换行与居中。
- 漏掉任一侧引用，打开文件时文字会脱离容器或丢失。

### 箭头绑定

- arrow 元素：`points` 为**相对起点**的坐标序列 `[[0,0],[dx,dy],…]`；`x/y` 是起点绝对坐标；`lastCommittedPoint: null`。
- 端点吸附靠 binding：`startBinding` / `endBinding` 为 `{"elementId":"<节点id>","focus":0,"gap":4}` 或 `null`（自由端）。`focus` 0 = 对准节点中心，±1 = 偏向节点两端；`gap` 为箭头端点与节点边缘的留白，4–8px 自然。
- 被指向的节点必须在 `boundElements` 里回加 `{"type":"arrow","id":"<箭头id>"}`。缺回指时拖动节点箭头不跟随。
- 箭头头部：`startArrowhead: null`、`endArrowhead: "arrow"`（单向箭头默认形态）。

### 坐标布局约定

- 画布从 `(0,0)` 附近开始，四周留 ≥40px 边距；坐标不出现负值堆叠。
- 常规节点 160–200 × 60–80；水平间距 80–120，垂直间距 100–140，保证箭头有可辨识的长度。
- 分层/泳道容器：容器矩形包住子元素并留 40px 内边距；容器自身不绑定箭头时用 `groupIds` 或 frame 组织。
- 文本独立元素（非容器绑定，如标题、边标签）：`containerId: null`，边标签放在对应箭头中点附近。

### 场景校验清单

生成或修补 `.excalidraw` 后逐项核对：

- [ ] JSON 可解析，顶层含 `type: "excalidraw"`、`version: 2`、`elements` 数组
- [ ] `elements` 非空，每个元素有唯一 `id` 且类型合法
- [ ] 所有 `startBinding`/`endBinding`/`containerId` 引用的 `elementId` 在 `elements` 中存在
- [ ] 所有绑定关系双向成立（节点 `boundElements` 回指箭头/文字）
- [ ] arrow 的 `points` 首点为 `[0,0]`，坐标为相对值
- [ ] 元素的 `width/height` 非负，`seed`/`versionNonce` 为随机整数
- [ ] 在 excalidraw.com 实际打开验证一次：文字在容器内、拖动节点箭头跟随

## 完成状态

- **DONE**：三件套（或 SVG+PNG 两件套 + 可编辑性限制说明）已渲染、已展示、路径已列出。
- **BLOCKED**：渲染页或无头浏览器不可用；已给出环境构建/安装命令，未用降级方式凑产物。
