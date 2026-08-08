---
name: confluence-cli
description: >
  提供 Confluence CLI 的基础能力，包括环境检查、`uv` 安装、命令调用方式、参数说明、
  页面/附件/搜索等通用操作，以及 Markdown 发布相关的基础转换规则。适用于需要查询、
  检索、读取、发布 Confluence 页面，或需要确认 CLI 用法与环境是否正确的场景。
---

说明：本 Skill 仅负责 Confluence CLI 的基础能力，包括环境检查、命令调用方式、参数约定与 Markdown/Confluence 转换能力。以下调用方式均以当前 `SKILL.md` 文件所在文件夹为 workdir。

## 职责边界

- 本 Skill 负责基础能力：`uv` 检查、环境变量要求、脚本调用方式、命令参数、输出格式、Markdown 发布能力
- 本 Skill 不包含任何部门/团队约定，例如默认空间、固定页面 ID、模板选择规则、文档组织规范、组员映射
- 若存在团队或部门级使用规范，应由独立的上层 guide skill 定义

## 前置环境要求

本 CLI 通过 `uv` 管理 Python 依赖，**无需手动安装任何 Python 包**，`uv run` 会自动按脚本头部 `# dependencies` 声明创建隔离虚拟环境并安装：

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| `uv` | 最新版 | 脚本运行器，**必须预先安装** |
| Python | ≥ 3.10 | 由 `uv` 自动管理，无需手动安装 |
| Python 依赖包 | 按脚本声明自动解析 | 首次 `uv run` 时自动下载并安装 |

### 检查并安装 `uv`

**在使用任何 CLI 命令前，先验证 `uv` 是否可用：**

```powershell
uv --version
```

如果命令不存在，按以下在线方式安装：

