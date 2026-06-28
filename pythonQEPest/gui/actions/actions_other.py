from tkinter import filedialog, messagebox

from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.gui.utility.DataManager import DataManager


class GUIActionsOther:
    def __init__(self, root, data_tree, result_tree, save_button, qepest, entry_panel):
        self.data_manager = DataManager()
        self.root = root
        self.data_tree = data_tree
        self.result_tree = result_tree
        self.save_button = save_button
        self.qepest = qepest
        self.entry_panel = entry_panel

    def load_file(self, *args):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            with open(file_path, encoding="utf-8") as file:
                self.data_manager.push_undo()
                self.data_manager.clear_file()
                self.data_tree.delete(*self.data_tree.get_children())

                for line in file:
                    parts = line.strip().split("\t")
                    if len(parts) == 7:
                        try:
                            float(parts[1])
                        except ValueError:
                            continue
                        idx = self.data_manager.next_file_id
                        self.data_manager.add_file((idx, *parts))
                        self.data_tree.insert("", "end", values=(idx, *parts))

            messagebox.showinfo(
                "File uploaded", f"Loaded {len(self.data_manager.file_data)} rows."
            )
        except Exception as e:
            messagebox.showerror("Loading error", str(e))

    def add_entry(self):
        next_id = self.data_manager.next_file_id
        self.entry_panel.clear_for_add(next_id)

    def save_from_panel(self, mode, item_id, values):
        self.data_manager.push_undo()
        if mode == "add":
            self.data_manager.add_file(tuple(values))
            self.data_tree.insert("", "end", values=tuple(str(v) for v in values))
            next_id = self.data_manager.next_file_id
            self.entry_panel.reset_after_save(next_id)
            messagebox.showinfo(
                "Added",
                "The entry has been added. Process the data to update the result.",
            )
        elif mode == "edit" and item_id:
            str_values = [str(v) for v in values]
            self.data_tree.item(item_id, values=tuple(str_values))

            old_id = int(self.data_tree.set(item_id, self.data_tree["columns"][0]))

            if self.result_tree.exists(item_id):
                child_values = list(self.result_tree.item(item_id, "values"))
                child_values[0] = str(values[0])
                child_values[1] = str(values[1])
                self.result_tree.item(item_id, values=tuple(child_values))

                res_matches = [
                    x for x in self.data_manager.result_data if x[0] == old_id
                ]
                if res_matches:
                    ridx = self.data_manager.result_data.index(res_matches[0])
                    updated = list(self.data_manager.result_data[ridx])
                    updated[0] = int(values[0])
                    updated[1] = str(values[1])
                    self.data_manager.update_result(
                        index=ridx, new_entry=tuple(updated)
                    )

            matches = [x for x in self.data_manager.file_data if x[0] == old_id]
            if matches:
                idx = self.data_manager.file_data.index(matches[0])
                self.data_manager.update_file(index=idx, new_entry=values)
            messagebox.showinfo("Saved", "The entry has been updated.")

    def process_data(self):
        if not self.data_manager.file_data:
            messagebox.showwarning("No data", "Please add or upload data first.")
            return

        self.data_manager.push_undo()
        self.data_manager.clear_result()
        self.result_tree.delete(*self.result_tree.get_children())

        for row in self.data_manager.file_data:
            try:
                result_row = [
                    row[0],
                    *self.qepest.compute_params(
                        QEPestInput.from_array(row[1:])
                    ).to_array(),
                ]
            except ValueError as e:
                messagebox.showwarning("Warning!", f"Line number: {row[0]}\n{str(e)}")
                continue
            self.data_manager.add_result(result_row)
            self.result_tree.insert("", "end", values=result_row)

        self.save_button.config(state="normal")

    def save_result(self, *args):
        if not self.data_manager.result_data:
            messagebox.showwarning("No result", "Process the data first.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )
        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write("Name\tQEH\tQEI\tQEF\n")
                for row in self.data_manager.result_data:
                    file.write("\t".join(map(str, row)) + "\n")

            messagebox.showinfo("Saved", f"The result is saved in: {save_path}")

        except Exception as e:
            messagebox.showerror("Saving error", str(e))
