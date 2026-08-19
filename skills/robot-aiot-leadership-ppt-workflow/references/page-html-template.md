# 领导汇报 PPT 逐页 HTML 模板规范

本模板定义逐页 HTML 的画布尺寸、页面类型目录、样式规范、布局审查清单和布局修复模式速查表。
agent 在 Phase 4 逐页 HTML 化时，必须从本模板加载布局规范，按页面类型裁剪后填充内容。

---

## 1. 固定画布

- 尺寸：**1920 x 1080px**（16:9 全高清）
- 不使用响应式布局、`max-width`、`width:100%` 或媒体查询
- 每个 HTML 文件只表达一页幻灯片内容
- 画布容器使用 `position:relative; overflow:hidden`

```html
<div class="canvas" style="position:relative;width:1920px;height:1080px;overflow:hidden;">
  <!-- 页面内容，全部使用 position:absolute 定位 -->
</div>
```

---

## 2. 字体规范

字体顺序（macOS 优先）：

```css
font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
```

### CSS 变量引用

页面 HTML 中的区域间距、内边距和配色应引用第 4 节 `:root` 定义的 CSS 变量，不使用随意硬编码值：

- **间距**：`margin`、`padding` 引用 `var(--space-sm/md/lg)`，值尽量对齐 MD3 8dp 倍数（8/16/24/32/48px）
- **配色**：背景色、边框色、文字色引用 `var(--primary-color)`、`var(--accent-color)`、`var(--bg-color)` 等
- **设计系统注入**：Phase 4 调用 `ui-ux-pro-max --design-system` 后，其输出覆盖 `:root` 变量初始值

---

## 3. 页面类型目录

8 种页面类型，每种附带布局模式和坐标参考。可扩展新类型，但需在此目录登记。

### 3.1 封面页

- 布局：浅蓝渐变背景 + SVG 弧形装饰 + 核心结论文字 + 四能力卡片 + **右上角美的品牌 Logo**
- 不使用页眉蓝条
- 坐标参考：标题 top:60-120px，能力卡片 top:600-800px，Logo right:60px;top:60px;height:72px

### 3.2 架构图页

- 布局：分层布局（L1-L4），每层彩色背景 + 白色卡片 + SVG 连接线
- 页眉蓝条 height:10px
- 坐标参考：层间距 ~40px，卡片间距 ~20px，SVG 连接线贴合节点边缘

### 3.3 数据看板页

- 布局：上排核心大数字卡片（2-3 个）+ 下排指标卡片网格 + 底部总结蓝条
- 坐标参考：大数字卡片 top:200-350px，指标卡片 top:400-600px

### 3.4 闭环流程页

- 布局：垂直步骤卡片 + 步骤间箭头连接 + 侧边维度卡片 + 底部总结蓝条
- 坐标参考：步骤卡片 height:100px，箭头位于卡片间距正中

### 3.5 漏斗策略页

- 布局：四级漏斗卡片逐级放大 + 级间方向箭头 + 底部总结蓝条
- 坐标参考：卡片间距 ≥40px（箭头 font-size × 1.4），底部蓝条与最后一级间距 ≤40px

### 3.6 治理闭环页

- 布局：左半看板数据 + 右半闭环步骤（看见→止损→修复）+ 四维度卡片 + 底部总结蓝条
- 坐标参考：左右分栏分割线 left:942px，右栏 left:966px，步骤卡片 height:100px

### 3.7 案例对比页

- 布局：左右对比卡片 + VS 圆块居中 + 对比条 + 下半品牌卡片 + 底部总结蓝条
- 坐标参考：对比卡片 left 居中计算，VS 圆块位于两卡片间距正中

### 3.8 尾页

- 布局：核心结论大字居中 + 底部联系信息 + **底部居中美的品牌 Logo**
- 坐标参考：结论文字 top:400-500px，Logo bottom:60px;height:56px

---

## 4. 样式色板速查表

### CSS 变量定义（:root）

以下 CSS 变量定义配色和间距系统。**初始值为硬编码默认值**，在 Phase 4 调用 `ui-ux-pro-max --design-system` 后，其输出的配色方案和间距系统 SHOULD 覆盖这些初始值。首页架构图 XML 确立的主色 MUST 优先覆盖 `--primary-color`。

```css
:root {
  /* 配色变量 — 初始值，由 ui-ux-pro-max --design-system 输出覆盖 */
  --primary-color: #0078D4;       /* 主色（首页架构图主色优先覆盖） */
  --accent-color: #00C853;        /* 强调色 */
  --bg-color: #FFFFFF;            /* 背景色 */
  --text-primary: #003D6B;        /* 主文字色 */
  --text-secondary: #555555;      /* 次文字色 */
  --header-bg: #E3F2FD;           /* 浅蓝背景 */

  /* 间距系统变量 — 参考 MD3 8dp 间距 token，由 ui-ux-pro-max 设计系统输出注入 */
  --space-sm: 8px;                /* 小间距（MD3 8dp × 1） */
  --space-md: 16px;               /* 中间距（MD3 8dp × 2） */
  --space-lg: 24px;               /* 大间距（MD3 8dp × 3） */
}
```

