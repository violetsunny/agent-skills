---
name: robot-aiot-archify-embed-page
description: "用 archify 出校验过的交互图、diagram-design 出 editorial 页面壳，以 iframe 原样嵌入合成完整知识页：保留 archify 全部交互（主题切换/动效/折叠/缩放/节点索引），页面壳含标题、副标题、信息卡与页脚。适用于把 docx/md 章节、知识体系、系统说明做成单页展示物，也适用于重建替换既有页面（verbatim 全内容移植+锚点保留+量化验收）与长章拆分（概览+子页家族，程序化切节+图号 X-0+家族并集验收）。执行第一动作是 precheck_deps.sh 校验两个基础 skill 与测高工具链，缺失自动安装。公司受限网络环境零外联（字体内嵌离线保真）。不适用于需要单文件自包含交付的场景（改走静态 SVG 移植路线，见 references/variants.md）。"
---

# Archify Embed Page

archify 出图（过完它自己的全部校验门）→ diagram-design 出页面壳 → archify 产物以 iframe 原样嵌入页面。两 skill 各干各的，不互相改写产物。

## 硬门（执行第一动作）

```bash
bash <skill-dir>/scripts/precheck_deps.sh
```

exit≠0 立即中止，不得降级、不得跳过。脚本校验 `~/.agents/skills/archify` 与 `~/.agents/skills/diagram-design`（缺失按 github 源自动安装后复检），以及测高工具链（Chrome、python3+PIL+numpy）。委派 subagent 执行本 skill 时，precheck 输出落盘 `_gen/precheck-robot-aiot-archify-embed-page.txt`。

## 模式路由（先读再动手）

- **新建模式**（默认）：新目录两文件交付，页面壳=标题+信息卡+iframe+页脚。走下面主流程。
- **重建模式**：替换已被引用的既有页面（原地覆盖、全章 verbatim 移植、锚点保留、量化验收）。先读 `references/rebuild-mode.md` 再动手，主流程第 3/5/6 步以该文件为准。
- **拆分模式**：长章拆概览+子页家族，或新文档体量≈整章新建家族。先读 `references/split-mode.md` 再动手，与重建模式约束叠加生效。
- **单文件自包含**：用户明确要求时不走 iframe，改走 `references/variants.md` 静态 SVG 移植路线。
- **公司受限网络**：shell 零外联是铁律（外联尝试即触发 DLP 告警，无论成败）。字体保真与断网验证见 `references/offline-env.md`。

## 路线边界

- iframe 内是 archify 原生配色与交互；页面壳是 diagram-design tokens。两者只做到**近似统一**（同为 light 或同为 dark），不做像素级统一。
- 交付为**两文件**：页面 html + 同目录 archify 产物 html。iframe 用相对路径 src，移动目录必须整目录移动；**单独移动/复制页面壳做对照或验证必断 iframe**（破图灰框易误判为其他缺陷），临时对照文件放页面同目录。

## 流程

### 1. 材料提取

docx 用 `textutil -convert txt -output <tmp> <file.docx>`；md 直接读。定位目标章节起止行，截取章节全文作为图与卡片的内容源。禁止凭记忆补内容。重建模式另做旧版清点（rebuild-mode.md 第 1 节）。

网页剪藏源另做保真处理（rebuild-mode.md §2 有完整配方）：噪声清洗（BOM/零宽/语言标签/卡片预览/UI 噪声图/CDN 图占位，脚本 `scripts/clean_export_md.py`）；控制字符防误删——`strip(" \t")` 不用默认 strip（U+001F 分隔符会被吃掉）；真实 apiKey 一律脱敏后逐字注入（HTML 转义，脚本 `scripts/inject_code_blocks.py` + blocks.json 行号表）；源文自相矛盾不自行裁决，写 challenge/callout 标注分歧。

### 2. archify 出图

按 archify SKILL.md 原生流程：选 type → 写 candidate.json（`meta.locale` 跟随材料语言）→ `finalize <type>` 过 validate/deliver/check/browser-check 四门。非零退出不是成功，按 archify 修复流程处理。

**嵌入场景选型与预检先读 `references/archify-gate-fixes.md`**：优先 workflow/architecture；tree 在 3.2.0 下视口拉伸禁默认用于嵌入；dataflow 异常高画布回落 workflow；timeline 强制 ISO 日期=编造陷阱；return/error 边不写 route；col≤5、canvas≤1240 写 candidate 前预检。

产物放交付目录的 `archify-source/` 子目录（candidate.json、<slug>.html、各 receipt 都在内）。双图页 candidate 命名 `candidate-<slug>.json` 防互覆。

### 3. 页面壳

以 `templates/iframe-page.html` 为骨架（diagram-design full editorial：衬线标题、无衬线正文、信息卡、页脚；默认系统字体栈零外联，品牌字体用 `scripts/embed_fonts.py` 内嵌）。tokens 用 diagram-design 默认或用户指定品牌；信息卡 3–4 张，宽度不等（如 `1.1fr 1fr 0.9fr 0.9fr`），内容全部取自材料原文，禁止编造。

全内容 shell（全章逐字移植+节锚点+组件族）是重建模式标准形态，见 rebuild-mode.md。

### 4. iframe 嵌入与定高

