# 动画特效目录与明确要求路由

本文件是扩展动画特效目录（CSS 入场动画 + canvas 持续特效）。**默认不用**：常规汇报 deck 只走 `interactive-mode-rules.md` 的克制入场表。仅当用户明确要求动画特效（"炫酷一点""要动效""庆祝感""科技感粒子""发布会风格"等）时，按本文件路由选型。

## 1. 路由规则（先读，再选效果）

1. **触发条件**：用户明确要求动画特效，或明确指定某个效果名。未提及 = 不启用本目录
2. **选型声明**：动手前列出所选效果清单（每页用了什么、为什么），一条短消息给用户确认；用户已锁定效果名时可跳过
3. **预算硬限**：
   - 单页 CSS 入场动画 ≤ 2 种（stagger 列表算 1 种）
   - 单页 canvas FX ≤ 1 个，且只放封面、尾页、重点强调页
   - 全套 deck 持续型特效（marquee/kenburns/FX）总计 ≤ 3 页
   - 豁免：验证/测试产物（test-run 下的验证 deck）不受本节预算约束，用于逐效果验收；豁免必须在验证报告中显式声明，交付 deck 不适用
4. **冲突裁决**：目录效果与既有硬约束冲突时，硬约束赢——动画属性仅限 transform/opacity/filter（clip-path 类效果见 §2 标注的例外条款）；FX 必须走 `generative-art-and-canvas.md` 生命周期契约（随页启停）；`prefers-reduced-motion` 一律降级
5. **色彩纪律**：所有特效颜色读语义 token（--primary-color 等），不硬编码色值
6. **情绪→动效路由**（用户给了情绪词但没点名效果时按表选）：

| 情绪档 | 动效基调 | 效果选择 |
|---|---|---|
| 震撼/电影感 | 慢、大、深 | 慢淡入 1-1.5s、scale 0.9→1 大过渡、blur-in、perspective-zoom、spotlight |
| 科技/未来 | 发光、故障、网格 | neon-glow、glitch-in、decode-flip、matrix-rain/data-stream FX、monospace 点缀 |
| 活泼/友好 | 弹、浮、圆 | 闭式弹簧 ζ0.6-0.7、spring-ticker、karaoke-highlight、圆角粉彩 |
| 专业/商务 | 快、克制、干净 | 200-300ms 微妙过渡、fade-up 一档、干净切页、数据可视化焦点 |
| 平静/极简 | 极慢、留白 | sine 极缓微动、柔和淡入、hold_breath 级呼吸 |
| 杂志/编辑 | 错落、图文交织 | waterfall-entry、staggered 逐词揭示、pull quote |

7. **动效动词索引**：描述效果用动词不用形容词——每个动元素领一个动词，命不出动词说明还没设计完：

| 动词类 | 动词 | 对应效果 |
|---|---|---|
| 冲击/重量 | 砸、重压、冲、碎裂、掉落 | beat-slam、drop-in、scale 0.6→1 back-out 过冲入场、shake（x -9→9→0 线性） |
| 方向/刻意 | 滑、推、拉、擦除、切 | fade-left/right、±150px quart-out 滑入、下划线 scaleX 0→1（origin left） |
| 揭示/生长 | 描、填、长、组装、计数 | path-draw、stat-grow、counter-up、card-morph |
| 有机/环境 | 浮、漂、呼吸、脉冲、环绕 | kenburns、scale 1.015 sine-inout 呼吸、orbit-ring、glow 脉冲 |
| 机械/精确 | 打字、咔哒、锁定、步进 | typewriter、spring-ticker、steps(N)、press-release |

## 1b. 缓动别名速查

目录内所有参数使用这些别名（闭式弹簧与 bounce/elastic/back 公式见 keyframe-animation.md，唯一实现不复制）：

| 别名 | cubic-bezier | 性格 |
|---|---|---|
| cubic-out | (0.25, 1, 0.5, 1) | 标准安定，默认主力 |
| quart-out | (0.22, 1, 0.36, 1) | 硬而决 |
| expo-out | (0.16, 1, 0.3, 1) | 最脆 |
| back-out | (0.34, 1.56, 0.64, 1) | 轻过冲，仅俏皮语域 |
| cubic-in | (0.32, 0, 0.67, 0) | 出场加速 |
| sine-inout | (0.37, 0, 0.63, 1) | 环境循环 |
| smooth-inout | (0.65, 0, 0.35, 1) | 移位对称 |

