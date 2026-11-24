# 重建模式：替换既有页面 / 站点

适用：交付目标是**替换已被引用的既有 html 页面**（原地覆盖），而非新目录新建页。新建模式走 SKILL.md 主流程；本文件是重建模式的完整约束。批量重建（多页流水线）时本文件 + archify-gate-fixes.md 是每票必读。长章拆分/新建子页家族叠加 split-mode.md（家族并集验收替换本文件逐页相等口径）。

## 1. 移植前清点（grep 实测，禁信票面/记忆数值）

对旧版页面逐项清点并记录基线：

- h2 数量与全部 `id`（节锚点）
- 内联 SVG 数量、代码块数量
- 内容外链（如 `../../articles/`）的 **href 条数**（不是行数——一行可含多条链接）
- 全部 class 清单（供 CSS 覆盖检查）
- **旧版真源的 git 基线 commit**：先核实（曾发生票面引用 commit 与 HEAD 不一致导致计数对不上），以实测为准

## 2. verbatim 保真

- 旧版全部节**逐字移植**：禁虚构、禁删减、禁改写正文。
- h2 **保留旧版原 id**——跨页深链（`chXX.html#sNN` 类）依赖这些 id。移植前 grep 全站入链盘点，移植后断链必须为 0（曾发生 16 页丢锚点、全站 42 处入链断链）。
- 代码块素 `<pre><code>`，去 data-lang 类装饰；代码内容（含 `// ...` 占位与 HTML 实体）原样保留。
- 内容外链 verbatim 保留，数量与旧版一致；URL-encoded 链接（`%3F` 等）存在性检查先 `urllib.parse.unquote`。
- 保真校验口径：剥标签比对文本时两侧统一用空串（不能用空格，否则大量假阳性）；void 标签（meta/link/br/img 等）不计入配对；href 属性另行多重集比对（文本 diff 不覆盖链接）。预期差异白名单：subtitle 追加句、figcap 后缀、footer。脚本：`scripts/fidelity_check.py <old> <new> --href-multiset`（白名单=--skip-classes）。
- 网页剪藏源噪声清洗配方：BOM/零宽字符剔除；语言标签残留在闭合围栏前一行（`lines[-2]`，不是 `lines[-1]`）；云效 `##### ✅标题 + 品牌词` 卡片预览剔除；UI 噪声图（如 no-search-result.png）剔除；CDN 图（cdn.nlark.com）→ `[IMG]` 占位后重表达。脚本：`scripts/clean_export_md.py`（卡片剔除须 --card-brand 指定品牌词）。
- 控制字符防误删：`strip(" \t")` 不用默认 strip——U+001F 等分隔符会被默认 strip 吃掉；页面写字面 `\u001f` 转义 + callout 说明。
- 源文含真实 apiKey 一律脱敏（→sk-xxx）后逐字块注入（HTML 转义，脚本 `scripts/inject_code_blocks.py` + blocks.json 行号表，剩余标记 exit 1）；源文自相矛盾（javadoc vs actual、步骤顺序等）不自行裁决，写 challenge/callout 标注分歧；broken table 重建并注明。

## 3. shell 自包含

- **禁任何 assets/ 引用**，验证 grep 口径 `(\.\./)?assets/`（裸前缀与 ../ 前缀都覆盖——曾只查 `../assets/` 漏掉 21 页裸引用）。
- inline CSS + 素代码块，不依赖宿主站点 js/css。
- **CSS 覆盖检查**：旧版 class 清单 → 新 shell CSS 逐项覆盖，MISSING=0 才开工；缺失组件从已完成样板页取或新建（高频缺口：有序列表、访谈/问答块、锚点 chips、subtitle 内链接）。
- 自动加载型外联（img/script/link/iframe src）必须为 0；文本型 URL（a href、代码块文本、SVG xmlns）永不 fetch，保留不动。

## 4. 原地覆盖交付（promote）

1. archify artifact 复制到页面同目录，命名加前缀（如 `archify-<页名>-<slug>.html`），避开宿主站点既有扫描 glob。
2. shell 原地覆盖旧页面（旧版靠 git 历史恢复，不留 legacy 副本——用户另有裁决时以用户为准）。
3. promote 编辑固定三处：subtitle 追加移植来源说明句；iframe src 指向同目录带前缀 artifact；figcap 按旧版文字替换。**预 promote 形态与 promote 后形态写死区分**（figcap 后缀、subtitle 追加句只在 promote 时出现），防跨票约定漂移。
4. 顶部/页内导航链接去 `../` 前缀适配根目录。

## 5. 一致性核对（sha）

- 复制即核 sha：embed 副本与 finalize 源 sha256 必须一致（曾发生断点续写后副本 STALE 仍是旧版）。
- promote 后根目录副本再核一次。
- 汇报强制带 artifact sha256 前 8 位。
- 断点续写第一步：核副本 staleness，再续做。

