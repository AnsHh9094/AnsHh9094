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
    "#69f0a0",  # Level 5
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
    cell_size = 11
    cell_gap = 3
    margin_left = 30
    margin_top = 20
    grid_height = 7 * (cell_size + cell_gap)
    footer_height = 30
    svg_height = margin_top + grid_height + footer_height + 10

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <defs>')
    svg.append('    <style>')
    svg.append('      .bg { fill: #0d1117; }')
    svg.append('      .prompt-text { font-family: "Courier New", Courier, monospace; font-size: 12px; fill: #79c0ff; font-weight: bold; }')
    svg.append('      .stat-text { font-family: "Courier New", Courier, monospace; font-size: 10px; fill: #8b949e; }')
    svg.append('      .stat-val { font-family: "Courier New", Courier, monospace; font-size: 10px; fill: #39d353; font-weight: bold; }')
    svg.append('      .legend-text { font-family: "Courier New", Courier, monospace; font-size: 10px; fill: #8b949e; }')
    svg.append('    </style>')
    svg.append('  </defs>')

    # Background
    svg.append(f'  <rect width="{svg_width}" height="{svg_height}" rx="10" ry="10" class="bg"/>')
    svg.append(f'  <rect width="{svg_width - 2}" height="{svg_height - 2}" x="1" y="1" rx="10" ry="10" stroke="#30363d" stroke-width="1" fill="none"/>')

    # Organize days into 53 columns x 7 rows
    # Pad so last day lands at bottom-right
    if days:
        # Find day-of-week for first entry (0=Mon, 6=Sun)
        first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
        first_dow = first_date.weekday()  # 0=Mon
        # GitHub uses Sun=top, so convert: Sun=0, Mon=1, ..., Sat=6
        first_dow_gh = (first_dow + 1) % 7

        # Pad start with empty cells
        padded = [{"date": "", "count": 0, "level": 0}] * first_dow_gh + days

        # Split into weeks of 7
        weeks = []
        for i in range(0, len(padded), 7):
            weeks.append(padded[i:i+7])

        # Limit to last 53 weeks
        if len(weeks) > 53:
            weeks = weeks[-53:]
    else:
        weeks = []

    # Render grid
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week):
            x = margin_left + col_idx * (cell_size + cell_gap)
            y = margin_top + row_idx * (cell_size + cell_gap)

            level = day.get("level", 0)
            color = PALETTE[min(level, len(PALETTE) - 1)]

            # Diagonal stagger for entrance animation
            delay = round((col_idx + row_idx) * 0.008, 3)

            svg.append(
                f'  <rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" '
                f'rx="2.5" ry="2.5" fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay}s" fill="freeze"/>'
            )
            if day.get("date"):
                svg.append(f'    <title>{day["date"]}: {day["count"]} contributions</title>')
            svg.append('  </rect>')

    # Footer: Stats left, Legend right
    footer_y = margin_top + grid_height + 18

    # Stats
    svg.append(f'  <text x="{margin_left}" y="{footer_y}" class="stat-text">'
               f'Total: <tspan class="stat-val">{total_contribs:,}</tspan>'
               f'  |  Current Streak: <tspan class="stat-val">{current_streak} days</tspan>'
               f'  |  Longest: <tspan class="stat-val">{longest_streak} days</tspan></text>')

    # Legend (right side)
    legend_x = svg_width - 130
    svg.append(f'  <text x="{legend_x}" y="{footer_y}" class="legend-text">Less</text>')
    for idx, c in enumerate(PALETTE[:5]):
        lx = legend_x + 30 + idx * 14
        svg.append(f'  <rect x="{lx}" y="{footer_y - 9}" width="10" height="10" rx="2" fill="{c}"/>')
    svg.append(f'  <text x="{legend_x + 30 + 5 * 14 + 2}" y="{footer_y}" class="legend-text">More</text>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_svg) if os.path.dirname(output_svg) else ".", exist_ok=True)
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Heatmap SVG rendered at {output_svg}")

if __name__ == "__main__":
    j_path = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap_svg(j_path, o_path)
