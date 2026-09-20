/* ============================================================================
 * inline-editor.js — 内联文本编辑模式：浏览器内直接点上屏文字修改，不回源码
 *
 * 来源：references/interactive-mode-rules.md「内联文本编辑模式」（271-311）
 *       （乙类：md 只有行为规格 + 一段 hover 链示例，按规格实现完整可运行代码）
 * 用途：草稿生成后默认内置的轻量微调能力。三路入口并存：E 键切换 / 左上角
 *       80×80px 固定热区（hover 显现编辑按钮、点击热区直接切换）/ 编辑按钮点击。
 *       激活后给上屏文字元素加 contenteditable + 虚线 outline；输入即自动存
 *       localStorage（key 含 deck 文件名，读取走消毒纪律）；Ctrl+S/Cmd+S 导出
 *       改动后的完整 HTML（先剥离编辑态属性再序列化 Blob 下载）；刷新按稳定
 *       选择器（data-slide-id + 页内序号）回填，不整页覆盖 DOM。
 * 接线：复制进交付物 <script>，DOMContentLoaded 后自动 init（或手动
 *       InlineEdit.init()）。与 deck-nav.js / presenter-window.js 共存——E 键与
 *       翻页键同口径守卫（input/textarea/select/contenteditable 内不响应全局键）。
 *       .notes 话术容器不进编辑范围（话术改动回源文件）。
 * 热区 hover 链硬规则：禁止 CSS `~` 兄弟选择器（按钮 pointer-events:none 会断
 *       hover 链）；必须 JS 接管，400ms 宽限留出鼠标从热区移到按钮的时间；按钮
 *       可见性只由 .show/.active class 控制；编辑激活期间 mouseleave 不隐藏。
 * 可调参数：热区 80×80px；hover 宽限 400ms；可编辑选择器 EDITABLE_SELECTOR；
 *       localStorage key = 'deck-edits::' + deck 文件名。
 * 交付说明（§307）：hover 左上角或按 E 进编辑、点文字改、Ctrl+S 导出。
 * 验证：scripts/headless_assert.py——E 键切换后抽一个文字元素断言
 *       isContentEditable===true、输入后 localStorage 有记录；Ctrl+S 的 Blob
 *       下载在 headless 不可达，记入真浏览器抽查清单（与跨窗口同步同批）。
 * ============================================================================ */

