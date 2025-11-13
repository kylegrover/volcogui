"""File import widget with drag-drop support."""

from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QFileDialog, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class FileImportWidget(QGroupBox):
    """Widget for importing G-code files via drag-drop or file dialog."""
    
    file_selected = pyqtSignal(str)  # Emits filepath when file is selected
    
    def __init__(self):
        super().__init__("G-code File")
        self.current_file = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Drag-drop area
        self.drop_area = QLabel("Drop .gcode file here")
        self.drop_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 30px;
                background-color: #f5f5f5;
                color: #666;
                font-size: 13px;
            }
        """)
        self.drop_area.setMinimumHeight(100)
        layout.addWidget(self.drop_area)
        
        # File name label
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        self.file_label.setWordWrap(True)
        layout.addWidget(self.file_label)
        
        # Browse button
        browse_button = QPushButton("Browse Files...")
        browse_button.clicked.connect(self._browse_file)
        layout.addWidget(browse_button)
        
        self.setLayout(layout)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1 and urls[0].toLocalFile().endswith('.gcode'):
                event.acceptProposedAction()
                self.drop_area.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #4CAF50;
                        border-radius: 5px;
                        padding: 30px;
                        background-color: #e8f5e9;
                        color: #2e7d32;
                        font-size: 13px;
                    }
                """)
                
    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 30px;
                background-color: #f5f5f5;
                color: #666;
                font-size: 13px;
            }
        """)
        
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        urls = event.mimeData().urls()
        if urls:
            filepath = urls[0].toLocalFile()
            if filepath.endswith('.gcode'):
                self._set_file(filepath)
                event.acceptProposedAction()
        
        # Reset styling
        self.dragLeaveEvent(event)
        
    def _browse_file(self):
        """Open file dialog to browse for G-code file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select G-code File",
            "",
            "G-code Files (*.gcode);;All Files (*)"
        )
        if filepath:
            self._set_file(filepath)
            
    def _set_file(self, filepath: str):
        """Set the selected file and emit signal."""
        self.current_file = filepath
        filename = Path(filepath).name
        self.file_label.setText(f"📄 {filename}")
        self.drop_area.setText(f"✓ {filename}")
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 30px;
                background-color: #e8f5e9;
                color: #2e7d32;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        self.file_selected.emit(filepath)
