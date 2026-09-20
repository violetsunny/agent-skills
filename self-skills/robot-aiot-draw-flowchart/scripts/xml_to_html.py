#!/usr/bin/env python3
"""
xml_to_html.py — draw.io / mxGraph XML 到 HTML 的确定性转换脚本

用法:
    python3 xml_to_html.py <input.xml> [-o <output.html>]

仅使用 Python 标准库，不引入第三方依赖。
"""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from html import escape

# ── 样式映射表 ──────────────────────────────────────────────
# 对应 references/xml-html-mapping.md

SHAPE_MAP = {
    "ellipse": "border-radius: 50%;",
    "rhombus": "transform: rotate(45deg);",
    "cylinder": "border-radius: 50% / 10%;",
    "cylinder3": "border-radius: 50% / 10%;",
    "hexagon": "clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);",
    "triangle": "clip-path: polygon(50% 0%, 0% 100%, 100% 100%);",
}


def parse_style(style_str: str | None) -> dict[str, str]:
    """将 draw.io style 字符串解析为 dict。"""
    if not style_str:
        return {}
    result = {}
    for part in style_str.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            result[k.strip()] = v.strip()
        else:
            result[part] = "1"
    return result


def map_style_to_css(
    style_dict: dict[str, str],
) -> tuple[str, str | None, dict[str, str], list[str]]:
    """将 draw.io style dict 映射为 CSS 字符串，返回 (css_str, shape, edge_info, unmapped_list)。"""
    css_parts = []
    shape = None
    edge_info = {}
    unmapped_list = []

    # shape（兼容 shape= 属性与 draw.io 裸关键字写法，如 "ellipse;whiteSpace=wrap;..."）
    if "shape" in style_dict:
        shape = style_dict["shape"]
        if shape in SHAPE_MAP:
            css_parts.append(SHAPE_MAP[shape])
    else:
        for _kw, _css in SHAPE_MAP.items():
            if style_dict.get(_kw) == "1":
                shape = _kw
                css_parts.append(_css)
                break
        if shape is None and style_dict.get("rounded") == "1":
            css_parts.append("border-radius: 8px;")

    # fillColor
    fill = style_dict.get("fillColor")
    if fill and fill != "none":
        css_parts.append(f"background-color: {fill};")
    elif fill == "none":
        pass  # 透明
    else:
        css_parts.append("background-color: #FFFFFF;")

    # strokeColor
    stroke = style_dict.get("strokeColor")
    if stroke and stroke != "none":
        css_parts.append(f"border-color: {stroke};")
        edge_info["stroke"] = stroke
    elif stroke == "none":
        css_parts.append("border: none;")
    else:
        css_parts.append("border: 1px solid #000000;")

    # fontColor
    font_color = style_dict.get("fontColor")
    if font_color and font_color != "none":
        css_parts.append(f"color: {font_color};")

    # opacity
    opacity = style_dict.get("opacity")
    if opacity is not None:
        try:
            css_parts.append(f"opacity: {int(opacity) / 100};")
        except ValueError:
            warn(f"opacity value not numeric: {opacity}, skipped")

    # dashed
    if style_dict.get("dashed") == "1":
        css_parts.append("border-style: dashed;")
    elif style_dict.get("dashed") == "0":
        css_parts.append("border-style: solid;")

    # shadow
    if style_dict.get("shadow") == "1":
        css_parts.append("box-shadow: 2px 2px 4px rgba(0,0,0,0.2);")

    # strokeWidth
    sw = style_dict.get("strokeWidth")
    if sw:
        css_parts.append(f"border-width: {sw}px;")
        edge_info["stroke_width"] = sw

    # fontSize
    fs = style_dict.get("fontSize")
    if fs:
        css_parts.append(f"font-size: {fs}px;")

    # fontStyle
    fst = style_dict.get("fontStyle", "0")
    try:
        fst_val = int(fst)
        if fst_val & 1:
            css_parts.append("font-weight: bold;")
        if fst_val & 2:
            css_parts.append("font-style: italic;")
        if fst_val & 4:
            css_parts.append("text-decoration: underline;")
    except ValueError:
        pass

    # align
    align = style_dict.get("align")
    if align in ("left", "center", "right"):
        css_parts.append(f"text-align: {align};")

    # verticalAlign
    valign = style_dict.get("verticalAlign")
    if valign in ("top", "middle", "bottom"):
        flex_map = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}
        css_parts.append(f"display: flex; align-items: {flex_map[valign]};")

    # edge-specific
    if style_dict.get("endArrow", "1") in ("0", "none"):
        edge_info["end_arrow"] = False
    else:
        edge_info["end_arrow"] = True

    if style_dict.get("startArrow") in ("classic", "1"):
        edge_info["start_arrow"] = True

    if style_dict.get("dashed") == "1":
        edge_info["dashed"] = True

    # edge label styling（标签背景色/字号/字色/粗体）
    if "labelBackgroundColor" in style_dict:
        edge_info["label_bg"] = style_dict["labelBackgroundColor"]
    if "fontColor" in style_dict:
        edge_info["font_color"] = style_dict["fontColor"]
    if "fontSize" in style_dict:
        edge_info["font_size"] = style_dict["fontSize"]
    try:
        if int(style_dict.get("fontStyle", "0")) & 1:
            edge_info["font_bold"] = True
    except ValueError:
        pass

    # edge connection point offsets
    for coord_key in ("exitX", "exitY", "entryX", "entryY"):
        if coord_key in style_dict:
            try:
                edge_info[coord_key] = float(style_dict[coord_key])
            except ValueError:
                warn(f"Invalid float for {coord_key}={style_dict[coord_key]}, skipped")

    # 安全忽略键：draw.io 模板强制或常见、但对 CSS 渲染无语义影响的键。
    # html=1 富文本语义已由 Vertex.to_html 原样渲染实现；whiteSpace=wrap 是 HTML div 默认行为；
    # arcSize 是 rounded 圆角的百分比微调（rounded 已映射固定圆角）；spacing* 是内边距微调。
    # 这些键不 WARN、不计入 unmapped 报告，避免每次转换产生必然噪音。
    safe_ignore_keys = {
        "html",
        "whiteSpace",
        "arcSize",
        "spacingLeft",
        "spacingRight",
        "spacingTop",
        "spacingBottom",
    }
    # warn on unmapped attributes
    mapped_keys = {
        "shape",
        "rounded",
        "fillColor",
        "strokeColor",
        "fontColor",
        "opacity",
        "dashed",
        "shadow",
        "strokeWidth",
        "fontSize",
        "fontStyle",
        "align",
        "verticalAlign",
        "endArrow",
        "startArrow",
        "exitX",
        "exitY",
        "entryX",
        "entryY",
        "labelBackgroundColor",
        *SHAPE_MAP.keys(),
    }
    for k, v in style_dict.items():
        if k in safe_ignore_keys:
            continue
        if k not in mapped_keys:
            warn(f"Unmapped style attribute: {k}={v}, skipped")
            unmapped_list.append(f"{k}={v}")

    return " ".join(css_parts), shape, edge_info, unmapped_list


