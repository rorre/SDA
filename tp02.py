import tkinter as tk
from typing import Literal

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "$": 3, "(": 4, ")": 4}


class MathTokenizer:
    OPERATORS = ("+", "-", "*", "/", "$", "(", ")")

    def __init__(self, expr: str):
        self._expr = list(expr.replace(" ", ""))
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

        while valid_token:
            if self._curr_idx == len(self._expr):
                break

            curr = self._expr[self._curr_idx]
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


def parse(expr: str):
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
                    raise Exception("Unmatch parantheses")
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
            raise Exception("Unmatch parentheses")
        cmds.append(op)

    return cmds


def evaluate(cmds: list[str]):
    num_stack: list[int] = []

    for token in cmds:
        if token.isdigit():
            num_stack.append(int(token))
            continue

        try:
            second = num_stack.pop()
            first = num_stack.pop()
        except IndexError:
            raise Exception("Invalid expression")

        result = eval_math(first, second, token)
        num_stack.append(result)

    return num_stack.pop()


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

        self.infix_lbl = tk.Label(self, text="Ekspresi Infix:")
        self.postfix_lbl = tk.Label(self, text="Ekspresi Postfix:")
        self.value_lbl = tk.Label(self, text="Nilai:")

        self.infix = tk.Entry(self, textvariable=self._expr)
        self.postfix = tk.Label(self)
        self.value = tk.Label(self)

        self.infix_lbl.grid(column=0, row=0, padx=5, pady=5, sticky="e")
        self.postfix_lbl.grid(column=0, row=1, padx=5, pady=5, sticky="e")
        self.value_lbl.grid(column=0, row=2, padx=5, pady=5, sticky="e")

        self.infix.grid(column=1, row=0, padx=5, pady=5, sticky="news")
        self.postfix.grid(column=1, row=1, padx=5, pady=5, sticky="w")
        self.value.grid(column=1, row=2, padx=5, pady=5, sticky="w")

    def on_change(self):
        expr = self._expr.get()
        if not expr:
            self.postfix.configure(text="")
            self.value.configure(text="")
            return

        try:
            expr_cmds = parse(expr)
            expr_cmds_str = " ".join(expr_cmds)
            expr_val = evaluate(expr_cmds)
        except BaseException as e:
            expr_cmds_str = expr_val = str(e)

        self.postfix.configure(text=expr_cmds_str)
        self.value.configure(text=expr_val)


def main():
    app = MainWindow()
    app.master.title("Infix-Postfix Converter")  # type: ignore
    app.master.geometry("500x100")
    app.mainloop()


if __name__ == "__main__":
    main()
