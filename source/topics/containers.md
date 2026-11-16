# Containers and iterators

Practice container contracts that affect correctness: whether lookup inserts,
whether reserved storage contains elements, and which iterators survive erasure.

**Starting knowledge:** Vectors, maps, loops, indexing, and basic iterators.

```{toctree}
:maxdepth: 1

../questions/containers-002
../questions/containers-003
../questions/containers-001
```

## Your learning path

1. Distinguish map lookup from insertion through a subscript.
2. Distinguish existing elements from capacity reserved for future growth.
3. Choose between resizing and appending when filling a vector.
4. Check invalidation rules before continuing a traversal after modification.
5. Explain container choices using their contracts and the task's requirements.

Review [ownership and RAII](ownership.md) when reasoning about element lifetimes.
