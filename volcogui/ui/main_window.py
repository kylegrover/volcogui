"""Main window for VolcoGUI application."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QMessageBox,
    QSplitter, QStatusBar, QProgressDialog, QScrollArea,
    QSizePolicy, QDialog, QDialogButtonBox, QPlainTextEdit,
)
from PyQt6.QtCore import Qt

from volcogui.ui.file_import_widget import FileImportWidget
from volcogui.ui.parameter_widget import ParameterWidget
from volcogui.ui.viewer_widget import ViewerWidget
from volcogui.backend.simulation_runner import SimulationWorker, validate_gcode_path


class MainWindow(QMainWindow):
    """Main application window for VolcoGUI."""
    
    def __init__(self):
        super().__init__()
        self.gcode_file = None
        self.output_stl = None
        self.simulation_worker = None
        self.progress_dialog = None
        self.last_run_diagnostics = ""
        self.last_run_summary = ""
        
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
        self.run_log_button = QPushButton("Run Log")
        self.run_log_button.setToolTip("View the bounded output from the most recent run")
        self.run_log_button.setEnabled(False)
        self.run_log_button.clicked.connect(self._show_run_diagnostics)
        self.status_bar.addPermanentWidget(self.run_log_button)
        
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
        self.file_import.file_error.connect(self._on_file_error)
        self.run_button.clicked.connect(self._on_run_simulation)
        
    def _on_file_selected(self, filepath: str):
        """Handle a validated G-code selection."""
        self.gcode_file = filepath
        self.run_button.setEnabled(True)
        self.status_bar.showMessage(f"Loaded: {filepath}")

    def _on_file_error(self, message: str):
        """Report a rejected G-code selection without discarding a valid one."""
        self.status_bar.showMessage(f"Invalid G-code file: {message}", 8000)
        
    def _on_run_simulation(self):
        """Handle run simulation button click."""
        if not self.gcode_file:
            QMessageBox.warning(self, "No File", "Please select a G-code file first.")
            return

        try:
            gcode_path = validate_gcode_path(self.gcode_file)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, "Invalid G-code File", str(exc))
            self.status_bar.showMessage(f"Invalid G-code file: {exc}", 8000)
            return

        # Get parameters
        params = self.parameters.get_parameters()
        
        # Disable controls during simulation
        self.run_button.setEnabled(False)
        self.file_import.setEnabled(False)
        self.parameters.setEnabled(False)
        
        self.last_run_diagnostics = ""
        self.last_run_summary = ""
        self.run_log_button.setEnabled(False)

        # Create progress dialog
        self.progress_dialog = QProgressDialog("Initializing...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Running Simulation")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setFixedWidth(360)
        self.progress_dialog.setStyleSheet("""
            QProgressDialog {
                background-color: #252525;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
            }
            QProgressBar {
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                text-align: center;
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #4a90d9;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        self.progress_dialog.canceled.connect(self._cancel_simulation)
        self.progress_dialog.show()
        
        # Create and start worker thread
        self.simulation_worker = SimulationWorker(str(gcode_path), params)
        self.simulation_worker.progress.connect(self._on_simulation_progress)
        self.simulation_worker.progress_percent.connect(self._on_simulation_progress_percent)
        self.simulation_worker.finished.connect(self._on_simulation_worker_finished)
        self.simulation_worker.start()
        
    def _on_simulation_progress_percent(self, percent: int):
        """Handle progress percentage updates."""
        if self.progress_dialog:
            self.progress_dialog.setValue(percent)

    def _on_simulation_progress(self, message: str):
        """Show worker progress without re-entering the Qt event loop."""
        if self.progress_dialog:
            self.progress_dialog.setLabelText(message)
        self.status_bar.showMessage(message)
        
    def _on_simulation_worker_finished(self):
        """Handle a worker only after its QThread has fully returned."""
        worker = self.simulation_worker
        if not worker:
            return

        worker.wait()
        self.last_run_diagnostics = worker.diagnostics_text
        self.last_run_summary = f"Result: {worker.outcome}\nG-code: {worker.gcode_path}"
        if worker.outcome == "success":
            self.last_run_summary += f"\nSTL: {worker.output_stl}"
        elif worker.outcome == "error":
            self.last_run_summary += f"\nError: {(worker.error_message or 'Unknown error')[:500]}"
        self.run_log_button.setEnabled(True)

        if worker.outcome == "success":
            self._on_simulation_finished(str(worker.output_stl))
        elif worker.outcome == "canceled":
            self._on_simulation_canceled()
        else:
            self._on_simulation_error(worker.error_message or "Simulation failed without an error message.")

    def _on_simulation_finished(self, stl_path: str):
        """Handle engine success and report viewer failures separately."""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        self.output_stl = stl_path
        viewer_error = None
        try:
            self.viewer_widget.load_stl(stl_path)
        except Exception as exc:
            viewer_error = str(exc)

        self._set_simulation_controls_enabled(True)
        if viewer_error:
            self.status_bar.showMessage(f"Simulation complete; could not display STL: {viewer_error}")
            QMessageBox.warning(
                self,
                "Simulation Complete — Viewer Error",
                f"The STL was created successfully at:\n{stl_path}\n\n"
                f"The 3D viewer could not display it:\n{viewer_error}\n\n"
                "The output file is still available at that path.",
            )
        else:
            self.status_bar.showMessage(f"Simulation complete! Output: {stl_path}")
        
    def _on_simulation_error(self, error_message: str):
        """Handle simulation error."""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
            
        QMessageBox.critical(self, "Simulation Error", error_message)
        self.status_bar.showMessage("Simulation failed")
        
        self._set_simulation_controls_enabled(True)

    def _cancel_simulation(self):
        """Request cancellation of the engine process."""
        worker = self.simulation_worker
        if worker and worker.isRunning():
            if self.progress_dialog:
                self.progress_dialog.setLabelText("Canceling simulation...")
                self.progress_dialog.setCancelButton(None)
            self.status_bar.showMessage("Canceling simulation...")
            worker.cancel()

    def _on_simulation_canceled(self):
        """Restore the interface after the child process has stopped."""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        self.status_bar.showMessage("Simulation canceled")
        self._set_simulation_controls_enabled(True)

    def _show_run_diagnostics(self):
        """Display the bounded output retained from the most recent run."""
        if not self.last_run_summary:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Volco Run Log")
        layout = QVBoxLayout(dialog)
        summary = QLabel(self.last_run_summary)
        summary.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(summary)

        output = QPlainTextEdit()
        output.setReadOnly(True)
        output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        output.setPlainText(self.last_run_diagnostics or "No engine output was captured.")
        layout.addWidget(output)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.resize(800, 500)
        dialog.exec()

    def _set_simulation_controls_enabled(self, enabled: bool):
        self.run_button.setEnabled(enabled)
        self.file_import.setEnabled(enabled)
        self.parameters.setEnabled(enabled)

    def closeEvent(self, event):
        """Stop the isolated engine process before destroying the window."""
        worker = self.simulation_worker
        if worker and worker.isRunning():
            worker.cancel()
            worker.wait()
        event.accept()
