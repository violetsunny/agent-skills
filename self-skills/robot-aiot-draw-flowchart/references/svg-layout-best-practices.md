# SVG 技术图表布局最佳实践

间距、字号、marker、阴影等基础参数的唯一权威是 `design-system.md`（§6/§7）；本文件只承载布局操作的增量技巧，与权威冲突处一律以 `design-system.md` 为准。

## 通用布局规则（对所有风格生效）

### 1. 组件间距
- **组件间净距**：取 `design-system.md` §7 允许集 {20, 24, 32, 40, 48}px，坐标落 4px 网格
- **箭头路径净空**：箭头路径与无关节点边缘保持可见净空，布线值同样落 4px 网格
- **层间垂直间距 / 同层水平间距**：在允许间距带上取值；布局需要更大节奏时可放大，但必须是 4 的倍数且不制造对角线布线需求

### 2. 箭头布线与连接点

#### 连接点规则
- **箭头永不接在组件角落** —— 用边的中点
- **入/出点**：
  - 上边：`cx ± offset`，单箭头 offset = 0，多箭头 ±30px
  - 下边：同规则
  - 左/右边：`cy ± offset`
- **距角净空**：最小 20px
- 同边多连接点按 `design-system.md` §6 规则 4 扇形均布（`L*k/(N+1)`，相邻 ≥12px）

#### 箭头路径布线
- **避免对角线穿越组件** —— 用正交布线（L 形路径），拐弯四分之一圆弧 r=8（紧凑布局最小 r=6，见 `design-system.md` §6 规则 1）
- **曲线箭头**：
  - 控制点距任何组件边缘 ≥40px
  - 复杂布线用中间折点：`M x1,y1 L x2,y2 Q cx,cy x3,y3`
- **同层间多条箭头**：Y 坐标错开 16-20px 防重叠（平行线错开 ≥12px 是 `design-system.md` §6 规则 3 的下限）

#### 箭头防重叠
```svg
<!-- Bad: diagonal arrow crosses component -->
<path d="M 200,100 L 600,400"/>

<!-- Good: orthogonal routing around component -->
<path d="M 200,100 L 200,250 L 600,250 L 600,400"/>

<!-- Good: curved with safe control point -->
<path d="M 200,100 Q 400,200 600,400"/>
<!-- Control point (400,200) is 50px+ away from any component -->
```

### 3. 箭头标签摆放
- **遮罩常驻**：每个箭头标签都必须有不透明遮罩矩形（`design-system.md` §6"Arrow labels — always mask, always with margin"），不是碰撞后才加的兜底
- **可见间距**：遮罩矩形底边与连线 stroke 之间强制 6–10px 可见间隙，标签永不压线
- **遮罩填充**：与背景色一致（默认 `#f5f5f5`），内边距水平 4px、垂直 2px 起步，按文本实际尺寸放大
- **安全距离**：距任何组件边缘 ≥15px；遮罩不得压住后绘节点（§6 规则 6）
- **多条汇聚箭头**：标签位置垂直错开 20px
- **长度上限**：≤14 字符（§6 规则），全大写、居中于线段中点；缩短为动宾短语，永不整句

### 4. 组件重叠检测
定稿 SVG 前检查：
- 组件包围盒互不重叠（8px 安全边距）
- 箭头路径不穿过组件内部（唯一例外：几何不可避免时按 §6 规则 5 改虚线过境）
- 文本标签不与组件或其他标签重叠

### 5. Z 序分层（SVG 渲染顺序）
```svg
<!-- Render order (top to bottom = back to front): -->
1. Background rect
2. Grouping containers (dashed rects)
3. Arrow paths
4. Arrow label background rects when collision fallback is needed
5. Components (boxes, cylinders, etc.)
6. Component text
7. Arrow label text
8. Legend
```

## 风格专属增强

### Style-1: Flat Icon Clean
- **严格对齐**：坐标吸附 8px 网格（4px 网格的更严子集）
- **利落圆角**：圆角矩形统一 rx="8" ry="8"
- **箭头**：细线（1.5-2px），实心 polygon marker
- **无阴影**：扁平设计原则

### Style-6: Claude Official Warm
- **柔和阴影**：`<feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#00000008"/>`（style-6 官方风格例外，已在 `design-system.md` §4 阴影禁令处登记）
- **更圆圆角**：rx="12" ry="12"（同属 style-6 官方风格例外）
- **箭头**：中等线宽（2px），弱化 marker

## 校验清单

