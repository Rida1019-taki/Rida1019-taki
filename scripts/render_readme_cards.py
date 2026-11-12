#!/usr/bin/env python3
"""
Render Rida Taki's GitHub profile README cards as animated SVGs into cards/.

Matched to https://www.ridataki.dev/ (warm dark obsidian #1a1714, ivory ink
#f2ece4, terracotta #e07040, luxury gold #d4a853, sapphire blue #5a8fd4;
Plus Jakarta Sans, Outfit, JetBrains Mono).

Every card is a standalone SVG shown through <img>, so it uses only what GitHub
allows there: inline CSS keyframes, SMIL <animate>/<set> elements, and subset
WOFF fonts embedded as base64 data URIs (no JS, no external requests).

Live numbers come from data/contributions.json (fetch_contributions.py) and
GitHub's public REST API (with offline fallbacks). Set STATIC=1 to render the
final end-state frame for screenshots/previews.
"""
import base64
import datetime
import json
import os
import re
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "cards")
FONTS = os.path.join(ROOT, "fonts")
PORTRAIT = os.path.join(ROOT, "avi-ascii.svg")

USERNAME = os.environ.get("GH_PROFILE_USER", "Rida1019-taki")
SITE_URL = "www.ridataki.dev"

# ---- fallback counts (overridden live from GitHub API when reachable) -------
DEFAULT_PUBLIC_REPOS = 45
HACKATHONS_COUNT = "3"
CERTS_COUNT = "3"

# ---- brand tokens (matched to www.ridataki.dev) -------------------------
BG = "#0e0c0b"
SURFACE = "#1a1714"
SURFACE_2 = "#231f1b"
BORDER = "#2c2622"
INK = "#f2ece4"
INK_SOFT = "#d4cbc0"
MUTED = "#8a7e72"
RULE = "#2c2622"

BRAND = "#e07040"       # Terracotta Orange (--brand)
BRAND_LIGHT = "#f0945a"
GOLD = "#d4a853"        # Luxury Gold (--accent-gold)
BLUE = "#5a8fd4"        # Sapphire Blue (--accent-blue)
EMERALD = "#5ab88a"     # Emerald (--accent-emerald)

W = 880  # full README column width

HEADING = "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif"
SANS = "'Outfit', system-ui, -apple-system, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"

FONT_FILES = {
    "head-600": ("Plus Jakarta Sans", "normal", 600, "jakarta-600.woff"),
    "head-700": ("Plus Jakarta Sans", "normal", 700, "jakarta-700.woff"),
    "head-700-i": ("Plus Jakarta Sans", "italic", 700, "jakarta-700-i.woff"),
    "head-800": ("Plus Jakarta Sans", "normal", 800, "jakarta-800.woff"),
    "head-800-i": ("Plus Jakarta Sans", "italic", 800, "jakarta-800-i.woff"),
    "sans-400": ("Outfit", "normal", 400, "outfit-400.woff"),
    "sans-600": ("Outfit", "normal", 600, "outfit-600.woff"),
    "mono-400": ("JetBrains Mono", "normal", 400, "jetbrains-400.woff"),
}

