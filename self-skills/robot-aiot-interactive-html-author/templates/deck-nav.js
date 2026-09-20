/* ============================================================================
 * deck-nav.js — 翻页导航核心：fragment 分步揭示 / 分支序列与导航栈 / 内容热点
 *                / #/N/M 深链 / 触摸滑动
 *
 * 来源：references/interactive-mode-rules.md「页内分步揭示（fragment）」「分支
 *       序列与导航栈」「内容热点」「触摸与深链」（乙类：按行为规格实现）
 * 用途：接管 deck 翻页状态机——活跃页按 Next 先推进 fragment 索引，最后一组
 *       揭示完才真正翻页，Prev 反向回收；附录页/深入页不进主线，由热点进入、
 *       原路返回；深链 #/N/M 加载直达停留点
 * 接线：复制进交付物 <script>，DOMContentLoaded 后自动 init（或手动
 *       DeckNav.init()）。与 templates/deck-skeleton.html 合用时删除骨架
 *       script 内的键盘绑定与 goTo/next/prev 段（避免双绑），保留 fit/打印底盘；
 *       本模块接管后 window.deckNav 即 presenter-window.js / 总览网格的导航真源。
 *       页面结构约定：<section class="slide" data-index="N" data-title="…">，
 *       分支页加 data-sequence="序列名"；页内分组标 data-fragment="1|2|3…"
 *       （未标注内容属 fragment 0，进页即可见）；热点
 *       <button class="hotspot" data-target="序列名" data-label="这个数怎么算的"
 *        data-region="left,top,width,height">（region 为 0-100 百分比包围盒，
 *       省略时渲染为页底带标签按钮）。
 *       前进事件消费顺序（pipeline 页）：先问 EntryRecipes.consumeForward()，
 *       false 再走 DeckNav.next()——本模块 next() 已内置该询问。
 * 深链约定：N = section 的 DOM 全局序号（data-index+1，含分支页），M = fragment；
 *       翻页 history.replaceState 写 hash，不污染回退栈
 * 可调参数：fragment 过渡 400ms cubic-bezier(0.4,0,0.2,1)（CSS 段）；入场
 *       stagger 150ms（100-200ms 区间）；触摸阈值 50px
 * 键位：→/Space/PageDown 下一页 · ←/PageUp 上一页 · Home/End 当前序列首/末页
 *       · Esc（分支内且无浮层）= back() 弹栈回精确父页 · B = 清栈回主线；
 *       input/textarea/select/contenteditable 内一律不响应（Esc 仅 blur）
 * ============================================================================ */

