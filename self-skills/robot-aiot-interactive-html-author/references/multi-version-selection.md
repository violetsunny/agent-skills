# 多版本并行设计与选优

## 定位

同一份真实内容并行产出三个视觉方向真正分叉的完整实现，评审后选定一个方向，再单向收敛到交付。
本文件管"什么时候发散、怎么发散、怎么评、怎么收"；单版实现规则见 `interactive-html-authoring.md`，合格性审查见 `premium-review-fix.md`，预设与旋钮见 `visual-style-presets.md`。

发散是昂贵动作：三份完整实现的代价约等于一版的三倍。判据不成立时不做，直接走单版流程。

## 一、适用场景与触发条件

### 该做多版本并行

| 场景 | 判据 |
|---|---|
| 用户点名要方向对比 | 出现"想看几个方向""多做几版对比""先出方案再定"等表述 |
| 风格未定 | `visual-style-presets.md` §1 mood 路由表圈不出唯一预设，或圈出的候选在 14px swatch 下难分辨 |
| 客户/领导口味不明且返工代价高 | 董事会、外部客户、发布会、投标等高风险汇报；反复改的成本高于并行三版 |
| 第一版被否但说不清要什么 | 用户给出否定但无具体方向，猜测式返工命中率低 |
| 同一内容需多形态分发 | 对内汇报版 + 对外传播版，两版受众与密度模式不同 |
| 内容与版式匹配存在真实分歧 | 同一批数据既能走演讲型也能走阅读型，且分歧无法靠摆事实消解 |

### 不该做

| 场景 | 走什么 |
|---|---|
| 已锁定登记版式（每页 `<section>` 带已登记 `data-layout` S01-S22 / M01-M10）且用户未要求换方向 | `premium-review-fix.md` 三步流程 |
| 用户已点名预设或给出明确风格参考且只要一版 | 直接单版实现，锁定该预设 |
| 单页微调：改文案、改数据、修溢出、调间距 | 直接改，改完跑四值实测 |
| 预算不足以产出三份完整实现 | 一版完整优于三版半成品；如实告知用户预算不足 |
| 已进入 4 Pass 收敛阶段 | 不回开发散，见第六节选择无效铁律 |

## 二、三方向硬门

三个版本必须在视觉方向上真正分叉。同一骨架换三套配色不是三方向，是无效发散。

### 分叉维度清单

| 维度 | 档位示例 | 分叉判据 |
|---|---|---|
| 版式骨架 | 单栏陈述 / 分屏对照 / 网格矩阵 / 全幅 hero；登记版式取 S 系或 M 系不同家族 | 三版骨架不同族；登记版式 deck 至少两版 `data-layout` 属不同家族 |
| 色彩策略 | 浅底单锚 / 深底反转 / 多色轮换 / 全墨单色 | 底色明暗档不同，或 accent 数量与面积占比不同 |
| 字体性格 | 系统衬线金句 / 全 sans 细字重巨字 / mono 数据主导 / 中英双语上下堆叠 | 标题字族不同，或字重档相差 ≥200 |
| 动效能量 | 静（仅翻页）/ 低（入场 + 数字滚动）/ 中（+ ambient 呼吸）/ 高（+ canvas FX） | 动效分层数量不同档；"高"档仅在用户明确要求扩展特效时可选 |
| 信息密度 | 演讲型（每页 ≤1 焦点、填充 ≤50%、必读 ≥40px）/ 阅读型（网格填满、正文 ≥16px） | 密度模式二分取不同档，见 `web-slide-strategies.md` |

### 硬门规则

1. 三版必须在 ≥3 个维度上取不同档位，逐维填表留档，不靠感觉宣称"风格不同"
2. 版式骨架与信息密度这两个维度中，至少有一个三版互不相同。只换配色、只换 accent = 无效发散，回 Phase 2 重做
3. 每版锁定一套预设（`visual-style-presets.md` §2），全程不混用第二套；登记版式 deck 每版锁定一个版式家族，不跨 S/M 混用
4. 14px swatch 可辨：三版首页缩略图并排压到 14px 高仍能一眼分辨；分辨不出即分叉不足
5. 三版构成固定为 1 安全款（最贴受众）+ 1 bold 款（高张力）+ 1 wildcard 款（跨情绪）
6. 每版写专属禁区：全局 AI 痕迹清单之外，该方向在自身语境下不许出现的东西。示例——全墨极简方向禁渐变与阴影；粗野网格方向禁圆角与柔和过渡；杂志编辑方向禁霓虹与等宽正文；浅底单锚方向禁第二 accent
7. 每版只允许一个 signature 元素，boldness 花在这一处，其余保持纪律（见 `anti-ai-slop-design.md`）

