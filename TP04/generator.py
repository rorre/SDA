import random
from typing import Optional
import string


def random_str(n: int):
    return "".join(random.SystemRandom().choice(string.ascii_letters) for _ in range(n))


def start(i: int):
    n = random.randint(10, 10 + 990 * int(i / 100))
    datas: dict[str, str] = {}

    user: Optional[str] = None
    f = open(f"in/{i}.txt", "w")
    for _ in range(n):
        cmds = [
            "IS_AUTHENTICATED",
            "LOGOUT",
            "INSPECT",
            "CHECK_USERNAME",
            "COUNT_USERNAME",
            "CAPACITY",
        ]

        if not user:
            cmds += ["LOGIN", "REGISTER", "UNREGISTER"]
        else:
            cmds += ["EDIT_CURRENT"]

        cmd = random.choice(cmds)
        if cmd == "LOGIN" or cmd == "REGISTER" or cmd == "UNREGISTER":
            if len(datas) != 0 and random.random() >= 0.5:
                username = random.choice(list(datas.keys()))
            else:
                username = random_str(random.randint(1, 10))

            password = random_str(random.randint(1, 10))
            actual_pw = datas.get(username)
            if actual_pw and random.random() >= 0.5:
                password = actual_pw

            print(f"{cmd} {username} {password}", file=f)

            if cmd == "REGISTER" and username not in datas:
                datas[username] = password

            if cmd == "UNREGISTER" and username in datas:
                del datas[username]

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
                    value = random_str(random.randint(1, 10))
                    orig_pw = datas[user]
                    del datas[user]
                    datas[value] = orig_pw
                    user = value
            else:
                value = random_str(random.randint(1, 10))
                datas[user] = value

            print(f"{cmd} {method} {value}", file=f)
            continue

        if cmd == "CHECK_USERNAME":
            if len(datas) != 0 and random.random() >= 0.5:
                username = random.choice(list(datas.keys()))
            else:
                username = random_str(random.randint(1, 10))

            print(f"{cmd} {username}", file=f)
            continue

        if cmd == "LOGOUT":
            user = None

        print(cmd, file=f)
    print("EXIT", file=f)
    f.close()


for i in range(100):
    start(i)
