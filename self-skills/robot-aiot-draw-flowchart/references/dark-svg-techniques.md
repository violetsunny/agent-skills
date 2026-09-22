# 深色主题 SVG 直绘技法

适用对象：slate 深色调色板（style-2 Dark Terminal 一族）的深色直绘 SVG。本文件补充 style-2-dark-terminal.md / style-8-dark-luxury.md / color-schemes.md 未覆盖的增量：深色底色层次、对比度硬约束、架构图/流程图/时序图/思维导图/结构图的深色绘制配方、独立 .svg 输出规格。

通用间距、连线与标签遮罩规则仍以 svg-layout-best-practices.md 与 design-system.md 为准；数值冲突时取更严格者。

## 1. 深色底色层次

### 1.1 底色与网格

底色 `#0f172a`（slate-900），叠加 40px 细网格提供尺度感而不干扰内容：

```svg
<defs>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="#0f172a"/>
<rect width="100%" height="100%" fill="url(#grid)"/>
```

网格线颜色取底色上一档的同色系（`#1e293b`），线宽 0.5px；网格可见度必须低于任何内容描边。

### 1.2 高程层次

深色下用亮度台阶表达深度，不用投影：

1. 画布 `#0f172a`（或渐变到 `#1a1a2e`）
2. 组件面板：rgba 半透明填充（§1.3）或不透明深色填充
3. 抬升面板/次级标题条：再亮一档（如 `#1a1a1a` / `rgba(30,41,59,0.8)`）

### 1.3 半透明填充 + 不透明遮罩双矩形（强制技法）

深色组件框常用 rgba 半透明填充保留背景质感。凡有箭头、网格可能从组件下方经过，必须先在同位置垫一个同几何的不透明遮罩矩形，否则底下线条会透过半透明填充显示出来：

```svg
<!-- 遮罩层：不透明，与组件同几何 -->
<rect x="100" y="100" width="160" height="60" rx="6" fill="#0f172a"/>
<!-- 视觉层：半透明填充 + 亮色描边 -->
<rect x="100" y="100" width="160" height="60" rx="6"
      fill="rgba(8,51,68,0.4)" stroke="#22d3ee" stroke-width="1.5"/>
<text x="180" y="125" fill="white" font-size="11" font-weight="600" text-anchor="middle">API Gateway</text>
<text x="180" y="141" fill="#94a3b8" font-size="9" text-anchor="middle">Kong / Nginx</text>
```

数据库圆柱、类图分栏框等复合形状的每个子形状（ellipse/rect）都要先垫遮罩再上半透明层。

### 1.4 绘制顺序（z-order）

SVG 后画者在上，严格按此顺序输出：

1. 背景底色 + 网格
2. 区域/分组边界（虚线框）
3. 连接箭头与线条
4. 不透明遮罩矩形（与组件框同位置）
5. 组件框（半透明填充 + 描边）
6. 文字标签
7. 图例（右下或底部，所有边界之外）
8. 标题块（左上）

## 2. 对比度硬约束

### 2.1 文字层级与下限

| 角色 | 字号/字重 | 颜色下限 |
|---|---|---|
| 标题 | 16px / 700 | white 或 `#e2e8f0` |
| 组件名 | 11-12px / 600 | white |
| 次级标签/描述 | 9px / 400 | `#94a3b8` |
| 注释/附注 | 8px / 400 | `#94a3b8` |
| 箭头小标签 | 7-8px | `#94a3b8` 或更亮 |

硬约束：

- 7px 是深色下任何文字的下限，不得低于此值。
- 禁止用 `#475569` 及更暗的 slate 作正文文字色——在 `#0f172a` 底上对比度不足，该档位只能作装饰性描边。
- 正文文字对比度 ≥ 4.5:1；大字号（≥18px）与图形元素 ≥ 3:1。
- 次级文字统一 `#94a3b8`，不再往下分档；需要更弱时用降低不透明度以外的手段（缩小字号至下限、精简文案）。

### 2.2 连线与降权

- 主连线描边 ≥ `#64748b`；重要连线用语义亮色（§3 的 stroke 列）。
- 次要连线降权用 `stroke-opacity="0.6"`，禁止换成更暗的颜色——变暗会直接跌破对比度下限。
- 主路径（happy path）比分支路径亮，用 stroke-opacity 差异形成视觉主次。

## 3. 深色语义色系统

八个语义类别，每类 = 深色 rgba 半透明填充 + 同色系亮色描边：

canonical 数据：`assets/dark-palette.json` — 以 json 为准（8 条，字段 category/fill/stroke/stroke_name/usage）。简表：

