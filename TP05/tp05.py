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
    # Get the longest width taken for every single digit to be used
    longest_len = 0
    size = len(arr)
    size_digits = get_digits(size)

    # Skip last line and first col, always 0
    for i in range(size - 1):
        for j in range(1, size):
            longest_len = max(longest_len, get_digits(arr[i][j]))

    # If for some reason the size digits is longer than content
    # then just use it. We will need the header be in line with content.
    if size_digits > longest_len:
        longest_len = size_digits

    # Header
    # Empty space on top left
    print("".rjust(size_digits), end="")
    print(" | ", end="")

    # Every j centerized
    for i in range(size):
        print(str(i).center(longest_len), end=" ")
    print()

    # Separator between header and content
    # size_digits + 2 -> left empty space + " |"
    # + 2 -> Ending " |"
    # (1 + longest_len) * size -> Largest digits + " " for each number
    print("-" * (size_digits + 2 + 2 + (1 + longest_len) * size))

    # Actual content
    for i in range(size):
        # Row number + sep
        print(str(i).center(size_digits), end=" ")
        print("| ", end="")

        # Print every col, right adjusted with length of highest num
        for j in range(size):
            obj = str(arr[i][j])
            print(obj.rjust(longest_len), end=" ")
        print("|")


def matrix_chain_order(dims: list[int]):
    # Initialize m and s table
    n = len(dims) - 1
    m = [[0 for _ in range(n)] for _ in range(n)]
    s = [[0 for _ in range(n)] for _ in range(n)]

    # Technically length is from 2 to n, but since we're deadling
    # with 0 indexing, we start from 1 to n - 1
    for length in range(1, n):
        # Same here, we go from 0 to n - length - 1
        for i in range(n - length):
            j = i + length
            m[i][j] = sys.maxsize  # 2^(arch64 ? 63 : 31) - 1

            # Try every "breaking point" from i to j
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                # Check if cost is lower than any other breaking point
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


def print_multip(s: list[list[int]], i: int, j: int):
    if i == j:
        # If we are here, then we basically only have its own
        # matrix to deal with, so just print the matrix
        # NOTE: i + 1 is there because assignment uses 1 indexing
        print(f"A{i+1}", end="")
    else:
        # Recursively go from the left and right side of the
        # "breaking point" that is the most efficient
        print("(", end="")
        print_multip(s, i, s[i][j])
        print(" ", end="")
        print_multip(s, s[i][j] + 1, j)
        print(")", end="")


while True:
    cmd = input()
    if cmd == "EXIT":
        break

    # All matrices are splitted by spaces
    matrices = input().split(" ")

    # Store all initial states
    valid = True
    dimensions: list[int] = []
    last_right = -1

    for matrix in matrices:
        left, right = matrix.split(",")
        left_int = int(left[1:])
        right_int = int(right[:-1])

        # On (a, b) (c, d), ensure b == c unless its the first matrix
        # just stop if theres an invalid matrix
        if last_right != left_int and last_right != -1:
            valid = False
            break

        # Append current left for the dimensions
        dimensions.append(left_int)
        last_right = right_int

    if not valid:
        print("Invalid Size")
        print()
        continue

    # All dimensions are appended, except the last one
    # so append last matrix's right.
    # NOTE: Will never error as long as there is at least one matrix
    dimensions.append(right_int)

    # Run matrix chain order and retrieve m and s
    m, s = matrix_chain_order(dimensions)

    # print("Tabel M")
    # pprint_table(m)

    # print("Tabel S")
    # pprint_table(s)

    # Print most optimized, which where i = 0 and j = n - 1
    print(m[0][-1])
    print_multip(s, 0, len(s) - 1)
    print()
    print()
