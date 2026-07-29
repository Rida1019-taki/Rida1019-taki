import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"  # bright -> dark

def convert_to_ascii_svg(image_path="source-prepped.png", output_svg="rida-ascii.svg"):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        # Fallback dummy grid if image is not prepared yet
        img = np.full((53, 100), 200, dtype=np.uint8)

    target_cols = 90
    aspect_ratio = img.shape[0] / img.shape[1]
    target_rows = int(target_cols * aspect_ratio * 0.5)

    resized = cv2.resize(img, (target_cols, target_rows))

    char_lines = []
    for row in resized:
        line = ""
        for px in row:
            idx = int((px / 255.0) * (len(RAMP) - 1))
            line += RAMP[idx]
        char_lines.append(line)

    char_width = 7
    char_height = 12
    width = target_cols * char_width + 20
    height = target_rows * char_height + 20

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .bg { fill: #0d1117; }',
        '    .ascii { font-family: monospace; font-size: 11px; fill: #818cf8; white-space: pre; }',
        '    @keyframes wipe { 0% { width: 0%; } 100% { width: 100%; } }',
        '    .row { overflow: hidden; animation: wipe 0.05s forwards; }',
        '  </style>',
        f'  <rect class="bg" width="{width}" height="{height}" rx="8"/>',
        '  <g class="ascii">'
    ]

    for idx, line in enumerate(char_lines):
        y = 20 + (idx * char_height)
        delay = idx * 0.04
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        svg_lines.append(
            f'    <text x="10" y="{y}" style="animation: wipe 0.2s ease-out {delay:.2f}s both;">{escaped_line}</text>'
        )

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"ASCII SVG generated at {output_svg}")

if __name__ == "__main__":
    convert_to_ascii_svg()