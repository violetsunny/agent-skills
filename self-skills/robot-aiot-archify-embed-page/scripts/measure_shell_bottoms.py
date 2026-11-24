#!/usr/bin/env python3
"""批量渲染整页 shell，自底扫描内容 bottom；--offline 与基线比对（吸收 verify_offline_fonts）。

与 measure_iframe_height.sh 分工：.sh 定单 artifact 的 iframe 高（饱和 scrollHeight 法）；
本脚本测整页 bottom（布局塌陷/截断检测 + 离线保真比对），不重叠。
角落像素口径（px[2,2] 定背景）对渐变背景失效——适用白底 shell；
artifact 定高禁走像素口径，用 measure_iframe_height.sh。

用法:
  python3 measure_shell_bottoms.py <root> [页面名 ...] [--glob '*.html'] [--width 1200]
      [--canvas-h 20000] [--out shell_bottoms.json] [--png-dir _bottoms]
  python3 measure_shell_bottoms.py <root> --offline [--baseline shell_bottoms.json]
      [--out offline_bottoms.json] [--png-dir _bottoms_offline]
页面名可带或不带 .html；缺省按 glob 收集（排除 archify-*.html，含 index）。
全部渲染带断网参数全套（offline-env.md 铁律，基线与离线同口径）。
--offline 须有基线 json（默认 <root>/shell_bottoms.json，缺失 exit 2）：
delta 为真实字体 vs 旧系统回退基线之差，预期非零（远程字体此前从未加载成功，
所谓「联网基线」其实就是系统回退）——delta 非零 = 真实字体首次生效，不是回归。
渲染失败或 bottom 触画布边（>= canvas-h-10）→ exit 1。
环境变量 CHROME_PATH 覆盖系统 Chrome。依赖 PIL。
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

CHROME = os.environ.get(
    "CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
NET_BLOCK = [
    "--host-resolver-rules=MAP * ~NOTFOUND",
    "--disable-background-networking",
    "--disable-component-update",
    "--disable-sync",
    "--disable-domain-reliability",
    "--disable-breakpad",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-features=Translate,OptimizationHints,MediaRouter,DomainReliability",
]


def bottom_of(png: Path) -> int:
    im = Image.open(png).convert("RGB")
    w, h = im.size
    px = im.load()
    bg = px[2, 2]

    def row_differs(y: int) -> bool:
        for x in range(0, w, 4):
            p = px[x, y]
            if abs(p[0] - bg[0]) + abs(p[1] - bg[1]) + abs(p[2] - bg[2]) > 12:
                return True
        return False

    for y in range(h - 1, -1, -1):
        if row_differs(y):
            return y + 1
    return 0


def render(png: Path, url: str, width: int, canvas_h: int):
    if png.exists():
        png.unlink()
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            *NET_BLOCK,
            f"--screenshot={png}",
            f"--window-size={width},{canvas_h}",
            "--virtual-time-budget=6000",
            url,
        ],
        capture_output=True,
        timeout=120,
    )
    return bottom_of(png) if png.exists() else None


def main():
    ap = argparse.ArgumentParser(
        description="整页 shell bottom 批量测量 / 离线基线比对"
    )
    ap.add_argument("root")
    ap.add_argument("pages", nargs="*", help="页面名（stem 或 .html）；缺省按 --glob")
    ap.add_argument("--glob", default="*.html")
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--canvas-h", type=int, default=20000)
    ap.add_argument("--out", default=None)
    ap.add_argument("--png-dir", default=None)
    ap.add_argument("--offline", action="store_true", help="与基线比对 delta")
    ap.add_argument("--baseline", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    pages = [p[:-5] if p.endswith(".html") else p for p in args.pages]
    if not pages:
        pages = sorted(
            f.stem for f in root.glob(args.glob) if not f.name.startswith("archify-")
        )
    baseline = None
    if args.offline:
        bp = Path(args.baseline) if args.baseline else root / "shell_bottoms.json"
        if not bp.exists():
            print(f"基线不存在: {bp}（先跑不带 --offline 的基线测量）")
            return 2
        baseline = json.loads(bp.read_text(encoding="utf-8"))
    png_dir = root / (
        args.png_dir or ("_bottoms_offline" if args.offline else "_bottoms")
    )
    png_dir.mkdir(exist_ok=True)
    out_path = (
        Path(args.out)
        if args.out
        else root / ("offline_bottoms.json" if args.offline else "shell_bottoms.json")
    )
    results = {}
    failed, edge = [], []
    for page in pages:
        b = render(
            png_dir / f"{page}.png",
            f"file://{root / (page + '.html')}",
            args.width,
            args.canvas_h,
        )
        if b is None:
            failed.append(page)
            results[page] = None
            print(f"{page}: RENDER_FAILED", flush=True)
            continue
        results[page] = b
        if b >= args.canvas_h - 10:
            edge.append(page)
        if args.offline:
            base = baseline.get(page)
            d = (b - base) if base is not None else None
            print(f"{page}: offline={b} fallback_baseline={base} delta={d}", flush=True)
        else:
            print(f"{page}: bottom={b}", flush=True)
    out_path.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"完成 {len(results)} 页；渲染失败 {failed}；触边 {edge}")
    if args.offline:
        print(
            "注：delta 为真实字体 vs 旧系统回退基线之差，预期非零（远程字体此前从未加载）"
        )
    print(f"written {out_path}")
    return 1 if (failed or edge) else 0


if __name__ == "__main__":
    sys.exit(main())
