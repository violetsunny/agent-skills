# 拆分模式：长章拆概览+子页家族 / 新文档新建家族

适用：既有单页过长需拆分，或新文档体量≈整章需新建子页家族。实测来源：LLMentor-handbook ch19 拆分（用户「太长了，可以拆分出两个」）与 ch13 家族新建（14 篇 AgentScope 文档）。新建/重建模式走 SKILL.md 与 rebuild-mode.md；本文件是拆分场景的完整约束，与 rebuild-mode.md 叠加生效（verbatim/sha/assets/量化验收同样适用）。

## 1. 触发与决策（question 让用户拍板，不自行定粒度）

两条路径：

- **新建家族**：新文档体量≈整章 → 母页保留概述 + 新建 N 个子页。选项给「两子页（推荐）/单子页/原地扩充」。
- **拆概览+子页**：既有单页过长 → 母页压 stub + 内容搬子页。

决策依据可量化：字符数 / 篇数 / 自然语义边界（如 LangChain|LangGraph 分界）/ 全站入链盘点。question 至少覆盖三个决策点：① 子页数与切分边界；② 母页 stub vs 删节（推荐 stub，入链不断）；③ 是否为子页新建 archify 图（助手可推荐不新建，用户拍板）。

## 2. 程序化 verbatim 切节（禁重打文字）

切块脚本放交付项目 `.scratch/`（过程性工具，不进 skill），核心纪律：

1. `re.split(r'(?=<div class="section">)')` 按节切原页 HTML，逐字搬运。
2. **切块前先把 body 截到 `<div class="pagenav">` 之前**——否则末块吞掉 pagenav/footer/`</body></html>`，搬进子页又留在母页，div 失衡 + 页尾重复（实测 ch19 概览 div 18/19）。
3. 执行前逐项核实脚本假设：日期常量、CSS 选择器正则（如 `.diagram-frame.frame-2`）、死代码行。
4. 执行输出三页 chars/ids/iframe 计数，供验收比对。
5. **脚本是再生真源**：定高/结构改动必须同步脚本常量（实测高度 1880→1920 改了产物没改脚本，重跑会回退）。

## 3. 母页 stub 与锚点

- 母页被搬走的节压 stub：保留 `<h2 id="sNN">` 原标题 + 1–2 句摘要 + 「完整内容见 ChX-N」深链。**母页全部原 id 保留**，跨页入链（如 ch20→ch19.html#s02）不断。
- 母页保留节（知识地图/学习路径/文档清单）不动。
- 子页锚点从 s01 重新编号（ch19-2 的 s01 = 原 s05）；子页 anchor-chips 与新 id 一一对应。
- 节间引用改跨页深链：原「（见第 06 节）」→ `ch19-2.html#s02`。

## 4. 图号惯例

- **母页 = 图 X-0，子页 = 图 X-1..N**。拆分时母页原图号让位（19-1→19-0）。
- 改号前 grep 全站确认引用范围才动。
- 回查既有家族有无重复图号遗留（实测 ch13 母页与 ch13-1 都叫「图 13-1」，两张不同的图——早期未确立惯例的遗留，发现即报用户）。

## 5. 家族导航与 index

- 子页 topnav：brand + 页名 + 目录 / ← 本章首页 / 下一页 →；末页 pagenav 指向下一章；eyebrow「Chapter X · 主题 · Step NN/MM」。
- 母页：topnav 加增量入口，s01 加学习路径卡（链子页），相关节加交叉深链，doclist 扩充收录新篇。
- index 导航页：章卡改家族样式「CHX · 概览+N 细节页」+ 子页编号链接行；统计篇数同步。改卡用 `assert count==1` 精确替换。index 是 assets 禁令唯一例外（导航页自身 + assets/style.css，存量不阻塞）。

## 6. 拆分专属验收（替换逐页相等口径）

- **外链守恒改家族并集**：`fam_root = re.sub(r'-\d+$', '', page)`，家族 = 根页 + 同名 `-N` 子页；外链在家族内不丢失即通过。逐页 href 条数相等会误报（拆分把外链搬子页，母页归零属正确行为）。
- 文件名变更归一化：源文件改名（如加 ✅ 前缀）后旧 href 更新属正确行为，比对前归一化前缀；URL-encoded 链接先 `urllib.parse.unquote`。
- HEAD 内容包含审计：块级比对旧版，intentional miss 白名单（subtitle 重写/figcap 改号/外链改名/节间引用改深链）之外丢失 = 0。
- 结构校验：ids==chips、标签平衡、assets 0、深链全通。
- 其余按 rebuild-mode.md §6（sha/geometry/bottom）+ SKILL.md 第 5 步双轨验证。

executable：`scripts/wrap_up_scan.py`（家族并集口径内置，新建子页不在 git 基线时自动 SKIP 不误报）+ `scripts/family_review_checks.py <root> --pages 母页.html 子页... [--expect expect.json]`（ids==chips/规则合规/深链/标签平衡恒跑；锚点序列/内容分布/doclist 逐字并集/图号映射走 expect；index 自身 assets 是唯一存量例外）。