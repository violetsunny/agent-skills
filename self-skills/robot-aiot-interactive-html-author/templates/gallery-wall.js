/* ============================================================================
 * gallery-wall.js — 画廊墙 render(t) 纯函数模式（24 卡 3D 倾斜陈列墙）
 *
 * 来源：references/ui-demo-choreography.md §6（逐字提取，CSS 块转为模板字符串）
 * 用途：多件产出同屏陈列的展览馆式页面——错峰入场 + 驻场慢漂 + hover 提升，
 *       三层 DOM 分工（outer 入场 / body 涟漪 / inner hover）互不抢 transform
 * 接线：GALLERY_CSS 写入页面 <style>；页面放 <div class="gallery-viewport">
 *       <div class="gallery-canvas"></div></div> 且宿主 section 带 .slide 与
 *       data-index；素材图放 assets/shot-01.png …（§2 素材三件套）；
 *       JS 段复制进交付物 <script>，依赖 slidechange 事件（deck 翻页派发）
 *       与 document.fonts.ready。涟漪层叠加见 templates/gallery-ripple.js。
 * 可调参数：COLS/ROWS/ENTRY_SEC（卡数与入场段时长）、3D 倾斜角（CSS 块内
 *           rotateX/Y/Z 与 perspective）、错峰系数 0.55、慢漂振幅 10/8px
 * 纪律：render(t) 是 t 的纯函数（同一 t 渲染一万次同一画面）；rAF 随页启停；
 *       reduced-motion 直接终态静帧；window.__seek(t) 供调试与 headless 截图
 * ============================================================================ */

/* ---------- 结构与皮肤 CSS（写入页面样式表） ---------- */

const GALLERY_CSS = `
.gallery-viewport{position:absolute;inset:0;overflow:hidden;perspective:2400px;perspective-origin:50% 45%}
.gallery-canvas{position:absolute;left:50%;top:50%;width:1600px;margin:-360px 0 0 -800px;
  display:grid;grid-template-columns:repeat(6,1fr);gap:32px;
  transform:rotateX(12deg) rotateY(-8deg) rotateZ(-2deg)}
.g-card{aspect-ratio:16/9;will-change:transform,opacity}
.g-body{width:100%;height:100%;will-change:transform}
.g-inner{width:100%;height:100%;padding:6px;background:#fff;border-radius:14px;overflow:hidden;
  border:1px solid var(--border-color,#e5e5ea);
  box-shadow:0 20px 60px -20px rgba(29,29,31,.12),0 6px 18px -6px rgba(29,29,31,.06);
  transition:transform .35s cubic-bezier(.25,1,.5,1),filter .35s cubic-bezier(.25,1,.5,1)}
.g-inner.lift{transform:translateY(-10px) scale(1.04);filter:brightness(1.05)}
.g-inner img{width:100%;height:100%;object-fit:cover;border-radius:9px;display:block}
`;

/* ---------- 建卡与 render(t) ---------- */

const COLS = 6, ROWS = 4, ENTRY_SEC = 6;                    // 24 卡，入场段 6s
const easeOutCubic = t => 1 - Math.pow(1 - t, 3);
const clamp01 = v => Math.max(0, Math.min(1, v));
const wall = document.querySelector('.gallery-canvas');
const MAXD = Math.hypot((COLS - 1) / 2, (ROWS - 1) / 2);
const cards = Array.from({ length: COLS * ROWS }, (_, i) => {
  const outer = document.createElement('div'); outer.className = 'g-card';
  const body  = document.createElement('div'); body.className  = 'g-body';
  const inner = document.createElement('div'); inner.className = 'g-inner';
  const img = new Image();
  img.src = `assets/shot-${String(i + 1).padStart(2, '0')}.png`;
  img.alt = `展品 ${i + 1}`;
  inner.appendChild(img); body.appendChild(inner); outer.appendChild(body); wall.appendChild(outer);
  inner.addEventListener('pointerenter', () => inner.classList.add('lift'));
  inner.addEventListener('pointerleave', () => inner.classList.remove('lift'));
  const col = i % COLS, row = (i / COLS) | 0;
  const dc = col - (COLS - 1) / 2, dr = row - (ROWS - 1) / 2;
  return { outer, body, inner, i, dc, dr, delay: Math.hypot(dc, dr) / MAXD * 0.55 };
});

function render(t) {                                          // t 归一化：[0,1] 入场段
  const sec = t * ENTRY_SEC;
  for (const c of cards) {
    const p = easeOutCubic(clamp01((t - c.delay) / 0.45));    // 错峰入场：距中心越远越晚
    const px = Math.sin(sec * 0.5 + c.i * 0.7) * 10 * p;      // 驻场慢漂：两条不可通约频率，
    const py = Math.cos(sec * 0.37 + c.i * 1.1) * 8 * p;      // 避免 marquee 式循环感
    c.outer.style.opacity = p;
    c.outer.style.transform =
      `translate3d(${(1 - p) * c.dc * 60 + px}px, ${(1 - p) * (c.dr * 50 + 40) + py}px, 0)` +
      ` scale(${0.9 + 0.1 * p})`;
  }
}

const host = wall.closest('.slide');
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let raf = 0, t0 = null;
function tick(now) {
  if (t0 === null) t0 = now;
  render((now - t0) / 1000 / ENTRY_SEC);                      // 不取模：无循环断点
  raf = requestAnimationFrame(tick);
}
function start() { if (!raf && !reduced) { t0 = null; raf = requestAnimationFrame(tick); } }
function stop()  { cancelAnimationFrame(raf); raf = 0; }
document.addEventListener('slidechange', e =>
  e.detail.index === +host.dataset.index ? start() : stop());
document.fonts.ready.then(() => {
  render(reduced ? 1 : 0);                                    // reduced-motion：直接终态静帧
  if (host.classList.contains('active')) start();
});
window.__seek = t => { stop(); render(t); };                  // 调试与 headless 截图入口