def warn(msg: str) -> None:
    """打印警告到 stderr，不阻塞转换。"""
    print(f"[WARN] {msg}", file=sys.stderr)


def _fmt(n: float) -> str:
    """坐标取整到 1 位小数；整数则去掉小数尾，避免浮点噪声（如 743.5999999999999）。"""
    r = round(n, 1)
    return str(int(r)) if r == int(r) else str(r)


def _color_slug(color: str | None) -> str:
    """把颜色转成合法的 CSS id 片段：'#0078D4' -> '0078d4'。"""
    return color.replace("#", "").lower() if color else "000000"


def _estimate_text_width(text: str, font_size: float) -> float:
    """估算文本像素宽度：CJK ≈ fontSize，ASCII ≈ 0.62 × fontSize。"""
    width = 0.0
    for ch in text:
        width += font_size if ord(ch) > 0x2E80 else font_size * 0.62
    return width


def _point_at_half(points: list[tuple[float, float]]) -> tuple[float, float]:
    """返回折线路径总长一半处的坐标，用于多拐点边的标签定位。"""
    segs = []
    total = 0.0
    for (ax, ay), (bx, by) in zip(points, points[1:], strict=False):
        d = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
        segs.append((ax, ay, bx, by, d))
        total += d
    half = total / 2
    for ax, ay, bx, by, d in segs:
        if half <= d:
            t = half / d if d else 0
            return ax + (bx - ax) * t, ay + (by - ay) * t
        half -= d
    return points[-1]


