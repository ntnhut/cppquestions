---
id: containers-003
topic: containers
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [vector, capacity, reserve, resize]
related: [containers-001, functions-002]
---

# Does reserving vector capacity create elements you can index?

```{question-meta}
```

**Starting knowledge:** Vectors, indexing, and inserting elements. `size()` counts
existing elements; `capacity()` describes available storage before reallocation.

In C++17, a loader expects up to six readings and reserves space before filling
its vector. Assume allocation succeeds. The example inspects the vector after
`reserve` and then creates three zero-valued elements with `resize`.

```{literalinclude} ../../examples/containers-003.cpp
:language: cpp
```

```{quizdown-explained}
## Which statement is correct immediately after samples.reserve(6)?

1. [ ] There are six integer elements, all initialized to zero
1. [x] The size is zero and capacity is at least six; samples[0] is not a valid element yet
1. [ ] The size is zero, but samples[0] can be assigned because storage was reserved
1. [ ] Six is now the maximum permitted size, so inserting a seventh element is rejected
## Answer and explanation

**Capacity is at least six, but the vector still contains no elements.**
The first line prints `0 1`: size zero and a true capacity comparison.

[`reserve`](https://timsong-cpp.github.io/cppwp/n4659/vector.capacity#4)
prepares storage without changing size. It does not create six integers, and
reserved storage alone does not make `samples[0]` a valid element. The
[sequence-access contract](https://timsong-cpp.github.io/cppwp/n4659/sequence.reqmts)
requires an existing element at the index.

`reserve(6)` also does not impose a maximum of six elements. The vector can grow
further, allocating more storage when necessary. Its capacity need not be
exactly six.

The later [`resize(3, 0)`](https://timsong-cpp.github.io/cppwp/n4659/vector.capacity#16)
creates three elements initialized to the supplied zero, so the second line
prints `3 0`.

## Interview follow-up

Which operation fits a loader that appends each reading as it arrives? Reserve
expected capacity, then use `push_back` for each actual reading. If instead you
need six existing positions to fill by index, use `resize(6, 0)` first. Choose
based on whether you need storage for future insertions or elements now.
```
