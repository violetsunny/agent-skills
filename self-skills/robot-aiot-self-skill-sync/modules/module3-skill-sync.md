# 模块 3：Skill 文件同步

> 共享规则见 `modules/shared.md`

模块 3 分为三类同步方式：

- **npx 管理型**（15 个项目）：通过 `npx skills@latest update` 统一更新，安装到 `~/.agents/skills/`；更新失败的 skill 走 rsync 兜底
- **自写 skill 同步**（模块 3.3）：`agent-skills/self-skills/` ↔ `~/.agents/skills/`，按文件级比对结果决定方向，排在外部同步之后
- **自写命令同步**（模块 3.4）：`agent-skills/commands/` ↔ `~/.agents/commands/`，方向判定同 3.3，排在 3.3 之后

> 原先独立的「rsync 管理型」类别已取消：唯一成员 anthropics-skills 已并入 3.1 npx 管理型（`anthropics/skills`）。rsync 在模块 3 中只承担两个角色——3.1 的**失败兜底**，以及 3.3 / 3.4 的双向落地工具。

OpenSpec 在 `~/.claude/skills/` 下生成的完整 skills 集合只走模块 2 的专门同步流程。外部同步（npx / rsync 兜底）遇到与 `self-skills/` 同名的 skill 一律跳过，自写 skill 的真源规则见 `modules/shared.md`。

## 3.1 npx 管理型项目（15 个）

以下 15 个项目通过 `npx skills@latest` 安装和更新，**不走常规 rsync 同步**（仅更新失败时走本节末尾的 rsync 兜底）。npx 安装更可靠，能正确处理 skill 依赖和元数据，大幅减少同步错误的可能性。

| 项目                     | GitHub 仓库 | 初始化安装命令 |
|------------------------|-----------|--------------|
| superpowers            | `obra/superpowers` | `npx skills@latest add obra/superpowers` |
| **matt-skills**            | `mattpocock/skills` | `npx skills@latest add mattpocock/skills` |
| **ui-ux-pro-max-skill**  | `nextlevelbuilder/ui-ux-pro-max-skill` | `npx skills@latest add nextlevelbuilder/ui-ux-pro-max-skill` |
| baoyu-skills           | `JimLiu/baoyu-skills` | `npx skills@latest add JimLiu/baoyu-skills` |
| **ppt-master**             | `hugohe3/ppt-master` | `npx skills@latest add hugohe3/ppt-master` |
| **claude-code-java**       |`decebals/claude-code-java`|`npx skills@latest add decebals/claude-code-java`|
| **anthropics-skills**      | `anthropics/skills` | `npx skills@latest add anthropics/skills` |
| ECC                    | `affaan-m/ECC` | `npx skills@latest add affaan-m/ECC` |
| ponytail               | `DietrichGebert/ponytail` | `npx skills@latest add DietrichGebert/ponytail` |
| **archify**                | `tt-a1i/archify` | `npx skills@latest add tt-a1i/archify` |
| **diagram-design**         | `cathrynlavery/diagram-design` | `npx skills@latest add cathrynlavery/diagram-design` |
| humanizer              | `blader/humanizer` | `npx skills@latest add blader/humanizer` |
| humanizer-zh           | `op7418/Humanizer-zh` | `npx skills@latest add op7418/Humanizer-zh` |
| **andrej-karpathy-skills** | `forrestchang/andrej-karpathy-skills` | `npx skills@latest add forrestchang/andrej-karpathy-skills` |
| vercel-agent-skills    | `vercel-labs/agent-skills` | `npx skills@latest add vercel-labs/agent-skills` |

### 更新流程

> **Tip**：使用 `--yes`（`-y`）和 `--global`（`-g`）标志可跳过交互提示，实现非交互式安装/更新。

1. `cd ~`（**必须在用户主目录下执行**）
2. **必须用 `env -u XDG_STATE_HOME` 执行**（见下方“环境变量陷阱”）
3. 执行 `npx skills@latest update -y -g`（`-y` 跳过确认，`-g` 全局安装并 Copy to all agents）
4. 等待更新完成

```bash
cd ~
# macOS 默认无 timeout：优先 timeout，其次 gtimeout（coreutils），都没有则留空由调用方控制超时
if command -v timeout >/dev/null 2>&1; then TO="timeout 300"
elif command -v gtimeout >/dev/null 2>&1; then TO="gtimeout 300"
else TO=""; fi
env -u XDG_STATE_HOME $TO npx skills@latest update -y -g 2>&1
```

