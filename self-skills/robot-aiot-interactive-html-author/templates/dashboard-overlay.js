/* ============================================================================
 * dashboard-overlay.js — 仪表盘浮层（遮罩压暗 → 卡片 stagger → 数字滚动 → 折线自绘）
 *
 * 来源：references/ui-demo-choreography.md §8（逐字提取；md 原形态为
 *       HTML / CSS / JS 三个独立代码块，此处 HTML 与 CSS 保留为模板字符串常量）
 * 用途：数据卡片从演示截图/页面之上逐层浮现的编排层完整实现
 * 接线：DASH_HTML 插入演示页 section 内（演示截图之上），DASH_CSS 写入页面
 *       <style>，JS 段复制进 <script>；触发 playDashboard(document.getElementById('dash'))。
 *       接 templates/demo-clock.js 调度器时，卡片 stagger 与数字滚动的 setTimeout
 *       改为 cue 时刻表。占位数据必须标"示意"（SKILL.md 硬约束 6）。
 * 依赖说明：CSS 变量 --primary-color / --border-color / --text-secondary 来自
 *           deck token 体系；.dash-card 的绝对定位坐标（left/top）按演示页
 *           截图布局自行补写（md 原块即不含定位值）
 * 可调参数：遮罩 300ms；卡片 delay 200+i×120ms、500ms expo-out；数字滚动
 *           1200ms cubic-out（countTo 内 dur）；折线 delay 600ms、1400ms；
 *           data-count / data-decimals / data-suffix 在 HTML 上声明
 * 契约：数字滚动有终止条件并 snap 精确值；tabular-nums 防抖；reduced-motion
 *       直显终态；全部落定 hold ≥1s（§5 铁律 6，由调度侧保证）
 * ============================================================================ */

/* ---------- HTML 结构（插入演示页） ---------- */

const DASH_HTML = `
<div class="dash-overlay" id="dash">
  <div class="dash-card" data-count="1284">
    <div class="k">在线设备</div><div class="v"><span class="num">0</span><span class="suf"></span></div>
  </div>
  <div class="dash-card" data-count="99.2" data-decimals="1" data-suffix="%">
    <div class="k">指令成功率</div><div class="v"><span class="num">0</span><span class="suf"></span></div>
  </div>
  <div class="dash-card wide">
    <div class="k">近 24h 上行消息（示意）</div>
    <svg viewBox="0 0 480 120" class="spark" aria-hidden="true"><polyline points="0,100 40,88 80,92 120,70 160,74 200,52 240,58 280,40 320,46 360,30 400,36 440,18 480,24" fill="none" stroke="var(--primary-color)" stroke-width="3" stroke-linejoin="round"/></svg>
  </div>
</div>
`;

/* ---------- CSS（写入页面样式表） ---------- */

const DASH_CSS = `
.dash-overlay{position:absolute;inset:0;z-index:40;background:rgba(10,15,30,.55);opacity:0}
.dash-card{position:absolute;width:360px;padding:24px 28px;background:#fff;border-radius:14px;
  border:1px solid var(--border-color,#e5e5ea);box-shadow:0 24px 64px -24px rgba(15,23,42,.35);opacity:0}
.dash-card .k{font-size:14px;color:var(--text-secondary,#545458)}
.dash-card .v{font-size:44px;font-weight:700;font-variant-numeric:tabular-nums}
.dash-card .suf{font-size:24px;margin-left:4px}
.spark{width:100%;height:120px}
`;

/* ---------- 编排 JS ---------- */

function countTo(el, card) {
  const target = parseFloat(card.dataset.count);
  const dec = parseInt(card.dataset.decimals || '0', 10);
  const dur = 1200, t0 = performance.now();
  (function step(now) {
    const p = Math.min(1, (now - t0) / dur);
    el.textContent = (target * (1 - Math.pow(1 - p, 3))).toFixed(dec);   // cubic-out
    if (p < 1) { requestAnimationFrame(step); return; }
    el.textContent = target.toFixed(dec);                                // 终止 snap 精确值
    const suf = card.querySelector('.suf');
    if (suf && card.dataset.suffix) {
      suf.textContent = card.dataset.suffix;
      suf.animate([{ opacity: 0, transform: 'scale(.6)' }, { opacity: 1, transform: 'scale(1)' }],
        { duration: 400, easing: 'cubic-bezier(0.34,1.56,0.64,1)', fill: 'both' });
    }
  })(t0);
}
function playDashboard(root) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const cards = [...root.querySelectorAll('.dash-card')];
  const line = root.querySelector('.spark polyline');
  const len = line ? line.getTotalLength() : 0;
  if (line) line.style.strokeDasharray = len;
  if (reduced) {                                             // 降级：直显终态
    root.style.opacity = 1;
    cards.forEach(c => { c.style.opacity = 1;
      const n = c.querySelector('.num');
      if (n) n.textContent = (+c.dataset.count).toFixed(+(c.dataset.decimals || 0));
      const s = c.querySelector('.suf'); if (s && c.dataset.suffix) s.textContent = c.dataset.suffix; });
    if (line) line.style.strokeDashoffset = 0;
    return;
  }
  root.animate([{ opacity: 0 }, { opacity: 1 }],
    { duration: 300, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
  cards.forEach((card, i) => {
    const delay = 200 + i * 120;
    card.animate([{ opacity: 0, transform: 'translateY(24px) scale(.96)' },
                  { opacity: 1, transform: 'translateY(0) scale(1)' }],
      { duration: 500, delay, easing: 'cubic-bezier(0.16,1,0.3,1)', fill: 'both' });
    const num = card.querySelector('.num');
    if (num && card.dataset.count) setTimeout(() => countTo(num, card), delay + 300);
  });
  if (line) line.animate([{ strokeDashoffset: len }, { strokeDashoffset: 0 }],
    { duration: 1400, delay: 600, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
}
