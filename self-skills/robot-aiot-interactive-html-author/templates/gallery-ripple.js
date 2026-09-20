/* ============================================================================
 * gallery-ripple.js — 画廊涟漪（鼠标磁场：邻近卡片位移/缩放平方衰减）
 *
 * 来源：references/ui-demo-choreography.md §7（逐字提取）
 * 用途：画廊墙 body 中间层的指针驱动涟漪——与入场（outer）、hover（inner）
 *       互不抢 transform；卡片中心一次性缓存，避免每帧强制同步布局
 * 接线：必须在 templates/gallery-wall.js 之后同页引入（复用其 wall / cards /
 *       reduced 变量）；启停并入 gallery-wall.js 的 slidechange 订阅点——
 *       start() 内追加 startRipple()，stop() 内追加 stopRipple()（见文末注释）
 * 可调参数：RADIUS 半径px / PUSH 最大位移px / LIFT 最大放大 / SMOOTH 平滑系数
 * 纪律：指针离开后 sx/sy 平滑趋近 -1e4 卡片自然回位；reduced-motion 不启动，
 *       墙保持静态终帧
 * ============================================================================ */

const RADIUS = 320, PUSH = 18, LIFT = 0.06, SMOOTH = 0.15;   // 半径px / 最大位移px / 最大放大 / 平滑系数
const pointer = { x: -1e4, y: -1e4, sx: -1e4, sy: -1e4 };
wall.addEventListener('pointermove', e => {
  const r = wall.getBoundingClientRect();
  pointer.x = e.clientX - r.left;
  pointer.y = e.clientY - r.top;
});
wall.addEventListener('pointerleave', () => { pointer.x = pointer.y = -1e4; });

function measure() {                                          // 布局就绪后缓存卡片中心，resize 重测
  const wr = wall.getBoundingClientRect();
  for (const c of cards) {
    const r = c.outer.getBoundingClientRect();
    c.cx = r.left + r.width / 2 - wr.left;
    c.cy = r.top + r.height / 2 - wr.top;
  }
}
document.fonts.ready.then(() => requestAnimationFrame(measure));
new ResizeObserver(measure).observe(wall);

let ripRaf = 0;
function rippleTick() {
  pointer.sx += (pointer.x - pointer.sx) * SMOOTH;            // 指数平滑：太快抖、太慢拖
  pointer.sy += (pointer.y - pointer.sy) * SMOOTH;
  for (const c of cards) {
    const dx = c.cx - pointer.sx, dy = c.cy - pointer.sy;
    const d = Math.hypot(dx, dy) || 1;
    const f = Math.max(0, 1 - d / RADIUS);
    const e = f * f;                                          // 平方衰减
    c.body.style.transform =
      `translate(${(dx / d) * e * PUSH}px, ${(dy / d) * e * PUSH}px) scale(${1 + e * LIFT})`;
  }
  ripRaf = requestAnimationFrame(rippleTick);
}
function startRipple() { if (!ripRaf && !reduced) { measure(); ripRaf = requestAnimationFrame(rippleTick); } }
function stopRipple()  { cancelAnimationFrame(ripRaf); ripRaf = 0; }
// 启停并入 §6 的 slidechange 订阅点：start() 内追加 startRipple()，stop() 内追加 stopRipple()
