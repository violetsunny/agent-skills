# Style Guide（样式指南）

**颜色、字体排印与 token 的唯一真源。** 每张图都从这里取值——而不是从其他 reference 文件里内联的十六进制值。想改这套设计系统的视觉皮肤，就改这个文件。

默认皮肤是一套冷调编辑风配色——white-smoke 纸面、jet-black 墨色、atomic-tangerine 强调色、blue-slate 次级色。开箱即用；替换这些值（或运行 [`onboarding.md`](onboarding.md)）后，每张新图都继承新皮肤，无需触碰任何类型专属逻辑。

想从网站 URL 生成自己的皮肤，见 [`onboarding.md`](onboarding.md)。

---

## Tokens

### Semantic roles（语义角色）

每个 token 都以**语义角色**引用，不以十六进制值引用。类型规范（`type-*.md`）与 design-system.md 写 `accent`，不写 `#f7591f`。

| Role | Purpose | Default (light) | Default (dark) |
|---|---|---|---|
| `paper` | Page background, default node fill | `#f5f5f5` (white-smoke) | `#2d3142` (jet-black) |
| `paper-2` | Diagram container bg, secondary fill | `#ececec` | `#393e53` |
| `ink` | Primary text, primary stroke | `#2d3142` (jet-black) | `#f5f5f5` (white-smoke) |
| `muted` | Secondary text, default arrow stroke | `#4f5d75` (blue-slate) | `#bfc0c0` (silver) |
| `soft` | Sublabels, boundary labels | `#7a8399` | `#8e98ac` |
| `rule` | Hairline borders | `rgba(45,49,66,0.12)` | `rgba(245,245,245,0.12)` |
| `rule-solid` | Stronger borders, baselines | `#bfc0c0` (silver) | `rgba(191,192,192,0.25)` |
| `accent` | Focal / 1–2 max per diagram | `#eb6c36` (atomic-tangerine) | `#f08a59` |
| `accent-tint` | Fill for accent-bordered boxes | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.10)` |
| `link` | HTTP/API calls, external arrows | `#2e5aa8` | `#6a95d8` |

> **品牌调色板来源：** 本皮肤映射到一个五色品牌调色板——`jet-black #2d3142`、`silver #bfc0c0`、`white-smoke #f5f5f5`、`atomic-tangerine #eb6c36`、`blue-slate #4f5d75`。`soft`、`rule`、`link` 三个 token 是派生值（更浅的 slate、带透明度的 ink、blue-slate 色相族的饱和变体），用于覆盖品牌调色板未直接命名的角色。

### 反色规则（light → dark）

light 中的任何 `rgba(28,25,23, X)` 在 dark 中变为 `rgba(250,247,242, X)`。透明度不变，RGB 翻转。accent 做轻微色相偏移调亮，以便在深色纸面上可读。

### Series palette（仅多系列图表类型）

一小组低饱和编辑风颜色，供确实需要区分多个重叠实体的图表类型使用（当前：**radar**）。"1 焦点"规则依然成立——`accent` 保留给焦点系列；下面的调色板覆盖其余系列。

| Token | Light | Dark | Notes |
|---|---|---|---|
| `series-1` | `#7c8f6f` (sage) | `#9caf8f` | Non-focal series |
| `series-2` | `#5e7a9b` (dusty-blue) | `#82a0c0` | Non-focal series |
| `series-3` | `#b8915a` (mustard) | `#d3ad7a` | Non-focal series |
| `series-4` | `#9c6b50` (rust-brown) | `#b88670` | Non-focal series |
| `series-5` | `#6e6479` (slate) | `#8d8298` | Non-focal series |

填充在 light 下用 `0.18` 透明度、dark 下 `0.22`；描边用全色。**不要把这些 token 回填到非图表类型**——architecture、swimlane 等继续使用 muted-ink 变体。series palette 是重叠形状需要可区分颜色的图表的 opt-in，不是给其他地方加颜色的许可。

