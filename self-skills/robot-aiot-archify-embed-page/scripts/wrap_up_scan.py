#!/usr/bin/env python3
"""全站一致性扫描：锚点序列/外链家族并集/assets/远程字体/sha receipt/geometry/index 收录。

口径（references/rebuild-mode.md §6、split-mode.md §6、archify-gate-fixes.md）：
  - 外链守恒用家族并集：fam_root = 页名去 -N 后缀，家族 = 根页 + 同名 -N 子页；
    旧 href 在家族并集内丢失才报（拆分场景逐页相等会误报，母页归零属正确行为）。
  - ✅ 前缀归一化后比对；URL-encoded 链接先 unquote 再查存在性。
  - receipt 双目录：只认 <receipt-dir>/<slug>/*.finalize.json（取最后一份）的 artifact.sha256，
    与文件实 sha 比对；新 artifact 须另建该目录放 receipt + 字节副本（gate-fixes 口径）。
  - git 基线不可用（非 git 仓库且未给 --baseline-dir）或单页不在基线（新建页）→
    该页 ids_match / 旧外链比对 SKIP 并显式记录，不误报。
  - problems 非空 → exit 1。输出 JSON 含 skips 清单（失败可见）。

用法:
  python3 wrap_up_scan.py <root> [--pages-glob '*.html'] [--git-ref HEAD] [--git-prefix '']
      [--baseline-dir DIR] [--articles-prefix '../../articles/'] [--subtitle-marker '']
      [--receipt-dir validation/archify] [--exclude NAME]... [--out wrap_up_scan.json]
--git-prefix：root 不是 git 仓库根时补路径前缀（如 sub/dir/）。
--subtitle-marker：promote 追加句标记（rebuild-mode §4），空则跳过该项。
--articles-prefix：内容外链前缀，空则跳过外链项。--exclude：排除页名（stem 或文件名，如非 archify- 前缀的 artifact）。
清理纪律保留的临时探针/对照 html 副本须 --exclude 或移出扫描根，否则按页面计入并误报 index 缺页。
依赖同目录 check_svg_geometry.py（自包含 import）；仅 stdlib。
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_svg_geometry import check_file

H2_RE = re.compile(r'<h2 id="(s\d+)"')


def git_old(root, page, ref, prefix):
    r = subprocess.run(
        ["git", "show", f"{ref}:{prefix}{page}.html"],
        capture_output=True,
        text=True,
        cwd=root,
    )
    return r.stdout if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser(description="全站一致性扫描（家族并集口径）")
    ap.add_argument("root")
    ap.add_argument("--pages-glob", default="*.html")
    ap.add_argument("--git-ref", default="HEAD")
    ap.add_argument("--git-prefix", default="")
    ap.add_argument("--baseline-dir", default=None, help="非 git 项目的旧版基线目录")
    ap.add_argument("--articles-prefix", default="../../articles/")
    ap.add_argument("--subtitle-marker", default="")
    ap.add_argument("--receipt-dir", default="validation/archify")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    excluded = {e[:-5] if e.endswith(".html") else e for e in args.exclude}
    pages = sorted(
        f.stem
        for f in root.glob(args.pages_glob)
        if f.stem != "index"
        and not f.name.startswith("archify-")
        and f.stem not in excluded
    )
    skips = []
    baseline_dir = Path(args.baseline_dir).resolve() if args.baseline_dir else None
    git_ok = False
    if baseline_dir is None:
        r = subprocess.run(
            ["git", "rev-parse", "--git-dir"], capture_output=True, cwd=root
        )
        git_ok = r.returncode == 0
        if not git_ok:
            skips.append(
                "git 基线不可用（非 git 仓库且未给 --baseline-dir）：ids_match/旧外链比对全 SKIP"
            )
    art_re = (
        re.compile(r'href="(' + re.escape(args.articles_prefix) + r'[^"]+)"')
        if args.articles_prefix
        else None
    )
    if art_re is None:
        skips.append("--articles-prefix 为空：外链守恒/断链检查 SKIP")

    pages_rec = {}
    problems = []
    for page in pages:
        html = (root / f"{page}.html").read_text(encoding="utf-8")
        if baseline_dir is not None:
            bf = baseline_dir / f"{page}.html"
            old = bf.read_text(encoding="utf-8") if bf.exists() else None
        elif git_ok:
            old = git_old(root, page, args.git_ref, args.git_prefix)
        else:
            old = None
        if old is None and (git_ok or baseline_dir is not None):
            skips.append(f"{page}: 不在基线（新建页），ids_match/旧外链比对 SKIP")
        old_h2 = H2_RE.findall(old) if old is not None else []
        new_ids = H2_RE.findall(html)
        iframes = re.findall(r'src="(archify-[^"]+\.html)"', html)
        assets = len(re.findall(r'(?:href|src)="(?:\.\./)?assets/', html))
        remote_fonts = len(re.findall(r"fonts\.googleapis|fonts\.gstatic", html))
        subtitle = (args.subtitle_marker in html) if args.subtitle_marker else None
        articles = art_re.findall(html) if art_re else []
        old_articles = art_re.findall(old) if (art_re and old) else []
        fam_root = re.sub(r"-\d+$", "", page)
        fam_files = [root / f"{fam_root}.html"] + sorted(
            root.glob(f"{fam_root}-*.html")
        )
        fam_articles = set()
        for ff in fam_files:
            if ff.exists() and art_re:
                fam_articles.update(art_re.findall(ff.read_text(encoding="utf-8")))
        fam_norm = {a.replace("✅", "") for a in fam_articles}
        lost = [a for a in old_articles if a.replace("✅", "") not in fam_norm]
        missing = [a for a in articles if not (root / unquote(a)).resolve().exists()]
        h1 = re.search(r"\.diagram-frame\s*\{[^}]*height:\s*(\d+)px", html)
        h2 = re.search(r"\.frame-2\s*\{[^}]*height:\s*(\d+)px", html)
        heights = ([h1.group(1)] if h1 else []) + ([h2.group(1)] if h2 else [])
        rec = {
            "baseline_found": old is not None,
            "sections_old": len(old_h2) if old is not None else None,
            "sections_new": len(new_ids),
            "ids_match": (old_h2 == new_ids) if old is not None else None,
            "iframes": iframes,
            "assets_refs": assets,
            "remote_font_refs": remote_fonts,
            "subtitle": subtitle,
            "articles_new": len(articles),
            "articles_old": len(old_articles),
            "articles_lost_in_family": lost,
            "articles_missing": missing,
            "iframe_heights": heights,
        }
        pages_rec[page] = rec
        if rec["ids_match"] is False:
            problems.append(f"{page}: 锚点序列与旧版不一致 old={old_h2} new={new_ids}")
        if assets:
            problems.append(f"{page}: assets 引用 {assets}")
        if remote_fonts:
            problems.append(f"{page}: 远程字体引用 {remote_fonts}（应内嵌离线）")
        if subtitle is False:
            problems.append(
                f"{page}: subtitle 追加句缺失（marker={args.subtitle_marker!r}）"
            )
        if lost:
            problems.append(f"{page}: 旧版外链在章节家族内丢失 {lost}")
        if missing:
            problems.append(f"{page}: 外链断链 {missing}")
        for f in iframes:
            if not (root / f).exists():
                problems.append(f"{page}: iframe 目标缺失 {f}")

    anchors_total = anchors_broken = 0
    for f in sorted(root.glob("*.html")):
        if f.name.startswith("archify-") or f.stem in excluded:
            continue
        html = f.read_text(encoding="utf-8")
        for m in re.finditer(r'href="([^"#]+\.html)#([^"]+)"', html):
            if "://" in m.group(1):
                continue
            anchors_total += 1
            t = root / m.group(1)
            if not t.exists() or f'id="{m.group(2)}"' not in t.read_text(
                encoding="utf-8"
            ):
                anchors_broken += 1
                problems.append(f"锚点断链: {f.name} -> {m.group(1)}#{m.group(2)}")

    artifacts = {}
    for f in sorted(root.glob("archify-*.html")):
        slug = f.name[len("archify-") : -len(".html")]
        sha = hashlib.sha256(f.read_bytes()).hexdigest()
        receipt_dir = root / args.receipt_dir / slug
        receipts = (
            sorted(receipt_dir.glob("*.finalize.json")) if receipt_dir.exists() else []
        )
        receipt_sha = None
        if receipts:
            d = json.loads(receipts[-1].read_text(encoding="utf-8"))
            receipt_sha = d.get("artifact", {}).get("sha256")
        n_findings = len(check_file(f))
        artifacts[f.name] = {
            "sha256_8": sha[:8],
            "receipt_sha_match": receipt_sha == sha,
            "receipt_found": bool(receipts),
            "geometry_findings": n_findings,
        }
        if receipt_sha != sha:
            problems.append(
                f"{f.name}: sha 与 receipt 不一致 (receipt={str(receipt_sha)[:8]})"
            )
        if n_findings:
            problems.append(f"{f.name}: geometry {n_findings} findings")

    index_rec = None
    index_file = root / "index.html"
    if index_file.exists():
        index_html = index_file.read_text(encoding="utf-8")
        index_links = set(re.findall(r'href="([^"#]+\.html)', index_html))
        index_missing = [p for p in pages if f"{p}.html" not in index_links]
        index_broken = [
            l for l in sorted(index_links) if "://" not in l and not (root / l).exists()
        ]
        if index_missing:
            problems.append(f"index.html 未收录页面: {index_missing}")
        if index_broken:
            problems.append(f"index.html 断链: {index_broken}")
        index_rec = {
            "links": len(index_links),
            "missing_pages": index_missing,
            "broken": index_broken,
        }
    else:
        skips.append("index.html 不存在：index 收录检查 SKIP")

    out = {
        "pages": pages_rec,
        "artifacts": artifacts,
        "anchors": {"total": anchors_total, "broken": anchors_broken},
        "index": index_rec,
        "skips": skips,
        "problems": problems,
    }
    out_path = Path(args.out) if args.out else root / "wrap_up_scan.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(
        f"页面 {len(pages_rec)} | artifact {len(artifacts)} | 锚点 {anchors_total} 断链 {anchors_broken}"
    )
    if index_rec:
        print(
            f"index 收录 {index_rec['links']} 缺页 {len(index_rec['missing_pages'])} 断链 {len(index_rec['broken'])}"
        )
    for s in skips:
        print(f"  [SKIP] {s}")
    print(f"问题 {len(problems)} 项:")
    for p in problems:
        print(f"  {p}")
    print(f"written {out_path}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
