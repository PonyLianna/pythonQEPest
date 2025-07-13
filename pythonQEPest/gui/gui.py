import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pyperclip

from pythonQEPest.core.qepest import QEPest
from pythonQEPest.dto.QEPestInput import QEPestInput


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PythonQEPest")

        self.qepest = QEPest()

        self.file_data = []
        self.result_data = []

        self.build_gui()

    def build_gui(self):
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=5)

        frame_buttons.pack(anchor='w', fill='x', pady=5)

        tk.Button(frame_buttons, text="Select File", command=self.load_file).pack(side='left', padx=[10,4])
        tk.Button(frame_buttons, text="Add entry", command=self.add_entry).pack(side='left', padx=4)
        tk.Button(frame_buttons, text="Delete entry", command=self.delete_selected).pack(side='left', padx=4)
        tk.Button(frame_buttons, text="Copy Data", command=self.copy_selected).pack(side='left', padx=4)
        tk.Button(frame_buttons, text="Paste Data", command=self.paste_entries).pack(side='left', padx=4)
        tk.Button(frame_buttons, text="Process Data", command=self.process_data).pack(side='right', padx=10)

        self.data_tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'MW', 'LogP', 'HBA', 'HBD', 'RB', 'arR'), show='headings')

        for col in self.data_tree['columns']:
            self.data_tree.heading(col, text=col)
        self.data_tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.result_tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'QEH', 'QEI', 'QEF'), show='headings')

        for col in self.result_tree['columns']:
            self.result_tree.heading(col, text=col)
        self.result_tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.save_button = tk.Button(self.root, text="Save Results", command=self.save_result, state='disabled')
        self.save_button.pack(padx=10, pady=10, side='right')

        self.data_tree.unbind_class("Treeview", "<Button-1>")
        self.result_tree.unbind_class("Treeview", "<Button-1>")

        self.data_tree.unbind_class("Treeview", "<Button-2>")
        self.result_tree.unbind_class("Treeview", "<Button-2>")

        self.data_tree.bind("<Button-1>", self.on_treeview_click_left)
        self.result_tree.bind("<Button-1>", self.on_treeview_click_left)

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Copy", command=self.copy_selected)
        self.menu.add_command(label="Paste", command=self.paste_entries)
        self.menu.add_command(label="Delete", command=self.delete_selected)

        self.data_tree.bind("<Button-3>", self.on_treeview_click_right)
        self.result_tree.bind("<Button-3>", self.on_treeview_click_right)

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
                idx = len(self.file_data)
                self.file_data.append((idx, *parts))
                self.data_tree.insert('', 'end', values=(idx, *parts))
                count_added += 1

        if count_added:
            messagebox.showinfo("Inserted", f"Inserted {count_added} entries. Don't forget to process the data.")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.file_data = []
                self.data_tree.delete(*self.data_tree.get_children())

                for idx, line in enumerate(file):
                    parts = line.strip().split('\t')
                    if len(parts) == 7:
                        self.file_data.append((idx, *parts))
                        self.data_tree.insert('', 'end', values=(idx, *parts))

            messagebox.showinfo("File uploaded", f"Loaded {len(self.file_data)} rows.")
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

            idx = len(self.file_data)
            self.file_data.append((idx, *values))
            self.data_tree.insert('', 'end', values=(idx, *values))
            form.destroy()
            messagebox.showinfo("Added", "The entry has been added. Process the data to update the result.")

        tk.Button(form, text="Add", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)

        form.wait_window()

    def delete_selected(self):
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Select Entry", "Select the entry to delete.")
            return

        for item in selected:
            values = self.data_tree.item(item, 'values')
            idx_to_remove = int(values[0])
            self.file_data = [row for row in self.file_data if row[0] != idx_to_remove]
            self.data_tree.delete(item)
            self.result_tree.delete(item)

        messagebox.showinfo("Deleted", "The selected records have been deleted. Please reprocess the data.")
        # self.result_tree.delete(*self.result_tree.get_children())
        self.save_button.config(state='disabled')

    def process_data(self):
        if not self.file_data:
            messagebox.showwarning("No data", "Please add or upload data first.")
            return

        self.result_data = []
        self.result_tree.delete(*self.result_tree.get_children())

        for row in self.file_data:
            result_row = [row[0], *self.qepest.compute_params(QEPestInput.from_array(row[1:])).to_array()]
            self.result_data.append(result_row)
            self.result_tree.insert('', 'end', values=result_row)

        self.save_button.config(state='normal')

    def save_result(self):
        if not self.result_data:
            messagebox.showwarning("No result", "Process the data first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")])
        if not save_path:
            return

        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write("Name\tQEH\tQEI\tQEF\n")
                for row in self.result_data:
                    file.write('\t'.join(map(str, row)) + '\n')

            messagebox.showinfo("Saved", f"The result is saved in: {save_path}")
            self.save_button.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Saving error", str(e))

    def on_treeview_click_left(self, event):
        tree = event.widget
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
        selected = tree.selection()
        if item_id in selected:
            tree.selection_remove(item_id)
        else:
            tree.selection_set(item_id) # [*selected, item_id]

    def on_treeview_click_right(self, event):
        tree = event.widget
        item_id = tree.identify_row(event.y)
        if item_id:
            tree.selection_set(item_id)
            self.menu.tk_popup(event.x_root, event.y_root)
        else:
            pass



if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