### Terminal skin（opt-in 备选皮肤）

terminal-window 基元（见 [primitive-terminal.md](primitive-terminal.md)）的自包含调色板——面向开发工具文章与技术社交卡片的 CLI 窗框风格。它不替代上面的默认皮肤，也不受 onboarding 影响；它是按图 opt-in 的第二套固定皮肤。

| Token | Hex | Purpose |
|---|---|---|
| `terminal-page` | `#0a0a0a` | Page background behind the window |
| `terminal-paper` | `#141414` | Window body, node fill |
| `terminal-bar` | `#1b1b1b` | Titlebar strip |
| `terminal-border` | `#2b2b2b` | Window border, hairlines |
| `terminal-ink` | `#f5f5f5` | Primary text, primary stroke (same white-smoke as default `ink`) |
| `terminal-muted` | `#9a9a9a` | Secondary text, sublabels, ring stroke |
| `terminal-soft` | `#5c5c5c` | Tertiary — inactive dots, spokes |
| `terminal-accent` | `#ff5a36` | The one accent — focal station, prompt sign, active dot |
| `terminal-accent-tint` | `rgba(255,90,54,0.12)` | Fill for accent-bordered boxes |

**1 强调色规则依然成立。** 凡不是 `terminal-ink` 或 `terminal-muted`/`terminal-soft` 的都应是 `terminal-accent`——永不引入第二个色相。

---

