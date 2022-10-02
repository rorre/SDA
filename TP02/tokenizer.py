from typing import Literal


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
