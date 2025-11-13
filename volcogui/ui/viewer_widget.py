"""3D STL viewer widget using PyVista."""

from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

try:
    from pyvistaqt import QtInteractor
    import pyvista as pv
    PYVISTA_AVAILABLE = True
except ImportError:
    PYVISTA_AVAILABLE = False


class ViewerWidget(QWidget):
    """Widget for displaying 3D STL files interactively."""
    
    def __init__(self):
        super().__init__()
        self.current_mesh = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        if PYVISTA_AVAILABLE:
            # Create PyVista plotter
            self.plotter = QtInteractor(self)
            self.plotter.set_background('white')
            layout.addWidget(self.plotter.interactor)
            
            # Add initial message
            self._show_placeholder()
        else:
            # Fallback if PyVista not available
            label = QLabel("PyVista not available.\nInstall with: uv pip install pyvista pyvistaqt")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: #999; font-size: 14px;")
            layout.addWidget(label)
        
        self.setLayout(layout)
        
    def _show_placeholder(self):
        """Show placeholder text when no model is loaded."""
        if not PYVISTA_AVAILABLE:
            return
            
        self.plotter.clear()
        # Add centered text using viewport coordinates
        self.plotter.add_text(
            "3D Viewer\n\nRun simulation to view results",
            position=(0.35, 0.5),  # Centered position in viewport coordinates
            font_size=14,
            color='gray',
            viewport=True
        )
        
    def load_stl(self, stl_path: str):
        """Load and display an STL file."""
        if not PYVISTA_AVAILABLE:
            return
            
        try:
            # Clear previous mesh
            self.plotter.clear()
            
            # Load mesh
            mesh = pv.read(stl_path)
            self.current_mesh = mesh
            
            # Add mesh to plotter
            self.plotter.add_mesh(
                mesh,
                color='lightblue',
                show_edges=True,
                edge_color='gray',
                opacity=0.9
            )
            
            # Reset camera
            self.plotter.reset_camera()
            self.plotter.view_isometric()
            
            # Add axes
            self.plotter.show_axes()
            
        except Exception as e:
            print(f"Error loading STL: {e}")
            self._show_placeholder()
            
    def clear(self):
        """Clear the viewer."""
        if PYVISTA_AVAILABLE:
            self._show_placeholder()
