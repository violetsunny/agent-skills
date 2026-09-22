# 五演示 Skill 验证清单（多轮验证修复参考）

适用对象：`self-skills/` 下五个 skill——
A = `robot-aiot-draw-flowchart`（v6.0.0，静态图表，无动画/GIF）
B = `robot-aiot-arch-diagram`（保留动画/GIF 链）
IHA = `robot-aiot-interactive-html-author`
PPT = `robot-aiot-ppt-presentation-workflow`（v4.1.0）
WEB = `robot-aiot-web-presentation-workflow`（v3.0.0）

仓库根：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills`（下文 `$R`）
运行时镜像：`~/.agents/skills/<skill 名>/`

## 使用方法与判定规则

1. 每轮验证按本清单逐项打勾；FAIL 项必须给证据：`文件:行号 + 最短决定性引文`。
2. 白名单命中 = 合法保留，不判 FAIL；白名单外命中一律 FAIL。
3. 修复后必须跑「回归三件套」：签名 grep 清零 + 门禁实跑 exit 0 + rsync/diff SYNC-OK。
4. 本机无 `rg`，用 grep 工具或系统 grep；zsh 变量不分词，多目录用数组。
5. 跑 python 一律 `PYTHONDONTWRITEBYTECODE=1`，结束前删 `__pycache__`。

### 根因教训（历轮漏检模式，验证时优先覆盖）

| # | 教训 | 对策 |
|---|---|---|
| 1 | 同源文件一侧修了另一侧漏修（第 2 轮补漏 24 项根因） | 任何 A/B 同源修复必须双侧镜像检查（M2） |
| 2 | 修复补丁落错节（裁决 A 限定语误落 studio 节，signal 节漏改 → I19） | 修复后按签名 grep 验证落点，不只验证「改过」 |
| 3 | grep 中文关键词漏英文措辞（abstain / Fallback only 假阴性） | 签名同时含中英文关键词 |
| 4 | subagent 汇报丢失但工作已落地 / 汇报落地但工作实际未做 | 不信汇报，主 agent 签名 grep 抽验 |
| 5 | 大改动（删文件/改名）引入悬空引用 | 手术后全仓悬空引用扫描（D1） |
| 6 | 声明与包内容不符（animation.md「不随包」但脚本在包里） | 文档声明与 ls 实态对照（B1/B2） |

---

## 一、全局横向验证项（五 skill 逐一跑）

**G1 运行时镜像一致性**
```bash
for s in robot-aiot-draw-flowchart robot-aiot-arch-diagram robot-aiot-interactive-html-author robot-aiot-ppt-presentation-workflow robot-aiot-web-presentation-workflow; do
  diff -r --exclude='_mideameta.json' --exclude='__pycache__' --exclude='.DS_Store' $R/self-skills/$s ~/.agents/skills/$s && echo "$s SYNC-OK"
done
```
通过标准：五个全 SYNC-OK。修复后同步命令：
`rsync -a --delete --exclude='_mideameta.json' --exclude='__pycache__' --exclude='.DS_Store' $R/self-skills/<s>/ ~/.agents/skills/<s>/`

**G2 旧名清零**
grep `leadership-ppt|robot-aiot-leadership-ppt-workflow|phase1-data-pool|phase2-audience-layering` → 五 skill 零命中（docs/ 目录不在范围）。

**G3 CLAUDE/codex 残留**
grep `CLAUDE\.md|codex`（大小写不敏感）→ 白名单外零命中。
白名单：①「codex-cli 永不自动选择」2 处（IHA content-imagery-and-infographic.md、B ai-image-generation.md——防御性路由禁令，裁决保留）；② IHA assets/onboarding-map.json 的 Codex 枚举（多宿主兼容矩阵数据，豁免）；③ PPT phase5-ppt-delivery.md「同时具备光栅页框清单与 Codex」（ppt-master routing.md 术语事实引用，合法）。

**G4 繁体字清零**
grep `類|產|圖|頁|設|樣|請求項` → 零命中。白名单：B style-guide.md 繁中标签节的字体栈演示样本（「請求項比對」等为繁中渲染示例文本，合法）。

**G5 TODO/FIXME 清零**
grep `TODO|FIXME|XXX` → 白名单外零命中。
白名单：① IHA scripts/fetch_images.py:91-92（运行时 manifest 占位，提示人工补许可）；② IHA swiss-layout-system.md「— 01 / XXX」（版式编号示例）；③ PPT brand-spec.md `#XXXXXX`（色值占位符）。

