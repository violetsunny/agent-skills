# 生成艺术与数据可视化动效

## 定位

当 Web 演示需要高度定制的数据可视化动效或艺术化背景时，使用本规则生成 Canvas API 驱动的生成艺术作品。优先使用原生 Canvas API，若必须用 p5.js 则将其源码内联（禁止 CDN）。

## 适用场景

1. 数据密集页面需要动态可视化（粒子流、力导向图、动态热力图）
2. 封面/过渡页需要独特的艺术化背景
3. 需要将抽象数据转化为感官体验（声音→波形、流量→粒子流）
4. 普通 Chart.js/SVG 无法满足表达需求时

## 两步工作流

### Step 1: 算法哲学

在写代码前输出算法哲学文档（4-6段）：

1. **核心隐喻** — 数据映射到什么视觉元素（粒子/线条/色块/波形）
2. **参数空间** — 从哲学出发定义参数（数量/尺度/概率/比率/角度/阈值）
3. **随机性策略** — 哪些维度允许随机，哪些必须确定性
4. **交互意图** — 用户如何影响生成过程（hover/click/scroll/time）

### Step 2: p5.js 实现

#### 确定性随机

动画帧内禁止 `Math.random()`——同一时刻会渲染出不同像素，翻回页面重触发时效果每次都不一样。两种原生实现：

```javascript
// 种子 PRNG：同一 seed 产出同一随机序列
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// 整数 hash：由元素索引/网格坐标直接派生伪随机值，无状态、同输入同输出
function hash2d(x, y) {
  let h = (x * 374761393 + y * 668265263) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
```

p5.js 语境用 `randomSeed(seed)` / `noiseSeed(seed)`，同 seed 必须产出相同结果。

#### 粒子物理质感（挤压拉伸与弧线）

粒子/彩带类 FX 不用纯线性运动，加两个物理量：

```javascript
// 体积守恒挤压拉伸：落地/撞击瞬间沿冲击轴压扁、垂直轴变宽
function squashStretch(intensity, direction = 'vertical') {
  return direction === 'vertical'
    ? { sx: 1 + intensity * 0.5, sy: 1 - intensity * 0.5 }
    : { sx: 1 - intensity * 0.5, sy: 1 + intensity * 0.5 };
}

// 抛物线弧线轨迹：x 线性，y = 线性插值 + 峰值在 t=0.5 的弧线偏移
function arcMotion(start, end, height, t) {
  const x = start.x + (end.x - start.x) * t;
  const y = start.y + (end.y - start.y) * t - 4 * height * t * (1 - t);
  return { x, y };
}
```

应用点：particle-burst/confetti-cannon 落地反弹瞬间压扁（intensity 0.3-0.6，2-3 帧内恢复）；抛射物用 arcMotion 替代直线（height = 水平距离的 10-25%）；反弹衰减配 keyframe-animation.md 的 bounceOut 闭式公式。

#### 状态代理驱动模式（state-proxy）

复杂多元素效果不直接 tween DOM，tween 一个普通对象、渲染函数读它：

1. 状态对象是唯一动画源：`const st = { progress: 0, camZ: 8 }`
2. 驱动器（rAF 或编排时间轴）只更新 st 的数值；render 函数把 st 应用到 DOM/canvas 后绘制
3. 初始化末尾手动调一次 render() seed 第 0 帧；任意时刻跳转/回看 = 由时间反推 st 再 render 一次，天然可擦洗、帧帧确定

#### 自包含要求

- 零外部依赖，一切 inline
- **优先方案**：用原生 Canvas API 实现
- **备选方案**：若必须用 p5.js，将其完整源码内联到 `<script>` 中，禁止 CDN 引用

#### 性能约束

- 目标 60fps
- 粒子数 ≤ 500（移动端 ≤ 200）
- 每帧计算 ≤ 8ms
- 提供 quality 降级开关

## 画布级图片生成

当不需要交互、只需静态高品质视觉时：

- 90% 视觉 / 10% 文字
- 设计哲学驱动，不是随机拼贴
- 边界约束：所有元素在画布内，有呼吸空间
- 精炼优于添加：第二轮优化不增加图形

## FIXED vs VARIABLE

| 固定不变 | 可自定义 |
|---------|---------|
| 布局结构框架 | 算法逻辑 |
| Seed 控件位置 | 参数滑块范围 |
| 品牌色 token | 色彩映射 |
| 无障碍契约 | 交互方式 |

## 动效画布生命周期契约

用户明确要求持续动效（粒子背景、力导向图、数据流等）时，画布必须接入 deck 生命周期，不允许"加载即跑、永不停止"：

