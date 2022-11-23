const S: [u8; 64] = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9,
    14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15,
    21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
];

const K: [u32; 64] = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
];

struct MD5Hash {
    message_len: u32,
    message: Vec<u8>,
    a: u32,
    b: u32,
    c: u32,
    d: u32,
}

impl MD5Hash {
    fn new(message: Vec<u8>, message_len: u32) -> Self {
        MD5Hash {
            message,
            message_len,
            a: 0x67452301,
            b: 0xEFCDAB89,
            c: 0x98BADCFE,
            d: 0x10325476,
        }
    }

    fn step_one(&mut self) {
        self.message.push(0x80);

        while self.message.len() % 64 != 56 {
            self.message.push(0x00);
        }
    }

    fn step_two(&mut self) {
        let len_in_bits: u64 = (self.message_len * 8).into();
        let len_bits = len_in_bits & 0xFFFFFFFFFFFFFFFF;
        self.message.extend(&len_in_bits.to_le_bytes());
    }

    fn step_four(&mut self) {
        for chunk in self.message.chunks(64) {
            let mut m: [u32; 16] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            for (i, block) in chunk.chunks(4).enumerate() {
                let mut num: u32 = 0u32;
                for n in 0..=3 {
                    let mut second_num: u32 = block[n].into();
                    second_num = second_num << (8 * (n - 4));
                    num = num | second_num;
                }
                m[i] = num;

                let mut A = self.a;
                let mut B = self.b;
                let mut C = self.c;
                let mut D = self.d;

                let mut F: u32 = 0;
                let mut g: u32 = 0;
                for i in 0..64 {
                    if i < 16 {
                        F = (B & C) | (!B & D);
                        g = i;
                    } else if i < 32 {
                        F = (D & B) | (!D & C);
                        g = (5 * i + 1) % 16;
                    } else if i < 48 {
                        F = B ^ C ^ D;
                        g = (3 * i + 5) % 16;
                    } else {
                        F = C ^ (B | !D);
                        g = (7 * i) % 16;
                    }

                    F = (F + A + K[i as usize] + m[g as usize]) & 0xFFFFFFFF;
                    A = D;
                    D = C;
                    C = B;
                    B = (B + rotate_left(F, S[i as usize])) & 0xFFFFFFFF;
                }

                self.a += A;
                self.b += B;
                self.c += C;
                self.d += D;

                self.a = self.a & 0xFFFFFFFF;
                self.b = self.b & 0xFFFFFFFF;
                self.c = self.c & 0xFFFFFFFF;
                self.d = self.d & 0xFFFFFFFF;
            }
        }
    }
}

fn rotate_left(x: u32, n: u8) -> u32 {
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF;
}

fn main() {
    println!("Hello, world!");
}
