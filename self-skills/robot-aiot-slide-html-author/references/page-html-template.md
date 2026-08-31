# 领导汇报逐页 HTML 模板

本模板定义固定画布、页面类型、token 变量、布局检查与图表嵌入约束。

## 1. 固定画布

1. 尺寸固定为 `1920 x 1080px`
2. 不使用响应式布局、媒体查询、`max-width` 或 `width: 100%` 页面思维
3. 每个 HTML 文件只表达一页幻灯片
4. 画布容器使用 `position: relative; overflow: hidden`

```html
<div class="canvas" style="position:relative;width:1920px;height:1080px;overflow:hidden;">
  <!-- 页面内容全部放在固定画布内 -->
</div>
```

## 2. 字体与 token

字体栈：

```css
font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
```

推荐根变量：

```css
:root {
  --primary-color: #0078D4;
  --secondary-color: #4F6BED;
  --tertiary-color: #00A389;
  --surface-color: #FFFFFF;
  --surface-muted: #F5F7FB;
  --outline-color: #D7DFEA;
  --text-primary: #16324F;
  --text-secondary: #5B6B7F;
  --success-color: #1F9D55;
  --warning-color: #D98324;
  --danger-color: #C93C37;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;
  --shadow-soft: 0 6px 24px rgba(18, 52, 86, 0.08);
}
```

规则：

1. 首页架构图主色优先覆盖 `--primary-color`
2. 页面中优先引用变量，不散落硬编码颜色和值
3. 表现层需要新颜色时，先判断是否能映射到现有语义角色

## 3. 页面类型

常用 8 类页面：

1. 封面页：核心结论、项目定位、能力卡、右上角 Logo
2. 架构图页：分层结构、连接关系、少量数字锚点
3. 数据看板页：上排大数字，下排指标卡片，底部总结
4. 闭环流程页：垂直步骤、箭头连接、侧边维度卡
5. 漏斗策略页：层级递进、方向箭头、底部总结
6. 治理闭环页：左右分栏，左数右流程
7. 案例对比页：左右对照、中心对比点、总结区
8. 尾页：核心结论收束、联系信息、底部居中 Logo

## 4. 常用区块

1. 页面标题区：说明本页主题
2. 结论区：一句话结论，必须突出
3. 主内容区：图表、表格、数字卡、流程图
4. 说明区：解释因果、风险、动作
5. 品牌区：封面右上或内容页页脚 Logo
6. 总结区：内容页底部总结条，可选但常用

## 5. 布局审查清单

每页生成后逐项检查：

| # | 检查项 | 标准 |
|---|---|---|
| 1 | 画布尺寸 | `.canvas` 为 `1920px × 1080px` |
| 2 | 标题可见性 | 标题未被装饰元素、Logo、图表遮挡 |
| 3 | 结论显著性 | 结论区是首屏第二视觉焦点 |
| 4 | 元素不重叠 | 任意两个主要绝对定位块无交叠 |
| 5 | 分栏均衡 | 左右主栏高度差不超过 `100px` |
| 6 | 内边距充足 | 卡片 `padding >= 14px` |
| 7 | 字号下限 | 正文 `>= 16px`，标签 `>= 12px`，主数字建议 `>= 28px` |
| 8 | 内容不溢出 | 文本、表格、卡片内容不超框 |
| 9 | 图表一致性 | 页面图表引用真源 HTML，未被替换重绘 |
| 10 | 水平居中 | 需要居中的元素组左右偏差不超过 `20px` |

## 6. 图表嵌入约束

图表区优先引用 Phase 3.5 已产出的 HTML：

```html
<div class="chart-zone">
  <iframe src="../<图表名>.html" width="100%" height="100%" frameborder="0"></iframe>
</div>
```

规则：

1. 不自造一份不同语义的替代图表
2. 图表区尺寸要尊重原图表比例，不强拉伸变形
3. 页面 token 可以统一外层容器，但不覆盖图表事实表达

## 7. 模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>第 N 页：页面标题</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --primary-color: #0078D4;
      --secondary-color: #4F6BED;
      --tertiary-color: #00A389;
      --surface-color: #FFFFFF;
      --surface-muted: #F5F7FB;
      --outline-color: #D7DFEA;
      --text-primary: #16324F;
      --text-secondary: #5B6B7F;
      --space-sm: 8px;
      --space-md: 16px;
      --space-lg: 24px;
      --space-xl: 32px;
      --space-2xl: 48px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      --shadow-soft: 0 6px 24px rgba(18, 52, 86, 0.08);
    }
    body {
      background: #EEF2F7;
      font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    }
    .canvas {
      position: relative;
      width: 1920px;
      height: 1080px;
      margin: var(--space-md) auto;
      background: var(--surface-color);
      overflow: hidden;
      box-shadow: var(--shadow-soft);
    }
  </style>
</head>
<body>
  <div class="canvas">
    <!-- 标题区 -->
    <!-- 结论区 -->
    <!-- 主内容区 -->
    <!-- 说明区 -->
    <!-- 品牌区 -->
  </div>
</body>
</html>
```
