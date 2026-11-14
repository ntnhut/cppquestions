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

An object owns an open file handle. Successful construction establishes
ownership, and the destructor closes the handle when the object is destroyed.
Assume normal scope exit or exception unwinding, rather than abrupt program
termination.

```{typed-answer}
## What is the four-letter acronym for this resource-management idiom?

## Answer and explanation

**RAII**, short for **Resource Acquisition Is Initialization**.

The resource is managed by an owning object: initialization establishes ownership,
and destruction releases the resource. Automatic objects are destroyed on normal
scope exit and during exception unwinding, so callers do not need to remember a
separate cleanup call on those paths.

The resource can be a file handle, lock, or allocation. RAII is not limited to
memory, and it does not depend on garbage collection.

## Interview follow-up

How does `std::unique_ptr` apply this idea? It owns a pointer and invokes its
deleter when destroyed, tying cleanup to the owning object's lifetime.
```

## Go deeper

```{related-questions}
```

Continue with the [ownership and RAII learning path](../topics/ownership.md).

## References

- [C++ Core Guidelines: R.1, manage resources automatically using RAII](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii)
- [C++ working draft: exiting a scope](https://eel.is/c++draft/stmt.dcl)
