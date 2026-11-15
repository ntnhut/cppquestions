---
id: polymorphism-002
topic: polymorphism
difficulty: intermediate
cpp_standard: c++17
kind: single-choice
status: verified
tags: [object-slicing, virtual-functions, references]
related: [polymorphism-001]
---

# What happens when a derived object is passed by value as its base?

```{question-meta}
```

**Starting knowledge:** Simple classes, passing by value and by reference,
inheritance, and virtual functions. This question applies when passing an object
to a function that accepts its base type.

In C++17, compare these two interfaces. Both call the same virtual member
function, but one takes a reference and the other takes a value.

```{literalinclude} ../../examples/polymorphism-002.cpp
:language: cpp
```

```{quizdown-explained}
## What does the program print?

1. [ ] `derived` followed by `derived`
1. [ ] `base` followed by `base`
1. [x] `derived` followed by `base`
1. [ ] The program does not compile because a base cannot be copied from a derived object
## Answer and explanation

**It prints `derived` followed by `base`, each on its own line.**

`by_reference` binds its `const Base&` parameter to the base subobject of the
original `Derived`. No new `Base` object is copied. The original object's
dynamic type is still `Derived`, so the
[virtual call selects its override](https://timsong-cpp.github.io/cppwp/n4659/class.virtual#2).
The reference's `const` qualification permits calling the const member function;
it does not disable virtual dispatch.

`by_value` constructs a separate `Base` parameter using `Base`'s implicit copy
constructor. It copies only the base subobject; this is called **object slicing**.
The [copy constructor copies the destination class's bases and members](https://timsong-cpp.github.io/cppwp/n4659/class.copy.ctor#14),
not an entire object of an arbitrary derived type. The parameter is a complete
`Base`, so its virtual call selects `Base::name()`.

Virtual functions preserve dynamic dispatch through references and pointers;
they do not make a by-value parameter retain a derived type. The base copy
constructor is accessible here and can bind to the derived object's base
subobject, so the program compiles.

## Interview follow-up

How would you change `by_value` if it should inspect objects polymorphically
without owning them? Give it a `const Base&` parameter, as in `by_reference`.
That avoids slicing and copying. The reference borrows the original object;
the caller must keep that object alive while the function uses it. This is a
useful interface for reading an existing object without creating a copy.
```
