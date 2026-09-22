# 环境诊断（doctor）

当用户要求为本 skill 运行诊断、健康检查或环境 doctor，或要求首次运行排障时加载本文件（例如"跑一下环境诊断"、"check why PNG export fails"、"run the doctor"）。

目标是一次性产出报告，检查本地环境对本 skill 导入/导出与命令路由的就绪程度，不修改用户文件、不安装依赖。

skill 安装根目录从本 reference 被加载时的路径解析，不从用户当前工作目录解析。普通项目目录是调用 doctor 的预期位置，不得当作仓库路径错误处理。

诊断只有一种模式：**installed-skill 模式**——检查运行时与解析出的 skill 安装目录，不要求任何维护者专属的仓库文件。

## 输入

可选参数：

- `--strict` — 最终汇总中把 warning 视为 failure。
- `--json` — 在人类可读汇总之外额外输出机器可读的 JSON 报告。

未提供参数时按标准模式运行。

## 必查项

按以下顺序执行全部检查，每项报告为 `pass`、`warn` 或 `fail`。

1. Python 运行时
- 先解析 `python3`，再解析 `python`。名字在 PATH 上但无法报告自身版本的候选不算解析成功：继续落到下一个候选。（Windows 自带的 `python3` App Execution Alias 是 Microsoft Store 存根而非解释器，且排在 python.org 安装之前。）完全无法启动的名字同样视为无效候选，报告为该项检查失败，而不是终止整个运行。
- 要求版本 >= 3.10。
- 找不到任何 Python 解释器时记 `fail`。
- 版本低于 3.10 时记 `fail`。

2. HTML→PNG 截图路径所需的 Playwright 可用性（见 export.md）
- HTML→PNG 截图路径（见 export.md）：探测当前 Python 解释器中 `import playwright` 是否可用，及其 Chromium 是否已安装（`playwright install --help` 可用即算命令存在，条件允许时优先检查浏览器缓存）。
- 缺失时标 `warn` 并打印精确安装提示：
  - `pip install playwright && playwright install chromium`
- 永不自动安装依赖。

3. 常见路径错误
- 在解析出的安装根目录下确认 `SKILL.md` 存在。不要相对用户当前项目搜索它，也不要指引用户进入维护者仓库。
- 当路径含空格且给出的命令示例未加引号时，提示 Windows 路径引号风险。
- 检测命令输出中引用的本地已安装 skill 路径是否不存在（如输出包含此类路径）。
- 以上均记 `warn` 并给出精确的修复建议。
- 解析出的 `SKILL.md` 缺失时，应建议重新安装或更新 robot-aiot-draw-flowchart，而不是切换到仓库 checkout。

## 输出契约

始终打印：

1. 一行紧凑汇总：
- `Doctor summary: <PASS|WARN|FAIL> (<pass_count> pass, <warn_count> warn, <fail_count> fail)`

2. 每项检查一行的清单：
- `[PASS] Python 3.11.9 found at ...`
- `[WARN] Playwright not installed ...`
- `[FAIL] SKILL.md not found under resolved installation root`

3. 仅当存在 warn/fail 时输出 `Next actions` 小节。

4. 提供 `--json` 时追加 JSON 对象，包含：
- `status`、`counts`、`checks[]`（`name`、`status`、`message`、可选 `fix`）、`timestamp`。

## 安全与行为规则

- 只做只读诊断：不修改文件、不安装包、不执行破坏性 git 命令。
- 任一命令意外失败时，捕获 stderr 并继续其余检查。
- 除非本次运行中直接验证过，否则永不宣称某项检查通过。
- 优先给出显式、可直接复制粘贴的修复命令。

## 结果示例

```text
Doctor summary: WARN (5 pass, 1 warn, 0 fail)
[PASS] Python 3.11.9 found at /usr/bin/python3
[WARN] Playwright package not found in active interpreter
[PASS] SKILL.md present under resolved installation root
...

Next actions
- Install PNG export dependencies: pip install playwright && playwright install chromium
- Re-run the environment doctor with `--strict` (warnings treated as failures)
```
