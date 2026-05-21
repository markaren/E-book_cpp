# Values, References, and Pointers

C++ gives you three ways to refer to data: by **value** (you have your own copy), by **reference** (an alias for someone else's data), and by **pointer** (an address that may or may not point to something).

Each behaves differently and each has its place. Choosing the right one decides whether your function modifies the caller's data, whether it makes an expensive copy, and whether the program crashes when something goes wrong.

This chapter explains all three and gives a clear default for each situation.

---

## Value types

A value type holds the data itself. Assigning or passing a value type **copies** it.

```cpp
int a = 25;
int b = a;    // b is a copy
b = 30;       // a is still 25
```

This is the safest default and how every built-in type and most class types behave by default. Each variable has its own independent storage.

The cost is the copy: for an `int` it is essentially free, for a 10 MB `std::vector` it is a heap allocation and a `memcpy`. (The [Move Semantics chapter](../Chapter4/move.md) explains how modern C++ avoids many of these copies automatically.)

---

## References

A **reference** is an alias for an existing variable. Reads and writes through the reference go straight to the original.

```cpp
int age = 42;
int& refAge = age;    // refAge is another name for age
refAge = 10;          // age is now 10
```

Three things make references different from pointers:

- A reference must be initialised when declared. There is no "uninitialised" reference.
- A reference cannot be rebound. Once it refers to `age`, it refers to `age` forever.
- A reference is never null. It always refers to some object.

References are the workhorse of efficient parameter passing in C++.

### `const` references

A `const` reference is read-only. The function can look at the data but cannot change it.

```cpp
void printVector(const std::vector<double>& v) {
    for (double x : v) {
        std::cout << x << "\n";
    }
    // v.push_back(0.0);   // compile error — const
}
```

This is the standard idiom for passing large objects without copying them:

```cpp
std::vector<double> data = readSensorBatch();
printVector(data);   // no copy — printVector sees the original via const&
```

Without `const&`, `printVector` would receive a 10 MB copy every call. With it, the call costs one pointer's worth of work.

---

## Pointers

A **pointer** is a variable that holds an *address*. The `*` operator looks through the address to the value stored there:

```cpp
int x = 7;
int* p = &x;     // p holds the address of x
*p = 42;         // writes through p — x is now 42
```

| Symbol | Meaning |
|--------|---------|
| `int*`  | "pointer to int" — the type of `p` |
| `&x`    | "address of x" — produces a pointer |
| `*p`    | "what `p` points to" — dereference |

Pointers differ from references in three important ways:

- A pointer can be `nullptr` — pointing to nothing.
- A pointer can be reassigned to point elsewhere.
- A pointer can be dangerous: dereferencing a null or invalid pointer is undefined behaviour.

```cpp
int* p = nullptr;   // valid pointer, points to nothing
if (p != nullptr) {
    *p = 5;         // safe — checked first
}
```

Always check before dereferencing, or use language constructs that guarantee non-null (references, smart pointers).

---

## The big lifetime trap

The rule: a reference or pointer is only valid as long as what it refers to is still alive. The single biggest source of crashes in C++ is using a reference or pointer to data that has been destroyed.

### Returning a reference or pointer to a local

```cpp
int& createIntRef() {
    int value = 1;
    return value;     // bad — `value` is destroyed when the function returns
}

int* createIntPtr() {
    int value = 1;
    return &value;    // bad — same problem
}

int main() {
    int& bad1 = createIntRef();    // dangling reference — undefined behaviour
    int* bad2 = createIntPtr();    // dangling pointer  — undefined behaviour
}
```

Both functions return a handle to memory that no longer belongs to anyone. Reading from `bad1` or `bad2` is undefined behaviour. Modern compilers warn about exactly this pattern — pay attention to the warnings.

The fix: return by value (you get your own copy) or pass a reference *into* the function so the caller controls the lifetime.

### Pointers and references into class internals

Returning a reference or pointer to a class's private data also breaks encapsulation:

```cpp
class Demo {
public:
    int  getValue() const   { return value_; }   // safe — returns a copy
    int& getValueRef()      { return value_; }   // hands out write access
    int* getValuePtr()      { return &value_; }  // hands out write access

private:
    int value_ = 0;
};

Demo obj;
int& ref = obj.getValueRef();
ref = 42;        // obj's private data is now 42 — invariants bypassed
```

If you must expose a member by reference, return `const T&` to keep it read-only. Otherwise external code can change your private state without going through the methods that enforce your invariants.

---

## Which one should I use?

Use this table whenever a function parameter or return type forces the question:

| Situation | Use |
|-----------|-----|
| Small, cheap-to-copy type (`int`, `double`, `bool`, an enum) | Pass by **value** |
| Function should not modify the input | Pass by **`const T&`** |
| Function modifies the input and the caller should see the change | Pass by **`T&`** |
| Function may receive "no value" | Pass a **pointer** (and check for null), or `std::optional<T>` |
| Function returns a freshly-computed result | Return by **value** (RVO makes this cheap) |
| Function returns one of its inputs unchanged | Return by **reference** (be careful about lifetimes) |

For data members of a class, the rules of thumb are similar:

| Situation | Use |
|-----------|-----|
| Class owns the data | Plain value member — `std::vector<int> data_` |
| Class observes data owned by something else | A reference or raw pointer — but think carefully about who keeps it alive |
| Class shares ownership with others | `std::shared_ptr<T>` (see [Memory](../Chapter4/memory.md)) |

---

## Summary

- **Value** types copy. Safe, sometimes expensive.
- **References** are aliases. Cannot be null, cannot be rebound, must be initialised.
- **Pointers** are addresses. Can be null, can be reassigned, must be checked.
- A reference or pointer outliving the thing it points to is undefined behaviour — the single most common cause of crashes.
- For function parameters: small types by value, large types by `const T&`, modify-the-input cases by `T&`.
- For ownership across class boundaries, prefer smart pointers over raw ones.
