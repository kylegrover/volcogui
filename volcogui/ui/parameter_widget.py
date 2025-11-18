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
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt


class NoWheelSpinBox(QDoubleSpinBox):
    """QDoubleSpinBox variant that ignores mouse wheel events.

    This prevents accidental value changes when the user scrolls the
    parameter panel.
    """

    def wheelEvent(self, event):
        event.ignore()
        return


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
        
        # Nozzle diameter with [– value +]
        self.nozzle_diameter = NoWheelSpinBox()
        self.nozzle_diameter.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.nozzle_diameter.setDecimals(2)
        self.nozzle_diameter.setRange(0.1, 5.0)
        self.nozzle_diameter.setSingleStep(0.1)
        self.nozzle_diameter.setValue(0.4)
        self.nozzle_diameter.setSuffix(" mm")
        self.nozzle_diameter.setToolTip("Diameter of the printer nozzle")
        # size and spacing
        self.nozzle_diameter.setFixedHeight(28)
        nozzle_layout = QHBoxLayout()
        nozzle_layout.setContentsMargins(0, 0, 0, 0)
        nozzle_layout.setSpacing(4)
        nozzle_minus = QPushButton("-")
        nozzle_minus.setFixedWidth(30)
        nozzle_minus.setFixedHeight(28)
        nozzle_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        nozzle_layout.addWidget(self.nozzle_diameter)
        nozzle_layout.addWidget(nozzle_minus)
        nozzle_plus = QPushButton("+")
        nozzle_plus.setFixedWidth(30)
        nozzle_plus.setFixedHeight(28)
        nozzle_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        nozzle_layout.addWidget(nozzle_plus)
        basic_layout.addRow("Nozzle Diameter:", nozzle_layout)
        nozzle_plus.clicked.connect(lambda: self.nozzle_diameter.stepUp())
        nozzle_minus.clicked.connect(lambda: self.nozzle_diameter.stepDown())

        # Voxel size with [– value +]
        self.voxel_size = NoWheelSpinBox()
        self.voxel_size.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.voxel_size.setDecimals(3)
        self.voxel_size.setRange(0.001, 10.0)
        self.voxel_size.setSingleStep(0.01)
        self.voxel_size.setValue(0.1)
        self.voxel_size.setSuffix(" mm")
        self.voxel_size.setToolTip("Size of each voxel (smaller = higher accuracy but slower)")
        self.voxel_size.setFixedHeight(28)
        voxel_layout = QHBoxLayout()
        voxel_layout.setContentsMargins(0, 0, 0, 0)
        voxel_layout.setSpacing(4)
        voxel_minus = QPushButton("-")
        voxel_minus.setFixedWidth(30)
        voxel_minus.setFixedHeight(28)
        voxel_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        voxel_layout.addWidget(self.voxel_size)
        voxel_layout.addWidget(voxel_minus)
        voxel_plus = QPushButton("+")
        voxel_plus.setFixedWidth(30)
        voxel_plus.setFixedHeight(28)
        voxel_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        voxel_layout.addWidget(voxel_plus)
        basic_layout.addRow("Voxel Size:", voxel_layout)
        voxel_plus.clicked.connect(lambda: self.voxel_size.stepUp())
        voxel_minus.clicked.connect(lambda: self.voxel_size.stepDown())

        # Step size with [– value +]
        self.step_size = NoWheelSpinBox()
        self.step_size.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.step_size.setDecimals(3)
        self.step_size.setRange(0.001, 10.0)
        self.step_size.setSingleStep(0.01)
        self.step_size.setValue(0.1)
        self.step_size.setSuffix(" mm")
        self.step_size.setToolTip(
            "Distance between simulation steps (smaller = higher accuracy but slower)\n"
            "Reduce this value if you hit divide-by-zero errors"
        )
        self.step_size.setFixedHeight(28)
        step_layout = QHBoxLayout()
        step_layout.setContentsMargins(0, 0, 0, 0)
        step_layout.setSpacing(4)
        step_minus = QPushButton("-")
        step_minus.setFixedWidth(30)
        step_minus.setFixedHeight(28)
        step_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        step_layout.addWidget(self.step_size)
        step_layout.addWidget(step_minus)
        step_plus = QPushButton("+")
        step_plus.setFixedWidth(30)
        step_plus.setFixedHeight(28)
        step_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        step_layout.addWidget(step_plus)
        basic_layout.addRow("Step Size:", step_layout)
        step_plus.clicked.connect(lambda: self.step_size.stepUp())
        step_minus.clicked.connect(lambda: self.step_size.stepDown())
        
        basic_group.setLayout(basic_layout)
        wrapper_layout.addWidget(basic_group)
        
        printer_group = QGroupBox("Printer")
        printer_group.setStyleSheet("font-weight: 400; font-size: 13px; letter-spacing: 0.5px;")
        printer_layout = QFormLayout()
        printer_layout.setSpacing(10)
        printer_layout.setContentsMargins(10, 15, 10, 10)
        
        # Feedstock filament diameter with [− value +]
        self.feedstock_diameter = NoWheelSpinBox()
        self.feedstock_diameter.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.feedstock_diameter.setDecimals(2)
        self.feedstock_diameter.setRange(0.5, 3.5)
        self.feedstock_diameter.setSingleStep(0.05)
        self.feedstock_diameter.setValue(1.75)
        self.feedstock_diameter.setSuffix(" mm")
        self.feedstock_diameter.setToolTip("Diameter of the plastic filament entering the extruder")
        self.feedstock_diameter.setFixedHeight(28)
        feed_layout = QHBoxLayout()
        feed_layout.setContentsMargins(0, 0, 0, 0)
        feed_layout.setSpacing(4)
        feed_minus = QPushButton("-")
        feed_minus.setFixedWidth(30)
        feed_minus.setFixedHeight(28)
        feed_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        feed_layout.addWidget(self.feedstock_diameter)
        feed_layout.addWidget(feed_minus)
        feed_plus = QPushButton("+")
        feed_plus.setFixedWidth(30)
        feed_plus.setFixedHeight(28)
        feed_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        feed_layout.addWidget(feed_plus)
        printer_layout.addRow("Filament Diameter:", feed_layout)
        feed_plus.clicked.connect(lambda: self.feedstock_diameter.stepUp())
        feed_minus.clicked.connect(lambda: self.feedstock_diameter.stepDown())

        # Nozzle jerk speed with [− value +]
        self.nozzle_jerk_speed = NoWheelSpinBox()
        self.nozzle_jerk_speed.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.nozzle_jerk_speed.setDecimals(1)
        self.nozzle_jerk_speed.setRange(0.0, 200.0)
        self.nozzle_jerk_speed.setSingleStep(0.5)
        self.nozzle_jerk_speed.setValue(10.0)
        self.nozzle_jerk_speed.setSuffix(" mm/s")
        self.nozzle_jerk_speed.setToolTip("Maximum instantaneous change in nozzle speed")
        self.nozzle_jerk_speed.setFixedHeight(28)
        jerk_layout = QHBoxLayout()
        jerk_layout.setContentsMargins(0, 0, 0, 0)
        jerk_layout.setSpacing(4)
        jerk_minus = QPushButton("-")
        jerk_minus.setFixedWidth(30)
        jerk_minus.setFixedHeight(28)
        jerk_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        jerk_layout.addWidget(self.nozzle_jerk_speed)
        jerk_layout.addWidget(jerk_minus)
        jerk_plus = QPushButton("+")
        jerk_plus.setFixedWidth(30)
        jerk_plus.setFixedHeight(28)
        jerk_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        jerk_layout.addWidget(jerk_plus)
        printer_layout.addRow("Nozzle Jerk:", jerk_layout)
        jerk_plus.clicked.connect(lambda: self.nozzle_jerk_speed.stepUp())
        jerk_minus.clicked.connect(lambda: self.nozzle_jerk_speed.stepDown())

        # Extruder jerk speed with [− value +]
        self.extruder_jerk_speed = NoWheelSpinBox()
        self.extruder_jerk_speed.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.extruder_jerk_speed.setDecimals(1)
        self.extruder_jerk_speed.setRange(0.0, 200.0)
        self.extruder_jerk_speed.setSingleStep(0.5)
        self.extruder_jerk_speed.setValue(5.0)
        self.extruder_jerk_speed.setSuffix(" mm/s")
        self.extruder_jerk_speed.setToolTip("Maximum instantaneous change in extruder speed")
        self.extruder_jerk_speed.setFixedHeight(28)
        ext_jerk_layout = QHBoxLayout()
        ext_jerk_layout.setContentsMargins(0, 0, 0, 0)
        ext_jerk_layout.setSpacing(4)
        ext_jerk_minus = QPushButton("-")
        ext_jerk_minus.setFixedWidth(30)
        ext_jerk_minus.setFixedHeight(28)
        ext_jerk_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        ext_jerk_layout.addWidget(self.extruder_jerk_speed)
        ext_jerk_layout.addWidget(ext_jerk_minus)
        ext_jerk_plus = QPushButton("+")
        ext_jerk_plus.setFixedWidth(30)
        ext_jerk_plus.setFixedHeight(28)
        ext_jerk_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        ext_jerk_layout.addWidget(ext_jerk_plus)
        printer_layout.addRow("Extruder Jerk:", ext_jerk_layout)
        ext_jerk_plus.clicked.connect(lambda: self.extruder_jerk_speed.stepUp())
        ext_jerk_minus.clicked.connect(lambda: self.extruder_jerk_speed.stepDown())

        # Nozzle acceleration with [− value +]
        self.nozzle_acceleration = NoWheelSpinBox()
        self.nozzle_acceleration.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.nozzle_acceleration.setDecimals(0)
        self.nozzle_acceleration.setRange(0, 50000)
        self.nozzle_acceleration.setSingleStep(100)
        self.nozzle_acceleration.setValue(1000.0)
        self.nozzle_acceleration.setSuffix(" mm/s^2")
        self.nozzle_acceleration.setToolTip("Max acceleration the nozzle planner can use")
        self.nozzle_acceleration.setFixedHeight(28)
        accel_layout = QHBoxLayout()
        accel_layout.setContentsMargins(0, 0, 0, 0)
        accel_layout.setSpacing(4)
        accel_minus = QPushButton("-")
        accel_minus.setFixedWidth(30)
        accel_minus.setFixedHeight(28)
        accel_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        accel_layout.addWidget(self.nozzle_acceleration)
        accel_layout.addWidget(accel_minus)
        accel_plus = QPushButton("+")
        accel_plus.setFixedWidth(30)
        accel_plus.setFixedHeight(28)
        accel_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        accel_layout.addWidget(accel_plus)
        printer_layout.addRow("Nozzle Accel:", accel_layout)
        accel_plus.clicked.connect(lambda: self.nozzle_acceleration.stepUp())
        accel_minus.clicked.connect(lambda: self.nozzle_acceleration.stepDown())

        # Extruder acceleration with [− value +]
        self.extruder_acceleration = NoWheelSpinBox()
        self.extruder_acceleration.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.extruder_acceleration.setDecimals(0)
        self.extruder_acceleration.setRange(0, 50000)
        self.extruder_acceleration.setSingleStep(100)
        self.extruder_acceleration.setValue(5000.0)
        self.extruder_acceleration.setSuffix(" mm/s^2")
        self.extruder_acceleration.setToolTip("Max acceleration for the extruder feeder")
        self.extruder_acceleration.setFixedHeight(28)
        extr_accel_layout = QHBoxLayout()
        extr_accel_layout.setContentsMargins(0, 0, 0, 0)
        extr_accel_layout.setSpacing(4)
        extr_accel_minus = QPushButton("-")
        extr_accel_minus.setFixedWidth(30)
        extr_accel_minus.setFixedHeight(28)
        extr_accel_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        extr_accel_layout.addWidget(self.extruder_acceleration)
        extr_accel_layout.addWidget(extr_accel_minus)
        extr_accel_plus = QPushButton("+")
        extr_accel_plus.setFixedWidth(30)
        extr_accel_plus.setFixedHeight(28)
        extr_accel_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        extr_accel_layout.addWidget(extr_accel_plus)
        printer_layout.addRow("Extruder Accel:", extr_accel_layout)
        extr_accel_plus.clicked.connect(lambda: self.extruder_acceleration.stepUp())
        extr_accel_minus.clicked.connect(lambda: self.extruder_acceleration.stepDown())
        
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
        
        # Radius increment with [− value +]
        self.radius_increment = NoWheelSpinBox()
        self.radius_increment.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.radius_increment.setDecimals(4)
        self.radius_increment.setRange(0.0001, 0.01)
        self.radius_increment.setSingleStep(0.0005)
        self.radius_increment.setValue(0.001)
        self.radius_increment.setSuffix(" mm")
        self.radius_increment.setToolTip("Increment used when dilating voxelized filaments")
        self.radius_increment.setFixedHeight(28)
        rad_layout = QHBoxLayout()
        rad_layout.setContentsMargins(0, 0, 0, 0)
        rad_layout.setSpacing(4)
        rad_minus = QPushButton("-")
        rad_minus.setFixedWidth(30)
        rad_minus.setFixedHeight(28)
        rad_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        rad_layout.addWidget(self.radius_increment)
        rad_layout.addWidget(rad_minus)
        rad_plus = QPushButton("+")
        rad_plus.setFixedWidth(30)
        rad_plus.setFixedHeight(28)
        rad_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        rad_layout.addWidget(rad_plus)
        sim_layout.addRow("Radius Increment:", rad_layout)
        rad_plus.clicked.connect(lambda: self.radius_increment.stepUp())
        rad_minus.clicked.connect(lambda: self.radius_increment.stepDown())

        # Solver tolerance with [− value +]
        self.solver_tolerance = NoWheelSpinBox()
        self.solver_tolerance.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.solver_tolerance.setDecimals(5)
        self.solver_tolerance.setRange(0.00001, 0.01)
        self.solver_tolerance.setSingleStep(0.00005)
        self.solver_tolerance.setValue(0.0001)
        self.solver_tolerance.setSuffix(" mm")
        self.solver_tolerance.setToolTip("Tolerance used by Volco's solver when merging voxels")
        self.solver_tolerance.setFixedHeight(28)
        tol_layout = QHBoxLayout()
        tol_layout.setContentsMargins(0, 0, 0, 0)
        tol_layout.setSpacing(4)
        tol_minus = QPushButton("-")
        tol_minus.setFixedWidth(30)
        tol_minus.setFixedHeight(28)
        tol_minus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 6px;")
        tol_layout.addWidget(self.solver_tolerance)
        tol_layout.addWidget(tol_minus)
        tol_plus = QPushButton("+")
        tol_plus.setFixedWidth(30)
        tol_plus.setFixedHeight(28)
        tol_plus.setStyleSheet("background-color: #2d2d2d; color: #f0f0f0; font-size: 14px; border: 1px solid #3a3a3a; border-radius: 4px; padding: 2px; margin-left: 4px;")
        tol_layout.addWidget(tol_plus)
        sim_layout.addRow("Solver Tolerance:", tol_layout)
        tol_plus.clicked.connect(lambda: self.solver_tolerance.stepUp())
        tol_minus.clicked.connect(lambda: self.solver_tolerance.stepDown())
        
        # STL output mode
        self.stl_ascii = QCheckBox("ASCII STL (larger files)")
        self.stl_ascii.setChecked(False)
        self.stl_ascii.setToolTip("Enable to generate human-readable STL output instead of binary")
        sim_layout.addRow("STL Format:", self.stl_ascii)

        # Preview mode (fast, lightweight visualization)
        self.preview_mode = QCheckBox("Preview Mode (fast)")
        self.preview_mode.setChecked(False)
        self.preview_mode.setToolTip(
            "Run a fast preview that traces the G-code path and fills extrusions without physics or overlap checks"
        )
        sim_layout.addRow("Preview Mode:", self.preview_mode)
        
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
            'preview_mode': self.preview_mode.isChecked(),
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
        if 'preview_mode' in params:
            self.preview_mode.setChecked(bool(params['preview_mode']))

    def _toggle_advanced(self, expanded: bool):
        """Show or hide advanced settings container."""
        self.advanced_container.setVisible(expanded)
        arrow = Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow
        self.advanced_toggle.setArrowType(arrow)
