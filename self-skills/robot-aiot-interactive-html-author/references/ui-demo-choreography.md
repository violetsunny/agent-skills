# UI 演示与画廊展示编排

本文件管两件事：**UI 演示编排**（把产品界面的"操作→响应"讲成绑定讲解节拍的演示段）与**画廊展示**（多件产出同屏陈列的统一渲染）。元素级动效参数（涟漪/打字/数字滚动/描边）在 `animation-fx-catalog.md`，时长预算/缓动族/叠加冲突规则在 `keyframe-animation.md`，画布生命周期与确定性随机在 `generative-art-and-canvas.md`——本文件只做编排层，不复制实现。全部纯原生零依赖（WAAPI / rAF / CSS / IntersectionObserver），代码按 `1920x1080` 设计画布编写；缓动别名（cubic-out / quart-out / expo-out / back-out / cubic-in / smooth-inout）见 `animation-fx-catalog.md` §1b。

## 0. 两条公理（凌驾于本文件所有参数）

| 公理 | 内容 |
|---|---|
| **演示即叙事** | 每个 UI 动作绑定一个讲解节拍（`.notes`/SPEAKER_NOTES 的一条 talk，或字幕条一句话）。说不出这个动作对应哪句话，就删掉这个动作——无绑定的动作是杂耍不是演示 |
| **观众视线唯一** | 同一时刻只有一个视觉焦点在动。两处同时动，观众两处都没看见；新焦点必须在旧焦点完全静止后才开始动。环境级微动（呼吸/慢漂）不算焦点，但幅度必须低于注意阈值（位移 ≤10px、周期 ≥8s） |

推论：光标是演示页里唯一的"人"，它在哪，观众看哪；光标不动时不许有别的东西动。

## 1. 决策树：演示页 / 静态截图 / 录屏 GIF / 活体 iframe

```
产品界面需要出场
│
├─ 界面只需"被看"，无元素需要单独动？
│   └─ 静态截图：素材图网格 + lightbox（interactive-html-authoring.md 素材图节）
│
├─ 需要讲"操作→响应"因果，但真实系统不在场 / 现场网络与登录态不可控？
│   └─ UI 演示页：§2 素材三件套 + §3 八式本地重建（默认正确答案）
│
├─ 已有现成录屏，只需线性播放、不需分步控制？
│   └─ 录屏 GIF：只允许小区域辅助（≤1/4 画布），主演示禁用——
│      GIF 不可 seek、不可变速、色带不可控、体积大
│
└─ 真实系统现场可访问、网络稳定、允许真人操作？
    └─ 活体 iframe：仅嵌自有可控页面；嵌第三方站点必踩 §10 三坑，
       任一条不满足即回退 UI 演示页
```

| 形态 | 分步/变速控制 | 现场风险 | 体积 | 判据 |
|---|---|---|---|---|
| 静态截图 | 无 | 零 | 小 | 界面是被观看对象 |
| 录屏 GIF | 无 | 零 | 大 | 小区域氛围辅助 |
| 活体 iframe | 真实交互但不可编排 | 高（网络/登录态/焦点） | 小 | 自有页面 + 现场可控 |
| UI 演示页 | seek/分步/倍速全可控（§9） | 零 | 中 | 因果叙事主体 |

## 2. 素材三件套（动手前先采齐，一次采集八式复用）

| 素材 | 规格 | 用途 |
|---|---|---|
| UI 截图序列 | 每个关键状态一张 2x 截图（源图像素 ≥ 显示尺寸 × 最大放大倍率），命名 `step-01.png`…；需单独动的元素另抠透明底切片（4x 更佳），并记录切片在截图坐标系的槽位 `{x,y,w,h}` | 式③⑥⑧的底图与"演员"；切片动完必须归位槽位，悬浮不落回布局观众立刻读出"假" |
| 高亮遮罩坐标表 | 每步目标区域 `{x,y,w,h}` + border-radius 值，取色器/截图工具实测，禁止目测 | 式②聚焦环与式①点击落点的定位锚 |
| 光标轨迹 | 每段轨迹的起点/终点/弧线控制点，整理成贝塞尔参数；禁止实录真实鼠标（实录带抖动与停顿，需清洗） | 式①轨迹回放 |

制作规范：截图必须来自真实系统（用户实截 / 官方演示视频截帧）；拿不到真实截图先向用户索取，禁止手搓假 UI 或用 CSS 画"像那么回事"的界面——我们在演示这个产品，不是"一个产品"。截图落盘遵守 `interactive-html-authoring.md` 素材图条款（原图高清、禁降质）。所有坐标相对截图左上角，截图装入画布时记录缩放比，坐标同比例换算。

## 3. 八式帧级参数

| # | 式 | 一句话 | 元素级参数交叉引用 |
|---|---|---|---|
| ① | 光标引导点击 | 光标当演员：弧线移动→按压→涟漪→目标响应 | catalog `click-ripple` / `cursor-press-duet` |
| ② | 区域高亮聚焦 | 框外压暗，聚焦环锁定目标 | catalog `marker-circle`（手绘风变体） |
| ③ | 步骤序列播放 | 多步操作串成时间轴，每步绑讲解节拍 | interactive-mode-rules fragment |
| ④ | 数据流动画 | 数据包沿连线匀速流动 | catalog `path-draw` / `icon-micro-motion`、FX `chain-react` |
| ⑤ | 状态切换对比 | 旧新态幕布擦除或交叉淡化 | catalog `card-flip-3d` / `card-morph` |
| ⑥ | 缩放深入细节 | 推近截图区域 + 高清切片交叉淡入 | interactive-html-authoring 素材图节 |
| ⑦ | 打字输入演示 | 字符事件表回放，光标常亮转闪烁 | catalog `typewriter` / `typewriter-multi` |
| ⑧ | 滚动浏览演示 | 快滚急刹，刹车点才是内容 | — |

