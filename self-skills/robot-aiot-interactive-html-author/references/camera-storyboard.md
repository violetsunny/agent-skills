# 页面级运镜与分镜规划

## 定位

本文件管**页面级 / deck 级**运镜（推/拉/横移/升降/环绕）与分镜规划：运镜预算、动机绑定、时长公式、相机层结构、能量节奏、分镜卡与缩略图审查。画布基准 1920×1080，全部参数 px 锚定。

与相邻文件的分工（本文件不重复其内容）：

| 文件 | 管什么 | 与本文件的关系 |
|---|---|---|
| `keyframe-animation.md` | 元素级缓动、时长预算、转场样式与速度匹配、页间相机飞行、叠加冲突 | 运镜缓动与页过渡样式从其选型；§4 结构与其"相机飞行过渡"兼容 |
| `animation-fx-catalog.md` | 元素级入场动画与 canvas FX 目录、预算硬限 | 运镜是页面级、特效是元素级，两层预算独立计，不互相抵扣 |
| `web-slide-strategies.md` | 布局模式、叙事策略、明暗主题节奏 | §12 能量骨架与其主题节奏是两条独立线，各自校验 |
| `generative-art-and-canvas.md` | rAF / canvas 生命周期契约 | §8 视差循环、§9 派生驱动遵守其随页启停契约 |
| `presenter-mode.md` | O 键总览网格、自动翻页 | §14 thumbnail pass 的运行时快捷方式即总览网格 |

两条铁律贯穿全文：**运镜是预算制，不是特效制**——每次镜头运动都是一笔观众注意力消费，预算花完，再好的镜头也不拍；**无动机运镜一律删**——答不出"这一镜替观众回答了什么问题"就不动镜头。静止永远是合法且常常是最优的导演决定。

## 1. 运镜预算制

预算三级核算，动手写代码前逐项过：

| 预算项 | 上限 | 手感与依据 |
|---|---|---|
| 单页运镜次数 | ≤2 次（入场定位 1 + 页内强调 1） | 第 3 次必然与内容抢注意力 |
| 全 deck 运镜页占比 | ≤40% 总页数 | ≥60% 的页面静止；运镜页不得连续 >2 页 |
| "烈"档运镜（§5） | 全 deck ≤2 页 | 最强镜头只留一处，放收尾峰或中段叙事峰 |
| 同页相邻运镜间隔 | ≥2.5s | 低于 2.5s 观众没消化完上一镜 |
| 推进倍率 | 下限 1.25x，上限 2.4x | <1.25x 视觉变化感知不足、纯属晃动；首页定场微推 1.06x 是唯一例外（§6） |
| 景别档差 | 相邻页至少差一档（§11） | 同档连切读作"画面跳了一下"；两级跳必须配转场垫住 |

超预算处置（三选一，禁止压缩间隔硬凑）：

1. **砍**：删动机最弱的一镜，降级为元素级强调（高亮/标记，见 `animation-fx-catalog.md`）
2. **并**：两个近距离运镜合并为一镜，取联合包围盒按 §11 定景公式重算倍率
3. **降**：烈降缓、缓降静；运镜降级永远比升级安全

## 2. 运镜动机表

每种镜头运动必须绑定叙事情由，对表选型；无理由运镜 = 删：

| 镜头运动 | 叙事情由（替观众回答什么问题） | 参数区间 | 禁用场合 |
|---|---|---|---|
| 推进 push in | 深入细节："接下来看这里"——聚焦某个图表/数字/代码块 | 倍率 1.25-2.4x；时长走 §3 对数公式 | 无具象锚点不推；页面转场进行中不推；信息密集页不推 |
| 拉远 pull out | 建立全局："原来它属于一个更大的系统"；收束谢幕 | 回 1x 或远景 0.85x；时长走 §3 | 下一镜立即又推回时不拉（泵动感）；相邻运镜间隙 ≥1.5s 才允许"拉出再推进" |
| 横移 pan | 并列对比：一镜扫过多个并列元素（对比列/KPI 排/卡片墙） | 位移 ≤420px；时长走 §3 位移公式 | 起止焦点距离 <420px 并为一镜；>860px（画布宽 45%）弃镜改翻页 |
| 升降 tilt/crane | 层级递进：架构分层、组织结构、金字塔自下而上逐层走 | 位移 ≤300px；时长同横移公式 | 文字密集页不升降 |
| 环绕 orbit | 多维审视：单一主体的 3D 质感（产品模型/核心概念） | rotY ≤24°，1.2-1.8s，smooth-inout；全 deck ≤1 页 | 文字密集页禁用；一种手法全 deck 只当一次主角 |
| 静止 | 阅读、信息密集、预算不足时的默认答案 | — | 无。静止永远合法 |

