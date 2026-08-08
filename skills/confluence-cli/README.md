# Confluence CLI

基于 Python + `uv` 的 Confluence 命令行工具，支持页面读写、附件管理、Markdown 一键发布。

---

## 前置要求

只需安装 `uv`，所有依赖自动管理，无需手动 `pip install`。脚本要求 Python 3.10 及以上，`uv` 会按脚本声明创建隔离环境。

```powershell
# Windows 安装（PowerShell）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 配置凭据

```powershell
$env:CONFLUENCE_BASE_URL   = "https://your-confluence.example.com"
$env:CONFLUENCE_USERNAME   = "your_username"
$env:CONFLUENCE_API_TOKEN  = "your_api_token_or_pat"
$env:CONFLUENCE_VERIFY_SSL = "false"   # 内网自签证书时加上
```

---

## 主要功能

- **页面管理**：获取、创建、更新、重命名、删除页面
- **附件管理**：列出、下载附件（支持按文件名或正则过滤）
- **Markdown 发布**：将本地 `.md` 文件发布到 Confluence，支持：
  - 标准 Markdown / GFM 语法
  - LaTeX 数学公式（行内 `$...$` 和块公式 `$$...$$`）
  - Mermaid 流程图（渲染为 SVG，自动附带折叠源码）
  - 折叠块 `[EXPAND 标题]...[/EXPAND]`，支持嵌套
  - 任务列表 `- [ ]` / `- [x]`（转为 Confluence 可交互复选框）
  - 本地图片自动上传为附件
  - 用户 @Mention、Emoji、目录 TOC
  - `confluence-storage` 代码块直通（嵌入原生 Confluence 宏）
  - `--dry-run` 预览转换结果，不发布到 Confluence
- **搜索**：CQL 全文搜索

---

## 推荐发布流程

1. 先使用 `--dry-run` 预览 Storage XML，检查标题、列表、表格、图片、代码块和宏。
2. 预览无误后再发布 Markdown。
3. 发布完成后用 `page get --fresh --body-format storage` 回读页面，确认正文和附件引用。

`--dry-run` 不创建或更新页面，也不会上传附件。

## 如何使用

直接告诉 AI（WorkSpace）你想做什么，例如：

> 帮我把 `./doc.md` 发布到 Confluence 页面 ID 168442036

> 帮我获取页面 168442036 的 storage 格式内容

> 帮我下载页面 168442036 的所有附件到 `./attachments`

AI 会调用本工具完成操作，无需手动执行命令。

---

## 直接执行（可选）

如需手动调用：

```powershell
cd path/to/confluence-cli/scripts

# 发布 Markdown
./confluence_cli.py page publish-markdown --parent-id 12345678 --page-id 87654321 --title "我的文档" --markdown-path ./doc.md

# 预览转换结果（不发布）
./confluence_cli.py page publish-markdown --parent-id 12345678 --title "我的文档" --markdown-path ./doc.md --dry-run
```

运行本地回归测试（在 `confluence-cli` 目录执行）：

```bash
uv run --with httpxyz --with latex2mathml --with markdown-it-py --with pydantic --with rich --with typer python -m unittest discover -s scripts/tests -v
```

> 使用 `./confluence_cli.py <命令> --help` 查看各命令参数。