选型纪律：一页以一种式为主角；多式同页按 §5 留呼吸帧；同一式全 deck 只当一次主角。独立播放时各式用自带 rAF/finished 链；接入 §9 调度器时改用统一时钟 `clock.t` 驱动（纯函数形态），setTimeout 链不可 seek。

### ① 光标引导点击

- 适用：一切"点这里→发生那事"的因果叙事
- 时长/缓动：轨迹移动 600-1000ms smooth-inout；按压 80-120ms cubic-in；回弹 250ms back-out；双圈涟漪 650ms cubic-out、圈间错峰 60-120ms；点击后停顿 ≥400ms
- 关键帧序列：0ms 光标弧线出发（±2px 手抖随接近收敛）→ 600ms 到达目标中心 → 680ms 按压 scale 0.85 → 800ms 双圈涟漪扩散 + 目标同帧亮起（brightness 1→1.08）→ 1050ms 光标回弹 → 1450ms 停顿结束
- 涟漪/按压的元素级参数以 catalog 为准，本式只管轨迹与时序；轨迹是二次贝塞尔 + 两条不可通约频率正弦叠加的确定性手抖

```js
// 光标外层管轨迹 translate，内层管按压 scale——两层两职，不抢同一 transform
function moveCursor(cursor, p0, p2, dur = 800) {
  const p1 = [(p0[0] + p2[0]) / 2 - 120, (p0[1] + p2[1]) / 2 + 70]; // 控制点偏离中点制造弧线
  return new Promise(res => {
    const t0 = performance.now();
    (function frame(now) {
      const p = Math.min(1, (now - t0) / dur);
      const e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2; // smooth-inout 二次近似
      const k = 1 - e;
      let x = k * k * p0[0] + 2 * k * e * p1[0] + e * e * p2[0];
      let y = k * k * p0[1] + 2 * k * e * p1[1] + e * e * p2[1];
      x += Math.sin(e * 47.13) * 2 * k;              // 手抖 ±2px，接近目标收敛
      y += Math.sin(e * 33.7 + 1.3) * 2 * k;
      cursor.style.transform = `translate(${x}px, ${y}px)`;
      p < 1 ? requestAnimationFrame(frame) : res();
    })(t0);
  });
}
// 双圈涟漪：环元素常驻 DOM（scale 0 / opacity 0），fill:forwards 不预渲染起始态
[[0, 52], [100, 76]].forEach(([delay, half]) => {
  document.querySelector(`.ring-${half}`).animate(
    [{ transform: 'scale(0.2)', opacity: 0.55 }, { transform: 'scale(1)', opacity: 0 }],
    { duration: 650, delay, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
});
```

### ② 区域高亮聚焦

- 适用：静态强调"看这一块"，讲解指向截图中某个区域
- 时长/缓动：聚焦环入场 400ms back-out 轻过冲；hold ≥1200ms；退场 300ms cubic-in
- 关键帧序列：0ms 环 scale 1.08→1 + opacity 0→1（环的 9999px box-shadow 即框外压暗层，压暗与锁环一个动作完成）→ 400ms 锁定，讲解开始 → 1600ms 环 opacity 1→0
- 压暗 0.45-0.6 足够，>0.75 变审讯灯；环圆角 = 目标圆角 + padding；定位（left/top/width/height）静态写入一次，不进动画时间轴

```css
#focus-ring{position:absolute;z-index:60;pointer-events:none;opacity:0;
  border:2px solid var(--primary-color);
  box-shadow:0 0 0 9999px rgba(10,15,30,.55)}
```

```js
function focusRegion(host, target, holdMs = 1600) {
  const ring = host.querySelector('#focus-ring');
  const h = host.getBoundingClientRect(), r = target.getBoundingClientRect(), pad = 10;
  Object.assign(ring.style, {
    left: (r.left - h.left - pad) + 'px', top: (r.top - h.top - pad) + 'px',
    width: (r.width + pad * 2) + 'px', height: (r.height + pad * 2) + 'px',
    borderRadius: (parseFloat(getComputedStyle(target).borderRadius) + pad) + 'px'
  });
  ring.animate([{ opacity: 0, transform: 'scale(1.08)' }, { opacity: 1, transform: 'scale(1)' }],
    { duration: 400, easing: 'cubic-bezier(0.34,1.56,0.64,1)', fill: 'forwards' });
  ring.animate([{ opacity: 1 }, { opacity: 0 }],
    { duration: 300, delay: 400 + holdMs, easing: 'cubic-bezier(0.32,0,0.67,0)', fill: 'forwards' });
}
```

### ③ 步骤序列播放

- 适用：多步操作流程（打开列表→选中→操作→确认），演示峰页主力式
- 时长/缓动：步内动作 300-700ms（按对应式）；步骤字幕入场 240ms linear；步间隔 ≥1.5s，含新信息的步 ≥2s
- 关键帧序列：字幕 i 亮 → 式①/②执行动作 → 响应落定 → 满板静止 ≥800ms → 字幕 i+1
- 步骤数 ≤5，超过拆页或合并；两种绑定：手动绑 fragment（`interactive-mode-rules.md`，每次 Next 消费一步，深链 `#/N/M` 直达）；自动绑 §9 调度器 CUES

