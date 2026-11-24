# 变体路线：静态 SVG 移植（单文件自包含）

用户明确要求**单文件自包含**交付时使用。代价：archify 交互与动效全部舍弃，合成页不受 archify 校验门覆盖。

## 提取清单（自 archify 产物 html）

1. `<svg viewBox ...>...</svg>` 整段（含其内嵌 `<style>`，tree-* 结构类全在内）。
2. 页面级 CSS 中的语义 class 规则（`.c-grid .c-mask .c-frontend .c-backend .c-external .t-primary .t-muted .a-default .m-default .m-emphasis .m-security .m-dashed` 及 `svg [data-node-id] > .c-mask`），加宿主作用域前缀防污染。
3. `<style id="archify-fonts">` 内嵌字体块（JetBrains Mono WOFF2 base64，保拉丁字形度量；CJK 走系统 fallback）。
4. 主题变量块：archify 变量中性色映射到 diagram-design tokens（`--text`→ink `#2d3142`、`--text-muted`→muted `#4f5d75`、`--text-dim/--text-faint`→soft `#5a6580`、`--arrow`→muted、`--arrow-emphasis`→accent `#bf4520`、`--lane-stroke`→rule-solid `#bfc0c0`、`--mask`→`#ffffff`），语义分支色（frontend/backend/database/cloud/security/messagebus/external）保留 archify 原值。

## 静态安全性

archify 动效全由 `html[data-motion-capable]`/`[data-ambient-entry]` 属性门控，宿主页不加这些属性即静态完整态；tree 折叠按钮变死控件（默认全展开，可接受）。

## 宿主 svg 规则

`.archify-fragment svg { min-width: <viewBox 宽>px; width: 100%; display: block; }`，容器 `overflow-x: auto`，print 时 `min-width: 0`。

## 实测参考

pilot（2026-11-19，JVM tree 24 节点，viewBox 924×1551）：移植页 155KB 单文件，Chrome headless 截图验证节点完整、配色统一。
