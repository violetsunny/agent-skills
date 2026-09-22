# Export to PNG / SVG（HTML 产物导出）

分工声明：本文件管 **HTML 产物导出流程**（从生成的图表 HTML 中提取 `<svg>` 产出 `.svg`/`.png`，含多图 gallery 源的识别）；**SVG→PNG 光栅化**（cairosvg / rsvg-convert / svg2png.js 渲染栈）见 [`png-export.md`](png-export.md)。两文件互指，各管各的。

把生成的图表 HTML 文件转换为同目录下可移植的 `.svg` 和/或 `.png`。**仅限用户明确要求——绝不主动执行。**

## 触发条件

以下情况加载本文件：

- 用户用自然语言要求把图表导出、保存、光栅化、转换或下载为 `.svg` 或 `.png` 形式，并指明源 HTML 文件。典型说法：
  - "export this as PNG"
  - "save as SVG"
  - "give me a PNG of that diagram"
  - "rasterize it"
  - "convert to png and svg"

## 范围

两种格式都**只导出图表本体**——即 `<svg>` 节点。编辑壳（header、summary cards、`-full` 变体的 footer）有意丢弃：导出交付物是图表本身，适用于 Figma、幻灯片、社交卡片或博客配图。

SVG 导出保留源 `<title>` 与 `<desc>`。它们的按图、按变体前缀 ID 是多个导出 SVG 安全内联进同一页面的保障——不会出现一张图解析到另一张图可访问名称的情况。

如果用户明确要"包含卡片的整页截图"，那是另一种需求——回退到用用户操作系统或浏览器做普通整页截图。

## SVG 导出流程

1. 读取源 HTML 文件。
2. 提取**第一个** `<svg ...>...</svg>` 块。用以 `<svg` 和 `</svg>` 锚定的多行正则。多数生成图只有一个 SVG；有多个时第一个是主图（gallery 文件是例外——见*边界情况*）。
3. 使其可独立渲染：
   - 确保开始标签带 `xmlns="http://www.w3.org/2000/svg"`，缺失则补。
   - 确保存在 `viewBox`。本 skill 模板总是包含；缺失时警告用户而不是猜测。
   - 原样保留 `role="img"`、`aria-labelledby` 与首子元素 `<title>` / `<desc>`。
   - **条件注入** Google Fonts `@import`（基准：`design-system.md` §5"模板默认零外链"）：**仅当**产物用于**联网发布场景**（在线文章、允许网络访问的单文件 HTML）且需要品牌 webfont 时注入，使 SVG 在浏览器中排版正确；**零外部请求交付物**（离线演示页、调用方工作流产物、调用方声明零外链）禁止注入，一律系统字体栈。注入时**必须把 `&` 分隔符 XML 转义为 `&amp;`**——独立 `.svg` 按严格 XML 解析，裸 `&` 会启动实体引用并导致整个文件解析失败。（不要从 HTML 的 `<link href>` 复制原始 URL；那种 ampersand 形式只在 HTML 中有效。）
     ```svg
     <defs>
       <style>@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=Geist:wght@400;500;600&amp;family=Geist+Mono:wght@400;500;600&amp;display=swap');</style>
     </defs>
     ```
     如果 SVG 已含 `<defs>` 块，把 `<style>` **合并**进去（不要加第二个 `<defs>`）。
     CJK 标签永不通过 `@import` 扩展额外 webfont 家族——韩文、简中、繁中的 `<text>` 元素自带 `font-family` 栈，经本地安装字体解析（韩文：`'Geist', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif`；繁中：`'Geist', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif`；拉丁/汉字混排标题：`'Instrument Serif', 'Noto Serif TC', serif`）。完整字体栈与度量见 [`style-guide.md`](style-guide.md)。
4. 为严格 SVG 1.1 消费方规范化颜色。本设计系统的 token 以 `rgba(...)` 书写（见 `style-guide.md`），在按 CSS 读取颜色的地方（浏览器、Figma、Illustrator）渲染正确；PowerPoint 的 SVG 导入器不行：它把 `rgba(...)` 与 `transparent` 当作无法识别并涂成**不透明黑**，把若有若无的 tint 变成吞掉内部标签的实心块。该变换无损（每处替换在浏览器中与原始渲染一致），因此对第 2 步提取的 SVG 字符串应用后再写文件：

   ```python
   import re

   svg = re.sub(
       r'(fill|stroke)="rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d*\.?\d+)\s*\)"',
       lambda m: '{0}="#{1:02x}{2:02x}{3:02x}" {0}-opacity="{4}"'.format(
           m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
       ),
       svg,
   )
   svg = re.sub(r'(fill|stroke)="transparent"', r'\1="none"', svg)
   ```

   各通道两侧的 `\s*` 同时容忍带空格的 `rgba(45, 49, 66, 0.03)` 与模板常用的紧凑形式 `rgba(45,49,66,0.03)`；`\d*\.?\d+` 接受带或不带前导零的 alpha（`0.03` 与 `.03` 都在既有 token 中出现过）。匹配范围限定在 `fill="..."` / `stroke="..."` 呈现属性，不是裸 `rgba(` 字符串，因此不会误伤其他内容——模板与示例只在 SVG 元素的这两个属性上表达颜色，从不用 `style="..."` 属性或 `<style>` 块。（`style-guide.md` 中品牌接入的调色板原则上可能引入第三种记法如 `hsl()`；当前没有任何既有 token 使用，故本 pass 不处理——将来引入时扩展正则。）
