---
id: functions-002
topic: functions
difficulty: basic
cpp_standard: c++17
kind: single-choice
status: verified
tags: [parameters, const, references, copying]
related: [functions-001, classes-001]
---

# How should a read-only function accept a large vector?

```{question-meta}
```

**Starting knowledge:** Passing by value and reference, vectors, and `const`.
The caller owns an existing vector and keeps it alive throughout the call.

In C++17, this helper sums costs without changing them. In the application,
the input vector may be large. The helper needs neither ownership nor its own
independent copy. Assume allocation succeeds and the sum fits in `int`.

```{literalinclude} ../../examples/functions-002.cpp
:language: cpp
```

```{quizdown-explained}
## Which parameter form avoids a vector copy and prevents element changes through costs?

1. [ ] `std::vector<int> costs`
1. [ ] `const std::vector<int> costs`
1. [x] `const std::vector<int>& costs`
1. [ ] `std::vector<int>& costs`
## Answer and explanation

**Use `const std::vector<int>& costs`.** The reference accesses the existing
vector, and `const` prevents changing its elements through this parameter.
The example prints `25`.

For an existing vector passed as an argument, a by-value parameter creates an
independent vector with copied elements. Adding `const` to that local value
restricts its use inside the function but does not remove the copy.

A non-const reference also avoids the copy, but permits the function to change
the vector. It does not express the required read-only access. A const reference
[binds to the existing object](https://timsong-cpp.github.io/cppwp/n4659/dcl.init.ref#5.1)
while providing a read-only access path.

This follows the [Core Guidelines' input-parameter advice](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-in):
pass inexpensive values by value and larger read-only inputs by reference to
const. It is a choice about this function's contract, not a rule that every
parameter should be a reference. The reference does not extend the caller's
object lifetime beyond the call or take ownership.

## Interview follow-up

Would you also pass a simple integer fee as `const int&` to avoid copying?
Usually pass it as `int`. An integer is inexpensive to copy, and a value
parameter already prevents local changes from modifying the caller's integer.
Use a non-const reference when modifying the caller is an intended part of the API.
```
