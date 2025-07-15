import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pyperclip

from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.gui.actions import GUIActionsCRUD, GUIActionsOther
from pythonQEPest.gui.actions import GUIActionsClicks
from pythonQEPest.gui.actions import GUIActionsCRUD
from pythonQEPest.gui.gui_meta import QEPestMeta


class GUI(QEPestMeta):
    def build_gui(self):
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=5)

        frame_buttons.pack(anchor='w', fill='x', pady=5)

        self.file_data = []
        self.select_file_button = tk.Button(frame_buttons, text="Select File")
        self.add_entry_button = tk.Button(frame_buttons, text="Add entry")
        self.delete_selected_button = tk.Button(frame_buttons, text="Delete entry")
        self.copy_button = tk.Button(frame_buttons, text="Copy Data")
        self.paste_button = tk.Button(frame_buttons, text="Paste Data")
        self.process_data_button = tk.Button(frame_buttons, text="Process Data")

        self.select_file_button.pack(side='left', padx=[10, 4])
        self.add_entry_button.pack(side='left', padx=4)
        self.delete_selected_button.pack(side='left', padx=4)
        self.copy_button.pack(side='left', padx=4)
        self.paste_button.pack(side='left', padx=4)
        self.process_data_button.pack(side='right', padx=10)

        self.data_tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'MW', 'LogP', 'HBA', 'HBD', 'RB', 'arR'),
                                      show='headings')

        for col in self.data_tree['columns']:
            self.data_tree.heading(col, text=col)

        self.data_tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.result_tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'QEH', 'QEI', 'QEF'), show='headings')

        for col in self.result_tree['columns']:
            self.result_tree.heading(col, text=col)
        self.result_tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.save_button = tk.Button(self.root, text="Save Results", state='disabled')
        self.save_button.pack(padx=10, pady=10, side='right')

        self.data_tree.unbind_class("Treeview", "<Button-1>")
        self.result_tree.unbind_class("Treeview", "<Button-1>")

        self.data_tree.unbind_class("Treeview", "<Button-2>")
        self.result_tree.unbind_class("Treeview", "<Button-2>")

        self.menu = tk.Menu(root, tearoff=0)

        self.actions_clicks = GUIActionsClicks(menu=self.menu)
        self.actions_crud = GUIActionsCRUD(data_tree=self.data_tree,
                                           result_tree=self.result_tree, save_button=self.save_button, file_data=self.file_data)

        self.actions_other = GUIActionsOther(data_tree=self.data_tree, result_tree=self.result_tree, qepest=self.qepest,
                                             root=self.root, save_button=self.save_button, file_data=self.file_data)

        self.select_file_button.config(command=self.actions_other.save_result)
        self.add_entry_button.config(command=self.actions_other.add_entry)
        self.delete_selected_button.config(command=self.actions_crud.delete_selected)
        self.copy_button.config(command=self.actions_crud.copy_selected)
        self.paste_button.config(command=self.actions_crud.paste_entries)
        self.process_data_button.config(command=self.actions_other.process_data)

        self.save_button.config(command=self.actions_other.save_result)

        self.data_tree.bind("<Button-1>", self.actions_clicks.on_treeview_click_left)
        self.result_tree.bind("<Button-1>", self.actions_clicks.on_treeview_click_left)

        self.data_tree.bind("<Button-3>", self.actions_clicks.on_treeview_click_right)
        self.result_tree.bind("<Button-3>", self.actions_clicks.on_treeview_click_right)

        self.menu.add_command(label="Copy", command=self.actions_crud.copy_selected)
        self.menu.add_command(label="Paste", command=self.actions_crud.paste_entries)
        self.menu.add_command(label="Delete", command=self.actions_crud.delete_selected)


if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
