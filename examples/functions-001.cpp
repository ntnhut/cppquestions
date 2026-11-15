#include <iostream>

void add_bonus(int points) {
    points += 5;
}

int main() {
    int total = 10;
    add_bonus(total);
    std::cout << total << '\n';
}
