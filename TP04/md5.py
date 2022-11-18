from typing import Iterable, Sequence, TypeVar

T = TypeVar("T")


def chunk_lst(lst: Sequence[T], length: int) -> Iterable[Sequence[T]]:
    for i in range(0, len(lst), length):
        yield lst[i : i + length]


def rotate_left(x: int, n: int):
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


if __name__ == "__main__":
    for t, e in [
        ("", "d41d8cd98f00b204e9800998ecf8427e"),
        ("a", "0cc175b9c0f1b6a831c399e269772661"),
        ("abc", "900150983cd24fb0d6963f7d28e17f72"),
        ("message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
        ("abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
        (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "d174ab98d277d9f5a5611c2c9f419d9f",
        ),
        (
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890",
            "57edf4a22be3c955ac49da2e2107b67a",
        ),
        ("你好吗？", "bb0b6bc45375143826f72439e050743e"),
        ("お元気ですか", "2e0bd9e58d042f5234a1202cc3c7d499"),
    ]:
        print(MD5Hash.hash(t), "expected", e)
