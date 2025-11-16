# VolcoGUI Installation & First Run

## ✨ What You're Building

A beautiful, cross-platform desktop application for Volco 3D print simulation with:
- Drag-and-drop G-code import
- Interactive 3D visualization
- Real-time progress updates
- Professional UI built with PyQt6

## 📋 Prerequisites

- **Windows 10/11** (or macOS/Linux)
- **Python 3.9+** (will be managed by uv)
- **uv** package manager (we'll install this first)

## 🚀 Installation Steps

### Step 1: Install uv Package Manager

**On Windows (PowerShell as Administrator):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**On macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, **restart your terminal** or run:
```bash
source $HOME/.cargo/env  # Linux/Mac
```

Verify installation:
```bash
uv --version
```

### Step 2: Navigate to Project Directory

```bash
cd c:\Users\kyle\projects\gcode\volcogui
```

### Step 3: Install Application Dependencies

This will create a virtual environment and install all required packages:

```bash
uv sync
```

This installs:
- PyQt6 (UI framework)
- PyVista + VTK (3D visualization)
- NumPy, SciPy, scikit-image (scientific computing)
- Trimesh (mesh operations)

**Expected time:** 2-3 minutes

### Step 4: Install Volco

#### Option A: Volco is in a sibling directory

If your directory structure is:
```
gcode/
└── volcogui/       # This application (with volco submodule)
```

Volco is included as a git submodule and should already be initialized if you cloned with `--recurse-submodules`.

If the `volco/` directory is empty, run:
```bash
cd volcogui
git submodule update --init --recursive
```

### Step 5: Verify Installation

```bash
uv pip list | grep -E "(PyQt6|pyvista|volco)"
```

You should see all packages listed.

## 🎮 Running the Application

### Quick Launch

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
./run.sh
```

### Alternative Launch Methods

**Method 1: Direct Python**
```bash
uv run python -m volcogui.main
```

**Method 2: Using entry point**
```bash
uv run volcogui
```

## 🧪 Testing Without Volco

The app includes a **test mode** that works without Volco installed. It generates a simple cube STL for testing the interface.

1. Launch the app (any method above)
2. Import the example file: `examples/test_cube.gcode`
3. Click "Run Simulation"
4. A test cube will appear in the 3D viewer

## 🎯 First Time Usage

### 1. Launch Application
```bash
uv run python -m volcogui.main
```

You should see a window with:
- Left panel: File import and parameters
- Right panel: 3D viewer (currently empty)

### 2. Import G-code File

**Option A: Drag & Drop**
- Drag a `.gcode` file onto the import area

**Option B: Browse**
- Click "Browse Files..." button
- Navigate to your G-code file
- Try: `examples/test_cube.gcode`

### 3. Configure Parameters

Default values are good for testing:
- **Voxel Size:** 0.1 mm
- **Step Size:** 0.1 mm  
- **Nozzle Diameter:** 0.4 mm

### 4. Run Simulation

- Click the green "Run Simulation" button
- Watch progress updates in the dialog
- Wait for completion (test cube: ~5 seconds)

### 5. Interact with 3D Model

Once complete, the STL appears in the viewer:
- **Left-click + drag:** Rotate
- **Right-click + drag:** Pan
- **Scroll wheel:** Zoom
- **R key:** Reset camera

## 🐛 Troubleshooting

### "uv: command not found"

**Solution:** Restart terminal after installing uv, or manually add to PATH:
```bash
# Add to ~/.bashrc or ~/.zshrc (Linux/Mac)
export PATH="$HOME/.cargo/bin:$PATH"
```

### "PyQt6 not found" or "pyvista not found"

**Solution:** Reinstall dependencies:
```bash
uv sync --reinstall
```

### "Volco not found" error

**Solution:** Make sure Volco is installed:
```bash
# Check if installed
uv pip list | grep volco

# If not, install it
uv pip install -e /path/to/volco
```

### Application window is blank or frozen

**Solution:** Check if PyVista/VTK installed correctly:
```bash
uv pip install --force-reinstall pyvista pyvistaqt vtk
```

### "Cannot import name 'run_simulation'" error

This is expected if Volco isn't installed yet. The app will run in **test mode** and create a simple cube for testing.

### VTK/OpenGL errors (Linux)

**Solution:** Install system OpenGL libraries:
```bash
# Ubuntu/Debian
sudo apt-get install libgl1-mesa-glx libglu1-mesa

# Fedora
sudo dnf install mesa-libGL mesa-libGLU
```

### Permission denied on run.sh

**Solution:** Make script executable:
```bash
chmod +x run.sh
```

## 📁 Project Structure

After installation, your directory should look like:

```
volcogui/
├── .venv/                  # Virtual environment (created by uv)
├── volcogui/               # Application source code
│   ├── backend/            # Simulation logic
│   ├── ui/                 # UI components
│   └── main.py             # Entry point
├── examples/               # Example G-code files
├── pyproject.toml          # Dependencies
├── run.bat / run.sh        # Launch scripts
└── README.md               # Full documentation
```

## 🔄 Updating Dependencies

If you need to update packages:

```bash
# Update all packages
uv sync --upgrade

# Update specific package
uv pip install --upgrade PyQt6
```

## 🎨 Next Steps

1. ✅ **Test with example file:** `examples/test_cube.gcode`
2. ✅ **Try your own G-code files**
3. ✅ **Experiment with parameters** (try smaller voxel sizes)
4. 📖 **Read DEVELOPMENT.md** to add more features
5. 🔧 **Modify parameters** to add more Volco options

## 📚 Additional Documentation

- **README.md** - Full feature documentation
- **QUICKSTART.md** - Condensed quick reference
- **DEVELOPMENT.md** - Developer guide for modifications
- **volco_llm_ref.md** - Complete Volco API reference

## 🤝 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all dependencies: `uv pip list`
3. Try test mode without Volco
4. Check terminal output for error messages
5. Ensure Volco works independently first

## ✅ Success Checklist

- [ ] uv installed and working (`uv --version`)
- [ ] Dependencies installed (`uv sync` completed)
- [ ] Application launches without errors
- [ ] Can import G-code files
- [ ] Test simulation works (creates cube)
- [ ] 3D viewer displays and is interactive
- [ ] Volco integration (if Volco installed)

---

**Ready to simulate!** 🎉

Run the application:
```bash
uv run python -m volcogui.main
```
