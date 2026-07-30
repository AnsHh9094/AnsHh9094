import os
import sys
import json
from datetime import datetime

PALETTE = [
    "#161b22",  # Level 0 (None)
    "#0e4429",  # Level 1
    "#006d32",  # Level 2
    "#26a641",  # Level 3
    "#39d353",  # Level 4
    "#69f0a0",  # Level 5 (Top neon peak)
]

def render_heatmap_svg(json_path="data/contributions.json", output_svg="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: Data file '{json_path}' missing.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    username = data.get("username", "user")

    # Dimensions
    svg_width = 860
    svg_height = 180
    cell_size = 11.5
    cell_gap = 3.5
    start_x = 35
    start_y = 45

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1; }')
    svg.append('    .header-text { font-family: "Fira Code", monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }')
    svg.append('    .stat-title { font-family: "Fira Code", monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .stat-val { font-family: "Fira Code", monospace; font-size: 11px; fill: #39d353; font-weight: bold; }')
    svg.append('    .month-text { font-family: "Fira Code", monospace; font-size: 10px; fill: #8b949e; }')
    svg.append('    ')
    svg.append('    @keyframes diagonalEntrance {')
    svg.append('      from { opacity: 0; transform: scale(0.3); }')
    svg.append('      to { opacity: 1; transform: scale(1); }')
    svg.append('    }')
    svg.append('    .cell { transform-origin: center; animation: diagonalEntrance 0.35s ease-out forwards; opacity: 0; }')
    svg.append('  </style>')

    # Background card
    svg.append(f'  <rect width="{svg_width}" height="{svg_height}" class="bg"/>')

    # Header title line
    svg.append(f'  <text x="20" y="28" class="header-text">❯ ./contributions.sh --user {username}</text>')

    # Calculate 53 weeks x 7 days
    # Map days into columns based on week index
    num_days = len(days)
    weeks = []
    current_week = []
    
    for i, d in enumerate(days):
        current_week.append(d)
        if len(current_week) == 7 or i == num_days - 1:
            weeks.append(current_week)
            current_week = []
            
    # Render Heatmap grid
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week):
            x = start_x + col_idx * (cell_size + cell_gap)
            y = start_y + row_idx * (cell_size + cell_gap)
            
            level = day.get("level", 0)
            color = PALETTE[min(level, len(PALETTE) - 1)]
            
            delay = round((col_idx + row_idx) * 0.012, 3)
            
            svg.append(
                f'  <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" '
                f'rx="2.5" ry="2.5" fill="{color}" class="cell" style="animation-delay: {delay}s;">'
                f'<title>{day["date"]}: {day["count"]} contributions</title></rect>'
            )

    # Footer stats & Legend
    footer_y = start_y + 7 * (cell_size + cell_gap) + 20
    
    # Left stats summary
    stats_str = f"Total: {total_contribs:,} | Current Streak: {current_streak} days | Longest: {longest_streak} days"
    svg.append(f'  <text x="35" y="{footer_y}" class="stat-title">{stats_str}</text>')

    # Right side legend ("Less" -> boxes -> "More")
    legend_x_end = svg_width - 35
    svg.append(f'  <text x="{legend_x_end - 110}" y="{footer_y}" class="month-text">Less</text>')
    for idx, c in enumerate(PALETTE[:5]):
        lx = legend_x_end - 80 + idx * 13
        svg.append(f'  <rect x="{lx}" y="{footer_y - 9}" width="10" height="10" rx="2" fill="{c}"/>')
    svg.append(f'  <text x="{legend_x_end - 10}" y="{footer_y}" class="month-text">More</text>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_svg) if os.path.dirname(output_svg) else ".", exist_ok=True)
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Heatmap SVG rendered at {output_svg}")

if __name__ == "__main__":
    j_path = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap_svg(j_path, o_path)
