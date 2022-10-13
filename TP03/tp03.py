from typing import Callable, Dict, List, Literal, Optional, Tuple

ArrowValue = Literal["PREV", "NEXT"]


class Node:
    """Represents a node in linked list"""

    __slot__ = ("value", "previous", "next")

    def __init__(
        self,
        value: str,
        previous: Optional["Node"],
        next: Optional["Node"],
    ):
        self.value = value
        self.previous = previous
        self.next = next


class DoublyLinkedList:
    """Doubly linked list implementation"""

    __slot__ = ("head", "tail", "pointer", "size")

    def __init__(self) -> None:
        # Initialize linked list with head and t ail
        self.head = Node("_HEAD", None, None)
        self.tail = Node("_TAIL", None, None)

        # Link head and tail
        self.head.next = self.tail
        self.tail.previous = self.head

        # Set pointer and size to default
        self.pointer = self.head
        self.size = 0

    def __str__(self) -> str:
        result = ""
        pointer: Optional[Node] = self.head
        while pointer is not None:
            # Create the "bridge" between each node, as long as its
            # not the head
            if pointer != self.head:
                result += "<->"

            # Add the bracket and the value
            result += f"['{pointer.value}'"
            if self.pointer == pointer:
                # If the pointer points here, also add the mark
                result += " (P)"
            result += "]"

            # Continue with next pointer until None
            pointer = pointer.next
        return result

    def _insert_after(self, pointer: Node, value: str):
        """Function to insert a node with value after pointer"""
        # Prevent inserting after tail
        if pointer == self.tail:
            raise IndexError("Insertion out of bound error")

        # Create the node with appropriate prev and next
        new_node = Node(value, pointer, pointer.next)

        # Set next's prev to new node if defined
        if pointer.next:
            pointer.next.previous = new_node

        # Set current's next as new node and inc size
        pointer.next = new_node
        self.size += 1

    def _insert_before(self, pointer: Node, value: str):
        # Prevent inserting before head
        if pointer == self.head:
            raise IndexError("Insertion out of bound error")

        # Create the node with appropriate prev and next
        new_node = Node(value, pointer.previous, pointer)

        # Set prev's next to new node if defined
        if pointer.previous:
            pointer.previous.next = new_node

        # Set current's next as new node and inc size
        pointer.previous = new_node
        self.size += 1

    def _remove(self, pointer: Node):
        # Prevent removing head or tail
        if pointer == self.head or pointer == self.tail:
            raise ValueError("Unable to remove head or tail")

        # Set previous' next to curr next
        if pointer.previous:
            pointer.previous.next = pointer.next

        # Set next's prev to curr prev
        if pointer.next:
            pointer.next.previous = pointer.previous

        # Dec size
        self.size -= 1

    def insert_head(self, value: str):
        """Inserts a node after head"""
        self._insert_after(self.head, value)

    def insert_tail(self, value: str):
        """Inserts a node before tail"""
        self._insert_before(self.tail, value)

    def remove_head(self):
        """Removes node after the head"""
        to_remove = self.head.next
        self._remove(to_remove)  # type: ignore

        # If we were removing current pointer, shift pointer to head
        if to_remove == self.pointer:
            self.pointer = self.head

    def remove_tail(self):
        """Removes node before the tail"""
        to_remove = self.tail.previous
        self._remove(to_remove)  # type: ignore

        # If we were removing current pointer, shift pointer to tail
        if to_remove == self.pointer:
            self.pointer = self.tail

    def insert_pointer(self, arrow: ArrowValue, value: str):
        """Inserts node based on pointer and arrow"""
        if arrow == "NEXT":
            self._insert_after(self.pointer, value)
        else:
            self._insert_before(self.pointer, value)

    def remove_pointer(self, arrow: ArrowValue):
        """Removes node pointed by arrow with current pointer"""
        if arrow == "NEXT":
            # Tail will always have None as next, prevent removal
            if self.pointer == self.tail:
                raise ValueError("Tail do not have next node")

            pointer_remove = self.pointer.next
        else:
            # Head will always have None as prev, prevent removal
            if self.pointer == self.head:
                raise ValueError("Head do not have previous node")

            pointer_remove = self.pointer.previous

        self._remove(pointer_remove)  # type: ignore

    def move_pointer(self, arrow: ArrowValue, steps: int):
        """Moves pointer for steps in arrow direction"""
        # TODO: this should not happen
        steps = int(steps)

        # Run for number of steps
        for _ in range(steps):
            # Select next pointer based on arrow
            if arrow == "NEXT":
                next_pointer = self.pointer.next
            else:
                next_pointer = self.pointer.previous

            # Ensure we do not step out of bounds by checking None
            if next_pointer is None:
                raise IndexError("Steps out of bound error")
            self.pointer = next_pointer

    def is_empty(self):
        """Check if list is empty or not"""
        return self.size == 0


