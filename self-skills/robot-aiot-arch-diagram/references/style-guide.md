# Style Guide（风格指南）

**颜色、排版与 token 的单一真源。** 每张图都从这里取色——而不是从其他 reference 文件里内联的 hex 值。想换这套设计系统的视觉皮肤，改这个文件。

默认皮肤是冷调编辑色板——white-smoke 纸面、jet-black 墨色、atomic-tangerine accent、blue-slate muted。开箱即用；替换这些值（或跑 [`onboarding.md`](onboarding.md) 流程），之后每张新图自动继承新皮肤，无需触碰任何类型专属逻辑。

想从网站 URL 生成自己的皮肤，见 [`onboarding.md`](onboarding.md)。

---

## Tokens

### 语义角色

每个 token 都以**语义角色**被引用，不以 hex 值引用。类型 reference（`type-*.md`）与 design-system.md 写 `accent`，不写 `#f7591f`。

| Role | Purpose | Default (light) | Default (dark) |
|---|---|---|---|
| `paper` | 页面背景、默认节点填充 | `#f5f5f5` (white-smoke) | `#2d3142` (jet-black) |
| `paper-2` | 图表容器背景、次级填充 | `#ececec` | `#393e53` |
| `ink` | 主文本、主 stroke | `#2d3142` (jet-black) | `#f5f5f5` (white-smoke) |
| `muted` | 次级文本、默认箭头 stroke | `#4f5d75` (blue-slate) | `#bfc0c0` (silver) |
| `soft` | 子标签、边界标签 | `#7a8399` | `#8e98ac` |
| `rule` | 发丝线边框 | `rgba(45,49,66,0.12)` | `rgba(245,245,245,0.12)` |
| `rule-solid` | 更重的边框、基线 | `#bfc0c0` (silver) | `rgba(191,192,192,0.25)` |
| `accent` | 焦点 / 每图至多 1–2 处 | `#eb6c36` (atomic-tangerine) | `#f08a59` |
| `accent-tint` | accent 描边盒的填充 | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.10)` |
| `link` | HTTP/API 调用、外部箭头 | `#2e5aa8` | `#6a95d8` |

> **品牌色板来源：** 本皮肤映射到一个五色品牌色板——`jet-black #2d3142`、`silver #bfc0c0`、`white-smoke #f5f5f5`、`atomic-tangerine #eb6c36`、`blue-slate #4f5d75`。`soft`、`rule`、`link` 三个 token 是派生值（更亮的 slate、ink 加透明度、blue-slate 色相族的饱和变体），用于覆盖品牌色板没有直接命名的角色。

### 反转规则（light → dark）

light 中任何 `rgba(28,25,23, X)` 在 dark 中变为 `rgba(250,247,242, X)`。透明度不变，RGB 翻转。accent 轻微色相偏移调亮，保证在深色纸面上可读。

### Series 色板（仅多序列图表类型）

一小组低饱和编辑色调颜色，供确实需要区分多个重叠实体的图表类型使用（当前：**radar**）。"1 焦点"规则依然成立——`accent` 留给焦点序列；下面的色板覆盖其余序列。

| Token | Light | Dark | Notes |
|---|---|---|---|
| `series-1` | `#7c8f6f` (sage) | `#9caf8f` | 非焦点序列 |
| `series-2` | `#5e7a9b` (dusty-blue) | `#82a0c0` | 非焦点序列 |
| `series-3` | `#b8915a` (mustard) | `#d3ad7a` | 非焦点序列 |
| `series-4` | `#9c6b50` (rust-brown) | `#b88670` | 非焦点序列 |
| `series-5` | `#6e6479` (slate) | `#8d8298` | 非焦点序列 |

填充在 light 下取 `0.18` 透明度、dark 下 `0.22`；stroke 用全色。**不要把这些 token 回填到非图表类型**——架构图、泳道图等继续使用 muted-ink 变体。series 色板是重叠形状需要可区分颜色的图的 opt-in，不是给别处加色的许可。

### Terminal 皮肤（opt-in 备选）

terminal-window 基元（见 [primitive-terminal.md](primitive-terminal.md)）的自包含色板——面向开发工具文章与技术社交卡片的 CLI 外观语域。它不替代上面的默认皮肤，也不受 onboarding 影响；它是按图 opt-in 的第二套固定皮肤。

| Token | Hex | Purpose |
|---|---|---|
| `terminal-page` | `#0a0a0a` | 窗口后面的页面背景 |
| `terminal-paper` | `#141414` | 窗口主体、节点填充 |
| `terminal-bar` | `#1b1b1b` | 标题栏条 |
| `terminal-border` | `#2b2b2b` | 窗口边框、发丝线 |
| `terminal-ink` | `#f5f5f5` | 主文本、主 stroke（与默认 `ink` 同 white-smoke） |
| `terminal-muted` | `#9a9a9a` | 次级文本、子标签、ring stroke |
| `terminal-soft` | `#5c5c5c` | 三级——非活动圆点、spoke |
| `terminal-accent` | `#ff5a36` | 唯一 accent——焦点站点、prompt 符号、活动圆点 |
| `terminal-accent-tint` | `rgba(255,90,54,0.12)` | accent 描边盒的填充 |

