# 输出规格 — format × size × detail × audience

四个刻度决定一张导入/重绘图表最终成为什么。适用于所有来源路径：draw.io 导入、Mermaid 导入、以及从文字描述直接生成。在重绘**之前**设定它们——它们改变交付物、布局、字号梯度、节点数量与措辞，事后补设意味着重画。

| 刻度 | 回答的问题 | 默认值 |
|---|---|---|
| **Format** | 这个文件落在哪里？ | `html` |
| **Size** | 画布多大，读者距离多远？ | `doc-inline` |
| **Detail level** | 复现每个元素，还是压缩？ | `balanced` |
| **Audience** | 措辞要多技术化？ | `mixed` |

请求中已明确的选项直接推断（例如"用于我的演示文稿"意味着 slide 预设）。对仍有实质歧义的选项，问一个简洁的问题。用户不在意时，使用上表默认值并说明用了哪些。

---

## 1. Format

| Format | 交付物 | 保留 | 丢弃 |
|---|---|---|---|
| `html` | 自包含 `.html`（默认） | 页头、图表、摘要卡片、页脚、实时字体 | 无 |
| `svg` | 源码旁的 `.svg` | `<svg>` 节点、矢量文本 | 编辑级外壳；离线工具中字体被替换 |
| `png` | 按 `device_scale_factor` 输出的 `.png` | 浏览器渲染的精确像素 | 矢量可编辑性 |
| `html+png` | 两者 | — | — |

始终先生成 HTML——`svg` 与 `png` 由它经 [`export.md`](export.md) 产出。绝不在文本编辑器里手写 SVG 文件：SKILL.md 路径 B 的 SVG 由生成脚本逐行输出，导出格式的 SVG/PNG 由 HTML 经 export.md 产出。HTML 外壳是唯一事实源，也是品味门（design-system.md §9）唯一针对的产物。

按目标场景选择：

| 目标场景 | Format | Size 预设 |
|---|---|---|
| 博客文章、README、文档站 | `html`（嵌入）或 `png` | `doc-inline` |
| Keynote / PowerPoint / Google Slides | `png` @2 | `slide-16x9` |
| Figma / Illustrator / 继续编辑 | `svg` | `fit` |
| X / LinkedIn / OG 链接卡片 | `png` @2 | `social-og` |
| 打印讲义、PDF 文稿 | `png` @3 | `print-a4-landscape` |
| Confluence / Notion / 内部 wiki | `png` @2 | `doc-wide` |

---

## 2. Size

预设决定 SVG `viewBox`。下表每个值都能被 4 整除，design-system.md §7 的网格规则依然成立。

| 预设 | viewBox | 宽高比 | PNG @2 | 字号梯度 | 用途 |
|---|---|---|---|---|---|
| `doc-inline`（默认） | `0 0 960 600` | 8:5 | 1920×1200 | standard | 文章或 README 的正文宽度图 |
| `doc-wide` | `0 0 1280 720` | 16:9 | 2560×1440 | standard | 全宽文档、wiki 页 |
| `slide-16x9` | `0 0 1280 720` | 16:9 | 2560×1440 | presentation | 演示文稿幻灯片、投影 |
| `slide-4x3` | `0 0 1024 768` | 4:3 | 2048×1536 | presentation | 旧版文稿模板 |
| `social-og` | `0 0 1200 632` | ~1.9:1 | 2400×1264 | presentation | 链接预览卡片 |
| `social-square` | `0 0 1080 1080` | 1:1 | 2160×2160 | presentation | 信息流帖子、轮播 |
| `print-a4-landscape` | `0 0 1120 792` | ~1.41:1 | @3 → 3360×2376 | print | A4 横向，96dpi 下约 10mm 页边距 |
| `print-letter-landscape` | `0 0 1056 816` | ~1.29:1 | @3 → 3168×2448 | print | US Letter 横向 |
| `fit` | 由内容推导 | 任意 | @2 | standard | 矢量交接；无固定画框 |

### 推导 `fit`

将内容包围盒**向上**取整到 4 的倍数，再加固定装饰区：四边各 40px 外边距，底部另加 60px 图例条。绝不让内容触碰 viewBox 边缘。

### 各尺寸类的字号梯度

画布变大时节点名相对缩小——要抵抗这一点。字号梯度随预设缩放，让投影幻灯片在最后一排也可读。