## 1c. 页面级入场编排 recipe（5 种）
> 规范实现：`templates/entry-recipes.js` — 按本节规格实现的完整可运行代码；复制进交付物，以 templates 为准

单个效果（§2）是叶子级动作，recipe 是页面级编排：页面激活时把一组 data-anim 元素按语义顺序播完。挂载属性分工：`<section>` 用 `data-animate="<recipe>"` 选编排；元素用裸 `data-anim`（无值）加入编排，或取角色值 `left / right / divider / line / step`。§2 的效果名值（如 `data-anim="fade-up"`）与 recipe 角色值互斥——页面带 data-animate 时整页按 recipe 时序播，不再单独播单效果名。一个 recipe 计入 §1.3"单页 CSS 入场 ≤ 2 种"预算时算 1 种。

| recipe | 触发 | 行为与帧级参数 |
|---|---|---|
| `cascade`（默认） | 不加 data-animate | 全部 data-anim：opacity 0→1 + translateY 16→0px，0.75s，delay = 0.15s + i×0.1s，quart-out |
| `hero` | data-animate="hero"（封面/章节大页） | y 14→0px，0.9s，delay = 0.2s + i×0.16s，quart-out——比 cascade 慢，仪式感 |
| `quote` | data-animate="quote" | 非 line 元素先出（y 8→0px，0.6s，stagger 0.12s、start 0.2s）；`data-anim="line"` 行 opacity 0.35→1 + y 10→0px，0.8s，行间 stagger 0.55s、start 0.5s，逐句揭示 |
| `directional` | data-animate="directional" | 其余元素先出（stagger 0.1s、start 0.15s）→ 左列 x -24→0px，0.8s，delay 0.35s → 分割线 opacity 0→0.25，0.5s，delay 0.9s → 右列 x 24→0px，0.8s，delay 1.0s |
| `pipeline` | data-animate="pipeline" | 进页全部 step 置 opacity 0.15；每次前进键点亮一个 step（opacity 0.15→1 + y 8→0px，0.5s），step 间箭头 opacity 0.15→0.7，0.3s，delay 0.15s；全部点亮后才放行翻页 |

库 API → 原生换算（全部 WAAPI/rAF/CSS，零依赖）：

| 库 API 形态 | 原生等价物 |
|---|---|
| `animate(el, {opacity:[0,1], y:[12,0]}, {duration:.6, easing:[.22,1,.36,1]})` | `el.animate([{opacity:0, transform:'translateY(12px)'}, {opacity:1, transform:'translateY(0)'}], {duration:600, easing:'cubic-bezier(.22,1,.36,1)', fill:'both'})` |
| `animate(list, …, {delay: stagger(step, {start})})` | `list.forEach((el,i) => el.animate(…, {delay: start + i*step, fill:'both'}))` |
| `x / y / scale` 简写属性 | 拼进 transform 字符串（translateX / translateY / scale） |
| easing 四元数组 `[x1,y1,x2,y2]` | `'cubic-bezier(x1,y1,x2,y2)'` 字符串 |
| 滚动驱动入场 | IntersectionObserver 触发，或 CSS `animation-timeline: view()`；不支持时回退页面激活即播 |

实现规则：

1. 触发时机：页面转场中段（转场开始约 450ms 后）调用 playSlide(idx)，避免与转场本体打架；翻回页面先复位再重播
2. pipeline 与导航耦合：前进事件（→ / 空格 / 滚轮下滑）先询问 pipeline 钩子是否还有未点亮 step，有则消费事件点亮，无则放行翻页
3. 保底：编排脚本报错时把所有 data-anim 强制 `opacity:1; transform:none`——内容可读性优先于动效
4. 低功耗 / reduced-motion：先 `document.getAnimations().forEach(a => a.cancel())` 再直接置可见态，不播任何入场
5. data-anim 只挂叶子语义块（标题/lead/卡片/图/列），不挂 grid 容器、不挂每个 li；整页不想入场就整页不打标

## 2. CSS 与 DOM 动画目录（49 种）

