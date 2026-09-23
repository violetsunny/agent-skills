# env-config — 目录结构唯一真源

本技能全部输出 / 生成 / 验证 / 读取 / 临时目录只在本文件登记。SKILL.md、references/、templates/、scripts/、assets/ 仅引用登记项，不另行定义目录结构。

规则：

1. 新增目录、修改路径、调整结构 → 只改本文件；改后 grep 技能内旧路径的内联引用一并修正。
2. 正文内联路径为使用示例；与本文件冲突时以本文件为准，并修正内联。
3. 验证产物（`test-run/`）人工确认前禁止清理；`/tmp` 只放过程性临时文件，禁止放交付物与验证产物。
4. 技能安装目录自身（references/assets/scripts/templates）只读，禁止写入任何产物。

## 交付根目录

被上层 workflow 委派时用委派方指定的输出目录；未指定时默认当前运行项目的 `doc-ppt/`。下表 `<交付根>` 按此整体替换。

## 目录登记表

| 类别 | 路径 | 用途 |
|---|---|---|
| 输出 | `<交付根>/flow/<name>.xml` | draw.io 图表 XML 原始真源，不可被 HTML 反向覆盖 |
| 输出 | `<交付根>/flow/<name>.html` | XML→HTML 桥接预览稿（页面编排与 PPT 还原的视觉约束输入） |
| 输出 | `<交付根>/pages/<页码>-<slug>.html` | 静态页面 HTML，一页一文件；引用图表用 `../flow/<name>.html` 相对路径 |
| 输出 | `<交付根>/assets/` | 品牌资源与素材图（如 midea-logo.png）；图表类产物与页面 HTML 不混放于此 |
| 输出 | `./diagrams/`（当前目录在 git 仓库内）或 `/tmp/diagrams/` | `.excalidraw` 三件套导出目录（export-excalidraw.md） |
| 输出 | 与 SVG 源同目录或用户指定路径 | PNG 导出产物（generate-diagram.sh / svg2png.js） |
| 生成 | `<交付根>/_gen/precheck-robot-aiot-draw-flowchart.txt` | 被委派时 precheck_deps.sh 输出存档 |
| 验证 | `<交付根>/test-run/<批次>/` | 验证批次产物（测试页面/截图/测量报告）；人工确认前禁止清理 |
| 读取 | 用户指定源文件（.drawio/.mmd/Mermaid 块/兼容 mxGraphModel XML/MD） | 导入重绘与内容源 |
| 读取 | 技能内 `assets/template*.html`、`assets/icons/`、`assets/brand-colors.json`、`assets/dark-palette.json`、`assets/onboarding-map.json`、`assets/robot-vacuum-icon.png`、`references/`、`templates/` | 只读资源 |
| 临时 | `/tmp/svg2png-core/`、`/tmp/svg2png-puppeteer/` | svg2png 依赖 npm 安装目录（--prefix 安装 + NODE_PATH 引用） |
| 临时 | `/tmp/diagram-render-<sha256前16位>.html` | excalidraw 渲染页内容寻址暂存副本（哈希一致复用，不一致原子 mv 覆盖） |
| 临时 | `/tmp/test.png` | cairosvg 冒烟测试产物，测完即删 |
