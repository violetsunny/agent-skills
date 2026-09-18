# 模块 3.5：同步到 free-stock-line-skills 汇总项目

> 共享规则见 `modules/shared.md`
> 确定性逻辑已内置于 `scripts/m35_stock_sync.sh`，主线程只调脚本、解读标记。

**目的**：`free-stock-line-skills/` 是用户自行维护的汇总 skill 项目。模块 1 完成后，将 `self/skills/` 下更新的项目内容同步到其中匹配的目录，保持一致。

```bash
S=~/.agents/skills/robot-aiot-self-skill-sync/scripts/m35_stock_sync.sh

$S --dry-run   # 预检：输出将同步项数与 [NEWER-TARGET] 跳过数（只读）
$S             # 正式同步
```

## 保护规则（脚本内置）

- **`stock-replay-workbench` 重点保护，禁止任何修改、同步或覆盖**（在跳过清单内）
- 非 skill 目录（`docs/`、`scripts/`、`tests/`、`openspec/`）跳过；清单在 `scripts/config.sh` 的 `M35_SKIP_LIST`
- `rsync -rtu` 不加 `--delete`，保留用户自定义文件（`AGENTS.md`、`INDEX.md` 等）；`-t` 保留 mtime、`-u` 跳过目标端更新文件
- 该目录位于保护目录 `gggggggood/` 下，但本同步是用户明确要求的操作，适用与模块 4 相同的例外规则

## 三条强制约束（实测违反后果，脚本已内置防护）

1. **跳过清单大小写不敏感**：源名与目标名都转小写后比对。`case` 大小写敏感而 `find -iname` 不敏感，混用会被绕过——实测源端 `self/skills/OpenSpec`（混合大小写）不匹配 `case` 中的 `openspec`，却被 `find -iname` 匹配到目标，导致独立 git 仓库被覆盖。脚本化改造时 dry-run 曾再次拦截同类失效（`local` 声明笔误使清单整体失效）。
2. **rsync 必须 `--exclude '.git/'`**：目标端 8 个目录（a-stock-data、claude-trading-skills、global-stock-data、openspec、short-term-stock-picker、stock-analysis-skill、stock-analyst、stock-trade-skill）是模块 1 独立拉取的 git 克隆，不排除会用源端 `.git/` 覆盖目标端（实测 `.git/HEAD` 被改写），破坏仓库身份。
3. **`[NEWER-TARGET]` 显式检测**：`rsync -rtu` 静默跳过、输出为空，脚本用两次 dry-run 差值（`rsync -rtn -i` 减 `rsync -rtun -i`）算出数量；**预检不得加 `--ignore-times`**（两端相同文件也会计入，实测虚增 newer_target：正确值 1 得 2）。

其他内置细节：`find -mindepth 1`（`-maxdepth 1` 含 depth 0，源项目与目标根同名会 rsync 进根目录）；rsync 退出码必查（实测 rc=23 时原写法仍报成功）；源端三种项目结构（根 `SKILL.md` / `skills/` / `.claude/skills/`）均整目录同步。

## 汇总口径

| 标记 | 含义 | 是否需用户处理 |
|------|------|------|
| `[SYNC]` | 已同步，全部为源端更新或新增（附传输项数） | 否 |
| `[SYNC+NEWER-TARGET]` | 已同步，但有目标端更新文件被 `-u` 跳过（附两个数量） | 是，需确认是否丢失汇总项目自定义内容 |
| `[UPTODATE]` | 两端一致，无文件传输 | 否 |
| `[SKIP-PROTECTED]` | 命中跳过清单（含 stock-replay-workbench 重点保护） | 否（豁免） |
| `[SKIP-NOMATCH]` | 目标端无大小写不敏感匹配目录 | 否 |
| `[FAIL]` | rsync 退出码非 0（附输出） | 是，需定位原因 |

`[SYNC]` 与 `[SYNC+NEWER-TARGET]` 必须附传输项数，`[FAIL]` 必须附 rsync 输出，否则汇总不可核查。
