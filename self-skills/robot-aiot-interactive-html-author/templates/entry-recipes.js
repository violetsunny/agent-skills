/* ============================================================================
 * entry-recipes.js — 页面级入场编排 recipe（cascade / hero / quote /
 *                     directional / pipeline 五种，帧级参数固化）
 *
 * 来源：references/animation-fx-catalog.md §1c（乙类：按 recipe 表与实现规则
 *       逐条实现；缓动别名取同文件 §1b：quart-out = cubic-bezier(0.22,1,0.36,1)）
 * 用途：页面激活时把一组 data-anim 元素按语义顺序播完。单个效果是叶子级动作，
 *       recipe 是页面级编排；一个 recipe 计入"单页 CSS 入场 ≤2 种"预算时算 1 种
 * 挂载属性分工：<section> 用 data-animate="<recipe>" 选编排（不加 = cascade）；
 *       元素用裸 data-anim（无值）加入编排，或取角色值 left / right / divider /
 *       line / step；pipeline 的步间箭头标 data-anim="arrow"。
 *       §2 的效果名值（如 data-anim="fade-up"）与 recipe 角色值互斥——页面带
 *       data-animate 时整页按 recipe 时序播，不再单独播单效果名。
 *       data-anim 只挂叶子语义块（标题/lead/卡片/图/列），不挂 grid 容器、
 *       不挂每个 li；整页不想入场就整页不打标。
 * 接线：复制进交付物 <script>。deck 侧两步——
 *       1) 页面激活（slidechange）立即 EntryRecipes.arm(slideEl) 预置起始态，
 *          约 450ms 后（转场中段，避免与转场本体打架）EntryRecipes.playSlide(slideEl)；
 *          翻回页面 playSlide 内部先复位再重播
 *       2) 前进事件（→ / 空格 / 滚轮下滑）先问 EntryRecipes.consumeForward()：
 *          返回 true = pipeline 还有未点亮 step，事件被消费点亮；false = 放行翻页
 * 可调参数：RECIPES 表即帧级参数真源（时长/位移/stagger/start/缓动），
 *       与 md §1c 表一一对应，改表即改节奏
 * 保底：编排脚本报错时把所有 data-anim 强制 opacity:1; transform:none——
 *       内容可读性优先于动效；reduced-motion 先 cancel 全部动画再直接置可见态
 * ============================================================================ */

