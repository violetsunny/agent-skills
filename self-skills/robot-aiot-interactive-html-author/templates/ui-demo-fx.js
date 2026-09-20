/* ============================================================================
 * ui-demo-fx.js — UI 演示八式函数群（式①-⑧ 帧级实现）
 *
 * 来源：references/ui-demo-choreography.md §3（八式帧级参数，逐字提取）
 * 用途：UI 演示页的八种演示式——①光标引导点击 ②区域高亮聚焦 ③步骤序列播放
 *       ④数据流动画 ⑤状态切换对比 ⑥缩放深入细节 ⑦打字输入演示 ⑧滚动浏览演示
 * 接线：复制进交付物 <script>。CSS 段（FOCUS_RING_CSS / CARET_CSS）写入页面
 *       <style> 或用注入 helper 挂载。各式可独立播放（自带 rAF/finished 链）；
 *       接入 templates/demo-clock.js 调度器时改用统一时钟 clock.t 驱动。
 * 依赖说明（md 原文即如此，复制时需自备）：
 *   - playStep 中的 cursorClick(el) = 式① moveCursor + 涟漪 + 按压组合
 *     （元素级参数见 animation-fx-catalog.md cursor-press-duet / click-ripple）
 *   - playStep 中的 stage = 演示舞台容器元素
 *   - CSS 变量 --primary-color 来自 deck token 体系
 *   - 式①的"双圈涟漪"片段是点击落点后的用法示例（md 原形态为顶层代码，
 *     .ring-52/.ring-76 不在 DOM 时立即执行会抛错）——复制时移入触发函数内
 *   - STEPS/CAPTION 为式③示例数据，按实际演示目标改写
 * 可调参数：各式函数签名默认值（dur/holdMs/speed/gap/scale/perChar 等），
 *           帧级纪律（时长区间/停顿下限）以 ui-demo-choreography.md §3 为准
 * ============================================================================ */

/* ---------- 式① 光标引导点击 ---------- */

// 式②聚焦环 CSS（写入页面样式表）
const FOCUS_RING_CSS = `
#focus-ring{position:absolute;z-index:60;pointer-events:none;opacity:0;
  border:2px solid var(--primary-color);
  box-shadow:0 0 0 9999px rgba(10,15,30,.55)}
`;

// 式⑦光标 CSS（写入页面样式表）
const CARET_CSS = `
.caret{display:inline-block;width:2px;height:1.1em;background:var(--primary-color);vertical-align:-0.15em}
.caret.blink{animation:caret-blink 1s steps(1) infinite}
@keyframes caret-blink{50%{opacity:0}}
`;

// 光标外层管轨迹 translate，内层管按压 scale——两层两职，不抢同一 transform
function moveCursor(cursor, p0, p2, dur = 800) {
  const p1 = [(p0[0] + p2[0]) / 2 - 120, (p0[1] + p2[1]) / 2 + 70]; // 控制点偏离中点制造弧线
  return new Promise(res => {
    const t0 = performance.now();
    (function frame(now) {
      const p = Math.min(1, (now - t0) / dur);
      const e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2; // smooth-inout 二次近似
      const k = 1 - e;
      let x = k * k * p0[0] + 2 * k * e * p1[0] + e * e * p2[0];
      let y = k * k * p0[1] + 2 * k * e * p1[1] + e * e * p2[1];
      x += Math.sin(e * 47.13) * 2 * k;              // 手抖 ±2px，接近目标收敛
      y += Math.sin(e * 33.7 + 1.3) * 2 * k;
      cursor.style.transform = `translate(${x}px, ${y}px)`;
      p < 1 ? requestAnimationFrame(frame) : res();
    })(t0);
  });
}
// 双圈涟漪：环元素常驻 DOM（scale 0 / opacity 0），fill:forwards 不预渲染起始态
[[0, 52], [100, 76]].forEach(([delay, half]) => {
  document.querySelector(`.ring-${half}`).animate(
    [{ transform: 'scale(0.2)', opacity: 0.55 }, { transform: 'scale(1)', opacity: 0 }],
    { duration: 650, delay, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
});

/* ---------- 式② 区域高亮聚焦 ---------- */

function focusRegion(host, target, holdMs = 1600) {
  const ring = host.querySelector('#focus-ring');
  const h = host.getBoundingClientRect(), r = target.getBoundingClientRect(), pad = 10;
  Object.assign(ring.style, {
    left: (r.left - h.left - pad) + 'px', top: (r.top - h.top - pad) + 'px',
    width: (r.width + pad * 2) + 'px', height: (r.height + pad * 2) + 'px',
    borderRadius: (parseFloat(getComputedStyle(target).borderRadius) + pad) + 'px'
  });
  ring.animate([{ opacity: 0, transform: 'scale(1.08)' }, { opacity: 1, transform: 'scale(1)' }],
    { duration: 400, easing: 'cubic-bezier(0.34,1.56,0.64,1)', fill: 'forwards' });
  ring.animate([{ opacity: 1 }, { opacity: 0 }],
    { duration: 300, delay: 400 + holdMs, easing: 'cubic-bezier(0.32,0,0.67,0)', fill: 'forwards' });
}

/* ---------- 式③ 步骤序列播放 ---------- */

const STEPS = [
  { target: '#tab-devices', act: 'click',  beat: '打开设备列表' },
  { target: '#row-gw-03',   act: 'focus',  beat: '选中网关 GW-03' },
  { target: '#btn-reboot',  act: 'click',  beat: '下发重启指令' },
  { target: '#toast-ok',    act: 'reveal', beat: '指令已确认，等待设备重连' }
];
const CAPTION = document.getElementById('demo-caption');
function playStep(i) {
  const s = STEPS[i], el = document.querySelector(s.target);
  CAPTION.textContent = `${i + 1}/${STEPS.length} · ${s.beat}`;
  CAPTION.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 240, easing: 'linear', fill: 'both' });
  if (s.act === 'click')  return cursorClick(el);                 // 式①
  if (s.act === 'focus')  { focusRegion(stage, el); return Promise.resolve(); } // 式②
  el.animate([{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'translateY(0)' }],
    { duration: 400, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'both' });
  return Promise.resolve();
}

