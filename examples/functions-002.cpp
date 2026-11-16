#include <iostream>
#include <vector>

int total_cost(const std::vector<int>& costs) {
    int total = 0;
    for (int cost : costs) {
        total += cost;
    }
    return total;
}

int main() {
    std::vector<int> costs{12, 8, 5};
    std::cout << total_cost(costs) << '\n';
}