挂载方式：入场类元素加 `data-anim="<name>"`，与 `data-enter-order` 共用触发机制——页面激活时按 order 依次播放，翻回该页时重触发。交互类（§2c）由事件绑定触发，数据类（§2d）随页面激活触发一次。

### 方向性淡入（安全默认档）

| 名称 | 效果 | 适用 |
|---|---|---|
| `fade-up` | 下方 32px 上移淡入 | 正文、卡片入场默认 |
| `fade-down` | 上方 32px 下移淡入 | 页眉、横幅、提示条 |
| `fade-left` | 左侧 40px 滑入淡入 | 分栏左列 |
| `fade-right` | 右侧 40px 滑入淡入 | 分栏右列 |

### 戏剧化入场

| 名称 | 效果 | 适用 |
|---|---|---|
| `rise-in` | 60px 上升 + 模糊消散 | 页面主标题、hero 大字 |
| `drop-in` | 60px 下落 + 轻微缩放 | 横幅、警示条 |
| `zoom-pop` | 0.6 → 1.04 → 1 弹缩 | 按钮、关键数字、CTA |
| `blur-in` | 18px 模糊渐清（filter） | 封面揭示 |
| `glitch-in` | clip-path 阶梯抖动 ⚠️ | 科技/故障风强调；clip-path 例外条款：仅用户点名要 glitch 风时可用，单页 ≤ 1 个元素 |

### 文字效果

| 名称 | 效果 | 适用 |
|---|---|---|
| `typewriter` | 打字机逐字显现 | 单行口号、金句 |
| `neon-glow` | 文字发光脉冲（text-shadow） | 深底科技风标题 |
| `shimmer-sweep` | 高光扫过 | 金属质感按钮、荣誉卡片 |
| `gradient-flow` | 渐变横向流动 | 品牌字标；与"正文禁文字特效"条款协调：仅限主标题 |

### 列表与数字

| 名称 | 效果 | 适用 |
|---|---|---|
| `stagger-list` | 子项依次上升入场 | 任何 ul/网格，配 data-enter-order 间隔 100-200ms |
| `counter-up` | 数字 0 → 目标值滚动 | KPI 页、大数字页；实现走 interactive-mode-rules 的 animateNumber（有终止条件） |

### SVG 几何

| 名称 | 效果 | 适用 |
|---|---|---|
| `path-draw` | 描边自绘（dasharray/dashoffset） | 连线、箭头、示意图；挂在 svg 上，内部 path 全部自绘 |
| `morph-shape` | 路径 d 值变形 | 背景形状；装饰性动效档，谨慎 |

### 3D 与透视（一次性入场，非持续背景，不触犯"禁 3D 持续旋转"条款）

| 名称 | 效果 | 适用 |
|---|---|---|
| `parallax-tilt` | hover 3D 倾斜 | hero 卡片、产品图 |
| `card-flip-3d` | Y 轴 90° 翻转 | before/after 揭示 |
| `cube-rotate-3d` | 立方体面旋入 | 章节过渡页 |
| `page-turn-3d` | 左轴翻页 | 叙事/编辑风 |
| `perspective-zoom` | 从 Z 轴 -400 拉近 | 封面开场 |

### 持续/氛围型（计入"全套 ≤ 3 页"预算）

| 名称 | 效果 | 适用 |
|---|---|---|
| `marquee-scroll` | 横向无限滚动 | 客户 logo 墙 |
| `kenburns` | 14s 缓慢缩放 | hero 背景图 |
| `confetti-burst` | 伪元素彩带迸发（一次性） | 致谢/达成页 |
| `spotlight` | 圆形 clip-path 聚光揭示 ⚠️ | 重大揭示时刻；clip-path 例外条款同 glitch-in |
| `ripple-reveal` | 角落涟漪展开 ⚠️ | 章节转场；同上 |

### 高级文字效果（扩展档）

