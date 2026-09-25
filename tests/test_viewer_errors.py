import pytest

from volcogui.ui import viewer_widget


def test_load_stl_reports_unavailable_viewer(monkeypatch):
    monkeypatch.setattr(viewer_widget, "PYVISTA_AVAILABLE", False)

    with pytest.raises(RuntimeError, match="PyVista is not available"):
        viewer_widget.ViewerWidget.load_stl(object(), "part.stl")