1. **随页启停**：监听页面激活/离开（翻页事件或 IntersectionObserver），进入页面才启动 rAF 循环，离开立即 `cancelAnimationFrame` 并释放引用；这是"禁止无限 rAF"约束的唯一豁免形态——循环仅在活跃页运行
2. **尺寸自适应**：容器尺寸变化用 `ResizeObserver` 重设画布宽高，并按 `devicePixelRatio` 缩放（`canvas.width = rect.width * dpr` + `ctx.scale(dpr, dpr)`），避免高分屏模糊
3. **配色读 token**：粒子/连线/文字颜色从 `getComputedStyle` 读取 `--primary-color`、`--secondary-color` 等语义 token，不硬编码色值；主题审阅（T 键）切换时同步换色
4. **容器显式尺寸**：画布容器必须有明确宽高，canvas 填充 100%；禁止靠内容撑开
5. **一页一效**：单页最多一个持续动效画布；与入场动画、数据动效同页时，持续动效透明度退后作背景层
6. **清理可验证**：交付自检时翻离页面后用 Performance 面板确认 rAF 已停止、无残留定时器

## ASCII 字符呼吸场

封面/章节页的点阵质感背景：单色品牌底上，等宽字符网格随噪声场明暗涌动，形成"仪表板呼吸"质感。纯 canvas 2D + rAF 零依赖；生命周期遵循"动效画布生命周期契约"全部条款，本节只写 ASCII 特有差异。

### 挂载与网格

1. 容器第一个子元素插入 `<canvas class="ascii-bg" aria-hidden="true">`；CSS：`position:absolute; inset:0; width:100%; height:100%; mix-blend-mode:screen; opacity:.92`，容器内其余内容 `position:relative; z-index:1` 浮于其上
2. 网格 CELL = 16px，字号 13px，字体读 `--mono` token（fallback monospace），字重 500，`ctx.textBaseline = 'top'`
3. DPR 取 `Math.min(devicePixelRatio, 2)`，`ctx.setTransform(dpr,0,0,dpr,0,0)`；尺寸重建走生命周期契约的 ResizeObserver 条款，重建回调用 rAF 去抖（cancel 上一帧再排新帧）

### 噪声场与字符密度映射

四个 sin 项叠加取均值到 [-1,1]，时间因子 `t = 经过秒数 × 0.55`（慢是关键，快了显躁）：

```javascript
const n = (
  Math.sin(col * 0.18 + t) +
  Math.sin(row * 0.24 - t * 0.7) +
  Math.sin((col + row) * 0.12 + t * 0.45) +
  Math.sin(Math.hypot(col - cols * 0.5, row - rows * 0.5) * 0.16 - t * 0.55)
) / 4;
const v = (n + 1) / 2; // [0,1]
```

1. 字符色板由疏到密：`'   ...:::---+++***◦◦••▢▣'`（开头三个空格 = 纯留白档）
2. `idx = Math.min(PALETTE.length - 1, Math.floor(v * PALETTE.length))`；命中空格字符的格子直接跳过，不进入 fillText
3. `v < 0.22` 的格子整体不画——留白比例决定质感，画满即噪
4. 透明度随场值线性爬升：`alpha = 0.08 + (v - 0.22) * 0.55`；深色品牌底用白色字符（screen 混合自然发亮），浅色底改主色字符（读 `--primary-color`）+ `mix-blend-mode:multiply`，不硬编码色值

### 生命周期与降级

1. 多个 ascii-bg 实例共用一个 rAF 循环，不各开各的；仅所在页激活时运行（随页启停条款）
2. 页面隐藏暂停：`visibilitychange` 且 `document.hidden` → 停循环并 `clearRect` 清场；恢复可见时以 `performance.now()` 重置 t0 再启动，不累计旧时间
3. 离屏降帧：同页多实例时，视口外实例每 4 帧才绘制一次（`(frame & 3) !== 0` 跳过）
4. 低功耗模式切换（自定义事件广播）时 stop/start；stop 必须 clearRect，不留残影
5. `prefers-reduced-motion`：不启动循环，只画 t=0 的静态单帧，或直接 `display:none` 保留纯色底——字符场不承载信息量，降级无损失
6. 性能预算：1920×1080 / CELL 16 ≈ 120×68 ≈ 8200 格每帧，主开销在 fillText；帧率不足先把 CELL 放大到 20-24 降密度，不降帧率
7. 预算归属：计入该页"一页一效"名额，并计入 animation-fx-catalog.md"持续型特效全套 ≤ 3 页"预算

## 约束

1. 生成艺术是增强手段，不是目的——内容理解优先
2. 必须提供静态降级（JS 禁用/性能不足时显示静态截图）
3. 数据映射必须有明确语义，不能为美观扭曲数据
4. prefers-reduced-motion 时降级为静态
5. 用户未明确要求时不主动使用生成艺术
