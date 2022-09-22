import tkinter as tk
from typing import Literal, Optional

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "$": 3, "(": 4, ")": 4}


class MathTokenizer:
    OPERATORS = ("+", "-", "*", "/", "$", "(", ")")

    def __init__(self, expr: str):
        self._expr = expr
        self._curr_idx = 0

    def __iter__(self):
        self._curr_idx = 0
        return self

    def __next__(self):
        return self.next_token()

    def next_token(self) -> tuple[str, Literal["op", "num"]]:
        valid_token = True
        result = ""
        if self._curr_idx == len(self._expr):
            raise StopIteration()

        while self._curr_idx != len(self._expr) and valid_token:
            curr = self._expr[self._curr_idx]
            if curr == " ":
                self._curr_idx += 1
                continue

            if curr in self.OPERATORS:
                if result == "":
                    result += curr
                    self._curr_idx += 1

                valid_token = False
            else:
                result += curr
                self._curr_idx += 1

        return (result, "op" if result in self.OPERATORS else "num")


def eval_math(left: int, right: int, op: str):
    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op == "*":
        return left * right
    elif op == "/":
        return left // right
    else:
        return left**right


def convert(expr: str) -> tuple[list[str], Optional[str]]:
    op_stack: list[str] = []
    cmds: list[str] = []

    tokenizer = MathTokenizer(expr)
    for token, t_type in tokenizer:
        if t_type == "num":
            cmds.append(token)
            continue

        if token == "(":
            op_stack.append(token)

        elif token == ")":
            last_op = op_stack.pop()
            while last_op != "(":
                cmds.append(last_op)
                if len(op_stack) == 0:
                    return cmds, "Missing opening parenthesis"
                last_op = op_stack.pop()

        else:
            while len(op_stack) != 0:
                last_op = op_stack.pop()
                if (
                    PRECEDENCE[token] > PRECEDENCE[last_op]
                    or last_op == "("
                    # Not assosiative
                    or (last_op == token and token == "$")
                ):
                    op_stack.append(last_op)
                    break

                cmds.append(last_op)

            op_stack.append(token)

    while len(op_stack) != 0:
        op = op_stack.pop()
        if op == "(":
            return cmds, "Missing closing parenthesis"
        cmds.append(op)

    return cmds, None


def evaluate(cmds: list[str]) -> tuple[int, Optional[str]]:
    num_stack: list[int] = []

    for token in cmds:
        if token.isdigit():
            num_stack.append(int(token))
            continue

        second = num_stack.pop()
        try:
            first = num_stack.pop()
        except IndexError:
            return second, "Missing operand"

        result = eval_math(first, second, token)
        num_stack.append(result)

    return num_stack.pop(), None


class BulletLabel(tk.Label):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        text = kwargs.pop("text", "")
        kwargs["text"] = self.bulletise(text)

    def bulletise(self, text):
        if len(text) == 0:  # no text so no bullets
            return ""
        lines = text.split("\n")
        parts = []
        for line in lines:  # for each line
            parts.extend(
                ["\u2022", line, "\n"]
            )  # prepend bullet and re append newline removed by split
        return "".join(parts)

    def configure(self, *args, **kwargs):
        text = kwargs.pop("text", "")
        kwargs["text"] = self.bulletise(text)
        super().configure(*args, **kwargs)


class MainWindow(tk.Frame):
    def __init__(self, master: tk.Misc = None):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure("all", weight=1)

        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        self._expr = tk.StringVar(self)
        self._expr.trace("w", lambda _, __, ___: self.on_change())

        self.infix_lbl = tk.Label(self, text="Infix Expression:")
        self.postfix_lbl = tk.Label(self, text="Postfix Expression:")
        self.value_lbl = tk.Label(self, text="Value:")
        self.error_lbl = tk.Label(self, text="Errors:")

        self.infix = tk.Entry(self, textvariable=self._expr)
        self.postfix = tk.Label(self)
        self.value = tk.Label(self)
        self.errors = BulletLabel(self)

        self.infix_lbl.grid(column=0, row=0, padx=5, pady=5, sticky="e")
        self.postfix_lbl.grid(column=0, row=1, padx=5, pady=5, sticky="e")
        self.value_lbl.grid(column=0, row=2, padx=5, pady=5, sticky="e")
        self.error_lbl.grid(column=0, row=3, padx=5, pady=5, sticky="e")

        self.infix.grid(column=1, row=0, padx=5, pady=5, sticky="news")
        self.postfix.grid(column=1, row=1, padx=5, pady=5, sticky="w")
        self.value.grid(column=1, row=2, padx=5, pady=5, sticky="w")
        self.errors.grid(column=1, row=3, padx=5, pady=5, sticky="w")

    def on_change(self):
        expr = self._expr.get()
        if not expr:
            self.postfix.configure(text="")
            self.value.configure(text="")
            return

        errors: list[str] = []

        expr_cmds, err = convert(expr)
        if err:
            errors.append(err)

        expr_cmds_str = " ".join(expr_cmds)

        expr_val, err = evaluate(expr_cmds)
        if err:
            errors.append(err)

        print(errors)
        self.errors.configure(text="\n".join(errors))

        self.postfix.configure(text=expr_cmds_str)
        self.value.configure(text=expr_val)


def main():
    app = MainWindow()
    app.master.title("Infix-Postfix Converter")  # type: ignore
    app.master.geometry("500x100")
    app.mainloop()


if __name__ == "__main__":
    main()
