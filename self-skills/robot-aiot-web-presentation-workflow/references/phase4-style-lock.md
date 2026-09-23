# Phase 4 风格锁定（deck 级默认基线）

多页/单页 deck 的页面 shell 与动画契约以此文件为准；`robot-aiot-interactive-html-author` 编写契约管编写期细则，两者冲突时本文件的 deck 级 token 与骨架优先。风格真源为 r4-anim-p01-p10 验证批次（位于该批次交付项目 `doc-web/test-run/` 下，存在时可作参照；不存在时以本文件规则为准）。

## 1. Token（逐字使用，禁改色值）

```css
--pri:#2563eb; --pri-d:#1d4ed8; --ink:#111827; --mut:#6b7280;
--line:#d1d5db; --bg:#fff; --band:#eff6ff; --band-l:#f9fafb; --band-m:#dbeafe;
--ok:#059669; --ok-bg:#ecfdf5; --err:#dc2626; --err-bg:#fef2f2;
```

- 全 deck 单色系：本基线默认全 light；dark 系 deck 将整套 token 镜像为暗底变体，禁止 light/dark 逐页交替
- body 底色 `#171c22`（画布外衬底），`.stage` 内 `--bg`
- 禁旧色系：`#0078D4` `#003D6B` `#E8F4FD` `#B85450` `#009624`（大小写均禁）

## 2. 骨架（结构序逐字一致）

```
body(#171c22) > .viewport(fixed 居中) > .stage#stage(1920x1080, padding:36px 64px 88px)
  .topline      logo 左 + meta 右（汇报对象/场景/日期）
  .eyebrow      章名 · P0N / 总页数
  h1            页面标题
  .concl        结论条：--band 底 + 左 4px --pri 边
  .main         grid 7fr 5fr（左图表区 / 右 .stack 卡片区）
  .notes        话术容器，display:none，footer 之后 stage 闭合前
footer.bar      64px 固定底：左 .tag（页码+章名+场景），右 prev/next
```

- 导航按钮：`a.btn` 白底描边；next 加 `.pri`（--pri 底白字）；首页 prev / 末页 next 用 `<span class="btn">`（无 href，且保留 `id="nav-prev"` / `id="nav-next"`，CSS `span.btn{opacity:.45}` 即禁用态），键盘翻页脚本须判 `tagName==='A'` 再跳
- `.stack` 右栏 `overflow-y:auto` + 细滚动条（`::-webkit-scrollbar` 6px）
- 每页独立自包含：自带 token、fit 壳、`.notes`、lightbox，双击可单开

## 3. 动画契约

- 入场：`[data-enter]` rise（opacity 0→1 + translateY 12px→0，.55s ease-out），stagger 90ms 递增
- SVG 节点：`.anim-pop`（scale .92→1 + fade，160ms/个 stagger）
- 连线：`.anim-draw`（stroke-dasharray/dashoffset 描线）；**箭头必须分离**为独立 `polygon.anim-head`（scale 1.5→1 + fade），delay = 所在线 delay + 描线时长，禁止 marker 随线渐显
- 虚线语义线描线：dasharray 已被虚线图案占用，不能直接用 `.anim-draw`；用 mask reveal——`<mask>` 内 rect 以 CSS 几何属性（y/height 或 x/width）沿线的方向生长，delay 走 `--i` 阶梯，reduced-motion 降级为满尺寸
- 循环流向：`.anim-flow`（dashoffset 无限循环，仅流向语义线）
- 数字：count-up（JS 递增；无 JS 时 HTML 内直接是终值）
- 预算：每页动效 ≤3 类、`animation` 声明 ≤40 条
- `prefers-reduced-motion: reduce` 全降级为即时可见（animation:none + opacity:1）
- 强制执行：箭头分离与虚线 mask reveal 由 `scripts/lint_deck_html.py` 检查 #8 硬检查
  （anim-draw/anim-fade 带 marker-end → FAIL；stroke-dasharray 虚线配 anim-draw/anim-fade → FAIL；
  anim-flow 豁免）。新制页与旧源拷贝页一律过 lint，prose 登记不等于合规

## 4. 箭头与图元规格

- marker 统一：`markerWidth="15" markerHeight="10.5" viewBox="0 0 10 7" markerUnits="userSpaceOnUse"`，orient auto
- 语义线色：主数据/能力流 --pri；控制/触发 橙 `#ea580c`；转换/标准化 紫 `#9333ea`；存储/读取 绿 `#059669`；异步/离线 灰虚线
- 图区底部放图例行（线样+语义名）

## 5. 右栏组件契约（禁文字平铺）

右栏 `.stack` 内信息块禁止整段 `<p>` 平铺，按语义选组件（CSS 统一插入 `.notes{display:none}` 之前）：

