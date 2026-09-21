# PNG Export

Load this reference only when the bundled `generate-diagram.sh` fallback is insufficient or a specific renderer must be selected.

## Renderer Choice

| Tool | Install | Use when |
| --- | --- | --- |
| CairoSVG | `python3 -m pip install cairosvg` | Default; good CSS support |
| `rsvg-convert` | `brew install librsvg` or `apt install librsvg2-bin` | Simple SVGs without complex CSS |
| Puppeteer | Node.js plus Chromium | Browser-generated SVG, CJK/emoji fallback, or pixel fidelity |

Prefer the bundled validation/export entry point:

```bash
SKILL_ROOT="${CLAUDE_SKILL_DIR:-/absolute/path/from-codex-skill-metadata}"
"$SKILL_ROOT/scripts/generate-diagram.sh" -t architecture -s 1 -o ./diagram.svg -w 1920
```

## Manual CairoSVG

```bash
python3 -c "import cairosvg; cairosvg.svg2png(url='input.svg', write_to='output.png', output_width=1920)"
```

## Manual librsvg

```bash
rsvg-convert -w 1920 input.svg -o output.png
```

## Puppeteer

`scripts/svg2png.js` 优先 `require("puppeteer")`；缺失时自动回退 `puppeteer-core` + 系统 Chrome（macOS/Linux 常见路径，或 `CHROME_PATH` 环境变量指定），无需下载 Chromium：

```bash
SKILL_ROOT="${CLAUDE_SKILL_DIR:-/absolute/path/from-codex-skill-metadata}"
npm install --prefix /tmp/svg2png-core puppeteer-core@25.3.0
NODE_PATH=/tmp/svg2png-core/node_modules node "$SKILL_ROOT/scripts/svg2png.js" ./output
```

完整 puppeteer 安装（自带 Chromium，弱网可能超时）仍受支持：

```bash
npm install --prefix /tmp/svg2png-puppeteer puppeteer
NODE_PATH=/tmp/svg2png-puppeteer/node_modules node "$SKILL_ROOT/scripts/svg2png.js" ./output
```

## Known Limits

- `rsvg-convert` can omit complex CSS, filters, and `<foreignObject>` content.
- CairoSVG can miss CJK or emoji glyphs when the selected system font lacks them. On macOS, fontconfig frequently fails to resolve system CJK family names (e.g. `fc-match "PingFang SC"` falls back to Verdana), and symbol glyphs such as `≈ × → ① …` render as tofu boxes in SVG text; restrict SVG text to the safe set `—— 、，。（）【】：+ / · “”` plus plain CJK/Latin/digits (HTML page text is unaffected — browsers fall back per glyph). Switch to the Puppeteer renderer when those symbols must appear.
- Use Puppeteer when browser rendering is required; its viewport path preserves the SVG dimensions more reliably than a raw Chrome `--window-size` screenshot.
- A zero exit code from any converter does not prove the PNG landed on disk. Verify each output with `[ -s output.png ]`; in batch runs, count failures and exit non-zero if any page is missing.