两条横向纪律：

- **速度感来自加速度，不是匀速快**：匀速运镜读作廉价；要"快"用短促加速段 + 长缓冲（quart-out / expo-out，别名见 `animation-fx-catalog.md` §1b），不是把时长砍半
- **机位服务可读性**：信息密集页正视（不加 rotX/rotY）；文字确需 3D 质感时 rotY 主导 ≤8°、rotX 给最小值；禁止全页一刀切倾斜

## 3. 对数时长公式

所有推拉时长由倍率变化量决定，不拍脑袋：

```
duration = 0.55s × log2(zoomEnd / zoomStart)    取绝对值，clamp 到 [0.30, 1.50]s
```

倍率变化量相同则时长相同，任何幅度的推拉"视觉速度"一致：大景别过渡自然更久、小景别更短，防"一蹿到位"也防"拖沓"。拉远与推进对称（2x→1x 同样 0.55s）。

换算表（自 1x 起推）：

| 倍率比 | log2 值 | 时长 |
|---|---|---|
| 1.5x | 0.58 | 0.32s |
| 2x | 1.00 | 0.55s |
| 3x | 1.58 | 0.87s |
| 4x | 2.00 | 1.10s |
| 6x | 2.58 | 1.42s |

3x 及以上档位已超 §1 推进上限（2.4x），列出仅为公式换算完备；实际触顶先改页内布局与素材密度，不硬推。

代码实现（本文件唯一实现，其余节直接调用）：

```javascript
// 返回秒。任意起止倍率均有效，自动取绝对值并 clamp
function zoomDuration(zoomStart, zoomEnd) {
  const d = 0.55 * Math.log2(zoomEnd / zoomStart);
  return Math.min(1.5, Math.max(0.3, Math.abs(d)));
}
```

匀速位移类（横移/升降）不走对数公式，走位移/速度：

```javascript
// 位移 px → 秒，基准速度 600px/s，clamp [0.4, 1.4]s
function panDuration(distancePx, speed = 600) {
  return Math.min(1.4, Math.max(0.4, Math.abs(distancePx) / speed));
}
```

例外档：首页定场微推（1.06x）不按公式计时（公式给 0.05s，无感知意义），固定 2.5-3.0s 慢推（§6）。

## 4. 相机层容器结构

镜头运动和元素动画不许抢同一个 transform（叠加冲突规则见 `keyframe-animation.md`）。所有镜头级运动收口到专职三层容器：

> 规范副本：`templates/camera-layer.js` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```html
<div class="camera-stage">                    <!-- 视口层：固定 1920×1080，overflow hidden，不动 -->
  <div class="camera-layer">                  <!-- 相机层：只承载相机 transform，运镜全部收口在这 -->
    <div class="content">…页面内容…</div>      <!-- 内容层：页面内容住这里 -->
  </div>
  <div class="stage-hud">…页码/角标/比例尺…</div>  <!-- 与相机层平级，天然不跟镜头动 -->
</div>
```

```css
.camera-stage { position: relative; width: 1920px; height: 1080px; overflow: hidden; }
.camera-layer { position: absolute; inset: 0; transform-origin: 0 0; }
.content      { position: absolute; inset: 0; }
.stage-hud    { position: absolute; inset: 0; z-index: 10; pointer-events: none; }
```

三层职责与 transform 归属：

| 层 | 职责 | transform 归属 | 禁止 |
|---|---|---|---|
| `.camera-stage` | 固定视口；需要 3D 运镜时持有 `perspective`（1100-1200px） | 无 transform | 放任何内容 |
| `.camera-layer` | 运镜（推/拉/横移/升降/环绕）唯一承载层 | 只出现相机 transform | 挂元素动画；读写布局属性 |
| `.content` | 页面内容与元素级动画（入场/stagger/hover） | 元素自身 transform | 碰 `.camera-layer` 的 transform |