def _clip_to_boundary(
    cx: float, cy: float, w: float, h: float, tx: float, ty: float
) -> tuple[float, float]:
    """从矩形中心 (cx,cy) 朝目标点 (tx,ty) 方向求与矩形边界的交点。

    用于无 exit/entry 锚点的边：draw.io 会自动把连线裁剪到节点边界，
    桥接层需同样处理，否则中心到中心的线段会穿越节点（edge-layer 渲染在节点上层）。
    """
    dx = tx - cx
    dy = ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    scale = float("inf")
    if dx != 0:
        scale = min(scale, (w / 2) / abs(dx))
    if dy != 0:
        scale = min(scale, (h / 2) / abs(dy))
    return cx + dx * scale, cy + dy * scale


# ── XML 解析 ────────────────────────────────────────────────


class Vertex:
    def __init__(
        self,
        cell_id: str,
        value: str,
        x: float,
        y: float,
        w: float,
        h: float,
        style_css: str,
        shape: str | None,
        parent_id: str,
    ) -> None:
        self.cell_id = cell_id
        self.value = value
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.style_css = style_css
        self.shape = shape
        self.parent_id = parent_id
        self.abs_x = x
        self.abs_y = y

    def to_html(self) -> str:
        # draw.io html=1 语义：value 本身是 HTML（<b>/<br>/<font> 等），须完全原样渲染。
        # 禁止任何转义：整体 escape 会把标签变明文；仅转义引号也会破坏内联样式
        # （style=&quot;…&quot; 被浏览器解码为带引号的属性值，CSS 解析失效）。
        text = self.value if self.value else ""
        # 内容包一层块级 div：flex 容器会把 <b>/<font> 等内联子元素提升为并排 flex item
        # 且忽略 <br>，破坏富文本行结构；单块级子项可保留正常块级排版。
        inner = f'<div style="width:100%;">{text}</div>' if text else ""
        return (
            f'    <div class="vertex" id="v-{self.cell_id}" '
            f'style="position:absolute; left:{_fmt(self.abs_x)}px; top:{_fmt(self.abs_y)}px; '
            f'width:{_fmt(self.w)}px; height:{_fmt(self.h)}px; {self.style_css}">'
            f"{inner}</div>\n"
        )


