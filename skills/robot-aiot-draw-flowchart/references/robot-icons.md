# Robot Vacuum Icons Reference

## Base Robot Icons

### 1. Simple Top View (简约俯视)
```xml
<mxCell id="robot_simple" value="" style="ellipse;fillColor=#333333;strokeColor=#1A1A1A;strokeWidth=2;shadow=1;" vertex="1" parent="1">
  <mxGeometry width="80" height="80" as="geometry" />
</mxCell>
<mxCell id="robot_lidar" value="" style="ellipse;fillColor=#555555;strokeColor=#444444;strokeWidth=1;" vertex="1" parent="1">
  <mxGeometry x="25" y="5" width="30" height="20" as="geometry" />
</mxCell>
<mxCell id="robot_btn" value="" style="ellipse;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=1;" vertex="1" parent="1">
  <mxGeometry x="32" y="35" width="16" height="16" as="geometry" />
</mxCell>
```

### 2. Top View with Side Brushes (带边刷俯视)
```xml
<mxCell id="robot_body" value="" style="ellipse;fillColor=#444444;strokeColor=#222222;strokeWidth=2;shadow=1;" vertex="1" parent="1">
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

### 3. Side View (侧视图)
```xml
<mxCell id="robot_side_body" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#444444;strokeColor=#222222;strokeWidth=2;arcSize=40;shadow=1;" vertex="1" parent="1">
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

## State-Specific Icons

### 4. Connected/OTA State (联网/OTA状态)
```xml
<mxCell id="robot_connected" value="" style="ellipse;fillColor=#0078D4;strokeColor=#005A9E;strokeWidth=2;shadow=1;" vertex="1" parent="1">
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

### 5. Charging State (充电中)
```xml
<mxCell id="robot_charging" value="" style="ellipse;fillColor=#555555;strokeColor=#333333;strokeWidth=2;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="20" y="25" width="70" height="70" as="geometry" />
</mxCell>
<mxCell id="battery_icon" value="⚡" style="text;html=1;fontSize=24;align=center;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="38" y="40" width="35" height="35" as="geometry" />
</mxCell>
<mxCell id="charging_dock" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#888888;strokeColor=#666666;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="90" y="35" width="15" height="50" as="geometry" />
</mxCell>
```

### 6. Cleaning Active (清扫中)
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
<mxCell id="robot_cleaning" value="" style="ellipse;fillColor=#333333;strokeColor=#1A1A1A;strokeWidth=2;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="30" width="60" height="60" as="geometry" />
</mxCell>
<mxCell id="clean_btn" value="" style="ellipse;fillColor=#00C853;strokeColor=#009624;" vertex="1" parent="1">
  <mxGeometry x="60" y="50" width="14" height="14" as="geometry" />
</mxCell>
<mxCell id="sparkle" value="✨" style="text;html=1;fontSize=14;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="85" y="20" width="25" height="25" as="geometry" />
</mxCell>
```

### 7. Error/Alert State (告警/故障)
```xml
<mxCell id="robot_error" value="" style="ellipse;fillColor=#B85450;strokeColor=#8C2E2E;strokeWidth=2;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="15" y="25" width="70" height="70" as="geometry" />
</mxCell>
<mxCell id="warning_icon" value="⚠️" style="text;html=1;fontSize=22;align=center;fillColor=none;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="32" y="40" width="35" height="35" as="geometry" />
</mxCell>
```

### 8. OTA Upgrade In Progress (OTA升级中)
```xml
<mxCell id="robot_upgrading" value="" style="ellipse;fillColor=#9673A6;strokeColor=#6A4C7D;strokeWidth=2;shadow=1;" vertex="1" parent="1">
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

## Usage Tips

1. **Group related elements** — After creating a robot icon with multiple parts, select all elements and Group them (Ctrl+G) for easy movement
2. **Maintain proportions** — Hold Shift while resizing to keep the circular shape
3. **Color consistency** — Always use the color codes from color-schemes.md
4. **Layer order** — Place the robot body first, then overlay LiDAR, buttons, and icons
5. **Signal waves** — Use multiple dashed ellipses with decreasing opacity for realistic effect
6. **Side brushes** — Use the spiral shape with orange stroke (#FF6B35) for authenticity

## PNG Image Asset

### 9. Robot Vacuum Icon (PNG)

**文件路径：** `assets/robot-vacuum-icon.png`

**描述：** 扫地机器人俯视图标，包含圆形机身、顶部激光雷达模块、两侧边刷、中间控制按钮

**使用方式：**
```xml
<mxCell id="robot_png" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=https://your-oss-url/robot-vacuum-icon.png;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry" />
</mxCell>
```

**本地使用（draw.io桌面版）：**
```xml
<mxCell id="robot_png_local" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry" />
</mxCell>
```

**注意事项：**
- 使用OSS链接时，需要先通过 `midea_oss_tool` 上传 `assets/robot-vacuum-icon.png`
- 本地使用时，需要将PNG转为base64编码嵌入XML
- 调整 `width` 和 `height` 保持等比例缩放
- 可通过 `rotation` 属性旋转图标（如 `rotation=45`）
