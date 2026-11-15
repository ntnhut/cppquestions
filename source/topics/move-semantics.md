# Move semantics

Optional advanced practice. The current question combines `const`, reference
binding, and copy/move overload selection. Begin with ordinary copying and
passing arguments to functions before working through this example.

**Starting knowledge:** References, `const`, copy and move constructors, and
overload selection. A reference written with `&&` is an rvalue reference;
understanding how it binds is needed for this question.

```{toctree}
:maxdepth: 1

../questions/move-001
```

## Your learning path

1. Understand copying a value and passing it by value or by reference.
2. Learn how library objects manage their own resources.
3. Learn what moving a resource-owning object means in a concrete example.
4. Review `const` and rvalue references when you need to reason about move behavior.
5. Try the const-move question after learning copy/move overload selection.

If resource ownership is unfamiliar, begin with [ownership and RAII](ownership.md).
