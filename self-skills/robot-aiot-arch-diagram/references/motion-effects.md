# 聚焦 SVG→GIF 动效（Focused SVG-to-GIF Motion）

动效只有一个公开契约：

```text
generated semantic SVG -> validated animated GIF
```

PNG 与 JPEG 不作为动画输入。动画 WebP、MP4、WebM、海报生成、旧版离线 motion-review 播放器均不属于本表面。静态 SVG/PNG 渲染与单文件交互式 HTML 导出器保持不变。

## 极简提示词

用户说以下内容时，使用最近一次生成的 SVG：

- `让这张图动起来`
- `生成 GIF`
- `制作 GIF`
- `把刚才的 SVG 转成 GIF`
- `Generate a GIF`
- `Animate this diagram`
- `Animate this SVG as a GIF`

无需提及格式、preset、时长或帧率。默认为 960px 宽、5.75 秒、20fps、115 帧、无限循环的 GIF。`auto` 从生成的 SVG 读取 style id 与显式 `data-motion-*` 边元数据。

输入必须满足十二个已批准 motion-scene 契约之一。源文件精确字节不锁定，因此受支持拓扑的、通过校验的标题与内容变体均可接受。role/stage/order 调度、路由方向、必需源色与几何保持 fail-closed；`auto` 不推断缺失元数据，也不把已评审的动效套用到任意同风格拓扑上。唯一的动效媒体产物是 GIF。除非 `--report` 指定其他路径，CLI 同时写出 `<output>.motion.json` 承载校验证据。

## ByteByteGo 衍生规则

六个实测 ByteByteGo newsletter GIF 使用 2.10–2.75 秒短循环，帧率统一为 20 或 33.33fps。一个循环内画布仅 1.20–3.56% 发生变化，且每个实测帧都唯一。默认循环延长到 5.75 秒，使已批准的 1.8 秒构建之后留出第 38–109 帧，作为清晰可读、持续运动的工作状态。本项目把这些经验固化为可复用的技术图表契约：

1. 第 0 帧保持节点与区域可读，所有连接线缺席。
2. 既有路由按语义顺序 draw-on，随后带方向标记落定。
3. 节点、标签、容器、marker 几何与镜头保持固定。
4. 连接线重叠度按场景钉死：Style 4 与 12 使用单条活跃构建，要求两条的方案强制两条，Style 7 的精确并行治理调度达到三条。完成的拓扑获得明显的工作状态停留。
5. 样例使用统一的 GIF 原生节奏；禁止 6/7 厘秒交替。
6. 最后一个槽位是真实动画采样，绝不是首帧复制。
7. 每条落定路由都携带无 marker 的工作态运动指向目标。Style 1–4 保留各自已批准的 packet-head、terminal-evidence、Blueprint-bead、Notion-card 身份。Style 5–12 每场景使用独立的 rail/signature 家族，并在 50% 审查尺寸下保持可辨。

## 已批准默认门

Style 1–12 已启用，其 signature、速度、路径、几何与构建契约均经用户批准。共享的 `+2s-settled-flow` 时序修订于 2026-07-17 批准，因此新的默认 5.75 秒包记录 `review_status: user-approved`。显式的 3.75 秒与 2.75 秒兼容时间线仍可按需提供。

### Style 1 — Memory Weave（记忆编织）

Style 1 遵循八个显式路由角色：

| 帧 | 角色 | 边含义 |
|---:|---|---|
| `1–8` | `ingress` | 用户请求 |
| `5–12` | `reason` | 应用到模型 |
| `9–16` | `extract` | 事实抽取 |
| `13–20` | `transform` | 抽取的事实 |
| `17–24` | `resolve` | 冲突消解 |
| `21–28` | `memory-write` | 持久化写入 |
| `25–32` | `memory-read` | 记忆关联/读取 |
| `29–36` | `response-context` | 上下文到响应 |

