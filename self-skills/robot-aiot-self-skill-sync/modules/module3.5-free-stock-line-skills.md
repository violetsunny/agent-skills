# 模块 3.5：同步到 free-stock-line-skills 汇总项目

> 共享规则见 `modules/shared.md`

**目的**：`free-stock-line-skills/` 是用户自行维护的汇总 skill 项目。模块 1 完成后，将 `self/skills/` 下更新的项目内容强制同步到 `free-stock-line-skills/` 中匹配的目录，保持汇总项目与源项目一致。

### 路径

| 字段 | 值 |
|---|---|
| 目标目录 | `/Users/kangll13/aiot/java-code/self/gggggggood/free-stock-line-skills/` |
| 源目录 | `self/skills/` 下各项目（模块 1 已 git pull 更新） |

### 保护规则

- **`stock-replay-workbench` 是重点保护项目，禁止任何修改、同步或覆盖。**
- 非_skill_ 目录（`docs/`、`scripts/`、`tests/`、`openspec/`）跳过，不同步。
- **跳过清单必须大小写不敏感比对**：源名与目标名都转小写后匹配清单。`case` 大小写敏感而 `find -iname` 大小写不敏感，混用会被 `OpenSpec` / `Stock-Replay-Workbench` 这类混合大小写名绕过（源端 `self/skills/OpenSpec` 实际存在）。
- **rsync 必须加 `--exclude '.git/'`**：目标端 8 个目录是模块 1 独立拉取的 git 克隆，不排除会用源端 `.git/` 覆盖目标端，破坏仓库身份。
- 同步使用 `rsync -rtu`（**不加 `--delete`**），保留用户在汇总项目中自定义的文件（如 `AGENTS.md`、`INDEX.md` 等），只覆盖源端有更新的文件和新增文件；`-t` 保留 mtime、`-u` 跳过目标端更新的文件（见 `modules/shared.md` 的“文件新旧比对规则”，被跳过的文件标记 `[NEWER-TARGET]`）。
- **`[NEWER-TARGET]` 必须显式检测**：`rsync -rtu` 静默跳过、输出为空，须用两次 dry-run 差值（`rsync -rtn -i` 减 `rsync -rtun -i`）算出数量，预检不得加 `--ignore-times`。
- 该目录位于保护目录 `gggggggood/` 下，但本同步是用户明确要求的操作，适用与模块 4 相同的例外规则。

### 同步流程

```
for each project in self/skills/:
  1. 获取项目名（如 a-stock-data、Stock-Analysis-Skill），转小写
  2. 小写名命中跳过清单（docs/scripts/tests/openspec/stock-replay-workbench）
     → [SKIP-PROTECTED] 跳过
  3. 在 free-stock-line-skills/ 中做大小写不敏感匹配（-mindepth 1 -maxdepth 1）
     → 未匹配：[SKIP-NOMATCH] 跳过
     → 匹配到：目标名转小写再校验一次跳过清单
        → 命中：[SKIP-PROTECTED] 跳过
        → 未命中：两次 dry-run 预检算出 will_send / newer_target，
          再 rsync -rtu --exclude '.git/' source/ → <matched_name>/
  4. 按 rsync 退出码与预检结果分类输出：
     rc≠0 → [FAIL]；will_send=0 且 newer_target=0 → [UPTODATE]；
     newer_target>0 → [SYNC+NEWER-TARGET]；其余 → [SYNC]
```

### 匹配规则

- 按**目录名大小写不敏感**匹配（macOS 文件系统默认大小写不敏感，但 rsync 保留目标目录名）
- `find` 必须带 `-mindepth 1`：`-maxdepth 1` 含 depth 0（`target_base` 自身），源项目若与目标根目录同名会 rsync 进根目录
- 源端支持三种项目结构：
  - 单 skill 项目（`SKILL.md` 在根目录）→ 整目录同步
  - 多 skill 项目（`skills/` 子目录）→ 整目录同步（包含 `skills/` 结构）
  - `.claude/skills/` 结构 → 整目录同步

### 同步命令