| 角色 | standard | presentation | print |
|---|---|---|---|
| 标题（Instrument Serif） | 28 | 40 | 32 |
| 节点名（Geist 600） | 12 | 16 | 12 |
| 副标签（Geist Mono） | 9 | 12 | 9 |
| 箭头标签（Geist Mono） | 8 | 12 | 8 |
| 眉标 / tag（Geist Mono） | 8 | 8 | 8 |
| 节点盒最小高度 | 48 | 64 | 48 |
| 节点最小间距 | 24 | 40 | 24 |

presentation 梯度意味着更少节点——64px 盒子里的 16px 名称会吃掉画布。`slide-16x9` 布局放不下时，是 size 刻度在告诉你 detail 刻度过高；降一级细节，而不是缩小字号。

### 安全区

- **所有预设：** 40px 外边距；图例条占底部 60px，其他内容不得进入。
- **`social-og`：** 四边外侧 64px 保持干净——各平台链接卡片裁切不可预测。
- **`slide-*`：** 文稿模板有页脚条时底部 80px 保持干净；不确定就问。

---

## 3. Detail level

源码有多少能存活。这是一个*数量*刻度——管多少元素通过，不管它们如何措辞（那是 §4）。

| 级别 | 节点 | 边 | 副标签 | 存活内容 |
|---|---|---|---|---|
| `faithful`（详细） | ≤24，必须分区 | ≤32 | 每个端口、协议、版本 | 源码中每个独立组件。仅完全重复项合并。 |
| `balanced`（默认） | ≤12 | ≤16 | ≤4 个节点带技术副标签 | 承载故事的组件；叶子簇各折叠为一个节点。 |
| `simplified`（简略） | ≤7 | ≤9 | 无 | 能力及其顺序。基础设施消失。 |

`balanced` 与 `simplified` 处于标准复杂度预算内（design-system.md §7）。**`faithful` 刻意超出预算**——这是交换，且附带条件：

1. **分区强制。** 超过 9 个节点时，每个节点必须属于一个带标签的区域（2–4 个区、发丝线边框、`paper-2` 填充、左上角 mono 大写区域标签）。20 节点不分区是接线图，不是示意图。
2. **连线规则不放松。** design-system.md §6 规则 1–5 在 24 节点时依然适用。无法在不重叠的情况下布线，就是超过了真实上限——拆图。
3. **超过 24 节点，拆分。** 产出一张总览（区域作为节点，`balanced` 语法）加每区一张细节图。命名 `<base>-overview.html`、`<base>-<zone>.html`。绝不交付 40 节点单画布。
4. **强调色保持 2 个。** 节点再多也不多给焦点元素。

### 降级阶梯

源码超出级别允许时，按此顺序删减，一旦低于预算立即停止。绝不随意删减。

1. **装饰性单元** — 便签、游离文本、标题块、水印、源码自带的图例。（值得保留的 note 变为标注 callout——最多 2 个，见 [primitive-annotation.md](primitive-annotation.md)。）
2. **完全重复项** — N 个相同 worker/副本/分片变为一个节点，标签 `Worker ×N`。
3. **叶子簇** — 子元素全为叶子的容器折叠为容器本身：`Core Services` 替代它的三个盒子。提取器在 *collapsible groups* 下列出这些。
4. **不改变故事的 1 度汇点** — 监控挂载、日志桶、归档层。
5. **横切基础设施** — 日志、指标、密钥、CI。`simplified` 下直接删除不必询问；`balanced` 下最多保留一个，且仅当图表主题与它相关。
6. **仍超？** 拆成总览 + 细节。拆分优于缩小。

步骤 2–6 删除的内容都进保真台账（§5）。步骤 1 无需报告。

---

## 4. Audience level

独立于 detail 刻度：同样 12 个节点，面向平台团队和面向指导委员会的命名不同。detail 决定*多少个*；audience 决定*叫什么*。

| Audience | 节点名 | 副标签 | 边标签 | 绝不 |
|---|---|---|---|---|
| `engineer` | 精确服务/组件名 | 协议、端口、版本、镜像 tag | `POST /v2/orders`、`SQL`、`gRPC` | "connects to" 之类的模糊动词 |
| `mixed`（默认） | 组件名，缩写展开 | 仅在影响决策处标技术 | 平实动词 — `verifies`、`writes`、`notifies` | 端口、版本、内部代号 |
| `executive` | 能力与结果 | 无 | 业务动词 — `approves`、`pays out` | 厂商名、基础设施、协议 |

