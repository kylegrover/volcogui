# VolcoGUI work notes

## Current direction

Keep the existing PyQt6/PyVista workbench and the bundled Volco `dev` submodule. Make it dependable before integrating experimental Volco work. Do not change the sibling Volco physics checkout as part of GUI cleanup.

Steps 1–2 landed on `main` in `61452ed` and `3553f16`: Volco now runs in a subprocess with per-run results, cancellable execution, bounded output capture, G-code path validation, stage-aware progress, a Run Log, and separate viewer-error reporting. The focused tests passed; source and packaged simulation smoke tests were reported. Interactive desktop behavior has **not** yet been verified.

## Review findings / decisions needed

1. Cancellation and window close still call `cancel()`/`wait()` on the GUI thread. Check real responsiveness on a long run; if it freezes, move shutdown off the UI thread rather than redesigning the app.
2. Successful STL runs remain under unique directories in the system temp folder; failed/canceled runs are deleted. Decide whether to retain results intentionally (with a way to find/save them) or define cleanup. Do not silently delete the only copy of a user's result.
3. Success currently means a nonempty STL file, not necessarily valid geometry; the viewer reports geometry/read failures separately. Test the happy path with a real STL fixture.
4. Run Log is disabled if the child produced no output, even on error; an error popup may contain the entire retained output as well. Prefer a short error plus an always-available run summary/log.

## Lifecycle check status

Automated offscreen Qt checks (viewer stub) exercised a real bundled-Volco preview run using `examples/test_cube.gcode`, a simulated viewer failure after successful output, an engine exit with no output, a Cancel-button click during a slow child process, and closing during a slow child process. Success produced a nonempty STL, populated Run Log, loaded the stub viewer, and restored controls. Viewer failure preserved the STL and raised a separate warning. Empty-output failure raised an error but left Run Log disabled (known issue). Cancel and close stopped the worker and removed their run directories; cancel restored controls. No live child was left in these cases. A direct worker preview smoke test also succeeded. Earlier simple close check took ~0.003s. These checks do **not** establish responsiveness with the real VTK viewer or a busy Volco process. Packaged execution was not retested in this pass.

## Next checkpoints

- **Desktop lifecycle check:** with a real window, try a successful run, cancel during a long simulation, close the window during a run, inspect Run Log after success/error/cancel, and confirm viewer failure doesn't lose the STL. Watch for a frozen window, orphan child, prematurely completed progress, or lost results. Automated/offscreen tests do not establish orbit feel or desktop responsiveness.
- **Step 3 (small UI changes):** consolidate viewer render/mesh/actor handling, add fit/reset and standard camera views; only adjust orbit after trying it interactively. Parameter control and file-drop cleanup are secondary. Preserve layout.
- **Step 4 (verification/delivery):** add lifecycle/start-cancel/error tests and a real STL fixture, test source and packaged flows, remove the absolute machine-specific path in `VolcoGUI.spec`, and reconcile stale documentation (especially references to test mode and an in-process Volco worker). Keep bundled Volco's own test suite separate from GUI regressions.

Out of scope for now: engine/plugin management, physics/FEA UI, presets, comparison tools, and a GUI rewrite.
