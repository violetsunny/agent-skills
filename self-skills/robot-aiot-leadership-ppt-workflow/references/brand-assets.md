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

## 品牌资产获取协议

触发条件：PPT 内容点名了美的之外的具体品牌/产品（客户案例、对比对象、生态伙伴、具体产品线）时，必须在 Phase 4 页面生成前执行本协议获取品牌资产。内置 `assets/midea-logo.png` 仅覆盖美的自身 Logo，其摆放尺寸、引用方式与配色协调见上文「品牌 Logo」「使用规则」「HTML 引用方式」「配色协调」，此处不重复。

核心原则：资产 > 规范。品牌识别度的根基是 logo，其次是产品图/UI 截图，色值与字体只是辅助。翻译成执行规则：

- 对比页/案例页点名的品牌必须取到真实 logo，不得用文字名称或手绘图形代替
- 只抽色值、不取 logo，即违反本协议
- 资产取不到时按「三级兜底」处理，禁止静默硬做

### 5 步获取流程

**Step 1 · 问（资产清单一次问全）**
- 输入：任务中点名的品牌/产品清单
- 动作：按清单逐项问用户，不要只问"有没有 brand guidelines"：1) Logo（SVG/高清 PNG）；2) 产品图/官方渲染图；3) UI 截图（数字产品）；4) 色值清单（HEX/品牌色盘）；5) 字体清单（Display/Body）；6) 品牌规范 PDF 或官网链接。有的直接发过来，没有的征得同意后转 Step 2 自取
- 产出：用户提供的资产文件，或"自行获取"授权

**Step 2 · 搜官方渠道**
- 输入：Step 1 确认的品牌清单与缺口项
- 动作：按资产类型搜索——Logo：`<brand>.com/brand`、`/press`、`/press-kit`、官网 header 的 inline SVG；产品图：产品详情页 hero image、press kit 附图、官方发布视频截帧；UI 截图：应用商店产品页截图、官网 screenshots 区、官方演示视频；色值：官网 CSS、品牌规范文件；字体：官网样式表引用、品牌规范文件
- 产出：候选资产 URL 清单（进入 Step 3 下载）

**Step 3 · 下载（落盘 `doc-ppt/assets/<brand>/`）**
- 输入：候选 URL 清单
- 动作：三渠道按命中率递减依次尝试（图标聚合源 → 官网 HTML 提取 inline SVG → 站点图标兜底），用自带脚本执行，脚本内置 unset 代理、落盘 `doc-ppt/assets/<brand>/` 与真实文件核对（HTML 空壳/几百字节占位报 WARN）：

```bash
SKILL=<本skill根目录>/scripts
bash "$SKILL/fetch_brand_assets.sh" midea 0072CE   # 参数：品牌小写名 主色HEX（不带#，可省） [资产根目录，默认 doc-ppt/assets]
```

  官网多为单页应用，直连静态路径常返回空壳，数字产品/AI 工具优先走图标聚合源；官方 brand/press 页的独立 SVG/PNG 直连文件，用 `curl -A "Mozilla/5.0" -L -o <目标路径> <Step 2 找到的直连 URL>` 下载
- 产出：`doc-ppt/assets/<brand>/` 下已核对的资产文件

**Step 4 · 验证 + 提取**
- 输入：已下载的资产文件
- 动作：Logo 确认可打开、透明背景、尽量含深底/浅底两版；产品图分辨率 ≥2000px、背景干净；UI 截图为最新版本、无用户数据污染。色值批量提取并过滤黑白灰：

```bash
brand=midea
grep -hoE '#[0-9A-Fa-f]{6}' "doc-ppt/assets/$brand"/*.svg "doc-ppt/assets/$brand"/*.html 2>/dev/null | sort | uniq -c | sort -rn | head -20
```

  警惕示范品牌污染：产品截图里演示的其他品牌色不是目标品牌的色，同时出现两种强色必须区分。品牌官网营销色与产品 UI 色可能不同，两套都是真的，按汇报场景选用
- 产出：可用资产清单 + 提取出的色值/字体（进入 Step 5）

