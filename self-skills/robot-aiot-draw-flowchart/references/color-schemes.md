# Color Schemes Reference

> **调色板谱系声明：** 通用图表节点与风格皮肤的默认主谱系是 `style-guide.md` / `design-system.md` §5 的语义 token（暖系编辑皮肤，机器人/IoT 场景优先把本文件主题色注入为品牌 token）。本文件的 `#0078D4` 科技蓝主题及其派生表为**辅助谱系**，仅适用于：① 机器人/IoT 设备本体与状态语义（联网、OTA、设备分组等）；② Azure/云厂商品牌语义；③ 用户明确要求蓝色系的场景。辅助谱系不得反向覆盖主谱系的语义 token。
>
> **draw.io Style Code 豁免声明：** 本文各节 `Style Code` 为 draw.io style 语法的色值登记示例，供 draw.io XML 路径直接使用，并作 SVG 直绘 / XML→HTML 桥接产物的色彩参考；SVG 渲染时按 `design-system.md` 换算（阴影禁令 §4、圆角上限 6–10 等），本文示例已按该权威对齐。

## Primary Color Themes

### Tech Blue (科技蓝)
**Use for:** Normal state, connectivity, active processes

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#0078D4` | Main robot body, primary buttons |
| Secondary | `#4DA8DA` | LiDAR, highlights, accents |
| Background | `#E3F2FD` | Status card backgrounds (layer/zone 背景请使用 `#E8F4FD`，见 Zone Background Colors) |
| Border | `#005A9E` | Strokes, main flow arrows |
| Text | `#003D6B` | Titles, important labels |

**Style Code:**
```
ellipse;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=2;shadow=1;
```

### Dark Black (暗夜黑)
**Use for:** Product appearance, hardware views, physical representation

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#333333` | Robot body (realistic) |
| Secondary | `#666666` | LiDAR, wheels, details |
| Highlight | `#555555` | Subtle accents |
| Border | `#1A1A1A` | Main strokes |
| Shadow | `#222222` | Depth elements |

**Style Code:**
```
ellipse;fillColor=#333333;strokeColor=#1A1A1A;strokeWidth=2;shadow=1;
```

### Fresh Green (清新绿)
**Use for:** Success state, cleaning complete, normal operation

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#00C853` | Success indicators, check marks |
| Secondary | `#82B366` | Cleaning trails, progress |
| Background | `#E8F5E9` | Success card backgrounds |
| Border | `#009624` | Success borders |
| Text | `#2E7D32` | Success messages |

**Style Code:**
```
ellipse;fillColor=#00C853;strokeColor=#009624;strokeWidth=2;shadow=1;
```

### Alert Red (告警红)
**Use for:** Error state, blocked, fault conditions

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#B85450` | Error indicators, warnings |
| Secondary | `#F8CECC` | Error card backgrounds |
| Border | `#8C2E2E` | Error borders, blocked arrows |
| Text | `#8C2E2E` | Error messages |

**Style Code:**
```
ellipse;fillColor=#B85450;strokeColor=#8C2E2E;strokeWidth=2;shadow=1;
```

### Upgrade Purple (升级紫)
**Use for:** OTA upgrade in progress, firmware updates

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#9673A6` | Upgrade indicators |
| Secondary | `#E1D5E7` | Upgrade card backgrounds |
| Border | `#6A4C7D` | Upgrade borders |
| Text | `#6A4C7D` | Upgrade messages |

**Style Code:**
```
ellipse;fillColor=#9673A6;strokeColor=#6A4C7D;strokeWidth=2;shadow=1;
```

## Secondary Colors

### Product Silver (产品银)
**Use for:** Product-illustration style robot bodies (detailed top-view icons), hardware shells with light metallic look

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#D9D9D9` | Light metallic body fill |
| Border | `#666666` | Body rim, seam lines |
| Highlight | `#FFFFFF` | Inner disc, panels |

**Style Code:**
```
ellipse;fillColor=#D9D9D9;strokeColor=#666666;strokeWidth=3;shadow=0;
```

### Warning Yellow (警告黄)
**Use for:** Charging, low battery, caution states

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#D6B656` | Warning indicators |
| Secondary | `#FFF8E1` | Warning card backgrounds |
| Border | `#B8960F` | Warning borders |
| Text | `#B8960F` | Warning messages |

### Side Brush Orange (边刷橙)
**Use for:** Side brushes, mechanical action indicators

| Element | Color Code | Style |
| --- | --- | --- |
| Primary | `#FF6B35` | Side brushes, action highlights |
| Border | `#E55A2B` | Brush outlines |

**Style Code:**
```
shape=spiral;fillColor=none;strokeColor=#FF6B35;strokeWidth=2;
```

