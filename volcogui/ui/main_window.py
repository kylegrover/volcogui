"""Main window for VolcoGUI application."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QGroupBox, QMessageBox,
    QSplitter, QStatusBar, QProgressDialog, QScrollArea,
    QSizePolicy
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
        
        self._apply_dark_theme()
        self._setup_ui()
        self._connect_signals()
    
    def _apply_dark_theme(self):
        """Apply dark theme to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QGroupBox {
                background-color: #252525;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 500;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 5px;
                left: 15px;
                color: #b0b0b0;
            }
            QLabel {
                background-color: transparent;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #252525;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666666;
                border-color: #333333;
            }
            QDoubleSpinBox, QSpinBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                padding: 4px;
                selection-background-color: #4a90d9;
            }
            QDoubleSpinBox:hover, QSpinBox:hover {
                border-color: #4a4a4a;
            }
            QDoubleSpinBox:focus, QSpinBox:focus {
                border-color: #4a90d9;
            }
            QCheckBox {
                color: #e0e0e0;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:hover {
                border-color: #4a4a4a;
            }
            QCheckBox::indicator:checked {
                background-color: #4a90d9;
                border-color: #4a90d9;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNS41IDEwLjVMMiA3bDEuNS0xLjVMNS41IDcuNSAxMi41IDJsMS41IDEuNXoiIGZpbGw9IndoaXRlIi8+PC9zdmc+);
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #252525;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #4a4a4a;
                border-radius: 5px;
                min-height: 30px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5a5a5a;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QStatusBar {
                background-color: #252525;
                color: #b0b0b0;
                border-top: 1px solid #3a3a3a;
            }
            QSplitter::handle {
                background-color: #2d2d2d;
            }
            QSplitter::handle:hover {
                background-color: #3a3a3a;
            }
        """)
        
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
        splitter.setStretchFactor(0, 2)  # Left panel
        splitter.setStretchFactor(1, 3)  # Right panel gets more space
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Import a G-code file to begin")
        
    def _create_left_panel(self) -> QWidget:
        """Create the left control panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: 0; }")
        layout.addWidget(scroll_area, stretch=1)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(5)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidget(scroll_content)
        
        # Title (redundant with main window title)
        # title = QLabel("Volco 3D Print Simulator")
        # title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px 0 5px 0; color: #f0f0f0;")
        # scroll_layout.addWidget(title)
        
        # File import section
        self.file_import = FileImportWidget()
        scroll_layout.addWidget(self.file_import)
        
        # Parameter section
        self.parameters = ParameterWidget()
        scroll_layout.addWidget(self.parameters)
        scroll_layout.addStretch()
        
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
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #2a4a2b;
                color: #666666;
            }
        """)
        self.run_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.run_button.setEnabled(False)
        layout.addWidget(self.run_button)
        
        # Info section
        info_label = QLabel("ℹ️ Drag & drop a .gcode file or use the import button above")
        info_label.setStyleSheet("color: #888; font-size: 11px; padding: 10px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
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
        # DEBUG: Write to file to verify this method is being called
        import tempfile
        try:
            with open(tempfile.gettempdir() + "/volcogui_ui_debug.log", "a") as f:
                f.write(f"UI received: {message}\n")
                f.flush()
        except:
            pass
        
        if self.progress_dialog:
            self.progress_dialog.setLabelText(message)
            # Force immediate update
            self.progress_dialog.repaint()
        self.status_bar.showMessage(message)
        # Process events to ensure UI updates
        from PyQt6.QtCore import QCoreApplication
        QCoreApplication.processEvents()
        
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
