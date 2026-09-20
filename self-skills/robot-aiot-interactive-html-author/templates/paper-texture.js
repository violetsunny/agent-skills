/* ============================================================================
 * paper-texture.js — 程序化纸纹（fractalNoise）：SVG 滤镜 data-URI 路线 +
 *                     canvas fBm 逐像素生成路线
 *
 * 来源：references/generative-art-and-canvas.md "程序化纸纹（fractalNoise）"
 *       （逐字提取，两条路线都收录；hash2d 从同文件"确定性随机"节随带收录，
 *       与 templates/deterministic-random.js 同源——两模板同页合用时删除
 *       本文件内的 hash2d 段，避免重复声明）
 * 用途：浅色底叠一层极弱的分形噪声纸纹——"看上去没区别，去掉就知道有了"。
 *       纸纹是静态纹理不是动效：一次生成、平铺复用，不占"一页一效"名额，
 *       不触发持续重绘
 * 接线：两条原生路线选一条——
 *       路线一（零 JS）：PAPER_SVG_CSS 写入页面 <style>，宿主元素加 .paper
 *       路线二（可读色 token、可导出纹块）：复制 JS 段，用法见 paperTexture
 *       尾部三行注释（宿主背景 / canvas 底纹 / 墨色读 token）
 * 可调参数：size 纹块边长（默认 200）；basePeriod 格点周期（≈ size × 0.85，
 *       细颗粒读作"纸"，低频大颗粒读作"云/大理石"）；seed；ink 墨色 [r,g,b]
 *       （按主题文字色 token 换算，不硬编码）；alpha ≤0.04（SVG 路线
 *       feColorMatrix alpha 0.035 量级 + 整体 opacity ≤0.5）
 * 纪律：强度在"几乎不可察"档，能看出"噪点/屏幕脏"即过强立刻减；只给浅色底；
 *       禁止叠在动画内容上（逐帧压缩导出体积与画质双爆）；同页纹理层 ≤1，
 *       不与 ASCII 呼吸场等点阵质感背景叠加；z-index 盖在内容之上且不拦截交互
 * ============================================================================ */

/* ---------- 路线一 · SVG 滤镜 data-URI（零 JS，CSS 背景平铺） ---------- */

const PAPER_SVG_CSS = `
.paper::before {
  content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 30;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.078  0 0 0 0 0.078  0 0 0 0 0.074  0 0 0 0.035 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity: 0.5;
}
`;
// feColorMatrix 的三个通道常量即墨色（按主题文字色 token 换算成 0-1 小数替换，
// data-URI 内读不到 CSS 变量）；stitchTiles='stitch' 保证四方连续无缝；
// z-index 按宿主层级调整，原则是盖在内容之上且不拦截交互。

/* ---------- 路线二 · canvas fBm 逐像素生成（可读色 token、可导出纹块） ---------- */

// 依赖：hash2d（与 templates/deterministic-random.js 同源，合用时删此段）
function hash2d(x, y) {
  let h = (x * 374761393 + y * 668265263) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

// 值噪声格点 + smoothstep 双线性插值，双 octave 叠加（fBm）：频率 ×2、振幅 ×0.5
// 格点值由 hash2d 直接派生（见上方"确定性随机"），同 seed 恒同纹块；
// 格点坐标对 period 取模回绕采样，保证四边无缝平铺
function paperTexture({ size = 200, basePeriod = 170, seed = 42, ink = [20, 20, 19], alpha = 0.04 } = {}) {
  const cv = document.createElement('canvas');
  cv.width = cv.height = size;
  const ctx = cv.getContext('2d');
  const img = ctx.createImageData(size, size);
  const lattice = (period, ix, iy) =>
    hash2d((ix % period) * 331 + seed, (iy % period) * 337 + seed);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      let v = 0, total = 0;
      for (const [period, amp] of [[basePeriod, 0.5], [basePeriod * 2, 0.25]]) {
        const fx = (x / size) * period, fy = (y / size) * period;
        const x0 = Math.floor(fx), y0 = Math.floor(fy);
        const tx = fx - x0, ty = fy - y0;
        const sx = tx * tx * (3 - 2 * tx), sy = ty * ty * (3 - 2 * ty);
        v += amp * ((lattice(period, x0, y0) * (1 - sx) + lattice(period, x0 + 1, y0) * sx) * (1 - sy) +
                    (lattice(period, x0, y0 + 1) * (1 - sx) + lattice(period, x0 + 1, y0 + 1) * sx) * sy);
        total += amp;
      }
      const i4 = (y * size + x) * 4;
      img.data[i4] = ink[0]; img.data[i4 + 1] = ink[1]; img.data[i4 + 2] = ink[2];
      img.data[i4 + 3] = Math.round((v / total) * alpha * 255);   // 噪声值调 alpha，墨色恒定
    }
  }
  ctx.putImageData(img, 0, 0);
  return cv;
}
// 用法：宿主背景 document.querySelector('.cover').style.backgroundImage = `url(${paperTexture().toDataURL()})`;
// canvas 底纹：const pat = ctx.createPattern(paperTexture(), 'repeat'); ctx.fillStyle = pat; ctx.fillRect(0, 0, W, H);
// 墨色读 token：getComputedStyle 取文字色 hex 后拆成 [r, g, b] 传 ink，不硬编码
