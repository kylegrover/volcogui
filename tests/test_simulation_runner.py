import subprocess
import sys
import threading
from pathlib import Path

from volcogui.backend.simulation_runner import SimulationWorker, build_simulation_config


PARAMS = {
    "nozzle_diameter": 0.4,
    "voxel_size": 0.08,
    "step_size": 0.1,
}


class CommandWorker(SimulationWorker):
    def __init__(self, command):
        super().__init__("unused.gcode", PARAMS)
        self.command = command

    def _command(self, config_path: Path) -> list[str]:
        return self.command


def test_config_uses_unique_results_directories(tmp_path):
    first = build_simulation_config("part.gcode", PARAMS, tmp_path / "run-1")
    second = build_simulation_config("part.gcode", PARAMS, tmp_path / "run-2")

    assert first["sim_config"]["results_folder"] != second["sim_config"]["results_folder"]
    assert first["sim_config"]["sphere_z_offset"] == 0.2
    assert first["gcode_path"].endswith("part.gcode")


def test_failed_engine_run_reports_output_and_removes_partial_files():
    worker = CommandWorker(
        [sys.executable, "-u", "-c", "print('engine failure', flush=True); raise SystemExit(7)"]
    )
    run_dir = worker.run_dir

    worker.start()
    assert worker.wait(10_000)

    assert worker.outcome == "error"
    assert "code 7" in worker.error_message
    assert "engine failure" in worker.error_message
    assert not run_dir.exists()


def test_cancel_terminates_child_and_removes_partial_files():
    worker = CommandWorker(
        [sys.executable, "-u", "-c", "import time; time.sleep(60)"]
    )
    run_dir = worker.run_dir

    worker.start()
    cancel_timer = threading.Timer(0.25, worker.cancel)
    cancel_timer.start()
    assert worker.wait(10_000)
    cancel_timer.join(timeout=2)

    assert worker.outcome == "canceled"
    assert not worker.isRunning()
    assert not run_dir.exists()
