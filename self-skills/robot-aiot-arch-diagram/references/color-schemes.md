# Color Schemes Reference

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

> **统一样式规范：** 所有箭头 strokeWidth=3。虚线（dashed）仅用于反馈回路和循环回退，演进/推进/错误路径一律实线。

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
7. **Dashed for feedback only** — Use dashed lines exclusively for feedback loops and loop-back arrows; error paths and progression arrows are solid
8. **Palette-only colors** — Only use colors defined in this file. Do NOT introduce off-palette colors (e.g., `#FFF3E0`/`#FF9800` are forbidden; use `#FFF8E1`/`#FFA000` for warning yellow instead)
9. **Blue layer background** — Layer/zone backgrounds use `#E8F4FD`; `#E3F2FD` is reserved for status card backgrounds only

## PPT 场景配色对齐声明

**PPT 领导汇报场景默认色**：主色 `#0078D4`（科技蓝 Tech Blue）。在 PPT 汇报图表场景中，应使用该色作为主色，以确保图表 HTML 与汇报逐页 HTML 的配色体系统一。