### 环境变量陷阱：`XDG_STATE_HOME` 导致静默空跑

`skills` CLI 的 lock 文件路径解析逻辑为：

```
XDG_STATE_HOME 已设置 → $XDG_STATE_HOME/skills/.skill-lock.json
XDG_STATE_HOME 未设置 → ~/.agents/.skill-lock.json   ← 真实 lock 在这里
```

部分 Agent 运行环境（如 workspace-cli）会注入 `XDG_STATE_HOME`。此时 `npx skills update -g`
读不到真实 lock，输出 `No global skills tracked in lock file.` 后**正常退出（exit 0）**，
一个 skill 都不更新——属于典型的静默失败。

硬性规则：

- 所有 `npx skills` 调用（`update` / `add` / `remove`）一律加 `env -u XDG_STATE_HOME`
- 输出中出现 `No global skills tracked in lock file.` → 判定为 `[NPX-LOCK-MISS]`，
  **不得报告为成功**；先确认 `~/.agents/.skill-lock.json` 存在且 `version >= 3`，
  再检查是否漏加 `env -u XDG_STATE_HOME`
- 判定 3.1 真正成功的标志：输出含 `Checking skills from source:` 且逐个源被检查，
  结尾为 `✓ All global skills are up to date` 或 `✓ Updated <skill>`

### 初始化安装

仅首次或新增项目时执行。逐个运行上述安装命令，同样在用户主目录下运行，加 `-y -g` 跳过交互提示，并同样加 `env -u XDG_STATE_HOME`。

```bash
cd ~
env -u XDG_STATE_HOME npx skills@latest add obra/superpowers -y -g
env -u XDG_STATE_HOME npx skills@latest add mattpocock/skills -y -g
env -u XDG_STATE_HOME npx skills@latest add nextlevelbuilder/ui-ux-pro-max-skill -y -g
env -u XDG_STATE_HOME npx skills@latest add JimLiu/baoyu-skills -y -g
env -u XDG_STATE_HOME npx skills@latest add hugohe3/ppt-master -y -g
env -u XDG_STATE_HOME npx skills@latest add decebals/claude-code-java -y -g
env -u XDG_STATE_HOME npx skills@latest add anthropics/skills -y -g
env -u XDG_STATE_HOME npx skills@latest add affaan-m/ECC -y -g
env -u XDG_STATE_HOME npx skills@latest add DietrichGebert/ponytail -y -g
env -u XDG_STATE_HOME npx skills@latest add tt-a1i/archify -y -g
env -u XDG_STATE_HOME npx skills@latest add cathrynlavery/diagram-design -y -g
env -u XDG_STATE_HOME npx skills@latest add blader/humanizer -y -g
env -u XDG_STATE_HOME npx skills@latest add op7418/Humanizer-zh -y -g
env -u XDG_STATE_HOME npx skills@latest add forrestchang/andrej-karpathy-skills -y -g
env -u XDG_STATE_HOME npx skills@latest add vercel-labs/agent-skills -y -g
```

### npx 更新失败时的 rsync 兜底（回退）

当 `npx skills@latest update -y -g` 输出中出现 `✗ Failed to update <skill_name>`（或整体命令失败）时，对**失败的 skill** 从 `/Users/kangll13/aiot/java-code/self/skills/` 下的本地 git 克隆（模块 1 已 git pull 更新）执行 rsync 兜底；npx 更新成功的其他 skill 不受影响、不走兜底。

**这是模块 3 中 rsync 对外部 skill 的唯一用途**：正常路径一律走 npx，rsync 只在 npx 失败时补位。

**项目 → 本地克隆映射**：