will-change 策略：只在运镜期间提升，不常驻——

1. 运镜开始前给 `.camera-layer` 设 `will-change: transform`，`finished` 后置回 `auto`
2. 禁止在 CSS 里常驻 will-change（常驻合成层有内存成本，与 `keyframe-animation.md` 性能红线一致）

相机定位与飞行（WAAPI，时长来自 §3，缓动 quart-out）：

```javascript
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
```

counter-transform 反向补偿：必须跟随 content 内某元素、但字号要恒定的标注/比例尺，做反向 `scale(1/zoom)`，与相机走同一条时间轴（同 duration 同 easing）即天然逐帧同步：

```javascript
function counterFly(el, fromZoom, toZoom, durationMs) {
  return el.animate(
    [{ transform: `scale(${1 / fromZoom})` }, { transform: `scale(${1 / toZoom})` }],
    { duration: durationMs, easing: 'cubic-bezier(0.22, 1, 0.36, 1)', fill: 'both' }
  );
}
```

chrome 首选放 `.stage-hud`（零成本静止）；counter-transform 只给"必须指向 content 内具体元素"的标注；`.stage-hud` 与 deck 全局 chrome 的叠字冲突见下方施工坑「全局 chrome 叠字」。

施工坑（镜头专属）：

- **横移露边**：位移 >0 时 `.content` 必须沿位移方向外扩 ≥ 位移量 + 32px；远景（<1x）时 `.content` 世界尺寸 ≥2400×1350（四周各扩 12.5%），否则拉远露出 `.camera-stage` 底色
- **perspective 被打断**：`.camera-layer` 与 `.content` 之间任何中间层加 `overflow: hidden`、`filter`、`opacity < 1` 都会杀掉 preserve-3d，3D 运镜瞬间变平；滤镜只加在最内层元素上
- **全局 chrome 叠字**：相机页自有 `.stage-hud`（页码/角标/比例尺）与 deck 全局 chrome（`#hint` 快捷键提示、`#pageNum` 页码）同坐标，两者同时可见即叠字；相机页用 `body:has(#sN.active) #hint, body:has(#sN.active) #pageNum { opacity: 0; }` 隐藏全局件，由 `.stage-hud` 独占接管。每个相机页各写一条 `:has` 规则；相机页内需要快捷键提示时自绘进 `.stage-hud`，不依赖全局件回归
- **与页间相机飞行的关系**：deck 采用 `keyframe-animation.md`"相机飞行过渡"（所有页在同一世界层）时，世界层即 deck 级相机层，本节结构是页内级；两级 transform 各归其层，页内运镜叠加在世界层飞行之上，互不抢写

## 5. 镜间三分律

晕和疲劳不是单镜造成的，是镜与镜之间的能量重复造成的。镜头能量分三档：

| 能量档 | 定义 | 例 |
|---|---|---|
| 静 | 无运镜，或只有入场定位 | 信息密集页、表格页、架构图页、自测页 |
| 缓 | 单次 ≤1.45x 慢推，或 ≤320px 慢速横移/升降 | 功能演示聚焦、并列对比 |
| 烈 | ≥1.8x 推进、环绕、>320px 快速横移、两级景别跳 | 关键数字揭示、全 deck 最强镜头 |

轮换规则：

1. 禁止连续三页同能量档：三连静读作"忘了加运镜"，三连缓催眠，两连烈晕
2. 烈不与烈相邻，两个烈页之间至少隔一个静页
3. 中段起伏（§12 ③）以 静/缓/烈 轮换为基准节奏；铺垫谷允许连续两页静（刻意减速），第三页必须换档
4. 自检法：把全 deck 能量序列写出来（如 缓-静-缓-静-烈-缓），扫一遍三连与烈烈相邻
5. 能量节奏与 `web-slide-strategies.md` 明暗主题节奏是两条独立线，分别校验；烈页恰逢 hero dark 页是加分项，不是硬要求

## 6. 开闭幕运镜

开场与闭幕各一镜，是全 deck 成本最低、作品感提升最明显的两处运镜。

