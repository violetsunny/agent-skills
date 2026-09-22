# Annotation Callout（斜体衬线旁注）

用于编辑风旁注——不与主图语法争抢注意力的"斜体指针"，标记一个细节。类比页边批注：*"structure IS the index"*、*"no imports, no configuration"*。

## 语法

```svg
<!-- 1. Italic Instrument Serif text -->
<text x="904" y="36" fill="#2d3142" font-size="14" font-style="italic"
      font-family="'Instrument Serif', serif" text-anchor="end">no imports, no configuration</text>
<!-- 2. Dashed Bézier leader -->
<path d="M 820 44 Q 700 84 520 216" fill="none"
      stroke="rgba(45,49,66,0.40)" stroke-width="1" stroke-dasharray="4,3"/>
<!-- 3. Landing dot -->
<circle cx="520" cy="216" r="2" fill="#2d3142"/>
```

## 规则
- 斜体 + 衬线共同构成"编辑声音"信号，与图内 sans/mono 主体形成对比。不要换成斜体 sans 或斜体 mono——这个组合是承重的。
- 虚线路径（`stroke-dasharray="4,3"`）把旁注引线与主箭头（实线）区分开。
- 旁注放在页边空白处（右上、左下）。永不放进图形活动区内部。
- 每张图最多 2 个旁注。再多就成了评论，不是信号。

## 颜色

| Intent | Text | Leader |
|---|---|---|
| Neutral aside | ink `#2d3142` | `rgba(45,49,66,0.40)` |
| Focal / accent | coral `#eb6c36` | `rgba(235,108,54,0.50)` |
| Tertiary (muted) | muted `#4f5d75` | `rgba(45,49,66,0.30)` |

## 反模式
- 实线箭头引线（会被读成流程箭头）。
- 斜体 sans 或斜体 mono——衬线是承重的。
- 旁注穿越主箭头/生命线——偏移到干净的页边。
- 用旁注去标注图本身应直接标注的东西——标签应放在元素上。
