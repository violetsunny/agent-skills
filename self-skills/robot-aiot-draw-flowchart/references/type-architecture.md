# Architecture（架构图）

**最适合：** 系统总览、数据流图、集成地图、基础设施拓扑。

## 布局约定
- 按层级或信任边界分组组件（frontend → backend → data；public → private）。
- 主流向为左→右或上→下。选定一个并坚持。
- 先画箭头后画盒子，让 z-order 把连线压在组件后面。
- 1–2 个珊瑚色焦点节点：主集成点、主数据存储或关键决策节点。
- 虚线边界矩形标记区域（VPC、安全组、信任区）；标签放在边界线上方的 paper 色遮罩上。

## 连线样式

所有非水平/垂直连接**强制使用圆角直角（正交）连线**——离轴节点之间的斜线 `<line>` 是硬性不合格（见 design-system.md §6 强制连线规则）。`r=8` 的双弯肘路径：

```svg
<!-- right+down: from (x1,y1) to (x2,y2), mid = (x1+x2)/2 -->
<path d="M x1,y1 H mid-8 Q mid,y1 mid,y1+8 V y2-8 Q mid,y2 mid+8,y2 H x2"
      fill="none" stroke="…" stroke-width="1.2" marker-end="url(#arrow)"/>
```

right+up 时翻转垂直方向符号。仅当端点共享同一 x 或 y 时才用普通 `<line>`。箭头标签放在垂直段上，水平居中于 `mid`，垂直位于两个拐角之间。

**端口选择——垂直连线用 top/bottom 端口。** 目标明显在源的上方或下方时，从源的上/下边缘出发，进入目标的上/下边缘。用单弯 L 路径（水平 → 拐角 → 垂直入节点），不用左/右侧端口：

```svg
<!-- entering a node from its bottom (destination above source) -->
<path d="M x1,y_src H x2-8 Q x2,y_src x2,y_src-8 V y_dst"
      fill="none" stroke="…" stroke-width="1.2" marker-end="url(#arrow)"/>
```

左/右端口留给以水平行进为主的连接。以垂直为主的路径从侧面进入节点，看起来像箭头刺穿节点正面，而不是从上/下方到达。

**虚线路径——同样的布线规则。** 可选、返回、异步、被动流用 `stroke-dasharray="4,3"` 与更轻的线宽（`stroke-width="1"`）。应用与实线**相同的正交布线、端口选择与桥接/跨越规则**——虚线样式只传达语义权重，不是另一套布线语法。虚线路径与实线路径必须交叉时，桥接虚线那条（按定义它是较不重要的连接）。

**区域标签边距。** 区域眉标底部与第一个内含节点顶部之间留 ≥16px。区域矩形高度要能容纳这个头部间隙（zone `y` = node_top − 32；label mask `y` = zone_y + 4）。

## 交叉箭头 — bridge / hop

两条正交箭头必须交叉时，在交叉点给**较不重要**的箭头加一个小弧（hop/bridge）。较重要的箭头不间断绘制。

```svg
<!-- Horizontal hop over a vertical crossing at x=cx, on a line at y -->
<path d="M x1,y H cx-8 a 8,8 0 0,1 16,0 H x2"
      fill="none" stroke="…" stroke-width="1.2" marker-end="url(#arrow)"/>
```

`a 8,8 0 0,1 16,0` 是 SVG 弧：rx=ry=8、large-arc=0、sweep=1（视觉向上弯曲）、向右推进 16px——在交叉点上方形成 8px 半径的半圆凸包。垂直路径跨越水平线时用 `a 8,8 0 0,0 0,16`。

决定桥接哪条箭头：桥接语义上较不重要的那条（被动、次要、写回），或线宽较轻的那条（虚线、muted）。绝不同时桥接两条。

## 区域分组

服务同一层级或信任边界的 2+ 个节点用区域矩形分组——在箭头与节点**之前**绘制（z-order：bg → zones → arrows → nodes）：

```svg
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="rgba(45,49,66,0.02)" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>
<rect x="{label_x}" y="{y+4}" width="{label_w}" height="12" rx="2" fill="{paper}"/>
<text x="{label_cx}" y="{y+13}" fill="rgba(45,49,66,0.40)" font-size="7"
      font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.14em">LAYER</text>
```

规则：
- 第一个内含节点上方留 12–16px——眉标位于该边距内。
- 区域填充：`rgba(45,49,66,0.02)`（2% 墨色淡洗）。再重就会与节点填充抢视觉。
- 每图最多 3 个区域。更多就读起来像泳道图（改用那个类型）。
- 深色模式：`rgba(45,49,66,…)` → `rgba(245,245,245,…)`，不透明度不变；标签遮罩填充 = `paper`（深色）。

## 反模式
- 每个盒子都是珊瑚色（"这个也重要"）——层级崩塌。
- 上下文已明确单向时使用双向箭头。
- 图例漂浮在图表区域内部。

## 示例
- minimal light
- minimal dark
- full editorial
