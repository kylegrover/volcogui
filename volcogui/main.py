"""Main application entry point for VolcoGUI."""

import sys
from PyQt6.QtWidgets import QApplication
from volcogui.ui.main_window import MainWindow


def main():
    """Launch the VolcoGUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("VolcoGUI")
    app.setOrganizationName("Volco")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
