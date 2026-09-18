# 逐页交互 HTML 编写规则

本文件定义 Phase 4 逐页交互 HTML 的编写规则。

## 总体结构

最终交付物为单个 HTML 文件，包含所有页面：

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

### 键盘绑定

```js
document.addEventListener('keydown', (e) => {
  switch (e.key) {
    case 'ArrowRight': case ' ': case 'PageDown': next(); break;
    case 'ArrowLeft': case 'PageUp': prev(); break;
    case 'Home': goTo(0); break;
    case 'End': goTo(totalSlides - 1); break;
    case 'f': case 'F': toggleFullscreen(); break;
    case 'Escape': exitFullscreen(); break;
  }
});
```

### 点击区域

右半区点击下一页，左半区点击上一页，底部进度条可跳转。
点击热区不遮挡可交互内容。

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
5. 多页形态素材图用相对路径引用，不 base64 内联；单文件 deck 形态才内联，且需控制总体积

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

## 静默布局坑

以下错误不报异常、自动化检查抓不到，表现为"元素永远不出现"或"渲染里被裁掉"：

1. **transform 对 inline 元素无效**：scaleX/translate 在 `display:inline` 的 span 上是 no-op；被动画元素必须 block/inline-block/flex-item 且有真实宽高——auto 宽 0px 元素做缩放等于永远不可见
2. **峰值尺寸留净空**：脉冲/过冲装饰（yoyo scale、back-out 过冲）按最大帧定位而非静止帧，且不跨 `overflow:hidden` 边界，否则被裁或压住邻居
3. **先建静态终态**：先用 HTML/CSS 搭出可见的静态终态，再往上加动画——终态本身错了，动画只会更晚暴露问题
4. **离屏 canvas 测文本**：字号自适应宽度时用离屏 canvas `ctx.measureText` 测量后二分字号，不写进页面再读回（每次读回都触发 reflow）
5. **正文不用 `<br>` 断行**：强制换行忽略实际渲染字宽，行已自然换行时多出一折造成重叠；用 max-width 控制自然换行。例外：短展示标题刻意每词一行

## prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

检测到时：翻页即时切换、数字直接显示最终值、入场动画跳过、背景特效关闭。

## 交付前审查

每页完成后按 `premium-review-fix.md` 执行审查，包括交互版专属审查项：
- 键盘翻页全部可用
- `prefers-reduced-motion` 适配
- 动画属性仅限 transform/opacity/filter
- 数字滚动/图表动画仅触发一次
- 非活跃页面无残留定时器
- 单页 DOM ≤ 500

## 合并为单文件

所有页面的 CSS 合并到 `<style>`，JS 合并到 `<script>`，图表 SVG 内联。
最终文件双击即可在浏览器完整运行，无任何外部请求。
