from tkinter import Menu as tkMenu


class Menu(tkMenu):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs, tearoff=0)

    def set_actions(self, actions_crud):
        self.add_command(label="Copy", command=actions_crud.copy_selected)
        self.add_command(label="Edit", command=actions_crud.edit_selected)
        self.add_command(label="Paste", command=actions_crud.paste_entries)
        self.add_command(label="Delete", command=actions_crud.delete_selected)
