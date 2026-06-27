import ttkbootstrap as tb

from dotenv import load_dotenv

from pythonQEPest.logger import init_logger

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


# TODO: Outdated. Must be dynamic
class GUI(QEPestMeta):
    def treeview_sort_column(self, treeview, col, reverse):
        for c in treeview["columns"]:
            text = c
            if c == col:
                text += " ▲" if not reverse else " ▼"
            treeview.heading(c, text=text)

        treeview_lst = [(treeview.set(k, col), k) for k in treeview.get_children("")]
        try:
            treeview_lst.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            treeview_lst.sort(key=lambda t: t[0], reverse=reverse)

        for index, (_, k) in enumerate(treeview_lst):
            treeview.move(k, "", index)

        treeview.heading(
            col, command=lambda: self.treeview_sort_column(treeview, col, not reverse)
        )

        other = self.result_tree if treeview is self.data_tree else self.data_tree
        id_to_item = {
            other.set(k, other["columns"][0]): k for k in other.get_children("")
        }
        for index, (_, k) in enumerate(treeview_lst):
            match_id = treeview.set(k, treeview["columns"][0])
            if match_id in id_to_item:
                other.move(id_to_item[match_id], "", index)

    def build_gui(self):
        self.file_data = []

        self.buttons_frame = ButtonsFrame(root=self.root)
        self.data_tree = DataTree(root=self.root)
        self.result_tree = ResultTree(root=self.root)
        self.save_button = SaveButton(root=self.root)
        self.menu = Menu(root=self.root)

        self.actions_clicks = GUIActionsClicks(menu=self.menu)
        self.actions_crud = GUIActionsCRUD(
            data_tree=self.data_tree,
            result_tree=self.result_tree,
            save_button=self.save_button,
        )

        self.actions_other = GUIActionsOther(
            data_tree=self.data_tree,
            result_tree=self.result_tree,
            qepest=self.qepest,
            root=self.root,
            save_button=self.save_button,
        )

        self.buttons_frame.set_actions(self.actions_crud, self.actions_other)
        self.data_tree.set_actions(self.treeview_sort_column, self.actions_clicks)
        self.result_tree.set_actions(self.treeview_sort_column, self.actions_clicks)
        self.save_button.set_actions(self.actions_other)
        self.menu.set_actions(self.actions_crud)

        self.root.bind("<Delete>", self.actions_crud.delete_selected)
        self.root.bind("<Control-s>", self.actions_other.save_result)
        self.root.bind("<Control-o>", self.actions_other.load_file)

        if pyperclip:
            self.root.bind("<Control-v>", self.actions_crud.paste_entries)
            self.root.bind("<Control-c>", self.actions_crud.copy_selected)


def main() -> int:
    load_dotenv()
    init_logger()

    root = tb.Window(themename="superhero")
    root.title("PythonQEPest")
    GUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
