# Import packages
from PIL import Image
import numpy as np

# Store multiple slices
stored_slices = []

def cut_slice(image: Image.Image, box: tuple) -> Image.Image:
    """
    Crop a rectangular sice from the image.
    """
    return image.crop(box)

def remove_background(image: Image.Image, fg_color=None, bg_color=(255,255,255), grid_size=5, mask_size=15):
    """
    Remove background pixels close to bg_color.
    fg_color can be used for more advanced masking (not implemented here).
    """
    arr = np.array(image.convert("RGBA"))
    r, g, b = bg_color
    threshold = 30
    mask = (np.abs(arr[...,0]-r) < threshold) & (np.abs(arr[...,1]-g) < threshold) & (np.abs(arr[...,2]-b) < threshold)
    arr[mask,3] = 0
    return Image.fromarray(arr)

def adjust_mark(image: Image.Image, fg_or_bg="fg") -> Image.Image:
    """
    Placeholder for FG/BG correction.
    """
    return image

def store_slice(image: Image.Image):
    """
    Store a slice in memory.
    """
    store_slice.append(image.copy())

def get_stored_slices():
    """
    Return list of stored slices.
    """
    return stored_slices

def clear_stored_slices():
    """
    Empty list of stored slices.
    """
    stored_slices.clear()