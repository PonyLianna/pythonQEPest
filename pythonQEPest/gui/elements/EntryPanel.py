from tkinter import messagebox

import ttkbootstrap as tb


class EntryPanel(tb.LabelFrame):
    FIELDS = ["ID", "Name", "MW", "LogP", "HBA", "HBD", "RB", "arR"]
    NUMERIC = {
        "MW": float,
        "LogP": float,
        "HBA": int,
        "HBD": int,
        "RB": int,
        "arR": int,
    }

    def __init__(self, parent):
        super().__init__(parent, text="Entry Details")
        self._on_save = None
        self._mode = "add"
        self._item_id = None
        self._orig_values = None

        for col in range(4):
            self.grid_columnconfigure(col, weight=1)

        self._entries = {}
        field_grid = [
            ("ID", 0, 0),
            ("Name", 0, 1),
            ("MW", 0, 2),
            ("LogP", 0, 3),
            ("HBA", 1, 0),
            ("HBD", 1, 1),
            ("RB", 1, 2),
            ("arR", 1, 3),
        ]

        for field, row, col in field_grid:
            f = tb.Frame(self)
            f.grid(row=row, column=col, sticky="nsew", padx=3, pady=2)
            tb.Label(f, text=field, font=("", 9)).pack(anchor="w")
            entry = tb.Entry(f, font=("", 10))
            entry.pack(fill="x", expand=True)
            self._entries[field] = entry

        self.id_entry = self._entries["ID"]

        btn_frame = tb.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=4, sticky="e", pady=(10, 0))

        self.cancel_btn = tb.Button(
            btn_frame,
            text="Cancel",
            bootstyle="secondary-outline",
            command=self._cancel,
        )
        self.cancel_btn.pack(side="right", padx=(5, 0))

        self.save_btn = tb.Button(
            btn_frame, text="Save", bootstyle="success", command=self._save
        )
        self.save_btn.pack(side="right")

        self._setup_mode("add")

    def set_on_save(self, callback):
        self._on_save = callback

    def load_entry(self, values, item_id):
        self._mode = "edit"
        self._item_id = item_id
        self._orig_values = list(values)
        self._setup_mode("edit")
        self._fill(values)

    def clear_for_add(self, next_id):
        self._mode = "add"
        self._item_id = None
        self._orig_values = None
        self._setup_mode("add")
        self._fill([str(next_id), "", "", "", "", "", "", ""])
        self._entries["Name"].focus()

    def get_mode(self):
        return self._mode

    def _setup_mode(self, mode):
        self.save_btn.configure(text="Add" if mode == "add" else "Save")

    def _fill(self, values):
        for i, field in enumerate(self.FIELDS):
            if i < len(values):
                self._entries[field].configure(state="normal")
                self._entries[field].delete(0, "end")
                self._entries[field].insert(0, str(values[i]))
        self.id_entry.configure(state="readonly")

    def cancel(self):
        self._cancel()

    def _cancel(self):
        if self._mode == "edit" and self._orig_values:
            self._fill(self._orig_values)
        else:
            for entry in self._entries.values():
                entry.configure(state="normal")
                entry.delete(0, "end")
            self.id_entry.configure(state="readonly")

    def _save(self):
        values = []
        for field in self.FIELDS:
            raw = self._entries[field].get().strip()
            if not raw:
                messagebox.showwarning(
                    "Validation Error",
                    f"The field '{field}' cannot be empty.",
                )
                self._entries[field].focus()
                return
            if field in self.NUMERIC:
                try:
                    raw = self.NUMERIC[field](raw)
                except ValueError:
                    messagebox.showwarning(
                        "Validation Error",
                        f"'{field}' must be a valid number.",
                    )
                    self._entries[field].focus()
                    return
            values.append(raw)

        if self._on_save:
            self._on_save(self._mode, self._item_id, values)

    def reset_after_save(self, next_id):
        self._mode = "add"
        self._item_id = None
        self._orig_values = None
        id_val = str(next_id)
        self._fill([id_val, "", "", "", "", "", "", ""])
        self._entries["Name"].focus()
        self.save_btn.configure(text="Add")
