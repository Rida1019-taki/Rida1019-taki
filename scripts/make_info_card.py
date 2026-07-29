def generate_info_card(output_svg="info-card.svg"):
    width = 490
    height = 360

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .card {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 8px; }}
    .title-bar {{ fill: #161b22; rx: 8px 8px 0 0; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .text-title {{ font-family: monospace; font-size: 13px; fill: #8b949e; font-weight: bold; }}
    .label {{ font-family: monospace; font-size: 12px; fill: #a78bfa; font-weight: bold; }}
    .value {{ font-family: monospace; font-size: 12px; fill: #c9d1d9; }}
    .highlight {{ font-family: monospace; font-size: 12px; fill: #38bdf8; }}
    
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .line {{ animation: fadeIn 0.4s ease-out forwards; opacity: 0; }}
  </style>

  <rect class="card" width="{width}" height="{height}" />
  <rect class="title-bar" width="{width}" height="32" />
  <circle class="dot-red" cx="16" cy="16" r="5" />
  <circle class="dot-yellow" cx="32" cy="16" r="5" />
  <circle class="dot-green" cx="48" cy="16" r="5" />
  <text class="text-title" x="70" y="21">rida@github:~ (neofetch)</text>

  <g transform="translate(20, 55)">
    <g class="line" style="animation-delay: 0.1s;">
      <text class="label" x="0" y="20">USER</text>
      <text class="value" x="100" y="20">: Rida Taki (@Rida1019-taki)</text>
    </g>
    
    <g class="line" style="animation-delay: 0.25s;">
      <text class="label" x="0" y="50">ROLE</text>
      <text class="value" x="100" y="50">: Full-Stack &amp; Mobile Developer</text>
    </g>

    <g class="line" style="animation-delay: 0.4s;">
      <text class="label" x="0" y="80">NOW</text>
      <text class="highlight" x="100" y="80">: Building HealthCare+ Management Platform</text>
    </g>

    <g class="line" style="animation-delay: 0.55s;">
      <text class="label" x="0" y="110">STACK</text>
      <text class="value" x="100" y="110">: Spring Boot, React.js, Kotlin, Flutter</text>
    </g>

    <g class="line" style="animation-delay: 0.7s;">
      <text class="label" x="0" y="140">DATABASES</text>
      <text class="value" x="100" y="140">: MySQL, SQLite, Firebase</text>
    </g>

    <g class="line" style="animation-delay: 0.85s;">
      <text class="label" x="0" y="170">TOOLS</text>
      <text class="value" x="100" y="170">: Docker, Maven, Git, Linux</text>
    </g>

    <g class="line" style="animation-delay: 1.0s;">
      <text class="label" x="0" y="200">LOCATION</text>
      <text class="value" x="100" y="200">: Morocco 🇲🇦</text>
    </g>

    <g class="line" style="animation-delay: 1.15s;">
      <text class="label" x="0" y="230">QUOTE</text>
      <text class="value" x="100" y="230">: "Transforming coffee into scalable code."</text>
    </g>
  </g>
</svg>'''

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Info Card SVG saved to {output_svg}")

if __name__ == "__main__":
    generate_info_card()