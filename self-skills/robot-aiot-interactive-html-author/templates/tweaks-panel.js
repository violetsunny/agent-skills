/* ============================================================================
 * tweaks-panel.js — 评审期实时调参面板（?tweaks=1 注入，零依赖 IIFE）
 *
 * 来源：references/multi-version-selection.md §八（逐字提取：deck 侧接线 CSS +
 *       twDur 用法示例 + 面板完整实现 IIFE）
 * 用途：评审与 Pass 2-4 期间挂实时调参面板（字号/间距/色相/动效四旋钮），
 *       不改代码探索参数空间；面板是工具不是交付物——?tweaks=1 才注入，
 *       不带参数时零 DOM、零样式痕迹；落定即固化（参数写回 :root token）
 * 接线：两步——
 *       1) TW_WIRING_CSS 必须写进页面 CSS（token 声明 + calc() 接线），
 *          WAAPI 动画时长用 window.twDur(ms) 取，不写字面量（用法见下方示例）；
 *          未接线的动画不受动效旋钮影响；翻页过渡/入场/数字滚动/ambient 四类必须接线
 *       2) 面板 IIFE 置于 </body> 前
 * 可调参数：DEFAULTS / RANGE / LABEL / HUE_TOKENS / CONTROLS（IIFE 顶部）；
 *           URL 键位 fs(1-1.2) gap(0.85-1.3) hue(±40°) mo(0.5-1.6)；
 *           优先级 URL > localStorage > 默认值；多项目共存改 STORE_KEY
 * 纪律：面板挂 body 直属、.fit-viewport 之外；截图矩阵/headless 断言/打印
 *       导出一律不带 ?tweaks=1；@media print 面板隐藏；reduced-motion 时
 *       动效旋钮锁定 off；色相偏移仅对 3/6 位 hex token 生效（oklch 自动跳过）
 * ============================================================================ */

/* ---------- deck 侧接线 CSS（必须写进页面 CSS） ---------- */

const TW_WIRING_CSS = `
:root {
  --tw-font-scale: 1;
  --tw-gap-scale: 1;
  --tw-motion: 1;
}
.slide h1        { font-size: calc(99px * var(--tw-font-scale)); }
.slide .lead     { font-size: calc(20px * var(--tw-font-scale)); }
.slide .body     { font-size: calc(18px * var(--tw-font-scale)); }
.slide .caption  { font-size: calc(16px * var(--tw-font-scale)); }
.card-grid       { gap: calc(24px * var(--tw-gap-scale)); }
.block           { padding: calc(32px * var(--tw-gap-scale)); }
.slide .enter {
  transition:
    opacity calc(500ms * var(--tw-motion)) cubic-bezier(0.4, 0, 0.2, 1),
    transform calc(500ms * var(--tw-motion)) cubic-bezier(0.4, 0, 0.2, 1);
}
`;

/* ---------- WAAPI 动画接线用法示例（md 原文，复制进动画代码处） ----------
el.animate(
  [{ opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'translateY(0)' }],
  { duration: twDur(600), easing: 'cubic-bezier(0.165, 0.84, 0.44, 1)', fill: 'both' }
);
-------------------------------------------------------------------------- */

/* ---------- 面板完整实现（原生 JS + CSS，零依赖，置于 </body> 前） ---------- */