/* ---------- 式④ 数据流动画 ---------- */

function spawnPackets(pathSel, dots, speed = 300, gap = 500, loops = 3) {
  const d = document.querySelector(pathSel).getAttribute('d');
  const len = document.querySelector(pathSel).getTotalLength();
  dots.forEach((dot, i) => {
    dot.style.offsetPath = `path("${d}")`;
    dot.animate([
      { offsetDistance: '0%',   opacity: 0 },
      { offsetDistance: '6%',   opacity: 1 },
      { offsetDistance: '94%',  opacity: 1 },
      { offsetDistance: '100%', opacity: 0 }
    ], { duration: len / speed * 1000, easing: 'linear', delay: i * gap,
         iterations: loops, fill: 'both' });   // 有限次循环，禁 Infinity
  });
}

/* ---------- 式⑤ 状态切换对比 ---------- */

// 幕布擦除只用 transform：after 窗口层反向平移、内容层等量正向平移，
// 内容始终静止，只有"可见窗口"滑动——不用 clip-path、不动 width
function wipe(stage, wrap, inner, handle, pct, dur = 900) {
  const W = stage.clientWidth, x = W * pct;
  const opts = { duration: dur, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' };
  wrap.animate([{ transform: `translateX(${-W}px)` }, { transform: `translateX(${x - W}px)` }], opts);
  inner.animate([{ transform: `translateX(${W}px)` }, { transform: `translateX(${W - x}px)` }], opts);
  handle.animate([{ transform: 'translateX(0)' }, { transform: `translateX(${x}px)` }], opts);
}

/* ---------- 式⑥ 缩放深入细节 ---------- */

function zoomInto(shotFrame, hiSlice, cx, cy, scale = 1.8) {
  shotFrame.style.transformOrigin = `${cx}px ${cy}px`;
  shotFrame.animate([{ transform: 'scale(1)' }, { transform: `scale(${scale})` }],
    { duration: 750, easing: 'cubic-bezier(0.22,1,0.36,1)', fill: 'forwards' });
  hiSlice.animate([{ opacity: 0 }, { opacity: 1 }],
    { duration: 200, delay: 480, easing: 'linear', fill: 'forwards' });
}

/* ---------- 式⑦ 打字输入演示 ---------- */

// 把"打→打错→停→退→改"编译成字符事件表，渲染层按时间查表，任意 t 可回放
function compileTypeScript(text, perChar = 120, typo = null) {
  const ev = []; let t = 0;
  for (let i = 0; i < text.length; i++) {
    if (typo && i === typo.at) {
      ev.push({ t, s: text.slice(0, i) + typo.wrong }); t += perChar;
      t += typo.pause;                                   // 停一拍（150-200ms）
      ev.push({ t, s: text.slice(0, i) }); t += perChar; // 退格
    }
    ev.push({ t, s: text.slice(0, i + 1) });
    t += perChar;
  }
  return { ev, total: t };
}
function renderType(el, caret, script, time) {
  let n = -1;
  while (n + 1 < script.ev.length && script.ev[n + 1].t <= time) n++;
  el.textContent = n < 0 ? '' : script.ev[n].s;
  caret.classList.toggle('blink', time >= script.total);
}

/* ---------- 式⑧ 滚动浏览演示 ---------- */

function scrollBrake(strip, fromY, toY, dur = 900) {
  return strip.animate(
    [{ transform: `translateY(${-fromY}px)` }, { transform: `translateY(${-toY}px)` }],
    { duration: dur, easing: 'cubic-bezier(0.16,1,0.3,1)', fill: 'forwards' }).finished;
}
async function scrollDemo(strip, stops) {          // stops: [{y, row}]，独立播放形态
  let y = 0;
  for (const s of stops) {
    await scrollBrake(strip, y, s.y);
    y = s.y;
    s.row.animate([{ filter: 'brightness(1)' }, { filter: 'brightness(1.12)' }],
      { duration: 300, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
    await new Promise(r => setTimeout(r, 1200));  // 接 §9 调度器时改为 cue 时刻，不用 setTimeout 链
  }
}
