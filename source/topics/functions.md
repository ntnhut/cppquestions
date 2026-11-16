# Functions and references

Choose parameter types that express whether a function borrows, copies, or
modifies its input. Practice explaining both the API contract and the cost of
passing an existing object.

**Starting knowledge:** Functions, value and reference parameters, `const`, and
standard containers.

```{toctree}
:maxdepth: 1

../questions/functions-001
../questions/functions-002
```

## Your learning path

1. Decide whether modifying the caller is part of a function's intended behavior.
2. Distinguish a separate value parameter from a reference to an existing object.
3. Use a const reference for a larger read-only input when no independent copy is needed.
4. Keep inexpensive scalar parameters by value when that meets the contract.
5. Check that borrowed objects remain alive for every use of the reference.

Practice reading stored values in [containers and iterators](containers.md).
