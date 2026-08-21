# Step 5: CHANGELOG 生成

从 Git 历史自动生成 `CHANGELOG.md`，遵循 Keep a Changelog 与 Semantic Versioning。

## 历史获取

1. 优先读取最近 tag
2. 有 tag 时，统计上个 tag 到 `HEAD` 的提交
3. 无 tag 时，读取有限条数的全部历史

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

## 版本号策略

1. Breaking Changes：主版本 +1
2. 新功能：次版本 +1
3. Bug 修复、文档、其他：修订版本 +1
4. 无 tag 时建议从 `v0.1.0` 起步

## 输出规则

1. 已有 `CHANGELOG.md`：在顶部追加新版本块
2. 无文件：创建新文件
3. 空分类整段省略，不留占位
4. 如果可验证，尽量关联 Issue/PR 编号与 CVE 编号
