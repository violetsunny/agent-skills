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
- 同步使用 `rsync -rtu`（**不加 `--delete`**），保留用户在汇总项目中自定义的文件（如 `AGENTS.md`、`INDEX.md` 等），只覆盖源端有更新的文件和新增文件；`-t` 保留 mtime、`-u` 跳过目标端更新的文件（见 `modules/shared.md` 的“文件新旧比对规则”，被跳过的文件标记 `[NEWER-TARGET]`）。
- 该目录位于保护目录 `ggggggood/` 下，但本同步是用户明确要求的操作，适用与模块 4 相同的例外规则。

### 同步流程

```
for each project in self/skills/:
  1. 获取项目名（如 a-stock-data、Stock-Analysis-Skill）
  2. 在 free-stock-line-skills/ 中做大小写不敏感匹配
     → 匹配到：执行文件新旧比对（见 shared.md），再
       rsync -rtu source/ → free-stock-line-skills/<matched_name>/
       内容不同且目标端更新的文件标记 [NEWER-TARGET] 跳过
     → 未匹配：跳过
  3. 跳过 stock-replay-workbench、docs/、scripts/、tests/、openspec/
```

### 匹配规则

- 按**目录名大小写不敏感**匹配（macOS 文件系统默认大小写不敏感，但 rsync 保留目标目录名）
- 源端支持三种项目结构：
  - 单 skill 项目（`SKILL.md` 在根目录）→ 整目录同步
  - 多 skill 项目（`skills/` 子目录）→ 整目录同步（包含 `skills/` 结构）
  - `.claude/skills/` 结构 → 整目录同步

### 同步命令

```bash
src_base="/Users/kangll13/aiot/java-code/self/skills"
target_base="/Users/kangll13/aiot/java-code/self/gggggggood/free-stock-line-skills"

for src_project in "$src_base"/*/; do
  [ -d "$src_project" ] || continue
  project_name=$(basename "$src_project")
  
  # 跳过非 skill 目录
  case "$project_name" in
    docs|scripts|tests|openspec|stock-replay-workbench) continue ;;
  esac
  
  # 大小写不敏感匹配
  match=$(find "$target_base" -maxdepth 1 -type d -iname "$project_name" 2>/dev/null | head -1)
  [ -z "$match" ] && continue
  
  # 强制同步，不加 --delete，保留用户自定义文件；-t 保留 mtime、-u 防旧覆盖新
  rsync -rtu "$src_project" "$match/"
  echo "[SYNC] $project_name → $(basename "$match")"
done
```

### 汇总统计

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 同步 | N | 源端和目标端都有匹配，已同步 |
| ⏭️ 跳过 | N | 目标端无匹配，或为非 skill 目录 |
| 🔒 保护 | 1 | stock-replay-workbench，禁止修改 |

### Sub Agent 建议

1. 先由 fresh sub agent 做大小写不敏感匹配草稿，识别哪些项目能同步、哪些无匹配、哪些属于保护或非 skill 目录
2. 主线程再执行真实 `rsync -rtu`，确保保护项目和跳过规则得到严格执行
3. `stock-replay-workbench` 的保护决策只能由主线程维持，sub agent 只能标记不可碰