```js
const STEPS = [
  { target: '#tab-devices', act: 'click',  beat: '打开设备列表' },
  { target: '#row-gw-03',   act: 'focus',  beat: '选中网关 GW-03' },
  { target: '#btn-reboot',  act: 'click',  beat: '下发重启指令' },
  { target: '#toast-ok',    act: 'reveal', beat: '指令已确认，等待设备重连' }
];
const CAPTION = document.getElementById('demo-caption');
function playStep(i) {
  const s = STEPS[i], el = document.querySelector(s.target);
  CAPTION.textContent = `${i + 1}/${STEPS.length} · ${s.beat}`;
  CAPTION.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 240, easing: 'linear', fill: 'both' });
  if (s.act === 'click')  return cursorClick(el);                 // 式①
  if (s.act === 'focus')  { focusRegion(stage, el); return Promise.resolve(); } // 式②
  el.animate([{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'translateY(0)' }],
    { duration: 400, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'both' });
  return Promise.resolve();
}
```

### ④ 数据流动画

- 适用：设备→网关→云的消息流、指令下发等抽象数据链路
- 时长/缓动：数据包 linear 匀速 200-400px/s（匀速运动不加缓动，加了读作抛射物）；包间错峰 400-600ms；端点脉冲 300ms back-out
- 关键帧序列：连线 path-draw 自绘（参数见 catalog）→ 包 opacity 0→1（路径前 6%）→ 匀速行进 → 94%-100% 淡出 → 到达瞬间端点节点 scale 脉冲一次
- 包数 ≤5；作持续氛围时计入 `animation-fx-catalog.md` §1 预算并随页启停

```js
function spawnPackets(pathSel, dots, speed = 300, gap = 500, loops = 3) {
  const d = document.querySelector(pathSel).getAttribute('d');
  const len = document.querySelector(pathSel).getTotalLength();
  dots.forEach((dot, i) => {
    dot.style.offsetPath = `path("${d}")`;
    dot.animate([
      { offsetDistance: '0%',   opacity: 0 },
      { offsetDistance: '6%',   opacity: 1 },
      { offsetDistance: '94%',  opacity: 1 },
      { offsetDistance: '100%', opacity: 0 }
    ], { duration: len / speed * 1000, easing: 'linear', delay: i * gap,
         iterations: loops, fill: 'both' });   // 有限次循环，禁 Infinity
  });
}
```

### ⑤ 状态切换对比

- 适用：before/after、开关状态、新旧版本对比
- 时长/缓动：交叉淡化变体——旧态 250ms cubic-in 淡出下沉 8px、新态 300ms cubic-out 淡入上浮；幕布变体——快甩 250ms expo-out 从 8% 到 72% → 停 500ms → 慢扫 1200ms cubic-out 到 45% 定格（快慢速度比 ≥3:1，否则节奏对比不可感：快甩宣告"变了"，慢扫证明"变在哪"）
- 关键帧序列（幕布）：手柄居左 → 快甩至 72% → 停顿 → 慢扫回 45% → hold ≥1s
- 两版必须同布局同机位，否则读作两个页面；before 用真实旧态（注入旧数据/关闭功能），不手搓"故意丑"的假 before

```js
// 幕布擦除只用 transform：after 窗口层反向平移、内容层等量正向平移，
// 内容始终静止，只有"可见窗口"滑动——不用 clip-path、不动 width
function wipe(stage, wrap, inner, handle, pct, dur = 900) {
  const W = stage.clientWidth, x = W * pct;
  const opts = { duration: dur, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' };
  wrap.animate([{ transform: `translateX(${-W}px)` }, { transform: `translateX(${x - W}px)` }], opts);
  inner.animate([{ transform: `translateX(${W}px)` }, { transform: `translateX(${W - x}px)` }], opts);
  handle.animate([{ transform: 'translateX(0)' }, { transform: `translateX(${x}px)` }], opts);
}
```

### ⑥ 缩放深入细节

- 适用：看清截图上的细节（表格字段、工具栏按钮、状态图标）
- 时长/缓动：推进前静止一拍 ≥500ms（让观众先看到全局，直接开推没有空间感）；推进 650-900ms quart-out；高清切片交叉淡入 200ms linear 接推进尾段；hold ≥1500ms；退出 500ms cubic-in
- 关键帧序列：全景静 → scale 1→1.8（transform-origin 落在目标点）→ 480ms 处 4x 切片 opacity 0→1 盖住低清底 → hold → 原曲线反向退出，切片同步淡出
- 防糊铁律：源图像素 ≥ 显示尺寸 × 最大倍率，不足必须叠高清切片；推进期间其余元素禁动（公理二）

```js
function zoomInto(shotFrame, hiSlice, cx, cy, scale = 1.8) {
  shotFrame.style.transformOrigin = `${cx}px ${cy}px`;
  shotFrame.animate([{ transform: 'scale(1)' }, { transform: `scale(${scale})` }],
    { duration: 750, easing: 'cubic-bezier(0.22,1,0.36,1)', fill: 'forwards' });
  hiSlice.animate([{ opacity: 0 }, { opacity: 1 }],
    { duration: 200, delay: 480, easing: 'linear', fill: 'forwards' });
}
```

### ⑦ 打字输入演示

