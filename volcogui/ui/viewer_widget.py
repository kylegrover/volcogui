"""3D STL viewer widget using PyVista."""

from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QButtonGroup, QToolBar
)
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
        self.current_actor = None
        self.view_mode = 'solid'  # 'solid', 'wireframe', 'surface'
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        if PYVISTA_AVAILABLE:
            # Create toolbar for view controls
            toolbar = self._create_toolbar()
            layout.addWidget(toolbar)
            
            # Create PyVista plotter
            self.plotter = QtInteractor(self)
            self.plotter.set_background('#2d2d2d')
            
            # Enable better lighting and anti-aliasing
            self.plotter.enable_anti_aliasing('msaa')
            
            # Add custom lighting for better material appearance
            self._setup_lighting()
            
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
    
    def _create_toolbar(self) -> QWidget:
        """Create toolbar with view mode controls."""
        toolbar_widget = QWidget()
        toolbar_widget.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border-bottom: 1px solid #3a3a3a;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                padding: 5px 12px;
                margin: 2px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border-color: #4a4a4a;
            }
            QPushButton:checked {
                background-color: #4CAF50;
                color: white;
                border-color: #4CAF50;
            }
            QLabel {
                color: #b0b0b0;
                font-size: 11px;
                font-weight: bold;
                padding: 0 5px;
            }
        """)
        
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(5, 3, 5, 3)
        toolbar_layout.setSpacing(3)
        
        # View mode label
        view_label = QLabel("View Mode:")
        toolbar_layout.addWidget(view_label)
        
        # Create button group for exclusive selection
        self.view_button_group = QButtonGroup(self)
        
        # Solid view button
        self.solid_btn = QPushButton("🔘 Solid")
        self.solid_btn.setCheckable(True)
        self.solid_btn.setChecked(True)
        self.solid_btn.clicked.connect(lambda: self._set_view_mode('solid'))
        self.view_button_group.addButton(self.solid_btn)
        toolbar_layout.addWidget(self.solid_btn)
        
        # Surface with edges button
        self.surface_btn = QPushButton("🔲 Surface + Edges")
        self.surface_btn.setCheckable(True)
        self.surface_btn.clicked.connect(lambda: self._set_view_mode('surface'))
        self.view_button_group.addButton(self.surface_btn)
        toolbar_layout.addWidget(self.surface_btn)
        
        # Wireframe button
        self.wireframe_btn = QPushButton("📐 Wireframe")
        self.wireframe_btn.setCheckable(True)
        self.wireframe_btn.clicked.connect(lambda: self._set_view_mode('wireframe'))
        self.view_button_group.addButton(self.wireframe_btn)
        toolbar_layout.addWidget(self.wireframe_btn)
        
        toolbar_layout.addStretch()
        
        return toolbar_widget
    
    def _setup_lighting(self):
        """Set up lighting for better material rendering."""
        # Remove default lighting
        self.plotter.remove_all_lights()
        
        # Add key light (main light from upper right)
        light1 = pv.Light(position=(2, 2, 3), focal_point=(0, 0, 0), color='white')
        light1.intensity = 0.7
        self.plotter.add_light(light1)
        
        # Add fill light (softer light from left)
        light2 = pv.Light(position=(-2, 1, 2), focal_point=(0, 0, 0), color='white')
        light2.intensity = 0.4
        self.plotter.add_light(light2)
        
        # Add back light for depth
        light3 = pv.Light(position=(0, -2, -1), focal_point=(0, 0, 0), color='white')
        light3.intensity = 0.3
        self.plotter.add_light(light3)
    
    def _set_view_mode(self, mode: str):
        """Change the view mode."""
        self.view_mode = mode
        
        # Re-render current mesh with new mode
        if self.current_mesh is not None:
            self._render_mesh()
    
    def _render_mesh(self):
        """Render the current mesh with current view mode settings."""
        if self.current_mesh is None or self.current_actor is None:
            return
        
        # Remove existing mesh
        self.plotter.remove_actor(self.current_actor)
        
        # Add mesh with appropriate style
        if self.view_mode == 'solid':
            self.current_actor = self.plotter.add_mesh(
                self.current_mesh,
                color='#5DADE2',  # Nice blue color
                smooth_shading=True,
                specular=0.5,
                specular_power=15,
                ambient=0.3,
                diffuse=0.7,
                show_edges=False,
                lighting=True
            )
        elif self.view_mode == 'surface':
            self.current_actor = self.plotter.add_mesh(
                self.current_mesh,
                color='#5DADE2',
                smooth_shading=True,
                specular=0.5,
                specular_power=15,
                ambient=0.3,
                diffuse=0.7,
                show_edges=True,
                edge_color='#2C3E50',
                line_width=1,
                lighting=True
            )
        elif self.view_mode == 'wireframe':
            self.current_actor = self.plotter.add_mesh(
                self.current_mesh,
                style='wireframe',
                color='#2C3E50',
                line_width=1.5,
                lighting=False
            )
        
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
            color='#888888',
            viewport=True
        )
        
    def load_stl(self, stl_path: str):
        """Load and display an STL file."""
        if not PYVISTA_AVAILABLE:
            return
            
        try:
            # Clear previous mesh
            self.plotter.clear()
            
            # Re-setup lighting after clear
            self._setup_lighting()
            
            # Load mesh
            mesh = pv.read(stl_path)
            self.current_mesh = mesh
            
            # Compute normals for better lighting
            if not self.current_mesh.point_normals.size:
                self.current_mesh.compute_normals(inplace=True)
            
            # Add mesh with current view mode
            if self.view_mode == 'solid':
                self.current_actor = self.plotter.add_mesh(
                    self.current_mesh,
                    color='#5DADE2',  # Nice blue color
                    smooth_shading=True,
                    specular=0.5,
                    specular_power=15,
                    ambient=0.3,
                    diffuse=0.7,
                    show_edges=False,
                    lighting=True
                )
            elif self.view_mode == 'surface':
                self.current_actor = self.plotter.add_mesh(
                    self.current_mesh,
                    color='#5DADE2',
                    smooth_shading=True,
                    specular=0.5,
                    specular_power=15,
                    ambient=0.3,
                    diffuse=0.7,
                    show_edges=True,
                    edge_color='#2C3E50',
                    line_width=1,
                    lighting=True
                )
            elif self.view_mode == 'wireframe':
                self.current_actor = self.plotter.add_mesh(
                    self.current_mesh,
                    style='wireframe',
                    color='#2C3E50',
                    line_width=1.5,
                    lighting=False
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
