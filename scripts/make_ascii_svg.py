import os
import sys
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Bright (space/sparse) -> Dark (dense)

def image_to_ascii(img_path, width=95):
    if not os.path.exists(img_path):
        print(f"Notice: '{img_path}' not found. Generating default ASCII profile portrait...")
        return generate_default_ascii(width)
        
    img = Image.open(img_path).convert("L")
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.52)  # 0.52 adjusts for monospaced font cell aspect ratio
    
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    arr = np.array(img_resized, dtype=np.float32)
    
    # Normalize brightness range for crisp contrast
    min_val, max_val = arr.min(), arr.max()
    if max_val > min_val:
        arr_norm = (arr - min_val) / (max_val - min_val) * 255.0
    else:
        arr_norm = arr
        
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            pixel_val = arr_norm[y, x]
            if pixel_val > 238:  # Clear background
                line += " "
            else:
                # Map 0-255 to RAMP index (0=darkest, 255=brightest)
                idx = int((255.0 - pixel_val) / 255.0 * (len(RAMP) - 1))
                idx = min(max(idx, 0), len(RAMP) - 1)
                line += RAMP[idx]
        lines.append(line)
    return lines

def generate_default_ascii(width=95):
    lines = [
        "              .---.              ",
        "             /     \\             ",
        "            | () () |            ",
        "             \\  ^  /             ",
        "              '|||'              ",
        "             .---.               ",
        "            /     \\              ",
        "           |       |             ",
        "           |   _   |             ",
        "           |  / \\  |             ",
        "           | |   | |             ",
    ]
    padded = [line.center(width) for line in lines]
    return padded

def generate_ascii_svg(ascii_lines, output_svg="ascii-portrait.svg"):
    num_rows = len(ascii_lines)
    num_cols = max(len(line) for line in ascii_lines) if num_rows > 0 else 90
    
    font_size = 9
    char_width = 5.4
    line_height = 10.5
    
    svg_width = int(num_cols * char_width + 30)
    svg_height = int(num_rows * line_height + 30)
    
    row_duration = 0.04  # seconds per row stagger
    row_type_time = 0.3  # duration of line wipe
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('    .ascii-text { font-family: "Fira Code", "Courier New", Courier, monospace; font-size: 9px; fill: #58a6ff; white-space: pre; }')
    svg.append('    .border { stroke: #30363d; stroke-width: 1; fill: none; rx: 10px; ry: 10px; }')
    svg.append('  </style>')
    
    svg.append(f'  <rect width="{svg_width}" height="{svg_height}" class="bg"/>')
    svg.append(f'  <rect width="{svg_width - 2}" height="{svg_height - 2}" x="1" y="1" class="border"/>')
    
    svg.append('  <defs>')
    for r in range(num_rows):
        start_delay = round(r * row_duration, 3)
        svg.append(f'    <clipPath id="clip-row-{r}">')
        svg.append(f'      <rect x="15" y="{15 + r * line_height}" width="0" height="{line_height}">')
        svg.append(f'        <animate attributeName="width" from="0" to="{svg_width - 30}" dur="{row_type_time}s" begin="{start_delay}s" fill="freeze" />')
        svg.append('      </rect>')
        svg.append('    </clipPath>')
    svg.append('  </defs>')
    
    svg.append('  <g class="ascii-text">')
    for r, line in enumerate(ascii_lines):
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        y_pos = 15 + (r + 1) * line_height - 2
        svg.append(f'    <text x="15" y="{y_pos}" clip-path="url(#clip-row-{r})">{escaped_line}</text>')
    svg.append('  </g>')
    
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(output_svg) if os.path.dirname(output_svg) else ".", exist_ok=True)
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"ASCII SVG generated at {output_svg}")

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "data/source-prepped.png"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "ascii-portrait.svg"
    lines = image_to_ascii(img_path)
    generate_ascii_svg(lines, out_path)