**首页入场镜头（定场微推）**：deck 加载/进入第一页时，相机自 1.0x 缓推至 1.06x（2.8s，sine-inout）。观众第一感受是"画面是活的"，而不是"开始播放了"。纪律：

1. 首页只此一镜，不叠加其他运镜；可与入场编排（`animation-fx-catalog.md` §1c hero recipe）共存
2. 1.06x 是 §1 预算表唯一允许低于 1.25x 的例外档
3. 不走 §3 对数公式，固定 2.5-3.0s
4. reduced-motion 下直接静帧

```javascript
const layer = document.querySelector('.camera-layer');
if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
  layer.animate(
    [{ transform: 'translate(0px, 0px) scale(1)' },
     { transform: 'translate(-57.60px, -32.40px) scale(1.06)' }],  // 对准画布中心 (960, 540)
    { duration: 2800, easing: 'cubic-bezier(0.37, 0, 0.63, 1)', fill: 'both' }
  );
}
```

**末页退场镜头（谢幕）**：deck 必须以全景静止收尾。

1. 末页若有推进，结束前拉回 1x（时长走 §3）+ ≥0.8s 全景 hold；绝不在推近态戛然而止
2. 谢幕的决定感来自 hold，不来自淡出——禁止整页 opacity 渐弱当退场镜头
3. 可选变体：缓拉至 0.92x 露出画布留白（`.content` 须按 §4 外扩，否则不拉，停 1x）
4. 收尾页恒为演讲型大留白（见 `web-slide-strategies.md`），运镜只做"落定"，不做新焦点

## 7. 转场三层模型

一次页过渡不是一个动画，是三层各自转场、错峰启动：

| 层 | 内容 | 启动偏移 | 时长 | 说明 |
|---|---|---|---|---|
| 背景层 | 底色/纹理/氛围渐变 | 0ms | 400-500ms | 先动先到；用共享背景层（见 `interactive-html-authoring.md`）时本层不动，偏移归零 |
| 内容层 | 主体块（标题/卡片/图表） | 100-150ms | 400-450ms | 分块 stagger 与入场参数见 `keyframe-animation.md` 时长预算与编排护栏 |
| 焦点层 | 标注/强调标记/chrome | 300-350ms | 200-250ms | 最后到；它出现前观众视线已被内容层接住 |

纪律：

1. 三层禁止同起同收——同时动 = 整页平移，空间感全无；层间启动错峰 80-150ms
2. 转场总时长仍落在 `keyframe-animation.md` 页面过渡 400-600ms 预算内：三层模型是预算内的启动错峰，不是时长 ×3；焦点层超预算就并入内容层末拍 stagger
3. 转场样式选型（交叉淡化/硬切/甩镜/穿雾/穿越缩放/View Transition）与速度匹配参数归 `keyframe-animation.md`；本节只管一次转场内部的层间时序
4. 相机飞行模式的页面：三层都住在世界层里，飞行 transform 归世界层，三层只做 opacity/局部位移错峰，不与飞行抢 transform

## 8. parallax 视差

视差是页面级的持续微信号：同一驱动信号按层给出不同位移，层间速度差即深度感。元素级单卡 hover 倾斜（`parallax-tilt`）见 `animation-fx-catalog.md`，本节管页面级多层。

层参数：

| 层 | 位移系数 | 鼠标驱动振幅 | 滚动驱动振幅 | 内容例 |
|---|---|---|---|---|
| 远层 | 0.35 | 7px | 42px | 背景渐变/纹理/剪影 |
| 中层 | 0.7 | 14px | 84px | 主体卡片群/图表 |
| 近层 | 1.4 | 28px | 168px | 前景装饰块/大字标注 |

硬规则：

1. 相邻层速度比 ≥2 才可辨（0.35/0.7/1.4 相邻恰为 2 倍）；1.2 倍的差异观众读不出，纯浪费预算
2. 层数 ≤4，超过 4 层的视差不可辨
3. 所有层由同一驱动信号派生位移，禁止每层独立动画（独立 = 不同步，一眼假）
4. 视差是质感不是运镜：振幅锁在微位移级（鼠标驱动近层 ≤28px），不计入也不得挪用 §1 运镜预算

鼠标驱动（rAF + 指数平滑；循环随页启停，契约见 `generative-art-and-canvas.md`）：