## 三、7 Phase 工作流

### Phase 1 · brief

- 输入：用户需求原文、母稿或四要素、品牌资产、图表真源
- 产出：一份 8 字段 brief（第四节模板），三版共用
- 纪律：字段缺失先问清再动手，不猜；受众未指定时默认领导层并在 brief 中写明这是默认值

### Phase 2 · 三方向发散

- 输入：brief、`visual-style-presets.md` §1 mood 路由表
- 产出：三张方向卡（分叉取值表 + 专属禁区 + signature 元素 + 一句话立意）
- 纪律：先填分叉维度表再过第二节硬门；三阶收敛读文件——先读路由表圈候选，再读候选条目 look/pick-when，仅对进入实现的方向读条目全文，不通读四十一套

### Phase 3 · 各自完整实现

- 输入：方向卡 + brief + 同一份真实内容与图表真源
- 产出：三份独立自包含 HTML，每份双击可运行、零外部请求
- 纪律：
  1. 三份都用真实标题、真实数据、真实话术，禁 lorem、禁占位注释、禁"同上"省略
  2. 三份可并行分派子任务；分派时每份 brief 必须写明"不要重复其他方向的美学"，否则趋同
  3. 每份各自遵守 SKILL.md 全部硬约束（scale-to-fit 壳、`.notes` 承载话术、reduced-motion 降级、单页 DOM ≤500）
  4. 某份失败或缺关键产出：同 brief 重启该份，不用另一份的实现补位；部分完成（缺截图）由主线补，不重启
  5. 等待期间主线做实事：修已确认的 bug、写评审表骨架、准备并排预览容器，不空转

### Phase 4 · 并排预览

- 输入：三份完整实现
- 产出：并排预览（三文件 + 一个仅含三个真实链接的入口页，或三张 1920×1080 首页截图并排）+ 每版一句话立意
- 纪律：
  1. 同一份内容、同一画布、同一数据，唯一变量是视觉方向
  2. 截图走 `interactive-html-authoring.md` headless 验证方法论条 4 的命令模板，加 `--force-prefers-reduced-motion` 取确定性终态
  3. 截图与预览一律不带 `?tweaks=1`；导出用 `?noscale` 取画布原始尺寸
  4. 预览真实性铁律：上屏文字只出现将真实交付的内容，预设名、token 名、旋钮档位、方向代号不上屏

### Phase 5 · 多维评审

- 输入：三份实现 + 并排预览 + 四值实测记录
- 产出：评审报告（每版每维分数、加权总分、六视角各一句话、出局名单与理由）
- 纪律：先过合格门再打分（第九节）；对比度实算不目测；溢出/nav-safe 侵入以实测值判定

### Phase 6 · 选优

- 输入：评审报告
- 产出：选定方向 + 落选版本封存记录 + 分歧说明（如有）
- 纪律：按第六节决策规则执行；分数接近时摆出冲突让用户裁决，不自行平摊、不折中混合

### Phase 7 · 微调收敛

- 输入：选定版本 + 评审报告中的未修项
- 产出：单一交付文件 + `premium-review-fix.md` 格式的审查报告（含 overflowPx / bottomWhitespacePx / titleGapPx / navSafeIntrusionPx 四值）
- 纪律：4 Pass 单向推进（第七节），每 pass 只动一类，改完即测；需要探索参数空间时挂调参面板（第八节），落定值回写 token

## 四、8 字段 brief 模板