`connector-draw-on-with-persistent-data-flow` 原语临时隐藏全部不可变源边及其路由所属的标签组。每条路由获得一个无 marker 的线性 draw 克隆，以及一个在到达时恢复原 marker 的落定克隆。其标签底板与文本只随该落定路由出现；标签几何从不移动。拓扑在第 36 帧完成。第 `36–114` 帧，每条落定路由获得一对相邻的、无 marker、无滤镜、保持源路径方向的克隆。`persistent-data-flow-stream` 主体使用 memory-cyan `#06b6d4`、圆角端点与连接、不透明度 `.90`、宽度 `min(4.0px, max(3.0px, source stroke × 1.60))`、虚线模式 `16 25`。Style 1 当前 2.4px 源路由因此精确解析为 3.84px。紧随其后的 `persistent-data-flow-head` 克隆停留在主体内部，颜色 `#e0f2fe`、宽 `2.20px`、不透明度 `.98`、圆角端点与连接、模式 `6 35`。两个模式周期均为 41 单位；head 的 dash offset 恒为 body offset 减 10 单位，把明亮的 6 单位段置于青色主体前导 6 单位之上。两个克隆都不携带 marker、滤镜、辉光或模糊。

两层每渲染帧向目标共同推进 `-6.0` SVG 用户单位：960px 下 6px/帧即 120px/s，50% 审查比例下 3px/帧即 60px/s。共享相位为 `(motionStage × 7 + motionOrder × 3) mod 41`；request/reason/extract/facts/resolved/write/relate/context 的相位顺序为 `[7, 14, 21, 28, 31, 35, 1, 8]`。周期 41 与步长 6 互质，39 个流采样不会重复相位。第 36、37、38 帧使用成对层系数 `.30`、`.65`、`1.00`；第 `38–109` 帧保持 body/head 满不透明度 `.90`/`.98`。第 `110–114` 帧两层继续推进，同时把落定拓扑、标签、body、head 的不透明度依次乘以 `1.00`、`.7575`、`.515`、`.2725`、`.03`。采样使用 `time × fps − 0.5`，因此第 `0–35` 帧与已接受的原始 Chromium 基线完全一致。这使重置保持运动，并让第 74 帧区别于无连接线的第 0 帧。运行时几何哨兵同样 fail-closed：除非 `ingress` 向右行进、`resolve` 向左行进、`memory-write` 沿 down → left → down 行进且 dash offset 保持为负，否则失败；仅声明 source/target 元数据不够。

### Style 2 — Dark Terminal 证据追踪（evidence trace）

Style 2 通过 SVG style 元数据选择 `tool-grounding` 场景。其调度以精确的 `(data-motion-role, data-motion-order)` 对为键，因此两条 grounding 路由保持独立可寻址，且每个期望键必须恰好出现一次。源边 stage 与路由颜色在渲染前校验。

| 帧 | Stage | Role / order | 证据转移 | 主体色 |
|---:|---:|---|---|---|
| `1–8` | `1` | `ingress / 0` | 查询进入应用 | `#a855f7` |
| `5–12` | `2` | `delegate / 0` | 应用委托给模型 | `#a855f7` |
| `9–16` | `3` | `tool-call / 0` | 模型发出终端命令 | `#38bdf8` |
| `13–20` | `4` | `inspect / 0` | 终端输出被检查 | `#38bdf8` |
| `17–24` | `5` | `index / 0` | 被检查的证据进入索引 | `#22c55e` |
| `21–28` | `6` | `grounding / 0` | 已索引证据返回 grounding | `#fb7185` |
| `25–32` | `6` | `grounding / 1` | grounding 到达答案上下文 | `#fb7185` |
| `29–36` | `7` | `answer / 0` | 有依据的答案返回用户 | `#f97316` |

每条路由落定后，获得一对相邻的、无 marker、无滤镜的克隆。`terminal-evidence-stream` 主体继承该源路由的描边，宽度 `min(3.8px, max(3.0px, source stroke × 1.50))`、不透明度 `.94`、虚线模式 `15 26`。Style 2 的 2.3px 路由精确解析为 3.45px。紧随其后的 `terminal-command-head` 为白色 `#f8fafc`、宽 2.0px、不透明度 `1.00`、模式 `5 36`；其 offset 为 body offset 减 10 单位。两者每渲染帧推进 `-6.0` SVG 用户单位，960px 下 6px/帧，50% 审查尺寸下 3px/帧。相位公式为 `(motionStage × 6 + motionOrder × 3) mod 41`，按调度顺序产生 `[6, 12, 18, 24, 30, 36, 39, 1]`。周期 41 与步长 6 互质，全部 39 个流采样相位唯一。