完整示例——同一节点在三种受众下：

| Audience | 节点名 | 副标签 |
|---|---|---|
| `engineer` | `Auth Service` | `JWT · RS256 · :8443` |
| `mixed` | `Auth Service` | `token check` |
| `executive` | `Sign-in` | — |

两条在所有受众级别都成立的规则：

- **绝不为填槽发明细节。** 源码写 `svc-04` 时，`executive` 输出只在上下文能判断其功能时才写功能——否则询问，不猜业务名。
- **专有名词保留源码词汇。** `executive` 下把 `Kafka` 改名为 `Message Bus` 可以；改成 `Event Grid`（另一个产品）是事实错误。

### 非拉丁标签

Geist 没有 CJK 覆盖。标签含日文、中文或韩文时，在那些 `<text>` 元素上扩展字体族——不要整体换皮肤：

```svg
<text font-family="'Geist', 'Hiragino Sans', 'Noto Sans JP', 'Yu Gothic', sans-serif">認証サービス</text>
<text font-family="'Geist', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif">인증 서비스</text>
<text font-family="'Geist', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif">认证服务</text>
<text font-family="'Geist', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif">認證服務</text>
```

Hiragino/Yu Gothic 栈不含谚文字形，韩文标签必须用韩文栈——不要复用日文栈。Noto Sans KR 随皮肤字体链接分发，因此它领衔该栈、本地字体族跟随；韩文在字体之外所需的字重、下限与标题规则见 [`style-guide.md`](style-guide.md#korean-labels)。日文字体也只覆盖汉字集的子集，且会以日文字形变体渲染简体字，因此中文标签必须用中文栈；简体与繁体因同一原因是两个独立的栈。中文栈通过本地安装字体解析——不为其添加外部 web font；繁体中文在字体之外所需的字重、下限与标题规则见 [`style-guide.md`](style-guide.md#traditional-chinese-labels)。mono 副标签用 `'Geist Mono', 'Noto Sans Mono CJK JP', monospace`（日文）、`'Geist Mono', 'Noto Sans Mono CJK KR', monospace`（韩文）或 `'Geist Mono', 'Noto Sans Mono CJK SC', monospace` / `'Geist Mono', 'Noto Sans Mono CJK TC', monospace`（中文）。宽度预算按**每个全角 CJK 字符 1em**，不是拉丁平均字形上加几个百分点；`verify-treemap.py` 对 Unicode 宽/全角字符采用该保守契约，并将组合记号视为零宽度。CJK 优先 12px 节点名而非 8px 副标签；谚文与汉字低于 12px 会发糊，因此把 12px 当下限而不是 10px。实际宽度仍随回退字体变化，翻译标签后运行相应的几何校验器。

---

## 5. 保真台账

只要输出小于输入——每次 `balanced` 与 `simplified` 运行，以及多数 `faithful` 运行——在文件路径之后、在聊天中报告删了什么。简短且具体：

```
Detail: balanced · 18 source nodes → 9 drawn
Merged:  worker-01..06 → "Ingest Worker ×6"
Collapsed: "Observability" group (Grafana, Loki, Tempo) → one node
Dropped: 2 sticky notes, CI pipeline (cross-cutting)
Kept in full: the request path (Client → Gateway → Orders → Postgres)
```

图表的读者看不到缺了什么。提出请求的人需要看到。

---

## 6. 检查清单

与 design-system.md §9 品味门一同运行。

- [ ] 四个刻度全部设定——明确请求、由目标场景推断，或采用默认并已说明？
- [ ] `viewBox` 与 size 预设完全一致，数值可被 4 整除？
- [ ] 字号梯度匹配尺寸类——幻灯片没有误用 standard 梯度？
- [ ] 40px 外边距遵守（`social-og` 为 64px）？
- [ ] 节点数在 detail 级别上限内？
- [ ] `faithful` 超 9 节点 → 已分区，超 24 → 已拆分？
- [ ] 节点名、副标签、边标签全部处于同一 audience 级别？
- [ ] CJK 标签已给字体回退？
- [ ] 所有删减已报保真台账？
- [ ] 图表 `<svg>` 有 `role="img"`、可解析的 `aria-labelledby`、非空首子元素 `<title>`、非空 `<desc>`、按 diagram/variant 加前缀的 ID？
- [ ] 请求的非 HTML 格式经 [`export.md`](export.md) 或路径 B 生成脚本产出，而非手写？