```text
1. 受众：<领导层 / 技术同行 / 外部客户 / 大众；写清具体角色与决策权。未指定时默认领导层，并注明是默认值>
2. 场景：<会议室投屏 / 桌面自阅 / 线上传播 / 展会大屏；含时长、观看距离、是否有演讲者>
3. 核心信息：<一句话主张 + 3 条支撑；全部真实内容，禁占位>
4. 情绪基调：<克制严肃 / 高燃发布 / 学术安静 / 人文温暖 …，对应 mood 路由表一行>
5. 禁忌：<品牌禁用色、客户明确否过的元素、竞品既视感、行业 cliché>
6. 交付形态：<单文件 deck / INDEX.html + pages/ / 单页交互页 / 竖版社交 deck>
7. 画布：<1920×1080（默认）或 810×1080 竖版；nav-safe 底部 86px 与分页圆点 bottom 22px 是否适用>
8. 动效预算：<静 / 低 / 中 / 高；入场总时长上限、过渡 400-600ms、是否允许 ambient 与 canvas FX>
```

每方向追加一张方向卡：

```text
方向立意：<一句话，用户视角，不含内部工作流词汇>
分叉取值：版式骨架=? | 色彩策略=? | 字体性格=? | 动效能量=? | 信息密度=?
预设锁定：<一套预设名 或 一个登记版式家族>
专属禁区：<3-5 条>
signature 元素：<1 个>
```

## 五、6 视角评审 + 5 维打分

### 六视角（每个视角只问自己那一件事）

| 视角 | 只问什么 |
|---|---|
| 决策者 | 30 秒内能否读出核心结论与要批的事；有没有把风险与代价讲清；能不能直接拿去做决定 |
| 设计师 | 层级是否一眼可辨；间距是否落在 8px 基线；圆角与字级是否成体系；signature 元素是否只有一处 |
| 工程师 | 是否零外部请求；动画属性是否只有 transform/opacity/filter；非活跃页有无残留定时器与 rAF；单页 DOM 是否 ≤500；控制台是否干净 |
| 受众代表 | 以 brief 第 1 字段的真实身份看：术语是否解释、字号在真实观看距离是否可读、有没有让人出戏的元素 |
| 品牌守门 | 品牌色是否被改动、logo 是否变形、是否出现品牌规范禁用元素、整套是否一致不漂移 |
| 可访问性 | 正文对比度是否 ≥4.5:1、大字 ≥3:1；语义是否只靠颜色传达；标题层级是否连续；reduced-motion 是否真降级 |

### 五维打分（各 1-5 分）

| 维度 | 1 分 | 3 分 | 5 分 |
|---|---|---|---|
| 信息传达 | 读不出主张，需人讲解 | 主张可见但被装饰稀释，层级模糊 | 30 秒读出主张与支撑，视线零摩擦 |
| 视觉张力 | 模板套皮，无 signature | 有一处亮点，整体平 | 有从内容长出的独有母题，缩略图仍可辨 |
| 品牌契合 | 品牌色被改或出现禁用元素 | 不冲突但无品牌识别 | 品牌资产被用作结构元素，识别度高 |
| 技术稳健 | 打不开/白屏/溢出/报错 | 可运行但有残留定时器或非合成属性动画 | 零外部请求、四值实测全过、reduced-motion 真降级 |
| 受众适配 | 术语与字号都不对路 | 大体合适，个别页出戏 | 密度模式与观看距离匹配，受众无需翻译 |

### 受众权重表（加权总分 = Σ(分×权重) / Σ权重，保留两位）

| 受众 | 信息传达 | 视觉张力 | 品牌契合 | 技术稳健 | 受众适配 |
|---|---|---|---|---|---|
| 领导层（未指定时默认） | 5 | 2 | 3 | 3 | 4 |
| 技术同行 | 5 | 2 | 2 | 4 | 4 |
| 外部客户 | 4 | 3 | 5 | 3 | 4 |
| 大众 / 公开传播 | 3 | 5 | 4 | 3 | 4 |

### 一票否决（先于加权总分）

1. 技术稳健 = 1（打不开、白屏、控制台报错、内容溢出画布、navSafeIntrusionPx > 0）→ 该版出局，不进排名
2. 品牌守门判定违反品牌规范硬条款 → 该版出局
3. 可访问性视角实测正文对比度 < 4.5:1 → 先修再评，不带着不达标项打分

## 六、选择无效铁律

选优一旦落定，落选版本立即失效。

