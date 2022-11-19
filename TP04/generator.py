import random
from typing import Optional
import string
from tp04 import is_prime


def random_str(n: int):
    return "".join(random.SystemRandom().choice(string.ascii_letters) for _ in range(n))


def start(i: int):
    n = 10 + int(990 * (i / 10))
    print(i, ":", n)
    datas: dict[str, str] = {}

    user: Optional[str] = None
    f = open(f"tc2/in/{i}.txt", "w")
    last_cmd = ""
    capacity = 11
    cnt = 0

    for _ in range(n):
        cmds = [
            "IS_AUTHENTICATED",
            "LOGOUT",
            "INSPECT",
            "CHECK_USERNAME",
            "COUNT_USERNAME",
            "CAPACITY",
            "INSPECT",
        ]

        if (cnt / capacity) >= 0.7:
            capacity *= 2
            while not is_prime(capacity):
                capacity += 1

        if not user:
            cmds += ["LOGIN", "REGISTER", "UNREGISTER"]
        else:
            cmds += ["EDIT_CURRENT"]

        cmd = random.choice(cmds)
        while cmd == last_cmd:
            cmd = random.choice(cmds)

        last_cmd = cmd
        if cmd == "INSPECT":
            for i in range(capacity):
                print(f"INSPECT {i}", file=f)
            continue

        if cmd == "LOGIN" or cmd == "REGISTER" or cmd == "UNREGISTER":
            if cmd == "UNREGISTER":
                if random.random() >= 0.25:
                    continue

            if len(datas) != 0 and random.random() >= 0.25:
                username = random.choice(list(datas.keys()))
            else:
                username = random_str(random.randint(5, 10))

            password = random_str(random.randint(5, 10))
            actual_pw = datas.get(username)
            if actual_pw and random.random() >= 0.25:
                password = actual_pw

            print(f"{cmd} {username} {password}", file=f)

            if cmd == "REGISTER" and username not in datas:
                datas[username] = password
                cnt += 1

            if cmd == "UNREGISTER" and username in datas:
                del datas[username]
                cnt -= 1
                if username == user:
                    user = None

            if cmd == "LOGIN" and datas.get(username) == password:
                user = username

            continue

        if cmd == "EDIT_CURRENT":
            if random.random() >= 0.5:
                method = "USERNAME"
            else:
                method = "PASSWORD"

            if method == "USERNAME":
                if len(datas) != 0 and random.random() >= 0.5:
                    value = random.choice(list(datas.keys()))
                else:
                    value = random_str(random.randint(5, 10))
                    orig_pw = datas[user]
                    del datas[user]
                    datas[value] = orig_pw
                    user = value
            else:
                value = random_str(random.randint(5, 10))
                datas[user] = value

            print(f"{cmd} {method} {value}", file=f)
            continue

        if cmd == "CHECK_USERNAME":
            if len(datas) != 0 and random.random() >= 0.25:
                username = random.choice(list(datas.keys()))
            else:
                username = random_str(random.randint(5, 10))

            print(f"{cmd} {username}", file=f)
            continue

        if cmd == "INSPECT":
            continue

        if cmd == "LOGOUT":
            user = None

        print(cmd, file=f)
    print("EXIT", file=f)
    f.close()


for i in range(200):
    start(i)
