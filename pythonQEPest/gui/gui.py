import tkinter as tk

try:
    import pyperclip
except ImportError:
    pyperclip = None

from pythonQEPest.gui.actions import GUIActionsCRUD
from pythonQEPest.gui.actions import GUIActionsClicks
from pythonQEPest.gui.actions import GUIActionsOther
from pythonQEPest.gui.elements.ButtonsFrame import ButtonsFrame
from pythonQEPest.gui.elements.DataTree import DataTree
from pythonQEPest.gui.elements.Menu import Menu
from pythonQEPest.gui.elements.ResultTree import ResultTree
from pythonQEPest.gui.elements.SaveButton import SaveButton
from pythonQEPest.gui.gui_meta import QEPestMeta


class GUI(QEPestMeta):
    def treeview_sort_column(self, treeview, col, reverse):
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0], reverse=reverse)

        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        treeview.heading(col, command=lambda: self.treeview_sort_column(treeview, col, not reverse))

    def build_gui(self):
        self.file_data = []
        self.index = 0

        self.buttons_frame = ButtonsFrame(root=root)
        self.data_tree = DataTree(root=root)
        self.result_tree = ResultTree(root=root)
        self.save_button = SaveButton(root=root)
        self.menu = Menu(root=root)

        self.actions_clicks = GUIActionsClicks(menu=self.menu)
        self.actions_crud = GUIActionsCRUD(data_tree=self.data_tree, result_tree=self.result_tree,
                                           save_button=self.save_button, index=self.index)

        self.actions_other = GUIActionsOther(data_tree=self.data_tree, result_tree=self.result_tree, qepest=self.qepest,
                                             root=self.root, save_button=self.save_button)

        self.buttons_frame.set_actions(self.actions_crud, self.actions_other)
        self.data_tree.set_actions(self.treeview_sort_column, self.actions_clicks)
        self.result_tree.set_actions(self.treeview_sort_column, self.actions_clicks)
        self.save_button.set_actions(self.actions_other)
        self.menu.set_actions(self.actions_crud)

        if pyperclip:
            root.bind('<Control-v>', self.actions_crud.paste_entries)
            root.bind('<Control-c>', self.actions_crud.copy_selected)


if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
