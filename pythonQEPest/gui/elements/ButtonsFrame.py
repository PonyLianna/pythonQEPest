from tkinter import Frame, Button

from pythonQEPest.gui.actions import GUIActionsCRUD, GUIActionsOther


class ButtonsFrame(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.pack(anchor='w', fill='x', pady=5)

        # TODO: select_file must have an option of CSV
        self.select_file_button = Button(self, text="Select File")
        self.add_entry_button = Button(self, text="Add entry")
        self.delete_selected_button = Button(self, text="Delete entry")
        self.copy_button = Button(self, text="Copy Data")
        self.paste_button = Button(self, text="Paste Data")
        self.process_data_button = Button(self, text="Process Data")

    def set_actions(self, actions_crud, actions_other):
        self.select_file_button.pack(side='left', padx=[10, 4])
        self.add_entry_button.pack(side='left', padx=4)
        self.delete_selected_button.pack(side='left', padx=4)
        self.copy_button.pack(side='left', padx=4)
        self.paste_button.pack(side='left', padx=4)
        self.process_data_button.pack(side='right', padx=10)

        self.select_file_button.config(command=actions_other.save_result)
        self.add_entry_button.config(command=actions_other.add_entry)
        self.delete_selected_button.config(command=actions_crud.delete_selected)
        self.copy_button.config(command=actions_crud.copy_selected)
        self.paste_button.config(command=actions_crud.paste_entries)
        self.process_data_button.config(command=actions_other.process_data)
        