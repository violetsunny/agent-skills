# 转换工作流

## Phase 1: 识别 XML 结构

先确认输入是否为本技能支持的 draw.io / mxGraph XML：

1. 存在 `mxfile`
2. 存在 `diagram`
3. 存在 `mxGraphModel`
4. 存在 `root` 与 `mxCell`

若不满足，不要盲目生成 HTML，应直接说明结构不受支持。

## Phase 2: 选择稳定转换路径

优先级如下：

1. 确定性渲染路径：运行 `scripts/xml_to_html.py`，结合 `references/xml-html-mapping.md` 确定性生成坐标驱动 HTML
2. 手工映射降级路径：仅当已确认目标环境无 Python 时，才允许按映射表手工翻译 mxCell 样式到 CSS
3. 人工近似重画：禁止作为可交付桥接稿直接放行

脚本调用示例：

```bash
python3 scripts/xml_to_html.py doc-ppt/<图表名>.xml -o doc-ppt/<图表名>.html
```

选择原则：

1. 只要确定性脚本可用，就不要切到人工路径
2. 若缺少稳定路径，必须显式阻塞，并说明缺失能力

## Phase 3: 生成 HTML 桥接稿

### 步骤 0：加载 UI 参考

必须加载 `ui-ux-pro-max`，并结合本技能内置的 MD3 风格补充规则做非阻塞 UI 检查。

重点检查：

1. 配色层级是否清晰
2. 字体梯度是否清晰
3. 图表与数据卡片可读性是否足够

这些检查不改变 `xml-html-mapping.md` 的确定性映射，只作为 Phase 4 补充检查依据。

### 步骤 1：生成 HTML 结构

推荐结构：

```html
<html>
  <head>
    <style>
      /* 固定画布尺寸、颜色变量、节点/连线/标签样式 */
    </style>
  </head>
  <body>
    <div class="diagram-canvas">
      <!-- 容器 -->
      <!-- 节点 -->
      <!-- 标签 -->
      <!-- 连线或等价表示 -->
    </div>
  </body>
</html>
```

生成要求：

1. 固定画布尺寸，不做响应式改版
2. 使用显式坐标或等价布局约束
3. 颜色、边框、字体、间距全部来自 XML 样式映射
4. 分层区块、泳道、数据卡片、图例必须逐项落地

已知缺口：`mxgraph.flowchart.*` 命名空间形状当前仍存在未映射项，需在输出中标记告警。

## Phase 5: 交付与冻结

输出说明中要明确：

1. XML 是图表真源
2. HTML 是 PPT 前的视觉约束层
3. XML 后续变更时，HTML 必须整稿重生

推荐交付说明：

```markdown
- 图表真源：doc-ppt/<name>.xml
- 图表 HTML：doc-ppt/<name>.html
- 状态：HTML 已完成，可进入 PPT 页面编排
```
