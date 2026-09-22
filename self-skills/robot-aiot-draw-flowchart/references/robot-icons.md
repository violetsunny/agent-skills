# 扫地机器人图标参考（Robot Vacuum Icons）

> **⚠️ 路径豁免声明：** 本文 draw.io mxGraphModel XML 可作 draw.io 可编辑交付，也可作 SVG 直绘 / XML→HTML 桥接产物的布局结构参考。机器人图标属插画资产而非流程图节点：机身子形状可用符合形态的 arcSize/填充（如 arcSize=40/50 的圆润机身），流程图节点样式以 `design-system.md` 为唯一权威；阴影禁令（§4）对本文件所有元素同样生效。
>
> **调色板谱系声明：** 本文件中的 `#0078D4` 蓝色系为辅助谱系，仅用于机器人/设备本体语义（按键、激光雷达、联网状态等）；通用图表节点的默认主谱系以 `style-guide.md` / `design-system.md` 为准。

## 基础机器人图标

### 1. 简约俯视
```xml
<mxCell id="robot_simple" value="" style="ellipse;fillColor=#333333;strokeColor=#1A1A1A;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry width="80" height="80" as="geometry" />
</mxCell>
<mxCell id="robot_lidar" value="" style="ellipse;fillColor=#555555;strokeColor=#444444;strokeWidth=1;" vertex="1" parent="1">
  <mxGeometry x="25" y="5" width="30" height="20" as="geometry" />
</mxCell>
<mxCell id="robot_btn" value="" style="ellipse;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=1;" vertex="1" parent="1">
  <mxGeometry x="32" y="35" width="16" height="16" as="geometry" />
</mxCell>
```

### 2. 带边刷俯视
```xml
<mxCell id="robot_body" value="" style="ellipse;fillColor=#444444;strokeColor=#222222;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="15" y="10" width="80" height="80" as="geometry" />
</mxCell>
<mxCell id="robot_lidar" value="" style="ellipse;fillColor=#666666;strokeColor=#555555;" vertex="1" parent="1">
  <mxGeometry x="40" y="15" width="30" height="18" as="geometry" />
</mxCell>
<mxCell id="brush_left" value="" style="shape=spiral;fillColor=none;strokeColor=#FF6B35;strokeWidth=2;rotation=-30;" vertex="1" parent="1">
  <mxGeometry x="2" y="60" width="25" height="25" as="geometry" />
</mxCell>
<mxCell id="brush_right" value="" style="shape=spiral;fillColor=none;strokeColor=#FF6B35;strokeWidth=2;rotation=30;" vertex="1" parent="1">
  <mxGeometry x="82" y="60" width="25" height="25" as="geometry" />
</mxCell>
<mxCell id="robot_btn" value="" style="ellipse;fillColor=#00C853;strokeColor=#009624;" vertex="1" parent="1">
  <mxGeometry x="47" y="42" width="16" height="16" as="geometry" />
</mxCell>
```

### 3. 侧视图
```xml
<mxCell id="robot_side_body" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#444444;strokeColor=#222222;strokeWidth=2;arcSize=40;" vertex="1" parent="1">
  <mxGeometry x="10" y="25" width="100" height="40" as="geometry" />
</mxCell>
<mxCell id="robot_lidar_top" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#666666;strokeColor=#555555;arcSize=30;" vertex="1" parent="1">
  <mxGeometry x="30" y="15" width="40" height="15" as="geometry" />
</mxCell>
<mxCell id="wheel_left" value="" style="ellipse;fillColor=#222222;strokeColor=#111111;" vertex="1" parent="1">
  <mxGeometry x="20" y="58" width="20" height="15" as="geometry" />
</mxCell>
<mxCell id="wheel_right" value="" style="ellipse;fillColor=#222222;strokeColor=#111111;" vertex="1" parent="1">
  <mxGeometry x="80" y="58" width="20" height="15" as="geometry" />
</mxCell>
<mxCell id="sensor" value="" style="ellipse;fillColor=#0078D4;strokeColor=#005A9E;" vertex="1" parent="1">
  <mxGeometry x="95" y="35" width="10" height="10" as="geometry" />
</mxCell>
```

