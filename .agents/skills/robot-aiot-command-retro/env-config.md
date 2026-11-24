# env-config.md — robot-aiot-command-retro 路径登记（唯一真源）

本 skill 目录结构与全部读写路径以本文件为准；其他文件仅引用，新增/变更路径只改这里。

## 读取

| 用途 | 路径 | 说明 |
|---|---|---|
| ws 会话数据库 | `~/.local/share/workspace-code-prd/opencode.db` | 全局 SQLite，可用环境变量 `WS_DB` 覆盖；表：session（directory=项目路径）、message、part（data JSON，type=text/tool/reasoning） |
| 目标项目根 | `/Users/kangll13/aiot/java-code/aiot-robot/` | 脚本 `--root` 可覆盖 |
| 指令真源（共性问题落改对象） | `self-skills/dev-paradigm-matt/`、`self-skills/robot-aiot-commit/`（agent-skills 仓库） | 三副本/两副本同步规则见 SKILL.md 硬约束节 |
| 特性问题落改对象 | `<目标项目>/.agents/AGENTS.md` | 只增改不删除 |

## 临时

| 用途 | 路径 | 说明 |
|---|---|---|
| 会话导出 dump | `/tmp/command-retro-<YYYYMMDD-HHMMSS>/` | sessions-index.txt、matched-ids.txt、matched/<sid>.txt；过程性文件，报告产出后可清理 |

## 输出

| 用途 | 路径 | 说明 |
|---|---|---|
| 分析报告 + 裁定清单 | `<agent-skills 仓库>/.agents/reports/command-retro/<YYYYMMDD-HHMM>/` | report.md（全量分析）+ decisions.md（共性问题编号裁定清单）；人工确认前禁止清理 |

## 生成 / 验证

无独立生成与验证目录（验证方式见 SKILL.md 出口检查节）。