5. 前置 `<?xml version="1.0" encoding="UTF-8"?>\n`，使文件成为合法 XML。
6. 写入源文件同目录的 `<basename>.svg`（如 `example-architecture.html` → `example-architecture.svg`）。用户给了显式输出路径则遵从。

### 需向用户提示的注意事项

不在导入时拉取远程字体的工具（离线 Illustrator、部分 Figma 导入路径、旧 SVG 查看器）会做字体替换。SVG 在任何现代浏览器中渲染正确。要像素级可移植，推荐 PNG 导出。

## PNG 导出流程

渲染**原始 HTML**（不是提取出的 SVG），只对 `<svg>` 元素的包围盒截图。这既保证字体加载可靠（源 HTML 已接好），又满足"只导图表"规则。PNG 始终**透明背景**（`omit_background=True`），可放到任何幻灯片或文档底色上而无白色光晕。截图前等待 `document.fonts.ready`；绝不按任意墙钟延迟导出。

### 检测

运行前先确认 Playwright 已安装：

```
python -c "import playwright" 2>NUL || python -c "import playwright"
```

导入失败时，向用户原样给出以下指引并停止：

> Playwright isn't installed. To enable PNG export, run:
> ```
> pip install playwright
> playwright install chromium
> ```
> Then ask me to export again.

不要自动安装。用户要的是一项功能，不是系统变更。

### 光栅化

把下面片段写入临时文件并以 `python <tmp.py> <src.html> <out.png>` 运行：

```python
from playwright.sync_api import sync_playwright
import sys, pathlib

src, out = sys.argv[1], sys.argv[2]
scale = int(sys.argv[3]) if len(sys.argv) > 3 else 2

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=scale)
    page.goto(f"file://{pathlib.Path(src).resolve()}")
    page.wait_for_load_state("networkidle")
    page.locator("svg").first.screenshot(path=out, omit_background=True)
    browser.close()
```

默认 `device_scale_factor=2` 保证清晰。紧凑素材可用 `1`，打印/retina hero 可用 `3`，作为第三个 CLI 参数传入。

### 输出命名

`example-architecture.html` → `example-architecture.png`，写在源文件同目录。遵从用户显式给出的路径。

## 导出尺寸

PNG 像素尺寸 = SVG `viewBox` × `device_scale_factor`。尺寸决策在画图时已经做出——预设见 [`output-spec.md` §2](output-spec.md)。导出只选倍率。

| 用途 | Scale | 1280×720 `viewBox` 的结果 |
|---|---|---|
| 文档、README、wiki | 2 | 2560×1440 |
| 幻灯片（投影） | 2 | 2560×1440 |
| 打印 / PDF 讲义 | 3 | 3840×2160 |
| 内联缩略图、邮件 | 1 | 1280×720 |

### 命中精确像素尺寸

用户需要特定尺寸时（OG 卡片精确 1200×630、幻灯片图 1920×1080），计算 scale 而不是猜——Playwright 接受小数值：

```
scale = target_width / viewBox_width
```

960 宽 `viewBox` 目标 1200px 即 `scale=1.25`。两条规则：

- **绝不为命中小目标把 scale 压到 1 以下**——那会让文字发虚。改用更小预设重画。
- **绝不超过 4**——再高就是在放大为更小画布设计的布局；改用 `slide-16x9` 或打印预设重画。

目标宽高比与 `viewBox` 宽高比不一致时，明说并主动提出按匹配预设重画。对成品图加边或裁切以适配画框不是导出操作——那会破坏 40px 安全边距。

## 边界情况

- **源是多图 gallery HTML**（一个文件多个 SVG；gallery 为用户源文件，不随 skill 分发）：拒绝导出并询问用户具体指哪个图表文件。不要猜。
- **找不到 `<svg>` 块**：源不是图表文件。告知用户；什么都不写。
- **用户在意 HTML 外壳**：他们要卡片/页头进图。告知本 skill 只导出图表本体，建议用浏览器整页截图（或单独打印 PDF）。
- **源在运行时缺字体**：Playwright 会做替换，截图观感会偏。先判断场景：零外链交付物（离线演示、调用方工作流产物）有意不带 `<link href="...fonts.googleapis.com...">`，以系统字体栈渲染——替换是预期行为，不是错误。只有需要品牌 webfont 的联网发布图表才检查 `<head>` 里有无该 link；缺失说明文件早于当前字体栈约定——修源文件，而不是在导出环节绕过。

## 本命令绝不做的事

- 修改源 HTML。
- 添加导出按钮或 `<script>` 标签。静态图表保持无脚本；导出永不注入脚本或控制器。
- 在生成 HTML 时自动顺带产出 `.svg` 或 `.png`。每次都必须用户明确要求。
- 通过 `foreignObject` 把 HTML 壳（卡片、页头）嵌进 SVG。跨渲染器太脆弱。
