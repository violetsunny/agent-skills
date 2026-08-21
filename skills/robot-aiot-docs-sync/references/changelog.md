# Step 5: CHANGELOG 生成

从 Git 历史自动生成 `CHANGELOG.md`。本模块吸收 `changelog-gen` 和 `changelog-generator` 的能力：既支持 Conventional Commits 分类，也优先兼容项目现有 changelog 风格、tag 规则和版本习惯。

## 先检查已有风格

更新前先读取已有 `CHANGELOG.md`、最近 tag 和仓库约定，按以下优先级判断：

1. `AGENTS.md` / `CLAUDE.md` / README 中是否有显式版本规则
2. 现有 `CHANGELOG.md` 的标题层级、分组顺序、链接风格
3. Git tag 格式，例如 `v1.2.3`、`release-1.2.3`、`2026.08`
4. 都无法识别时，再回退到默认的 Keep a Changelog + SemVer

## 历史获取

1. 优先读取最近 tag
2. 有 tag 时，统计上个 tag 到 `HEAD` 的提交
3. 无 tag 时，读取有限条数的全部历史
4. 初筛优先使用 `git log --oneline`，只有怀疑存在 `BREAKING CHANGE` 时再读取更完整提交体

## 提交分类

按 Conventional Commits 分类：

1. `feat`
2. `fix`
3. `docs`
4. `refactor`
5. `perf`
6. `test`
7. `chore`
8. `deps`
9. `BREAKING CHANGE` / `!`
10. 安全修复

不符合 Conventional Commits 的提交归入“其他变更”。

### 提交到 changelog 分组的映射

1. `feat` → Added / 新功能
2. `fix` → Fixed / Bug 修复
3. `perf`、`refactor`、`deps` → Changed / 变更
4. `docs` → Documentation / 文档（若项目已有此分组）
5. `BREAKING CHANGE` → 顶部高优先级提示
6. 含 CVE 或明确安全问题 → Security / 安全修复

如果项目现有 changelog 的分组顺序不同，必须跟随既有顺序。

## 版本号策略

1. 优先沿用项目已存在的版本格式：SemVer / 带前缀 SemVer / 双段版本 / CalVer
2. Breaking Changes：主版本 +1
3. 新功能：次版本 +1
4. Bug 修复、文档、其他：修订版本 +1
5. 无 tag 且无既有约定时建议从 `v0.1.0` 起步

## 输出格式规则

1. 已有 `CHANGELOG.md` 时，沿用它的标题级别和分组风格
2. 若文件带 `[Unreleased]` 段，优先更新该段或在其后插入新版本块
3. 若项目已经使用 reference-style links，则继续追加，不要改成内联链接
4. 若仓库地址可验证，优先补 Issue / PR / compare link
5. 安全修复尽量保留 CVE 编号

## 输出规则

1. 已有 `CHANGELOG.md`：在顶部追加新版本块
2. 无文件：创建新文件
3. 空分类整段省略，不留占位
4. 如果可验证，尽量关联 Issue/PR 编号与 CVE 编号
5. Breaking Changes 放在最前面
6. 条目要短句化，强调用户可见变化，而不是实现细节流水账