- 适用：搜索框输入、命令行、表单填写——"用户在打字"
- 时长：**汉字 100-150ms/字**（观众逐字跟读的阅读速度下限）；英文字母/数字 40-70ms/字符；终端代码 60-90ms/字符；标点处停 300-500ms；打完到页面响应留 350-450ms 确认停顿（打完立刻响应读作机器自动，观众跟不上因果）
- 关键帧序列：光标入场闪烁 → 开始打字（光标**常亮**，打字中闪烁读作卡顿）→ 可选退格修正一次 → 打完光标转闪烁（常亮→闪烁的切换本身就是"打完了"的信号）→ 确认停顿 → 页面响应
- 与 AI 流式输出是两回事：用户输入逐字符匀稳，AI 输出 chunk 涌现走 catalog `typewriter`/`typewriter-multi`；写混读作"输入框自己在生成"
- 退格修正必须预写进事件表（确定性），禁止运行时 `Math.random`；回放是时间纯函数，双向 seek 安全

```css
.caret{display:inline-block;width:2px;height:1.1em;background:var(--primary-color);vertical-align:-0.15em}
.caret.blink{animation:caret-blink 1s steps(1) infinite}
@keyframes caret-blink{50%{opacity:0}}
```

```js
// 把"打→打错→停→退→改"编译成字符事件表，渲染层按时间查表，任意 t 可回放
function compileTypeScript(text, perChar = 120, typo = null) {
  const ev = []; let t = 0;
  for (let i = 0; i < text.length; i++) {
    if (typo && i === typo.at) {
      ev.push({ t, s: text.slice(0, i) + typo.wrong }); t += perChar;
      t += typo.pause;                                   // 停一拍（150-200ms）
      ev.push({ t, s: text.slice(0, i) }); t += perChar; // 退格
    }
    ev.push({ t, s: text.slice(0, i + 1) });
    t += perChar;
  }
  return { ev, total: t };
}
function renderType(el, caret, script, time) {
  let n = -1;
  while (n + 1 < script.ev.length && script.ev[n + 1].t <= time) n++;
  el.textContent = n < 0 ? '' : script.ev[n].s;
  caret.classList.toggle('blink', time >= script.total);
}
```

### ⑧ 滚动浏览演示

- 适用：长页产品截图、设备列表、日志流——"滚给你看"
- 时长/缓动：一条 expo-out 曲线 700-1100ms 走完"快滚急刹"全程（分段减速会"泵"）；刹车点停留 ≥1.2s；相邻两次"滚动+刹车"间隔 ≥2.6s；15s 窗口内 ≤4 个刹车点——刹车点是注意力消费，比滚动本身贵
- 关键帧序列：静止 → translateY 快滚 → 急刹 → 目标行 brightness 提升 + 其余退暗至 0.38（退暗别到 0，上下文要在）→ 停留 → 下一段
- 滚动用 transform translateY 不用 scrollTop（布局滚动不可合成）；滚动期间禁推近（会晕）；刹车点没有强调，观众不知道为什么停在这

```js
function scrollBrake(strip, fromY, toY, dur = 900) {
  return strip.animate(
    [{ transform: `translateY(${-fromY}px)` }, { transform: `translateY(${-toY}px)` }],
    { duration: dur, easing: 'cubic-bezier(0.16,1,0.3,1)', fill: 'forwards' }).finished;
}
async function scrollDemo(strip, stops) {          // stops: [{y, row}]，独立播放形态
  let y = 0;
  for (const s of stops) {
    await scrollBrake(strip, y, s.y);
    y = s.y;
    s.row.animate([{ filter: 'brightness(1)' }, { filter: 'brightness(1.12)' }],
      { duration: 300, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
    await new Promise(r => setTimeout(r, 1200));  // 接 §9 调度器时改为 cue 时刻，不用 setTimeout 链
  }
}
```

## 4. 能量骨架落位

deck 能量曲线：`封面峰 → 下行陈述 → 铺垫谷（背景/问题/方案） → 【演示峰：UI 演示页】 → 论证段（数据/价值） → 画廊体量页（可选） → 收尾`。

1. UI 演示页通常落在中段"铺垫谷"之后，作为全片"演示峰"：谷为峰提供对比；开场即演示 = 观众没有语境，不知道在看什么
2. 一个 deck 只一个演示峰；多个演示页组成能量递减的演示段：主演示（峰）→ 细节缩放（中）→ 静态截图/画廊（平）
3. 演示峰前 1-2 页是呼吸页：低密度慢节奏，不放高能量特效——hold/静止预算先划走再排动效（对齐 `keyframe-animation.md` build/breathe/resolve）
4. 演示峰后一页必须放结论/价值页承接：演示是证据，主张放下一页
5. 画廊墙页（§6-§8）是"体量陈述"，放演示峰之后、收尾页之前，能量中高但以静态陈列为主，不与演示峰抢
6. 叙事策略对齐 `web-slide-strategies.md`（Product Demo：痛点→Demo→价值→下一步）；明暗节奏上演示峰页可用 hero dark 制造暗拍

## 5. 节奏铁律

1. **交互演示按真人操作速度**：打字、点击、响应全部人速（§3 各式参数）。第一版几乎总是偏快，起稿就按人速写
2. **动作间隔 ≥ 观众消化时间**：简单动作（点击/高亮）后停 ≥0.8s；出现新信息的动作（新面板/新数据/新页面）后停 ≥1.5s
3. **禁止连续无停顿动作**：任何两个演示动作之间至少一个呼吸帧（≥400ms 满板静止）；连发操作观众只记得最后一帧
4. **每式之间留呼吸帧**：同页多式衔接处 0.5s 满板静止；批量动效收尾（网格落完/列表嵌完）满板静止 0.5s 再走下一段
5. **一页一主角**：公理二的执行条款——同页两式并发时，一式降为静态终态
6. **收尾真静止**：演示结束 hold ≥1s，禁任何尾漂（scale 微变、opacity 微调都算）；"静"是设计出来的一拍
7. **节拍对齐**：每个动作起点落在讲解节拍句首，动作总时长 ≤ 该句口播时长；自动播放模式（§9）的字幕条是节拍的可见化

