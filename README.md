# VolcoGUI

Desktop GUI for [Volco](https://github.com/FullControlXYZ/volco), a 3D printing voxel simulator. Provides drag-and-drop G-code import, parameter configuration, and interactive 3D STL visualization.

## Download

**Latest Release:** [v0.1.0-alpha](https://github.com/kylegrover/volcogui/releases/tag/v0.1.0-alpha)

**Windows:** Download `VolcoGUI_v0.1.zip`, extract, and run `VolcoGUI.exe`. No installation required - Volco is bundled.

**Other platforms:** Build from source (see below).

## Features

- Drag-and-drop G-code file import
- Configurable simulation parameters (voxel size, step size, nozzle diameter)
- Background processing with progress tracking
- Interactive 3D STL viewer (PyVista/VTK)
- Bundled Volco engine (no separate install needed for releases)

## Quick Start (Development)

**Prerequisites:** [uv](https://github.com/astral-sh/uv) package manager, Volco in `../volco`

```bash
# Setup
git clone https://github.com/FullControlXYZ/volco.git
git clone https://github.com/kylegrover/volcogui.git
cd volcogui
uv sync

# Run
uv run python -m volcogui.main
```

Or use convenience scripts: `run.bat` (Windows) / `./run.sh` (Mac/Linux)

## Usage

1. Import G-code: Drag-and-drop `.gcode` file or use "Browse Files..."
2. Configure parameters:
   - **Voxel Size** (0.001-10mm): Simulation resolution (default 0.1mm)
   - **Step Size** (0.001-10mm): Filament discretization (default 0.1mm)  
   - **Nozzle Diameter** (0.1-5mm): Printer nozzle (default 0.4mm)
3. Click "Run Simulation" and wait for completion (30-120s typical)
4. View/interact with result in 3D viewer (left-click drag to rotate)

## Parameters

- **voxel_size**: Grid resolution. Smaller = more accurate but slower. Try 0.2mm for quick preview, 0.05mm for detail.
- **step_size**: Filament segment length. Must be small enough relative to filament length (see troubleshooting).
- **nozzle_diameter**: Match your printer's actual nozzle.

## Performance

Example (344 filaments, 0.1mm voxel): ~12s

Time complexity: O(n³) for voxel size, O(m) for filament count.

## Building Releases

See [BUILD.md](BUILD.md) for creating standalone executables with bundled Volco.

```bash
uv pip install pyinstaller
uv run python build.py
# Creates dist/VolcoGUI/ folder ready for distribution
```

## Troubleshooting

**"Volco not found"**: Ensure `../volco` exists (dev mode) or use bundled release.

**"Division by zero"**: `step_size` too large. Reduce to ≤0.1mm.

**Slow simulation**: Reduce `voxel_size` (0.2mm for preview, 0.05mm for quality).

**Missing dependencies**: Run `uv sync`

See [LESSONS_LEARNED.md](LESSONS_LEARNED.md) for more solutions.

## Documentation

- [START_HERE.md](START_HERE.md) - Project navigation
- [LESSONS_LEARNED.md](LESSONS_LEARNED.md) - Integration notes and known issues
- [DEVELOPMENT.md](DEVELOPMENT.md) - Architecture and extension guide
- [BUILD.md](BUILD.md) - Release build instructions

## Tech Stack

- **UI**: PyQt6
- **3D Rendering**: PyVista (VTK)
- **Simulation**: Volco
- **Package Manager**: uv

## Contributing

Pull requests welcome. See [DEVELOPMENT.md](DEVELOPMENT.md) for architecture details.

## Credits

- [Volco](https://github.com/FullControlXYZ/volco) - 3D print simulation engine
- [PyVista](https://pyvista.org/) - VTK visualization
- [uv](https://github.com/astral-sh/uv) - Python packaging