全部八个方向都是运行时哨兵：`ingress / 0` 向右；`delegate / 0` down → left → down；`tool-call / 0` 向右；`inspect / 0` 向下；`index / 0` right → up；`grounding / 0` up → left → up；`grounding / 1` 向右；`answer / 0` 向右。body/head 对在第 `36–38` 帧淡入，第 `38–109` 帧保持满不透明度，随后继续运动并共享五帧重置。

终端提示符上出现一个场景签名：`terminal-prompt-cursor`。渲染器要求恰好一个 `data-node-id="terminal"` 节点，且其中恰好一个未被修改的 `_` 源文本。一个 2.2px 高的 `#a7f3d0` 矩形由该下划线的运行时 `getBBox()` 导出，置于独立签名层。它只改变不透明度：第 `16–69` 帧内，每个 16 帧周期有八个 `.95` 亮帧，随后八个缺席帧。其节奏持续到 `reset_start - 1`；第 `110–114` 帧把亮光标乘以共享重置不透明度。源下划线保持可见且未被修改。终端文字打字机、扫描线、辉光、镜头运动、动画背景均在本场景契约之外。

### Style 3 — Blueprint 分发波（distribution wave）

Style 3 选择 `service-blueprint` 场景。SHA-256 `b8f55d9ea0c6111176d8ff50d2e844b2001ee5087a3940621e635e1b875d470d` 仍是已评审的参考源，而非精确字节输入锁。其调度以精确的 `(data-motion-role, data-motion-order)` 对为键。每个键解析到一条不可变源边，且每个源 stage 与路由颜色在渲染前校验。

| 帧 | Stage | Role / order | Blueprint 转移 | 主体色 |
|---:|---:|---|---|---|
| `1–6` | `1` | `ingress / 0` | 客户端请求进入网关 | `#38bdf8` |
| `4–9` | `2` | `policy / 0` | 网关校验身份与策略 | `#67e8f9` |
| `8–13` | `3` | `fanout / 0` | 网关打开 Order 分支 | `#38bdf8` |
| `11–16` | `3` | `fanout / 1` | 网关打开 Catalog 分支 | `#38bdf8` |
| `14–19` | `3` | `fanout / 2` | 网关打开 Billing 分支 | `#38bdf8` |
| `18–23` | `4` | `data-write / 0` | Order 写入 Postgres | `#fde047` |
| `21–26` | `4` | `data-write / 1` | Catalog 写入 Redis | `#fde047` |
| `24–29` | `4` | `data-write / 2` | Billing 写入 Warehouse | `#fde047` |
| `28–33` | `5` | `event / 0` | Billing 发布事件 | `#fb7185` |
| `31–36` | `6` | `telemetry / 0` | Event Router 发出指标 | `#fb7185` |

自第 36 帧起，每条落定路由获得一个无 marker、无滤镜的 `blueprint-distribution-wave` 主体。它继承源描边，宽度 `min(3.4px, max(2.8px, source stroke × 1.40))`、不透明度 `.92`、圆角端点与连接、虚线模式 `12 31`。已评审的 2.1px 路由精确解析为 2.94px，50% 审查比例下为 1.47px。dash offset 每渲染帧推进 `-6.0` SVG 单位。

每个主体配一个 `blueprint-registration-bead`：半径 3.0px 的圆，填充 `#e0f2fe`、源色 1.2px 描边、不透明度 `.98`。其初始路径距离为路由相位。每渲染帧通过 `getPointAtLength` 把 `cx`、`cy` 推进 `+6.0` 用户单位；bead 从目标端回绕到源起点，从不反向。只有 `cx`、`cy`、`opacity` 变化。

