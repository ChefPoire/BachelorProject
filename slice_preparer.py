# Import packages
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QSizePolicy, QSpacerItem, QSpinBox, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from image_viewer import ImageViewer, SelectionMode

# ===== WIDGET CLASS ===== #

class SlicePreparerWidget(QWidget):
    """
    Widget for preparing 2D slices of brain images.
    Allows image loading, cropping, background removal,
    and storing multiple processed slices for export.
    """

    # Signal to return back to the home screen
    go_back_to_home = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_signals()

    def init_ui(self):
        """
        Build the layout of the slice preparer screen:
        - Three image viewers (original, cropped, final output)
        - Control panels with buttons and spinboxes
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Top row: three image viewers ---
        viewer_row = QHBoxLayout()
        self.viewer_original_image = ImageViewer(self)
        self.viewer_cropped_slice = ImageViewer(self)
        self.viewer_final_output = ImageViewer(self)

        viewer_row.addWidget(self.viewer_original_image, 1)
        viewer_row.addWidget(self.viewer_cropped_slice, 1)
        viewer_row.addWidget(self.viewer_final_output, 1)
        main_layout.addLayout(viewer_row, 3)

        # --- Bottom row: controls ---
        controls_row = QHBoxLayout()
        controls_row.setContentsMargins(0, 0, 0, 0)
        controls_row.setSpacing(10)

        # Column 1: image selection, cut slice, FG/BG selection
        col1_layout = QVBoxLayout()
        col1_layout.setContentsMargins(0, 0, 0, 0)

        grid1 = QGridLayout()
        grid1.setHorizontalSpacing(10)
        grid1.setVerticalSpacing(6)

        # Image selection
        self.btn_select_image = QPushButton("Select Image")
        self.btn_select_image.clicked.connect(self._on_select_image_clicked)
        grid1.addWidget(self.btn_select_image, 0, 0, 1, 2) # 

        # Foreground selection
        self.btn_select_fg = QPushButton("Select Fg")
        self.btn_select_fg.clicked.connect(self._on_select_fg_clicked)
        grid1.addWidget(self.btn_select_fg, 0, 2, 1, 2)

        # Background selection
        self.btn_select_bg = QPushButton("Select Bg")
        self.btn_select_bg.clicked.connect(self._on_select_bg_clicked)
        grid1.addWidget(self.btn_select_bg, 0, 4, 1, 2)

        # Cut slice
        self.btn_cut_slice = QPushButton("Cut Slice")
        self.btn_cut_slice.clicked.connect(self._on_cut_slice_clicked)
        grid1.addWidget(self.btn_cut_slice, 0, 6, 1, 2)
        
        # Grid/mask parameters
        grid1.addWidget(QLabel("Grid Size:"), 2, 0, alignment=Qt.AlignLeft)
        self.spinbox_grid_size = QSpinBox()
        self.spinbox_grid_size.setRange(1, 100)
        self.spinbox_grid_size.setValue(5)
        grid1.addWidget(self.spinbox_grid_size, 2, 1, 1, 2)

        grid1.addWidget(QLabel("Mask Size:"), 2, 4, alignment=Qt.AlignLeft)
        self.spinbox_mask_size = QSpinBox()
        self.spinbox_mask_size.setRange(0, 100)
        self.spinbox_mask_size.setValue(15)
        grid1.addWidget(self.spinbox_mask_size, 2, 5, 1, 2)

        col1_layout.addLayout(grid1)
        col1_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controls_row.addLayout(col1_layout, 1)

        # Column 2: background removal and mask corrections
        col2_layout = QVBoxLayout()
        col2_layout.setContentsMargins(0, 0, 0, 0)

        grid2 = QGridLayout()
        grid2.setHorizontalSpacing(10)
        grid2.setVerticalSpacing(6)
        
        # Remove Background
        self.btn_rm_bg = QPushButton("Rm Bg")
        self.btn_rm_bg.clicked.connect(self._on_remove_background_clicked)
        grid2.addWidget(self.btn_rm_bg, 0, 0)
        
        # Store slice
        self.btn_store_slice = QPushButton("Store Slice")
        self.btn_store_slice.clicked.connect(self._on_store_slice_clicked)
        grid2.addWidget(self.btn_store_slice, 0, 1)

        # Set as Foreground
        self.btn_set_as_fg = QPushButton("Set as Fg")
        self.btn_set_as_fg.clicked.connect(self._on_set_as_fg_clicked)
        grid2.addWidget(self.btn_set_as_fg, 1, 0)

        # Set as Background
        self.btn_set_as_bg = QPushButton("Set as Bg")
        self.btn_set_as_bg.clicked.connect(self._on_set_as_bg_clicked)
        grid2.addWidget(self.btn_set_as_bg, 1, 1)

        col2_layout.addLayout(grid2)
        col2_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controls_row.addLayout(col2_layout, 1)


        # Column 3: slice management and navigation
        col3_layout = QVBoxLayout()
        col3_layout.setContentsMargins(0, 0, 0, 0)

        grid3 = QGridLayout()
        grid3.setHorizontalSpacing(10)
        grid3.setVerticalSpacing(6)

        # Del last slice
        self.btn_del_last_slice = QPushButton("Del Last Slice")
        self.btn_del_last_slice.clicked.connect(self._on_delete_last_slice_clicked)
        grid3.addWidget(self.btn_del_last_slice, 0, 0)

        # Send image to 3D viewer
        self.btn_save_pngs = QPushButton("Send to 3D Viewer")
        self.btn_save_pngs.clicked.connect(self._on_send_clicked)
        grid3.addWidget(self.btn_save_pngs, 0, 1)

        # Back to Home button
        self.btn_back_to_home = QPushButton("Back to Home")
        self.btn_back_to_home.clicked.connect(self.go_back_to_home.emit)
        grid3.addWidget(self.btn_back_to_home, 1, 0, 1, 2, alignment=Qt.AlignRight)

        col3_layout.addLayout(grid3)
        col3_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controls_row.addLayout(col3_layout, 1)

        main_layout.addLayout(controls_row, 1)

    def init_signals(self):
        """
        Connect signals from ImageViewer widgets to handlers.
        """
        self.viewer_original_image.cut_slice_cords.connect(self._on_cut_slice)
        self.viewer_original_image.bg_ref_cords.connect(self._on_select_bg)
        self.viewer_original_image.fg_ref_cords.connect(self._on_select_fg)
        self.viewer_cropped_slice.set_bg_cords.connect(self._on_set_as_bg)
        self.viewer_cropped_slice.set_fg_cords.connect(self._on_set_as_fg)

    # ===== BUTTON HANDLERS ===== #
    def _on_select_image_clicked(self):
        """
        Opens a file dialog and passes the selected image path 
        to the 2D image viewer component.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.viewer_original_image.set_image_from_path(file_path)

    def _on_cut_slice_clicked(self):
        """
        Activate slice cutting mode in the original viewer.
        """
        self.viewer_original_image.set_selection_active(SelectionMode.CUT_SLICE)
    
    def _on_cut_slice(self):
        """
        Triggered after a slice is cut.
        Display cutout in cropped slice viewer.
        """
        cutout = self.viewer_original_image.return_cutout()
        self.viewer_cropped_slice.set_image(cutout)

    def _on_select_fg_clicked(self): #The Button activated method
        """
        Activate FG selection mode 
        (user selects foreground area).
        """
        self.viewer_original_image.set_selection_active(SelectionMode.SELECT_FG_REF)
    
    def _on_select_fg(self):
        """
        Triggered when foreground is selected. Store FG color reference.
        """
        fg_lab = self.viewer_original_image.get_fg_lab()
        self.viewer_cropped_slice._fg_lab_mean = fg_lab

    def _on_select_bg_clicked(self): #The Button activated method
        """
        Activate background selection mode
        (user selects background area).
        """
        self.viewer_original_image.set_selection_active(SelectionMode.SELECT_BG_REF)
    
    def _on_select_bg(self):
        """
        Triggered when background is selected. Store BG color reference.
        """
        bg_lab = self.viewer_original_image.get_bg_lab()
        self.viewer_cropped_slice._bg_lab_mean = bg_lab

    def _on_remove_background_clicked(self):
        """
        Perform background removal on cropped slice.
        """
        grid_size = self.spinbox_grid_size.value()
        mask_size = self.spinbox_mask_size.value()
        self.viewer_cropped_slice.remove_background(grid_size, mask_size)

    def _on_set_as_fg_clicked(self):
        """
        Activate correction mode to set selected area as foreground (visible).
        """
        self.viewer_cropped_slice.set_selection_active(SelectionMode.SET_AS_FG_CORRECTION)    
    
    def _on_set_as_fg(self): # The Signal activated method
        """
        Triggered when foreground correction is confirmed.
        Update mask to show selection
        """
        self.viewer_cropped_slice.adjust_mask(turn_visible=True)

    def _on_set_as_bg_clicked(self):
        """
        Activate correction mode to set selected area as background (invisible).
        """
        self.viewer_cropped_slice.set_selection_active(SelectionMode.SET_AS_BG_CORRECTION)
    
    def _on_set_as_bg(self): # The Signal activated method
        """
        Triggered when background correction is confirmed.
        Update mask to hide selection.
        """
        self.viewer_cropped_slice.adjust_mask(turn_visible=False)

    def _on_store_slice_clicked(self):
        """
        Store the current cropped slice into final output viewer.
        """
        new_slice = self.viewer_cropped_slice._current_pil_image
        self.viewer_final_output.store_slice(new_slice)

    def _on_send_clicked(self):
        """
        Emit stored slices to be used in the 3D viewer.
        """
        self.viewer_final_output.emit_stored_slices()

    def _on_delete_last_slice_clicked(self):
        """
        NOT YET IMPLEMENTED
        Delete the last stored slice.
        """
        pass