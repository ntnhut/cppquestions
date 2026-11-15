#include <iostream>
#include <vector>

int main() {
    std::vector<int> prices{4, 7, 2};
    int total = 0;

    for (int price : prices) {
        total += price;
    }

    std::cout << total << '\n';
}
