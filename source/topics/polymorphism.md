# Inheritance and polymorphism

Optional intermediate practice for code that uses base-class interfaces.
Start with ordinary classes, constructors, member functions, and composition
before studying inheritance. The questions here assume you have already learned
how virtual functions select an implementation through a base reference.

**Starting knowledge:** Classes, value/reference parameters, public inheritance,
and virtual functions. The destruction example also requires `std::unique_ptr`.

```{toctree}
:maxdepth: 1

../questions/polymorphism-002
../questions/polymorphism-001
```

## Your learning path

1. Use simple classes and objects without inheritance.
2. Learn composition: an object can contain other objects as members.
3. Learn base and derived classes when an interface needs different implementations.
4. Review virtual calls through references before trying the slicing question.
5. Study virtual destruction when owning objects through a base pointer.

Review [ownership and RAII](ownership.md) for resource lifetimes and owning pointers.
