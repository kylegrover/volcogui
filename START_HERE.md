# 🎯 START HERE - VolcoGUI

**A complete cross-platform desktop application for Volco 3D print simulation**

## ⚡ Quick Start (3 Commands)

```bash
cd volcogui
uv sync
uv run python -m volcogui.main
```

**Or use the automated first-run script:**
- **Windows:** Double-click `first_run.bat`
- **Linux/Mac:** `./first_run.sh`

## 📚 Documentation Index

Choose your path based on what you need:

### 🚀 I want to get started quickly
→ **Read:** [QUICKSTART.md](QUICKSTART.md)
- Essential commands
- 5-minute setup
- Quick workflow guide

### 📖 I want complete setup instructions
→ **Read:** [INSTALLATION.md](INSTALLATION.md)
- Step-by-step installation
- Platform-specific guides
- Comprehensive troubleshooting
- Success checklist

### 🎨 I want to understand the interface
→ **Read:** [UI_GUIDE.md](UI_GUIDE.md)
- Visual layout guide
- UI states and interactions
- Color scheme and styling
- Mouse controls

### 🔧 I want to modify or extend the app
→ **Read:** [DEVELOPMENT.md](DEVELOPMENT.md)
- Architecture overview
- How to add parameters
- Code patterns
- Extension guide

### 📋 I want to see what was built
→ **Read:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- Complete feature list
- Technology stack
- Project structure
- Status and achievements

### 📘 I want full documentation
→ **Read:** [README.md](README.md)
- Feature overview
- Usage guide
- Configuration options
- Troubleshooting

### 🔬 I want to understand Volco
→ **Read:** [volco_llm_ref.md](volco_llm_ref.md)
- Volco API reference
- Configuration parameters
- Architecture details

## 🎯 What This App Does

VolcoGUI is a desktop application that:

1. **Imports** G-code files (drag-drop or browse)
2. **Configures** simulation parameters (voxel size, step size, nozzle diameter)
3. **Runs** Volco 3D print simulation in the background
4. **Displays** the output STL in an interactive 3D viewer

## ✨ Key Features

- 🖱️ **Drag & Drop** G-code import
- ⚙️ **Easy Configuration** with 3 main parameters
- 🔄 **Background Processing** with progress updates
- 👁️ **Interactive 3D Viewer** with rotate, pan, zoom
- 🎨 **Professional UI** built with PyQt6
- 🖥️ **Cross-Platform** (Windows, macOS, Linux)
- 🧪 **Test Mode** works without Volco installed

## 📦 What's Included

```
volcogui/
├── volcogui/              # Application source code
│   ├── main.py            # Entry point
│   ├── ui/                # UI components
│   └── backend/           # Simulation logic
├── examples/              # Example G-code files
├── first_run.bat/sh       # Automated setup scripts
├── run.bat/sh             # Quick launch scripts
└── [Multiple .md docs]    # Comprehensive documentation
```

## 🚦 Installation Status Check

Run these commands to verify your setup:

```bash
# Check uv is installed
uv --version

# Install dependencies (from volcogui directory)
uv sync

# Verify key packages
uv pip list | grep -E "(PyQt6|pyvista)"

# Check if Volco is available (optional for testing)
uv pip show volco
```

## 🎮 Three Ways to Run

### Method 1: Automated Script (Recommended for first time)
```bash
# Windows
first_run.bat

# Linux/Mac
./first_run.sh
```

### Method 2: Quick Launch Scripts
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### Method 3: Direct Python
```bash
uv run python -m volcogui.main
```

## 🧪 Testing Without Volco

The app includes **test mode** - works without Volco installed!

1. Launch app (any method above)
2. Import: `examples/test_cube.gcode`
3. Click: "Run Simulation"
4. Result: Test cube appears in 3D viewer

This lets you test the interface before integrating Volco.

## 📋 Requirements

- **Python:** 3.9+ (managed by uv)
- **uv:** Package manager ([install guide](https://github.com/astral-sh/uv))
- **Volco:** Optional for testing, required for real simulations

## 🎯 Typical Workflow

```
1. Launch app          → uv run python -m volcogui.main
2. Import G-code       → Drag file or click "Browse Files..."
3. Set parameters      → Adjust voxel size, step size, nozzle diameter
4. Run simulation      → Click green "Run Simulation" button
5. View result         → Interact with 3D model (rotate, pan, zoom)
```

## 🐛 Common Issues

### "uv: command not found"
**Fix:** Install uv, then restart terminal
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "Volco not found"
**Not an error!** App runs in test mode. To install Volco:
```bash
uv pip install -e /path/to/volco
```

### "PyVista not available"
**Fix:** Reinstall dependencies
```bash
uv sync --reinstall
```

See [INSTALLATION.md](INSTALLATION.md) for complete troubleshooting.

## 🎨 Current Parameters

The app currently exposes 3 key Volco parameters:

- **Voxel Size** (0.001-10mm): Resolution of simulation grid
- **Step Size** (0.001-10mm): Distance between simulation steps  
- **Nozzle Diameter** (0.1-5mm): Printer nozzle size

**Want more parameters?** See [DEVELOPMENT.md](DEVELOPMENT.md) for easy extension guide.

## 🔗 Quick Links

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | Fast reference | 2 min |
| [INSTALLATION.md](INSTALLATION.md) | Setup guide | 10 min |
| [UI_GUIDE.md](UI_GUIDE.md) | Interface tour | 5 min |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Dev guide | 15 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | What was built | 5 min |
| [README.md](README.md) | Full documentation | 20 min |

## 🎉 Ready to Go!

Your VolcoGUI is **100% complete and ready to use**.

**First time setup (3 commands):**
```bash
cd volcogui
uv sync
uv run python -m volcogui.main
```

**Or double-click:**
- Windows: `first_run.bat`
- Mac/Linux: `first_run.sh`

Enjoy your new 3D print simulation GUI! 🚀

---

**Questions?** Check the documentation links above, especially:
- Setup issues → [INSTALLATION.md](INSTALLATION.md)
- Usage questions → [README.md](README.md)
- Want to customize → [DEVELOPMENT.md](DEVELOPMENT.md)
