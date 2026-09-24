# 代码与 JSON 数据块展示规范

适用：deck / 落地页 / 文档形态中一切 JSON、配置、报文示例类数据块（物模型定义、DeviceMessage、遥测上行、调用示例等）。定版自 AIOT 演示 deck 实测（p09 定版、p08/p10/p12 对齐），生成样式时直接引用本节的 CSS 与 markup 范式，不另发明。

## 1. 排版范式（规整格式，硬约束）

- 外层 `{` 与 `}` 各独占一行
- 每个字段独占一行，嵌套层级 2 空格缩进
- 叶级短对象 / 短数组允许单行：元素 ≤4 个且单行总宽 ≤60 字符（如 `{ "type": "boolean", "access": "rw" }`、`["code", "severity"]`）
- 禁止多字段挤一行的紧凑写法（`{"a":1,"b":2}` 整块单行）；禁止用省略号截断真实字段
- 空对象 / 空数组写作 `{}` / `[]`，不拆行

## 2. 容器与行结构 CSS（复制即用）

```css
pre.code{background:var(--band-l);border:1px solid var(--line);border-radius:8px;padding:8px 12px;
font-family:'SF Mono',Menlo,Consolas,'Courier New',monospace;font-size:12px;line-height:1.7;
color:var(--ink);overflow-x:auto;white-space:pre;margin:0}
.ln{display:block;white-space:pre}
.jk{color:var(--pri-d);font-weight:700}
.jstr{color:#059669}
.jnum{color:#ea580c}
.jbool{color:#9333ea}
```

- 容器 token 随页面主题变量（`--band-l`/`--line`/`--ink`/`--pri-d`），暗色主题自动跟随，不硬编码底色
- 行结构二选一：静态展示用 `.ln` 纯行；需要逐行入场动效时用 `.jl` 变体（`display:block;opacity:0;animation:rise .45s ease-out forwards;animation-delay:calc(var(--j)*90ms + .35s)`，行上标 `style="--j:n"`），reduced-motion 下 `.jl{animation:none;opacity:1}` 降级直显

## 3. 语法着色四色（硬约束）

| 元素 | class | 色值 | 形态 |
|---|---|---|---|
| key | `.jk` | `var(--pri-d)` | 加粗 |
| 字符串值 | `.jstr` | `#059669` | 常规 |
| 数字 | `.jnum` | `#ea580c` | 常规 |
| 布尔 / null | `.jbool` | `#9333ea` | 常规 |

markup 范式（key 与值均包 `<b class="…">`，标点不着色）：

```html
<pre class="code"><span class="ln">{</span><span class="ln">  <b class="jk">"deviceId"</b>: <b class="jstr">"ac-001"</b>,</span><span class="ln">  <b class="jk">"value"</b>: <b class="jbool">true</b>,</span><span class="ln">  <b class="jk">"ts"</b>: <b class="jnum">1715145600000</b></span><span class="ln">}</span></pre>
```

## 4. 可选联动（有图时启用）

- 行 → 图层联动：行 span 加 `data-hl="<图内节点 id>"`，hover 行时对应 SVG 节点高亮（JS：读 data-hl → getElementById → 加高亮 class）；用于 JSON 字段与架构图层级的对应讲解
- 字段语义着色例外：当某 key 承载叙事语义（如 desired/reported/delta 三态对照）时，可用语义 class 覆盖四色（橙/蓝/紫），但同一 deck 内语义色含义必须唯一
- 折叠承载：超长报文（>14 行）放 `<details><summary>` 内默认收起，展开态仍守本节排版范式

## 5. 禁止清单

- 禁引外部高亮库（highlight.js / prism 等）——自包含零依赖红线
- 禁整块单行紧凑 JSON、禁表格化 JSON（key 一列 value 一列）
- 禁截图代替文本 JSON（不可复制、不可着色、放大发糊）
- 禁在 JSON 块内加注释（`//` 非合法 JSON）；解释放块外 `.key`/`.kv` 组件
