# Terminal Window（CLI 窗框变体）

可选的整页皮肤，把任意图表包进一个仿终端窗口——带三个圆点的标题栏、一行 `$` 提示符、全局等宽字体。用于开发工具发布、CLI 产品文章与技术社交卡片：截图需要读作"终端"而不是"编辑风文档"的场合。

这是**第二套固定皮肤**——token 表见 [style-guide.md § Terminal 皮肤](style-guide.md#terminal-皮肤opt-in-备选)。它不继承 `onboarding.md` 的品牌 token，也不参与 light/dark 反色规则；无论宿主站点品牌如何，所有 terminal 示例都用同一组九个 token。

## 语法

```html
<div class="terminal">
  <div class="titlebar">
    <div class="dot accent"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="titlebar-name">loop.sh — self-improving-loop</div>
  </div>
  <main class="frame">
    <p class="prompt">
      <span class="sign">$</span> diagram-design render --type loop
    </p>
    <h1># The self-improving loop</h1>
    <svg>...</svg>
  </main>
</div>
```

```css
body {
  background: var(--terminal-page);
}
.terminal {
  background: var(--terminal-paper);
  border: 1px solid var(--terminal-border);
  border-radius: 12px;
}
.titlebar {
  background: var(--terminal-bar);
  border-bottom: 1px solid var(--terminal-border);
}
.dot {
  background: var(--terminal-soft);
}
.dot.accent {
  background: var(--terminal-accent);
}
```

SVG 内部把默认 light/dark token 1:1 换成对应 `terminal-*`：`paper` → `terminal-paper`、`ink` → `terminal-ink`、`muted`/`soft` → `terminal-muted`/`terminal-soft`、`accent`/`accent-tint` → `terminal-accent`/`terminal-accent-tint`。hub/焦点节点模式（唯一高亮元素用反色填充）依然适用。

## 字体排印

**全部等宽**——这是唯一允许这样做的变体。完全弃用 Instrument Serif 与 Geist sans；页面标题用 mono 加粗，前缀 `# `（读作注释行）。eyebrow 变成 shell 提示符：`$ ` 用 `terminal-accent`，命令用 `terminal-muted`。

每个文本角色比 `style-guide.md` 默认字级**上调约 1–2px**（如 `node-name` 12px → 14px、`sublabel`/`arrow-label` 8–9px → 9–10px、hub 标签 16px → 18px）。等宽字体在默认字号下相对它替代的 sans/serif 混排显得偏小，且这类卡片通常以社交信息流尺寸观看，不是全幅展示。

## 标题栏圆点

三个 10px 圆点，macOS 风格。**1 强调色规则在这里同样封顶**：一个点用 `terminal-accent`，另外两个用 `terminal-soft`。不要用红/黄/绿交通灯三件套——那是第二、第三个色相，调色板禁止。

## 关键规则

- 禁纯黑（`#000000`）——用 `terminal-page`（`#0a0a0a`）/ `terminal-paper`（`#141414`）。与默认皮肤同规则同原因：真黑在 OLED 与打印中会死黑一片。
- 只有一个强调色。图需要第二个焦点元素时，用 `terminal-ink`（白）通过字重/字号强调，不引入第二个颜色。
- 背景点阵图案（如使用）保持 `rgba(255,255,255,0.06–0.08)`——若有若无的纹理，不与标题栏窗框争抢视觉。

## 何时使用

- 开发工具/CLI 产品发布文章（npm 包、CLI flag、基于终端的工作流）。
- "这是给工程师的工具"本身就是信息一部分的技术社交卡片。
- 需要在深色模式为主的信息流（X、Discord、dev blog）中跳出来的截图。

## 何时不用

- 编辑风/长文文章——改用默认 light 或全编辑风变体。
- `onboarding.md` 的品牌匹配输出——terminal 是固定皮肤，不做品牌 token 化。不要试图调和两者。
- 受众不会把 `$`/`#`/标题栏圆点读作窗框（而非内容）的任何图表。