| npx 项目 | 本地克隆 | 源 skill 目录 |
|---|---|---|
| superpowers | `self/skills/superpowers/` | `skills/` |
| matt-skills | `self/skills/matt-skills/` | `skills/<分类>/<skill_name>/`（两级，按 skill 名定位同名目录） |
| ui-ux-pro-max-skill | `self/skills/ui-ux-pro-max-skill/` | `.claude/skills/` |
| claude-code-java | `self/skills/claude-code-java/` | `.claude/skills/` |
| baoyu-skills | `self/skills/baoyu-skills/` | `skills/`（补充：`.claude/skills/` 下另有 release-skills） |
| ppt-master | `self/skills/ppt-master/` | `skills/` |
| anthropics-skills | `self/skills/anthropics-skills/` | `skills/`（直接子目录即为 skill 名） |
| ECC | `self/skills/ECC/` | `skills/`（直接子目录即为 skill 名） |
| ponytail | `self/skills/ponytail/` | `skills/`（直接子目录即为 skill 名） |
| archify | `self/skills/archify/` | `archify/`（该目录自身即单个 skill，含 SKILL.md） |
| diagram-design | `self/skills/diagram-design/` | `skills/`（单 skill：diagram-design） |
| andrej-karpathy-skills | `self/skills/andrej-karpathy-skills/` | `skills/`（单 skill：karpathy-guidelines；克隆 remote 为 `multica-ai/andrej-karpathy-skills`，与 lock 源 `forrestchang/...` 不一致，疑上游更名/迁移） |
| humanizer | （无本地克隆） | —（兜底按规则 5 标 `[NPX-FALLBACK-MISS]`） |
| humanizer-zh | （无本地克隆） | —（兜底按规则 5 标 `[NPX-FALLBACK-MISS]`） |
| vercel-agent-skills | `self/skills/vercel-agent-skills/` | `skills/`（直接子目录即为 skill 名） |

**兜底规则**（交集口径，自包含）：

1. 只处理失败清单中的 skill；在对应本地克隆内按 skill 名定位源目录（含 `SKILL.md` 的目录）
2. `~/.agents/skills/<skill_name>/` **已存在** → 先执行文件新旧比对（见 `modules/shared.md`），再 `rsync -rtu`（**不加 `--delete`**，附加常规排除项）；内容不同且目标端更新的文件标记 `[NEWER-TARGET]` 跳过，严禁旧覆盖新
3. `~/.agents/skills/` 中**不存在** → **不新增，跳过**。兜底只补位「运行时已有但 npx 没更新成功」的 skill，不借兜底之机扩充运行时清单
4. 与 `self-skills/` 同名 → 跳过，标记 `[SELF-SKILL-SKIP]`
5. 无本地克隆、或克隆中定位不到该 skill → 标记 `[NPX-FALLBACK-MISS]`，提示用户手动 clone 对应仓库或人工处理；**不自动 clone 仓库**
6. 兜底成功标记 `[NPX-FALLBACK]`；兜底也失败仍标记 `[NPX-FAILED]` 并记录错误
7. **严禁回写 git 克隆**：兜底方向只有「克隆 → 运行时」。克隆是上游镜像不是真源，回写会 dirty 已跟踪文件，模块 1 随即判 `[SKIP-DIRTY]` 永久跳过 `git pull --ff-only`，该克隆静默冻结收不到上游更新。需要长期定制某个外部 skill 时，把它复制进 `self-skills/` 转为自写 skill（改由 3.3 管理），而不是改克隆或运行时副本

### 注意事项

- **必须在用户主目录（`~`）下执行**，不得在项目目录或批处理子 shell 中代执行
- **必须加 `env -u XDG_STATE_HOME`**，否则 lock 路径被劫持导致静默空跑（见“环境变量陷阱”）
- 使用 `-y -g` 标志跳过交互提示（`--yes` 确认安装，`--global` 全局安装并 Copy to all agents）
- 超时 300s，但 `timeout` 在 macOS 默认不存在：按 `timeout` → `gtimeout` → 空 的顺序降级探测，
  探测不到时由调用方（如 Agent 工具超时）控制，**不得因 `command not found: timeout` 直接判定 3.1 失败**；
  超时**不中断后续 3.3 / 3.4 的同步**
- 安装/更新成功标记 `[NPX-AUTO]` 并报告更新的 skill 数量；失败的 skill 先走上述 rsync 兜底，兜底成功标记 `[NPX-FALLBACK]`，兜底不可用或失败标记 `[NPX-FAILED]` / `[NPX-FALLBACK-MISS]`；lock 读不到标记 `[NPX-LOCK-MISS]`，不计入成功
- 这些项目的 skill 最终在 `~/.agents/skills/` 中，模块 4.1 全量 rsync 会同步到知识库
- **模块 4.1A 排除全部 15 个 npx 管理型项目**（见模块 4 文档），避免其 `self/skills/` 下的 git 源结构被误判

### Sub Agent 建议