## 状态专用图标

### 4. 联网/OTA 状态
```xml
<mxCell id="robot_connected" value="" style="ellipse;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="20" y="30" width="70" height="70" as="geometry" />
</mxCell>
<mxCell id="robot_lidar_blue" value="" style="ellipse;fillColor=#4DA8DA;strokeColor=#0078D4;" vertex="1" parent="1">
  <mxGeometry x="38" y="35" width="24" height="15" as="geometry" />
</mxCell>
<mxCell id="signal_wave1" value="" style="ellipse;fillColor=none;strokeColor=#0078D4;strokeWidth=1.5;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="5" y="10" width="30" height="30" as="geometry" />
</mxCell>
<mxCell id="signal_wave2" value="" style="ellipse;fillColor=none;strokeColor=#0078D4;strokeWidth=1;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="-5" y="0" width="45" height="45" as="geometry" />
</mxCell>
<mxCell id="wifi_icon" value="📶" style="text;html=1;fontSize=16;align=center;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="75" y="5" width="30" height="25" as="geometry" />
</mxCell>
```

### 5. 充电中
```xml
<mxCell id="robot_charging" value="" style="ellipse;fillColor=#555555;strokeColor=#333333;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="20" y="25" width="70" height="70" as="geometry" />
</mxCell>
<mxCell id="battery_icon" value="⚡" style="text;html=1;fontSize=24;align=center;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="38" y="40" width="35" height="35" as="geometry" />
</mxCell>
<mxCell id="charging_dock" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#888888;strokeColor=#666666;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="90" y="35" width="15" height="50" as="geometry" />
</mxCell>
```

### 6. 清扫中
```xml
<mxCell id="cleaning_trail" value="" style="endArrow=classic;strokeColor=#82B366;strokeWidth=2;dashed=1;curved=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="10" y="80" as="sourcePoint" />
    <mxPoint x="50" y="50" as="targetPoint" />
    <Array as="points">
      <mxPoint x="20" y="40" />
      <mxPoint x="35" y="70" />
    </Array>
  </mxGeometry>
</mxCell>
<mxCell id="robot_cleaning" value="" style="ellipse;fillColor=#333333;strokeColor=#1A1A1A;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="40" y="30" width="60" height="60" as="geometry" />
</mxCell>
<mxCell id="clean_btn" value="" style="ellipse;fillColor=#00C853;strokeColor=#009624;" vertex="1" parent="1">
  <mxGeometry x="60" y="50" width="14" height="14" as="geometry" />
</mxCell>
<mxCell id="sparkle" value="✨" style="text;html=1;fontSize=14;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="85" y="20" width="25" height="25" as="geometry" />
</mxCell>
```

### 7. 告警/故障
```xml
<mxCell id="robot_error" value="" style="ellipse;fillColor=#B85450;strokeColor=#8C2E2E;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="15" y="25" width="70" height="70" as="geometry" />
</mxCell>
<mxCell id="warning_icon" value="⚠️" style="text;html=1;fontSize=22;align=center;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="32" y="40" width="35" height="35" as="geometry" />
</mxCell>
```

### 8. OTA 升级中
```xml
<mxCell id="robot_upgrading" value="" style="ellipse;fillColor=#9673A6;strokeColor=#6A4C7D;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="20" y="25" width="70" height="70" as="geometry" />
</mxCell>
<mxCell id="upgrade_arrow" value="⬆️" style="text;html=1;fontSize=20;align=center;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="38" y="38" width="35" height="35" as="geometry" />
</mxCell>
<mxCell id="progress_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#FFFFFF;strokeWidth=1;arcSize=50;" vertex="1" parent="1">
  <mxGeometry x="30" y="78" width="50" height="8" as="geometry" />
</mxCell>
<mxCell id="progress_fill" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;arcSize=50;" vertex="1" parent="1">
  <mxGeometry x="30" y="78" width="30" height="8" as="geometry" />
</mxCell>
```

