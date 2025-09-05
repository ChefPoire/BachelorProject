# Import packages
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class HomeScreenWidget(QWidget):
    """
    The home screen widget for the Brain Slice Application.
    - Displays the application title
    - Provides two large buttons:
        * One for navigating to the 3D Viewer
        * One for navigating to the Slice Preparer
    - Emits signals when a button is clicked
    """

    # Custom signals that will be emitted when buttons are clicked
    goto_3d_viewer = pyqtSignal()
    goto_slice_preparer = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Build the layout and widgets
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI elements and layout.
        """

        # ===== Main vertical layout ===== #
        layout = QVBoxLayout(self)

        # Center all content
        layout.setAlignment(Qt.AlignCenter)

        # Add flexible empty space at the top
        layout.addStretch()


        # ===== Title Label ===== #
        title_label = QLabel("Brain Slice Application")

        # Center horizontally
        title_label.setAlignment(Qt.AlignCenter)
        
        # Set font and font size
        title_font = QFont()
        title_font.setPointSize(24)
        title_label.setFont(title_font)

        # Add title label
        layout.addWidget(title_label)

        # Add vertical space between title and buttons
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed))


        # ===== Horizontal Layout for the two Buttons ===== #
        button_row_layout = QHBoxLayout()

        # Add flexible space before first button
        button_row_layout.addStretch()

        # Set font and font size for the buttons
        button_font = QFont()
        button_font.setPointSize(16)
        button_font.setBold(True)


        # ===== Button for 3D Viewer =====  #
        btn_3d_viewer = QPushButton("3D Viewer")
        btn_3d_viewer.setFont(button_font)

        # Large fixed button size
        btn_3d_viewer.setFixedSize(200, 70)

        # Connect button click → emit the goto_3d_viewer signal
        btn_3d_viewer.clicked.connect(self.goto_3d_viewer.emit)
        button_row_layout.addWidget(btn_3d_viewer)

        # Add horizontal space between the two buttons
        button_row_layout.addSpacerItem(QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # ===== Button for Slice Preparer ===== #
        btn_slice_preparer = QPushButton("Slice Preparer")
        btn_slice_preparer.setFont(button_font)
        btn_slice_preparer.setFixedSize(200, 70)

        # Connect button click → emit the goto_slice_preparer signal
        btn_slice_preparer.clicked.connect(self.goto_slice_preparer.emit)
        button_row_layout.addWidget(btn_slice_preparer)

        # Add flexible space after second button
        button_row_layout.addStretch()

        # Add the horizontal button row into the main vertical layout
        layout.addLayout(button_row_layout)

        # Add flexible space at the bottem
        layout.addStretch()

