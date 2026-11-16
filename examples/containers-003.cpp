#include <iostream>
#include <vector>

int main() {
    std::vector<int> samples;
    samples.reserve(6);
    std::cout << samples.size() << ' ' << (samples.capacity() >= 6) << '\n';

    samples.resize(3, 0);
    std::cout << samples.size() << ' ' << samples[0] << '\n';
}