| 类别 | 描边 |
|---|---|
| Primary | `#22d3ee` cyan |
| Secondary | `#34d399` emerald |
| Tertiary | `#a78bfa` violet |
| Accent | `#fbbf24` amber |
| Alert | `#fb7185` rose |
| Connector | `#fb923c` orange |
| Neutral | `#94a3b8` slate |
| Highlight | `#60a5fa` blue |

使用规则：

- 架构图按技术类别赋色；流程图与时序图按角色（actor/决策/过程）赋色，不按技术。
- 填充 alpha 控制在 0.3-0.5：既保留背景网格质感，又靠遮罩矩形（§1.3）保证不透底。
- 本表是深色直绘调色板，与 color-schemes.md 的浅色机器人调色板不混用；同一张图只允许一套调色板体系。

## 4. 箭头与 marker

```svg
<!-- 标准灰箭头 -->
<marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
</marker>

<!-- 开放箭头（空心）：异步消息、返回消息 -->
<marker id="arrow-open" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polyline points="0 0, 10 3.5, 0 7" fill="none" stroke="#64748b" stroke-width="1.5"/>
</marker>
```

- marker 不继承线条 stroke 颜色：每种用到的箭头颜色单独建一个 marker（如 `arrow-cyan` 填 `#22d3ee`）。
- 空心形状（继承三角、聚合菱形）用底色填充 + 亮色描边，在深色下才能读出"空心"语义：

```svg
<marker id="inherit" markerWidth="12" markerHeight="10" refX="12" refY="5" orient="auto">
  <polygon points="0 0, 12 5, 0 10" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
</marker>
<marker id="composition" markerWidth="12" markerHeight="8" refX="0" refY="4" orient="auto">
  <polygon points="0 4, 6 0, 12 4, 6 8" fill="#94a3b8"/>
</marker>
<marker id="aggregation" markerWidth="12" markerHeight="8" refX="0" refY="4" orient="auto">
  <polygon points="0 4, 6 0, 12 4, 6 8" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
</marker>
```

## 5. 分类型深色绘制配方

### 5.1 架构图

- 主方向二选一：LTR（数据管道/请求流，客户端在左、存储在右）或 TTB（分层架构，客户端在上、基础设施在下）。
- 列距 200-220px（LTR，按列起点计），行距 120-140px（TTB，按行起点计）；组件更宽时相应放大。
- 总线/事件总线：在服务层之间的空隙画一条水平横条，用 Connector 橙色；上下组件用短垂直线接入总线。

```
Services:  [ Svc A ]    [ Svc B ]    [ Svc C ]
               │              │            │
Bus:     ════╪══════════════╪════════════╪═══════
               │              │            │
Data:    [ DB A ]        [ DB B ]     [ Cache ]
```

- 多区域嵌套用虚线疏密区分层级：外层 `stroke-dasharray="12,4"`，中层 `"8,4"`，内层 `"4,4"`。
- 区域边界：亮色虚线框（rx=12，stroke-width=1）+ 左上角 9px/600 同色标签；安全组用 rose `4,4` 虚线 + 8px 标签。
- 会穿越组件的连线改两段 L 形路径；繁忙图中次要连线 `stroke-opacity="0.6"`。

### 5.2 流程图

形状词汇与深色赋色：

| 形状 | 含义 | SVG | 深色赋色 |
|---|---|---|---|
| 大圆角矩形 rx=25 | 开始/结束 | `<rect rx="25">` | Highlight 蓝 |
| 矩形 rx=6 | 过程/动作 | `<rect rx="6">` | Primary cyan 或 Secondary emerald |
| 菱形 100×70（点对点） | 决策 | `<polygon>` | Accent amber（天然吸引视线） |
| 平行四边形 | 输入/输出 | 斜切 `<polygon>` | Neutral slate |
| 圆柱 | 数据存储 | ellipse+rect 组合 | Tertiary violet |

布局与标注：

- 主流程自上而下走中线；决策分支 Yes 继续向下、No 向右（空间紧张时向左）。
- Yes/No（或 是/否、True/False）标签直接放在出口箭头旁，距菱形边缘 10px，8px 字号：Yes 用 `#34d399`，No 用 `#fb7185`。
- 分支水平偏移 200px（距中线）；汇合连线距任何框 ≥20px；回退循环沿图最左/最右侧向上绕曲线。
- 步骤间垂直间距 60-80px（容纳箭头 + 可选标签）。
- 错误/异常路径：rose 虚线箭头。
- 10+ 步骤：按阶段分组成泳道（垂直列 + 顶部 header 条），泳道边界复用架构图区域边界配方。

决策菱形深色配方（双 polygon 遮罩）：

