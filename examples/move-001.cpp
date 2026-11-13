#include <iostream>
#include <utility>

struct Widget {
    Widget() = default;
    Widget(const Widget&) { std::cout << "copy\n"; }
    Widget(Widget&&) { std::cout << "move\n"; }
};

int main() {
    const Widget a;
    Widget b = std::move(a);
}
