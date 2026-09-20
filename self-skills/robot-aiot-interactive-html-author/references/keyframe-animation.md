# 关键帧动画与动效接缝规则

## 定位

为 Web 演示提供专业级动画编排能力，确保动效流畅、有节奏、不干扰内容阅读。

## 关键帧动画系统

### 核心概念

- **Keyframe**：定义动画起止状态和中间节点
- **Seam**：多个动画元素之间的时序衔接点
- **Orchestration**：全局动画编排，控制节奏和层次

### 接缝门控（Seam Gate）

动画元素之间的衔接必须通过接缝检查：

1. **时序对齐**：前一个元素的结束帧与后一个元素的起始帧时间差 ≤ 50ms
2. **属性连续**：衔接点的 transform/opacity 值不得跳变
3. **缓动一致**：同一组关联动画使用相同缓动函数
4. **层级正确**：z-index 在过渡期间不发生闪烁

### 缓动函数选择

速查表：

| 场景 | 推荐缓动 | CSS值 |
|------|---------|-------|
| 入场 | ease-out | `cubic-bezier(0, 0, 0.2, 1)` |
| 退场 | ease-in | `cubic-bezier(0.4, 0, 1, 1)` |
| 强调 | ease-in-out | `cubic-bezier(0.4, 0, 0.2, 1)` |
| 弹性 | 闭式弹簧（见下） | `linear()` 采样或 rAF 驱动 |
| 数据变化 | linear | `linear` |

#### 缓动族性格表

| 族 | 性格 | 典型用途 |
|----|------|---------|
| 幂次（quad/cubic/quart） | 温和→激进 | 通用主力；cubic-out 是默认工马，quart-out 用于戏剧性收束 |
| 正弦 sine | 平滑有机无硬角 | 环境漂浮、呼吸、Ken Burns、一切循环动效；inOut 用于往返 |
| 指数 expo | 极端加速度 | 高级感揭示、戏剧性入场 |
| 圆弧 circ | 极快起、极缓收 | 相机移动、轨道运动、场景转换 |
| 阶梯 steps(N) | 离散跳变无插值 | 打字机、光标闪烁、计数器跳动、复古数字感 |
| 过冲 back(N) | 越过目标再回落，N 控过冲量 | 仅俏皮语域，永不做默认；N ≤ 2，优先用闭式弹簧替代 |
| 弹性 elastic | 弹簧震荡 | 同上，仅俏皮语域 |
| 弹跳 bounce | 球体落地弹跳 | 仅物理喜剧语域（真实掉落物） |

**方向语义（不可选）**：入场用 `.out`（快起缓收，响应感）；退场用 `.in`（慢起加速甩出）；位置移动用 `.inOut`。最常见错误就是装反：入场用 in 显得迟钝，出场用 out 显得不情愿。

#### 双档时长与缓动（productive / expressive）

短促状态变化与大位移入场是两档事，分档给参数：

| 档 | 时长 | 本库缓动 | 用途 |
|----|------|---------|------|
| productive | 120-240ms | ease-out `cubic-bezier(0,0,0.2,1)`（上方速查表入场档） | chrome/元信息淡入、位置对齐、小强调 |
| expressive | 400-700ms | cubic-out 或 quart-out（animation-fx-catalog.md §1b） | 大标题入场、整块升起、hero 页序列 |

差异裁决（以本文件既有规则为准）：

1. productive 档参考曲线 `cubic-bezier(.2,0,.38,.9)` 起步带加速，违反"入场用 .out"方向语义——本库入场类一律不用；仅在非入场的对称短位移（如双栏镜像归位）可选用
2. expressive 档参考入场曲线 `cubic-bezier(0,0,.3,1)` 与本库入场 ease-out `(0,0,0.2,1)` 仅末段控制点不同（.3 vs .2，减速略更缓），不引入这第三条曲线；需要更长尾直接升档 cubic-out `(0.25,1,0.5,1)`
3. 时长档对齐下方预算表：productive ≈ 微交互 100-200ms 档（上限放宽到 240ms），expressive 落在元素入场 300-500ms 与页面过渡 400-600ms 档；编排序列总时长 ≤ 2000ms 约束不变

