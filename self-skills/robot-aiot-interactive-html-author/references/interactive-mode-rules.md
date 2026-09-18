# 交互版演示 HTML 规则

本文件定义交互版汇报页的翻页、动画、特效、数据动效和交互图表规则。
交互版与静态版共享设计 token 和排版体系，仅增加交互层。

## 技术约束

1. 纯原生 HTML/CSS/JS，禁止任何外部依赖（无 CDN、无 npm 包）
2. 双击 HTML 文件即可在浏览器完整运行
3. 固定 `1920x1080` 画布不变
4. 所有动画使用 CSS `@keyframes` + `transition` + 原生 View Transition API；JS 仅负责状态切换和事件绑定
5. 禁止 `setInterval` 持续动画和无限 `requestAnimationFrame` 循环；`requestAnimationFrame` 仅允许用于有明确终止条件的有限动画（如数字滚动到目标值后停止）。唯一豁免：`animation-fx-catalog.md` 的 canvas FX 循环型特效，必须遵守 `generative-art-and-canvas.md` 生命周期契约（随页启停、离页即销毁）
6. 尊重 `prefers-reduced-motion`：检测到减少动画偏好时，所有过渡降级为即时切换

## 翻页系统

### 键盘控制

| 按键 | 动作 |
|------|------|
| `→` / `Space` / `PageDown` | 下一页 |
| `←` / `PageUp` | 上一页 |
| `Home` | 首页 |
| `End` | 末页 |
| `Esc` | 退出全屏 / 关闭总览与抽屉 |
| `F` | 切换全屏 |
| `S` | 打开演讲者窗口（机制见 `presenter-mode.md`） |
| `N` | 当前页话术抽屉 |
| `O` | 总览网格 |
| `B` | 回主线（清空分支导航栈） |
| `T` | 主题审阅循环（仅评审期，声明了 `data-themes` 时生效） |

### 触摸与深链

1. 触摸设备左右滑动翻页（水平位移 ≥ 50px 且大于垂直位移），与点击热区互斥
2. 触控目标（翻页热区、按钮、进度条点击区）≥ 44×44px（触摸精度下限）
3. 翻页同步 `#/N` 深链（`history.replaceState`），页内有 fragment 时扩展为 `#/N/M`；加载时解析 hash 直达对应页与停留点
4. 实现细则见 `presenter-mode.md` §5-§6

### 点击控制

1. 页面右半区点击 → 下一页
2. 页面左半区点击 → 上一页
3. 底部进度条可点击跳转到对应页
4. 点击热区不遮挡可交互内容（图表、按钮）

### 页面结构

多页合并为单文件时：

```html
<div class="deck">
  <section class="slide active" data-index="0" data-title="页面标题">
    <!-- 可见内容 -->
    <div class="notes"><!-- 本页话术，display:none，仅供演讲者 --></div>
  </section>
  <section class="slide" data-index="1" data-title="页面标题">...</section>
</div>
```

- 当前页 `.active` 可见，其余 `visibility: hidden; position: absolute`
- 不使用 `display: none`（会导致 View Transition 无法捕获旧帧）
- `data-title` 供总览网格与深链展示使用
- 每页话术写入 `.notes` 容器（`display: none`），演讲者专用文字禁止出现在可见区域；承载与显示机制见 `presenter-mode.md` §2

### 页内分步揭示（fragment）

同一页要分多次揭示内容（先给结论、再逐条给证据）时，用 fragment 停留点，不拆成多页：

1. 页内内容分组标 `data-fragment="1|2|3…"`；未标注的内容属 fragment 0（进页即可见）
2. 翻页状态机：活跃页按 Next 先推进 fragment 索引（下一组入场），最后一组揭示完才真正翻页；Prev 反向回收
3. fragment 是离散停留点不是播放：每次 Next 直接呈现该组完整终态（可加入场动画，但终态确定）
4. 深链 `#/N/M` = 第 N 页第 M 个 fragment，加载直达该停留点
5. 页码显示 fragment 进度：`N / total · 步 M/K`；演讲者窗口 NEXT 预览在页内还有 fragment 时显示下一 fragment 态而非下一页

### 分支序列与导航栈

附录页/深入页不进主线，由热点进入、原路返回：

1. 分支页 `<section>` 标 `data-sequence="序列名"`，不参与主线翻页序
2. 热点点击 push `{sequenceId, slideIndex:0}` 进导航栈并进入分支首页
3. 分支内 `←`/`→` 只在该序列内翻页；页码 scoped 到序列（`1 / 2`，不是全局计数）
4. `Esc`（分支内且无浮层）= back()：弹栈回到持有热点的精确父页；`B` = 清栈回主线
5. 面包屑从栈渲染：`主线 › 序列名 › 第 2 页`，显示在分支页顶部
6. 总览网格（O 键）主线与各分支序列分组显示，组头 = 序列名

### 内容热点

1. 声明式热点：`<button class="hotspot" data-target="序列名" data-label="这个数怎么算的">`，region 用百分比包围盒（left/top/width/height，0-100）定位在触发它的内容上
2. 省略 region 时渲染为页底带标签按钮，不做无形整页热区
3. 样式微弱（细描边 + hover 显 label），不抢正文视觉焦点；仅活跃页可点
4. 热点点击 `stopPropagation`，不冒泡到左右半屏翻页热区
5. 用途：领导汇报的附录跳转（"数据来源""怎么算的""演示分支"）

## 页面过渡动画

### 过渡类型选择

| 页面关系 | 推荐过渡 | CSS 类名 |
|----------|----------|----------|
| 顺序翻页 | 淡入淡出 | `fade` |
| 章节跳转 | 水平滑动 | `slide-horizontal` |
| 深入细节 | 缩放推入 | `zoom-in` |
| 返回上级 | 缩放拉出 | `zoom-out` |
| 并列对比 | 垂直滑动 | `slide-vertical` |

