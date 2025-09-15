# Import pacckages
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QSlider, QColorDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from image_viewer import ImageViewer
from three_d_viewer import ThreeDViewer

# ===== 3D VIEWER WIDGET ===== #

class ThreeDViewerWidget(QWidget):
    """
    A widget that combines a 3D volume viewer and a 2D image viewer.
    Provides controls (buttons and sliders) for both viewers,
    as well as a navigation back to the home screen.
    """
    # Signal emitted when user clicks 'Home'
    go_back_to_home = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the layout and UI components for the 3D/2D viewer widget.
        - Top section: Side-by-side 3D viewer and 2D image viewer.
        - Middle section: Controls (buttons & sliders) split across 4 columns.
        - Bottem section: 'Home' button to navigate back.
        """

        # --- Main vertical layout for the whole widget ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # --- Row with the 3D viewer and the 2D image viewer ---
        viewers_layout = QHBoxLayout()
        viewers_layout.setContentsMargins(0, 0, 0, 0)

        # 3D brain slice viewer
        self.three_d_viewer_component = ThreeDViewer(self)

        # 2D image viewer
        self.image_viewer_component = ImageViewer(self)

        # Place viewers side by side
        viewers_layout.addWidget(self.three_d_viewer_component, 1)
        viewers_layout.addWidget(self.image_viewer_component, 1)

        # Add to main layout with stretch factor 3 (takes most of the space)
        self.main_layout.addLayout(viewers_layout, 3)

        # --- Helper fuction to create labeled sliders ---
        def make_slider(label_text, min_val, max_val, default_val, slot, step=1):
            layout = QHBoxLayout()
            label = QLabel(label_text)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(default_val)
            slider.setSingleStep(step)
            slider.valueChanged.connect(slot)
            layout.addWidget(label)
            layout.addWidget(slider)
            return layout, slider

        # --- Button control area split into 4 columns ---
        bottom_controls_layout = QHBoxLayout()

        # COLUMN 1: BUTTONS FOR 3D VIEWER
        col_1 = QVBoxLayout()
        col_1.setAlignment(Qt.AlignTop)

        # Select folder
        self.btn_select_folder = QPushButton("Select Folder")
        self.btn_select_folder.clicked.connect(self._select_folder_and_load_3d_slices)
        
        # Reset view
        self.btn_reset_view_3d = QPushButton("Reset View")
        self.btn_reset_view_3d.clicked.connect(self.reset_view_3d)
        
        # Invert colors
        self.btn_invert_colors_3d = QPushButton("Invert Colors")
        self.btn_invert_colors_3d.clicked.connect(self.invert_colors_3d)
        
        # Grayscale
        self.btn_grayscale_3d = QPushButton("Grayscale")
        self.btn_grayscale_3d.clicked.connect(self.grayscale_3d)
        
        # Set background color
        self.btn_bg_color_3d = QPushButton("Set BG Color")
        self.btn_bg_color_3d.clicked.connect(self.set_bg_color_3d)
        
        # Screenshot view
        self.btn_screenshot_3d = QPushButton("Screenshot View")
        self.btn_screenshot_3d.clicked.connect(self.screenshot_3d)

        # Add all buttons to column 1
        for btn in [
            self.btn_select_folder, self.btn_reset_view_3d, self.btn_invert_colors_3d,
            self.btn_grayscale_3d, self.btn_bg_color_3d, self.btn_screenshot_3d
        ]:
            col_1.addWidget(btn)

        # COLUMN 2: SLIDERS FOR 3D VIEWER
        col_2 = QVBoxLayout()
        col_2.setAlignment(Qt.AlignTop)

        # Z-spacing
        layout, self.slider_zspacing_3d =   make_slider("Z-Spacing ", 1, 100, 10, self.set_zspacing_3d)
        col_2.addLayout(layout)

        # Opacity
        layout, self.slider_opacity_3d =    make_slider("Opacity   ", 0, 100, 100, self.set_opacity_3d)
        col_2.addLayout(layout)

        # Brightness
        layout, self.slider_brightness_3d = make_slider("Brightness", 0, 200, 100, self.set_brightness_3d)
        col_2.addLayout(layout)

        # Contrast
        layout, self.slider_contrast_3d =   make_slider("Contrast  ", 0, 200, 100, self.set_contrast_3d)
        col_2.addLayout(layout)

        # Saturation
        layout, self.slider_saturation_3d = make_slider("Saturation", 0, 200, 100, self.set_saturation_3d)
        col_2.addLayout(layout)


        # COLUMN 3: BUTTONS FOR 2D VIEWER
        col_3 = QVBoxLayout()
        col_3.setAlignment(Qt.AlignTop)

        # Select image
        self.btn_select_image = QPushButton("Select Image")
        self.btn_select_image.clicked.connect(self._select_file_and_load_2d_image)
        
        # Invert colors
        self.btn_invert_colors_2d = QPushButton("Invert Colors")
        self.btn_invert_colors_2d.clicked.connect(self.invert_colors_2d)
        
        # Grayscale
        self.btn_grayscale_2d = QPushButton("Grayscale")
        self.btn_grayscale_2d.clicked.connect(self.grayscale_2d)
        
        # Set background color
        self.btn_bg_color_2d = QPushButton("Set BG Color")
        self.btn_bg_color_2d.clicked.connect(self.set_bg_color_2d)
        
        # Screenshot view
        self.btn_screenshot_2d = QPushButton("Screenshot View")
        self.btn_screenshot_2d.clicked.connect(self.screenshot_2d)

        # Add all buttons to column 3
        for btn in [
            self.btn_select_image, self.btn_invert_colors_2d, self.btn_grayscale_2d,
            self.btn_bg_color_2d, self.btn_screenshot_2d
        ]:
            col_3.addWidget(btn)


        # COLUMN 4: SLIDERS FOR 2D VIEWER
        col_4 = QVBoxLayout()
        col_4.setAlignment(Qt.AlignTop)
        
        # Opacity
        layout, self.slider_opacity_2d =    make_slider("Opacity   ", 0, 100, 100, self.set_opacity_2d)
        col_4.addLayout(layout)
        
        # Brightness
        layout, self.slider_brightness_2d = make_slider("Brightness", 0, 200, 100, self.set_brightness_2d)
        col_4.addLayout(layout)
        
        # Contrast
        layout, self.slider_contrast_2d =   make_slider("Contrast  ", 0, 200, 100, self.set_contrast_2d)
        col_4.addLayout(layout)
        
        # Satuartions
        layout, self.slider_saturation_2d = make_slider("Saturation", 0, 200, 100, self.set_saturation_2d)
        col_4.addLayout(layout)

        # Add all 4 columns to bottom layout
        bottom_controls_layout.addLayout(col_1)
        bottom_controls_layout.addLayout(col_2)
        bottom_controls_layout.addLayout(col_3)
        bottom_controls_layout.addLayout(col_4)

        # Add control section to main layout
        self.main_layout.addLayout(bottom_controls_layout, 0)

        # --- Bottom row with Home Button ---

        # Home button at the bottom
        home_layout = QHBoxLayout()
        home_layout.setAlignment(Qt.AlignCenter)
        self.btn_back_to_home = QPushButton("Home")
        self.btn_back_to_home.clicked.connect(self.go_back_to_home.emit)
        home_layout.addWidget(self.btn_back_to_home)
        self.main_layout.addLayout(home_layout)

# ===== METHODS FOR 3D & 2D VIEWER ===== #

    def receive_image_list(self, image_list):
        """
        Receives a list of images (from slice preparer) and 
        loads them into the 3D viewer.
        """
        self.three_d_viewer_component.store_images(image_list)
        self.three_d_viewer_component.plot_images()

    def _select_folder_and_load_3d_slices(self):
        """
        Opens a dialog to select a folder and loads its images
        into the the 3D viewer.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing Slices")
        if folder_path:
            self.three_d_viewer_component.load_images(folder_path)
            self.three_d_viewer_component.plot_images()

    def _select_file_and_load_2d_image(self):
        """
        Opens a dialog to select a single image and loads 
        it into the 2D viewer.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.image_viewer_component.set_image_from_path(file_path)

    def showEvent(self, event):
        """
        Ensure the 3D viewer is properly updated when the widget
        becomes visible.
        """
        super().showEvent(event)
        self.three_d_viewer_component.showEvent(event)

    def hideEvent(self, event):
        """
        Clean up or pause the 3D viewer when the widget is hidden.
        """
        super().hideEvent(event)
        self.three_d_viewer_component.hideEvent(event)

    def reset_view_3d(self):
        """
        Reset the 3D viewer to its default state.
        """ 
        self.three_d_viewer_component.reset_view()

    def invert_colors_3d(self):
        """
        Invert colors in the 3D viewer.
        """ 
        self.three_d_viewer_component.invert_colors()

    def grayscale_3d(self):
        """
        Switch the 3D viewer to grayscale mode.
        """ 
        self.three_d_viewer_component.grayscale()

    def set_bg_color_3d(self):
        """
        Open a color picker dialog and 
        set the 3D viewer background color.
        """
        color = QColorDialog.getColor()
        if color.isValid(): 
            self.three_d_viewer_component.set_bg_color(color)

    def screenshot_3d(self):
        """
        Take a screenshot of the 3D rendering.
        """ 
        self.three_d_viewer_component.screenshot()

    def set_zspacing_3d(self, val):
        """
        Adjust the spacing between slices in the 3D viewer.
        """
        self.three_d_viewer_component.set_zspacing(val)

    def set_opacity_3d(self, val):
        """
        Adjust the opacity of the 3D rendering.
        """ 
        self.three_d_viewer_component.set_opacity(val)

    def set_brightness_3d(self, val):
        """
        Adjust the brightness of the 3D rendering.
        """ 
        self.three_d_viewer_component.set_brightness(val)

    def set_contrast_3d(self, val):
        """
        Adjust the contrast of the 3D rendering.
        """ 
        self.three_d_viewer_component.set_contrast(val)

    def set_saturation_3d(self, val):
        """
        Adjust the saturation of the 3D rendering.
        """ 
        self.three_d_viewer_component.set_saturation(val)

    def invert_colors_2d(self):
        """
        Invert colors in the 2D viewer.
        """ 
        self.image_viewer_component.invert_colors()

    def grayscale_2d(self):
        """
        Switch the 2D viewer to grayscale mode.
        """
        self.image_viewer_component.grayscale()

    def set_bg_color_2d(self):
        """
        Open a color picker dialog and 
        set the 2D viewer background color. 
        """
        color = QColorDialog.getColor()
        if color.isValid(): 
            self.image_viewer_component.set_bg_color(color)

    def screenshot_2d(self):
        """
        take a screenshot of the current 2D view.
        """
        self.image_viewer_component.screenshot()

    def set_opacity_2d(self, val):
        """
        Adjust opacity of the 2D image.
        """
        self.image_viewer_component.set_opacity(val)

    def set_brightness_2d(self, val):
        """
        Adjust brightness of the 2D image.
        """
        self.image_viewer_component.set_brightness(val)

    def set_contrast_2d(self, val):
        
        """
        Adjust contrast of the 2D image.
        """
        self.image_viewer_component.set_contrast(val)

    def set_saturation_2d(self, val):
        """
        Adjust saturation of the 2D image.
        """
        self.image_viewer_component.set_saturation(val)
