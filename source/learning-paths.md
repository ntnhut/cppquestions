# Learning paths

A question can reveal a gap in understanding. These paths assume familiarity
with ordinary C++ syntax, functions, classes, pointers, and standard containers.
Choose a topic, explain the contract or bug, and compare your reasoning with
the answer. Use the starting knowledge on each page to choose an appropriate question.

| Available topic | Starting knowledge | Current practice |
| --- | --- | --- |
| [Core language and common bugs](topics/fundamentals.md) | Numeric types, pointers, and Boolean operators | Integer-division bugs and short-circuit pointer guards |
| [Functions and references](topics/functions.md) | Parameters, references, const, and containers | Read-only input contracts, copying costs, and mutation |
| [Containers and iterators](topics/containers.md) | Vectors, maps, indexing, and iterators | Lookup versus insertion, reserve versus resize, safe erasure |
| [Classes and const-correctness](topics/classes.md) | Classes, member functions, and const references | Read-only getters and mutable access permissions |
| [Ownership and RAII](topics/ownership.md) | Scope, constructors, and destructors; smart pointers for the code example | Basic cleanup terminology, then intermediate resource lifetime tracing |
| [Inheritance and polymorphism](topics/polymorphism.md) | Value/reference parameters, inheritance, and virtual functions | Optional intermediate practice on slicing and destruction |
| [Move semantics](topics/move-semantics.md) | Copy/move constructors, reference binding, const, and overload selection | Optional advanced practice on const and copying |

Move semantics and inheritance can wait until your code or study requires them.
Work through ordinary object use and container operations before these more
specialized examples.