1. 落选版本移入 `variants/` 留档，交付目录只保留选定版；留档不参与后续任何取材
2. 禁止把落选版的 token 值、组件、版式骨架、动效档、配色、文案样式拷进选定版。理由：预设与登记版式是成套锁定的，跨版取材必然造成圆角档、accent 数、字重阶梯、动效能量不一致，`premium-review-fix.md` 的一致性阻塞项当场挂掉
3. 若发现"选定版的骨架 + 落选版的配色更好"，说明方向选错：回 Phase 2 重开一轮，把该组合作为新的安全款完整实现，不在两个成品之间做拼接
4. 例外——内容层不属于风格元素，可自由复用：真实数据、文案、话术、图表真源。图表真源恒以 `robot-aiot-arch-diagram` 产出为准，不参与选优、不允许任何版本重绘
5. 例外——多形态分发（对内版 + 对外版）允许保留两个版本，但每个用途各自锁定一套，互不取材，各自独立走完 4 Pass
6. 收敛阶段不回开发散：进入 Phase 7 后不再新增方向、不再换预设；需求确实越界时回 Phase 2 重锁，不在收敛中打补丁

### 选优决策规则

- 加权总分差 ≥0.5 → 取高分版
- 差 <0.5 → 比"决策者视角"单项，取高者
- 仍平 → 摆出两版的取舍点让用户裁决，不平摊、不折中
- 用户裁决与评审结论冲突时，如实说明冲突点与代价，按用户裁决执行

## 七、4 Pass 微调收敛

顺序不可颠倒，每 pass 只动一类，改完立刻实测再进下一 pass；不连改两轮再验（对齐 `premium-review-fix.md` 修完反查）。

### Pass 1 · 结构

- 动什么：版式骨架内的模块顺序、模块取舍、拆页与合页、`data-layout` 归属
- 检查：每页仍为已登记编号；Bento 格子数 = 内容条目数、无空格子；无"三个等大功能卡片横排"；主线语义不互相覆盖
- 禁止：改页面契约（标题/结论/上屏内容/话术）、改图表真源、动色彩与动效
- 实测：overflowPx、bottomWhitespacePx、titleGapPx、navSafeIntrusionPx 四值

### Pass 2 · 排版

- 动什么：字级档位、字重、行高、对齐、间距基线、文案长度
- 检查：字级梯度相邻差 ≥2px；中文大标题按 `typography.md` 第三节分档；任何文字守住第四节下限 18/16/14px；数字 `tabular-nums` 且同列对齐；kicker 在大标题上方
- 禁止：靠降字号解决拥挤（拥挤走文案压缩、拆页、换更高容量登记版式）；引入第三字族
- 实测：titleGapPx（两段式 65-86px，章节级 ≥97px，<54px 为阻塞；封面/仪式页豁免，判读见 `premium-review-fix.md` title gap 节）

### Pass 3 · 色彩

- 动什么：token 变量值、accent 归属、surface 明暗档、阴影色调
- 检查：强调色唯一；无 AI 紫/霓虹渐变、无纯黑硬阴影；灰阶冷暖不混用；主色块上文字走成对 `on-primary`，与主色实算 ≥4.5:1；同一 deck 明暗节奏不连续 3 页同主题
- 禁止：在组件里散落硬编码 hex；页面配色与图表真源冲突时改页面（以图表为准）
- 实测：WCAG 相对亮度公式实算对比度，渐变底/图片底上的小字取背景最暗点

### Pass 4 · 动效

- 动什么：入场顺序与延迟、过渡时长与缓动、ambient 幅度、数字滚动时长
- 检查：动画属性仅 transform/opacity/filter（进度条 width 除外）；瞬态不循环、持续随页启停；过渡 400-600ms、入场总时长 ≤2s；reduced-motion 下降级为即时切换；非活跃页无残留定时器与 rAF
- 禁止：新增 canvas FX 或扩展特效（除非用户明确要求）；用动效掩盖结构问题
- 实测：入场播完后（翻页约 2-3s）做 sweep_static 静默扫查；headless 加 `--force-prefers-reduced-motion` 跑交互断言

## 八、调参面板（tweaks panel）

评审与 Pass 2-4 期间挂一个实时调参面板，让用户不改代码就能看到参数空间。面板是工具不是交付物：`?tweaks=1` 才注入，不带参数时零 DOM、零样式痕迹。

### 面板纪律

