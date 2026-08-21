# Phase 3-3.5: 图表生成与桥接转换

图表链路分两步：先产出 XML 真源，再产出 HTML 桥接稿。

## Phase 3: 调用 robot-aiot-draw-flowchart

### 选型

1. 分层架构图：系统架构展示、多模块分层说明，推荐用作首页主视觉
2. 泳道流程图：多角色协作流程
3. 线性/分支流程图：单链路流程
4. 循环流程图：重试机制、治理闭环

### 执行要求

1. 使用 `skill` 工具加载 `robot-aiot-draw-flowchart`
2. 按需读取其 `references/layered-architecture.md` 或 `references/flowchart-patterns.md`
3. 图表表达的是业务能力和治理闭环，不是底层技术部署拓扑
4. 图表底部补 2-3 个数据锚点，保持与数据池一致
5. 首页架构图确立全局主色系，后续页面在统一配色下允许展示风格多样性

### 产物

输出到 `doc-ppt/`：

```markdown
- 图表真源：`doc-ppt/<图表文件名>.xml`
- 图表状态：Phase 3 已完成，待进入 Phase 3.5 转换
```

## Phase 3.5: 调用 robot-aiot-xml-html-bridge

### 执行要求

1. 使用 `skill` 工具加载 `robot-aiot-xml-html-bridge`
2. 对每个 `.xml` 生成对应 `.html`
3. 校验 HTML 保留 XML 的样式、布局、层级、比例和关键标签关系
4. 只有 HTML 校验通过，才能进入 Phase 4

### 阻塞规则

1. 没有完成图表 HTML，不允许进入 Phase 4
2. 图表 HTML 与 XML 视觉不一致，不允许进入 Phase 5
3. XML 改动后，关联图表 HTML 必须整稿重生

### 产物

```markdown
- 图表真源：`doc-ppt/<图表文件名>.xml`
- 图表 HTML：`doc-ppt/<图表文件名>.html`
```
