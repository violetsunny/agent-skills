# Nested Containment（嵌套包含图）

**最适合：** 用包含表达层级——scope 边界、agent 规则文件级联（如 AGENTS.md cascade）、trust zone、文件夹嵌套、blast radius。外层 = 更宽泛，内层 = 更具体。

## 布局约定
- 3–5 个圆角矩形（`rx=8`）嵌套，内边距一致（推荐水平 24–32px、垂直 32–36px）。
- 每层在左上角用 Geist Mono eyebrow 风格标注（7–8px，letter-spacing 0.14em）。标签置于环顶边框上的 paper 色遮罩矩形之上。
- 描边层级：外环 faint（`rgba(..,0.30–0.45)`），向内渐进为 muted、ink，最内焦点用 coral。
- 填充不透明度由外向内递增：`rgba(..,0.015)` → `rgba(..,0.025)` → 最内层 accent-tint。
- 可选：每层内放文件图标字形（折角矩形），暗示 scope 内容。
- 斜体 Instrument Serif 旁注（见 `references/primitive-annotation.md`）——最多 1–2 个。

## 反模式
- 超过 6 层（信息向内消失）。
- 层间 padding 不规则——未对齐的嵌套看起来像失误。
- 环内放不属于层级的内容——改用并列图。
- coral 用在多个层级——层级随之坍塌。

## 示例
- minimal light
- minimal dark
- full editorial
