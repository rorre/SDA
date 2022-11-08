import hashlib
from typing import List, Literal, Tuple, Optional, Union, cast
import math

UserData = Tuple[str, str]
MaybeUserData = Union[Tuple[None, None], UserData]
PRIME = 7


def username_hashcode(uname: str) -> int:
    total = 0
    for char in uname:
        total += ord(char)
    return total


def get_row_idx(username: str, table_size: int):
    key = username_hashcode(username)
    base_idx = key % table_size
    i = base_idx
    hkey = PRIME - (key % PRIME)
    while i < table_size:
        yield i
        i += hkey


def is_prime(n: int) -> bool:
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def hash_str(data: str) -> str:
    h = hashlib.md5()
    h.update(data.encode())
    return h.hexdigest()


class AuthTable:
    LOAD_FACTOR = 0.7

    def __init__(self) -> None:
        self._data: List[MaybeUserData] = [(None, None) for _ in range(11)]
        self._rows = 11
        self._capacity = 0

    def _expand_table(self):
        orig_row = self._rows
        self._rows *= 2
        while True:
            if is_prime(self._rows):
                break

            self._rows += 1

        for _ in range(self._rows - orig_row):
            self._data.append((None, None))

    def _find_username_idx(self, username: str) -> int:
        for i in get_row_idx(username, self._rows):
            current_data = self._data[i]
            if current_data[0] == username:
                return i

        raise KeyError()

    def get(self, username: str) -> UserData:
        idx = self._find_username_idx(username)
        return self._data[idx]  # type: ignore

    def update(self, username: str, password: str):
        pw_hashed = hash_str(password)
        idx = self._find_username_idx(username)
        self._data[idx] = (username, pw_hashed)

    def delete(self, username: str):
        idx = self._find_username_idx(username)
        self._data[idx] = (None, None)
        self._capacity -= 1

    def create(self, username: str, password: str, hashed: bool = False):
        try:
            self.get(username)
            raise Exception("Username already exist")
        except KeyError:
            pass

        self._capacity += 1
        if not hashed:
            pw_hashed = hash_str(password)
        else:
            pw_hashed = password

        for i in get_row_idx(username, self._rows):
            if self._data[i][0] == None:
                self._data[i] = (username, pw_hashed)
                break

        if self._capacity / self._rows > 0.7:
            self._expand_table()
        return self._data[i]


current_user: MaybeUserData = (None, None)
user_data = AuthTable()


def register(username: str, password: str):
    try:
        user_data.create(username, password)
        return "Register Successful"
    except Exception as e:
        return "Username Already Exist"


def login(username: str, password: str):
    global current_user
    try:
        user = user_data.get(username)
    except KeyError:
        return "Username Not Found"

    pw_hashed = hash_str(password)
    if pw_hashed != user[1]:
        return "Incorrect Password"

    current_user = user
    return "Login Successful"


def edit_current(mode: Literal["USERNAME", "PASSWORD"], value: str):
    global current_user
    current_user = cast(UserData, current_user)

    if mode == "PASSWORD":
        user_data.update(current_user[0], value)
        return "Your Account Has Been Updated"

    try:
        user_data.get(value)
        return "Username Already Exist"
    except KeyError:
        pass

    user_data.delete(current_user[0])
    user_data.create(value, current_user[1], hashed=True)
    current_user = (value, current_user[1])
    return "Your Account Has Been Updated"


def is_authenticated():
    if current_user != (None, None):
        return " ".join(current_user)
    else:
        return "Please Login"


def unregister(username: str, password: str):
    pw_hashed = hash_str(password)
    try:
        user = user_data.get(username)
    except KeyError:
        return "Username Not Found"

    if user[1] != pw_hashed:
        return "Incorrect Password"

    user_data.delete(username)
    return "Your Account Has Been Deleted"


def logout():
    global current_user
    if current_user == (None, None):
        return "You Have Not Been Logged In"

    current_user = (None, None)
    return "You Have Been Logged Out"


def inspect(row: str):
    int_row = int(row)
    user = user_data._data[int_row]
    if user != (None, None):
        return " ".join(user)
    else:
        return "Row Is Empty"


def check_username(username: str):
    try:
        user_data.get(username)
        return "Username Is Registered"
    except KeyError:
        return "Username Not Found"


def count_username():
    return str(user_data._capacity)


def capacity():
    return str(user_data._rows)


while True:
    cmd, *args = input().split()
    if cmd == "EXIT":
        break

    cmds = {
        "REGISTER": register,
        "LOGIN": login,
        "EDIT_CURRENT": edit_current,
        "IS_AUTHENTICATED": is_authenticated,
        "UNREGISTER": unregister,
        "LOGOUT": logout,
        "INSPECT": inspect,
        "CHECK_USERNAME": check_username,
        "COUNT_USERNAME": count_username,
        "CAPACITY": capacity,
    }
    print(cmds[cmd](*args))
