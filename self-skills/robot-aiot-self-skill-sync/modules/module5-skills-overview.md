# 模块 5：更新 `docs/skills-overview.md`

> 共享规则见 `modules/shared.md`

**目的**：在所有 skills 同步完成后，更新当前项目中的 `/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/docs/skills-overview.md`，形成统一的技能总览文档，分别展示 `~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/` 三个目录下的技能名称和说明。

### 输出要求

- 文档固定路径：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/docs/skills-overview.md`
- 文档必须分为三部分：
  - **第一部分**：`~/.agents/skills/` 下的技能和说明
  - **第二部分**：`agent-skills/skills/` 下的技能和说明（外部 skill 副本）
  - **第三部分**：`agent-skills/self-skills/` 下的技能和说明（用户自写 skill 真源）
- 每部分至少包含：
  - 扫描目录说明
  - skill 总数
  - 技能名称与简要说明表格
- 技能名称优先读取 `SKILL.md` frontmatter 中的 `name:`；若缺失，再退回 skill 根目录名
- 表格列为 `技能 | 路径 | 说明`：`路径` 为 `SKILL.md` 所在目录相对各部分扫描根目录的相对路径（扁平 skill 即目录名，嵌套子目录如 `robot-aiot-draw-flowchart/archify` 保留相对层级）
- 技能说明**不直接使用原始 `description:`**，而是基于其提炼的**中文摘要**，规则见下「说明列规则」

### 说明列规则（中文摘要）

说明列是基于原始 `description` 提炼的中文摘要，不是原文照搬：

- **长度**：≤500 字（上限，非目标）；力求简洁，多数 skill 控制在 50-150 字
- **语言**：统一中文；英文 `description` 翻译成中文，中文 `description` 去冗余压缩
- **内容**：提炼核心——这个 skill 做什么 + 何时触发/适用场景；不逐字翻译，要概括
- **专有名词保留英文**：API 名、命令名、文件名、协议名、关键触发短语保留英文原样（如 OpenSpec、draw.io、MQTT、`/opsx`、`SKILL.md`、NONMEM），其余用中文
- **单行无换行**：摘要放入 Markdown 表格单元格，不得含换行符，内部用逗号/分号断句
- **转义竖线**：摘要中的 `|` 必须转义为 `\|`，避免断表
- **去冗余**：删除客套、重复罗列、无信息量修饰；触发词只保留代表性的几个，不全量罗列
- **兜底**：原始 `description` 为空时，说明写 `（无描述）`

### 扫描范围

- 第一部分扫描：`/Users/kangll13/.agents/skills/`
- 第二部分扫描：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`
- 第三部分扫描：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`
- 三部分都应递归查找 `SKILL.md`，兼容存在分类目录的情况
- 只读取各自目录内部的 `SKILL.md`，不得跨目录混扫

### 同步规则

- 模块 5 在模块 2、模块 3、模块 4 全部完成后执行
- 模块 5 只更新 `docs/skills-overview.md` 文档，不修改任何 skill 源目录
- 生成文档时允许整体重写 `docs/skills-overview.md`，但**不得**删除 `~/.agents/`、`agent-skills/skills/` 或 `agent-skills/self-skills/` 中任何文件
- 如果某个 `SKILL.md` frontmatter 缺少 `name` 或 `description`，在文档中按兜底规则展示，并在汇总中计入“缺失字段数量”

### 增量快照

模块 5 支持 mtime 增量更新，避免每次全量翻译。快照文件固定为 `docs/.skills-overview-mtimes.json`，与 `docs/skills-overview.md` 同目录。

快照结构：

```json
{
  "<abs_path_to_SKILL.md>": {
    "mtime": 1726480000,
    "name": "skill-name",
    "zh": "中文摘要..."
  }
}
```

增量规则：

- **首次运行**（快照不存在）：全量执行，完成后写入快照
- **后续运行**：脚本提取阶段同时读取快照，逐条比对 `SKILL.md` 的 mtime：
  - mtime 相同且快照中有 `zh` → 复用缓存摘要，不送翻译
  - mtime 变化或快照中无该条目 → 标记为 dirty，送 sub agent 翻译
  - 快照中有但磁盘上已删除的条目 → 从快照和文档中移除
- **回填后更新快照**：将本次所有条目（含复用的和新翻译的）写回快照
- 快照文件不参与 git 提交（应加入 `.gitignore`），仅作为本地增量缓存

### 建议生成步骤

说明列为中文摘要，需模型翻译压缩，不能用纯脚本完成。采用「脚本提取 + 增量比对 + sub agent 翻译 + 脚本回填」四段式，确定性工作交脚本、语言工作交 sub agent：

1. **脚本提取 + 增量比对**：递归扫描三目录所有 `SKILL.md`，解析 frontmatter 取 `name`/`description`，折叠多行为单行，输出记录列表（每条含 `part`/`name`/`rel`/`desc`/`abs_path`/`mtime`）；同时加载 `docs/.skills-overview-mtimes.json` 快照，逐条比对 mtime，将未变化的条目标记 `cached: true` 并携带缓存 `zh`，变化的标记 `cached: false`
2. **去重**：仅对 `cached: false` 的条目按 `(name, desc)` 去重得 dirty unique 集，分配全局 id；`cached: true` 的条目直接保留缓存 `zh` 不参与翻译
3. **分批**：dirty unique 集按每批 ≤45 个切分，每批写 `/tmp/zh/in_NN.json`（`[{id,name,desc}]`）；若 dirty 集为空则跳过步骤 4-5，直接用缓存生成文档
4. **sub agent 翻译压缩**：并行派 sub agent，每个读 `in_NN.json`、生成中文摘要、写 `/tmp/zh/out_NN.json`（`[{id,zh}]`），只返回简短确认（详见下「Sub Agent 处理方式」）
5. **脚本合并回填**：合并所有 `out_NN.json` 得 `id→zh`，与缓存 `zh` 合并，按映射回填到每条记录，按部分分组、按 `name` 排序，生成三部分 Markdown 写入 `docs/skills-overview.md`；同时将全量结果写回 `docs/.skills-overview-mtimes.json` 快照
6. **验证报告**：校验条数一致、id 无缺漏、`zh` 非空/无换行/≤500 字、表格无断行；报告总数、各部分数、缓存命中数、新翻译数、删除数、缺失字段数（`name`/`description` 走兜底的数量）、说明长度分布（min/max/mean/median）、超标数

### Sub Agent 处理方式

翻译压缩是语言工作，交给并行 sub agent；提取/去重/分批/回填/验证是确定性工作，交给脚本。两者分离，避免主线程上下文被数百条原文污染。

- **批次大小**：每个 sub agent 处理 ≤45 个 unique 描述（输入约 1.5 万字、输出约 4 千字，单 agent 可稳定完成）
- **并行度**：每轮并行 5 个 sub agent，分多轮跑完全部批次（如 658 unique → 15 批 → 3 轮）
- **输入输出走文件**：sub agent 读 `/tmp/zh/in_NN.json`、写 `/tmp/zh/out_NN.json`，**不在返回消息里回传 JSON 内容**，只返回「写入 out_NN.json，N 条」，省主线程上下文
- **sub agent prompt 要点**（须逐条写明）：
  1. `zh` 为单行中文摘要，≤500 字，简洁不冗余
  2. 提炼用途 + 触发场景，不逐字翻译
  3. 英文译中、中文去冗余
  4. 专有名词/API/命令/文件名/关键触发短语保留英文
  5. `zh` 不含换行符
  6. 输出 id 与输入一一对应、数量一致，不得遗漏或新增
  7. 直接写中文（非 `\u` 转义）
- **每轮验证**：每轮 sub agent 完成后，脚本校验该轮 `out_NN.json`（条数、id 匹配、`zh` 非空/无换行/≤500 字），发现超标或异常条目单独修正后再进入下一轮，避免系统性错误重蹈
- **主线程职责**：派 sub agent、跑验证脚本、合并回填、写入文档、最终统计；不亲自逐条翻译

### 建议文档结构

```md
# 技能总览