**平滑胜过弹跳**：默认入场是 cubic-out 或临界阻尼弹簧。过冲族（back/elastic/bounce）是"语域"不是调味品——需要变化时在平滑族内部换能量档（sine → 幂次 → expo），不要伸手拿弹跳。一种缓动用到底显平，弹跳用满屏显廉价，后者更糟。

**情绪映射**：sine/quad = 沉静冥想；quart-out/expo-out = 干脆自信；back-out = 弹跳物理感（仅明确俏皮的页面）。缓动是副词：同一个滑入，expo-out = 自信，sine-inOut = 梦幻，elastic-out = 顽皮。

**速度传达重量**：

| 时长 | 传达 |
|------|------|
| 0.15-0.3s | 能量、紧迫、自信 |
| 0.3-0.5s | 专业，大多数内容 |
| 0.5-0.8s | 重力、奢华、沉思 |
| 0.8-2.0s | 电影感、情绪、氛围 |

#### 闭式阻尼弹簧（springEase）

"系统级质感"是阻尼弹簧的速度曲线：快速发射 + 长渐近安定，不是弹跳。闭式解是进度的纯函数——无状态、不逐帧积分、可任意跳转回退，天然确定性。实时弹簧积分器（速度逐帧累积）禁止用于编排动画，因为无法直接跳到任意时刻。

> 规范副本：`templates/easing.js` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```javascript
// response ≈ 一次振荡的周期秒数（入场用 0.3-0.6）
// dampingFraction 1.0    = 临界阻尼，无过冲（默认）
//                 0.80-0.85 ≈ 系统级质感，过冲 ~1-1.5%，能感觉到但看不出来
//                 0.60-0.70 = 俏皮语域，过冲 ~5-10%（少用）
function springEase({ response = 0.5, dampingFraction = 1 } = {}) {
  const w = (2 * Math.PI) / response;
  const z = dampingFraction;
  let pos;
  if (z < 1) {
    const wd = w * Math.sqrt(1 - z * z);
    pos = (t) => 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t));
  } else if (z > 1) {
    const wo = w * Math.sqrt(z * z - 1);
    pos = (t) => 1 - Math.exp(-z * w * t) * (Math.cosh(wo * t) + ((z * w) / wo) * Math.sinh(wo * t));
  } else {
    pos = (t) => 1 - Math.exp(-w * t) * (1 + w * t);
  }
  const EPS = 0.001;
  const rate = z <= 1 ? z * w : (z - Math.sqrt(z * z - 1)) * w;
  const SCAN = 12 / rate;
  const N = 4800;
  let T = SCAN;
  for (let i = N; i >= 0; i--) {
    const t = (i / N) * SCAN;
    if (Math.abs(1 - pos(t)) > EPS) { T = ((i + 1) / N) * SCAN; break; }
  }
  const xT = pos(T);
  return { duration: T, ease: (p) => pos(p * T) + p * (1 - xT) };
}
```

**duration 和 ease 都从返回值取**——安定时间就是物理的一部分；改 duration 只是给同一条曲线重新计时，调快慢应调 response。

落地两条路（WAAPI/CSS 不接受任意函数）：

```javascript
// 路线1：采样成 CSS linear() 缓动串（Chrome 113+），可直接用于 transition/WAAPI
function sampleToLinear(ease, n = 32) {
  const pts = [];
  for (let i = 0; i <= n; i++) pts.push(`${ease(i / n).toFixed(4)} ${((i / n) * 100).toFixed(2)}%`);
  return `linear(${pts.join(', ')})`;
}

// 路线2：rAF 驱动，每帧算 ease(p) 写 transform——DOM 与 canvas 通用，无兼容性问题
```

参数选择：

| dampingFraction | 过冲 | 语域 |
|-----------------|------|------|
| 1.0（默认） | 无（单调） | 商务/汇报的标准安定 |
| 0.80-0.85 | ~1-1.5% | "活而不跳"，系统级质感 |
| 0.60-0.70 | ~5-10% | 明确俏皮专用 |
| < 0.55 | > 12% | 禁止，卡通抖动区 |

| response | duration (ζ=1) | 手感 |
|----------|----------------|------|
| 0.25-0.35 | 0.37-0.51s | 紧凑脆响——chip、小组件 |
| 0.35-0.50 | 0.51-0.74s | 标准入场 |
| 0.50-0.70 | 0.74-1.03s | 有重量的英雄落地 |

