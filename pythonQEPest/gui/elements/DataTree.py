from tkinter.ttk import Treeview


class DataTree(Treeview):
    def __init__(self, parent, *args, **kwargs):
        columns = ("ID", "Name", "MW", "LogP", "HBA", "HBD", "RB", "arR")
        super().__init__(parent, *args, columns=columns, show="headings", **kwargs)

        for col in columns:
            self.heading(col, text=col)

    def set_actions(self, sort_column, actions_clicks):
        for col in self["columns"]:
            self.heading(
                col, text=col, command=lambda _col=col: sort_column(self, _col, False)
            )

        self.bind("<Button-3>", actions_clicks.on_treeview_click_right)

        self.bind("<Double-1>", actions_clicks.resize_columns)
