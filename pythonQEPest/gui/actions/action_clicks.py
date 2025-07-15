class GUIActionsClicks:
    def __init__(self, menu):
        self.menu = menu

    def on_treeview_click_left(self, event):
        tree = event.widget
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
        selected = tree.selection()
        if item_id in selected:
            tree.selection_remove(item_id)
        else:
            tree.selection_set(item_id)  # [*selected, item_id]

    def on_treeview_click_right(self, event):
        tree = event.widget
        item_id = tree.identify_row(event.y)
        if item_id:
            tree.selection_set(item_id)
            self.menu.tk_popup(event.x_root, event.y_root)