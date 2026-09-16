# Diagram Patterns（UML 覆盖与高频架构模式）

融合自 fireworks-tech-graph 的模式速查：UML 14 图型映射 + 常见系统架构模式骨架。用于快速起稿；具体布局语法仍以对应 type reference 为准。

## UML Coverage Map

UML 14 种图型到本 SKILL 支持类型的映射：

| UML Diagram | Supported As | Notes |
|-------------|-------------|-------|
| Class | Class Diagram（`type-uml-class.md`） | Full UML notation |
| Component | Architecture Diagram | Use colored fills per component type |
| Deployment | Architecture / `type-deployment.md` | Add node/instance labels |
| Package | Architecture Diagram | Use dashed grouping containers |
| Composite Structure | Architecture Diagram | Nested rects within components |
| Object | Class Diagram | Instance boxes with underlined name |
| Use Case | Use Case Diagram | Full actor/ellipse/relationship（见 SKILL.md 工程专项类型） |
| Activity | Flowchart / Process Flow | Add fork/join bars |
| State Machine | State Machine Diagram（`type-state.md`） | Full UML notation |
| Sequence | Sequence Diagram（`type-sequence.md`） | Add alt/opt/loop frames |
| Communication | — | Approximate with Sequence (swap axes) |
| Timing | Timeline（`type-timeline.md`） | Adapt time axis |
| Interaction Overview | Flowchart | Combine activity + sequence fragments |
| ER Diagram | ER Diagram（`type-er.md`） | Chen/Crow's foot notation |

## 高频架构模式骨架

这些模式出现频率高，起稿时直接内化其拓扑：

- **RAG Pipeline**: Query → Embed → VectorSearch → Retrieve → Augment → LLM → Response
- **Agentic RAG**: adds Agent loop with Tool use between Query and LLM
- **Agentic Search**: Query → Planner → [Search Tool / Calculator / Code] → Synthesizer → Response
- **Mem0 / Memory Layer**: Input → Memory Manager → [Write: VectorDB + GraphDB] / [Read: Retrieve+Rank] → Context
- **Agent Memory Types**: Sensory (raw input) → Working (context window) → Episodic (past interactions) → Semantic (facts) → Procedural (skills)
- **Multi-Agent**: Orchestrator → [SubAgent A / SubAgent B / SubAgent C] → Aggregator → Output
- **Tool Call Flow**: LLM → Tool Selector → Tool Execution → Result Parser → LLM (loop)

## 机器人/IoT 场景对应

| 业务场景 | 建议模式 |
| --- | --- |
| 扫地机端云协同 | Architecture 分层：设备端 → 边缘网关 → 云端服务 → 存储 |
| OTA 升级流程 | Flowchart + 状态机（`type-state.md`）：下载→校验→重启→回滚 |
| 设备影子/物模型同步 | Data flow：写路径与读路径分色（参考记忆架构图读写分离） |
| 多设备调度 | Multi-Agent 变体：调度器 → [设备 A/B/C] → 汇总 |
| 故障上报链路 | Event Transit 风格（style-11）：Topic → 处理器 → 消费组 → DLQ |
