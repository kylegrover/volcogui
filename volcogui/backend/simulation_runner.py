"""Run Volco simulations in a separate process so they can be canceled safely."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal


SIMULATION_NAME = "volcogui_simulation"
MAX_DIAGNOSTIC_LINES = 100
MAX_DIAGNOSTIC_LINE_LENGTH = 2000


def build_simulation_config(gcode_path: str, params: dict, run_dir: Path) -> dict:
    """Build the Volco inputs for one isolated run directory."""
    results_dir = run_dir / "results"
    nozzle_diameter = params["nozzle_diameter"]

    printer_config = {
        "nozzle_diameter": nozzle_diameter,
        "feedstock_filament_diameter": params.get("feedstock_filament_diameter", 1.75),
        "nozzle_jerk_speed": params.get("nozzle_jerk_speed", 10.0),
        "extruder_jerk_speed": params.get("extruder_jerk_speed", 5.0),
        "nozzle_acceleration": params.get("nozzle_acceleration", 1000.0),
        "extruder_acceleration": params.get("extruder_acceleration", 5000.0),
    }

    simulation_config = {
        "simulation_name": SIMULATION_NAME,
        "results_folder": str(results_dir),
        "voxel_size": params["voxel_size"],
        "step_size": params["step_size"],
        "x_offset": 5 * nozzle_diameter,
        "y_offset": 5 * nozzle_diameter,
        "z_offset": 5 * nozzle_diameter,
        "sphere_z_offset": 0.5 * nozzle_diameter,
        "x_crop": ["all", "all"],
        "y_crop": ["all", "all"],
        "z_crop": ["all", "all"],
        "radius_increment": params.get("radius_increment", 0.001),
        "solver_tolerance": params.get("solver_tolerance", 0.0001),
        "consider_acceleration": params.get("consider_acceleration", False),
        "stl_ascii": params.get("stl_ascii", False),
        "preview_mode": params.get("preview_mode", False),
    }

    return {
        "gcode_path": str(Path(gcode_path).resolve()),
        "printer_config": printer_config,
        "sim_config": simulation_config,
    }


class SimulationWorker(QThread):
    """Own and monitor an isolated Volco process."""

    progress = pyqtSignal(str)
    progress_percent = pyqtSignal(int)

    def __init__(self, gcode_path: str, params: dict):
        super().__init__()
        self.gcode_path = gcode_path
        self.params = params
        self.run_dir = Path(tempfile.mkdtemp(prefix="volcogui-run-"))
        self.output_stl = self.run_dir / "results" / f"{SIMULATION_NAME}.stl"
        self.outcome = "running"
        self.error_message: str | None = None
        self._cancel_requested = threading.Event()
        self._process_lock = threading.Lock()
        self._process: subprocess.Popen | None = None
        self._recent_output: deque[str] = deque(maxlen=MAX_DIAGNOSTIC_LINES)
        self._start_time = 0.0
        self._last_progress_update = 0.0
        self._total_steps = 0

    def cancel(self) -> None:
        """Request cancellation and stop the child process without killing this thread."""
        self._cancel_requested.set()
        with self._process_lock:
            process = self._process

        if process is None or process.poll() is not None:
            return

        try:
            process.terminate()
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        except OSError:
            # The process may have exited between poll() and terminate().
            pass

    def _command(self, config_path: Path) -> list[str]:
        if getattr(sys, "frozen", False):
            return [sys.executable, "--volcogui-simulation-worker", str(config_path)]

        worker_script = Path(__file__).with_name("simulation_process.py")
        return [sys.executable, "-u", str(worker_script), str(config_path)]

    def _working_directory(self) -> Path:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)
        return Path(__file__).resolve().parents[2]

    def _handle_output(self, line: str) -> None:
        """Extract the progress messages Volco currently writes to its log."""
        import re

        filament_match = re.search(r"Number of printed filaments:\s*(\d+)", line)
        if filament_match:
            self._total_steps = int(filament_match.group(1))
            self._start_time = time.monotonic()
            self.progress.emit(f"Found {self._total_steps} filaments to process")
            return

        step_matches = re.findall(r"Deposited step\s+(\d+)/(\d+)", line)
        if step_matches:
            step, total = map(int, step_matches[-1])
            self._total_steps = total
            now = time.monotonic()
            if now - self._last_progress_update >= 0.1 or step == total:
                elapsed = int(now - self._start_time) if self._start_time else 0
                self.progress.emit(f"Voxelizing step {step}/{total} - {elapsed}s elapsed")
                # Reserve 100% for the successfully completed/exported output.
                self.progress_percent.emit(min(99, int(step * 100 / total)) if total else 0)
                self._last_progress_update = now
            return

        step_one = re.search(r"Depositing filament:\s*step\s*=\s*1/", line)
        if step_one and self._total_steps:
            elapsed = int(time.monotonic() - self._start_time) if self._start_time else 0
            self.progress.emit(f"Voxelizing - {elapsed}s elapsed")

    def _error_message(self, return_code: int) -> str:
        details = "\n".join(self._recent_output)
        message = f"Volco exited with code {return_code}."
        if details:
            message += f"\n\nRecent Volco output:\n{details}"
        return message

    def _remove_failed_run(self) -> None:
        shutil.rmtree(self.run_dir, ignore_errors=True)

    def run(self) -> None:
        """Run the engine and report success only when its STL is present."""
        config_path = self.run_dir / "run.json"
        process = None
        succeeded = False

        try:
            if self._cancel_requested.is_set():
                self.outcome = "canceled"
                return

            config = build_simulation_config(self.gcode_path, self.params, self.run_dir)
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            self.progress.emit("Starting Volco simulation...")
            self._start_time = time.monotonic()

            with self._process_lock:
                if self._cancel_requested.is_set():
                    self.outcome = "canceled"
                    return
                process = subprocess.Popen(
                    self._command(config_path),
                    cwd=self._working_directory(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
                self._process = process

            assert process.stdout is not None
            for output_line in process.stdout:
                line = output_line.rstrip()
                self._recent_output.append(line[:MAX_DIAGNOSTIC_LINE_LENGTH])
                self._handle_output(line)

            return_code = process.wait()
            if self._cancel_requested.is_set():
                self.outcome = "canceled"
                return
            if return_code != 0:
                raise RuntimeError(self._error_message(return_code))
            if not self.output_stl.is_file() or self.output_stl.stat().st_size == 0:
                raise FileNotFoundError(
                    f"Volco exited successfully but did not create an STL at {self.output_stl}"
                )

            succeeded = True
            self.outcome = "success"
            self.progress.emit("Simulation complete!")
            self.progress_percent.emit(100)
        except Exception as exc:
            if self._cancel_requested.is_set():
                self.outcome = "canceled"
            else:
                self.outcome = "error"
                self.error_message = str(exc)
        finally:
            if process is not None:
                if process.poll() is None:
                    self.cancel()
                if process.stdout is not None:
                    process.stdout.close()
                with self._process_lock:
                    self._process = None
            if not succeeded:
                self._remove_failed_run()
