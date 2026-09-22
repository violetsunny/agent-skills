# 可选动画

动画用于解释一张已经完整的静态图；它从不补齐缺失的含义。仅当动效被明确要求，或能实质澄清顺序、累积、评估、包含或传播时，才加载本 reference。否则使用 `none` 模式并交付静态 HTML。

## 模式

每张图用 `data-motion-mode="none|reveal|step|loop"` 选定一种模式。

| 模式 | 行为 | 控件 / 实现 | 用途 |
|---|---|---|---|
| `none` | 完整稳定图形 | 无 JavaScript | 默认、打印、截图、导出、reduced-motion 回退（播放控件不可用） |
| `reveal` | 一次确定性自动播放，结束于完整状态 | ≤5s 用纯 CSS；否则用作用域控制器 | 简短的顺序讲解；绝不自动重播 |
| `step` | 可暂停的语义状态 | 最小内联 JS 提供 Play、Pause、Replay、Previous、Next | 教学、对比、策略追踪 |
| `loop` | 一个装饰性 token 循环，不改变含义 | 默认纯 CSS | 安静的流动提示；周期 ≥3s |

只有 `loop` 允许重复。队列状态、打字、字段值、策略结果、包含关系与审计条目用 `reveal` 或 `step`，且必须结束于完整状态。

`reveal` 是唯一获准的自动播放模式：仅在动效被明确要求时可于初次加载运行一次，之后保持完整状态。视口重入或无显式 Replay 动作时绝不重新播放。

## 静态优先增强契约

1. **源即完整。** 每个语义节点、标签、连线、状态与结果在增强前都已在 HTML/SVG 中可见。只有 `.motion-ready` 之下的选择器可以隐藏或变换它们。
2. **稳定捕获。** 初始 `data-frame="static"`、`?motion=static`、打印、无 JS、独立 SVG 导出都呈现完整帧，并隐藏控件与装饰 token。不得在任意延迟后捕获。
3. **CSS 负责呈现。** 外观与位移用 CSS transitions/keyframes。最小内联 JavaScript 仅允许：绑定显式控件、更新 step/state 属性、调度确定性步骤、更新专用 live-status 区域。禁止 fetch、markup 注入、路径测量、修改语义图表标签或值。
4. **单一时钟。** 使用 `--motion-fast: 160ms`、`--motion-step: 480ms`、`--motion-hold: 720ms`、`--motion-total` ≤ `8000ms`；延迟由整数步骤推导。禁止随机数、弹簧物理、transition 事件计时。
5. **显式顺序。** 用 `data-motion-item data-step="N"` 标记条目，N 取整数 1–8。DOM 顺序跟随叙事顺序。每步最多两个条目入场。
6. **稳定终点。** 完成时呈现全部条目并设 `data-frame="end"`。Replay 先重置到第 0 步。Pause 清除待触发 timer，resume 从同一步继续。
7. **作用域状态。** 控件只作用于最近的 `[data-motion-root]`；ID、timer、live region、步骤状态绝不跨图边界。
8. **失败安全启动。** JavaScript 仅在控件绑定且初始渲染成功后才添加 `.motion-ready`。在此之前脚本出错，完整源内容保持可见。

## 语义基元

除颜色外，每个基元都必须有文本、计数、符号、图案或轮廓。

