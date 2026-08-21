# Step 0-2: 项目发现与结构推断

## Step 0: 定位根目录与现状

先定位项目根目录，并检测现有文档状态、Git 标签状态和 init 命令文件。

建议获取：

1. 项目根目录
2. 是否已有 `AGENTS.md`、`README.md`、`CHANGELOG.md`、`docs/`
3. 是否存在项目级 init 命令
4. Git tag 与近期提交
5. 现有文档分别承担什么职责，是否已有明显的 README / changelog / docs 分层

## Step 1: 处理 init 命令

若存在 init 命令且项目根目录没有 `AGENTS.md`：

1. 先读取 init 命令文件
2. 以其结果为 `AGENTS.md` 基础
3. 后续只补充结构、入口和规则，不覆盖 init 生成的项目专属内容

## Step 2: 扫描项目结构

这一步不能省略，先读后写是整个技能成立的前提。

### 2a. 文件扫描

优先使用 `Glob`、`Grep`、`Read` 等工具，而不是依赖一次性 shell 截断扫描。扫描时跳过：

1. `.git`
2. `node_modules`
3. `.venv`
4. `__pycache__`
5. `dist`
6. `build`
7. `.next`
8. `.idea`
9. `vendor`

### 2b. 元数据读取

读取存在的项目元数据文件：

1. `package.json`、`pyproject.toml`、`pom.xml`、`build.gradle`、`Cargo.toml`、`go.mod`
2. `requirements.txt`、`setup.py`、`setup.cfg`
3. `.env.example`、`config.yaml`、`config.example.yml`
4. 现有 `README.md`、`AGENTS.md`、`CHANGELOG.md`
5. `CLAUDE.md`、`CONTRIBUTING.md`
6. 主入口文件，如 `main.py`、`app.py`、`index.ts`、`Main.java`

### 2c. 架构推断输出

至少推断出：

1. 主要语言
2. 框架
3. 项目类型
4. 主入口
5. 关键目录及职责
6. 测试框架
7. 构建工具
8. 包管理器
9. 是否 monorepo

### 2d. 文档分层判断

吸收 `gstack-document-generate` 的 Diataxis 思路，但只落在现有 5 个文件中：

1. `README.md` 主要承担 tutorial / how-to 入口
2. `docs/project-map.md` 主要承担 reference
3. `docs/architecture.md` 主要承担 explanation
4. `CHANGELOG.md` 主要承担时间线式 reference
5. `AGENTS.md` 主要承担 Agent 操作约束

### 2e. 业务目的提炼

从代码和配置中回答：

1. 项目解决什么问题
2. 主要用户是谁
3. 主要能力有哪些
4. 明确不做什么
5. 与同类方案相比的差异点是什么

### 2f. 文档缺口识别

在开始写文档前，先判断缺的是哪一类内容，避免把所有信息都塞进 README：

1. 缺入口说明：优先补 README
2. 缺 Agent 工作约束：优先补 `AGENTS.md`
3. 缺版本演进记录：优先补 `CHANGELOG.md`
4. 缺结构说明：优先补 `docs/project-map.md`
5. 缺架构与设计解释：优先补 `docs/architecture.md`
