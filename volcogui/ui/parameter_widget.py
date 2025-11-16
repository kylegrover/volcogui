"""Parameter input widget for simulation and printer configuration."""

from PyQt6.QtWidgets import (
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QFormLayout,
    QDoubleSpinBox,
    QCheckBox,
    QToolButton,
    QLabel,
)
from PyQt6.QtCore import Qt


class ParameterWidget(QWidget):
    """Widget for configuring simulation and printer parameters."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the user interface."""
        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setSpacing(12)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)

        basic_group = QGroupBox("Quick Settings")
        basic_group.setStyleSheet("font-weight: 500; font-size: 15px; letter-spacing: 0.5px;")
        basic_layout = QFormLayout()
        basic_layout.setSpacing(10)
        basic_layout.setContentsMargins(10, 10, 10, 10)
        
        # Nozzle diameter
        self.nozzle_diameter = QDoubleSpinBox()
        self.nozzle_diameter.setDecimals(2)
        self.nozzle_diameter.setRange(0.1, 5.0)
        self.nozzle_diameter.setSingleStep(0.1)
        self.nozzle_diameter.setValue(0.4)
        self.nozzle_diameter.setSuffix(" mm")
        self.nozzle_diameter.setToolTip("Diameter of the printer nozzle")
        basic_layout.addRow("Nozzle Diameter:", self.nozzle_diameter)
        
        # Voxel size
        self.voxel_size = QDoubleSpinBox()
        self.voxel_size.setDecimals(3)
        self.voxel_size.setRange(0.001, 10.0)
        self.voxel_size.setSingleStep(0.01)
        self.voxel_size.setValue(0.1)
        self.voxel_size.setSuffix(" mm")
        self.voxel_size.setToolTip("Size of each voxel (smaller = higher accuracy but slower)")
        basic_layout.addRow("Voxel Size:", self.voxel_size)
        
        # Step size
        self.step_size = QDoubleSpinBox()
        self.step_size.setDecimals(3)
        self.step_size.setRange(0.001, 10.0)
        self.step_size.setSingleStep(0.01)
        self.step_size.setValue(0.1)
        self.step_size.setSuffix(" mm")
        self.step_size.setToolTip(
            "Distance between simulation steps (smaller = higher accuracy but slower)\n"
            "Reduce this value if you hit divide-by-zero errors"
        )
        basic_layout.addRow("Step Size:", self.step_size)
        
        basic_group.setLayout(basic_layout)
        wrapper_layout.addWidget(basic_group)
        
        printer_group = QGroupBox("Printer")
        printer_group.setStyleSheet("font-weight: 400; font-size: 13px; letter-spacing: 0.5px;")
        printer_layout = QFormLayout()
        printer_layout.setSpacing(10)
        printer_layout.setContentsMargins(10, 15, 10, 10)
        
        # Feedstock filament diameter
        self.feedstock_diameter = QDoubleSpinBox()
        self.feedstock_diameter.setDecimals(2)
        self.feedstock_diameter.setRange(0.5, 3.5)
        self.feedstock_diameter.setSingleStep(0.05)
        self.feedstock_diameter.setValue(1.75)
        self.feedstock_diameter.setSuffix(" mm")
        self.feedstock_diameter.setToolTip("Diameter of the plastic filament entering the extruder")
        printer_layout.addRow("Filament Diameter:", self.feedstock_diameter)
        
        # Nozzle jerk speed
        self.nozzle_jerk_speed = QDoubleSpinBox()
        self.nozzle_jerk_speed.setDecimals(1)
        self.nozzle_jerk_speed.setRange(0.0, 200.0)
        self.nozzle_jerk_speed.setSingleStep(0.5)
        self.nozzle_jerk_speed.setValue(10.0)
        self.nozzle_jerk_speed.setSuffix(" mm/s")
        self.nozzle_jerk_speed.setToolTip("Maximum instantaneous change in nozzle speed")
        printer_layout.addRow("Nozzle Jerk:", self.nozzle_jerk_speed)
        
        # Extruder jerk speed
        self.extruder_jerk_speed = QDoubleSpinBox()
        self.extruder_jerk_speed.setDecimals(1)
        self.extruder_jerk_speed.setRange(0.0, 200.0)
        self.extruder_jerk_speed.setSingleStep(0.5)
        self.extruder_jerk_speed.setValue(5.0)
        self.extruder_jerk_speed.setSuffix(" mm/s")
        self.extruder_jerk_speed.setToolTip("Maximum instantaneous change in extruder speed")
        printer_layout.addRow("Extruder Jerk:", self.extruder_jerk_speed)
        
        # Nozzle acceleration
        self.nozzle_acceleration = QDoubleSpinBox()
        self.nozzle_acceleration.setDecimals(0)
        self.nozzle_acceleration.setRange(0, 50000)
        self.nozzle_acceleration.setSingleStep(100)
        self.nozzle_acceleration.setValue(1000.0)
        self.nozzle_acceleration.setSuffix(" mm/s^2")
        self.nozzle_acceleration.setToolTip("Max acceleration the nozzle planner can use")
        printer_layout.addRow("Nozzle Accel:", self.nozzle_acceleration)
        
        # Extruder acceleration
        self.extruder_acceleration = QDoubleSpinBox()
        self.extruder_acceleration.setDecimals(0)
        self.extruder_acceleration.setRange(0, 50000)
        self.extruder_acceleration.setSingleStep(100)
        self.extruder_acceleration.setValue(5000.0)
        self.extruder_acceleration.setSuffix(" mm/s^2")
        self.extruder_acceleration.setToolTip("Max acceleration for the extruder feeder")
        printer_layout.addRow("Extruder Accel:", self.extruder_acceleration)
        
        printer_group.setLayout(printer_layout)
        wrapper_layout.addWidget(printer_group)
        
        # Simulation parameters
        sim_group = QGroupBox("Simulation")
        sim_group.setStyleSheet("font-weight: 400; font-size: 13px; letter-spacing: 0.5px;")
        sim_layout = QFormLayout()
        sim_layout.setSpacing(10)
        sim_layout.setContentsMargins(10, 15, 10, 10)
        
        # Consider acceleration toggle
        self.consider_acceleration = QCheckBox("Apply acceleration model")
        self.consider_acceleration.setChecked(False)
        self.consider_acceleration.setToolTip("Include acceleration limits when calculating feed rates")
        sim_layout.addRow("Acceleration Model:", self.consider_acceleration)
        
        # Radius increment
        self.radius_increment = QDoubleSpinBox()
        self.radius_increment.setDecimals(4)
        self.radius_increment.setRange(0.0001, 0.01)
        self.radius_increment.setSingleStep(0.0005)
        self.radius_increment.setValue(0.001)
        self.radius_increment.setSuffix(" mm")
        self.radius_increment.setToolTip("Increment used when dilating voxelized filaments")
        sim_layout.addRow("Radius Increment:", self.radius_increment)
        
        # Solver tolerance
        self.solver_tolerance = QDoubleSpinBox()
        self.solver_tolerance.setDecimals(5)
        self.solver_tolerance.setRange(0.00001, 0.01)
        self.solver_tolerance.setSingleStep(0.00005)
        self.solver_tolerance.setValue(0.0001)
        self.solver_tolerance.setSuffix(" mm")
        self.solver_tolerance.setToolTip("Tolerance used by Volco's solver when merging voxels")
        sim_layout.addRow("Solver Tolerance:", self.solver_tolerance)
        
        # STL output mode
        self.stl_ascii = QCheckBox("ASCII STL (larger files)")
        self.stl_ascii.setChecked(False)
        self.stl_ascii.setToolTip("Enable to generate human-readable STL output instead of binary")
        sim_layout.addRow("STL Format:", self.stl_ascii)
        
        sim_group.setLayout(sim_layout)
        wrapper_layout.addWidget(sim_group)
        wrapper_layout.addStretch()
        
    def get_parameters(self) -> dict:
        """Get current parameter values as a dictionary."""
        return {
            'voxel_size': self.voxel_size.value(),
            'step_size': self.step_size.value(),
            'nozzle_diameter': self.nozzle_diameter.value(),
            'feedstock_filament_diameter': self.feedstock_diameter.value(),
            'nozzle_jerk_speed': self.nozzle_jerk_speed.value(),
            'extruder_jerk_speed': self.extruder_jerk_speed.value(),
            'nozzle_acceleration': self.nozzle_acceleration.value(),
            'extruder_acceleration': self.extruder_acceleration.value(),
            'consider_acceleration': self.consider_acceleration.isChecked(),
            'radius_increment': self.radius_increment.value(),
            'solver_tolerance': self.solver_tolerance.value(),
            'stl_ascii': self.stl_ascii.isChecked(),
        }
    
    def set_parameters(self, params: dict):
        """Set parameter values from a dictionary."""
        if 'voxel_size' in params:
            self.voxel_size.setValue(params['voxel_size'])
        if 'step_size' in params:
            self.step_size.setValue(params['step_size'])
        if 'nozzle_diameter' in params:
            self.nozzle_diameter.setValue(params['nozzle_diameter'])
        if 'feedstock_filament_diameter' in params:
            self.feedstock_diameter.setValue(params['feedstock_filament_diameter'])
        if 'nozzle_jerk_speed' in params:
            self.nozzle_jerk_speed.setValue(params['nozzle_jerk_speed'])
        if 'extruder_jerk_speed' in params:
            self.extruder_jerk_speed.setValue(params['extruder_jerk_speed'])
        if 'nozzle_acceleration' in params:
            self.nozzle_acceleration.setValue(params['nozzle_acceleration'])
        if 'extruder_acceleration' in params:
            self.extruder_acceleration.setValue(params['extruder_acceleration'])
        if 'consider_acceleration' in params:
            self.consider_acceleration.setChecked(bool(params['consider_acceleration']))
        if 'radius_increment' in params:
            self.radius_increment.setValue(params['radius_increment'])
        if 'solver_tolerance' in params:
            self.solver_tolerance.setValue(params['solver_tolerance'])
        if 'stl_ascii' in params:
            self.stl_ascii.setChecked(bool(params['stl_ascii']))

    def _toggle_advanced(self, expanded: bool):
        """Show or hide advanced settings container."""
        self.advanced_container.setVisible(expanded)
        arrow = Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow
        self.advanced_toggle.setArrowType(arrow)
