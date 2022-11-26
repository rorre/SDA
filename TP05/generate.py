import random

f = open("tc.txt", "w")

i = 2
prev_invalid = False
while i <= 200:
    f.write(f"{i}\n")

    matrices: list[tuple[int, int]] = []
    right = -1
    has_invalid = False
    for _ in range(i):
        if prev_invalid:
            valid = True
        else:
            valid = random.random() >= 0.05

        if not valid:
            has_invalid = True

        if right == -1 or not valid:
            left = random.randint(1, 100)
        else:
            left = right

        right = random.randint(1, 100)
        matrices.append((left, right))

    if has_invalid:
        prev_invalid = True
    else:
        prev_invalid = False
        i += 1

    to_write = ""
    for matrix in matrices:
        to_write += " "
        to_write += "("
        to_write += ",".join(map(str, matrix))
        to_write += ")"
    print(to_write)
    f.write(to_write.strip())
    f.write("\n")

f.close()
