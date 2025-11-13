"""Simulation runner for Volco."""

import tempfile
from pathlib import Path
from typing import Optional
from PyQt6.QtCore import QThread, pyqtSignal


class SimulationWorker(QThread):
    """Worker thread for running Volco simulations."""
    
    # Signals
    progress = pyqtSignal(str)  # Progress message
    finished = pyqtSignal(str)  # Output STL file path
    error = pyqtSignal(str)     # Error message
    
    def __init__(self, gcode_path: str, params: dict):
        super().__init__()
        self.gcode_path = gcode_path
        self.params = params
        self.output_stl = None
        
    def run(self):
        """Run the simulation in a background thread."""
        try:
            self.progress.emit("Initializing simulation...")
            
            # Import Volco (only import when needed)
            try:
                # TODO: Replace this with actual Volco import once installed
                # from volco import run_simulation
                
                # For now, we'll create a mock simulation
                import time
                time.sleep(1)  # Simulate some work
                
                self.progress.emit("Parsing G-code...")
                time.sleep(1)
                
                self.progress.emit("Running voxel simulation...")
                time.sleep(2)
                
                self.progress.emit("Generating mesh...")
                time.sleep(1)
                
                # Create a temporary output file
                temp_dir = tempfile.gettempdir()
                self.output_stl = str(Path(temp_dir) / "volco_output.stl")
                
                # TODO: Replace with actual Volco simulation
                """
                output = run_simulation(
                    gcode_path=self.gcode_path,
                    printer_config={
                        'nozzle_diameter': self.params['nozzle_diameter'],
                        # Add other printer params with defaults
                        'feedstock_filament_diameter': 1.75,
                        'nozzle_jerk_speed': 10.0,
                        'extruder_jerk_speed': 5.0,
                        'nozzle_acceleration': 1000.0,
                        'extruder_acceleration': 5000.0,
                    },
                    sim_config={
                        'voxel_size': self.params['voxel_size'],
                        'step_size': self.params['step_size'],
                        # Add other sim params with defaults
                        'x_offset': 5 * self.params['nozzle_diameter'],
                        'y_offset': 5 * self.params['nozzle_diameter'],
                        'z_offset': 5 * self.params['nozzle_diameter'],
                        'sphere_z_offset': 0.5 * self.params['nozzle_diameter'],
                        'x_crop': ['all', 'all'],
                        'y_crop': ['all', 'all'],
                        'z_crop': ['all', 'all'],
                        'radius_increment': 0.001,
                        'solver_tolerance': 0.0001,
                        'consider_acceleration': False,
                        'stl_ascii': False,
                    }
                )
                
                # Export STL
                output.export_mesh_to_stl(self.output_stl)
                """
                
                # For testing, create a simple cube STL
                self._create_test_stl(self.output_stl)
                
                self.progress.emit("Simulation complete!")
                self.finished.emit(self.output_stl)
                
            except ImportError as e:
                self.error.emit(f"Volco not found. Please install Volco first.\n\n{str(e)}")
                return
                
        except Exception as e:
            self.error.emit(f"Simulation failed: {str(e)}")
            
    def _create_test_stl(self, output_path: str):
        """Create a simple test STL file for testing purposes."""
        # Simple ASCII STL of a cube
        stl_content = """solid cube
  facet normal 0 0 1
    outer loop
      vertex 0 0 10
      vertex 10 0 10
      vertex 10 10 10
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0 0 10
      vertex 10 10 10
      vertex 0 10 10
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 0 0
      vertex 10 10 0
      vertex 10 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 0 0
      vertex 0 10 0
      vertex 10 10 0
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 10 0 0
      vertex 10 10 10
      vertex 10 0 10
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 10 0 0
      vertex 10 10 0
      vertex 10 10 10
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 0 10
      vertex 0 10 10
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 10 10
      vertex 0 10 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 10 0
      vertex 0 10 10
      vertex 10 10 10
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 10 0
      vertex 10 10 10
      vertex 10 10 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 10 0 10
      vertex 0 0 10
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 10 0 0
      vertex 10 0 10
    endloop
  endfacet
endsolid cube
"""
        with open(output_path, 'w') as f:
            f.write(stl_content)
