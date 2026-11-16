---
id: fundamentals-002
topic: fundamentals
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [short-circuit, pointers, null-checks]
related: [fundamentals-001, functions-001]
---

# How does a short-circuit condition guard a nullable pointer?

```{question-meta}
```

**Starting knowledge:** Pointers, `nullptr`, member access with `->`, and Boolean
conditions. A non-null pointer in this example always refers to a live `User`.

In C++17, callers may pass no user (`nullptr`), an inactive user, or an active
user. Access should be allowed only for a present, active user. The helper must
avoid reading a member through a null pointer.

```{literalinclude} ../../examples/fundamentals-002.cpp
:language: cpp
```

```{quizdown-explained}
## Which condition both implements the access rule and safely handles nullptr?

1. [x] `user != nullptr && user->active`
1. [ ] `user->active && user != nullptr`
1. [ ] `user != nullptr || user->active`
1. [ ] `(user != nullptr) & user->active`
## Answer and explanation

**Check for null first, then use `&&`.** The program prints `true false false`
for the active user, inactive user, and missing user respectively.

The [built-in logical AND operator](https://timsong-cpp.github.io/cppwp/n4659/expr.log.and#1)
evaluates its left operand first. If that operand is false, it does not evaluate
the right operand. Thus `user->active` is read only after the pointer is known
to be non-null.

Reversing the operands reads `user->active` before checking the pointer, so
it is not a valid guard. Reading that member through a null pointer has undefined
behavior; it is not guaranteed to produce false or throw an exception.

[Logical OR](https://timsong-cpp.github.io/cppwp/n4659/expr.log.or#1)
skips the right operand when the left is true. That would allow any non-null
user, even an inactive one; for null it would still try to read the member.
The single `&` is bitwise AND and does not short-circuit, so both operands are
evaluated and it does not protect the member access.

## Interview follow-up

Does a non-null check prove a pointer is safe to use? No. It does not prove the
pointed-to object is still alive. This helper's contract assumes any non-null
pointer refers to a live user; the caller must maintain that lifetime. A null
check cannot repair a dangling pointer.
```
