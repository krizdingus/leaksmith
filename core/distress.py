"""
PDF distress effects for authentic leaked document appearance.
"""

import os
import tempfile
import subprocess
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import random

def apply_distress(input_pdf, output_pdf, dpi=150):
    # print(f"[DEBUG] apply_distress called with input={input_pdf}, output={output_pdf}, dpi={dpi}")
    """
    Apply distress effect to a PDF file.
    
    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path to the output PDF file.
        dpi (int): DPI for the output PDF.
    """
    if not os.path.exists(input_pdf):
        raise FileNotFoundError(f"Input PDF file not found: {input_pdf}")

    # Create a temporary directory for intermediate files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert PDF to images
        subprocess.run(['pdftoppm', '-r', str(dpi), input_pdf, os.path.join(temp_dir, 'page')], check=True)

        # Apply distress effect to each image
        for img_file in os.listdir(temp_dir):
            if img_file.endswith('.ppm'):
                img_path = os.path.join(temp_dir, img_file)
                img = Image.open(img_path)
                img_array = np.array(img)
                # Stronger noise
                noise = np.random.normal(0, 40, img_array.shape).astype(np.int16)
                img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
                img = Image.fromarray(img_array)
                # Add blur
                img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
                # Add random lines/stains
                draw = ImageDraw.Draw(img)
                for _ in range(random.randint(3, 8)):
                    x1, y1 = random.randint(0, img.width), random.randint(0, img.height)
                    x2, y2 = random.randint(0, img.width), random.randint(0, img.height)
                    color = (random.randint(0, 80),) * 3
                    width = random.randint(1, 4)
                    draw.line((x1, y1, x2, y2), fill=color, width=width)
                img.save(img_path)

        # Convert images back to PDF
        subprocess.run(['magick', 'convert', os.path.join(temp_dir, '*.ppm'), output_pdf], check=True) 