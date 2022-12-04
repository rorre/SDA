import string
import random


def gen_word(n: int):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))


def gen_edge(i: int, j: int):
    return set(
        (i, v)
        for v in random.choices(
            list(range(0, i)),
            k=random.randint(0, i - 1),
        )
    )


def gen_tc(i: int):
    f = open(f"tc/in/in{i}.txt", "w")
    vertexes = [gen_word(10) for _ in range((i + 1) * 20)]

    for i in range(len(vertexes)):
        v = vertexes[i]
        if i == 0:
            deps = ""
        else:
            edges = gen_edge(i, len(vertexes) - 1)
            deps = " ".join(map(lambda x: vertexes[x[1]], edges))
        print(f"ADD_MATKUL {v} {deps}".strip(), file=f)
        if random.random() > 0.75:
            print("CETAK_URUTAN", file=f)

    for i in range(len(vertexes)):
        v = vertexes[i]
        if i == 0:
            deps = ""
        else:
            edges = gen_edge(i, len(vertexes) - 1)
            deps = " ".join(map(lambda x: vertexes[x[1]], edges))
        print(f"EDIT_MATKUL {v} {deps}".strip(), file=f)
        if random.random() > 0.75:
            print("CETAK_URUTAN", file=f)

    print("CETAK_URUTAN", file=f)
    print("EXIT", file=f)
    f.close()


for i in range(51):
    gen_tc(i)
