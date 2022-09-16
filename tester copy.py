import subprocess

RUN_CMD = "python tp01-2.py"

f = open("output-2.txt", "w")
c = 1
for i in range(2, 11):
    for j in range(2, 11):
        inp = f"Tara\n{i} {j}"
        print("Attempting:", inp)

        p = subprocess.Popen(
            RUN_CMD.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        out, _ = p.communicate(inp.encode(), 5)
        f.write(f"{i} {j}|{out.decode()}")

        c += 1
f.close()
