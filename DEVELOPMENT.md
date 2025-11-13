# Development Notes - VolcoGUI

## Architecture Overview

VolcoGUI is built using PyQt6 with a clear separation between UI and backend logic:

```
UI Layer (PyQt6)
    ↓
Backend Layer (Simulation Runner)
    ↓
Volco Library (3D Print Simulation)
```

## Key Components

### 1. Main Window (`ui/main_window.py`)
- Orchestrates the entire UI
- Manages application state (file path, parameters, output)
- Coordinates between widgets
- Handles simulation workflow

### 2. File Import Widget (`ui/file_import_widget.py`)
- Drag & drop functionality
- File dialog integration
- Visual feedback for file selection
- Emits `file_selected` signal with filepath

### 3. Parameter Widget (`ui/parameter_widget.py`)
- Input controls for simulation parameters
- Currently supports: voxel_size, step_size, nozzle_diameter
- Uses QDoubleSpinBox for validated numeric input
- `get_parameters()` returns dict of current values

### 4. Viewer Widget (`ui/viewer_widget.py`)
- PyVista-based 3D STL viewer
- Interactive controls (rotate, pan, zoom)
- `load_stl(path)` method to display models
- Falls back gracefully if PyVista unavailable

### 5. Simulation Runner (`backend/simulation_runner.py`)
- QThread-based worker for background execution
- Signals: `progress`, `finished`, `error`
- Currently includes test mode (creates cube STL)
- Ready for Volco integration

## Adding More Parameters

To expose additional Volco parameters:

### 1. Update `ParameterWidget`
```python
# In ui/parameter_widget.py
self.new_param = QDoubleSpinBox()
self.new_param.setValue(default_value)
layout.addRow("New Parameter:", self.new_param)

# In get_parameters()
return {
    # existing params...
    'new_param': self.new_param.value()
}
```

### 2. Update `SimulationRunner`
```python
# In backend/simulation_runner.py
# Add to sim_config or printer_config dict
sim_config={
    # existing config...
    'new_param': self.params['new_param']
}
```

## Integrating Real Volco

Replace the test simulation in `backend/simulation_runner.py`:

```python
def run(self):
    try:
        from volco import run_simulation
        
        self.progress.emit("Running simulation...")
        
        # Create temp output path
        import tempfile
        from pathlib import Path
        temp_dir = tempfile.gettempdir()
        self.output_stl = str(Path(temp_dir) / "volco_output.stl")
        
        # Run Volco
        output = run_simulation(
            gcode_path=self.gcode_path,
            printer_config={
                'nozzle_diameter': self.params['nozzle_diameter'],
                'feedstock_filament_diameter': 1.75,
                # ... other printer params
            },
            sim_config={
                'voxel_size': self.params['voxel_size'],
                'step_size': self.params['step_size'],
                # ... other sim params
            }
        )
        
        # Export STL
        output.export_mesh_to_stl(self.output_stl)
        
        self.finished.emit(self.output_stl)
        
    except Exception as e:
        self.error.emit(str(e))
```

## Threading and Signals

The app uses Qt's threading model:
- **Main Thread**: UI updates, user interaction
- **Worker Thread**: Volco simulation (CPU-intensive)
- **Signals**: Communication between threads (thread-safe)

Never update UI directly from worker thread - always use signals.

## Error Handling

Three levels of error handling:
1. **Input Validation**: QDoubleSpinBox ranges prevent invalid input
2. **Import Errors**: Graceful fallback if Volco/PyVista missing
3. **Runtime Errors**: Try-catch in worker with error signal to UI

## Future Enhancements

### Easy Additions
- [ ] Save/load parameter presets
- [ ] Recent files list
- [ ] Export STL with custom filename
- [ ] View statistics (vertices, faces, volume)
- [ ] Progress bar percentage (requires Volco callback)

### Medium Complexity
- [ ] Advanced parameter panel (expandable section)
- [ ] Multiple visualization modes (wireframe, solid, transparent)
- [ ] Comparison view (multiple STLs side-by-side)
- [ ] Batch processing (multiple G-code files)

### Complex Features
- [ ] Real-time simulation preview
- [ ] G-code visualization overlay
- [ ] Custom material properties
- [ ] Plugin system for post-processing

## Building Standalone Executable

### Using PyInstaller
```bash
uv pip install pyinstaller
pyinstaller --onefile --windowed --name VolcoGUI volcogui/main.py
```

### Considerations
- Bundle Python interpreter
- Include all dependencies (PyQt6, PyVista, VTK)
- Test on clean system without Python
- Expect 200-300MB executable size

## Testing

Create tests in `tests/` directory:
```bash
tests/
├── test_file_import.py
├── test_parameters.py
└── test_simulation_runner.py
```

Run with:
```bash
uv run pytest
```

## Performance Notes

- **Voxel Size**: Biggest impact on memory (O(n³))
- **PyVista Rendering**: GPU-accelerated, generally fast
- **File I/O**: Temp directory for STL output
- **Thread Safety**: All Volco work in background thread

## Dependencies

Core:
- PyQt6: UI framework
- PyVista: 3D visualization
- VTK: 3D rendering engine (PyVista dependency)

Volco dependencies:
- NumPy: Arrays
- SciPy: Scientific computing
- scikit-image: Image processing (marching cubes)
- Trimesh: Mesh operations

## Code Style

Following PEP 8:
- 4 spaces for indentation
- docstrings for all classes/methods
- Type hints where beneficial
- Max line length: 100 chars

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes, test

# Commit
git add .
git commit -m "Add: description of feature"

# Push and create PR
git push origin feature/new-feature
```

## Resources

- [PyQt6 Documentation](https://doc.qt.io/qtforpython-6/)
- [PyVista Examples](https://docs.pyvista.org/examples/)
- [Volco Reference](volco_llm_ref.md)
- [uv Documentation](https://github.com/astral-sh/uv)