1. 最多 4-6 个旋钮，再多就变成配置页，失去快速探索的意义
2. 默认值必须是完整可交付的设计：面板全归零时页面就是成品
3. 旋钮暴露有思考的离散/受限区间，不做"全区间随便拖"（例：圆角给档位选择，不给 0-50px 滑杆）
4. 字号倍率只向上（1.00-1.20）：下限是硬约束，拥挤走文案压缩与拆页，不靠缩字号
5. 面板自身样式允许硬编码颜色（它不属于 deck 视觉系统）；调参结果必须回写 token 变量，面板色值不带进页面
6. 面板挂在 body 直属、`.fit-viewport` 之外，不参与 scale-to-fit 缩放，不占画布 nav-safe 区域；默认折叠，不遮内容、不抢翻页热区
7. 面板输入受既有键盘守卫保护（`interactive-html-authoring.md` 键盘绑定对 input/textarea/select 的豁免），拖动滑杆不触发翻页；不额外绑定 Esc，避免与 lightbox / 退出全屏冲突
8. 截图矩阵、headless 断言、打印导出一律不带 `?tweaks=1`；`@media print` 下面板隐藏
9. 落定即固化：把最终参数写回 `:root` token 与 CSS 字面值，交付文件不依赖面板存在

### deck 侧接线（必须写进页面 CSS）

```css
:root {
  --tw-font-scale: 1;
  --tw-gap-scale: 1;
  --tw-motion: 1;
}
.slide h1        { font-size: calc(99px * var(--tw-font-scale)); }
.slide .lead     { font-size: calc(20px * var(--tw-font-scale)); }
.slide .body     { font-size: calc(18px * var(--tw-font-scale)); }
.slide .caption  { font-size: calc(16px * var(--tw-font-scale)); }
.card-grid       { gap: calc(24px * var(--tw-gap-scale)); }
.block           { padding: calc(32px * var(--tw-gap-scale)); }
.slide .enter {
  transition:
    opacity calc(500ms * var(--tw-motion)) cubic-bezier(0.4, 0, 0.2, 1),
    transform calc(500ms * var(--tw-motion)) cubic-bezier(0.4, 0, 0.2, 1);
}
```

WAAPI 动画用 `window.twDur()` 取时长，不写字面量：

```js
el.animate(
  [{ opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'translateY(0)' }],
  { duration: twDur(600), easing: 'cubic-bezier(0.165, 0.84, 0.44, 1)', fill: 'both' }
);
```

未接线的动画不受动效旋钮影响；接线范围以"用户能感知的时长"为准，翻页过渡、入场、数字滚动、ambient 四类必须接线。

### 面板完整实现（原生 JS + CSS，零依赖，置于 `</body>` 前）