**配色变量说明**：上述配色变量为初始默认值。Phase 4 调用 `ui-ux-pro-max --design-system` 后，将输出的配色方案注入这些变量。其中 `--primary-color` 由首页架构图 XML 确立的主色优先覆盖，`ui-ux-pro-max` 推荐的主色降级为辅助色。

**间距变量说明**：上述间距变量参考 `material-3/references/layout-and-responsive.md` 的 MD3 8dp 间距 token 系统（8/16/24/32/48px）。Phase 4 调用 `ui-ux-pro-max --design-system` 后，将输出的间距系统注入这些变量。页面 HTML 中的区域间距和内边距应引用这些变量，不使用随意值。

### 色板速查表

| 色系 | 背景色 | 边框色 | 用途 |
|---|---|---|---|
| 蓝 | `#E3F2FD` | `#0078D4` | 主能力、设备级运营 |
| 绿 | `#E8F5E9` | `#388E3C` | 成功状态、发布效率 |
| 深蓝 | `#E3F2FD` | `#1976D2` | 次级能力 |
| 紫 | `#F3E5F5` | `#7B1FA2` | 运营动作、定推 |
| 橙 | `#FFF3E0` | `#FF9800` | 警告、ODM 场景 |
| 红 | `#FFEBEE` | `#D32F2F` | 异常、止损 |
| 黄 | `#FFF8E1` | `#FFA000` | 区域分布 |

### 页眉蓝条

```css
.header-bar {
  position: absolute; left: 0; top: 0; width: 1920px; height: 10px;
  background: var(--primary-color);
}
```
适用于 P03-P07，封面页和尾页不使用。

### 底部总结蓝条

```css
.summary-bar {
  position: absolute; left: 60px; width: 1800px; height: 60px;
  background: var(--primary-color); border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: bold; color: #fff;
  padding: 0 var(--space-md);
}
```
top 值与上方最近元素间距 ≤40px。

### 白色卡片统一模式

```css
.card {
  background: var(--bg-color); border-radius: 10~12px;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.06~0.08);
  padding: var(--space-sm) var(--space-md);
}
```

---

## 5. 布局审查清单

每页生成后必须逐项检查，不通过则修复后重新检查：

| # | 检查项 | 验证方法 | 标准 |
|---|---|---|---|
| 1 | 画布尺寸一致性 | 检查 `.canvas` width/height | `1920px × 1080px` |
| 2 | 底部蓝条间距 | 蓝条 top - 上方元素 bottom | ≤40px |
| 3 | 元素不重叠 | 任意两绝对定位元素矩形不相交 | 无交集 |
| 4 | 分栏均衡 | 左右分栏高度差 | ≤100px |
| 5 | padding 充足性 | 卡片 padding | ≥14px |
| 6 | 字号下限 | 正文 / 数据大字 | 正文 ≥12px，数据 ≥28px |
| 7 | 箭头可见性 | 垂直卡片间距 vs 箭头 font-size | 间距 ≥ font-size × 1.4 |
| 8 | 徽章对齐 | flex 等高卡片底部徽章 | `flex-direction:column` + `margin-top:auto` |
| 9 | 内容溢出 | 卡片 height vs 内容行数 × line-height + padding | height ≥ 内容高度 |
| 10 | 水平居中 | 元素组左右边距差 | ≤20px |

---

## 6. SVG 连接线管理

架构图页的 SVG 连接线使用**节点边界速查表**管理坐标。

### 方法

1. 先建立速查表（节点名 → top/left/width/height）
2. 连线起止点从速查表中计算，不使用硬编码坐标
3. 连线起止点贴合节点边缘（误差 ≤5px）

### 速查表模板

```
| 节点名 | top | left | width | height | 上边缘 | 下边缘 | 左边缘 | 右边缘 |
|---|---|---|---|---|---|---|---|---|
| L1-卡片1 | 170 | 60 | 380 | 80 | 170 | 250 | 60 | 440 |
```

边缘值 = top/left + width/height，连线坐标从边缘值计算。

---

## 7. 布局修复模式速查表

生成后审查发现以下 4 类常见 bug 时，按对应 CSS 修复模式修复：

| Bug 类型 | 症状 | 根因 | CSS 修复模式 |
|---|---|---|---|
| **箭头被遮挡** | 垂直排列卡片间的 `↓` 箭头被下方卡片背景遮盖 | 卡片间距 < 箭头渲染高度 | 间距 ≥ font-size × 1.4；箭头 top = 上卡片 bottom + (gap - font-size) / 2 |
| **flex 徽章错位** | flex stretch 等高卡片内底部徽章因内容行数不同而垂直错位 | 徽章用固定 `margin-top` 相对内容定位 | 卡片 `display:flex;flex-direction:column` + 徽章 `margin-top:auto` |
| **内容溢出** | 卡片文字超出边框 | height < 内容行数 × line-height + padding | height ≥ line_count × line-height + padding-top + padding-bottom |
| **水平偏移** | 元素组未在画布内居中，左右空白不对称 | left 值未居中计算 | left = (1920 - element_width) / 2 |