| 名称 | 效果 | 关键参数 | 适用 |
|---|---|---|---|
| `decode-flip` | 字符从 90° 翻下，翻动中闪随机字形，落定显真字符 | 根 `perspective:1500px`；字符 `transform-origin:bottom` + `preserve-3d`；翻转 0.4-1.0s quart-out；字符 stagger 0.03-0.08s；进度 <0.5-0.7 时显伪字形、每 3-6 帧一换；字形种子 `i*1000+floor(p*100)` 保证确定性；同文 ghost 副本占宽防抖动，monospace 优先 | 品牌词/标签解码式揭示 |
| `waterfall-entry` | 词群自下方甩入，后词在前词落定前启动（负重叠） | opacity 二值 0→1 不淡入；按权重分档：锚点词 y 60-80px/0.16-0.20s、普通词 40-50px/0.13-0.16s、轻词 30-48px/0.10-0.13s；quart-out（更脆 expo-out），禁 inOut；`nextStart = prevStart + prevDur − 重叠1-2帧` | 标题卡、段落开场 |
| `beat-slam` | 短语按统一节拍逐条砸入，每条入场方式不同，终局锁定微呼吸 | 节拍间距 1.2-1.8s；入场 0.35-0.6s、出场 ≤0.25s；一组内 ≥3 种缓动（quart-out 硬砸/expo-out 侧snap/back-out 仅重音词）；终局呼吸 scale 1→1.01、1.6s sine-inout 循环；字 ≥150px、line-height 0.96、tracking -0.03em、恰好 1 个强调色 | tagline、宣言、开场造势 |
| `spring-ticker` | 老虎机竖滚，每格过冲咔哒落定 | 容器高 = 格高（fontSize×1.25）像素级相等 + `overflow:hidden`；1-4 步；每步 0.3-0.7s、步间隔 0.3-0.5s 且 ≤ 步时长（必须重叠才叠加）；过冲系数 1.4-2.5；`translateY(−Σ各弹簧进度×格高)` 必须 rAF 求和驱动（WAAPI 无法表达叠加）；数字 `tabular-nums`；终步后停 ≥1s | 价格滚动、名单轮播、倒计时 |
| `text-depth-3d` | 同文 N 层偏移副本渐透明，立体挤出感 | 4-6 层；每层偏移 1-3px（>4px 变 glitch）；后层 alpha 上限 0.6-0.85、逐层递减 0.08-0.15；字 ≥60px、weight 900；后层透明度写 `color:rgba()` 不用元素 opacity；入场后层先 cascade 0.04-0.10s/层；偏移方向 = 统一光向；禁叠加 text-shadow | 大标题立体感 |
| `karaoke-highlight` | 逐词累积高亮 | 词点亮 0.06s 变强调色 + scale 1.1、回退 0.08s；组入场 scale 1.3→1、0.15s back-out；组出场 opacity 0 + scale 0.9、0.1s，且终点强制 `visibility:hidden` 收口防复活；粗描边 `-webkit-text-stroke` + `paint-order:stroke fill` | 逐词讲稿强调、歌词式叙述 |
| `font-axis-morph` | 可变字体轴动画（字重/光学尺寸滑动） | `font-variation-settings` 经自定义属性 --wght/--opsz 动画，需 `@property` 注册（`syntax:"<number>"`）才可插值；0.45s cubic-out | 高级感标题、强调词变重 |

### 打字机两场景（标题逐字 / 正文逐块）

打字机不是一种效果而是两种场景，场景用错比参数不对更扎眼：流式输出做成匀速逐字读作"老电影字幕"，真人输入做成块状涌现读作"输入框自己在生成"。先定场景再取参数：

| 场景 | 条目 | 何时用 | 参数范围 | 原生实现要点 |
|---|---|---|---|---|
| 标题逐字 | `typewriter` | 单行口号、金句、终端命令、章节标题——短文本（≤20 字）且"机械/精确"动词档是刻意风格选择 | 字速与真人输入档同源：汉字 100-150ms/字（观众逐字跟读的速度下限）、英文/数字 40-70ms/字符；匀速逐字、不加不规律抖动——抖动是流式输出的性格，标题档要的恰是机械感；光标打字常亮、打完转 steps(1) 闪烁（帧级参数表与光标状态机见 ui-demo-choreography.md §3 式⑦，不复制） | 按字符拆 `<span>`，逐字 opacity 0→1 用 steps(1) 离散切换（无缓动插值），字符间 delay = 字速 × 序号（WAAPI 逐字 `delay` 或 CSS `animation-delay: calc(var(--i) * 字速)`）；禁 width + steps(N) 裁剪方案——width 是布局属性，触犯 §1 冲突裁决的动画属性白名单 |
| 正文逐块 | `typewriter-multi` | AI 流式输出、Agent 回复、多行日志生成——"模型在吐 token"；单行流式输出也走本档节奏 | 2-5 字符/块；中文按词 + 标点切块（不切词中间）；块间隔不规律 40-120ms；多行并发时行间起步错峰 100-150ms、强调色光标只跟最新一行——两个光标同时闪就是两个作者；文本过长先对时长预算：砍块数/砍行数，不加速 | 块间隔用种子随机（generative-art-and-canvas.md mulberry32）预生成累计时刻表，render(t) 纯函数按时间查表重建完整可见文本（与 ui-demo-choreography.md §3 式⑦ 的事件表回放同构）——双向 seek 安全、翻回页面重播帧帧一致；禁 setTimeout + Math.random 链 |

