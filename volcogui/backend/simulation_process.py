"""Child-process entry point for one Volco simulation."""

from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path
from typing import Sequence


def _ensure_output_streams() -> None:
    """Restore redirected pipe streams in PyInstaller windowed child processes."""
    for name, descriptor in (("stdout", 1), ("stderr", 2)):
        if getattr(sys, name) is None:
            try:
                stream = os.fdopen(
                    descriptor,
                    "w",
                    buffering=1,
                    encoding="utf-8",
                    errors="replace",
                    closefd=False,
                )
            except OSError:
                stream = open(os.devnull, "w", encoding="utf-8")
            setattr(sys, name, stream)


def run_simulation(config_path: Path) -> None:
    """Load the run request, import the bundled engine, and export its STL."""
    _ensure_output_streams()
    config = json.loads(config_path.read_text(encoding="utf-8"))

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundle_root = Path(sys._MEIPASS)
    else:
        bundle_root = Path(__file__).resolve().parents[2]

    volco_path = bundle_root / "volco"
    if not (volco_path / "volco.py").is_file():
        raise FileNotFoundError(
            f"Bundled Volco engine not found at {volco_path}. "
            "Initialize the Volco submodule and rebuild the application."
        )

    sys.path.insert(0, str(volco_path))
    from volco import run_simulation as run_volco_simulation

    output = run_volco_simulation(
        gcode_path=config["gcode_path"],
        printer_config=config["printer_config"],
        sim_config=config["sim_config"],
    )
    output.export_mesh_to_stl()

    output_path = (
        Path(config["sim_config"]["results_folder"])
        / f'{config["sim_config"]["simulation_name"]}.stl'
    )
    if not output_path.is_file() or output_path.stat().st_size == 0:
        raise FileNotFoundError(f"Volco did not produce an STL at {output_path}")


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point used by source and PyInstaller child processes."""
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Usage: simulation_process.py RUN_CONFIG.json", file=sys.stderr)
        return 2

    try:
        run_simulation(Path(args[0]))
    except Exception:
        traceback.print_exc(file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
