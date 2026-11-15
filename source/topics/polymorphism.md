# Classes and polymorphism

Practice how inheritance affects object identity, virtual calls, and safe
destruction. Use these rules to reason about interfaces that accept base types.

**Starting knowledge:** Classes, constructors, destructors, references, and public inheritance.

```{toctree}
:maxdepth: 1

../questions/polymorphism-001
../questions/polymorphism-002
```

## Your learning path

1. Distinguish a complete derived object from its base subobject.
2. Understand virtual dispatch through base references and pointers.
3. Use a virtual destructor when supporting deletion through a base pointer.
4. Recognize slicing when copying or passing a derived object as a base value.
5. Choose interfaces that express borrowing, ownership, and copying clearly.

Review [ownership and RAII](ownership.md) for resource lifetimes and owning pointers.
