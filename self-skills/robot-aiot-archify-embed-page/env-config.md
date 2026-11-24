# env-config — robot-aiot-archify-embed-page

本 skill 目录结构与路径的唯一真源。新增/改路径只改本文件，其他文件仅引用。

## 输出（交付物）

- 交付根：用户指定目录优先；未指定时 `<cwd>/archify-embed-<slug>-<YYYYMMDD-HHMMSS>/`
- 页面：`<交付根>/<slug>-page.html`
- archify 产物副本（iframe src 目标）：`<交付根>/<slug>-tree.html`（命名跟随 archify 产物原名）

## 生成（中间产物）

- `<交付根>/archify-source/`：candidate.json、archify finalize 产物 html、finalize/delivery/browser-check receipts

## 验证

- `<交付根>/_review/`：Chrome headless 整页截图（page-<ts>.png）、artifact 单独渲染截图、shell 分段切片、测高截图（measure-<slug>.png，measure_iframe_height.sh 第 4 参指定）
- 量化验收脚本输出（wrap_up_scan.json / shell_bottoms.json / offline_bottoms.json / family_review_output.txt）默认落扫描根目录，`--out` 可指到 `<交付根>/_review/`；bottom 截图 `--png-dir` 默认 `_bottoms`/`_bottoms_offline`（相对扫描根）
- 人工确认前禁清理；确认后只删未跟踪可再生产物，archify-source/ 回执与 candidate 是真源禁删（见 SKILL.md 清理纪律）

## 读取

- 用户提供的源材料（docx/md 绝对路径）
- `~/.agents/skills/archify/`、`~/.agents/skills/diagram-design/`（precheck 校验对象，只读）

## 临时

- `/tmp/` 仅放过程性临时文件（如 textutil 转出的 txt、未指定输出路径时的测高 png、embed_fonts.py 的 woff2/css 缓存默认 `/tmp/embed-fonts-cache`，可用 EMBED_FONTS_CACHE 覆盖）；验证产物禁放 /tmp
