# 品牌资源与输出目录

所有交付物统一落在当前项目的 `doc-ppt/` 目录下，不散落到其他路径。

```text
doc-ppt/
├── assets/
│   └── midea-logo.png
├── <chart-name>.xml
├── <chart-name>.html
├── <project>_PPT母稿.md
├── pages/
│   ├── 01-cover.html
│   ├── 02-overview.html
│   └── ...
└── <project>.pptx
```

## 品牌 Logo

本技能内置美的品牌 Logo，路径：`assets/midea-logo.png`。

## 使用规则

1. 封面页：右上角或左上角放置 Logo，建议 `height: 60~80px`
2. 内容页页脚：右下角放置缩略版，建议 `height: 24~32px`
3. 尾页：底部联系信息区域放置 Logo，建议 `height: 48~60px`

## HTML 引用方式

Phase 4 开始前先复制品牌资源：

```bash
mkdir -p doc-ppt/assets
cp <skill-path>/assets/midea-logo.png doc-ppt/assets/midea-logo.png
```

```html
<img src="assets/midea-logo.png"
     style="position:absolute;right:60px;top:60px;height:72px;object-fit:contain;"
     alt="Midea"/>

<img src="assets/midea-logo.png"
     style="position:absolute;right:60px;bottom:24px;height:28px;object-fit:contain;opacity:0.85;"
     alt="Midea"/>
```

## 配色协调

1. Logo 周围优先使用白色或浅色背景
2. 深色背景时补白色圆角底卡片，`padding: 8~12px`，`border-radius: 6~8px`
3. Logo 不得遮挡标题、结论或关键数据区域