| 基元 | 机制 | 静态 / reduced-motion 结果 | 上限 |
|---|---|---|---|
| **Path draw**（路径绘制） | `pathLength="1"` 的装饰性复制路径 + dash offset 动画 | 带标签的基础连线保持可见 | ≤2 条路径；同时 1 条活动 |
| **Staggered reveal**（分阶段揭示） | `data-motion-item` + opacity/translate ≤8px | 所有阶段可见 | ≤8 步、12 个条目 |
| **Queue counter**（队列累积） | 稳定槽位；条目揭示加可见数字计数 | 最终队列与计数可见 | ≤5 个条目；禁止重排 |
| **Typing / field population**（打字/字段填充） | 完整可访问字符串；裁剪式装饰覆盖层或按行揭示并带标签 | 完整文本/字段一次性可见 | ≤32 个打字字符或 6 个字段 |
| **Policy evaluation**（规则评估） | 有序规则行 + 文本状态 + 当前行轮廓 | 每个状态与结果可见 | 3–6 条规则；2 条 trace |
| **Flow token**（流动 token） | 固定路径上的 `aria-hidden` token | token 隐藏；连线保留 | 1 个 token；周期 ≥3s |
| **Containment**（包含） | 先揭示子元素，再显示持久的带标签边界 | 子元素与边界可见 | 1 次边界过渡 |
| **Audit append**（审计追加） | 按时间顺序揭示行；时间戳/序号稳定 | 完整有序日志可见 | ≤5 行追加 |

不要给布局坐标、连线路径、`viewBox`、节点尺寸或语义文本加动画。避免缩放、视差、弹跳、抖动、发光、粒子与无限闪烁。

```css
:root {
  --motion-fast: 160ms;
  --motion-step: 480ms;
  --motion-hold: 720ms;
  --motion-total: 3600ms; /* five steps × hold; set this per diagram */
  --motion-ease: cubic-bezier(.2,.8,.2,1);
}
.motion-ready [data-motion-item] {
  opacity: .12;
  transform: translateY(8px);
  transition: opacity var(--motion-step) var(--motion-ease),
              transform var(--motion-step) var(--motion-ease);
}
.motion-ready [data-motion-item].is-visible,
.motion-ready[data-frame="end"] [data-motion-item] {
  opacity: 1;
  transform: none;
}
[data-motion-controls][hidden] { display: none !important; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
  [data-motion-item] { opacity: 1 !important; transform: none !important; }
  [data-motion-decorative] { display: none !important; }
  [data-motion-controls] { display: none !important; }
}
@media print {
  [data-motion-controls], [data-motion-decorative] { display: none !important; }
  [data-motion-item] { opacity: 1 !important; transform: none !important; }
}
```

## 交互控件与键盘

每个交互式 `step` 图都在 SVG 之外提供 **Play、Pause、Replay、Previous、Next** 原生按钮。使用 `data-motion-action="play|pause|replay|prev|next"`、≥44×44px 触达目标、可见焦点、不可用动作的 disabled 状态、play/pause 状态的 `aria-pressed`。

焦点位于 motion root 内时：`ArrowRight` 前进、`ArrowLeft` 后退、`Home` 重置、`End` 直达结束、`Space` 在焦点不位于原生控件上时切换播放/暂停、无修饰键的 `R` 重播。Control、Command 或 Alt 按下时绝不拦截 `R`。不从输入框、链接或无关区域抢键。帧变化时绝不移动焦点。

提供可见的使用说明与作用域化的 `role="status" aria-live="polite" aria-atomic="true"`。live region 放在 motion root 内、`[data-motion-controls]` 外，确保 reduced/static 状态隐藏控件时不会连带隐藏播报。只播报用户动作（如"第 3/5 步：首次分歧"）；不播报自动播放的每一帧。控件只作用于最近的 `[data-motion-root]`。

使用 [`assets/template-motion.html`](../assets/template-motion.html)，不要另发明控制器。其内联控制器是可执行实现契约：逐字复制该 script 主体。皮肤 linter 会拒绝被修改或额外新增的控制器，即使它们带有 `data-diagram-controls`。替换图表内容与 slug 前缀 ID，但保留控制器及其 state/control 属性。

## Reduced motion、颜色与无障碍

