import tkinter as tk
from tkinter.ttk import Treeview

from pythonQEPest.gui.utility.DataManager import DataManager


class EditWindow(tk.Toplevel):
    def __init__(self, tree: Treeview, child_tree: Treeview, item_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Edit Entry")

        self.data_manager = DataManager()

        values = tree.item(item_id, "values")
        old_id = int(values[0])

        entries = []
        columns = tree["columns"]

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.resizable(True, False)

        for idx, col in enumerate(columns):
            tk.Label(self, text=col).grid(
                row=idx, column=0, padx=5, pady=5, sticky="ew"
            )
            entry = tk.Entry(self)
            entry.insert(0, values[idx])
            entry.grid(row=idx, column=1, padx=(5, 5), pady=5, sticky="ew")
            entries.append(entry)

        def save_changes() -> None:
            new_values = [entry.get() for entry in entries]
            new_values[0] = int(new_values[0])

            tree.item(item_id, values=tuple(str(v) for v in new_values))

            if child_tree.exists(item_id):
                new_child_values = list(child_tree.item(item_id, "values"))
                if new_child_values[0] != str(new_values[0]):
                    new_child_values[0] = str(new_values[0])
                    child_tree.item(item_id, values=new_child_values)

            elements = [x for x in self.data_manager.file_data if x[0] == old_id]
            if elements:
                idx = self.data_manager.file_data.index(elements[0])
                self.data_manager.update_file(index=idx, new_entry=new_values)
            self.destroy()

        tk.Button(self, text="Save", command=save_changes).grid(
            row=len(columns), column=0, columnspan=2, pady=10
        )

        self.grab_set()
        self.wait_window()
