# PNG 导出（SVG→PNG 光栅化）

> **分工声明：** 本文件管 SVG→PNG 光栅化（cairosvg / rsvg-convert / svg2png.js 栈）；HTML 产物导出（HTML→PNG 截图、多图 gallery、OG 卡片）见 `export.md`。两文件互指，不重复内容。

仅当内置 `generate-diagram.sh` 回退链不够用，或必须手动指定特定渲染器时才加载本参考。

## 渲染器选择

| 工具 | 安装 | 适用场景 |
| --- | --- | --- |
| CairoSVG | `python3 -m pip install cairosvg` | 默认选择；CSS 支持好 |
| `rsvg-convert` | `brew install librsvg` 或 `apt install librsvg2-bin` | 无复杂 CSS 的简单 SVG |
| Puppeteer | Node.js + Chromium | 浏览器生成的 SVG、CJK/emoji 回退、或需要像素级保真 |

优先使用内置的校验/导出入口：

```bash
SKILL_ROOT="$HOME/.agents/skills/robot-aiot-arch-diagram"  # 本 skill 安装目录（SKILL.md 所在处），按实际安装路径调整
"$SKILL_ROOT/scripts/generate-diagram.sh" -t architecture -s 1 -o ./diagram.svg -w 1920
```

## 手动 CairoSVG

```bash
python3 -c "import cairosvg; cairosvg.svg2png(url='input.svg', write_to='output.png', output_width=1920)"
```

## 手动 librsvg

```bash
rsvg-convert -w 1920 input.svg -o output.png
```

## Puppeteer

`scripts/svg2png.js` 优先 `require("puppeteer")`；缺失时自动回退 `puppeteer-core` + 系统 Chrome（macOS/Linux 常见路径，或 `CHROME_PATH` 环境变量指定），无需下载 Chromium：

```bash
SKILL_ROOT="$HOME/.agents/skills/robot-aiot-arch-diagram"  # 本 skill 安装目录（SKILL.md 所在处），按实际安装路径调整
npm install --prefix /tmp/svg2png-core puppeteer-core@25.3.0
NODE_PATH=/tmp/svg2png-core/node_modules node "$SKILL_ROOT/scripts/svg2png.js" ./output
```

完整 puppeteer 安装（自带 Chromium，弱网可能超时）仍受支持：

```bash
npm install --prefix /tmp/svg2png-puppeteer puppeteer
NODE_PATH=/tmp/svg2png-puppeteer/node_modules node "$SKILL_ROOT/scripts/svg2png.js" ./output
```

## 已知限制

- `rsvg-convert` 可能省略复杂 CSS、滤镜与 `<foreignObject>` 内容。
- CairoSVG 在所选系统字体缺字形时会漏掉 CJK 或 emoji。macOS 上 fontconfig 经常解析不到系统 CJK 族名（如 `fc-match "PingFang SC"` 回退到 Verdana），且 `≈ × → ① …` 等符号字形在 SVG 文本中渲染为豆腐块；SVG 文本限制在安全集 `—— 、，。（）【】：+ / · “”` 加普通中文/拉丁/数字内（HTML 页面文本不受影响——浏览器按字形逐个回退）。必须出现这些符号时改用 Puppeteer 渲染器。
- 需要浏览器渲染时用 Puppeteer；其 viewport 路径比裸 Chrome `--window-size` 截图更可靠地保持 SVG 尺寸。
- 任何转换器退出码为 0 都不能证明 PNG 已落盘。用 `[ -s output.png ]` 校验每个输出；批量运行时统计失败数，任一页面缺失即以非零码退出。
