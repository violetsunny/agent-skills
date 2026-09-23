# env-config — 目录结构唯一真源

本技能全部输出 / 生成 / 验证 / 读取 / 临时目录只在本文件登记。SKILL.md 与 references/ 仅引用登记项，不另行定义目录结构。

规则：

1. 新增目录、修改路径、调整输出范围 → 只改本文件；改后 grep 技能内旧路径的内联引用一并修正。
2. 正文内联路径为使用示例；与本文件冲突时以本文件为准，并修正内联。
3. 只写登记为「输出」的 5 个文件；不碰源码、配置、测试文件，不生成登记外的任何文件。

## 目录登记表

作用根目录 = 目标项目根（Step 0 定位的当前运行项目根目录）。

| 类别 | 路径 | 用途 |
|---|---|---|
| 输出 | `<项目根>/AGENTS.md` | AI 协作规则入口 |
| 输出 | `<项目根>/README.md` | 项目入口文档（tutorial + how-to 入口） |
| 输出 | `<项目根>/CHANGELOG.md` | 变更记录（版本分类/提交映射规则见 references/changelog.md） |
| 输出 | `<项目根>/docs/project-map.md` | 项目地图（Diataxis reference 层；目录树 ≤3 层） |
| 输出 | `<项目根>/docs/architecture.md` | 架构说明（Diataxis explanation 层；FAQ 并入本文件章节，不独立成文件） |
| 读取 | 目标项目源码、git log / git tag、既有文档、init 命令文件 | 扫描与推断输入 |
| 读取 | 技能内 `references/*.md` | 只读规则资源 |
| 临时 | 无 | 本技能不落中间产物；确需临时文件只用 `/tmp` 且用后即删 |

## 输出边界

1. 不单独生成 `docs/api-reference.md` 等登记外文档
2. `docs/` 下只写 `project-map.md` 与 `architecture.md` 两个文件
3. 所有命令、路径、示例必须可溯源到目标项目真实内容
