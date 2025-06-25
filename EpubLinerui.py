#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui_label.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class EpubLinerUI:
    def __init__(
        self,
        master=None,
        translator=None,
        on_first_object_cb=None,
        data_pool=None
    ):
        self.builder = pygubu.Builder(
            translator=translator,
            on_first_object=on_first_object_cb,
            data_pool=data_pool
        )
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = self.builder.get_object("tk_1", master)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def a(self, event=None):
        pass

    def d(self, event=None):
        pass

    def h(self, event=None):
        pass

    def s(self, event=None):
        pass

    def w(self, event=None):
        pass

    def x(self, event=None):
        pass

    def z(self, event=None):
        pass


if __name__ == "__main__":
    app = EpubLinerUI()
    app.run()
