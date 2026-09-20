/* ============================================================================
 * presenter-window.js — 演讲者模式全套：S 键演讲者窗口 / 四张磁吸卡 / 像素级
 *   预览 iframe / 双窗口同步（BroadcastChannel + file:// 降级 postMessage）/
 *   可编辑备注 / SPEAKER_NOTES 结构化话术 / TIMER 计时与排练 / 自动翻页 /
 *   激光笔与圈选 / 观众屏黑白冻结 / 同步状态机与心跳 / 演前检查 / N 话术抽屉 /
 *   O 总览网格 / T 主题审阅 / #/N 深链联动
 *
 * 来源：references/presenter-mode.md §2.1、§3（3.1-3.6）、§4、§7、§9-§19
 *       （乙类：md 只有行为规格无完整代码，按规格实现完整可运行代码）
 * 用途：给交互 deck 内建演讲辅助。观众窗口（主 deck）按 S 弹出独立演讲者窗口；
 *       两窗口经同步通道双向跟随翻页；演讲者窗口提供 CURRENT/NEXT 像素级预览、
 *       SCRIPT 可编辑话术、TIMER 计时排练、状态灯、演前检查、激光笔/圈选、
 *       观众屏控制、自动翻页。
 * 接线：复制进交付物 <script>，与 templates/deck-nav.js（或 deck-skeleton.html
 *       内置导航）合用——本模块监听 document 的 'slidechange' 事件作为翻页真源，
 *       编程翻页优先用 window.DeckNav.goToGlobal，回退 window.deckSkeleton.goTo。
 *       DOMContentLoaded 后自动 install。页面结构约定：
 *         <section class="slide" data-index="N" data-title="…" data-slide-id="slug">
 *           …可见内容…
 *           <div class="notes">话术（display:none）</div>
 *         </section>
 *       结构化话术（可选）：window.__SPEAKER_NOTES__ = [{id,title,minutes,talk,…}]
 *       主题审阅（可选）：<body data-themes="基调A,基调B"> + window.__THEMES__={…}
 * 预览原理：CURRENT/NEXT 各是一个 <iframe>，加载同一 deck 文件带 ?preview=N；
 *       命中 ?preview 的实例只渲染第 N 页、隐藏全部 chrome、body 加 preview-mode；
 *       翻页时演讲者窗口 postMessage({type:'preview-goto',idx})，iframe 只切 .active。
 * 同步通道：http/https 用 BroadcastChannel('deck-sync-<文件名>')；file:// 降级
 *       window.opener.postMessage + message 监听（校验 event.source）。消息只携带
 *       页码与动作，不携带 DOM 状态。
 * 可调参数：DESIGN_W/H=1920×1080（预览设计画布）；HEARTBEAT_MS=2000；
 *       TIMEOUT_MS=6000（心跳超时判未连接）；卡片最小 120px；自动翻页默认间隔
 *       30s；激光淡出 600ms；布局/备注/排练 localStorage key 均含 deck 文件名。
 * 键位（观众窗口）：S 演讲者窗口 · N 话术抽屉 · O 总览网格 · T 主题审阅 ·
 *       F 全屏（deck 自带）。键位（演讲者窗口）：←/→ 翻页 · R 重置计时 ·
 *       Esc 关闭窗口 · L 激光笔 · C 圈选 · X 清除标注 · B 黑屏 · W 白屏 ·
 *       Shift+F 冻结 · A 自动翻页 · ? 快捷键说明。备注 textarea 内一律不触发。
 * 解读说明：§15.5 'bye'/'演示已结束' 遮罩由演讲者窗口「结束演示」按钮显式触发，
 *       仅按 Esc 关窗不发 bye（观众 deck 仍可继续手动操作），避免误判演示结束。
 * ============================================================================ */

