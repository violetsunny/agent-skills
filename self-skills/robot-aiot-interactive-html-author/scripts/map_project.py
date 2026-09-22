#!/usr/bin/env python3
"""经纬度 → 面板百分比坐标投影（content-imagery-and-infographic.md 原生 SVG 静态地图/经纬度 → 百分比坐标换算）。

用法:
  python3 map_project.py --points '[[117.1946,39.1052],[117.1988,39.1080],[117.2028,39.1090]]'
  python3 map_project.py points.json [--p 12] [--cos]
  points.json 形状: {"points":[{"id":"a","coord":[lng,lat]},...], "bbox":[lngMin,latMin,lngMax,latMax](可选)}

规则:
  - 包围盒线性投影，贴边余量 p=12 百分点:
      x = p + (lng-lngMin)/(lngMax-lngMin) * (100-2p)
      y = p + (latMax-lat)/(latMax-latMin) * (100-2p)   （纬度反转，北在上）
  - bbox 缺省时取全部点位包围盒
  - 退化情形: 单点或某维跨度为 0 → 该维取 50 居中
  - --cos: 跨省域尺度时 x 轴跨度先乘 cos(中心纬度) 压缩横向，避免东西向拉伸
  - 坐标越界（lng∉[-180,180] / lat∉[-90,90]）→ FAIL 退出码 1
  - 输出 JSON: id → {x,y}（保留 2 位）；换算结果写回数据契约 x/y 后渲染阶段不再触碰经纬度
"""

import argparse
import json
import math
import sys


def project(points, bbox=None, p=12.0, cos_correct=False):
    """points: [(id, lng, lat)]；返回 [(id, x, y)]"""
    lngs = [pt[1] for pt in points]
    lats = [pt[2] for pt in points]
    if bbox:
        lng_min, lat_min, lng_max, lat_max = bbox
    else:
        lng_min, lng_max = min(lngs), max(lngs)
        lat_min, lat_max = min(lats), max(lats)
    span_lng = lng_max - lng_min
    span_lat = lat_max - lat_min
    span = 100.0 - 2 * p
    cos_c = 1.0
    if cos_correct:
        lat_center = (lat_min + lat_max) / 2
        cos_c = math.cos(math.radians(lat_center))
    out = []
    for pid, lng, lat in points:
        if span_lng == 0:
            x = 50.0
        else:
            x = p + (lng - lng_min) / span_lng * span * cos_c
        if span_lat == 0:
            y = 50.0
        else:
            y = p + (lat_max - lat) / span_lat * span
        out.append((pid, round(x, 2), round(y, 2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="points.json；缺省用 --points")
    ap.add_argument("--points", default="", help="内联坐标列表 [[lng,lat],...]")
    ap.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("LNG_MIN", "LAT_MIN", "LNG_MAX", "LAT_MAX"),
    )
    ap.add_argument("--p", type=float, default=12.0, help="贴边余量百分点，默认 12")
    ap.add_argument(
        "--cos", action="store_true", help="x 轴乘 cos(中心纬度) 压缩（跨省域尺度）"
    )
    args = ap.parse_args()

    try:
        if args.file:
            with open(args.file, encoding="utf-8") as f:
                data = json.load(f)
            pts = [
                (str(pt.get("id", i)), float(pt["coord"][0]), float(pt["coord"][1]))
                for i, pt in enumerate(data["points"])
            ]
            bbox = data.get("bbox", args.bbox)
        elif args.points:
            raw = json.loads(args.points)
            pts = [(str(i), float(c[0]), float(c[1])) for i, c in enumerate(raw)]
            bbox = args.bbox
        else:
            print("FAIL 需要 points.json 或 --points 之一", file=sys.stderr)
            sys.exit(2)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"FAIL 输入解析失败: {e}", file=sys.stderr)
        sys.exit(2)

    if not pts:
        print("FAIL 点位列表为空", file=sys.stderr)
        sys.exit(1)
    for pid, lng, lat in pts:
        if not (-180 <= lng <= 180 and -90 <= lat <= 90):
            print(f"FAIL 坐标越界: {pid} [{lng},{lat}]", file=sys.stderr)
            sys.exit(1)
    if bbox:
        lng_min, lat_min, lng_max, lat_max = (float(v) for v in bbox)
        if lng_max < lng_min or lat_max < lat_min:
            print("FAIL bbox 逆序: max < min", file=sys.stderr)
            sys.exit(1)

    result = project(pts, bbox=bbox, p=args.p, cos_correct=args.cos)
    print(
        json.dumps(
            {pid: {"x": x, "y": y} for pid, x, y in result},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
