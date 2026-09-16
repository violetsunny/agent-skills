# 自包含 HTML 构建规则（内化自 web-artifacts-builder，适配纯原生）

## 定位

确保 Web 演示产出为单个自包含 HTML 文件，零外部依赖，双击即可运行。

## 核心原则

1. **单文件交付**：所有 CSS/JS/SVG/图片资源全部 inline
2. **零 CDN**：禁止任何外部链接（字体、图标库、框架）
3. **零构建工具**：不使用 Vite/Webpack/Parcel，纯手写原生代码
4. **Node 无关**：最终产物不依赖 Node.js 运行时

## 资源内联策略

| 资源类型 | 内联方式 |
|---------|---------|
| CSS | `<style>` 标签内联在 `<head>` |
| JavaScript | `<script>` 标签内联在 `</body>` 前 |
| SVG 图标 | 直接嵌入 HTML 或 data URI |
| 小图片（<50KB） | base64 data URI |
| 大图片（≥50KB） | 同目录 assets/ 引用，或压缩后 base64 |
| 字体 | @font-face + base64 woff2，或使用系统字体栈 |

## 代码组织

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>演示标题</title>
  <style>
    /* === Token === */
    :root { ... }
    /* === Reset === */
    /* === Layout === */
    /* === Components === */
    /* === Animations === */
  </style>
</head>
<body>
  <!-- 页面结构 -->
  <script>
    // === State ===
    // === Navigation ===
    // === Animations ===
    // === Init ===
  </script>
</body>
</html>
```

## 性能约束

- 单页 DOM 节点 ≤ 500
- 动画仅限 transform/opacity/filter
- 首屏渲染 ≤ 1s（本地文件打开）
- 总文件大小建议 ≤ 2MB（含内联资源）

## 反 AI slop

- 禁止过度居中布局
- 禁止紫色渐变默认配色
- 禁止统一圆角（所有元素同一 border-radius）
- 禁止 Inter 字体作为唯一选择