```js
(function () {
  'use strict';

  var QS = new URLSearchParams(location.search);
  if (QS.get('tweaks') !== '1') return;

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var STORE_KEY = 'deck-tweaks';
  var DEFAULTS = { fs: 1, gap: 1, hue: 0, mo: 1 };
  var RANGE = {
    fs:  { min: 1,    max: 1.2,  step: 0.01 },
    gap: { min: 0.85, max: 1.3,  step: 0.01 },
    hue: { min: -40,  max: 40,   step: 1 },
    mo:  { min: 0.5,  max: 1.6,  step: 0.05 }
  };
  var LABEL = { fs: '字号倍率', gap: '间距倍率', hue: '色相偏移', mo: '动效时长' };
  var HUE_TOKENS = ['--primary-color', '--secondary-color', '--tertiary-color'];
  var CONTROLS = [
    { key: 'fs',  fmt: function (v) { return v.toFixed(2) + 'x'; } },
    { key: 'gap', fmt: function (v) { return v.toFixed(2) + 'x'; } },
    { key: 'hue', fmt: function (v) { return (v > 0 ? '+' : '') + v + '\u00B0'; } },
    { key: 'mo',  fmt: function (v) { return v === 0 ? 'off' : v.toFixed(2) + 'x'; } }
  ];

  function clamp(k, v) {
    v = Number(v);
    if (!isFinite(v)) return DEFAULTS[k];
    return Math.min(RANGE[k].max, Math.max(RANGE[k].min, v));
  }

  function readState() {
    var stored = null;
    try { stored = JSON.parse(localStorage.getItem(STORE_KEY) || 'null'); } catch (e) { stored = null; }
    var s = {};
    Object.keys(DEFAULTS).forEach(function (k) {
      if (QS.has(k)) s[k] = clamp(k, QS.get(k));
      else if (stored && stored[k] != null) s[k] = clamp(k, stored[k]);
      else s[k] = DEFAULTS[k];
    });
    if (REDUCED) s.mo = 0;
    return s;
  }

  var state = readState();

  function parseHex(v) {
    var m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(String(v).trim());
    if (!m) return null;
    var h = m[1];
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    var n = parseInt(h, 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
  }

  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var d = max - min, l = (max + min) / 2, h = 0, s = 0;
    if (d !== 0) {
      s = d / (1 - Math.abs(2 * l - 1));
      if (max === r) h = ((g - b) / d) % 6;
      else if (max === g) h = (b - r) / d + 2;
      else h = (r - g) / d + 4;
      h *= 60;
      if (h < 0) h += 360;
    }
    return { h: h, s: s, l: l };
  }

  function hslToHex(h, s, l) {
    h = ((h % 360) + 360) % 360;
    var c = (1 - Math.abs(2 * l - 1)) * s;
    var x = c * (1 - Math.abs((h / 60) % 2 - 1));
    var m = l - c / 2;
    var seg = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x]
            : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
    var to = function (v) {
      var t = Math.round((v + m) * 255).toString(16);
      return t.length === 1 ? '0' + t : t;
    };
    return '#' + to(seg[0]) + to(seg[1]) + to(seg[2]);
  }

  var baseHsl = {};
  var cs = getComputedStyle(document.documentElement);
  HUE_TOKENS.forEach(function (k) {
    var rgb = parseHex(cs.getPropertyValue(k));
    if (rgb) baseHsl[k] = rgbToHsl(rgb.r, rgb.g, rgb.b);
  });

  function currentUrl() {
    var p = new URLSearchParams(location.search);
    p.set('tweaks', '1');
    Object.keys(state).forEach(function (k) {
      if (state[k] === DEFAULTS[k]) p.delete(k); else p.set(k, String(state[k]));
    });
    return location.pathname + '?' + p.toString() + location.hash;
  }

  function persist() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* 无痕模式不可用：URL 仍是唯一真源 */ }
    try { history.replaceState(null, '', currentUrl()); }
    catch (e) { console.warn('[tweaks] replaceState 不可用，请从地址栏手动复制参数：' + e.message); }
    var link = document.getElementById('tw-link');
    if (link) link.href = currentUrl();
  }

  function apply() {
    var rs = document.documentElement.style;
    rs.setProperty('--tw-font-scale', state.fs.toFixed(2));
    rs.setProperty('--tw-gap-scale', state.gap.toFixed(2));
    rs.setProperty('--tw-motion', state.mo.toFixed(2));
    Object.keys(baseHsl).forEach(function (k) {
      var b = baseHsl[k];
      rs.setProperty(k, hslToHex(b.h + state.hue, b.s, b.l));
    });
    CONTROLS.forEach(function (c) {
      var input = document.getElementById('tw-' + c.key);
      var out = document.getElementById('tw-' + c.key + '-o');
      if (input && Number(input.value) !== state[c.key]) input.value = String(state[c.key]);
      if (out) out.textContent = c.fmt(state[c.key]);
    });
    persist();
  }

  var CSS_TEXT = [
    '#tw-panel{position:fixed;right:20px;bottom:20px;z-index:9999;',
    'font:13px/1.5 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;color:#1a1a1a}',
    '#tw-panel *{box-sizing:border-box}',
    '#tw-toggle{border:0;border-radius:9999px;background:#1a1a1a;color:#f5f3ef;padding:8px 16px;',
    'font:inherit;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.18)}',
    '#tw-toggle:focus-visible{outline:2px solid #1a1a1a;outline-offset:2px}',
    '#tw-body{margin-bottom:10px;padding:16px;width:288px;background:#fff;',
    'border:1px solid rgba(0,0,0,.12);border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.16)}',
    '.tw-row{display:grid;grid-template-columns:66px 1fr 54px;align-items:center;gap:8px;margin-bottom:12px}',
    '.tw-row label{color:#555}',
    '.tw-row output{text-align:right;font-variant-numeric:tabular-nums}',
    '.tw-row input[type=range]{width:100%;margin:0;accent-color:#1a1a1a}',
    '.tw-row input[type=range]:disabled{opacity:.4}',
    '.tw-foot{display:flex;gap:8px;align-items:center;margin-top:4px}',
    '.tw-foot button,.tw-foot a{flex:1;padding:6px 8px;border:1px solid rgba(0,0,0,.14);border-radius:8px;',
    'background:#f5f3ef;color:#1a1a1a;font:inherit;text-align:center;text-decoration:none;cursor:pointer}',
    '.tw-foot button:hover,.tw-foot a:hover{background:#eae7e0}',
    '.tw-hint{margin:10px 0 0;color:#666;font-size:12px}',
    '@media print{#tw-panel{display:none !important}}'
  ].join('\n');

  var rows = CONTROLS.map(function (c) {
    var r = RANGE[c.key];
    return '<div class="tw-row">' +
      '<label for="tw-' + c.key + '">' + LABEL[c.key] + '</label>' +
      '<input type="range" id="tw-' + c.key + '" min="' + r.min + '" max="' + r.max + '" step="' + r.step + '">' +
      '<output id="tw-' + c.key + '-o" for="tw-' + c.key + '"></output>' +
      '</div>';
  }).join('');

  var style = document.createElement('style');
  style.textContent = CSS_TEXT;
  document.head.appendChild(style);

  var panel = document.createElement('div');
  panel.id = 'tw-panel';
  panel.setAttribute('role', 'group');
  panel.setAttribute('aria-label', '设计调参面板');
  panel.innerHTML =
    '<div id="tw-body" hidden>' + rows +
      '<div class="tw-foot">' +
        '<button type="button" id="tw-reset">重置</button>' +
        '<button type="button" id="tw-copy">复制参数</button>' +
        '<a id="tw-link" href="#" target="_blank" rel="noopener">新窗口</a>' +
      '</div>' +
      '<p class="tw-hint" id="tw-hint"></p>' +
    '</div>' +
    '<button type="button" id="tw-toggle" aria-expanded="false" aria-controls="tw-body">调参</button>';
  document.body.appendChild(panel);

  var toggle = document.getElementById('tw-toggle');
  var body = document.getElementById('tw-body');
  var hint = document.getElementById('tw-hint');

  toggle.addEventListener('click', function () {
    var willOpen = body.hasAttribute('hidden');
    if (willOpen) body.removeAttribute('hidden'); else body.setAttribute('hidden', '');
    toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    toggle.textContent = willOpen ? '收起调参' : '调参';
  });

  CONTROLS.forEach(function (c) {
    var input = document.getElementById('tw-' + c.key);
    input.value = String(state[c.key]);
    if (c.key === 'mo' && REDUCED) input.disabled = true;
    input.addEventListener('input', function () {
      state[c.key] = clamp(c.key, input.value);
      apply();
    });
  });

  document.getElementById('tw-reset').addEventListener('click', function () {
    state = { fs: DEFAULTS.fs, gap: DEFAULTS.gap, hue: DEFAULTS.hue, mo: REDUCED ? 0 : DEFAULTS.mo };
    apply();
    hint.textContent = '已回到默认值（默认值即成品态）';
  });

  document.getElementById('tw-copy').addEventListener('click', function () {
    var url = location.href;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(
        function () { hint.textContent = '已复制当前参数 URL'; },
        function () { hint.textContent = '复制被拒绝，请从地址栏手动复制'; }
      );
    } else {
      hint.textContent = '当前环境无 clipboard API，请从地址栏手动复制';
    }
  });

  window.twDur = function (ms) { return Math.round(ms * state.mo); };

  if (REDUCED) hint.textContent = 'reduced-motion 已生效：动效时长锁定为 off';
  else hint.textContent = '动效旋钮只作用于 calc(基准 * var(--tw-motion)) 与 twDur() 接线的动画';

  apply();
})();
```

