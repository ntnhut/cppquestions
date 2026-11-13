#include <iostream>
#include <memory>

struct Resource {
    ~Resource() { std::cout << "destroy\n"; }
};

int main() {
    {
        auto owner = std::make_unique<Resource>();
    }
    std::cout << "end\n";
}