```powershell
# Windows（PowerShell，需要外网）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后**重新开启终端**（或重新加载 PATH），再次执行 `uv --version` 确认可用。

> `uv` 是唯一需要手动安装的前置依赖，所有 Python 包均由 `uv run` 在线自动处理。

---

脚本调用方式：使用脚本 shebang，避免绕过 inline dependencies。
```bash
cd skills/confluence-cli
./scripts/confluence_cli.py --json page get --page-id 3060336952
```
Windows PowerShell：
```powershell
uv run --script .\scripts\confluence_cli.py --json page get --page-id 3060336952
```

不要使用 `python scripts/confluence_cli.py` 或 `uv run python ...`，这可能绕过脚本头部的依赖声明。

1) 常用子命令（覆盖日常场景）
- `space`
  - `list [--start --limit --expand]`
  - `get --space-key [--expand]`
- `page`
  - `get --page-id [--body-format --expand --fresh]`
  - `by-title --space-key --title [--body-format --expand]`
  - `children --page-id [--start --limit --expand]`
  - `rename --page-id --title`
  - `delete --page-id [--yes]`
  - `publish-markdown --parent-id --title --markdown-path [--page-id --update-if-exists --body-format --expand --dry-run]`
- `attachment`
  - `list --page-id [--start --limit --expand]`
  - `download --page-id [--output-dir --name --filter --all --start --limit --expand]`
- `search`
  - `--cql [--start --limit --body-format --expand]`

2) 输出格式
- 所有调用统一在脚本后、子命令前加 `--json`（示例：`./scripts/confluence_cli.py --json page get --page-id ...`）

3) 冷门参数/字段怎么查
- 运行 `./scripts/confluence_cli.py <command> --help` 查看该命令的参数
- 需要更深入的 Confluence API 字段时，可扩展脚本中的 `expand` 参数

4) 注意事项
- `page get` 默认保持普通缓存读；刚更新页面后需要校验正文时，使用 `--fresh` 绕过 Confluence 或代理缓存，例如：`./scripts/confluence_cli.py --json page get --page-id ... --body-format storage --expand body.storage,version --fresh`

5) 附件下载示例
- 下载指定附件（可重复传入 `--name`）：`./scripts/confluence_cli.py attachment download --page-id 3060336952 --output-dir ./attachments --name a.png --name b.png`
- 下载全部附件（自动分页）：`./scripts/confluence_cli.py attachment download --page-id 3060336952 --all --output-dir ./attachments`
- 过滤下载（正则）：`./scripts/confluence_cli.py attachment download --page-id 3060336952 --filter 'image2026-1-19_.*\\.png' --all --output-dir ./attachments`

6) 发布 Markdown 示例
- 发布到父页面（同名则更新）：`./scripts/confluence_cli.py --json page publish-markdown --parent-id 3061931928 --title "批量重置 Offset 功能测试" --markdown-path /path/to/doc.md`
- **直接更新已知页面**（推荐，无需查父页面）：`./scripts/confluence_cli.py --json page publish-markdown --parent-id <父页面ID> --page-id <页面ID> --title "页面标题" --markdown-path /path/to/doc.md`
  - `--page-id` 直接指定要更新的页面 ID，跳过按标题查找子页面的步骤，速度更快且不会误创建重名页面
  - 指定 `--page-id` 后 `--update-if-exists` 失效（始终执行更新）
  - 页面 ID 可从 Confluence URL（`?pageId=...`）或 `page by-title` / `page get` 返回结果中获取
- **试运行（调试格式）**：`./scripts/confluence_cli.py page publish-markdown --parent-id <ID> --title "标题" --markdown-path /path/to/doc.md --dry-run`
  - 只将 Markdown 转换为 Storage XML 并打印到终端，**不调用 Confluence API**，不创建/更新任何页面
  - 发布前先用 `--dry-run` 检查转换结果，可以避免格式问题直接出现在线上页面
- 本地图片发布时会按最大展示框自动生成单个 Confluence 尺寸属性：默认最大宽度 `1000`、最大高度 `800`，可用 `--image-max-width` / `--image-max-height` 覆盖；只写触发缩放的 `ac:width` 或 `ac:height`，不修改附件原图。
- 如需覆盖单张图片展示尺寸，可使用 Markdown title：`![图](./a.png "confluence-width=1200")`、`![图](./a.png "confluence-height=600")`、`![图](./a.png "confluence-size=original")`。
- **复选框/任务列表**：Markdown 中的 `- [ ]` 和 `- [x]` 会自动转换为 Confluence 原生任务列表（`<ac:task-list>` 宏）。示例：
  ```markdown
  - [ ] 未完成的任务
  - [x] 已完成的任务
  ```
  渲染为 Confluence 可交互的复选框，支持在页面上直接勾选/取消。

- **折叠块（expand 宏）**：使用 `[EXPAND 标题]...[/EXPAND]` 语法，发布时自动转换为 Confluence expand 宏。内部支持完整 Markdown 语法（列表、任务列表、加粗等）。标题可省略。示例：
  ```markdown
  [EXPAND 0618 周]
  **进展：**
  - 内容 A
  - 内容 B

  **待办：**
  - [ ] 任务 1 — 负责人
  [/EXPAND]
  ```
  渲染为 Confluence 可点击展开/折叠的区块，适合进展记录的近期动态章节。

- **LaTeX 数学公式**：使用标准 Markdown 数学公式语法，发布时自动用 `latex2mathml` 渲染为 MathML，通过 html 宏（block）或直接内嵌（inline）写入页面，无需外部 CSS/JS，离线可用。
  兼容主流 Markdown 编辑器的语法：

  | 类型 | 语法 | 兼容编辑器 |
  |------|------|-----------|
  | 行内 | `$...$` | Obsidian, GitHub |
  | 行内 | `\(...\)` | Typora |
  | Block | `$$...$$` | Obsidian, GitHub |
  | Block | `\[...\]` | Typora |

  - 代码块（`` ` `` 或 ` ``` `）内的公式符号**不会**被处理
  - 渲染失败时降级为 `<code>` 原始 LaTeX，不中止发布
  - **Block 公式（`$$` / `\[`）必须独占行**：`$$` 或 `\[` 必须出现在行首，`$$` 或 `\]` 作为结束也必须在行首。标题、段落中间的 `$$` 符号不会被识别为公式定界符。
  ```markdown
  行内（Obsidian/GitHub）：$\omega_{max} = 44 \times \frac{2\pi}{60}$ rad/s

  行内（Typora）：\(E = mc^2\) 爱因斯坦

  Block（Obsidian/GitHub）：

  $$
  \omega_{max}=44 \times \frac{2\pi}{60}=4.61 \text{ rad/s}
  $$

  Block（Typora）：

  \[
  \omega_{max}=44 \times \frac{2\pi}{60}=4.61 \text{ rad/s}
  \]
  ```

- **@mention 用户**：使用 `@姓名` 语法，发布时自动转换为 Confluence user mention 宏。映射表由环境变量 `CONFLUENCE_MENTION_MAP` 提供，格式为逗号分隔的 `姓名=userkey` 对。未设置或未匹配的 `@xxx` 保持原样。示例：
  ```markdown
  - [ ] 完成显示驱动验证 — @王文
  ```
  对应环境变量设置：
  ```
  CONFLUENCE_MENTION_MAP="张三=abc123userkey,李四=def456userkey"
  ```

- **emoji / 表情**：使用 `:name:` 语法，发布时自动转换为 Confluence emoticon 宏。**仅支持以下 20 个名称**，使用不在列表中的短码（如 `:rocket:`、`:fire:` 等）会报错终止：
  `smile`, `sad`, `cheeky`, `laugh`, `wink`, `thumbs-up`, `thumbs-down`, `information`, `tick`, `cross`, `warning`, `plus`, `minus`, `question`, `light-on`, `light-off`, `yellow-star`, `red-star`, `green-star`, `blue-star`

- **confluence-storage 逃生通道**：当 Markdown 无法表达的内容需要直接写入 Confluence storage XML 时，使用 `confluence-storage` 围栏语法。围栏内容**原样透传**，不转义、不包装。围栏内必须是合法的 Confluence storage XML 片段，CLI 不做校验。

  **场景 1：保留页面已有图片（`<ri:attachment>` 引用）**
  
  整理已有页面时，图片是页面附件，本地没有文件，无法用普通 Markdown `![]()` 语法引用。用此围栏原样保留：
  ````markdown
  ```confluence-storage
  <ac:image ac:height="250"><ri:attachment ri:filename="screenshot.png" /></ac:image>
  ```
  ````
  `ac:height` / `ac:width` 为可选展示尺寸。步骤说明文字写在围栏**外部**（普通 Markdown），图片写在围栏**内部**，两者交替排列即可。

  **场景 2：保留附件下载链接**
  ````markdown
  ```confluence-storage
  <p><ac:link><ri:attachment ri:filename="find_git.py" /></ac:link> 说明文字</p>
  ```
  ````

  **场景 3：保留附件预览宏（view-file）**
  ````markdown
  ```confluence-storage
  <ac:structured-macro ac:name="view-file" ac:schema-version="1" ac:macro-id="原有macro-id">
    <ac:parameter ac:name="name"><ri:attachment ri:filename="tools.zip" /></ac:parameter>
    <ac:parameter ac:name="height">250</ac:parameter>
  </ac:structured-macro>
  ```
  ````
  > **重要**：整理已有页面时，从 `page get --body-format storage` 返回的 XML 中**原样复制** `ac:macro-id`，不要自行生成，否则 Confluence 会将其视为新宏并可能丢失附件关联。

  **场景 4：嵌入 Confluence 原生信息宏**
  ````markdown
  ```confluence-storage
  <ac:structured-macro ac:name="info" ac:schema-version="1">
    <ac:parameter ac:name="title">提示标题</ac:parameter>
    <ac:rich-text-body><p>内容</p></ac:rich-text-body>
  </ac:structured-macro>
  ```
  ````

  **步骤编号 + 图片混排注意事项**：Markdown 有序列表（`1. 2. 3.`）在步骤间插入图片时，会被截断为多个独立 `<ol>`，每段都从 1 重新计数。推荐改用加粗纯文本编号（`**1**`、`**2**`），图片用围栏插在两个编号之间：
  ```markdown
  **1** 解压工具包，将目录添加到 PATH。

  ```confluence-storage
  <ac:image ac:height="250"><ri:attachment ri:filename="step1.png" /></ac:image>
  ```

  **2** 双击安装驱动。
  ```

- **Mermaid 流程图**：Markdown 中的 `mermaid` 围栏代码块，发布时自动调用 [mermaid.ink](https://mermaid.ink) HTTP API 渲染为内联 SVG，直接嵌入页面，无需安装 Node.js 或额外工具。

  - **无需任何安装**，开箱即用
  - 需要能访问 `https://mermaid.ink`（公网服务）
  - 内网环境可通过环境变量 `MERMAID_INK_SERVER` 指向自建服务：
    ```bash
    export MERMAID_INK_SERVER=http://your-internal-server:3000
    ```
  - 每个 mermaid 图表下方自动附带一个**折叠的源码块**（"查看 Mermaid 源码"），方便读者复用或修改
  - 渲染失败时自动降级为普通代码块展示源码，不中止发布；失败会重试 3 次（退避 2s/4s）
  - 一个 Markdown 文件中可包含多个 mermaid 代码块，每个独立渲染
  - **节点标签内禁用以下字符**（mermaid 语法特殊字符，写在标签里会导致渲染失败）：
    - `(` `)` — 括号（mermaid 用于圆角节点形状）
    - `|` — 竖线（mermaid 用于分支标签）
    - 替代写法：括号改用空格或描述性文字，`|x|` 形式改写为 `x 超限` 等

  示例：
  ````markdown
  ```mermaid
  graph TD
      A[开始] --> B{判断}
      B -->|是| C[处理]
      B -->|否| D[结束]
  ```
  ````

- **代码块自动折叠**：代码块超过 **200 行**时自动添加 `collapse=true`，200 行以内始终展开。

## 样式发布门禁

- 发布前必须先执行 `--dry-run`，确认标题层级、表格、列表、任务列表、图片、代码块和宏的 Storage XML 输出；dry-run 不创建或更新页面。
- dry-run 通过后再发布；如果上传了附件，发布完成后必须使用 `page get --body-format storage --expand body.storage,version --fresh` 重新读取页面，确认图片引用和正文版本已更新。
- 只使用本 Skill 声明的 Markdown 语法。原始 HTML、未列出的 emoji、带 query/fragment 的本地附件链接会被拒绝，不要静默改写。
- `confluence-storage` 只用于确实需要保留的原生宏或附件引用；内容应来自已读取的 Storage XML，避免手写错误的宏 ID。
- Mermaid 依赖网络或内部渲染服务；渲染失败会降级为代码块，发布前必须检查终端 warning 和 dry-run 输出。

## 资源

- [confluence_cli.py](scripts/confluence_cli.py)：主 CLI 入口，负责读取配置并发起 API 调用。
- [confluence_api_client.py](scripts/confluence_api_client.py)：SDK 封装层，收敛常用 API 调用。
