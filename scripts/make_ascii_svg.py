import os
import sys
import numpy as np
from PIL import Image

# Shorter ramp with cleaner glyphs — avoids noisy chars
RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def image_to_ascii(img_path, width=80):
    """Convert a grayscale image to ASCII lines with clean background handling."""
    if not os.path.exists(img_path):
        print(f"Notice: '{img_path}' not found. Generating placeholder portrait...")
        return generate_placeholder(width)

    img = Image.open(img_path).convert("L")
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)

    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    arr = np.array(img_resized, dtype=np.float32)

    # Normalize to full 0-255 range
    lo, hi = np.percentile(arr, 2), np.percentile(arr, 98)
    if hi - lo < 30:
        lo, hi = arr.min(), arr.max()
    if hi > lo:
        arr = np.clip((arr - lo) / (hi - lo) * 255.0, 0, 255)

    # Determine background brightness (sample corners)
    corners = [
        arr[:5, :5].mean(),
        arr[:5, -5:].mean(),
        arr[-5:, :5].mean(),
        arr[-5:, -5:].mean(),
    ]
    bg_brightness = np.median(corners)

    # Set threshold: anything close to background -> space
    bg_threshold = 40  # pixels within this range of BG are treated as blank

    lines = []
    ramp_len = len(RAMP) - 1
    for y in range(height):
        line = ""
        for x in range(width):
            pv = arr[y, x]
            # If pixel is close to background brightness, use space
            if abs(pv - bg_brightness) < bg_threshold and pv > 180:
                line += " "
            else:
                # Map brightness: 255 (white) -> space end of ramp, 0 (black) -> dense end
                idx = int(pv / 255.0 * ramp_len)
                idx = max(0, min(ramp_len, idx))
                line += RAMP[idx]
        lines.append(line)

    # Trim trailing blank rows
    while lines and lines[-1].strip() == "":
        lines.pop()
    # Trim leading blank rows
    while lines and lines[0].strip() == "":
        lines.pop(0)

    return lines


def generate_placeholder(width=80):
    lines = [
        r"        ___        ",
        r"       /   \       ",
        r"      | o o |      ",
        r"      |  ^  |      ",
        r"       \___/       ",
        r"      /|   |\      ",
        r"     / |   | \     ",
    ]
    return [line.center(width) for line in lines]


def generate_ascii_svg(ascii_lines, output_svg="ascii-portrait.svg"):
    num_rows = len(ascii_lines)
    num_cols = max(len(line) for line in ascii_lines) if num_rows > 0 else 80

    font_size = 8
    char_width = 4.82
    line_height = 9.5

    svg_width = int(num_cols * char_width + 30)
    svg_height = int(num_rows * line_height + 30)

    # Stagger timing
    total_anim_time = 2.5  # total seconds for whole portrait to type in
    row_stagger = total_anim_time / max(num_rows, 1)
    row_wipe_dur = 0.25

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <defs>')
    svg.append('    <style>')
    svg.append('      .bg { fill: #0d1117; }')
    svg.append('      .ascii { font-family: "Courier New", Courier, monospace; font-size: 8px; fill: #58a6ff; white-space: pre; }')
    svg.append('    </style>')
    svg.append('  </defs>')

    # Background
    svg.append(f'  <rect width="{svg_width}" height="{svg_height}" rx="10" ry="10" class="bg"/>')
    svg.append(f'  <rect width="{svg_width - 2}" height="{svg_height - 2}" x="1" y="1" rx="10" ry="10" stroke="#30363d" stroke-width="1" fill="none"/>')

    # Clip paths for row-by-row reveal (SMIL animate — works on GitHub)
    for r in range(num_rows):
        delay = round(r * row_stagger, 3)
        svg.append(f'  <clipPath id="cr{r}">')
        svg.append(f'    <rect x="15" y="{15 + r * line_height}" width="0" height="{line_height}">')
        svg.append(f'      <animate attributeName="width" from="0" to="{svg_width}" dur="{row_wipe_dur}s" begin="{delay}s" fill="freeze"/>')
        svg.append('    </rect>')
        svg.append('  </clipPath>')

    # Text rows
    svg.append('  <g class="ascii">')
    for r, line in enumerate(ascii_lines):
        escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        y_pos = 15 + (r + 1) * line_height - 2
        svg.append(f'    <text x="15" y="{y_pos}" clip-path="url(#cr{r})">{escaped}</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    os.makedirs(os.path.dirname(output_svg) if os.path.dirname(output_svg) else ".", exist_ok=True)
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"ASCII SVG generated at {output_svg} ({num_cols}x{num_rows} chars)")


if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "data/source-prepped.png"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "ascii-portrait.svg"
    lines = image_to_ascii(img_path)
    generate_ascii_svg(lines, out_path)