真人在输入框/终端打字（带犹豫、退格修正、确认停顿）是 UI 演示层形态，事件表编译与回放实现见 ui-demo-choreography.md §3 式⑦，本目录不收；三种形态共用同一光标纪律：打字常亮、打完 steps(1) 闪烁。

### 标记强调（手绘感）

| 名称 | 效果 | 关键参数 |
|---|---|---|
| `marker-highlight` | 马克笔横条扫过文字 | 半透明黄条 opacity 0.35、`inset:0 -6px`、radius 3px；scaleX 0→1 0.5s cubic-out；可选 skewX(-2°)；多行 stagger 0.3s |
| `marker-circle` | 手绘风圈注 | 环 130%×160%（短词 150%）、border 3px 强调色；scale 0→1 + rotate -3°、0.6s back-out |
| `marker-burst` | 放射爆线 | 12 条每 30° 一条、长 40-80px 必须不等长；scaleY 0→1 0.4s cubic-out、stagger 0.03s；线宽 3px |
| `marker-scribble` | 波浪下划线自绘 | SVG Q 控制点 y 交替 0/24、半波宽 25-50px；dashoffset len→0 0.8s smooth-inout |
| `marker-sketchout` | 双线条划掉 | 两条 2px 线，倾角随文字宽度自适应：线端垂直偏移 ≤8px（rotate = atan(8/宽度)，短标签 ≈±12°、宽文本 ≈±2°）；scaleX 0→1 各 0.3s、第二条晚 0.15s；线在文字上层 |

模式轮换节奏：高能量页每 2-3 组换一个模式，中能量 3-4 组，低能量 4-5 组。

### 物理交互（事件驱动）

| 名称 | 效果 | 关键参数 |
|---|---|---|
| `press-release` | 按钮线性压缩→弹簧回弹 + 背后光环爆发 | 压缩 scale 0.88-0.96（禁 <0.85），0.10-0.30s cubic-in；回弹 0.40-0.90s back-out；光环 scale 1→3-8 + 淡出、blur 40-100px、层级在按钮下；高潮后停留 ≥1s |
| `cursor-press-duet` | 演示光标与目标元素同时压缩、一起弹回 | 光标 48-96px、`transform-origin:0 0`（箭尖）、`pointer-events:none`；两者同 scale = 1−intensity（0.05-0.15）；按压 0.1-0.25s、回弹 0.4-0.7s back-out；hold 0.05-0.8s；同一次 animate 调用同时作用两者 |
| `displacement-kick` | 新元素弹入把旧元素"撞"出画面 | 单 rAF driver 0→1、back-out 过冲 1.4-1.6、总时长 0.6-1.4s；旧元素在进度 0.4-0.5 处完成退场（上限 0.6）；新元素 tilt 5-15° 随进度归 0；同轴反向；新元素 z-index 显式更高；容器 `overflow:hidden` |
| `click-ripple` | 光标点击涟漪扩散 | 移动 0.4-1.0s smooth-inout；按压 0.06-0.12s（光标压至 0.80-0.90 更狠、目标 0.92-0.97）；涟漪 1-3 圈 scale→3-6、0.5-1.0s cubic-out、圈间 stagger 0.06-0.12s；涟漪元素 t=0 就在 DOM（scale 0/opacity 0），`fill:forwards` 不预渲染起始态 |

### 数据动效（扩展档）

