# Terminal Window（CLI 外壳变体）

可选的整页皮肤，把任意图表包进一个仿终端窗口——带三个圆点的标题栏、一行 `$` 提示符、全篇等宽字体。用于开发工具发布、CLI 产品帖子，以及截图需要读起来像"终端"而不是"编辑级文档"的技术社交卡片。

这是**第二套固定皮肤**——token 表见 [style-guide.md § Terminal skin](style-guide.md#terminal-skin-opt-in-alternate)。它不继承 `onboarding.md` 的品牌 token，也不参与 light/dark 反转规则；无论宿主站点品牌如何，所有 terminal 示例都用同样的九个 token。

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
      <span class="sign">$</span> render --type loop
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

SVG 内部把默认 light/dark token 按 1:1 换成对应的 `terminal-*`：`paper` → `terminal-paper`、`ink` → `terminal-ink`、`muted`/`soft` → `terminal-muted`/`terminal-soft`、`accent`/`accent-tint` → `terminal-accent`/`terminal-accent-tint`。枢纽/焦点节点模式（唯一高亮元素用反色填充）依然适用。

## 字体排印

**全部等宽**——这是唯一这样做才正确的变体。完全弃用 Instrument Serif 与 Geist sans；页面标题用 mono 粗体，前缀 `# `（读作注释行）。眉标变为 shell 提示符：`$ ` 用 `terminal-accent`，命令用 `terminal-muted`。

每个文本角色比 `style-guide.md` 默认字号梯度**大 1–2px**（如 `node-name` 12px → 14px、`sublabel`/`arrow-label` 8–9px → 9–10px、枢纽标签 16px → 18px）。默认字号的等宽字体与被替换的 sans/serif 混排相比显得小，且这类卡片通常以社交信息流尺寸观看，不是全幅展示。

## 标题栏圆点

三个 10px 圆，macOS 风格。**1 强调色规则在这里同样限制用色**：一个圆点用 `terminal-accent`，另外两个用 `terminal-soft`。不要用红/黄/绿交通灯三色——那是第二、第三种色相，调色板禁止。

## 关键规则

- 不用纯黑（`#000000`）——用 `terminal-page`（`#0a0a0a`）/ `terminal-paper`（`#141414`）。与默认皮肤同一规则、同一理由：真黑在 OLED 与打印中会死黑成块。
- 只有一个强调色。图表需要第二个焦点元素时，用 `terminal-ink`（白）通过字重/字号强调，不用第二种颜色。
- 背景点阵纹理（如使用）保持 `rgba(255,255,255,0.06–0.08)`——若有似无的质感，不与标题栏外壳抢视觉。

## 何时使用

- 开发工具 / CLI 产品发布帖（npm 包、CLI flag、基于终端的工作流）。
- "这是给工程师的工具"本身就是信息一部分的技术社交卡片。
- 需要在深色模式为主的信息流（X、Discord、开发博客）中跳出来的截图。

## 何时不用

- 编辑级 / 长文帖子——改用默认 light 或 full-editorial 变体。
- `onboarding.md` 的品牌匹配输出——terminal 是固定皮肤，不做品牌 token 化。不要试图调和两者。
- 受众不是开发者、无法把 `$`/`#`/标题栏圆点读作外壳而非内容的任何图表。
