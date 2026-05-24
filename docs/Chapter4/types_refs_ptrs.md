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

The cost is the copy: for an `int` it is essentially free, for a 10 MB `std::vector` it is a heap allocation and a `memcpy`. (The [Move Semantics chapter](../Chapter5/move.md) explains how modern C++ avoids many of these copies automatically.)

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
    // v.push_back(0.0);   // compile error, const
}
```

This is the standard idiom for passing large objects without copying them:

```cpp
std::vector<double> data = readSensorBatch();
printVector(data);   // no copy, printVector sees the original via const&
```

Without `const&`, `printVector` would receive a 10 MB copy every call. With it, the call costs one pointer's worth of work.

---

## Pointers

A **pointer** is a variable that holds an *address*. The `*` operator looks through the address to the value stored there:

```cpp
int x = 7;
int* p = &x;     // p holds the address of x
*p = 42;         // writes through p, x is now 42
```

| Symbol | Meaning |
|--------|---------|
| `int*`  | "pointer to int"; the type of `p` |
| `&x`    | "address of x"; produces a pointer |
| `*p`    | "what `p` points to"; dereference  |

A reference and a pointer can both refer to the same variable `x`, but the mechanics differ — a reference gives `x` a second *name*, while a pointer is a separate cell that stores `x`'s *address*:

<svg viewBox="0 0 500 175" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Referring to the variable x: a reference (int ampersand r = x) gives x's cell a second name r; a pointer (int star p = ampersand x) is a separate cell holding x's address, reached by following the arrow." style="display:block;margin:1rem auto;max-width:500px;width:100%;height:auto;font-family:var(--md-code-font-family,monospace);font-size:13px;" fill="none" stroke="currentColor" stroke-width="1.5">
  <defs>
    <marker id="rp-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor" stroke="none"/>
    </marker>
  </defs>
  <text x="40" y="28" stroke="none" fill="currentColor" font-weight="bold">int&amp; r = x;</text>
  <rect x="40" y="50" width="120" height="56" rx="4"/>
  <line x1="40" y1="76" x2="160" y2="76"/>
  <text x="100" y="68" stroke="none" fill="currentColor" text-anchor="middle">x &#183; r</text>
  <text x="100" y="97" stroke="none" fill="currentColor" text-anchor="middle" font-size="15">7</text>
  <text x="40" y="140" stroke="none" fill="currentColor" font-size="11" opacity="0.7">r is another name for x</text>
  <text x="280" y="28" stroke="none" fill="currentColor" font-weight="bold">int* p = &amp;x;</text>
  <rect x="280" y="50" width="70" height="56" rx="4"/>
  <line x1="280" y1="76" x2="350" y2="76"/>
  <text x="315" y="68" stroke="none" fill="currentColor" text-anchor="middle">p</text>
  <text x="315" y="97" stroke="none" fill="currentColor" text-anchor="middle">&amp;x</text>
  <rect x="410" y="50" width="70" height="56" rx="4"/>
  <line x1="410" y1="76" x2="480" y2="76"/>
  <text x="445" y="68" stroke="none" fill="currentColor" text-anchor="middle">x</text>
  <text x="445" y="97" stroke="none" fill="currentColor" text-anchor="middle" font-size="15">7</text>
  <line x1="350" y1="92" x2="408" y2="92" marker-end="url(#rp-arrow)"/>
  <text x="280" y="140" stroke="none" fill="currentColor" font-size="11" opacity="0.7">p stores x's address</text>
</svg>

Pointers differ from references in three important ways:

- A pointer can be `nullptr`, meaning it points to nothing.
- A pointer can be reassigned to point elsewhere.
- A pointer can be dangerous: dereferencing a null or invalid pointer is undefined behaviour.

```cpp
int* p = nullptr;   // valid pointer, points to nothing
if (p != nullptr) {
    *p = 5;         // safe, checked first
}
```

Always check before dereferencing, or use language constructs that guarantee non-null (references, smart pointers).

---

## The big lifetime trap

The rule: a reference or pointer is only valid as long as what it refers to is still alive. The single biggest source of crashes in C++ is using a reference or pointer to data that has been destroyed.

### Returning a reference or pointer to a local

<!-- no-ce -->
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
    int* bad2 = createIntPtr();    // dangling pointer — undefined behaviour
}
```

Both functions return a handle to memory that no longer belongs to anyone. Reading from `bad1` or `bad2` is undefined behaviour. Modern compilers warn about exactly this pattern; pay attention to the warnings.

The fix: return by value (you get your own copy) or pass a reference *into* the function so the caller controls the lifetime.

### Pointers and references into class internals

Returning a reference or pointer to a class's private data also breaks the **encapsulation** you met in [Classes](classes.md):

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
ref = 42;        // obj's private data is now 42, invariants bypassed
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
| Class owns the data | Plain value member (e.g. `std::vector<int> data_`) |
| Class observes data owned by something else | A reference or raw pointer — but think carefully about who keeps it alive |
| Class shares ownership with others | `std::shared_ptr<T>` (see [Memory](../Chapter5/memory.md)) |

---

## Summary

- **Value** types copy. Safe, sometimes expensive.
- **References** are aliases. Cannot be null, cannot be rebound, must be initialised.
- **Pointers** are addresses. Can be null, can be reassigned, must be checked.
- A reference or pointer outliving the thing it points to is undefined behaviour — the single most common cause of crashes.
- For function parameters: small types by value, large types by `const T&`, modify-the-input cases by `T&`.
- For ownership across class boundaries, prefer smart pointers over raw ones.
