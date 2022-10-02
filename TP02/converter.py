from typing import Optional

from tokenizer import MathTokenizer

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "$": 3, "(": 4, ")": 4}


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
            # Check if stack is empty or not
            if len(op_stack) == 0:
                return cmds, "Missing opening parenthesis"

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
        try:
            second = num_stack.pop()
        except IndexError:
            return 0, "Missing operand"

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

    # 1 karena seharusnya hasil akhir berada di stack
    if len(num_stack) != 1:
        return num_stack.pop(), "Missing operator"

    return num_stack.pop(), None
