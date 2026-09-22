# Diagram Patterns（UML 覆盖与高频架构模式）

模式速查：UML 14 图型映射 + 常见系统架构模式骨架。用于快速起稿；具体布局语法仍以对应 type reference 为准。

## UML 覆盖映射

UML 14 种图型到本 SKILL 支持类型的映射：

| UML 图型 | 支持为 | 备注 |
|-------------|-------------|-------|
| Class | 类图（`type-uml-class.md`） | 完整 UML 记法 |
| Component | 架构图 | 按组件类型分色填充 |
| Deployment | 架构图 / `type-deployment.md` | 添加节点/实例标签 |
| Package | 架构图 | 用虚线分组容器 |
| Composite Structure | 架构图 | 组件内嵌套矩形 |
| Object | 类图 | 名称带下划线的实例盒 |
| Use Case | 用例图 | 完整 actor/椭圆/关系（见 SKILL.md 工程专项类型） |
| Activity | 流程图 / 过程流 | 添加 fork/join 条 |
| State Machine | 状态机图（`type-state.md`） | 完整 UML 记法 |
| Sequence | 时序图（`type-sequence.md`） | 添加 alt/opt/loop 框 |
| Communication | — | 用时序图近似（交换轴线） |
| Timing | 时间线（`type-timeline.md`） | 适配时间轴 |
| Interaction Overview | 流程图 | 组合活动 + 时序片段 |
| ER Diagram | ER 图（`type-er.md`） | Chen/Crow's foot 记法 |

## 高频架构模式骨架

这些模式出现频率高，起稿时直接内化其拓扑：

- **RAG Pipeline**：查询 → 嵌入 → 向量检索 → 召回 → 增强 → LLM → 响应
- **Agentic RAG**：在查询与 LLM 之间加入带工具调用的 Agent 循环
- **Agentic Search**：查询 → 规划器 → [搜索工具 / 计算器 / 代码] → 综合器 → 响应
- **Mem0 / Memory Layer**：输入 → 记忆管理器 → [写：VectorDB + GraphDB] / [读：检索+排序] → 上下文
- **Agent 记忆类型**：感觉记忆（原始输入）→ 工作记忆（上下文窗口）→ 情景记忆（过往交互）→ 语义记忆（事实）→ 程序记忆（技能）
- **Multi-Agent**：编排器 → [SubAgent A / SubAgent B / SubAgent C] → 聚合器 → 输出
- **工具调用流**：LLM → 工具选择器 → 工具执行 → 结果解析器 → LLM（循环）

## 机器人/IoT 场景对应

| 业务场景 | 建议模式 |
| --- | --- |
| 扫地机端云协同 | 架构图分层：设备端 → 边缘网关 → 云端服务 → 存储 |
| OTA 升级流程 | 流程图 + 状态机（`type-state.md`）：下载→校验→重启→回滚 |
| 设备影子/物模型同步 | 数据流图：写路径与读路径分色（参考记忆架构图读写分离） |
| 多设备调度 | Multi-Agent 变体：调度器 → [设备 A/B/C] → 汇总 |
| 故障上报链路 | Event Transit 风格（style-11）：Topic → 处理器 → 消费组 → DLQ |