(function () {
  'use strict';

  var QS = new URLSearchParams(location.search);
  if (QS.get('tweaks') !== '1') return;

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var STORE_KEY = 'deck-tweaks';
  var DEFAULTS = { fs: 1, gap: 1, hue: 0, mo: 1 };
  var RANGE = {
    fs:  { min: 1,    max: 1.2,  step: 0.01 },
    gap: { min: 0.85, max: 1.3,  step: 0.01 },
    hue: { min: -40,  max: 40,   step: 1 },
    mo:  { min: 0.5,  max: 1.6,  step: 0.05 }
  };
  var LABEL = { fs: '字号倍率', gap: '间距倍率', hue: '色相偏移', mo: '动效时长' };
  var HUE_TOKENS = ['--primary-color', '--secondary-color', '--tertiary-color'];
  var CONTROLS = [
    { key: 'fs',  fmt: function (v) { return v.toFixed(2) + 'x'; } },
    { key: 'gap', fmt: function (v) { return v.toFixed(2) + 'x'; } },
    { key: 'hue', fmt: function (v) { return (v > 0 ? '+' : '') + v + '\u00B0'; } },
    { key: 'mo',  fmt: function (v) { return v === 0 ? 'off' : v.toFixed(2) + 'x'; } }
  ];

  function clamp(k, v) {
    v = Number(v);
    if (!isFinite(v)) return DEFAULTS[k];
    return Math.min(RANGE[k].max, Math.max(RANGE[k].min, v));
  }

  function readState() {
    var stored = null;
    try { stored = JSON.parse(localStorage.getItem(STORE_KEY) || 'null'); } catch (e) { stored = null; }
    var s = {};
    Object.keys(DEFAULTS).forEach(function (k) {
      if (QS.has(k)) s[k] = clamp(k, QS.get(k));
      else if (stored && stored[k] != null) s[k] = clamp(k, stored[k]);
      else s[k] = DEFAULTS[k];
    });
    if (REDUCED) s.mo = 0;
    return s;
  }

  var state = readState();

  function parseHex(v) {
    var m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(String(v).trim());
    if (!m) return null;
    var h = m[1];
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    var n = parseInt(h, 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
  }

  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var d = max - min, l = (max + min) / 2, h = 0, s = 0;
    if (d !== 0) {
      s = d / (1 - Math.abs(2 * l - 1));
      if (max === r) h = ((g - b) / d) % 6;
      else if (max === g) h = (b - r) / d + 2;
      else h = (r - g) / d + 4;
      h *= 60;
      if (h < 0) h += 360;
    }
    return { h: h, s: s, l: l };
  }

  function hslToHex(h, s, l) {
    h = ((h % 360) + 360) % 360;
    var c = (1 - Math.abs(2 * l - 1)) * s;
    var x = c * (1 - Math.abs((h / 60) % 2 - 1));
    var m = l - c / 2;
    var seg = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x]
            : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
    var to = function (v) {
      var t = Math.round((v + m) * 255).toString(16);
      return t.length === 1 ? '0' + t : t;
    };
    return '#' + to(seg[0]) + to(seg[1]) + to(seg[2]);
  }

  var baseHsl = {};
  var cs = getComputedStyle(document.documentElement);
  HUE_TOKENS.forEach(function (k) {
    var rgb = parseHex(cs.getPropertyValue(k));
    if (rgb) baseHsl[k] = rgbToHsl(rgb.r, rgb.g, rgb.b);
  });

  function currentUrl() {
    var p = new URLSearchParams(location.search);
    p.set('tweaks', '1');
    Object.keys(state).forEach(function (k) {
      if (state[k] === DEFAULTS[k]) p.delete(k); else p.set(k, String(state[k]));
    });
    return location.pathname + '?' + p.toString() + location.hash;
  }

  function persist() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* 无痕模式不可用：URL 仍是唯一真源 */ }
    try { history.replaceState(null, '', currentUrl()); }
    catch (e) { console.warn('[tweaks] replaceState 不可用，请从地址栏手动复制参数：' + e.message); }
    var link = document.getElementById('tw-link');
    if (link) link.href = currentUrl();
  }

  function apply() {
    var rs = document.documentElement.style;
    rs.setProperty('--tw-font-scale', state.fs.toFixed(2));
    rs.setProperty('--tw-gap-scale', state.gap.toFixed(2));
    rs.setProperty('--tw-motion', state.mo.toFixed(2));
    Object.keys(baseHsl).forEach(function (k) {
      var b = baseHsl[k];
      rs.setProperty(k, hslToHex(b.h + state.hue, b.s, b.l));
    });
    CONTROLS.forEach(function (c) {
      var input = document.getElementById('tw-' + c.key);
      var out = document.getElementById('tw-' + c.key + '-o');
      if (input && Number(input.value) !== state[c.key]) input.value = String(state[c.key]);
      if (out) out.textContent = c.fmt(state[c.key]);
    });
    persist();
  }

  var CSS_TEXT = [
    '#tw-panel{position:fixed;right:20px;bottom:20px;z-index:9999;',
    'font:13px/1.5 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;color:#1a1a1a}',
    '#tw-panel *{box-sizing:border-box}',
    '#tw-toggle{border:0;border-radius:9999px;background:#1a1a1a;color:#f5f3ef;padding:8px 16px;',
    'font:inherit;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.18)}',
    '#tw-toggle:focus-visible{outline:2px solid #1a1a1a;outline-offset:2px}',
    '#tw-body{margin-bottom:10px;padding:16px;width:288px;background:#fff;',
    'border:1px solid rgba(0,0,0,.12);border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.16)}',
    '.tw-row{display:grid;grid-template-columns:66px 1fr 54px;align-items:center;gap:8px;margin-bottom:12px}',
    '.tw-row label{color:#555}',
    '.tw-row output{text-align:right;font-variant-numeric:tabular-nums}',
    '.tw-row input[type=range]{width:100%;margin:0;accent-color:#1a1a1a}',
    '.tw-row input[type=range]:disabled{opacity:.4}',
    '.tw-foot{display:flex;gap:8px;align-items:center;margin-top:4px}',
    '.tw-foot button,.tw-foot a{flex:1;padding:6px 8px;border:1px solid rgba(0,0,0,.14);border-radius:8px;',
    'background:#f5f3ef;color:#1a1a1a;font:inherit;text-align:center;text-decoration:none;cursor:pointer}',
    '.tw-foot button:hover,.tw-foot a:hover{background:#eae7e0}',
    '.tw-hint{margin:10px 0 0;color:#666;font-size:12px}',
    '@media print{#tw-panel{display:none !important}}'
  ].join('\n');

  var rows = CONTROLS.map(function (c) {
    var r = RANGE[c.key];
    return '<div class="tw-row">' +
      '<label for="tw-' + c.key + '">' + LABEL[c.key] + '</label>' +
      '<input type="range" id="tw-' + c.key + '" min="' + r.min + '" max="' + r.max + '" step="' + r.step + '">' +
      '<output id="tw-' + c.key + '-o" for="tw-' + c.key + '"></output>' +
      '</div>';
  }).join('');

  var style = document.createElement('style');
  style.textContent = CSS_TEXT;
  document.head.appendChild(style);

  var panel = document.createElement('div');
  panel.id = 'tw-panel';
  panel.setAttribute('role', 'group');
  panel.setAttribute('aria-label', '设计调参面板');
  panel.innerHTML =
    '<div id="tw-body" hidden>' + rows +
      '<div class="tw-foot">' +
        '<button type="button" id="tw-reset">重置</button>' +
        '<button type="button" id="tw-copy">复制参数</button>' +
        '<a id="tw-link" href="#" target="_blank" rel="noopener">新窗口</a>' +
      '</div>' +
      '<p class="tw-hint" id="tw-hint"></p>' +
    '</div>' +
    '<button type="button" id="tw-toggle" aria-expanded="false" aria-controls="tw-body">调参</button>';
  document.body.appendChild(panel);

  var toggle = document.getElementById('tw-toggle');
  var body = document.getElementById('tw-body');
  var hint = document.getElementById('tw-hint');

  toggle.addEventListener('click', function () {
    var willOpen = body.hasAttribute('hidden');
    if (willOpen) body.removeAttribute('hidden'); else body.setAttribute('hidden', '');
    toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    toggle.textContent = willOpen ? '收起调参' : '调参';
  });

  CONTROLS.forEach(function (c) {
    var input = document.getElementById('tw-' + c.key);
    input.value = String(state[c.key]);
    if (c.key === 'mo' && REDUCED) input.disabled = true;
    input.addEventListener('input', function () {
      state[c.key] = clamp(c.key, input.value);
      apply();
    });
  });

  document.getElementById('tw-reset').addEventListener('click', function () {
    state = { fs: DEFAULTS.fs, gap: DEFAULTS.gap, hue: DEFAULTS.hue, mo: REDUCED ? 0 : DEFAULTS.mo };
    apply();
    hint.textContent = '已回到默认值（默认值即成品态）';
  });

  document.getElementById('tw-copy').addEventListener('click', function () {
    var url = location.href;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(
        function () { hint.textContent = '已复制当前参数 URL'; },
        function () { hint.textContent = '复制被拒绝，请从地址栏手动复制'; }
      );
    } else {
      hint.textContent = '当前环境无 clipboard API，请从地址栏手动复制';
    }
  });

  window.twDur = function (ms) { return Math.round(ms * state.mo); };

  if (REDUCED) hint.textContent = 'reduced-motion 已生效：动效时长锁定为 off';
  else hint.textContent = '动效旋钮只作用于 calc(基准 * var(--tw-motion)) 与 twDur() 接线的动画';

  apply();
})();
