import string
import random
import heapq

words = [
    "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    for _ in range(100)
]


def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]


def append_then_sort(arr: list[str]):
    for item in words:
        arr.append(item)
    return heapsort(arr)


def heap(arr: list[str]):
    for item in words:
        heapq.heappush(arr, item)

    return [heapq.heappop(arr) for _ in range(len(arr))]
