#!/usr/bin/env python3
"""
Generate a burgundy-themed Neofetch-style info card SVG for Sri Sushmita Dasari.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATHS = [
    os.path.join(HERE, "..", "assets", "info-card.svg"),
    os.path.join(HERE, "..", "info-card.svg"),
]

def generate_info_card():
    width = 490
    height = 360

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .card {{ fill: #10070C; stroke: #451126; stroke-width: 1.2px; rx: 12px; }}
    .title-bar {{ fill: #190B12; rx: 12px 12px 0 0; }}
    .dot-1 {{ fill: #701A3D; }}
    .dot-2 {{ fill: #A22B58; }}
    .dot-3 {{ fill: #C77B9B; }}
    .text-title {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 12.5px; fill: #8E5B70; font-weight: 600; }}
    .label {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 11.5px; fill: #C77B9B; font-weight: bold; }}
    .value {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 11.5px; fill: #F8F0F3; }}
    .highlight {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 11.5px; fill: #E5B5C7; font-weight: 600; }}
    
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .line {{ animation: fadeIn 0.4s ease-out forwards; opacity: 0; }}
    @media (prefers-reduced-motion: reduce) {{
      .line {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <rect class="card" width="{width}" height="{height}" />
  <rect class="title-bar" width="{width}" height="34" />
  <circle class="dot-1" cx="20" cy="17" r="5" />
  <circle class="dot-2" cx="36" cy="17" r="5" />
  <circle class="dot-3" cx="52" cy="17" r="5" />
  <text class="text-title" x="72" y="21">sushmita@matrix:~ (neofetch)</text>

  <g transform="translate(22, 58)">
    <g class="line" style="animation-delay: 0.10s;">
      <text class="label" x="0" y="20">IDENTITY</text>
      <text class="value" x="110" y="20">: Sri Sushmita Dasari</text>
    </g>
    
    <g class="line" style="animation-delay: 0.22s;">
      <text class="label" x="0" y="48">POSITION</text>
      <text class="value" x="110" y="48">: AI/ML Engineer &amp; Full-Stack Dev</text>
    </g>

    <g class="line" style="animation-delay: 0.34s;">
      <text class="label" x="0" y="76">ACADEMICS</text>
      <text class="highlight" x="110" y="76">: B.Tech AI/ML @ Aditya (CGPA 9.10)</text>
    </g>

    <g class="line" style="animation-delay: 0.46s;">
      <text class="label" x="0" y="104">HONORS</text>
      <text class="value" x="110" y="104">: Flipkart GRiD 7.0 Semi-Finalist</text>
    </g>

    <g class="line" style="animation-delay: 0.58s;">
      <text class="label" x="0" y="132">HACKATHON</text>
      <text class="value" x="110" y="132">: Myntra HackerRamp Top 100</text>
    </g>

    <g class="line" style="animation-delay: 0.70s;">
      <text class="label" x="0" y="160">STACK</text>
      <text class="value" x="110" y="160">: Java, Python, PyTorch, React, Next</text>
    </g>

    <g class="line" style="animation-delay: 0.82s;">
      <text class="label" x="0" y="188">CLOUD</text>
      <text class="value" x="110" y="188">: AWS AI Practitioner &amp; Foundations</text>
    </g>

    <g class="line" style="animation-delay: 0.94s;">
      <text class="label" x="0" y="216">LOCATION</text>
      <text class="value" x="110" y="216">: India 🇮🇳</text>
    </g>

    <g class="line" style="animation-delay: 1.06s;">
      <text class="label" x="0" y="244">ETHOS</text>
      <text class="value" x="110" y="244">: "Create with intention. Ship with care."</text>
    </g>
  </g>
</svg>'''

    for p in OUT_PATHS:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Saved {p}")

if __name__ == "__main__":
    generate_info_card()