class Edge:
    def __init__(
        self,
        cell_id: str,
        value: str,
        source_id: str,
        target_id: str,
        edge_info: dict[str, str],
        waypoints: list[tuple[float, float]] | None = None,
    ) -> None:
        self.cell_id = cell_id
        self.value = value
        self.source_id = source_id
        self.target_id = target_id
        self.edge_info = edge_info
        self.waypoints = waypoints or []

    def to_svg(self, vertices: dict[str, Vertex]) -> str:
        """生成 SVG line，支持 exitX/exitY/entryX/entryY 连接点偏移。

        无锚点时按节点边界裁剪（与 draw.io 行为一致）：起点取源节点朝向目标的边界交点，
        终点取目标节点朝向起点的边界交点，避免线段穿越节点内部。
        标签渲染：文字下垫背景 rect（labelBackgroundColor，默认白）防止连线贯穿文字；
        箭头按颜色引用 per-color marker（arrow-end-{slug}），坐标统一取整。
        """
        src = vertices.get(self.source_id)
        tgt = vertices.get(self.target_id)
        if not src or not tgt:
            warn(f"Edge {self.cell_id}: missing source or target vertex, skipped")
            return ""

        ei = self.edge_info
        has_exit = "exitX" in ei or "exitY" in ei
        has_entry = "entryX" in ei or "entryY" in ei
        x1 = src.abs_x + ei.get("exitX", 0.5) * src.w
        y1 = src.abs_y + ei.get("exitY", 0.5) * src.h
        x2 = tgt.abs_x + ei.get("entryX", 0.5) * tgt.w
        y2 = tgt.abs_y + ei.get("entryY", 0.5) * tgt.h
        if not has_exit:
            aim = self.waypoints[0] if self.waypoints else (x2, y2)
            x1, y1 = _clip_to_boundary(
                src.abs_x + src.w / 2,
                src.abs_y + src.h / 2,
                src.w,
                src.h,
                aim[0],
                aim[1],
            )
        if not has_entry:
            aim = self.waypoints[-1] if self.waypoints else (x1, y1)
            x2, y2 = _clip_to_boundary(
                tgt.abs_x + tgt.w / 2,
                tgt.abs_y + tgt.h / 2,
                tgt.w,
                tgt.h,
                aim[0],
                aim[1],
            )
        path_points = [(x1, y1)] + list(self.waypoints) + [(x2, y2)]

        stroke = ei.get("stroke", "#000000")
        sw = ei.get("stroke_width", "1.5")
        dash = ' stroke-dasharray="8,4"' if ei.get("dashed") else ""
        slug = _color_slug(stroke)

        # arrow markers（per-color，硬编码 fill，userSpaceOnUse 固定尺寸）
        marker_end = (
            f' marker-end="url(#arrow-end-{slug})"' if ei.get("end_arrow", True) else ""
        )
        marker_start = (
            f' marker-start="url(#arrow-start-{slug})"'
            if ei.get("start_arrow", False)
            else ""
        )

        # label at midpoint with background rect
        label_svg = ""
        if self.value:
            fs = float(ei.get("font_size", "12"))
            if self.waypoints:
                mx, my = _point_at_half(path_points)
            else:
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
            label_text = escape(self.value)
            text_w = _estimate_text_width(self.value, fs)
            pad_x = 4
            pad_y = 2
            bg = ei.get("label_bg", "#FFFFFF")
            font_color = ei.get("font_color", stroke)
            weight = ' font-weight="bold"' if ei.get("font_bold") else ""
            label_svg = (
                f'<rect x="{_fmt(mx - text_w / 2 - pad_x)}" y="{_fmt(my - fs / 2 - pad_y)}" '
                f'width="{_fmt(text_w + pad_x * 2)}" height="{_fmt(fs + pad_y * 2)}" fill="{bg}" />\n'
                f'    <text x="{_fmt(mx)}" y="{_fmt(my + fs * 0.35)}" text-anchor="middle" '
                f'font-size="{_fmt(fs)}" fill="{font_color}"{weight}>{label_text}</text>'
            )

        if self.waypoints:
            pts = " ".join(f"{_fmt(px)},{_fmt(py)}" for px, py in path_points)
            return (
                f'    <polyline points="{pts}" fill="none" '
                f'stroke="{stroke}" stroke-width="{sw}"{dash}{marker_end}{marker_start} />\n'
                f"    {label_svg}"
            )
        return (
            f'    <line x1="{_fmt(x1)}" y1="{_fmt(y1)}" x2="{_fmt(x2)}" y2="{_fmt(y2)}" '
            f'stroke="{stroke}" stroke-width="{sw}"{dash}{marker_end}{marker_start} />\n'
            f"    {label_svg}"
        )


