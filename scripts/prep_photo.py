import sys
import os
import io
import cv2
import numpy as np
from PIL import Image

def prep_photo(input_path, output_path="data/source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: Input photo '{input_path}' not found.")
        sys.exit(1)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Processing photo: {input_path}...")
    
    # Try background removal via rembg
    try:
        from rembg import remove
        with open(input_path, 'rb') as f:
            input_bytes = f.read()
        output_bytes = remove(input_bytes)
        img_pil = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
        print("Background removed successfully using rembg.")
    except Exception as e:
        print(f"Warning: rembg background removal skipped ({e}). Processing direct image...")
        img_pil = Image.open(input_path).convert("RGBA")

    # Composite onto solid white background
    white_bg = Image.new("RGBA", img_pil.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, img_pil).convert("RGB")
    
    # Convert OpenCV image array
    img_np = np.array(composite)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Save result
    cv2.imwrite(output_path, enhanced)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(input_file)
