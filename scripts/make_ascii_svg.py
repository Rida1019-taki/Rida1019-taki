# scripts/make_ascii_svg.py
import cv2
import numpy as np
import os

RAMP = " .`:-=+*cs#%@"  # bright -> dark

def convert_to_ascii_svg():
    # Check prepped or original photo
    img_path = "source-prepped.png" if os.path.exists("source-prepped.png") else "source-photo.jpg"
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Error: No image found!")
        return

    # Contrast Boost
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    img = clahe.apply(img)

    target_cols = 75
    aspect_ratio = img.shape[0] / img.shape[1]
    target_rows = int(target_cols * aspect_ratio * 0.45)

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
    width = 370
    height = target_rows * char_height + 30

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .bg { fill: #0d1117; }',
        '    .ascii { font-family: monospace; font-size: 10px; fill: #818cf8; white-space: pre; }',
        '  </style>',
        f'  <rect class="bg" width="{width}" height="{height}" rx="8"/>',
        '  <g class="ascii">'
    ]

    for idx, line in enumerate(char_lines):
        y = 20 + (idx * char_height)
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        svg_lines.append(f'    <text x="10" y="{y}">{escaped_line}</text>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open("rida-ascii.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print("rida-ascii.svg generated successfully!")

if __name__ == "__main__":
    convert_to_ascii_svg()