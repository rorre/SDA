from collections import defaultdict

vertexes: dict[str, "Vertex"] = {}
inside: dict["Vertex", set["Vertex"]] = defaultdict(set)
outside: dict["Vertex", set["Vertex"]] = defaultdict(set)


class Vertex:
    __slots__ = ("name", "level", "seen")

    def __init__(self, name: str):
        self.name = name
        self.level = -1
        self.seen = False

    def __lt__(self, other: object):
        if isinstance(other, Vertex):
            return self.level < other.level or (
                self.level == other.level and self.name < other.name
            )

    def __hash__(self) -> int:
        return hash(id(self))


class VertexHeap:
    __slots__ = ("_data",)

    def __init__(self, iter: list[Vertex]):
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

    def append(self, elem: Vertex):
        self._data.append(elem)
        self._upheap(len(self._data) - 1)

    def pop(self):
        if len(self._data) == 0:
            raise IndexError("Attempting to pop an empty heap")

        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheap(0)
        return item


def add_vertex(v_name: str):
    v = Vertex(v_name)
    inside[v] = set()
    outside[v] = set()
    vertexes[v_name] = v
    return v


def add_edge(source: Vertex, target: Vertex):
    outside[source].add(target)
    inside[target].add(source)


def remove_edge(source: Vertex, target: Vertex):
    outside[source].remove(target)
    inside[target].remove(source)


def add_matkul(matkul: str, *deps: str):
    if matkul in vertexes:
        print(f"Matkul {matkul} sudah ada")
        return

    for dep in deps:
        if dep not in vertexes:
            print(f"Matkul {dep} tidak ditemukan")
            return

    v = add_vertex(matkul)
    for dep in deps:
        u = vertexes[dep]
        add_edge(u, v)


def edit_matkul(matkul: str, *deps: str):
    if matkul not in vertexes:
        print(f"Matkul {matkul} tidak ditemukan")
        return

    for dep in deps:
        if dep not in vertexes:
            print(f"Matkul {dep} tidak ditemukan")
            return

    v = vertexes[matkul]
    for u in inside[v].copy():
        remove_edge(u, v)

    for dep in deps:
        u = vertexes[dep]
        add_edge(u, v)


def print_sorted() -> None:
    leveled = VertexHeap([])
    for v in vertexes.values():
        if len(inside[v]) == 0:
            v.seen = True
            v.level = 1
            leveled.append(v)
        else:
            v.seen = False
            v.level = -1

    def visit(u: Vertex):
        u.seen = True

        max_level = 1
        for adj_v in inside[u]:
            if not adj_v.seen:
                visit(adj_v)

            max_level = max(max_level, adj_v.level)

        u.level = max_level + 1
        leveled.append(u)

    for v in vertexes.values():
        if not v.seen:
            visit(v)

    print(
        ", ".join(
            [leveled.pop().name for _ in range(len(vertexes))],
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
