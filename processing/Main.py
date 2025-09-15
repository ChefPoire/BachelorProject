import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget


# Import the individual screen widgets
from home_screen import HomeScreenWidget
from three_d_viewer_widget import ThreeDViewerWidget
from slice_preparer import SlicePreparerWidget

class MyApp(QMainWindow):
    """
    The main application window.
    It manages multiple 'screens' (Home, 3D Viewer, Slice Preparer)
    using a QStackedWidget.
    """
    
    def __init__(self):
        super().__init__()

        # Set Window Title & Show the window
        self.setWindowTitle("Brain Slice Application")
        self.show()

        # QStackedWidget: Container that can hold multiple widgets,
        # only one is visible at a time.
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of the different screen widgets
        self.home_screen = HomeScreenWidget()
        self.three_d_viewer = ThreeDViewerWidget()
        self.slice_preparer = SlicePreparerWidget()

        # Add the screens to the stacked widget.
        # The order here determines their index (0 = Home, 1 = 3D Viewer, 2 = Slice Preparer)
        self.stacked_widget.addWidget(self.home_screen)      # Index 0 
        self.stacked_widget.addWidget(self.three_d_viewer)   # Index 1 
        self.stacked_widget.addWidget(self.slice_preparer)   # Index 2 

        # Connect signals from home screen to navigation functions (see part below)
        # → When the user clicks a button, the widget emits a signal
        self.home_screen.goto_3d_viewer.connect(self.show_3d_viewer)
        self.home_screen.goto_slice_preparer.connect(self.show_slice_preparer)

        # Connect signals from the viewer/preparer screens to go back to home
        self.three_d_viewer.go_back_to_home.connect(self.show_home_screen)
        self.slice_preparer.go_back_to_home.connect(self.show_home_screen)

        # When the slice preparer has generated slices,
        # it emits them to the 3D viewer for visualization
        self.slice_preparer.viewer_final_output.slices_ready.connect(self.three_d_viewer.receive_image_list)
        
        # Set the initial screen to the home screen / start app on home screen.
        self.show_home_screen()

# ===== NAVIGATION FUNCTIONS ===== #

    def show_home_screen(self):
        """Switches to the home screen."""
        self.stacked_widget.setCurrentIndex(0) # Index 0 self.home_screen

    def show_3d_viewer(self):
        """Switches to the 3D viewer screen."""
        self.stacked_widget.setCurrentIndex(1) # Index 1 self.three_d_viewer

    def show_slice_preparer(self):
        """Switches to the slice preparer screen."""
        self.stacked_widget.setCurrentIndex(2) # Index 2 self.slice_preparer

# ===== APPLICATION ENTRY POINT ===== #

if __name__ == '__main__':

    # Every PyQt application needs exactly one QApplication instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MyApp()

    # Start the QT event loop (keeps the GUI responsive)
    sys.exit(app.exec_())

