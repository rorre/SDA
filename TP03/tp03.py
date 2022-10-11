from typing import Callable, Dict, List, Literal, Optional, Tuple

ArrowValue = Literal["PREV", "NEXT"]


class Node:
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
    __slot__ = ("head", "tail", "pointer", "size")

    def __init__(self) -> None:
        self.head = Node("_HEAD", None, None)
        self.tail = Node("_TAIL", None, None)
        self.head.next = self.tail
        self.tail.previous = self.head

        self.pointer = self.head
        self.size = 0

    def __str__(self) -> str:
        result = ""
        pointer: Optional[Node] = self.head
        while pointer is not None:
            if pointer != self.head:
                result += "<->"
            result += f"['{pointer.value}'"
            if self.pointer == pointer:
                result += " (P)"
            result += "]"

            pointer = pointer.next
        return result

    def _insert_after(self, pointer: Node, value: str):
        if pointer == self.tail:
            raise ValueError("Insertion out of bound error")

        new_node = Node(value, pointer, pointer.next)
        if pointer.next:
            pointer.next.previous = new_node
        pointer.next = new_node
        self.size += 1

    def _insert_before(self, pointer: Node, value: str):
        if pointer == self.head:
            raise ValueError("Insertion out of bound error")

        new_node = Node(value, pointer.previous, pointer)
        if pointer.previous:
            pointer.previous.next = new_node
        pointer.previous = new_node
        self.size += 1

    def _remove(self, pointer: Node):
        if pointer == self.head or pointer == self.tail:
            raise ValueError("Unable to remove head or tail")

        if pointer.previous:
            pointer.previous.next = pointer.next

        if pointer.next:
            pointer.next.previous = pointer.previous

        self.size -= 1

    def insert_head(self, value: str):
        self._insert_after(self.head, value)

    def insert_tail(self, value: str):
        self._insert_before(self.tail, value)

    def remove_head(self):
        to_remove = self.head.next
        self._remove(to_remove)  # type: ignore
        if to_remove == self.pointer:
            self.pointer = self.head

    def remove_tail(self):
        to_remove = self.tail.previous
        self._remove(to_remove)  # type: ignore
        if to_remove == self.pointer:
            self.pointer = self.tail

    def insert_pointer(self, arrow: ArrowValue, value: str):
        if arrow == "NEXT":
            self._insert_after(self.pointer, value)
        else:
            self._insert_before(self.pointer, value)

    def remove_pointer(self, arrow: ArrowValue):
        if arrow == "NEXT":
            if self.pointer == self.tail:
                raise Exception("Tail do not have next node")

            pointer_remove = self.pointer.next
        else:
            if self.pointer == self.head:
                raise Exception("Head do not have previous node")

            pointer_remove = self.pointer.previous

        self._remove(pointer_remove)  # type: ignore

    def move_pointer(self, arrow: ArrowValue, steps: int):
        # TODO: this should not happen
        steps = int(steps)
        for _ in range(steps):
            if arrow == "NEXT":
                next_pointer = self.pointer.next
            else:
                next_pointer = self.pointer.previous

            if next_pointer is None:
                raise ValueError("Steps out of bound error")
            self.pointer = next_pointer

    def is_empty(self):
        return self.size == 0


def validate_arrow(value: str):
    return value == "PREV" or value == "NEXT"


def validate_int(value: str):
    return int(value) > 0


def validate_args(cmd: str, args: List[str]):
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
    validation_data = validators.get(cmd)
    if not validation_data:
        return False

    if len(args) != validation_data[0]:
        return False

    for i, validator in enumerate(validation_data[1]):
        if not validator(args[i]):
            return False

    return True


def process_cmd(dlist: DoublyLinkedList, cmd: str, args: List[str]):
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
        print(f"    {cmds[cmd]()}".upper())
        return

    print("    Before: ")
    print(f"    {dlist}")
    print()

    if not validate_args(cmd, args):
        print("    Syntax error")
        return

    cmd_func = cmds[cmd]
    try:
        cmd_func(*args)

        print("    After: ")
        print(f"    {dlist}")
    except Exception as e:
        print("    " + str(e))


def main():
    dlist = DoublyLinkedList()
    inp = input()
    while inp != "EXIT":
        cmd, *args = inp.split()
        process_cmd(dlist, cmd, args)

        print()
        inp = input()


main()
