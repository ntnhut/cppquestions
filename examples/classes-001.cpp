#include <iostream>

class Invoice {
public:
    Invoice(int cents) : cents_(cents) {}

    int amount() const { return cents_; }
    void add_fee(int fee) { cents_ += fee; }

private:
    int cents_;
};

void print_amount(const Invoice& invoice) {
    std::cout << invoice.amount() << '\n';
}

int main() {
    Invoice invoice(1200);
    print_amount(invoice);
    invoice.add_fee(50);
    print_amount(invoice);
}
