# 模块 5：更新 `docs/skills-overview.md`

> 共享规则见 `modules/shared.md`
> 四段式已脚本化：提取/增量比对/分批/回填/验证在 `scripts/m5_extract.sh` 与 `scripts/m5_render.sh`，只有「翻译压缩」是语言工作交并行 sub agent。

**目的**：所有 skills 同步完成后，更新 `agent-skills/docs/skills-overview.md`，分三部分展示 `~/.agents/skills/`（运行时）、`agent-skills/skills/`（外部副本库）、`agent-skills/self-skills/`（自写真源）的技能名称与中文摘要说明。

## 执行序列

```bash
S=~/.agents/skills/robot-aiot-self-skill-sync/scripts

$S/m5_extract.sh     # 1) 扫描+frontmatter解析+mtime增量比对+分批 → /tmp/zh/in_NN.json
# 2) 并行派 sub agent 翻译（每轮 5 个，读 in_NN.json 写 out_NN.json，不回传 JSON 正文）
$S/m5_render.sh      # 3) 合并回填+生成文档+重建快照+验证报告
```

- dirty 集为空时 extract 会提示跳过翻译，直接跑 render 用缓存生成
- render 遇缺翻译（`[M5-MISS-ZH]`）会**拒绝生成残缺文档**并 exit 1，补齐 out_NN.json 后重跑

## 增量快照

`docs/.skills-overview-mtimes.json`（与文档同目录，不参与 git 提交，确认在 `.gitignore`）：

```json
{ "<SKILL.md绝对路径>": { "mtime": 1726480000, "name": "...", "zh": "中文摘要" } }
```

- mtime 未变且快照有 `zh` → 复用缓存不送翻译；mtime 变化或无条目 → dirty 送 sub agent
- 快照中有但磁盘已删的条目 → render 重建快照时自然移除
- 去重按 `(name, desc)`：同名同描述只翻译一次复用到所有出现位置

## 说明列规则（sub agent prompt 须逐条写明）

1. `zh` 为单行中文摘要 ≤500 字（上限非目标，多数 50-150 字），简洁不冗余
2. 提炼「做什么 + 何时触发/适用场景」，不逐字翻译
3. 英文 description 译中，中文去冗余压缩
4. 专有名词保留英文：API 名、命令名、文件名、协议名、关键触发短语（如 OpenSpec、draw.io、MQTT、`/opsx`、`SKILL.md`）
5. `zh` 不含换行符（表格单元格内用逗号/分号断句；`|` 由 render 自动转义）
6. 输出 id 与输入一一对应、数量一致，不得遗漏或新增
7. 直接写中文（非 `\u` 转义）
8. 原始 description 为空 → 说明写 `（无描述）`（extract 已兜底）

## Sub agent 派发方式

- 批次 ≤45 个 unique 描述/agent（输入约 1.5 万字、输出约 4 千字）；并行度每轮 5 个，分多轮跑完
- **输入输出走文件**：读 `/tmp/zh/in_NN.json`、写 `/tmp/zh/out_NN.json`（`[{id,zh}]`），返回消息只写「写入 out_NN.json，N 条」，不回传 JSON 正文（省主线程上下文）
- 每轮完成后跑 render 前可先用 `jq -e` 校验该轮 out 文件（render 也会整体校验：条数、id 匹配、zh 非空/无换行/≤500 字），异常条目单独修正再进下一轮

## 文档与扫描规则（脚本内置）

- 三部分各自递归查找 `SKILL.md`（兼容分类目录），只读各自目录内部，不跨目录混扫
- 技能名优先 frontmatter `name:`，缺失回退目录名；表格列 `技能 | 路径 | 说明`，路径为相对各部分扫描根的相对路径（嵌套保留层级）
- 文档允许整体重写，但不得删除三个源目录中任何文件
- 内容以实际扫描为准，不依赖手工维护的静态分组；frontmatter 多行 description 折叠为单行

## 验证报告（render 自动输出）

`[M5-STAT]`：总数、各部分数、缓存命中数、新翻译数、超 500 字数、长度分布（min/max/mean/median）、快照已删条目数。缺失字段走兜底的条目数在 extract 的 `[M5-STAT]` 中报告。
