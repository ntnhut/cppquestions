---
id: fundamentals-001
topic: fundamentals
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [arithmetic, integer-division, conversions]
related: [functions-002, fundamentals-002]
---

# Why does assigning an integer quotient to double lose the fraction?

```{question-meta}
```

**Starting knowledge:** Integer and floating-point types, arithmetic, and
`static_cast<double>` for converting a value to `double`.

In C++17, a metrics calculation averages seven bytes over two messages. The
message count is positive. The program prints `3`, although the intended
average is `3.5`.

```{literalinclude} ../../examples/fundamentals-001.cpp
:language: cpp
```

```{quizdown-explained}
## Which initializer preserves the fraction for these integer inputs?

1. [ ] `static_cast<double>(total_bytes / message_count)`
1. [x] `static_cast<double>(total_bytes) / message_count`
1. [ ] `total_bytes / message_count`, because the destination variable is double
## Answer and explanation

**Convert an operand before division: `static_cast<double>(total_bytes) / message_count`.**
For these inputs, the corrected program prints `3.5`.

When both operands are integers, [division discards the fractional part](https://timsong-cpp.github.io/cppwp/n4659/expr.mul#4).
The original expression computes integer three first. Storing that result in a
`double` cannot recover the discarded fraction. Casting the result of the
integer division is too late for the same reason.

Converting `total_bytes` to `double` first makes the division use floating-point
arithmetic: the [operand types determine the calculation](https://timsong-cpp.github.io/cppwp/n4659/expr.mul#2),
not the type of the variable receiving the result. In this case the calculation
is seven divided by two without integer truncation.

This distinction matters in averages, ratios, and percentages computed from
integer counts. It is not a display-formatting problem.

## Interview follow-up

What should happen if there are no messages? Handle a zero count before computing
an average, for example by reporting that no average is available. Changing the
cast does not decide what an empty input should mean for the application. The
example assumes a positive count and does not execute a zero-divisor case.
```
