#!/usr/bin/env python3
"""动画触发验收：逐页 virtual-time-budget 100ms / 6000ms 双时间点截图并比对。

两时间点截图字节相同 = 该页无可见动画触发 → FAIL。
终态截图（t6000）同时留作目检底图。

用法: python3 shoot_anim.py <pages 目录> <截图输出目录>
退出码: 有无差异页 → 1
"""

import glob
import os
import subprocess
import sys

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def shoot(chrome, url, out, budget):
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1920,1080",
    ]
    if budget:
        cmd.append(f"--virtual-time-budget={budget}")
    cmd += [f"--screenshot={out}", url]
    subprocess.run(cmd, capture_output=True, timeout=120)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    chrome = find_chrome()
    if not chrome:
        print("[FAIL] 未找到系统 Chrome，设 CHROME_PATH 后重试")
        sys.exit(1)
    pages = sorted(glob.glob(os.path.join(sys.argv[1], "p*.html")))
    if not pages:
        print(f"[FAIL] 目录无 p*.html: {sys.argv[1]}")
        sys.exit(1)
    os.makedirs(sys.argv[2], exist_ok=True)
    fails = []
    for p in pages:
        name = os.path.basename(p)[:-5]
        url = f"file://{os.path.abspath(p)}"
        t1 = os.path.join(sys.argv[2], f"{name}-t100.png")
        t2 = os.path.join(sys.argv[2], f"{name}-t6000.png")
        shoot(chrome, url, t1, 100)
        shoot(chrome, url, t2, 6000)
        s1, s2 = os.path.getsize(t1), os.path.getsize(t2)
        if s1 == s2:
            fails.append(f"{name}: 双时间点截图无差异（动画未触发）")
            print(f"{name}: 无差异 FAIL ({s1}B)")
        else:
            print(f"{name}: 动画触发 OK (t100={s1}B t6000={s2}B)")
    if fails:
        print("[FAILS]")
        for f in fails:
            print(" ", f)
        sys.exit(1)
    print(f"ALL PASS: {len(pages)} pages anim triggered")


if __name__ == "__main__":
    main()
