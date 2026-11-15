---
id: polymorphism-001
topic: polymorphism
difficulty: intermediate
cpp_standard: c++17
kind: single-choice
status: verified
tags: [virtual-destructor, unique-ptr, lifetime]
related: [ownership-001, polymorphism-002]
---

# Why does deleting through a base pointer need a virtual destructor?

```{question-meta}
```

**Starting knowledge:** Inheritance, virtual functions, destructors, and
`std::unique_ptr`. This question applies when maintaining code that owns derived
objects through a base-class interface.

In C++17, this owning pointer deletes a `Derived` object through a `Base*`.
Assume allocation succeeds.

```{literalinclude} ../../examples/polymorphism-001.cpp
:language: cpp
```

```{quizdown-explained}
## What makes destruction through this owner safe?

1. [ ] `unique_ptr<Base>` remembers the type originally passed to `make_unique`
1. [x] `Base` has a virtual destructor, so deleting through `Base*` destroys the complete derived object
1. [ ] Public inheritance makes every base destructor virtual automatically
1. [ ] Deleting through a base pointer always destroys only the base part safely
## Answer and explanation

**The virtual destructor makes this deletion safe.** The program prints `derived`
followed by `base`, each on its own line.

At scope exit, `owner` uses its
[default deleter](https://timsong-cpp.github.io/cppwp/n4659/unique.ptr.dltr.dflt#3)
to delete through `Base*`.
The C++17 [delete-expression rule](https://timsong-cpp.github.io/cppwp/n4659/expr.delete#3)
requires a virtual base destructor when the static and dynamic types differ in
this way. Virtual destruction starts with `Derived::~Derived()`, then
[destroys its base subobject](https://timsong-cpp.github.io/cppwp/n4659/class.dtor#9).

The resulting owner is a `unique_ptr<Base>` with the default deleter for `Base`;
it does not retain a separate `Derived` deleter from `make_unique`.
Public inheritance permits the pointer conversion, but does not make an
otherwise non-virtual destructor virtual. Without the virtual base destructor,
this deletion would have undefined behavior, not a guarantee that only `base`
is printed. A smart pointer does not repair an invalid deletion contract.

## Interview follow-up

Does an ordinary local object need a virtual destructor for cleanup at scope
exit? No. A local object's destructor runs when its scope ends whether or not
it is virtual. The special requirement here comes from deleting a derived
object through a base pointer. Use a public virtual destructor for a base
interface that supports that kind of ownership.
```