- `prefers-reduced-motion: reduce` 以完整静态帧初始化，禁用并隐藏所有播放控件，隐藏装饰性动效，暴露 `data-motion-state="reduced"` 及"播放不可用"的状态文本。绝不在完整帧旁显示部分步骤的播报。
- SVG 的 `<title>` 与 `<desc>` 描述完整含义，而不是动画。交互说明保持为可见的 HTML 文本。
- 装饰性覆盖层带 `aria-hidden="true" focusable="false"`。语义文本在无障碍树中只出现一次。
- 状态绝不仅靠颜色：策略用符号 + `PASS/FAIL/SKIPPED/NOT REACHED`；队列显示计数；活动阶段用编号/标签/轮廓。
- 任何元素每秒闪烁或亮度变化不超过 3 次。

## 复杂度与确定性时序

动效不提高静态图预算：≤8 个语义步骤（目标 3–6）、≤12 个标记条目、≤2 个同时揭示、≤2 条绘制路径、1 个 flow-token 循环、160–600ms 过渡、400–1200ms 停留、≤24px 位移、自动播放总时长 3–8s。

声明 `data-step-count`；不要从 transition 事件推断步骤。`--motion-total` 设为步骤数 × `--motion-hold`，保持在 8 秒预算内。每个 root 只用一条 `setTimeout` 链，其停留时长由 `--motion-hold` 推导，在 Pause/Replay/页面隐藏时以及渲染完最后一步后立即清除，语义播放绝不用 `setInterval`。`document.visibilityState` 变为 hidden 时暂停，事后不补播。`?motion=step&step=N` 仅当 `N` 是 0 到 `data-step-count` 之间的非负十进制整数时，才暴露零时长的精确帧供视觉回归；缺失、小数、负数、超范围的值一律保持正常播放。

终态捕获契约是同步的：`?motion=static`、`<html data-motion="static">` 或模式 `none` 暴露每个语义条目、隐藏控件与装饰覆盖层、设置 `data-frame="static"`。捕获前等待 `document.fonts.ready`。同一 URL、视口、字体、设备缩放下两次捕获必须像素级一致；禁止随机延迟、生成式 ID、时钟、运行时路径测量。

## 导出与验证

PNG 与 SVG 导出是静态终态产物，除非用户明确要求某个具名步骤。捕获前打开 `?motion=static`，等待 `document.fonts.ready`，断言 `data-frame="static"`。SVG 提取会省略 HTML 控件与脚本；源内可见的语义标记保证结果完整。

运行：

```bash
python3 scripts/self_check.py path/to/animated-diagram.html
```

`self_check.py` 是日常门禁（canonical 运动控制器、外部请求、无障碍契约）；`verify-motion.py`/`lint-skin.py` 是完整校验器，随包分发，深度检查时用（见 `doctor.md`）。

校验器检查：模式/状态声明、步骤连续性、动效预算、SVG 命名完整性、无 JS 源可见性、装饰元素无障碍、完整控件集、live status、reduced-motion/打印 CSS、键盘处理、页面隐藏暂停、有界 static/test 覆盖、最后一步立即停止、canonical 控制器逐字一致。其对抗性测试对 canonical 模板注入变异，证明每类失败都会被拒绝。

然后在浏览器中验证：

1. 禁用 JavaScript：完整图表保持可见且有含义。
2. 模拟 `prefers-reduced-motion: reduce`：终态完整，播放控件隐藏且禁用，DOM 状态显示播放不可用。
3. 只用键盘：Tab 到达每个原生控件；Enter/Space 激活；Left/Right/Home/End 步进且不移动焦点。
4. 暂停、恢复、重播两次：顺序与终态一致。
5. `document.fonts.ready` 后捕获 `?motion=static` 两次：像素稳定。
6. 打印预览加 PNG/SVG 导出：控件与装饰 token 缺席，所有语义标签与关系保留。

## 反模式

- 未被请求的自动播放、唯一获准的 `reveal` 之外的自动播放、视口重入重播、语义内容无限循环。
- 无 JS 或 reduced-motion 下的空白/不完整帧。
- 用动效拯救过密或无标签的静态图。
- pass/fail、队列满度或结果仅靠色相编码。
- 远程脚本、通用应用逻辑、运行时几何计算、重复的语义文本。
- 用墙钟延迟捕获，而不是显式 static 覆盖。
