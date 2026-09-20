/* ============================================================================
 * lightbox.js — 素材图点击放大（纯原生零依赖，自注入遮罩层）
 *
 * 来源：references/interactive-html-authoring.md「素材图网格与 lightbox」
 *       参考实现（逻辑逐字；HTML/CSS 块转为自注入，页面不必手写遮罩节点；
 *       缩略图点击加 stopPropagation——deck 集成必需，同 interactive-mode-rules.md
 *       热点规则条 4：不冒泡到左右半屏翻页热区）
 * 用途：交互页面素材图网格（.img-grid）的点击放大——点击缩略图弹出全屏
 *       遮罩显示放大图，Esc 或点击遮罩关闭，打开时 body 锁定滚动
 * 接线：复制进交付物 <script>，置于 DOM 就绪后执行（body 尾部即可）。
 *       缩略图容器类名固定 .img-grid；放大图用缩略图同一 src（原图高清
 *       落盘规则见来源 md：压的是格位占位空间，不是图片）
 * 可调参数：遮罩背景 rgba(0,0,0,.85)；放大图上限 92vw/92vh、object-fit:contain
 * 自检：点击缩略图弹出、Esc 关闭、点遮罩关闭；打开期间页面不滚动、关闭后
 *       恢复；放大图不拉伸变形、不超视口
 * ============================================================================ */

(function () {
  var LIGHTBOX_CSS = [
    '.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;z-index:999}',
    '.lightbox.open{display:flex}',
    '.lightbox img{max-width:92vw;max-height:92vh;object-fit:contain}'
  ].join('\n');

  var lb = document.getElementById('lightbox');
  if (!lb) {
    var style = document.createElement('style');
    style.textContent = LIGHTBOX_CSS;
    document.head.appendChild(style);
    lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.id = 'lightbox';
    lb.innerHTML = '<img alt="">';
    document.body.appendChild(lb);
  }
  var big = lb.querySelector('img');
  document.querySelectorAll('.img-grid img').forEach(function (t) {
    t.addEventListener('click', function (e) { e.stopPropagation(); big.src = t.src; lb.classList.add('open'); document.body.style.overflow = 'hidden'; });
  });
  function close() { lb.classList.remove('open'); document.body.style.overflow = ''; }
  lb.addEventListener('click', close);
  addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
