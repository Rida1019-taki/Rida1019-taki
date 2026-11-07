#!/usr/bin/env python3
"""
Render data/contributions.json as a GitHub contribution heatmap SVG.
Supports both classic/burgundy and One Piece Grand Line Ocean themes.
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 24
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 34

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

def render(data, theme="onepiece"):
    if theme == "onepiece":
        palette = ["#0B1322", "#1E3A8A", "#0284C7", "#D97706", "#F59E0B", "#FFD700"]
        bg = "#070C16"
        bg2 = "#0F172A"
        border = "#1E293B"
        border_acc = "#334155"
        muted = "#64748B"
        text = "#F8FAFC"
        accent = "#38BDF8"
        gold = "#FFD700"
        title_text = "rida@thousand-sunny:~ (grand_line_log)"
    else:
        palette = ["#190B12", "#451126", "#701A3D", "#A22B58", "#C77B9B", "#E5B5C7"]
        bg = "#10070C"
        bg2 = "#190B12"
        border = "#451126"
        border_acc = "#701A3D"
        muted = "#8E5B70"
        text = "#F8F0F3"
        accent = "#C77B9B"
        gold = "#E5B5C7"
        title_text = "rida@matrix:~ (neofetch)"

    days = data["days"]
    by_date = {d["date"]: d["count"] for d in days}
    start = datetime.date.fromisoformat(data["range"]["start"])
    end = datetime.date.fromisoformat(data["range"]["end"])

    first_sunday = start - datetime.timedelta(days=(start.weekday() + 1) % 7)
    weeks = []
    cur = first_sunday
    while cur <= end:
        col = []
        for row in range(7):
            d = cur + datetime.timedelta(days=row)
            if d < start or d > end:
                col.append(None)
            else:
                ds = d.isoformat()
                c = by_date.get(ds, 0)
                col.append((ds, c, level_for(c)))
        weeks.append(col)
        cur += datetime.timedelta(days=7)

    num_cols = len(weeks)
    art_w = LEFT_LABEL_W + num_cols * STEP
    art_h = TOP_LABEL_H + 7 * STEP
    canvas_w = art_w + 2 * PAD
    canvas_h = TITLEBAR_H + art_h + 2 * PAD + 74

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        "<style>",
        f".card {{ fill: {bg}; stroke: {border}; stroke-width: 1.2px; rx: 16px; }}",
        f".title-bar {{ fill: {bg2}; rx: 16px 16px 0 0; }}",
        ".dot-1 { fill: #EF4444; }",
        ".dot-2 { fill: #F59E0B; }",
        ".dot-3 { fill: #10B981; }",
        f".text-title {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 12.5px; fill: {muted}; font-weight: 600; }}",
        f"text {{ font-family: ui-monospace, Menlo, Consolas, monospace; fill: {text}; }}",
        "@keyframes pop {",
        "  0% { transform: scale(0.2); opacity: 0; }",
        "  70% { transform: scale(1.15); opacity: 1; }",
        "  100% { transform: scale(1); opacity: 1; }",
        "}",
        f".bc {{ animation: pop {CELL_DUR}s cubic-bezier(0.34, 1.56, 0.64, 1) both; transform-box: fill-box; transform-origin: center; }}",
        "@media (prefers-reduced-motion: reduce) { .bc { animation: none !important; opacity: 1 !important; transform: none !important; } }",
        "</style>",
        f'<rect class="card" width="{canvas_w}" height="{canvas_h}"/>',
        f'<rect class="title-bar" width="{canvas_w}" height="{TITLEBAR_H}"/>',
        '<circle class="dot-1" cx="20" cy="17" r="5"/>',
        '<circle class="dot-2" cx="36" cy="17" r="5"/>',
        '<circle class="dot-3" cx="52" cy="17" r="5"/>',
        f'<text class="text-title" x="72" y="21">{title_text}</text>',
    ]

    months_labels = []
    prev_m = None
    for ci, col in enumerate(weeks):
        for cell in col:
            if cell is not None:
                d = datetime.date.fromisoformat(cell[0])
                if d.month != prev_m and d.day <= 14:
                    months_labels.append((ci, d.strftime("%b")))
                    prev_m = d.month
                break

    grid_left = PAD + LEFT_LABEL_W
    grid_top = TITLEBAR_H + PAD + TOP_LABEL_H

    for ci, name in months_labels:
        x = grid_left + ci * STEP
        y = TITLEBAR_H + PAD + 12
        parts.append(f'<text x="{x}" y="{y}" fill="{muted}" font-size="10">{name}</text>')

    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for row, name in day_labels:
        y = grid_top + row * STEP + CELL * 0.8
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{muted}" font-size="10">{name}</text>')

    for ci, column in enumerate(weeks):
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
                f'fill="{palette[lvl]}" stroke="{border}" stroke-width="0.5" stroke-opacity="0.3" '
                f'style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    leg_y = grid_top + art_h + 8
    leg_x = canvas_w - PAD - (len(palette) * (CELL - 1) + 70)
    parts.append(f'<text x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" fill="{muted}" font-size="10" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for lvl, color in enumerate(palette):
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="{CELL-1}" height="{CELL-1}" rx="2.2" fill="{color}" stroke="{border}" stroke-width="0.5"/>')
        lx += CELL
    parts.append(f'<text x="{lx + 4}" y="{leg_y + CELL*0.8:.1f}" fill="{muted}" font-size="10">More</text>')

    sep_y = leg_y + CELL + 14
    parts.append(f'<line x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" stroke="{border}" stroke-opacity="0.35"/>')

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    best = data["best_day"]
    rng = data["range"]
    active_days = data.get("active_days", sum(1 for d in days if d["count"] > 0))

    ly = sep_y + 24
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{accent}">'
                 f'<tspan font-weight="700">{total:,}</tspan>'
                 f'<tspan fill="{muted}"> contributions charted over the past year ({active_days} active days)</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{muted}" text-anchor="end">'
                 f'{rng["start"]} &#8594; {rng["end"]}</text>')
    ly += 24
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{muted}">current streak '
                 f'<tspan fill="{gold}" font-weight="700">{cs} days</tspan>'
                 f'<tspan fill="{muted}">   &#183;   longest </tspan>'
                 f'<tspan fill="{gold}" font-weight="700">{ls} days</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{muted}" text-anchor="end">'
                 f'peak day <tspan fill="{accent}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')

    parts.append("</svg>")
    return "".join(parts)

if __name__ == "__main__":
    data = json.load(open(IN_PATH))
    
    # Generate onepiece heatmap
    op_svg = render(data, theme="onepiece")
    with open(os.path.join(HERE, "..", "assets", "onepiece-heatmap.svg"), "w", encoding="utf-8") as f:
        f.write(op_svg)
    with open(os.path.join(HERE, "..", "contrib-heatmap.svg"), "w", encoding="utf-8") as f:
        f.write(op_svg)
    print("Generated onepiece-heatmap.svg successfully.")