window.EntryRecipes = (function () {
  'use strict';

  var QUART_OUT = 'cubic-bezier(0.22, 1, 0.36, 1)';
  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 帧级参数固化（md §1c 表逐行转写；单位 ms / px） */
  var RECIPES = {
    cascade: { dur: 750, y: 16, start: 150, stagger: 100, easing: QUART_OUT },
    hero:    { dur: 900, y: 14, start: 200, stagger: 160, easing: QUART_OUT },
    quote: {
      rest:  { dur: 600, y: 8,  start: 200, stagger: 120, easing: QUART_OUT },
      line:  { dur: 800, y: 10, start: 500, stagger: 550, easing: QUART_OUT, from: 0.35 } // opacity 0.35→1 逐句揭示
    },
    directional: {
      rest:      { dur: 750, y: 16, start: 150, stagger: 100, easing: QUART_OUT },
      left:      { dur: 800, x: -24, delay: 350, easing: QUART_OUT },
      divider:   { dur: 500, to: 0.25, delay: 900, easing: QUART_OUT },   // opacity 0→0.25
      right:     { dur: 800, x: 24, delay: 1000, easing: QUART_OUT }
    },
    pipeline: {
      step:      { dur: 500, y: 8, easing: QUART_OUT, dim: 0.15 },        // 进页全部 step 置 opacity 0.15
      arrow:     { dur: 300, delay: 150, to: 0.7, dim: 0.15 }             // 箭头 opacity 0.15→0.7
    }
  };

  /* 预置起始态样式（arm 挂 .er-pre，playSlide 的 WAAPI fill:both 接管后覆盖） */
  var STYLE = document.createElement('style');
  STYLE.textContent =
    '[data-anim].er-pre{opacity:0}' +
    '[data-anim="step"].er-pre,[data-anim="arrow"].er-pre{opacity:.15}';
  document.head.appendChild(STYLE);

  var pipelineState = null;   // { sec, steps, arrows, lit }

  function marked(sec) {
    return Array.prototype.slice.call(sec.querySelectorAll('[data-anim]'));
  }

  /* ---------- 保底与降级 ---------- */
  function forceVisible(sec) {
    marked(sec).forEach(function (el) {
      el.classList.remove('er-pre');
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }
  function reducedShow(sec) {
    document.getAnimations().forEach(function (a) { a.cancel(); });
    forceVisible(sec);
  }

  /* ---------- 复位（翻回页面先复位再重播） ---------- */
  function reset(sec) {
    marked(sec).forEach(function (el) {
      el.getAnimations().forEach(function (a) { a.cancel(); });
      el.style.opacity = '';
      el.style.transform = '';
    });
    pipelineState = null;                                  // 无条件清：经 Prev/总览/深链离开 pipeline 页后不再误吞前进键
  }

  /* ---------- 预置起始态：页面激活即调用，转场中段再 playSlide ---------- */
  function arm(sec) {
    pipelineState = null;                                  // slidechange 即清，不等 450ms 后的 playSlide
    if (REDUCED) return;
    marked(sec).forEach(function (el) { el.classList.add('er-pre'); });
  }

  function fadeSlide(el, p, delay, fromOpacity) {
    var kf0 = { opacity: fromOpacity === undefined ? 0 : fromOpacity, transform: 'translate(' + (p.x || 0) + 'px, ' + (p.y || 0) + 'px)' };
    var kf1 = { opacity: 1, transform: 'translate(0px, 0px)' };
    if (p.to !== undefined) { kf0.opacity = fromOpacity === undefined ? 0 : fromOpacity; kf1.opacity = p.to; }
    el.classList.remove('er-pre');
    return el.animate([kf0, kf1], { duration: p.dur, delay: delay, easing: p.easing, fill: 'both' });
  }

  /* ---------- 五种 recipe ---------- */
  function playCascade(sec, els, R) {
    els.forEach(function (el, i) { fadeSlide(el, R, R.start + i * R.stagger); });
  }

  function playQuote(sec, els) {
    var R = RECIPES.quote;
    var rest = els.filter(function (el) { return el.dataset.anim !== 'line'; });
    var lines = els.filter(function (el) { return el.dataset.anim === 'line'; });
    rest.forEach(function (el, i) { fadeSlide(el, R.rest, R.rest.start + i * R.rest.stagger); });
    lines.forEach(function (el, i) {                    // 行间 stagger 0.55s，逐句揭示
      fadeSlide(el, R.line, R.line.start + i * R.line.stagger, R.line.from);
    });
  }

  function playDirectional(sec, els) {
    var R = RECIPES.directional;
    var roles = { left: [], right: [], divider: [] };
    var rest = [];
    els.forEach(function (el) {
      var r = el.dataset.anim;
      if (roles[r]) roles[r].push(el); else rest.push(el);
    });
    rest.forEach(function (el, i) {                      // 其余元素先出
      fadeSlide(el, R.rest, R.rest.start + i * R.rest.stagger);
    });
    roles.left.forEach(function (el) { fadeSlide(el, R.left, R.left.delay); });       // 左列 x -24→0
    roles.divider.forEach(function (el) { fadeSlide(el, R.divider, R.divider.delay); }); // 分割线 opacity 0→0.25
    roles.right.forEach(function (el) { fadeSlide(el, R.right, R.right.delay); });    // 右列 x 24→0
  }

  function playPipeline(sec, els) {
    var R = RECIPES.pipeline;
    var steps = els.filter(function (el) { return el.dataset.anim === 'step'; });
    var arrows = els.filter(function (el) { return el.dataset.anim === 'arrow'; });
    els.forEach(function (el) {                          // 进页全部 step/箭头置 0.15（.er-pre 已置）
      if (el.dataset.anim !== 'step' && el.dataset.anim !== 'arrow') fadeSlide(el, RECIPES.cascade, RECIPES.cascade.start);
    });
    pipelineState = { sec: sec, steps: steps, arrows: arrows, lit: 0 };
    steps.forEach(function (el) { el.classList.add('er-pre'); });
    arrows.forEach(function (el) { el.classList.add('er-pre'); });
  }

  /* pipeline 与导航耦合：前进事件先问本钩子，有未点亮 step 则消费事件 */
  function consumeForward() {
    if (!pipelineState) return false;
    var st = pipelineState, R = RECIPES.pipeline;
    if (st.lit >= st.steps.length) return false;         // 全部点亮后才放行翻页
    var step = st.steps[st.lit];
    step.classList.remove('er-pre');
    step.animate([{ opacity: R.step.dim, transform: 'translateY(' + R.step.y + 'px)' },
                  { opacity: 1, transform: 'translateY(0px)' }],
      { duration: R.step.dur, easing: R.step.easing, fill: 'both' });
    var arrow = st.arrows[st.lit];                       // step 间箭头随点亮跟进
    if (arrow) {
      arrow.classList.remove('er-pre');
      arrow.animate([{ opacity: R.arrow.dim }, { opacity: R.arrow.to }],
        { duration: R.arrow.dur, delay: R.arrow.delay, easing: R.step.easing, fill: 'both' });
    }
    st.lit++;
    return true;
  }

  /* ---------- 主入口 ---------- */
  function playSlide(sec) {
    try {
      if (!sec) return;
      var recipe = sec.dataset.animate || 'cascade';     // 不加 data-animate = cascade（默认）
      var els = marked(sec);
      reset(sec);
      if (REDUCED) { reducedShow(sec); return; }
      if (!els.length) return;
      if (recipe === 'quote') playQuote(sec, els);
      else if (recipe === 'directional') playDirectional(sec, els);
      else if (recipe === 'pipeline') playPipeline(sec, els);
      else playCascade(sec, els, RECIPES[recipe] ? mergeDefaults(RECIPES[recipe]) : RECIPES.cascade);
    } catch (err) {
      forceVisible(sec);                                 // 保底：报错强制可见
    }
  }

  function mergeDefaults(R) {
    return { dur: R.dur, y: R.y, x: 0, start: R.start, stagger: R.stagger, easing: R.easing };
  }

  return {
    playSlide: playSlide,     // 转场开始约 450ms 后调用
    arm: arm,                 // 页面激活即调用（预置起始态）
    reset: reset,
    consumeForward: consumeForward,
    forceVisible: forceVisible,
    RECIPES: RECIPES
  };
})();
