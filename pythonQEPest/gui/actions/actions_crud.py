from tkinter import messagebox, ttk

try:
    import pyperclip
except ImportError:
    pyperclip = None

from pythonQEPest.gui.utility.DataManager import DataManager


class GUIActionsCRUD:
    def __init__(self, data_tree, result_tree, save_button, entry_panel):
        self.data_manager = DataManager()
        self.data_tree: ttk.Treeview = data_tree
        self.result_tree: ttk.Treeview = result_tree
        self.save_button = save_button
        self.entry_panel = entry_panel

    def sync_selection_to_panel(self, *args, **kwargs):
        selected = self.data_tree.selection()
        if selected:
            item_id = selected[0]
            values = self.data_tree.item(item_id, "values")
            self.entry_panel.load_entry(values, item_id)

    def edit_selected(self, *args, **kwargs):
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Select Entry", "Select Entry for editing")
            return

        self.sync_selection_to_panel()

    def undo(self, *args, **kwargs):
        if self.data_manager.undo() is None:
            return
        self._rebuild_from_data_manager()

    def _rebuild_from_data_manager(self):
        self.data_tree.delete(*self.data_tree.get_children())
        self.result_tree.delete(*self.result_tree.get_children())

        for row in self.data_manager.file_data:
            self.data_tree.insert("", "end", values=tuple(str(v) for v in row))
        for row in self.data_manager.result_data:
            self.result_tree.insert("", "end", values=tuple(str(v) for v in row))

        self.entry_panel.cancel()
        self.save_button.config(
            state="normal" if self.data_manager.result_data else "disabled"
        )

    def copy_selected(self, *args, **kwargs):
        selected_data_tree = self.data_tree.selection()
        selected_result_tree = self.result_tree.selection()

        if not (selected_data_tree or selected_result_tree):
            messagebox.showwarning("Select Entry", "Select Entry for coping")
            return

        rows_text = []
        if selected_data_tree:
            rows_text.append(
                "\t".join(
                    map(str, ("ID", "Name", "MW", "LogP", "HBA", "HBD", "RB", "arR"))
                )
            )
            for item in selected_data_tree:
                values = self.data_tree.item(item, "values")[1:]
                rows_text.append("\t".join(map(str, values)))

        if selected_result_tree:
            rows_text.append("\t".join(map(str, ("ID", "Name", "QEH", "QEI", "QEF"))))
            for item in selected_result_tree:
                values = self.result_tree.item(item, "values")[1:]
                rows_text.append("\t".join(map(str, values)))

        data_str = "\n".join(rows_text)

        if not pyperclip:
            messagebox.showerror(
                "Error",
                "pyperclip module is not installed. Install it with command"
                + "'pip install .[gui]' or 'poetry install --with ui'"
                + "to enable copy functionality.",
            )
            return

        pyperclip.copy(data_str)
        messagebox.showinfo("Copied", "Data copied to clipboard.")

    def paste_entries(self, *args, **kwargs):
        if not pyperclip:
            messagebox.showerror(
                "Error",
                "pyperclip module is not installed. Install it with command"
                + "'pip install .[gui]' or 'poetry install --with ui'"
                + "to enable copy functionality.",
            )
            return

        clipboard_text = pyperclip.paste()
        if not clipboard_text.strip():
            messagebox.showwarning("Clipboard is empty", "Copy the text first.")
            return

        lines = clipboard_text.strip().splitlines()
        count_added = 0

        self.data_manager.push_undo()
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) == 7:
                try:
                    float(parts[1])
                except ValueError:
                    continue
                idx = self.data_manager.next_file_id
                self.data_manager.add_file((idx, *parts))
                self.data_tree.insert("", "end", values=(idx, *parts))
                count_added += 1

        if count_added:
            messagebox.showinfo(
                "Inserted",
                f"Inserted {count_added} entries. Don't forget to process the data.",
            )

    def delete_selected(self, *args, **kwargs):
        selected_data = self.data_tree.selection()
        selected_result = self.result_tree.selection()

        if not selected_data and not selected_result:
            messagebox.showwarning("Select Entry", "Select the entry to delete.")
            return

        idxs_to_remove = []

        self.data_manager.push_undo()
        for item in selected_data:
            values = self.data_tree.item(item, "values")
            idxs_to_remove.append(int(values[0]))
            self.data_tree.delete(item)

        for item in selected_result:
            values = self.result_tree.item(item, "values")
            idxs_to_remove.append(int(values[0]))
            self.result_tree.delete(item)

        for child in self.result_tree.get_children(""):
            if int(self.result_tree.set(child, "ID")) in idxs_to_remove:
                self.result_tree.delete(child)

        for child in self.data_tree.get_children(""):
            if int(self.data_tree.set(child, "ID")) in idxs_to_remove:
                self.data_tree.delete(child)

        self.data_manager.remove_result_by_ids(idxs_to_remove)
        self.data_manager.remove_file_by_ids(idxs_to_remove)

        messagebox.showinfo("Deleted", "The selected records have been deleted.")

    def clear_everything(self, *args, **kwargs):
        self.data_manager.push_undo()
        self.data_manager.clear_file()
        self.data_manager.clear_result()

        self.data_tree.delete(*self.data_tree.get_children())
        self.result_tree.delete(*self.result_tree.get_children())
        self.save_button.config(state="disabled")