```bash
src_base="/Users/kangll13/aiot/java-code/self/skills"
target_base="/Users/kangll13/aiot/java-code/self/gggggggood/free-stock-line-skills"

# 跳过/保护清单（小写形式；源名与目标名均转小写比对，防大小写绕过）
SKIP_LIST="docs scripts tests openspec stock-replay-workbench"

for src_project in "$src_base"/*/; do
  [ -d "$src_project" ] || continue
  project_name=$(basename "$src_project")
  pn_lower=$(printf '%s' "$project_name" | tr '[:upper:]' '[:lower:]')

  # 源名命中跳过清单 → 不同步
  case " $SKIP_LIST " in
    *" $pn_lower "*) echo "[SKIP-PROTECTED] $project_name"; continue ;;
  esac

  # 大小写不敏感匹配目标目录；-mindepth 1 排除 target_base 自身
  match=$(find "$target_base" -mindepth 1 -maxdepth 1 -type d -iname "$project_name" 2>/dev/null | head -1)
  [ -z "$match" ] && { echo "[SKIP-NOMATCH] $project_name"; continue; }

  # 目标名二次校验（源名与目标名大小写可能不同）
  mn_lower=$(printf '%s' "$(basename "$match")" | tr '[:upper:]' '[:lower:]')
  case " $SKIP_LIST " in
    *" $mn_lower "*) echo "[SKIP-PROTECTED] $project_name → $(basename "$match")"; continue ;;
  esac

  # 预检：两次 dry-run 差值 = -u 将跳过的「目标端更新」文件数
  # 不加 --ignore-times，否则两端完全相同的文件也会计入，虚增 newer_target
  all_diff=$(rsync -rtn -i --exclude '.git/' "$src_project" "$match/" 2>/dev/null | grep -c '^[<>ch.]')
  will_send=$(rsync -rtun -i --exclude '.git/' "$src_project" "$match/" 2>/dev/null | grep -c '^[<>ch.]')
  newer_target=$((all_diff - will_send))

  # 正式同步：--exclude '.git/' 保护目标独立仓库身份；不加 --delete 保留用户自定义文件
  out=$(rsync -rtu --exclude '.git/' "$src_project" "$match/" 2>&1); rc=$?

  if [ "$rc" -ne 0 ]; then
    echo "[FAIL] $project_name → $(basename "$match") rc=$rc: $out"
  elif [ "$will_send" -eq 0 ] && [ "$newer_target" -eq 0 ]; then
    echo "[UPTODATE] $project_name → $(basename "$match")"
  elif [ "$newer_target" -gt 0 ]; then
    echo "[SYNC+NEWER-TARGET] $project_name → $(basename "$match") 同步 $will_send 项，跳过 $newer_target 个目标端更新文件"
  else
    echo "[SYNC] $project_name → $(basename "$match") 同步 $will_send 项"
  fi
done
```

**三条强制约束（实测违反后果）**：

1. **跳过清单必须大小写不敏感**。`case` 是大小写敏感匹配，`find -iname` 是大小写不敏感匹配，两者混用会绕过保护：源端 `self/skills/OpenSpec`（混合大小写，实际存在）不匹配 `case` 中的 `openspec`，却被 `find -iname` 匹配到目标 `free-stock-line-skills/openspec`，导致独立 git 仓库被覆盖。`stock-replay-workbench` 重点保护同理会被 `Stock-Replay-Workbench` 绕过。修复方式：源名与目标名都转小写后比对清单。

2. **rsync 必须加 `--exclude '.git/'`**。目标端 8 个目录（`a-stock-data`、`claude-trading-skills`、`global-stock-data`、`openspec`、`short-term-stock-picker`、`stock-analysis-skill`、`stock-analyst`、`stock-trade-skill`）是模块 1 独立拉取的 git 克隆。不加排除时 rsync 会用源端 `.git/` 覆盖目标端 `.git/`（实测 `.git/HEAD` 被改写），破坏仓库身份并使模块 1 后续拉取失效。

3. **`[NEWER-TARGET]` 必须显式检测，不得依赖 rsync 静默跳过**。`rsync -rtu` 跳过目标端更新文件时输出为空，脚本无从标记。用两次 dry-run 差值检测：`rsync -rtn -i`（全部差异）减 `rsync -rtun -i`（实际传输）。**预检不得加 `--ignore-times`**，否则两端完全相同的文件也计入差异，实测虚增 `newer_target`（3 文件场景：正确值 1，加 `--ignore-times` 得 2）。

`find` 必须带 `-mindepth 1`：`-maxdepth 1` 含 depth 0（`target_base` 自身），源项目若与目标根目录同名会 rsync 进根目录。

rsync 退出码必须检查：rc≠0 时标 `[FAIL]` 并附输出，禁止无条件 `echo "[SYNC]"`（实测 rsync 到不存在目录 rc=23，原写法仍报同步成功）。

### 汇总统计

按以下标记计数，每类列出项目名（与模块 1 汇总口径保持一致，不用 emoji）：

| 标记 | 含义 | 是否需用户处理 |
|------|------|------|
| `[SYNC]` | 已同步，全部为源端更新或新增文件 | 否 |
| `[SYNC+NEWER-TARGET]` | 已同步，但有目标端更新文件被 `-u` 跳过 | 是，需确认是否丢失汇总项目自定义内容 |
| `[UPTODATE]` | 两端一致，无文件传输 | 否 |
| `[SKIP-PROTECTED]` | 命中跳过清单（含 `stock-replay-workbench` 重点保护） | 否（豁免） |
| `[SKIP-NOMATCH]` | 目标端无大小写不敏感匹配目录 | 否 |
| `[FAIL]` | rsync 退出码非 0 | 是，需查看输出定位原因 |

`[SYNC]` 与 `[SYNC+NEWER-TARGET]` 必须附带传输项数，`[FAIL]` 必须附带 rsync 输出，否则汇总不可核查。

### Sub Agent 建议

1. 先由 fresh sub agent 做大小写不敏感匹配草稿，识别哪些项目能同步、哪些无匹配、哪些属于保护或非 skill 目录
2. 主线程再执行真实 `rsync -rtu --exclude '.git/'`，确保保护项目和跳过规则得到严格执行
3. `stock-replay-workbench` 的保护决策只能由主线程维持，sub agent 只能标记不可碰
4. sub agent 做匹配草稿时必须同时报告源名与目标名的**小写归一化结果**，主线程据此复核跳过清单，不得只看原始大小写
