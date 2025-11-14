# Lessons Learned - VolcoGUI Integration

## Volco Integration Notes

### Key Discoveries

1. **Volco is not a pip package** - It exists only on GitHub without `setup.py` or `pyproject.toml`
   - Solution: Add Volco directory to Python path dynamically at runtime
   - Location: Automatically detected in sibling directory (`../volco`)

2. **Required Volco Dependencies**
   - All dependencies from Volco's `requirements.txt` must be installed in volcogui
   - Critical additions: `plotly>=5.13.0`, `nbformat>=4.2.0`
   - Already had: `numpy`, `scipy`, `trimesh`, `scikit-image`

3. **Required Volco Configuration Fields**
   - `simulation_name` (string) - Name for the simulation
   - `results_folder` (string) - Where Volco saves output files
   - Both are mandatory, KeyError if missing

4. **STL Export Behavior**
   - `output.export_mesh_to_stl()` takes NO file path parameter
   - Volco automatically saves to: `{results_folder}/{simulation_name}.stl`
   - Our solution: Let Volco create the file, then copy to desired location

5. **PyVista Text Positioning**
   - `position='middle'` is NOT valid for `add_text()`
   - Use viewport coordinates instead: `position=(0.35, 0.5)` with `viewport=True`

## Implementation Details

### Volco Path Detection
```python
# Check these locations in order:
volco_paths = [
    Path(__file__).parent.parent.parent.parent / "volco",  # Sibling to volcogui
    Path.home() / "projects" / "gcode" / "volco",  # Common location
]
```

### Minimal Volco Configuration
```python
printer_config = {
    'nozzle_diameter': float,  # User-configurable
    'feedstock_filament_diameter': 1.75,  # Standard default
    'nozzle_jerk_speed': 10.0,
    'extruder_jerk_speed': 5.0,
    'nozzle_acceleration': 1000.0,
    'extruder_acceleration': 5000.0,
}

sim_config = {
    'simulation_name': str,  # REQUIRED
    'results_folder': str,  # REQUIRED
    'voxel_size': float,  # User-configurable
    'step_size': float,  # User-configurable
    'x_offset': float,  # 5 * nozzle_diameter
    'y_offset': float,  # 5 * nozzle_diameter
    'z_offset': float,  # 5 * nozzle_diameter
    'sphere_z_offset': float,  # 0.5 * nozzle_diameter
    'x_crop': ['all', 'all'],
    'y_crop': ['all', 'all'],
    'z_crop': ['all', 'all'],
    'radius_increment': 0.001,
    'solver_tolerance': 0.0001,
    'consider_acceleration': False,
    'stl_ascii': False,
}
```

## Project Structure Decisions

### Why PyQt6 over Tauri/Electron
- All Python - seamless integration with Volco
- No language barrier (no Rust/JS interop needed)
- Easier to bundle dependencies
- Native performance for 3D rendering

### Why PyVista for 3D Viewing
- VTK-based, industry standard
- Interactive by default (rotate, pan, zoom)
- Qt integration via pyvistaqt
- Handles large meshes well

### Directory Structure
```
volcogui/              # GUI application
volco/                 # Volco library (sibling directory)
```
This structure allows:
- Independent development
- Easy path detection
- No installation conflicts

## Common Issues & Solutions

### Issue: "No module named 'volco'"
**Cause:** Volco not in expected location or path not added
**Solution:** App automatically searches sibling directory, falls back to test mode

### Issue: "No module named 'plotly'"
**Cause:** Volco dependencies not installed in volcogui environment
**Solution:** Added to pyproject.toml dependencies

### Issue: Malformed STL output
**Cause:** Passing file path to `export_mesh_to_stl()` when it doesn't accept one
**Solution:** Let Volco save automatically, then copy from results folder

### Issue: PyVista text position error
**Cause:** Invalid position string 'middle'
**Solution:** Use viewport coordinates (0.35, 0.5) instead

### Issue: Division by zero during simulation
**Cause:** `step_size` is too large relative to filament segment lengths in G-code
**Why it happens:** Volco calculates `number_simulation_steps = round(filament_length / step_size)`. If this rounds to 0, then `step_size = filament_length / number_simulation_steps` causes division by zero
**Solution:** 
- Reduce `step_size` (try 0.05mm or 0.02mm instead of 0.1mm)
- Increase `voxel_size` slightly
- Check G-code for very short movements (retractions, etc.)

## Performance Notes

- **Voxel Size Impact:** Smaller = more accurate but exponentially slower (O(n³))
- **Typical Values:**
  - Fast preview: 0.2mm
  - Good quality: 0.1mm
  - High detail: 0.05mm
  - Very high: 0.02mm (slow!)

- **Simulation Time Examples** (18650 filaments):
  - 0.2mm voxel: ~10 seconds
  - 0.1mm voxel: ~30 seconds
  - 0.05mm voxel: ~2 minutes

## Best Practices

1. **Always test with example G-code first**
2. **Start with larger voxel sizes** (0.1-0.2mm) for quick iteration
3. **Use temp directories** for results to avoid clutter
4. **Copy STL files** to desired location rather than trying to specify in Volco
5. **Run simulations in background threads** to keep UI responsive
6. **Provide progress updates** - simulations can take time

## Future Enhancements Ideas

### Easy Additions
- [ ] Save/load parameter presets to JSON
- [ ] Export STL to user-chosen location
- [ ] Display simulation statistics (vertices, faces, volume, time)
- [ ] Recent files list with parameters
- [ ] Advanced parameters panel (collapsible)

### Medium Complexity
- [ ] Batch processing multiple G-code files
- [ ] Compare two simulations side-by-side
- [ ] G-code visualization overlay on 3D view
- [ ] Custom material properties input
- [ ] Parameter templates for common printers

### Advanced Features
- [ ] Real-time simulation progress visualization
- [ ] Integration with Volco FEA module
- [ ] Machine learning for parameter optimization
- [ ] Cloud/server-based simulation option
- [ ] Multi-material simulation support

## Dependencies Summary

### Core Dependencies (PyQt6 + 3D)
- PyQt6 >= 6.6.0 - UI framework
- pyvista >= 0.43.0 - 3D visualization
- pyvistaqt >= 0.11.0 - PyVista Qt integration

### Volco Dependencies
- numpy >= 1.24.0 - Arrays
- scipy >= 1.11.0 - Scientific computing
- trimesh >= 4.0.0 - Mesh operations
- scikit-image >= 0.22.0 - Marching cubes
- plotly >= 5.13.0 - Volco visualization (required)
- nbformat >= 4.2.0 - Jupyter support (required)

Total environment size: ~400MB

## Testing Strategy

1. **Test Mode** - Works without Volco, creates cube
2. **Example G-code** - Small test file (18650 filaments)
3. **Real G-code** - User's actual print files
4. **Parameter Validation** - UI enforces ranges
5. **Error Handling** - Graceful failures with user feedback

---

**Last Updated:** November 13, 2025
**Status:** Production Ready ✓
