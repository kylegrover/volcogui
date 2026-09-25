import sys
import threading
from pathlib import Path

import pytest
from PyQt6.QtCore import Qt

from volcogui.backend.simulation_runner import (
    MAX_DIAGNOSTIC_LINES,
    MAX_DIAGNOSTIC_LINE_LENGTH,
    SimulationWorker,
    build_simulation_config,
    validate_gcode_path,
)


PARAMS = {
    "nozzle_diameter": 0.4,
    "voxel_size": 0.08,
    "step_size": 0.1,
}


class CommandWorker(SimulationWorker):
    def __init__(self, command, gcode_path):
        super().__init__(str(gcode_path), PARAMS)
        self.command = command

    def _command(self, config_path: Path) -> list[str]:
        if callable(self.command):
            return self.command(config_path)
        return self.command


def test_config_uses_unique_results_directories(tmp_path):
    gcode_path = tmp_path / "part.gcode"
    gcode_path.write_text("G28\n", encoding="utf-8")
    first = build_simulation_config(str(gcode_path), PARAMS, tmp_path / "run-1")
    second = build_simulation_config(str(gcode_path), PARAMS, tmp_path / "run-2")

    assert first["sim_config"]["results_folder"] != second["sim_config"]["results_folder"]
    assert first["sim_config"]["sphere_z_offset"] == 0.2
    assert first["gcode_path"] == str(gcode_path.resolve())


def test_gcode_path_validation_requires_existing_gcode_file(tmp_path):
    valid_path = tmp_path / "part.GCODE"
    valid_path.write_text("G28\n", encoding="utf-8")
    assert validate_gcode_path(valid_path) == valid_path.resolve()

    with pytest.raises(FileNotFoundError, match="does not exist"):
        validate_gcode_path(tmp_path / "missing.gcode")
    with pytest.raises(ValueError, match="not a file"):
        validate_gcode_path(tmp_path)

    wrong_extension = tmp_path / "part.txt"
    wrong_extension.write_text("G28\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Expected a .gcode"):
        validate_gcode_path(wrong_extension)


def test_progress_stays_below_complete_until_output_is_validated(tmp_path):
    gcode_path = tmp_path / "part.gcode"
    gcode_path.write_text("G28\n", encoding="utf-8")
    worker = SimulationWorker(str(gcode_path), PARAMS)
    percentages = []
    messages = []
    worker.progress_percent.connect(percentages.append, Qt.ConnectionType.DirectConnection)
    worker.progress.connect(messages.append, Qt.ConnectionType.DirectConnection)

    worker._handle_output("Deposited step 10/10")
    assert percentages == [99]
    assert worker.outcome == "running"

    worker._handle_output("VOLCOGUI_STAGE:stl_export")
    worker._handle_output("VOLCOGUI_STAGE:output_validation")
    assert messages[-2:] == ["Generating STL mesh...", "Validating STL output..."]
    worker._remove_failed_run()


def test_success_keeps_bounded_diagnostics_and_validates_stl(tmp_path):
    gcode_path = tmp_path / "part.gcode"
    gcode_path.write_text("G28\n", encoding="utf-8")
    script = "\n".join((
        "import json, sys, time",
        "from pathlib import Path",
        "config = json.loads(Path(sys.argv[1]).read_text())",
        "print('Number of printed filaments: 1')",
        "print('Deposited step 1/1')",
        "for i in range(105): print(f'engine line {i}')",
        "print('x' * 2500)",
        "print('VOLCOGUI_STAGE:stl_export', flush=True)",
        "time.sleep(0.3)",
        "output = Path(config['sim_config']['results_folder']) / 'volcogui_simulation.stl'",
        "output.parent.mkdir(parents=True, exist_ok=True)",
        "output.write_bytes(b'solid part')",
    ))
    worker = CommandWorker(
        lambda config_path: [sys.executable, "-u", "-c", script, str(config_path)],
        gcode_path,
    )
    percentages = []
    final_voxel_step_seen = threading.Event()

    def record_progress(percent):
        percentages.append(percent)
        if percent == 99:
            final_voxel_step_seen.set()

    worker.progress_percent.connect(record_progress, Qt.ConnectionType.DirectConnection)

    worker.start()
    assert final_voxel_step_seen.wait(5)
    assert worker.isRunning()
    assert not worker.output_stl.exists()
    assert 100 not in percentages
    assert worker.wait(10_000)

    assert worker.outcome == "success"
    assert worker.output_stl.is_file()
    assert percentages[-1] == 100
    diagnostics = worker.diagnostics_text.splitlines()
    assert len(diagnostics) <= MAX_DIAGNOSTIC_LINES
    assert all(len(line) <= MAX_DIAGNOSTIC_LINE_LENGTH for line in diagnostics)
    assert "Generating STL mesh..." in worker.diagnostics_text


def test_failed_engine_run_reports_output_and_removes_partial_files(tmp_path):
    gcode_path = tmp_path / "failure.gcode"
    gcode_path.write_text("G28\n", encoding="utf-8")
    worker = CommandWorker(
        [sys.executable, "-u", "-c", "print('engine failure', flush=True); raise SystemExit(7)"],
        gcode_path,
    )
    run_dir = worker.run_dir

    worker.start()
    assert worker.wait(10_000)

    assert worker.outcome == "error"
    assert "code 7" in worker.error_message
    assert "engine failure" in worker.error_message
    assert not run_dir.exists()


def test_cancel_terminates_child_and_removes_partial_files(tmp_path):
    gcode_path = tmp_path / "cancel.gcode"
    gcode_path.write_text("G28\n", encoding="utf-8")
    worker = CommandWorker(
        [sys.executable, "-u", "-c", "import time; time.sleep(60)"],
        gcode_path,
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
