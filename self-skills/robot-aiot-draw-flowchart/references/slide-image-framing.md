# 图片上屏原语与图片布局选型

本文件定义位图（截图、照片、AI 配图、导出的图表 PNG）进入 1920x1080 固定画布的上屏规则。
图表 HTML 真源不走本文件，仍按 `slide-page-template.md` 第 6 节 iframe 嵌入约束执行。

## 1. 核心原语：.img-frame 容器

固定画布 + `overflow: hidden` 下，裸 `<img>` 会按原始尺寸撑破版面，属事前可预防的布局事故。规则：

1. **禁止裸 img**：任何位图必须包在 `.img-frame` 容器内，由容器持有尺寸与裁剪，图片只负责填充
2. 容器用 `aspect-ratio` 锁定比例，`<img>` 用 `object-fit` 填充，换任何比例的图都不破坏版式
3. 容器比例用 `--img-ratio` 调节（默认 `16/10`），焦点位置用 `--img-pos`（即 `object-position`）调节

```css
.img-frame {
  position: relative;
  aspect-ratio: var(--img-ratio, 16/10);
  overflow: hidden;
  border-radius: var(--radius-md);
  background: var(--surface-muted);
}
.img-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: var(--img-pos, center);
  display: block;
}
.img-frame.contain img { object-fit: contain; }
```

```html
<figure class="img-frame"><img src="photo.png" alt="场景照片"></figure>
<figure class="img-frame contain" style="--img-ratio:4/3"><img src="dashboard-shot.png" alt="平台截图"></figure>
```

## 2. contain / cover 选型（硬规则）

| 图片内容 | object-fit | 原因 |
|---|---|---|
| 产品截图、系统界面 | `contain`（letterbox） | 裁剪丢失功能信息，边缘控件被切即废图 |
| 图表 PNG、架构图导出图 | `contain` | 裁剪丢失数据与图例 |
| Logo、图标类位图 | `contain` | 裁剪破坏品牌资产 |
| 场景照片、AI 氛围配图 | `cover` | 照片裁掉边缘不损失信息，铺满更高级 |

1. `contain` 留出的 letterbox 空档由容器背景（`--surface-muted`）承接，不用纯白或纯黑
2. 拿不准就 `contain`：宁可留白，不可裁掉事实

## 3. 图片布局选型表

按页面要承载的图片数量与角色选版式：

| 场景 | 版式 | 要点 |
|---|---|---|
| 一张截图/图表 PNG | 单图版式 | `.img-frame.contain` + 图外下方 caption |
| 一张照片要撑起整页 | 全出血版式 | `cover` 铺满 + 渐变 scrim 保证标题可读（见 §4） |
| 一图一论点 | 图文分栏 | 50/50 或 60/40，图在左/右与阅读顺序一致 |
| 3-6 张图 | 网格版式 | 统一 `.img-frame` 比例归一化混合来源比例，每图一行 caption |
| 改造前/后、方案 A/B | 对比版式 | 两侧容器同尺寸同比例，结论分别置于图下方 |

规则：

1. 同一页所有 `.img-frame` 使用同一 `--img-ratio`，混合比例只允许出现在网格版式（由容器归一化）
2. caption 放图外下方，用 `--text-secondary` / `--text-tertiary`，不进画面
3. 图片数量超过 6 张时拆页，不缩格硬塞

## 4. scrim（渐变遮罩）使用边界

1. scrim 仅允许出现在**全出血版式**：图上必须承载标题/结论文字时，在文字侧加单向渐变遮罩保证对比度 ≥ 4.5:1
2. scrim 不是装饰：非全出血版式（单图、分栏、网格、对比）一律不加
3. scrim 与"禁止给图片叠加标签胶囊"条款不冲突——scrim 是可读性保障，胶囊角标是装饰，后者仍禁止
4. 常用实现：`linear-gradient(to top, rgba(10,16,26,.72), rgba(10,16,26,0) 55%)`，深色端朝文字侧

## 5. 交付审查联动

图片上屏问题在 `slide-premium-review.md` 中按以下口径判定：

1. 裸 img、截图/图表被 cover 裁剪 → 阻塞项
2. 同页混用容器比例（网格版式除外）、scrim 用在非全出血页 → 非阻塞项（`[UI-WARN]`）
3. 图片文件与页面 HTML 同目录相对引用，路径可解析
