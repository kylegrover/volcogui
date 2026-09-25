"""Run Log remains useful even when the engine produces no output."""

from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QPlainTextEdit, QWidget

from volcogui.ui import main_window


def test_error_without_engine_output_has_accessible_run_log(monkeypatch):
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance() or QApplication([])
    monkeypatch.setattr(main_window, "ViewerWidget", QWidget)
    monkeypatch.setattr(main_window.QMessageBox, "critical", lambda *args: None)

    window = main_window.MainWindow()

    class FailedWorker:
        outcome = "error"
        error_message = "Could not start the engine"
        diagnostics_text = ""
        gcode_path = "part.gcode"

        def wait(self):
            return True

        def isRunning(self):
            return False

    window.simulation_worker = FailedWorker()
    window._on_simulation_worker_finished()
    assert window.run_log_button.isEnabled()
    assert "Could not start the engine" in window.last_run_summary

    displayed = {}

    def inspect_dialog(dialog):
        displayed["summary"] = dialog.findChild(QLabel).text()
        displayed["output"] = dialog.findChild(QPlainTextEdit).toPlainText()
        return 0

    monkeypatch.setattr(QDialog, "exec", inspect_dialog)
    window._show_run_diagnostics()
    assert "Result: error" in displayed["summary"]
    assert displayed["output"] == "No engine output was captured."
    window.close()
