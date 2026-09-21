#!/usr/bin/env python3
""".notes 话术容器 computed 不可见断言（浏览器级）。

生成 iframe wrapper 加载全部页面，调用系统 Chrome headless dump-dom，
断言每页 .notes 容器存在、computed display 为 none、零几何泄漏。

用法: python3 check_notes_hidden.py <pages 目录>
退出码: 有失败 → 1；无 .notes 容器 → 1（演讲 deck 必带话术容器）
"""

import glob
import os
import re
import subprocess
import sys

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]

WRAPPER = """<!DOCTYPE html>
<html><body><pre id="out">RUNNING</pre>
<script>
var pages=%s;
var done=0,results=[];
pages.forEach(function(p){
  var ifr=document.createElement("iframe");
  ifr.src=p;
  ifr.style.cssText="width:400px;height:225px";
  ifr.onload=function(){
    try{
      var notes=ifr.contentDocument.querySelectorAll(".notes");
      var allHidden=notes.length>0&&Array.prototype.every.call(notes,function(n){return getComputedStyle(n).display==="none";});
      var leak=Array.prototype.some.call(notes,function(n){var r=n.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(n).display!=="none";});
      results.push(p+": notes="+notes.length+" computedHidden="+allHidden+" leak="+leak);
    }catch(e){results.push(p+": ERR "+e.message);}
    if(++done===pages.length)document.getElementById("out").textContent="RESULTS\\n"+results.join("\\n")+"\\nEND";
  };
  document.body.appendChild(ifr);
});
</script></body></html>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    chrome = find_chrome()
    if not chrome:
        print("[FAIL] 未找到系统 Chrome，设 CHROME_PATH 后重试")
        sys.exit(1)
    pages = sorted(
        os.path.basename(p) for p in glob.glob(os.path.join(sys.argv[1], "p*.html"))
    )
    if not pages:
        print(f"[FAIL] 目录无 p*.html: {sys.argv[1]}")
        sys.exit(1)
    import json

    wrapper = WRAPPER % json.dumps(pages)
    wp = os.path.join(sys.argv[1], "_notes_assert.html")
    with open(wp, "w", encoding="utf-8") as f:
        f.write(wrapper)
    try:
        out = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--allow-file-access-from-files",
                "--virtual-time-budget=15000",
                "--dump-dom",
                f"file://{os.path.abspath(wp)}",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        ).stdout
    finally:
        os.remove(wp)
    m = re.search(r"RESULTS\n(.*?)\nEND", out, re.S)
    if not m:
        print("[FAIL] wrapper 未产出 RESULTS（iframe 加载超时？）")
        sys.exit(1)
    fails = []
    for line in m.group(1).splitlines():
        print(line)
        if (
            "computedHidden=true" not in line
            or "leak=false" not in line
            or "notes=0" in line
        ):
            fails.append(line)
    if fails:
        print(f"[FAIL] {len(fails)} 页 .notes 断言不过")
        sys.exit(1)
    print(f"ALL PASS: {len(pages)} pages notes hidden")


if __name__ == "__main__":
    main()
