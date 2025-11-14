# Build Instructions for VolcoGUI

## Prerequisites

Ensure you have:
1. Volco installed in `../volco` relative to this project
2. PyInstaller: `uv pip install pyinstaller`

## Building with Bundled Volco

### Quick Build
```bash
uv run python build.py
```

This will:
- Bundle Volco inside the application
- Create a self-contained distribution in `dist/VolcoGUI/`
- No external dependencies needed for end users!

## Output

The build creates `dist/VolcoGUI/` folder containing:
- `VolcoGUI.exe` - The main executable
- `volco/` - Bundled Volco library
- All required DLLs and dependencies

## Distribution

### For GitHub Release

1. **Zip the entire folder**:
   ```bash
   cd dist
   Compress-Archive -Path VolcoGUI -DestinationPath VolcoGUI-v1.0-windows.zip
   ```

2. **Upload to GitHub**:
   - Go to Releases → Create new release
   - Upload `VolcoGUI-v1.0-windows.zip`
   - Add release notes

3. **User Instructions**:
   ```
   1. Download and extract VolcoGUI-v1.0-windows.zip
   2. Run VolcoGUI.exe
   3. Drag and drop your .gcode file
   4. Adjust parameters and click "Run Simulation"
   ```

## Size Information

Expected size: ~400-600MB due to:
- VTK/PyVista (3D visualization)
- PyQt6 (GUI framework)
- Volco and scientific libraries (numpy, scipy, trimesh, etc.)

This is normal for scientific visualization applications.

## Testing

After building:
1. Navigate to `dist/VolcoGUI/`
2. Run `VolcoGUI.exe`
3. Test with a sample gcode file
4. Verify simulation runs and STL viewer displays output

## Troubleshooting

### Build fails with "Volco not found"
- Ensure `../volco` directory exists relative to volcogui
- Check that `../volco/volco.py` exists

### Missing module errors during build
- Add to hidden imports in build.py: `--hidden-import=module_name`

### Runtime "DLL load failed"
- May need Visual C++ Redistributable (include in release notes)

### Application crashes on startup
- Run from terminal to see error messages
- Check all dependencies are bundled correctly
