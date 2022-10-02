import tkinter as tk
from typing import Optional

from converter import convert, evaluate


class MainWindow(tk.Frame):
    def __init__(self, master: Optional[tk.Misc] = None):
        super().__init__(master)

        # Expand on resize
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure("all", weight=1)

        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        self._expr = tk.StringVar(self)
        self._expr.trace("w", lambda _, __, ___: self.on_change())

        # Label definitions
        self.infix_lbl = tk.Label(self, text="Infix Expression:")
        self.postfix_lbl = tk.Label(self, text="Postfix Expression:")
        self.value_lbl = tk.Label(self, text="Value:")
        self.error_lbl = tk.Label(self, text="Errors:")

        # Result labels and input definition
        self.infix = tk.Entry(self, textvariable=self._expr)
        self.postfix = tk.Label(self)
        self.value = tk.Label(self)
        self.errors = tk.Label(self)

        # Putting widgets into place
        self.infix_lbl.grid(column=0, row=0, padx=5, pady=5, sticky="e")
        self.postfix_lbl.grid(column=0, row=1, padx=5, pady=5, sticky="e")
        self.value_lbl.grid(column=0, row=2, padx=5, pady=5, sticky="e")
        self.error_lbl.grid(column=0, row=3, padx=5, pady=5, sticky="e")

        self.infix.grid(column=1, row=0, padx=5, pady=5, sticky="news")
        self.postfix.grid(column=1, row=1, padx=5, pady=5, sticky="w")
        self.value.grid(column=1, row=2, padx=5, pady=5, sticky="w")
        self.errors.grid(column=1, row=3, padx=5, pady=5, sticky="w")

    def on_change(self):
        # Triggers on any change in input
        expr = self._expr.get()
        if not expr:
            # Expression input is empty, just reset
            self.postfix.configure(text="")
            self.value.configure(text="")
            return

        errors: list[str] = []

        # Everything below is golang styled, sorry
        # Convert infix to postfix
        expr_cmds, err = convert(expr)
        if err:
            errors.append(err)

        if expr_cmds:
            # This is run even if there is error, as long as convert
            # can still parse it as best as it can
            expr_cmds_str = " ".join(expr_cmds)

            # Evauate the infix form
            expr_val, err = evaluate(expr_cmds)
            if err:
                errors.append(err)
        else:
            # We were not able to parse anything, so just reset
            expr_cmds_str = ""
            expr_val = ""

        # Update all labels
        self.errors.configure(text=", ".join(errors))
        self.postfix.configure(text=expr_cmds_str)
        self.value.configure(text=expr_val)


def main():
    """Main entry"""
    app = MainWindow()
    app.master.title("Infix-Postfix Converter")  # type: ignore
    app.master.geometry("500x125")  # type: ignore
    app.mainloop()


if __name__ == "__main__":
    main()
