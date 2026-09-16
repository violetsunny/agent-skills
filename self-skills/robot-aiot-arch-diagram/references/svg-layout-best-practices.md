# SVG Technical Diagram Layout Best Practices

## Universal Layout Rules (Apply to All Styles)

### 1. Component Spacing
- **Minimum clearance between components**: 80px (edge to edge)
- **Minimum clearance for arrow paths**: 60px from component edges
- **Layer vertical spacing**: 120px between horizontal layers
- **Same-layer horizontal spacing**: 100-120px between components

### 2. Arrow Routing & Connection Points

#### Connection Point Rules
- **Never connect arrows to component corners** - use midpoints of edges
- **Entry/exit points**:
  - Top edge: `cx ± offset` where offset = 0 for single arrow, ±30px for multiple
  - Bottom edge: same rule
  - Left/right edges: `cy ± offset`
- **Clearance from corners**: minimum 20px

#### Arrow Path Routing
- **Avoid diagonal lines crossing components** - use orthogonal routing (L-shaped paths)
- **For curved arrows**:
  - Control point should be at least 40px away from any component edge
  - Use intermediate waypoints for complex routing: `M x1,y1 L x2,y2 Q cx,cy x3,y3`
- **Multiple arrows between same layers**: stagger Y-coordinates by 15-20px to avoid overlap

#### Arrow Overlap Prevention
```svg
<!-- Bad: diagonal arrow crosses component -->
<path d="M 200,100 L 600,400"/>

<!-- Good: orthogonal routing around component -->
<path d="M 200,100 L 200,250 L 600,250 L 600,400"/>

<!-- Good: curved with safe control point -->
<path d="M 200,100 Q 400,200 600,400"/>
<!-- Control point (400,200) is 50px+ away from any component -->
```

### 3. Arrow Label Placement
- **Position**: midpoint of arrow path, offset by 5-10px perpendicular to arrow direction
- **Offset first**: move the label 5-10px perpendicular to the arrow so it does not sit on the stroke
- **Background rect fallback**: include only when offsetting cannot avoid another visual element, with:
  - Padding: 4px horizontal, 2px vertical
  - Fill: match background color
  - Opacity: 0.9-0.95
- **Safety distance**: 15px minimum from any component edge
- **Multiple converging arrows**: stagger label positions vertically by 20px

### 4. Component Overlap Detection
Before finalizing SVG, check:
- No component bounding boxes overlap (8px safety margin)
- No arrow paths pass through component interiors (except intentional tunneling with dashed style)
- No text labels overlap with components or other labels

### 5. Z-Index Layering (SVG render order)
```svg
<!-- Render order (top to bottom = back to front): -->
1. Background rect
2. Grouping containers (dashed rects)
3. Arrow paths
4. Arrow label background rects when collision fallback is needed
5. Components (boxes, cylinders, etc.)
6. Component text
7. Arrow label text
8. Legend
```

## Style-Specific Enhancements

### Style-1: Flat Icon Clean
- **Perfect alignment**: snap all coordinates to 8px grid
- **Sharp corners**: rx="8" ry="8" for rounded rects (consistent)
- **Arrows**: thin (1.5-2px), filled polygon markers
- **No shadows**: flat design principle

### Style-6: Claude Official Warm
- **Soft shadows**: `<feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#00000008"/>`
- **Rounded corners**: rx="12" ry="12" (more rounded than Style-1)
- **Arrows**: medium weight (2px), subtle markers

## Validation Checklist

Before exporting PNG, verify:
- [ ] No arrow-component overlaps (visual inspection)
- [ ] Arrow labels are offset from lines; fallback background rects are used only where needed
- [ ] Minimum 60px clearance for all arrow paths
- [ ] Component spacing ≥ 80px
- [ ] Arrow connection points avoid corners (≥20px from corner)
- [ ] Multiple arrows between layers are staggered
- [ ] Legend is readable and doesn't overlap content
- [ ] SVG renders cleanly via `cairosvg` (or `rsvg-convert` as fallback)

## Common Anti-Patterns to Avoid

| Anti-Pattern | Fix |
|--------------|-----|
| Arrow crosses component | Use orthogonal routing, increase control point distance |
| Label overlaps component | Increase offset; add a matching-background rect if the collision remains |
| Components too close | Increase spacing to 80px minimum |
| Arrow connects to corner | Move connection point to edge midpoint offset |
| No z-index planning | Follow render order: arrows -> components -> text |

## Line Overlap Prevention (jump-over)

When two arrows must cross, ALWAYS use jump-over arcs to prevent visual overlap:

- Crossing horizontal arrows: add a small semicircle arc (radius 5px, stroke same color as arrow, fill none) that "jumps over" the other line.
- SVG pattern for jump-over: use a white/matching-background arc on the lower layer, then draw the upper arc on top.
- Multiple crossings: stagger arc radii (5px, 7px, 9px) so arcs don't overlap each other.
- Never let two arrows' straight-line segments cross without a jump-over arc.

## SVG Technical Rules

