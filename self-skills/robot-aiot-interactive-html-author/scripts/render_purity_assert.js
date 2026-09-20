/* render_purity_assert.js — render(t) canvas 2D 纯度断言（配合 headless_assert.py 注入运行）
 *
 * 用法:
 *   python3 headless_assert.py deck.html scripts/render_purity_assert.js --deep-link '#/N'
 *   # deck 需先暴露 window.__seek(t)（停 rAF → render(t)，ui-demo-choreography.md §6 同款入口）
 *
 * 契约来源: generative-art-and-canvas.md「render(t) canvas 2D 侧纯函数契约」验收标准——
 *   连续调用 render(0.5) 一万次，像素级一致。
 *   纯度三条（无副作用/单帧单画/时间归一）违反任意一条都会在本断言下现形：
 *   帧计数器、Math.random()、读时钟、跨帧累积拖尾 → 迭代间像素漂移 → FAIL。
 *
 * 参数（注入前在页面或本文件同级 window 上预设即可覆盖）:
 *   window.__PURITY_T__            采样时刻，默认 0.5（t∈[0,1] 入场段中点）
 *   window.__PURITY_N__            调用次数，默认 10000（契约值；调试可临时调小）
 *   window.__PURITY_CAPTURE_EVERY__ 每多少次迭代抓一次像素，默认 100
 *                                  （首末两次必抓且全量逐字节比对；中间抓取按 stride 抽样，
 *                                   万次全量读回在 headless 下不可行——两个都设 1 即严格全比对）
 *   window.__PURITY_STRIDE__       中间抓取的字节比对步长，默认 16
 *   window.__PURITY_CANVAS_SELECTOR__ canvas 选择器，默认 'canvas'（多 canvas 页指定目标）
 *
 * 结果: window.__ASSERT_RESULT__ 写入 PASS/FAIL 行（headless_assert.py 约定，含 FAIL 退出码 1）。
 * 语法自检: node --check scripts/render_purity_assert.js
 */
(function () {
  var lines = [];
  function fail(msg) {
    lines.push('FAIL render-purity: ' + msg);
    window.__ASSERT_RESULT__ = lines.join('\n');
  }

  var T = window.__PURITY_T__ !== undefined ? window.__PURITY_T__ : 0.5;
  var N = window.__PURITY_N__ !== undefined ? window.__PURITY_N__ : 10000;
  var EVERY = window.__PURITY_CAPTURE_EVERY__ !== undefined ? window.__PURITY_CAPTURE_EVERY__ : 100;
  var STRIDE = window.__PURITY_STRIDE__ !== undefined ? window.__PURITY_STRIDE__ : 16;
  var SELECTOR = window.__PURITY_CANVAS_SELECTOR__ || 'canvas';

  var seek = window.__seek || window.render;
  if (typeof seek !== 'function') {
    fail('window.__seek 缺失（也无 window.render 兜底）——契约要求暴露 seek 入口: 停 rAF → render(t)');
    return;
  }
  var cv = document.querySelector(SELECTOR);
  if (!cv || cv.tagName !== 'CANVAS') {
    fail('canvas 未找到 (selector=' + SELECTOR + ')——本断言只覆盖 canvas 2D 侧 render(t)');
    return;
  }
  if (!(cv.width > 0 && cv.height > 0)) {
    fail('canvas 尺寸为 0 (' + cv.width + 'x' + cv.height + ')，页面可能未完成初始化');
    return;
  }
  var ctx = cv.getContext('2d');
  if (!ctx) {
    fail('canvas 2d 上下文不可用（可能是 webgl 页，本断言仅适用 canvas 2D）');
    return;
  }

  function diffFull(a, b) {
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return i;
    return -1;
  }
  function diffStride(a, b, s) {
    for (var i = 0; i < a.length; i += s) if (a[i] !== b[i]) return i;
    return -1;
  }

  var t0 = Date.now();
  var ref = null;
  var refIter = 0;
  var captures = 0;
  var mismatch = null;
  for (var k = 1; k <= N; k++) {
    try {
      seek(T);
    } catch (e) {
      fail('第 ' + k + ' 次调用抛异常: ' + String((e && e.message) || e));
      return;
    }
    var isEdge = k === 1 || k === N;
    if (isEdge || k % EVERY === 0) {
      var data = ctx.getImageData(0, 0, cv.width, cv.height).data;
      captures++;
      if (ref === null) {
        ref = data;
        refIter = k;
      } else {
        var d = isEdge ? diffFull(ref, data) : diffStride(ref, data, STRIDE);
        if (d >= 0) {
          mismatch =
            '第 ' + k + ' 次 render(' + T + ') 与第 ' + refIter + ' 次基准像素不一致' +
            (isEdge ? '（全量比对）' : '（stride=' + STRIDE + ' 抽样）') +
            ': byte[' + d + '] ' + ref[d] + ' -> ' + data[d] +
            '——render(t) 非纯函数（帧计数器/随机/读时钟/跨帧累积之一）';
          break;
        }
      }
    }
  }
  var secs = ((Date.now() - t0) / 1000).toFixed(1);
  if (mismatch) {
    fail(mismatch + '（' + secs + 's, 迭代 ' + k + '/' + N + '）');
    return;
  }
  lines.push(
    'PASS render-purity: render(' + T + ')×' + N + ' 像素一致' +
    '（captures=' + captures + ', 首末全量+中间 stride=' + STRIDE + ' 抽样, ' +
    'canvas=' + cv.width + 'x' + cv.height + ', ' + secs + 's）'
  );
  window.__ASSERT_RESULT__ = lines.join('\n');
})();