- `.stat`：量级/结论数字（`<b>` 34px --pri + `<span>` 单位说明；`.bad`/`.good` 变体色）
- `.kv`：键值对照（左 `span` mut / 右 `b` ink，逐行分隔线）——职责边界、类比映射、参数对照
- `.key`：重点句（--band 底 + 左 4px --pri 边，加粗）——本页必须记住的一句话
- `.vs`：双列对比（`>div.good` 绿 / `>div.bad` 红 / 中性白，各带 `h4` + `ul`）——正解 vs 反模式、选型对比
- `.steps`：有序流程（`ol` 编号圆圈 + 竖线，`li` 内 `<b>` 节点名 + 说明）——链路、演进路径、步骤
- `.bars`：CSS 条形图（`.row` = 88px 标签 + `i` 条 `--w` 控宽 + 64px 数值）——占比/吞吐对比
- `.fx`：公式条（`.lhs` 阶段实色块 + `.eq` 等号 + `.term` 胶囊 + `.plus` 加号，每式一行 flex）——公式/定义式（A = B + C 组合）
- `.quote`：引用块（`::before` 大引号 + 语义变色强调 span，--band-l 底圆角）——纯引用/证言；链式主张（A → B → C 演进式单句论断）按文字散文改图条直落页内小 SVG，不占 .quote
- `.pit`：行级问题对策对（`grid 1fr 28px 1fr`：`.bad` 红底问题 + `.arw` 箭头 + `.good` 绿底对策）——避坑/风险对策行对
- `.grid2` + `.mini`：2 列网格迷你卡（`b` 类别名 pri + `span` 内容；`.minis` 单列变体；`i` 人设/别称 mut；`span.lim` 边界/代价 err；`.mono` 等宽代码）——属性枚举、格式对照、多库/多方案卡片清单
- 复用既有：`chips`（枚举标签）、`table`（结构化多列）、`pre`（代码/公式）、`details`（折叠明细）、`shots`（实拍图）
- 文字散文改图：链路/流向类散文（A → B → C → 多输出）优先画页内小 SVG（静态线 + 分离 polygon 箭头，无 anim 类不触 lint #8），不堆文字；小 SVG 的 viewBox 宽度须接近渲染容器宽度（右栏约 700px），使图内 font-size 即实际 12-14px 档——viewBox 过窄会等比放大字号脱离全页字档；主轴/注释箭头用水平细线（stroke ≤1.5）+ 小箭头（头长 ≤10），禁歪斜粗大箭头

判定：右栏任一卡片内连续 ≥2 句散文且无上述组件承载 → 违例，改写为组件。每页自包含：页内使用任一组件前必须确认该页 CSS 含其定义（grep `.chip{`/`.mini{` 等），缺则随组件补丁一并插入——组件使用无 CSS 定义会静默退化为裸文本。

## 6. 脚本与交互（每页必带）

- fit 壳：`scale(min(innerWidth/1920, innerHeight/1080))`，resize 监听
- 键盘：←/→ 翻 prev/next（判 A 标签）
- lightbox：`figure img` 点击放大（`.lb` 遮罩 + img），Esc/遮罩点击关闭，`body.lb-open` 锁滚动
- 素材图：按页面相对输出目录的实际层级回退到 `<输出目录>/assets/`（多页形态 pages/ 下为 `../assets/`，test-run 参照目录按实际深度）+ `onerror` 缺图降级占位
- 明细数据用 `<details>` 折叠，summary 蓝字 ▶ 前缀；折叠取舍口径：删掉该卡本页结论仍成立则折叠（补充细则、笔记章节展开、素材图参照），不成立则常驻（定义、职责表、代码示例）；全 deck 统一执行，不逐页临场改口径
- 交互反馈（每页必带）：`a.btn`/`summary` 带 `transition:background .15s`；hover 态 `a.btn:not(.pri):hover,summary:hover{background:var(--band)}`、`a.btn.pri:hover{background:var(--pri-d)}`；键盘焦点 `a.btn:focus-visible,summary:focus-visible{outline:2px solid var(--pri);outline-offset:2px}`
- 框类 hover 微放大（每页必带，覆盖全部框类组件含封面页）：小框（prin/fx/pit/stg/阶段胶囊/角色卡等）`scale(1.03)`、大容器（card/chart/主张条等）`scale(1.01)`，均 `transition:transform .15s ease`；SVG 框类组加 `transform-box:fill-box;transform-origin:center` 保中心缩放
- 编写期依赖检查：委派 `robot-aiot-interactive-html-author` 写页前必须跑其执行前依赖检查（ui-ux-pro-max 齐备），并用 ui-ux-pro-max 的 search.py 检索设计数据资产核对风格/交互缺口；检索结果仅为数据建议，不得覆盖本文件 token 与硬约束

## 7. 验收（批次必跑）

1. `scripts/lint_deck_html.py` 逐页 FAIL=0（含 .notes 防泄漏检查 + 设计质量硬检查：#9 组件使用必有页内 CSS 定义、#10 平铺散文/长 li ul 禁（.notes 话术区豁免）、#11 :focus-visible 与 hover 反馈必在）
2. `scripts/check_deck_batch.py <pages目录>`：stage 1920x1080 / footer.bar / h1 / fit / reduced-motion / data-enter>3 / --pri 在位 / DOM≤500 / lightbox 齐备 / 禁色零命中
3. `scripts/shoot_anim.py <pages目录> <输出目录>`：virtual-time-budget 100 与 6000 双时间点截图，逐页字节须有差异；母稿登记的静态页以 `--static-pages` 传入 `check_deck_batch.py` 与 `shoot_anim.py` 豁免动画触发检查，字节无差异属合法；t6000 留作目检底图
4. `scripts/check_notes_hidden.py <pages目录>`：iframe 加载后全量 `getComputedStyle(n).display==='none'` 且零泄漏
5. 终态截图（t6000）逐页目检：内容全量可见、导航/禁用态正确、无话术泄漏
