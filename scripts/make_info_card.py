import os
import sys

def generate_info_card(
    name="Anand Ansh",
    handle="AnshH9094",
    role="Full-Stack & AI Systems Engineer",
    stack="Python • TypeScript • React • Node.js • Docker",
    focus="Building Autonomous Web Agents & Clean Interfaces",
    output_path="info-card.svg"
):
    width = 490
    height = 240
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .card-bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    svg.append('    .header-bar { fill: #161b22; rx: 10px; ry: 10px; }')
    svg.append('    .title-text { font-family: "Fira Code", monospace; font-size: 12px; fill: #8b949e; font-weight: bold; }')
    svg.append('    .prompt-text { font-family: "Fira Code", monospace; font-size: 13px; fill: #79c0ff; font-weight: bold; }')
    svg.append('    .key-text { font-family: "Fira Code", monospace; font-size: 12px; fill: #7ee787; font-weight: bold; }')
    svg.append('    .val-text { font-family: "Fira Code", monospace; font-size: 12px; fill: #c9d1d9; }')
    svg.append('    .sub-text { font-family: "Fira Code", monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    ')
    svg.append('    /* Row fade-in slide keyframes */')
    svg.append('    @keyframes rowFadeIn {')
    svg.append('      from { opacity: 0; transform: translateY(6px); }')
    svg.append('      to { opacity: 1; transform: translateY(0); }')
    svg.append('    }')
    svg.append('    ')
    svg.append('    .animated-row { opacity: 0; animation: rowFadeIn 0.4s ease-out forwards; }')
    svg.append('    .row-1 { animation-delay: 0.1s; }')
    svg.append('    .row-2 { animation-delay: 0.25s; }')
    svg.append('    .row-3 { animation-delay: 0.4s; }')
    svg.append('    .row-4 { animation-delay: 0.55s; }')
    svg.append('    .row-5 { animation-delay: 0.7s; }')
    svg.append('  </style>')
    
    # Outer Card
    svg.append(f'  <rect width="{width}" height="{height}" class="card-bg"/>')
    
    # Header bar
    svg.append(f'  <rect width="{width}" height="32" class="header-bar"/>')
    # Terminal buttons
    svg.append('  <circle cx="18" cy="16" r="5" fill="#ff5f56"/>')
    svg.append('  <circle cx="34" cy="16" r="5" fill="#ffbd2e"/>')
    svg.append('  <circle cx="50" cy="16" r="5" fill="#27c93f"/>')
    
    # Header Title
    svg.append(f'  <text x="{width // 2}" y="20" text-anchor="middle" class="title-text">neofetch --user {handle}</text>')
    
    # Content Body
    start_y = 62
    row_height = 32
    
    rows = [
        ("OS", "Arch Linux / Windows Subsystem for Linux"),
        ("Host", f"{name} (@{handle})"),
        ("Role", role),
        ("Stack", stack),
        ("Focus", focus),
    ]
    
    for i, (key, val) in enumerate(rows):
        y = start_y + (i * row_height)
        svg.append(f'  <g class="animated-row row-{i+1}">')
        svg.append(f'    <text x="22" y="{y}" class="prompt-text">❯</text>')
        svg.append(f'    <text x="40" y="{y}" class="key-text">{key.ljust(7)}:</text>')
        svg.append(f'    <text x="115" y="{y}" class="val-text">{val}</text>')
        svg.append('  </g>')
        
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Info Card SVG generated at {output_path}")

if __name__ == "__main__":
    generate_info_card()
