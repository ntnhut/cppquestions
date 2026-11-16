# Classes and const-correctness

Design read and update operations that callers can use through the appropriate
interface. Start with const-correctness in ordinary classes before studying
inheritance-based interfaces.

**Starting knowledge:** Classes, constructors, member functions, private data,
and const references.

```{toctree}
:maxdepth: 1

../questions/classes-001
```

## Your learning path

1. Separate operations that inspect an object from operations that change it.
2. Make read-only member functions callable through a const reference.
3. Distinguish const access to an object from the type of a returned value.
4. Keep permissions to modify data visible in the interface.
5. Apply the same reasoning when objects are passed to other functions.

Review [functions and references](functions.md) for read-only input parameters.
