/* ============================================================================
 * easing.js — 缓动唯一实现：闭式阻尼弹簧 springEase + 采样线性化 + 三条过冲曲线
 *
 * 来源：references/keyframe-animation.md（逐字提取；md 明示"缓动函数以本节为
 *       唯一实现，其他文件只留指针不复制代码"）
 * 用途：springEase 闭式阻尼弹簧（进度纯函数——无状态、不逐帧积分、可任意跳转
 *       回退，天然确定性；实时弹簧积分器禁止用于编排动画）；sampleToLinear
 *       把任意 ease 采样成 CSS linear() 缓动串（Chrome 113+，可用于
 *       transition/WAAPI）；backOut / elasticOut / bounceOut 过冲族闭式公式
 *       （rAF 与 canvas 共用）
 * 接线：复制进交付物 <script>。springEase 返回 { duration, ease }——duration
 *       和 ease 都从返回值取（安定时间就是物理的一部分；调快慢应调 response，
 *       不是改 duration）。落地两条路：路线1 sampleToLinear(ease) 得 CSS
 *       缓动串；路线2 rAF 驱动，每帧算 ease(p) 写 transform（DOM 与 canvas
 *       通用，无兼容性问题）。
 * 可调参数：response ≈ 一次振荡的周期秒数（入场 0.3-0.6）；dampingFraction
 *       1.0 临界阻尼无过冲（默认，商务/汇报标准安定）、0.80-0.85 系统级质感
 *       （过冲 ~1-1.5%）、0.60-0.70 俏皮语域（过冲 ~5-10%，少用）、
 *       <0.55 禁止（卡通抖动区）；backOut 的 s 默认 1.70158
 * 工艺要点（md 原文）：ζ<1 时过冲曲线只能上 transform，禁止上 opacity（会冲破
 *       1）和颜色，opacity 拆到同一起点的独立 quad-out 轨；
 *       in 变体 = 1 - out(1 - t)；inOut 变体 = 前半 out(2t)/2、后半 out(2t-1)/2 + 0.5
 * ============================================================================ */

/* ---------- 闭式阻尼弹簧（springEase） ---------- */

// response ≈ 一次振荡的周期秒数（入场用 0.3-0.6）
// dampingFraction 1.0    = 临界阻尼，无过冲（默认）
//                 0.80-0.85 ≈ 系统级质感，过冲 ~1-1.5%，能感觉到但看不出来
//                 0.60-0.70 = 俏皮语域，过冲 ~5-10%（少用）
function springEase({ response = 0.5, dampingFraction = 1 } = {}) {
  const w = (2 * Math.PI) / response;
  const z = dampingFraction;
  let pos;
  if (z < 1) {
    const wd = w * Math.sqrt(1 - z * z);
    pos = (t) => 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t));
  } else if (z > 1) {
    const wo = w * Math.sqrt(z * z - 1);
    pos = (t) => 1 - Math.exp(-z * w * t) * (Math.cosh(wo * t) + ((z * w) / wo) * Math.sinh(wo * t));
  } else {
    pos = (t) => 1 - Math.exp(-w * t) * (1 + w * t);
  }
  const EPS = 0.001;
  const rate = z <= 1 ? z * w : (z - Math.sqrt(z * z - 1)) * w;
  const SCAN = 12 / rate;
  const N = 4800;
  let T = SCAN;
  for (let i = N; i >= 0; i--) {
    const t = (i / N) * SCAN;
    if (Math.abs(1 - pos(t)) > EPS) { T = ((i + 1) / N) * SCAN; break; }
  }
  const xT = pos(T);
  return { duration: T, ease: (p) => pos(p * T) + p * (1 - xT) };
}

/* ---------- 采样线性化（WAAPI/CSS 不接受任意函数的落地路线1） ---------- */

// 路线1：采样成 CSS linear() 缓动串（Chrome 113+），可直接用于 transition/WAAPI
function sampleToLinear(ease, n = 32) {
  const pts = [];
  for (let i = 0; i <= n; i++) pts.push(`${ease(i / n).toFixed(4)} ${((i / n) * 100).toFixed(2)}%`);
  return `linear(${pts.join(', ')})`;
}

// 路线2：rAF 驱动，每帧算 ease(p) 写 transform——DOM 与 canvas 通用，无兼容性问题

/* ---------- 过冲/弹跳/弹性闭式公式（rAF 与 canvas 共用） ---------- */

function backOut(t, s = 1.70158) { return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); }
function elasticOut(t) {
  if (t === 0 || t === 1) return t;
  return Math.pow(2, -10 * t) * Math.sin((t - 0.075) * (2 * Math.PI) / 0.3) + 1;
}
function bounceOut(t) {
  if (t < 1 / 2.75) return 7.5625 * t * t;
  if (t < 2 / 2.75) return 7.5625 * (t -= 1.5 / 2.75) * t + 0.75;
  if (t < 2.5 / 2.75) return 7.5625 * (t -= 2.25 / 2.75) * t + 0.9375;
  return 7.5625 * (t -= 2.625 / 2.75) * t + 0.984375;
}

// in 变体 = 1 - out(1 - t)；inOut 变体 = 前半 out(2t) / 2、后半 out(2t - 1) / 2 + 0.5
