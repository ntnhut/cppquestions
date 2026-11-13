---
id: ownership-001
topic: ownership
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
---

# Does a unique pointer release its resource at scope exit?

**Basic · C++17 · Ownership and RAII · Single choice**

Assume allocation succeeds and execution reaches the end of the inner scope.
What does this program print?

```{literalinclude} ../../examples/ownership-001.cpp
:language: cpp
```

Select an answer, then choose **Evaluate** to read the explanation.

```{quizdown-explained}
## What is the output?

1. [ ] `end` followed by `destroy`
1. [x] `destroy` followed by `end`
1. [ ] Only `end`; the resource is leaked
1. [ ] The program does not compile
## Answer and explanation

**`destroy` followed by `end`, each on its own line.** The local `owner` is
destroyed when execution leaves the inner scope. Its `std::unique_ptr` destructor
uses the default deleter to delete the owned `Resource`, which calls the
`Resource` destructor. Execution then prints `end`.

No explicit `delete` is needed. This is RAII: the owning object's lifetime
determines when the resource is released. The output order follows scope exit;
it does not depend on a garbage collector running later.

The program is valid C++17. `std::make_unique` is available from C++14 onward.

## Interview follow-up

What would happen if the scope were exited by an exception caught outside it?
During stack unwinding, the fully constructed local owner would be destroyed
and release its resource.
```

## Go deeper

Continue with the [ownership and RAII learning path](../topics/ownership.md).

## References

- [C++ working draft: unique_ptr destructor](https://eel.is/c++draft/unique.ptr.single.dtor)
- [C++ working draft: exiting a scope](https://eel.is/c++draft/stmt.dcl)
