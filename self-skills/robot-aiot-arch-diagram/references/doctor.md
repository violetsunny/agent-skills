# 环境诊断（Environment Doctor）

当用户要求对本 skill 运行诊断、健康检查、环境 doctor，或要求首次运行排障时加载本文件（如"跑一下环境诊断"、"check why PNG export fails"、"run the doctor"）。

目标是一次性报告：检查本地对本 skill 导入/导出与命令路由的就绪程度，不修改用户文件、不安装依赖。

skill 安装位置从本加载的 reference 解析，而不是从用户当前工作目录解析。普通项目目录是调用诊断的预期位置，不得当作仓库路径错误处理。

诊断只针对解析出的 skill 安装副本：本 skill 按自包含安装包分发，不要求、也不检查任何维护者仓库文件。

## 入参

可选 flag：

- `--strict` — 最终汇总中把 warning 视为 failure。
- `--json` — 在人类可读摘要之外输出机器可读 JSON 报告。

未提供 flag 时按标准模式运行。

## 必查项

按以下顺序运行全部检查，每项标记为 `pass`、`warn` 或 `fail`。

1. Python 运行时
- 先解析 `python3`，再解析 `python`。在 PATH 上但无法报告自身版本的名称不赢得解析：落到下一个候选。（Windows 的 `python3` App Execution Alias 是 Microsoft Store 占位程序而非解释器，且在 PATH 上排在 python.org 安装之前。）完全无法启动的名称视为同类无效候选，记为检查失败而不是终止整个运行。
- 要求版本 >= 3.10。
- 找不到任何 Python 解释器时 `fail`。
- 版本低于 3.10 时 `fail`。

2. PNG 导出渲染栈（与 `fireworks.py doctor` 探测面一致）
- SVG→PNG 光栅化主路径（见 png-export.md）：
  - 探测 `cairosvg` 是否可导入（`importlib.util.find_spec("cairosvg")`）。
  - 探测 `rsvg-convert` 是否在 PATH 上。
  - 回退链：`node` 在 PATH 上 + `scripts/svg2png.js` 存在 + `puppeteer-core` 可解析 + 系统 Chrome 可用（`CHROME_PATH` 或默认安装路径）。
  - `raster_export` 可用 = cairosvg 或 rsvg-convert 至少其一可用；两者皆缺但回退链可用时标 `warn`；全链不可用时标 `warn` 并打印精确安装提示：
    - `pip install cairosvg`（或 `brew install librsvg` / `apt-get install librsvg2-bin`）
- HTML→PNG 截图路径（见 export.md）：探测 `import playwright` 是否可用及其 Chromium 是否已安装（`playwright install --help` 可用即算命令存在，条件允许时优先检查浏览器缓存）；缺失时标 `warn` 并打印精确安装提示：
  - `pip install playwright && playwright install chromium`
- 永不自动安装依赖。

3. 预期脚本存在性
- 验证 excalidraw 导入提取器存在于 `$SKILL_ROOT/scripts/excalidraw_extract.py`；缺失时 `fail`。

4. 常见路径错误
- 验证解析出的安装根目录下存在 `SKILL.md`。不要相对用户当前项目搜索它，也不要指示用户进入维护者仓库。
- 当路径包含空格且给出的命令示例缺少引号时，检测 Windows 路径引号风险。
- 检测对不存在的本地已安装 skill 路径的引用（如果命令输出中出现）。
- 以上标记为 `warn` 并给出精确修复建议。
- 解析出的 `SKILL.md` 缺失时，应建议重新安装或更新 robot-aiot-arch-diagram（本 skill），而不是切换到仓库检出目录。

## 输出契约

始终打印：

1. 一行紧凑摘要：
- `Doctor summary: <PASS|WARN|FAIL> (<pass_count> pass, <warn_count> warn, <fail_count> fail)`

2. 每项检查一行的清单：
- `[PASS] Python 3.11.9 found at ...`
- `[WARN] cairosvg not installed ...`
- `[FAIL] Missing scripts/excalidraw_extract.py`

3. 仅当存在 warn/fail 时输出 `Next actions` 节。

4. 提供 `--json` 时，追加 JSON 对象，含：
- `status`、`counts`、`checks[]`（`name`、`status`、`message`、可选 `fix`）、`timestamp`。

## 安全与行为规则

- 只做只读诊断：不修改文件、不安装包、不运行破坏性 git 命令。
- 任何命令意外失败时，捕获 stderr 并继续剩余检查。
- 除非本次运行中直接验证过，否则绝不声称某项检查通过。
- 优先给出显式、可直接复制粘贴的修复命令。

## 结果示例

```text
Doctor summary: WARN (6 pass, 2 warn, 0 fail)
[PASS] Python 3.11.9 found at /usr/bin/python3
[WARN] cairosvg 与 rsvg-convert 均不可用；svg2png.js 回退链就绪
[PASS] scripts/excalidraw_extract.py present
...

Next actions
- 安装 SVG→PNG 光栅化依赖: pip install cairosvg
- 使用 `--strict` 重新运行环境诊断（warning 视为 failure）
```
