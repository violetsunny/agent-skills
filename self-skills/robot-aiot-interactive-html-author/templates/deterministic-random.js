/* ============================================================================
 * deterministic-random.js — 确定性随机与粒子物理质感（mulberry32 / hash2d /
 *                            squashStretch / arcMotion）
 *
 * 来源：references/generative-art-and-canvas.md（逐字提取："确定性随机"与
 *       "粒子物理质感（挤压拉伸与弧线）"两节）
 * 用途：动画帧内禁止 Math.random()——同一时刻会渲染出不同像素，翻回页面重
 *       触发时效果每次都不一样。mulberry32 种子 PRNG（同 seed 同序列）；
 *       hash2d 整数 hash（由元素索引/网格坐标直接派生伪随机值，无状态、
 *       同输入同输出）；squashStretch 体积守恒挤压拉伸；arcMotion 抛物线弧线
 * 接线：复制进交付物 <script>，供 canvas FX / 粒子系统调用。p5.js 语境用
 *       randomSeed(seed) / noiseSeed(seed)，同 seed 必须产出相同结果。
 *       paper-texture.js 依赖本文件的 hash2d。
 * 可调参数：mulberry32 的 seed；squashStretch 的 intensity（落地反弹瞬间
 *       0.3-0.6，2-3 帧内恢复）与 direction；arcMotion 的 height
 *       （= 水平距离的 10-25%）
 * 配套：反弹衰减配 easing.js 的 bounceOut 闭式公式；种子随机序列在启动前
 *       一次生成完毕（render(t) 纯函数契约）
 * ============================================================================ */

// 种子 PRNG：同一 seed 产出同一随机序列
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// 整数 hash：由元素索引/网格坐标直接派生伪随机值，无状态、同输入同输出
function hash2d(x, y) {
  let h = (x * 374761393 + y * 668265263) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

// 体积守恒挤压拉伸：落地/撞击瞬间沿冲击轴压扁、垂直轴变宽
function squashStretch(intensity, direction = 'vertical') {
  return direction === 'vertical'
    ? { sx: 1 + intensity * 0.5, sy: 1 - intensity * 0.5 }
    : { sx: 1 - intensity * 0.5, sy: 1 + intensity * 0.5 };
}

// 抛物线弧线轨迹：x 线性，y = 线性插值 + 峰值在 t=0.5 的弧线偏移
function arcMotion(start, end, height, t) {
  const x = start.x + (end.x - start.x) * t;
  const y = start.y + (end.y - start.y) * t - 4 * height * t * (1 - t);
  return { x, y };
}
