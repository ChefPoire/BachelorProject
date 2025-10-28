"""
VSItoPNG.py

Converts .VSI (while-slide image) files ot standard PNG images using OpenSlide.

OpenSlide is a fully open-source library for reading whole-slide image formats
(such as .svs, .vsi, .tif). It provides efficient reading of different zoom levels
without needing Java or proprietary software.

Usage:
    python VSItoPNG.py input_file.vsi output_dir/

Dependencies:
    - openslide-python
    - pillow
    - numpy
"""

# Imports
import openslide
import numpy as np
from PIL import Image
import os
import sys

# Define function
def vsi_to_png(input_path, output_dir, level=0):
    """
    Converts a .VSI file into one or more PNG-images.

    Parameters
    ---
    input_path: str
        Path to the .vsi file.
    output_dir: str
        Directory where the PNG-images will be saved.
    level: int, optional
        The OpenSlide zoom level to extract (0 = highest resolution, default).

    Notes
    ---
    .VSI files are often very large, so you may not want to export the full
    resolution image. You can specify a lower level to get a downsampled view.
    """

    # Open the VSI slide
    slide = openslide.OpenSlide(input_path)

    # Get slide dimensions for the chosen level
    width, height = slide.level_dimensions[level]
    print(f"Reading level {level} with size {width}x{height}")

    # Read the entire region at this level
    # (0,0) is the top-left corner
    region = slide.read_region((0,0), level, (width, height))
    # Convert from RGBA to RGB
    region = region.convert("RGB")

    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Construct output filename
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{basename}_L{level}.png")

    # Save image
    region.save(output_path)
    print(f"Saved: {output_path}")

    # Optionally return the numpy array (for potential further processing)
    return np.array(region)

if __name__ == "__main__":
    # Example useage from command line
    if len(sys.argv) < 3:
        print("Usage: python VSItoPNG.py <input.vsi> <output_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    vsi_to_png(input_file, output_folder, level=0)