> 规范副本：`templates/parallax.js` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```javascript
function mountParallax(stage, layers, amp = 20) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return () => {};
  let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0;
  const onMove = (e) => {
    const r = stage.getBoundingClientRect();
    tx = ((e.clientX - r.left) / r.width - 0.5) * 2;      // 归一化到 [-1, 1]
    ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
  };
  const loop = () => {
    cx += (tx - cx) * 0.1;                                 // 指数平滑：跟得紧但不抖
    cy += (ty - cy) * 0.1;
    for (const L of layers) {
      L.el.style.transform = `translate3d(${(-cx * amp * L.k).toFixed(2)}px, ${(-cy * amp * L.k).toFixed(2)}px, 0)`;
    }
    raf = requestAnimationFrame(loop);
  };
  stage.addEventListener('pointermove', onMove);
  raf = requestAnimationFrame(loop);
  return () => {                                           // 离开页面时调用（生命周期契约）
    cancelAnimationFrame(raf);
    stage.removeEventListener('pointermove', onMove);
    for (const L of layers) L.el.style.transform = 'none';
  };
}

const dispose = mountParallax(document.querySelector('.camera-stage'), [
  { el: document.querySelector('.px-far'),  k: 0.35 },
  { el: document.querySelector('.px-mid'),  k: 0.7  },
  { el: document.querySelector('.px-near'), k: 1.4  }
]);
```

滚动驱动（仅长页滚动叙事形态；deck 内 1920×1080 画布无滚动条，见 SKILL.md 硬约束 1）：

```javascript
function scrollParallax(layers) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const doc = document.scrollingElement;
  addEventListener('scroll', () => {
    const p = doc.scrollTop / (doc.scrollHeight - innerHeight);   // [0, 1]
    for (const L of layers) {
      L.el.style.transform = `translate3d(0, ${(-p * 120 * L.k).toFixed(2)}px, 0)`;
    }
  }, { passive: true });
}
```

reduced-motion 降级：两种驱动都在挂载入口检测，命中即不挂监听、不起循环，各层保持零位移静帧（SKILL.md 硬约束 12）。

## 9. 派生信号

镜头参数必须是**进度的纯函数**派生，不是事件回调里的增量修改：`f(p) → { cx, cy, zoom }`。任意进度 p 都能一帧重算出相机参数——翻回页面、`#/N/M` 深链直达、总览网格点选都直接落到正确状态，不需要"把动画播一遍才能到那个状态"。与 `keyframe-animation.md` 闭式弹簧"进度纯函数"是同一确定性要求。

三种派生源：

| 派生源 | 进度定义 | 适用形态 |
|---|---|---|
| fragment 步序 | p = 当前步 / 总步数 | 页内分步揭示（deck 默认形态） |
| 滚动进度 | p = scrollTop / (scrollHeight − 视口高) | 长页滚动叙事 |
| 播放时间 | p = elapsed / duration | 自动播放模式（见 `presenter-mode.md`） |

步序 → 相机关键帧（§13 分镜卡的镜头列即此表数据源）：

```javascript
const SHOTS = [
  { cx: 960,  cy: 540, zoom: 1.0  },   // step 0：全景基准面
  { cx: 620,  cy: 400, zoom: 1.45 },   // step 1：中景推近接入层
  { cx: 1380, cy: 700, zoom: 1.8  },   // step 2：近景聚焦告警卡片
  { cx: 960,  cy: 540, zoom: 1.0  }    // step 3：拉回全景谢幕
];

// 纯函数：给目标步，返回起止相机与时长；无状态，任意时刻可重算
function shotAt(step) {
  const i = Math.max(0, Math.min(SHOTS.length - 1, step));
  const from = SHOTS[Math.max(0, i - 1)];
  const to = SHOTS[i];
  const duration = from === to ? 0 : zoomDuration(from.zoom, to.zoom);
  return { from, to, duration };
}
```

从速度派生次级信号（"镜头感"的来源，不靠更快的 duration）：

```javascript
// 中央差分求 zoom 速度，blur 强度 ∝ 速度；只在运动瞬态模糊，静止帧永远锐利
function motionBlurPx(zoomFn, p, dp = 0.02) {
  const v = Math.abs(zoomFn(p + dp) - zoomFn(p - dp)) / (2 * dp);
  return v > 0.6 ? Math.min(10, (v - 0.6) * 5) : 0;   // 阈值 0.6 与系数 5 按手感校准
}
```

