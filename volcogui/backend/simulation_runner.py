"""Simulation runner for Volco."""

import sys
import shutil
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
            
            # Import Volco (add parent directory to path if needed)
            try:
                # Try to find Volco in a sibling directory
                volco_paths = [
                    Path(__file__).parent.parent.parent.parent / "volco",  # Sibling to volcogui
                    Path.home() / "projects" / "gcode" / "volco",  # Common location
                ]
                
                volco_found = False
                for volco_path in volco_paths:
                    if volco_path.exists() and (volco_path / "volco.py").exists():
                        sys.path.insert(0, str(volco_path))
                        volco_found = True
                        break
                
                if not volco_found:
                    # Fall back to test mode
                    self.progress.emit("Volco not found - running in TEST MODE...")
                    import time
                    time.sleep(2)
                    temp_dir = tempfile.gettempdir()
                    self.output_stl = str(Path(temp_dir) / "volco_output.stl")
                    self._create_test_stl(self.output_stl)
                    self.progress.emit("Test simulation complete!")
                    self.finished.emit(self.output_stl)
                    return
                
                # Import Volco
                from volco import run_simulation
                
                self.progress.emit("Parsing G-code...")
                
                # Create a temporary output file
                temp_dir = tempfile.gettempdir()
                self.output_stl = str(Path(temp_dir) / "volco_output.stl")
                
                self.progress.emit("Running voxel simulation...")
                
                # Create temp directory for results
                temp_dir = tempfile.gettempdir()
                results_folder = str(Path(temp_dir) / "volcogui_results")
                
                # Run Volco simulation
                output = run_simulation(
                    gcode_path=self.gcode_path,
                    printer_config={
                        'nozzle_diameter': self.params['nozzle_diameter'],
                        'feedstock_filament_diameter': 1.75,
                        'nozzle_jerk_speed': 10.0,
                        'extruder_jerk_speed': 5.0,
                        'nozzle_acceleration': 1000.0,
                        'extruder_acceleration': 5000.0,
                    },
                    sim_config={
                        'simulation_name': 'volcogui_simulation',
                        'results_folder': results_folder,
                        'voxel_size': self.params['voxel_size'],
                        'step_size': self.params['step_size'],
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
                
                self.progress.emit("Generating mesh...")
                
                # Export STL (Volco creates the file in results_folder/simulation_name.stl)
                output.export_mesh_to_stl()
                
                # Get the actual STL path that Volco created
                actual_stl_path = Path(results_folder) / "volcogui_simulation.stl"
                
                # Copy to our output location for consistency
                if actual_stl_path.exists():
                    shutil.copy(str(actual_stl_path), self.output_stl)
                else:
                    raise FileNotFoundError(f"STL file not found at {actual_stl_path}")
                
                self.progress.emit("Simulation complete!")
                self.finished.emit(self.output_stl)
                
            except ImportError as e:
                self.error.emit(f"Volco import failed: {str(e)}\n\nMake sure Volco is in the correct location.")
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
