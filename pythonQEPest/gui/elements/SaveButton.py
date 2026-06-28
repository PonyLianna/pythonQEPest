from ttkbootstrap import Button


class SaveButton(Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(
            root,
            *args,
            text="Save Results",
            state="disabled",
            bootstyle="primary",
            **kwargs,
        )
        self.pack(padx=10, pady=10, side="right")

    def set_actions(self, actions_other):
        self.config(command=actions_other.save_result)
