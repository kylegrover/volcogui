"""Simulation runner for Volco."""

import sys
import io
import re
import shutil
import tempfile
import threading
from pathlib import Path
from typing import Optional
from PyQt6.QtCore import QThread, pyqtSignal


class ProgressCapture(io.StringIO):
    """Custom StringIO that captures output and triggers callbacks."""
    
    def __init__(self, callback, original_stream=None):
        super().__init__()
        self.callback = callback
        self.buffer = ""
        self.original_stream = original_stream
        
    def write(self, text):
        super().write(text)
        self.buffer += text
        
        # Also write to original stream so we can see console output
        if self.original_stream:
            try:
                self.original_stream.write(text)
                self.original_stream.flush()
            except:
                pass
        
        # Trigger callback with new text
        if self.callback and text.strip():  # Only callback if there's actual content
            try:
                self.callback(text)
            except Exception as e:
                # Write errors to original stream if available
                if self.original_stream:
                    self.original_stream.write(f"[Callback Error: {e}]\n")
        return len(text)
    
    def flush(self):
        """Flush is called by logging handlers."""
        if self.original_stream:
            try:
                self.original_stream.flush()
            except:
                pass


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
        self.total_filaments = 0
        self.processed_filaments = 0
        self.last_progress_update = 0
        self.is_running = False
        self.simulation_start_time = 0
    
    def _handle_progress_output(self, text: str):
        """Handle progress updates from Volco stdout."""
        import re
        import time
        
        # Look for total filaments count
        filament_match = re.search(r'Number of printed filaments:\s*(\d+)', text)
        if filament_match:
            self.total_filaments = int(filament_match.group(1))
            self.processed_filaments = 0  # Reset counter
            self.progress.emit(f"Found {self.total_filaments} filaments to process")
            self.simulation_start_time = time.time()
        
        # Count "Depositing filament: step = 1/X" which indicates a NEW filament starting
        if self.total_filaments > 0:
            # Match "step = 1" which means starting a new filament
            step_one_match = re.search(r'Depositing filament:\s*step\s*=\s*1/', text)
            if step_one_match:
                self.processed_filaments += 1
                percentage = int((self.processed_filaments / self.total_filaments) * 100)
                # Emit every 5% to avoid UI spam
                if percentage % 5 == 0 or self.processed_filaments == self.total_filaments:
                    elapsed = int(time.time() - self.simulation_start_time) if hasattr(self, 'simulation_start_time') else 0
                    self.progress.emit(f"Voxelizing filament {self.processed_filaments}/{self.total_filaments} ({percentage}%) - {elapsed}s elapsed")
        
    def run(self):
        """Run the simulation in a background thread."""
        try:
            self.progress.emit("Initializing simulation...")
            
            # Import Volco (add parent directory to path if needed)
            try:
                # Try to find Volco in multiple locations
                volco_paths = [
                    # For PyInstaller bundled version
                    Path(sys._MEIPASS) / "volco" if hasattr(sys, '_MEIPASS') else None,
                    # Development: submodule in volcogui/volco
                    Path(__file__).parent.parent.parent / "volco",
                ]
                
                # Filter out None paths
                volco_paths = [p for p in volco_paths if p is not None]
                
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
                
                # Import volco first to let it configure logging normally
                import logging
                from volco import run_simulation
                
                # NOW reconfigure logging to capture output AFTER volco has imported everything
                # Capture both stdout and stderr with progress tracking
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                captured_output = ProgressCapture(self._handle_progress_output, old_stderr)
                sys.stdout = captured_output
                sys.stderr = captured_output
                
                # Reconfigure ALL existing loggers to use our handler
                root_logger = logging.getLogger()
                
                # Remove all existing handlers
                for handler in root_logger.handlers[:]:
                    root_logger.removeHandler(handler)
                
                # Add our custom handler that writes to captured_output
                new_handler = logging.StreamHandler(captured_output)
                new_handler.setFormatter(logging.Formatter("%(levelname)s %(asctime)s %(message)s"))
                new_handler.setLevel(logging.INFO)
                root_logger.addHandler(new_handler)
                root_logger.setLevel(logging.INFO)
                
                # CRITICAL: Force all child loggers to use parent handlers
                # This ensures volco's module loggers (like voxel_space) use our handler
                for logger_name in logging.root.manager.loggerDict:
                    logger_obj = logging.getLogger(logger_name)
                    logger_obj.handlers = []
                    logger_obj.propagate = True  # Ensure it uses root logger's handlers
                
                self.progress.emit("Parsing G-code...")
                
                # Create a temporary output file
                temp_dir = tempfile.gettempdir()
                self.output_stl = str(Path(temp_dir) / "volco_output.stl")
                
                # Create temp directory for results
                results_folder = str(Path(temp_dir) / "volcogui_results")
                
                try:
                    import time
                    self.progress.emit("Running voxel simulation...")
                    self.is_running = True
                    self.simulation_start_time = time.time()
                    
                    # Start a thread to emit heartbeat updates every 2 seconds
                    import threading
                    def heartbeat():
                        while self.is_running:
                            time.sleep(2)
                            if self.is_running:
                                elapsed = int(time.time() - self.simulation_start_time)
                                self.progress.emit(f"Voxelizing {self.total_filaments} filaments... {elapsed}s elapsed")
                    
                    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
                    heartbeat_thread.start()
                    
                    # Run Volco simulation
                    printer_config = {
                      'nozzle_diameter': self.params['nozzle_diameter'],
                      'feedstock_filament_diameter': self.params.get('feedstock_filament_diameter', 1.75),
                      'nozzle_jerk_speed': self.params.get('nozzle_jerk_speed', 10.0),
                      'extruder_jerk_speed': self.params.get('extruder_jerk_speed', 5.0),
                      'nozzle_acceleration': self.params.get('nozzle_acceleration', 1000.0),
                      'extruder_acceleration': self.params.get('extruder_acceleration', 5000.0),
                    }

                    sim_config = {
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
                      'radius_increment': self.params.get('radius_increment', 0.001),
                      'solver_tolerance': self.params.get('solver_tolerance', 0.0001),
                      'consider_acceleration': self.params.get('consider_acceleration', False),
                      'stl_ascii': self.params.get('stl_ascii', False),
                    }

                    output = run_simulation(
                      gcode_path=self.gcode_path,
                      printer_config=printer_config,
                      sim_config=sim_config
                    )
                
                    self.is_running = False
                    self.progress.emit("Generating mesh...")
                    
                    # Export STL (Volco creates the file in results_folder/simulation_name.stl)
                    output.export_mesh_to_stl()
                    
                finally:
                    self.is_running = False
                    # Restore stdout and stderr
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                    output_text = captured_output.getvalue()
                    
                    # Extract progress info for debugging
                    if "Number of printed filaments:" in output_text:
                        match = re.search(r'Number of printed filaments: (\d+)', output_text)
                        if match:
                            total_filaments = match.group(1)
                            self.progress.emit(f"Processed {total_filaments} filaments")
                
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
                
        except ZeroDivisionError as e:
            self.error.emit(
                f"Division by zero error in simulation.\n\n"
                f"This usually happens when:\n"
                f"• Step size is larger than filament segments\n"
                f"• G-code contains very short movements\n\n"
                f"Try:\n"
                f"• Reducing step_size (current: {self.params['step_size']}mm)\n"
                f"• Increasing voxel_size\n\n"
                f"Technical details: {str(e)}"
            )
        except Exception as e:
            error_msg = str(e)
            # Make division by zero errors more user-friendly
            if "division by zero" in error_msg.lower() or "divide by zero" in error_msg.lower():
                self.error.emit(
                    f"Division by zero error in simulation.\n\n"
                    f"Current parameters:\n"
                    f"• Step size: {self.params['step_size']}mm\n"
                    f"• Voxel size: {self.params['voxel_size']}mm\n"
                    f"• Nozzle diameter: {self.params['nozzle_diameter']}mm\n\n"
                    f"Try reducing the step_size or check your G-code for very short movements.\n\n"
                    f"Error: {error_msg}"
                )
            else:
                self.error.emit(f"Simulation failed: {error_msg}")
            
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
