# VolcoGUI - Application Layout Guide

## Application Window Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│ VolcoGUI - 3D Print Simulator                                    [─][□][×]│
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────┐  │  ┌──────────────────────────────────────┐  │
│  │                      │  │  │                                       │  │
│  │  Volco 3D Print      │  │  │                                       │  │
│  │     Simulator        │  │  │          3D Viewer                    │  │
│  │                      │  │  │                                       │  │
│  ├──────────────────────┤  │  │      "3D Viewer"                     │  │
│  │  ┌─ G-code File ──┐  │  │  │                                       │  │
│  │  │                 │  │  │  │   "Run simulation to                 │  │
│  │  │  Drop .gcode    │  │  │  │      view results"                   │  │
│  │  │   file here     │  │  │  │                                       │  │
│  │  │                 │  │  │  │                                       │  │
│  │  │                 │  │  │  │  [Interactive 3D STL Viewer]         │  │
│  │  └─────────────────┘  │  │  │                                       │  │
│  │  📄 No file selected  │  │  │  • Left-click + drag = Rotate        │  │
│  │                        │  │  │  • Right-click + drag = Pan          │  │
│  │  [Browse Files...]    │  │  │  • Scroll = Zoom                     │  │
│  ├──────────────────────┤  │  │                                       │  │
│  │ ┌─ Simulation     ─┐ │  │  │                                       │  │
│  │ │ Parameters       │ │  │  │                                       │  │
│  │ │                  │ │  │  │                                       │  │
│  │ │ Voxel Size:      │ │  │  │                                       │  │
│  │ │ [0.100] mm       │ │  │  │                                       │  │
│  │ │                  │ │  │  │                                       │  │
│  │ │ Step Size:       │ │  │  │                                       │  │
│  │ │ [0.100] mm       │ │  │  │                                       │  │
│  │ │                  │ │  │  │                                       │  │
│  │ │ Nozzle Diameter: │ │  │  │                                       │  │
│  │ │ [0.40] mm        │ │  │  │                                       │  │
│  │ └──────────────────┘ │  │  │                                       │  │
│  │                        │  │  │                                       │  │
│  │  ┌──────────────────┐ │  │  │                                       │  │
│  │  │  Run Simulation  │ │  │  │                                       │  │
│  │  └──────────────────┘ │  │  │                                       │  │
│  │                        │  │  │                                       │  │
│  │                        │  │  └───────────────────────────────────────┘  │
│  │         (space)        │  │                                            │
│  │                        │  │                                            │
│  │  ℹ️ Drag & drop a      │  │                                            │
│  │  .gcode file or use    │  │                                            │
│  │  the import button     │  │                                            │
│  └────────────────────────┘  │                                            │
│                                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│ Status: Ready - Import a G-code file to begin                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## UI States

### State 1: Initial State (No File)
- Drop zone: Gray dashed border
- File label: "No file selected"
- Run button: **Disabled** (grayed out)
- Viewer: Placeholder text
- Status: "Ready - Import a G-code file to begin"

### State 2: File Imported
- Drop zone: **Green solid border** with ✓
- File label: "📄 filename.gcode"
- Run button: **Enabled** (green)
- Viewer: Still placeholder
- Status: "Loaded: /path/to/file.gcode"

### State 3: Simulation Running
- Drop zone: Disabled
- Parameters: Disabled
- Run button: Disabled
- **Progress Dialog appears:**
  ```
  ┌─────────────────────────────┐
  │ Running Simulation          │
  ├─────────────────────────────┤
  │ Parsing G-code...           │
  │                             │
  │ [════════════░░░░] 60%      │
  │                             │
  │         [Cancel]            │
  └─────────────────────────────┘
  ```
- Status: Updates with progress messages

### State 4: Simulation Complete
- All controls: Re-enabled
- Viewer: **Displays 3D STL model**
- Status: "Simulation complete! Output: /path/to/output.stl"

### State 5: Error Occurred
- All controls: Re-enabled
- Viewer: Unchanged
- **Error Dialog appears:**
  ```
  ┌─────────────────────────────┐
  │ ⚠️ Simulation Error          │
  ├─────────────────────────────┤
  │ Error message details here  │
  │                             │
  │            [OK]             │
  └─────────────────────────────┘
  ```

## Color Scheme