## 6. 画廊墙 render(t) 纯函数模式

多件产出同屏陈列的展览馆式页面：浅底（禁纯黑底——黑底让作品像电影剧照，不像"可被采用的成果"）、卡片带 6px 装裱内边距 + 1px hairline 描边 + 双层软阴影、3D 倾斜参数 rotateX 10-15deg / rotateY ±8-12deg / rotateZ ±2-3deg（打破工整）/ perspective 2000-2800px（<2000 鱼眼，>3000 近正投影）。点击放大走素材 lightbox（`interactive-html-authoring.md`），不在墙内另做浮层。

**统一渲染契约**：`render(t)` 接收归一化时间 t（[0,1] 为入场段，t>1 继续线性推进、只驱动驻场漂移），返回唯一布局状态——所有元素状态由 t 推导，无 setTimeout 链、无状态机、无事件残留；同一 t 渲染一万次是同一画面。三层 DOM 分工（`keyframe-animation.md` 叠加冲突规则的落地）：outer 承接入场（render 写）、body 承接涟漪（§7 rAF 写）、inner 承接 hover 提升（CSS class 写），三层各管一个 transform 互不抢占。

预算与生命周期：画廊墙属持续动效页，仅用户明确要求陈列展示时启用，计入 `animation-fx-catalog.md` §1 持续型预算（全套 ≤3 页）；卡片数 12-30（24 卡 × 4 节点 ≈ 100 DOM，不破单页 ≤500）；rAF 随页启停（`slidechange` 事件，`generative-art-and-canvas.md` 契约）。

```css
.gallery-viewport{position:absolute;inset:0;overflow:hidden;perspective:2400px;perspective-origin:50% 45%}
.gallery-canvas{position:absolute;left:50%;top:50%;width:1600px;margin:-360px 0 0 -800px;
  display:grid;grid-template-columns:repeat(6,1fr);gap:32px;
  transform:rotateX(12deg) rotateY(-8deg) rotateZ(-2deg)}
.g-card{aspect-ratio:16/9;will-change:transform,opacity}
.g-body{width:100%;height:100%;will-change:transform}
.g-inner{width:100%;height:100%;padding:6px;background:#fff;border-radius:14px;overflow:hidden;
  border:1px solid var(--border-color,#e5e5ea);
  box-shadow:0 20px 60px -20px rgba(29,29,31,.12),0 6px 18px -6px rgba(29,29,31,.06);
  transition:transform .35s cubic-bezier(.25,1,.5,1),filter .35s cubic-bezier(.25,1,.5,1)}
.g-inner.lift{transform:translateY(-10px) scale(1.04);filter:brightness(1.05)}
.g-inner img{width:100%;height:100%;object-fit:cover;border-radius:9px;display:block}
```

```js
const COLS = 6, ROWS = 4, ENTRY_SEC = 6;                    // 24 卡，入场段 6s
const easeOutCubic = t => 1 - Math.pow(1 - t, 3);
const clamp01 = v => Math.max(0, Math.min(1, v));
const wall = document.querySelector('.gallery-canvas');
const MAXD = Math.hypot((COLS - 1) / 2, (ROWS - 1) / 2);
const cards = Array.from({ length: COLS * ROWS }, (_, i) => {
  const outer = document.createElement('div'); outer.className = 'g-card';
  const body  = document.createElement('div'); body.className  = 'g-body';
  const inner = document.createElement('div'); inner.className = 'g-inner';
  const img = new Image();
  img.src = `assets/shot-${String(i + 1).padStart(2, '0')}.png`;
  img.alt = `展品 ${i + 1}`;
  inner.appendChild(img); body.appendChild(inner); outer.appendChild(body); wall.appendChild(outer);
  inner.addEventListener('pointerenter', () => inner.classList.add('lift'));
  inner.addEventListener('pointerleave', () => inner.classList.remove('lift'));
  const col = i % COLS, row = (i / COLS) | 0;
  const dc = col - (COLS - 1) / 2, dr = row - (ROWS - 1) / 2;
  return { outer, body, inner, i, dc, dr, delay: Math.hypot(dc, dr) / MAXD * 0.55 };
});

function render(t) {                                          // t 归一化：[0,1] 入场段
  const sec = t * ENTRY_SEC;
  for (const c of cards) {
    const p = easeOutCubic(clamp01((t - c.delay) / 0.45));    // 错峰入场：距中心越远越晚
    const px = Math.sin(sec * 0.5 + c.i * 0.7) * 10 * p;      // 驻场慢漂：两条不可通约频率，
    const py = Math.cos(sec * 0.37 + c.i * 1.1) * 8 * p;      // 避免 marquee 式循环感
    c.outer.style.opacity = p;
    c.outer.style.transform =
      `translate3d(${(1 - p) * c.dc * 60 + px}px, ${(1 - p) * (c.dr * 50 + 40) + py}px, 0)` +
      ` scale(${0.9 + 0.1 * p})`;
  }
}

const host = wall.closest('.slide');
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let raf = 0, t0 = null;
function tick(now) {
  if (t0 === null) t0 = now;
  render((now - t0) / 1000 / ENTRY_SEC);                      // 不取模：无循环断点
  raf = requestAnimationFrame(tick);
}
function start() { if (!raf && !reduced) { t0 = null; raf = requestAnimationFrame(tick); } }
function stop()  { cancelAnimationFrame(raf); raf = 0; }
document.addEventListener('slidechange', e =>
  e.detail.index === +host.dataset.index ? start() : stop());
document.fonts.ready.then(() => {
  render(reduced ? 1 : 0);                                    // reduced-motion：直接终态静帧
  if (host.classList.contains('active')) start();
});
window.__seek = t => { stop(); render(t); };                  // 调试与 headless 截图入口
```

