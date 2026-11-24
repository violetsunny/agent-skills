# AGENTS.md — agent-skills 仓库

Skill 知识仓库，非可编译应用。核心操作是 skill 编写与 self-skill-sync 同步。

## 仓库结构

- `self-skills/` — 16 个自写 skill（可修改，源真）
- `skills/` — 693 个外部 skill 副本（只读，同步产物，禁止手改）
- `commands/` — 22 个 slash command 定义 + `opsx/`（12 个 OpenSpec 命令）
- `agents/` — 21 个 agent 角色定义
- `rules/` — 按 tech stack 分类的编码规则（common/java/react/typescript/vue）
- `openspec/` — spec-driven 配置 + 12 个 spec
- `key-skills-git/` — 20 个外部 git 克隆（gitignored，禁入库，纯克隆禁改，处置归用户人工）
- `docs/` — skills-overview.md（133+ skill 索引）、验证清单
- `.agents/memories/MEMORY.md` — 历史裁决与踩坑记录

## 同步工具

路径真源：`self-skills/robot-aiot-self-skill-sync/scripts/config.sh`。所有 m*.sh 脚本 source 它。改路径只改 config.sh，禁硬编码。

```bash
S=~/.agents/skills/robot-aiot-self-skill-sync/scripts

# Module 1: 批量 git pull（顺序执行）
$S/m1_git_pull.sh probe → scan → classify → pull → clean-tmp-pack → clean-nosync → report

# Module 3: skill 同步
$S/m3_npx_update.sh                              # 16 个 npx 管理型外部 skill
$S/m3_fallback.sh --from-file /tmp/.../m3_failed.txt  # rsync 降级
$S/m3_self_sync.sh --dry-run                     # self-skills ↔ runtime 双向
$S/m3_cmd_sync.sh                                # commands 双向

# Module 5: skills overview
$S/m5_extract.sh → $S/m5_render.sh
```

## 关键约束

- `skills/` 目录只读——手改会被下次同步覆盖。自写 skill 改 `self-skills/`。
- 改 `~/.agents/skills/` 中的自写 skill 安装副本后，须镜像回 `self-skills/` 仓库源（`_mideameta.json` 仅安装侧有）。
- `~/.agents/` 和 `agent-skills/` 只允许增改，禁止删除。
- `key-skills-git/` 20 个克隆一律纯克隆，禁任何修改、添加文件、本地提交（2026-11-14 曾因 `update skills` 本地提交致 13 仓库积累 merge 链，已 reset 恢复）；发现污染（本地提交/merge 链/tracked 改动）经用户授权后 `git reset --hard origin/main` 恢复。
- `key-skills-git/`、市场端重发布、stock-replay-workbench 遗留改动三项由用户人工处理，agent 不得擅自操作。
- 自写 skill 的示例/参考文件引用不得超出自身 SKILL 目录（目标环境找不到外部路径）。
- 吸收外部 skill 能力时须内化到自身 references/，禁止保留外部 skill 名作为条件依赖。
- 自写 skill/command 结构约定：command 指令文件必须 ≤200 行，只留可执行骨架与关键规则；SKILL.md 可全面详尽，细则可分类放 references/、脚本放 scripts/；command 与 SKILL 各自独立运行、各自完整自包含，禁止 command 靠引用 SKILL 补细节。
- command 三副本（`~/.agents/commands/`、仓库 `commands/`、`self-skills/*/**-command.md`）任改一处必须同步其余两处并镜像回 self-skills 源，提交前 diff 三副本确认零漂移。

## 各 self-skill 的 env-config.md

8 个自写 skill 各自有 `env-config.md`，是该 skill 目录结构的唯一真源（输出/生成/验证/读取/临时五类路径登记）。新增目录改路径只改对应 env-config.md，其他文件仅引用。

## 已知环境坑

- puppeteer 完整版 Chromium 下载本机超 5 分钟；svg2png.js 用 puppeteer-core + 系统 Chrome（`CHROME_PATH` 可覆盖）。
- 本机 Intel macOS 26.6 无 poppler bottle、未装 Keynote（仅 WPS）；渲染终审只能 WPS 人工。
- ruff 有缓存但仓库根无 ruff 配置文件，使用默认规则。

## 根目录已有规则文件

- `AGENTS.md` — 通用行为规则（已由 WorkSpace 自动加载）
- `RULES.md` — 最全规则（含 tech stack、delivery flow、tool routing）
- `CLAUDE.md` / `AGENTS-2.md` — 英文变体
- `PROJECT.md` — 底层项目 tech stack（SpringBoot 3.x / JDK 21 / Python 3.13）
- `.agents/memories/MEMORY.md` — 用户裁决与踩坑（已由 WorkSpace 自动加载）
