# Layer Stack（层级栈）

**最适合：** OSI 模型、CSS 层叠、上下文层级、技术栈、抽象层、存储层次。

## 布局约定
- 水平条带垂直堆叠。每层是一个全宽矩形（同 x、同宽）。共 4–6 层。
- 层高 56–72px，宽通常 800–880px，位于 1000px viewBox 内。
- 每行包含（左→右）：
  1. **索引标签**在最左（`L3`、`07`、`APPLICATION`）——Geist Mono 8–9px 眉标。
  2. **层名**在中偏左——Geist 14–16px 600。
  3. **子标签 / 备注**在最右——Geist Mono 9–10px muted。
- 层间边框：1px 发丝线 `rgba(45,49,66,0.12)`。外轮廓 1px ink 或 muted。
- 填充：交替淡色（paper / paper-2）或全部 paper 配发丝分隔线，二选一。选定一个并坚持。
- 方向指示器放在左侧边距（栈外）：小上/下箭头 + Geist Mono 标签（`abstraction ↑`、`packets ↓`）。
- 珊瑚色用在**一个**焦点层上（描边 + 淡色填充）——瓶颈层、pay-rent 层、正在讨论的那层。

## 反模式
- 各层实际并非层级关系（改用 swimlane 或 architecture）。
- 编号跳跃（L3 与 L5 之间缺 L4 且无说明）。
- 每层不同颜色——层级不可见。
- 层高不一致且无理由。

## 示例
- minimal light
- minimal dark
- full editorial
