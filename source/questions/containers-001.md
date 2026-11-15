---
id: containers-001
topic: containers
difficulty: intermediate
cpp_standard: c++17
kind: single-choice
status: verified
tags: [vector, iterators, invalidation, erase]
related: [containers-002]
---

# How do you keep iterating safely after erasing from a vector?

```{question-meta}
```

**Starting knowledge:** A vector stores a sequence of values. An iterator marks
a position, `*it` reads its value, and `end()` marks the position after the last
element. Review ordinary vector loops before this intermediate erasure example.

In C++17, this loop removes every even number, including adjacent even numbers.
Assume allocation succeeds.

```{literalinclude} ../../examples/containers-001.cpp
:language: cpp
```

```{quizdown-explained}
## Why does the erase branch assign to it without then incrementing it?

1. [ ] Only iterators to erased elements are invalidated; assigning the result is optional
1. [ ] Erasing invalidates every iterator into the vector, so the loop must restart at begin
1. [ ] erase returns the element before the erased one, so the next iteration advances it
1. [x] erase invalidates the old iterator and returns the next position, which still needs to be checked
## Answer and explanation

**Assign the iterator returned by `erase`, then check that position on the next
iteration.** This program prints `1` followed by `3`, each on its own line.

For `vector`, [erasing invalidates iterators and references at or after the erase position](https://timsong-cpp.github.io/cppwp/n4659/vector.modifiers#3).
Iterators before it remain valid. Reusing or incrementing the old `it` after
erasure is not a valid way to advance the loop, even if storage stays allocated.

The [returned iterator](https://timsong-cpp.github.io/cppwp/n4659/sequence.reqmts#11)
points to the element following the erased element, or to the new `end()` if
there is no such element. It does not point backward, and there is no need to
restart from `begin()`.

After removing `2`, the returned iterator designates `4`. Incrementing it
immediately would skip checking `4`. After removing the final `6`, the result
is `end()`; the loop condition detects that before any dereference. The loop
calls `values.end()` again on each iteration instead of saving an invalidated
end iterator.

## Interview follow-up

Would calling `reserve` before the loop make old iterators safe after `erase`?
No. Avoiding allocation does not change `erase`'s invalidation rule; elements
after the erased position are shifted. Keep using the returned iterator.
Invalidation rules depend on the specific container and operation, so do not
apply a rule about vector growth to vector erasure.
```