window.InlineEdit = (function () {
  'use strict';

  var HOTZONE_SIZE = 80;
  var HOVER_GRACE = 400;
  var EDITABLE_SELECTOR = 'h1,h2,h3,h4,h5,h6,p,li,td,th,figcaption,.caption,[data-editable]';
  var BLOCKED_ANCESTOR = '.notes,script,style,textarea,input,select,button,[data-no-edit]';

  function deckKey() {
    var p = (location.pathname.split('/').pop() || 'deck').split('?')[0];
    return p || 'deck';
  }
  var STORE_KEY = 'deck-edits::' + deckKey();

  function safeParse(str, fallback) {
    if (str == null) return fallback;
    try { var v = JSON.parse(str); return (v && typeof v === 'object') ? v : fallback; } catch (_) { return fallback; }
  }
  // 消毒：剥离 script/style/iframe 等危险标签、on* 事件属性、javascript: 链接（§304 不注入未校验内容）
  function sanitizeHTML(html) {
    var tmp = document.createElement('div');
    tmp.innerHTML = String(html == null ? '' : html);
    tmp.querySelectorAll('script,style,iframe,object,embed,link,meta').forEach(function (n) { n.remove(); });
    tmp.querySelectorAll('*').forEach(function (el) {
      Array.prototype.slice.call(el.attributes).forEach(function (a) {
        var nm = a.name.toLowerCase();
        if (nm.indexOf('on') === 0) el.removeAttribute(a.name);
        if ((nm === 'href' || nm === 'src' || nm === 'xlink:href') && /^\s*javascript:/i.test(a.value)) el.removeAttribute(a.name);
      });
    });
    return tmp.innerHTML;
  }

  var isActive = false;
  var hideTimeout = null;
  var hotzone = null, toggle = null, styleEl = null, hintShown = false;

  /* ---------- 可编辑元素枚举（只取最外层匹配元素，避免 contenteditable 嵌套） ---------- */
  function isCandidate(el) {
    if (!el || el.nodeType !== 1) return false;
    if (el.closest(BLOCKED_ANCESTOR)) return false;
    try { return el.matches(EDITABLE_SELECTOR); } catch (_) { return false; }
  }
  function editablesIn(container) {
    var all = Array.prototype.slice.call(container.querySelectorAll(EDITABLE_SELECTOR));
    return all.filter(function (el) {
      if (!isCandidate(el)) return false;
      var p = el.parentElement;
      while (p && p !== container) { if (isCandidate(p)) return false; p = p.parentElement; }
      return true;
    });
  }
  function slideOf(el) { return el.closest ? el.closest('.slide') : null; }
  // 稳定选择器：data-slide-id（无则全局页序）+ 页内可编辑序号（§306）
  function stableKey(el) {
    var slide = slideOf(el);
    if (slide) {
      var sid = slide.getAttribute('data-slide-id');
      if (!sid) {
        var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
        sid = 'idx' + slides.indexOf(slide);
      }
      return sid + '::' + editablesIn(slide).indexOf(el);
    }
    return 'global::' + editablesIn(document.body).indexOf(el);
  }
  function allEditables() {
    var out = [];
    var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    if (slides.length) slides.forEach(function (s) { out = out.concat(editablesIn(s)); });
    else out = editablesIn(document.body);
    return out;
  }

  /* ---------- 持久化 ---------- */
  function loadStore() { return safeParse(localStorage.getItem(STORE_KEY), {}); }
  function saveEntry(key, html) {
    var store = loadStore();
    store[key] = html;
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (_) {}
  }
  function restore() {
    var store = loadStore();
    var keys = Object.keys(store);
    if (!keys.length) return;
    allEditables().forEach(function (el) {
      var k = stableKey(el);
      if (Object.prototype.hasOwnProperty.call(store, k)) el.innerHTML = sanitizeHTML(store[k]);
    });
  }

  /* ---------- 激活 / 退出 ---------- */
  function activate() {
    if (isActive) return;
    isActive = true;
    allEditables().forEach(function (el) {
      el.setAttribute('contenteditable', 'true');
      el.classList.add('ie-editing');
    });
    if (toggle) toggle.classList.add('active');
    if (!hintShown) { hintShown = true; showHint(); }
  }
  function deactivate() {
    if (!isActive) return;
    isActive = false;
    allEditables().forEach(function (el) {
      el.removeAttribute('contenteditable');
      el.classList.remove('ie-editing');
    });
    if (toggle) toggle.classList.remove('active');
  }
  function toggleMode() { if (isActive) deactivate(); else activate(); }

  function showHint() {
    var h = document.createElement('div');
    h.className = 'ie-hint';
    h.textContent = '编辑模式：点文字直接改 · 输入即自动保存 · Ctrl+S 导出 HTML · 再按 E 退出';
    document.body.appendChild(h);
    setTimeout(function () { h.classList.add('ie-hint-out'); }, 2600);
    setTimeout(function () { h.remove(); }, 3200);
  }

  /* ---------- 导出完整 HTML（§305） ---------- */
  function exportHTML() {
    var wasActive = isActive;
    if (wasActive) deactivate();                       // 先移除编辑态 outline 与 contenteditable
    var clone = document.documentElement.cloneNode(true);
    // 剥离编辑器 chrome 与残留编辑态属性
    clone.querySelectorAll('.ie-hotzone,.ie-toggle,.ie-hint,[contenteditable]').forEach(function (n) {
      if (n.classList && (n.classList.contains('ie-hotzone') || n.classList.contains('ie-toggle') || n.classList.contains('ie-hint'))) { n.remove(); return; }
      n.removeAttribute('contenteditable');
    });
    clone.querySelectorAll('.ie-editing').forEach(function (n) { n.classList.remove('ie-editing'); });
    var html = '<!doctype html>\n' + clone.outerHTML;
    var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = deckKey();
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    if (wasActive) activate();
  }

  /* ---------- 热区 + 按钮（JS 接管 hover 链，§283） ---------- */
  function buildHotzone() {
    hotzone = document.createElement('div');
    hotzone.className = 'ie-hotzone';
    hotzone.style.cssText = 'position:fixed;top:0;left:0;width:' + HOTZONE_SIZE + 'px;height:' + HOTZONE_SIZE + 'px;z-index:9990;pointer-events:auto';
    toggle = document.createElement('button');
    toggle.className = 'ie-toggle';
    toggle.type = 'button';
    toggle.title = '内联文本编辑（E）';
    toggle.textContent = '编辑';
    hotzone.appendChild(toggle);
    document.body.appendChild(hotzone);

    var show = function () { clearTimeout(hideTimeout); toggle.classList.add('show'); };
    var scheduleHide = function () {
      hideTimeout = setTimeout(function () {
        if (!isActive) toggle.classList.remove('show');
      }, HOVER_GRACE);   // 400ms 宽限：留出鼠标从热区移到按钮的时间
    };
    hotzone.addEventListener('mouseenter', show);
    hotzone.addEventListener('mouseleave', scheduleHide);
    toggle.addEventListener('mouseenter', show);
    toggle.addEventListener('mouseleave', scheduleHide);
    // 点击热区直接切换；点击按钮也切换（按钮在热区内，阻止冒泡避免双触发）
    hotzone.addEventListener('click', function (e) { if (e.target === hotzone) toggleMode(); });
    toggle.addEventListener('click', function (e) { e.stopPropagation(); toggleMode(); });
  }

  /* ---------- 样式 ---------- */
  function injectStyle() {
    styleEl = document.createElement('style');
    styleEl.textContent =
      '.ie-toggle{position:absolute;top:14px;left:14px;width:52px;height:52px;border-radius:12px;' +
        'border:1px solid var(--outline-color,#d2d2d7);background:var(--surface,#fff);color:var(--text-primary,#1d1d1f);' +
        'font:600 13px/1 system-ui,-apple-system,"PingFang SC",sans-serif;cursor:pointer;' +
        'opacity:0;pointer-events:none;transition:opacity 180ms,background 180ms;box-shadow:0 2px 10px rgba(0,0,0,.12)}' +
      '.ie-toggle.show,.ie-toggle.active{opacity:1;pointer-events:auto}' +
      '.ie-toggle.active{background:var(--primary-color,#0a84ff);color:#fff;border-color:var(--primary-color,#0a84ff)}' +
      '.ie-toggle:hover{background:var(--surface-muted,#f5f5f7)}' +
      '.ie-toggle.active:hover{background:var(--primary-color,#0a84ff)}' +
      '[contenteditable].ie-editing{outline:1px dashed var(--primary-color,#0a84ff);outline-offset:2px;' +
        'cursor:text;border-radius:2px}' +
      '[contenteditable].ie-editing:focus{outline:2px solid var(--primary-color,#0a84ff);background:rgba(10,132,255,.06)}' +
      '.ie-hint{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);z-index:9991;' +
        'background:rgba(20,20,22,.92);color:#f5f5f4;padding:10px 18px;border-radius:10px;' +
        'font:13px/1.5 system-ui,-apple-system,"PingFang SC",sans-serif;transition:opacity 400ms}' +
      '.ie-hint-out{opacity:0}';
    document.head.appendChild(styleEl);
  }

  /* ---------- 全局键：E 切换 / Ctrl+S 导出（输入态守卫，§277） ---------- */
  function onKeydown(e) {
    var t = e.target;
    var inField = t && t.closest && t.closest('input,textarea,select,[contenteditable]');
    // Ctrl+S / Cmd+S 导出（即使焦点在可编辑元素内也允许）
    if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
      e.preventDefault(); exportHTML(); return;
    }
    if (inField) return;                       // contenteditable / 输入框内不触发 E
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === 'e' || e.key === 'E') { e.preventDefault(); toggleMode(); }
  }

  /* ---------- 输入即自动存（委托，§304） ---------- */
  function onInput(e) {
    var el = e.target;
    if (!el || !el.getAttribute || el.getAttribute('contenteditable') !== 'true') return;
    if (!isCandidate(el)) return;
    saveEntry(stableKey(el), el.innerHTML);
  }

  /* ---------- 安装 ---------- */
  function init() {
    if (document.getElementById('ie-style-installed')) return;
    injectStyle();
    buildHotzone();
    restore();                                   // 刷新恢复（§306）
    document.addEventListener('keydown', onKeydown);
    document.addEventListener('input', onInput);
    var marker = document.createElement('meta');
    marker.id = 'ie-style-installed';
    document.head.appendChild(marker);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  return {
    init: init,
    toggle: toggleMode,
    activate: activate,
    deactivate: deactivate,
    exportHTML: exportHTML,
    isActive: function () { return isActive; },
    // 供 hover 链规格引用（§290 editor.isActive）
    editor: { get isActive() { return isActive; } }
  };
})();
