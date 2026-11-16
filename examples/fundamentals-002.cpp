#include <iostream>

struct User {
    bool active;
};

bool can_login(const User* user) {
    return user != nullptr && user->active;
}

int main() {
    User active{true};
    User inactive{false};
    std::cout << std::boolalpha
              << can_login(&active) << ' '
              << can_login(&inactive) << ' '
              << can_login(nullptr) << '\n';
}
