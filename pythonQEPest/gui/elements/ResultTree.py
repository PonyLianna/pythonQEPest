from tkinter.ttk import Treeview


class ResultTree(Treeview):
    def __init__(self, root, *args, **kwargs):
        columns = ('ID', 'Name', 'QEH', 'QEI', 'QEF')
        super().__init__(root, columns=columns, show='headings', *args, **kwargs)

        for col in columns:
            self.heading(col, text=col)
        self.pack(padx=10, pady=10, fill='both', expand=True)

    def set_actions(self, sort_column, actions_clicks):
        for col in self['columns']:
            self.heading(col, text=col, command=lambda _col=col: sort_column(self, _col, False))

        self.bind("<Button-1>", actions_clicks.on_treeview_click_left)
        self.bind("<Button-3>", actions_clicks.on_treeview_click_right)