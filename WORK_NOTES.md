# VolcoGUI work notes

## Current direction

Keep the existing PyQt6/PyVista workbench and the bundled Volco `dev` submodule. Make it dependable before integrating experimental Volco work. Do not change the sibling Volco physics checkout as part of GUI cleanup.

Steps 1–2 landed on `main` in `61452ed` and `3553f16`: Volco now runs in a subprocess with per-run results, cancellable execution, bounded output capture, G-code path validation, stage-aware progress, a Run Log, and separate viewer-error reporting. Focused tests passed; source and packaged simulation smoke tests were reported. A limited real-desktop lifecycle check is recorded below; packaged execution and orbit changes have not been retested since.

## Review findings / decisions needed

1. Cancellation and window close still call `cancel()`/`wait()` on the GUI thread. Check real responsiveness on a long run; if it freezes, move shutdown off the UI thread rather than redesigning the app.
2. Successful STL runs remain under unique directories in the system temp folder; failed/canceled runs are deleted. Decide whether to retain results intentionally (with a way to find/save them) or define cleanup. Do not silently delete the only copy of a user's result.
3. Success currently means a nonempty STL file, not necessarily valid geometry; the viewer reports geometry/read failures separately. Test the happy path with a real STL fixture.
4. Run Log is now available after an engine error with no child output (pre-step-3 fix); an error popup may still contain the entire retained output. Consider shortening the popup later.

## Lifecycle check status

Automated offscreen Qt checks (viewer stub) exercised a real bundled-Volco preview run using `examples/test_cube.gcode`, a simulated viewer failure after successful output, an engine exit with no output, a Cancel-button click during a slow child process, and closing during a slow child process. Success produced a nonempty STL, populated Run Log, loaded the stub viewer, and restored controls. Viewer failure preserved the STL and raised a separate warning. Empty-output failure raised an error but left Run Log disabled (known issue). Cancel and close stopped the worker and removed their run directories; cancel restored controls. No live child was left in these cases. A direct worker preview smoke test also succeeded. Earlier simple close check took ~0.003s. These checks do **not** establish responsiveness with the real VTK viewer or a busy Volco process. Packaged execution was not retested in this pass.

## Desktop check (partial)

A source-app run with `examples/test_cube.gcode` completed, progressed through mesh export, and produced an STL that matched the displayed model; Run Log and result path worked. **Engine investigation:** that run has a large glob at one frame corner, visible in both the viewer and the saved STL ([screenshot](docs/test_cube_corner_glob.png)). Exact GUI parameter values from the run were not recorded; reproduce before diagnosing Volco/G-code deposition. This is not a viewer-only artifact. Free orbit allows the build plate to turn sideways/upside-down; consider a fixed-up interaction mode or quick camera reset in step 3. Cancel on a larger file felt smooth to the user.

Closing the main window could not be tested by mouse because the progress dialog is modal. Ctrl+C in the launching terminal instead killed the GUI without its normal close handler and **left a Volco child process tree running** (Windows `.venv` launcher and an underlying Python process). That specific orphaned tree was stopped manually. This is not evidence that `closeEvent()` fails, but it exposes a forced-exit/process-tree cleanup gap; do not treat Ctrl+C as a close test. A controlled **real desktop** run with the VTK viewer and the same larger G-code invoked `window.close()` by timer during simulation: close returned in ~0.035s, the worker reported `canceled`, its run directory was removed, and no simulation child process remained. Confirm child/grandchild behavior during a normal cancel on a long enough run as part of the follow-up.

## Next checkpoints

- **Lifecycle follow-up:** a controlled Windows test reproduced an orphaned Python grandchild when canceling only the venv launcher. Normal cancel now terminates the process tree via `taskkill /T /F` (regression test). A real busy bundled-Volco run showed two engine Python processes before cancellation and zero afterward; the worker stopped and deleted its run directory. Real close path passed. Forced terminal exit still bypasses normal app cleanup; avoid using Ctrl+C as a close test. Consider bounded cancel UI latency if it becomes noticeable.
- **Step 3 (small UI changes):** consolidate viewer render/mesh/actor handling, add fit/reset and standard camera views; only adjust orbit after trying it interactively. Parameter control and file-drop cleanup are secondary. Preserve layout.
- **Step 4 (verification/delivery):** add lifecycle/start-cancel/error tests and a real STL fixture, test source and packaged flows, remove the absolute machine-specific path in `VolcoGUI.spec`, and reconcile stale documentation (especially references to test mode and an in-process Volco worker). Keep bundled Volco's own test suite separate from GUI regressions.

Out of scope for now: engine/plugin management, physics/FEA UI, presets, comparison tools, and a GUI rewrite.
