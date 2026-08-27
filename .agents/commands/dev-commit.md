---
description: "读取 Git diff 生成三行中文提交说明并执行提交。/dev-commit [可选：提交说明或指令]"
---

为当前 Git 改动生成统一格式的中文提交说明，并在用户确认后执行提交。

$ARGUMENTS

---

## Step 1 — 读取状态

并行执行以下命令，收集提交所需信息：

```bash
git rev-parse --abbrev-ref HEAD    # 当前分支名（提取 JIRA）
git diff --cached                   # staged diff
git diff                            # unstaged diff
git log --oneline -5                # 近期提交风格参考
```

确认：
- 当前分支名
- staged 与 unstaged 的改动范围
- 是否存在无关改动（如 `__pycache__`、临时文件、嵌入式 git 仓库）

---

## Step 2 — 判断提交类型

根据真实 diff 判断主类型（按用户最关心的主目标选一个，不混写）：

| 类型 | 适用场景 |
|------|----------|
| `FEAT` | 引入新能力、对外新增功能 |
| `FIX` | 修复错误行为、缺陷、异常、兼容性问题 |
| `ENH` | 不新增对外功能，但改善性能、稳定性、结构、体验 |
| `DOC` | 仅文档、说明、示例、注释等改动 |
| `CHORE` | 构建、脚本、配置、版本号、依赖升级等工程性调整 |

`FIX` 与 `ENH` 同时存在时：主要恢复正确行为用 `FIX`，主要提升性能/结构/可维护性用 `ENH`。

---

## Step 3 — 提取 JIRA

从当前 Git 分支名提取 JIRA 标识：

1. 优先适配本项目常见分支：`feature_YYYYMMDD_XXX-xxxx`、`fix_YYYYMMDD_XXX-xxxx`（JIRA 工单号格式为 `PROJECT-NUMBER`，如 `IOTRP-4697`、`AIOT-123`）— 按 `_` 分段取最后一段
2. 回退：按 `/` 分段取最后一段
3. 既不含 `_` 也不含 `/`：直接沿用整个分支名
4. 不在 Git 分支或无法获取：标记为 `[待补充]`

示例：
- `feature_20260721_IOTRP-4697` → `IOTRP-4697`
- `fix_20260721_AIOT-123` → `AIOT-123`
- `feature/robot/AIOT-123` → `AIOT-123`
- `main` → `main`

若用户通过 $ARGUMENTS 明确指定 JIRA 值（如"JIRA: 无"），以用户指定为准。

---

## Step 4 — 生成提交说明

输出三行格式，严格控制长度：

```text
<TYPE>: <业务修改总结>
JIRA: <branch-last-segment>
DIFF: <具体修改代码总结>
```

**第一行**（≤ 200 字符）：
- 用动宾短语直接说结果，例如"优化技能同步模块的差异处理"
- 先写业务或工程价值，再写对象
- 不写"修改代码""调整一些内容"这类空话

**第二行**：JIRA 标识，不杜撰工单号

**第三行**（≤ 1000 字符）：
- 基于实际 diff，不凭想象补内容
- 总结关键改动：改了什么、影响哪里、是否补充约束或流程
- 不重复堆砌文件列表
- 推荐句式：`DIFF: 更新 A 与 B，补充 C 规则，调整 D 阶段顺序，并明确 E 的校验边界。`

内容优先中文，保留必要英文术语、模块名、类名、命令名。

**示例：**

```text
ENH: 优化 dev-commit 的 JIRA 提取规则以适配下划线分支命名
JIRA: main
DIFF: dev-commit.md 更新 JIRA 提取逻辑，新增 feature_YYYYMMDD_IOTRP-xxxx 下划线命名适配，并补充 fallback 层级说明。
```

---

## Step 5 — 输出与确认

1. 向用户展示三行提交说明
2. 询问用户是否提交（或用户已在 $ARGUMENTS 中明确要求提交时直接执行）
3. 若用户只要文案，输出三行后停止

---

## Step 6 — 执行提交（仅当用户确认后）

1. 暂存相关文件，排除以下无关改动：
   - `**/__pycache__/**`、`*.pyc`
   - `.DS_Store`
   - 项目下的 `doc/`、`docs/`、`openspec/`、`.agents/`
   - 嵌入式 git 仓库（`git add` 时出现 "embedded git repository" 警告的路径，用 `git rm --cached` 取消暂存）
   - 其他临时文件
2. 复核待提交文件范围，确保不混入无关改动
3. 使用三行说明作为 commit message 执行 `git commit`
4. 不得默认 `git push`；push 需要单独授权

---

## 守则

1. 先看 diff，再写总结；禁止空泛概括
2. 优先写"为什么值得提交"，其次才是"改了哪些文件"
3. 长度超限时，先压缩形容词和重复背景，不删关键事实
4. 若改动不足以形成单一逻辑提交，先提醒用户拆分提交
5. 不使用 `feat(scope): subject` 这种 Conventional Commits 格式
6. 只在用户明确要求时执行 `git add`、`git commit`、`git push`
7. 默认不提交项目下的 `doc/`、`docs/`、`openspec/`、`.agents/` 目录；若用户明确要求提交，再单独复核这些路径

$ARGUMENTS