## 7. Gallery Ripple（画廊涟漪）

鼠标位置驱动邻近卡片位移/缩放衰减：写在 §6 的 body 中间层，与入场（outer）、hover（inner）互不抢 transform。衰减用平方曲线（近强远弱、边缘柔和）；位移方向为鼠标→卡片的外推方向，配合小幅 scale 提升，读作"磁场"。卡片中心一次性缓存——每帧 `getBoundingClientRect` 会强制同步布局。

```js
const RADIUS = 320, PUSH = 18, LIFT = 0.06, SMOOTH = 0.15;   // 半径px / 最大位移px / 最大放大 / 平滑系数
const pointer = { x: -1e4, y: -1e4, sx: -1e4, sy: -1e4 };
wall.addEventListener('pointermove', e => {
  const r = wall.getBoundingClientRect();
  pointer.x = e.clientX - r.left;
  pointer.y = e.clientY - r.top;
});
wall.addEventListener('pointerleave', () => { pointer.x = pointer.y = -1e4; });

function measure() {                                          // 布局就绪后缓存卡片中心，resize 重测
  const wr = wall.getBoundingClientRect();
  for (const c of cards) {
    const r = c.outer.getBoundingClientRect();
    c.cx = r.left + r.width / 2 - wr.left;
    c.cy = r.top + r.height / 2 - wr.top;
  }
}
document.fonts.ready.then(() => requestAnimationFrame(measure));
new ResizeObserver(measure).observe(wall);

let ripRaf = 0;
function rippleTick() {
  pointer.sx += (pointer.x - pointer.sx) * SMOOTH;            // 指数平滑：太快抖、太慢拖
  pointer.sy += (pointer.y - pointer.sy) * SMOOTH;
  for (const c of cards) {
    const dx = c.cx - pointer.sx, dy = c.cy - pointer.sy;
    const d = Math.hypot(dx, dy) || 1;
    const f = Math.max(0, 1 - d / RADIUS);
    const e = f * f;                                          // 平方衰减
    c.body.style.transform =
      `translate(${(dx / d) * e * PUSH}px, ${(dy / d) * e * PUSH}px) scale(${1 + e * LIFT})`;
  }
  ripRaf = requestAnimationFrame(rippleTick);
}
function startRipple() { if (!ripRaf && !reduced) { measure(); ripRaf = requestAnimationFrame(rippleTick); } }
function stopRipple()  { cancelAnimationFrame(ripRaf); ripRaf = 0; }
// 启停并入 §6 的 slidechange 订阅点：start() 内追加 startRipple()，stop() 内追加 stopRipple()
```

指针离开后 `sx/sy` 平滑趋近 -1e4，卡片自然回位，无跳变。reduced-motion 下涟漪不启动，墙保持静态终帧。

## 8. Dashboard Overlay（仪表盘浮层）

数据卡片从演示截图/页面之上逐层浮现：遮罩压暗 → 卡片 stagger 入场 → 数字滚动 → 图表渐进绘制 → hold。元素级参数（数字+缩放复合、柱/条/环生长、追踪线扫过）见 catalog `count-scale` / `stat-grow` / `chart-scrub`；数字滚动必须有终止条件并 snap 精确值（`interactive-mode-rules.md` animateNumber 契约）。本节给编排层完整实现。

时序：0ms 遮罩 opacity 0→1（300ms cubic-out）→ 卡片 i 入场 delay 200+i×120ms（500ms expo-out，y 24px + scale 0.96）→ 每卡落定后 300ms 数字滚动（1200ms cubic-out，`tabular-nums` 防抖）→ 后缀符号 back-out 弹入 → 图表 polyline dashoffset 绘制（delay 600ms，1400ms cubic-out）→ 全部落定 hold ≥1s（§5 铁律 6）。

```html
<div class="dash-overlay" id="dash">
  <div class="dash-card" data-count="1284">
    <div class="k">在线设备</div><div class="v"><span class="num">0</span><span class="suf"></span></div>
  </div>
  <div class="dash-card" data-count="99.2" data-decimals="1" data-suffix="%">
    <div class="k">指令成功率</div><div class="v"><span class="num">0</span><span class="suf"></span></div>
  </div>
  <div class="dash-card wide">
    <div class="k">近 24h 上行消息（示意）</div>
    <svg viewBox="0 0 480 120" class="spark" aria-hidden="true"><polyline points="0,100 40,88 80,92 120,70 160,74 200,52 240,58 280,40 320,46 360,30 400,36 440,18 480,24" fill="none" stroke="var(--primary-color)" stroke-width="3" stroke-linejoin="round"/></svg>
  </div>
</div>
```

```css
.dash-overlay{position:absolute;inset:0;z-index:40;background:rgba(10,15,30,.55);opacity:0}
.dash-card{position:absolute;width:360px;padding:24px 28px;background:#fff;border-radius:14px;
  border:1px solid var(--border-color,#e5e5ea);box-shadow:0 24px 64px -24px rgba(15,23,42,.35);opacity:0}
.dash-card .k{font-size:14px;color:var(--text-secondary,#545458)}
.dash-card .v{font-size:44px;font-weight:700;font-variant-numeric:tabular-nums}
.dash-card .suf{font-size:24px;margin-left:4px}
.spark{width:100%;height:120px}
```

