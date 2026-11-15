---
id: fundamentals-001
topic: fundamentals
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [initialization, variables, integers]
related: [containers-003]
---

# Why initialize a local counter before adding to it?

```{question-meta}
```

**Starting knowledge:** `int` stores an integer. `completed += 3` adds three to
the current value of `completed`. `std::cout` prints a value.

In C++17, a task counter should start at zero. This program records three
completed tasks and prints `3`.

```{literalinclude} ../../examples/fundamentals-001.cpp
:language: cpp
```

```{quizdown-explained}
## Why give completed an initial value of zero?

1. [ ] It is optional because every local integer starts at zero
1. [x] It gives the counter a known starting value before += reads it
1. [ ] It is optional because += sets a value without reading the old one
1. [ ] It is required because declaring a local integer without an initializer never compiles
## Answer and explanation

**The initializer gives the counter a known starting value before the addition.**
`int completed = 0;` creates the variable with the value zero.
Then `completed += 3` adds three to that value, so the program prints `3`.

For this integer variable, [`+=` uses the previous value](https://timsong-cpp.github.io/cppwp/n4659/expr.ass#7):
`completed += 3` has the effect of `completed = completed + 3`.
It does not simply replace the old value with three.

Changing the declaration to `int completed;` would leave this local integer
[without an initialized value](https://timsong-cpp.github.io/cppwp/n4659/dcl.init#12).
Reading it in the addition would have undefined behavior in C++17, meaning
C++ gives no guaranteed result for that execution. A local `int` is not
automatically zero just because it is declared inside a function.

A declaration without an initializer can compile; a warning is possible, but
compilation does not establish that the later read is valid. Initialize a
counter to the value your calculation needs.

## Interview follow-up

What if two tasks were already completed before this code runs? Start with
`int completed = 2;`. Adding three more then gives five. The starting value
should describe the situation being counted; it does not always have to be zero.
```