window.PresenterMode = (function () {
  'use strict';

  /* ============================ 共享常量与工具 ============================ */
  var DESIGN_W = 1920, DESIGN_H = 1080;
  var HEARTBEAT_MS = 2000, TIMEOUT_MS = 6000;
  var MIN_CARD = 120;
  var NOTES_PREFIX = 'deck-notes::';
  var LASER_FADE_MS = 600;
  var DEFAULT_AUTO_INTERVAL = 30;

  function deckKey() {
    var p = (location.pathname.split('/').pop() || 'deck').split('?')[0];
    return p || 'deck';
  }
  function syncChannelName() { return 'deck-sync-' + deckKey(); }
  function layoutKey() { return 'deck-presenter-layout::' + deckKey(); }
  function rehearsalKey() { return 'deck-rehearsal::' + deckKey(); }
  function autoKey() { return 'deck-auto::' + deckKey(); }
  // §2.1 / §9.3 备注 key 契约：前缀 + JSON.stringify([deckKey, seqId||'', slideId||idx, sceneId||''])
  function notesKey(slideId, seqId, idx, sceneId) {
    return NOTES_PREFIX + JSON.stringify([deckKey(), seqId || '', slideId || ('idx:' + idx), sceneId || '']);
  }
  function safeParse(str, fallback) {
    if (str == null) return fallback;
    try { var v = JSON.parse(str); return v == null ? fallback : v; } catch (_) { return fallback; }
  }
  function clampNum(v, min, max, def) {
    v = Number(v);
    if (!isFinite(v)) return def;
    return Math.min(max, Math.max(min, v));
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* 导航适配：优先 DeckNav，回退 deckSkeleton，再回退裸 DOM */
  function nav() {
    if (window.DeckNav && DeckNav.goToGlobal) {
      return {
        idx: function () { return DeckNav.currentIndex(); },
        total: function () { return DeckNav.total(); },
        slides: function () { return DeckNav.slides(); },
        goTo: function (i) { DeckNav.goToGlobal(i, 0, 'presenter'); },
        kind: 'DeckNav'
      };
    }
    if (window.deckSkeleton && deckSkeleton.goTo) {
      return {
        idx: function () { return deckSkeleton.current(); },
        total: function () { return deckSkeleton.total(); },
        slides: function () { return deckSkeleton.slides; },
        goTo: function (i) { deckSkeleton.goTo(i, 'presenter'); },
        kind: 'deckSkeleton'
      };
    }
    var secs = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    return {
      idx: function () {
        for (var i = 0; i < secs.length; i++) if (secs[i].classList.contains('active')) return i;
        return 0;
      },
      total: function () { return secs.length; },
      slides: function () { return secs; },
      goTo: function (i) {
        i = Math.max(0, Math.min(secs.length - 1, i));
        secs.forEach(function (s, k) { s.classList.toggle('active', k === i); });
      },
      kind: 'bare'
    };
  }

  /* 同步通道工厂：http(s) 用 BroadcastChannel；file:// 降级 postMessage */
  function makeChannel(selfWin, getPeer, name, onMsg) {
    var useBC = false;
    try { useBC = selfWin.location.protocol !== 'file:' && 'BroadcastChannel' in selfWin; } catch (_) { useBC = false; }
    var bc = null;
    if (useBC) {
      bc = new selfWin.BroadcastChannel(name);
      bc.onmessage = function (e) { onMsg(e.data, 'broadcast'); };
    } else {
      selfWin.addEventListener('message', function (e) {
        var peer = getPeer ? getPeer() : null;
        // file:// 下 origin 均为 null，用 event.source 校验（§3.3 条4 / §18.1）
        if (peer && (e.source === peer || e.source === selfWin.opener)) onMsg(e.data, 'postmessage');
      });
    }
    return {
      post: function (msg) {
        if (bc) { try { bc.postMessage(msg); } catch (_) {} return; }
        var peer = getPeer ? getPeer() : null;
        if (peer) { try { peer.postMessage(msg, '*'); } catch (_) {} }
      },
      close: function () { if (bc) { try { bc.close(); } catch (_) {} bc = null; } },
      kind: useBC ? 'broadcast' : 'postmessage'
    };
  }

  var params = new URLSearchParams(location.search);
  var IS_PREVIEW = params.has('preview');
  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ============================ 预览模式（?preview=N） ============================ */
  // §3.2：只渲染第 N 页、隐藏全部 chrome、body 加 preview-mode；监听 preview-goto 切页不重载
  function initPreview() {
    var startIdx = parseInt(params.get('preview') || '0', 10) || 0;
    var seek = params.get('seek');
    var st = document.createElement('style');
    st.textContent =
      'body.preview-mode .dn-chrome,body.preview-mode .progress-bar,body.preview-mode .page-number,' +
      'body.preview-mode .nav-btn,body.preview-mode .hotspot,body.preview-mode .dn-breadcrumb,' +
      'body.preview-mode [data-pw-chrome]{display:none!important}' +
      'body.preview-mode *{animation:none!important;transition:none!important}';
    document.head.appendChild(st);
    function show(i) {
      var n = nav();
      n.goTo(i);
      // 裸 DOM 回退时手动切 active
      if (n.kind === 'bare') n.goTo(i);
    }
    function boot() {
      document.body.classList.add('preview-mode');
      show(startIdx);
      // §19.2：?preview=N&seek=M 由 deck 自身的 demoSeek 处理（ui-demo-choreography §9），此处不注入脚本
      if (seek != null) { try { window.dispatchEvent(new CustomEvent('demo-seek', { detail: { step: parseInt(seek, 10) || 0 } })); } catch (_) {} }
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
    window.addEventListener('message', function (e) {
      if (e.source !== window.parent) return;          // 只接受父（演讲者窗口）指令
      var d = e.data; if (!d || d.type !== 'preview-goto') return;
      show(d.idx | 0);
    });
  }

  if (IS_PREVIEW) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initPreview);
    else initPreview();
    return { role: 'preview' };
  }

  /* ============================ 观众窗口（主 deck） ============================ */
  var presenterWin = null;
  var audienceChannel = null;
  var applyingRemote = false;       // 应用远端 goto 时抑制回声
  var seqNum = 0;                   // 单调递增序列号（§15.1 / §15.3）
  var frozen = false;               // §14 观众屏冻结
  var frozenPendingIdx = null;      // 冻结期间缓存的最新页码，解冻追平
  var heartbeatTimer = null;
  var laserDot = null, annotateLayer = null, screenOverlay = null, endMask = null;
  var notesDrawer = null, overviewGrid = null;
  var themeIdx = 0;

  function nextSeq() { return ++seqNum; }

  /* ----- 覆盖层构建（激光点 / 圈选 SVG / 黑白屏 / 结束遮罩 / 话术抽屉 / 总览） ----- */
  function ensureOverlays() {
    if (!laserDot) {
      laserDot = document.createElement('div');
      laserDot.setAttribute('data-pw-chrome', '1');
      laserDot.style.cssText = 'position:fixed;z-index:9998;width:18px;height:18px;border-radius:50%;' +
        'background:radial-gradient(circle,#ff3b30 0%,rgba(255,59,48,.35) 60%,transparent 70%);' +
        'pointer-events:none;opacity:0;transition:opacity ' + LASER_FADE_MS + 'ms;transform:translate(-50%,-50%);left:0;top:0';
      document.body.appendChild(laserDot);
    }
    if (!annotateLayer) {
      annotateLayer = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      annotateLayer.setAttribute('data-pw-chrome', '1');
      annotateLayer.style.cssText = 'position:fixed;inset:0;z-index:9997;pointer-events:none;width:100%;height:100%';
      document.body.appendChild(annotateLayer);
    }
    if (!screenOverlay) {
      screenOverlay = document.createElement('div');
      screenOverlay.setAttribute('data-pw-chrome', '1');
      screenOverlay.style.cssText = 'position:fixed;inset:0;z-index:9999;display:none;pointer-events:none';
      document.body.appendChild(screenOverlay);
    }
    if (!endMask) {
      endMask = document.createElement('div');
      endMask.setAttribute('data-pw-chrome', '1');
      endMask.style.cssText = 'position:fixed;inset:0;z-index:10000;display:none;align-items:center;' +
        'justify-content:center;background:#0b0b0c;color:#f5f5f4;font:600 28px/1.4 system-ui,-apple-system,"PingFang SC",sans-serif';
      endMask.textContent = '演示已结束';
      document.body.appendChild(endMask);
    }
  }

  function showLaser(x, y, on) {
    ensureOverlays();
    if (!on) { laserDot.style.opacity = '0'; return; }
    laserDot.style.left = (x * innerWidth) + 'px';
    laserDot.style.top = (y * innerHeight) + 'px';
    laserDot.style.opacity = '1';
  }

  function drawAnnotation(points) {
    ensureOverlays();
    if (!points || points.length < 2) return;
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    var pts = points.map(function (p) { return (p[0] * innerWidth) + ',' + (p[1] * innerHeight); }).join(' ');
    path.setAttribute('points', pts);
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', '#ff3b30');
    path.setAttribute('stroke-width', '4');
    path.setAttribute('stroke-linecap', 'round');
    path.setAttribute('stroke-linejoin', 'round');
    annotateLayer.appendChild(path);
  }
  function clearAnnotations() { ensureOverlays(); while (annotateLayer.firstChild) annotateLayer.removeChild(annotateLayer.firstChild); }

  function applyScreen(mode) {
    ensureOverlays();
    if (mode === 'black') { screenOverlay.style.display = 'block'; screenOverlay.style.background = '#000'; }
    else if (mode === 'white') { screenOverlay.style.display = 'block'; screenOverlay.style.background = '#fff'; }
    else { screenOverlay.style.display = 'none'; screenOverlay.style.background = 'transparent'; }
  }

  /* ----- 话术抽屉（N 键，§3.4） ----- */
  function toggleNotesDrawer() {
    ensureOverlays();
    if (notesDrawer && notesDrawer.style.display === 'block') { notesDrawer.style.display = 'none'; return; }
    if (!notesDrawer) {
      notesDrawer = document.createElement('div');
      notesDrawer.setAttribute('data-pw-chrome', '1');
      notesDrawer.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:9996;max-height:38vh;overflow:auto;' +
        'background:rgba(20,20,22,.94);color:#f5f5f4;padding:18px 26px;font:16px/1.7 system-ui,-apple-system,"PingFang SC",sans-serif;' +
        'border-top:1px solid rgba(255,255,255,.15);display:none';
      document.body.appendChild(notesDrawer);
    }
    var n = nav();
    var sec = n.slides()[n.idx()];
    var notesEl = sec && sec.querySelector('.notes');
    notesDrawer.innerHTML = notesEl ? notesEl.innerHTML : '<em style="opacity:.6">本页无话术</em>';
    notesDrawer.style.display = 'block';
  }

  /* ----- 总览网格（O 键，§4） ----- */
  function toggleOverview() {
    ensureOverlays();
    if (overviewGrid) { overviewGrid.remove(); overviewGrid = null; return; }
    var n = nav();
    var secs = n.slides();
    var cur = n.idx();
    overviewGrid = document.createElement('div');
    overviewGrid.setAttribute('data-pw-chrome', '1');
    overviewGrid.style.cssText = 'position:fixed;inset:0;z-index:9995;background:rgba(12,12,14,.96);overflow:auto;' +
      'padding:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px;' +
      'align-content:start';
    secs.forEach(function (sec, i) {
      var cell = document.createElement('div');
      cell.style.cssText = 'cursor:pointer;border:2px solid ' + (i === cur ? '#0a84ff' : 'rgba(255,255,255,.18)') +
        ';border-radius:10px;overflow:hidden;background:#1c1c1e;transition:border-color 150ms';
      var wrap = document.createElement('div');
      wrap.style.cssText = 'position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;pointer-events:none';
      var clone = sec.cloneNode(true);
      clone.classList.add('active');
      clone.style.cssText = 'position:absolute;top:0;left:0;width:' + DESIGN_W + 'px;height:' + DESIGN_H + 'px;' +
        'transform:scale(' + (260 / DESIGN_W) + ');transform-origin:top left;margin:0;opacity:1;visibility:visible';
      var notes = clone.querySelector('.notes'); if (notes) notes.remove();
      wrap.appendChild(clone);
      var label = document.createElement('div');
      label.style.cssText = 'padding:8px 10px;font:13px/1.3 system-ui,-apple-system,"PingFang SC",sans-serif;color:#f5f5f4';
      label.textContent = sec.getAttribute('data-title') || ('第 ' + (i + 1) + ' 页');
      cell.appendChild(wrap); cell.appendChild(label);
      cell.addEventListener('click', function () { n.goTo(i); toggleOverview(); });
      overviewGrid.appendChild(cell);
    });
    document.body.appendChild(overviewGrid);
  }

  /* ----- 主题审阅（T 键，§7） ----- */
  function cycleTheme() {
    var themes = window.__THEMES__;
    var declared = document.body.getAttribute('data-themes');
    if (!themes || !declared) return;
    var names = declared.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    if (!names.length) return;
    // 先清空上一组覆盖
    Object.keys(themes[names[(themeIdx - 1 + names.length) % names.length]] || {}).forEach(function (k) {
      document.documentElement.style.removeProperty(k);
    });
    var set = themes[names[themeIdx % names.length]] || {};
    Object.keys(set).forEach(function (k) { document.documentElement.style.setProperty(k, set[k]); });
    themeIdx = (themeIdx + 1) % names.length;
  }

  /* ----- 观众侧同步通道消息处理 ----- */
  function onAudienceMessage(msg) {
    if (!msg || typeof msg !== 'object') return;
    var n = nav();
    switch (msg.type) {
      case 'goto':
        if (typeof msg.seq === 'number' && msg.seq <= lastAppliedSeq) return;   // §15.3 旧消息丢弃
        if (typeof msg.seq === 'number') lastAppliedSeq = msg.seq;
        if (frozen) { frozenPendingIdx = msg.idx | 0; return; }                 // §14 冻结期间保留原页
        clearAnnotations();                                                     // §13.2 翻页自动清除标注
        applyingRemote = true; n.goTo(msg.idx | 0); applyingRemote = false;
        sendAck();
        break;
      case 'screen':
        if (msg.mode === 'freeze') { frozen = true; }
        else if (msg.mode === 'none') {
          frozen = false;
          if (frozenPendingIdx != null) { applyingRemote = true; n.goTo(frozenPendingIdx); applyingRemote = false; frozenPendingIdx = null; sendAck(); }
          applyScreen('none');
        } else { frozen = false; applyScreen(msg.mode); }
        break;
      case 'laser': showLaser(msg.x, msg.y, msg.on !== false); break;
      case 'annotate':
        if (msg.op === 'clear') clearAnnotations();
        else if (msg.op === 'path') drawAnnotation(msg.points);
        break;
      case 'bye':
        // §15.5：脚本打开的观众窗口尝试 close()，拒绝则显示结束遮罩
        ensureOverlays(); endMask.style.display = 'flex';
        try { if (window.opener) window.close(); } catch (_) {}
        break;
      case 'hello':
        sendAck();   // 演讲者窗口握手，回传当前页
        break;
    }
  }
  var lastAppliedSeq = -1;

  function postToPresenter(msg) { if (audienceChannel) audienceChannel.post(msg); }
  function sendAck() { postToPresenter({ type: 'ack', idx: nav().idx(), seq: nextSeq() }); }

  function startHeartbeat() {
    stopHeartbeat();
    heartbeatTimer = setInterval(function () {
      postToPresenter({ type: 'heartbeat', idx: nav().idx(), seq: seqNum });
    }, HEARTBEAT_MS);
  }
  function stopHeartbeat() { if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; } }

  /* ----- 打开演讲者窗口（S 键，§3） ----- */
  function buildConfig() {
    var n = nav();
    var secs = n.slides();
    var slides = secs.map(function (sec, i) {
      var notesEl = sec.querySelector('.notes');
      return {
        id: sec.getAttribute('data-slide-id') || '',
        title: sec.getAttribute('data-title') || ('第 ' + (i + 1) + ' 页'),
        notesHTML: notesEl ? notesEl.innerHTML : '',
        seq: sec.getAttribute('data-sequence') || '',
        file: sec.getAttribute('data-file') || ''
      };
    });
    var deckURL = location.href.split('#')[0].split('?')[0];
    return {
      deckKey: deckKey(),
      deckURL: deckURL,
      syncChannel: syncChannelName(),
      layoutKey: layoutKey(),
      rehearsalKey: rehearsalKey(),
      autoKey: autoKey(),
      notesPrefix: NOTES_PREFIX,
      slideCount: slides.length,
      slides: slides,
      speakerNotes: window.__SPEAKER_NOTES__ || null,
      startIdx: n.idx(),
      designW: DESIGN_W, designH: DESIGN_H,
      reducedMotion: REDUCED,
      targetMinutes: Number(document.body.getAttribute('data-target-minutes')) || 0,
      isFile: location.protocol === 'file:',
      mode: document.body.getAttribute('data-deck-mode') || 'single'
    };
  }

  function openPresenter() {
    if (presenterWin && !presenterWin.closed) { try { presenterWin.focus(); } catch (_) {} return; }
    var cfg = buildConfig();
    var win = window.open('', 'deckPresenter_' + cfg.deckKey, 'width=1280,height=880,menubar=no,toolbar=no,location=no');
    if (!win) { toastPopupBlocked(); return; }              // §15.2 弹窗被拦截
    presenterWin = win;
    win.document.open();
    win.document.write(presenterHTML(cfg));
    win.document.close();
    // 观众侧通道（peer = 演讲者窗口）
    if (audienceChannel) audienceChannel.close();
    audienceChannel = makeChannel(window, function () { return presenterWin; }, cfg.syncChannel, onAudienceMessage);
    lastAppliedSeq = -1;
    startHeartbeat();
    sendAck();
    // 演讲者窗口关闭时清理
    win.addEventListener('pagehide', function () {
      stopHeartbeat();
      if (audienceChannel) { audienceChannel.close(); audienceChannel = null; }
      presenterWin = null;
      applyScreen('none'); clearAnnotations(); showLaser(0, 0, false);
    });
  }

  function toastPopupBlocked() {
    var t = document.createElement('div');
    t.setAttribute('data-pw-chrome', '1');
    t.style.cssText = 'position:fixed;top:18px;left:50%;transform:translateX(-50%);z-index:10001;' +
      'background:#ff453a;color:#fff;padding:12px 20px;border-radius:10px;font:14px/1.5 system-ui,-apple-system,"PingFang SC",sans-serif;' +
      'box-shadow:0 6px 24px rgba(0,0,0,.3)';
    t.textContent = '弹窗被拦截：请在浏览器地址栏允许本页弹出窗口，然后重新按 S';
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 6000);
  }

  /* ----- 观众窗口键盘：S / N / O / T（§3.4 / §4 / §7） ----- */
  function onAudienceKey(e) {
    if (e.target.closest && e.target.closest('input,textarea,select,[contenteditable]')) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var k = e.key;
    if (k === 's' || k === 'S') { e.preventDefault(); openPresenter(); return; }
    if (k === 'n' || k === 'N') { e.preventDefault(); toggleNotesDrawer(); return; }
    if (k === 'o' || k === 'O') { e.preventDefault(); toggleOverview(); return; }
    if (k === 't' || k === 'T') { e.preventDefault(); cycleTheme(); return; }
    if (k === 'Escape') {
      if (notesDrawer && notesDrawer.style.display === 'block') { notesDrawer.style.display = 'none'; return; }
      if (overviewGrid) { toggleOverview(); return; }
    }
  }

  /* ----- 观众窗口安装 ----- */
  function installAudience() {
    ensureOverlays();
    document.addEventListener('keydown', onAudienceKey);
    // 本地翻页 → 通知演讲者窗口（抑制远端回声）
    document.addEventListener('slidechange', function () {
      if (applyingRemote) return;
      if (audienceChannel) { postToPresenter({ type: 'goto', idx: nav().idx(), seq: nextSeq() }); sendAck(); }
    });
    // §15.4 由演讲者窗口重开的观众窗不走 openPresenter：加载即建通道并主动 hello 握手，
    // 演讲者侧收到后补发当前页与标注历史（file:// 降级时 peer = opener 即演讲者窗口）
    if (!audienceChannel) {
      audienceChannel = makeChannel(window, function () { return presenterWin || window.opener; }, syncChannelName(), onAudienceMessage);
      postToPresenter({ type: 'hello', role: 'audience', idx: nav().idx() });
    }
    // 加载完成回传首个 ack（§15.1）——若演讲者窗口已开
    window.addEventListener('pagehide', function () { stopHeartbeat(); if (audienceChannel) audienceChannel.close(); });
  }

  /* ============================ 演讲者窗口 HTML 外壳 ============================ */
  function presenterHTML(cfg) {
    var css = presenterCSS();
    var cfgJSON = JSON.stringify(cfg).replace(/<\/script>/gi, '<\\/script>');
    var fnSrc = presenterMain.toString().replace(/<\/script>/gi, '<\\/script>');
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<title>演讲者视图 — ' + esc(cfg.deckKey) + '</title>' +
      '<style>' + css + '</style></head>' +
      '<body class="pw-body">' +
      '<div id="pw-toolbar"></div>' +
      '<div id="pw-root"></div>' +
      '<div id="pw-help" class="pw-hidden"></div>' +
      '<script>(' + fnSrc + ')(' + cfgJSON + ');<\/script>' +
      '</body></html>';
  }

  function presenterCSS() {
    return '' +
      '*{box-sizing:border-box}' +
      'html,body{margin:0;height:100%;overflow:hidden;background:#16161a;color:#f5f5f4;' +
        'font:14px/1.5 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}' +
      '.pw-body{position:relative}' +
      '#pw-toolbar{position:fixed;top:0;left:0;right:0;height:46px;z-index:50;display:flex;align-items:center;' +
        'gap:10px;padding:0 14px;background:#1f1f24;border-bottom:1px solid #2c2c32}' +
      '#pw-toolbar .pw-lamp{display:inline-flex;align-items:center;gap:6px;font-size:12px;padding:3px 10px;' +
        'border-radius:9999px;background:#2a2a30;border:1px solid #3a3a42}' +
      '#pw-toolbar .pw-lamp i{width:9px;height:9px;border-radius:50%;background:#8e8e93;display:inline-block}' +
      '.pw-lamp[data-state="synced"] i{background:#30d158}.pw-lamp[data-state="connecting"] i{background:#ffd60a}' +
      '.pw-lamp[data-state="unsynced"] i{background:#ff9f0a}.pw-lamp[data-state="frozen"] i{background:#64d2ff}' +
      '.pw-lamp[data-state="disconnected"] i{background:#ff453a}.pw-lamp[data-state="popup-blocked"] i{background:#ff453a}' +
      '#pw-toolbar button{background:#2c2c32;color:#f5f5f4;border:1px solid #3a3a42;border-radius:7px;' +
        'padding:5px 11px;font-size:12px;cursor:pointer}' +
      '#pw-toolbar button:hover{background:#3a3a42}' +
      '#pw-toolbar button.on{background:#0a84ff;border-color:#0a84ff;color:#fff}' +
      '#pw-toolbar .pw-spacer{flex:1}' +
      '#pw-root{position:absolute;top:46px;left:0;right:0;bottom:0}' +
      '.pw-card{position:absolute;background:#1c1c1e;border:1px solid #2c2c32;border-radius:10px;' +
        'display:flex;flex-direction:column;overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,.35);min-width:120px;min-height:120px}' +
      '.pw-card>.pw-head{height:30px;flex:0 0 30px;display:flex;align-items:center;gap:8px;padding:0 10px;' +
        'background:#232329;border-bottom:1px solid #2c2c32;cursor:move;user-select:none;font-size:12px;' +
        'color:#a1a1a6;letter-spacing:.04em}' +
      '.pw-card>.pw-head b{color:#f5f5f4;font-weight:600}' +
      '.pw-card>.pw-body{flex:1;position:relative;overflow:hidden}' +
      '.pw-resize{position:absolute;right:0;bottom:0;width:16px;height:16px;cursor:nwse-resize;z-index:5;' +
        'background:linear-gradient(135deg,transparent 50%,#4a4a52 50%)}' +
      '.pw-preview-wrap{position:absolute;top:0;left:0;transform-origin:top left;background:#000}' +
      '.pw-preview-wrap iframe{border:0;display:block;width:' + DESIGN_W + 'px;height:' + DESIGN_H + 'px;' +
        'pointer-events:none;background:#000}' +
      '.pw-script{padding:12px 14px;overflow:auto;height:100%}' +
      '.pw-script textarea{width:100%;min-height:120px;background:#16161a;color:#f5f5f4;border:1px solid #2c2c32;' +
        'border-radius:7px;padding:9px 11px;font:18px/1.6 system-ui,-apple-system,"PingFang SC",sans-serif;resize:vertical}' +
      '.pw-script .pw-sn-title{font-size:16px;font-weight:600;margin:0 0 6px}' +
      '.pw-script .pw-sn-row{margin:6px 0;font-size:15px;line-height:1.6}' +
      '.pw-script .pw-sn-row .k{color:#8e8e93;margin-right:6px}' +
      '.pw-script ul.pw-talk{margin:4px 0 8px;padding-left:20px}.pw-script ul.pw-talk li{margin:3px 0;font-size:15px;line-height:1.55}' +
      '.pw-script .pw-cue{margin-top:8px;padding:7px 10px;border-left:3px solid #ffd60a;background:#2a2618;' +
        'border-radius:0 6px 6px 0;font-size:14px;color:#ffd60a}' +
      '.pw-timer{padding:12px 14px;display:flex;flex-direction:column;gap:9px;height:100%;overflow:auto}' +
      '.pw-timer .pw-times{display:flex;gap:16px;flex-wrap:wrap}' +
      '.pw-timer .pw-t{flex:1;min-width:90px;background:#16161a;border:1px solid #2c2c32;border-radius:8px;padding:8px 10px}' +
      '.pw-timer .pw-t .lab{font-size:11px;color:#8e8e93}.pw-timer .pw-t .val{font-size:24px;font-variant-numeric:tabular-nums;font-weight:600}' +
      '.pw-timer .pw-t .val.over{color:#ff453a}' +
      '.pw-timer .pw-btns{display:flex;gap:8px;flex-wrap:wrap}' +
      '.pw-timer button{background:#2c2c32;color:#f5f5f4;border:1px solid #3a3a42;border-radius:7px;padding:6px 11px;font-size:12px;cursor:pointer}' +
      '.pw-timer button:hover{background:#3a3a42}.pw-timer button.on{background:#0a84ff;border-color:#0a84ff;color:#fff}' +
      '.pw-timer .pw-page{font-size:13px;color:#a1a1a6}.pw-timer .pw-page b{color:#f5f5f4;font-size:16px}' +
      '.pw-timer .pw-rehearsal{font-size:12px;color:#8e8e93;border-top:1px solid #2c2c32;padding-top:8px;margin-top:2px}' +
      '.pw-timer .pw-rehearsal table{width:100%;border-collapse:collapse;font-size:11px}' +
      '.pw-timer .pw-rehearsal td,.pw-timer .pw-rehearsal th{padding:2px 5px;text-align:left;border-bottom:1px solid #232329}' +
      '.pw-stepper{display:inline-flex;align-items:center;border:1px solid #3a3a42;border-radius:7px;overflow:hidden}' +
      '.pw-stepper button{border:0;border-radius:0;background:#2c2c32;padding:5px 9px;cursor:pointer;color:#f5f5f4}' +
      '.pw-stepper span{padding:0 8px;font-size:12px;min-width:46px;text-align:center;font-variant-numeric:tabular-nums}' +
      '#pw-checklist{position:fixed;top:46px;right:0;width:360px;max-height:calc(100% - 46px);overflow:auto;z-index:60;' +
        'background:#1c1c1e;border-left:1px solid #2c2c32;border-bottom:1px solid #2c2c32;padding:14px;display:none}' +
      '#pw-checklist.open{display:block}' +
      '#pw-checklist h3{margin:0 0 10px;font-size:14px}#pw-checklist .item{display:flex;gap:8px;align-items:flex-start;' +
        'padding:6px 0;border-bottom:1px solid #232329;font-size:12.5px;line-height:1.45}' +
      '#pw-checklist .item .dot{width:9px;height:9px;border-radius:50%;flex:0 0 9px;margin-top:4px}' +
      '#pw-checklist .item.pass .dot{background:#30d158}#pw-checklist .item.fail .dot{background:#ff453a}' +
      '#pw-checklist .item.warn .dot{background:#ffd60a}#pw-checklist .note{margin-top:10px;font-size:11.5px;color:#ff9f0a;line-height:1.5}' +
      '#pw-help{position:fixed;inset:46px 0 0 0;z-index:70;background:rgba(12,12,14,.97);padding:30px 40px;overflow:auto}' +
      '#pw-help.pw-hidden{display:none}#pw-help h2{margin:0 0 14px;font-size:18px}' +
      '#pw-help table{border-collapse:collapse;font-size:13.5px}#pw-help td{padding:5px 14px 5px 0;border-bottom:1px solid #232329}' +
      '#pw-help kbd{background:#2c2c32;border:1px solid #3a3a42;border-radius:5px;padding:1px 7px;font:12px ui-monospace,Menlo,monospace}' +
      '.pw-laser-local{position:fixed;z-index:65;width:14px;height:14px;border-radius:50%;pointer-events:none;' +
        'background:radial-gradient(circle,#ff3b30 0%,rgba(255,59,48,.3) 60%,transparent 70%);transform:translate(-50%,-50%);opacity:0;' +
        'transition:opacity ' + LASER_FADE_MS + 'ms}' +
      '.pw-annotate-local{position:fixed;inset:46px 0 0 0;z-index:64;pointer-events:none}' +
      '.pw-annotate-local.draw{pointer-events:auto;cursor:crosshair}' +
      '.pw-hidden{display:none!important}';
  }

  /* ============================ 演讲者窗口主逻辑（序列化进弹窗，自包含） ============================ */
  function presenterMain(cfg) {
    /* ---- 本函数经 toString() 注入弹窗独立运行，不得引用外层作用域 ---- */
    'use strict';
    var DESIGN_W = cfg.designW, DESIGN_H = cfg.designH;
    var HEARTBEAT_TIMEOUT = 6000;
    var LASER_FADE = 600;
    var DEFAULT_INTERVAL = 30;
    var doc = document, win = window;

    function safeParse(s, fb) { if (s == null) return fb; try { var v = JSON.parse(s); return v == null ? fb : v; } catch (e) { return fb; } }
    function clamp(v, mn, mx, df) { v = Number(v); if (!isFinite(v)) return df; return Math.min(mx, Math.max(mn, v)); }
    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
    function fmt(ms) {
      if (ms == null || !isFinite(ms)) return '—';
      var neg = ms < 0; ms = Math.abs(ms);
      var m = Math.floor(ms / 60000), s = Math.floor((ms % 60000) / 1000);
      return (neg ? '-' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    }

    /* ---- 状态 ---- */
    var idx = clamp(cfg.startIdx, 0, cfg.slideCount - 1, 0);
    var channel = null;
    var lastAckIdx = idx, lastAckSeq = -1, lastHeartbeat = 0, lastAck = 0;
    var frozen = false, screenMode = 'none', popupBlocked = false;
    var laserOn = false, circleOn = false, drawing = false, drawPts = [];
    var annotHistory = [];              // §15.4 当前页标注历史（观众窗重开握手时补发；翻页/清除时清空）
    var audienceWin = null;             // reopenAudience 打开的观众窗（file:// 降级下的 post 目标与来源校验）
    var autoOn = false, autoInterval = DEFAULT_INTERVAL, autoRemaining = 0, autoTimer = null, autoPaused = false;
    var timerState = 'stopped', timerStart = 0, timerAccum = 0, timerTick = null;
    var pageEnterTime = 0, rehearsalActive = false, rehearsalRows = [];
    var applyingRemote = false;
    var seqNum = 0;
    function nextSeq() { return ++seqNum; }

    /* ---- 通道（演讲者侧：peer = opener 观众窗口） ---- */
    function makeChan(onMsg) {
      var useBC = false;
      try { useBC = win.location.protocol !== 'file:' && 'BroadcastChannel' in win; } catch (e) { useBC = false; }
      var bc = null;
      if (useBC) { bc = new win.BroadcastChannel(cfg.syncChannel); bc.onmessage = function (e) { onMsg(e.data); }; }
      else {
        win.addEventListener('message', function (e) {
          if (e.source === win.opener || e.source === audienceWin) onMsg(e.data);   // §15.4 重开的观众窗也是合法来源
        });
      }
      return {
        post: function (m) {
          if (bc) { try { bc.postMessage(m); } catch (e) {} return; }
          try { if (win.opener) win.opener.postMessage(m, '*'); } catch (e) {}
          try { if (audienceWin && audienceWin !== win.opener) audienceWin.postMessage(m, '*'); } catch (e) {}   // file:// 降级同步到重开窗
        },
        close: function () { if (bc) { try { bc.close(); } catch (e) {} } },
        kind: useBC ? 'broadcast' : 'postmessage'
      };
    }

    /* ---- 布局：默认排列 + localStorage 消毒恢复（§3.1） ---- */
    var root = doc.getElementById('pw-root');
    function defaultLayout() {
      var W = root.clientWidth, H = root.clientHeight;
      var pad = 14, gap = 12;
      var leftW = Math.round((W - pad * 2 - gap) * 0.56);
      var rightX = pad + leftW + gap;
      var rightW = W - rightX - pad;
      var topY = pad;
      var prevH = Math.round((H - pad * 2 - gap) * 0.62);
      return {
        CURRENT: { x: pad, y: topY, w: leftW, h: prevH },
        NEXT: { x: rightX, y: topY, w: rightW, h: Math.round(prevH * 0.5) - gap },
        SCRIPT: { x: rightX, y: topY + Math.round(prevH * 0.5) + gap, w: rightW, h: H - (topY + Math.round(prevH * 0.5) + gap) - pad },
        TIMER: { x: pad, y: topY + prevH + gap, w: leftW, h: H - (topY + prevH + gap) - pad }
      };
    }
    function sanitizeLayout(raw) {
      var def = defaultLayout(), out = {};
      if (!raw || typeof raw !== 'object') return def;
      var W = root.clientWidth, H = root.clientHeight;
      ['CURRENT', 'NEXT', 'SCRIPT', 'TIMER'].forEach(function (k) {
        var c = raw[k], d = def[k];
        if (!c || typeof c !== 'object') { out[k] = d; return; }
        var w = clamp(c.w, 120, W, d.w), h = clamp(c.h, 120, H, d.h);
        var x = clamp(c.x, 0, Math.max(0, W - 60), d.x), y = clamp(c.y, 0, Math.max(0, H - 40), d.y);
        if (!isFinite(x) || !isFinite(y) || x > W || y > H || w < 120 || h < 120) { out[k] = d; return; }
        out[k] = { x: x, y: y, w: w, h: h };
      });
      return out;
    }
    var layout = sanitizeLayout(safeParse(win.localStorage.getItem(cfg.layoutKey), null));
    function saveLayout() { try { win.localStorage.setItem(cfg.layoutKey, JSON.stringify(layout)); } catch (e) {} }

    /* ---- 卡片构建 ---- */
    var cards = {};
    function makeCard(key, titleText) {
      var el = doc.createElement('div');
      el.className = 'pw-card';
      el.innerHTML = '<div class="pw-head"><b>' + esc(titleText) + '</b><span class="pw-sub"></span></div>' +
        '<div class="pw-body"></div><div class="pw-resize"></div>';
      root.appendChild(el);
      var body = el.querySelector('.pw-body');
      cards[key] = { el: el, body: body, head: el.querySelector('.pw-head'), sub: el.querySelector('.pw-sub') };
      applyCardGeom(key);
      wireDragResize(key, el);
      return cards[key];
    }
    function applyCardGeom(key) {
      var g = layout[key], el = cards[key].el;
      el.style.transform = 'translate(' + g.x + 'px,' + g.y + 'px)';
      el.style.width = g.w + 'px'; el.style.height = g.h + 'px';
      el.style.left = '0'; el.style.top = '0';
    }
    function wireDragResize(key, el) {
      var head = el.querySelector('.pw-head'), handle = el.querySelector('.pw-resize');
      var drag = null;
      head.addEventListener('mousedown', function (e) {
        if (e.target.tagName === 'BUTTON') return;
        drag = { sx: e.clientX, sy: e.clientY, ox: layout[key].x, oy: layout[key].y };
        e.preventDefault();
      });
      handle.addEventListener('mousedown', function (e) {
        drag = { resize: true, sx: e.clientX, sy: e.clientY, ow: layout[key].w, oh: layout[key].h };
        e.preventDefault();
      });
      win.addEventListener('mousemove', function (e) {
        if (!drag) return;
        if (drag.resize) {
          layout[key].w = clamp(drag.ow + (e.clientX - drag.sx), 120, root.clientWidth, drag.ow);
          layout[key].h = clamp(drag.oh + (e.clientY - drag.sy), 120, root.clientHeight, drag.oh);
        } else {
          layout[key].x = clamp(drag.ox + (e.clientX - drag.sx), 0, root.clientWidth - 60, drag.ox);
          layout[key].y = clamp(drag.oy + (e.clientY - drag.sy), 0, root.clientHeight - 40, drag.oy);
        }
        applyCardGeom(key);
      });
      win.addEventListener('mouseup', function () { if (drag) { drag = null; saveLayout(); } });
    }

    /* ---- 工具栏 ---- */
    var toolbar = doc.getElementById('pw-toolbar');
    function tbButton(label, cls, fn) {
      var b = doc.createElement('button'); b.textContent = label; if (cls) b.className = cls;
      b.addEventListener('click', fn); toolbar.appendChild(b); return b;
    }
    var lamp = doc.createElement('span'); lamp.className = 'pw-lamp'; lamp.setAttribute('data-state', 'connecting');
    lamp.innerHTML = '<i></i><span class="pw-lamp-text">连接中</span>';
    toolbar.appendChild(lamp);
    var spacer = doc.createElement('span'); spacer.className = 'pw-spacer'; toolbar.appendChild(spacer);
    var btnAuto = tbButton('自动翻页：关', '', function () { toggleAuto(); });
    var intervalStepper = doc.createElement('span'); intervalStepper.className = 'pw-stepper';
    intervalStepper.innerHTML = '<button data-d="-5">−</button><span>' + autoInterval + 's</span><button data-d="5">＋</button>';
    toolbar.appendChild(intervalStepper);
    intervalStepper.addEventListener('click', function (e) {
      var d = e.target.getAttribute && e.target.getAttribute('data-d'); if (!d) return;
      autoInterval = clamp(autoInterval + Number(d), 5, 600, DEFAULT_INTERVAL);
      intervalStepper.querySelector('span').textContent = autoInterval + 's';
      if (autoOn) restartAutoCountdown();
    });
    tbButton('激光笔', '', function () { setLaser(!laserOn); });
    tbButton('圈选', '', function () { setCircle(!circleOn); });
    tbButton('清除标注', '', function () { clearAnnotate(); });
    tbButton('黑屏', '', function () { setScreen(screenMode === 'black' ? 'none' : 'black'); });
    tbButton('白屏', '', function () { setScreen(screenMode === 'white' ? 'none' : 'white'); });
    tbButton('冻结', '', function () { setScreen(frozen ? 'none' : 'freeze'); });
    tbButton('检查', '', function () { runChecklist(); });
    tbButton('重置布局', '', function () { layout = defaultLayout(); ['CURRENT', 'NEXT', 'SCRIPT', 'TIMER'].forEach(applyCardGeom); saveLayout(); fitPreviews(); });
    tbButton('重新打开观众屏', '', function () { reopenAudience(); });
    tbButton('结束演示', '', function () { endShow(); });
    tbButton('？', '', function () { toggleHelp(); });

    /* ---- 卡片实例化 ---- */
    makeCard('CURRENT', 'CURRENT');
    makeCard('NEXT', 'NEXT');
    makeCard('SCRIPT', 'SCRIPT');
    makeCard('TIMER', 'TIMER');

    /* ---- 预览 iframe（§3.2 / §18） ---- */
    function previewSrc(i) {
      if (cfg.mode === 'multi' && cfg.slides[i] && cfg.slides[i].file) return cfg.slides[i].file + '?preview=1';
      return cfg.deckURL + '?preview=' + i;
    }
    var ifrCur = null, ifrNext = null;
    function buildPreview(card, i) {
      var wrap = doc.createElement('div'); wrap.className = 'pw-preview-wrap';
      var ifr = doc.createElement('iframe');
      ifr.setAttribute('tabindex', '-1');            // §18.3 焦点恒留演讲者窗口
      ifr.setAttribute('scrolling', 'no');
      ifr.src = previewSrc(i);
      wrap.appendChild(ifr); card.body.appendChild(wrap);
      return { wrap: wrap, iframe: ifr };
    }
    var pvCur = buildPreview(cards.CURRENT, idx);
    var pvNext = buildPreview(cards.NEXT, Math.min(idx + 1, cfg.slideCount - 1));
    ifrCur = pvCur.iframe; ifrNext = pvNext.iframe;
    function fitPreviews() {
      [['CURRENT', pvCur], ['NEXT', pvNext]].forEach(function (pr) {
        var g = layout[pr[0]];
        var scale = Math.min(g.w / DESIGN_W, (g.h - 30) / DESIGN_H);   // 减 header 高
        pr[1].wrap.style.transform = 'scale(' + scale + ')';
        pr[1].wrap.style.width = DESIGN_W + 'px'; pr[1].wrap.style.height = DESIGN_H + 'px';
      });
    }
    fitPreviews();
    win.addEventListener('resize', function () { fitPreviews(); });
    function gotoPreview(ifr, i) {
      try { if (ifr && ifr.contentWindow) ifr.contentWindow.postMessage({ type: 'preview-goto', idx: i }, '*'); } catch (e) {}
    }

    /* ---- SCRIPT 卡：备注 / SPEAKER_NOTES（§2.1 / §10） ---- */
    var scriptBody = cards.SCRIPT.body;
    function slideMeta(i) { return cfg.slides[i] || { id: '', title: '', notesHTML: '', seq: '' }; }
    function noteStorageKey(i) {
      var m = slideMeta(i);
      return cfg.notesPrefix + JSON.stringify([cfg.deckKey, m.seq || '', m.id || ('idx:' + i), '']);
    }
    function readNoteOverride(i) {
      var v = win.localStorage.getItem(noteStorageKey(i));
      return v == null ? null : v;   // 空串是有效值（§2.1 条4）
    }
    function speakerNoteFor(i) {
      if (!cfg.speakerNotes || !cfg.speakerNotes.length) return null;
      var m = slideMeta(i);
      for (var k = 0; k < cfg.speakerNotes.length; k++) if (cfg.speakerNotes[k].id === m.id) return cfg.speakerNotes[k];
      return cfg.speakerNotes[i] || null;
    }
    function renderScript() {
      var i = idx, m = slideMeta(i), sn = speakerNoteFor(i);
      var override = readNoteOverride(i);
      scriptBody.innerHTML = '';
      var wrap = doc.createElement('div'); wrap.className = 'pw-script';
      if (sn) {
        // §10 结构化承载
        var h = '<div class="pw-sn-title">' + esc(sn.title || m.title) + '</div>';
        if (sn.section) h += '<div class="pw-sn-row"><span class="k">章节</span>' + esc(sn.section) + '</div>';
        if (sn.minutes != null) h += '<div class="pw-sn-row"><span class="k">计划</span>' + esc(sn.minutes) + ' 分钟</div>';
        if (sn.purpose) h += '<div class="pw-sn-row"><span class="k">目的</span>' + esc(sn.purpose) + '</div>';
        if (sn.talk && sn.talk.length) {
          h += '<div class="pw-sn-row"><span class="k">讲述</span></div><ul class="pw-talk">' +
            sn.talk.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>';
        }
        if (sn.transition) h += '<div class="pw-sn-row"><span class="k">转场</span>' + esc(sn.transition) + '</div>';
        if (sn.cue) h += '<div class="pw-cue">提示：' + esc(sn.cue) + '</div>';
        wrap.innerHTML = h;
      } else {
        // §2 回退 .notes 富文本（只读展示）+ 可编辑覆盖
        var src = doc.createElement('div');
        src.innerHTML = override != null ? esc(override) : (m.notesHTML || '<em style="opacity:.55">本页无话术</em>');
        src.style.cssText = 'font-size:18px;line-height:1.6;margin-bottom:10px';
        wrap.appendChild(src);
      }
      // §2.1 可编辑 textarea（叠加在承载之上，按 data-slide-id 存储）
      var ta = doc.createElement('textarea');
      ta.value = override != null ? override : '';
      ta.placeholder = '本地备注（叠加保存，不改 HTML 文件）';
      ta.addEventListener('input', function () {
        try { win.localStorage.setItem(noteStorageKey(i), ta.value); } catch (e) {}   // 清空保存空串，不 removeItem
      });
      wrap.appendChild(ta);
      scriptBody.appendChild(wrap);
    }

    /* ---- TIMER 卡（§11） ---- */
    var timerBody = cards.TIMER.body;
    var tTotal, tPage, tLeft, pageLabel, btnStart, btnRehearse, rehearsalBox;
    (function buildTimer() {
      timerBody.innerHTML = '<div class="pw-timer">' +
        '<div class="pw-page">页码 <b class="pw-cur">1</b> / ' + cfg.slideCount + '</div>' +
        '<div class="pw-times">' +
          '<div class="pw-t"><div class="lab">已进行总时长</div><div class="val pw-total">0:00</div></div>' +
          '<div class="pw-t"><div class="lab">本页已用</div><div class="val pw-page-t">0:00</div></div>' +
          '<div class="pw-t"><div class="lab">剩余 / 超时</div><div class="val pw-left">—</div></div>' +
        '</div>' +
        '<div class="pw-btns">' +
          '<button class="pw-start">开始计时</button>' +
          '<button class="pw-reset">重置计时</button>' +
          '<button class="pw-prev">上一页</button>' +
          '<button class="pw-next">下一页</button>' +
          '<button class="pw-rehearse">排练模式</button>' +
        '</div>' +
        '<div class="pw-rehearsal"></div>' +
        '</div>';
      tTotal = timerBody.querySelector('.pw-total');
      tPage = timerBody.querySelector('.pw-page-t');
      tLeft = timerBody.querySelector('.pw-left');
      pageLabel = timerBody.querySelector('.pw-cur');
      btnStart = timerBody.querySelector('.pw-start');
      btnRehearse = timerBody.querySelector('.pw-rehearse');
      rehearsalBox = timerBody.querySelector('.pw-rehearsal');
      timerBody.querySelector('.pw-reset').addEventListener('click', resetTimer);
      timerBody.querySelector('.pw-prev').addEventListener('click', function () { step(-1); });
      timerBody.querySelector('.pw-next').addEventListener('click', function () { step(1); });
      btnStart.addEventListener('click', function () {
        if (timerState === 'stopped' || timerState === 'paused') startTimer(); else pauseTimer();
      });
      btnRehearse.addEventListener('click', toggleRehearsal);
    })();
    function startTimer() {
      if (timerState === 'running') return;
      timerStart = Date.now(); timerState = 'running';
      btnStart.textContent = '暂停计时'; btnStart.classList.add('on');
      if (!timerTick) timerTick = win.setInterval(tickTimer, 250);
    }
    function pauseTimer() {
      if (timerState !== 'running') return;
      timerAccum += Date.now() - timerStart; timerState = 'paused';
      btnStart.textContent = '继续计时'; btnStart.classList.remove('on');
    }
    function resetTimer() {
      timerState = 'stopped'; timerAccum = 0; timerStart = 0;
      btnStart.textContent = '开始计时'; btnStart.classList.remove('on');
      if (timerTick) { win.clearInterval(timerTick); timerTick = null; }
      pageEnterTime = Date.now();
      tickTimer();
    }
    function elapsedTotal() { return timerAccum + (timerState === 'running' ? Date.now() - timerStart : 0); }
    function tickTimer() {
      tTotal.textContent = fmt(elapsedTotal());
      var pageMs = Date.now() - pageEnterTime;
      tPage.textContent = fmt(pageMs);
      var sn = speakerNoteFor(idx);
      if (sn && sn.minutes != null) {
        var left = sn.minutes * 60000 - pageMs;
        tLeft.textContent = fmt(left);
        tLeft.classList.toggle('over', left < 0);
      } else { tLeft.textContent = '—'; tLeft.classList.remove('over'); }
      pageLabel.textContent = String(idx + 1);
      if (rehearsalActive) rehearsalRows[idx] = pageMs;
    }
    function toggleRehearsal() {
      rehearsalActive = !rehearsalActive;
      btnRehearse.classList.toggle('on', rehearsalActive);
      btnRehearse.textContent = rehearsalActive ? '结束排练并保存' : '排练模式';
      if (rehearsalActive) { rehearsalRows = []; pageEnterTime = Date.now(); if (timerState === 'stopped') startTimer(); }
      else { saveRehearsal(); }
    }
    function saveRehearsal() {
      var total = elapsedTotal();
      var rec = { at: Date.now(), total: total, pages: rehearsalRows.map(function (v, i) { return { i: i, ms: v || 0, minutes: (speakerNoteFor(i) || {}).minutes }; }) };
      var hist = safeParse(win.localStorage.getItem(cfg.rehearsalKey), []);
      if (!Array.isArray(hist)) hist = [];
      hist.unshift(rec); hist = hist.slice(0, 5);   // 保留最近 5 次
      try { win.localStorage.setItem(cfg.rehearsalKey, JSON.stringify(hist)); } catch (e) {}
      renderRehearsal();
    }
    function renderRehearsal() {
      var hist = safeParse(win.localStorage.getItem(cfg.rehearsalKey), []);
      if (!Array.isArray(hist) || !hist.length) { rehearsalBox.innerHTML = '<div style="opacity:.6">暂无排练记录</div>'; return; }
      var last = hist[0];
      var rows = (last.pages || []).map(function (p) {
        var plan = p.minutes != null ? p.minutes * 60000 : null;
        var diff = plan != null ? fmt(p.ms - plan) : '—';
        return '<tr><td>' + (p.i + 1) + '</td><td>' + fmt(p.ms) + '</td><td>' + (plan != null ? fmt(plan) : '—') + '</td><td>' + diff + '</td></tr>';
      }).join('');
      rehearsalBox.innerHTML = '<div>最近排练（共 ' + esc(hist.length) + ' 次，总时长 ' + fmt(last.total) + '）</div>' +
        '<table><tr><th>页</th><th>实际</th><th>计划</th><th>差值</th></tr>' + rows + '</table>';
    }
    renderRehearsal();

    /* ---- 翻页（演讲者侧） ---- */
    function step(d) {
      var ni = clamp(idx + d, 0, cfg.slideCount - 1, idx);
      if (ni === idx) return;
      goTo(ni, true);
    }
    function goTo(i, broadcast) {
      i = clamp(i, 0, cfg.slideCount - 1, idx);
      idx = i;
      pageEnterTime = Date.now();
      clearAnnotate();                                                       // §13.2 翻页自动清除标注（本地清空 + 广播观众窗）
      gotoPreview(ifrCur, idx);
      gotoPreview(ifrNext, Math.min(idx + 1, cfg.slideCount - 1));
      renderScript();
      tickTimer();
      refreshAutoCountdown();
      if (broadcast) { channel.post({ type: 'goto', idx: idx, seq: nextSeq() }); }
    }

    /* ---- 自动翻页（§12） ---- */
    function pageIntervalMs() {
      var sn = speakerNoteFor(idx);
      if (sn && sn.autoAdvanceSeconds) return sn.autoAdvanceSeconds * 1000;
      return autoInterval * 1000;
    }
    function autoPausedNow() {
      // §12.3 暂停条件：圈选进行中 / 黑屏白屏冻结 / 未同步或断连 / 文档隐藏
      return circleOn || screenMode !== 'none' || frozen || doc.hidden || lampState() === 'disconnected' || lampState() === 'unsynced';
    }
    function restartAutoCountdown() { autoRemaining = pageIntervalMs(); }
    function refreshAutoCountdown() { if (autoOn) restartAutoCountdown(); }
    function toggleAuto() {
      autoOn = !autoOn;
      btnAuto.textContent = '自动翻页：' + (autoOn ? '开' : '关');
      btnAuto.classList.toggle('on', autoOn);
      try { win.localStorage.setItem(cfg.autoKey, JSON.stringify({ on: autoOn, interval: autoInterval })); } catch (e) {}
      if (autoOn) { restartAutoCountdown(); if (!autoTimer) autoTimer = win.setInterval(autoTick, 250); }
      else { if (autoTimer) { win.clearInterval(autoTimer); autoTimer = null; } }
    }
    function autoTick() {
      if (!autoOn) return;
      if (autoPausedNow()) { autoPaused = true; return; }   // 暂停不清零，保留 remaining（§12.4）
      autoPaused = false;
      autoRemaining -= 250;
      if (autoRemaining <= 0) {
        if (idx >= cfg.slideCount - 1) { autoRemaining = 0; return; }   // §12.5 尾页停止不循环
        step(1);
        restartAutoCountdown();
      }
    }
    (function restoreAuto() {
      var s = safeParse(win.localStorage.getItem(cfg.autoKey), null);
      if (s && typeof s === 'object') { autoInterval = clamp(s.interval, 5, 600, DEFAULT_INTERVAL); intervalStepper.querySelector('span').textContent = autoInterval + 's'; }
    })();

    /* ---- 激光笔 / 圈选（§13） ---- */
    var laserLocal = doc.createElement('div'); laserLocal.className = 'pw-laser-local'; doc.body.appendChild(laserLocal);
    var annotLocal = doc.createElementNS('http://www.w3.org/2000/svg', 'svg');
    annotLocal.setAttribute('class', 'pw-annotate-local'); doc.body.appendChild(annotLocal);
    var laserFadeTimer = null;
    function setLaser(on) {
      laserOn = on;
      if (!on) { laserLocal.style.opacity = '0'; channel.post({ type: 'laser', on: false }); }
    }
    function setCircle(on) {
      circleOn = on;
      annotLocal.classList.toggle('draw', on);
      if (!on) { drawing = false; drawPts = []; }
    }
    function clearAnnotate() {
      while (annotLocal.firstChild) annotLocal.removeChild(annotLocal.firstChild);
      annotHistory = [];                                                     // 历史随清空联动（§13.2 翻页清除 / X 清除）
      channel.post({ type: 'annotate', op: 'clear' });
    }
    win.addEventListener('mousemove', function (e) {
      if (laserOn) {
        var x = e.clientX / win.innerWidth, y = e.clientY / win.innerHeight;
        laserLocal.style.left = e.clientX + 'px'; laserLocal.style.top = e.clientY + 'px'; laserLocal.style.opacity = '1';
        channel.post({ type: 'laser', x: x, y: y, on: true });
        if (laserFadeTimer) win.clearTimeout(laserFadeTimer);
        laserFadeTimer = win.setTimeout(function () { laserLocal.style.opacity = '0'; channel.post({ type: 'laser', on: false }); }, LASER_FADE);
      }
    });
    annotLocal.addEventListener('mousedown', function (e) {
      if (!circleOn) return;
      drawing = true; drawPts = [[e.clientX / win.innerWidth, e.clientY / win.innerHeight]];
      var pl = doc.createElementNS('http://www.w3.org/2000/svg', 'polyline');
      pl.setAttribute('fill', 'none'); pl.setAttribute('stroke', '#ff3b30'); pl.setAttribute('stroke-width', '3');
      pl.setAttribute('stroke-linecap', 'round'); pl.setAttribute('stroke-linejoin', 'round');
      annotLocal.appendChild(pl); drawPts.el = pl;
    });
    win.addEventListener('mousemove', function (e) {
      if (!drawing) return;
      var p = [e.clientX / win.innerWidth, e.clientY / win.innerHeight];
      drawPts.push(p);
      var r = annotLocal.getBoundingClientRect();
      drawPts.el.setAttribute('points', drawPts.map(function (q) { return (q[0] * win.innerWidth - r.left) + ',' + (q[1] * win.innerHeight - r.top); }).join(' '));
    });
    win.addEventListener('mouseup', function () {
      if (!drawing) return;
      drawing = false;
      var pts = drawPts.map(function (q) { return [q[0], q[1]]; });
      annotHistory.push(pts);                                                // §15.4 留存标注历史，观众窗重开时补发
      channel.post({ type: 'annotate', op: 'path', points: pts });
    });

    /* ---- 观众屏控制（§14） ---- */
    function setScreen(mode) {
      if (mode === 'freeze') { frozen = true; screenMode = 'none'; }
      else if (mode === 'none') { frozen = false; screenMode = 'none'; }
      else { frozen = false; screenMode = mode; }
      channel.post({ type: 'screen', mode: mode });
      updateLamp();
    }

    /* ---- 状态灯（§15.2 六态） ---- */
    function lampState() {
      if (popupBlocked) return 'popup-blocked';
      var now = Date.now();
      if (frozen) return 'frozen';
      if (!lastHeartbeat || now - lastHeartbeat >= HEARTBEAT_TIMEOUT) return 'disconnected';
      if (lastAckIdx !== idx) return 'unsynced';
      if (!lastAck) return 'connecting';
      return 'synced';
    }
    var LAMP_TEXT = { connecting: '连接中', synced: '已同步', unsynced: '未同步', frozen: '已冻结', disconnected: '未连接', 'popup-blocked': '弹窗被拦截' };
    function updateLamp() {
      var s = lampState();
      lamp.setAttribute('data-state', s);
      lamp.querySelector('.pw-lamp-text').textContent = LAMP_TEXT[s] || s;
    }

    /* ---- 通道消息（演讲者侧） ---- */
    function onMessage(msg) {
      if (!msg || typeof msg !== 'object') return;
      switch (msg.type) {
        case 'ack':
          lastAck = Date.now(); lastHeartbeat = Date.now();
          if (typeof msg.seq === 'number') lastAckSeq = msg.seq;
          lastAckIdx = msg.idx | 0;
          // §15.3 未同步自愈：页码不一致时重发当前页
          if (lastAckIdx !== idx) channel.post({ type: 'goto', idx: idx, seq: nextSeq() });
          updateLamp();
          break;
        case 'heartbeat':
          lastHeartbeat = Date.now(); lastAckIdx = msg.idx | 0; updateLamp();
          break;
        case 'goto':
          // 观众窗口本地翻页 → 演讲者跟随（不回声）
          if (typeof msg.seq === 'number' && msg.seq <= lastAckSeq) { updateLamp(); return; }
          applyingRemote = true; goTo(msg.idx | 0, false); applyingRemote = false;
          lastAckIdx = msg.idx | 0; updateLamp();
          break;
        case 'hello':
          // §15.4 观众窗重开/重载握手：补发当前页 + 全部标注历史
          channel.post({ type: 'goto', idx: idx, seq: nextSeq() });
          annotHistory.forEach(function (pts) { channel.post({ type: 'annotate', op: 'path', points: pts }); });
          break;
      }
    }

    /* ---- 演前检查（§16） ---- */
    var checklistEl = doc.getElementById('pw-checklist');
    if (!checklistEl) { checklistEl = doc.createElement('div'); checklistEl.id = 'pw-checklist'; doc.body.appendChild(checklistEl); }
    function addItem(cls, text) {
      var d = doc.createElement('div'); d.className = 'item ' + cls;
      d.innerHTML = '<span class="dot"></span><span>' + esc(text) + '</span>';
      checklistEl.appendChild(d);
    }
    function runChecklist() {
      checklistEl.classList.add('open');
      checklistEl.innerHTML = '<h3>演前检查</h3>';
      // 1 观众屏同步
      addItem(lampState() === 'synced' ? 'pass' : 'fail', '观众屏同步：' + (LAMP_TEXT[lampState()] || ''));
      // 2 弹窗权限（试验性 open 立即关闭）
      var tw = null;
      try { tw = win.open('', 'pw_popup_test', 'width=10,height=10'); } catch (e) { tw = null; }
      if (tw) { addItem('pass', '弹窗权限：允许'); try { tw.close(); } catch (e) {} } else { popupBlocked = true; addItem('fail', '弹窗权限：被拦截（请在地址栏允许弹窗）'); updateLamp(); }
      // 3 全屏可用
      addItem(doc.fullscreenEnabled ? 'pass' : 'warn', '全屏可用：' + (doc.fullscreenEnabled ? '是' : '否'));
      // 4 字体就绪
      var fontsOk = true;
      try { fontsOk = doc.fonts && doc.fonts.status === 'loaded'; } catch (e) { fontsOk = false; }
      if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { addItem('pass', '字体就绪：已加载'); });
      else addItem(fontsOk ? 'pass' : 'warn', '字体就绪：' + (fontsOk ? '是' : '检测中'));
      // 5 图片/视频就绪
      var imgs = doc.images || [], imgsOk = true;
      for (var a = 0; a < imgs.length; a++) if (!imgs[a].complete) imgsOk = false;
      addItem(imgsOk ? 'pass' : 'warn', '图片就绪：' + (imgsOk ? '全部完成' : '有未加载'));
      // 6 版面无溢出（演讲者窗口自身）
      var noOverflow = doc.body.scrollWidth <= win.innerWidth + 1 && doc.body.scrollHeight <= win.innerHeight + 1;
      addItem(noOverflow ? 'pass' : 'warn', '版面无溢出：' + (noOverflow ? '是' : '存在溢出'));
      // 7 备注一致性 + data-slide-id 无重复无缺失
      var ids = {}, dup = false, missing = 0;
      cfg.slides.forEach(function (s) {
        if (!s.id) missing++;
        else { if (ids[s.id]) dup = true; ids[s.id] = 1; }
      });
      addItem(!dup && !missing ? 'pass' : 'fail', 'data-slide-id：' + (dup ? '存在重复' : missing ? ('缺失 ' + missing + ' 个') : '无重复无缺失'));
      if (cfg.speakerNotes) {
        var snOk = cfg.speakerNotes.length === cfg.slideCount;
        addItem(snOk ? 'pass' : 'warn', 'SPEAKER_NOTES 数量：' + cfg.speakerNotes.length + ' / 页面 ' + cfg.slideCount + (snOk ? '' : '（不一致）'));
      }
      // 8 时间预算
      if (cfg.targetMinutes > 0) {
        var allHave = cfg.speakerNotes && cfg.speakerNotes.every(function (s) { return s.minutes != null; });
        if (allHave) {
          var sum = cfg.speakerNotes.reduce(function (t, s) { return t + Number(s.minutes || 0); }, 0);
          if (sum > cfg.targetMinutes * 0.9) addItem('fail', '时间预算：总计划 ' + sum.toFixed(1) + ' 分 > 目标 ' + cfg.targetMinutes + '×90%（超时）');
          else if (sum < cfg.targetMinutes * 0.55) addItem('warn', '时间预算：总计划 ' + sum.toFixed(1) + ' 分 < 目标 ' + cfg.targetMinutes + '×55%（脚本量不足）');
          else addItem('pass', '时间预算：总计划 ' + sum.toFixed(1) + ' 分，目标 ' + cfg.targetMinutes + ' 分');
        } else addItem('warn', '时间预算：timing is partial（部分页缺 minutes，跳过）');
      } else addItem('warn', '时间预算：未声明目标时长（data-target-minutes）');
      var note = doc.createElement('div'); note.className = 'note';
      note.textContent = '检查结果不能证明外接屏物理连通，投影仪线缆与扩展模式必须目视确认。';
      checklistEl.appendChild(note);
    }

    /* ---- 重新打开观众屏 / 结束演示（§15.4 / §15.5） ---- */
    function reopenAudience() {
      var w = null;
      try { w = win.open(cfg.deckURL + '#/' + (idx + 1), 'deckAudience_' + cfg.deckKey); } catch (e) { w = null; }
      if (!w) { popupBlocked = true; updateLamp(); return; }
      audienceWin = w;                             // file:// 降级：认这扇重开窗为 post 目标与消息来源
      popupBlocked = false; updateLamp();
      // §15.4 当前页与全部标注由观众窗 load 后的 hello 握手补发；此处延时 goto 兜底
      win.setTimeout(function () {
        channel.post({ type: 'goto', idx: idx, seq: nextSeq() });
      }, 600);
    }
    function endShow() {
      channel.post({ type: 'bye' });
      try { if (win.opener) win.opener.focus(); } catch (e) {}
      win.close();
    }

    /* ---- 快捷键说明（? 键，§17） ---- */
    var helpEl = doc.getElementById('pw-help');
    function toggleHelp() {
      if (helpEl.classList.contains('pw-hidden')) {
        helpEl.innerHTML = '<h2>演讲者窗口快捷键</h2><table>' +
          '<tr><td><kbd>←</kbd> <kbd>→</kbd></td><td>翻页（同步观众窗口）</td></tr>' +
          '<tr><td><kbd>R</kbd></td><td>重置计时器</td></tr>' +
          '<tr><td><kbd>L</kbd></td><td>激光笔开关</td></tr>' +
          '<tr><td><kbd>C</kbd></td><td>圈选模式开关</td></tr>' +
          '<tr><td><kbd>X</kbd></td><td>清除当前页标注</td></tr>' +
          '<tr><td><kbd>B</kbd> / <kbd>W</kbd></td><td>观众屏黑屏 / 白屏</td></tr>' +
          '<tr><td><kbd>Shift</kbd>+<kbd>F</kbd></td><td>冻结 / 恢复观众屏</td></tr>' +
          '<tr><td><kbd>A</kbd></td><td>自动翻页开关</td></tr>' +
          '<tr><td><kbd>Esc</kbd></td><td>关闭演讲者窗口</td></tr>' +
          '<tr><td><kbd>?</kbd></td><td>本说明</td></tr>' +
          '</table>';
        helpEl.classList.remove('pw-hidden');
      } else helpEl.classList.add('pw-hidden');
    }

    /* ---- 键盘（§3.4 / §17；备注 textarea 内不触发） ---- */
    doc.addEventListener('keydown', function (e) {
      var t = e.target;
      if (t && t.closest && t.closest('textarea,input,select,[contenteditable]')) return;
      if (e.key === 'Escape') {
        if (!helpEl.classList.contains('pw-hidden')) { helpEl.classList.add('pw-hidden'); return; }
        if (checklistEl.classList.contains('open')) { checklistEl.classList.remove('open'); return; }
        win.close(); return;
      }
      if (e.key === '?' || (e.key === '/' && e.shiftKey)) { e.preventDefault(); toggleHelp(); return; }
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      switch (e.key) {
        case 'ArrowRight': e.preventDefault(); step(1); break;
        case 'ArrowLeft': e.preventDefault(); step(-1); break;
        case 'r': case 'R': e.preventDefault(); resetTimer(); break;
        case 'l': case 'L': e.preventDefault(); setLaser(!laserOn); break;
        case 'c': case 'C': e.preventDefault(); setCircle(!circleOn); break;
        case 'x': case 'X': e.preventDefault(); clearAnnotate(); break;
        case 'b': case 'B': e.preventDefault(); setScreen(screenMode === 'black' ? 'none' : 'black'); break;
        case 'w': case 'W': e.preventDefault(); setScreen(screenMode === 'white' ? 'none' : 'white'); break;
        case 'F': if (e.shiftKey) { e.preventDefault(); setScreen(frozen ? 'none' : 'freeze'); } break;
        case 'a': case 'A': e.preventDefault(); toggleAuto(); break;
      }
    });

    /* ---- 通道建立 + 心跳监测 + 清理 ---- */
    channel = makeChan(onMessage);
    channel.post({ type: 'hello', role: 'presenter', idx: idx });
    var lampTimer = win.setInterval(function () { updateLamp(); }, 1000);
    pageEnterTime = Date.now();
    goTo(idx, false);
    updateLamp();
    win.addEventListener('pagehide', function () {
      if (timerTick) win.clearInterval(timerTick);
      if (autoTimer) win.clearInterval(autoTimer);
      if (lampTimer) win.clearInterval(lampTimer);
      if (laserFadeTimer) win.clearTimeout(laserFadeTimer);
      if (channel) channel.close();
    });
  }

  /* ============================ 安装 ============================ */
  function install() {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installAudience);
    else installAudience();
  }
  install();

  return {
    role: 'audience',
    open: openPresenter,
    toggleNotesDrawer: toggleNotesDrawer,
    toggleOverview: toggleOverview,
    cycleTheme: cycleTheme,
    deckKey: deckKey
  };
})();