导出 PNG 前核对：
- [ ] 无箭头-组件重叠（目检）
- [ ] 箭头标签带遮罩且与连线保持 6–10px 可见间距
- [ ] 箭头路径对无关节点保持可见净空
- [ ] 组件间距取 `design-system.md` §7 允许集 {20, 24, 32, 40, 48}px
- [ ] 箭头连接点避开角落（距角 ≥20px）
- [ ] 层间多条箭头已错开
- [ ] 图例可读且不遮内容
- [ ] SVG 经 `cairosvg`（或 `rsvg-convert` 兜底）渲染干净

## 常见反模式与修法

| 反模式 | 修法 |
|--------------|-----|
| 箭头穿越组件 | 正交布线，加大控制点距离 |
| 标签压组件 | 加大偏移；补常驻遮罩矩形并保持 6–10px 线距 |
| 组件过近 | 间距回到 §7 允许集（20–48px）内取值，或扩大画布 |
| 箭头接角落 | 连接点移到边中点偏移位 |
| 无 Z 序规划 | 按渲染顺序：arrows -> components -> text |
| 跨层箭头反复出现 | 收拢为内容区外单条 "delegates down" 汇流轨 |
| 元素挤太密 | 加大 viewBox 高/宽，而不是继续挤 |

## 连线防重叠（jump-over）

两条箭头必须交叉时，一律用跳线弧防视觉重叠：

- 水平箭头交叉：加小半圆弧（半径 5px，stroke 同箭头色，fill none）"跳过"另一条线
- jump-over 的 SVG 画法：下层先画白/同底色弧，再在其上画上层的弧
- 多处交叉：弧半径错开（5px、7px、9px），弧与弧不重叠
- 绝不允许两条箭头的直线段无跳线弧直接交叉

## SVG 技术规则

- ViewBox：默认 `0 0 960 600`；竖版 `0 0 960 800`；宽版 `0 0 1200 600`
- 字体：经 `<style>font-family: ...</style>` 内嵌 —— 不用外部 `@import`（cairosvg / rsvg-convert 无法拉取外部 URL）
- `<defs>`：arrow marker、渐变、filter、clip path
- 文本：字号取 `design-system.md` §7 允许集 {8, 12, 16, 20, 24, 28, 32, 40}；角色分工按 §5 Typography（节点名 12px sans 600、技术子标签 9px mono、箭头标签 8px mono、页面标题按 style-guide）
- 所有箭头：`<marker>` 配 `markerEnd`，尺寸按 `design-system.md` §6 动态标准 —— `markerWidth` = 画布 viewBox 宽 × 0.9375%，`markerHeight` = markerWidth × 0.7，`markerUnits="userSpaceOnUse"`（960 宽 → 9.0×6.3；1000 → 9.4×6.6；1200 → 11.2×7.9），全图一个尺寸
- 阴影：禁止（`design-system.md` §4"Shadows are out. Borders are in."）；唯一例外是已登记的 style-6 官方风格
- 曲线路径：循环/反馈箭头用 `M x1,y1 C cx1,cy1 cx2,cy2 x2,y2` 三次贝塞尔
- 内容裁切：文本可能溢出节点框时用 `<clipPath>`
- Filter 边界安全：每个带 `filter="url(...)"` 的元素距 viewBox 边缘至少 `max(元素尺寸 20%, 阴影模糊半径 × 3)`，否则靠边一侧 stroke 被裁掉（边框单边消失）

## 生成后箭头优化

用户对已生成的图要求"优化箭头" / "fix arrow routing" / "optimize the diagram"时，保留全部节点、容器、样式与布局——只改 JSON 数据中的 `arrows` 条目，然后用 `scripts/generate-from-template.py` 重渲染。

可用的箭头覆盖字段（按推荐使用顺序）：

| 字段 | 类型 | 何时使用 |
|-------|------|-------------|
| `source_port` / `target_port` | `"left"` / `"right"` / `"top"` / `"bottom"` | 箭头出/入边不对 |
| `corridor_x` | `[x, ...]` | 提示垂直段走该 x 通道（软偏好） |
| `corridor_y` | `[y, ...]` | 提示水平段走该 y 通道（软偏好） |
| `route_points` | `[[x1,y1], [x2,y2], ...]` | 精确有序折点；每段正交布线，不安全点会被拒绝 |
| `routing_padding` | number (default: 24) | *（进阶）*调整该箭头的障碍净空 |
| `port_clearance` | number | *（进阶）*调整首段距节点边缘的偏移 |
| `label_style` | `"badge"` / `"offset"` | badge 底色造成视觉杂乱时选 `"offset"`；传统/高对比标签保持默认 `"badge"` |
| `stroke_width` | number (default: style `arrow_width`, e.g. 2.4) | 线宽；模板渲染路径的箭头 marker 为 `markerUnits="userSpaceOnUse"` 动态尺寸（viewBox 宽 × 0.9375%），不随 stroke 缩放，`stroke_width` 只改线身粗细。箭头显粗时设 1.6–1.8 |

