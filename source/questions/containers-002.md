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

**Starting knowledge:** A map stores key-value pairs. Here the keys are strings
and the values are integers. `size()` reports the number of pairs, and `find`
returns `end()` if a key is absent. Focus on whether reading with `[]` changes
the map.

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

[`map::operator[]`](https://timsong-cpp.github.io/cppwp/n4659/map.access#2)
adds a key-value pair when the key is missing. In this map, the new integer
value [starts at zero](https://timsong-cpp.github.io/cppwp/n4659/dcl.init#8),
not an indeterminate value. The map now has two elements: the original `ready`
entry and the new `missing` entry.

The subscript is useful for deliberately creating a counter, as in
`++counts[key]`. It is unsuitable for a lookup that must leave the map unchanged.
`at()` is the access operation that throws `std::out_of_range` for a missing
key; `operator[]` inserts instead. If the key already exists, the subscript
returns a reference to its existing value without resetting it.

## Interview follow-up

When is insertion through `[]` useful? When counting events, for example:
`++counts["requests"]` starts a missing counter at zero and then increases it
to one. If that counter already exists, it increases the stored value. Use
`find` when you only want to check for an entry without adding one.
```
