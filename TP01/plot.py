import math

import matplotlib.pyplot as plt

fname = "output-2.txt"

nums: list[int] = []
with open(fname, "r") as f:
    for line in f:
        data = int(line.split()[-1])
        nums.append(data)

maxnum = max(nums)
maxpow = math.ceil(math.log(maxnum, 5))

arr = [0] * (maxpow - 1)
for num in nums:
    power = math.ceil(math.log(num, 5))
    arr[power - 2] += 1

x = []
for i in range(maxpow - 1):
    x.append(f"<= 5^{i+2}")

plt.bar(x, arr)
plt.show()