1. 把 archify 产物 html 复制到页面同目录，**复制即核 sha256 与源一致**。
2. 定 iframe 内宽：**禁公式推算**（旧「容器宽−边框=1198」口径已证伪——body/container padding 都减内宽，本模板窗口 1200 下实为 1134）。用探针在真实页面上下文读 `iframe.clientWidth`（临时 wrapper 复刻 shell 的 padding/container，或在页面临时副本注入探针）。
3. 测内容真实高度（饱和 scrollHeight 法）：

   ```bash
   bash <skill-dir>/scripts/measure_iframe_height.sh <archify-html> <内宽> 24000 <交付目录>/_review/measure-<slug>.png
   ```

   脚本用 wrapper iframe 读 scrollHeight，从矮壳高向上扫取最后溢出值作内容估计，建议高度=估计+2（vh 联动跳档自动迭代）；再自动做高窗口（≥12000）wrapper 截图 + 右缘灰条扫描验证，有滚动条自动加高重验。输出 `content_height` 与 `suggested_height`。
4. exit 93 = 须人工裁决：tree 100vh 拉伸 → 改 workflow 重出图；**不饱和 reader-area 类**（scrollH=壳高+常数，加高溢出不变）→ 禁改 height，报用户按现状交付。禁止拍脑袋定高。
5. 填入模板 `{{IFRAME_HEIGHT}}`。sequence 类 100vh 居中产物用 harness 读 scrollHeight（gate-fixes.md）。拆分脚本是再生真源：定高改动须同步脚本常量（split-mode.md §2）。

### 5. 验证（双轨，不依赖 headless iframe 合成）

headless 对 iframe 的合成行为随 Chrome 版本变化（实测结论反转过两次），整页截图里 iframe 区域可能空白——**不得把整页截图当 iframe 内容的唯一判据**。双轨：

1. **artifact 单独渲染**：按 iframe 精确尺寸（内宽×定高）单独截图产物，Read 目视验图语义与节点索引完整。
2. **shell 分段 crop**：整页截图（宽=容器宽，`--virtual-time-budget=6000` + offline-env.md 断网参数全套）后裁非 iframe 区段切片，目视验排版、cards/footer 在 container 内。长页必须分段切片，不许只看缩略整页。

截图存 `<交付目录>/_review/`。偶发空白渲染（仅滚动条边缘带）重试；bottom 触画布边加大 `--window-size` 重拍。分段切片相邻 band 重叠裁切保证整页覆盖；**band 没拍到组件主体只能报「覆盖缺口」补裁，不能猜 PASS/FAIL**。滚动条判定用右缘灰条像素扫描（客观判据，测高脚本已内置高窗口第三上下文验证），不靠目视。重建/拆分模式另过 rebuild-mode.md §6 量化验收（锚点/外链家族并集/assets/sha/geometry/bottom/HEAD 内容包含审计）。几何扫描 exit 0 不等于视觉通过，须与截图联合判定。委派目视复核 subagent 时：清单化（A–H 项）+ 报告落盘 + 回复 ≤15 行 + 修复后闭环补记。

量化验收脚本入口（均在 `scripts/`，输出默认落扫描根目录，`--out` 可指到 `_review/`）：

```bash
python3 <skill-dir>/scripts/wrap_up_scan.py <root>            # 全站一致性：锚点/家族并集/assets/sha receipt/geometry/index，problems 非空 exit 1
python3 <skill-dir>/scripts/check_svg_geometry.py <root> --include-artifacts   # SVG 遮盖/箭头埋入
python3 <skill-dir>/scripts/fidelity_check.py <old> <new> --href-multiset      # verbatim 文本 + 链接多重集
python3 <skill-dir>/scripts/audit_iframe_overflow.py [页面...]  # 既有页 iframe 溢出批量审计（建议值须按测高 .sh 复测定高）
python3 <skill-dir>/scripts/measure_shell_bottoms.py <root> [--offline --baseline <json>]  # 整页 bottom / 离线比对
python3 <skill-dir>/scripts/family_review_checks.py <root> --pages 母页 子页... [--expect expect.json]  # 拆分家族独立复核
```

### 6. 交付说明

回复给：页面链接、archify 源产物链接、artifact sha256 前 8 位、iframe 定高与 content_height、验收清单（人工核对卡片文字与原文、iframe 交互可用）、已知边界（非单文件、近似统一、合成页不受 archify 校验门覆盖）。重建/拆分模式按 rebuild-mode.md / split-mode.md 汇报各项计数。

## 输出目录与清理

见 `env-config.md`（五类路径唯一真源）。用户指定交付目录时以用户为准，内部子目录结构不变。

人工确认后的清理纪律：验证/review 截图**默认全部删除**（含已入库的 `git rm`；用户偏好 2026-11-24 升级），保留 py 脚本/html 探针副本/woff2 缓存；用户另有裁决时以用户为准。删前 `git ls-files` 核查跟踪状态；`archify-source/` 的 candidate 与 receipts 是图源真源，**禁整目录删除**；内容素材（assets/images）与验证截图严格区分。批量重建后提交须精确暂存本次产物路径，防暂存区预存无关文件混入；**提交前 secret 扫描**（staged diff grep key 前缀；检测脚本自身禁用完整 key 作模式，防密钥扩散进新文件）。

## 禁止

- 禁止改写 archify 产物 html 的任何字节（iframe 依赖其完整性；其内文本型 URL 永不 fetch，不是外联）。
- 禁止在页面壳里内联 archify 的 SVG/脚本（那是 variants.md 的静态路线）。
- 禁止跳过 finalize 直接用 candidate 渲染。
- 禁止 precheck 未过就开工。
- 禁止 shell 自动加载型外联（远程字体/css/js/img）；headless 验证禁止不带断网参数。