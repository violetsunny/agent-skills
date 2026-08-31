# 守则

1. 先读后写：更新前先读取现有文件
2. 保留项目专属规则：已有 `AGENTS.md` 中的项目约束只追加不覆盖
3. 内容可溯源：所有声明必须能追溯到项目中的实际文件、配置或代码模式
4. 无法确认时写“TODO: 待补充”，不编造
5. 已有 README 和 CHANGELOG 优先精确更新，不整体覆盖
6. 若 init 命令已引导生成 `AGENTS.md`，后续只在此基础上补充
7. 仅修改文档范围：`AGENTS.md`、`README.md`、`CHANGELOG.md`、`docs/project-map.md`、`docs/architecture.md`
8. README、project-map、architecture 以中文为主，技术名词保留英文原文
9. 文档职责不能串位：不要把架构说明塞进 README，不要把使用指南塞进 CHANGELOG
10. 优先沿用项目既有格式、标题层级、版本风格和术语口径
11. 中文润色只能优化表达，不能改变已确认事实
12. 生成后至少做一次术语、一致性、链接和命令可复制性检查