工艺要点：
- ζ=1 与 cubic-out 的差异：弹簧前段更猛（1/4 时刻走完 ~67% vs ~58%），渐近长尾更长——长尾就是"高级感"来源，安定时刻本身是焦点时用（标识落定、最终组合锁定）
- ζ<1 时过冲曲线只能上 transform，禁止上 opacity（会冲破 1）和颜色；opacity 拆到同一起点的独立 quad-out 轨
- 物理参数→过冲量经验公式：过冲比 ≈ `(stiffness / damping²) × 1.4`（如 damping 12 / stiffness 100 ≈ 过冲参数 1.4，时长 ~0.7s；公式粗糙，以视觉调准）

#### 过冲/弹跳/弹性闭式公式（rAF 与 canvas 共用）

```javascript
function backOut(t, s = 1.70158) { return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); }
function elasticOut(t) {
  if (t === 0 || t === 1) return t;
  return Math.pow(2, -10 * t) * Math.sin((t - 0.075) * (2 * Math.PI) / 0.3) + 1;
}
function bounceOut(t) {
  if (t < 1 / 2.75) return 7.5625 * t * t;
  if (t < 2 / 2.75) return 7.5625 * (t -= 1.5 / 2.75) * t + 0.75;
  if (t < 2.5 / 2.75) return 7.5625 * (t -= 2.25 / 2.75) * t + 0.9375;
  return 7.5625 * (t -= 2.625 / 2.75) * t + 0.984375;
}
```

in 变体 = `1 - out(1 - t)`；inOut 变体 = 前半 `out(2t) / 2`、后半 `out(2t - 1) / 2 + 0.5`。缓动函数以本节为唯一实现，其他文件只留指针不复制代码；canvas 粒子物理（挤压拉伸/弧线弹道）见 generative-art-and-canvas.md。

## 编排与节奏

### 编排护栏（七条）

1. **不要全场同缓动**：一页内相同缓动的独立动画 ≤ 2 个；像换字重一样换缓动
2. **不要全场同速**：最慢页 = 最快页 × 3，时长差是刻意设计出来的
3. **不要全员同方向入场**：默认坏习惯是每个元素都 `y:30px + opacity:0`；换用左/右/缩放/纯透明度/字距收拢
4. **不要复用 stagger 节奏**：每页有自己的节奏
5. **不要页页加环境动效**：慢速平移/微旋转/ scale 推进/颜色漂移/完全静止，每页选一种；运动之后的静止有力量
6. **不要从 t=0 开始**：首个动画偏移 0.1-0.3s，零延迟像跳切
7. **stagger 起步偏移总量 < 500ms**（不论元素多少）；整组含动画本体的总时长仍受下方预算表约束（≤ 2000ms）

### 页面节奏：build / breathe / resolve

每页停留时间分三段：

- **Build（0-30%）**：元素 stagger 入场，不要一次全倒出来
- **Breathe（30-70%）**：内容完整可见，只保留一种环境动效
- **Resolve（70-100%）**：退场或决定性收束；出场比入场快

入出场不对称：卡片入场 0.4s、出场 0.25s。

### 编排即层级

先动的元素被感知为最重要——按重要性排 stagger，不按 DOM 顺序。不要等上一个完全结束再动下一个，入场要重叠。

### 转场语义与节奏预设

转场是语义：交叉淡化 = "此段延续"；硬切 = "打断/醒醒"；慢溶解 = "随我漂移"。不要什么都交叉淡化。

时长预设：instant 0.15s / snappy 0.2s / smooth 0.4s / dramatic 0.5s / gentle 0.6s / luxe 0.7s。

节奏声明法：写代码前先给整个 deck 命名节奏模式（如 fast-fast-SLOW-fast-大效果-hold），从内容与受众推导，不套模板。

## 动效分层与时长预算

### 动效分层

1. **结构性动效**：页面切换、布局变化（必须有）
2. **反馈性动效**：hover/click 响应（可选）
3. **装饰性动效**：纯视觉增强（谨慎使用）

### 时长预算

