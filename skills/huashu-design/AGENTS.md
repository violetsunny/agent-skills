# AGENTS.md

## 这是什么

huashu-design 是一个 **AI agent skill**（不是应用程序）。核心产物是 `SKILL.md`（582 行，agent 读的主文档）+ `references/`（33 篇按需加载的子文档）+ `assets/`（Starter Components）+ `scripts/`（导出工具链）。设计目标是让任意支持 markdown skill 的 agent（Claude Code / Codex / Cursor 等）用 HTML 产出高保真设计交付物。

## 没有 build / test / lint

- `package.json` 只有 4 个依赖（`playwright` `sharp` `pptxgenjs` `pdf-lib`），**无 scripts 字段**，不是构建配置。
- 仓库没有测试框架、linter、typecheck。`test-prompts.json` 是手工测试用例清单，不是自动化测试。
- 修改 `SKILL.md` / `references/` 后无需运行任何验证命令——它们是给 agent 读的纯文本指令。

## 安装依赖（仅 export 脚本需要）

核心设计流程（HTML 产出）零依赖。以下依赖仅用于 `scripts/` 里的导出工具：

```bash
npm install                    # playwright + sharp + pptxgenjs + pdf-lib
# Python 脚本用 uv 或 pip:
pip install python-pptx Pillow requests  # pptx_from_rendered.py, fetch_images.py
# 系统级:
brew install ffmpeg             # render-video.js / convert-formats.sh / add-music.sh
npx playwright install chromium # 浏览器截图与渲染
```

## 关键脚本（scripts/）

| 脚本 | 作用 | 典型调用 |
|------|------|---------|
| `render-video.js` | HTML 动画 → 25fps MP4（中间产物） | `node scripts/render-video.js demo.html out.mp4` |
| `render-video-seek.js` | 逐帧 seek → 真 60fps 确定性 MP4 | `node scripts/render-video-seek.js demo.html out.mp4 --fps=60` |
| `convert-formats.sh` | MP4 → 60fps 插帧 + palette 优化 GIF | `bash scripts/convert-formats.sh input.mp4` |
| `add-music.sh` | MP4 + BGM 混音 | `bash scripts/add-music.sh input.mp4 assets/bgm-tech.mp3` |
| `export_deck_pdf.mjs` | 多文件 HTML deck → PDF（矢量可搜） | `node scripts/export_deck_pdf.mjs slides/ out.pdf` |
| `export_deck_pptx.mjs` | HTML → 可编辑 PPTX（路线 A，HTML 未写时用） | `node scripts/export_deck_pptx.mjs slides/ out.pptx` |
| `pptx_from_rendered.py` | HTML → 可编辑 PPTX（路线 B，HTML 已写好时用） | `python3 scripts/pptx_from_rendered.py demo.html out.pptx` |
| `html2pptx.js` | DOM 逐元素 → PowerPoint 对象（被 export_deck_pptx.mjs 调用） | 不单独调用 |
| `fetch_images.py` | Wikimedia/Unsplash 取公共领域图片 | `python3 scripts/fetch_images.py --query "parrot" --out assets/img --count 2` |
| `verify.py` | Playwright 截图 + 控制台错误检查 | `python3 scripts/verify.py demo.html` |
| `verify-video.sh` | 视频产物硬校验（黑帧/时长/音频流） | `bash scripts/verify-video.sh out.mp4` |
| `design-gate-hook.sh` | 渲染前 gate 检查（block 无 direction-approved.md 的长片渲染） | 手动安装到 settings.json，非自动 |
| `narrate-pipeline.mjs` | 解说稿 → TTS mp3 + timeline.json（豆包 TTS） | `node scripts/narrate-pipeline.mjs script.md` |
| `render-narration.sh` | 带解说的动画 → 最终 MP4（无声 + 人声 + BGM） | `bash scripts/render-narration.sh demo.html --timeline=timeline.json` |

## 云能力（scripts/cloud/，完全可选）

`scripts/cloud/` 里的两个脚本（`ai-review-video.py`、`tts-doubao.mjs`）是**仅有的网络调用点**，需自备 API key + `--yes` 显式确认。核心设计流程 100% 本地、零网络、零 key。详见 `SECURITY.md`。

## 修改 SKILL.md 时的注意事项

- `SKILL.md` 是 agent 的主指令文档，修改直接影响 skill 在所有 agent 上的行为。
- 文件已接近 token 上限，新增内容优先考虑能否写进对应的 `references/` 子文档再在 SKILL.md 引用。
- `references/` 路由表（SKILL.md 末尾）和「任务路由」表（SKILL.md 中部）是 agent 查找子文档的索引，新增 reference 文件时同步更新这两处。
- Gate 文件协议（`brand-spec.md` / `direction-approved.md` / `导演稿.md`）是 SKILL.md 里最硬的约束，改动需理解其在 `scripts/design-gate-hook.sh` 中的对应检查逻辑。

## 仓库结构约定

- `assets/` — Starter Components（JSX/HTML/JS），agent 读取后 inline 进产出 HTML。`personal-asset-index.json` 被 gitignore（仅保留 `.example.json` 模板）。
- `references/` — 33 篇按任务类型加载的子文档，SKILL.md 通过路由表引用。
- `demos/` — 能力演示（GIF/HTML），大视频走 GitHub Releases 不进仓库（`demos/**/*.mp4` 被 gitignore）。
- `scripts/cloud/` — 云能力隔离区，与核心本地流程物理分离。
- 产物目录 `design-demos/` 和 `_style-research/` 被 gitignore（skill 内部研发用，不分发）。

## git 约定

- commit message 用中文描述 + conventional commit 前缀（`feat:` / `fix:` / `docs:` / `security:` / `merge:`）。
- 无 CI、无 pre-commit hook、无分支保护规则。
