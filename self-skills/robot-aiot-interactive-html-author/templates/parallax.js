/* ============================================================================
 * parallax.js — 页面级多层视差（鼠标驱动 + 滚动驱动）
 *
 * 来源：references/camera-storyboard.md §8（逐字提取）
 * 用途：同一驱动信号按层给出不同位移，层间速度差即深度感——质感不是运镜，
 *       振幅锁在微位移级，不计入也不得挪用运镜预算
 * 接线：复制进交付物 <script>。鼠标驱动 mountParallax(stage, layers, amp)
 *       返回 dispose 函数——离开页面时调用（生命周期契约，随页启停，
 *       见 generative-art-and-canvas.md）；滚动驱动 scrollParallax(layers)
 *       仅长页滚动叙事形态用（deck 内 1920×1080 画布无滚动条）。
 *       层元素自备 .px-far / .px-mid / .px-near（或任意选择器）。
 * 可调参数：amp 鼠标驱动振幅（近层 ≤28px）；层位移系数 k：远 0.35 / 中 0.7 /
 *           近 1.4（相邻层速度比 ≥2 才可辨）；平滑系数 0.1；滚动振幅 120px 基准
 * 纪律：层数 ≤4；所有层由同一驱动信号派生，禁止每层独立动画；
 *       reduced-motion 在挂载入口检测，命中即不挂监听不起循环、零位移静帧
 * ============================================================================ */

function mountParallax(stage, layers, amp = 20) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return () => {};
  let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0;
  const onMove = (e) => {
    const r = stage.getBoundingClientRect();
    tx = ((e.clientX - r.left) / r.width - 0.5) * 2;      // 归一化到 [-1, 1]
    ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
  };
  const loop = () => {
    cx += (tx - cx) * 0.1;                                 // 指数平滑：跟得紧但不抖
    cy += (ty - cy) * 0.1;
    for (const L of layers) {
      L.el.style.transform = `translate3d(${(-cx * amp * L.k).toFixed(2)}px, ${(-cy * amp * L.k).toFixed(2)}px, 0)`;
    }
    raf = requestAnimationFrame(loop);
  };
  stage.addEventListener('pointermove', onMove);
  raf = requestAnimationFrame(loop);
  return () => {                                           // 离开页面时调用（生命周期契约）
    cancelAnimationFrame(raf);
    stage.removeEventListener('pointermove', onMove);
    for (const L of layers) L.el.style.transform = 'none';
  };
}

const dispose = mountParallax(document.querySelector('.camera-stage'), [
  { el: document.querySelector('.px-far'),  k: 0.35 },
  { el: document.querySelector('.px-mid'),  k: 0.7  },
  { el: document.querySelector('.px-near'), k: 1.4  }
]);

/* ---------- 滚动驱动（仅长页滚动叙事形态） ---------- */

function scrollParallax(layers) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const doc = document.scrollingElement;
  addEventListener('scroll', () => {
    const p = doc.scrollTop / (doc.scrollHeight - innerHeight);   // [0, 1]
    for (const L of layers) {
      L.el.style.transform = `translate3d(0, ${(-p * 120 * L.k).toFixed(2)}px, 0)`;
    }
  }, { passive: true });
}
