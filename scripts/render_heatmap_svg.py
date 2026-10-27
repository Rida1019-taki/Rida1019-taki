#!/usr/bin/env python3
"""
Render data/contributions.json as a premium burgundy-themed GitHub contribution heatmap SVG.
Grid of rounded, colored boxes in the classic 53-week x 7-day calendar,
revealed with a diagonal cascading animation (CSS keyframes), Less->More legend,
and real stats footer.
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATHS = [
    os.path.join(HERE, "..", "assets", "sushmita-contrib-heatmap.svg"),
    os.path.join(HERE, "..", "contrib-heatmap.svg"),
]

# Burgundy color palette
PALETTE = [
    "#190B12",  # Level 0 (dark wine empty)
    "#451126",  # Level 1 (burgundy)
    "#701A3D",  # Level 2 (wine accent)
    "#A22B58",  # Level 3 (vivid wine)
    "#C77B9B",  # Level 4 (rose)
    "#E5B5C7",  # Level 5 (pale rose highlight)
]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 24
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 34

BG = "#10070C"       # Midnight
BG2 = "#190B12"      # Dark wine
BORDER = "#451126"   # Deep burgundy stroke
BORDER_ACC = "#701A3D"
MUTED = "#8E5B70"    # Muted rose
TEXT = "#F8F0F3"     # Ivory
ACCENT = "#C77B9B"   # Rose
GOLD = "#E5B5C7"     # Pale rose

COL_T = 0.016
ROW_T = 0.040
CELL_DUR = 0.45

def level_for(count):
    if count == 0:
        return 0
    if count <= 2:
        return 1
    if count <= 6:
        return 2
    if count <= 12:
        return 3
    if count <= 20:
        return 4
    return 5

def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid

def render(data):
    days = data["days"]
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 88
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes bcell {{
  0%   {{ opacity: 0; transform: translateY(-5px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
.bc {{ opacity: 0; animation: bcell {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both; }}
@media (prefers-reduced-motion: reduce) {{
  .bc {{ opacity: 1 !important; animation: none !important; }}
}}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG2}"/><stop offset="100%" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="14" fill="url(#bgGrad)"/>',
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="14" '
        f'fill="none" stroke="{BORDER_ACC}" stroke-width="1.2" stroke-opacity="0.45"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{BORDER}" stroke-opacity="0.5"/>',
    ]

    for i, dotcol in enumerate(["#701A3D", "#A22B58", "#C77B9B"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle" font-weight="600">rida@matrix: ~/contributions --verified-activity</text>')

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text x="{x}" y="{TITLEBAR_H + 14}" fill="{MUTED}" font-size="10">{label}</text>')

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{wname}</text>')

    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            parts.append(
                f'<rect class="bc" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{PALETTE[lvl]}" stroke="{BORDER}" stroke-width="0.5" stroke-opacity="0.3" '
                f'style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    leg_y = grid_top + art_h + 8
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL - 1) + 70)
    parts.append(f'<text x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for lvl, color in enumerate(PALETTE):
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="{CELL-1}" height="{CELL-1}" rx="2.2" fill="{color}" stroke="{BORDER}" stroke-width="0.5"/>')
        lx += CELL
    parts.append(f'<text x="{lx + 4}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10">More</text>')

    sep_y = leg_y + CELL + 14
    parts.append(f'<line x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" stroke="{BORDER}" stroke-opacity="0.35"/>')

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    best = data["best_day"]
    rng = data["range"]
    active_days = data.get("active_days", sum(1 for d in days if d["count"] > 0))

    ly = sep_y + 24
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{ACCENT}">'
                 f'<tspan font-weight="700">{total:,}</tspan>'
                 f'<tspan fill="{MUTED}"> contributions in the last year ({active_days} active days)</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
                 f'{rng["start"]} &#8594; {rng["end"]}</text>')
    ly += 24
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{MUTED}">current streak '
                 f'<tspan fill="{GOLD}" font-weight="700">{cs} days</tspan>'
                 f'<tspan fill="{MUTED}">   &#183;   longest </tspan>'
                 f'<tspan fill="{GOLD}" font-weight="700">{ls} days</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
                 f'peak day <tspan fill="{ACCENT}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')

    parts.append("</svg>")
    return "".join(parts)

if __name__ == "__main__":
    data = json.load(open(IN_PATH))
    svg = render(data)
    for p in OUT_PATHS:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {p} ({len(svg)} bytes)")
