# 逐页交互 HTML 编写规则

本文件定义 Phase 4 逐页交互 HTML 的编写规则。

## 总体结构

最终交付物为单个 HTML 文件，包含所有页面：

> 规范副本：`templates/deck-skeleton.html` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>演示标题</title>
  <style>/* 全局样式 + token */</style>
</head>
<body>
  <div class="deck">
    <section class="slide active" data-index="0"><!-- Page 1 --></section>
    <section class="slide" data-index="1"><!-- Page 2 --></section>
    <!-- ... -->
  </div>
  <nav class="controls"><!-- 导航控件 --></nav>
  <script>/* 翻页 + 动画 + 交互 */</script>
</body>
</html>
```

## 形态选择与批量节奏

1. 默认形态为单文件（"合并为单文件"节）；仅上层 workflow 明确要求时才走 `INDEX.html` + `pages/` 多页形态（SKILL.md 硬约束 10），细则见"多页形态（INDEX + pages/）细则"节
2. deck 页数较多且风格基调尚未经用户确认时，禁止从第 1 页直接写到最后一页：先做 2 页代表性 showcase（选视觉结构差异最大的两页，通常是封面 + 核心内容页）交用户确认，锁定视觉语法（版式/字体/色彩/间距/中英双语比例），再批量铺开其余页——方向性返工成本封顶在 2 页，不放大到全套 N 页
3. 触发阈值、showcase 页选择标准、确认点与未过处置以下列两处真源为准，本文件不重述：
   - PPT 汇报语境：`robot-aiot-leadership-ppt-workflow` 的 `phase4-page-authoring.md`"两页 showcase 门"
   - Web 演示语境：`robot-aiot-web-presentation-workflow` 的 `phase2-pagination.md`"两页 showcase 确认门"

## Token 体系

在 `<style>` 根级定义语义 token：

```css
:root {
  --primary-color: #...;
  --secondary-color: #...;
  --tertiary-color: #...;
  --surface-color: #...;
  --surface-muted: #...;
  --text-primary: #...;
  --text-secondary: #...;
  --outline-color: #...;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
}
```

主色来自 Phase 3 首页架构图，其余 token 按 `design-system-standards.md` 规则派生。

## 画布约束

1. 固定 `1920x1080`，不响应式
2. 内容区四周留 `32-48px` 安全边距
3. 使用绝对定位或 CSS Grid/Flexbox 布局
4. 元素不重叠、不溢出
5. 画布外必须包一层 scale-to-fit 视口自适应壳：浏览器任意窗口尺寸下画布等比缩放居中、无滚动条完整可见；`1920x1080` 视口时 scale=1，headless 截图与下游消费不受影响
6. 例外——竖版社交 deck 画布：小红书图文/社交轮播类交付形态可用竖版 3:4 画布，标准 `810x1080`（与 `content-imagery-and-infographic.md` 竖版画布规则对齐）；仅此形态豁免第 1 条的 `1920x1080`，本节其余条款照常适用，scale-to-fit 壳的缩放分母改为画布实际宽高（`Math.min(innerWidth/W,innerHeight/H)`）。用户未点名竖版 deck 时一律 `1920x1080`

标准实现（本文件结构中 `.canvas` 即 `.deck` 容器）：

```html
<div class="fit-viewport"><div class="canvas">…</div></div>
<script>
(function(){var c=document.querySelector('.canvas');function fit(){var s=Math.min(innerWidth/1920,innerHeight/1080);c.style.transform='scale('+s+')';}addEventListener('resize',fit);fit();})();
</script>
```

```css
html,body{height:100%;overflow:hidden}
.fit-viewport{height:100vh;display:flex;align-items:center;justify-content:center}
.canvas{transform-origin:center center;flex-shrink:0}
```

## 翻页实现

### 页面切换

当前页 `.active` 可见，其余隐藏但保留 DOM：

```css
.slide {
  position: absolute;
  inset: 0;
  visibility: hidden;
}
.slide.active {
  visibility: visible;
}
```

隐藏规则挂 `.js` 前缀类（JS 首行加到 `documentElement`），head 内配 `<noscript>` 顺序流回退样式：禁/受限 JS 环境降级为顺序可读全文，白屏判交付失败。入场动画同规则，触发用 `setTimeout` 不用 `requestAnimationFrame`（后台标签页 rAF 暂停）。

不使用 `display: none`，否则 View Transition 无法捕获旧帧。

### View Transition

```js
function goTo(index) {
  if (!document.startViewTransition) {
    swapSlide(index);
    return;
  }
  document.startViewTransition(() => swapSlide(index));
}
```

不支持时降级为 class 切换 + CSS transition。

翻页落定后（View Transition 完成回调或降级 transition 结束）派发 `slidechange` 事件：

```js
document.dispatchEvent(new CustomEvent('slidechange', {
  detail: { index: current, reason } // reason: 'key' | 'click' | 'hash' | 'auto'
}));
```

页内 ambient 动画、数字滚动、自动推进定时器一律订阅该事件启停——这是"非活跃页面无残留定时器"的落地机制；禁止定时器自行轮询可见性。

### 键盘绑定

```js
document.addEventListener('keydown', (e) => {
  if (e.target.closest('input,textarea,select,[contenteditable]')) {
    if (e.key === 'Escape') e.target.blur();
    return; // 输入态除 Escape 外不触发翻页
  }
  if (/^[1-9]$/.test(e.key)) { goTo(Math.min(+e.key - 1, totalSlides - 1)); return; }
  switch (e.key) {
    case 'ArrowRight': case ' ': case 'PageDown': next(); break;
    case 'ArrowLeft': case 'PageUp': prev(); break;
    case 'Home': goTo(0); break;
    case 'End': goTo(totalSlides - 1); break;
    case 'r': case 'R': goTo(0); break; // 重置回首页
    case 'f': case 'F': toggleFullscreen(); break;
    case 'Escape': exitFullscreen(); break;
  }
});
```

### 点击区域

右半区点击下一页，左半区点击上一页，底部进度条可跳转。
点击热区不遮挡可交互内容。
触屏改三分区：左右 1/3 翻页、中间 1/3 死区（持握防误触）；鼠标保持左右半区。

## 入场动画

页面变为 `.active` 后，子元素按 `data-enter-order` 依次入场：

```html
<h1 data-enter-order="1">标题</h1>
<p data-enter-order="2">结论</p>
<div data-enter-order="3">图表区</div>
```

CSS：

```css
.slide .enter {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 500ms, transform 500ms cubic-bezier(0.4, 0, 0.2, 1);
}
.slide.active .enter.entered {
  opacity: 1;
  transform: translateY(0);
}
```

JS 在页面激活后按 order 依次添加 `.entered` 类，间隔 `100-200ms`。

## 数据动效

### 数字滚动

仅在元素首次进入视口或页面激活时触发一次：

```js
function animateNumber(el, target, duration = 1200) {
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(target * eased).toLocaleString();
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

### 进度条填充

填充层固定 `width:100%`，用 `transform: scaleX(0→PCT)` + `transform-origin:left`，transition 800ms cubic-out；不 transition width（触发 layout，违反性能红线）。

### 图表动画

SVG 路径用 `stroke-dasharray` + `stroke-dashoffset`；柱状图从底部生长；延迟 `300ms` 开始。

## 图表引用

优先内联 Phase 3 生成的图表 HTML 中的 SVG 内容，或通过 iframe/object 引用。
不修改图表节点坐标、结构关系和数据语义。

## 素材图网格与 lightbox

素材图（截图/照片佐证）规则：

1. 原图高清落盘：素材图按原始分辨率复制进产物 `assets/`，禁止降分辨率/降质（`sips -Z` 缩边、thumbs 平铺小图均禁止）；清晰度靠格位尺寸控制——压的是占位空间，不是图片
2. 固定格位网格平铺：grid 定列数、格位同宽同高、容器 `overflow:hidden`、区内任何情况无滚动条
3. `object-fit` 归一为 `contain` 或 `cover`，不拉伸变形
4. 每图一行 caption；单页 ≤4 张
5. 多页形态素材图用相对路径引用，不 base64 内联；单文件 deck 形态才内联，且需控制总体积；相对路径深度按页文件相对 `assets/` 的层级定（页在三层子目录即 `../../../assets/`），写毕用静态检查或开页验证资源不 404

交互页面另加 lightbox 点击放大：纯原生零依赖，点击缩略图弹出全屏遮罩层显示放大图，Esc 键或点击遮罩关闭，打开时 body 锁定滚动。

参考实现：

```html
<div class="lightbox" id="lightbox"><img alt=""></div>
```

```css
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;z-index:999}
.lightbox.open{display:flex}
.lightbox img{max-width:92vw;max-height:92vh;object-fit:contain}
```

```js
(function(){
  var lb=document.getElementById('lightbox'),big=lb.querySelector('img');
  document.querySelectorAll('.img-grid img').forEach(function(t){
    t.addEventListener('click',function(){big.src=t.src;lb.classList.add('open');document.body.style.overflow='hidden';});
  });
  function close(){lb.classList.remove('open');document.body.style.overflow='';}
  lb.addEventListener('click',close);
  addEventListener('keydown',function(e){if(e.key==='Escape')close();});
})();
```

## 品牌 logo 声明

deck 需要常驻公司/产品 logo 时，声明一次、全 deck 生效，不逐页手放：

1. **常驻元素挂在 slide 同级**：logo 不属于任何 `.slide`，绝对定位在 `.canvas` 四角之一（内缩沿用画布安全边距 32-48px），跨页持续存在：

```html
<div class="canvas">
  <img class="deck-logo" src="data:image/svg+xml;base64,…" alt="品牌名">
  <section class="slide active">…</section>
</div>
```

```css
.deck-logo{position:absolute;right:40px;bottom:40px;height:44px;width:auto;opacity:.9;z-index:5;pointer-events:none}
```

2. **logo 源零外部请求**：内联 `<svg>` 优先，其次 base64 data URI；禁止 `<img src="logo.svg">` 外链文件（违反单文件自包含硬约束）
3. **按页豁免走纯 CSS**：封面与自带品牌元素的全幅图页不显示 logo——页面加 `data-no-logo` 标记，用 `:has()` 豁免，无需 JS：

```css
.canvas:has(.slide.active[data-no-logo]) .deck-logo{opacity:0}
```

4. **不抢戏**：高度 40-48px、不透明度 ≤ 0.9、`pointer-events:none` 不挡翻页热区；不与页码/进度条及页内内容重叠，冲突时换角或对该页豁免；`alt` 写品牌名（装饰性内联 SVG 用 `aria-hidden="true"`）
5. **打印态逐页 logo**：绝对定位的 `.deck-logo` 在打印展开时只锚定一次（落单页或消失），带 logo 的 deck 导出 PDF 必丢；print 态隐藏 logo 元素，改由伪元素逐页绘制（打印中一个 `.slide` 恰好一页，`data-no-logo` 豁免延续）：

```css
@media print {
  .deck-logo { display: none !important; }
  .slide:not([data-no-logo])::after {
    content: ""; position: absolute; right: 40px; bottom: 40px;
    width: 88px; height: 44px;              /* 按 logo 宽高比调整 */
    background-image: var(--logo-print);    /* 编写期声明 --logo-print: url("data:image/svg+xml;base64,…")，与 .deck-logo 同源 */
    background-repeat: no-repeat; background-position: right bottom; background-size: contain;
  }
}
```

## 共享背景层

跨页持续的视觉状态（底色渐变、氛围画布、grain/暗角）用"共享背景层 + 透明内容层"，不要每页各带一份不透明背景：

```html
<div class="canvas">
  <div id="bg" class="full-bleed"></div>    <!-- 常驻背景，不属于任何页 -->
  <section class="slide active">…</section> <!-- 内容层背景透明 -->
</div>
```

```css
.full-bleed { position: absolute; inset: 0; }
.slide { background: transparent; }
```

规则：

1. 背景层不随翻页显隐，存在整个 deck 生命周期；全局色调偏移、暗角、grain 只在共享层驱动一次，不在每页重复实现
2. 背景层必须 `position:absolute; inset:0` 自己撑满——它不参与翻页布局，塌成 0 高时上面画的任何东西都不可见（此模式最常见错误）
3. 氛围画布 FX 仍走 `generative-art-and-canvas.md` 启停契约；共享背景层只解决"跨页连续视觉状态"
4. 页面容器自身不加 display/visibility 动画（与翻页机制的显隐逻辑竞争），要动就动页内子包装

## 禁用 emoji：Unicode 文字符号与内联 SVG

禁 emoji 的两条硬理由：

1. **导出豆腐块**：headless Chromium 默认不带彩色 emoji 字体，`--screenshot` 与导出 PDF 时 emoji 渲染为空方框，且不报任何异常——与"静默布局坑"同类，自动化抓不到
2. **色彩失控**：emoji 自带各平台彩色字形，不走 token 体系，与 deck 色彩纪律冲突；活泼气质与汇报场景不合

替代物两级：

1. **Unicode 文字符号**：属文本，继承 `currentColor` 与字号，色彩随 token 可控；只用下方对照表内、字体栈覆盖已确认的常见符号
2. **内联 SVG 线性图标**：物件类图标一律用它，`stroke="currentColor"`、线宽 1.5-2px，与页面线宽语言对齐；零外部请求，内联或 base64（同"品牌 logo 声明"条 2）

对照表（高频 emoji 码位 → 替代物）：

| 禁用符号（码位） | 语义 | 替代 |
|---|---|---|
| U+2705 / U+2611 | 正确、完成 | ✓（U+2713），重要场景用加粗 ✓ |
| U+274C / U+274E / U+1F6AB | 错误、禁止 | ✕（U+2715） |
| U+2B50 / U+1F31F | 高亮、精选 | ★（U+2605）或 ✦（U+2726） |
| U+27A1、U+25B6 带 U+FE0F | 方向、下一步 | →（U+2192）/ ▸（U+25B8） |
| U+1F534、U+2022 带 U+FE0F | 列表圆点 | ·（U+00B7）/ ‣（U+2023） |
| U+26A0 / U+2757 | 警告 | 内联 SVG 三角感叹号，或文案改"注意：" |
| U+1F4E7 / U+1F4F1 / U+1F50D / U+1F4CA / U+23F1 | 物件图标（邮件/手机/搜索/图表/计时） | 内联 SVG 线性图标，或直接文字（"Email · 23"而非图标+数字） |
| U+1F389 / U+1F525 / U+1F4A1 | 氛围符号（庆祝/火热/点子） | 直接删除；氛围由版式与色彩承担，不靠符号 |

规则：

1. deck 全部文案禁 emoji：上屏文字、`.notes` 话术、caption、`alt`、按钮文案都算
2. 文字符号只取对照表白名单；生僻符号（✦ ✧ 等）交付前实测字体栈覆盖，任一平台缺字形即降级为内联 SVG
3. 不用 icon font（SKILL.md 硬约束 11 禁外部字体）；不为图标引任何外部请求
4. 交付前自检加"上屏零 emoji"断言（浏览器控制台或 headless 跑，批量走 `scripts/emoji_audit.py`；禁段覆盖 emoji 主块与 emoji 变体选择符 U+FE0F，白名单文字符号 ✓ ✕ ★ ✦ → ▸ · ‣ 不在其中）：

```js
(function () {
  var RE = /[\u{1F000}-\u{1FAFF}\u{FE0F}\u{203C}\u{2049}\u{231A}\u{231B}\u{23E9}-\u{23FA}\u{2611}\u{26A0}\u{2705}\u{274C}\u{274E}\u{27A1}\u{2B50}\u{2B55}]/u;
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  var hits = [];
  while (walker.nextNode()) {
    var n = walker.currentNode;
    var p = n.parentElement;
    if (p && !p.closest('script,style') && RE.test(n.nodeValue)) hits.push(n.nodeValue.trim());
  }
  console.assert(hits.length === 0, '上屏 emoji 残留: ' + hits.join(' | '));
})();
```

## 静默布局坑

以下错误不报异常、自动化检查抓不到，表现为"元素永远不出现"或"渲染里被裁掉"：

1. **transform 对 inline 元素无效**：scaleX/translate 在 `display:inline` 的 span 上是 no-op；被动画元素必须 block/inline-block/flex-item 且有真实宽高——auto 宽 0px 元素做缩放等于永远不可见
2. **峰值尺寸留净空**：脉冲/过冲装饰（yoyo scale、back-out 过冲）按最大帧定位而非静止帧，且不跨 `overflow:hidden` 边界，否则被裁或压住邻居
3. **先建静态终态**：先用 HTML/CSS 搭出可见的静态终态，再往上加动画——终态本身错了，动画只会更晚暴露问题
4. **离屏 canvas 测文本**：字号自适应宽度时用离屏 canvas `ctx.measureText` 测量后二分字号，不写进页面再读回（每次读回都触发 reflow）
5. **正文不用 `<br>` 断行**：强制换行忽略实际渲染字宽，行已自然换行时多出一折造成重叠；用 max-width 控制自然换行。例外：短展示标题刻意每词一行
6. **`.notes{display:none}` 漏写**：话术容器只在 HTML 挂了 class 而 CSS 规则漏写时，话术全文泄漏进观众视图且不报任何异常；CSS 规则必须显式落盘，验证时断言全量容器 `[...document.querySelectorAll('.notes')].every(n => getComputedStyle(n).display === 'none')`（每页一个容器，只查首个会漏检）
7. **SVG 浮动标签与节点盒碰撞**：凭经验坐标放的 `<text>` 标签易压相邻节点盒或连线（实测中英混排标签 font 14 宽可达 80px+，纯 4 汉字仅 ≈56px，按字数估 gap 不可靠）；标签与任何盒边/连线净空 ≥8px，完成后逐页 headless 截图目检
8. **`-clamp()`/`-min()`/`-max()` 负号前缀静默失效**：`margin-top: -clamp(20px, 4vw, 60px)` 整条声明被浏览器丢弃，无 console 错误，元素只是出现在错误位置；负值必须写 `calc(-1 * clamp(20px, 4vw, 60px))`

## prefers-reduced-motion

> 规范副本：`templates/deck-skeleton.html` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

检测到时：翻页即时切换、数字直接显示最终值、入场动画跳过、背景特效关闭。

headless 验证注意：无渲染帧环境（`--dump-dom`/`--screenshot`）下 .01ms 动画/过渡卡 progress=0、计算值冻结在起始帧（截图全白/画布不居中/rect 测量污染），处置见本文件 headless 验证方法论条 6。

## 交付前审查

每页完成后按 `premium-review-fix.md` 执行审查，包括交互版专属审查项：
- 键盘翻页全部可用
- `prefers-reduced-motion` 适配
- 动画属性仅限 transform/opacity/filter
- 数字滚动/图表动画仅触发一次
- 非活跃页面无残留定时器
- 单页 DOM ≤ 500
- 数字键 1-9 直跳、R 重置、E 内联编辑切换、输入态守卫（input/textarea/contenteditable 内不翻页）全部可用
- `@media print` 一页一张按序展开、缩放壳已禁用、入场动画元素强制可见
- 上屏零 emoji，图标走 Unicode 文字符号或内联 SVG（见"禁用 emoji"节自检断言）

## 合并为单文件

所有页面的 CSS 合并到 `<style>`，JS 合并到 `<script>`，图表 SVG 内联。
最终文件双击即可在浏览器完整运行，无任何外部请求。

## 多页形态（INDEX + pages/）细则

仅上层 workflow 明确要求多页形态时使用（SKILL.md 硬约束 10），默认仍为单文件。多页形态的价值：每页文件双击即可独立验证（"改一点验一点"成本接近零）、headless 截图直接访问单页文件不需 JS 跳页、多人/多子任务并行做不同页零冲突、一页样式错误不波及他页。

### 文件结构

```text
交付根/
├── INDEX.html            # 导航壳：MANIFEST + iframe 视口 + 上一页/下一页 + 概览入口
├── assets/               # 素材图等共享资源（相对路径引用）
└── pages/
    ├── 01-cover.html     # 每页都是完整 1920×1080 自包含 HTML
    ├── 02-agenda.html
    └── 03-architecture.html
```

1. 每页文件独立自包含：自带 token、scale-to-fit 壳、`.notes` 话术容器，本文件全部规则照常适用；双击可单独打开，不依赖 INDEX 存在
2. 素材图按"素材图网格与 lightbox"条 5：多页形态用相对路径引 `assets/`，不 base64 内联；除此之外每页零外部请求
3. INDEX.html 用 MANIFEST 声明页序与标签，`slideId` 与各页 `data-slide-id` 对齐（`presenter-mode.md` §9）：

```js
window.DECK_MANIFEST = [
  { file: 'pages/01-cover.html',        label: '封面',     slideId: 'cover' },
  { file: 'pages/02-agenda.html',       label: '议程',     slideId: 'agenda' },
  { file: 'pages/03-architecture.html', label: '系统架构', slideId: 'architecture' }
];
```

### 上一页 / 下一页导航

1. INDEX 单 iframe 视口，翻页 = 换 `src` 为目标页文件；底部提供"上一页 / 下一页"按钮与页码 `N / total`，键盘 ←/→/Space/PageUp/PageDown 绑同一动作
2. 导航链接真实存在（SKILL.md 硬约束 10）：每页文件自带指向相邻页文件的真实 `<a href>` 上一页/下一页链接，作脱离 INDEX 时的兜底导航；首末页对应链接隐藏或禁用，不写死链
3. iframe 焦点防护：iframe 加 `tabindex="-1"`；页文件内导航键转发给 INDEX 处理（转发实现见 `ui-demo-choreography.md` §10 坑三，不重述）；INDEX 监听 `blur` 兜底收回焦点
4. 翻页状态写 `localStorage`（key 含 INDEX 文件名），刷新恢复当前页
5. 概览入口（可选）：INDEX 以网格陈列全部页缩略单元、点击跳页，实现遵守下方"概览墙三条硬约束"

### `#/N` 深链

1. `#/N/M` 深链是单文件 deck 专属能力（SKILL.md 多页形态豁免条款：S 演讲者窗、O 总览网格、深链、Home/End、触摸滑动均不判验收）；多页形态翻页以 INDEX 与页间真实链接为准
2. INDEX 可选实现 `INDEX.html#/N` 位置记忆：翻页时 `history.replaceState` 写 hash，加载时解析并直达第 N 页；页文件自身不做 `#/N`
3. 多页形态下演讲者模式联动（预览 iframe 指向页文件带 `?preview=1`、BroadcastChannel 用 INDEX 文件名）见 `presenter-mode.md` §8.5，不重述

### 多页形态打印与导出

1. 每页文件自带 `@media print` 规则（同"打印与导出"节，一页一张），单页打开单页打印
2. INDEX 不做聚合打印（跨 iframe 打印遍历不可靠）；用户要整套聚合 PDF 时说明取舍——回单文件形态导出，或逐页打印后合并，不静默丢页

## 概览墙三条硬约束

适用于 O 键总览网格（`presenter-mode.md` §4，交互契约以其为准）与 INDEX 概览页；画廊式陈列页（内容展示）走 `ui-demo-choreography.md` §6，本节只约束作导航与自检用的概览墙：

1. **禁用 `transform-style: preserve-3d` 做卡片墙**：preserve-3d 的 3D 场景里，浏览器对向后倾斜卡片的命中测试不可靠——顶排点不到、中排时好时坏。正解：整墙作为单个被 3D 倾斜的平面（墙容器不开 preserve-3d），全部卡片共面，点击即普通 DOM 命中测试、天然可靠；hover 提升用 2D `scale`，不用 `translateZ`
2. **任意页数自适应**：按页数 + 视口尺寸计算列数，行数增多则倾斜角变平，一屏放不下就纵向滚动；禁止两种懒做法——固定列数 + 写死强倾斜（页一多溢出塌角、透视失真），把几十页硬塞一屏缩成邮票（概览是看清页，不是看墙）
3. **缩略图分辨率下限**：单文件 deck 的 O 键总览恒用真实 DOM `transform: scale()` 渲染（`presenter-mode.md` §4 条 1，所见即所得）；多页形态页数极多、确需 `<img>` 缩略单元做性能兜底时，源图宽 ≥1600px，<1000px 在 hover 放大后必然发虚

## 打印与导出

deck 需支持打印 / 导出 PDF（发给听众做资料）：

> 规范副本：`templates/deck-skeleton.html` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```css
@media print {
  .canvas { transform: none !important; } /* scale-to-fit 缩放禁用 */
  .nav-ui, .progress-bar { display: none !important; }
  .slide {
    position: relative !important;
    display: block !important;
    opacity: 1 !important;
    width: 1920px; height: 1080px;
    page-break-after: always;
    break-after: page;
  }
  .slide .enter { opacity: 1 !important; transform: none !important; } /* 入场动画元素强制可见 */
}
@page { size: 1920px 1080px; margin: 0; } /* 竖版 deck 同步改 810×1080 */
```

- 打印态全部 slide 按序展开、一页一张；控件与进度条隐藏
- `!important` 一个都不能省：作用域规则（如 `.tpl-name .slide`，特异性 (0,2,0)）会压过 `@media print` 里的裸 `.slide`（(0,1,0)），被压即多页缩到 1-2 页，且屏幕预览完全正常、只在打印时暴露；交付前导出一次 PDF 断言页数 == slide 数（chrome `--print-to-pdf` + python3 数页）
- 截图 / 导出工具用 `?noscale` URL 参数跳过 scale-to-fit 壳，按设计画布原始尺寸渲染（fit 脚本检测该参数即不施加 transform）

## headless 验证方法论

交互机制的自动化验证用 headless Chrome，九条确定性规则：

1. **交互断言加 reduced-motion**：`--virtual-time-budget` 下 View Transition 回调时序不确定（状态机正确但 DOM 落定延迟且不可复现）；翻页/frag/分支/回退等交互断言一律加 `--force-prefers-reduced-motion`，走 REDUCED 同步落 DOM 路径；VT 本体靠 `document.startViewTransition` 存在性检查 + CSS 中 `::view-transition` 规则文本存在性检查（grep 级），真实浏览器表现信任人工目检
2. **截图矩阵**：深链 `#/N/M` 加载即对应步的即时终态，适合逐 frag 截图；分支页无深链，用全局索引 `?preview=N` 截图；拍完逐张目检话术零泄漏、标签碰撞、划线飞出、裁切
3. **注入断言用 rpartition**：场景脚本必须经 `src.rpartition('</body>')` 插入临时副本——deck 的演讲者窗 HTML 字符串内含 `</body>` 字面量，`replace('</body>')` 会命中它截断 deck 脚本，导致全部断言假失败；注入后用 `dispatchEvent(new KeyboardEvent(...))` 与 `el.click()` 驱动，结果写隐藏节点，`--dump-dom` 提取
4. **命令模板**：`chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 --virtual-time-budget=6000 --screenshot=OUT "file://DECK#/N/M"`
5. **捆绑 webfont 的产物**：截图/导出 PDF 前确保字体就绪或已超时锁定回系统栈——体积闸、子集化与 3500ms 超时锁定见 `typography.md` §5.7，此处不重述细节；命令模板的 `--virtual-time-budget=6000` 已覆盖该等待窗口，默认系统栈产物无此问题
6. **reduced-motion 核弹片段在无帧 headless 下冻结**：`*{animation-duration:.01ms!important;transition-duration:.01ms!important}` 依赖渲染帧推进；`--dump-dom`/`--screenshot` 无帧时动画/过渡启动后卡 progress=0，计算值冻结在起始帧——三个典型症状：`.slide.active` 的 visibility 停 hidden（截图全白）、scale-to-fit 内联 transform 停 none（画布不居中）、入场起始帧 `translateY` 位移垫偏 `.entered` 元素 rect（动画源优先级高于内联样式，titleGap 等四值测量被污染，实测偏差=起始帧位移量）。处置二选一：测量/截图前驱动里统一 `document.getAnimations().forEach(a=>a.cancel())`；或验证副本把该块改 `animation:none!important;transition:none!important`（前提：REDUCED 路径终态有内联兜底，如入场函数直置 opacity/transform）。真浏览器有帧，两种写法等价
7. **截图用原始 deck + 深链**：不对注入断言脚本的临时副本截图——场景脚本会驱动 deck 状态（翻页/播放/调参），末态停在脚本最后一步而与 URL 深链无关，多页截图字节级全同、逐页目检失效；断言用注入副本、截图用原始文件，两者分开
8. **跨窗口状态同步 headless 不可达，生产前真浏览器抽查**：BroadcastChannel/postMessage 双窗口同步（演讲者模式，见 `presenter-mode.md` §3.3）与调参双真源（URL+localStorage，见 `multi-version-selection.md`）这类跨窗口/跨标签链路在 headless 单页模式零覆盖，`--dump-dom` 断言全绿不代表同步可用；生产 deck 交付前必须真浏览器开双窗口抽查一次——S 键开演讲者窗口、双向翻页跟随、调参跨窗生效、刷新恢复翻页状态
9. **截图输出文件存在性校验**：chrome `--screenshot` 退出码 0 不代表 PNG 落盘（路径不可写、深链无内容等场景静默失败）；每页截图后必须检查文件存在且非空（`[ -s OUT ]`），批量循环结束汇总失败数、>0 非零退出——某页没写出来时，目检环节会整页漏掉它

以上方法论已固化为本 skill `scripts/` 下的可执行脚本，验证优先跑脚本、不手敲命令：

| 脚本 | 覆盖条目 | 用途 |
|---|---|---|
| `scripts/headless_assert.py` | 条 1/3/6 | 通用注入断言：assert.js 经 rpartition 注入临时副本，结果写 `window.__ASSERT_RESULT__`，dump-dom 提取；含 getAnimations().cancel() 与 reduced-motion |
| `scripts/screenshot_matrix.py` | 条 2/4/7/9 | 深链 `#/N/M`、`?preview=N`、多页形态三种截图矩阵，逐张存在性校验 |
| `scripts/measure_four_values.py` | 条 6 + 四值实测 | overflowPx/bottomWhitespacePx/titleGapPx/navSafeIntrusionPx 逐页 JSON 报告（阈值见 `premium-review-fix.md`） |
| `scripts/emoji_audit.py` | 禁用 emoji 节条 4 | 全文档 TreeWalker emoji 扫描（含 `.notes`） |
| `scripts/minutes_budget.py` | `presenter-mode.md` §16 条 8 | 演讲时间预算静态断言 |
| `scripts/fetch_images.py` / `scripts/preprocess_images.py` | `content-imagery-and-infographic.md` 真图纪律 | 批量取图（manifest 记来源许可）/ 压缩裁剪 base64 管线 |
