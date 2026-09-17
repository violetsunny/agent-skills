# 动画特效目录与明确要求路由

本文件是扩展动画特效目录（CSS 入场动画 + canvas 持续特效）。**默认不用**：常规汇报 deck 只走 `interactive-mode-rules.md` 的克制入场表。仅当用户明确要求动画特效（"炫酷一点""要动效""庆祝感""科技感粒子""发布会风格"等）时，按本文件路由选型。

## 1. 路由规则（先读，再选效果）

1. **触发条件**：用户明确要求动画特效，或明确指定某个效果名。未提及 = 不启用本目录
2. **选型声明**：动手前列出所选效果清单（每页用了什么、为什么），一条短消息给用户确认；用户已锁定效果名时可跳过
3. **预算硬限**：
   - 单页 CSS 入场动画 ≤ 2 种（stagger 列表算 1 种）
   - 单页 canvas FX ≤ 1 个，且只放封面、尾页、重点强调页
   - 全套 deck 持续型特效（marquee/kenburns/FX）总计 ≤ 3 页
4. **冲突裁决**：目录效果与既有硬约束冲突时，硬约束赢——动画属性仅限 transform/opacity/filter（clip-path 类效果见 §2 标注的例外条款）；FX 必须走 `generative-art-and-canvas.md` 生命周期契约（随页启停）；`prefers-reduced-motion` 一律降级
5. **色彩纪律**：所有特效颜色读语义 token（--primary-color 等），不硬编码色值

## 2. CSS 入场动画目录（27 种）

挂载方式：元素加 `data-anim="<name>"`，与 `data-enter-order` 共用触发机制——页面激活时按 order 依次播放，翻回该页时重触发。

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

## 3. Canvas FX 目录（20 种）

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

FX 附加规则：

1. 每页 ≤ 1 个 FX；FX 页的 CSS 入场动画降为最简（fade-up 一档）
2. 数据语义类 FX（knowledge-graph/neural-net/chain-react）节点与连线数量服从复杂度预算，不为炫技加密度
3. FX 容器必须有显式高度；canvas 填充 100%
4. 汇报正文页（数据看板、表格、架构图）禁止叠加 FX，图表可读性优先

## 4. 交付审查联动

1. 选型声明与实际使用一致，无未声明效果
2. 预算硬限逐项核对（单页 CSS ≤2、FX ≤1、持续型全套 ≤3 页）
3. clip-path 例外效果（glitch-in/spotlight/ripple-reveal）仅在用户点名风格时出现
4. reduced-motion 下全部特效降级为即时显示；FX 画布不启动
5. 翻离页面后 rAF 停止、无残留定时器（Performance 面板验证）
