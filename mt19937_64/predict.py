#!/usr/bin/env python3
"""
std::mt19937_64 predictor
"""
from typing import List
import z3


class mt19937_64:
    def __init__(self):
        self._n = 312
        self._i = 0
        self._state = [0] * self._n

    def _untemper(self, value: int) -> int:
        solver = z3.Solver()
        original_value = z3.BitVec('vs', 64)
        modified_value = original_value

        modified_value ^= z3.LShR(modified_value, 29) & 0x5555555555555555
        modified_value ^= (modified_value << 17) & 0x71d67fffeda60000
        modified_value ^= (modified_value << 37) & 0xfff7eee000000000
        modified_value ^= z3.LShR(modified_value, 43)

        solver.add(modified_value == value)
        assert solver.check() == z3.sat
        return solver.model()[original_value].as_long()

    def from_output(self, output: List[int]) -> None:
        assert len(output) >= self._n
        output = output[:self._n]
        self._state = list(map(self._untemper, output))

    def random(self) -> int:
        j = (self._i + 1) % self._n
        mask = (1 << 31) - 1
        inv_mask = (1 << 64) - 1 - mask
        yp = (self._state[self._i] & inv_mask) | (self._state[j] & mask)
        k = (self._i + 156) % self._n
        self._state[self._i] = self._state[k] ^ (yp >> 1) ^ (
            0xb5026f5aa96619e9 * (yp & 1))
        z = self._state[self._i] ^ (
            (self._state[self._i] >> 29) & 0x5555555555555555)
        self._i = j
        z ^= (z << 17) & 0x71d67fffeda60000
        z ^= (z << 37) & 0xfff7eee000000000
        return z ^ (z >> 43)


if __name__ == '__main__':
    import subprocess
    import os
    subprocess.run(
        ["g++", "mt19937_64.cpp", "-o", "mt19937_64", "-march=native", "-O3"],
        check=True)
    proc = subprocess.Popen(["./mt19937_64"],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    out, err = proc.communicate(b"8787\n")
    
    res = out.strip().split()
    pre = mt19937_64()
    pre.from_output(list(map(int, res[:312])))
    for rand in res[312:]:
        assert(int(rand) == pre.random())

    os.remove("mt19937_64")