仅按 stage 的相位公式为 `(motionStage × 7 + motionOrder × 0) mod 43`，产生 `[7, 14, 21, 21, 21, 28, 28, 28, 35, 42]`。因此三条 fan-out 路由共享相位 21，三条等长 data-write 路由共享相位 28，并在整个活跃区间内保持相同的 bead Y 坐标。周期 43 与步长 6 互质，39 个活跃采样不会重复 body 相位。

十个运行时方向哨兵要求：ingress 向右；policy 向右；fan-out/0 down → left → down；fan-out/1 向下；fan-out/2 down → right → down；三条 data write 全部向下；event 向右；telemetry 向下。body dash offset 必须保持为负，bead 行进保持为正。body 与 bead 在第 35 帧前缺席，第 `36–38` 帧以 `.30`、`.65`、`1.00` 系数淡入，第 `38–109` 帧保持满不透明度，随后在五帧重置中继续推进。辉光、模糊、阴影、扫描线、节点/文本/镜头/背景运动、光晕、涟漪、终端光标均在 Style 3 契约之外。

### Style 4 — Notion 记忆卡片交接（memory-card handoff）

Style 4 选择 `memory-lifecycle` 场景。SHA-256 `04cf833659e82c3e1743db4042cacf839a6d784a99c32d076e36fd4776e70c1b` 仍是已评审的参考源，而非精确字节输入锁。其精确的 `(data-motion-role, data-motion-order)` 调度只允许一条活跃连接线构建：

| 帧 | Stage | Role / order | 记忆转移 | rail/卡片色 |
|---:|---:|---|---|---|
| `1–4` | `1` | `sample / 0` | 感官输入进入工作记忆 | `#3b82f6` |
| `5–8` | `2` | `attend / 0` | 活跃上下文到达 agent | `#3b82f6` |
| `9–12` | `3` | `invoke / 0` | agent 调用程序性记忆 | `#7c3aed` |
| `13–22` | `4` | `remember / 0` | 工作上下文进入情景记忆 | `#059669` |
| `23–26` | `5` | `consolidate / 0` | 情景固化为语义知识 | `#ea580c` |
| `27–36` | `6` | `recall / 0` | 语义知识返回 agent | `#ea580c` |

自第 36 帧起，全部六条落定路径获得无 marker、无滤镜的 `notion-memory-rail`。每条 rail 使用目标记忆色、宽度 `min(3.0px, max(2.4px, source stroke × 1.50))`、不透明度 `.88`、圆角端点与连接、虚线模式 `12 35`。已评审的 1.8px 路径精确解析为 2.70px，50% 审查尺寸下为 1.35px。相位公式 `(motionStage × 7 + motionOrder × 0) mod 47` 产生 `[7, 14, 21, 28, 35, 42]`；dash offset 每帧推进 `-6.0` 用户单位。周期 47 与步长 6 互质，39 个活跃 rail 采样无一重复。

每条 rail 配一个 `notion-memory-card` 组。其白色外框矩形为 `x=-7`、`y=-5`、`14×10`、`rx=2`，带 1.4px 语义色描边。两条 2px 平头墨线使用 `shape-rendering="crispEdges"`，分别从 `(-4.5,-2)` 到 `(4,-2)`、从 `(-4.5,2)` 到 `(0.5,2)`。精确的归一化起始进度向量为 `[0.08, 0.22, 0.36, 0.50, 0.64, 0.78]`；距离为 `8 + progress × (pathLength − 16)`。卡片与两端点保持 8px 净空，每渲染帧推进 `+6.0` 路径单位，从目标端净空回绕到源端净空，且只动画组 `transform` 与 `opacity`。

方向哨兵要求 sample、attend、invoke 指向右（`0°`）；remember 指向下（`90°`）；consolidate 指向右（`0°`）；recall 指向上（`-90°`）。rail 与卡片在第 35 帧前缺席，第 `36–38` 帧以 `.30`、`.65`、`1.00` 系数淡入，第 `38–109` 帧保持满不透明度，并在共享五帧重置期间继续推进。卡片与 rail 保持在路由标签与节点之下。通用 packet head、圆形 bead、终端光标、辉光、模糊、阴影、扫描线、节点/文本/镜头/背景运动、光晕、涟漪均在 Style 4 契约之外。

