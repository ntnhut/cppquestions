# Move semantics

Understand when an operation copies, when it moves, and why calling `std::move`
does not itself transfer any resources.

**Starting knowledge:** References, `const`, constructors, and overload resolution.

```{toctree}
:maxdepth: 1

../questions/move-001
```

## Your learning path

1. Review lvalue references, rvalue references, and `const`.
2. Distinguish lvalues, xvalues, and prvalues.
3. Learn how copy and move overloads are selected.
4. Explore moved-from objects and resource-owning types.
5. Apply move semantics in containers and interfaces.

If resource ownership is unfamiliar, begin with [ownership and RAII](ownership.md).
