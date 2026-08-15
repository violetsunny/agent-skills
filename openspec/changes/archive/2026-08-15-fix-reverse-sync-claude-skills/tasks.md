## 1. 模块 2 注明同步范围

- [x] 1.1 在 `modules/module2-openspec.md` 的 `.claude/skills/ → .agents/skills/` 同步段落中注明：该同步是 OpenSpec 生成的 commands 和 skills 的同步，模块 3 维护的 skills 的最新性由模块 3 保证，`.claude/skills/` 的运行时备份由模块 4 保证

## 2. 模块 4 新增备份同步步骤

- [x] 2.1 在 `modules/module4-knowledge-base.md` 的步骤 4.3（变更报告）之后新增「步骤 4.4：备份同步到 .claude/skills/」段落
- [x] 2.2 新增备份同步命令：`rsync -r ~/.agents/skills/ ~/.claude/skills/`（不加 `--delete`），注明目的是运行时备份
- [x] 2.3 新增备份同步汇总统计：在模块 4 汇总中报告备份同步的 skill 数量

## 3. 汇总模板增强

- [x] 3.1 在 `modules/summary.md` 的「知识库同步汇总（模块 4）」段落中新增「备份同步到 .claude/skills/」字段

## 4. 三处同步

- [x] 4.1 从 `~/.agents/skills/git-self-update/` 同步到 `~/.claude/skills/git-self-update/`（`rsync -r --delete --exclude='_mideameta.json'`）
- [x] 4.2 从 `~/.agents/skills/git-self-update/` 同步到 `agent-skills/skills/git-self-update/`（`rsync -r`，不加 `--delete`）
- [x] 4.3 验证三处目录的 `modules/` 子目录文件完全一致

## 5. 验证

- [x] 5.1 确认 `modules/module2-openspec.md` 包含同步范围注明
- [x] 5.2 确认 `modules/module4-knowledge-base.md` 包含步骤 4.4 备份同步
- [x] 5.3 确认 `modules/summary.md` 包含备份同步字段
- [x] 5.4 确认备份同步使用 `rsync -r` 不加 `--delete`
- [x] 5.5 确认改动不涉及模块 1/3/3.5 的行为
