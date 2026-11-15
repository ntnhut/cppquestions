---
id: ownership-001
topic: ownership
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [raii, lifetime, unique-ptr]
related: [ownership-002, move-001]
---

# Does a unique pointer release its resource at scope exit?

```{question-meta}
```

In C++17, assume allocation succeeds and execution reaches the end of the inner
scope normally. What does this program print?

```{literalinclude} ../../examples/ownership-001.cpp
:language: cpp
```

```{quizdown-explained}
## What is the output?

1. [ ] `end` followed by `destroy`
1. [x] `destroy` followed by `end`
1. [ ] Only `end`; the resource is leaked
1. [ ] The program does not compile
## Answer and explanation

**`destroy` followed by `end`, each on its own line.** The local `owner` is
destroyed when [execution leaves the inner scope](https://timsong-cpp.github.io/cppwp/n4659/stmt.dcl#2).
Its [`std::unique_ptr` destructor](https://timsong-cpp.github.io/cppwp/n4659/unique.ptr.single.dtor)
uses the default deleter to delete the owned `Resource`, which calls the
`Resource` destructor. Execution then prints `end`.

No explicit `delete` is needed. This is RAII: the owning object's lifetime
determines when the resource is released. The output order follows scope exit;
it does not depend on a garbage collector running later.

The program compiles in C++17: `std::make_unique<Resource>()` constructs the
resource and returns its owning pointer. The resource is released before `end`
is printed, so neither the reversed order nor the leak option describes this
execution.

## Interview follow-up

What would happen if the scope were exited by an exception caught outside it?
During [stack unwinding to that handler](https://timsong-cpp.github.io/cppwp/n4659/except.ctor#2),
the fully constructed local owner would be destroyed and release its resource.
It would still print `destroy`. If the exception skips the statement printing
`end`, that statement is not executed. This guarantee depends on unwinding;
abrupt termination is a different case.
```
