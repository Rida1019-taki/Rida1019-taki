import json

PALETTE = ["#161b22", "#312e81", "#4338ca", "#6366f1", "#818cf8", "#c4b5fd"]

def render_heatmap(json_path="data/contributions.json", output_svg="contrib-heatmap.svg"):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {"days": []}

    days = data.get("days", [])
    width = 860
    height = 160

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .bg { fill: #0d1117; rx: 8px; stroke: #30363d; stroke-width: 1px; }',
        '    .title { font-family: monospace; font-size: 13px; fill: #a78bfa; font-weight: bold; }',
        '    @keyframes slideIn { from { opacity: 0; transform: scale(0.3); } to { opacity: 1; transform: scale(1); } }',
        '    .box { animation: slideIn 0.3s ease-out forwards; opacity: 0; }',
        '  </style>',
        f'  <rect class="bg" width="{width}" height="{height}" />',
        '  <text class="title" x="20" y="25">rida@github:~ $ ./contributions.sh --53-weeks</text>',
        '  <g transform="translate(20, 40)">'
    ]

    col = 0
    row = 0
    for idx, day in enumerate(days[-371:]):  # 53 weeks * 7
        x = col * 15
        y = row * 15
        level = min(day.get("level", 0), 5)
        color = PALETTE[level]
        delay = (col + row) * 0.015

        svg_lines.append(
            f'    <rect class="box" x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}" '
            f'style="animation-delay: {delay:.3f}s;" />'
        )

        row += 1
        if row >= 7:
            row = 0
            col += 1

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Heatmap SVG generated at {output_svg}")

if __name__ == "__main__":
    render_heatmap()