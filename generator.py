#!/usr/bin/env python3
import os
import base64
import urllib.request

# Define color schemes
THEMES = {
    "dark": {
        "{{BG_MAIN}}": "#0A101F",
        "{{BG_CARD}}": "#111930",
        "{{BORDER}}": "#1E293B",
        "{{CARD_BORDER}}": "#1E293B",
        "{{TERM_BG}}": "#050B14",
        "{{TEXT}}": "#F8FAFC",
        "{{PRIMARY}}": "#A78BFA",
        "{{SECONDARY}}": "#7C3AED",
        "{{ACCENT_BLUE}}": "#22D3EE",
        "{{ACCENT_GREEN}}": "#10B981",
        "{{MUTED}}": "#94A3B8",
        "{{GLOW_COLOR}}": "rgba(167, 139, 250, 0.15)",
        "{{STATUS_BG}}": "rgba(16, 185, 129, 0.1)",
        "{{TERM_CURSOR}}": "#22D3EE"
    },
    "light": {
        "{{BG_MAIN}}": "#F8FAFC",
        "{{BG_CARD}}": "#FFFFFF",
        "{{BORDER}}": "#E2E8F0",
        "{{CARD_BORDER}}": "#E2E8F0",
        "{{TERM_BG}}": "#0F172A",  # Dark terminal for premium contrast
        "{{TEXT}}": "#0F172A",
        "{{PRIMARY}}": "#7C3AED",
        "{{SECONDARY}}": "#6D28D9",
        "{{ACCENT_BLUE}}": "#0EA5E9",
        "{{ACCENT_GREEN}}": "#059669",
        "{{MUTED}}": "#64748B",
        "{{GLOW_COLOR}}": "rgba(124, 58, 237, 0.08)",
        "{{STATUS_BG}}": "rgba(5, 150, 105, 0.1)",
        "{{TERM_CURSOR}}": "#0EA5E9"
    }
}

SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 380" width="100%" height="380">
  <defs>
    <linearGradient id="avatar-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{{PRIMARY}}" />
      <stop offset="100%" stop-color="{{SECONDARY}}" />
    </linearGradient>
    <radialGradient id="bg-glow" cx="20%" cy="30%" r="60%">
      <stop offset="0%" stop-color="{{GLOW_COLOR}}" />
      <stop offset="100%" stop-color="transparent" />
    </radialGradient>
    <clipPath id="avatar-clip">
      <circle cx="60" cy="105" r="24" />
    </clipPath>
  </defs>

  <style>
    :root {
      --bg-main: {{BG_MAIN}};
      --bg-card: {{BG_CARD}};
      --border: {{BORDER}};
      --card-border: {{CARD_BORDER}};
      --term-bg: {{TERM_BG}};
      --text: {{TEXT}};
      --primary: {{PRIMARY}};
      --secondary: {{SECONDARY}};
      --accent-blue: {{ACCENT_BLUE}};
      --accent-green: {{ACCENT_GREEN}};
      --muted: {{MUTED}};
      --term-cursor: {{TERM_CURSOR}};
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      --font-mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    }

    * {
      box-sizing: border-box;
    }

    text {
      user-select: none;
    }

    /* Global keyframes for elements */
    @keyframes pulse-opacity {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1; }
    }

    @keyframes pulse-glow {
      0%, 100% { filter: drop-shadow(0 0 2px {{PRIMARY}}); }
      50% { filter: drop-shadow(0 0 8px {{PRIMARY}}); }
    }

    /* Cursor blink */
    @keyframes blink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    .cursor {
      animation: blink 0.9s infinite;
      fill: var(--term-cursor);
    }

    /* Command 1: Typing cat info.json (13 chars) */
    @keyframes type-cmd-1 {
      0%, 4% { width: 110px; }
      16%, 52% { width: 0px; }
      55%, 100% { width: 110px; }
    }
    .mask-cmd-1 {
      animation: type-cmd-1 14s infinite steps(13);
    }

    /* JSON Output Lines */
    @keyframes fade-line-2 { 0%, 19% { opacity: 0; } 21%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }
    @keyframes fade-line-3 { 0%, 21% { opacity: 0; } 23%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }
    @keyframes fade-line-4 { 0%, 23% { opacity: 0; } 25%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }
    @keyframes fade-line-5 { 0%, 25% { opacity: 0; } 27%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }
    @keyframes fade-line-6 { 0%, 27% { opacity: 0; } 29%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }
    @keyframes fade-line-7 { 0%, 29% { opacity: 0; } 31%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }
    @keyframes fade-line-8 { 0%, 31% { opacity: 0; } 33%, 52% { opacity: 1; } 54%, 100% { opacity: 0; } }

    .term-l2 { animation: fade-line-2 14s infinite; }
    .term-l3 { animation: fade-line-3 14s infinite; }
    .term-l4 { animation: fade-line-4 14s infinite; }
    .term-l5 { animation: fade-line-5 14s infinite; }
    .term-l6 { animation: fade-line-6 14s infinite; }
    .term-l7 { animation: fade-line-7 14s infinite; }
    .term-l8 { animation: fade-line-8 14s infinite; }

    /* Command 2 prompt appears after command 1 clears */
    @keyframes fade-p2 {
      0%, 54% { opacity: 0; }
      56%, 98% { opacity: 1; }
      100% { opacity: 0; }
    }
    .term-p2 {
      animation: fade-p2 14s infinite;
    }

    /* Command 2: Typing npm run deploy (14 chars) */
    @keyframes type-cmd-2 {
      0%, 56% { width: 120px; }
      68%, 98% { width: 0px; }
      100% { width: 120px; }
    }
    .mask-cmd-2 {
      animation: type-cmd-2 14s infinite steps(14);
    }

    /* Command 2 outputs */
    @keyframes fade-line-10 { 0%, 70% { opacity: 0; } 72%, 98% { opacity: 1; } 100% { opacity: 0; } }
    @keyframes fade-line-11 { 0%, 74% { opacity: 0; } 76%, 98% { opacity: 1; } 100% { opacity: 0; } }
    @keyframes fade-line-12 { 0%, 78% { opacity: 0; } 80%, 98% { opacity: 1; } 100% { opacity: 0; } }
    @keyframes fade-c-end { 0%, 82% { opacity: 0; } 84%, 98% { opacity: 1; } 100% { opacity: 0; } }

    .term-l10 { animation: fade-line-10 14s infinite; }
    .term-l11 { animation: fade-line-11 14s infinite; }
    .term-l12 { animation: fade-line-12 14s infinite; }
    .cursor-end { animation: fade-c-end 14s infinite; }

    /* Skill metrics pulse animation */
    @keyframes bar-expand-backend {
      0% { width: 0px; }
      100% { width: 234px; }
    }
    @keyframes bar-expand-frontend {
      0% { width: 0px; }
      100% { width: 221px; }
    }
    .bar-back {
      animation: bar-expand-backend 1.8s cubic-bezier(0.1, 0.8, 0.2, 1) forwards;
    }
    .bar-front {
      animation: bar-expand-frontend 1.8s cubic-bezier(0.1, 0.8, 0.2, 1) forwards;
    }
  </style>

  <!-- Main Background -->
  <rect width="830" height="380" rx="16" fill="var(--bg-main)" stroke="var(--border)" stroke-width="2"/>
  
  <!-- Glowing Background Effect -->
  <rect x="2" y="2" width="826" height="376" rx="14" fill="url(#bg-glow)" opacity="0.8"/>

  <!-- Window Header -->
  <g id="window-header">
    <circle cx="25" cy="22" r="5" fill="#EF4444" />
    <circle cx="41" cy="22" r="5" fill="#F59E0B" />
    <circle cx="57" cy="22" r="5" fill="#10B981" />
    
    <rect x="180" y="10" width="470" height="24" rx="12" fill="var(--bg-card)" stroke="var(--border)" stroke-width="1"/>
    <text x="415" y="26" text-anchor="middle" font-family="var(--font-mono)" font-size="11" fill="var(--muted)">rida1019-taki / developer-dashboard.json</text>
    
    <g transform="translate(680, 11)">
      <rect width="125" height="22" rx="11" fill="{{STATUS_BG}}" stroke="{{ACCENT_GREEN}}" stroke-opacity="0.3" stroke-width="1"/>
      <circle cx="15" cy="11" r="4" fill="{{ACCENT_GREEN}}">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="26" y="15" font-family="var(--font-sans)" font-size="10" font-weight="bold" fill="{{ACCENT_GREEN}}">SYSTEM ONLINE</text>
    </g>
  </g>

  <!-- Horizontal Divider -->
  <line x1="0" y1="45" x2="830" y2="45" stroke="var(--border)" stroke-width="1.5" />

  <!-- LEFT COLUMN: Profile & Status -->
  <g id="left-column">
    <!-- Card 1: User Profile Widget -->
    <g id="profile-card">
      <rect x="20" y="60" width="290" height="145" rx="12" fill="var(--bg-card)" stroke="var(--border)" stroke-width="1"/>
      
      <!-- Avatar Image Frame -->
      <g style="animation: pulse-glow 3s infinite;">
        {{AVATAR_ELEMENT}}
      </g>
      
      <!-- User Info -->
      <text x="96" y="98" font-family="var(--font-sans)" font-size="16" font-weight="bold" fill="var(--text)">Rida Taki</text>
      <text x="96" y="115" font-family="var(--font-sans)" font-size="11" fill="var(--primary)" font-weight="600">Full-Stack &amp; Mobile Dev</text>
      <text x="96" y="130" font-family="var(--font-sans)" font-size="10" fill="var(--muted)">Morocco 🇲🇦</text>
      
      <!-- Status Pill -->
      <rect x="35" y="155" width="260" height="24" rx="12" fill="{{STATUS_BG}}" stroke="{{ACCENT_GREEN}}" stroke-opacity="0.3" stroke-width="1"/>
      <circle cx="50" cy="167" r="3.5" fill="{{ACCENT_GREEN}}">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <text x="62" y="171" font-family="var(--font-sans)" font-size="9" font-weight="bold" fill="{{ACCENT_GREEN}}">Open to Full-Stack / Backend Internship</text>
    </g>

    <!-- Card 2: Interactive Metrics Grid -->
    <g id="metrics-card">
      <rect x="20" y="215" width="290" height="145" rx="12" fill="var(--bg-card)" stroke="var(--border)" stroke-width="1"/>
      
      <!-- Section Title -->
      <text x="35" y="235" font-family="var(--font-sans)" font-size="10" font-weight="bold" fill="var(--muted)" letter-spacing="1">CURRENT METRICS</text>
      
      <!-- Skill Bar 1: Backend -->
      <text x="35" y="255" font-family="var(--font-sans)" font-size="9.5" fill="var(--text)">Backend: Spring Boot, Java, JPA</text>
      <rect x="35" y="262" width="260" height="6" rx="3" fill="var(--border)"/>
      <rect x="35" y="262" width="234" height="6" rx="3" fill="var(--primary)" class="bar-back"/>
      
      <!-- Skill Bar 2: Frontend & Mobile -->
      <text x="35" y="285" font-family="var(--font-sans)" font-size="9.5" fill="var(--text)">Frontend &amp; Mobile: React, Flutter</text>
      <rect x="35" y="292" width="260" height="6" rx="3" fill="var(--border)"/>
      <rect x="35" y="292" width="221" height="6" rx="3" fill="var(--accent-blue)" class="bar-front"/>
      
      <!-- Bottom Details -->
      <text x="35" y="322" font-family="var(--font-sans)" font-size="9" font-weight="bold" fill="var(--text)">Focus: <tspan fill="var(--primary)">REST APIs</tspan> &amp; <tspan fill="var(--accent-blue)">State Management</tspan></text>
      <text x="35" y="337" font-family="var(--font-sans)" font-size="9" fill="var(--muted)">Education: Technicien Spécialisé, OFPPT</text>
    </g>
  </g>

  <!-- RIGHT COLUMN: Animated bash Terminal -->
  <g id="right-column">
    <!-- Terminal Background -->
    <rect x="325" y="60" width="485" height="300" rx="12" fill="var(--term-bg)" stroke="var(--border)" stroke-width="1.5"/>
    
    <!-- Terminal Tab Bar -->
    <rect x="325" y="60" width="485" height="28" rx="12" fill="#0A0F1D" opacity="0.8"/>
    <text x="345" y="77" font-family="var(--font-mono)" font-size="11" fill="var(--muted)">bash</text>
    <text x="567" y="77" font-family="var(--font-mono)" font-size="10" fill="var(--muted)" text-anchor="end">rida@ubuntu: ~</text>
    <circle cx="790" cy="74" r="3" fill="var(--muted)"/>
    <circle cx="798" cy="74" r="3" fill="var(--muted)"/>
    
    <!-- Console Content Area -->
    <g transform="translate(340, 105)">
      
      <!-- COMMAND 1: cat info.json -->
      <g>
        <text x="0" y="0" font-family="var(--font-mono)" font-size="12" fill="{{PRIMARY}}" font-weight="bold">rida@ubuntu:~$ <tspan fill="var(--text)" font-weight="normal">cat info.json</tspan></text>
        <!-- Overlay mask block to simulate typing -->
        <rect x="110" y="-12" width="110" height="16" fill="var(--term-bg)" class="mask-cmd-1" />
        
        <!-- Blinking cursor during command 1 -->
        <rect x="110" y="-10" width="6" height="12" class="cursor">
          <animate attributeName="x" values="110;118;126;134;142;150;158;166;174;182;190;198;206;214" dur="14s" repeatCount="indefinite" keyTimes="0;0.01;0.02;0.03;0.04;0.05;0.06;0.07;0.08;0.09;0.1;0.11;0.12;0.13" />
          <animate attributeName="opacity" values="1;0" dur="0.9s" repeatCount="indefinite" />
          <animate attributeName="visibility" values="visible;hidden" keyTimes="0;0.52" dur="14s" repeatCount="indefinite"/>
        </rect>
      </g>

      <!-- JSON OUTPUT (Command 1 output) -->
      <text x="10" y="20" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l2">{</text>
      <text x="10" y="38" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l3">  "name": <tspan fill="{{ACCENT_BLUE}}">"Rida Taki"</tspan>,</text>
      <text x="10" y="56" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l4">  "role": <tspan fill="{{ACCENT_BLUE}}">"Full-Stack &amp; Mobile Developer"</tspan>,</text>
      <text x="10" y="74" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l5">  "education": <tspan fill="{{ACCENT_BLUE}}">"OFPPT - ISTA Oued Zem"</tspan>,</text>
      <text x="10" y="92" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l6">  "skills": [<tspan fill="{{PRIMARY}}">"Spring Boot"</tspan>, <tspan fill="{{PRIMARY}}">"React"</tspan>, <tspan fill="{{PRIMARY}}">"Flutter"</tspan>],</text>
      <text x="10" y="110" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l7">  "status": <tspan fill="{{ACCENT_GREEN}}">"Open to Internship Opportunities"</tspan></text>
      <text x="10" y="128" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l8">}</text>

      <!-- COMMAND 2: npm run deploy (appears at y=155) -->
      <g class="term-p2">
        <text x="0" y="155" font-family="var(--font-mono)" font-size="12" fill="{{PRIMARY}}" font-weight="bold">rida@ubuntu:~$ <tspan fill="var(--text)" font-weight="normal">npm run deploy</tspan></text>
        <!-- Overlay mask to simulate typing -->
        <rect x="110" y="143" width="120" height="16" fill="var(--term-bg)" class="mask-cmd-2" />
        
        <!-- Blinking cursor during command 2 -->
        <rect x="110" y="145" width="6" height="12" class="cursor">
          <animate attributeName="x" values="110;118;126;134;142;150;158;166;174;182;190;198;206;214;222" dur="14s" repeatCount="indefinite" keyTimes="0;0.56;0.57;0.58;0.59;0.60;0.61;0.62;0.63;0.64;0.65;0.66;0.67;0.68;0.69" />
          <animate attributeName="opacity" values="1;0" dur="0.9s" repeatCount="indefinite" />
          <animate attributeName="visibility" values="hidden;visible;hidden" keyTimes="0;0.56;0.98" dur="14s" repeatCount="indefinite"/>
        </rect>
      </g>

      <!-- COMMAND 2 OUTPUT -->
      <text x="10" y="178" font-family="var(--font-mono)" font-size="11" fill="var(--muted)" class="term-l10">> healthcare-platform@2.0.0 deploy</text>
      <text x="10" y="196" font-family="var(--font-mono)" font-size="11" fill="{{ACCENT_BLUE}}" class="term-l11">[INFO] Deploying medical dashboard to Vercel...</text>
      <text x="10" y="214" font-family="var(--font-mono)" font-size="11" fill="{{ACCENT_GREEN}}" font-weight="bold" class="term-l12">[SUCCESS] Deployed in 0.8s! https://rida-taki.vercel.app 🚀</text>

      <!-- Idle Cursor at end of run -->
      <rect x="10" y="232" width="6" height="12" fill="var(--term-cursor)" class="cursor-end">
        <animate attributeName="opacity" values="1;0" dur="0.9s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>
