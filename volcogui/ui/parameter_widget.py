"""Parameter input widget for simulation configuration."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QDoubleSpinBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt


class ParameterWidget(QGroupBox):
    """Widget for configuring simulation parameters."""
    
    def __init__(self):
        super().__init__("Simulation Parameters")
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        layout = QFormLayout()
        layout.setSpacing(10)
        
        # Voxel size
        self.voxel_size = QDoubleSpinBox()
        self.voxel_size.setDecimals(3)
        self.voxel_size.setRange(0.001, 10.0)
        self.voxel_size.setSingleStep(0.01)
        self.voxel_size.setValue(0.1)
        self.voxel_size.setSuffix(" mm")
        self.voxel_size.setToolTip("Size of each voxel (smaller = higher accuracy but slower)")
        layout.addRow("Voxel Size:", self.voxel_size)
        
        # Step size
        self.step_size = QDoubleSpinBox()
        self.step_size.setDecimals(3)
        self.step_size.setRange(0.001, 10.0)
        self.step_size.setSingleStep(0.01)
        self.step_size.setValue(0.1)
        self.step_size.setSuffix(" mm")
        self.step_size.setToolTip("Distance between simulation steps (smaller = higher accuracy but slower)")
        layout.addRow("Step Size:", self.step_size)
        
        # Nozzle diameter
        self.nozzle_diameter = QDoubleSpinBox()
        self.nozzle_diameter.setDecimals(2)
        self.nozzle_diameter.setRange(0.1, 5.0)
        self.nozzle_diameter.setSingleStep(0.1)
        self.nozzle_diameter.setValue(0.4)
        self.nozzle_diameter.setSuffix(" mm")
        self.nozzle_diameter.setToolTip("Diameter of the printer nozzle")
        layout.addRow("Nozzle Diameter:", self.nozzle_diameter)
        
        self.setLayout(layout)
        
    def get_parameters(self) -> dict:
        """Get current parameter values as a dictionary."""
        return {
            'voxel_size': self.voxel_size.value(),
            'step_size': self.step_size.value(),
            'nozzle_diameter': self.nozzle_diameter.value()
        }
    
    def set_parameters(self, params: dict):
        """Set parameter values from a dictionary."""
        if 'voxel_size' in params:
            self.voxel_size.setValue(params['voxel_size'])
        if 'step_size' in params:
            self.step_size.setValue(params['step_size'])
        if 'nozzle_diameter' in params:
            self.nozzle_diameter.setValue(params['nozzle_diameter'])
