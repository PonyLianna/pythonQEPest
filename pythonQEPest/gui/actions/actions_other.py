import tkinter as tk
from tkinter import filedialog, messagebox

from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.gui.utility.DataManager import DataManager


class GUIActionsOther:
    def __init__(self, root, data_tree, result_tree, save_button, qepest):
        self.data_manager = DataManager()
        self.root = root
        self.data_tree = data_tree
        self.result_tree = result_tree
        self.save_button = save_button
        self.qepest = qepest

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data_manager.clear_file()
                self.data_tree.delete(*self.data_tree.get_children())

                for idx, line in enumerate(file):
                    parts = line.strip().split('\t')
                    if len(parts) == 7:
                        self.data_manager.add_file((idx, *parts))
                        self.data_tree.insert('', 'end', values=(idx, *parts))

            messagebox.showinfo("File uploaded", f"Loaded {len(self.data_manager.file_data)} rows.")
        except Exception as e:
            messagebox.showerror("Loading error", str(e))

    def add_entry(self):
        form = tk.Toplevel(self.root)
        form.title("Add entry")
        form.transient(self.root)
        form.grab_set()

        entries = {}
        fields = ['Name', 'MW', 'LogP', 'HBA', 'HBD', 'RB', 'arR']

        for idx, field in enumerate(fields):
            tk.Label(form, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(form)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries[field] = entry

        def submit():
            values = []
            for field in fields:
                val = entries[field].get().strip()
                if not val:
                    messagebox.showwarning("Error", f"The field {field} not filled.")
                    return
                values.append(val)

            idx = len(self.data_manager.file_data)
            self.data_manager.add_file((idx, *values))
            self.data_tree.insert('', 'end', values=(idx, *values))
            form.destroy()
            messagebox.showinfo("Added", "The entry has been added. Process the data to update the result.")

        tk.Button(form, text="Add", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)

        form.wait_window()

    def process_data(self):
        if not self.data_manager.file_data:
            messagebox.showwarning("No data", "Please add or upload data first.")
            return

        # self.result_data = []
        # self.result_tree.delete(*self.result_tree.get_children())

        for row in self.data_manager.file_data:
            try:
                result_row = [row[0], *self.qepest.compute_params(QEPestInput.from_array(row[1:])).to_array()]
            except ValueError as e:
                messagebox.showwarning("Warning!", f"Line number: {row[0]}\n{str(e)}")
                continue
            self.data_manager.add_result(result_row)
            self.result_tree.insert('', 'end', values=result_row)

        self.save_button.config(state='normal')

    def save_result(self):
        if not self.data_manager.result_data:
            messagebox.showwarning("No result", "Process the data first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])
        if not save_path:
            return

        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write("Name\tQEH\tQEI\tQEF\n")
                for row in self.data_manager.result_data:
                    file.write('\t'.join(map(str, row)) + '\n')

            messagebox.showinfo("Saved", f"The result is saved in: {save_path}")

        except Exception as e:
            messagebox.showerror("Saving error", str(e))
