/* ============================================================================
 * demo-clock.js — 演示页统一时钟与 URL 参数控制（?seek / ?autoplay / ?speed）
 *
 * 来源：references/ui-demo-choreography.md §9（逐字提取）
 * 用途：三个 URL 参数作用于同一个演示时钟——倍速改时钟流速（不改各动画
 *       duration），seek 重放 cue 表并把 WAAPI 动画快进到终态
 * 接线：复制进演示页 <script>，置于 ui-demo-fx.js / dashboard-overlay.js 之后
 *       （CUES 引用 playStep / playDashboard）。前提：所有演示动作触发即确定，
 *       fired 集合是唯一副作用，seek 时重置重放。
 *       参数分工：#/N/M 页级/fragment 级深链（deck-nav.js）；?seek 页内演示步级；
 *       ?preview=N（演讲者预览）优先于 autoplay；?noscale（截图导出）并存不冲突。
 * 可调参数：CUES 演示步表（t 秒，步间隔 ≥1.5s）；SPEED clamp [0.25, 4]
 * 自检：window.__demo = { play, pause, seek, clock }；headless 用法
 *       ?seek=0/1/2… 逐步截图核对终态；?autoplay=1&speed=4 快速回归整段时序
 * ============================================================================ */

const params = new URLSearchParams(location.search);
const AUTOPLAY = params.get('autoplay') === '1' && params.get('preview') === null;
const SPEED = Math.min(4, Math.max(0.25, parseFloat(params.get('speed')) || 1));
const SEEK = params.get('seek');

const clock = { t: 0, playing: false, last: null, raf: 0 };
const CUES = [                                   // 演示步表：t 秒；步间隔 ≥1.5s（§5 铁律 2）
  { t: 0.0, run: () => playStep(0) },
  { t: 2.4, run: () => playStep(1) },
  { t: 5.0, run: () => playStep(2) },
  { t: 7.6, run: () => playDashboard(document.getElementById('dash')) }
];
let fired = new Set();

function demoTick(now) {
  if (clock.last === null) clock.last = now;
  clock.t += ((now - clock.last) / 1000) * SPEED;
  clock.last = now;
  for (let i = 0; i < CUES.length; i++) {
    if (!fired.has(i) && clock.t >= CUES[i].t) { fired.add(i); CUES[i].run(); }
  }
  document.getAnimations().forEach(a => { a.playbackRate = SPEED; });  // WAAPI 跟随倍速
  if (clock.playing) clock.raf = requestAnimationFrame(demoTick);
}
function demoPlay() { if (!clock.playing) { clock.playing = true; clock.last = null; clock.raf = requestAnimationFrame(demoTick); } }
function demoPause() { clock.playing = false; cancelAnimationFrame(clock.raf); clock.raf = 0; }
function demoSeek(n) {                           // ?seek=N：确定性快进到第 N 步终态
  demoPause();
  fired = new Set();
  clock.t = n < CUES.length ? CUES[n].t + 0.001 : CUES[CUES.length - 1].t + 3;
  CUES.forEach((cue, i) => { if (cue.t <= clock.t) { fired.add(i); cue.run(); } });
  document.getAnimations().forEach(a => {
    try { a.finish(); } catch (err) { /* iterations:Infinity 的动画无终态，跳过 */ }
  });
}
if (SEEK !== null) demoSeek(Math.max(0, parseInt(SEEK, 10) || 0));
else if (AUTOPLAY) document.fonts.ready.then(demoPlay);
window.__demo = { play: demoPlay, pause: demoPause, seek: demoSeek, clock };