BASE_CSS = """
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.15)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes nudge{0%,100%{transform:none}50%{transform:translateX(4px)}}
@keyframes nudgeup{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}
.r{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) both;transform-box:fill-box}
.f{opacity:0;animation:fade .9s ease-out both}
.g{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.7,.2,1) both}
.p{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s ease-out both}
.live{animation:pulse 1.6s ease-in-out infinite}
.n{transform-box:fill-box;animation:nudge 1.8s ease-in-out infinite}
.nu{transform-box:fill-box;animation:nudgeup 1.8s ease-in-out infinite}
@keyframes tilein{0%{opacity:0;transform:translateY(90px) scale(.6) rotate(-9deg)}55%{opacity:1;transform:translateY(-10px) scale(1.05) rotate(2deg)}75%{transform:translateY(3px) scale(.98) rotate(-.8deg)}90%{transform:translateY(-1px) scale(1.01) rotate(.2deg)}100%{opacity:1;transform:none}}
@keyframes slidein{from{opacity:0;transform:translateX(-26px)}to{opacity:1;transform:none}}
@keyframes arrowin{0%{opacity:0;transform:translateX(-30px)}60%{opacity:1;transform:translateX(6px)}100%{opacity:1;transform:none}}
@keyframes roll{from{transform:translateY(60px)}to{transform:none}}
@keyframes sheen{0%{transform:translateX(-260px) skewX(-20deg)}22%,100%{transform:translateX(420px) skewX(-20deg)}}
@keyframes ring{0%{opacity:.7;transform:scale(.2)}100%{opacity:0;transform:scale(2.4)}}
.ti{opacity:0;transform-box:fill-box;transform-origin:50% 60%;animation:tilein 1.1s cubic-bezier(.2,.8,.2,1) both}
.sl{opacity:0;transform-box:fill-box;animation:slidein .6s cubic-bezier(.2,.7,.2,1) both}
.ai{opacity:0;transform-box:fill-box;animation:arrowin .7s cubic-bezier(.2,.7,.2,1) both}
.ro{transform-box:fill-box;animation:roll .8s cubic-bezier(.15,.8,.2,1) both}
.sh{animation:sheen 5s ease-in-out infinite}
.rg{opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 1s ease-out both}
@media (prefers-reduced-motion: reduce){.r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai,.ro,.rg{animation:none!important;opacity:1!important;transform:none!important}.sh,.rg,.cu-mid{display:none}.cu-end{opacity:1!important}}
"""

GAP = 12
BOTTOM = 12


def font_face(keys):
    out = []
    for k in keys:
        fam, style, weight, fn = FONT_FILES[k]
        with open(os.path.join(FONTS, fn), "rb") as fp:
            b64 = base64.b64encode(fp.read()).decode()
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"src:url(data:font/woff;base64,{b64}) format('woff')}}"
        )
    return "".join(out)


