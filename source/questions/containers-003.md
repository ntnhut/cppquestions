---
id: containers-003
topic: containers
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [vector, range-for, loops]
related: [fundamentals-001, containers-002]
---

# How does a range-based loop read a vector's values?

```{question-meta}
```

**Starting knowledge:** Integer variables, loops, and `+=` for addition.
A `std::vector<int>` stores a sequence of integers; here its values are `4`,
`7`, and `2`. The variable `total` starts at zero.

In C++17, this program adds a list of whole-number prices. Assume allocation
succeeds.

```{literalinclude} ../../examples/containers-003.cpp
:language: cpp
```

```{quizdown-explained}
## Which values does the loop add to total?

1. [ ] The positions `0`, `1`, and `2`
1. [ ] The number of elements, `3`, once
1. [ ] Only `2`, the last value
1. [x] Each stored value once: `4`, `7`, and `2`
## Answer and explanation

**It adds `4`, then `7`, then `2`, so the program prints `13`.**

In [`for (int price : prices)`](https://timsong-cpp.github.io/cppwp/n4659/stmt.ranged#1),
each iteration takes the next element's value as `price` and executes the body.
The loop runs three times for this vector. It reads the stored prices, rather
than their positions or the number of elements.

`total += price` adds the current price to the running total. The total becomes
four, then eleven, then thirteen. The loop processes all three values, so the
last value is only the final addition.

A range-based loop is useful when you want to read every item without managing
an index yourself. This loop leaves the values in `prices` unchanged.

## Interview follow-up

What would happen with an empty vector? The body would run zero times, so
`total` would keep its initial value of zero and the program would print `0`.
The same loop handles both an empty list and a list containing prices.
```
