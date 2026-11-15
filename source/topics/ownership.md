# Ownership and RAII

Start with the idea that an object can clean up a resource when its lifetime
ends. A file object closing its file is one example. Learn scope, construction,
and destruction before tracing smart-pointer behavior.

**Starting knowledge:** Functions, scopes, classes, constructors, and destructors.

```{toctree}
:maxdepth: 1

../questions/ownership-002
../questions/ownership-001
```

## Your learning path

1. Understand when a local object is created and leaves scope.
2. Recognize constructors and destructors as setup and cleanup operations.
3. Learn the name RAII for managing a resource through an object's lifetime.
4. Recognize who is responsible for cleanup and who merely uses a resource.
5. Try the intermediate `std::unique_ptr` example after learning its ownership rule.

Explore the other [learning paths](../learning-paths.md) to choose what to study next.
