from collections import defaultdict

inside: dict[str, set[str]] = defaultdict(set)
outside: dict[str, set[str]] = defaultdict(set)


class IntHeap:
    __slots__ = ("_data",)

    def __init__(self, iter: list[str]):
        self._data = iter

    def __len__(self):
        return len(self._data)

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j: int):
        parent_idx = (j - 1) >> 1  # // 2
        if j > 0 and self._data[j] < self._data[parent_idx]:
            self._swap(j, parent_idx)
            self._upheap(parent_idx)

    def _downheap(self, j: int):
        left_idx = 2 * j + 1
        if left_idx >= len(self._data):
            # Left node doesnt exist
            return

        smallest_child = left_idx

        right_idx = 2 * j + 2
        if right_idx < len(self._data):
            if self._data[right_idx] < self._data[left_idx]:
                smallest_child = right_idx

        if self._data[smallest_child] < self._data[j]:
            self._swap(j, smallest_child)
            self._downheap(smallest_child)

    def append(self, elem: str):
        self._data.append(elem)
        self._upheap(len(self._data) - 1)

    def pop(self):
        if len(self._data) == 0:
            raise IndexError("Attempting to pop an empty heap")

        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheap(0)
        return item


def add_vertex(v: str):
    inside[v] = set()
    outside[v] = set()


def add_edge(source: str, target: str):
    outside[source].add(target)
    inside[target].add(source)


def remove_edge(source: str, target: str):
    outside[source].remove(target)
    inside[target].remove(source)


def add_matkul(matkul: str, *deps: str):
    if matkul in inside:
        print(f"Matkul {matkul} sudah ada")
        return

    for dep in deps:
        if dep not in inside:
            print(f"Matkul {dep} tidak ditemukan")
            return

    add_vertex(matkul)
    for dep in deps:
        add_edge(dep, matkul)


def edit_matkul(matkul: str, *deps: str):
    if matkul not in inside:
        print(f"Matkul {matkul} tidak ditemukan")
        return

    for dep in deps:
        if dep not in inside:
            print(f"Matkul {dep} tidak ditemukan”")
            return

    for prev_dep in inside[matkul].copy():
        remove_edge(prev_dep, matkul)

    for dep in deps:
        add_edge(dep, matkul)


def print_sorted() -> None:
    state: dict[str, int] = {}
    leveled: list[IntHeap] = []

    for v in inside:
        state[v] = 0

    def visit(u: str, level: int):
        if len(leveled) < level:
            leveled.append(IntHeap([u]))
        else:
            arr = leveled[level - 1]
            arr.append(u)

        state[u] = 1

        for adj_v in outside[u]:
            if state[adj_v] == 0:
                visit(adj_v, level + 1)

        state[u] = 2

    for v in inside:
        if state[v] == 0:
            visit(v, 1)

    print(
        ", ".join(
            map(
                lambda x: ", ".join([x.pop() for _ in range(len(x))]),
                leveled,
            )
        )
    )


cmds = {
    "ADD_MATKUL": add_matkul,
    "EDIT_MATKUL": edit_matkul,
    "CETAK_URUTAN": print_sorted,
}

while True:
    cmd, *args = input().split()
    if cmd == "EXIT":
        break

    if cmd not in cmds:
        print("Perintah tidak ditemukan")
        continue

    cmds[cmd](*args)  # type: ignore
