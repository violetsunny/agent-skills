# 领导汇报逐页 HTML 模板

本模板定义固定画布、页面类型、token 变量、布局检查与图表嵌入约束。

## 1. 固定画布

1. 尺寸固定为 `1920 x 1080px`
2. 不使用响应式布局、媒体查询、`max-width` 或 `width: 100%` 页面思维
3. 每个 HTML 文件只表达一页幻灯片
4. 画布容器使用 `position: relative; overflow: hidden`
5. **scale-to-fit 视口自适应壳（强制）**：画布外必须包一层缩放壳，浏览器任意窗口尺寸下画布等比缩放居中、完整可见、无滚动条。设计画布尺寸不变（仍是 1920x1080 绝对定位坐标系），缩放只发生在壳层；1920x1080 视口时 scale=1，headless 截图/下游转 PPT 消费不受影响

```html
<div class="fit-viewport"><!-- scale-to-fit 壳 -->
  <div class="canvas" style="position:relative;width:1920px;height:1080px;overflow:hidden;">
    <!-- 页面内容全部放在固定画布内 -->
  </div>
</div>
<script>
(function () {
  var canvas = document.querySelector('.canvas');
  function fit() {
    var s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    canvas.style.transform = 'scale(' + s + ')';
  }
  window.addEventListener('resize', fit);
  fit();
})();
</script>
```

```css
html, body { height: 100%; overflow: hidden; }
.fit-viewport {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-color);
}
.canvas { transform-origin: center center; flex-shrink: 0; }
```

## 2. 字体与 token

字体栈：

```css
font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
```

推荐根变量：

```css
:root {
  --primary-color: #0078D4;
  --on-primary-color: #FFFFFF;
  --secondary-color: #4F6BED;
  --on-secondary-color: #FFFFFF;
  --tertiary-color: #00A389;
  --bg-color: #EEF2F7;
  --surface-color: #FFFFFF;
  --surface-muted: #F5F7FB;
  --outline-color: #D7DFEA;
  --text-primary: #16324F;
  --text-secondary: #5B6B7F;
  --text-tertiary: #8A99AC;
  --success-color: #1F9D55;
  --on-success-color: #FFFFFF;
  --warning-color: #D98324;
  --on-warning-color: #FFFFFF;
  --danger-color: #C93C37;
  --on-danger-color: #FFFFFF;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;
  --shadow-soft: 0 6px 24px rgba(18, 52, 86, 0.08);
}
```

规则：

1. 首页架构图主色优先覆盖 `--primary-color`
2. 页面中优先引用变量，不散落硬编码颜色和值
3. 表现层需要新颜色时，先判断是否能映射到现有语义角色
4. `on-*` ink 值按 `slide-design-system.md` §1 配对规则实测选定（白或近黑，对该填充色 ≥ 4.5:1），换强调色时必须复核配对 ink
5. `--bg-color` 是画布外 body 底色，与画布 `--surface-color` 分层，禁止在 body 上硬编码 hex

## 3. 页面类型

常用 13 类页面：

1. 封面页：核心结论、项目定位、能力卡、右上角 Logo
2. 架构图页：分层结构、连接关系、少量数字锚点
3. 数据看板页：上排大数字，下排指标卡片，底部总结
4. 闭环流程页：垂直步骤、箭头连接、侧边维度卡
5. 漏斗策略页：层级递进、方向箭头、底部总结
6. 治理闭环页：左右分栏，左数右流程
7. 案例对比页：左右对照、中心对比点、总结区
8. 时间线页：水平/垂直里程碑节点 + 关键事件 + 当前进度锚点；节点多或需精确排期时改引甘特图真源 iframe
9. 数据表格页：表格为唯一主体，表头用 surface 分层，数字列 `tabular-nums` 右对齐，行高均匀，超过 8 行拆页或摘要化
10. 观点引用页：大字观点/客户原话 + 来源行（`--text-tertiary`），大留白，仅封面级单一结论使用
11. 路线图页：NOW / NEXT / LATER 分栏卡片，每栏 ≤ 4 条；精确到周的排期不手绘，引甘特图真源 iframe
12. 检查清单页：单列列表（4-8 条，超出拆页），每行 = 22×22 方框 checkbox + 一行事项（`>= 18px`）+ 右侧 mono 小标签（`--text-tertiary`）；完成态 `--success-color` 填充 + 反白 ✓ + 文字删除线降为 `--text-tertiary`；行间 `--outline-color` 发丝分隔；完成/未完成两态必须同页可见区分
13. 尾页：核心结论收束、联系信息、底部居中 Logo

## 4. 常用区块

1. 页面标题区：说明本页主题
2. 结论区：一句话结论，必须突出
3. 主内容区：图表、表格、数字卡、流程图
4. 说明区：解释因果、风险、动作
5. 品牌区：封面右上或内容页页脚 Logo
6. 总结区：内容页底部总结条，可选但常用

## 5. 布局审查清单

每页生成后逐项检查：