## 产品插画风格

### 9. 智能家居产品风格（详细俯视）

复刻 draw.io「Smart Home / IoT Devices」形状库的产品插画风格：浅银机身、白色内盘、绿色电源键、蓝色 LDS 塔与回充键、黑色三叉边刷、灰尘粒子。纯矢量 mxCell 组合，包围盒约 200x200。

```xml
<!-- 灰尘粒子（最底层） -->
<mxCell id="pv_dust1" value="" style="ellipse;fillColor=#666666;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="30" y="190" width="5" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_dust2" value="" style="ellipse;fillColor=#666666;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="45" y="193" width="4" height="4" as="geometry" />
</mxCell>
<mxCell id="pv_dust3" value="" style="ellipse;fillColor=#666666;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="58" y="188" width="3" height="3" as="geometry" />
</mxCell>
<mxCell id="pv_dust4" value="" style="ellipse;fillColor=#666666;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="140" y="190" width="4" height="4" as="geometry" />
</mxCell>
<mxCell id="pv_dust5" value="" style="ellipse;fillColor=#666666;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="155" y="193" width="5" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_dust6" value="" style="ellipse;fillColor=#666666;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="168" y="188" width="3" height="3" as="geometry" />
</mxCell>
<!-- 左边刷（三叉，rotation 对称） -->
<mxCell id="pv_brush_l1" value="" style="rounded=1;fillColor=#1A1A1A;strokeColor=none;arcSize=50;rotation=20;" vertex="1" parent="1">
  <mxGeometry x="18" y="169" width="40" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_brush_l2" value="" style="rounded=1;fillColor=#1A1A1A;strokeColor=none;arcSize=50;rotation=80;" vertex="1" parent="1">
  <mxGeometry x="18" y="169" width="40" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_brush_l3" value="" style="rounded=1;fillColor=#1A1A1A;strokeColor=none;arcSize=50;rotation=140;" vertex="1" parent="1">
  <mxGeometry x="18" y="169" width="40" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_hub_l" value="" style="ellipse;fillColor=#1A1A1A;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="33" y="167" width="10" height="10" as="geometry" />
</mxCell>
<!-- 右边刷（三叉，rotation 对称） -->
<mxCell id="pv_brush_r1" value="" style="rounded=1;fillColor=#1A1A1A;strokeColor=none;arcSize=50;rotation=20;" vertex="1" parent="1">
  <mxGeometry x="142" y="169" width="40" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_brush_r2" value="" style="rounded=1;fillColor=#1A1A1A;strokeColor=none;arcSize=50;rotation=80;" vertex="1" parent="1">
  <mxGeometry x="142" y="169" width="40" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_brush_r3" value="" style="rounded=1;fillColor=#1A1A1A;strokeColor=none;arcSize=50;rotation=140;" vertex="1" parent="1">
  <mxGeometry x="142" y="169" width="40" height="5" as="geometry" />
</mxCell>
<mxCell id="pv_hub_r" value="" style="ellipse;fillColor=#1A1A1A;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="157" y="167" width="10" height="10" as="geometry" />
</mxCell>
<!-- 机身外圈 -->
<mxCell id="pv_body" value="" style="ellipse;fillColor=#D9D9D9;strokeColor=#666666;strokeWidth=3;shadow=0;" vertex="1" parent="1">
  <mxGeometry x="10" y="0" width="180" height="180" as="geometry" />
</mxCell>
<!-- 保险杠接缝线 -->
<mxCell id="pv_seam" value="" style="endArrow=none;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="12" y="90" as="sourcePoint" />
    <mxPoint x="188" y="90" as="targetPoint" />
  </mxGeometry>
</mxCell>
<!-- 白色内盘 -->
<mxCell id="pv_inner" value="" style="ellipse;fillColor=#FFFFFF;strokeColor=#D9D9D9;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="45" y="35" width="110" height="110" as="geometry" />
</mxCell>
<!-- 顶部控制行：左点缀方块 / 电源键 / 右点缀方块 -->
<mxCell id="pv_btn_left" value="" style="rounded=1;fillColor=#00C853;strokeColor=#009624;strokeWidth=1;arcSize=30;" vertex="1" parent="1">
  <mxGeometry x="68" y="50" width="16" height="16" as="geometry" />
</mxCell>
<mxCell id="pv_btn_power" value="⏻" style="rounded=1;fillColor=#00C853;strokeColor=#009624;strokeWidth=1;arcSize=30;fontColor=#FFFFFF;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="90" y="46" width="24" height="24" as="geometry" />
</mxCell>
<mxCell id="pv_btn_right" value="" style="rounded=1;fillColor=#4DA8DA;strokeColor=#0078D4;strokeWidth=1;arcSize=30;" vertex="1" parent="1">
  <mxGeometry x="118" y="50" width="16" height="16" as="geometry" />
</mxCell>
<!-- LDS 激光雷达塔 -->
<mxCell id="pv_lds_ring" value="" style="ellipse;fillColor=#005A9E;strokeColor=#003D6B;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="78" y="78" width="52" height="52" as="geometry" />
</mxCell>
<mxCell id="pv_lds" value="LDS" style="ellipse;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=1;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="84" y="84" width="40" height="40" as="geometry" />
</mxCell>
<!-- 回充键 -->
<mxCell id="pv_btn_home" value="⌂" style="ellipse;fillColor=#4DA8DA;strokeColor=#0078D4;strokeWidth=1;fontColor=#FFFFFF;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="88" y="126" width="24" height="24" as="geometry" />
</mxCell>
```