**G6 垃圾文件清零**
`find $R/self-skills/<五 skill> -name '__pycache__' -o -name '.DS_Store' -o -name '*.pyc'` → 零命中。（其他 skill 目录如 stock-replay-workbench 的既有 __pycache__ 不在范围。）

**G7 语法门禁**
五 skill 全部 `.py` 跑 `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile`；`.sh` 跑 `bash -n`；`.js` 跑 `node --check` → 全部通过。

**G8 自包含红线（交叉引用白名单）**
grep 五 skill 互引，仅允许：PPT→`robot-aiot-draw-flowchart`/`ppt-master`；WEB→`robot-aiot-arch-diagram`/IHA；A/B→`archify`/`diagram-design`/`ui-ux-pro-max`（硬门依赖）；自名引用合法；「上层 workflow」「调用方」泛称合法。禁止：两 workflow 互提、依赖 skill 指向上层 workflow 名、跨工作流区别说明、IHA 引用其他 4 skill 名。

**G9 英文散文清零（中文化，裁决 a+b 全量）**
扫描各 references/*.md 围栏外「≥5 连续英文单词且无 CJK」行 → 零命中。
白名单：触发短语引用（`- English:` 行）、产品名/许可证、代码字面量与报错原文、路径/命令/配置键、draw.io style 属性串、双语节标题、Style-N 风格名、排印术语（serif/sans/uppercase 等）、表格中属性名/值单元格。

**G10 死链/死锚**
① 全部 .md/.py/.sh 中相对路径引用（references/、templates/、scripts/、assets/）逐一验证文件存在；example-*.html、fixtures/、assets/index.html 类应有「不随包分发」注记。
② 锚点引用可达：中文节标题锚点格式为 `#中文标题`（GitHub 规则：去空格连字符化）；历史死锚 `#korean-labels`、`#traditional-chinese-labels`、`#terminal-skin-opt-in-alternate` 必须零命中。
③ 孤儿文件：每个 references 文件至少被 SKILL.md 或其他 references 导航引用（A doctor.md 挂 SKILL.md:123）。

**G11 版本一致性**
SKILL.md frontmatter version 与文内声明一致：A=6.0.0、B=2.4.0、IHA=1.12.0、PPT=4.1.0、WEB=3.0.0。功能删减升 major，修复升 patch。

---

## 二、同源镜像验证（A ↔ B）

A/B 约 84 对同源 references 文件。合法差异白名单（diff 后逐 hunk 判定，仅此几类）：
- 自名引用（各自 skill 名）与 `.diagram-design` 命名空间
- A 独有：Mermaid/excalidraw 导入、xml-html 桥接注记、draw.io XML 路径能力声明（color-schemes:5）、39 类索引、自动化自检注记、模板口径（template.html 含 h1/eyebrow）
- B 独有：动画/GIF 链全部内容（animation.md、motion-effects、Max motion 预算行、Animation 段、template-motion 步骤、fireworks/lint-skin 交付门豁免）、type-waterfall（40 类）、grouped-container-style 字号例外、excalidraw 检查节（doctor）
- fixtures「不随包分发」注记措辞差异

**M1 同源对 diff**：84 对逐对 diff，剩余差异全部落在白名单内。
**M2 修复签名双向同步**：任何一侧的修复（参数对齐/豁免声明/裁决落地/中文化），另一侧同名文件必须同步检查。核对签名清单：arcSize 允许集 {4,6,8}、间距允许集 {20,24,32,40,48}、shadow 禁令（唯一例外 style-6 feDropShadow）、Google Fonts 条件注入、87 icons、暖系主/#0078D4 辅谱系、PNG 双路径互指、dashed 语义扩展+箭头双源裁决+中性工具色豁免（style-consistency 与 color-schemes 规则 10/11 双侧在位）、分层图例外预算段（B design-system）、图例底部放置（B layered-architecture）。
**M3 文档同步门禁**：两侧 `scripts/verify-docs-sync.py` 实跑 exit 0。
**M4 precheck 一致**：两侧 `precheck_deps.sh` 逐字节相同（archify+diagram-design+ui-ux-pro-max 三依赖硬门，exit≠0 中止），实跑 exit 0。

---

## 三、draw-flowchart 专项（A，v6.0.0 静态口径）

**D1 动画/GIF 链删除完整性**
已删 10 文件不存在：scripts/{verify-motion.py, lint-skin.py, test-verify-motion.py, motion.py, svg2gif.js, fireworks.py, fireworks_geometry.py}、assets/template-motion.html、references/{animation.md, motion-effects.md}。
全仓悬空引用 grep `gif-motion|svg2gif|verify-motion|lint-skin|animation\.md|motion-effects|template-motion|fireworks` → 白名单外零命中（含 B 侧与其他 skill 对 A 的引用）。
白名单：① self_check.py motion 条件分支代码与 docstring（:25/:214/:287，无害保留）；② type-loop 图表类型语义（loop 图非动画）与 templates/type-loop.yaml；③ 否定式禁令（「禁用 GIF」「不做动画」「静态版不做…」）；④ interactive_html.py prefers-reduced-motion（viewer 无障碍降级）；⑤ MOTION_INTENSITY 设计刻度（恒静态）；⑥ deck 壳入场动画 CSS（slide-deck-interactive.html/slide-page-template.md/slide-premium-*——交互预览非动图，裁决保留）；⑦ type-scatter/verify-beeswarm 的 CSS motion path（定位属性禁令）；⑧ type-medallion「promotions」子串假命中；⑨ B 侧全部自引用。

**D2 diagram_geometry 改名一致性**
`scripts/diagram_geometry.py` 存在；validate_svg.py 与 generate-from-template.py `import diagram_geometry`；A 侧 `fireworks_geometry` 零命中（B 侧保留 fireworks_geometry.py 合法）。

**D3 data-generator 标记同步**
写入方 generate-from-template.py 与读取方 validate_svg.py 均用 `robot-aiot-tech-graph`；A 侧 `fireworks-tech-graph` 零命中（B 侧保留合法）。

**D4 包完整性门禁**：`python3 scripts/verify-plugin-package.py` exit 0。
**D5 自检门禁**：`python3 scripts/self_check.py assets/template.html` exit 0。
**D6 SKILL.md 结构**：version 6.0.0；description 无 GIF 字样；tags 无 gif-motion；硬约束编号连续；`##` 章节完整；导航无死链；「GIF|动图」仅否定式语境。
**D7 样式值合规**：references 中 `shadow=1` 零命中（唯一例外 style-6 feDropShadow 登记）；arcSize ∈ {4,6,8}。白名单：draw.io XML 路径百分比语义的 `arcSize=15`（3 处既有豁免声明覆盖，与 SVG rx 允许集不同属性体系）。
**D8 间距允许集**：{20,24,32,40,48}；80px 仅豁免登记处。
**D9 Google Fonts 条件注入**：零外链基准段在 design-system §5「模板默认零外链」；联网发布限定+`&amp;` 转义；export.md 排障条目为「替换是预期行为不是错误」口径；dark-svg-techniques:267 为指针式。
**D10 87 icons**（非 41）：type-it-state 与 robot-icons 一致。
**D11 调色板谱系**：暖系为主、#0078D4 蓝系为辅（限设备/云语义/用户要求），color-schemes:3 与 robot-icons:5 声明在位。
**D12 PNG 双路径分工互指**：export.md（HTML 产物导出）↔ png-export.md（SVG 光栅化）头部分工声明。

---

## 四、arch-diagram 专项（B，动画链保留）

**B1 动画链完整**：scripts/{verify-motion.py, lint-skin.py, test-verify-motion.py, motion.py, svg2gif.js, fireworks.py, fireworks_geometry.py}、references/{animation.md, motion-effects.md}、assets/template-motion.html 全部存在。
**B2 声明与实态一致**：animation.md 为「self_check.py 日常门禁；verify-motion.py/lint-skin.py 完整校验器随包分发」口径（禁「不随包」失实声明）。
**B3 CHROME_PATH 统一**：svg2gif.js 读 `CHROME_PATH`，`FIREWORKS_CHROME_PATH` 作 fallback。
**B4 门禁**：verify-docs-sync.py、precheck_deps.sh 实跑 exit 0；全部 .py py_compile。

---

## 五、interactive-html-author 专项（IHA）

**I1 裁决 A 严格单色系**：visual-style-presets.md + swiss-layout-system.md 全文件 grep「反转|翻面|交替|dark 页|light 页」逐处判定——页级主题切换语义零命中；组件级 accent 反转必须带「组件级反转，非页级主题反转/全 deck 仍单主题」类限定。
白名单：① studio :532「双表面反转」深度手段描述（look :529 已限定）；② 否定式/禁止式条款（禁逐页互换等）；③ 选中态/按压态反转；④ 纬度反转（地图语义）；⑤ 明度阶梯推导规则；⑥ mood 路由标签；⑦ multi-version 版本间色彩策略（非 deck 内翻面）；⑧ 非主题语义交替（旋转角/节点填充/色相轮转/贝塞尔/能量/几何/叙事）；⑨ web-slide-strategies「页内节奏由 ink 反转块制造」（「页内」已限定）。
重点回归位：signal :487-497、studio :529-539、kraft-journal :579（同表面+组件级限定）、grove :301、emerald-editorial :277/:280/:284/:287、mat :327、stencil-tablet :523、swiss token :587/:601/:615/:629「ink 反转块——组件级」、swiss-layout-system :30/:52。
**I2 41 套预设**：§2.1-§2.41 编号连续无跳号；SKILL.md「41 套」计数一致。
**I3 导航完整**：SKILL.md 链接全部 references（20 个），零孤儿。
**I4 依赖红线**：其他 4 个 skill 名零命中（「上层 workflow」泛称合法）。
**I5 关键文件在位**：templates/lightbox.js、deck-skeleton.html、deck-nav.js；图片点击放大（SKILL.md lightbox 登记）、path-draw 三坑+入场同步三条款（animation-fx-catalog.md）、Mermaid 构建期渲染失败降级不静默丢图（diagram-embed-rendering.md）。
**I6 语法**：19 .py + 1 .sh + 21 .js 全过。

---

## 六、ppt-presentation-workflow 专项（PPT）

**P1 六阶段链路**：源文件→反问（页数/汇报对象/汇报范围/演讲时长）→母稿 G1→图表 G2→回写母稿→ppt-master 生成；description 与正文反问清单一致（含演讲时长，裁决保留）。
**P2 受众四档**：领导层/技术同行/外部客户/大众（未指定默认领导层）——description、反问清单、正文三处+phase1 表四行一致。
**P3 外部引用前缀**：引 draw-flowchart 文件带 `robot-aiot-draw-flowchart/references/` 前缀或 `~/.agents/skills/` 绝对路径（重点：ppt-image-and-cover.md :92/:99/:156、slide-layout-strategies.md、phase4-page-authoring.md）。
**P4 母稿禁动效**：SKILL.md、phase2-manuscript.md、templates/ppt-manuscript.md 三处禁动效标注在位；全链路禁动画禁 Chart.js。
**P5 间距规范**：phase5 px÷2 换算、行距倍数换算在位。
**P6 门禁**：全部 .py py_compile、.sh bash -n；keynote_verify.sh 为 slide images 直出 PNG 口径（本机无 poppler，渲染终审 WPS 人工）。

---

## 七、web-presentation-workflow 专项（WEB）

**W1 六阶段链路**：反问五项（页数/对象/范围/场景/交付形态，无演讲时长——与 PPT 不串台）；G1/G2/回写/生成顺序一致。
**W2 --static-pages 豁免三处登记**：SKILL.md:192、phase2-pagination.md:23、phase4-style-lock.md §7 验收清单；shoot_anim.py 与 check_deck_batch.py 参数实现。
**W3 母稿动效备注节**：每页必带（SKILL.md、phase2-pagination.md、templates/deck-manuscript.md；lint_manuscript.py 缺失 FAIL）。
**W4 phase4-style-lock**：ui-ux-pro-max 转述保留（裁决）；search.py 归属明确为 ui-ux-pro-max；r4-anim-p01-p10 参照为「存在时可作参照」口径。
**W5 showcase 两页确认门**：SKILL.md 登记在位。
**W6 门禁**：全部 .py py_compile。

---

## 八、裁决来源索引

| 裁决 | 内容 | 落地位置 |
|---|---|---|
| 13 项裁决（2026-09-22） | ①archify 入 precheck 硬门 ②.diagram-design 命名空间保留 ③英文 references 中文化 ④孤儿脚本挂文档 ⑤孤儿 references 补导航 ⑥演讲时长保留 ⑦showcase 门登记 ⑧ui-ux-pro-max 转述保留 ⑨「上层 workflow」泛称保留 ⑩暖系主/蓝系辅 ⑪PNG 双路径分工 ⑫CHROME_PATH 统一 ⑬其余小项全修 | commit 91ef3f33 |
| 裁决 A 严格单色系 | 全 deck 全 light 或全 dark，禁页级翻面；页内组件级 accent 色块反转允许（须带限定）；非主题语义交替合法 | 91ef3f33 + 63e2590b（signal）+ 06a36938（I19 批） |
| 中文化 a+b 全量 | 同源不一致对齐 + 双侧同英文全译；散文中文，代码/路径/属性名英文 | 06a36938 + 2487f17b |
| 动画/GIF 归属 | draw-flowchart 无动画无 GIF（v6.0.0 删 10 文件）；动画+GIF 仅 arch-diagram 与 IHA；deck 壳翻页动画属交互预览保留；fireworks_geometry→diagram_geometry（静态几何库）；标记 fireworks-tech-graph→robot-aiot-tech-graph | 06a36938 |
| flowchart-patterns 声明 | 「历史示意」声明非用户要求→示例改合规值（shadow=0/arcSize=8），声明删失实措辞 | 06a36938 |
| codex-cli 禁令 | 防御性路由规则保留，非残留 | 判定保留 |
| onboarding-map Codex | 多宿主兼容矩阵数据，豁免 | 判定保留 |
| 历史四需求 | PPT 间距换算、Web path-draw 延迟特效三条款、图片点击放大 lightbox、禁平铺组件化（lint #10） | 已固化，见 I5/P5/W3 |

## 九、提交与同步规程

1. 修复只改 `self-skills/`（唯一真源），提交格式 `FIX:/FEAT:/CHORE: <标题> JIRA: main DIFF: <详述>`，禁止 push。
2. 提交前：rsync 五 skill → diff SYNC-OK → 回归三件套 → `git status` 确认无 __pycache__/.DS_Store 混入。
3. `_mideameta.json` 仅安装侧有，rsync 必 exclude，不回写仓库。
4. 市场端 skillId SKILL_CS30SK20260814000011855853 仍绑旧名注册、description 为旧版（含 GIF 字样）——重新发布/下架待用户决定；`docs/skills-overview.md` 待 sync skill module 5 再生成。
