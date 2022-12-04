def chk(i: int):
    f = open(f"tc/in/in{i}.txt", "r")
    d: dict[str, list[str]] = {}
    for line in f:
        cmd, *args = line.strip().split()
        if cmd not in ("ADD_MATKUL", "EDIT_MATKUL"):
            continue

        matkul = args[0]
        deps = args[1:]
        d[matkul] = deps

    vertex_count = 0
    edge_count = 0
    for v in d.values():
        vertex_count += 1
        edge_count += len(v)

    print(f"{i:>3}: {vertex_count:>4} | {edge_count}")


for i in range(101):
    chk(i)
