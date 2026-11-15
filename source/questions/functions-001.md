---
id: functions-001
topic: functions
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [functions, parameters, references]
related: [fundamentals-001, containers-003]
---

# How can a function update the caller's integer?

```{question-meta}
```

**Starting knowledge:** Calling functions with integer arguments and using `+=`
to add to a variable. A parameter is the name declared inside the function's
parentheses. `void` means the function returns no value.

In C++17, `add_bonus` is intended to add five points to the caller's `total`.
The version below prints `10`, so it has not updated that variable.

```{literalinclude} ../../examples/functions-001.cpp
:language: cpp
```

```{quizdown-explained}
## What change makes add_bonus update the caller's total?

1. [ ] Rename the parameter from `points` to `total`
1. [ ] Print `points` inside the function instead of printing `total` in main
1. [x] Change the parameter from `int points` to `int& points`
1. [ ] Change the initial value of `total` from `10` to `0`
## Answer and explanation

**Use `int& points`.** The `&` makes the parameter a reference: another name for
the caller's integer. With that change, `points += 5` updates `total`, and the
program prints `15`. The call stays `add_bonus(total)`.

In the original function, `int points` is a separate integer
[initialized from the argument](https://timsong-cpp.github.io/cppwp/n4659/expr.call#4).
It starts at ten, becomes fifteen inside the function, and does not change
`total`. This is passing by value.

With the reference parameter, `points` refers to `total`, so
[assigning through it changes that same integer](https://timsong-cpp.github.io/cppwp/n4659/dcl.init.ref#2).
This is passing by reference. It is useful when changing the caller's variable
is the function's intended job.

Renaming a value parameter does not make it refer to the caller's variable.
Printing `points` inside the original function would display its local value
of fifteen, but would still leave `total` at ten. Changing `total`'s starting
value also does not change how the argument is passed.

## Interview follow-up

Should every integer parameter be a reference? No. Pass an integer by value
when the function should work with its own value without changing the caller's
variable. Use `int&` when updating that variable is part of the function's job.
Choose according to the behavior the caller expects.
```