**Step 5 · 固化为 brand-spec**
- 输入：Step 4 的资产清单与提取结果
- 动作：写入 `doc-ppt/brand-spec.md`（模板见下文「brand-spec 固化」），供全 PPT 页面复用
- 产出：`doc-ppt/brand-spec.md`

### 三级兜底

拿不到品牌资产时按以下顺序降级，禁止跳级、禁止静默：

1. **向用户索取**：说明缺哪类资产、已尝试过哪些渠道，请用户提供或确认放弃
2. **项目既有资产盘点**：检查 `doc-ppt/assets/` 与项目资源目录中已有素材，存在可用素材时向用户确认选配，不得静默忽略（与 SKILL.md Phase 4 阻塞性要求第 5 条一致）
3. **通用占位并显式标注**：灰块 + 文字标签（如"产品图待补"），登记进 brand-spec 缺口清单，交付时向用户可见

### 5-10-2-8 门槛

除 logo 外素材（产品图/UI 截图/参考图/配图）的质量门槛：

| 维度 | 标准 | 反模式 |
|---|---|---|
| 5 轮搜索 | 多渠道交叉搜（官网/press kit/官方社媒/视频截帧/公共素材库/用户账号截屏） | 第一页结果抓前 2 个就停 |
| 10 个候选 | 至少凑 10 个备选才开始筛 | 只抓 2 个，没得选 |
| 选 2 个好的 | 从候选中精选 2 个作为最终素材 | 全都用，视觉过载 |
| 每个 ≥8/10 分 | 不够 8 分宁可不用，改走诚实占位 | 凑数 7 分素材进 brand-spec |

8/10 评分维度（打分记录进 brand-spec）：分辨率（≥2000px）、版权清晰度（官方来源 > 公共领域 > 免费素材，疑似盗图直接 0 分）、与品牌气质关键词契合度、多素材并排的风格一致性、独立叙事能力。

Logo 例外：有就必须用，不适用 5-10-2-8；没有就停下问用户。6 分的 logo 也比没有 logo 强。

### brand-spec 固化

获取到的资产统一写入 `doc-ppt/brand-spec.md`，作为全 PPT 页面品牌资产的唯一真源。成品骨架见 `templates/brand-spec.md`，复制到 `doc-ppt/brand-spec.md` 后逐字段填充，不得凭记忆转抄或删减字段。

执行纪律：

1. 页面 HTML 必须引用 brand-spec 登记的真实文件路径，不得用手绘图形或通用渐变代替
2. 色值/字体从 brand-spec 注入 CSS 变量（`:root { --brand-primary: ...; }`），页面只用 `var(--brand-*)`；想临时加色，先改 brand-spec
3. 与 Phase 4 前复制资产约定的关系：内置美的 Logo 仍按上文「HTML 引用方式」在 Phase 4 前复制；本协议获取的资产已直接落盘 `doc-ppt/assets/`，无需二次复制

### 失败兜底表

| 失败场景 | 兜底动作 | 是否阻塞 |
|---|---|---|
| Logo 完全找不到（全渠道失败） | 停下问用户，不得用文字或手绘图形代替 logo | 阻塞：涉及页面不得进入 Phase 4 |
| 产品图/场景图找不到 | 以官方参考图为基底 AI 生成（规则见 `references/ppt-image-and-cover.md`）→ 向用户索取 → 灰块占位并标注"产品图待补" | 不阻塞，登记缺口清单 |
| UI 截图找不到 | 向用户索取其账号截屏 → 官方演示视频截帧；不用 mockup 凑数 | 不阻塞，登记缺口清单 |
| 色值完全找不到 | 从 logo SVG/官网 CSS 提取 → 向用户推荐 3 个配色方向并标注为假设 | 不阻塞 |
| 资产疑似版权侵权 | 弃用该资产，换官方或公共领域渠道重取 | 不阻塞，换源重取 |
| 全部渠道失败 | 走三级兜底第 3 级：通用占位并显式标注，交付时说明资产缺口 | 不阻塞，但必须向用户可见 |
