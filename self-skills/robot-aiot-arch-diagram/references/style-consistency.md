# 统一样式规范

本文件承载样式数值统一的增量标准；样式唯一权威是 `design-system.md`（语义 token 见 `style-guide.md`），冲突时以权威为准。draw.io XML 路径已移除（SKILL.md 硬约束 1）；路径 B 直绘 SVG 时按属性映射执行：`fontSize`→`font-size`、`strokeWidth`→`stroke-width`、`arcSize`→`rx`、`fillColor`→`fill`、`shadow=0`→不加滤镜。`references/` 中的示例若与这里冲突，以本文件与 `design-system.md` 为准。

## 节点样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| fontSize | 12 | 所有普通节点统一 |
| strokeWidth | 2 | 所有普通节点统一 |
| arcSize | 6–8 | 圆角对齐 design-system §7 允许集 {4, 6, 8}，上限 6–10（§4） |
| shadow | 0 | 常规节点不使用阴影 |
| fillColor | #FFFFFF | 常规节点白色填充 |

## 分层容器样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| strokeWidth | 3 | 分层容器统一 |
| 层标签 fontSize | 16 | 层标签统一 |
| 层标签 fontColor | 层边框色 | 与层色对齐 |
| 蓝色层 fillColor | #E8F4FD | 不使用 `#E3F2FD` |
| 主椭圆 strokeWidth | 3 | 核心椭圆强调但不再放大到 4 |

## 箭头样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| strokeWidth | 3 | 所有箭头统一 |
| dashed 语义 | 仅反馈/循环 | 演进、推进、错误路径一律实线 |

## 文本与内嵌样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| 内嵌 HTML font-size | 11px | 节点内富文本统一 |

## 颜色使用标准

1. 颜色语义 token 以 `style-guide.md` / `design-system.md` 为单一真源；机器人/IoT 主题色板见 `references/color-schemes.md`（辅助谱系使用条件见该文件头部声明）
2. 警告黄色系固定为背景 `#FFF8E1`、边框/主色 `#FFA000`
3. 蓝色层背景固定为 `#E8F4FD`

## 语义例外

| 元素 | 偏离项 | 原因 |
|------|--------|------|
| 语义强调节点 | 特殊背景色 + strokeWidth=3 | 需要视觉突出 |
| 总结条/摘要条 | fontSize=14 | 需要层级区分 |
| 主椭圆等核心视觉元素 | fillColor=层色 + strokeWidth=3 | 保留焦点强调；强调用填充与边框承载，不用阴影（design-system §4 阴影禁令） |

判断原则：任何偏离标准的样式都必须有明确语义理由。
