"""Main window for VolcoGUI application."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QGroupBox, QMessageBox,
    QSplitter, QStatusBar, QProgressDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from volcogui.ui.file_import_widget import FileImportWidget
from volcogui.ui.parameter_widget import ParameterWidget
from volcogui.ui.viewer_widget import ViewerWidget
from volcogui.backend.simulation_runner import SimulationWorker


class MainWindow(QMainWindow):
    """Main application window for VolcoGUI."""
    
    def __init__(self):
        super().__init__()
        self.gcode_file = None
        self.output_stl = None
        self.simulation_worker = None
        self.progress_dialog = None
        
        self.setWindowTitle("VolcoGUI - 3D Print Simulator")
        self.setMinimumSize(1200, 800)
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """Set up the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel (controls)
        left_panel = self._create_left_panel()
        
        # Right panel (3D viewer)
        self.viewer_widget = ViewerWidget()
        
        # Splitter to allow resizing
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.viewer_widget)
        splitter.setStretchFactor(0, 1)  # Left panel
        splitter.setStretchFactor(1, 2)  # Right panel gets more space
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Import a G-code file to begin")
        
    def _create_left_panel(self) -> QWidget:
        """Create the left control panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Volco 3D Print Simulator")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # File import section
        self.file_import = FileImportWidget()
        layout.addWidget(self.file_import)
        
        # Parameter section
        self.parameters = ParameterWidget()
        layout.addWidget(self.parameters)
        
        # Run button
        self.run_button = QPushButton("Run Simulation")
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.run_button.setEnabled(False)
        layout.addWidget(self.run_button)
        
        # Spacer
        layout.addStretch()
        
        # Info section
        info_label = QLabel("ℹ️ Drag & drop a .gcode file or use the import button above")
        info_label.setStyleSheet("color: #666; font-size: 11px; padding: 10px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        panel.setMaximumWidth(400)
        return panel
    
    def _connect_signals(self):
        """Connect widget signals to slots."""
        self.file_import.file_selected.connect(self._on_file_selected)
        self.run_button.clicked.connect(self._on_run_simulation)
        
    def _on_file_selected(self, filepath: str):
        """Handle file selection."""
        self.gcode_file = filepath
        self.run_button.setEnabled(True)
        self.status_bar.showMessage(f"Loaded: {filepath}")
        
    def _on_run_simulation(self):
        """Handle run simulation button click."""
        if not self.gcode_file:
            QMessageBox.warning(self, "No File", "Please select a G-code file first.")
            return
        
        # Get parameters
        params = self.parameters.get_parameters()
        
        # Disable controls during simulation
        self.run_button.setEnabled(False)
        self.file_import.setEnabled(False)
        self.parameters.setEnabled(False)
        
        # Create progress dialog
        self.progress_dialog = QProgressDialog("Initializing...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowTitle("Running Simulation")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.canceled.connect(self._cancel_simulation)
        self.progress_dialog.show()
        
        # Create and start worker thread
        self.simulation_worker = SimulationWorker(self.gcode_file, params)
        self.simulation_worker.progress.connect(self._on_simulation_progress)
        self.simulation_worker.finished.connect(self._on_simulation_finished)
        self.simulation_worker.error.connect(self._on_simulation_error)
        self.simulation_worker.start()
        
    def _on_simulation_progress(self, message: str):
        """Handle progress updates from simulation."""
        if self.progress_dialog:
            self.progress_dialog.setLabelText(message)
        self.status_bar.showMessage(message)
        
    def _on_simulation_finished(self, stl_path: str):
        """Handle successful simulation completion."""
        if self.progress_dialog:
            self.progress_dialog.close()
            
        self.output_stl = stl_path
        self.viewer_widget.load_stl(stl_path)
        
        self.status_bar.showMessage(f"Simulation complete! Output: {stl_path}")
        
        # Re-enable controls
        self.run_button.setEnabled(True)
        self.file_import.setEnabled(True)
        self.parameters.setEnabled(True)
        
    def _on_simulation_error(self, error_message: str):
        """Handle simulation error."""
        if self.progress_dialog:
            self.progress_dialog.close()
            
        QMessageBox.critical(self, "Simulation Error", error_message)
        self.status_bar.showMessage("Simulation failed")
        
        # Re-enable controls
        self.run_button.setEnabled(True)
        self.file_import.setEnabled(True)
        self.parameters.setEnabled(True)
        
    def _cancel_simulation(self):
        """Cancel the running simulation."""
        if self.simulation_worker and self.simulation_worker.isRunning():
            self.simulation_worker.terminate()
            self.simulation_worker.wait()
            
        self.status_bar.showMessage("Simulation canceled")
        
        # Re-enable controls
        self.run_button.setEnabled(True)
        self.file_import.setEnabled(True)
        self.parameters.setEnabled(True)