window.DeckNav = (function () {
  'use strict';

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ENTER_STAGGER = 150;

  var slides = [];          // 全部 section，DOM 序
  var mainline = [];        // 无 data-sequence 的主线页
  var sequences = {};       // { 序列名: [slides] }
  var stack = [];           // 导航栈 [{sequenceId, parentPos, parentFrag}]
  var ctx = { seq: null, pos: 0, frag: 0 };
  var suppressClickUntil = 0;
  var inited = false;

  /* ---------- 注入样式：fragment 揭示 / 面包屑 / 热点 ---------- */
  var STYLE = document.createElement('style');
  STYLE.textContent =
    '.js [data-fragment]{opacity:0;transform:translateY(12px);' +
      'transition:opacity 400ms cubic-bezier(0.4,0,0.2,1),transform 400ms cubic-bezier(0.4,0,0.2,1)}' +
    '.js [data-fragment].revealed{opacity:1;transform:none}' +
    '.js [data-fragment].dn-noanim{transition:none}' +
    '.dn-breadcrumb{position:absolute;top:16px;left:50%;transform:translateX(-50%);z-index:70;' +
      'font:14px/1.4 system-ui,-apple-system,"PingFang SC",sans-serif;color:var(--text-secondary,#545458);' +
      'background:var(--surface-muted,#f5f5f4);border:1px solid var(--outline-color,#e7e5e4);' +
      'border-radius:9999px;padding:4px 14px;pointer-events:none}' +
    '.dn-breadcrumb[hidden]{display:none}' +
    '.hotspot{position:absolute;z-index:20;min-width:44px;min-height:44px;cursor:pointer;' +
      'background:transparent;border:1px solid var(--outline-color,#999);border-radius:8px;' +
      'color:var(--text-secondary,#545458);font:13px/1.2 system-ui,-apple-system,"PingFang SC",sans-serif;' +
      'padding:6px 10px;opacity:.55;transition:opacity 200ms}' +
    '.hotspot:hover,.hotspot:focus-visible{opacity:1}' +
    '.hotspot:focus-visible{outline:2px solid var(--primary-color,#2563eb);outline-offset:2px}' +
    '.hotspot .dn-label{display:none;white-space:nowrap}' +
    '.hotspot:hover .dn-label,.hotspot:focus-visible .dn-label{display:inline}' +
    '.slide:not(.active) .hotspot{pointer-events:none}';   /* 仅活跃页可点 */
  document.head.appendChild(STYLE);

  /* ---------- 工具 ---------- */
  function gi(slide) { return slides.indexOf(slide); }
  function list() { return ctx.seq ? sequences[ctx.seq] : mainline; }
  function cur() { return list()[ctx.pos] || list()[0]; }
  function maxFrag(slide) {
    var m = 0;
    slide.querySelectorAll('[data-fragment]').forEach(function (el) {
      var k = parseInt(el.dataset.fragment, 10);
      if (isFinite(k) && k > m) m = k;
    });
    return m;
  }
  function seqOf(slide) { return slide.dataset.sequence || null; }

  /* ---------- fragment 呈现（离散停留点：直接呈现完整终态，可加入场动画） ---------- */
  function applyFragments(slide, frag, animate) {
    slide.querySelectorAll('[data-fragment]').forEach(function (el) {
      var k = parseInt(el.dataset.fragment, 10) || 0;
      var on = k <= frag;
      if (!animate) el.classList.add('dn-noanim');
      el.classList.toggle('revealed', on);
      if (!animate) {
        void el.offsetWidth;                              // 强制回流后移除，深链直达即终态
        requestAnimationFrame(function () { el.classList.remove('dn-noanim'); });
      }
    });
  }

  /* ---------- 入场编排（data-enter-order，setTimeout 不用 rAF） ---------- */
  function playEnter(slide) {
    (slide.__dnTimers || []).forEach(clearTimeout);
    slide.__dnTimers = [];
    var els = Array.prototype.slice.call(slide.querySelectorAll('.enter'))
      .sort(function (a, b) { return (+a.dataset.enterOrder || 0) - (+b.dataset.enterOrder || 0); });
    if (REDUCED) { els.forEach(function (el) { el.classList.add('entered'); }); return; }
    els.forEach(function (el, i) {
      slide.__dnTimers.push(setTimeout(function () { el.classList.add('entered'); }, ENTER_STAGGER * i));
    });
  }
  function clearEnter(slide) {
    (slide.__dnTimers || []).forEach(clearTimeout);
    slide.__dnTimers = [];
    slide.querySelectorAll('.enter').forEach(function (el) { el.classList.remove('entered'); });
  }

  /* ---------- chrome：页码（含 fragment 进度）与面包屑 ---------- */
  var crumb = null;
  function ensureCrumb() {
    if (crumb) return crumb;
    crumb = document.createElement('div');
    crumb.className = 'dn-breadcrumb';
    crumb.setAttribute('hidden', '');
    var host = document.querySelector('.canvas') || document.body;
    host.appendChild(crumb);
    return crumb;
  }
  function updateChrome() {
    var L = list(), slide = cur();
    var mf = maxFrag(slide);
    var pagePart = ctx.seq
      ? (ctx.pos + 1) + ' / ' + L.length                  // 分支内页码 scoped 到序列
      : (ctx.pos + 1) + ' / ' + L.length;
    var txt = pagePart + (mf > 0 ? ' · 步 ' + ctx.frag + '/' + mf : '');
    var num = document.getElementById('pageNum');
    if (num) num.textContent = txt;
    var fill = document.getElementById('progressFill');
    if (fill && !ctx.seq) fill.style.width = (L.length > 1 ? ctx.pos / (L.length - 1) * 100 : 100) + '%';
    var c = ensureCrumb();
    if (ctx.seq) {                                        // 面包屑从栈渲染：主线 › 序列名 › 第 N 页
      c.textContent = '主线 › ' + ctx.seq + ' › 第 ' + (ctx.pos + 1) + ' 页';
      c.removeAttribute('hidden');
    } else {
      c.setAttribute('hidden', '');
    }
  }

  /* ---------- 深链 ---------- */
  function writeHash() {
    var h = '#/' + (gi(cur()) + 1) + (ctx.frag > 0 ? '/' + ctx.frag : '');
    try { history.replaceState(null, '', h); } catch (e) { /* file:// 下容忍失败 */ }
  }
  function parseHash() {
    var m = /^#\/(\d+)(?:\/(\d+))?$/.exec(location.hash || '');
    if (!m) return null;
    var idx = parseInt(m[1], 10) - 1;
    if (idx < 0 || idx >= slides.length) return null;
    return { slide: slides[idx], frag: m[2] ? parseInt(m[2], 10) : 0 };
  }

  /* ---------- 状态落盘 ---------- */
  function applyState(reason, animateFrag) {
    var slide = cur();
    slides.forEach(function (s) {
      if (s === slide) {
        if (!s.classList.contains('active')) { s.classList.add('active'); playEnter(s); }
      } else if (s.classList.contains('active')) {
        s.classList.remove('active');
        clearEnter(s);
      }
    });
    applyFragments(slide, ctx.frag, animateFrag && !REDUCED);
    updateChrome();
    writeHash();
    document.dispatchEvent(new CustomEvent('slidechange', {
      detail: { index: gi(slide), frag: ctx.frag, seq: ctx.seq, reason: reason }
    }));
  }

  /* ---------- 导航动作 ---------- */
  function next(reason) {
    if (window.EntryRecipes && EntryRecipes.consumeForward()) return;   // pipeline 未点亮完不放行
    var slide = cur();
    if (ctx.frag < maxFrag(slide)) { ctx.frag++; applyState(reason || 'key', true); return; }
    if (ctx.pos < list().length - 1) { ctx.pos++; ctx.frag = 0; applyState(reason || 'key', true); }
    // 序列末页/主线末页：停住不循环
  }
  function prev(reason) {
    if (ctx.frag > 0) { ctx.frag--; applyState(reason || 'key', true); return; }
    if (ctx.pos > 0) {
      ctx.pos--;
      ctx.frag = maxFrag(cur());                          // 回上一页呈全揭示终态，再 Prev 逐组回收
      applyState(reason || 'key', true);
    }
  }
  function goToMain(pos, frag, reason) {
    ctx.seq = null;
    ctx.pos = Math.max(0, Math.min(mainline.length - 1, pos));
    ctx.frag = Math.max(0, Math.min(maxFrag(cur()), frag || 0));
    applyState(reason || 'click', false);
  }
  function goToGlobal(idx, frag, reason) {                // 总览网格/深链直达任意页
    var slide = slides[idx];
    if (!slide) return;
    var seq = seqOf(slide);
    if (seq) {
      ctx.seq = seq;
      ctx.pos = sequences[seq].indexOf(slide);
    } else {
      ctx.seq = null;
      ctx.pos = mainline.indexOf(slide);
    }
    ctx.frag = Math.max(0, Math.min(maxFrag(slide), frag || 0));
    applyState(reason || 'hash', false);
  }
  function enterBranch(seqName, reason) {                 // 热点进入：push 栈 + 分支首页
    if (!sequences[seqName]) return;
    stack.push({ sequenceId: seqName, parentPos: ctx.seq ? 0 : ctx.pos, parentFrag: ctx.frag });
    ctx.seq = seqName; ctx.pos = 0; ctx.frag = 0;
    applyState(reason || 'click', false);
  }
  function back() {                                       // Esc：弹栈回到持有热点的精确父页
    if (!ctx.seq || !stack.length) return false;
    var e = stack.pop();
    ctx.seq = null; ctx.pos = e.parentPos; ctx.frag = e.parentFrag;
    applyState('key', false);
    return true;
  }
  function clearStack() {                                 // B：清栈回主线
    if (!stack.length && !ctx.seq) return;
    var bottom = stack[0];
    stack = [];
    ctx.seq = null;
    ctx.pos = bottom ? bottom.parentPos : 0;
    ctx.frag = bottom ? bottom.parentFrag : 0;
    applyState('key', false);
  }

  /* ---------- 演讲者窗口 NEXT 预览用：下一停留点 ---------- */
  function peekNext() {
    var slide = cur();
    if (ctx.frag < maxFrag(slide)) return { index: gi(slide), frag: ctx.frag + 1 };
    var L = list();
    if (ctx.pos < L.length - 1) return { index: gi(L[ctx.pos + 1]), frag: 0 };
    return null;
  }

  /* ---------- 总览网格分组数据（O 键实现方消费） ---------- */
  function getGroups() {
    var groups = [{ name: '主线', slides: mainline.slice() }];
    Object.keys(sequences).forEach(function (name) {
      groups.push({ name: name, slides: sequences[name].slice() });   // 组头 = 序列名
    });
    return groups;
  }

  /* ---------- 热点接线 ---------- */
  function wireHotspots() {
    document.querySelectorAll('.hotspot[data-target]').forEach(function (btn) {
      var label = btn.dataset.label || btn.dataset.target;
      if (!btn.querySelector('.dn-label')) {
        var sp = document.createElement('span');
        sp.className = 'dn-label';
        sp.textContent = label;
        btn.appendChild(sp);
      }
      if (!btn.textContent.trim()) btn.setAttribute('aria-label', label);
      var region = (btn.dataset.region || '').split(',').map(function (v) { return parseFloat(v); });
      if (region.length === 4 && region.every(isFinite)) {
        // 百分比包围盒定位在触发它的内容上
        btn.style.left = region[0] + '%';
        btn.style.top = region[1] + '%';
        btn.style.width = region[2] + '%';
        btn.style.height = region[3] + '%';
      } else {
        // 省略 region：渲染为页底带标签按钮，不做无形整页热区
        var slide = btn.closest('.slide');
        if (slide && btn.parentElement !== slide) {
          btn.style.position = 'absolute';
          btn.style.left = '48px';
          btn.style.bottom = '48px';
          btn.style.width = 'auto';
          btn.style.height = 'auto';
          slide.appendChild(btn);
        }
        btn.style.position = btn.style.position || 'absolute';
        var s2 = btn.closest('.slide');
        if (s2 && !btn.style.left) { btn.style.left = '48px'; btn.style.bottom = '48px'; }
        btn.querySelector('.dn-label').style.display = 'inline';
      }
      btn.addEventListener('click', function (e) {
        e.stopPropagation();                              // 不冒泡到左右半屏翻页热区
        var slide = btn.closest('.slide');
        if (!slide || !slide.classList.contains('active')) return;
        enterBranch(btn.dataset.target, 'click');
      });
    });
  }

  /* ---------- 键盘 ---------- */
  function onKeydown(e) {
    if (e.target.closest && e.target.closest('input,textarea,select,[contenteditable]')) {
      if (e.key === 'Escape') e.target.blur();
      return;                                             // 输入态守卫
    }
    switch (e.key) {
      case 'ArrowRight': case ' ': case 'PageDown': e.preventDefault(); next('key'); break;
      case 'ArrowLeft': case 'PageUp': e.preventDefault(); prev('key'); break;
      case 'Home': e.preventDefault(); ctx.pos = 0; ctx.frag = 0; applyState('key', false); break;
      case 'End': e.preventDefault(); ctx.pos = list().length - 1; ctx.frag = maxFrag(cur()); applyState('key', false); break;
      case 'b': case 'B': clearStack(); break;
      case 'Escape': {
        var overlay = document.querySelector('[data-nav-overlay].open');
        if (overlay) {                                    // 有浮层先关浮层，不弹栈
          document.dispatchEvent(new CustomEvent('decknav:close-overlays'));
        } else if (ctx.seq) {
          back();                                         // 分支内且无浮层 = back()
        } else if (document.fullscreenElement && document.exitFullscreen) {
          document.exitFullscreen();
        }
        break;
      }
    }
  }

  /* ---------- 触摸滑动翻页（与点击热区互斥；[data-interactive] 不劫持） ---------- */
  var touchStart = null;
  function onTouchStart(e) {
    if (e.target.closest && e.target.closest('[data-interactive]')) { touchStart = null; return; }
    var t = e.changedTouches[0];
    touchStart = { x: t.clientX, y: t.clientY };
  }
  function onTouchEnd(e) {
    if (!touchStart) return;
    var t = e.changedTouches[0];
    var dx = t.clientX - touchStart.x, dy = t.clientY - touchStart.y;
    touchStart = null;
    if (Math.abs(dx) >= 50 && Math.abs(dx) > Math.abs(dy)) {
      suppressClickUntil = Date.now() + 400;              // 触摸翻页不触发点击热区（防双翻）
      if (dx < 0) next('click'); else prev('click');      // 左滑下一页、右滑上一页
    }
  }
  function onClickCapture(e) {
    if (Date.now() < suppressClickUntil) { e.stopPropagation(); e.preventDefault(); }
  }

  /* ---------- 初始化 ---------- */
  function init() {
    if (inited) return api;
    inited = true;
    slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    slides.forEach(function (s, i) {
      if (!s.dataset.index) s.dataset.index = String(i);
    });
    mainline = slides.filter(function (s) { return !s.dataset.sequence; });
    sequences = {};
    slides.forEach(function (s) {
      var seq = s.dataset.sequence;
      if (seq) (sequences[seq] = sequences[seq] || []).push(s);
    });

    wireHotspots();

    var h = parseHash();                                  // 加载时解析 hash 直达对应页与停留点
    if (h) {
      var seq = seqOf(h.slide);
      if (seq) { ctx.seq = seq; ctx.pos = sequences[seq].indexOf(h.slide); }
      else { ctx.seq = null; ctx.pos = mainline.indexOf(h.slide); }
      ctx.frag = Math.max(0, Math.min(maxFrag(h.slide), h.frag));
      slides.forEach(function (s) { s.classList.remove('active'); });
    } else {
      var act = slides.findIndex(function (s) { return s.classList.contains('active'); });
      var slide = slides[act >= 0 ? act : 0];
      if (slide) {
        var sq = seqOf(slide);
        ctx.seq = sq;
        ctx.pos = sq ? sequences[sq].indexOf(slide) : mainline.indexOf(slide);
        ctx.frag = 0;
      }
    }
    applyState('hash', false);

    document.addEventListener('keydown', onKeydown);
    document.addEventListener('touchstart', onTouchStart, { passive: true });
    document.addEventListener('touchend', onTouchEnd, { passive: true });
    document.addEventListener('click', onClickCapture, true);
    addEventListener('hashchange', function () {
      var hh = parseHash();
      if (hh && hh.slide !== cur()) goToGlobal(gi(hh.slide), hh.frag, 'hash');
    });
    return api;
  }

  var api = {
    init: init,
    next: next, prev: prev, back: back, clearStack: clearStack,
    goToMain: goToMain, goToGlobal: goToGlobal, enterBranch: enterBranch,
    peekNext: peekNext, getGroups: getGroups,
    current: function () { return cur(); },
    currentIndex: function () { return gi(cur()); },
    currentFrag: function () { return ctx.frag; },
    maxFrag: function (s) { return maxFrag(s || cur()); },
    inBranch: function () { return !!ctx.seq; },
    stackDepth: function () { return stack.length; },
    slides: function () { return slides.slice(); },
    total: function () { return slides.length; },
    ownsTouch: true
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  return api;
})();
