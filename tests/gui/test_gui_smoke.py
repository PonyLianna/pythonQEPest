import os
import tkinter as tk

import pytest

from pythonQEPest.gui.gui import GUI


@pytest.mark.skip(reason="Bruh")
@pytest.mark.skipif(
    os.name != "nt",
    reason="Tkinter GUI smoke test is enabled only on Windows by default.",
)
def test_gui_smoke_creation():
    root = tk.Tk()
    root.withdraw()

    GUI(root)

    root.destroy()
