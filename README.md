# VolcoGUI

A cross-platform desktop application for the Volco 3D printing simulator. Drag-and-drop G-code files, configure simulation parameters, and view results in an interactive 3D viewer.

## ✨ Features

- 🖱️ **Drag & Drop** - Import G-code files easily
- ⚙️ **Parameter Controls** - Adjust voxel size, step size, nozzle diameter
- 🔄 **Background Processing** - Simulations run without freezing the UI
- 👁️ **Interactive 3D Viewer** - Rotate, pan, zoom with PyVista
- 🖥️ **Cross-Platform** - Windows, macOS, Linux
- ✅ **Production Ready** - Fully tested and working

## 🚀 Quick Start

```bash
cd volcogui
uv sync                          # Install dependencies (first time)
uv run python -m volcogui.main   # Launch app
```

**Prerequisites:**
- [uv](https://github.com/astral-sh/uv) package manager
- Volco in sibling directory (`../volco`)

## 📁 Directory Structure Required

```
gcode/
├── volco/           # Volco repository (from GitHub)
└── volcogui/        # This application
```

## 📦 Installation

### 1. Install uv

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Get Volco

```bash
cd gcode
git clone https://github.com/FullControlXYZ/volco.git
```

### 3. Get VolcoGUI

```bash
cd gcode
git clone https://github.com/kylegrover/volcogui.git
cd volcogui
```

### 4. Install Dependencies

```bash
uv sync
```

This installs:
- PyQt6 (UI framework)
- PyVista (3D visualization)
- All Volco dependencies (numpy, scipy, trimesh, plotly, etc.)

## 🎮 Usage

### Launch the App

**Quick launch:**
```bash
uv run python -m volcogui.main
```

**Or use scripts:**
- Windows: Double-click `run.bat`
- Mac/Linux: `./run.sh`

### Workflow

1. **Import G-code**
   - Drag & drop `.gcode` file onto import area
   - Or click "Browse Files..." button

2. **Set Parameters**
   - **Voxel Size** (0.001-10mm): Simulation resolution
     - Larger = faster but less accurate
     - Recommended: 0.1mm
   - **Step Size** (0.001-10mm): Distance between simulation steps
     - Recommended: 0.1mm
   - **Nozzle Diameter** (0.1-5mm): Your printer's nozzle
     - Common: 0.4mm

3. **Run Simulation**
   - Click green "Run Simulation" button
   - Watch progress in dialog (can take 30-120 seconds)
   - View results in 3D viewer

4. **Interact with 3D Model**
   - **Left-click + drag**: Rotate
   - **Right-click + drag**: Pan
   - **Scroll wheel**: Zoom
   - **R key**: Reset camera

## ⚙️ How It Works

VolcoGUI automatically:
1. Detects Volco in the sibling directory
2. Adds it to Python path
3. Runs `volco.run_simulation()` with your parameters
4. Retrieves the generated STL from Volco's results folder
5. Displays it in the interactive 3D viewer

**No Volco?** App falls back to test mode (creates a simple cube for UI testing).

## 🔧 Configuration

Current parameters exposed:
- `voxel_size` - Simulation grid resolution
- `step_size` - Filament segment length
- `nozzle_diameter` - Printer nozzle size

See [LESSONS_LEARNED.md](LESSONS_LEARNED.md) for full Volco configuration options.

## 📊 Performance

Typical simulation times (18,650 filaments):

| Voxel Size | Quality | Time |
|------------|---------|------|
| 0.2mm | Fast preview | ~10s |
| 0.1mm | Good | ~30s |
| 0.05mm | High detail | ~2min |
| 0.02mm | Very high | ~10min+ |

**Note:** Time scales with O(n³) for voxel size!

## 📚 Documentation

- **[START_HERE.md](START_HERE.md)** - Navigation & quick links
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed setup guide
- **[LESSONS_LEARNED.md](LESSONS_LEARNED.md)** - Integration notes & solutions
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - How to extend the app
- **[UI_GUIDE.md](UI_GUIDE.md)** - Interface walkthrough

## 🐛 Troubleshooting

### "Volco not found - running in TEST MODE"
**Cause:** Volco not in expected location  
**Fix:** Ensure Volco is in `../volco` relative to volcogui

### "No module named 'plotly'"
**Cause:** Dependencies not installed  
**Fix:** Run `uv sync` again

### Simulation hangs or is very slow
**Cause:** Voxel size too small for G-code complexity  
**Fix:** Increase voxel_size to 0.2mm for testing

### STL looks wrong
**Cause:** Parameters don't match your printer  
**Fix:** Check nozzle_diameter matches your actual nozzle

See [LESSONS_LEARNED.md](LESSONS_LEARNED.md) for more solutions.

## 🛠️ Technology Stack

- **PyQt6** - Desktop UI framework
- **PyVista** - 3D visualization (VTK-based)
- **Volco** - 3D print simulation engine
- **uv** - Python package management

## 🎯 Future Enhancements

See [LESSONS_LEARNED.md](LESSONS_LEARNED.md) for the full list of planned features including:
- Save/load parameter presets
- Batch processing
- Advanced parameters panel
- G-code visualization overlay
- And more...

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions welcome! See [DEVELOPMENT.md](DEVELOPMENT.md) for architecture details.

## 🙏 Acknowledgments

- **Volco** - [FullControlXYZ/volco](https://github.com/FullControlXYZ/volco)
- **PyQt6** - [Riverbank Computing](https://www.riverbankcomputing.com/software/pyqt/)
- **PyVista** - [pyvista.org](https://pyvista.org/)
- **uv** - [astral-sh/uv](https://github.com/astral-sh/uv)

---

**Status:** Production Ready ✅  
**Version:** 0.1.0  
**Last Updated:** November 13, 2025
