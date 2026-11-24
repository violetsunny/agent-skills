---
name: ws-session-cleaner
description: >
  清理 ws (workspace-cli) 历史会话数据：按保留天数删除过期 session 及其关联的
  message/part/todo 记录与 session-search 全文索引，删除前自动备份数据库，支持
  dry-run 预览。Use when 用户说"清理历史会话""清除 N 天前的会话记录""保留最近 N 天
  会话""ws 会话太多了""清理 session 数据库""释放会话存储空间""会话搜索库太大"等。
---

# ws-session-cleaner

按"保留最近 N 天"策略清理 ws 历史会话。判定标准是 `session.time_updated`（最后活动时间）：最近 N 天内活动过的会话一律保留，正在运行的当前会话天然受保护。

## 数据存储位置

| 文件 | 内容 |
| --- | --- |
| `~/.local/share/workspace-code-prd/opencode.db` | 主库：`session` / `message` / `part` / `todo` / `session_entry` / `session_share` 表，时间戳为毫秒 epoch |
| `~/.local/share/workspace-code-prd/session-search.db` | 全文搜索索引：`search_entry` / `search_progress` + FTS5（触发器自动同步） |

数据目录可用环境变量 `WS_DATA_DIR` 覆盖；默认路径不存在时脚本会自动发现唯一候选。

依赖：`sqlite3` CLI + `python3`。搜索索引库带 FTS5 触发器，而 sqlite3 CLI（含 macOS 系统版与 platform-tools 版）普遍未编译 FTS5 模块，删除/VACUUM 索引库的步骤统一走 python3 的 sqlite3（自带 FTS5）；脚本在 apply 前预检，缺 FTS5 时中止且不修改任何数据。

## 工作流程

1. **确认保留天数 N**：用户已指定则直接使用；未指定则询问用户（可建议默认 30 天），不得擅自替用户决定。
2. **预览**（必做，不可跳过）：

   ```bash
   bash <skill目录>/scripts/clean_sessions.sh --days N --dry-run
   ```

   把统计结果（将删除的 session/message/part/search_entry 数量、保留数量）展示给用户。
3. **用户明确确认后执行**：

   ```bash
   bash <skill目录>/scripts/clean_sessions.sh --days N --apply --vacuum
   ```

   `--vacuum` 回收磁盘空间（数据量大时建议加上；耗时略长）。
4. **汇报**：删除数量、剩余 session 数、数据库大小变化、本次备份路径。脚本每次运行（含 dry-run）末尾都会输出"备份占用"报告（历史备份份数、合计大小、逐份明细），把该报告转达给用户，并询问是否需要清除旧备份；用户明确同意后才可删除指定备份，且建议至少保留最近 1 份。

## 脚本参数

```
clean_sessions.sh --days N (--dry-run | --apply) [--no-backup] [--vacuum]
```

- `--days N`：保留最近 N 天，N 为 >=1 的整数（必填）
- `--dry-run`：只统计不修改；`--apply`：实际删除（二者必选其一）
- `--no-backup`：跳过备份；`--vacuum`：删除后 VACUUM 回收空间

`--apply` 默认先把两个数据库 `.backup` 到 `<数据目录>/backups/session-clean-<时间戳>/`，再在单事务内删除主库数据（part → message → todo → session_entry → session_share → session），最后按"孤儿记录"清理搜索索引（session_id 已不存在于主库的 search_entry/search_progress，FTS5 由触发器自动同步）。孤儿式清理幂等且自愈：apply 可重复执行，无过期 session 时跳过备份与主库删除，仅清孤儿；历史失败留下的半清理状态也会被下一次 apply 修复。任一步失败事务回滚，不会出现半删状态。

## 安全规则

- 不可逆操作：必须先 `--dry-run` 展示统计、经用户确认后才允许 `--apply`。
- 不要传 `--no-backup`，除非用户明确要求。
- 备份默认只增不删；每次清理必须向用户汇报备份占用并询问是否清除旧备份。仅在用户明确指示时删除指定备份，建议至少保留最近 1 份。
- 建议执行时关闭其他长期挂起的 ws 会话窗口（闲置超过 N 天的打开中会话会被删除）。
- 禁止绕过脚本手写 SQL 删除会话数据；脚本已处理事务、锁等待（busy_timeout）与搜索索引联动。

## 验证

清理后可用以下方式确认：

```bash
sqlite3 ~/.local/share/workspace-code-prd/opencode.db \
  "SELECT count(*), datetime(min(time_updated)/1000,'unixepoch','localtime') FROM session;"
```

剩余 session 的最早活动时间应不早于 N 天前；ws 中 `session_search` 不应再命中已删除会话。