1. 用 fresh sub agent 预先枚举 15 个 npx 管理型项目，并核对 `~/.agents/.skill-lock.json` 中各 source 的 skill 数，生成执行清单
2. 若上一轮出现 `✗ Failed to update`，由 sub agent 对失败清单做兜底交集草稿：哪些 skill 运行时已存在可兜底、哪些会被拒绝新增、哪些无本地克隆
3. 主线程执行 `env -u XDG_STATE_HOME npx skills@latest update -y -g` 和兜底时的实际 `rsync -rtu`
4. 成功/失败计数、拒绝新增数量和项目级状态由主线程统一汇总

## 3.2 rsync 管理型项目（0 个 — 类别已取消）

本类别已取消，不再有独立走 rsync 常规同步的外部项目：

- claude-code-java 早前并入 3.1（`decebals/claude-code-java`）
- anthropics-skills 现并入 3.1（`anthropics/skills`，初始化 `npx skills@latest add anthropics/skills -y -g`）

模块 3 中 rsync 不再作为外部 skill 的常规同步路径，只剩两个用途：

1. **3.1 失败兜底** — 仅当 `npx skills update` 报 `✗ Failed to update <skill>` 时，按 3.1 的「项目 → 本地克隆映射」从本地克隆补位同步，标记 `[NPX-FALLBACK]`；交集口径、新旧比对、拒绝新增等规则全部见 3.1「兜底规则」
2. **3.3 / 3.4 的双向落地工具** — 自写 skill 与自写命令的部署与回写，见 3.3 / 3.4

### 3.2.1 anthropics-skills 本地克隆（仅供 3.1 兜底读取）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/anthropics-skills/` |
| 远端 | `https://github.com/anthropics/skills.git` |
| npx source | `anthropics/skills` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

该克隆由模块 1 的 `git pull --ff-only` 更新，模块 3 只在 3.1 兜底时**读取**它。

**严禁回写任何外部项目克隆**：兜底方向只有「克隆 → 运行时」。克隆是上游镜像、不是用户真源，回写会 dirty 已跟踪文件，模块 1 随即判 `[SKIP-DIRTY]` 永久跳过 `git pull --ff-only`，克隆静默冻结、收不到上游更新。需要长期定制某个外部 skill 时，正确做法是把它复制进 `self-skills/` 转为自写 skill（自写 skill 对同名冲突拥有最终权威，外部同步一律 `[SELF-SKILL-SKIP]`），而不是改克隆或改运行时副本。

## 3.3 自写 skill 同步（self-skills ↔ 运行时，双向按比对定向）

`agent-skills/self-skills/` 是用户自写 skill 的唯一真源。但用户也可能直接在运行时 `~/.agents/skills/` 里改（会话中临时修、`skill_manage patch` 等）。本步骤**先比对两边、再按文件决定方向**，让两个方向的修改都不丢：仓库里的改动生效到运行时，运行时的改动回收进真源。

**规则**：

- **skill 级门禁：只更新、不新增**（不变）。只处理在 `~/.agents/skills/` 中**已经存在**的自写 skill；运行时没有的绝不私自加入，标记 `[SELF-DEPLOY-SKIP]` 并提示用户人工手动加入
- **文件级方向由比对决定**（口径见 `modules/shared.md` 的“文件新旧比对规则”）：

  | 比对结果 | 方向 | 标记 |
  |---|---|---|
  | 内容一致 | 无操作（顺带对齐 mtime） | — |
  | 内容不同，**真源更新** | 真源 → 运行时 | `[SELF-DEPLOY]` |
  | 内容不同，**运行时更新** | 运行时 → 真源（回写） | `[SELF-PULLBACK]` |
  | 仅运行时存在（不在排除清单内） | 运行时 → 真源（回写） | `[SELF-PULLBACK-NEW]` |
  | 仅真源存在 | 真源 → 运行时 | `[SELF-DEPLOY]` |