本文档汇总三个技能目录：`~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/`，根据各目录下实际存在的 `SKILL.md` 递归生成。技能名称优先读取 frontmatter `name`（缺失回退目录名）；说明为基于原始 `description` 提炼的中文摘要（≤500 字，简洁概括用途与触发场景）。

## 第一部分：`~/.agents/skills/`

扫描目录：`/Users/kangll13/.agents/skills/`（运行时技能目录）

共 **N** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `foo` | `foo` | 中文摘要：做什么 + 何时触发，保留专有名词英文，≤500 字。 |

## 第二部分：`agent-skills/skills/`

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`（外部 skill 副本库）

共 **N** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `bar` | `bar` | 中文摘要…… |

## 第三部分：`agent-skills/self-skills/`（用户自写）

扫描目录：`/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`（用户自写 skill 真源）

共 **N** 个 `SKILL.md`。

| 技能 | 路径 | 说明 |
|------|------|------|
| `baz` | `parent-dir/baz` | 中文摘要……（嵌套子目录保留相对路径） |
```

### 注意事项

- 若技能较多，应保持文档为单文件，但避免引入与技能分组强耦合的手工分类，优先采用稳定、可重复生成的格式
- 原始 `description` 的多行在脚本提取阶段折叠为单行，再交 sub agent 生成中文摘要；文档说明列本身即单行摘要，不含换行
- 文档内容以实际扫描结果为准，不依赖人工维护的静态技能列表
- 说明列是中文摘要而非原文照搬，长度 median 宜控制在 ~120 字；超 500 字的条目须单独重压
- 去重按 `(name, desc)`：同名同描述只翻译一次并复用到所有出现位置，同名不同描述分别翻译
- sub agent 只走文件交换数据、不回传 JSON 正文，主线程上下文只保留统计与验证结果
