# Flowchart Patterns Reference

## 1. 线性流程图 (Linear Flow)

**适用场景:** 步骤顺序执行，无分支

**结构:**
```
[开始] → [步骤1] → [步骤2] → [步骤3] → [结束]
```

**XML 模式:**
```xml
<!-- 开始节点 -->
<mxCell id="start" value="开始" style="ellipse;fillColor=#0078D4;fontColor=#FFFFFF;strokeColor=#005A9E;strokeWidth=2;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="40" as="geometry" />
</mxCell>

<!-- 处理步骤 -->
<mxCell id="step1" value="步骤1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#0078D4;strokeWidth=2;arcSize=20;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="220" y="90" width="120" height="60" as="geometry" />
</mxCell>

<!-- 连接线 -->
<mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#005A9E;strokeWidth=2;" edge="1" source="start" target="step1" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**布局要点:**
- 节点间距：水平 120-150px，垂直 80-100px
- 节点尺寸：矩形 120x60，椭圆 80x40
- 箭头：正交连线，strokeWidth=2

---

## 2. 分支流程图 (Branching Flow)

**适用场景:** 有条件判断，多路径选择

**结构:**
```
        ┌─ 是 ─→ [路径A]
[判断] ─┤
        └─ 否 ─→ [路径B]
```

**XML 模式:**
```xml
<!-- 决策节点 -->
<mxCell id="decision" value="条件判断?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;strokeWidth=2;fontSize=11;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="120" height="80" as="geometry" />
</mxCell>

<!-- 是路径 -->
<mxCell id="path_yes" value="路径A" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#82B366;strokeWidth=2;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="400" y="50" width="120" height="60" as="geometry" />
</mxCell>

<!-- 否路径 -->
<mxCell id="path_no" value="路径B" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFEBEE;strokeColor=#B85450;strokeWidth=2;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="400" y="150" width="120" height="60" as="geometry" />
</mxCell>

<!-- 带标签的箭头 -->
<mxCell id="arrow_yes" value="是" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#82B366;strokeWidth=2;fontColor=#82B366;fontSize=11;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" source="decision" target="path_yes" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<mxCell id="arrow_no" value="否" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#B85450;strokeWidth=2;fontColor=#B85450;fontSize=11;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" source="decision" target="path_no" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**布局要点:**
- 决策节点用菱形，尺寸 120x80
- 分支路径上下或左右对称分布
- 箭头必须带标签（是/否、成功/失败）
- 成功路径用绿色，失败路径用红色

---

## 3. 循环流程图 (Loop Flow)

**适用场景:** 有重复执行、重试机制

**结构:**
```
[步骤1] → [判断] ─┬─ 完成 → [结束]
              ↑   │
              └─ 未完成 ─┘
```

**XML 模式:**
```xml
<!-- 循环体 -->
<mxCell id="step1" value="执行操作" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#0078D4;strokeWidth=2;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>

<mxCell id="check" value="完成?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;strokeWidth=2;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="280" y="100" width="100" height="60" as="geometry" />
</mxCell>

<!-- 循环回退箭头（虚线） -->
<mxCell id="loop_back" value="未完成" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#B85450;strokeWidth=2;dashed=1;fontColor=#B85450;fontSize=11;labelBackgroundColor=#FFFFFF;" edge="1" source="check" target="step1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="330" y="200" />
      <mxPoint x="160" y="200" />
    </Array>
  </mxGeometry>
</mxCell>
```

**布局要点:**
- 循环回退用虚线箭头
- 回退箭头用红色或橙色
- 循环次数可标注在箭头上（如 "重试≤3次"）

---

## 4. 并行流程图 (Parallel Flow)

**适用场景:** 多个任务同时执行

**结构:**
```
              ┌─ [任务A] ─┐
[开始] ─ 分叉 ─┼─ [任务B] ─┼─ 汇合 → [结束]
              └─ [任务C] ─┘
```

**XML 模式:**
```xml
<!-- 分叉点 -->
<mxCell id="fork" value="" style="shape=mxgraph.flowchart.merge_or_storage;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="150" y="120" width="20" height="60" as="geometry" />
</mxCell>

<!-- 并行任务 -->
<mxCell id="task_a" value="任务A" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#0078D4;strokeWidth=2;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="250" y="50" width="120" height="50" as="geometry" />
</mxCell>

<mxCell id="task_b" value="任务B" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#0078D4;strokeWidth=2;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="250" y="120" width="120" height="50" as="geometry" />
</mxCell>

<mxCell id="task_c" value="任务C" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#0078D4;strokeWidth=2;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="250" y="190" width="120" height="50" as="geometry" />
</mxCell>

<!-- 汇合点 -->
<mxCell id="join" value="" style="shape=mxgraph.flowchart.merge_or_storage;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="450" y="120" width="20" height="60" as="geometry" />
</mxCell>
```

