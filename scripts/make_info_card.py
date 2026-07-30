import os
import sys

def generate_info_card(
    name="Anand Ansh",
    handle="AnsHh9094",
    role="Full-Stack & AI Systems Engineer",
    stack="Python · TypeScript · React · Node.js · Docker",
    focus="Building Autonomous Web Agents & Clean Interfaces",
    output_path="info-card.svg"
):
    width = 490
    height = 260

    # Use SMIL animations instead of CSS @keyframes (GitHub strips CSS keyframes from <img> SVGs)
    rows = [
        ("OS", "Arch Linux / WSL"),
        ("Host", f"{name} (@{handle})"),
        ("Role", role),
        ("Stack", stack),
        ("Focus", focus),
    ]

    start_y = 62
    row_height = 32

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <defs>')
    svg.append('    <style>')
    svg.append('      .card-bg { fill: #0d1117; }')
    svg.append('      .header-bar { fill: #161b22; }')
    svg.append('      .title-text { font-family: "Courier New", Courier, monospace; font-size: 12px; fill: #8b949e; font-weight: bold; }')
    svg.append('      .key-text { font-family: "Courier New", Courier, monospace; font-size: 12px; fill: #7ee787; font-weight: bold; }')
    svg.append('      .val-text { font-family: "Courier New", Courier, monospace; font-size: 12px; fill: #c9d1d9; }')
    svg.append('      .prompt-char { font-family: "Courier New", Courier, monospace; font-size: 13px; fill: #79c0ff; font-weight: bold; }')
    svg.append('    </style>')
    svg.append('  </defs>')

    # Background card with rounded corners
    svg.append(f'  <rect width="{width}" height="{height}" rx="10" ry="10" class="card-bg"/>')
    svg.append(f'  <rect width="{width}" height="{height}" rx="10" ry="10" stroke="#30363d" stroke-width="1" fill="none"/>')

    # Header bar
    svg.append(f'  <rect width="{width}" height="32" rx="10" ry="10" class="header-bar"/>')
    svg.append(f'  <rect x="0" y="22" width="{width}" height="10" class="header-bar"/>')

    # Terminal window buttons
    svg.append('  <circle cx="18" cy="16" r="5" fill="#ff5f56"/>')
    svg.append('  <circle cx="34" cy="16" r="5" fill="#ffbd2e"/>')
    svg.append('  <circle cx="50" cy="16" r="5" fill="#27c93f"/>')

    # Title
    svg.append(f'  <text x="{width // 2}" y="20" text-anchor="middle" class="title-text">neofetch --user {handle}</text>')

    # Rows with SMIL fade-in animation (works on GitHub!)
    for i, (key, val) in enumerate(rows):
        y = start_y + (i * row_height)
        delay = round(0.2 + i * 0.15, 2)

        svg.append(f'  <g opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze"/>')
        svg.append(f'    <text x="22" y="{y}" class="prompt-char">&#x276F;</text>')
        svg.append(f'    <text x="40" y="{y}" class="key-text">{key.ljust(7)}:</text>')
        svg.append(f'    <text x="115" y="{y}" class="val-text">{val}</text>')
        svg.append('  </g>')

    # Bottom separator line
    sep_y = start_y + len(rows) * row_height + 8
    svg.append(f'  <line x1="20" y1="{sep_y}" x2="{width - 20}" y2="{sep_y}" stroke="#30363d" stroke-width="0.5"/>')

    # Bottom cursor blink
    cursor_y = sep_y + 18
    svg.append(f'  <text x="22" y="{cursor_y}" class="prompt-char">&#x276F;</text>')
    svg.append(f'  <rect x="38" y="{cursor_y - 10}" width="8" height="13" fill="#58a6ff">')
    svg.append(f'    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>')
    svg.append('  </rect>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Info Card SVG generated at {output_path}")

if __name__ == "__main__":
    generate_info_card()
