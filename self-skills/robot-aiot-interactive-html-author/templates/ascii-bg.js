/* ============================================================================
 * ascii-bg.js — ASCII 字符呼吸场（封面/章节页点阵质感背景，canvas 2D + rAF）
 *
 * 来源：references/generative-art-and-canvas.md「ASCII 字符呼吸场」（乙类：
 *       按行为规格实现；噪声场代码块逐字内嵌）
 * 用途：单色品牌底上，等宽字符网格随噪声场明暗涌动，"仪表板呼吸"质感；
 *       纯 canvas 2D + rAF 零依赖，遵循动效画布生命周期契约全部条款
 * 接线：AsciiBg.mount(container, opts) 把 <canvas class="ascii-bg"> 插为容器
 *       第一个子元素并返回实例 { start, stop, destroy }；容器内其余内容需
 *       position:relative; z-index:1 浮于其上（canvas 的 CSS 由本文件写入）。
 *       随页启停示例：
 *         const inst = AsciiBg.mount(document.querySelector('#s3 .ascii-host'));
 *         document.addEventListener('slidechange', e =>
 *           e.detail.index === 2 ? inst.start() : inst.stop());
 *       多个实例自动共用一个 rAF 循环；低功耗模式切换广播自定义事件
 *       document.dispatchEvent(new CustomEvent('deck:lowpower', {detail:{on:true}}))
 * 可调参数：opts.cell 网格边长（默认 16；帧率不足先放大到 20-24 降密度，
 *       不降帧率）；opts.theme 'dark'（默认，白色字符 + screen 混合）|
 *       'light'（主色字符读 --primary-color + multiply 混合），不硬编码色值
 * 预算：计入该页"一页一效"名额与 animation-fx-catalog.md 持续型"全套 ≤3 页"
 * 降级：prefers-reduced-motion 不启动循环，只画 t=0 静态单帧；页面隐藏停循环
 *       并 clearRect，恢复时重置 t0 不累计旧时间；stop 必 clearRect 不留残影
 * ============================================================================ */