def validate_arrow(value: str):
    """Validates arrow value"""
    return value == "PREV" or value == "NEXT"


def validate_int(value: str):
    """Validates int value"""
    return int(value) > 0


def validate_args(cmd: str, args: List[str]):
    """Validates arguments based on cmd"""
    # Dictionary to standardize the spec for each argument
    # Value is formatted in the following pattern:
    # (num_of_args, [validator_func1, validator_func2, ..., validator_funcn])
    validators: Dict[str, Tuple[int, List[Callable]]] = {
        "INSERT_HEAD": (1, [str]),
        "REMOVE_HEAD": (0, []),
        "INSERT_TAIL": (1, [str]),
        "REMOVE_TAIL": (0, []),
        "INSERT_NODE_USING_POINTER": (2, [validate_arrow, str]),
        "REMOVE_NODE_USING_POINTER": (1, [validate_arrow]),
        "MOVE_POINTER": (2, [validate_arrow, validate_int]),
        "IS_EMPTY": (0, []),
        "SIZE": (0, []),
    }

    # Get validation spec, if none then there is no such command
    validation_data = validators.get(cmd)
    if not validation_data:
        return False

    # Check arguments length
    if len(args) != validation_data[0]:
        return False

    # For every argument, check if it's valid
    for i, validator in enumerate(validation_data[1]):
        # If any is invalid, just return False
        if not validator(args[i]):
            return False

    # All good :)
    return True


def process_cmd(dlist: DoublyLinkedList, cmd: str, args: List[str]):
    """Processes command with given args"""
    # Translation table for function to call on each command
    cmds: Dict[str, Callable] = {
        "INSERT_HEAD": dlist.insert_head,
        "REMOVE_HEAD": dlist.remove_head,
        "INSERT_TAIL": dlist.insert_tail,
        "REMOVE_TAIL": dlist.remove_tail,
        "INSERT_NODE_USING_POINTER": dlist.insert_pointer,
        "REMOVE_NODE_USING_POINTER": dlist.remove_pointer,
        "MOVE_POINTER": dlist.move_pointer,
        "IS_EMPTY": dlist.is_empty,
        "SIZE": lambda: dlist.size,
    }

    print(cmd, *args)
    if cmd == "SIZE" or cmd == "IS_EMPTY":
        # Simply print size and upper (because IS_EMPTY)
        print(f"    {cmds[cmd]()}".upper())
        return

    # Print original list
    print("    Before: ")
    print(f"    {dlist}")
    print()

    # Validate and check for syntax errors
    if not validate_args(cmd, args):
        print("    Syntax error")
        return

    # Get command function and run it
    cmd_func = cmds[cmd]
    try:
        cmd_func(*args)

        print("    After: ")
        print(f"    {dlist}")
    except Exception as e:
        # Any exception happens here, simply str() it
        # Should be guaranteed that it is our own exceptions tho
        print("    " + str(e))


def main():
    dlist = DoublyLinkedList()
    inp = input()
    while inp != "EXIT":
        cmd, *args = inp.split()
        process_cmd(dlist, cmd, args)

        print()
        inp = input()


if __name__ == "__main__":
    main()
