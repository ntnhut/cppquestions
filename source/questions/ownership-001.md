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

Assume allocation succeeds and execution reaches the end of the inner scope.
What does this program print?

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
destroyed when [execution leaves the inner scope](https://eel.is/c++draft/stmt.dcl).
Its [`std::unique_ptr` destructor](https://eel.is/c++draft/unique.ptr.single.dtor)
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
