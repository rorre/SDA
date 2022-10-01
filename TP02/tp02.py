import tkinter as tk
from typing import Literal, Optional

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "$": 3, "(": 4, ")": 4}

TokenType = Literal["op", "num", "invalid"]


class MathTokenizer:
    """Class to parse and tokenize math expression string.

    This is an iterator class. That means it will iterate in a for loop
    until StopIteration() is raised in __next__"""

    OPERATORS = ("+", "-", "*", "/", "$", "(", ")")

    def __init__(self, expr: str):
        self._expr = expr
        self._curr_idx = 0

    def __iter__(self):
        self._curr_idx = 0
        return self

    def __next__(self) -> tuple[str, TokenType]:
        # valid_token here means that there is still characters to process
        # in current token.
        valid_token = True
        result = ""

        # We are at the end of the string, let's stop.
        if self._curr_idx == len(self._expr):
            raise StopIteration()

        # Loop until either we reach the end of the string, or current character
        # does no longer belong to previous token.
        while self._curr_idx != len(self._expr) and valid_token:
            curr = self._expr[self._curr_idx]

            # Skip whitespace
            if curr == " ":
                self._curr_idx += 1
                continue

            # See if current character is an operator or operand
            if curr in self.OPERATORS:
                # If it is, and buffer is empty, shift to next character
                # and mark next character as new token, therefore returning current op.

                # Else, mark current character as new token, but does NOT
                # shift the pointer, instead let next iteration do the above.
                # This makes sure that current token and previous token is returned properly.
                valid_token = False
                if result == "":
                    result += curr
                    self._curr_idx += 1

            # This is an operand, simply add the character to the buffer.
            else:
                result += curr
                self._curr_idx += 1

        # If the result is empty, that means we are only processing
        # whitespaces at the end of the string, so let's just stop.
        if result == "":
            raise StopIteration()

        # Set token type whether if its an operand, operator, or invalid.
        t_type: TokenType = "invalid"
        if result in self.OPERATORS:
            t_type = "op"
        elif result.isdigit():
            t_type = "num"

        return (result, t_type)


def eval_math(left: int, right: int, op: str) -> int:
    """A wrapper to do math from given args."""
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
    """Converts infix to postfix

    Returns:
        A tuple of converted tokens in stack, and an optional error if happens.
    """
    op_stack: list[str] = []
    cmds: list[str] = []

    # Iterate through all token
    tokenizer = MathTokenizer(expr)
    for token, t_type in tokenizer:
        # Return error with whatever that has been processed
        if t_type == "invalid":
            return cmds, "Invalid character"

        # Simply append to cmds if its a number
        if t_type == "num":
            cmds.append(token)
            continue

        # Open bracket only needs to be appended to stack
        if token == "(":
            op_stack.append(token)

        elif token == ")":
            # Append all operators until we see an open paranthesis
            last_op = op_stack.pop()
            while last_op != "(":
                cmds.append(last_op)

                # We are at the end of stack, but no opening, therefore
                # it is missing from the input.
                if len(op_stack) == 0:
                    return cmds, "Missing opening parenthesis"
                last_op = op_stack.pop()

        else:
            # Append all operators in order of precedence
            while len(op_stack) != 0:
                last_op = op_stack.pop()
                if (
                    # If something takes more precendence, it'll be
                    # inserted first before current operator
                    PRECEDENCE[token] > PRECEDENCE[last_op]
                    or last_op == "("
                    # Not assosiative
                    or (last_op == token and token == "$")
                ):
                    op_stack.append(last_op)
                    break

                cmds.append(last_op)

            # All that takes precedence has been popped, now add current
            op_stack.append(token)

    # Clear all remainding operator stack
    while len(op_stack) != 0:
        op = op_stack.pop()
        # By this stage, there should never be any opening paranthesis
        # If there is, then there is an unclosed one
        if op == "(":
            return cmds, "Missing closing parenthesis"
        cmds.append(op)

    return cmds, None


def evaluate(cmds: list[str]) -> tuple[int, Optional[str]]:
    """Evaluates a queue of postfix commands to its result"""
    num_stack: list[int] = []

    for token in cmds:
        # If its a number, just append to stack
        if token.isdigit():
            num_stack.append(int(token))
            continue

        # Pop top two stacks, and evaluate
        second = num_stack.pop()
        try:
            first = num_stack.pop()
        except IndexError:
            return second, "Missing operand"

        try:
            result = eval_math(first, second, token)
        except ZeroDivisionError:
            return first, "Zero division"

        # Push the result back to stack
        num_stack.append(result)

    return num_stack.pop(), None


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
