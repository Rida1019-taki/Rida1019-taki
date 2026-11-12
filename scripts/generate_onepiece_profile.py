#!/usr/bin/env python3
"""
Generate One Piece Themed SVG Assets for Rida Taki's GitHub Profile README.
Faithfully adapted from Meghamittal0920's 2-page guide and repo architecture,
transforming Naruto motifs into an epic, high-end ONE PIECE adventure!
"""
import os
import json
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
DATA_DIR = os.path.join(ROOT, "data")

os.makedirs(ASSETS, exist_ok=True)

# Load base64 photo for hero circle
photo_path = os.path.join(DATA_DIR, "photo_b64.txt")
with open(photo_path, "r", encoding="utf-8") as f:
    PHOTO_B64 = f.read().strip()

# Load processed wanted photo with warm parchment background blend
wanted_photo_path = os.path.join(DATA_DIR, "wanted_photo_b64.txt")
if os.path.exists(wanted_photo_path):
    with open(wanted_photo_path, "r", encoding="utf-8") as f:
        WANTED_PHOTO_B64 = f.read().strip()
else:
    WANTED_PHOTO_B64 = PHOTO_B64

# Load contributions data
contrib_path = os.path.join(DATA_DIR, "contributions.json")
with open(contrib_path, "r", encoding="utf-8") as f:
    contrib_data = json.load(f)

TOTAL_CONTRIB = contrib_data.get("total_contributions", 552)
ACTIVE_DAYS = contrib_data.get("active_days", 168)
LONGEST_STREAK = contrib_data.get("longest_streak", {}).get("length", 13)
AVG_PER_DAY = contrib_data.get("avg_per_active_day", 3.3)


