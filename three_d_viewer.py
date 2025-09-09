# Import packages
import os
import numpy as np
from PIL import Image, ImageEnhance
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog
import pyvista as pv
from pyvistaqt import QtInteractor

# ===== 3D VIEWER WIDGET ===== #

class ThreeDViewer(QWidget):
    """
    A QWidget that integrates a 3D volume viewer using PyVista and QtInteractor.
    This viewer loads 2D image slices (PNGs), stacks themm in 3D and allows
    real-time adjustments like opacity, brightness, contrast, sturation and z-spacing.

    It also supports color inversion, grayscale toggling, screenshots, 
    and background color changes.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # PyVista interactor for 3D rendering
        self.plotter = QtInteractor(self)
        self.layout.addWidget(self.plotter.interactor)

        # Add default scene settings
        self.plotter.add_axes()
        
        # Set default camera to XY view.
        self.plotter.view_xy()
        self.plotter.set_background("gray")

        # Image storage
        self.images = []              # currently displayed images (with filters applied)
        self.original_images = []     # original unmodified images
        self.meshes = []              # PyVista meshes used to display images

        # Display parameters
        self.opacity = 1.0
        self.zspacing = 5.0

        # Image filter parameters
        self.brightness = 1.0
        self.contrast = 1.0
        self.saturation = 1.0
        self.is_grayscale = False

    def load_images(self, folder_path: str):
        """
        Loads all PNG images from the given folder, stores them, 
        resets the grayscale state, and plots them in 3D.
        """
        image_files = sorted([
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(".png")
        ])

        # Load and convert all images to RGBA
        self.original_images = [
            Image.open(img).convert("RGBA") for img in image_files
        ]
        self.images = list(self.original_images)
        self.is_grayscale = False
        self.plot_images()

    def store_images(self, images):
        """
        Store a provided list of images (used when passing images from outside).
        Resets grayscale state, but does not automatically plot.
        """
        self.original_images = list(images)
        self.images = list(images)
        self.is_grayscale = False

    def plot_images(self):
        """
        Clears the current 3D scene and re-plots all stored images
        as textured planes with spacing and opacity applied.
        """
        self.plotter.clear()
        self.meshes = []

        for i, img in enumerate(self.images):

            # Convert PIL image to numpy array
            img_array = np.array(img)

            # Create PyVista texture
            texture = pv.Texture(img_array)
            h, w = img_array.shape[:2]

            # Create plane of correct size
            plane = pv.Plane(i_size=w, j_size=h)

            # Stack slices in z-axis
            plane = plane.translate((0, 0, -i * self.zspacing))
            mesh = self.plotter.add_mesh(plane, texture=texture, opacity=self.opacity, name=f"slice_{i}")
            self.meshes.append(mesh)

        # Reset view to include all objects
        self.plotter.reset_camera()
        self.plotter.render()

    def showEvent(self, event):
        """
        Ensure the PyVista interactor is shown when the widget is displayed.
        """
        super().showEvent(event)
        self.plotter.show()
        self.plotter.render()

    def hideEvent(self, event):
        """
        Hide the PyVista interactor when widget is hidden.
        """
        super().hideEvent(event)
        self.plotter.hide()

    def reset_view(self):
        """
        Reset the camera view to the XY plane and re-center the scene.
        """
        self.plotter.view_xy()
        self.plotter.reset_camera()
        self.plotter.render()

    def invert_colors(self):
        """
        Invert the RGB values of all currently displayed images.
        """
        new_images = []
        for img in self.images:
            arr = np.array(img)
            
            # Invert only RGB channels
            arr[..., :3] = 255 - arr[..., :3]
            new_images.append(Image.fromarray(arr))
        self.images = new_images
        self.plot_images()

    def grayscale(self):
        """
        Toggle between grayscale and original images.
        If not grayscale, convert to grayscale. If grayscale, restore originals.
        """
        if not self.is_grayscale:
            self.images = [img.convert("L").convert("RGBA") for img in self.images]
            self.is_grayscale = True
        else:
            self.images = list(self.original_images)
            self.is_grayscale = False
        self.plot_images()

    def set_bg_color(self, color):
        """
        Set the background color of the 3D scene using a QColor.
        """
        self.plotter.set_background(color.name())
        self.plotter.render()

    def screenshot(self):
        """
        Open a dialog to save a screenshot of the current 3D view as PNG.
        """
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "screenshot.png", "PNG Files (*.png)"
        )
        if path:
            self.plotter.screenshot(path)

    def set_opacity(self, val):
        """
        Set global opacity for all images (scaled from slider 0-100).
        """
        self.opacity = val / 100.0
        self.plot_images()

    def set_zspacing(self, val):
        """
        Set z-axis spacing between slices (slider value by /10).
        """
        self.zspacing = val / 10.0
        self.plot_images()

    def set_brightness(self, val):
        """
        Set brightness scaling (0-2.0 range).
        """
        self.brightness = val / 100.0
        self._apply_filters()

    def set_contrast(self, val):
        """
        Set contrast (0-2.0 range).
        """
        self.contrast = val / 100.0
        self._apply_filters()

    def set_saturation(self, val):
        """
        Set saturation scaling (0-2.0 range).
        """
        self.saturation = val / 100.0
        self._apply_filters()

    def _apply_filters(self):
        """
        Apply brightness, contrast, and saturation adjustments to the original images.
        This overwrites `self.images` with filtered versions while keeping originals intact.
        """
        new_images = []
        for img in self.original_images:

            # Apply brightness
            filtered = ImageEnhance.Brightness(img).enhance(self.brightness)

            # Apply contrast
            filtered = ImageEnhance.Contrast(filtered).enhance(self.contrast)

            # Seperate RGBA channels to apply saturation on RBG only
            r, g, b, a = filtered.split()
            rgb = Image.merge("RGB", (r, g, b))
            rgb = ImageEnhance.Color(rgb).enhance(self.saturation)

            # Merge back with alpha channel
            filtered = Image.merge("RGBA", (*rgb.split(), a))
            new_images.append(filtered)
            
        self.images = new_images
        self.is_grayscale = False
        self.plot_images()
