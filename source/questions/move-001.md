---
id: move-001
topic: move-semantics
difficulty: intermediate
cpp_standard: c++17
kind: single-choice
status: verified
tags: [const, std-move, overload-resolution]
related: [ownership-001]
---

# Why does std::move on a const object copy?

```{question-meta}
```

What does this program print?

```{literalinclude} ../../examples/move-001.cpp
:language: cpp
```

Select an answer to see feedback and read the explanation below the choices.

```{quizdown-explained}
## Which constructor initializes b?

1. [x] The copy constructor; the program prints `copy`
1. [ ] The move constructor; the program prints `move`
1. [ ] The default constructor; the program prints nothing
1. [ ] None; the program does not compile
## Answer and explanation

**The copy constructor is called, and the program prints `copy`.**
For this expression, `std::move(a)` produces an xvalue of type `const Widget`;
the returned reference type is `const Widget&&`.

The move constructor takes `Widget&&`. It cannot bind to this const object,
because that would discard `const`. The copy constructor takes `const Widget&`,
which can bind to the expression, so it is selected.

`std::move` casts its argument to an rvalue reference; it does not call a move
constructor itself or remove `const`. The default constructor initializes `a`,
but initialization of `b` requires a constructor accepting the supplied argument.
There is a viable copy constructor, so the program compiles.

## Interview follow-up

What changes if `a` is declared as `Widget a;`? The expression `std::move(a)`
can then bind to `Widget&&`, and overload resolution selects the move constructor.
```

## Go deeper

```{related-questions}
```

Continue with the [move semantics learning path](../topics/move-semantics.md).
Review [ownership and RAII](../topics/ownership.md) before implementing a
resource-owning type.

## References

- [C++ working draft: move helpers](https://eel.is/c++draft/forward)
- [C++ working draft: reference initialization](https://eel.is/c++draft/dcl.init.ref)