# ==============================================================================
# 1. HERO BANNER (onepiece-hero.svg) - 1280x560
# ==============================================================================
def make_hero_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 560" width="1280" height="560">
  <defs>
    <linearGradient id="ocean-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070C16" />
      <stop offset="50%" stop-color="#0C1424" />
      <stop offset="100%" stop-color="#141E34" />
    </linearGradient>

    <linearGradient id="gold-fire" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFD700" />
      <stop offset="35%" stop-color="#FFA500" />
      <stop offset="70%" stop-color="#FF4500" />
      <stop offset="100%" stop-color="#FFD700">
        <animate attributeName="stop-color" 
          values="#FFD700;#FF4500;#FFA500;#FFD700" 
          dur="5s" repeatCount="indefinite" />
      </stop>
    </linearGradient>

    <linearGradient id="brass-edge" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#B8860B" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#FF4500" stop-opacity="0.8" />
    </linearGradient>

    <radialGradient id="sun-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFD700" stop-opacity="0.25" />
      <stop offset="60%" stop-color="#FF4500" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#070C16" stop-opacity="0" />
    </radialGradient>

    <clipPath id="avatar-clip">
      <circle cx="1030" cy="280" r="175" />
    </clipPath>
  </defs>

  <style>
    .panel {{ fill: url(#ocean-bg); stroke: url(#brass-edge); stroke-width: 1.5px; rx: 24px; }}
    .corner-bracket {{ stroke: #FFD700; stroke-width: 2.5px; fill: none; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .serif {{ font-family: Georgia, 'Times New Roman', serif; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    
    @keyframes pulse {{
      0% {{ opacity: 0.3; }}
      50% {{ opacity: 1; }}
      100% {{ opacity: 0.3; }}
    }}
    .live-dot {{ animation: pulse 2s infinite ease-in-out; }}
    
    @keyframes orbit-cw {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    @keyframes orbit-ccw {{
      from {{ transform: rotate(360deg); }}
      to {{ transform: rotate(0deg); }}
    }}
    .ring-cw {{ transform-origin: 1030px 280px; animation: orbit-cw 24s linear infinite; }}
    .ring-ccw {{ transform-origin: 1030px 280px; animation: orbit-ccw 16s linear infinite; }}
  </style>

  <rect class="panel" x="0" y="0" width="1280" height="560" />

  <path class="corner-bracket" d="M 32 60 L 32 32 L 60 32" />
  <path class="corner-bracket" d="M 1248 60 L 1248 32 L 1220 32" />
  <path class="corner-bracket" d="M 32 500 L 32 528 L 60 528" />
  <path class="corner-bracket" d="M 1248 500 L 1248 528 L 1220 528" />

  <text class="mono" x="72" y="44" fill="#94A3B8" font-size="11" letter-spacing="1.5px">NAV-LOG // NEW WORLD: [35°41'N · 139°46'E] • GRAND LINE SECTOR 7</text>
  <text class="mono" x="1208" y="44" text-anchor="end" fill="#FFD700" font-size="11" letter-spacing="1px">VESSEL: THOUSAND SUNNY MK-IV</text>

  <g transform="translate(68, 90)">
    <rect x="0" y="0" width="310" height="30" rx="15" fill="#1E293B" stroke="#334155" stroke-width="1" />
    <circle class="live-dot" cx="16" cy="15" r="5" fill="#10B981" />
    <text class="mono" x="32" y="20" fill="#38BDF8" font-size="11" font-weight="700" letter-spacing="1px">STATUS: SAILING THE GRAND LINE</text>

    <text class="sans" x="0" y="70" fill="#94A3B8" font-size="18" font-weight="500">Ahoy there! I'm</text>

    <text class="serif" x="0" y="145" fill="url(#gold-fire)" font-size="68" font-weight="bold" letter-spacing="-1px">RIDA TAKI</text>

    <g transform="translate(0, 185)">
      <rect x="0" y="0" width="8" height="24" rx="2" fill="#FF4500" />
      <text class="mono" x="18" y="18" fill="#F8FAFC" font-size="15" font-weight="700" letter-spacing="0.5px">FULL-STACK &amp; MOBILE DEVELOPER // SYSTEM ARCHITECT</text>
    </g>

    <text class="sans" x="0" y="250" fill="#CBD5E1" font-size="16">
      <tspan x="0" dy="0">Engineering unsinkable Spring Boot backends, fluid React web interfaces,</tspan>
      <tspan x="0" dy="26">and cross-platform mobile systems built to conquer the modern digital ocean.</tspan>
    </text>

    <g transform="translate(0, 335)">
      <rect x="0" y="0" width="180" height="58" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1.2" />
      <text class="mono" x="16" y="22" fill="#94A3B8" font-size="10" font-weight="700" letter-spacing="1px">HOME PORT</text>
      <text class="sans" x="16" y="44" fill="#F8FAFC" font-size="14" font-weight="600">📍 Morocco (Mugiwara)</text>

      <rect x="195" y="0" width="180" height="58" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1.2" />
      <text class="mono" x="211" y="22" fill="#94A3B8" font-size="10" font-weight="700" letter-spacing="1px">ISLANDS CHARTED</text>
      <text class="sans" x="211" y="44" fill="#FFD700" font-size="14" font-weight="700">⚓ 46 Repositories</text>

      <rect x="390" y="0" width="220" height="58" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1.2" />
      <text class="mono" x="406" y="22" fill="#94A3B8" font-size="10" font-weight="700" letter-spacing="1px">ACTIVE BOUNTY</text>
      <text class="sans" x="406" y="44" fill="#F87171" font-size="14" font-weight="700">฿ 552,000,000 Berries</text>
    </g>
  </g>

  <!-- Right Side: Rida Portrait in Grand Line Compass Halo -->
  <g>
    <circle cx="1030" cy="280" r="230" fill="url(#sun-glow)" />

    <circle class="ring-cw" cx="1030" cy="280" r="205" fill="none" stroke="#FFD700" stroke-width="1.5" stroke-dasharray="14 10" opacity="0.7" />
    <circle class="ring-ccw" cx="1030" cy="280" r="188" fill="none" stroke="#FF4500" stroke-width="1.2" stroke-dasharray="8 6" opacity="0.6" />
    <circle cx="1030" cy="280" r="177" fill="none" stroke="#38BDF8" stroke-width="2.5" opacity="0.8" />

    <text class="mono" x="1030" y="70" text-anchor="middle" fill="#FFD700" font-size="12" font-weight="bold">N</text>
    <text class="mono" x="1245" y="284" text-anchor="middle" fill="#FFD700" font-size="12" font-weight="bold">E</text>
    <text class="mono" x="1030" y="498" text-anchor="middle" fill="#FFD700" font-size="12" font-weight="bold">S</text>
    <text class="mono" x="815" y="284" text-anchor="middle" fill="#FFD700" font-size="12" font-weight="bold">W</text>

    <image clip-path="url(#avatar-clip)" x="855" y="105" width="350" height="350" href="data:image/jpeg;base64,{PHOTO_B64}" preserveAspectRatio="xMidYMid slice" />
    <circle cx="1030" cy="280" r="175" fill="none" stroke="url(#brass-edge)" stroke-width="3" />

    <g transform="translate(1030, 455)">
      <rect x="-85" y="-18" width="170" height="36" rx="18" fill="#1E293B" stroke="#FFD700" stroke-width="1.2" />
      <text class="mono" x="0" y="5" text-anchor="middle" fill="#FFD700" font-size="11" font-weight="bold" letter-spacing="1px">☠ STRAW HAT CREW</text>
    </g>
  </g>
</svg>"""


# ==============================================================================
# 2. PIRATE CODE // THE WILL OF D (onepiece-code.svg) - 1280x520
# ==============================================================================
def make_code_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 520" width="1280" height="520">
  <defs>
    <linearGradient id="code-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080E1A" />
      <stop offset="100%" stop-color="#10192E" />
    </linearGradient>
    <linearGradient id="gold-line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF4500" />
      <stop offset="50%" stop-color="#FFD700" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>
    <linearGradient id="card-sheen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.9" />
    </linearGradient>
  </defs>

  <style>
    .panel {{ fill: url(#code-bg); stroke: #1E293B; stroke-width: 1.5px; rx: 24px; }}
    .card-box {{ fill: url(#card-sheen); stroke: #334155; stroke-width: 1.2px; rx: 16px; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .serif {{ font-family: Georgia, 'Times New Roman', serif; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    .badge {{ font-family: ui-monospace, monospace; font-size: 11px; font-weight: 600; fill: #E2E8F0; }}
  </style>

  <rect class="panel" x="0" y="0" width="1280" height="520" />

  <g transform="translate(60, 48)">
    <text class="mono" x="0" y="0" fill="#FFD700" font-size="12" font-weight="700" letter-spacing="2px">01 // MY PIRATE CODE</text>
    <text class="serif" x="0" y="38" fill="#F8FAFC" font-size="34" font-weight="bold">THE WILL OF D. IN EVERY COMMIT</text>
    <text class="sans" x="0" y="66" fill="#94A3B8" font-size="15" font-style="italic">
      "Inherited Will, the Swell of the Era, and the Dreams of Its People — These are things that cannot be stopped."
    </text>
    <line x1="0" y1="84" x2="1160" y2="84" stroke="url(#gold-line)" stroke-width="2" />
  </g>

  <!-- Pillar 1: Unsinkable Architectures -->
  <g transform="translate(60, 165)">
    <rect class="card-box" x="0" y="0" width="365" height="310" />
    <rect x="24" y="24" width="48" height="48" rx="12" fill="#451A03" stroke="#D97706" stroke-width="1.2" />
    <text class="sans" x="48" y="55" text-anchor="middle" font-size="24">⚓</text>
    <text class="serif" x="24" y="105" fill="#F8FAFC" font-size="20" font-weight="bold">Unsinkable Architectures</text>
    <text class="mono" x="24" y="125" fill="#F59E0B" font-size="11" font-weight="700">SPRING BOOT &amp; DOCKER</text>
    <text class="sans" x="24" y="156" fill="#94A3B8" font-size="13.5">
      <tspan x="24" dy="0">Forging enterprise-grade REST APIs</tspan>
      <tspan x="24" dy="20">and microservice backends that weather</tspan>
      <tspan x="24" dy="20">high concurrency storms with zero</tspan>
      <tspan x="24" dy="20">downtime and clean layered patterns.</tspan>
    </text>
    <g transform="translate(24, 252)">
      <rect x="0" y="0" width="90" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="45" y="17" text-anchor="middle">Spring Boot</text>
      <rect x="98" y="0" width="85" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="140" y="17" text-anchor="middle">REST APIs</text>
      <rect x="191" y="0" width="65" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="223" y="17" text-anchor="middle">MySQL</text>
      <rect x="264" y="0" width="68" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="298" y="17" text-anchor="middle">Docker</text>
    </g>
  </g>

  <!-- Pillar 2: Fluid Web Interfaces -->
  <g transform="translate(457, 165)">
    <rect class="card-box" x="0" y="0" width="365" height="310" />
    <rect x="24" y="24" width="48" height="48" rx="12" fill="#082F49" stroke="#0284C7" stroke-width="1.2" />
    <text class="sans" x="48" y="55" text-anchor="middle" font-size="24">🌊</text>
    <text class="serif" x="24" y="105" fill="#F8FAFC" font-size="20" font-weight="bold">Fluid Grand Line UI</text>
    <text class="mono" x="24" y="125" fill="#38BDF8" font-size="11" font-weight="700">REACT.JS &amp; TAILWIND</text>
    <text class="sans" x="24" y="156" fill="#94A3B8" font-size="13.5">
      <tspan x="24" dy="0">Crafting cinematic, responsive frontends</tspan>
      <tspan x="24" dy="20">with modern component lifecycles,</tspan>
      <tspan x="24" dy="20">seamless state synchronization, and</tspan>
      <tspan x="24" dy="20">ergonomic, user-first UI journeys.</tspan>
    </text>
    <g transform="translate(24, 252)">
      <rect x="0" y="0" width="75" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="37" y="17" text-anchor="middle">React.js</text>
      <rect x="83" y="0" width="85" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="125" y="17" text-anchor="middle">JavaScript</text>
      <rect x="176" y="0" width="85" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="218" y="17" text-anchor="middle">TypeScript</text>
      <rect x="269" y="0" width="70" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="304" y="17" text-anchor="middle">Tailwind</text>
    </g>
  </g>

  <!-- Pillar 3: Cross-Ocean Mobile -->
  <g transform="translate(855, 165)">
    <rect class="card-box" x="0" y="0" width="365" height="310" />
    <rect x="24" y="24" width="48" height="48" rx="12" fill="#4C0519" stroke="#E11D48" stroke-width="1.2" />
    <text class="sans" x="48" y="55" text-anchor="middle" font-size="24">📱</text>
    <text class="serif" x="24" y="105" fill="#F8FAFC" font-size="20" font-weight="bold">Cross-Ocean Mobile</text>
    <text class="mono" x="24" y="125" fill="#FB7185" font-size="11" font-weight="700">KOTLIN &amp; FLUTTER</text>
    <text class="sans" x="24" y="156" fill="#94A3B8" font-size="13.5">
      <tspan x="24" dy="0">Building native Android capabilities</tspan>
      <tspan x="24" dy="20">in Kotlin alongside multi-platform</tspan>
      <tspan x="24" dy="20">Flutter builds powered by real-time</tspan>
      <tspan x="24" dy="20">Firebase auth and offline-first SQLite.</tspan>
    </text>
    <g transform="translate(24, 252)">
      <rect x="0" y="0" width="85" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="42" y="17" text-anchor="middle">Kotlin App</text>
      <rect x="93" y="0" width="85" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="135" y="17" text-anchor="middle">Flutter/Dart</text>
      <rect x="186" y="0" width="75" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="223" y="17" text-anchor="middle">Firebase</text>
      <rect x="269" y="0" width="65" height="26" rx="6" fill="#0F172A" stroke="#334155" />
      <text class="badge" x="301" y="17" text-anchor="middle">SQLite</text>
    </g>
  </g>
</svg>"""


# ==============================================================================
# 3. DEVIL FRUIT & HAKI ARSENAL (onepiece-haki-stack.svg) - 1280x520
# ==============================================================================
def make_haki_stack_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 520" width="1280" height="520">
  <defs>
    <linearGradient id="haki-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070C16" />
      <stop offset="100%" stop-color="#0F1A2E" />
    </linearGradient>
    <linearGradient id="haki-line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFD700" />
      <stop offset="50%" stop-color="#FF4500" />
      <stop offset="100%" stop-color="#8B5CF6" />
    </linearGradient>
  </defs>

  <style>
    .panel {{ fill: url(#haki-bg); stroke: #1E293B; stroke-width: 1.5px; rx: 24px; }}
    .quad-box {{ fill: #0B1322; stroke: #1E293B; stroke-width: 1.2px; rx: 14px; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .serif {{ font-family: Georgia, 'Times New Roman', serif; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    .chip {{ rx: 8px; stroke-width: 1px; }}
    .chip-text {{ font-family: ui-monospace, monospace; font-size: 12px; font-weight: 600; }}
  </style>

  <rect class="panel" x="0" y="0" width="1280" height="520" />

  <g transform="translate(60, 48)">
    <text class="mono" x="0" y="0" fill="#FFD700" font-size="12" font-weight="700" letter-spacing="2px">02 // DEVIL FRUIT &amp; HAKI ARSENAL</text>
    <text class="serif" x="0" y="38" fill="#F8FAFC" font-size="34" font-weight="bold">TECH STACK COMMANDED ACROSS THE SEAS</text>
    <text class="sans" x="0" y="66" fill="#94A3B8" font-size="15">
      Mastering the three forms of Haki and ancient Devil Fruit powers to engineer modern software solutions.
    </text>
    <line x1="0" y1="84" x2="1160" y2="84" stroke="url(#haki-line)" stroke-width="2" />
  </g>

  <!-- 1. Conqueror's Haki -->
  <g transform="translate(60, 160)">
    <rect class="quad-box" x="0" y="0" width="565" height="150" />
    <rect x="20" y="16" width="38" height="38" rx="8" fill="#451A03" stroke="#D97706" />
    <text class="sans" x="39" y="42" text-anchor="middle" font-size="18">👑</text>
    <text class="serif" x="70" y="34" fill="#F8FAFC" font-size="18" font-weight="bold">Conqueror's Haki (Haoshoku Haki)</text>
    <text class="mono" x="70" y="50" fill="#F59E0B" font-size="11" font-weight="700">CORE PROGRAMMING LANGUAGES</text>

    <g transform="translate(20, 75)">
      <rect class="chip" x="0" y="0" width="115" height="28" fill="#172554" stroke="#3B82F6" />
      <text class="chip-text" x="57" y="18" text-anchor="middle" fill="#93C5FD">Java (Core)</text>
      <rect class="chip" x="125" y="0" width="110" height="28" fill="#422006" stroke="#EAB308" />
      <text class="chip-text" x="180" y="18" text-anchor="middle" fill="#FDE047">JavaScript</text>
      <rect class="chip" x="245" y="0" width="110" height="28" fill="#172554" stroke="#2563EB" />
      <text class="chip-text" x="300" y="18" text-anchor="middle" fill="#60A5FA">TypeScript</text>
      <rect class="chip" x="365" y="0" width="90" height="28" fill="#064E3B" stroke="#10B981" />
      <text class="chip-text" x="410" y="18" text-anchor="middle" fill="#6EE7B7">Python</text>

      <rect class="chip" x="0" y="36" width="100" height="28" fill="#4C0519" stroke="#E11D48" />
      <text class="chip-text" x="50" y="54" text-anchor="middle" fill="#FDA4AF">Kotlin</text>
      <rect class="chip" x="110" y="36" width="90" height="28" fill="#082F49" stroke="#0284C7" />
      <text class="chip-text" x="155" y="54" text-anchor="middle" fill="#7DD3FC">Dart</text>
      <rect class="chip" x="210" y="36" width="90" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="255" y="54" text-anchor="middle" fill="#CBD5E1">SQL / C++</text>
    </g>
  </g>

  <!-- 2. Armament Haki -->
  <g transform="translate(655, 160)">
    <rect class="quad-box" x="0" y="0" width="565" height="150" />
    <rect x="20" y="16" width="38" height="38" rx="8" fill="#1E1B4B" stroke="#6366F1" />
    <text class="sans" x="39" y="42" text-anchor="middle" font-size="18">🛡️</text>
    <text class="serif" x="70" y="34" fill="#F8FAFC" font-size="18" font-weight="bold">Armament Haki (Busoshoku Haki)</text>
    <text class="mono" x="70" y="50" fill="#818CF8" font-size="11" font-weight="700">BACKEND ARCHITECTURE &amp; FORTRESS DATA</text>

    <g transform="translate(20, 75)">
      <rect class="chip" x="0" y="0" width="125" height="28" fill="#14532D" stroke="#22C55E" />
      <text class="chip-text" x="62" y="18" text-anchor="middle" fill="#86EFAC">Spring Boot</text>
      <rect class="chip" x="135" y="0" width="105" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="187" y="18" text-anchor="middle" fill="#E2E8F0">REST APIs</text>
      <rect class="chip" x="250" y="0" width="95" height="28" fill="#0C4A6E" stroke="#0284C7" />
      <text class="chip-text" x="297" y="18" text-anchor="middle" fill="#38BDF8">MySQL</text>
      <rect class="chip" x="355" y="0" width="90" height="28" fill="#0C4A6E" stroke="#0369A1" />
      <text class="chip-text" x="400" y="18" text-anchor="middle" fill="#7DD3FC">Docker</text>

      <rect class="chip" x="0" y="36" width="115" height="28" fill="#451A03" stroke="#D97706" />
      <text class="chip-text" x="57" y="54" text-anchor="middle" fill="#FCD34D">Firebase Auth</text>
      <rect class="chip" x="125" y="36" width="85" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="167" y="54" text-anchor="middle" fill="#CBD5E1">SQLite</text>
      <rect class="chip" x="220" y="36" width="115" height="28" fill="#1E293B" stroke="#475569" />
      <text class="chip-text" x="277" y="54" text-anchor="middle" fill="#E2E8F0">Git / GitHub</text>
    </g>
  </g>

  <!-- 3. Observation Haki -->
  <g transform="translate(60, 330)">
    <rect class="quad-box" x="0" y="0" width="565" height="150" />
    <rect x="20" y="16" width="38" height="38" rx="8" fill="#0F766E" stroke="#14B8A6" />
    <text class="sans" x="39" y="42" text-anchor="middle" font-size="18">👁️</text>
    <text class="serif" x="70" y="34" fill="#F8FAFC" font-size="18" font-weight="bold">Observation Haki (Kenbunshoku Haki)</text>
    <text class="mono" x="70" y="50" fill="#2DD4BF" font-size="11" font-weight="700">SYSTEM DESIGN, SECURITY &amp; CI/CD</text>

    <g transform="translate(20, 75)">
      <rect class="chip" x="0" y="0" width="135" height="28" fill="#134E4A" stroke="#0D9488" />
      <text class="chip-text" x="67" y="18" text-anchor="middle" fill="#5EEAD4">System Design</text>
      <rect class="chip" x="145" y="0" width="125" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="207" y="18" text-anchor="middle" fill="#E2E8F0">JWT Security</text>
      <rect class="chip" x="280" y="0" width="120" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="340" y="18" text-anchor="middle" fill="#CBD5E1">MVC Pattern</text>

      <rect class="chip" x="0" y="36" width="120" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="60" y="54" text-anchor="middle" fill="#CBD5E1">CI/CD Actions</text>
      <rect class="chip" x="130" y="36" width="95" height="28" fill="#431407" stroke="#EA580C" />
      <text class="chip-text" x="177" y="54" text-anchor="middle" fill="#FDBA74">Postman</text>
      <rect class="chip" x="235" y="36" width="135" height="28" fill="#1E293B" stroke="#475569" />
      <text class="chip-text" x="302" y="54" text-anchor="middle" fill="#E2E8F0">Linux / DevOps</text>
    </g>
  </g>

  <!-- 4. Devil Fruit Powers -->
  <g transform="translate(655, 330)">
    <rect class="quad-box" x="0" y="0" width="565" height="150" />
    <rect x="20" y="16" width="38" height="38" rx="8" fill="#581C87" stroke="#A855F7" />
    <text class="sans" x="39" y="42" text-anchor="middle" font-size="18">🌀</text>
    <text class="serif" x="70" y="34" fill="#F8FAFC" font-size="18" font-weight="bold">Devil Fruit Abilities (Akuma no Mi)</text>
    <text class="mono" x="70" y="50" fill="#C084FC" font-size="11" font-weight="700">FLUID FRONTEND &amp; CROSS-PLATFORM INTERFACES</text>

    <g transform="translate(20, 75)">
      <rect class="chip" x="0" y="0" width="105" height="28" fill="#082F49" stroke="#0284C7" />
      <text class="chip-text" x="52" y="18" text-anchor="middle" fill="#38BDF8">React.js</text>
      <rect class="chip" x="115" y="0" width="95" height="28" fill="#0C4A6E" stroke="#0284C7" />
      <text class="chip-text" x="162" y="18" text-anchor="middle" fill="#7DD3FC">Flutter</text>
      <rect class="chip" x="220" y="0" width="115" height="28" fill="#134E4A" stroke="#06B6D4" />
      <text class="chip-text" x="277" y="18" text-anchor="middle" fill="#67E8F9">Tailwind CSS</text>
      <rect class="chip" x="345" y="0" width="85" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="387" y="18" text-anchor="middle" fill="#CBD5E1">HTML5</text>

      <rect class="chip" x="0" y="36" width="85" height="28" fill="#1E293B" stroke="#64748B" />
      <text class="chip-text" x="42" y="54" text-anchor="middle" fill="#CBD5E1">CSS3</text>
      <rect class="chip" x="95" y="36" width="130" height="28" fill="#3B0764" stroke="#9333EA" />
      <text class="chip-text" x="160" y="54" text-anchor="middle" fill="#D8B4FE">Responsive UI</text>
      <rect class="chip" x="235" y="36" width="130" height="28" fill="#4A044E" stroke="#C026D3" />
      <text class="chip-text" x="300" y="54" text-anchor="middle" fill="#F0ABFC">State Machines</text>
    </g>
  </g>
</svg>"""


# ==============================================================================
# 4. PIRATE WANTED POSTER & MISSION DASHBOARD (onepiece-wanted-dashboard.svg) - 1280x640
# ==============================================================================
def make_wanted_dashboard_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 640" width="1280" height="640">
  <defs>
    <linearGradient id="dash-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070C16" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>

    <!-- Warm Parchment Paper Background -->
    <linearGradient id="parchment" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F2DFCA" />
      <stop offset="50%" stop-color="#E8CEB0" />
      <stop offset="100%" stop-color="#DCBE9B" />
    </linearGradient>

    <!-- Precise Clip Path for Wanted Poster Photo (Matched to Frame) -->
    <clipPath id="wanted-clip">
      <rect x="47" y="147" width="316" height="261" rx="4" />
    </clipPath>
  </defs>

  <style>
    .panel {{ fill: url(#dash-bg); stroke: #1E293B; stroke-width: 1.5px; rx: 24px; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .serif {{ font-family: Georgia, 'Times New Roman', serif; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    .wanted-font {{ font-family: 'Impact', 'Arial Black', sans-serif; letter-spacing: 4px; }}
    .marine-text {{ font-family: 'Times New Roman', Georgia, serif; font-weight: bold; letter-spacing: 3px; }}
    .kpi-tile {{ fill: #0B1322; stroke: #1E293B; stroke-width: 1.2px; rx: 12px; }}
  </style>

  <rect class="panel" x="0" y="0" width="1280" height="640" />

  <!-- ==================== LEFT: AUTHENTIC ONE PIECE WANTED POSTER ==================== -->
  <g transform="translate(45, 30)">
    <!-- Parchment Sheet (Width 410, Height 580) -->
    <rect x="0" y="0" width="410" height="580" rx="14" fill="url(#parchment)" stroke="#8C6239" stroke-width="2.5" />
    <rect x="14" y="14" width="382" height="552" rx="8" fill="none" stroke="#5C3A21" stroke-width="1.8" />
    <rect x="20" y="20" width="370" height="540" rx="6" fill="none" stroke="#8C6239" stroke-width="0.8" />

    <!-- Marine Header Text -->
    <text class="marine-text" x="205" y="58" text-anchor="middle" fill="#3D2314" font-size="28">M A R I N E</text>

    <!-- WANTED Title -->
    <text class="wanted-font" x="205" y="125" text-anchor="middle" fill="#2E1708" font-size="64">WANTED</text>

    <!-- Photo Frame (Width 320, perfectly centered at x=45 on 410 sheet) -->
    <rect x="45" y="145" width="320" height="265" fill="#C5AA8E" stroke="#5C3A21" stroke-width="2.5" rx="6" />

    <!-- Rida Portrait Processed with Warm Parchment Background -->
    <image clip-path="url(#wanted-clip)" x="47" y="147" width="316" height="261" href="data:image/jpeg;base64,{WANTED_PHOTO_B64}" preserveAspectRatio="xMidYMid slice" />

    <!-- Subtle Inner Border Overlay -->
    <rect x="47" y="147" width="316" height="261" rx="4" fill="none" stroke="#5C3A21" stroke-width="1.5" opacity="0.6" />

    <!-- DEAD OR ALIVE banner (Centered at x=205) -->
    <text class="marine-text" x="205" y="442" text-anchor="middle" fill="#3D2314" font-size="22">DEAD OR ALIVE</text>

    <!-- Pirate Name (Centered at x=205) -->
    <text class="wanted-font" x="205" y="490" text-anchor="middle" fill="#1C0E05" font-size="36">RIDA TAKI</text>

    <!-- Berry Symbol & Bounty (Centered at x=190) -->
    <g transform="translate(190, 536)">
      <text class="serif" x="0" y="0" text-anchor="middle" font-size="28" font-weight="bold">
        <tspan fill="#2E1708">฿ </tspan>
        <tspan font-family="'Impact', 'Arial Black', sans-serif" font-size="30" letter-spacing="2px">552,000,000 -</tspan>
      </text>
    </g>

    <!-- Marine Red Wax Stamp (Bottom Right, perfectly offset) -->
    <g transform="translate(345, 515)">
      <circle cx="0" cy="0" r="26" fill="#991B1B" opacity="0.88" />
      <circle cx="0" cy="0" r="22" fill="none" stroke="#FEE2E2" stroke-width="1.2" stroke-dasharray="3 2" />
      <text class="mono" x="0" y="-4" text-anchor="middle" fill="#FEE2E2" font-size="6.5" font-weight="bold">GRAND LINE</text>
      <text class="mono" x="0" y="7" text-anchor="middle" fill="#FEE2E2" font-size="7.5" font-weight="bold">VERIFIED</text>
    </g>
  </g>

  <!-- ==================== RIGHT: PIRATE LOG & VOYAGE DASHBOARD ==================== -->
  <g transform="translate(500, 48)">
    <text class="mono" x="0" y="0" fill="#FFD700" font-size="12" font-weight="700" letter-spacing="2px">03 // PIRATE REGISTRATION &amp; MISSION LOG</text>
    <text class="serif" x="0" y="36" fill="#F8FAFC" font-size="32" font-weight="bold">GRAND LINE FLEET DASHBOARD</text>
    <text class="sans" x="0" y="62" fill="#94A3B8" font-size="14.5">
      Verified navigational logs, commit velocity, and repository exploration across the digital sea.
    </text>

    <g transform="translate(0, 85)">
      <rect class="kpi-tile" x="0" y="0" width="345" height="90" />
      <text class="mono" x="20" y="26" fill="#64748B" font-size="10" font-weight="700" letter-spacing="1px">ISLANDS CHARTED</text>
      <text class="serif" x="20" y="64" fill="#F8FAFC" font-size="32" font-weight="bold">46 <tspan font-family="ui-monospace" font-size="14" fill="#38BDF8" font-weight="normal">Public Repos</tspan></text>

      <rect class="kpi-tile" x="370" y="0" width="345" height="90" />
      <text class="mono" x="390" y="26" fill="#64748B" font-size="10" font-weight="700" letter-spacing="1px">ANNUAL BOUNTY EARNED</text>
      <text class="serif" x="390" y="64" fill="#F8FAFC" font-size="32" font-weight="bold">{TOTAL_CONTRIB} <tspan font-family="ui-monospace" font-size="14" fill="#F59E0B" font-weight="normal">Commits Logged</tspan></text>

      <rect class="kpi-tile" x="0" y="105" width="345" height="90" />
      <text class="mono" x="20" y="131" fill="#64748B" font-size="10" font-weight="700" letter-spacing="1px">ACTIVE SAILING DAYS</text>
      <text class="serif" x="20" y="169" fill="#F8FAFC" font-size="32" font-weight="bold">{ACTIVE_DAYS} <tspan font-family="ui-monospace" font-size="14" fill="#10B981" font-weight="normal">Days Active</tspan></text>

      <rect class="kpi-tile" x="370" y="105" width="345" height="90" />
      <text class="mono" x="390" y="131" fill="#64748B" font-size="10" font-weight="700" letter-spacing="1px">LONGEST EXPEDITION STREAK</text>
      <text class="serif" x="390" y="169" fill="#F8FAFC" font-size="32" font-weight="bold">{LONGEST_STREAK} <tspan font-family="ui-monospace" font-size="14" fill="#F87171" font-weight="normal">Days Non-Stop</tspan></text>
    </g>

    <g transform="translate(0, 305)">
      <rect class="kpi-tile" x="0" y="0" width="715" height="135" />
      <text class="mono" x="20" y="24" fill="#94A3B8" font-size="11" font-weight="700" letter-spacing="1px">CODEBASE LANGUAGE ALLOCATION</text>
      <text class="mono" x="695" y="24" text-anchor="end" fill="#FFD700" font-size="11" font-weight="600">46 PUBLIC REPOSITORIES</text>

      <g transform="translate(20, 36)">
        <rect x="0" y="0" width="255" height="10" rx="5" fill="#3B82F6" />
        <rect x="258" y="0" width="182" height="10" rx="5" fill="#EAB308" />
        <rect x="443" y="0" width="91" height="10" rx="5" fill="#EC4899" />
        <rect x="537" y="0" width="73" height="10" rx="5" fill="#6366F1" />
        <rect x="613" y="0" width="62" height="10" rx="5" fill="#10B981" />
      </g>

      <g transform="translate(20, 68)">
        <circle cx="6" cy="6" r="4.5" fill="#3B82F6" />
        <text class="sans" x="18" y="10" fill="#F8FAFC" font-size="12.5" font-weight="600">Java: <tspan fill="#94A3B8" font-weight="normal">37.8% (14 repos)</tspan></text>

        <circle cx="210" cy="6" r="4.5" fill="#EAB308" />
        <text class="sans" x="222" y="10" fill="#F8FAFC" font-size="12.5" font-weight="600">JavaScript: <tspan fill="#94A3B8" font-weight="normal">27.0% (10 repos)</tspan></text>

        <circle cx="430" cy="6" r="4.5" fill="#EC4899" />
        <text class="sans" x="442" y="10" fill="#F8FAFC" font-size="12.5" font-weight="600">HTML/CSS: <tspan fill="#94A3B8" font-weight="normal">13.5% (5 repos)</tspan></text>

        <circle cx="6" cy="36" r="4.5" fill="#6366F1" />
        <text class="sans" x="18" y="40" fill="#F8FAFC" font-size="12.5" font-weight="600">TypeScript: <tspan fill="#94A3B8" font-weight="normal">10.8% (4 repos)</tspan></text>

        <circle cx="210" cy="36" r="4.5" fill="#10B981" />
        <text class="sans" x="222" y="40" fill="#F8FAFC" font-size="12.5" font-weight="600">Python &amp; Kotlin: <tspan fill="#94A3B8" font-weight="normal">10.9% (3 repos)</tspan></text>
      </g>
    </g>

    <g transform="translate(0, 460)">
      <rect class="kpi-tile" x="0" y="0" width="715" height="90" />
      <text class="mono" x="20" y="24" fill="#38BDF8" font-size="10.5" font-weight="700" letter-spacing="1px">CISCO NETWORKING ACADEMY // VERIFIED SEALS</text>
      
      <g transform="translate(20, 36)">
        <text class="sans" x="0" y="20" fill="#F8FAFC" font-size="13.5" font-weight="600">📜 Python Essentials 1</text>
        <text class="sans" x="230" y="20" fill="#F8FAFC" font-size="13.5" font-weight="600">🛡️ Intro to Cybersecurity</text>
        <text class="sans" x="470" y="20" fill="#F8FAFC" font-size="13.5" font-weight="600">⚙️ IT Hardware Fundamentals</text>
        
        <text class="mono" x="0" y="38" fill="#10B981" font-size="11">✓ Verified Certificate</text>
        <text class="mono" x="230" y="38" fill="#10B981" font-size="11">✓ Verified Certificate</text>
        <text class="mono" x="470" y="38" fill="#10B981" font-size="11">✓ Verified Certificate</text>
      </g>
    </g>
  </g>
</svg>"""


# ==============================================================================
# 5. GRAND LINE LEGENDARY VOYAGES (onepiece-voyages.svg) - 1280x620
# ==============================================================================
def make_voyages_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 620" width="1280" height="620">
  <defs>
    <linearGradient id="voy-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070C16" />
      <stop offset="100%" stop-color="#0F182B" />
    </linearGradient>
    <linearGradient id="gold-line-v" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFD700" />
      <stop offset="50%" stop-color="#FF4500" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>
    <linearGradient id="card-glass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#111C30" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#0B1220" stop-opacity="0.95" />
    </linearGradient>
  </defs>

  <style>
    .panel {{ fill: url(#voy-bg); stroke: #1E293B; stroke-width: 1.5px; rx: 24px; }}
    .voy-card {{ fill: url(#card-glass); stroke: #23354E; stroke-width: 1.2px; rx: 16px; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .serif {{ font-family: Georgia, 'Times New Roman', serif; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    .chip {{ rx: 6px; stroke-width: 1px; }}
    .chip-t {{ font-family: ui-monospace, monospace; font-size: 11px; font-weight: 600; }}
  </style>

  <rect class="panel" x="0" y="0" width="1280" height="620" />

  <g transform="translate(60, 44)">
    <text class="mono" x="0" y="0" fill="#FFD700" font-size="12" font-weight="700" letter-spacing="2px">04 // GRAND LINE LEGENDARY VOYAGES</text>
    <text class="serif" x="0" y="38" fill="#F8FAFC" font-size="34" font-weight="bold">FEATURED PRODUCTS &amp; EXPEDITIONS</text>
    <text class="sans" x="0" y="66" fill="#94A3B8" font-size="15">
      Battle-tested architectures, enterprise medical management, and cross-platform mobile solutions.
    </text>
    <line x1="0" y1="84" x2="1160" y2="84" stroke="url(#gold-line-v)" stroke-width="2" />
  </g>

  <!-- Card 1: HealthCare+ Platform -->
  <g transform="translate(60, 155)">
    <rect class="voy-card" x="0" y="0" width="565" height="205" />
    <text class="serif" x="24" y="36" fill="#F8FAFC" font-size="20" font-weight="bold">🏥 HealthCare+ Platform</text>
    <text class="mono" x="24" y="54" fill="#F59E0B" font-size="10.5" font-weight="700" letter-spacing="1px">ENTERPRISE CLINICAL &amp; HOSPITAL SYSTEM</text>

    <rect x="435" y="16" width="106" height="24" rx="12" fill="#451A03" stroke="#D97706" stroke-width="1" />
    <text class="mono" x="488" y="32" text-anchor="middle" fill="#FDE047" font-size="10.5" font-weight="bold">👑 S-RANK</text>

    <text class="sans" x="24" y="84" fill="#94A3B8" font-size="13">
      <tspan x="24" dy="0">Production-oriented medical platform with multi-module domain separation,</tspan>
      <tspan x="24" dy="20">strict JWT role-based security, appointment workflows, patient records,</tspan>
      <tspan x="24" dy="20">and containerized Docker Compose microservice environment.</tspan>
    </text>

    <g transform="translate(24, 156)">
      <rect class="chip" x="0" y="0" width="95" height="24" fill="#14532D" stroke="#22C55E" />
      <text class="chip-t" x="47" y="16" text-anchor="middle" fill="#86EFAC">Spring Boot</text>
      <rect class="chip" x="103" y="0" width="75" height="24" fill="#082F49" stroke="#0284C7" />
      <text class="chip-t" x="140" y="16" text-anchor="middle" fill="#38BDF8">React.js</text>
      <rect class="chip" x="186" y="0" width="70" height="24" fill="#172554" stroke="#3B82F6" />
      <text class="chip-t" x="221" y="16" text-anchor="middle" fill="#93C5FD">MySQL</text>
      <rect class="chip" x="264" y="0" width="70" height="24" fill="#0C4A6E" stroke="#0284C7" />
      <text class="chip-t" x="299" y="16" text-anchor="middle" fill="#7DD3FC">Docker</text>
      <rect class="chip" x="342" y="0" width="85" height="24" fill="#1E1B4B" stroke="#6366F1" />
      <text class="chip-t" x="384" y="16" text-anchor="middle" fill="#A5B4FC">JWT Security</text>
    </g>
  </g>

  <!-- Card 2: Spring Boot & React Ecosystem -->
  <g transform="translate(655, 155)">
    <rect class="voy-card" x="0" y="0" width="565" height="205" />
    <text class="serif" x="24" y="36" fill="#F8FAFC" font-size="20" font-weight="bold">🎓 Spring &amp; React Learning Platform</text>
    <text class="mono" x="24" y="54" fill="#38BDF8" font-size="10.5" font-weight="700" letter-spacing="1px">FULL-STACK ARCHITECTURE &amp; APIS</text>

    <rect x="435" y="16" width="106" height="24" rx="12" fill="#082F49" stroke="#0284C7" stroke-width="1" />
    <text class="mono" x="488" y="32" text-anchor="middle" fill="#7DD3FC" font-size="10.5" font-weight="bold">⚓ ACTIVE</text>

    <text class="sans" x="24" y="84" fill="#94A3B8" font-size="13">
      <tspan x="24" dy="0">Full-stack educational platform built with Controller-Service-Repository pattern,</tspan>
      <tspan x="24" dy="20">JPA/Hibernate database persistence, automated RESTful API specs,</tspan>
      <tspan x="24" dy="20">and an ergonomic component-driven client user interface.</tspan>
    </text>

    <g transform="translate(24, 156)">
      <rect class="chip" x="0" y="0" width="55" height="24" fill="#172554" stroke="#3B82F6" />
      <text class="chip-t" x="27" y="16" text-anchor="middle" fill="#93C5FD">Java</text>
      <rect class="chip" x="63" y="0" width="95" height="24" fill="#14532D" stroke="#22C55E" />
      <text class="chip-t" x="110" y="16" text-anchor="middle" fill="#86EFAC">Spring Boot</text>
      <rect class="chip" x="166" y="0" width="75" height="24" fill="#082F49" stroke="#0284C7" />
      <text class="chip-t" x="203" y="16" text-anchor="middle" fill="#38BDF8">React.js</text>
      <rect class="chip" x="249" y="0" width="85" height="24" fill="#1E293B" stroke="#64748B" />
      <text class="chip-t" x="291" y="16" text-anchor="middle" fill="#CBD5E1">REST APIs</text>
      <rect class="chip" x="342" y="0" width="90" height="24" fill="#172554" stroke="#2563EB" />
      <text class="chip-t" x="387" y="16" text-anchor="middle" fill="#60A5FA">JPA / SQL</text>
    </g>
  </g>

  <!-- Card 3: Cross-Ocean Mobile Applications -->
  <g transform="translate(60, 380)">
    <rect class="voy-card" x="0" y="0" width="565" height="205" />
    <text class="serif" x="24" y="36" fill="#F8FAFC" font-size="20" font-weight="bold">📱 Cross-Ocean Mobile Apps</text>
    <text class="mono" x="24" y="54" fill="#FB7185" font-size="10.5" font-weight="700" letter-spacing="1px">NATIVE ANDROID &amp; MULTI-PLATFORM</text>

    <rect x="435" y="16" width="106" height="24" rx="12" fill="#4C0519" stroke="#E11D48" stroke-width="1" />
    <text class="mono" x="488" y="32" text-anchor="middle" fill="#FDA4AF" font-size="10.5" font-weight="bold">🚀 SHIPPED</text>

    <text class="sans" x="24" y="84" fill="#94A3B8" font-size="13">
      <tspan x="24" dy="0">Native Android applications engineered in Kotlin alongside cross-platform</tspan>
      <tspan x="24" dy="20">Flutter builds, powered by real-time Firebase authentication, Firestore data,</tspan>
      <tspan x="24" dy="20">and offline-first local SQLite caching for seamless mobile journeys.</tspan>
    </text>

    <g transform="translate(24, 156)">
      <rect class="chip" x="0" y="0" width="95" height="24" fill="#4C0519" stroke="#E11D48" />
      <text class="chip-t" x="47" y="16" text-anchor="middle" fill="#FDA4AF">Kotlin Native</text>
      <rect class="chip" x="103" y="0" width="65" height="24" fill="#082F49" stroke="#0284C7" />
      <text class="chip-t" x="135" y="16" text-anchor="middle" fill="#7DD3FC">Flutter</text>
      <rect class="chip" x="176" y="0" width="55" height="24" fill="#082F49" stroke="#0284C7" />
      <text class="chip-t" x="203" y="16" text-anchor="middle" fill="#38BDF8">Dart</text>
      <rect class="chip" x="239" y="0" width="80" height="24" fill="#451A03" stroke="#D97706" />
      <text class="chip-t" x="279" y="16" text-anchor="middle" fill="#FCD34D">Firebase</text>
      <rect class="chip" x="327" y="0" width="65" height="24" fill="#1E293B" stroke="#64748B" />
      <text class="chip-t" x="359" y="16" text-anchor="middle" fill="#CBD5E1">SQLite</text>
    </g>
  </g>

  <!-- Card 4: Cisco Marine Academy Credentials -->
  <g transform="translate(655, 380)">
    <rect class="voy-card" x="0" y="0" width="565" height="205" />
    <text class="serif" x="24" y="36" fill="#F8FAFC" font-size="20" font-weight="bold">🛡️ Cisco Marine Academy Protocols</text>
    <text class="mono" x="24" y="54" fill="#34D399" font-size="10.5" font-weight="700" letter-spacing="1px">VERIFIED NETWORKING &amp; SECURITY SEALS</text>

    <rect x="435" y="16" width="106" height="24" rx="12" fill="#064E3B" stroke="#10B981" stroke-width="1" />
    <text class="mono" x="488" y="32" text-anchor="middle" fill="#6EE7B7" font-size="10.5" font-weight="bold">📜 VERIFIED</text>

    <text class="sans" x="24" y="84" fill="#94A3B8" font-size="13">
      <tspan x="24" dy="0">Three verified professional certifications from Cisco Networking Academy:</tspan>
      <tspan x="24" dy="20">Python Essentials 1, Introduction to Cybersecurity, and IT Hardware Basics.</tspan>
      <tspan x="24" dy="20">Backed by authentic credentials and network diagnostic mastery.</tspan>
    </text>

    <g transform="translate(24, 156)">
      <rect class="chip" x="0" y="0" width="135" height="24" fill="#064E3B" stroke="#10B981" />
      <text class="chip-t" x="67" y="16" text-anchor="middle" fill="#6EE7B7">Python Essentials 1</text>
      <rect class="chip" x="143" y="0" width="145" height="24" fill="#134E4A" stroke="#0D9488" />
      <text class="chip-t" x="215" y="16" text-anchor="middle" fill="#5EEAD4">Cybersecurity Intro</text>
      <rect class="chip" x="296" y="0" width="130" height="24" fill="#1E293B" stroke="#64748B" />
      <text class="chip-t" x="361" y="16" text-anchor="middle" fill="#CBD5E1">Hardware Basics</text>
    </g>
  </g>
</svg>"""


# ==============================================================================
# 6. PIRATE ALLIANCE & CONNECT (onepiece-connect.svg) - 1280x440
# ==============================================================================
def make_connect_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 440" width="1280" height="440">
  <defs>
    <linearGradient id="conn-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070C16" />
      <stop offset="100%" stop-color="#111B30" />
    </linearGradient>
    <linearGradient id="conn-line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFD700" />
      <stop offset="50%" stop-color="#FF4500" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>
  </defs>

  <style>
    .panel {{ fill: url(#conn-bg); stroke: #1E293B; stroke-width: 1.5px; rx: 24px; }}
    .conn-card {{ fill: #0B1322; stroke: #1E293B; stroke-width: 1.2px; rx: 14px; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .serif {{ font-family: Georgia, 'Times New Roman', serif; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  </style>

  <rect class="panel" x="0" y="0" width="1280" height="440" />

  <g transform="translate(60, 48)">
    <text class="mono" x="0" y="0" fill="#FFD700" font-size="12" font-weight="700" letter-spacing="2px">05 // PIRATE ALLIANCE &amp; DEN DEN TRANSMISSION</text>
    <text class="serif" x="0" y="38" fill="#F8FAFC" font-size="34" font-weight="bold">READY TO FORM A FLEET ALLIANCE?</text>
    <text class="sans" x="0" y="66" fill="#94A3B8" font-size="15">
      Seeking a reliable First Mate, Full-Stack Engineer, or System Architect for your next high-seas expedition? Connect below!
    </text>
    <line x1="0" y1="84" x2="1160" y2="84" stroke="url(#conn-line)" stroke-width="2" />
  </g>

  <g transform="translate(60, 165)">
    <!-- 1. Portfolio Log Pose -->
    <g transform="translate(0, 0)">
      <rect class="conn-card" x="0" y="0" width="270" height="210" />
      <rect x="20" y="20" width="46" height="46" rx="10" fill="#0C4A6E" stroke="#0284C7" />
      <text class="sans" x="43" y="52" text-anchor="middle" font-size="22">🧭</text>
      <text class="serif" x="20" y="98" fill="#F8FAFC" font-size="18" font-weight="bold">Portfolio Log Pose</text>
      <text class="mono" x="20" y="118" fill="#38BDF8" font-size="10.5" font-weight="700">PERSONAL SHOWCASE</text>
      <text class="sans" x="20" y="146" fill="#94A3B8" font-size="12.5">Explore shipped projects and live interactive demos.</text>
      <text class="mono" x="20" y="186" fill="#FFD700" font-size="11.5" font-weight="600">→ www.ridataki.dev</text>
    </g>

    <!-- 2. LinkedIn Vivre Card -->
    <g transform="translate(295, 0)">
      <rect class="conn-card" x="0" y="0" width="270" height="210" />
      <rect x="20" y="20" width="46" height="46" rx="10" fill="#172554" stroke="#2563EB" />
      <text class="sans" x="43" y="52" text-anchor="middle" font-size="22">📜</text>
      <text class="serif" x="20" y="98" fill="#F8FAFC" font-size="18" font-weight="bold">LinkedIn Vivre Card</text>
      <text class="mono" x="20" y="118" fill="#60A5FA" font-size="10.5" font-weight="700">PROFESSIONAL NETWORK</text>
      <text class="sans" x="20" y="146" fill="#94A3B8" font-size="12.5">Track my journey, career milestones, and network.</text>
      <text class="mono" x="20" y="186" fill="#FFD700" font-size="11.5" font-weight="600">→ /in/rida-taki-bb44a8350</text>
    </g>

    <!-- 3. Den Den Mushi (Email) -->
    <g transform="translate(590, 0)">
      <rect class="conn-card" x="0" y="0" width="270" height="210" />
      <rect x="20" y="20" width="46" height="46" rx="10" fill="#450A0A" stroke="#DC2626" />
      <text class="sans" x="43" y="52" text-anchor="middle" font-size="22">🐌</text>
      <text class="serif" x="20" y="98" fill="#F8FAFC" font-size="18" font-weight="bold">Den Den Mushi</text>
      <text class="mono" x="20" y="118" fill="#F87171" font-size="10.5" font-weight="700">DIRECT INBOX FREQUENCY</text>
      <text class="sans" x="20" y="146" fill="#94A3B8" font-size="12.5">Reach out directly for contracts, teams, or questions.</text>
      <text class="mono" x="20" y="186" fill="#FFD700" font-size="11.5" font-weight="600">→ takirida72@gmail.com</text>
    </g>

    <!-- 4. Grand Fleet (GitHub) -->
    <g transform="translate(885, 0)">
      <rect class="conn-card" x="0" y="0" width="275" height="210" />
      <rect x="20" y="20" width="46" height="46" rx="10" fill="#3B0764" stroke="#9333EA" />
      <text class="sans" x="43" y="52" text-anchor="middle" font-size="22">🏴‍☠️</text>
      <text class="serif" x="20" y="98" fill="#F8FAFC" font-size="18" font-weight="bold">Mugiwara Fleet</text>
      <text class="mono" x="20" y="118" fill="#C084FC" font-size="10.5" font-weight="700">SOURCE CODE REPOSITORIES</text>
      <text class="sans" x="20" y="146" fill="#94A3B8" font-size="12.5">Inspect open-source codebases and public branches.</text>
      <text class="mono" x="20" y="186" fill="#FFD700" font-size="11.5" font-weight="600">→ github.com/Rida1019-taki</text>
    </g>
  </g>
</svg>"""


def main():
    generators = [
        ("onepiece-hero.svg", make_hero_svg),
        ("onepiece-code.svg", make_code_svg),
        ("onepiece-haki-stack.svg", make_haki_stack_svg),
        ("onepiece-wanted-dashboard.svg", make_wanted_dashboard_svg),
        ("onepiece-voyages.svg", make_voyages_svg),
        ("onepiece-connect.svg", make_connect_svg),
    ]

    for name, gen_fn in generators:
        svg_content = gen_fn()
        try:
            ET.fromstring(svg_content)
        except Exception as e:
            print(f"XML Validation Error in {name}: {e}")
            raise e
        
        target = os.path.join(ASSETS, name)
        with open(target, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated {name} successfully (Valid XML, size: {len(svg_content)} bytes)")

if __name__ == "__main__":
    main()
