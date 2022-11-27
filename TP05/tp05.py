import sys


def get_digits(num: int):
    """Returns number of digits of given number"""
    n = 0
    while num > 0:
        n += 1
        num //= 10
    return n


def pprint_table(arr: list[list[int]]):
    """Pretty print given table

    List must be of size NxN."""
    longest_len = 0
    size = len(arr)
    size_digits = get_digits(size)
    for i in range(size - 1):
        for j in range(1, size):
            longest_len = max(longest_len, get_digits(arr[i][j]))

    if size_digits > longest_len:
        longest_len = size_digits

    print("".rjust(size_digits), end="")
    print(" | ", end="")
    for i in range(size):
        print(str(i).center(longest_len), end=" ")
    print()
    print("-" * (size_digits + 2 + 2 + (1 + longest_len) * size))

    for i in range(size):
        print(str(i).center(size_digits), end=" ")
        print("| ", end="")
        for j in range(size):
            obj = str(arr[i][j])
            print(obj.rjust(longest_len), end=" ")
        print("|")


def matrix_chain_order(dims: list[int]):
    n = len(dims) - 1
    m = [[0 for _ in range(n)] for _ in range(n)]
    s = [[0 for _ in range(n)] for _ in range(n)]

    for length in range(1, n):
        for i in range(n - length):
            j = i + length
            m[i][j] = sys.maxsize

            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s


def print_multip(s: list[list[int]], i: int, j: int):
    if i == j:
        print(f"A{i+1}", end="")
    else:
        print("(", end="")
        print_multip(s, i, s[i][j])
        print(" ", end="")
        print_multip(s, s[i][j] + 1, j)
        print(")", end="")


while True:
    cmd = input()
    if cmd == "EXIT":
        break

    matrices = input().split(" ")

    valid = True
    dimensions: list[int] = []
    last_right = -1
    for matrix in matrices:
        left, right = matrix.split(",")
        left_int = int(left[1:])
        right_int = int(right[:-1])

        if last_right != left_int and last_right != -1:
            valid = False
            break

        dimensions.append(left_int)
        last_right = right_int

    if not valid:
        print("Invalid Size")
        print()
        continue

    dimensions.append(right_int)
    m, s = matrix_chain_order(dimensions)

    print("Tabel M")
    pprint_table(m)

    print("Tabel S")
    pprint_table(s)

    print(m[0][-1])
    print_multip(s, 0, len(s) - 1)
    print()
    print()