| 名称 | 效果 | 关键参数 |
|---|---|---|
| `chart-scrub` | 竖直追踪线+圆点+tooltip 沿已画好折线扫过，数值里程表跳动 | 单 rAF driver p:0→1；总时长 1.5-3s smooth-inout；marker r 6-12px；tooltip 偏移 16-48px 右上、贴右缘翻符号；数值文本仅在整数索引变化时写（防每帧 reflow）；`tabular-nums` + 固定 min-width；终点停留 ≥0.8s；构建后以 p=0 先 seed 一帧初始态 |
| `count-scale` | 数字计数与 scale 生长同步 | 计数 1.2-2.5s（<0.8s 成闪烁）cubic-out + scale 从起止尺寸比（40-60%）到 1，两动画同缓动同起点；后缀（%/×/+）计数完成后 0.3-0.6s back-out 入；label 提前（计数一半前）y:12→0；数字本体禁 back/elastic；`tabular-nums` + 固定宽容器必需 |
| `stat-grow` | 柱生长/进度填充/环进度/星级 | 柱：高度写死只动 scaleY 0→1、0.7s cubic-out、stagger 0.08s、origin bottom；条：`.fill` 固定 `width:100%` 再 scaleX 0→PCT、1.0s；环：dashoffset 实测长→长×(1−PCT)、1.1s，先 `rotate(-90deg)` 从 12 点起；星：金层 `clip-path:inset()` 右缘 100%→(100−评分%)、1.0s；禁 height/width tween；恰好 1 个 accent 色 |

### SVG 与变形

| 名称 | 效果 | 关键参数 |
|---|---|---|
| `icon-micro-motion` | 图标零件各自动：转针/开合/脉冲/流虚线 | 旋转 linear 4-10s 转 0.5-2.0 圈（避免整数圈）；脉冲 2-4 cycles/3-5s，环幅度 < 点幅度且相位滞后 π/2；虚线流 offset 为 dash 周期整数倍；**关键坑**：绕 SVG 内部指定点旋转/缩放必须用 transform attribute（`rotate(deg cx cy)`），CSS transform-origin 对细线/小圆会飞离圆心 |
| `card-morph` | 容器变形尺寸/圆角/表面即转场 | 禁 width/height tween——表观尺寸用 uniform scale；border-radius 目标 = 表观半径/scale；变形 0.6-1.2s smooth-inout（禁 back/elastic）；旧内容前 30-50% 淡出、新内容后 30-50% 淡入；非居中目标用 `getBoundingClientRect()` 双测差值（FLIP），不手算 |
| `path-follow` | 元素沿 SVG 路径运动 | `offset-path:path("M...")` + animate `offset-distance:0→100%`（1.5s cubic-out），原生零依赖 |

### 既有条目参数增补

- `gradient-flow`：background-size 必须 200-400%（≤100% 时 position 动画静默无效）；百分比轴反向（100%→0% = 视觉左→右）；连续扫 1.2-3s **linear**（加缓动读作物体不像光）；逐词点亮变体 = 双层像素级相同副本 + 词间滞后 0.25-0.5s；色相扫变体 `hue-rotate(0→40-180deg)`（>180° 调色板解体）。`-webkit-background-clip:text` + `background-clip:text` + `color:transparent` 三者缺一不可
- `path-draw`：单段 0.3-0.8s（>1s 拖沓）；多段 stagger = 下一段在前段 70-80% 处启动；末段时长 = 普通段 60-80%；cubic-out 或 linear（笔不弹，禁 back/elastic）；dasharray 用 `getTotalLength()` 实测，复杂路径可 ×1.05 高估（偏大仅起始不可见、偏小截尾）；连接线两端必须落在真实元素上
- `path-draw` 三坑（r4 批次实测）：① `marker-end` 箭头不受 `stroke-dashoffset` 裁切，线体未画时箭头即渲染（"箭头先出"）——正解是箭头分离：去掉 marker-end，在 path 终点生成独立 polygon（按 d 末段终点+切线角定位旋转），delay = 线 delay + 描线时长，线画完箭头才落位；opacity 门控（path `opacity:0` + keyframes `0%`/`to` 双帧 `opacity:1`，`to` 帧漏写则 forwards 结束后回落 0 终态连线消失）只是下限，门控后描线窗口内箭头仍先于线体可见；② reduced-motion 分支的 `stroke-dashoffset:0` 会被 path 内联 style 覆盖（只剩箭头无线体），须 `!important`；③ 验证必须截早期帧（virtual-time-budget≈300）+ 终态帧 + reduced 帧三态，只看终态截图发现不了①②
- 入场同步三条款（r4 批次实测，虚线/箭头瞬现根因）：① 无限流动动画（`anim-flow` 类 flowdash）禁止裸挂——元素无入场控制时虚线与 marker-end 箭头在页面加载即瞬现，与整体 `--i` 编排脱节；正解是双动画叠加 `animation:fadein .6s ease forwards,flowdash 1.6s linear infinite`，两个 `animation-delay` 均取 `calc(var(--i)*160ms)`（flowdash 可再加偏移），元素必须带 `--i`；② 带 dasharray 图案的虚线连接线禁用 `anim-draw`（dasharray 被覆盖、虚线变实线），用 `.anim-fade{opacity:0;animation:fadein .5s ease forwards;animation-delay:calc(var(--i)*160ms)}` 整体淡入，marker-end 箭头随线同帧淡入无需分离；③ reduced-motion 分支对新增入场类必须写 `animation:none;opacity:1`（只写 `animation:none` 会留 `opacity:0` 初值，元素永久隐藏）；SVG 图例组 `<g id="*-legend">` 必须挂入场类（anim-pop + `--i` 排在全图最后元素之后），裸 `<g>` 瞬现
- `shimmer-sweep`：光带位置用注册自定义属性 `@property --shimmer-pos`（`syntax:"<percentage>"`）-20%→120%、1.2s smooth-inout、多元素 stagger 0.15s；--shimmer-width 默认 20%、--shimmer-angle 默认 120deg
- `counter-up`：计数+缩放复合变体见 `count-scale`
- `typewriter` / `typewriter-multi`：两场景（标题逐字 / 正文逐块）选型与参数范围见上方"打字机两场景"小节

