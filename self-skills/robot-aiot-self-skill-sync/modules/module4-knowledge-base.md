# 模块 4：同步到个人知识库（agent-skills）

> 共享规则见 `modules/shared.md`
> 确定性逻辑已内置于 `scripts/m4_kb_sync.sh`，主线程只调脚本、审查 `[NEWER-TARGET]` / `[DUPLICATE-SKILL]` 清单、决定是否放行。

**目的**：将 `~/.agents/skills/` 中经模块 2-3 更新后的 skill 全量同步到个人知识库 `agent-skills/skills/`。知识库只收录外部 skill；自写 skill 真源在 `agent-skills/self-skills/`，同步必须排除它们，且**禁止向 `self-skills/` 写入任何内容**（脚本无任何路径指向它，结构保证）。

```bash
S=~/.agents/skills/robot-aiot-self-skill-sync/scripts/m4_kb_sync.sh

$S --dry-run   # 预检：[NEWER-TARGET] 清单 + 全部同步对（只读）
$S             # 正式执行 4.1 → 4.1A → 4.2 → 4.3 → 4.4
```

## 保护规则例外（用户明确授权，脚本内置）

- **允许**：`~/.agents/skills/` 覆盖到 `agent-skills/skills/`（`rsync -rtu` 不加 `--delete`，覆盖前 `[NEWER-TARGET]` 预检）
- **禁止写入 `self-skills/`**：回写真源只允许发生在模块 3.3/3.4，来源只能是运行时
- **禁止删除 skill**：任何模块都不允许删除 skill 目录或文件，只能新增或更新；删除只能用户手动执行（防止误删知识库积累）
- **禁止** `--delete`、`git add/commit/push`、`git reset/checkout --/clean`
- 同步后仅报告变更清单，由用户自行审查提交

## 脚本步骤

### 4.1 运行时全量 → 知识库
`~/.agents/skills/` → `agent-skills/skills/`，排除 `self-skills/` 下全部自写 skill 名（排除项用 `/名称` 锚定顶层，避免误伤 skill 内部同名文件）+ 统一排除项（`.git/`、`.gitignore`、`.gitmodules`、`.DS_Store`、`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`node_modules/`、`_mideameta.json`）。被排除的自写名单在输出中列出。`_mideameta.json` 是市场元数据只属于运行时，知识库不需要（不影响 4.4 备份保留运行时原貌）。

### 4.1A `self/skills/` 项目源补充 → 知识库
兼容四类结构，规则脚本内置：

- **排除 16 个 npx 管理型项目**（清单在 `config.sh` 的 `NPX_PROJECTS`）：它们走 3.1 npx + 4.1 全量，避免 git 源结构被误判。humanizer / humanizer-zh 当前无本地克隆天然扫不到；将来补克隆无须改动（按 NPX_PROJECTS 排除）
- **gstack 特例最先判断**：根目录同时有 `SKILL.md`（路由入口）和 `.agents/skills/`（54 个子技能），必须走 `.agents/skills/` 分支逐个同步，禁止整目录同步（会把 1G+ 项目本体和 `node_modules/` 带入知识库）
- 根目录有 `SKILL.md` → 单 skill 项目整目录同步（其下 `skills/` 嵌套同名副本不展开，避免 `[DUPLICATE-SKILL]`）
- `skills/`、`.claude/skills/`、`.agents/skills/` 三种多技能结构**可在同一项目内并存**（OpenSpec = skills/ + .agents/skills/，hyperframes = 三者并存），必须全部遍历，禁止命中一个跳过其余
- 同一 `skill_name` 出现在多个结构 → `[DUPLICATE-SKILL]`，报告冲突路径清单并跳过，禁止自动挑选其一覆盖
- **路径作用域**：`.claude/skills/`、`.agents/skills/` 均指 `self/skills/<project>/` 项目内相对路径，禁止回退到 `~/.claude/skills/` 或 `~/.agents/skills/` 查找（运行时全量只由 4.1 负责）

### 4.1B 统一发现（非默认，仅疑难兜底）
项目结构不规则时允许「查找 `SKILL.md` 倒推父目录为 skill 根」，只限 `self/skills/<project>/` 内部，禁止跨到用户根目录；同名冲突同样 `[DUPLICATE-SKILL]` 跳过。此逻辑不默认执行，需要时主线程手动定位后交给 4.1A 的同步对处理。

### 4.2 commands → 知识库
`~/.agents/commands/` → `agent-skills/commands/`，`rsync -rtu` 不加 `--delete`，`[NEWER-TARGET]` 预检。

### 4.3 变更报告（只读）
`git -C agent-skills status --short`，报告新增(??)/更新(M) 数量与前 50 行清单。**不执行 `git add`/`git commit`**，由用户自行审查提交。

### 4.4 运行时 → `.claude/skills/` 备份
`rsync -rtu` 不加 `--delete`，保留 `.claude/skills/` 额外文件，`[NEWER-TARGET]` 预检，输出 `[BACKUP-SYNC]` 数量。备份含已部署的自写 skill 属正常——下次模块 2 迁移会对其输出 `[SELF-SKILL-SKIP]`，不会回滚。目的仅是运行时备份，不改变模块 2 中 `.claude/` 作为 OpenSpec 权威源的关系；下次 `openspec update` 有权覆盖 `.claude/skills/` 任何内容。

## 汇总口径

- 4.1 记「全量同步」、4.1A 记「项目源补充同步」，分开统计不重复计
- `[NEWER-TARGET]`（目标端更新被跳过）、`[DUPLICATE-SKILL]`（冲突跳过）必须逐条列入汇总
- `[BACKUP-SYNC]` 单独记录，不得与模块 2 的生成状态或迁移结果混为一条
