#!/usr/bin/env python3
"""
xml_to_html.py — draw.io / mxGraph XML 到 HTML 的确定性转换脚本

用法:
    python3 xml_to_html.py <input.xml> [-o <output.html>]

仅使用 Python 标准库，不引入第三方依赖。
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
from html import escape


# ── 样式映射表 ──────────────────────────────────────────────
# 对应 references/xml-html-mapping.md

SHAPE_MAP = {
    "ellipse": "border-radius: 50%;",
    "rhombus": "transform: rotate(45deg);",
    "cylinder": "border-radius: 50% / 10%;",
    "hexagon": "clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);",
    "triangle": "clip-path: polygon(50% 0%, 0% 100%, 100% 100%);",
}


def parse_style(style_str):
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


def map_style_to_css(style_dict):
    """将 draw.io style dict 映射为 CSS 字符串，返回 (css_str, shape, edge_info, unmapped_list)。"""
    css_parts = []
    shape = None
    edge_info = {}
    unmapped_list = []

    # shape
    if "shape" in style_dict:
        shape = style_dict["shape"]
        if shape in SHAPE_MAP:
            css_parts.append(SHAPE_MAP[shape])
    elif style_dict.get("rounded") == "1":
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

    # edge connection point offsets
    for coord_key in ("exitX", "exitY", "entryX", "entryY"):
        if coord_key in style_dict:
            try:
                edge_info[coord_key] = float(style_dict[coord_key])
            except ValueError:
                warn(f"Invalid float for {coord_key}={style_dict[coord_key]}, skipped")

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
    }
    for k, v in style_dict.items():
        if k not in mapped_keys:
            warn(f"Unmapped style attribute: {k}={v}, skipped")
            unmapped_list.append(f"{k}={v}")

    return " ".join(css_parts), shape, edge_info, unmapped_list


def warn(msg):
    """打印警告到 stderr，不阻塞转换。"""
    print(f"[WARN] {msg}", file=sys.stderr)


# ── XML 解析 ────────────────────────────────────────────────


class Vertex:
    def __init__(self, cell_id, value, x, y, w, h, style_css, shape, parent_id):
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

    def to_html(self):
        text = self.value if self.value else ""
        return (
            f'    <div class="vertex" id="v-{self.cell_id}" '
            f'style="position:absolute; left:{self.abs_x}px; top:{self.abs_y}px; '
            f'width:{self.w}px; height:{self.h}px; {self.style_css}">'
            f"{text}</div>\n"
        )


class Edge:
    def __init__(self, cell_id, value, source_id, target_id, edge_info):
        self.cell_id = cell_id
        self.value = value
        self.source_id = source_id
        self.target_id = target_id
        self.edge_info = edge_info

    def to_svg(self, vertices):
        """生成 SVG line，支持 exitX/exitY/entryX/entryY 连接点偏移，无偏移时回退中心到中心。"""
        src = vertices.get(self.source_id)
        tgt = vertices.get(self.target_id)
        if not src or not tgt:
            warn(f"Edge {self.cell_id}: missing source or target vertex, skipped")
            return ""

        ei = self.edge_info
        x1 = src.abs_x + ei.get("exitX", 0.5) * src.w
        y1 = src.abs_y + ei.get("exitY", 0.5) * src.h
        x2 = tgt.abs_x + ei.get("entryX", 0.5) * tgt.w
        y2 = tgt.abs_y + ei.get("entryY", 0.5) * tgt.h

        stroke = self.edge_info.get("stroke", "#000000")
        sw = self.edge_info.get("stroke_width", "1.5")
        dash = ' stroke-dasharray="8,4"' if self.edge_info.get("dashed") else ""

        # arrow markers
        marker_end = (
            ' marker-end="url(#arrow-end)"'
            if self.edge_info.get("end_arrow", True)
            else ""
        )
        marker_start = (
            ' marker-start="url(#arrow-start)"'
            if self.edge_info.get("start_arrow", False)
            else ""
        )

        # label at midpoint
        label_svg = ""
        if self.value:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            label_text = self.value
            label_svg = f'<text x="{mx}" y="{my - 6}" text-anchor="middle" font-size="12" fill="{stroke}">{label_text}</text>'

        return (
            f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{sw}"{dash}{marker_end}{marker_start} />\n'
            f"    {label_svg}"
        )


def parse_xml(xml_path):
    """解析 draw.io XML，返回 (vertices, edges, canvas_w, canvas_h, unmapped_all)。"""
    tree = ET.parse(xml_path)
    root_elem = tree.getroot()

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
            edges.append(Edge(cell_id, value, source_id, target_id, edge_info))
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


def generate_html(vertices, edges, canvas_w, canvas_h):
    """生成完整 HTML 文档。"""
    # vertex HTML
    vertex_html = "".join(v.to_html() for v in vertices.values())

    # edge SVG
    edge_svg_lines = "".join(e.to_svg(vertices) for e in edges)

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
        <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
          <path d="M0,0 L0,6 L9,3 Z" fill="context-stroke" />
        </marker>
        <marker id="arrow-start" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto">
          <path d="M9,0 L9,6 L0,3 Z" fill="context-stroke" />
        </marker>
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


def verify_fidelity(vertices, edges, html_content, unmapped_all):
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

    # 2. Edge 数量校验
    edge_count = len(edges)
    html_edge_count = html_content.count("<line ")
    if edge_count != html_edge_count:
        errors.append(
            f"Edge count mismatch: XML has {edge_count} edges, "
            f"HTML has {html_edge_count} SVG lines"
        )
    else:
        print(f"[OK] Edges: {edge_count} match {html_edge_count} SVG lines")

    # 3. 文本内容校验
    text_missing = []
    for vid, vtx in vertices.items():
        if not vtx.value:
            continue
        if vtx.value not in html_content:
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
    print(f"\n--- Fidelity Report ---")
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


def main():
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