---

## 8. 可隐藏区域

不同页面类型可裁剪区域，但标题区和底部总结不可隐藏（**封面页（cover 类型）无底部总结蓝条，此规则仅适用于内容页**）：

| 页面类型 | 隐藏区域 | 说明 |
|---|---|---|
| 全图页 | 结论区、数据区 | 图表占满中部 |
| 对比页 | 图表区 | 左右两列数据对比 |
| 纯数据页 | 图表区 | 只有数据表格 |
| 封面页 | 结论区、图表区、数据区、备注区 | 只有标题区，居中放大 |
| 标准页 | 无隐藏 | 全区域齐全 |

---

## 9. 图表嵌入约束

图表区引用 `robot-aiot-xml-html-bridge` 生成的图表 HTML，不自造替代图表：

```html
<!-- 正确：引用 Phase 3.5 生成的图表 HTML -->
<div class="chart-zone">
  <iframe src="../<图表名>.html" width="100%" height="100%" frameborder="0"></iframe>
</div>

<!-- 正确：直接嵌入图表 HTML 的关键内容（需与图表 HTML 视觉一致） -->
<div class="chart-zone">
  <!-- 从 doc-ppt/<图表名>.html 提取的图表内容 -->
</div>

<!-- 错误：自造一份不同风格的替代图表 -->
<div class="chart-zone">
  <div style="...">自行绘制的不同风格图表</div>
</div>
```

**约束：**
- 图表区引用 `doc-ppt/<图表名>.html`，不自造替代图表
- 图表 HTML 使用的主色必须与页面配色体系统一
- 图表区的尺寸比例应与图表 HTML 的画布比例协调，不强制拉伸变形

---

## 10. 完整模板示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第 N 页：<页面标题></title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    /* 配色变量 — 初始值，由 ui-ux-pro-max --design-system 输出覆盖 */
    --primary-color: #0078D4;
    --accent-color: #00C853;
    --bg-color: #FFFFFF;
    --text-primary: #003D6B;
    --text-secondary: #555555;
    --header-bg: #E3F2FD;
    /* 间距变量 — 参考 MD3 8dp 间距 token */
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
  }
  body { background: #f5f5f5; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
  .canvas {
    position: relative;
    width: 1920px;
    height: 1080px;
    margin: var(--space-md) auto;
    background: var(--bg-color);
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  }
  .header-bar {
    position: absolute; left: 0; top: 0; width: 1920px; height: 10px;
    background: var(--primary-color);
  }
  .page-num {
    position: absolute; bottom: var(--space-md); left: var(--space-md);
    font-size: 16px; color: #aab4cc;
  }
  /* 美的品牌 Logo — 封面页右上角 */
  .brand-logo-cover {
    position: absolute; right: 60px; top: 60px; height: 72px;
    object-fit: contain;
  }
  /* 美的品牌 Logo — 内容页页脚水印 */
  .brand-logo-footer {
    position: absolute; right: 60px; bottom: 24px; height: 28px;
    object-fit: contain; opacity: 0.85;
  }
</style>
</head>
<body>
<div class="canvas">

  <div class="header-bar"></div>

  <!-- 页面标题 -->
  <div style="position:absolute;left:60px;top:28px;font-size:32px;font-weight:bold;color:#003D6B;">
    第 N 页：<页面标题>
  </div>
  <div style="position:absolute;left:60px;top:76px;font-size:18px;color:#0078D4;font-weight:bold;">
    <一句话定位>
  </div>
  <div style="position:absolute;left:60px;top:114px;font-size:15px;color:#555;">
    <补充说明>
  </div>
  <div style="position:absolute;left:60px;top:146px;width:1800px;height:2px;background:#E3F2FD;"></div>

  <!-- 中部内容区域（按页面类型布局） -->
  <!-- ... -->

  <!-- 底部总结蓝条 -->
  <div style="position:absolute;left:60px;top:<N>px;width:1800px;height:60px;
    background:#0078D4;border-radius:10px;
    display:flex;align-items:center;justify-content:center;">
    <div style="font-size:16px;font-weight:bold;color:#fff;">
      💡 <一句话总结>
    </div>
  </div>

  <div class="page-num">第 N 页</div>

  <!-- 美的品牌 Logo（内容页页脚水印，封面页改用 .brand-logo-cover 类） -->
  <img src="../assets/midea-logo.png" class="brand-logo-footer" alt="Midea"/>
</div>
</body>
</html>
```
