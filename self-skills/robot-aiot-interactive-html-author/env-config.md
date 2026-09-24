# env-config — 目录结构唯一真源

本技能全部输出 / 生成 / 验证 / 读取 / 临时目录只在本文件登记。SKILL.md、references/、templates/、scripts/、assets/ 仅引用登记项，不另行定义目录结构。

规则：

1. 新增目录、修改路径、调整结构 → 只改本文件；改后 grep 技能内旧路径的内联引用一并修正。
2. 正文内联路径为使用示例；与本文件冲突时以本文件为准，并修正内联。
3. 验证产物（`test-run/`）人工确认前禁止清理；`/tmp` 只放过程性临时文件，禁止放交付物与验证产物。
4. 技能安装目录自身（references/assets/scripts/templates）只读，禁止写入任何产物。

## 输出根目录

被上层 workflow 委派时用委派方指定的输出目录；独立使用时由用户指定。下表 `<输出根>` 按此整体替换。

## 目录登记表

| 类别 | 路径 | 用途 |
|---|---|---|
| 输出 | `<输出根>/<project>-presentation.html` | 单文件多页 deck（默认交付形态，自包含零依赖双击可运行） |
| 输出 | `<输出根>/INDEX.html` + `<输出根>/pages/<页码>-<slug>.html`（如 01-cover.html） | 多页形态（上层 workflow 明确要求时）：总纲导航壳（MANIFEST + iframe 视口）+ 逐页独立自包含 HTML，导航链接真实存在 |
| 输出 | `<输出根>/<project>-landing.html` | 落地页 / 滚动叙事页形态（用户或上层 workflow 点名时）：1440px 基准响应式连续长页，无翻页纵向滚动，规格见 `references/content-imagery-and-infographic.md`「落地页 / 产品官网形态」 |
| 输出 | `<输出根>/<project>-doc.html` | 文档形态 PDF 排版源 HTML（用户点名文档形态时）：`@page` A4 排版后导出 PDF，规格见 `references/content-imagery-and-infographic.md`「文档形态 PDF」 |
| 输出 | `<输出根>/assets/` | 素材图（fetch_images.py `-o assets/` 落盘；manifest.json 同目录，许可字段人工补填，许可不明的图不用） |
| 生成 | `<输出根>/_gen/precheck-robot-aiot-interactive-html-author.txt` | 被委派时 precheck_deps.sh 输出存档 |
| 验证 | `<输出根>/test-run/<批次>/` | 验证 deck、动画触发截图、验证报告；验证 deck 不受动画预算约束但豁免必须在验证报告中显式声明；人工确认前禁止清理 |
| 读取 | 调用方输入：页面四要素/母稿片段、图表 HTML/SVG、主色基调 | Phase 输入，不改节点坐标与数据语义 |
| 读取 | 技能内 `references/`、`templates/`（deck-skeleton.html、deck-nav.js、lightbox.js、presenter-window.js 等）、`assets/palettes.json` | 只读资源 |
| 临时 | `/tmp/deck.pdf` | pdf_page_count.py 打印页数中间产物 |
