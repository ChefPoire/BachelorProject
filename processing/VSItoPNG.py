"""
VSItoPNG.py

Converts .VSI files to .PNG files using the bioio library (pure Python, open-source).
"""

# Imports
import os
import sys
import numpy as np
from PIL import Image
import openslide
# from bioio import BioImage

# Function definition
def vsi_to_png(input_path, output_dir, level=0):
    """
    Converts a .VSI whole slide image to PNG using OpenSlide only.
    """

    # Open the VSI slide
    slide = openslide.OpenSlide(input_path)

    # check how many levels are available
    levels = slide.level_count
    print(f"Slide contains {levels} resolution levels")
    if level >= levels:
        raise ValueError(f"Requested level {level} but slide only has {levels} levels.")

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
    output_path = os.path.join(output_dir, f"{base_name}_L{level}.png")

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
    level = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    vsi_to_png(input_file, output_folder, level=0)







# # Define function (BIOFORMATS EDITION)
# def vsi_to_png(input_path, output_dir, level=0):
#     """
#     Converts a .VSI file into a PNG image using bioio.
#     """

#     os.makedirs(output_dir, exist_ok=True)
#     base_name = os.path.splitext(os.path.basename(input_path))[0]

#     # Read the image
#     bio_img = BioImage(input_path)

#     # Select the first scene
#     scene = bio_img.scenes[level] if level < len(bio_img.scenes) else bio_img.scenes[0]
#     bio_img.set_scene(scene)

#     # Convert to numpy (BioImage auto-loads correct shape: [Z, C, Y, X])
#     img_data = bio_img.xarray_data.squeeze().transpose("Y", "X", "C").values

#     # Convert to 8-bit if needed
#     if img_data.dtype != np.uint8:
#         img_data = (255 * (img_data / np.max(img_data))).astype(np.uint8)
    
#     # Create PIL image and save
#     pil_img = Image.fromarray(img_data)
#     output_path = os.path.join(output_dir, f"{base_name}_scene{level}.png")
#     pil_img.save(output_path)

#     print(f"Saved: {output_path}")
#     return img_data