**1-accent 规则依然成立。** 凡不是 `terminal-ink` 或 `terminal-muted`/`terminal-soft` 的都应是 `terminal-accent`——绝不引入第二个色相。

---

## 排版

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | Instrument Serif | 1.75rem | 400 | 页面 H1 |
| `node-name` | Geist (sans) | 12px | 600 | 人类可读标签 |
| `sublabel` | Geist Mono | 9px | 400 | 端口、协议、URL、字段类型 |
| `eyebrow` | Geist Mono | 7–8px | 500, tracked 0.18em, uppercase | 类型标签、轴标签 |
| `arrow-label` | Geist Mono | 8px | 400, tracked 0.06em | 箭头注释 |
| `callout` | Instrument Serif *italic* | 14px | 400 | 仅编辑旁注 |

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@400&display=swap" rel="stylesheet">
```

**场景裁决**：`assets/` 模板默认零外链、内置系统字体栈。上方 link 仅联网发布场景手动加入；零外部请求交付物（离线演示、调用方工作流产物）禁止外链，SVG 内品牌字体名自动回退系统字体。裁决细则见 [design-system.md §5](design-system.md)。

### 韩文标签

Geist 与 Instrument Serif 不含 Hangul。韩文 `<text>` 元素扩展自己的 family——绝不换皮肤：

```svg
<text font-family="'Geist', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif">결제 서비스</text>
```

两个 Noto 字体都在上方 font link 中，因此联网发布场景下 web font 先于本地安装字体解析，同一文件在 macOS、Windows 与评审者浏览器中渲染一致。本地 family 排在其后供离线查看。页面标题需要 serif 等价物——`'Instrument Serif', 'Noto Serif KR', serif`——否则拉丁/韩文混排标题的 Hangul 会经平台通用 serif 解析，两半风格打架。Google 的 `css2` endpoint 按 unicode-range 切分韩文，只有几个韩文标签的图仅下载触及的切片。模板出厂零外链（系统字体栈）；为可能含 Hangul 的联网图手动加 link 时，两个 Noto 字体都要带上——纯拉丁图可以保留更短的 link，因为没有 Hangul 的文件无可解析。零外链交付物中，Hangul 经平台本地字体解析（family 列表中的 `'Apple SD Gothic Neo'`/`'Malgun Gothic'` 覆盖 macOS/Windows）。

**宽度预算。** 按字符计量，不按文字系统计量：**每个 Unicode wide 或 full-width 字符计 1em，其余每个字符计其字面的 Latin advance**（sans 0.60em、mono 0.62em），非间距/包围记号不计。对字符串求和后乘字号得文本宽度，再加 padding 并把盒宽向上取整到 4 的倍数。`verify-treemap.py` 对 treemap 单元标签强制执行的就是这个文本宽度；padding 与取整是书写约定，其他类型没有自动检查，预算靠你自己守住。

按文字系统计数是陷阱。`주문 v2.1` 是两个全宽音节加五个窄字符；一个只统计 Hangul、拉丁字母和空格的公式会静默丢掉 `2`、`.`、`1`，按七个字符中的四个定盒宽。每个渲染出来的字符都有成本——按字符计量，永不按文字系统计量。

由 Hangul 度量得出三条规则：

- **子标签保持拉丁。** 端口、协议、字段类型、URL 本来就是拉丁——保留 `Geist Mono`，不要翻译。9px mono 子标签里的 Hangul 不可读，且没有 mono 字面可回退。
- **12px 下限。** Hangul 低于 12px 会糊。韩文名称在 12px 放不下就删减名称——不要缩字号。
- **箭头标签、eyebrow、图例文本换语域。** 这些槽位是 7–8px Geist Mono、大写加 tracking，Hangul 既无字面也无可读性。这些槽位中的韩文标签改为 12px sans、weight 500、无 tracking、无大写变换，遮罩矩形随之放大（高 16px，宽按上面的预算，仍取整到 4 的倍数）。同一张图中的拉丁标签保持 mono 处理。

**承重规则：** Mono 只用于*技术*内容（端口、命令、URL、字段类型）。名称用 Geist sans。页面标题用 Instrument Serif。斜体 Instrument Serif 保留给注释 callout（见 [primitive-annotation.md](primitive-annotation.md)）。**绝不用 JetBrains Mono** 当整体"开发感"字体。

### 繁体中文标签

Geist 与 Instrument Serif 不含汉字。繁中 `<text>` 元素扩展自己的 family——绝不换皮肤：

```svg
<text font-family="'Geist', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif">請求項比對</text>
```

汉字不加载外部 web font——字体栈经本地安装字面解析：有 `Noto Sans TC` 用之，macOS 上 `PingFang TC`，Windows 上 `Microsoft JhengHei`。页面标题需要 serif 等价物——`'Instrument Serif', 'Noto Serif TC', serif`——否则拉丁/汉字混排标题的汉字会经平台通用 serif 解析，两半风格打架。

**宽度预算。** 上面的按字符契约不变：每个 Unicode wide 或 full-width 字符计 1em，其余每个字符计其字面的 Latin advance，非间距记号不计。全角标点——`（）「」，。：`——是 wide，同样计 1em，这是最常被漏掉的部分。

按文字系统计数是陷阱。`請求項 v2.1` 是三个全宽字符加五个窄字符；一个只统计汉字和拉丁字母的公式会静默丢掉 `2`、`.`、`1`，按九个字符中的六个定盒宽。

由汉字度量得出三条规则，与 Hangul 的镜像：

- **子标签保持拉丁。** 端口、协议、字段类型、URL 本来就是拉丁——保留 `Geist Mono`，不要翻译。9px mono 子标签里的汉字不可读，且没有 mono 字面可回退。散文式（而非值式）的子标签可以用中文，但随即按下面第三条换语域。
- **12px 下限。** 同等 em 框内汉字笔画比 Hangul 更密，12px 下限在这里至少同样硬。中文名称在 12px 放不下就删减名称——不要缩字号。
- **箭头标签、eyebrow、图例文本换语域。** 这些槽位是 7–8px Geist Mono、大写加 tracking，汉字既无字面也无可读性。这些槽位中的中文标签改为 12px sans、weight 500、无 tracking、无大写变换，遮罩矩形随之放大（高 16px，宽按上面的预算，仍取整到 4 的倍数）。同一张图中的拉丁标签保持 mono 处理。

简体中文套用同样三条规则，用简中字体栈（`'Noto Sans SC'`、`'PingFang SC'`、`'Microsoft YaHei'`），同样经查看者本地字体解析。

---

## Stroke、圆角、间距

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | `0.8` | 标签盒轮廓、叶节点 |
| `stroke-default` | `1` | 多数 stroke |
| `stroke-strong` | `1.2` | 强调 stroke |
| `radius-sm` | `4` | 小标签 |
| `radius-md` | `6` | 节点盒 |
| `radius-lg` | `8` | 容器、ring |
| `grid` | `4` | 每个坐标、尺寸、间距都被 4 整除（硬规则） |

---

## 节点类型 → 处理方式

语义角色组合——类型规格中按名称引用。

| Type | Fill | Stroke |
|---|---|---|
| `focal`（至多 1–2） | `accent-tint` | `accent` |
| `backend` | `#ffffff` (white) | `ink` |
| `store` | `ink @ 0.05` | `muted` |
| `external` | `ink @ 0.03` | `ink @ 0.30` |
| `input` | `muted @ 0.10` | `soft` |
| `optional` | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` |
| `security` | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

---

## 定制皮肤

四个选项：

1. **跑 onboarding** —— 见 [`onboarding.md`](onboarding.md)。给一个 URL；skill 提取色板 + 字体并重写本文件。
2. **手工编辑** —— 改上表中的 hex 值。改完跑一遍输出前品味门，验证 accent 在新纸色上仍然读作"焦点"。
3. **品牌交接** —— 把现成的 design-token JSON 贴进这里的新章节，并把其 token 映射到上面的语义角色。
4. **客户档案** —— 用 [`profiles.md`](profiles.md) 保存与切换命名皮肤，或把皮肤绑定到项目。

### 约束（不可破坏）

- **对比度**：`ink` 在 `paper` 上必须达 WCAG AA。`muted` 在 `paper` 上对 11px+ 文本必须达 AA。
- **单 accent**：`accent` 只选一个颜色。两个 accent 会抹掉焦点信号。
- **禁彩虹色板**：品牌给了 8 个颜色就选 3 个（paper、ink、accent），其余做 `muted` 变体。
- **Serif + sans + mono**：三个 family，不能更多。品牌排版全是 sans 也照样保留 Instrument Serif 做 `title` 和 `callout`——这个对比是承重的。
- **Paper 是暖中性，不是纯白**：纯白让设计失去血色。选带一点暖意的 cream、bone 或浅灰。
- **点阵图案是可选不是默认**：22×22 dot pattern 是 opt-in 的"点纸"变体（适合长文编辑 hero 图）。默认背景是干净的 `paper` 填充，无图案。启用时它以 `ink` 在 `paper` 上约 10% 透明度呈现——可见但安静。
- **容器默认干净**：图表直接坐在页面纸面上，无二级容器背景或边框。带框变体（`paper-2` 底 + `rule` 边框 + 8px 圆角 + padding）是卡片密集布局的 opt-in，不要默认伸手去拿——多余的外壳与图形打架。
