# Gantt Chart（甘特图）

**最适合：** 项目计划与路线图——带明确起止日期的任务，按阶段分组。当读者需要一眼看到时间重叠、并行轨道与里程碑顺序时使用。

## 布局约定

- **左侧标签列：** x=20–200（180px）。任务名 Geist sans 11px 600。阶段标签用 Geist Mono 7px 眉标置于每组上方。
- **时间线区域：** x=200–960（760px）。时间轴左→右。
- **行高：** 每任务 40px。每根条 h=24px 在行内居中（顶部留白 8px）。
- **时间轴：** Geist Mono 8px 周/月标签位于 x=200+i×pitch、y=56（首任务行上方）。y=64 处一条发丝分隔线。
- **阶段分组：** 每个阶段的行后面垫一个淡色 zone 矩形（与 architecture zone 同模式），左上边距处放眉标。填充 `rgba(45,49,66,0.02)`，描边 `rgba(45,49,66,0.10)`。
- **焦点任务条：** 1 根条用 accent 填充/描边（关键交付物或关键路径任务）。其余全部：muted 填充 @ 0.15、muted 描边。
- **今天 / 里程碑标记：** 可选，在当前周 x 位置画 `muted` 垂直虚线。

### 任务条模式

```svg
<!-- 非焦点任务 -->
<rect x="X_start" y="ROW_Y+8" width="DURATION_PX" height="24" rx="4"
      fill="rgba(79,93,117,0.15)" stroke="#4f5d75" stroke-width="1"/>
<text x="X_start+8" y="ROW_Y+25" fill="#2d3142" font-size="10" font-weight="600"
      font-family="'Geist', sans-serif">Task name</text>

<!-- 焦点任务 -->
<rect x="X_start" y="ROW_Y+8" width="DURATION_PX" height="24" rx="4"
      fill="rgba(235,108,54,0.12)" stroke="#eb6c36" stroke-width="1"/>
<text x="X_start+8" y="ROW_Y+25" fill="#eb6c36" font-size="10" font-weight="600"
      font-family="'Geist', sans-serif">Key task</text>
```

时长像素数：`(end_week - start_week) × pitch`。Pitch = timeline_width / total_weeks。

## 反模式

- 超过 12 个任务（拆分为子计划或折叠为阶段级视图）。
- 每阶段超过 5 条并行轨道（重叠不可读）。
- v1 就画任务间依赖箭头（仅在必要时添加；标签用 annotation primitive）。
- 起止日期写进条内标签（放到 x 轴或 tooltip 注释里）。
- 所有条视觉权重相同（焦点任务必须突出）。

## 示例

- minimal light
- minimal dark
- full editorial