## 3. Canvas FX 目录（21 种）

挂载方式：容器加 `data-fx="<name>"` 并给定明确宽高；全部走生命周期契约（进入页面启动、离开 cancelAnimationFrame 释放、ResizeObserver + DPR 适配、颜色读 token）。

| 名称 | 效果 | 适用场景 |
|---|---|---|
| `particle-burst` | 中心粒子爆散，重力+淡出，每 2.5s 一轮 | 揭示时刻、大数字页 |
| `confetti-cannon` | 双底角彩带抛物 | 致谢/成功页 |
| `firework` | 火箭升空炸开火花，持续 | 庆祝、发布页 |
| `starfield` | 3D 星空迎面飞行 | 深空/科幻背景 |
| `matrix-rain` | 绿色字符雨落 | 网络安全、数据主题 |
| `knowledge-graph` | 力导向图，节点带标签、实时物理 | 知识图谱/RAG 页 |
| `neural-net` | 前馈网络结构，脉冲沿边传输 | 模型架构页 |
| `constellation` | 漂移点阵，距离 <150px 自动连线 | 氛围 hero 背景 |
| `orbit-ring` | 多同心环差速旋转 + 径向光晕 | 系统/分层概念 |
| `galaxy-swirl` | 对数螺旋粒子群慢旋 | 封面开场 |
| `word-cascade` | 词语自顶部落下堆积 | 概念云、词汇页 |
| `letter-explode` | 标题字母四散飞入，约 4.5s 一轮 | 大标题；文本经 `data-fx-text` 传入 |
| `chain-react` | 圆点多米诺脉冲波传递 | 流水线/顺序流程 |
| `magnetic-field` | 粒子沿贝塞尔/正弦曲线留迹 | 能量/流动抽象表达 |
| `data-stream` | 滚动十六进制/二进制文本行 | 数据、API、安全 |
| `gradient-blob` | 多团模糊径向渐变漂移叠加 | 柔和 hero 背景 |
| `sparkle-trail` | 指针跟随星光发射（空闲自动摆动） | 交互揭示 |
| `shockwave` | 中心扩散环循环 | 冲击、告警、发布 |
| `typewriter-multi` | 多行并发打字 + 光标闪烁（DOM 实现） | 终端风、Agent 启动日志 |
| `counter-explosion` | 数字滚动到目标后粒子爆散，4s 重置 | KPI 揭示、创新高 |
| `shader-fbm-bg` | WebGL FBM 噪声流场背景（余弦调色板+暗角） | 高级感封面、章节页；骨架见下 |