纪律：

1. 派生 blur 只出现在运镜瞬态；静止帧带 blur = 脏
2. 派生信号在 reduced-motion 下一律输出 0
3. 运镜焦点必须来自分镜卡关键帧表，禁止用鼠标位置派生相机焦点（鼠标只驱动 §8 视差微位移）

## 10. 定格帧十一律

每页在加运镜之前，先按十一律检查它的静态定格帧——构图不成立，运镜救不了：

1. **焦点唯一**：每页定格帧只有一个视觉焦点；说不出观众第一眼看哪，构图不成立
2. **三分定位**：主体落画布三分线（竖线 640px / 1280px，横线 360px / 720px）或交点上；居中构图只给仪式页（封面/章节页/收尾页）
3. **引导线唯一**：每页只有一条引导线（箭头/视线/块边缘/光带）且指向焦点；引导线方向 = 该页镜头运动方向（与 §2 动机表互检）
4. **负空间 ≥30%**：负空间不是空，是呼吸和下一步的落点；文字落负空间，不压主体
5. **视觉重量平衡**：深色/大面积/高饱和重，浅色/小面积/低饱和轻；失衡用负空间或次级元素配平，不靠加装饰
6. **活跃元素 ≤3**：任一定格帧内活跃元素（高对比/运动中/大面积）≤3；新元素入场，旧元素必须退场（blur/dim/移出）
7. **前中后景分层**：显式写出三层各是什么、谁遮挡谁；这个分层就是 §8 视差的素材，说不出即未分层
8. **accent 单区**：强调色每页只出现在一个焦点区；accent 满页 = 没有焦点（与 `design-system-standards.md` 一致）
9. **网格对齐**：主体边缘对齐版式网格线（见 `swiss-layout-system.md`）；斜向/自由排布只给明确要动感的页
10. **缩小可读**：定格帧缩到 160×90（§14）时最大的词仍可辨；不因"反正会动"缩小字号——动的画面每帧分到的注意力比静图更少，字号只能更大
11. **封面测试**：随机暂停任一页任一帧，该帧能直接当封面用；过不了的帧说明这页只是元素堆叠，没有构图

## 11. 景别五档

远/全/中/近/特五档在 1920×1080 画布上的 px 级定义（可视世界范围 = 1920/zoom × 1080/zoom）：

| 景别 | zoom 档位 | 可视世界范围 | 观众看到什么 | 适用页型 |
|---|---|---|---|---|
| 远景 | 0.8-0.85x | 2400×1350 至 2259×1271 | 整页 + 四周留白 | 开场定场、收尾全家福、总览/议程页 |
| 全景 | 1.0x | 1920×1080 | 完整单页布局 | 叙事基准面：问题陈述、解决方案、对比分析及多数正文页 |
| 中景 | 1.3-1.45x | 1477×831 至 1324×745 | 一个功能区块/一组卡片 | Feature Grid 单区、流程图画一段、图表单列 |
| 近景 | 1.6-1.8x | 1200×675 至 1067×600 | 单个组件/单条数据 | 看板单 KPI、Timeline 单节点、单步交互 |
| 特写 | 2.0-2.4x | 960×540 至 800×450 | 单个数字/按钮/代码行/logo | Big Number 关键数字、锚点细节揭示 |

景别节奏规则：

1. 相邻页同档不连切——至少差一档，否则翻页读作"画面跳了一下"而不是"换镜头了"
2. 两级跳（全景→近景、中景→特写）必须是有意强调，且配速度匹配转场垫住（见 `keyframe-animation.md`）
3. 推进终点必须是具象锚点（那个数字/那张卡片/那行代码）；背景纹理、氛围渐变、装饰图形不配推进
4. 档位是设计词汇不是枷锁：1.5x、2.2x 都合法，档位的作用是让"中景""特写"在分镜卡里有确定数值含义

定景公式（拿不准档位时算）：

```
zoom = 0.8 / max(目标包围盒宽 / 1920, 目标包围盒高 / 1080)    再夹到本表档位区间
```