### Style 5–12 — 已批准签名与共享时序

全部八个已批准风格契约保持不可变的源路径、标签、节点、容器、文本与 marker。它们复用无连接线开场、精确语义 draw-on、第 `36–38` 帧活跃淡入、第 `38–109` 帧工作状态停留、运动中的 `110–114` 帧重置。活跃 rail 从不超过其源描边宽度或场景上限。

| Style | Preset | Rail | 签名/辅助元素 | 行进速度 | 风格/时序状态 |
|---:|---|---|---|---:|---|
| 5 | `agent-orchestration` | `glass-handoff-rail` | 14×9 `glass-task-capsule`；协调器光晕 | 6px/帧 | 已批准 / `+2s` 已批准 |
| 6 | `governed-runtime` | `governance-thread` | 12×12 `policy-seal` | 6px/帧 | 已批准 / `+2s` 已批准 |
| 7 | `token-stream` | `api-token-rail` | 三节 `token-train` | 6px/帧 | 已批准 / `+2s` 已批准 |
| 8 | `golden-circuit` | `luxury-circuit-rail` | `gem-tracer`；仅其宝石光晕允许使用滤镜 | 6px/帧 | 已批准 / `+2s` 已批准 |
| 9 | `review-trace` | `review-trace-rail` | `review-cursor` | 5px/帧 | 已批准 / `+2s` 已批准 |
| 10 | `cloud-flow` | `cloud-flow-rail` | 区域 chevron、复制胶囊、可用性脉冲 | 6px/帧 | 已批准 / `+2s` 已批准 |
| 11 | `event-transit` | `event-transit-rail` | 事件列车、异常/投影车厢、停留环 | 5px/帧 | 已批准 / `+2s` 已批准 |
| 12 | `ops-pulse` | incident / telemetry rails | ECG/导出头、trace 揭示、`waterfall-scanner` | 5px/帧 | 已批准 / `+2s` 已批准 |

Style 8、11、12 使用 `(data-motion-role, data-motion-stage, data-motion-order)`，因为重复角色必须保持独立可寻址。Style 10–12 只向静态源图添加显式 motion 元数据；剥离 `data-motion-role`、`data-motion-stage`、`data-motion-order` 后精确还原动画前的静态 SVG 几何。

## CLI

```bash
SKILL_ROOT="$HOME/.agents/skills/robot-aiot-arch-diagram"  # 本 skill 安装目录（SKILL.md 所在处），按实际安装路径调整
python3 "$SKILL_ROOT/scripts/fireworks.py" animate diagram.svg diagram.gif
```

可选控制项刻意保持精简：

```bash
python3 "$SKILL_ROOT/scripts/fireworks.py" animate diagram.svg diagram.gif \
  --preset auto --duration 5.75 --fps 20 --width 960 \
  --report diagram.motion.json
```

`--dry-run` 用于在不启动 Chrome、不写产物的情况下校验身份、语义、几何、时间线、输出路径与渲染预算。`duration × fps` 必须是至少 55 帧的整数。宽 × 高 × 帧数不得超过 6 亿渲染像素。

## 运行时

SVG→GIF 导出需要 Node.js 18+、FFmpeg/FFprobe、Chrome/Chromium，以及 `puppeteer` 或 `puppeteer-core` 之一：

```bash
brew install ffmpeg
SKILL_ROOT="$HOME/.agents/skills/robot-aiot-arch-diagram"
npm install --prefix "$SKILL_ROOT" --ignore-scripts --no-save --package-lock=false puppeteer-core@25.3.0
python3 "$SKILL_ROOT/scripts/fireworks.py" doctor
```

Chrome 安装在非标准位置时设置 `CHROME_PATH`（兼容旧变量 `FIREWORKS_CHROME_PATH`，仅在 `CHROME_PATH` 未设置时生效）。Node 运行时放在别处时，用 `FIREWORKS_PUPPETEER_PATH` 指定显式的可信模块目录。渲染器解析从不搜索调用方工作目录，因此在图表项目里安装 `puppeteer-core` 不会让复制安装的 Skill 可用。`skills --copy` 安装会产生两个独立根目录，每个既有根都需要各自的运行时安装。Chrome 沙箱默认启用；no-sandbox 覆盖仅保留给隔离的 CI runner。

