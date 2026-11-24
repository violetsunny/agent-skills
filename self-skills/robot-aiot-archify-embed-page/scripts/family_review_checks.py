#!/usr/bin/env python3
"""拆分家族提交前独立复核（只读）：锚点/内容无丢失/doclist/图号/规则合规/深链/标签平衡。

对应 references/rebuild-mode.md §9 复核票与 split-mode.md §6 结构校验。
通用项（ids==chips/规则合规/深链/标签平衡）恒跑；期望值项（锚点序列/内容分布/doclist 计数/图号映射）
须 --expect expect.json，无则显式报 SKIP。
secret 检测用通用正则（任何非脱敏占位的 sk- 令牌即 FAIL），不携带任何真实 key 前缀。

用法:
  python3 family_review_checks.py <root> --pages 母页.html 子页1.html 子页2.html
      [--expect expect.json] [--out review_output.txt] [--stub-marker 完整内容见]
--pages 第一页为母页。expect.json:
  {
    "母页.html": {"ids": ["s01",...], "doclist_count": 19, "fig": "图 X-0",
                  "artifact": "archify-....html", "stub_sections": ["s02",...]},
    "子页1.html": {"ids": [...], "doclist_count": 7, "fig": "图 X-1",
                  "artifact": "...", "content_sections": ["s02",...]},
    "_inbound": {"page": "下一章.html", "family_prefix": "ch19"}
  }
_inbound 可选：入链页对家族的全部深链必须存在且 id 在位，无入链报 FAIL。
stub 判定：table/pre=0 且段落>=1 且「stub-marker + 深链」在位；子页内容节：table/pre/card>0 且文本>200 且无 stub 标记。
doclist 并集：母页清单 == 子页清单按 --pages 顺序拼接（原始 + 实体解码双口径）。
任何 FAIL → exit 1。证据落盘 --out（默认 <root>/family_review_output.txt）。
index.html 自身 assets/style.css 是 assets 禁令唯一例外（split-mode §5），报 FAIL 时按存量裁决，不阻塞新页提交。仅 stdlib。
"""

import argparse
import html as H
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SECRET_RE = re.compile(r"\bsk-(?!xxx\b)[A-Za-z0-9]{8,}\b")
OUT = []


def log(s=""):
    OUT.append(s)
    print(s)


def sections(s):
    ms = list(re.finditer(r'<h2 id="(s\d+)"', s))
    out = {}
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(s)
        out[m.group(1)] = s[m.start() : end]
    return out


def strip_tags(x):
    return re.sub(r"<[^>]+>", "", x)