## Arrow Colors by Purpose

> **统一样式规范：** 所有箭头 strokeWidth=3。虚线（dashed）仅用于反馈回路、循环回退，以及"隔离/断联/边界切断"类目（链路断开、组件下线、网络/信任边界切断）；演进/推进/错误路径一律实线。

| Purpose | Color | Stroke Width | Style |
| --- | --- | --- | --- |
| Main flow | `#005A9E` | 3px | Solid |
| Success path | `#82B366` | 3px | Solid |
| Error/blocked | `#B85450` | 3px | Solid |
| Feedback loop | `#0078D4` | 3px | Dashed |
| Data reporting | `#82B366` | 3px | Solid |
| Control signal | `#B85450` | 3px | Solid |
| Cross-layer | target layer color | 3px | Solid |

## Status Card Backgrounds

| Status | Background Color | Border Color | Text Color |
| --- | --- | --- | --- |
| Normal | `#E8F5E9` | `#82B366` | `#2E7D32` |
| Active | `#E3F2FD` | `#0078D4` | `#005A9E` |
| Upgrading | `#F3E5F5` | `#9673A6` | `#6A4C7D` |
| Error | `#FFEBEE` | `#B85450` | `#8C2E2E` |
| Charging | `#FFF8E1` | `#D6B656` | `#B8960F` |

**Card Style Code:**
```
rounded=1;fillColor=#E3F2FD;strokeColor=#0078D4;strokeWidth=2;arcSize=20;shadow=1;
```

## Regional/Device Group Colors

| Region/Group | Fill Color | Border Color |
| --- | --- | --- |
| China | `#D5E8D4` | `#82B366` |
| Asia Pacific | `#D5E8D4` | `#82B366` |
| Europe | `#D5E8D4` | `#82B366` |
| North America | `#D5E8D4` | `#82B366` |

**Device Group Style Code:**
```
shape=cylinder3;fillColor=#D5E8D4;strokeColor=#82B366;size=10;
```

## Zone Background Colors

| Zone Type | Fill Color | Border Color | Opacity |
| --- | --- | --- | --- |
| iFlow Platform | `#E8F4FD` | `#0078D4` | 60% |
| OTA Service | `#F0F7FC` | `#005A9E` | 60% |
| Global Devices | `#F5FBF5` | `#82B366` | 60% |
| Admin Console | `#FDF5E6` | `#D6B656` | 60% |

**Zone Background Style Code:**
```
rounded=1;fillColor=#E8F4FD;strokeColor=#0078D4;strokeWidth=2;dashed=1;arcSize=8;opacity=60;
```

## Color Usage Rules

1. **One primary color per state** — Don't mix blue and green for the same status
2. **Consistent meaning** — Red always means error, green always means success
3. **Background opacity** — Zone backgrounds should be 60% opacity to avoid visual dominance
4. **Text contrast** — Always ensure text is readable against background (use dark text on light backgrounds)
5. **Border consistency** — Main elements use 2px borders, details use 1px, layer containers use 3px
6. **Shadow usage** — Apply shadows only to key visual elements (robot bodies, core ellipses); regular nodes use shadow=0
7. **Dashed for feedback only** — Use dashed lines exclusively for feedback loops and loop-back arrows; error paths and progression arrows are solid。虚线还可用于"隔离/断联/边界切断"类目（链路断开、组件下线、边界切断）；除此之外一律实线
8. **Palette-only colors** — Only use colors defined in this file. Do NOT introduce off-palette colors (e.g., `#FFF3E0`/`#FF9800` are forbidden; use `#FFF8E1`/`#FFA000` for warning yellow instead)
9. **Blue layer background** — Layer/zone backgrounds use `#E8F4FD`; `#E3F2FD` is reserved for status card backgrounds only
10. **中性工具色豁免** — `#CCCCCC` 一类中性工具色仅限非数据元素（分隔线、占位边框、禁用态、中性汇总容器边框），是色板规则的明确豁免，不与"数据系列禁灰"冲突；数据系列/状态语义仍禁止用灰色表达
11. **箭头颜色双源裁决** — 同一箭头同时命中本表通用语义色（Main flow/Success/Error 等）与图表类型/层级配色规则（如分层图跨层箭头用目标层主题色）时，图表类型/层级规则优先

## 静态交付产物场景配色对齐声明

**机器人/IoT 主题静态交付产物默认主色**：`#0078D4`（科技蓝）——属上方「调色板谱系声明」中辅助谱系的设备语义应用。图表嵌入汇报页面、文档插图、离线演示等静态交付产物时，以该色为主色，确保图表 HTML 与宿主页面的配色体系统一；调用方注入品牌 token 或指定 style-guide 皮肤时，以主谱系为准。