window.AsciiBg = (function () {
  'use strict';

  var PALETTE = '   ...:::---+++***◦◦••▢▣';   // 由疏到密，开头三个空格 = 纯留白档
  var FONT_PX = 13;
  var instances = [];
  var sharedRaf = 0, frame = 0, t0 = null;
  var lowPower = false;
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 噪声场（md 逐字）：四个 sin 项叠加取均值到 [-1,1] ---------- */
  function field(col, row, cols, rows, t) {
    const n = (
      Math.sin(col * 0.18 + t) +
      Math.sin(row * 0.24 - t * 0.7) +
      Math.sin((col + row) * 0.12 + t * 0.45) +
      Math.sin(Math.hypot(col - cols * 0.5, row - rows * 0.5) * 0.16 - t * 0.55)
    ) / 4;
    const v = (n + 1) / 2; // [0,1]
    return v;
  }

  /* ---------- 单帧绘制 ---------- */
  function draw(inst, t) {
    var ctx = inst.ctx, cell = inst.cell;
    ctx.clearRect(0, 0, inst.cssW, inst.cssH);
    var cols = inst.cols, rows = inst.rows;
    for (var row = 0; row < rows; row++) {
      for (var col = 0; col < cols; col++) {
        var v = field(col, row, cols, rows, t);
        if (v < 0.22) continue;                       // 留白比例决定质感，画满即噪
        var idx = Math.min(PALETTE.length - 1, Math.floor(v * PALETTE.length));
        var ch = PALETTE[idx];
        if (ch === ' ') continue;                     // 命中空格档直接跳过，不进 fillText
        var alpha = 0.08 + (v - 0.22) * 0.55;         // 透明度随场值线性爬升
        ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
        ctx.fillText(ch, col * cell, row * cell);
      }
    }
    ctx.globalAlpha = 1;
  }

  /* ---------- 共享 rAF 循环（多实例一个循环，不各开各的） ---------- */
  function loop(now) {
    frame++;
    if (t0 === null) t0 = now;
    var t = ((now - t0) / 1000) * 0.55;               // 慢是关键，快了显躁
    var anyRunning = false;
    for (var i = 0; i < instances.length; i++) {
      var inst = instances[i];
      if (!inst.running) continue;
      anyRunning = true;
      if (!inst.onScreen && (frame & 3) !== 0) continue;  // 离屏降帧：每 4 帧画一次
      draw(inst, t);
    }
    if (anyRunning && !lowPower && !document.hidden) {
      sharedRaf = requestAnimationFrame(loop);
    } else {
      sharedRaf = 0;
    }
  }
  function ensureLoop() {
    if (!sharedRaf && !lowPower && !reduced && !document.hidden) {
      t0 = null;                                       // 启动/恢复以 performance.now() 重置 t0
      sharedRaf = requestAnimationFrame(loop);
    }
  }
  function anyRunning() {
    return instances.some(function (i) { return i.running; });
  }

  /* ---------- 页面隐藏暂停：停循环并 clearRect；恢复重置 t0 再启动 ---------- */
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      if (sharedRaf) { cancelAnimationFrame(sharedRaf); sharedRaf = 0; }
      instances.forEach(function (inst) { inst.ctx.clearRect(0, 0, inst.cssW, inst.cssH); });
    } else if (anyRunning()) {
      ensureLoop();
    }
  });

  /* ---------- 低功耗模式切换（自定义事件广播）：stop/start，stop 必 clearRect ---------- */
  document.addEventListener('deck:lowpower', function (e) {
    lowPower = !!(e.detail && e.detail.on);
    if (lowPower) {
      if (sharedRaf) { cancelAnimationFrame(sharedRaf); sharedRaf = 0; }
      instances.forEach(function (inst) { inst.ctx.clearRect(0, 0, inst.cssW, inst.cssH); });
    } else if (anyRunning()) {
      ensureLoop();
    }
  });

  /* ---------- 尺寸重建（ResizeObserver + DPR，rAF 去抖） ---------- */
  function resize(inst) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var rect = inst.canvas.getBoundingClientRect();
    inst.cssW = Math.max(1, rect.width);
    inst.cssH = Math.max(1, rect.height);
    inst.canvas.width = Math.round(inst.cssW * dpr);
    inst.canvas.height = Math.round(inst.cssH * dpr);
    inst.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var mono = getComputedStyle(document.documentElement).getPropertyValue('--mono').trim() || 'monospace';
    inst.ctx.font = '500 ' + FONT_PX + 'px ' + mono;
    inst.ctx.textBaseline = 'top';
    inst.ctx.fillStyle = inst.color;
    inst.cols = Math.ceil(inst.cssW / inst.cell);
    inst.rows = Math.ceil(inst.cssH / inst.cell);
    if (inst.running || reduced) draw(inst, reduced ? 0 : ((performance.now() - (t0 || performance.now())) / 1000) * 0.55);
  }

  /* ---------- 挂载 ---------- */
  function mount(container, opts) {
    opts = opts || {};
    var cell = opts.cell || 16;                        // CELL = 16px（性能不足放大到 20-24）
    var theme = opts.theme || 'dark';
    var canvas = document.createElement('canvas');
    canvas.className = 'ascii-bg';
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;' +
      'mix-blend-mode:' + (theme === 'light' ? 'multiply' : 'screen') + ';opacity:.92';
    container.insertBefore(canvas, container.firstChild);
    if (getComputedStyle(container).position === 'static') container.style.position = 'relative';

    var color = '#fff';                                // 深色品牌底用白色字符（screen 自然发亮）
    if (theme === 'light') {                           // 浅色底改主色字符，读 token 不硬编码
      color = getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim() || '#1c1917';
    }

    var inst = {
      canvas: canvas, ctx: canvas.getContext('2d'), cell: cell, color: color,
      cols: 0, rows: 0, cssW: 1, cssH: 1,
      running: false, onScreen: true, resizeRaf: 0
    };
    instances.push(inst);

    // 视口内外判定（离屏降帧依据）
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        inst.onScreen = entries[0].isIntersecting;
      }).observe(canvas);
    }

    // 尺寸重建走 ResizeObserver，回调用 rAF 去抖（cancel 上一帧再排新帧）
    new ResizeObserver(function () {
      cancelAnimationFrame(inst.resizeRaf);
      inst.resizeRaf = requestAnimationFrame(function () { resize(inst); });
    }).observe(canvas);

    resize(inst);

    var api = {
      start: function () {
        if (reduced) { draw(inst, 0); return; }        // reduced-motion：不启动循环，只画 t=0 静态单帧
        inst.running = true;
        ensureLoop();
      },
      stop: function () {
        inst.running = false;
        inst.ctx.clearRect(0, 0, inst.cssW, inst.cssH); // stop 必须 clearRect，不留残影
        if (!anyRunning() && sharedRaf) { cancelAnimationFrame(sharedRaf); sharedRaf = 0; }
      },
      destroy: function () {
        api.stop();
        instances.splice(instances.indexOf(inst), 1);
        canvas.remove();
      }
    };
    if (reduced) draw(inst, 0);                        // 降级静帧先行呈现
    return api;
  }

  return { mount: mount, PALETTE: PALETTE };
})();