| # | 检查项 | 标准 |
|---|---|---|
| 1 | 画布尺寸 | `.canvas` 为 `1920px × 1080px` |
| 2 | 标题可见性 | 标题未被装饰元素、Logo、图表遮挡 |
| 3 | 结论显著性 | 结论区是首屏第二视觉焦点 |
| 4 | 元素不重叠 | 任意两个主要绝对定位块无交叠 |
| 5 | 分栏均衡 | 左右主栏高度差不超过 `100px` |
| 6 | 内边距充足 | 卡片 `padding >= 14px` |
| 7 | 字号下限 | 正文 `>= 16px`，标签 `>= 12px`，主数字建议 `>= 28px` |
| 8 | 内容不溢出 | 文本、表格、卡片内容不超框 |
| 9 | 图表一致性 | 页面图表引用真源 HTML，未被替换重绘 |
| 10 | 水平居中 | 需要居中的元素组左右偏差不超过 `20px` |

## 6. 图表嵌入约束

图表区优先引用 Phase 3.5 已产出的 HTML：

```html
<div class="chart-zone">
  <iframe src="../flow/<图表名>.html" width="100%" height="100%" frameborder="0"></iframe>
</div>
```

规则：

1. 不自造一份不同语义的替代图表
2. 图表区尺寸要尊重原图表比例，不强拉伸变形
3. 页面 token 可以统一外层容器，但不覆盖图表事实表达

## 7. 模板骨架

### 静态版模板骨架

