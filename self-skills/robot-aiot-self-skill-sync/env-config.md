# env-config — 目录结构唯一真源

本技能全部输出 / 生成 / 验证 / 读取 / 临时目录只在本文件登记。**可执行路径的唯一真源是 `scripts/config.sh`**（所有 m*.sh 脚本 source 它；改路径/清单/豁免项只改 config.sh，不改各模块脚本）。本文件是 config.sh 的目录登记镜像：改 config.sh 必须同步更新本表，两者不一致时以 config.sh 为准并立即修表。

规则：

1. 新增目录、修改路径 → 只改 `scripts/config.sh` + 本文件；模块脚本（m*.sh）不得硬编码路径。
2. `~/.agents/` 与 `agent-skills/` 只允许新增和修改，绝对不允许删除（唯一例外：模块 1 步骤 1.6 强制清除 `agent-skills/skills/` 下残留的 `.git`/`.github`）。
3. 中间产物只落 `/tmp`（WORK_DIR、ZH_DIR），禁止写入源码仓库与运行时目录。
4. 保护目录（gggggggood，7 个 g）内禁止删除与强制 git 操作；config.sh 启动即断言 g 数量。

## 目录登记表

| 类别 | config.sh 变量 / 路径 | 用途 |
|---|---|---|
| 读取 | `SELF_ROOT=/Users/kangll13/aiot/java-code/self` | 模块 1 扫描根（递归 5 层嵌套 git 仓库） |
| 读取 | `KB_ROOT=$SELF_ROOT/ggggggggood/agent-skills` | 知识库根（保护目录内） |
| 读取/输出 | `KB_SELF_SKILLS=$KB_ROOT/self-skills` | 自写 skill 唯一真源（模块 3.3 与运行时双向同步） |
| 读取/输出 | `KB_COMMANDS=$KB_ROOT/commands` | 自写命令唯一真源（模块 3.4 与运行时双向同步） |
| 输出 | `KB_SKILLS=$KB_ROOT/skills`（=`NOSYNC_DIR`） | 外部 skill 副本：只同步覆盖禁私改；模块 1 禁拉；1.6 仅清 .git/.github |
| 输出 | `KB_DOCS=$KB_ROOT/docs` | `skills-overview.md` + `.skills-overview-mtimes.json`（模块 5 产出，快照不参与 git 提交） |
| 读取/输出 | `RUNTIME_SKILLS=~/.agents/skills` | 运行时 skill（3.3 部署/回写；`_mideameta.json` 永远运行时权威） |
| 读取/输出 | `RUNTIME_COMMANDS=~/.agents/commands` | 运行时命令（3.4；模块 2 仅同步 `opsx/` 子目录，根目录扁平 opsx-*.md 归 3.4） |
| 读取 | `CLAUDE_SKILLS=~/.claude/skills` | OpenSpec 生成源（模块 2，单向 .claude→.agents，不反向） |
| 读取 | `EXTERNAL_CLONES=$SELF_ROOT/skills` | 外部项目本地克隆（只读，严禁回写；模块 3.1 rsync 兜底源） |
| 输出 | `STOCK_TARGET=$SELF_ROOT/gggggggood/free-stock-line-skills` | 模块 3.5 同步目标（跳过清单 `M35_SKIP_LIST`） |
| 临时 | `WORK_DIR=/tmp/self-skill-sync`（环境变量可覆盖） | 中间产物：m1_repos.txt、m1_results.txt、m3_failed.txt、m3_npx_output.txt、m5_records.jsonl 等 |
| 临时 | `ZH_DIR=/tmp/zh` | 模块 5 翻译文件交换：in_NN.json（extract 产出）/ out_NN.json（sub agent 写回）；每轮清空重建 |

## 同步排除项

`EXCLUDES` / `EXCL_RE`（config.sh 登记）：`.git/`、`.gitignore`、`.gitmodules`、`.DS_Store`、`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`node_modules/`、`_mideameta.json`。