**使用方式：**
1. 将整段 XML 用作 draw.io 可编辑资产或 SVG 直绘的布局结构参考：全部 `pv_` 元素合并进同一分组（draw.io 中 Group，SVG 中同一 `<g>`），便于整体移动/缩放
2. 缩放时使用同一 scale 系数等比变换，保持圆形比例

## 使用技巧

1. **组合相关元素** — 多部件机器人图标完成后，把所有元素合并进同一分组（draw.io 中 Ctrl+G，SVG 中同一 `<g>`），便于整体移动
2. **保持比例** — 等比缩放（draw.io 中按住 Shift，SVG 用同一 scale 系数），保持圆形机身比例
3. **颜色一致性** — 色值一律取自 color-schemes.md 登记的调色板
4. **图层顺序** — 先画机器人本体，再叠加激光雷达、按键与状态图标
5. **信号波纹** — 用多个虚线椭圆按递减不透明度叠加，表现信号扩散
6. **边刷** — 用 spiral 形状配橙色描边（#FF6B35）增强真实感
7. **产品插画风格属限定例外** — 图标 #9 是插画资产而非流程图节点：design-system.md §5 的节点样式（白色填充、arcSize 6–8，圆角上限见 §4）只约束流程图节点；插画子形状可用符合形态的填充/arcSize（如银色机身、arcSize=30/50 按键）；shadow=0（阴影禁令见 §4），颜色仍全部来自 color-schemes.md 调色板
8. **交付前调色板校验** — 核对引用图标块中的每个 fillColor/strokeColor 均已在 color-schemes.md 登记

## PNG 图像资产

### 10. 扫地机器人图标（PNG）

**文件路径：** `assets/robot-vacuum-icon.png`

**描述：** 扫地机器人俯视图标，包含圆形机身、顶部激光雷达模块、两侧边刷、中间控制按钮

**使用方式（base64 内嵌）：**
```xml
<mxCell id="robot_png_local" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry" />
</mxCell>
```

**注意事项：**
- 使用时将 `assets/robot-vacuum-icon.png` 转为 base64 编码嵌入 XML
- 调整 `width` 和 `height` 保持等比例缩放
- 可通过 `rotation` 属性旋转图标（如 `rotation=45`）