## Typography（字体排印）

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | Instrument Serif | 1.75rem | 400 | Page H1 |
| `node-name` | Geist (sans) | 12px | 600 | Human-readable labels |
| `sublabel` | Geist Mono | 9px | 400 | Port, protocol, URL, field type |
| `eyebrow` | Geist Mono | 7–8px | 500, tracked 0.18em, uppercase | Type tags, axis labels |
| `arrow-label` | Geist Mono | 8px | 400, tracked 0.06em | Arrow annotations |
| `callout` | Instrument Serif *italic* | 14px | 400 | Editorial asides only |

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@400&display=swap" rel="stylesheet">
```

### 韩文标签

Geist 与 Instrument Serif 不含谚文（Hangul）。韩文 `<text>` 元素扩展自己的 font-family——永不因此换皮肤：

```svg
<text font-family="'Geist', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif">결제 서비스</text>
```

两款 Noto 字体都在上面的 font link 中，因此 web font 先于任何本地安装字体解析，同一文件在 macOS、Windows 与审阅者浏览器中渲染一致。本地字体族排在其后用于离线查看。页面标题需要对应的衬线栈——`'Instrument Serif', 'Noto Serif KR', serif`——否则拉丁/韩文混排标题的谚文会落到平台通用 serif 上，两半风格不一致。Google 的 `css2` 端点按 unicode-range 切分韩文，含少量韩文标签的图只下载用到的切片。四个模板携带两款字体是因为新图可能含谚文；随包的纯拉丁示例保留较短的 link，因为无谚文的文件没有需要解析的内容。

**宽度预算。** 按字符度量，不按文字系统度量：**每个 Unicode wide/full-width 字符计 1em，其余字符计其字体的拉丁 advance**（sans 0.60em、mono 0.62em），非间距/包围符号计 0。对整串求和后乘以字号得到文本宽度，再加 padding 并把框向上取整到 4 的倍数。`verify-treemap.py` 对 treemap 单元格标签强制执行的就是这个文本宽度；padding 与取整属于写作约定，其他类型没有自动检查，预算靠作者自己守住。

按文字系统计数是陷阱。`주문 v2.1` 是两个全角音节加五个窄字符；按"谚文、拉丁字母、空格"分类 tallies 的公式会静默丢掉 `2`、`.`、`1`，只按七个字符中的四个来定框宽。每个渲染出来的字符都有成本——按字符度量，永不按文字系统度量。

由谚文度量引出三条规则：

- **Sublabel 保持拉丁。** 端口、协议、字段类型、URL 本来就是拉丁——那里继续用 `Geist Mono`，不要翻译。9px mono sublabel 里的谚文不可读，且没有 mono 字体可回退。
- **12px 下限。** 谚文低于 12px 会糊。韩文名称在 12px 放不下就删减名称——不要缩小字号。
- **箭头标签、eyebrow、图例文本换寄存器。** 这些槽位是 7–8px Geist Mono、大写加 tracking，谚文既没有对应字体也没有可读性。这些槽位中的韩文标签改为 12px sans、weight 500、无 tracking、无大写变换，其遮罩 rect 相应增大（高 16px，宽按上面的预算，仍取整到 4 的倍数）。同一张图中的拉丁标签保持 mono 处理。

**承重规则：** Mono 用于*技术*内容（端口、命令、URL、字段类型）。名称用 Geist sans。页面标题用 Instrument Serif。斜体 Instrument Serif 保留给注释 callout（见 [primitive-annotation.md](primitive-annotation.md)）。**永不用 JetBrains Mono** 充当笼统的"开发风"字体。

---

## Stroke、radius、spacing

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | `0.8` | Tag-box outlines, leaf nodes |
| `stroke-default` | `1` | Most strokes |
| `stroke-strong` | `1.2` | Emphasis strokes |
| `radius-sm` | `4` | Small tags |
| `radius-md` | `6` | Node boxes |
| `radius-lg` | `8` | Containers, rings |
| `grid` | `4` | Every coord, size, and gap is divisible by 4 (hard rule) |

---

## 节点类型 → treatment

语义角色组合——在类型规范中按名称引用。

| Type | Fill | Stroke |
|---|---|---|
| `focal` (1–2 max) | `accent-tint` | `accent` |
| `backend` | `#ffffff` (white) | `ink` |
| `store` | `ink @ 0.05` | `muted` |
| `external` | `ink @ 0.03` | `ink @ 0.30` |
| `input` | `muted @ 0.10` | `soft` |
| `optional` | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` |
| `security` | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

---

## 定制皮肤

四个选项：

1. **运行 onboarding** — 见 [`onboarding.md`](onboarding.md)。给一个 URL；skill 提取调色板 + 字体并重写本文件。
2. **手工编辑** — 改上面表格中的十六进制值。改完运行输出前 taste gate，验证 accent 在新纸面色上仍读作"焦点"。
3. **品牌交接** — 把既有 design-token JSON 粘贴到本文件新小节，并将其 token 映射到上面的语义角色。
4. **客户 profile** — 用 [`profiles.md`](profiles.md) 保存/切换具名皮肤，或把某个皮肤绑定到项目。

### 约束（不得破坏）

- **对比度**：`ink` 在 `paper` 上必须达到 WCAG AA。`muted` 在 `paper` 上对 11px+ 文本必须达到 AA。
- **单强调色**：`accent` 只选一个颜色。两个强调色会抹掉焦点信号。
- **禁彩虹调色板**：品牌有 8 个颜色时选 3 个（paper、ink、accent），其余变成 `muted` 变体。
- **Serif + sans + mono**：三个字体族，不能更多。品牌字体全是 sans 时，`title` 与 `callout` 仍保留 Instrument Serif——这个对比是承重的。
- **Paper 是暖中性色，不是纯白**：纯白让设计显得无菌。选带一点暖意的 cream、bone 或浅灰。
- **点阵图案是可选非默认**：22×22 点阵是 opt-in 的"点纸"变体（适合长文编辑风 hero 图）。默认背景是干净的 `paper` 填充，无图案。启用图案时用 `ink` 在 `paper` 上约 10% 透明度——可见但安静。
- **容器默认干净**：图直接坐在页面纸面上，无二级容器背景或边框。带框变体（`paper-2` bg + `rule` border + 8px radius + padding）作为卡片密集布局的 opt-in 提供，但默认不要伸手去拿——多余的窗框与图形争抢注意力。
