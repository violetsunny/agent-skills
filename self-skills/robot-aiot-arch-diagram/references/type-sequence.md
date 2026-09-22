# Sequence（时序图）

**最适合：** 请求/响应流、协议交换、多参与者随时间的交互、API 调用追踪、事故重建、带分支的认证/token 刷新路径。

## 布局约定
- 参与者（actor）为顶部水平一排的盒子。
- **生命线（Lifeline）**：从每个参与者向下延伸到底部的虚线垂直线。
- 消息：生命线之间的水平箭头；时间从上→下流动。
- **激活条（Activation bar）**：生命线上的窄矩形（`w=8`，muted 填充，0.8 发丝描边），跨越该参与者持有控制权的区间。嵌套调用时堆叠。
- 自消息：返回同一生命线的短 U 形环；标签在环右侧。
- 返回消息：**虚线**描边 + **实心** marker（绝不用开放箭头）。优先 muted；配对多跳堆栈时可选与发起调用同色。头条成功消息可用实线珊瑚色（见消息种类）。
- 珊瑚色用于主成功响应或头条消息——一个，最多两个。参与者焦点描边不计入珊瑚消息预算。
- 流程**分支**时（token 有效 vs 无效、重试、可选步骤），画**组合片段（combined fragment）**框——不要发明自由漂浮的 if/else 箭头簇。

## 消息种类

| 种类 | 描边 | Marker | 何时用 |
|---|---|---|---|
| Call（同步） | 实线 muted 或 link-blue | 实心 | 期待回复的请求 |
| Return | **虚线** muted（或与调用同色） | 实心 | 同步调用的回复——绝不实线 |
| Async / fire-and-forget | 虚线 muted | **开放**箭头 | 信标、事件、单向通知 |
| 头条成功 | 实线 accent（≤1–2 条消息） | accent 实心 | 仅主 happy-path 响应 |

### 开放箭头（async）

在 `<defs>` 中定义一次，仅用于 fire-and-forget：

```svg
<marker id="arrow-open" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polyline points="0 0, 8 3, 0 6" fill="none" stroke="#4f5d75" stroke-width="1.2"/>
</marker>
```

深色模式：描边 `#bfc0c0`（深色纸上的 muted）。不要填充开放 marker——空心箭头就是 async 信号。返回消息即使是虚线也保持**实心** marker。

## 组合片段（`alt` / `opt` / `loop`）

使用只跨越参与分支的生命线的矩形**框**。操作符标签为 Geist Mono、大写，放在框左上角的小 tab 内。框内时间仍从上→下流动。

### 框 primitive（共享）

```svg
<!-- Frame: light ink wash + hairline. Label tab top-left. -->
<rect x="X" y="Y" width="W" height="H" rx="4"
      fill="rgba(45,49,66,0.02)" stroke="rgba(45,49,66,0.22)" stroke-width="1"/>
<!-- Operator tab -->
<rect x="X" y="Y" width="40" height="16" rx="2"
      fill="#f5f5f5" stroke="rgba(45,49,66,0.22)" stroke-width="1"/>
<text x="X+20" y="Y+12" fill="#4f5d75" font-size="8"
      font-family="'Geist Mono', monospace" text-anchor="middle"
      letter-spacing="0.12em">ALT</text>
```

深色模式：框填充 `rgba(245,245,245,0.04)`，描边 `rgba(245,245,245,0.22)`，tab 填充 = 深色 `paper`（`#2d3142`），tab 文字 = 深色 `muted`（`#bfc0c0`）。

### 操作符

| 操作符 | 区域数 | 分隔线 | 守卫标签 |
|---|---|---|---|
| `opt` | 1 | 无 | tab 下方 `[if condition]`（Geist Mono 8px） |
| `alt` | **最多 2** | 横穿框的虚线水平发丝线 | 区域 1 标 `[guard]`；区域 2 标 `[else]`（或第二个守卫） |
| `loop` | 1 | 无 | tab 下方 `[for each item]` 或 `[retry ≤ 3]` |