```js
function countTo(el, card) {
  const target = parseFloat(card.dataset.count);
  const dec = parseInt(card.dataset.decimals || '0', 10);
  const dur = 1200, t0 = performance.now();
  (function step(now) {
    const p = Math.min(1, (now - t0) / dur);
    el.textContent = (target * (1 - Math.pow(1 - p, 3))).toFixed(dec);   // cubic-out
    if (p < 1) { requestAnimationFrame(step); return; }
    el.textContent = target.toFixed(dec);                                // 终止 snap 精确值
    const suf = card.querySelector('.suf');
    if (suf && card.dataset.suffix) {
      suf.textContent = card.dataset.suffix;
      suf.animate([{ opacity: 0, transform: 'scale(.6)' }, { opacity: 1, transform: 'scale(1)' }],
        { duration: 400, easing: 'cubic-bezier(0.34,1.56,0.64,1)', fill: 'both' });
    }
  })(t0);
}
function playDashboard(root) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const cards = [...root.querySelectorAll('.dash-card')];
  const line = root.querySelector('.spark polyline');
  const len = line ? line.getTotalLength() : 0;
  if (line) line.style.strokeDasharray = len;
  if (reduced) {                                             // 降级：直显终态
    root.style.opacity = 1;
    cards.forEach(c => { c.style.opacity = 1;
      const n = c.querySelector('.num');
      if (n) n.textContent = (+c.dataset.count).toFixed(+(c.dataset.decimals || 0));
      const s = c.querySelector('.suf'); if (s && c.dataset.suffix) s.textContent = c.dataset.suffix; });
    if (line) line.style.strokeDashoffset = 0;
    return;
  }
  root.animate([{ opacity: 0 }, { opacity: 1 }],
    { duration: 300, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
  cards.forEach((card, i) => {
    const delay = 200 + i * 120;
    card.animate([{ opacity: 0, transform: 'translateY(24px) scale(.96)' },
                  { opacity: 1, transform: 'translateY(0) scale(1)' }],
      { duration: 500, delay, easing: 'cubic-bezier(0.16,1,0.3,1)', fill: 'both' });
    const num = card.querySelector('.num');
    if (num && card.dataset.count) setTimeout(() => countTo(num, card), delay + 300);
  });
  if (line) line.animate([{ strokeDashoffset: len }, { strokeDashoffset: 0 }],
    { duration: 1400, delay: 600, easing: 'cubic-bezier(0.25,1,0.5,1)', fill: 'forwards' });
}
```

接 §9 调度器时，卡片 stagger 与数字滚动的 setTimeout 改为 cue 时刻表；占位数据必须标"示意"（SKILL.md 硬约束 6）。

## 9. URL 参数控制：?seek / ?autoplay / ?speed

三个参数作用于**同一个演示时钟**：倍速改时钟流速（不改各动画 duration），seek 重放 cue 表并把 WAAPI 动画快进到终态。与既有参数分工：`#/N/M` 是页级/fragment 级深链（`presenter-mode.md` §5），`?seek` 是页内演示步级；`?preview=N`（演讲者预览）优先于 autoplay；`?noscale`（截图导出）并存不冲突。前提：所有演示动作触发即确定（§3 各式；⑦⑧的纯函数形态直接由 `clock.t` 驱动），`fired` 集合是唯一副作用，seek 时重置重放——与 `generative-art-and-canvas.md` state-proxy 模式一致。

```js
const params = new URLSearchParams(location.search);
const AUTOPLAY = params.get('autoplay') === '1' && params.get('preview') === null;
const SPEED = Math.min(4, Math.max(0.25, parseFloat(params.get('speed')) || 1));
const SEEK = params.get('seek');

const clock = { t: 0, playing: false, last: null, raf: 0 };
const CUES = [                                   // 演示步表：t 秒；步间隔 ≥1.5s（§5 铁律 2）
  { t: 0.0, run: () => playStep(0) },
  { t: 2.4, run: () => playStep(1) },
  { t: 5.0, run: () => playStep(2) },
  { t: 7.6, run: () => playDashboard(document.getElementById('dash')) }
];
let fired = new Set();

function demoTick(now) {
  if (clock.last === null) clock.last = now;
  clock.t += ((now - clock.last) / 1000) * SPEED;
  clock.last = now;
  for (let i = 0; i < CUES.length; i++) {
    if (!fired.has(i) && clock.t >= CUES[i].t) { fired.add(i); CUES[i].run(); }
  }
  document.getAnimations().forEach(a => { a.playbackRate = SPEED; });  // WAAPI 跟随倍速
  if (clock.playing) clock.raf = requestAnimationFrame(demoTick);
}
function demoPlay() { if (!clock.playing) { clock.playing = true; clock.last = null; clock.raf = requestAnimationFrame(demoTick); } }
function demoPause() { clock.playing = false; cancelAnimationFrame(clock.raf); clock.raf = 0; }
function demoSeek(n) {                           // ?seek=N：确定性快进到第 N 步终态
  demoPause();
  fired = new Set();
  clock.t = n < CUES.length ? CUES[n].t + 0.001 : CUES[CUES.length - 1].t + 3;
  CUES.forEach((cue, i) => { if (cue.t <= clock.t) { fired.add(i); cue.run(); } });
  document.getAnimations().forEach(a => {
    try { a.finish(); } catch (err) { /* iterations:Infinity 的动画无终态，跳过 */ }
  });
}
if (SEEK !== null) demoSeek(Math.max(0, parseInt(SEEK, 10) || 0));
else if (AUTOPLAY) document.fonts.ready.then(demoPlay);
window.__demo = { play: demoPlay, pause: demoPause, seek: demoSeek, clock };
```