| 类型 | 时长范围 | 说明 |
|------|---------|------|
| 微交互 | 100-200ms | hover/focus/press |
| 元素入场 | 300-500ms | 单个元素淡入/滑入 |
| 页面过渡 | 400-600ms | 整页切换 |
| 数据动效 | 800-1500ms | 数字滚动/图表绘制 |
| 编排序列 | ≤ 2000ms | 一组元素依次入场总时长 |

### prefers-reduced-motion

检测到 `prefers-reduced-motion: reduce` 时：
- 所有过渡降级为即时切换（duration: 0）
- 保留状态变化，移除运动
- 数据动效直接显示最终值

## 速度匹配转场

原则：出场页用加速缓动（`.in` 族）+ 模糊坡道离开，入场页用减速缓动（`.out` 族）+ 去模糊进入；两条速度曲线的最快点在切换点相遇，观众感知为连续相机运动而非两段动画。出场末速与入场初速匹配到 ~5% 容差内。

快选参数（原生 WAAPI/CSS 值）：

| 模式 | 出场 | 入场 |
|------|------|------|
| 甩镜 whip pan | `x→-400px, blur→24px`，0.3s `cubic-bezier(0.7, 0, 0.84, 0)` | `x:400px→0, blur:24px→0`，0.3s `cubic-bezier(0.16, 1, 0.3, 1)` |
| 穿雾 blur through | `blur→20px`，0.3s | `blur:20px→0`，0.25s cubic-out |
| 穿越缩放 zoom through | `scale:1→1.2, blur→20px`，0.2s cubic-in | `scale:0.75→1, blur:20px→0`，0.5s `cubic-bezier(0.16, 1, 0.3, 1)` |
| 上冲速度匹配 | `y→-150px, blur→30px`，0.33s cubic-in | `y:150px→0, blur:30px→0`，1.0s cubic-out |

转场三选一：

- **全屏大效果**（View Transition / WebGL shader 类）：揭示、logo 亮相、能量切换、"哇"时刻；每 deck 1-2 处足够（英雄揭示 + 结尾），多了冲淡冲击
- **CSS 交叉淡化**：连接性页面、连续相机运动、极简编辑节奏
- **硬切**：快闪列表、打击乐节奏、3+ 连续快速切换、任何 0.3-0.8s 转场会显慢的场合

## 相机飞行过渡（连续空间模式）

与 View Transition 并列的另一种切页模式：所有页面放在同一"世界层"上，切页 = 移动相机（对世界层做 translate+scale），产生连续空间感。

```javascript
function flyCamera(world, x, y, scale, animate = true) {
  world.classList.toggle('camera-static', !animate);
  world.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
}
```

规则：

- 参数：760ms `cubic-bezier(0.22, 1, 0.36, 1)`，transition 挂在世界层
- 跳变检测：相邻切页才飞；跨页跳转（总览网格点选、深链直达）或距上次移动 > 1.2s 时静态定位——`.camera-static` 临时禁 transition，定位完成后移除
- 单向连续：相机保持单向运动避免中途折返；页面沿一条直线或缓曲线排布
- 一个 deck 只选相机飞行或 View Transition 之一，不混用

## 相机 Rig 内的元素级接口

相机三层容器（`.camera-stage` > `.camera-layer` > `.content`）、对数时长公式与运镜预算见 camera-storyboard.md §1-§4；本节只定元素入场/退场动画在 rig 内的 keyframe 层契约，不复制运镜参数。

### 入场/退场与相机并发契约

1. 元素入场/退场/stagger/hover 动画只写在 `.content` 内部的元素上，相机 transform 只归 `.camera-layer`——两层互不知晓，相机可随时整体重排而不碰元素动画（层职责与 transform 归属表见 camera-storyboard.md §4）
2. 元素的关键动作与运镜配合时：相机在动作开始前约 0.15s 进镜（镜头先到、动作后发生），动作落定后停留 ≥1.2s 再走下一镜；时长 <1.2s 的孤立小动作不值得单独给运镜，降级为元素级强调
3. 运镜进行中的元素入场照常走本文件"时长预算"表，不因相机在动而额外放慢；但元素大位移入场不与"烈"档运镜同刻启动——两层预算独立计，消费的却是同一批观众（能量档与预算见 camera-storyboard.md §1、§5）
4. 相机需要跟随 rig 内运动元素时做逐帧越界兜底：每帧检查跟随目标是否越出可视区，越出则保持倍率、只沿越界轴做最小修正拉回边界——宁可镜头"让一步"，不许目标出画