目标占可视区 80%，留 20% 呼吸，不顶格。例：目标卡片 960×540，归一化 0.5/0.5，zoom = 1.6 → 近景档。

## 12. 能量骨架

全 deck 镜头能量不平均分配，按四段位规划：

| 段位 | 页数占比 | 能量 | 运镜策略 |
|---|---|---|---|
| ① 开场峰 | 前 1-2 页（8-12%） | 高印象、低运动 | 首页定场微推（§6）+ 入场编排；开场峰的"峰"是视觉印象不是运镜强度，页内不加运镜 |
| ② 铺垫谷 | 12-15% | 低，全 deck 最慢 | 整段静或仅缓；给观众进入叙事的时间，本段页面信息密度最高 |
| ③ 中段起伏 | 55-65% | 中高 ⇄ 低交替 | 每次运镜绑一个叙事情由，烈/缓交替（§5）；章节页是天然呼吸点，每 1 个烈页后插 1 个静页 |
| ④ 收尾峰 | 末 13-16% | 全 deck 峰值 | 倒数第二页允许全 deck 最强镜头（唯一环绕页/最深推进）；末页谢幕回全景静止 hold ≥0.8s（§6） |

排片纪律：**先划走静止预算，再排运镜**：

1. 标出必须静止的页：信息密集页、表格页、架构图页、自测页（见 `web-slide-strategies.md` 教学场景）
2. 标出全 deck 最强镜头：只有一处，放收尾峰或中段最重要叙事点
3. 剩余页按 §5 三分律排 缓/烈 交替
4. 排完逐页校验：四段位齐全、无"全程缓"（无峰 = 无记忆点）、无烈烈相邻

## 13. 分镜卡 8 字段模板

deck 级运镜规划落成一张分镜卡表，每页一行、八字段一个不能少；先填表再写代码：

| 页码 | 景别 | 镜头运动 | 时长 | 动机 | 能量级 | 转场 | 备注 |

字段写法要求：

- **页码**：从 1 起；含 fragment 分步的页用 `页.步` 记法（如 3.2 = 第 3 页第 2 步），每步一行
- **景别**：§11 五档之一 + zoom 数值
- **镜头运动**：动词（推/拉/横移/升/降/环绕/静止）+ 起止倍率或位移 px；"静止"也要写，并写为什么静止
- **时长**：§3 公式的计算结果，写数值不写"快/慢"
- **动机**：一句话，对照 §2 动机表；写不出就删运镜
- **能量级**：静/缓/烈 之一（§5）
- **转场**：`keyframe-animation.md` 转场样式选型，不许留空、不许写"默认"
- **备注**：counter-transform 元素、视差层分配、reduced-motion 降级行为、锚点说明

示例（6 页设备管理平台汇报 deck）：

| 页码 | 景别 | 镜头运动 | 时长 | 动机 | 能量级 | 转场 | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | 全景 1.0→1.06x | 定场微推 | 2.8s（例外档） | 开场仪式：让观众感到画面是活的 | 缓 | —（首页） | hero recipe 入场；reduced-motion 直接静帧 |
| 2 | 全景 1.0x | 静止 | — | 表格信息密集，阅读优先 | 静 | 交叉淡化 0.4s | 无运镜无视差 |
| 3 | 全景→中景 1.0→1.45x | 推进 | 0.30s | 深入细节：接入层是本页主角 | 缓 | 相机飞行 | 锚点=接入模块卡片；页码走 .stage-hud |
| 4 | 全景 1.0x | 静止 | — | 看板数字多，给观众读的时间 | 静 | 交叉淡化 0.4s | KPI 入场走 count-scale（见 animation-fx-catalog.md） |
| 5 | 全景→近景 1.0→1.8x | 推进 | 0.47s | 深入细节：全 deck 唯一关键结论数字 | 烈 | 穿越缩放 | 锚点=99.2% 在线率数字；推进前悬停 0.5s（见 keyframe-animation.md） |
| 6 | 全景 1.0x | 静止（谢幕 hold） | hold ≥0.8s | 谢幕：全景收尾，决定感来自 hold | 静 | —（末页） | 收尾页恒演讲型（见 web-slide-strategies.md） |

