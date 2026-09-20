/* ============================================================================
 * animate-number.js — 数字滚动（关键数字从起始值滚动到目标值，cubic-out 缓动）
 *
 * 来源：references/interactive-html-authoring.md「数据动效」与
 *       references/interactive-mode-rules.md「数据动态效果」（两处合并：
 *       取带 from 参数的超集签名；按硬约束 12 增加 reduced-motion 直显守卫，
 *       其余逻辑逐字）
 * 用途：数据动效三件套之一（数字滚动/进度条填充/图表动画）——MOTION_INTENSITY
 *       2 档默认需求；结束帧 snap 精确值（progress=1 → eased=1 → 恰为 target）
 * 接线：复制进交付物 <script>。触发纪律：仅在元素首次进入视口或页面激活时
 *       触发一次，用 IntersectionObserver 或订阅 deck 的 slidechange 事件
 *       （deck-skeleton.html 翻页落定后派发）；宿主元素 CSS 加
 *       font-variant-numeric: tabular-nums 防逐帧抖动
 * 可调参数：duration 默认 1200ms；from 默认 0；数字格式保留原始单位
 *       （%、万、亿 写在元素相邻的静态文本里，不进滚动值）
 * 自检：滚动只触发一次（重复翻页不重滚）；reduced-motion 下直显终值；
 *       结束显示值 === target.toLocaleString()
 * ============================================================================ */

function animateNumber(el, target, duration = 1200, from = 0) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    el.textContent = Math.round(target).toLocaleString();
    return;
  }
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(from + (target - from) * eased).toLocaleString();
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