## 质量契约

- 要求源 SVG 带 `viewBox`、有效语义元数据，且每条被评审的边带显式 motion role、stage、order。
- 消毒 SVG，阻断脚本、事件处理器、外部引用、活动 CSS 与浏览器网络请求。
- 渲染前通过 XML、marker、几何与构图检查。
- 保留源 SHA-256，并在每次帧捕获前断言静态 DOM。
- 用临时样式表隐藏源边与路由标签；在节点之下插入 draw、settled-marker、按风格的 stream-body、packet-head、registration-bead 或 memory-card 装饰。Style 1/2 的 head 保持紧随其 body，Style 3 的 bead 与 Style 4 的卡片保持在路由标签与节点之下，到达标签层保持在所有运动路径之上。Style 2 的仅不透明度光标保持在终端节点之上，且不修改其源下划线。
- 在手动时间线上渲染统一的帧中心采样。
- 对比 Style 1 在 55 帧与 75 帧时间线上的原始 Chromium 帧 `0–35`；GIF 调色板量化前其哈希必须一致。为已批准的 Style 1 worker 保留独立的 75 帧原始基线，并要求改动后的每一帧保持字节一致。
- GIF 编码前对 Style 2 做光栅测试：body/head 分层、6px/帧全尺寸行进、3px/帧半尺寸行进、语义路由色、全部八个方向哨兵、光标节奏、五帧重置。
- 对 Style 3 做光栅测试：无连接线开场、十个 body 与十个 registration bead、6px/帧全尺寸与 3px/帧半尺寸 bead 行进、stage 锁定的 fan-out/data-write 同步、全部十个方向、源 DOM 完整性。
- 为已批准的 Style 1–3 保留各自独立的 75 帧原始 Chromium 基线，并要求改动后的每一帧保持字节一致。
- 每个风格分别以 75 与 115 帧渲染，帧 `0–70` 的全部 852 组原始对比通过三级兼容门接受：二进制 SHA-256 精确、解码 RGBA 精确、再是受保护的合成器抗锯齿等价。受保护级要求 AE ≤ 128、归一化 RMSE ≤ 0.001、每个连通差异分量至多 2px 宽或高、且每个分量保持在边或节点边框上。分级分别报告。DOM 与按风格签名几何在 GIF 调色板量化前保持严格精确。
- 对 Style 4 做光栅测试：无连接线开场、六路由顺序到达、六条语义 rail 与六张描边卡片、8px 端点净空、6px/帧全尺寸与 3px/帧半尺寸行进、精确 progress/phase/rotation 向量、全部六个方向、源 DOM 完整性。真实 Chromium 捕获并 50% 点采样降采样后，横向、向下、向上的卡片必须各自保留两条不接触、不等长的墨线，且其间有完整的背景行或列。
- 要求 FFprobe 给出精确的编解码器、尺寸、时长与帧数。
- 要求精确的原始与编码帧数，且相邻帧零重复。75 帧内每帧唯一。更长时间线要求至少 75 个唯一光栅，并允许满不透明度帧 `38–109` 内部出现重复哈希。第 `110` 帧是唯一允许的边界重复，因其未变化的重置不透明度恰为 `1.00`；归类为 `intentional_reset_boundary_repeat`。第 `111–114` 帧保持全局唯一。记录全部重复帧索引，并内嵌 GIF 无限循环。
- GIF 与可选 JSON 报告原子化安装。
- 以 500KB 为聚焦产物目标，并报告确定性的体积建议。
- 每个风格评审交付一个实时 GIF 加一张相位缩略图联排（contact sheet）。

**验证脚本：** `python3 "$SKILL_ROOT/scripts/test-verify-motion.py"` — 对 verify-motion.py 的对抗测试（正极：`assets/template-motion.html` 必须零 finding 通过；负极：每个变异必须产生含预期子串的 finding），仅用 Python 标准库；退出码 0=全部通过，1=任一失败。
