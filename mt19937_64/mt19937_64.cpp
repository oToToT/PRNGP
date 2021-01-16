#include <cinttypes>
#include <iostream>
#include <random>

int main() {
  uint64_t seed;
  std::cin >> seed;
  std::mt19937_64 rng(seed);
  for (int i = 0; i < 1000; ++i) {
    std::cout << rng() << '\n';
  }
  return 0;
}