**布局要点:**
- 分叉/汇合点用粗竖线表示
- 并行任务垂直排列，间距 20px
- 所有并行任务完成后才能继续

> ⚠️ `mxgraph.flowchart.merge_or_storage` 等 `mxgraph.flowchart.*` 命名空间形状目前在 robot-aiot-xml-html-bridge 的映射表中无对应 CSS，转换时会触发未映射属性警告。已知缺口，待后续 change 补充映射。

---

## 5. 子流程图 (Subprocess)

**适用场景:** 复杂流程分解为子模块

**结构:**
```
[主流程] → [子流程] → [主流程继续]
              ↓
         [子流程详情]
```

**XML 模式:**
```xml
<!-- 子流程引用（带双边框） -->
<mxCell id="subprocess" value="子流程名称" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F3E5F5;strokeColor=#9673A6;strokeWidth=3;arcSize=20;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="140" height="60" as="geometry" />
</mxCell>

<!-- 子流程展开区域 -->
<mxCell id="subprocess_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F3E5F5;strokeColor=#9673A6;strokeWidth=1;dashed=1;arcSize=8;opacity=30;" vertex="1" parent="1">
  <mxGeometry x="150" y="250" width="500" height="300" as="geometry" />
</mxCell>

<mxCell id="subprocess_title" value="子流程详情" style="text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;fillColor=#9673A6;fontColor=#FFFFFF;strokeColor=#6A4C7D;rounded=1;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="300" y="260" width="200" height="30" as="geometry" />
</mxCell>
```

**布局要点:**
- 子流程引用用双边框（strokeWidth=3）
- 子流程详情放在下方或右侧，用虚线框包围
- 用紫色系表示子流程

---

## 6. 泳道流程图 (Swimlane Flow)

**适用场景:** 多角色/多部门协作流程

**结构:**
```
┌─────────────────────────────────────┐
│ 角色A │ [步骤1] → [步骤2]          │
├─────────────────────────────────────┤
│ 角色B │          [步骤3] → [步骤4]  │
├─────────────────────────────────────┤
│ 角色C │                   [步骤5]   │
└─────────────────────────────────────┘
```

**XML 模式:**
```xml
<!-- 泳道背景 -->
<mxCell id="lane_a_bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#0078D4;strokeWidth=1;opacity=30;" vertex="1" parent="1">
  <mxGeometry x="150" y="80" width="800" height="120" as="geometry" />
</mxCell>

<mxCell id="lane_a_label" value="角色A" style="text;html=1;fontSize=13;fontStyle=1;align=center;verticalAlign=middle;fillColor=#0078D4;fontColor=#FFFFFF;strokeColor=#005A9E;rounded=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="30" y="110" width="100" height="40" as="geometry" />
</mxCell>

<!-- 泳道分隔线 -->
<mxCell id="lane_divider" value="" style="endArrow=none;dashed=1;strokeColor=#0078D4;strokeWidth=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="30" y="200" as="sourcePoint" />
    <mxPoint x="950" y="200" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

**布局要点:**
- 泳道垂直排列，每个泳道高度 120-150px
- 泳道标签在左侧，宽度 100px
- 流程节点在各泳道内水平排列
- 跨泳道的箭头表示协作

---

## 通用规范

### 节点尺寸标准
| 类型 | 宽度 | 高度 | 说明 |
| --- | --- | --- | --- |
| 开始/结束 | 80 | 40 | 椭圆形 |
| 处理步骤 | 120 | 60 | 圆角矩形 |
| 决策判断 | 120 | 80 | 菱形 |
| 子流程 | 140 | 60 | 双边框圆角矩形 |

### 间距标准
- 水平间距：120-150px
- 垂直间距：80-100px
- 箭头长度：至少 40px

### 箭头规范
- 主流程：实线，strokeWidth=2，蓝色
- 成功路径：实线，strokeWidth=2，绿色
- 失败/回退：虚线，strokeWidth=2，红色
- 跨域调用：虚线，strokeWidth=2，紫色

### 文本规范
- 节点文本：fontSize=11-12
- 箭头标签：fontSize=10-11
- 标题：fontSize=14-16
- 字体颜色：与边框色一致或深一级