### Primary Colors
- **Background:** White (#FFFFFF)
- **Panel Background:** Light gray (#F5F5F5)
- **Text:** Dark gray (#333333)
- **Border:** Medium gray (#AAAAAA)

### Interactive Elements
- **Run Button (Enabled):** Green (#4CAF50)
- **Run Button (Hover):** Dark green (#45a049)
- **Run Button (Disabled):** Light gray (#CCCCCC)

### File Import States
- **Normal:** Gray dashed border (#AAA)
- **Drag Over:** Green border (#4CAF50) + light green background (#E8F5E9)
- **File Loaded:** Solid green border + green background

### Status Indicators
- **Info:** Gray text (#666666)
- **Success:** Green (#2E7D32)
- **Error:** Red (#C62828)

## Drag & Drop Interaction

### Visual Feedback Sequence

1. **No file - Normal state:**
   ```
   ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
   │                       │
   │  Drop .gcode file     │
   │       here            │
   │                       │
   └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
   ```

2. **Dragging file over window:**
   ```
   ┌───────────────────────┐
   │   [Light green bg]    │
   │  Drop .gcode file     │
   │       here            │
   │                       │
   └───────────────────────┘
   ```

3. **File dropped - Success:**
   ```
   ┌═══════════════════════┐
   ║   [Green background]  ║
   ║  ✓ filename.gcode     ║
   ║                       ║
   └═══════════════════════┘
   ```

## 3D Viewer Interactions

### Mouse Controls
```
┌─────────────────────────────────┐
│                                  │
│         [3D Model Here]          │
│                                  │
│   🖱️  Mouse Controls:            │
│                                  │
│   • Left-click + drag            │
│     → Rotate model               │
│                                  │
│   • Right-click + drag           │
│     → Pan camera                 │
│                                  │
│   • Scroll wheel                 │
│     → Zoom in/out                │
│                                  │
│   • 'R' key                      │
│     → Reset camera               │
│                                  │
└─────────────────────────────────┘
```

### Viewer Features
- Isometric view by default
- Edge display (wireframe overlay)
- Coordinate axes (X, Y, Z)
- Auto-fit model to view
- Professional lighting
- Anti-aliasing

## Parameter Controls

### Spin Box Appearance
```
┌─ Simulation Parameters ─────┐
│                              │
│ Voxel Size:                  │
│ ┌──────────┐                │
│ │ 0.100 ▼  │ mm             │
│ └──────────┘                │
│ [Smaller = higher accuracy] │
│                              │
│ Step Size:                   │
│ ┌──────────┐                │
│ │ 0.100 ▼  │ mm             │
│ └──────────┘                │
│                              │
│ Nozzle Diameter:             │
│ ┌──────────┐                │
│ │ 0.40  ▼  │ mm             │
│ └──────────┘                │
│                              │
└──────────────────────────────┘
```

### Interaction
- Click number to type directly
- Use up/down arrows to increment/decrement
- Scroll wheel over field to adjust
- Tooltips appear on hover

## Window Sizing

### Minimum Size
- **Width:** 1200px
- **Height:** 800px

### Recommended Size
- **Width:** 1400-1600px
- **Height:** 900-1000px

### Panel Proportions
- **Left Panel:** 400px fixed width
- **Right Panel:** Remaining space (resizable)
- **Splitter:** Draggable divider between panels

## Responsive Behavior

### Small Window
```
┌─────────┬─────────────┐
│ Left    │   Right     │
│ 30%     │   70%       │
└─────────┴─────────────┘
```

### Large Window
```
┌────────┬──────────────────────┐
│  Left  │      Right           │
│  20%   │      80%             │
└────────┴──────────────────────┘
```

## Typography

### Font Sizes
- **Title:** 18px, bold
- **Section Headers:** 12px, bold
- **Body Text:** 11px, regular
- **Status Bar:** 11px, regular
- **Button Text:** 14px, bold
- **Help Text:** 11px, italic

### Font Family
- System default sans-serif
- Monospace for file paths

## Icons & Symbols

- ✓ File loaded successfully
- 📄 File indicator
- ℹ️ Information
- ⚠️ Warning/Error
- 🖱️ Mouse interaction hint
- 🔄 Processing/loading

## Accessibility

- **Keyboard Navigation:** Tab through controls
- **Enter Key:** Activates focused button
- **Escape Key:** Closes dialogs
- **Tooltips:** Hover help on all controls
- **Status Updates:** Screen reader compatible
- **High Contrast:** Compatible with system themes

---

This layout provides:
- ✅ Clear visual hierarchy
- ✅ Intuitive workflow (left to right)
- ✅ Immediate feedback on actions
- ✅ Professional appearance
- ✅ Efficient use of space
- ✅ Modern, clean design