- **执行顺序固定为「先回写、后部署」**：回写后运行时更新的文件已在真源对齐，部署阶段不会再把旧内容推回运行时；两步收敛到「两边各自最新内容的并集」
- 两个方向都用 `rsync -rtu`，**都不加 `--delete`**：任何一边的文件删除都不传播；`self-skills/` 中 skill 的删除、重命名只能由用户手动执行
- **`_mideameta.json` 永远运行时权威**：不参与比对、不部署、不回写（市场元数据以运行时为准，仓库副本不得回滚其版本）
- 排除 `.git/`、`.DS_Store`、`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`node_modules/` 等无关文件与缓存
- 排在 3.1（npx + 失败兜底）之后执行：同名冲突时自写版本是最终权威
- 自写 skill 名单 = `self-skills/` 下的实际子目录，不写死清单；非目录条目一律跳过
- **审查义务**：所有 `[SELF-PULLBACK]` / `[SELF-PULLBACK-NEW]` 必须**逐文件**列入汇总。判新旧只依赖 mtime，mtime 被 `cp` 不带 `-p`、git 操作、不带 `-t` 的 rsync 打乱时会误判并把旧内容当新内容回写；发现误回写由用户手动 git 回滚，本技能不自动撤销

### 步骤 A：比对分类（只读，不改任何文件）

```bash
self_skills_dir="/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills"
runtime_dir="$HOME/.agents/skills"
EXCL='(^|/)\.DS_Store$|_mideameta\.json|(^|/)\.git/|__pycache__/|\.pyc$|\.idea/|\.vscode/|node_modules/'

for skill_dir in "$self_skills_dir"/*/; do
  [ -d "$skill_dir" ] || continue
  n=$(basename "$skill_dir"); rt="$runtime_dir/$n"
  [ -d "$rt" ] || { printf '[SELF-DEPLOY-SKIP] %s（运行时不存在，需人工手动加入）\n' "$n"; continue; }

  while IFS= read -r f; do
    printf '%s\n' "$f" | grep -qE "$EXCL" && continue
    s="$skill_dir/$f"; t="$rt/$f"
    if   [ ! -f "$t" ]; then                  printf '[SELF-DEPLOY]        %s :: %s（仅真源存在）\n' "$n" "$f"
    elif cmp -s "$s" "$t"; then               :
    elif [ "$t" -nt "$s" ]; then              printf '[SELF-PULLBACK]        %s :: %s（运行时更新，回写真源）\n' "$n" "$f"
    else                                      printf '[SELF-DEPLOY]        %s :: %s（真源更新，部署运行时）\n' "$n" "$f"; fi
  done < <(cd "$skill_dir" && find . -type f | sed 's|^\./||')

  while IFS= read -r f; do
    printf '%s\n' "$f" | grep -qE "$EXCL" && continue
    [ -f "$skill_dir/$f" ] || printf '[SELF-PULLBACK-NEW]    %s :: %s（仅运行时存在，回写真源）\n' "$n" "$f"
  done < <(cd "$rt" && find . -type f | sed 's|^\./||')
done
```

### 步骤 B：先回写，后部署

```bash
EXCL=(--exclude '.git/' --exclude '.DS_Store' --exclude '__pycache__/' \
      --exclude '*.pyc' --exclude '.idea/' --exclude '.vscode/' \
      --exclude 'node_modules/' --exclude '_mideameta.json')

for skill_dir in "$self_skills_dir"/*/; do
  [ -d "$skill_dir" ] || continue
  n=$(basename "$skill_dir"); rt="$runtime_dir/$n"
  [ -d "$rt" ] || continue          # skill 级不新增，步骤 A 已报 [SELF-DEPLOY-SKIP]

  # B1 回写：运行时 → 真源（-u 只放行运行时更新或真源缺失的文件）
  back=$(rsync -rtu --itemize-changes "${EXCL[@]}" "$rt/" "$skill_dir" 2>&1) || \
    { printf '[SELF-PULLBACK-FAILED] %s\n' "$n"; continue; }
  nb=$(printf '%s\n' "$back" | grep -cE '^>f' || true)

  # B2 部署：真源 → 运行时（-u 只放行真源更新或运行时缺失的文件）
  fwd=$(rsync -rtu --itemize-changes "${EXCL[@]}" "$skill_dir" "$rt/" 2>&1) || \
    { printf '[SELF-DEPLOY-FAILED] %s\n' "$n"; continue; }
  nf=$(printf '%s\n' "$fwd" | grep -cE '^>f' || true)

  if [ "$nb" -gt 0 ] || [ "$nf" -gt 0 ]; then
    printf '[SELF-SYNC] %s（回写 %s / 部署 %s）\n' "$n" "$nb" "$nf"
    [ "$nb" -gt 0 ] && printf '%s\n' "$back" | grep -E '^>f' | sed 's/^/    pullback: /'
    [ "$nf" -gt 0 ] && printf '%s\n' "$fwd"  | grep -E '^>f' | sed 's/^/    deploy:   /'
  else
    printf '[SELF-DEPLOY] %s（无变化）\n' "$n"
  fi
