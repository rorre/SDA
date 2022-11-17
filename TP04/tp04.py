from typing import List, Literal, Tuple, Union, cast
import math
from md5 import MD5Hash

UserData = Tuple[str, str]
MaybeUserData = Union[Tuple[None, None], UserData]
PRIME = 7


class AlreadyExist(Exception):
    pass


def username_hashcode(uname: str) -> int:
    """Calculates hashcode of given username.

    Assumes that the sum of username hash does NOT exceed 2^32."""
    total = 0
    for char in uname:
        total += ord(char)
    return total


def get_row_idx(username: str, table_size: int):
    """Finds all possible combination of rows"""
    # Calculate the hash code
    key = username_hashcode(username)
    # From h(key) = key % table_size
    base_idx = key % table_size

    # Double hashing here
    # h'(key) is PRIME - (h(key) % PRIME)
    # This is essentially h'(key) + f(1)
    i = base_idx
    hkey = PRIME - (key % PRIME)

    # Since new idx is h'(key) + f(i) for consecutive i (1, 2, ...)
    # We simply just do iteration for max of table_size
    # table_size is set as max as at that point we are guaranteed that
    # we ahve gone through every single idx of the table
    for _ in range(table_size):
        yield i

        # Increment by hkey, same as incrementing i in f(i)
        i += hkey

        # Circle thru the hash table
        i = i % table_size


def is_prime(n: int) -> bool:
    # Prime table for every number from 2 to n + 1
    # Mark every single prime as True
    primes = [True for _ in range(n + 1)]
    for i in range(2, int(math.sqrt(n)) + 1):
        if primes[i]:
            # If this is prime, then mark all of its multip as not prime
            # Starts at i * i because it is guaranteed that
            # i * x where x < i is already marked before, due to the fact
            # that x must be either a prime or a multiplication of other prime
            for j in range(i * i, n + 1, i):
                primes[j] = False

    # Last element of the table is the number itself
    return primes[-1]


def hash_str(data: str) -> str:
    """Hashes given string with MD5"""
    return MD5Hash.hash(data)


class AuthTable:
    LOAD_FACTOR = 0.7

    def __init__(self) -> None:
        # Initialize all data with empty and initial states
        self._data: List[MaybeUserData] = [(None, None) for _ in range(11)]
        self._rows = 11  # Or capacity
        self._load = 0

    def _expand_table(self):
        """Expands table into capacity of
        next prime that is 2 times of current rows."""
        self._rows *= 2

        # Simply iterate through every single integer after rows
        while True:
            if is_prime(self._rows):
                break

            self._rows += 1

        # Initialize a new array to move all data to new one
        new_datas: List[MaybeUserData] = [(None, None)] * self._rows
        for data in self._data:
            # Checks if row is empty
            if data[0] is None:
                continue

            # Move data to new place if row is not empty
            username, pw_hashed = data
            for i in get_row_idx(username, self._rows):
                # Only fill row if there is no user residing in it
                if new_datas[i][0] is not None:
                    new_datas[i] = (username, pw_hashed)
                    break

        # Set hash data to new array
        self._data = new_datas

    def _find_username_idx(self, username: str) -> int:
        """Find given username's hash array index"""
        # Iterate through all possible rows for username
        for i in get_row_idx(username, self._rows):
            current_data = self._data[i]
            if current_data[0] == username:
                return i

        # Username not found, just throw error
        raise KeyError()

    def get(self, username: str) -> UserData:
        """Get user data"""
        idx = self._find_username_idx(username)
        return self._data[idx]  # type: ignore

    def update(self, username: str, password: str):
        """Updates user data"""
        pw_hashed = hash_str(password)
        idx = self._find_username_idx(username)

        # Simply replaces row data with new one
        self._data[idx] = (username, pw_hashed)

    def delete(self, username: str):
        """Deletes existing user data"""
        idx = self._find_username_idx(username)
        self._data[idx] = (None, None)
        self._load -= 1

    def create(self, username: str, password: str, hashed: bool = False):
        """Creates a user in user table"""
        try:
            # Check if user already exists
            self.get(username)
            raise AlreadyExist("Username already exist")
        except KeyError:
            # Will only ever happen if uname doesnt exist
            pass

        # Increment load and hash the password
        self._load += 1
        if not hashed:
            pw_hashed = hash_str(password)
        else:
            # Only ever used for renaming username
            pw_hashed = password

        # Insert data in row where it is possible
        for i in get_row_idx(username, self._rows):
            if self._data[i][0] is not None:
                self._data[i] = (username, pw_hashed)
                break

        # Expand table if we're already at threshold
        if self._load / self._rows >= self.LOAD_FACTOR:
            self._expand_table()

        return self._data[i]


# Set application initial state
current_user: MaybeUserData = (None, None)
user_data = AuthTable()


def register(username: str, password: str):
    """Registers a user with given username or password"""
    try:
        user_data.create(username, password)
        return "Register Successful"
    except AlreadyExist:
        return "Username Already Exist"


def login(username: str, password: str):
    global current_user

    # Find user from hash table
    try:
        user = user_data.get(username)
    except KeyError:
        return "Username Not Found"

    # Then hash given login password
    pw_hashed = hash_str(password)
    if pw_hashed != user[1]:
        return "Incorrect Password"

    # All good, set current user
    current_user = user
    return "Login Successful"


def edit_current(mode: Literal["USERNAME", "PASSWORD"], value: str):
    global current_user
    current_user = cast(UserData, current_user)

    # Check current mode
    if mode == "PASSWORD":
        # If password, just update new data and revalidate current_user
        user_data.update(current_user[0], value)
        current_user = user_data.get(current_user[0])
        return "Your Account Has Been Updated"

    # Else is username, check if already exists
    try:
        user_data.get(value)
        return "Username Already Exist"
    except KeyError:
        pass

    # If not, simply remove and recreate user with new usernamme
    # using hashed=True so that hashtable doesnt rehash the already
    # hashed value
    user_data.delete(current_user[0])
    user_data.create(value, current_user[1], hashed=True)

    # Update current user data
    current_user = (value, current_user[1])
    return "Your Account Has Been Updated"


def is_authenticated():
    if current_user != (None, None):
        return " ".join(current_user)
    else:
        return "Please Login"


def unregister(username: str, password: str):
    # Check for user existence
    try:
        user = user_data.get(username)
    except KeyError:
        return "Username Not Found"

    # Check for password validity
    pw_hashed = hash_str(password)
    if user[1] != pw_hashed:
        return "Incorrect Password"

    # Delete if all checks are OK
    user_data.delete(username)
    return "Your Account Has Been Deleted"


def logout():
    global current_user
    if current_user == (None, None):
        return "You Have Not Been Logged In"

    # Simply mark current_user as None to log out
    current_user = (None, None)
    return "You Have Been Logged Out"


def inspect(row: str):
    # Inspect data row by getting from array

    int_row = int(row)
    user = user_data._data[int_row]
    if user != (None, None):
        return " ".join(user)  # type: ignore
    else:
        return "Row Is Empty"


def check_username(username: str):
    try:
        user_data.get(username)
        return "Username Is Registered"
    except KeyError:
        # Will only occur if not found
        return "Username Not Found"


def count_username():
    return str(user_data._load)


def capacity():
    return str(user_data._rows)


while True:
    # Split cmd and its args
    cmd, *args = input().split()
    if cmd == "EXIT":
        break

    # Command mapping, all cmd will always return string
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
    # Run the command and print the string result
    print(cmds[cmd](*args))  # type: ignore