```svg
<g transform="translate(CX, CY)">
  <polygon points="0,-35 50,0 0,35 -50,0" fill="#0f172a"/>
  <polygon points="0,-35 50,0 0,35 -50,0"
           fill="rgba(120,53,15,0.3)" stroke="#fbbf24" stroke-width="1.5"/>
  <text y="4" fill="white" font-size="10" font-weight="600" text-anchor="middle">Condition?</text>
</g>
```

### 5.3 时序图

- actor 横排顶部，间距 150-200px；actor 框 130×45，用双矩形遮罩配方（§1.3）。
- 生命线：actor 框底部中点向下的垂直虚线，`stroke="#334155"` `stroke-width="1"` `stroke-dasharray="6,4"`。
- 消息为水平箭头，按时间自上而下排布，行距 40-50px。
- 线型语义：同步 = 实线 `#94a3b8` 1.5px + 实心箭头；异步 = 开放空心箭头（§4）；返回 = 虚线 `6,3` `#64748b` 1px，标签 8px 斜体 `#94a3b8`。
- 激活条：宽 10px 居中于生命线，从入向消息延伸到出向消息，`fill="rgba(8,51,68,0.6)"`，stroke 用该 actor 的颜色。
- 自消息：U 形回环，向右伸出 40px、向下 25px 返回同一生命线，标签在回环右侧。
- 注释 note：折角圆角矩形（右上角小三角内折成折页效果），先垫双矩形遮罩（§1.3），紧贴被注释的消息或框架放置。
- alt/opt/loop 框架：`stroke-dasharray="4,3"` 边界 + 左上角标签 tab（50×18，`fill="rgba(30,41,59,0.8)"`，8px/600 标签）+ 条件文本斜体；else 分隔用横贯虚线 + `[else]` 斜体标签。
- 8+ 条消息时逐条编号：起点左侧 r=8 圆（`fill="rgba(59,130,246,0.3)"` `stroke="#60a5fa"`）+ 7px/600 白色数字。
- 每个 actor 分配调色板中的一种专属颜色，用于：actor 框描边、该生命线的激活条、（复杂图可选）该 actor 的出向箭头。

### 5.4 思维导图

- 中心概念节点向四周放射布局；中心节点字号最大，向外逐级递减。
- 分支用三次贝塞尔曲线（`<path>` C 指令）有机延伸，不用直线或正交折线。
- 各主分支在 §3 调色板内变换颜色；子分支继承所属主分支的颜色。
- 同级分支保持角度均衡分布，避免挤在半侧；分支末端文字沿放射方向放置，不压线。

### 5.5 结构图（类图 / ER / 组织架构图）

- 类框三栏（名称/属性/方法）：整框先垫遮罩；栏分隔线用框的 stroke 色，`stroke-width="0.5"` `stroke-opacity="0.5"`；名称 11px/700 居中，属性/方法 8px `#94a3b8` 左对齐，带 `+`/`-` 可见性前缀。
- 抽象类名斜体；接口在名称上方加小字号 `«interface»` 行。
- 关系线：继承 = 实线 + 空心三角（指向父类）；实现 = 虚线 + 空心三角；组合 = 实线 + 实心菱形（在拥有端）；聚合 = 实线 + 空心菱形；依赖 = 虚线 + 开放箭头；关联 = 实线 + 开放箭头或无箭头。marker 配方见 §4。
- 基数标签（`1..*` 等）8px `#94a3b8`，距框边 5-8px。
- ER 图：两栏框（实体名 + 属性），主键 `PK` 前缀加粗，外键 `FK` 前缀；关系端用鸦爪表示法——"一"端单线，"多"端三条短线扇形收拢到端点。
- 组织架构图：自顶向下树形，根在顶部居中，层级垂直间距 100-120px，兄弟节点水平均分；连线 = 父底部中心垂直到水平横杆，再垂直向下到各子顶部中心；按部门或层级赋色；5+ 层的深树改横向布局。
- 树宽由最宽一层决定，整体在 viewBox 中水平居中。

## 6. 深色组件基元

数据库圆柱（每个子形状先遮罩后半透明）：

```svg
<g transform="translate(X, Y)">
  <rect x="0" y="10" width="120" height="50" rx="2" fill="#0f172a"/>
  <ellipse cx="60" cy="10" rx="60" ry="12" fill="#0f172a"/>
  <ellipse cx="60" cy="60" rx="60" ry="12" fill="#0f172a"/>
  <rect x="0" y="10" width="120" height="50" fill="rgba(76,29,149,0.4)"/>
  <ellipse cx="60" cy="10" rx="60" ry="12" fill="rgba(76,29,149,0.4)" stroke="#a78bfa" stroke-width="1.5"/>
  <ellipse cx="60" cy="60" rx="60" ry="12" fill="rgba(76,29,149,0.4)" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="0" y1="10" x2="0" y2="60" stroke="#a78bfa" stroke-width="1.5"/>
  <line x1="120" y1="10" x2="120" y2="60" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="60" y="40" fill="white" font-size="11" font-weight="600" text-anchor="middle">PostgreSQL</text>
</g>
```