## 6. 量化验收（替代纯目视）

| 项 | 标准 |
|---|---|
| assets 引用 | = 0 |
| 节锚点 | 数量与 id 序列 = 旧版 h2；全站入链断链 = 0 |
| 内容外链 | **家族并集内丢失 = 0**（拆分场景逐页相等会误报，见 split-mode.md §6）；unquote 后目标全存在；文件名改名（✅ 前缀等）比对前归一化 |
| HEAD 内容包含审计 | 块级比对旧版，intentional miss 白名单（subtitle/figcap/外链改名/节间引用改深链）外丢失 = 0 |
| artifact sha | 与 receipts 一致 |
| geometry | 0 findings（扫描器 exit 0 不等于视觉通过，仍须截图联合判定） |
| shell bottom | 记录数值；异常值排查布局塌陷，不设固定阈值（长页可远超常规区间，复测排除截断即可） |

geometry 扫描：`scripts/check_svg_geometry.py <root> --include-artifacts`（默认 glob `*.html` 已含 artifact；窄 glob 时用 --include-artifacts 补齐）。`check_file(Path)` 可 import 单独调用（传 Path 对象，传 str 报 AttributeError）。

executable 入口：`scripts/wrap_up_scan.py`（锚点/家族并集/assets/sha receipt/geometry/index，problems 非空 exit 1；清理纪律保留的探针/对照 html 副本须 --exclude，否则误报 index 缺页）、`scripts/measure_shell_bottoms.py`（shell bottom）、`scripts/audit_iframe_overflow.py`（既有页 iframe 溢出批量审计，建议值须按测高 .sh 复测定高）。

分段切片的 band 区间用节偏移探针定：wrapper iframe 加载页面 + `--dump-dom --allow-file-access-from-files`，JS 输出 h2[id]/h3/.cards/.doclist/.pagenav/.footer 的 `getBoundingClientRect().top`；提取正则收紧为 `<pre id="res">RESULT::([^<]*)</pre>`（宽松正则会误匹配 wrapper 自身脚本源码）。band 相邻重叠裁切；没拍到组件主体只能报「覆盖缺口」补裁，不能猜。

## 7. 变体

- **双图页**：两个 artifact 各自独立走完整管线（各自 candidate-<slug>.json / finalize / 测高 / figcap）；第二 iframe 高度写独立 CSS 类，不共用 inline style。
- **无图页**：0 artifact、0 iframe，仅统一 shell 重建；subtitle 用「统一 shell 重构版」句式，不提 archify；geometry 不适用。

## 8. 机械替换工具绕路

cp 覆盖后 Edit 类工具会拒编辑（"has been modified since it was last read"）。promote 三处编辑用 bash 内联 python 精确替换，每处 `assert count==1`，失败即报错不静默。

## 9. 批量流水线纪律

- 管线配方与已知坑集中一份 PIPELINE 文档作单一真源，每票开工前强制先读，随发现持续更新；票面只引用不重抄。
- 已完成基线页仍须复核（geometry/相对引用/bottom/promote 编辑/sha），通过才回勾。
- subagent 无文本返回 ≠ 失败也 ≠ 成功：查产物判定实际进度，用 task_id resume 续做。
- 批量渲染用显式参数/数组逐页执行，禁 zsh `set -- $spec`（zsh 不分词，整串当 $1，window-size 参数错致截图没生成、读到旧文件误判）。
- 每票完成后主 agent grep/shasum 抽查再标 done。
- 批量交付提交前委派**独立复核票**：清单化（锚点/内容无丢失/doclist 计数逐字/图号/规则合规/深链/工具改动合理性/标签平衡），脚本 `scripts/family_review_checks.py`（通用项恒跑，期望值项 --expect expect.json，secret 通用正则不携带真实前缀）；禁整文件 Read 已嵌字体页（base64 巨大），用正则提取；git HEAD 比对区分**存量 FAIL vs 新引入 FAIL**（存量例外不阻塞本次提交，单独报）；检查脚本 + 原始输出作复核产物落盘；路径解析用 `ROOT/unquote(a).resolve().exists()`（相对路径从错误 cwd 解析会假报不存在）。
- 提交前 secret 扫描：staged diff grep key；**检测脚本用前缀模式（前 12 hex）不用完整 key**——完整 key 作检测模式会把密钥扩散进新文件（实测复核脚本自身泄漏 12 处）。
- 提交须**精确暂存本次产物路径**，提交前核验暂存区无预存无关文件（git commit 提交整个暂存区，曾混入 116MB 无关个人文件进公开仓库）；敏感/不可逆 git 操作先征得用户同意。