数字类动效（counter-explosion / 数字滚动）公共约束：HTML 文本即终值、JS 仅增强（无 JS 与截图时刻读到的都是终值）；headless 截图场景用 `setInterval` + 步数上限保证 virtual-time 内收敛到终值，禁 rAF（后台标签页暂停、virtual-time 下不收敛，通规见 `interactive-html-authoring.md` 画布约束与 `interactive-mode-rules.md` 入场触发条）

`shader-fbm-bg` 骨架（原生 WebGL 零依赖，全屏 quad + 单 fragment shader）：

> 规范副本：`templates/shader-fbm-bg.glsl` — 复制进交付物，以 templates 为准（下方代码块为参考摘录）
```glsl
precision mediump float;
varying vec2 v_uv; uniform float u_time; uniform vec2 u_res;
float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p){
  vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1,0)), f.x),
             mix(hash(i + vec2(0,1)), hash(i + vec2(1,1)), f.x), f.y);
}
float fbm(vec2 p){
  float v = 0.0, a = 0.5; mat2 R = mat2(0.8, 0.6, -0.6, 0.8);
  for (int i = 0; i < 5; i++){ v += a * noise(p); p = R * p * 2.02; a *= 0.5; }
  return v;
}
vec3 palette(float t){ return vec3(0.5) + vec3(0.5) * cos(6.28318 * (t + vec3(0.0, 0.33, 0.67))); }
void main(){
  vec2 uv = v_uv; uv.x *= u_res.x / u_res.y;
  float t = u_time * 0.4;
  vec2 q = vec2(fbm(uv*3.0 + t*0.3), fbm(uv*3.0 + vec2(5.2,1.3) + t*0.2));
  vec2 r = vec2(fbm(uv*3.0 + q*4.0 + vec2(1.7,9.2) + t*0.15), fbm(uv*3.0 + q*4.0 + vec2(8.3,2.8) + t*0.1));
  float n = fbm(uv*3.0 + r*2.0);
  vec3 col = palette(n*2.0 + t*0.2);
  col = mix(col, palette(length(q)*3.0 + t*0.1), 0.4);
  col *= 0.7 + 0.3*n;
  gl_FragColor = vec4(col * (1.0 - 0.4*length(v_uv - 0.5)), 1.0);
}
```

驱动与降级：`u_time` 由 rAF 线性推进并遵守画布生命周期契约（离页即停）；调色板相位偏移量（vec3(0.0,0.33,0.67) 的加数）换成从语义 token 主色推导的值以贴合品牌色；`getContext('webgl')` 失败 → 降级 `gradient-blob` 或 CSS 多层 radial-gradient 静态背景；reduced-motion 直接静帧。

FX 附加规则：

1. 每页 ≤ 1 个 FX；FX 页的 CSS 入场动画降为最简（fade-up 一档）
2. 数据语义类 FX（knowledge-graph/neural-net/chain-react）节点与连线数量服从复杂度预算，不为炫技加密度
3. FX 容器必须有显式高度；canvas 填充 100%
4. 汇报正文页（数据看板、表格、架构图）禁止叠加 FX，图表可读性优先
5. `shader-fbm-bg` 计入"全套 ≤ 3 页"持续型预算，且一个 deck 只允许一处 WebGL 背景

## 4. 交付审查联动

1. 选型声明与实际使用一致，无未声明效果
2. 预算硬限逐项核对（单页 CSS ≤2、FX ≤1、持续型全套 ≤3 页；交付 deck 适用，验证产物豁免见 §1 预算硬限豁免条款）
3. clip-path 例外效果（glitch-in/spotlight/ripple-reveal）仅在用户点名风格时出现
4. reduced-motion 下全部特效降级为即时显示；FX 画布不启动
5. 翻离页面后 rAF 停止、无残留定时器（Performance 面板验证）
6. 名称→技术一致性自查：效果名含 spring 则代码必有 elastic/back/bounce 或闭式弹簧；含 mask 必有 clip-path/mask；含 glass 必有 backdrop-filter；含 3d 必有 perspective/rotateX/Y/translateZ；含 draw 必有 stroke-dash/pathLength——名称虚称技术的，改名或补实现
7. 动效去重：两个效果的动作参数（属性/时长/缓动）与 DOM 骨架均相同的只保留一个，名字如实描述动作的优先