区域边界与安全组：

```svg
<!-- 区域边界 -->
<rect x="X" y="Y" width="W" height="H" rx="12" fill="none"
      stroke="#fbbf24" stroke-width="1" stroke-dasharray="8,4"/>
<text x="X+12" y="Y+16" fill="#fbbf24" font-size="9" font-weight="600">AWS us-east-1</text>

<!-- 安全组 -->
<rect x="X" y="Y" width="W" height="H" rx="8" fill="none"
      stroke="#fb7185" stroke-width="1" stroke-dasharray="4,4"/>
<text x="X+10" y="Y+14" fill="#fb7185" font-size="8" font-weight="500">VPC / Security Group</text>
```

## 7. 深色间距节奏

- 组件框高度：标准 50-70px，大型/复杂组件 80-120px。
- 区域边界内边距：距所含组件四周 ≥20px。
- 箭头标签距任何框边缘 ≥10px。
- 图例：最低图表元素下方 ≥20px，且在所有区域边界之外。
- 标题块：距左上角 20px，位于内容区之外。
- viewBox：内容包围盒 + 四边各 30px padding。
- 与通用规则的关系：本节是深色直绘的排版节奏（行距/列距/消息距/内边距）；间距与网格基准以 design-system.md §7 为唯一权威（节点间距取 20/24/32/40/48px 允许集、4px 网格），本节数值是深色场景的增量节奏，与通用允许值冲突时取更大者。

## 8. 独立 .svg 输出规格

适用于直绘 SVG 主路径。import 重绘（drawio/mermaid）流程的格式与尺寸档位仍以 output-spec.md 为准。

1. 输出单个自包含 `.svg` 文件——零外部依赖；仅联网发布场景且需要品牌 webfont 时允许加 Google Fonts `@import`（零外链交付物禁止，一律系统字体栈）。
2. 根 `<svg>` 必须带 `xmlns="http://www.w3.org/2000/svg"`。
3. `viewBox` 按内容 + 30px padding 设置；不写固定 `width`/`height` 属性，让 SVG 响应式缩放。
4. `<style>`、`<defs>`、marker、pattern 全部置于文件顶部。
5. 居中标签用 `text-anchor="middle"`；文字不得溢出所在框。
6. 中文标签：`font-family` 追加 `'Noto Sans SC','PingFang SC'` 回退，并加宽框体——CJK 字符更宽。
7. 等宽字体引用（可选，**仅联网发布场景**；零外链交付物禁止 `@import`，离线环境自动回退系统等宽字体）：

```svg
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap');
  text { font-family: 'JetBrains Mono', 'SF Mono', 'Cascadia Code', monospace; }
</style>
```

8. 保存位置：输入为文件时存 `{输入文件目录}/diagram/`；否则存 `{项目目录}/diagram/{topic-slug}/`；目录不存在则创建。
9. 保存后可导出 @2x PNG 用于预览与位图交付场景。

## 9. 交付前自检

- [ ] 底色 + 网格正确渲染；所有半透明填充组件下方都有同几何不透明遮罩
- [ ] 绘制顺序符合 §1.4，箭头不从组件框内透出
- [ ] 全部文字 ≥7px；次级文字 ≥ `#94a3b8`；无 `#475569` 及更暗的正文
- [ ] 次要连线用 opacity 降权，未使用更暗颜色
- [ ] 颜色全部来自 §3 调色板；同图未混入浅色调色板体系
- [ ] 空心 marker（继承/聚合/开放箭头）用底色填充，深色下语义可读
- [ ] 图例在所有边界外；viewBox = 内容 + 30px；无固定 width/height
- [ ] 中文标签有 CJK 字体回退且框宽足够

自动化校验：`python3 $SKILL_ROOT/scripts/check_dark_svg.py <file.svg> [--bg HEX]` 按本节 §2/§7/§8/§9 硬约束检查深色 SVG（7px 字号下限、WCAG 对比度、viewBox 30px 内边距、CJK 回退）；`--bg` 覆盖背景自动探测。exit 0 = 无 error（允许 warning），1 = 有 error；检测到浅色背景时弃权（exit 0，深色规则不适用）。