JSON/模板渲染默认保持 `"badge"` 以向后兼容。单条箭头设 `"label_style": "offset"` 可得无底色矩形的偏移标签。

优化步骤：

1. 读现有 SVG —— 找出哪些箭头重叠、穿节点或明显错位
2. 在 JSON 数据中按 `source` / `target` 对定位这些箭头
3. 出/入方向不对加 `source_port` / `target_port`；平行箭头要分开加 `corridor_x` / `corridor_y`；提示解决不了才用 `route_points`
4. 用更新后的 JSON 重跑 `generate-from-template.py`，并以 `validate-svg.sh` 校验

示例 —— 把两条重叠箭头分进不同通道：

```json
{ "source": "nodeA", "target": "nodeB", "corridor_y": [280] }
{ "source": "nodeC", "target": "nodeD", "corridor_y": [320] }
```

示例 —— 收细粗箭头头，并把长跨层控制箭头改走外边距：

```json
{ "source": "d1", "target": "g1", "flow": "data", "stroke_width": 1.8 }
{ "source": "a3", "target": "g1", "flow": "control", "label": "控制",
  "source_port": "right", "target_port": "right",
  "route_points": [[915, 160], [915, 425]], "stroke_width": 1.8 }
```

箭头精修规则：

- 绝不让两条箭头共用一个节点的端口区（如都在 top-center）；用 `source_port` / `target_port` 给其中一条换边
- 长跨层箭头贴外边距走：同侧端口（right→right 或 left→left）+ `route_points` 走在容器边缘与画布边缘之间的通道（如 960 宽画布上的 x=915），得到干净 C 形而不是斜穿节点列的对角线
- `route_points` 各段必须与声明端口正交、不得穿越节点矩形，否则生成时报 route error —— 移通道，不要硬凑路径

## SVG 生成与防错

**强制：Python list 逐行生成法**（手写 SVG 一律用这个）：

```python
python3 << 'EOF'
lines = []
lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700">')
lines.append('  <defs>')
# ... each line separately
lines.append('</svg>')

with open('/path/to/output.svg', 'w') as f:
    f.write('\n'.join(lines))
print("SVG generated successfully")
EOF
```

为什么强制：防字符截断、防手误、防语法错误。每行独立、逐行可校验。

**Pre-Tool-Call 三问**（每次调用前都过）：

1. 现在能一次写出完整命令/内容吗？
2. 所有必需参数都备齐了吗？
3. 检查过待写内容的语法错误了吗？

任一为否：停止调用，先备好内容。

**错误恢复协议**：

- 第一次错误：分析根因，针对性修复
- 第二次错误：整体换方法（Python list → 分块生成）
- 第三次错误：停止并报告用户 —— 不无限循环
- 永不：重试同一条失败命令、用空参数调用工具

**常见语法错误**：

- ❌ `yt-anchor` → ✅ `y="60" text-anchor="middle"`
- ❌ `x="390` (missing y) → ✅ `x="390" y="250"`
- ❌ `fill=#fff` → ✅ `fill="#ffffff"`
- ❌ `marker-end=` → ✅ `marker-end="url(#arrow)"`
- ❌ `L 29450` → ✅ `L 290,220`
- ❌ 末尾缺少 `</svg>`

**校验**（生成后运行）：

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')" && echo "✓ Valid XML"
# Or use cairosvg as a render-time check:
python3 -c "import cairosvg; cairosvg.svg2png(url='file.svg', write_to='/tmp/test.png')" && echo "✓ Renders" && rm /tmp/test.png
```

## SVG 文本字形安全（CairoSVG 导出）

CairoSVG 是默认 PNG 导出渲染器（png-export.md）。macOS 下 fontconfig 常无法解析系统中文字体名，以下字符在 SVG `<text>` 中渲染为豆腐块：`≈ × → ① ② ③ …`。

- SVG 文本只用安全字形集：`—— 、，。（）【】：+ / · “”` 与普通中日韩/拉丁/数字。
- 语义改用文字表达：`→` 写"演进到/导向"，`×` 写"与/对应"，`≈` 写"约"，圈号写"问题1/第1项"。
- HTML 页面文本不受限（浏览器逐字形回退）；本规则只约束 SVG 文本与经 CairoSVG 导出的 PNG。
- 导出后目检 PNG 一次确认无豆腐；必需符号无法回避时改用 Puppeteer 渲染器（png-export.md）。
- 自动检查：`python3 $SKILL_ROOT/scripts/check_glyph_safety.py <file.svg>` —— 按本节安全字形集扫描 SVG `<text>` 内容（箭头/数学运算符/圈号等 Unicode 区块报违规），exit 0 = 无错误（允许 warning），exit 1 = 有错误。