def main():
    ap = argparse.ArgumentParser(description="拆分家族提交前独立复核（只读）")
    ap.add_argument("root")
    ap.add_argument("--pages", nargs="+", required=True, help="第一页为母页")
    ap.add_argument("--expect", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--stub-marker", default="完整内容见")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    pages = args.pages
    parent = pages[0]
    missing = [f for f in pages if not (root / f).exists()]
    if missing:
        print(f"页面文件不存在: {missing}")
        return 2
    expect = (
        json.loads(Path(args.expect).read_text(encoding="utf-8"))
        if args.expect
        else None
    )
    cache = {}

    def read(name):
        if name not in cache:
            p = root / name
            cache[name] = p.read_text(encoding="utf-8") if p.exists() else ""
        return cache[name]

    for f in pages:
        read(f)
    if (root / "index.html").exists():
        read("index.html")
    inb = (expect or {}).get("_inbound")
    if inb:
        read(inb["page"])

    log("=== 1 锚点完整性 ===")
    for f in pages:
        ids = re.findall(r'<h2 id="(s\d+)"', read(f))
        nav = re.search(r'<nav class="anchor-chips">(.*?)</nav>', read(f), re.S)
        chips = re.findall(r'href="#(s\d+)"', nav.group(1)) if nav else []
        want = (expect or {}).get(f, {}).get("ids")
        if want is not None:
            ok = ids == want and chips == want
            log(
                f"{f}: h2={ids} chips={chips} 期望={want} -> {'PASS' if ok else 'FAIL'}"
            )
        else:
            ok = (ids == chips) if nav else True
            log(
                f"{f}: h2={ids} chips={chips} (ids==chips) -> {'PASS' if ok else 'FAIL'}"
            )
    if inb:
        pf, prefix = inb["page"], inb["family_prefix"]
        links = re.findall(
            r'href="(' + re.escape(prefix) + r'[^"#]*\.html)#(s\d+)"', read(pf)
        )
        for tgt, anc in links:
            tgt = unquote(tgt)
            ok = (root / tgt).exists() and f'id="{anc}"' in read(tgt)
            log(f"{pf} -> {tgt}#{anc}: {'PASS' if ok else 'FAIL'}")
        if not links:
            log(f"{pf} 无 {prefix}*#sNN 入链 FAIL")
    else:
        log("入链深链检查 SKIP（--expect._inbound 未给）")

    log("\n=== 2 内容无丢失 ===")
    if expect:
        sec = {f: sections(read(f)) for f in pages}
        for f in pages[1:]:
            for sid in expect.get(f, {}).get("content_sections", []):
                b = sec[f].get(sid)
                if b is None:
                    log(f"{f} {sid}: 节缺失 FAIL")
                    continue
                nt, np = len(re.findall(r"<table\b", b)), len(re.findall(r"<pre\b", b))
                nc = len(re.findall(r'class="[^"]*\bcard\b', b))
                txt = len(strip_tags(b).strip())
                ok = (nt + np + nc) > 0 and txt > 200 and args.stub_marker not in b
                log(
                    f"{f} {sid}: table={nt} pre={np} card={nc} 文本长={txt} -> {'PASS' if ok else 'FAIL'}"
                )
        for sid in expect.get(parent, {}).get("stub_sections", []):
            b = sec[parent].get(sid)
            if b is None:
                log(f"{parent} {sid}: 节缺失 FAIL")
                continue
            nt, np = len(re.findall(r"<table\b", b)), len(re.findall(r"<pre\b", b))
            prose = len(re.findall(r"<p\b", b))
            deep = re.findall(
                re.escape(args.stub_marker) + r'\s*<a href="([^"]+\.html#[^"]+)"', b
            )
            deep_ok = all(
                (root / unquote(d.split("#")[0])).exists()
                and f'id="{d.split("#")[1]}"' in read(unquote(d.split("#")[0]))
                for d in deep
            )
            ok = nt == 0 and np == 0 and prose >= 1 and len(deep) >= 1 and deep_ok
            log(
                f"{parent} {sid}: table={nt} pre={np} 段落={prose} 深链={deep} -> {'PASS' if ok else 'FAIL'}"
            )
        log("table/pre 分布:")
        for f in pages:
            per = {
                sid: (len(re.findall(r"<table\b", b)), len(re.findall(r"<pre\b", b)))
                for sid, b in sec[f].items()
            }
            tot_t = len(re.findall(r"<table\b", read(f)))
            tot_p = len(re.findall(r"<pre\b", read(f)))
            log(f"  {f}: 全页 table={tot_t} pre={tot_p} | 分节(table,pre)={per}")
    else:
        log("SKIP（--expect 未给）")

    log("\n=== 3 文档清单 ===")

    def doclist(f):
        m = re.search(r'<ul class="doclist">(.*?)</ul>', read(f), re.S)
        return (
            [x.strip() for x in re.findall(r"<li>(.*?)</li>", m.group(1), re.S)]
            if m
            else []
        )

    if expect:
        dl = {f: doclist(f) for f in pages}
        for f in pages:
            want = expect.get(f, {}).get("doclist_count")
            if want is None:
                continue
            log(
                f"{f} doclist={len(dl[f])} 项 (期望{want}) -> {'PASS' if len(dl[f]) == want else 'FAIL'}"
            )
        concat = [x for f in pages[1:] for x in dl[f]]
        same_raw = dl[parent] == concat
        same_unesc = [H.unescape(x) for x in dl[parent]] == [
            H.unescape(x) for x in concat
        ]
        log(
            f"{len(dl[parent])} == {len(concat)} 逐字(原始): {same_raw} | 逐字(实体解码后): {same_unesc} -> {'PASS' if same_raw else 'FAIL'}"
        )
        if not same_raw:
            for i, (a, b) in enumerate(zip(dl[parent], concat)):
                if a != b:
                    log(f"  差异#{i}: 母页={a!r} vs 子页={b!r}")
            log(f"  长度: {len(dl[parent])} vs {len(concat)}")
        for f in pages:
            log(f"  {f} 清单: {dl[f]}")
    else:
        log("SKIP（--expect 未给）")

    log("\n=== 4 图号与 iframe ===")
    if expect:
        for f in pages:
            e = expect.get(f, {})
            if "fig" not in e and "artifact" not in e:
                continue
            caps = re.findall(r'<p class="figcap">(.*?)</p>', read(f), re.S)
            srcs = re.findall(r'<iframe[^>]*src="([^"]+)"', read(f))
            has_fig = any(e["fig"] in c for c in caps) if "fig" in e else None
            ok = True
            if "fig" in e:
                ok &= has_fig
            if "artifact" in e:
                ok &= srcs == [e["artifact"]] and (root / e["artifact"]).exists()
            log(
                f"{f}: figcap含{e.get('fig')}={has_fig} "
                f"iframe={srcs} 期望={e.get('artifact')} -> {'PASS' if ok else 'FAIL'}"
            )
    else:
        log("SKIP（--expect 未给）")

    log("\n=== 5 规则合规 ===")
    check_files = pages + (
        ["index.html"]
        if (root / "index.html").exists() and "index.html" not in pages
        else []
    )
    for f in check_files:
        s = read(f)
        a = re.findall(r'(?:href|src)="(?:\.\./)?assets/', s)
        rf = re.findall(r"fonts\.googleapis|fonts\.gstatic", s)
        kk = SECRET_RE.findall(s)
        ok = not a and not rf and not kk
        log(
            f"{f}: 裸assets={len(a)} 远程字体={len(rf)} 真实apiKey={kk} -> {'PASS' if ok else 'FAIL'}"
        )
    names = list(check_files)
    for f in pages:
        names += re.findall(r'<iframe[^>]*src="([^"]+)"', read(f))
    bad = [n for n in names if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.html", n)]
    log(f"文件名 kebab-case: {names} 违规={bad} -> {'PASS' if not bad else 'FAIL'}")

    log("\n=== 6 深链 ===")
    allok = True
    for f in pages:
        for tgt, anc in re.findall(r'href="([^"#]+\.html)#([^"]+)"', read(f)):
            if "://" in tgt:
                continue
            tgt = unquote(tgt)
            ok = (root / tgt).exists() and f'id="{anc}"' in read(tgt)
            allok &= ok
            log(f"{f} -> {tgt}#{anc}: {'PASS' if ok else 'FAIL'}")
    for f in pages:
        for nav in ["topnav", "pagenav"]:
            m = re.search(r'class="' + nav + r'"(.*?)</(?:nav|div)>', read(f), re.S)
            hrefs = re.findall(r'href="([^"#]+)"', m.group(1)) if m else []
            for h in hrefs:
                if "://" in h:
                    continue
                h = unquote(h)
                ok = (root / h).exists()
                allok &= ok
                log(f"{f} {nav} -> {h}: {'PASS' if ok else 'FAIL'}")
    log(f"深链总体: {'PASS' if allok else 'FAIL'}")

    log("\n=== 8 标签平衡（body 内） ===")
    for f in pages:
        body = re.search(r"<body.*?>(.*)</body>", read(f), re.S).group(1)
        body_ns = re.sub(r"<script\b.*?</script>", "", body, flags=re.S)
        row = []
        ok = True
        for tag in ["div", "p", "table", "pre", "code", "a", "ul", "li"]:
            o = len(re.findall(r"<" + tag + r"(?=[\s>])", body_ns))
            c = len(re.findall(r"</" + tag + r"\s*>", body_ns))
            o_raw = len(re.findall(r"<" + tag + r"(?=[\s>])", body))
            c_raw = len(re.findall(r"</" + tag + r"\s*>", body))
            ok &= o == c
            row.append(
                f"{tag}:{o}/{c}"
                + (f"(含script:{o_raw}/{c_raw})" if (o_raw, c_raw) != (o, c) else "")
            )
        log(f"{f}: {' '.join(row)} -> {'PASS' if ok else 'FAIL'}")

    fails = sum(1 for l in OUT if l.endswith("FAIL"))
    log(f"\n合计 FAIL: {fails}")
    out_path = Path(args.out) if args.out else root / "family_review_output.txt"
    out_path.write_text("\n".join(OUT) + "\n", encoding="utf-8")
    print(f"written {out_path}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
