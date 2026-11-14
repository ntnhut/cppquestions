# Ownership and RAII

How long does a resource live, and who releases it? Practice reasoning about
ownership before choosing between raw pointers and smart pointers.

**Starting knowledge:** Functions, scopes, classes, constructors, and destructors.

```{toctree}
:maxdepth: 1

../questions/ownership-001
../questions/ownership-002
```

## Your learning path

1. Understand automatic storage duration and object lifetime.
2. Use constructors and destructors to manage resources (RAII).
3. Express exclusive ownership with `std::unique_ptr`.
4. Distinguish ownership from borrowing through references or raw pointers.
5. Study shared ownership and exception-safe resource handling.

Read the [course plans](../learning-paths.md) for how deeper study will fit together.
