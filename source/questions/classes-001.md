---
id: classes-001
topic: classes
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [classes, const, member-functions, interfaces]
related: [functions-002, functions-001]
---

# Why should a read-only getter be a const member function?

```{question-meta}
```

**Starting knowledge:** Classes, member functions, private data, and const references.
The `Invoice` below stores a whole-number amount in cents. Its reader takes a
`const Invoice&`; its update method changes the ordinary integer member.

In C++17, the same invoice is read before and after a fee is added. Focus on
`const` after the getter's parameter list.

```{literalinclude} ../../examples/classes-001.cpp
:language: cpp
```

```{quizdown-explained}
## Why is amount() declared const while add_fee() is not?

1. [ ] It makes the returned integer const instead of qualifying the member function
1. [ ] It permanently prevents every caller from changing an Invoice object
1. [x] It allows read-only calls through const Invoice& and prevents changing cents_ through this getter
1. [ ] It makes amount() callable only on const objects, not on ordinary non-const objects
## Answer and explanation

**The trailing `const` makes the getter usable through a const reference and
restricts changes to the object through that member function.** The example
prints `1200`, then `1250` after the fee is added.

A [const member function](https://timsong-cpp.github.io/cppwp/n4659/class.this#1)
accesses its object through a const access path. This getter can read `cents_`
but cannot assign to that ordinary, non-mutable data member. The qualifier
belongs to the member function; it does not make the returned `int` const.

The reader's `const Invoice&` can
[call this const getter](https://timsong-cpp.github.io/cppwp/n4659/class.this#3).
Removing the trailing `const` would make that call invalid even if the getter's
body happened only to read the member. Const member functions can also be called
on non-const objects.

The original `invoice` in `main` is non-const, so its owner can call `add_fee`.
A read-only access path does not freeze the object permanently. The update
method is non-const because it deliberately changes `cents_`.

## Interview follow-up

Should the reader take `Invoice&` just to allow calling a getter that lacks
`const`? If the operation only reads the invoice, keep `const Invoice&` and mark
the getter const. Reserve a non-const reference for an operation that is allowed
to modify the invoice; the interface should make that permission clear.
```
