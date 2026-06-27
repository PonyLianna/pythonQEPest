from ttkbootstrap import Frame, Button

try:
    import pyperclip
except ImportError:
    pyperclip = None


class ButtonsFrame(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.pack(anchor="w", fill="x", pady=(10, 0))

        self.select_file_button = Button(self, text="Select File", bootstyle="primary")
        self.add_entry_button = Button(self, text="Add entry", bootstyle="success")
        self.edit_entry_button = Button(self, text="Edit entry", bootstyle="info")
        self.delete_selected_button = Button(
            self, text="Delete entry", bootstyle="danger"
        )
        self.copy_button = Button(self, text="Copy Data", bootstyle="secondary")
        self.paste_button = Button(self, text="Paste Data", bootstyle="secondary")

        self.process_data_button = Button(
            self, text="Process Data", bootstyle="success"
        )
        self.clear_button = Button(self, text="Clear Data", bootstyle="danger-outline")

    def set_actions(self, actions_crud, actions_other):
        self.select_file_button.pack(side="left", padx=(10, 4))
        self.add_entry_button.pack(side="left", padx=4)
        self.edit_entry_button.pack(side="left", padx=4)
        self.delete_selected_button.pack(side="left", padx=4)

        if not pyperclip:
            self.copy_button.config(state="disabled")
            self.paste_button.config(state="disabled")

        self.copy_button.pack(side="left", padx=4)
        self.paste_button.pack(side="left", padx=4)

        self.process_data_button.pack(side="right", padx=(4, 10))
        self.clear_button.pack(side="right", padx=4)

        self.select_file_button.config(command=actions_other.load_file)
        self.add_entry_button.config(command=actions_other.add_entry)
        self.edit_entry_button.config(command=actions_crud.edit_selected)
        self.delete_selected_button.config(command=actions_crud.delete_selected)
        self.copy_button.config(command=actions_crud.copy_selected)
        self.paste_button.config(command=actions_crud.paste_entries)

        self.process_data_button.config(command=actions_other.process_data)
        self.clear_button.config(command=actions_crud.clear_everything)
