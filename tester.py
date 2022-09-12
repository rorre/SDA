import subprocess

RUN_CMD = "tp01"

f = open("output.txt", "w")
c = 1
for i in range(2, 11):
    for j in range(2, 11):
        for k in ("Tara", "Kenneth"):
            inp = f"{k}\n{i} {j}"
            print("Attempting:", inp)

            p = subprocess.Popen(
                "tp01",
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
            out, _ = p.communicate(inp.encode(), 5)
            f.write(f"input{c}: {out.decode()}")

            c += 1
f.close()
