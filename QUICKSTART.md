# Quick Start Guide - VolcoGUI

## First Time Setup

### Step 1: Install uv (if needed)
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Navigate to project directory
```bash
cd volcogui
```

### Step 3: Install dependencies
```bash
uv sync
```

### Step 4: Install Volco
You need to have Volco installed. Either:

**Option A: Install from source (if you have Volco locally)**
```bash
# Navigate to Volco directory and install
cd ../volco
uv pip install -e .
cd ../volcogui
```

**Option B: Install from package (if available)**
```bash
uv pip install volco
```

## Running the Application

### Method 1: Using the run script
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### Method 2: Using uv directly
```bash
uv run python -m volcogui.main
```

### Method 3: After installing package
```bash
uv run volcogui
```

## Testing Without Volco

The app includes a test mode that creates a simple cube STL for testing the interface without needing Volco installed. Simply run the app and try importing the example G-code file at `examples/test_cube.gcode`.

## Workflow

1. **Launch the app**
2. **Import G-code**: Drag & drop or click "Browse Files..."
3. **Adjust parameters** (optional):
   - Voxel Size: 0.1 mm (default)
   - Step Size: 0.1 mm (default)
   - Nozzle Diameter: 0.4 mm (default)
4. **Click "Run Simulation"**
5. **View the 3D result**:
   - Left-click + drag to rotate
   - Right-click + drag to pan
   - Scroll to zoom

## Troubleshooting

### Dependencies not found
```bash
uv sync --reinstall
```

### PyVista/Qt errors
```bash
uv pip install --force-reinstall pyvista pyvistaqt PyQt6
```

### Can't find Volco
Make sure Volco is installed in the same Python environment. Check with:
```bash
uv pip list | grep volco
```

## Next Steps

- Try the example G-code file in `examples/test_cube.gcode`
- Experiment with different parameter values
- Check the full README.md for more details
- Modify `volcogui/backend/simulation_runner.py` to expose more Volco parameters
