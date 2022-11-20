import math
from typing import Iterable, List, Literal, Sequence, Tuple, TypeVar, Union, cast


T = TypeVar("T")
UserData = Tuple[str, str]
MaybeUserData = Union[Tuple[None, None], UserData]
PRIME = 7


def chunk_lst(lst: Sequence[T], length: int) -> Iterable[Sequence[T]]:
    """Split a sequence into n length per item"""
    for i in range(0, len(lst), length):
        yield lst[i : i + length]


def rotate_left(x: int, n: int):
    """Rotate left from MD5 spec

    From RFC-1321's C reference code:
    #define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32-(n))))
    """
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


class MD5Hash:
    # fmt: off
    # Constants for step 4
    # Number of rotation per i
    s = [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,
    ]
    # Essentially precalculated version of floor(2^32 × abs(sin(i + 1)))
    # For i in 0 to 63
    K = [
            0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
            0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
            0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
            0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
            0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
            0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
            0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
            0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
            0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
            0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
            0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
            0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
            0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
            0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
            0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
            0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
        ]
    # fmt: on

    @classmethod
    def hash(cls, data: str):
        c = cls(data)
        c._step_one()
        c._step_two()
        c._step_four()
        return c._step_five()

    def __init__(self, data: str):
        # Step 3: Initial state, all values are little endian
        self._a = 0x67452301
        self._b = 0xEFCDAB89
        self._c = 0x98BADCFE
        self._d = 0x10325476
        self._orig_len = len(data.encode("utf-8"))
        self._message = bytearray(data.encode("utf-8"))

    def _step_one(self):
        """
        Step 1. Append Padding Bits

        The message is "padded" (extended) so that its length (in bits) is
        congruent to 448, modulo 512. That is, the message is extended so
        that it is just 64 bits shy of being a multiple of 512 bits long.
        Padding is always performed, even if the length of the message is
        already congruent to 448, modulo 512.

        Padding is performed as follows: a single "1" bit is appended to the
        message, and then "0" bits are appended so that the length in bits of
        the padded message becomes congruent to 448, modulo 512. In all, at
        least one bit and at most 512 bits are appended.
        """
        # Append 1000 0000 since we're working with bytes, it's technically
        # the same thing and is accurate when compared to the RFC's
        # reference implementation
        self._message.append(0x80)

        # Simply append 0 bytez until we are congruent to 448 modulo 512
        # 448 bits -> 56 bytes
        # 512 bits -> 64 bytes
        while len(self._message) % 64 != 56:
            self._message.append(0)

    def _step_two(self):
        """
        Step 2. Append Length

        A 64-bit representation of b (the length of the message before the
        padding bits were added) is appended to the result of the previous
        step. In the unlikely event that b is greater than 2^64, then only
        the low-order 64 bits of b are used. (These bits are appended as two
        32-bit words and appended low-order word first in accordance with the
        previous conventions.)

        At this point the resulting message (after padding with bits and with
        b) has a length that is an exact multiple of 512 bits. Equivalently,
        this message has a length that is an exact multiple of 16 (32-bit)
        words. Let M[0 ... N-1] denote the words of the resulting message,
        where N is a multiple of 16.
        """
        # Byte array is in...bytes. So multiple by 8
        len_bits = (self._orig_len * 8) & 0xFFFFFFFFFFFFFFFF  # Mod 2^64
        # Change len bits into bytes, as little endian value
        self._message += len_bits.to_bytes(8, "little")

    def _step_four(self):
        # Process per 512-bit block
        for curr_chunk in chunk_lst(self._message, 64):
            # Split 512-bit block into 16 32-bit block
            M = [int.from_bytes(chunk, "little") for chunk in chunk_lst(curr_chunk, 4)]

            A = self._a
            B = self._b
            C = self._c
            D = self._d

            for i in range(64):
                if i < 16:
                    F = (B & C) | (~B & D)
                    g = i
                elif i < 32:
                    F = (D & B) | (~D & C)
                    g = (5 * i + 1) % 16
                elif i < 48:
                    F = B ^ C ^ D
                    g = (3 * i + 5) % 16
                else:
                    F = C ^ (B | ~D)
                    g = (7 * i) % 16

                # Ensure that calculation is in uint bounds
                F = (F + A + self.K[i] + M[g]) & 0xFFFFFFFF  # mod 2^32
                A = D
                D = C
                C = B
                B = (B + rotate_left(F, self.s[i])) & 0xFFFFFFFF  # mod 2^32

            # Add values and mod by 2^32
            self._a += A
            self._b += B
            self._c += C
            self._d += D

            self._a &= 0xFFFFFFFF
            self._b &= 0xFFFFFFFF
            self._c &= 0xFFFFFFFF
            self._d &= 0xFFFFFFFF

    def _step_five(self):
        """
        Step 5. Output

        The message digest produced as output is A, B, C, D. That is, we
        begin with the low-order byte of A, and end with the high-order byte
        of D.
        """
        # Essentially putting the bytes into the following order:
        # DDDDCCCCBBBBAAAA
        result = 0
        for i, x in enumerate((self._a, self._b, self._c, self._d)):
            result |= x << (32 * i)

        # Result is in int, so change to hex bytes with still little endian
        b = result.to_bytes(16, byteorder="little")

        # Then reparse the byte as big endian to format it
        return "{:032x}".format(int.from_bytes(b, byteorder="big"))


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
                if new_datas[i][0] is None:
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
            if self._data[i][0] is None:
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


if __name__ == "__main__":
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