done
```

### Sub Agent 建议

1. sub agent 执行步骤 A 的只读比对，生成 `[SELF-DEPLOY]` / `[SELF-PULLBACK]` / `[SELF-PULLBACK-NEW]` / `[SELF-DEPLOY-SKIP]` 分类草稿
2. 主线程复核草稿后执行步骤 B 的真实 `rsync -rtu`（先回写后部署），并统一计数
3. 回写清单必须原样进入最终汇总供用户审查；sub agent 不得自行判定“这个回写不合理”而丢弃，只能标注疑点上报

## 3.4 自写命令同步（commands/ ↔ 运行时，双向按比对定向）

`agent-skills/commands/` 是自写命令的编辑面。与 3.3 同理，用户也可能直接改运行时 `~/.agents/commands/`。本步骤**先比对、再按结果决定方向**，两个方向的修改都不丢。

**规则**：

- 同步范围为**自写命令**（当前：`dev-commit.md`、`dev-paradigm.md`、`opsx-apply.md`、`opsx-propose.md`）；OpenSpec 生成的 `opsx/` **子目录**命令集由模块 2 的 `.claude -> .agents` 迁移管理，不在本步骤范围。**注意区分**：根目录扁平的 `opsx-apply.md` / `opsx-propose.md` 是用户自写命令（归本步骤），`opsx/` 子目录才是 OpenSpec 生成物（归模块 2），二者不得混淆。新增自写命令需人工把文件名加入本清单
- **文件级方向由比对决定**（口径同 3.3，见 `modules/shared.md`）：

  | 比对结果 | 方向 | 标记 |
  |---|---|---|
  | 内容一致 | 无操作 | — |
  | 内容不同，**仓库更新** | `commands/` → 运行时 | `[COMMAND-DEPLOY]` |
  | 内容不同，**运行时更新** | 运行时 → `commands/`（回写） | `[COMMAND-PULLBACK]` |

- **命令级门禁：只更新、不新增**。只处理在 `~/.agents/commands/` 中**已经存在**的命令；运行时没有的绝不私自加入，标记 `[COMMAND-DEPLOY-SKIP]` 并提示用户人工手动加入
- **执行顺序固定为「先回写、后部署」**，与 3.3 一致；单文件场景下两个方向互斥，只会命中其一
- 两个方向都用 `rsync -rtu`，**都不加 `--delete`**，不删除运行时中额外的内容
- **审查义务**：`[COMMAND-PULLBACK]` 必须列入汇总。mtime 失真时会把旧命令当新内容回写；发现误回写由用户手动 git 回滚，本技能不自动撤销
- 确需“旧覆盖新”（刻意回退到某个版本）必须写明原因由用户手动执行，本流程绝不自动做

```bash
commands_dir="/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/commands"
rt_cmds="$HOME/.agents/commands"

for cmd in dev-commit.md dev-paradigm.md opsx-apply.md opsx-propose.md; do
  s="$commands_dir/$cmd"; t="$rt_cmds/$cmd"
  [ -f "$s" ] || { printf '[COMMAND-MISSING-SRC] %s（仓库中不存在）\n' "$cmd"; continue; }

  # 命令级只更新不新增：运行时不存在的，留给用户人工手动加入
  if [ ! -e "$t" ]; then
    printf '[COMMAND-DEPLOY-SKIP] %s（运行时不存在，需人工手动加入）\n' "$cmd"
    continue
  fi

  if cmp -s "$s" "$t"; then
    printf '[COMMAND-DEPLOY] %s（内容一致，无变化）\n' "$cmd"
  elif [ "$t" -nt "$s" ]; then
    # 运行时更新 → 回写仓库（先回写）
    rsync -rtu "$t" "$s" && printf '[COMMAND-PULLBACK] %s（运行时更新，已回写仓库，需审查）\n' "$cmd" \
                           || printf '[COMMAND-PULLBACK-FAILED] %s\n' "$cmd"
  else
    # 仓库更新 → 部署运行时（后部署）
    rsync -rtu "$s" "$t" && printf '[COMMAND-DEPLOY] %s（仓库更新，已部署运行时）\n' "$cmd" \
                         || printf '[COMMAND-DEPLOY-FAILED] %s\n' "$cmd"
  fi
done
```
