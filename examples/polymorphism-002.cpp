#include <iostream>

struct Base {
    virtual const char* name() const { return "base"; }
    virtual ~Base() = default;
};

struct Derived : Base {
    const char* name() const override { return "derived"; }
};

void by_reference(const Base& object) {
    std::cout << object.name() << '\n';
}

void by_value(Base object) {
    std::cout << object.name() << '\n';
}

int main() {
    Derived object;
    by_reference(object);
    by_value(object);
}