能量序列 缓-静-缓-静-烈-静：无三连、烈不邻烈，过 §5 校验；页 5 是全 deck 唯一烈页且位于倒数第二页（收尾峰），符合 §12。

## 14. thumbnail pass

分镜卡是文字，thumbnail pass 把它变成看得见的节奏验证：全部页缩到 160×90（1/12）按 deck 页序并排，一眼看全 deck。

看三件事：

1. **能量节奏**：烈/缓/静分布与 §12 四段位是否一致；有没有烈页连片、有没有整排全缓（无峰 = 无记忆点）
2. **视觉重复**：先盖住文字标签，相邻页构图差异还看不看得出来；看不出 = 版式模板没轮换，回 `swiss-layout-system.md` 换版式或 `web-slide-strategies.md` 调主题节奏
3. **单帧纪律**：每张缩略图过 §10 律六（活跃元素 ≤3）与律十（160×90 下最大的词可辨）

时机两次：分镜卡完成后跑一次（验规划，可用灰盒色块代替真实内容）；交付前再跑一次（验成品）。

运行时快捷方式：单文件 deck 的总览网格（O 键，见 `presenter-mode.md`）就是内建 thumbnail pass，交付前直接在总览态逐页目检。

构建期并排表（审查工具，不进交付物；多页形态用 iframe 引用各页文件，单文件形态把各 section 克隆进 .thumb）：

```html
<style>
  .contact-sheet { display: flex; flex-wrap: wrap; gap: 8px; padding: 16px; background: #808080; }
  .contact-sheet .thumb { width: 160px; height: 90px; overflow: hidden; position: relative; }
  .contact-sheet .thumb iframe {
    width: 1920px; height: 1080px; border: 0;
    transform: scale(0.0833333);            /* 160 / 1920 = 1/12 */
    transform-origin: 0 0;
  }
</style>
<div class="contact-sheet">
  <div class="thumb"><iframe src="pages/p1.html" scrolling="no" tabindex="-1" loading="lazy"></iframe></div>
  <div class="thumb"><iframe src="pages/p2.html" scrolling="no" tabindex="-1" loading="lazy"></iframe></div>
</div>
```

批量截图走 headless 浏览器（方法论见 `interactive-html-authoring.md` headless 验证），产出并排表图片存档目检。

## 15. 自检清单（交付前逐项核对）

- [ ] 1. 每个运镜都答得出"替观众回答了什么问题"？答不出的删了？
- [ ] 2. 单页运镜 ≤2 次、全 deck 运镜页 ≤40% 总页数、烈档 ≤2 页？
- [ ] 3. 没有 <1.25x 的 zoom（首页 1.06x 定场微推除外）？没有超 2.4x 上限的推进？
- [ ] 4. 推拉时长全走 §3 对数公式、横移/升降走位移公式，没有拍脑袋的固定 duration？
- [ ] 5. 相邻三页能量档无三连、烈不邻烈（§5）？
- [ ] 6. 首页定场微推是首页唯一镜头？末页以全景静止 hold ≥0.8s 收尾、不在推近态结束（§6）？
- [ ] 7. 转场三层（背景/内容/焦点）错峰 80-150ms、不同起同收，总时长在页面过渡预算内（§7）？
- [ ] 8. 视差层数 ≤4、相邻层速比 ≥2、所有层同一驱动信号（§8）？
- [ ] 9. 视差 rAF 循环随页启停，离页 cancelAnimationFrame、无残留监听（§8）？
- [ ] 10. 相机参数是进度纯函数，深链直达/翻回页面可一帧重算（§9）？
- [ ] 11. 派生 blur 只在运动瞬态，静止帧全部锐利（§9）？
- [ ] 12. 运镜全部收口在 .camera-layer，没和元素动画抢同一个 transform；will-change 运镜前加、结束后移除（§4）？
- [ ] 13. counter-transform 元素与相机同时间轴、字号恒定；横移与远景页 .content 外扩足够、全程无露边；相机页全局 #hint/#pageNum 已隐藏、.stage-hud 无叠字（§4）？
- [ ] 14. reduced-motion 下运镜/视差/派生信号全部降级为即时定位与静帧？
- [ ] 15. thumbnail pass 已执行：能量节奏与 §12 骨架一致、相邻页构图不重复、每帧 160×90 可读（§14）？
