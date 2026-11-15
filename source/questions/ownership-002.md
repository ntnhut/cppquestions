---
id: ownership-002
topic: ownership
difficulty: basic
cpp_standard: c++17
kind: typed-answer
status: verified
tags: [raii, lifetime, resource-management]
related: [ownership-001]
answer_label: "Resource-management idiom (four-letter acronym)"
accepted_answers: [RAII]
answer_normalization: trim-case-insensitive
---

# What idiom ties resource ownership to an object's lifetime?

```{question-meta}
```

**Starting knowledge:** An object can acquire a resource when constructed and
release it in its destructor. This question checks the name for that pattern.

In C++17, an object owns an open file handle. Successful construction establishes
ownership, and the destructor closes the handle when the object is destroyed.
Assume normal scope exit or exception unwinding, rather than abrupt program
termination.

```{typed-answer}
## What is the four-letter acronym for this resource-management idiom?

## Answer and explanation

**[RAII](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii)**,
short for **Resource Acquisition Is Initialization**.

The resource is managed by an owning object: initialization establishes ownership,
and destruction releases the resource. Automatic objects are destroyed on
[normal scope exit](https://timsong-cpp.github.io/cppwp/n4659/stmt.dcl#2) and during
[exception unwinding to a handler](https://timsong-cpp.github.io/cppwp/n4659/except.ctor#2),
so callers do not need to remember a separate cleanup call on those paths.

The resource can be a file handle, lock, or allocation. RAII is not limited to
memory, and it does not depend on garbage collection.
The owner can live on the stack, inside another object, or in dynamic storage;
RAII describes the ownership and cleanup relationship, not a storage location.
Merely storing a borrowed handle without taking responsibility for closing it
would not make that object its RAII owner.

## Interview follow-up

Why is this useful in a function with several early returns? A local file-owning
object is destroyed when execution leaves its scope, including through a
`return`. Each path gets the same cleanup without remembering a separate close
call. Cleanup follows the owning object's lifetime.
```
