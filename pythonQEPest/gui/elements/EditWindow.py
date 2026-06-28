import ttkbootstrap as tb
from tkinter import messagebox


class EditWindow(tb.Toplevel):
    FIELDS = ["ID", "Name", "MW", "LogP", "HBA", "HBD", "RB", "arR"]
    NUMERIC = {
        "MW": float,
        "LogP": float,
        "HBA": int,
        "HBD": int,
        "RB": int,
        "arR": int,
    }

    def __init__(self, parent, title="Edit Entry", initial_values=None):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.result = None

        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        w, h = 400, 420
        self.geometry(f"{w}x{h}+{px + (pw - w) // 2}+{py + (ph - h) // 2}")
        self.resizable(False, False)

        main = tb.Frame(self, padding=15)
        main.pack(fill="both", expand=True)

        tb.Label(main, text="Entry Information", font=("", 14, "bold")).pack(
            anchor="w", pady=(0, 15)
        )

        form = tb.Frame(main)
        form.pack(fill="both", expand=True)
        form.grid_columnconfigure(1, weight=1)

        self.entries = {}

        for i, field in enumerate(self.FIELDS):
            tb.Label(form, text=field, font=("", 10)).grid(
                row=i, column=0, padx=(0, 10), pady=4, sticky="e"
            )
            entry = tb.Entry(form, font=("", 10))
            entry.grid(row=i, column=1, padx=0, pady=4, sticky="ew")

            if initial_values and i < len(initial_values):
                entry.insert(0, str(initial_values[i]))
            if field == "ID":
                entry.configure(state="readonly")

            self.entries[field] = entry

        btn_frame = tb.Frame(main)
        btn_frame.pack(fill="x", pady=(15, 0))

        tb.Button(
            btn_frame,
            text="Cancel",
            bootstyle="secondary-outline",
            command=self.destroy,
        ).pack(side="right", padx=(5, 0))

        tb.Button(
            btn_frame, text="Save", bootstyle="success", command=self._submit
        ).pack(side="right")

        self.bind("<Return>", lambda e: self._submit())
        self.bind("<Escape>", lambda e: self.destroy())

        self.entries["Name"].focus()
        self.grab_set()
        self.wait_window()

    def _submit(self):
        values = []
        for field in self.FIELDS:
            raw = self.entries[field].get().strip()
            if not raw:
                messagebox.showwarning(
                    "Validation Error", f"The field '{field}' cannot be empty."
                )
                self.entries[field].focus()
                return
            if field in self.NUMERIC:
                try:
                    raw = self.NUMERIC[field](raw)
                except ValueError:
                    messagebox.showwarning(
                        "Validation Error", f"'{field}' must be a valid number."
                    )
                    self.entries[field].focus()
                    return
            values.append(raw)

        self.result = values
        self.destroy()
