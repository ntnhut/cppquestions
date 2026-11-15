---
id: containers-002
topic: containers
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [map, lookup, insertion, value-initialization]
related: [containers-001]
---

# Can looking up a missing map key insert an element?

```{question-meta}
```

In C++17, compare `find` and `operator[]` on this `std::map`. Assume all
allocations succeed. Boolean output uses the default numeric formatting.

```{literalinclude} ../../examples/containers-002.cpp
:language: cpp
```

```{quizdown-explained}
## What does the second output line contain?

1. [ ] `0 1`: a missing key yields zero without inserting anything
1. [x] `0 2`: the subscript inserts the missing key with an integer value of zero
1. [ ] There is no second line because operator[] throws std::out_of_range
1. [ ] An indeterminate integer followed by `2`
## Answer and explanation

**The second line is `0 2`.** The complete output is `1 1` followed by `0 2`.

[`find`](https://timsong-cpp.github.io/cppwp/n4659/associative.reqmts) returns
`end()` when the key is absent; it does not insert an element. The first line
therefore reports a true comparison (`1`) and the original size (`1`).

In C++17, [`map::operator[]`](https://timsong-cpp.github.io/cppwp/n4659/map.access#2)
is specified in terms of `try_emplace`. When the key is missing,
[it inserts it](https://timsong-cpp.github.io/cppwp/n4659/map.modifiers#4)
and constructs the mapped value with no supplied arguments. For this map with
its default allocator, the `int` is
[value-initialized to zero](https://timsong-cpp.github.io/cppwp/n4659/dcl.init#8),
not left indeterminate. The map now has two elements.

The subscript is useful for deliberately creating a counter, as in
`++counts[key]`. It is unsuitable for a lookup that must leave the map unchanged.
`at()` is the access operation that throws `std::out_of_range` for a missing
key; `operator[]` inserts instead. If the key already exists, the subscript
returns a reference to its existing value without resetting it.

## Interview follow-up

How would you read a possibly absent count from a `const std::map`? Use `find`,
compare its result with `end()`, and read `it->second` only when found. Decide
explicitly whether an absent entry means zero or an error. `operator[]` is not
available on a const map because it can insert. Use `at()` if absence should
throw. Both `find` and `at` support this read-only use in C++17.
```
