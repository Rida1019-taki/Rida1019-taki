"""
Convert source-photo.jpg into a clean, positive-polarity monochrome ASCII-art SVG
for dark backgrounds (#1a1714), plus standalone terminal preview (avi-ascii.svg).

Wait: light characters on a dark background carry light/highlights, so bright skin
uses denser characters while shadows, glasses rims, facial features, and background
stay sparse/blank. Neutral studio wall pixels connected to the image border are
segmented cleanly so zero background noise leaks into the portrait.
"""
import html
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "avi-ascii.svg")

COLS = 92
ROWS = 84
CELL_W = 8.4
CELL_H = 9.2
ART_W = round(COLS * CELL_W)   # 773
ART_H = round(ROWS * CELL_H)   # 773 (1:1 aspect ratio matching crop)
PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD

# Light-on-dark density ramp: space -> sparse -> dense
RAMP = " .'`:-=+*x#%@"

BG = "#0e0c0b"
BG2 = "#1a1714"
FRAME = "#2c2622"
TITLE_TEXT = "#8a7e72"
INK = "#d4cbc0"

ROW_DUR = 0.09
STAGGER = 0.018

im_bgr = cv2.imread(SRC)
if im_bgr is None:
    raise FileNotFoundError(f"Could not read source photo: {SRC}")
h, w = im_bgr.shape[:2]

# 1. Remove neutral bright studio wall connected to the outer border
hsv = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2HSV)
gray_full = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)
is_wall = (hsv[:, :, 1] < 24) & (gray_full > 165)
num_labels, labels = cv2.connectedComponents(is_wall.astype(np.uint8) * 255)
border_labels = set()
border_labels.update(np.unique(labels[0, :]))
border_labels.update(np.unique(labels[:, 0]))
border_labels.update(np.unique(labels[:, w - 1]))
border_labels.discard(0)

fg_mask = (~np.isin(labels, list(border_labels))).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
fg_alpha = cv2.GaussianBlur(fg_mask.astype(np.float32) / 255.0, (11, 11), 3.0)

# 2. Balanced head-and-shoulders crop (square-ish so proportions match 1:1 grid)
crop_top, crop_bot = int(h * 0.03), int(h * 0.96)
crop_left, crop_right = int(w * 0.08), int(w * 0.92)
fg_bgr = im_bgr[crop_top:crop_bot, crop_left:crop_right]
alpha = fg_alpha[crop_top:crop_bot, crop_left:crop_right]

# 3. Positive-polarity tone mapping with sharp dark features & subtle rim highlights
g = cv2.cvtColor(fg_bgr, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.1, tileGridSize=(8, 8))
g_eq = clahe.apply(g)

# Use Canny edge highlight only on dark regions (hair curls & coat collar)
# so glasses rims, pupils, and mustache stay crisp dark gaps on bright skin!
edges = cv2.Canny(g_eq, 65, 155).astype(np.float32) / 255.0
edges = cv2.GaussianBlur(edges, (3, 3), 0.7)

lum = g_eq.astype(np.float32) / 255.0
dark_region = np.clip((0.30 - lum) / 0.25, 0.0, 1.0)
toned = np.clip(np.power(lum, 0.92) * 0.90 + 0.04, 0.0, 1.0)
toned = np.clip(toned + edges * 0.22 * dark_region, 0.0, 1.0) * alpha

small = cv2.resize(toned, (COLS, ROWS), interpolation=cv2.INTER_AREA)
small_a = cv2.resize(alpha, (COLS, ROWS), interpolation=cv2.INTER_AREA)

rows_txt = []
for y in range(ROWS):
    # Softly fade bottom 8 rows so shoulders dissolve cleanly into the card
    v_fade = 1.0 if y < ROWS - 8 else max(0.0, (ROWS - 1 - y) / 8.0)
    chars = []
    for x in range(COLS):
        if small_a[y, x] < 0.30:
            chars.append(" ")
            continue
        val = small[y, x] * v_fade
        if val < 0.05:
            chars.append(" ")
            continue
        idx = int(val * (len(RAMP) - 1) + 0.5)
        idx = max(1, min(len(RAMP) - 1, idx))
        chars.append(RAMP[idx])
    rows_txt.append("".join(chars))

STATIC = bool(os.environ.get("STATIC"))
art_top = TITLEBAR_H + PAD * 0.35
font_size = 9.8

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W - 1}" height="{CANVAS_H - 1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{CANVAS_W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
    f'text-anchor="middle">rida@github: ~$ ./portrait.sh</text>'
)

for ry, line in enumerate(rows_txt):
    y = art_top + ry * CELL_H + CELL_H * 0.80
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    safe = html.escape(line)
    text = (
        f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
        f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>'
    )
    if STATIC:
        parts.append(text)
        continue
    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H:.1f}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
    f'rida@github:~$ whoami <tspan fill="{INK}">Rida Taki</tspan></text>'
)
parts.append("</svg>")

svg_out = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg_out)
print("wrote", OUT, len(svg_out), "bytes;", CANVAS_W, "x", CANVAS_H)