headless 自检用法：`?seek=0/1/2…` 逐步截图核对每步终态；`?autoplay=1&speed=4` 快速回归整段时序；截图矩阵方法见 `interactive-html-authoring.md` headless 验证节。

## 10. iframe 三坑

### 坑一：跨域通信

- 成因：嵌第三方站点的 iframe 不同源，`contentDocument` 与脚本注入被同源策略禁止；`postMessage` 需对方页面配合监听，第三方站点不会配合。`file://` 下双方 origin 均为 `"null"`，无法用 `event.origin` 白名单校验（`presenter-mode.md` §3.3 的 file:// 降级是同源自有页面的同类实测）
- 规避：主演示不嵌第三方站点，走 §2 素材三件套本地重建；iframe 只嵌自有产物（同一文件或 `pages/` 相对路径）；消息校验分协议——http(s) 校验 `event.origin`，`file://` 校验 `event.source === iframe.contentWindow`

### 坑二：缩放失真

- 成因：浏览器按 iframe 的**布局尺寸**栅格化内容，scale-to-fit 壳的 `transform: scale()` 只放大位图——非整数倍率下文字发糊、hairline 变粗（与式⑥放大发糊同根因）
- 规避：iframe 的 width/height 固定写 1920×1080 设计画布尺寸，缩放施加在外层 wrapper 上（`presenter-mode.md` §3.2 预览卡即此结构）；显示尺寸优先取整数倍率（1x / 0.5x）；不对 iframe 用 CSS `zoom`（每帧 re-layout，跨浏览器行为不一致）

### 坑三：焦点抢占

- 成因：点击 iframe 内部后焦点进入 iframe 文档，键盘事件（←→ 翻页、S/O/N/F）全部落在 iframe 里，deck 快捷键失效，观众以为页面卡死
- 规避：iframe 加 `tabindex="-1"`；自有页面 iframe 内转发导航键给父窗口（下方代码）；第三方页面无法转发即不嵌（回到坑一结论）；父窗口监听 `blur` 兜底收回焦点

```js
// iframe 内（自有页面）：导航键转发给父窗口
addEventListener('keydown', e => {
  const NAV = ['ArrowLeft', 'ArrowRight', ' ', 'PageUp', 'PageDown', 'Home', 'End'];
  if (window.parent !== window && NAV.includes(e.key)) {
    e.preventDefault();
    window.parent.postMessage({ type: 'deck-key', key: e.key }, '*'); // file:// 下 origin 为 null 只能 '*'；消息不含敏感数据
  }
});
// 父窗口：只信自有 iframe 发来的按键，重派发进 deck 既有键盘处理
addEventListener('message', e => {
  const mine = [...document.querySelectorAll('iframe')].some(f => f.contentWindow === e.source);
  if (mine && e.data && e.data.type === 'deck-key') {
    document.dispatchEvent(new KeyboardEvent('keydown', { key: e.data.key, bubbles: true }));
  }
});
```

## 11. 自检清单

- [ ] 走了 §1 决策树？没有在"静态截图就够"的场景做演示页重建，没有把录屏 GIF 当主演示？
- [ ] 素材三件套采齐？截图来自真实系统（无手搓假 UI），切片动完归位槽位坐标？
- [ ] 每个 UI 动作绑定了一个讲解节拍（talk 条目或字幕）？无绑定的动作已删除？
- [ ] 同一时刻只有一个视觉焦点在动（公理二）？两式并发时其一已降为静态终态？
- [ ] 光标与正在发生的操作全程在画布可视区内（含 32-48px 安全边距）？
- [ ] 打字演示汉字 100-150ms/字、英文数字 40-70ms/字符？光标打字常亮、打完才闪？退格修正预写进事件表、无运行时随机？
- [ ] 两个演示动作间隔 ≥0.8s（含新信息 ≥1.5s）？每式之间 0.4-0.5s 呼吸帧？演示收尾 hold ≥1s 真静止、无尾漂？
- [ ] 数据流包速 linear 匀速、iterations 有限？滚动演示刹车点有目标行强调、滚动期间无推近？
- [ ] before/after 同布局同机位、before 是真实旧态？
- [ ] 画廊墙 render(t) 是 t 的纯函数：无 setTimeout 链、无状态机，`window.__seek(t)` 任意时刻可复现同一画面？
- [ ] 入场/涟漪/hover 三层 transform 分管（outer/body/inner），没有两个动画抢同一元素？
- [ ] 画廊与涟漪 rAF 随页启停（slidechange），离页 cancelAnimationFrame，Performance 面板无残留？画廊页计入持续型特效预算？
- [ ] 数字滚动有终止条件、结束 snap 精确值、`tabular-nums` 防抖？占位数据已标"示意"？
- [ ] `?seek=N` 确定性快进到第 N 步终态？`?speed` 作用于统一时钟与 playbackRate，未改各动画 duration？`?preview` 下 autoplay 不生效？
- [ ] iframe 只嵌自有产物？焦点转发或 blur 收回就位？iframe 本体 1920×1080、缩放施加在 wrapper 层？
- [ ] `prefers-reduced-motion` 下：演示直显终态、画廊静帧、涟漪不启动、光标闪烁动画停止？
- [ ] 动画属性仅 transform/opacity/filter（SVG dashoffset 属 path-draw 既有例外）？无 width/height/top/left 动画？