def svg(w, h, body, fonts, label, extra_css="", left=0, right=0, bottom=BOTTOM):
    """Card of w x h drawn at x=left inside a transparent canvas, padded so rows tile cleanly."""
    if left:
        body = f'<g transform="translate({left:.3f} 0)">{body}</g>'
    w_tot, h_tot = w + left + right, h + bottom
    css = font_face(fonts) + BASE_CSS + extra_css
    if os.environ.get("STATIC"):
        css += (
            ".r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai,.ro"
            "{animation:none!important;opacity:1!important;transform:none!important}"
            ".sh,.rg{display:none}"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_tot:.3f}" height="{h_tot}" '
        f'viewBox="0 0 {w_tot:.3f} {h_tot}" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title><style>{css}</style>{body}</svg>"
    )


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote cards/{name} ({len(content) // 1024} KB)")


def d(s):
    return f'style="animation-delay:{s:.2f}s"'


def wrap(text, n):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > n:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def text_lines(x, y, lines, lh, attrs):
    return "".join(
        f'<text x="{x}" y="{y + i * lh}" {attrs}>{escape(l)}</text>'
        for i, l in enumerate(lines)
    )


# ---- 1 · hero -----------------------------------------------------------------
def hero():
    h = 420
    with open(PORTRAIT, "r", encoding="utf-8") as f:
        src = f.read()
    rows = re.findall(
        r'<text xml:space="preserve"[^>]*\by="([\d.]+)"[^>]*>(.*?)</text>',
        src,
        re.S,
    )
    portrait = []
    for i, (y, txt) in enumerate(rows):
        portrait.append(
            f'<text class="f" style="animation-delay:{0.25 + i * 0.014:.3f}s;animation-duration:.35s" '
            f'xml:space="preserve" x="20" y="{y}" fill="{INK_SOFT}" font-size="9.8" '
            f'textLength="773" lengthAdjust="spacing">{txt}</text>'
        )
    s = 0.45
    body = f"""
<defs>
  <clipPath id="hero-clip"><rect width="{W}" height="{h}" rx="14"/></clipPath>
  <radialGradient id="orb-brand" cx="80%" cy="28%" r="48%">
    <stop offset="0" stop-color="{BRAND}" stop-opacity=".16"/>
    <stop offset="1" stop-color="{BRAND}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="orb-gold" cx="18%" cy="88%" r="42%">
    <stop offset="0" stop-color="{GOLD}" stop-opacity=".10"/>
    <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">
    <stop offset="0" stop-color="{INK}"/><stop offset=".38" stop-color="{INK}"/>
    <stop offset=".48" stop-color="{BRAND}"/><stop offset=".54" stop-color="{GOLD}"/>
    <stop offset=".62" stop-color="{INK}"/><stop offset="1" stop-color="{INK}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;600 0"
      keyTimes="0;.45;1" dur="7s" begin="1.6s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<g clip-path="url(#hero-clip)">
  <rect width="{W}" height="{h}" fill="{SURFACE}"/>
  <rect width="{W}" height="{h}" fill="url(#orb-brand)"/>
  <rect width="{W}" height="{h}" fill="url(#orb-gold)"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14" fill="none" stroke="{BORDER}"/>
<g class="f" {d(0)}>
  <rect class="live" x="48" y="48" width="8" height="8" rx="2" fill="{EMERALD}"/>
  <text x="66" y="56" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}">FULL STACK &amp; MOBILE DEVELOPER · OUED ZEM</text>
</g>
<text class="r" {d(0.15)} x="44" y="176" font-family="{HEADING}" font-weight="800" font-size="104" letter-spacing="-3.5" fill="{INK}">Rida</text>
<text class="r" {d(0.30)} x="44" y="274" font-family="{HEADING}" font-weight="800" font-style="italic" font-size="104" letter-spacing="-3.5" fill="url(#shine)">Taki</text>
<g class="r" {d(0.55)}>
  {text_lines(48, 330, ["Architecting Spring Boot APIs, React dashboards,", "and mobile apps with clean, resilient code."], 26, f'font-family="{SANS}" font-size="17.5" fill="{INK_SOFT}"')}
</g>
<g class="f" {d(0.80)}>
  <text x="48" y="392" font-family="{MONO}" font-size="13" fill="{GOLD}">{SITE_URL}</text>
  <text class="nu" x="178" y="392" font-family="{MONO}" font-size="13" fill="{BRAND}">&#8599;</text>
</g>
<g transform="translate(502 36) scale({s}) translate(-20 -37)" font-family="{MONO}">
  {''.join(portrait)}
</g>
"""
    write(
        "hero.svg",
        svg(
            W,
            h,
            body,
            ["head-800", "head-800-i", "sans-400", "mono-400"],
            "Rida Taki. Full Stack and Mobile Developer. Architecting Spring Boot APIs, React dashboards, and mobile apps.",
        ),
    )


# ---- 2 · world tiles ----------------------------------------------------------
TILE_W, TILE_H = 880 / 3 - 8, 210  # 285.33: two 12px gaps across the row


def count_up(num, word, x, y, attrs, begin, dur=1.1, frames=18):
    """Number counts up from 0 with SMIL <set> frames (works inside <img>), easing out."""
    m = re.match(r"([\d.]+)(.*)", num)
    val, suf = float(m.group(1)), m.group(2)
    dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
    tail = f' <tspan font-style="italic" font-weight="700">{escape(word)}</tspan>'
    if os.environ.get("STATIC"):
        return f'<text x="{x}" y="{y}" {attrs}>{escape(num)}{tail}</text>'
    out = []
    for i in range(frames + 1):
        e = 1 - (1 - i / frames) ** 3
        txt = num if i == frames else f"{val * e:.{dec}f}{suf}"
        on = begin + dur * i / frames
        off = "" if i == frames else f'<set attributeName="opacity" to="0" begin="{begin + dur * (i + 1) / frames:.3f}s"/>'
        cls = "cu-end" if i == frames else "cu-mid"
        out.append(
            f'<text class="{cls}" x="{x}" y="{y}" {attrs} opacity="0">{escape(txt)}{tail}'
            f'<set attributeName="opacity" to="1" begin="{on:.3f}s"/>{off}</text>'
        )
    return "".join(out)


def tile(name, label, color, on, num, word, blurb, delay, pos):
    lines = wrap(blurb, 33)
    blurb_svg = "".join(
        f'<text class="r" {d(delay + 0.75 + i * 0.1)} x="24" y="{148 + i * 20}" '
        f'font-family="{SANS}" font-size="13.5" fill="{on}" opacity=".92">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    body = f"""
<defs>
  <clipPath id="card"><rect width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>
  <clipPath id="slot"><rect x="0" y="60" width="{TILE_W}" height="64"/></clipPath>
  <linearGradient id="gl" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".30"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<g class="ti" {d(delay)}>
  <g clip-path="url(#card)">
    <rect width="{TILE_W}" height="{TILE_H}" fill="{color}"/>
    <circle class="rg" {d(delay + 0.5)} cx="{TILE_W - 40}" cy="{TILE_H - 40}" r="60" fill="none" stroke="{on}" stroke-opacity=".45" stroke-width="2"/>
    <rect class="sh" style="animation-delay:{delay + 1.4:.2f}s" x="0" y="-20" width="90" height="{TILE_H + 40}" fill="url(#gl)" transform="translate(-260 0)"/>
  </g>
  <text class="sl" {d(delay + 0.35)} x="24" y="38" font-family="{MONO}" font-size="11.5" letter-spacing="1.2" fill="{on}">{label}</text>
  <g class="ai" {d(delay + 0.5)}><text class="n" style="animation-delay:{delay + 1.3:.2f}s" x="250" y="38" font-family="{MONO}" font-size="14" fill="{on}">&#8594;</text></g>
  <g clip-path="url(#slot)"><g class="ro" {d(delay + 0.45)}>
    {count_up(num, word, 24, 110, f'font-family="{HEADING}" font-weight="800" font-size="38" letter-spacing="-1" fill="{on}"', delay + 0.45)}
  </g></g>
  {blurb_svg}
</g>
"""
    write(
        f"{name}.svg",
        svg(
            TILE_W,
            TILE_H,
            body,
            ["head-700-i", "head-800", "sans-400", "mono-400"],
            f"{label}: {num} {word}. {blurb}",
            left=4 * pos,
            right=8 - 4 * pos,
        ),
    )


# ---- 3 · activity (monthly bars) ------------------------------------------------
def activity(data):
    h = 340
    monthly = data["monthly"][-12:]
    best = max(monthly[:-1] or monthly, key=lambda m: m["total"])
    top = max(best["total"], 1)
    x0, x1, base, maxh, gap = 40, 600, 292, 136, 10
    bw = (x1 - x0 - gap * (len(monthly) - 1)) / len(monthly)
    bars = []
    for i, m in enumerate(monthly):
        partial = i == len(monthly) - 1
        is_best = m is best
        bh = max(4, round(m["total"] / top * maxh))
        x = x0 + i * (bw + gap)
        fill = BRAND if is_best else ("#4a4139" if partial else INK_SOFT)
        label = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")
        bars.append(
            f'<rect class="g" style="animation-delay:{2.2 + i * 0.07:.2f}s" x="{x:.1f}" y="{base - bh}" '
            f'width="{bw:.1f}" height="{bh}" rx="4" fill="{fill}"><title>{label}: {m["total"]:,}</title></rect>'
            f'<text class="f" style="animation-delay:{2.2 + i * 0.07:.2f}s" x="{x + bw / 2:.1f}" y="{base + 22}" '
            f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{label}</text>'
        )
        if is_best:
            bars.append(
                f'<text class="p" style="animation-delay:3.2s" x="{x + bw / 2:.1f}" y="{base - bh - 10}" '
                f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{BRAND_LIGHT}">{m["total"]:,}</text>'
            )
    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    streak_note = "current streak, and the longest" if cs >= ls else f"current streak, longest {ls}"
    total_days = len(data["days"])
    stats = [
        (f'{cs} <tspan font-style="italic" font-weight="700" fill="{GOLD}">days</tspan>', streak_note),
        (f'{data["active_days"]}<tspan fill="{MUTED}"> / {total_days}</tspan>', "days with a commit"),
        (f'{data["best_day"]["count"]}', "on the busiest day"),
    ]
    side = []
    for i, (big, small) in enumerate(stats):
        y = 104 + i * 92
        side.append(
            f'<g class="r" {d(2.6 + i * 0.15)}>'
            f'<text x="650" y="{y}" font-family="{HEADING}" font-weight="800" font-size="36" letter-spacing="-1" fill="{INK}">{big}</text>'
            f'<text x="650" y="{y + 24}" font-family="{SANS}" font-size="13" fill="{MUTED}">{small}</text></g>'
        )
        if i < 2:
            side.append(f'<rect class="f" {d(2.6)} x="650" y="{y + 44}" width="190" height="1" fill="{RULE}"/>')
    body = f"""
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14" fill="{SURFACE}" stroke="{BORDER}"/>
<text class="f" {d(1.9)} x="40" y="56" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}">THE LAST 12 MONTHS ON GITHUB</text>
<text class="r" {d(2.0)} x="38" y="110" font-family="{HEADING}" font-weight="800" font-size="46" letter-spacing="-1.5" fill="{INK}">{data["total_contributions"]:,} <tspan font-style="italic" font-weight="700" fill="{GOLD}">contributions</tspan></text>
{''.join(bars)}
{''.join(side)}
"""
    write(
        "activity.svg",
        svg(
            W,
            h,
            body,
            ["head-700-i", "head-800", "sans-400", "mono-400"],
            f'{data["total_contributions"]:,} contributions in the last year, {cs}-day streak',
        ),
    )


# ---- 4 · repo cards -----------------------------------------------------------
REPO_W, REPO_H = 880 / 3 - 8, 176
REPOS = [
    (
        "logitrack-api",
        "Enterprise logistics and shipment tracking REST API with JWT RBAC and MySQL.",
        "Java",
        BRAND,
    ),
    (
        "healthcare-web",
        "Medical and hospital portal for managing patients, doctors, and consultations.",
        "JavaScript",
        GOLD,
    ),
    (
        "fleetflow-api",
        "Fleet orchestration platform for vehicles, drivers, and CI/CD delivery flows.",
        "Java",
        BLUE,
    ),
]


def repo_card(i, name, desc, lang, color, stars):
    delay = 4.6 + i * 0.12
    meta = f"{lang}  ·  ★ {stars}" if stars else f"{lang}  ·  live"
    body = f"""
<rect x="0.5" y="0.5" width="{REPO_W - 1}" height="{REPO_H - 1}" rx="14" fill="{SURFACE}" stroke="{BORDER}"/>
<g class="r" {d(delay)}>
  <rect x="24" y="29" width="8" height="8" rx="2" fill="{color}"/>
  <text x="40" y="38" font-family="{HEADING}" font-weight="700" font-size="17" fill="{INK}">{escape(name)}</text>
  {text_lines(24, 70, wrap(desc, 33), 20, f'font-family="{SANS}" font-size="13.5" fill="{INK_SOFT}"')}
  <text x="24" y="{REPO_H - 22}" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{escape(meta)}</text>
</g>
"""
    write(
        f"repo-{name}.svg",
        svg(
            REPO_W,
            REPO_H,
            body,
            ["head-700", "sans-400", "mono-400"],
            f"{name}: {desc}",
            left=4 * i,
            right=8 - 4 * i,
        ),
    )


def section_title(text, italic, theme):
    fg = INK if theme == "dark" else "#1a1714"
    body = (
        f'<text class="r" {d(4.4)} x="2" y="44" font-family="{HEADING}" font-weight="800" font-size="30" '
        f'letter-spacing="-0.8" fill="{fg}">{escape(text)} '
        f'<tspan font-style="italic" font-weight="700" fill="{BRAND}">{escape(italic)}</tspan></text>'
    )
    write(
        f"title-coding-{theme}.svg",
        svg(W, 60, body, ["head-700-i", "head-800"], f"{text} {italic}", bottom=0),
    )


# ---- 5 · brand contribution graph (warm terracotta ember) ---------------------
EMBER = [SURFACE_2, "#4d2818", "#7d3c20", "#b0532c", BRAND, BRAND_LIGHT]


def level_for(c):
    return 0 if c == 0 else 1 if c <= 3 else 2 if c <= 8 else 3 if c <= 14 else 4 if c <= 20 else 5


def heatmap(data):
    days = data["days"]
    first = datetime.date.fromisoformat(days[0]["date"])
    lead = (first.weekday() + 1) % 7  # sunday = 0
    cell, step, gx, gy = 12, 15, 44, 96
    cells, months, seen = [], [], set()
    for i, day in enumerate(days):
        k = i + lead
        col, row = divmod(k, 7)
        date = datetime.date.fromisoformat(day["date"])
        if date.day <= 7 and (date.year, date.month) not in seen and row == 0:
            seen.add((date.year, date.month))
            months.append((col, date.strftime("%b")))
        c = day["count"]
        delay = 1.0 + col * 0.03 + row * 0.02
        cells.append(
            f'<rect class="p" style="animation-delay:{delay:.2f}s" x="{gx + col * step}" y="{gy + row * step}" '
            f'width="{cell}" height="{cell}" rx="3" fill="{EMBER[level_for(c)]}">'
            f'<title>{day["date"]}: {c} contribution{"s" if c != 1 else ""}</title></rect>'
        )
    ncols = (len(days) + lead + 6) // 7
    right = gx + ncols * step - 3
    labels = "".join(
        f'<text x="{gx + col * step}" y="{gy + 7 * step + 16}" font-family="{MONO}" font-size="11" fill="{MUTED}">{m}</text>'
        for col, m in months
        if col < ncols - 12
    )
    legend_x = right - 34 - len(EMBER) * 14
    legend = "".join(
        f'<rect x="{legend_x + i * 14}" y="{gy + 7 * step + 6}" width="11" height="11" rx="2.5" fill="{c}"/>'
        for i, c in enumerate(EMBER)
    )
    h = gy + 7 * step + 44
    body = f"""
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14" fill="{SURFACE}" stroke="{BORDER}"/>
<text class="r" {d(0.8)} x="42" y="60" font-family="{HEADING}" font-weight="800" font-size="30" letter-spacing="-0.8" fill="{INK}">Every commit, <tspan font-style="italic" font-weight="700" fill="{BRAND}">in ember</tspan></text>
<text class="f" {d(0.8)} x="{right}" y="58" text-anchor="end" font-family="{MONO}" font-size="11.5" letter-spacing="1" fill="{MUTED}">REFRESHED DAILY</text>
{''.join(cells)}
<g class="f" {d(2.4)}>{labels}
<text x="{legend_x - 8}" y="{gy + 7 * step + 16}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">less</text>
{legend}
<text x="{right}" y="{gy + 7 * step + 16}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">more</text></g>
"""
    write(
        "heatmap.svg",
        svg(
            W,
            h,
            body,
            ["head-700-i", "head-800", "mono-400"],
            f'Contribution graph: {data["total_contributions"]:,} contributions in the last year',
        ),
    )


def fetch_github_meta():
    repo_count = DEFAULT_PUBLIC_REPOS
    meta = {}
    try:
        import requests

        u = requests.get(f"https://api.github.com/users/{USERNAME}", timeout=10)
        if u.ok:
            repo_count = u.json().get("public_repos", DEFAULT_PUBLIC_REPOS)
        for name, _, default_lang, _ in REPOS:
            r = requests.get(f"https://api.github.com/repos/{USERNAME}/{name}", timeout=10)
            if r.ok:
                rj = r.json()
                meta[name] = (
                    rj.get("stargazers_count", 0),
                    rj.get("language") or default_lang,
                )
    except Exception as e:  # offline: keep going with defaults
        print(f"github api unavailable: {e}")
    return repo_count, meta


if __name__ == "__main__":
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    repo_count, repo_meta = fetch_github_meta()
    hero()
    tile(
        "build",
        "BUILD",
        BRAND,
        "#ffffff",
        str(repo_count),
        "repos",
        "Spring Boot 3 APIs, React dashboards, Kotlin & Flutter apps with Docker.",
        3.1,
        0,
    )
    tile(
        "arena",
        "ARENA",
        GOLD,
        BG,
        HACKATHONS_COUNT,
        "hackathons",
        "FootTech National Finalist, Hacktoberfest Oued Zem & Rally AI sprints.",
        3.35,
        1,
    )
    tile(
        "learn",
        "CERTIFIED",
        BLUE,
        "#ffffff",
        CERTS_COUNT,
        "certs",
        "Cisco Cybersecurity, Python & Hardware; ENAA Software Engineering.",
        3.6,
        2,
    )
    activity(data)
    for i, (name, desc, default_lang, color) in enumerate(REPOS):
        stars, lang = repo_meta.get(name, (0, default_lang))
        repo_card(i, name, desc, lang, color, stars)
    section_title("What I'm", "coding", "dark")
    section_title("What I'm", "coding", "light")
    heatmap(data)
