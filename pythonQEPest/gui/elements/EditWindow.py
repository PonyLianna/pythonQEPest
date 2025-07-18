import tkinter as tk


class EditWindow(tk.Toplevel):
    def __init__(self, tree, item_id, file_data, *args, **kwargs):
        super().__init__(master=tree, *args, **kwargs)
        self.file_data = file_data
        values = tree.item(item_id, 'values')

        self.title("Edit Entry")

        entries = []
        columns = tree['columns']

        for idx, col in enumerate(columns):
            tk.Label(self, text=col).grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(self)
            entry.insert(0, values[idx])
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        def save_changes():
            new_values = [entry.get() for entry in entries]
            tree.item(item_id, values=new_values)

            # Fix it someday plz
            new_values[0] = int(new_values[0])

            element = list(filter(lambda x: str(x[0]) == str(new_values[0]), self.file_data))[0]
            if element:
                self.file_data[element[0]] = new_values
            self.destroy()

        tk.Button(self, text="Save", command=save_changes).grid(row=len(columns), column=0, columnspan=2, pady=10)

        self.grab_set()
        self.wait_window()