### counter-transform（反向变换抵消父级相机变换）

必须跟随 `.content` 内某元素、又要字号恒定的标注/比例尺，做反向 `scale(1/zoom)` 抵消相机放大，与相机走同一条时间轴（同 duration 同 easing）即逐帧同步（WAAPI 实现见 camera-storyboard.md §4 counterFly）。元素级 keyframe 契约：

1. counter-transform 元素自身的入场/退场动画写在它的**子元素**上：外层专职 `scale(1/zoom)`，内层管入场 transform，一层一个 transform——与下方"叠加冲突（承重规则）"的父子两层解法是同一拆法
2. counter-transform 只抵消 scale；相机带旋转（rotY/rotX）时，标注要么与主体同处一个 3D 空间接受旋转，要么移去 `.stage-hud`——反向旋转抵消会产生透视畸变，成本大于收益
3. 页码/角标/比例尺等 chrome 首选放 `.stage-hud`（天然不跟镜头动，零成本）；counter-transform 只留给"必须指向 content 内具体元素"的标注

### 放大防糊（栅格化契约）

`transform: scale()` 放大不重新栅格化：浏览器按元素布局尺寸栅格化位图、再放大位图，文字必糊，2x 以上不可交付。防糊四层按需取用：

1. **合成层提升**：运镜开始前给相机层加 `will-change: transform`、结束后移除（同下方"性能红线"）；`translateZ(0)` 可作强制层提升的兜底写法。层提升后多数浏览器会按放大后的比例重新栅格化，中低倍率（≤1.5x）文字即可保持锐利
2. **raster 预算控制**：合成层纹理有最大尺寸上限（设备相关，常见 4096-16384px），大世界画布 × 高倍率极易超限，超限后引擎回退低分辨率栅格、无解必糊——世界层尺寸从紧（远景外扩量按 camera-storyboard.md §4 施工坑执行，不无限外扩），不把"整块巨画布放大"当运镜手段
3. **布局级缩放**：高倍率（≥1.8x）文字特写时，相机层放大从 `scale()` 换成 CSS `zoom` 属性——zoom 是布局级缩放，按放大后尺寸重新 layout 并栅格化，文字任意倍率保持矢量级锐利。两条配套纪律：zoom 改变布局坐标系，同层 translate 量必须除以 zoom 补偿；zoom 每帧触发 re-layout，是"禁动画布局属性"红线的唯一合法例外，只许用在相机层，禁止扩散到普通元素
4. **位图素材倍率冗余**：源图像素 ≥ 显示尺寸 × 最大放大倍率；特写元素另备高倍率切片，在推进期交叉淡入盖住低清纹理（实现见 ui-demo-choreography.md §3 式⑥）

reduced-motion 下运镜为静态定位，防糊第 1、2 条随之失效也无害（无动画即无栅格化时序问题）；第 3、4 条的素材倍率冗余仍然生效。

## 叠加冲突（承重规则）

- **同一元素禁止叠加两个 transform 动画**（如入场 y 位移 + 环境 scale 缩放并发）：会互相覆盖，元素可能永不出现且无任何报错。两种解法：合并为一条关键帧序列；或拆父子两层——入场动画挂父层，环境动画挂子层
- **显式起止状态**：CSS animation / WAAPI 用 `fill: both` 且起止关键帧都写全，不依赖"从当前样式开始"的隐式起点，防止切页回看时闪跳
- **环境循环动画跟随页面可见性生命周期**：隐藏页立即暂停，契约见 generative-art-and-canvas.md

## View Transition API

优先使用 View Transition API 实现页面过渡：

```javascript
if (document.startViewTransition) {
  document.startViewTransition(() => {
    updateDOM();
  });
} else {
  // 降级 CSS transition
  element.classList.add('transition-fallback');
  updateDOM();
}
```

## 性能红线

- 动画仅限 transform / opacity / filter
- 避免触发 layout/paint 的属性（width/height/top/left/margin/padding）
- will-change 仅在动画开始前添加，结束后移除
- 同时运动的元素 ≤ 10 个