### 守卫 + 分隔线 primitive

```svg
<!-- Guard: left-aligned inside the frame, mono -->
<text x="X+12" y="GUARD_Y" fill="#4f5d75" font-size="8"
      font-family="'Geist Mono', monospace" letter-spacing="0.04em">[token valid]</text>

<!-- alt region divider -->
<line x1="X+8" y1="DIV_Y" x2="X+W-8" y2="DIV_Y"
      stroke="rgba(45,49,66,0.20)" stroke-width="1" stroke-dasharray="4,3"/>
```

### 片段布局规则
- 框左右内缩距最外参与生命线中心 ≥12px（让激活条留在框内）。
- 区域内相邻消息 y 层级间 ≥24px（4px 网格）。
- 守卫位于 tab 下方约前 20px；该区域第一条消息在守卫基线下 ≥24px。
- 分隔线 y 在 4px 网格上；距上下消息 ≥16px 净空。
- 嵌套片段：**最多 1 层**。宁可拆两张图也不深嵌套。
- 默认：每图**一个**片段。第二个仅在两者都处于复杂度预算内时才允许。
- 珊瑚色在全图保持**一条**头条成功消息（通常是第一个 `alt` 区域内的 happy-path 返回，或 loop 外的最终成功）。不要给两个 `alt` 分支都上珊瑚色。

### 节徽章对齐
- 节/框标签徽章必须与其第一条消息箭头垂直居中：`badge_y = first_arrow_y - badge_height / 2`（如 height=18 徽章、首箭头 y=840 → badge_y = 831）。
- 在 Python list 中生成坐标时用变量强制该约束，绝不手写魔法数字：`sec_y = 840; badge_y = sec_y - 9  # height=18`。
- 向既有图表增量追加新节后，重新核对新节徽章与既有节的对齐——增量添加内容时最常见的回归。
- 片段操作符 tab 豁免：保持左上角语法。

### 范围外（不要发明）
- `par`、`critical`、`break`、`ref` 及其他 UML 操作符——需要时另开一轮。
- 参与者创建/销毁、found/lost 消息、duration 计时条。

## 复杂度预算（sequence 专属）
- 最大生命线数：5（与 design-system.md §7 相同）。
- 最大消息数（箭头）：12。
- 最大组合片段数：1（硬默认）；仅当每个都是单区域 `opt`/`loop` 时允许 2。
- 最大 `alt` 区域数：2。
- 最大片段嵌套深度：1。
- 最大珊瑚元素：2（片段图优先 1）。

超出就拆分：总览（happy path）+ 细节（失败/刷新路径）。

## 生命线 primitive
```svg
<line x1="CX" y1="TOP" x2="CX" y2="BOTTOM"
      stroke="rgba(45,49,66,0.20)" stroke-width="1" stroke-dasharray="3,3"/>
```

## 激活条 primitive
```svg
<rect x="CX-4" y="TOP" width="8" height="H"
      fill="rgba(45,49,66,0.06)" stroke="#4f5d75" stroke-width="0.8"/>
```

## 反模式
- 消息箭头*向上*指（时间倒流——绝不）。
- 激活条永不闭合。
- 标签压在另一条生命线上——缩短或把 y 移进间隙。
- 用泳道式 lane 替代生命线（不同语法）。
- 把 `if/else` 画成两簇自由漂浮箭头而**没有**片段框。
- `alt` 内嵌套 `alt`（拆成两张图）。
- 片段操作符标签用 Geist sans——必须 mono：`ALT` / `OPT` / `LOOP`。
- 两个 `alt` 分支都上珊瑚色。
- 框覆盖了片段内无消息的参与者。
- async fire-and-forget 用实心箭头（用开放 marker）。
- 返回消息用开放箭头（返回保持实心 + 虚线）。

## 示例
- minimal light（冷缓存 happy path）
- minimal dark
- full editorial
- special：bearer 调用 + `alt` 刷新（light）
- 同 special，dark
- 同 special，full editorial
