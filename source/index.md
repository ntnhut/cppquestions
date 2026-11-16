# C++ Questions

Practice C++ interview questions about code, bugs, and design decisions.

Work through free interview questions and read the complete explanations.
Choose questions whose starting knowledge matches what you have learned.
The questions assume you can already write ordinary C++ code. Each states its
prerequisites and asks you to explain a practical behavior, diagnose a bug, or
choose an API that meets a stated requirement.

## Start practicing

- [Core language and common bugs](topics/fundamentals.md): integer division and short-circuit pointer guards.
- [Functions and references](topics/functions.md): copying costs, read-only inputs, and intended mutation.
- [Containers and iterators](topics/containers.md): map lookup, vector capacity, and safe erasure.
- [Classes and const-correctness](topics/classes.md): read-only getters and update permissions.
- [Ownership and RAII](topics/ownership.md): automatic cleanup, followed by an intermediate smart-pointer example.
- [Inheritance and polymorphism](topics/polymorphism.md): optional intermediate questions for code using base-class interfaces.
- [Move semantics](topics/move-semantics.md): optional advanced practice on copying from a const object.

This is the first prototype, with thirteen questions using single-choice and typed
answers. Each question includes its C++ version, difficulty, starting knowledge,
explanation, and a follow-up to think through. Basic questions target common
junior interview concepts; intermediate questions combine them; advanced
questions examine more detailed language rules.

```{toctree}
:caption: Practice and learn
:maxdepth: 2

topics/fundamentals
topics/functions
topics/containers
topics/classes
topics/ownership
topics/polymorphism
topics/move-semantics
learning-paths
about
```
