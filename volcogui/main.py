"""Main application entry point for VolcoGUI."""

import sys


WORKER_MODE = "--volcogui-simulation-worker"


def main():
    """Launch the GUI or dispatch an isolated simulation child process."""
    if len(sys.argv) > 1 and sys.argv[1] == WORKER_MODE:
        from volcogui.backend.simulation_process import main as simulation_process_main

        return simulation_process_main(sys.argv[2:])

    from PyQt6.QtWidgets import QApplication
    from volcogui.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("VolcoGUI")
    app.setOrganizationName("Volco")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    raise SystemExit(main())
