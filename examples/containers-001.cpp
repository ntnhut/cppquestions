#include <iostream>
#include <vector>

int main() {
    std::vector<int> values{1, 2, 4, 3, 6};
    for (auto it = values.begin(); it != values.end();) {
        if (*it % 2 == 0) {
            it = values.erase(it);
        } else {
            ++it;
        }
    }

    for (int value : values) {
        std::cout << value << '\n';
    }
}
