# Sketchy Filter（手绘变体）

可选的位移滤镜，让每条描边和边缘轻微抖动——不改布局，把任何极简变体变成手绘"编辑风"寄存器。图伴随随笔（而非技术文档）时使用。

## 语法

```svg
<defs>
  <filter id="sketchy" x="-2%" y="-2%" width="104%" height="104%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/>
    <feDisplacementMap in="SourceGraphic" scale="1.5"/>
  </filter>
</defs>

<!-- Apply to a group wrapping shapes — NOT text -->
<g filter="url(#sketchy)">
  <!-- rects, paths, circles, lines go here -->
</g>

<!-- Text sits OUTSIDE the filtered group — legibility stays crisp -->
<text ...>Labels go here</text>
```

## 调参

| 参数 | 范围 | 效果 |
|---|---|---|
| `baseFrequency` | 0.01–0.04 | 值越低线条越慵懒波浪，越高越抖动。默认 0.02。 |
| `numOctaves` | 1–3 | 值越高噪声细节越多。2 已足够。 |
| `scale` | 1–6 | 1 几乎无感，1.5 默认，2 明显可见，4+ 卡通化。 |
| `seed` | 整数 | 换一个值即得不同的随机图案。 |

## 关键规则
滤镜作用于形状，不作用于文本。经位移映射的文本会不可读。组织 SVG 时让文本位于滤镜组之外的兄弟分组中。

## 何时使用
- 随笔/博客/newsletter，图是叙事页面的主角。
- "工作草图"寄存器——表达某物处于思考中途，不是最终架构。

## 何时不用
- 技术文档（精确性优先）。
- 标签密集或对齐紧凑的图（滤镜会被读成噪点）。
- 深色变体——抖动在深色背景上会被读作渲染瑕疵。先测试。