canonical 副本：`templates/slide-page-static.html` — 复制使用，以 templates 为准
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>第 N 页：页面标题</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --primary-color: #0078D4;
      --on-primary-color: #FFFFFF;
      --secondary-color: #4F6BED;
      --tertiary-color: #00A389;
      --bg-color: #EEF2F7;
      --surface-color: #FFFFFF;
      --surface-muted: #F5F7FB;
      --outline-color: #D7DFEA;
      --text-primary: #16324F;
      --text-secondary: #5B6B7F;
      --text-tertiary: #8A99AC;
      --space-sm: 8px;
      --space-md: 16px;
      --space-lg: 24px;
      --space-xl: 32px;
      --space-2xl: 48px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      --shadow-soft: 0 6px 24px rgba(18, 52, 86, 0.08);
    }
    html, body { height: 100%; overflow: hidden; }
    body {
      background: var(--bg-color);
      font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    }
    .fit-viewport {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .canvas {
      position: relative;
      width: 1920px;
      height: 1080px;
      flex-shrink: 0;
      transform-origin: center center;
      background: var(--surface-color);
      overflow: hidden;
      box-shadow: var(--shadow-soft);
    }
    .notes { display: none; }
  </style>
</head>
<body>
  <div class="fit-viewport">
  <div class="canvas">
    <!-- 标题区 -->
    <!-- 结论区 -->
    <!-- 主内容区 -->
    <!-- 说明区 -->
    <!-- 品牌区 -->
    <div class="notes"><!-- 本页汇报话术，仅供演讲者，永不上屏 --></div>
  </div>
  </div>
  <script>
  (function () {
    var canvas = document.querySelector('.canvas');
    function fit() {
      var s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
      canvas.style.transform = 'scale(' + s + ')';
    }
    window.addEventListener('resize', fit);
    fit();
  })();
  </script>
</body>
</html>
```

### 交互版模板骨架

canonical 副本：`templates/slide-deck-interactive.html` — 复制使用，以 templates 为准
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>汇报演示</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --primary-color: #0078D4;
      --on-primary-color: #FFFFFF;
      --secondary-color: #4F6BED;
      --tertiary-color: #00A389;
      --bg-color: #EEF2F7;
      --surface-color: #FFFFFF;
      --surface-muted: #F5F7FB;
      --outline-color: #D7DFEA;
      --text-primary: #16324F;
      --text-secondary: #5B6B7F;
      --text-tertiary: #8A99AC;
      --space-sm: 8px;
      --space-md: 16px;
      --space-lg: 24px;
      --space-xl: 32px;
      --space-2xl: 48px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      --shadow-soft: 0 6px 24px rgba(18, 52, 86, 0.08);
      --transition-duration: 500ms;
      --transition-easing: cubic-bezier(0.4, 0, 0.2, 1);
    }
    body {
      background: var(--bg-color);
      font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
      overflow: hidden;
    }
    .notes { display: none; }
    .deck {
      position: relative;
      width: 1920px;
      height: 1080px;
      margin: 0 auto;
    }
    .slide {
      position: absolute;
      top: 0; left: 0;
      width: 1920px;
      height: 1080px;
      background: var(--surface-color);
      overflow: hidden;
      visibility: hidden;
      opacity: 0;
      transition: opacity var(--transition-duration) var(--transition-easing);
    }
    .slide.active {
      visibility: visible;
      opacity: 1;
    }
    /* 入场动画 */
    [data-enter-order] {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 500ms var(--transition-easing), transform 500ms var(--transition-easing);
    }
    .slide.active [data-enter-order].entered {
      opacity: 1;
      transform: translateY(0);
    }
    /* 导航控件 */
    .nav-progress {
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 6px;
      z-index: 10;
    }
    .nav-dot {
      width: 8px; height: 8px;
      border-radius: 50%;
      background: var(--outline-color);
      cursor: pointer;
      transition: background 200ms;
    }
    .nav-dot.active { background: var(--primary-color); }
    .page-counter {
      position: absolute;
      bottom: 16px; right: 24px;
      font-size: 14px;
      color: var(--text-secondary);
      z-index: 10;
    }
    /* reduced motion
       headless 无帧验证（--dump-dom/--screenshot）下 .01ms 动画/过渡卡 progress=0、
       计算值冻结起始帧：测量截图前驱动里 document.getAnimations().forEach(a=>a.cancel())，
       或验证副本改 animation:none/transition:none（前提 REDUCED 终态有内联兜底） */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
    /* View Transition */
    ::view-transition-old(slide),
    ::view-transition-new(slide) {
      animation-duration: var(--transition-duration);
      animation-timing-function: var(--transition-easing);
    }
  </style>
</head>
<body>
  <div class="deck">
    <section class="slide active" data-index="0">
      <!-- 第一页内容，元素加 data-enter-order="1/2/3..." -->
      <div class="notes"><!-- 本页话术 --></div>
    </section>
    <section class="slide" data-index="1">
      <!-- 第二页内容 -->
      <div class="notes"><!-- 本页话术 --></div>
    </section>
  </div>
  <div class="nav-progress"></div>
  <div class="page-counter"></div>
  <script>
    (function() {
      const slides = document.querySelectorAll('.slide');
      const total = slides.length;
      let current = 0;
      const counter = document.querySelector('.page-counter');
      const progress = document.querySelector('.nav-progress');

      // 生成进度点
      for (let i = 0; i < total; i++) {
        const dot = document.createElement('div');
        dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
        dot.addEventListener('click', () => goTo(i));
        progress.appendChild(dot);
      }

      function updateUI() {
        counter.textContent = (current + 1) + ' / ' + total;
        progress.querySelectorAll('.nav-dot').forEach((d, i) => {
          d.classList.toggle('active', i === current);
        });
      }

      function triggerEnterAnim(slide) {
        const els = slide.querySelectorAll('[data-enter-order]');
        els.forEach(el => el.classList.remove('entered'));
        requestAnimationFrame(() => {
          const groups = {};
          els.forEach(el => {
            const order = el.dataset.enterOrder;
            (groups[order] = groups[order] || []).push(el);
          });
          Object.keys(groups).sort((a, b) => a - b).forEach((order, idx) => {
            setTimeout(() => {
              groups[order].forEach(el => el.classList.add('entered'));
            }, idx * 150);
          });
        });
      }

      function swapSlide(index) {
        slides[current].classList.remove('active');
        current = index;
        slides[current].classList.add('active');
        triggerEnterAnim(slides[current]);
        updateUI();
      }

      function goTo(index) {
        if (index < 0 || index >= total || index === current) return;
        if (document.startViewTransition) {
          document.startViewTransition(() => swapSlide(index));
        } else {
          swapSlide(index);
        }
      }

      document.addEventListener('keydown', e => {
        switch(e.key) {
          case 'ArrowRight': case ' ': case 'PageDown': goTo(current + 1); break;
          case 'ArrowLeft': case 'PageUp': goTo(current - 1); break;
          case 'Home': goTo(0); break;
          case 'End': goTo(total - 1); break;
          case 'f': case 'F':
            document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
            break;
        }
      });

      document.addEventListener('click', e => {
        if (e.target.closest('.nav-dot') || e.target.closest('[data-interactive]')) return;
        const x = e.clientX / window.innerWidth;
        if (x > 0.5) goTo(current + 1);
        else goTo(current - 1);
      });

      updateUI();
      triggerEnterAnim(slides[0]);
    })();
  </script>
</body>
</html>
```

## 8. 话术 notes 容器

每页四要素中的"汇报话术"必须随 HTML 一起交付，承载体是画布内的 `.notes` 容器：

```html
<div class="notes">
  <p>话术段落，核心关键词可加 <strong>强调</strong>。</p>
</div>
```

规则：

1. `.notes { display: none; }`，任何情况下不得改为可见，也不得用可见元素复述话术
2. 话术只写给演讲者：解释含义、风险、动作，不复述屏幕上已有的文字
3. 演讲者专用文字（"这一页讲……"、提示语、口播稿）一律进 `.notes`，出现在可见区域即违反页面契约
4. `display:none` 无渲染成本，静态版与交互版通用；下游 PPTX 转换时该容器可作为演讲者备注来源

## 9. 图片上屏

位图（截图/照片/AI 配图/图表 PNG）必须经 `.img-frame` 容器上屏，禁止裸 `<img>`；contain/cover 选型、图片版式与 scrim 边界见 `slide-image-framing.md`。图表 HTML 真源仍走第 6 节 iframe 约束，不适用本节。