def _reject_unsafe_xml(xml: str, source: str) -> None:
    """拒绝可能触发外部实体扩展的 DTD/ENTITY 声明（与 drawio_extract.py 同口径）。"""
    upper = xml.upper()
    if "<!DOCTYPE" in upper or "<!ENTITY" in upper:
        print(
            f"[ERROR] {source}: DTD and entity declarations are not supported",
            file=sys.stderr,
        )
        sys.exit(2)


def parse_xml(
    xml_path: str,
) -> tuple[dict[str, Vertex], list[Edge], int, int, list[str]]:
    """解析 draw.io XML，返回 (vertices, edges, canvas_w, canvas_h, unmapped_all)。"""
    with open(xml_path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    _reject_unsafe_xml(raw, xml_path)
    root_elem = ET.fromstring(raw)

    # 支持 mxfile 包装或裸 mxGraphModel
    mxgraph = root_elem.find(".//mxGraphModel")
    if mxgraph is None:
        if root_elem.tag == "mxGraphModel":
            mxgraph = root_elem
        else:
            print("[ERROR] No mxGraphModel found in XML", file=sys.stderr)
            sys.exit(1)

    # 画布尺寸 (task 1.7)
    canvas_w = int(mxgraph.get("pageWidth", "1600"))
    canvas_h = int(mxgraph.get("pageHeight", "1100"))

    xml_root = mxgraph.find("root")
    if xml_root is None:
        print("[ERROR] No root element in mxGraphModel", file=sys.stderr)
        sys.exit(1)

    vertices = {}
    edges = []
    parent_map = {}  # cell_id -> parent_id
    unmapped_all = []  # 收集所有未映射属性

    for cell in xml_root.findall("mxCell"):
        cell_id = cell.get("id", "")
        parent_id = cell.get("parent", "")

        # 跳过 id=0 和 id=1 的结构元素
        if cell_id in ("0", "1"):
            continue

        style_str = cell.get("style", "")
        value = cell.get("value", "")
        style_dict = parse_style(style_str)
        style_css, shape, edge_info, unmapped_list = map_style_to_css(style_dict)
        unmapped_all.extend(unmapped_list)

        is_edge = cell.get("edge") == "1"
        is_vertex = cell.get("vertex") == "1"

        geom = cell.find("mxGeometry")
        if geom is None:
            if is_edge:
                warn(f"Edge {cell_id} has no mxGeometry, skipped")
            continue

        if is_edge:
            source_id = cell.get("source", "")
            target_id = cell.get("target", "")
            waypoints = []
            arr = geom.find("Array[@as='points']")
            if arr is not None:
                for pt in arr.findall("mxPoint"):
                    waypoints.append((float(pt.get("x", "0")), float(pt.get("y", "0"))))
            edges.append(
                Edge(cell_id, value, source_id, target_id, edge_info, waypoints)
            )
        elif is_vertex:
            x = float(geom.get("x", "0"))
            y = float(geom.get("y", "0"))
            w = float(geom.get("width", "120"))
            h = float(geom.get("height", "60"))
            vertices[cell_id] = Vertex(
                cell_id, value, x, y, w, h, style_css, shape, parent_id
            )
            parent_map[cell_id] = parent_id

    # 处理 parent-child 相对坐标 → 绝对坐标 (task 1.6)
    # 使用 parent.x/y（原始相对坐标）而非 parent.abs_x/y，避免多层嵌套时重复累加
    for vid, vtx in vertices.items():
        pid = parent_map.get(vid)
        while pid and pid in vertices:
            parent = vertices[pid]
            vtx.abs_x += parent.x
            vtx.abs_y += parent.y
            pid = parent_map.get(pid)

    return vertices, edges, canvas_w, canvas_h, unmapped_all


# ── HTML 生成 ───────────────────────────────────────────────


def generate_html(
    vertices: dict[str, Vertex], edges: list[Edge], canvas_w: int, canvas_h: int
) -> str:
    """生成完整 HTML 文档。"""
    # vertex HTML
    vertex_html = "".join(v.to_html() for v in vertices.values())

    # edge SVG
    edge_svg_lines = "".join(e.to_svg(vertices) for e in edges)

    # arrow markers：只为边实际用到的颜色生成，硬编码 fill（不依赖 context-stroke），
    # markerUnits="userSpaceOnUse" 固定尺寸，避免箭头随线宽放大。
    end_colors = set()
    start_colors = set()
    for e in edges:
        stroke = e.edge_info.get("stroke", "#000000")
        if e.edge_info.get("end_arrow", True):
            end_colors.add(stroke)
        if e.edge_info.get("start_arrow", False):
            start_colors.add(stroke)

    marker_defs = []
    # Arrow size standard: markerWidth = canvas width * 0.9375%, height = width * 0.7.
    arrow_w = f"{canvas_w * 0.009375:.1f}"
    arrow_h = f"{canvas_w * 0.009375 * 0.7:.1f}"
    for color in sorted(end_colors):
        slug = _color_slug(color)
        marker_defs.append(
            f'        <marker id="arrow-end-{slug}" markerWidth="{arrow_w}" markerHeight="{arrow_h}" '
            f'viewBox="0 0 11 8" refX="11" refY="4" orient="auto" markerUnits="userSpaceOnUse">\n'
            f'          <path d="M0,0 L0,8 L11,4 Z" fill="{color}" />\n'
            f"        </marker>"
        )
    for color in sorted(start_colors):
        slug = _color_slug(color)
        marker_defs.append(
            f'        <marker id="arrow-start-{slug}" markerWidth="{arrow_w}" markerHeight="{arrow_h}" '
            f'viewBox="0 0 11 8" refX="0" refY="4" orient="auto" markerUnits="userSpaceOnUse">\n'
            f'          <path d="M11,0 L11,8 L0,4 Z" fill="{color}" />\n'
            f"        </marker>"
        )
    marker_defs_str = "\n".join(marker_defs)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diagram Preview</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 100%; height: 100%; }}
  body {{ background: #f5f5f5; padding: 20px; overflow: auto; }}
  .diagram-stage {{
    width: 100%;
    min-height: calc(100vh - 40px);
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }}
  .diagram-scale-box {{
    position: relative;
    width: {canvas_w}px;
    height: {canvas_h}px;
    transform-origin: top left;
  }}
  .diagram-canvas {{
    position: relative;
    width: {canvas_w}px;
    height: {canvas_h}px;
    background: #FFFFFF;
    border: 1px solid #cccccc;
    overflow: hidden;
    margin: 0 auto;
  }}
  .vertex {{
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    border: 1px solid #000000;
    overflow: hidden;
    padding: 4px;
    box-sizing: border-box;
  }}
  .edge-layer {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }}
</style>
</head>
<body>
  <div class="diagram-stage">
    <div class="diagram-scale-box" id="diagramScaleBox">
      <div class="diagram-canvas">
{vertex_html}    <svg class="edge-layer" width="{canvas_w}" height="{canvas_h}" xmlns="http://www.w3.org/2000/svg">
      <defs>
{marker_defs_str}
      </defs>
{edge_svg_lines}    </svg>
      </div>
    </div>
  </div>
  <script>
    (function() {{
      const canvasWidth = {canvas_w};
      const canvasHeight = {canvas_h};
      const bodyPadding = 40;
      const box = document.getElementById('diagramScaleBox');

      function fitDiagram() {{
        const availableWidth = Math.max(window.innerWidth - bodyPadding, 320);
        const availableHeight = Math.max(window.innerHeight - bodyPadding, 240);
        const scale = Math.min(availableWidth / canvasWidth, availableHeight / canvasHeight, 1);
        box.style.transform = `scale(${{scale}})`;
        box.style.width = `${{canvasWidth * scale}}px`;
        box.style.height = `${{canvasHeight * scale}}px`;
      }}

      window.addEventListener('resize', fitDiagram);
      fitDiagram();
    }})();
  </script>
</body>
</html>"""
    return html


# ── 保真校验 (task 1.8) ─────────────────────────────────────


def verify_fidelity(
    vertices: dict[str, Vertex],
    edges: list[Edge],
    html_content: str,
    unmapped_all: list[str],
) -> None:
    """多维度保真校验：vertex 数量、edge 数量、文本内容、未映射属性报告。"""
    errors = []

    # 1. Vertex 数量校验
    vertex_count = len(vertices)
    html_vertex_count = html_content.count('class="vertex"')
    if vertex_count != html_vertex_count:
        errors.append(
            f"Vertex count mismatch: XML has {vertex_count} vertices, "
            f"HTML has {html_vertex_count} positioned elements"
        )
    else:
        print(f"[OK] Vertices: {vertex_count} match {html_vertex_count} HTML elements")

    # 2. Edge 数量校验（直线 line + 折线 polyline）
    edge_count = len(edges)
    html_edge_count = html_content.count("<line ") + html_content.count("<polyline ")
    if edge_count != html_edge_count:
        errors.append(
            f"Edge count mismatch: XML has {edge_count} edges, "
            f"HTML has {html_edge_count} SVG lines/polylines"
        )
    else:
        print(f"[OK] Edges: {edge_count} match {html_edge_count} SVG lines/polylines")

    # 3. 文本内容校验
    text_missing = []
    for vid, vtx in vertices.items():
        if not vtx.value:
            continue
        expected_text = vtx.value
        if expected_text not in html_content:
            text_missing.append(f"  vertex {vid}: expected '{vtx.value}'")
    if text_missing:
        print(f"[WARN] Text content: {len(text_missing)} vertex text(s) missing:")
        for line in text_missing:
            print(line)
    else:
        print("[OK] Text content: all matched")

    # 4. 未映射属性报告
    if unmapped_all:
        print(f"[INFO] Unmapped attributes ({len(unmapped_all)}):")
        for attr in unmapped_all:
            print(f"  {attr}")
    else:
        print("[OK] Unmapped attributes: none")

    # 结构化报告汇总
    print("\n--- Fidelity Report ---")
    print(f"  Vertices: {vertex_count}")
    print(f"  Edges: {edge_count}")
    print(
        f"  Text: {'all matched' if not text_missing else f'{len(text_missing)} missing'}"
    )
    print(f"  Unmapped: {len(unmapped_all)}")
    print(f"  Result: {'FAIL' if errors else 'WARN' if text_missing else 'PASS'}")

    if errors:
        for e in errors:
            print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


# ── 主入口 ──────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert draw.io / mxGraph XML to fixed-canvas HTML"
    )
    parser.add_argument("input", help="Input XML file path")
    parser.add_argument(
        "-o",
        "--output",
        help="Output HTML file path (default: same dir, same name, .html)",
    )
    args = parser.parse_args()

    input_path = args.input
    if not os.path.isfile(input_path):
        print(f"[ERROR] Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # 默认输出路径：同目录同名 .html (task 1.3)
    if args.output:
        output_path = args.output
    else:
        base = os.path.splitext(input_path)[0]
        output_path = base + ".html"

    # 解析 XML
    vertices, edges, canvas_w, canvas_h, unmapped_all = parse_xml(input_path)

    # 生成 HTML
    html_content = generate_html(vertices, edges, canvas_w, canvas_h)

    # 写入文件（在校验前写入，确保校验失败时用户仍可检查 HTML）
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 保真校验
    verify_fidelity(vertices, edges, html_content, unmapped_all)

    print(f"[OK] HTML generated: {output_path}")
    print(f"     Canvas: {canvas_w}x{canvas_h}px")
    print(f"     Vertices: {len(vertices)}, Edges: {len(edges)}")


if __name__ == "__main__":
    main()