</svg>
"""

FOOTER_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 55" width="100%" height="55">
  <style>
    @keyframes pulse-shadow {
      0%, 100% { filter: drop-shadow(0 0 1px {{PRIMARY}}); }
      50% { filter: drop-shadow(0 0 6px {{ACCENT_BLUE}}); }
    }
    .footer-line {
      stroke: url(#footer-grad);
      stroke-width: 2;
      stroke-linecap: round;
      animation: pulse-shadow 4s infinite ease-in-out;
    }
  </style>
  <defs>
    <linearGradient id="footer-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{{PRIMARY}}" />
      <stop offset="50%" stop-color="{{ACCENT_BLUE}}" />
      <stop offset="100%" stop-color="{{PRIMARY}}" />
    </linearGradient>
  </defs>
  <line x1="15" y1="20" x2="815" y2="20" class="footer-line"/>
  <text x="415" y="38" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="{{MUTED}}" letter-spacing="1.5">RIDA TAKI • FULL-STACK &amp; MOBILE DEVELOPER</text>
</svg>
"""


def fetch_avatar_as_base64(username):
    print(f"Fetching GitHub avatar for {username}...")
    url = f"https://github.com/{username}.png"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            image_bytes = response.read()
            b64_data = base64.b64encode(image_bytes).decode("utf-8")
            mime_type = response.headers.get_content_type() or "image/png"
            print("Successfully loaded avatar and converted to Base64.")
            return f'<image href="data:{mime_type};base64,{b64_data}" x="36" y="81" width="48" height="48" clip-path="url(#avatar-clip)"/>'
    except Exception as e:
        print(f"Failed to fetch avatar ({e}). Using default initials vector fallback...")
        return '<circle cx="60" cy="105" r="24" fill="url(#avatar-grad)"/><text x="60" y="111" text-anchor="middle" font-family="var(--font-sans)" font-size="15" font-weight="bold" fill="#FFFFFF">RT</text>'


def generate_svgs():
    # Fetch avatar representation
    avatar_element = fetch_avatar_as_base64("Rida1019-taki")

    print("Generating animated dashboard and footer SVGs...")
    for theme_name, theme_data in THEMES.items():
        # Generate Banner
        banner_filename = f"{theme_name}.svg"
        banner_content = SVG_TEMPLATE
        for placeholder, value in theme_data.items():
            banner_content = banner_content.replace(placeholder, value)
        
        # Inject avatar
        banner_content = banner_content.replace("{{AVATAR_ELEMENT}}", avatar_element)

        with open(banner_filename, "w", encoding="utf-8") as f:
            f.write(banner_content)
        print(f"Successfully generated: {banner_filename}")

        # Generate Footer
        footer_filename = f"footer-{theme_name}.svg"
        footer_content = FOOTER_TEMPLATE
        for placeholder, value in theme_data.items():
            footer_content = footer_content.replace(placeholder, value)
        with open(footer_filename, "w", encoding="utf-8") as f:
            f.write(footer_content)
        print(f"Successfully generated: {footer_filename}")


if __name__ == "__main__":
    generate_svgs()
