#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> counts{{"ready", 3}};
    auto found = counts.find("missing");
    std::cout << (found == counts.end()) << ' ' << counts.size() << '\n';

    int value = counts["missing"];
    std::cout << value << ' ' << counts.size() << '\n';
}