### 时长与缓动

- 过渡时长：`400ms - 600ms`
- 缓动函数：`cubic-bezier(0.4, 0, 0.2, 1)`（标准减速曲线）
- 禁止弹跳、回弹、过冲缓动

### 实现方式

优先使用原生 View Transition API：

```js
function goTo(index) {
  if (!document.startViewTransition) {
    swapSlide(index);
    return;
  }
  document.startViewTransition(() => swapSlide(index));
}
```

CSS：

```css
::view-transition-old(slide) {
  animation: fade-out 400ms cubic-bezier(0.4, 0, 0.2, 1);
}
::view-transition-new(slide) {
  animation: fade-in 400ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

不支持 View Transition 的浏览器降级为 class 切换 + CSS transition。

## 元素入场动画

### 触发时机

页面变为 `.active` 后，子元素按 `data-enter-order` 依次入场：

```html
<h1 data-enter-order="1">标题</h1>
<p data-enter-order="2">结论</p>
<div data-enter-order="3">图表区</div>
```

### 入场效果

| 元素类型 | 推荐效果 | 时长 |
|----------|----------|------|
| 标题 | 从上方淡入下滑 | 500ms |
| 结论/正文 | 透明度渐入 | 400ms |
| 数字卡片 | 缩放+透明度 | 500ms |
| 图表容器 | 透明度渐入 | 600ms |
| 列表项 | 逐项从左滑入 | 每项间隔 100ms |

### 延迟序列

- 相邻 order 间隔：`100ms - 200ms`
- 最大总入场时间不超过 `2s`
- 同一 order 的元素同时入场

## 数据动态效果

### 数字滚动

关键数字从 0 滚动到目标值：

```js
function animateNumber(el, target, duration = 1200) {
  const start = performance.now();
  const from = 0;
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(from + (target - from) * eased).toLocaleString();
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

- 仅在元素首次进入视口或页面激活时触发一次
- 使用 `IntersectionObserver` 或页面切换事件触发
- 数字格式保留原始单位（%、万、亿）

### 进度条填充

- 宽度从 0% 过渡到目标值
- 时长 `800ms - 1200ms`
- 使用 CSS `transition: width` 而非 JS 逐帧

### 图表逐步绘制

- SVG 路径使用 `stroke-dasharray` + `stroke-dashoffset` 动画
- 柱状图从底部生长
- 饼图扇区依次展开
- 所有图表动画在页面激活后延迟 `300ms` 开始，避免与入场动画抢注意力

## 交互式图表

### Hover 高亮

- 鼠标悬停数据点/柱体/扇区时高亮并显示 tooltip
- tooltip 使用绝对定位，跟随鼠标但不超出画布边界
- 离开时 `200ms` 淡出

### 点击展开

- 点击聚合数据可展开明细（仅当母稿提供明细数据时）
- 展开/收起使用高度过渡，时长 `300ms`
- 未提供明细数据时不添加点击交互

### 筛选联动

- 仅当母稿明确包含多维度数据时启用
- 筛选器样式与页面 token 一致
- 切换时图表区域淡出→更新→淡入，总时长 `400ms`

## 背景与视觉特效

### 允许的背景效果

1. 微渐变呼吸：背景色在两个相近色值间缓慢过渡，周期 `8s - 12s`，色差 ≤ 5%
2. 粒子点缀：少量（≤ 20个）低透明度圆点缓慢漂移，仅用于封面/尾页
3. 光晕：径向渐变跟随鼠标位置微移，偏移量 ≤ 30px，仅用于重点强调区

### 禁止的背景效果

1. 视频背景
2. 高频闪烁、脉冲
3. 大面积颜色快速变化
4. 3D 透视旋转

### 扩展特效路由

用户明确要求动画特效（"炫酷""动效""粒子""发布会风格"等）时，从 `animation-fx-catalog.md` 的 49 种 CSS 入场动画与 21 种 canvas FX 中路由选型，遵守其预算硬限与例外条款；未明确要求时只用本文件的克制入场表，不主动加特效。

## 字体效果

1. 标题可使用渐变文字（`background-clip: text`），但仅限主标题且整套汇报统一
2. 正文禁止文字特效
3. 数字可使用等宽字体增强可读性
4. 文字描边、阴影、发光效果仅在字号 ≥ 36px 时使用

## 按钮与交互控件

### 按钮样式

- 使用页面 token 中的 `--primary-color` 作为主按钮色
- hover：亮度提升 10% + 轻阴影
- active：亮度降低 5%
- focus：`outline: 2px solid var(--primary-color); outline-offset: 2px`
- 过渡时长 `200ms`

### 导航控件

- 左右箭头按钮：半透明，hover 时完全不透明
- 进度指示器：底部居中，当前页高亮
- 页码显示：`当前页 / 总页数`，右下角

## 性能约束

1. 单页 DOM 节点数 ≤ 500
2. 动画属性仅限 `transform`、`opacity`、`filter`；禁止动画 `width`、`height`、`top`、`left`（进度条除外）
3. 图片使用 `loading="lazy"`
4. 首屏渲染时间 ≤ 500ms（无网络请求）
5. 内存占用：销毁非活跃页面的定时器和事件监听

## prefers-reduced-motion 适配

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

检测到减少动画偏好时：
- 翻页改为即时切换
- 数字直接显示最终值
- 入场动画跳过
- 背景特效关闭

## 与静态版的关系

1. 交互版复用静态版的 token、配色、排版、图表引用
2. 交互版不修改图表真源内容
3. 静态版是 ppt-master 的输入；交互版仅供浏览器演示
4. 两者并行生成，互不覆盖