参数与 URL 键位：`fs` 字号倍率 1.00-1.20、`gap` 间距倍率 0.85-1.30、`hue` 色相偏移 -40°…+40°、`mo` 动效时长倍率 0.50-1.60。优先级 URL > localStorage > 默认值；等于默认值的键不写进 URL，`#/N/M` 深链在 `replaceState` 时原样保留。多项目共存时把 `STORE_KEY` 改成 `deck-tweaks-<项目名>`。

色相偏移从 `:root` 计算样式读取 `--primary-color` / `--secondary-color` / `--tertiary-color` 的当前值作为基准，在 HSL 空间整体旋转 H，S/L 不动；token 值不是 3 位或 6 位 hex（如 `oklch()`）时该 token 自动跳过，不报错、不写坏值。需要偏移 `oklch()` 色板时改在 `anti-ai-slop-design.md` OKLCH 派生层调 H，不走本面板。

## 九、与 premium-review-fix.md 的衔接

分工不重叠：

| 环节 | 用哪套 |
|---|---|
| 合格门（能不能交付） | `premium-review-fix.md`：第二步诊断逐项审计（排版/色彩/布局/形状与容器/内容真实性/完整性/Web 可访问性与语义）+ 交付前预检清单阻塞项 + 交互版专属审查项 + 登记版式专属校验 |
| 选优排序（哪版更好） | 本文件第五节：6 视角 + 5 维 1-5 分 + 受众权重 |
| 收敛修复（怎么改） | `premium-review-fix.md` 第三步修复顺序 + 修复红线；本文件第七节把它编排成 4 Pass |

