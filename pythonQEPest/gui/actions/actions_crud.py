from tkinter import messagebox, ttk
from pythonQEPest.gui.elements.EditWindow import EditWindow
import pyperclip

from pythonQEPest.gui.utility.DataManager import DataManager


class GUIActionsCRUD:
    def __init__(self, data_tree, result_tree, save_button, index):
        self.index = index
        self.data_manager = DataManager()
        self.data_tree: ttk.Treeview = data_tree
        self.result_tree: ttk.Treeview = result_tree
        self.save_button = save_button

    def edit_selected(self):
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Select Entry", "Select Entry for editing")
            return

        item_id = selected[0]
        EditWindow(item_id=item_id, tree=self.data_tree, child_tree=self.result_tree)

    def copy_selected(self):
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Select Entry", "Select Entry for coping")
            return

        rows_text = []
        for item in selected:
            values = self.data_tree.item(item, 'values')[1:]  # без ID
            rows_text.append('\t'.join(map(str, values)))

        data_str = '\n'.join(rows_text)
        pyperclip.copy(data_str)
        messagebox.showinfo("Copied", "Data copied to clipboard.")

    def paste_entries(self):
        clipboard_text = pyperclip.paste()
        if not clipboard_text.strip():
            messagebox.showwarning("Clipboard is empty", "Copy the text first.")
            return

        lines = clipboard_text.strip().splitlines()
        count_added = 0

        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) == 7:
                idx = self.index
                self.data_manager.add_file((idx, *parts))
                self.data_tree.insert('', 'end', values=(idx, *parts))
                count_added += 1
                self.index += 1

        if count_added:
            messagebox.showinfo("Inserted", f"Inserted {count_added} entries. Don't forget to process the data.")

    def delete_selected(self):
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Select Entry", "Select the entry to delete.")
            return

        idxs_to_remove = []
        for item in selected:
            values = self.data_tree.item(item, 'values')
            idx_to_remove = int(values[0])
            idxs_to_remove.append(idx_to_remove)

            self.data_tree.delete(item)

            if self.result_tree.exists(item):
                self.result_tree.delete(item)

        self.data_manager.remove_result_by_ids(idxs_to_remove)
        self.data_manager.remove_file_by_ids(idxs_to_remove)

        messagebox.showinfo("Deleted", "The selected records have been deleted.")

        if not self.data_manager:
            self.save_button.config(state='disabled')
