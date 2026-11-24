# key-skills-git 外部克隆目录索引

`key-skills-git/` 是仓库内 **gitignored**（`.gitignore:53`）的外部 skill 仓库克隆区，不入库、只读参考。**20 个克隆一律纯克隆，禁任何修改、添加文件、本地提交**；处置（增删、重新 clone、清理）归用户人工，agent 不得擅自操作（AGENTS.md 约定）。

当前共 **20 个 git 克隆**，已于 2026-11-14 全部恢复为**纯克隆**（behind=0 / ahead=0，fetch 远端比对确认）。本文档为人工整理索引，非脚本生成；重新 clone 或增删目录后需手动更新。

## 总览

| 目录 | 来源 (origin) | 内容定位 | SKILL.md | 最后提交 | 本地改动* |
|------|---------------|----------|----------|----------|-----------|
| ECC | github.com/affaan-m/ECC | Agent harness 操作系统（大规模 agent 技能集） | 1068 | 2026-11-06 | 干净 |
| OpenSpec | github.com/Fission-AI/OpenSpec | spec-driven 开发 CLI 工具及配套 skills | 31 | 2026-11-13 | 仅 .idea/ |
| addyo-agent-skills | github.com/addyosmani/agent-skills | Addy Osmani 生产级工程 skills | 25 | 2026-11-13 | 仅 .idea/ |
| andrej-karpathy-skills | github.com/multica-ai/andrej-karpathy-skills | Karpathy 观察提炼的 CLAUDE.md 行为准则 | 1 | 2026-09-22 | .DS_Store+.idea/ |
| anthropics-skills | github.com/anthropics/skills | Anthropic 官方 skills | 20 | 2026-11-06 | 干净 |
| archify | github.com/tt-a1i/archify | 交互式架构图/可视化生成（独立 HTML） | 5 | 2026-11-13 | 仅 .idea/ |
| baoyu-skills | github.com/JimLiu/baoyu-skills | 宝玉分享的日常效率 skills（中英双语） | 22 | 2026-11-06 | 干净 |
| caveman | github.com/JuliusBrussee/caveman | 输出 token 压缩（说少读少、代码保真） | 28 | 2026-11-13 | 仅 .idea/ |
| claude-code-java | github.com/decebals/claude-code-java | Java 项目 agent skills（Spring/JPA/并发等） | 18 | 2026-11-02 | 仅 .DS_Store |
| diagram-design | github.com/cathrynlavery/diagram-design | 编辑级风格图表设计 skill | 1 | 2026-11-13 | .DS_Store+.idea/ |
| frontend-slides | github.com/zarazhangrui/frontend-slides | HTML 演示文稿创建 skill（PPT 转换） | 2 | 2026-09-22 | 仅 .idea/ |
| hyperframes | github.com/heygen-com/hyperframes | HyperFrames 幻灯片/演示框架（bun 项目，含 skills/ 与 themes/） | 28 | 2026-11-14 | 干净 |
| i-have-adhd | github.com/ayghri/i-have-adhd | ADHD 友好输出格式 skill | 2 | 2026-10-27 | 仅 .idea/ |
| matt-skills | github.com/mattpocock/skills | Matt Pocock TypeScript 工程方法论 skills | 39 | 2026-11-13 | .DS_Store+.idea/ |
| ponytail | github.com/DietrichGebert/ponytail | 极简主义"懒senior"工程风格 skills | 12 | 2026-11-02 | 仅 .idea/ |
| ppt-master | github.com/hugohe3/ppt-master | AI 从任意文档生成原生 PPTX | 1 | 2026-11-12 | 干净 |
| scientific-agent-skills | github.com/K-Dense-AI/scientific-agent-skills | 177 个科研领域 skills（化学/生物/数据分析） | 177 | 2026-11-13 | 仅 .idea/ |
| superpowers | github.com/obra/superpowers | 完整软件开发方法论 skill 集 | 15 | 2026-11-05 | 仅 .idea/ |
| ui-ux-pro-max-skill | github.com/nextlevelbuilder/ui-ux-pro-max-skill | UI/UX 设计增强 skill | 13 | 2026-11-10 | 干净 |
| vercel-agent-skills | github.com/vercel-labs/agent-skills | Vercel 官方 agent skills（部署/优化） | 9 | 2026-11-02 | 仅 .idea/ |

\* 本地改动截至 2026-11-14 检查：现存 dirty **全部为 untracked 噪音**（macOS `.DS_Store` 与 JetBrains IDE 重新生成的 `.idea/`），无 tracked 文件改动，不影响 pull 的 fast-forward。

## 纯克隆恢复记录（2026-11-14）

**背景**：2026-09-22 起 13 个克隆含用户本地提交 `update skills`（作者 kangll13，多为 `.idea/` 提交），导致后续每次 pull 无法 fast-forward、持续积累 `Merge remote-tracking branch 'origin/main'` merge 提交。

**处置**（用户授权执行）：对 13 个仓库执行 `git reset --hard origin/main`，丢弃本地提交与 merge 链：

OpenSpec、diagram-design、andrej-karpathy-skills、i-have-adhd、claude-code-java、frontend-slides、archify、caveman、matt-skills、scientific-agent-skills、superpowers、ponytail、vercel-agent-skills

**备份**：被丢弃本地提交中的实质文件（7 个）已备份至 `key-skills-git/pre-reset-backup-20261114.tar.gz`（170K）：

- i-have-adhd/AGENTS.md（上游亦有此文件，reset 后为上游版本）
- claude-code-java/MCP_CONFIG.md、claude-code-java/mcp-config.json
- frontend-slides/AGENTS.md
- matt-skills/skills-reference.md
- scientific-agent-skills/docs/security-report.json、.md

**验证**：20 个克隆全部 behind=0 / ahead=0；此后 pull 恢复 fast-forward，不再产生 merge 提交。备份 tar 去留由用户人工决定。

## 与同步工具链的关系

1. **m1 批量 git pull**：`m1_git_pull.sh scan` 执行 `find $SELF_ROOT -maxdepth 5`，本目录下克隆（路径深度 4 层）**在扫描范围内**，`pull` 阶段会一并更新；dirty 克隆会被 classify 跳过（当前 dirty 仅为 .DS_Store/.idea 噪音）。
2. **m3 npx 更新**：`config.sh` 的 `NPX_MAP` 登记 16 个 npx 管理项目，其中 14 个在本目录有对应克隆（humanizer / humanizer-zh 为 `none` 无本地克隆）。npx 更新走 lock 文件，不直接读取本目录。
3. **m3 兜底路径不在本目录**：`m3_fallback.sh` 的克隆基准是 `EXTERNAL_CLONES=$SELF_ROOT/skills`（即 `/Users/kangll13/aiot/java-code/self/skills/`），**不是本目录**。两处为独立克隆（HEAD 各异），本目录仅作仓库内参考副本，勿混淆。
4. **skills/ 副本真源**：本目录克隆是"源头参考"，实际安装到 `~/.agents/skills/` 的 skill 副本以 `skills/`（693 个，只读）与 `self-skills/` 为准。

## 磁盘占用参考（2026-11-14）

合计约 **5.1G**。最大三项：archify 2.4G、hyperframes 866M、scientific-agent-skills 754M。清理需用户人工决策。