- ViewBox: `0 0 960 600` default; `0 0 960 800` tall; `0 0 1200 600` wide.
- Fonts: embed via `<style>font-family: ...</style>` — no external `@import` (cairosvg / rsvg-convert cannot fetch external URLs).
- `<defs>`: arrow markers, gradients, filters, clip paths.
- Text: minimum 12px, prefer 13-14px labels, 11px sub-labels, 16-18px titles.
- All arrows: `<marker>` with `markerEnd`, sized `markerWidth="10" markerHeight="7"`.
- Drop shadows: `<feDropShadow>` in `<filter>`, apply sparingly (key nodes only).
- Curved paths: use `M x1,y1 C cx1,cy1 cx2,cy2 x2,y2` cubic bezier for loops/feedback arrows.
- Clip content: use `<clipPath>` if text might overflow a node box.
- Filter boundary safety: for every element with `filter="url(...)"`, keep it at least `max(20% of element size, shadow blur radius × 3)` away from viewBox edges, or the edge-side stroke gets clipped (one side of the border vanishes).

## Post-Generation Arrow Optimization

When a user asks to "优化箭头" / "fix arrow routing" / "optimize the diagram" on an already-generated diagram, preserve all nodes, containers, styles, and layout — only modify the `arrows` entries in the JSON data, then re-render with `scripts/generate-from-template.py`.

Available arrow override fields (in recommended order of use):

| Field | Type | When to Use |
|-------|------|-------------|
| `source_port` / `target_port` | `"left"` / `"right"` / `"top"` / `"bottom"` | Arrow exits/enters from the wrong edge |
| `corridor_x` | `[x, ...]` | Hint vertical segments toward this x lane (soft preference) |
| `corridor_y` | `[y, ...]` | Hint horizontal segments toward this y lane (soft preference) |
| `route_points` | `[[x1,y1], [x2,y2], ...]` | Exact ordered waypoints; each leg is routed orthogonally and unsafe points are rejected |
| `routing_padding` | number (default: 24) | *(Advanced)* Adjust obstacle clearance for this arrow |
| `port_clearance` | number | *(Advanced)* Adjust first-segment offset from node edge |
| `label_style` | `"badge"` / `"offset"` | Choose `"offset"` when badge backgrounds create visual clutter; keep `"badge"` (default) for legacy/high-contrast labels |

For JSON/template rendering, the default remains `"badge"` for backward compatibility. Set `"label_style": "offset"` on individual arrows for offset-first labels without background rects.

Optimization steps:

1. Read the existing SVG — identify which arrows overlap, cross nodes, or look misaligned.
2. Find those arrows in the JSON data by `source` / `target` pair.
3. Add `source_port` / `target_port` if the exit/entry direction is wrong; add `corridor_x` / `corridor_y` to space parallel arrows apart; use `route_points` only when hints alone cannot resolve the path.
4. Re-run `generate-from-template.py` with the updated JSON and validate with `validate-svg.sh`.

Example — spacing two overlapping arrows into separate corridors:

```json
{ "source": "nodeA", "target": "nodeB", "corridor_y": [280] }
{ "source": "nodeC", "target": "nodeD", "corridor_y": [320] }
```

## SVG Generation & Error Prevention

**MANDATORY: Python List Method** (ALWAYS use this for hand-written SVG):

```python
python3 << 'EOF'
lines = []
lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700">')
lines.append('  <defs>')
# ... each line separately
lines.append('</svg>')

with open('/path/to/output.svg', 'w') as f:
    f.write('\n'.join(lines))
print("SVG generated successfully")
EOF
```

Why mandatory: prevents character truncation, typos, and syntax errors. Each line is independent and easy to verify.

**Pre-Tool-Call Checklist** (use EVERY time):

1. Can I write out the COMPLETE command/content right now?
2. Do I have ALL required parameters ready?
3. Have I checked for syntax errors in my prepared content?

If ANY answer is NO: STOP. Do NOT call the tool. Prepare the content first.

**Error Recovery Protocol**:

- First error: analyze root cause, apply targeted fix.
- Second error: switch method entirely (Python list → chunked generation).
- Third error: STOP and report to user — do NOT loop endlessly.
- Never: retry the same failing command or call tools with empty parameters.

**Common Syntax Errors to Avoid**:

- ❌ `yt-anchor` → ✅ `y="60" text-anchor="middle"`
- ❌ `x="390` (missing y) → ✅ `x="390" y="250"`
- ❌ `fill=#fff` → ✅ `fill="#ffffff"`
- ❌ `marker-end=` → ✅ `marker-end="url(#arrow)"`
- ❌ `L 29450` → ✅ `L 290,220`
- ❌ Missing `</svg>` at end

**Validation** (run after generation):

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')" && echo "✓ Valid XML"
# Or use cairosvg as a render-time check:
python3 -c "import cairosvg; cairosvg.svg2png(url='file.svg', write_to='/tmp/test.png')" && echo "✓ Renders" && rm /tmp/test.png
```