衔接规则：

1. Phase 5 打分前先跑合格门。阻塞项未过的版本不进打分，先按其第三步修复顺序修完再评——不给带阻塞项的版本打分，否则分数没有可比性
2. 本文件 5 维不重复定义合格判据：技术稳健维直接取其阻塞项通过情况与四值实测结果；可访问性视角直接取其"Web 可访问性与语义"清单与对比度实测法
3. 登记版式 deck 的三版都跑其"登记版式专属校验"四项静态扫描（`data-layout` 登记、大标题居中拦截、SVG 可见文字拦截、nav-safe 底部安全区），扫描命令不在本文件重述
4. Phase 7 每 pass 结束按其"后验测量"取四值，审查报告逐版附 overflowPx / bottomWhitespacePx / titleGapPx / navSafeIntrusionPx；无测量记录的版本不算通过评审
5. 修复红线全程有效：不改图表真源、不改页面契约语义、不引入响应式与滚动动画、不跨页漂移、每次修复可追溯到诊断条目

## 十、自检清单

发散前：

- [ ] 触发条件命中第一节"该做"表至少一行，且未命中"不该做"表任何一行
- [ ] 8 字段 brief 无空缺；受众未指定时已注明默认领导层
- [ ] 三份实现用的是同一份真实内容与同一份图表真源，无占位、无 lorem
- [ ] 预算够产出三份完整实现（不够则如实告知并降为一版）

方向分叉：

- [ ] 分叉维度表已填，≥3 个维度取不同档位
- [ ] 版式骨架或信息密度至少一维三版互不相同
- [ ] 每版锁定单一预设或单一登记版式家族，无混用
- [ ] 三版首页缩略图压到 14px 高仍可一眼分辨
- [ ] 构成为 1 安全款 + 1 bold 款 + 1 wildcard 款
- [ ] 每版有专属禁区与唯一 signature 元素
- [ ] 动效能量"高"档只在用户明确要求扩展特效时出现

预览与评审：

- [ ] 并排预览上屏文字无内部工作流词汇（预设名、token 名、旋钮档位、方向代号）
- [ ] 截图不带 `?tweaks=1`，且加 `--force-prefers-reduced-motion` 取确定性终态
- [ ] 三版都先过 `premium-review-fix.md` 阻塞项，未过的已修完再打分
- [ ] 5 维分数按受众权重表加权，一票否决三条已逐版检查
- [ ] 分数差 <0.5 时已摆出取舍点让用户裁决，未自行平摊

收敛与交付：

- [ ] 落选版本已移入 `variants/` 留档，交付目录只有选定版
- [ ] 选定版中无任何来自落选版的 token/组件/骨架/动效档/配色
- [ ] 4 Pass 按序完成，每 pass 只动一类，每 pass 后有四值实测记录
- [ ] 调参落定值已回写 `:root` token 与 CSS 字面值，交付文件不依赖面板
- [ ] 交付文件不带 `?tweaks=1` 时零面板 DOM、零面板样式；`@media print` 下面板隐藏
- [ ] 面板接线覆盖翻页过渡、入场、数字滚动、ambient 四类时长；reduced-motion 下动效恒为即时切换
- [ ] 最终审查报告为 `premium-review-fix.md` 报告格式，结论为"可交付"
