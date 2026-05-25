# Strings and Vectors

Two types from the standard library turn up in almost every desktop program: `std::string` for text, and `std::vector` for a list of values. They are not built into the language the way `int` and `double` are, but in desktop C++ you will reach for them constantly — without them you can hold only one value at a time and cannot work with words at all. (On small microcontrollers they are often unavailable; see [Arduino vs. Desktop C++](../arduino_vs_desktop.md).)

This page covers just enough to use both. The full detail comes in Chapter 3 — [Strings](../strings.md), the [Standard Library](../Chapter3/standard_library.md), and [Data Structures](../Chapter3/data_structures.md).

---

## `std::string`: text

You have already used text as string *literals* — the `"Hello, world!"` in quotes. A `std::string` is a *variable* that holds text you can build, change, and inspect. Include `<string>` to use it:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Ada";
    std::string greeting = "Hello, " + name + "!";   // join pieces with +

    std::cout << greeting << "\n";        // Hello, Ada!
    std::cout << name.length() << "\n";   // 3  — number of characters
}
```

The everyday operations:

| Operation            | Example            | Result                          |
|----------------------|--------------------|---------------------------------|
| Join                 | `"Hi " + name`     | a new string `"Hi Ada"`         |
| Append in place      | `greeting += "!"`  | adds to the end of `greeting`   |
| Length               | `name.length()`    | `3` (also `name.size()`)        |
| One character        | `name[0]`          | `'A'` — a `char`, counting from 0 |
| Compare              | `name == "Ada"`    | `true`                          |
| Is it empty?         | `name.empty()`     | `false`                         |

### Reading text from the user

`std::cin >> word` reads a single **word** — it stops at the first space. To read a whole line, spaces and all, use `std::getline`:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string fullName;

    std::cout << "Enter your full name: ";
    std::getline(std::cin, fullName);   // reads the entire line

    std::cout << "Hello, " << fullName << "!\n";
}
```

Had you written `std::cin >> fullName`, typing `Ada Lovelace` would store only `Ada` and leave `Lovelace` behind — a classic beginner surprise. Use `>>` for single words, `getline` for whole lines.

---

## `std::vector`: a list of values

A `std::vector` holds a sequence of values **of one type**, and it grows as you add to it. Include `<vector>`, and put the element type in angle brackets:

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings = {42, 17, 99};   // start with three ints

    readings.push_back(8);                  // add one to the end → {42, 17, 99, 8}

    std::cout << readings.size() << "\n";   // 4  — how many elements
    std::cout << readings[0]     << "\n";   // 42 — the first (index 0)
    std::cout << readings[3]     << "\n";   // 8  — the fourth (index 3)
}
```

A few things to hold onto:

- The type in `<...>` is the **element type**: `std::vector<int>` holds `int`s, `std::vector<std::string>` holds strings. Every element has the same type.
- **Indexing starts at 0.** The first element is `[0]`, the last is `[size() - 1]`.
- Reading or writing past the end — `readings[99]` here — is **undefined behaviour**: the program may crash or quietly misbehave. Stay between `0` and `size() - 1`.
- `push_back` adds to the end and the vector grows on its own. You never manage its memory.

> C++ also has lower-level, built-in arrays (`int a[4]`), but `std::vector` is the one to reach for: it knows its own size and resizes itself. Prefer it.

To *do* something with every element — print them all, sum them, find the largest — you use a **loop**. That is exactly what the next page, [Control Statements](control_statements.md), is for; the range-based `for` reads especially cleanly over a vector.

---

## Summary

- `std::string` (from `<string>`) holds text: join with `+`, measure with `.length()`, read one character with `[i]`, read a whole line with `std::getline`.
- `std::vector<T>` (from `<vector>`) holds a growable list of values of type `T`: add with `push_back`, count with `.size()`, read with `[i]` (starting at 0).
- Both clean up their own memory — you never have to.
- This is a working minimum. Chapter 3 goes much deeper — [Strings](../strings.md), the [Standard Library](../Chapter3/standard_library.md), and [Data Structures](../Chapter3/data_structures.md).
