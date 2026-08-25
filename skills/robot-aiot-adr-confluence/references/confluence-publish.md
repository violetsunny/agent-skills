# Phase 5: Confluence 发布

Confluence 发布是可选阶段，只在用户明确要求发布且本地存在所需脚本时执行。

## 依赖定位

按以下优先级搜索 `confluence_cli.py`：

1. 环境变量 `CONFLUENCE_CLI_SCRIPTS` 指向的 scripts 目录
2. 当前项目 `.agents/skills/confluence-cli/scripts/`
3. 全局 `~/.agents/skills/confluence-cli/scripts/`
4. 全局 `~/.claude/skills/confluence-cli/scripts/`

```bash
CONFLUENCE_CLI=""
for candidate in \
  "${CONFLUENCE_CLI_SCRIPTS:+$CONFLUENCE_CLI_SCRIPTS/confluence_cli.py}" \
  ".agents/skills/confluence-cli/scripts/confluence_cli.py" \
  "$HOME/.agents/skills/confluence-cli/scripts/confluence_cli.py" \
  "$HOME/.claude/skills/confluence-cli/scripts/confluence_cli.py"; do
  [ -n "$candidate" ] && [ -f "$candidate" ] && CONFLUENCE_CLI="$candidate" && break
done
```

## 找不到依赖时的降级

如果脚本未找到：

1. 说明当前只能输出 Markdown 草稿
2. 提示用户安装 `confluence-cli` 或设置 `CONFLUENCE_CLI_SCRIPTS`
3. 保存本地 Markdown 文件
4. 返回后续可执行的发布命令模板

## 发布前检查

1. 检查 `uv --version`
2. 若缺少 `uv`，停止发布链路，说明当前只能交付本地 Markdown，并提示先安装 `uv` 后再重试
3. 若本轮文档命中了验证链触发条件，先确认核查已完成，或已在交付说明中记录跳过原因
4. 若当前发布的是 ADR，且前序已按 `robot-aiot-adr-generator` 完成核查，应保留其验证摘要或跳过说明随文档一并交付
5. 将文档保存为本地 `.md`
6. 先执行 `page publish-markdown --dry-run`
7. 确认标题层级、表格、列表、Mermaid、折叠块、任务列表、公式和 `confluence-storage` 围栏都被正确转换

## 正式发布

```bash
uv run --script "$CONFLUENCE_CLI" --json page publish-markdown \
  --parent-id <父页面ID> --title "<文档标题>" --markdown-path /tmp/adr-confluence-output.md
```

若已知页面 ID，优先同时传 `--page-id` 做原位更新。

## 发布后验证

```bash
uv run --script "$CONFLUENCE_CLI" --json page get \
  --page-id <页面ID> --body-format storage --expand body.storage,version --fresh
```

确认：

1. 版本已更新
2. Mermaid、公式、折叠块和任务列表渲染正常
3. 图片和宏引用正确

## 支持的富文本能力

1. Mermaid
2. LaTeX
3. `[EXPAND]...[/EXPAND]`
4. 任务列表
5. 受支持的 emoji 名称
6. `confluence-storage` 原样透传
7. 通过图片 title 控制展示宽度
