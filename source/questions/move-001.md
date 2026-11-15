---
id: move-001
topic: move-semantics
difficulty: advanced
cpp_standard: c++17
kind: single-choice
status: verified
tags: [const, std-move, overload-resolution]
related: [ownership-001]
---

# Why does std::move on a const object copy?

```{question-meta}
```

This advanced question combines copy and move constructors, `const`, and
overload selection. Review references and ordinary object copying first.

In C++17, what does this program print?

```{literalinclude} ../../examples/move-001.cpp
:language: cpp
```

```{quizdown-explained}
## Which constructor initializes b?

1. [x] The copy constructor; the program prints `copy`
1. [ ] The move constructor; the program prints `move`
1. [ ] The default constructor; the program prints nothing
1. [ ] None; the program does not compile
## Answer and explanation

**The copy constructor is called, and the program prints `copy`.**
For this expression, [`std::move(a)`](https://timsong-cpp.github.io/cppwp/n4659/forward#5) produces an xvalue of type `const Widget`;
the returned reference type is `const Widget&&`.

The move constructor takes `Widget&&`. [It cannot bind to this const object](https://timsong-cpp.github.io/cppwp/n4659/dcl.init.ref#4),
because that would discard `const`. The copy constructor takes `const Widget&`,
which can bind to the expression, so it is selected.

`std::move` casts its argument to an rvalue reference; it does not call a move
constructor itself or remove `const`. The default constructor initializes `a`,
but initialization of `b` requires a constructor accepting the supplied argument.
There is a viable copy constructor, so the program compiles.

## Interview follow-up

What changes if `a` is declared as `Widget a;`? The expression `std::move(a)`
can then bind to both `Widget&&` and `const Widget&`.
[Overload resolution prefers the rvalue-reference binding](https://timsong-cpp.github.io/cppwp/n4659/over.ics.rank#3.2.3),
so this program prints `move`. Using `a` without `std::move` would still copy:
the expression naming `a` is an lvalue even when the object is non-const.
```
