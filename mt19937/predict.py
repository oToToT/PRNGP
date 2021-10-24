#!/usr/bin/env python3
"""
std::mt19937_64 predictor
"""
from typing import List


class mt19937:
    def __init__(self):
        self._n = 624
        self._i = 0
        self._state = [0] * self._n

    def _untemper(self, value: int) -> int:
        value ^= value >> 18
        value ^= (value << 15) & 0xefc60000
        value ^= ((value << 7) & 0x9d2c5680) ^ ((value << 14) & 0x94284000) ^ (
            (value << 21) & 0x14200000) ^ ((value << 28) & 0x10000000)
        return value ^ (value >> 11) ^ (value >> 22)

    def from_output(self, output: List[int]) -> None:
        assert len(output) >= self._n
        output = output[:self._n]
        self._state = list(map(self._untemper, output))

    def random(self) -> int:
        j = (self._i + 1) % self._n
        mask = 0x7fffffff
        inv_mask = (1 << 32) - 1 - mask
        yp = (self._state[self._i] & inv_mask) | (self._state[j] & mask)
        k = (self._i + 397) % self._n
        self._state[self._i] = self._state[k] ^ (yp >> 1) ^ (0x9908b0df *
                                                             (yp & 1))
        z = self._state[self._i] ^ (self._state[self._i] >> 11)
        self._i = j
        z ^= (z << 7) & 0x9d2c5680
        z ^= (z << 15) & 0xefc60000
        return z ^ (z >> 18)


if __name__ == '__main__':
    import subprocess
    import os
    import random
    subprocess.run(
        ["g++", "mt19937.cpp", "-o", "mt19937", "-march=native", "-O3"],
        check=True)
    proc = subprocess.Popen(["./mt19937"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    out, err = proc.communicate(
        str(random.randint(0, 2**64 - 1)).encode('ascii') + b"\n")

    res = out.strip().split()
    pre = mt19937()
    pre.from_output(list(map(int, res[:624])))
    for rand in res[624:]:
        assert (int(rand) == pre.random())

    os.remove("mt19937")
