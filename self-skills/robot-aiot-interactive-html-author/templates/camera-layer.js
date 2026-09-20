/* ============================================================================
 * camera-layer.js — 相机层三层容器 + 相机定位/飞行/反向补偿
 *
 * 来源：references/camera-storyboard.md §4（逐字提取）；zoomDuration /
 *       panDuration 取自同文件 §3（md 明示"本文件唯一实现，其余节直接调用"，
 *       flyTo 依赖 zoomDuration，故一并收录保证可运行）
 * 用途：镜头运动与元素动画分家——所有镜头级运动收口到专职三层容器
 *       （.camera-stage 视口 / .camera-layer 相机 / .content 内容），
 *       运镜只写 .camera-layer 的 transform
 * 接线：CAMERA_HTML 结构写进相机页 section，CAMERA_CSS 写入页面 <style>，
 *       JS 段复制进 <script>。相机状态 = { cx, cy, zoom }，(960,540) 为画布中心。
 *       will-change 只在运镜期间提升（flyTo 已内置），禁止 CSS 常驻。
 * 可调参数：时长来自 zoomDuration（对数公式 0.55s×log2，clamp [0.3,1.5]s）与
 *           panDuration（600px/s，clamp [0.4,1.4]s）；缓动 quart-out
 *           cubic-bezier(0.22,1,0.36,1)；3D 运镜时 .camera-stage 加
 *           perspective 1100-1200px
 * 施工坑（详见 md §4）：横移露边需 .content 外扩 ≥ 位移量+32px；
 *       .camera-layer 与 .content 之间禁 overflow:hidden/filter/opacity<1 中间层；
 *       全局 chrome 叠字用 body:has(#sN.active) 隐藏全局件
 * ============================================================================ */

/* ---------- 容器结构 HTML（写进相机页） ---------- */

const CAMERA_HTML = `
<div class="camera-stage">                    <!-- 视口层：固定 1920×1080，overflow hidden，不动 -->
  <div class="camera-layer">                  <!-- 相机层：只承载相机 transform，运镜全部收口在这 -->
    <div class="content">…页面内容…</div>      <!-- 内容层：页面内容住这里 -->
  </div>
  <div class="stage-hud">…页码/角标/比例尺…</div>  <!-- 与相机层平级，天然不跟镜头动 -->
</div>
`;

/* ---------- 容器 CSS（写入页面样式表） ---------- */

const CAMERA_CSS = `
.camera-stage { position: relative; width: 1920px; height: 1080px; overflow: hidden; }
.camera-layer { position: absolute; inset: 0; transform-origin: 0 0; }
.content      { position: absolute; inset: 0; }
.stage-hud    { position: absolute; inset: 0; z-index: 10; pointer-events: none; }
`;

/* ---------- 时长公式（§3 唯一实现） ---------- */

// 返回秒。任意起止倍率均有效，自动取绝对值并 clamp
function zoomDuration(zoomStart, zoomEnd) {
  const d = 0.55 * Math.log2(zoomEnd / zoomStart);
  return Math.min(1.5, Math.max(0.3, Math.abs(d)));
}

// 位移 px → 秒，基准速度 600px/s，clamp [0.4, 1.4]s
function panDuration(distancePx, speed = 600) {
  return Math.min(1.4, Math.max(0.4, Math.abs(distancePx) / speed));
}

/* ---------- 相机定位与飞行（WAAPI，时长来自 §3，缓动 quart-out） ---------- */

// 相机状态 = { cx, cy, zoom }：(cx, cy) 是镜头对准的世界坐标点，画布中心为 (960, 540)
function cameraTransform({ cx, cy, zoom }) {
  return `translate(${(960 - cx * zoom).toFixed(2)}px, ${(540 - cy * zoom).toFixed(2)}px) scale(${zoom})`;
}

function flyTo(layer, from, to) {
  layer.style.willChange = 'transform';
  const anim = layer.animate(
    [{ transform: cameraTransform(from) }, { transform: cameraTransform(to) }],
    { duration: zoomDuration(from.zoom, to.zoom) * 1000,
      easing: 'cubic-bezier(0.22, 1, 0.36, 1)', fill: 'both' }
  );
  anim.finished.then(() => { layer.style.willChange = 'auto'; });
  return anim;
}

/* ---------- counter-transform 反向补偿（字号恒定的标注/比例尺） ---------- */

function counterFly(el, fromZoom, toZoom, durationMs) {
  return el.animate(
    [{ transform: `scale(${1 / fromZoom})` }, { transform: `scale(${1 / toZoom})` }],
    { duration: durationMs, easing: 'cubic-bezier(0.22, 1, 0.36, 1)', fill: 'both' }
  );
}
