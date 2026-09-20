#!/usr/bin/env python3
"""截图矩阵（headless 验证方法论条 2/4/7/9）：原始 deck + 深链逐页截图，产物存在性校验。

用法:
  python3 screenshot_matrix.py <deck.html> --pages 8 [-o shots/] [--budget 6000]
  python3 screenshot_matrix.py <deck.html> --steps 3:2,5:1        # 页3有2步: #/3/1 #/3/2
  python3 screenshot_matrix.py <deck.html> --preview 1-12          # 分支页 ?preview=N
  python3 screenshot_matrix.py <pages目录> --multi                 # 多页形态逐文件截图
  python3 screenshot_matrix.py <deck.html> --pages 8 --portrait    # 竖版 810×1080（小红书图文形态）
  python3 screenshot_matrix.py <deck.html> --pages 8 --size 1080x1080  # 自定义画布 WxH

条 9: chrome --screenshot 退出码 0 不代表 PNG 落盘；每张截图后校验文件存在且非空，
批量结束汇总失败数，>0 非零退出。截图一律用原始文件，不用注入断言的临时副本（条 7）。

竖版契约（content-imagery-and-infographic.md 竖版 deck 画布条 1）: 画布固定 810×1080（3:4），
出图按 4/3 线性放大 → --window-size=810,1080 --force-device-scale-factor=1.3333；
--portrait 即该组合，--size 810x1080 同样自动附加 1.3333；其余自定义尺寸不加 dsf。
默认 1920×1080 行为不变。
"""

import argparse
import os
import re
import subprocess
import sys
from shutil import which

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        p = c if os.path.sep in c and os.path.exists(c) else which(c)
        if p and os.path.exists(p):
            return p
    print("FAIL 未找到 Chrome/Chromium", file=sys.stderr)
    sys.exit(2)


def shoot(chrome, url, out, budget, size="1920,1080", dsf=None):
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={size}",
    ]
    if dsf:
        cmd.append(f"--force-device-scale-factor={dsf}")
    cmd += [
        f"--virtual-time-budget={budget}",
        f"--screenshot={out}",
        url,
    ]
    subprocess.run(cmd, capture_output=True, timeout=180)
    return os.path.exists(out) and os.path.getsize(out) > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--pages", type=int, default=0)
    ap.add_argument("--steps", default="")
    ap.add_argument("--preview", default="")
    ap.add_argument("--multi", action="store_true")
    ap.add_argument(
        "--portrait",
        action="store_true",
        help="竖版 810×1080 + dsf 1.3333（content-imagery-and-infographic.md 竖版契约）",
    )
    ap.add_argument(
        "--size",
        default="",
        help="自定义画布 WxH（如 1080x1080；810x1080 自动加 dsf 1.3333）",
    )
    ap.add_argument("-o", "--outdir", default="shots")
    ap.add_argument("--budget", type=int, default=6000)
    args = ap.parse_args()

    size, dsf = "1920,1080", None
    if args.portrait and args.size:
        print("FAIL --portrait 与 --size 互斥", file=sys.stderr)
        sys.exit(2)
    if args.portrait:
        size, dsf = "810,1080", "1.3333"
    elif args.size:
        m = re.fullmatch(r"(\d+)[xX,](\d+)", args.size.strip())
        if not m:
            print(f"FAIL --size 格式 WxH: {args.size}", file=sys.stderr)
            sys.exit(2)
        size = f"{m.group(1)},{m.group(2)}"
        if size == "810,1080":
            dsf = "1.3333"

    chrome = find_chrome()
    os.makedirs(args.outdir, exist_ok=True)
    jobs = []
    base = os.path.abspath(args.target)

    if args.multi:
        if not os.path.isdir(base):
            print("FAIL --multi 需要 pages 目录", file=sys.stderr)
            sys.exit(2)
        for f in sorted(x for x in os.listdir(base) if x.endswith(".html")):
            jobs.append(
                (
                    f"file://{os.path.join(base, f)}",
                    f"page-{os.path.splitext(f)[0]}.png",
                )
            )
    elif args.preview:
        m = re.fullmatch(r"(\d+)-(\d+)", args.preview)
        if not m:
            print("FAIL --preview 格式 N-M", file=sys.stderr)
            sys.exit(2)
        for n in range(int(m.group(1)), int(m.group(2)) + 1):
            jobs.append((f"file://{base}?preview={n}", f"preview-{n:02d}.png"))
    else:
        step_map = {}
        for part in filter(None, args.steps.split(",")):
            pg, st = part.split(":")
            step_map[int(pg)] = int(st)
        total = args.pages or (max(step_map) if step_map else 0)
        if not total:
            print(
                "FAIL 需要 --pages / --steps / --preview / --multi 之一",
                file=sys.stderr,
            )
            sys.exit(2)
        for pg in range(1, total + 1):
            jobs.append((f"file://{base}#/{pg}", f"p{pg:02d}.png"))
            for st in range(1, step_map.get(pg, 0) + 1):
                jobs.append((f"file://{base}#/{pg}/{st}", f"p{pg:02d}-s{st}.png"))

    failures = []
    for url, name in jobs:
        out = os.path.join(args.outdir, name)
        ok = shoot(chrome, url, out, args.budget, size, dsf)
        print(("OK  " if ok else "MISS") + f" {name}")
        if not ok:
            failures.append(name)

    print(f"--- 截图汇总: {len(jobs)} 张, 失败 {len(failures)} ---")
    if failures:
        print(
            "FAIL 以下截图未落盘（退出码0不代表成功，条9）:",
            ", ".join(failures),
            file=sys.stderr,
        )
        sys.exit(1)
    print("PASS 全部落盘，逐张目检: 话术零泄漏/标签碰撞/划线飞出/裁切")


if __name__ == "__main__":
    main()
