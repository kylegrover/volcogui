# VolcoGUI

A cross-platform graphical interface for the Volco 3D printing simulator. VolcoGUI provides an intuitive way to run Volco simulations with drag-and-drop G-code import, configurable parameters, and interactive 3D visualization of results.

## Features

- 🎯 **Drag & Drop Interface**: Simply drag your G-code files into the app
- ⚙️ **Configurable Parameters**: Adjust voxel size, step size, and nozzle diameter
- 🔄 **Background Processing**: Simulations run in the background with progress updates
- 👁️ **Interactive 3D Viewer**: View and interact with STL output using PyVista
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Volco (the 3D print simulator library)

## Installation

### 1. Install uv (if not already installed)

```bash
# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone/Download this repository

```bash
cd volcogui
```

### 3. Install dependencies

```bash
uv sync
```

This will create a virtual environment and install all required packages including PyQt6, PyVista, and other dependencies.

### 4. Install Volco

If Volco is available as a package:
```bash
uv pip install volco
```

Or if you have Volco locally, install it in editable mode:
```bash
uv pip install -e /path/to/volco
```

## Usage

### Running the Application

```bash
uv run python -m volcogui.main
```

Or use the shorthand:

```bash
uv run volcogui
```

### Using the Interface

1. **Import G-code File**
   - Drag and drop a `.gcode` file onto the import area
   - Or click "Browse Files..." to select a file

2. **Configure Parameters**
   - **Voxel Size**: Size of each voxel in mm (default: 0.1)
     - Smaller = higher accuracy but slower and more memory
   - **Step Size**: Distance between simulation steps in mm (default: 0.1)
     - Smaller = higher accuracy but slower
   - **Nozzle Diameter**: Diameter of your printer's nozzle in mm (default: 0.4)

3. **Run Simulation**
   - Click "Run Simulation"
   - Progress updates will appear in a dialog
   - Simulation runs in the background

4. **View Results**
   - The 3D viewer will automatically load the output STL
   - Use your mouse to interact:
     - **Left-click + drag**: Rotate
     - **Right-click + drag**: Pan
     - **Scroll wheel**: Zoom

## Project Structure

```
volcogui/
├── volcogui/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   ├── ui/                        # UI components
│   │   ├── __init__.py
│   │   ├── main_window.py         # Main application window
│   │   ├── file_import_widget.py  # G-code import widget
│   │   ├── parameter_widget.py    # Parameter controls
│   │   └── viewer_widget.py       # 3D STL viewer
│   └── backend/                   # Backend logic
│       ├── __init__.py
│       └── simulation_runner.py   # Volco simulation wrapper
├── pyproject.toml                 # Project dependencies
└── README.md                      # This file
```

## Development

### Installing in Development Mode

```bash
uv pip install -e .
```

### Running Tests

```bash
uv run pytest
```

### Adding Dependencies

```bash
uv add <package-name>
```

## Troubleshooting

### "PyVista not available" error

Make sure PyVista and pyvistaqt are installed:
```bash
uv pip install pyvista pyvistaqt
```

### "Volco not found" error

Ensure Volco is installed in your environment:
```bash
uv pip install volco
# or
uv pip install -e /path/to/volco
```

### Application won't start

Check that all dependencies are installed:
```bash
uv sync --reinstall
```

## Configuration

Default parameters can be modified in `volcogui/ui/parameter_widget.py`. 

For full Volco configuration options, refer to the [Volco documentation](volco_llm_ref.md).

## Advanced Usage

### Using Custom Volco Settings

The simulation runner (`volcogui/backend/simulation_runner.py`) can be modified to expose additional Volco parameters such as:
- Acceleration consideration
- Sphere z-offset
- Solver tolerance
- Cropping boundaries
- And more...

See `volco_llm_ref.md` for complete parameter documentation.

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- 3D visualization powered by [PyVista](https://pyvista.org/)
- Manages packages with [uv](https://github.com/astral-sh/uv)
- Simulations powered by [Volco](https://github.com/yourusername/volco)
