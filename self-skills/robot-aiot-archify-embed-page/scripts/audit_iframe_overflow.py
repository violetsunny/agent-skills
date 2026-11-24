#!/usr/bin/env python3
"""批量审计既有页面内每个 archify iframe 在真实壳布局下的溢出（单视口 ground truth）。

与 measure_iframe_height.sh 分工：.sh 是「单 artifact 定高」（饱和 scrollHeight 扫 + 高窗口 graybar 验证）；
本脚本是「批量审计既有页现状」——wrapper 加载整页，读内层 iframe clientWidth/Height 与 artifact
scrollHeight/Width，发现哪些页溢出需重定高。

为什么不能只用像素口径测高脚本：
  1) --hide-scrollbars 截图量的是「最后一行非背景像素」，不含底部纯背景 padding；
  2) 容器宽人工传，传错（如把 .container 的 max-width 当内宽）会低估回流后的高度；
  3) archify 产物含 min-height:100vh / max-height:min(Nrem,Kvh)，高度随视口变化，
     必须扫到「scrollHeight 不再随视口增长」的饱和值才是真实内容高。
本脚本直接问浏览器要 ground truth，不做像素推断。

局限：单视口（默认 2000px）下 vh 联动产物的 scrollHeight 未必饱和——建议高度须按
measure_iframe_height.sh 复测定高；「仅对会饱和的 artifact 成立：加高一档复测，溢出不变即属
reader-area 不饱和类，禁改 height」警示随建议值输出。

用法: python3 audit_iframe_overflow.py [页面.html ...] [--glob '*.html']
      [--wrapper-width 1240] [--wrapper-height 2000]
缺省审计 cwd 下 glob（排除 archify-*.html 自身）。wrapper 尺寸默认 1240x2000 为 handbook 实测参考，
按真实壳内宽调整。环境变量 CHROME_PATH 覆盖系统 Chrome。断网参数全套内置（offline-env.md 铁律）。
溢出/错误 → exit 1。仅 stdlib + Chrome。
"""

import argparse
import glob
import os
import re
import subprocess
import sys
import tempfile

CHROME = os.environ.get(
    "CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
OFFLINE = [
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

WRAPPER = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#fff}iframe{width:__W__px;height:__H__px;border:0;display:block}
</style></head><body>
<iframe id="f" src="file://__SRC__"></iframe><div id="p">PENDING</div>
<script>
function go(){
  var f=document.getElementById('f'), d=f.contentDocument;
  if(!d){document.getElementById('p').textContent='NO_ACCESS';return;}
  var out=[];
  var frs=d.querySelectorAll('iframe');
  for(var i=0;i<frs.length;i++){
    var fr=frs[i], id=fr.contentDocument;
    if(!id||!id.documentElement){out.push('NO_ACCESS_INNER');continue;}
    var de=id.documentElement, b=id.body;
    var sh=Math.max(de.scrollHeight,b?b.scrollHeight:0);
    var sw=Math.max(de.scrollWidth,b?b.scrollWidth:0);
    out.push('FRAME src='+fr.getAttribute('src')+' innerW='+fr.clientWidth+
      ' innerH='+fr.clientHeight+' artScrollH='+sh+' artScrollW='+sw+
      ' overflowY='+(sh-fr.clientHeight)+' overflowX='+(sw-fr.clientWidth));
  }
  document.getElementById('p').textContent='RESULT::'+(out.length?out.join(' || '):'NO_IFRAME');
}
document.getElementById('f').addEventListener('load',function(){setTimeout(go,2500);});
setTimeout(go,7000);
</script></body></html>"""


def audit(page, width, height):
    src = os.path.abspath(page)
    with tempfile.TemporaryDirectory() as td:
        wp = os.path.join(td, "w.html")
        with open(wp, "w", encoding="utf-8") as fh:
            fh.write(
                WRAPPER.replace("__SRC__", src)
                .replace("__W__", str(width))
                .replace("__H__", str(height))
            )
        cmd = [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--dump-dom",
            f"--window-size={width + 40},{height}",
            "--allow-file-access-from-files",
            "--virtual-time-budget=12000",
            *OFFLINE,
            f"file://{wp}",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    m = re.search(r"RESULT::([^<]+)", r.stdout)
    if not m:
        return [("ERROR", r.stdout[-200:] or r.stderr[-200:])]
    if m.group(1).strip() == "NO_IFRAME":
        return []
    rows = []
    for chunk in m.group(1).split(" || "):
        if not chunk.startswith("FRAME"):
            rows.append(("ERROR", chunk))
            continue
        kv = dict(p.split("=", 1) for p in chunk.split()[1:])
        rows.append((kv["src"], kv))
    return rows


def main():
    ap = argparse.ArgumentParser(
        description="批量审计既有页 iframe 溢出（单视口 ground truth）"
    )
    ap.add_argument("pages", nargs="*", help="页面路径；缺省按 --glob 收集")
    ap.add_argument("--glob", default="*.html")
    ap.add_argument("--wrapper-width", type=int, default=1240)
    ap.add_argument("--wrapper-height", type=int, default=2000)
    args = ap.parse_args()
    pages = args.pages
    if not pages:
        pages = [
            p
            for p in sorted(glob.glob(args.glob))
            if not os.path.basename(p).startswith("archify-")
        ]
    bad = 0
    for page in pages:
        if not os.path.isfile(page):
            print(f"[SKIP] {page} 不存在")
            continue
        rows = audit(page, args.wrapper_width, args.wrapper_height)
        if not rows:
            print(f"{page}: 无 iframe")
            continue
        for src, kv in rows:
            if src == "ERROR":
                print(f"{page}: [ERROR] {kv}")
                bad += 1
                continue
            oy, ox = int(kv["overflowY"]), int(kv["overflowX"])
            flag = "OK"
            if oy > 0 or ox > 0:
                flag = "OVERFLOW"
                bad += 1
            suggest = int(kv["artScrollH"]) + 2
            print(
                f"{page} :: {src}\n"
                f"    innerW={kv['innerW']} innerH={kv['innerH']} "
                f"artScrollH={kv['artScrollH']} artScrollW={kv['artScrollW']} "
                f"overflowY={oy:+d} overflowX={ox:+d}  [{flag}]"
                + (
                    f"  建议 height={suggest}px（仅对会饱和的 artifact 成立：加高一档复测，溢出不变即属 reader-area 不饱和类，禁改 height；vh 联动产物须按 measure_iframe_height.sh 复测定高）"
                    if oy > 0
                    else ""
                )
            )
    print(f"\n合计溢出/错误 iframe 数: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
