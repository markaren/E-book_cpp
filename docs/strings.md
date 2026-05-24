# Strings

Text in C++ is handled by `std::string`. You will use it everywhere: for filenames, sensor IDs, log messages, command parsing, error descriptions. It behaves like any other value type: copying makes a real copy; passing by value is safe but potentially expensive.

This page is a quick reference for the operations you will reach for most. The full API is on [cppreference's std::string page](https://en.cppreference.com/w/cpp/string/basic_string).

---

## Creating strings

```cpp
#include <string>

std::string a;                          // empty
std::string b = "hello";                // from a string literal
std::string c{"hello"};                 // same, brace form
std::string d(5, 'a');                  // "aaaaa"
std::string e = std::to_string(42);     // "42" (convert a number)
```

A bare string literal in your source code (`"hello"`) is technically a `const char[]`, not a `std::string`. In most contexts it converts implicitly, but for the cases where it does not, you can force it:

```cpp
auto x = std::string{"hello"};      // explicit construction
```

---

## Length, emptiness, and access

```cpp
std::string s = "robotics";

s.length();          // 8 (same as s.size())
s.empty();           // false
s[0];                 // 'r' (no bounds check)
s.at(0);              // 'r' (bounds-checked, throws if out of range)
s.front();            // 'r'
s.back();             // 's'
```

`length()` and `size()` are identical; `std::string` carries both names for historical reasons. Use whichever reads better.

---

## Concatenation

`+` and `+=` work the way you expect:

```cpp
std::string greeting = "Hello, ";
std::string name     = "Alice";

std::string out = greeting + name + "!";   // "Hello, Alice!"
greeting += name;                            // greeting is now "Hello, Alice"
greeting += '!';                             // appending a single char also works
```

For building up long strings piece by piece, repeated `+=` is fine. For combining several small pieces, especially with non-string types mixed in, `std::format` is the cleanest option:

```cpp
#include <format>

std::string message = std::format("Motor {} at {} RPM", id, rpm);
```

The placeholders (`{}`) take the arguments in order and convert each to text automatically. No string concatenation, no `std::to_string`, no temporary streams.

Two older alternatives you will still see in existing code:

```cpp
// std::ostringstream (pre-C++20 idiom)
#include <sstream>
std::ostringstream out;
out << "Motor " << id << " at " << rpm << " RPM";
std::string message = out.str();

// Concatenation with std::to_string (works but reads poorly)
std::string message = "Motor " + std::to_string(id)
                    + " at "    + std::to_string(rpm) + " RPM";
```

Prefer `std::format` in new code.

---

## Searching

```cpp
std::string s = "hello world";

s.find("world");      // 6
s.find("xyz");        // std::string::npos, meaning "not found"

if (s.find("world") != std::string::npos) {
    // found
}

s.starts_with("hello"); // true   (C++20)
s.ends_with("world");   // true   (C++20)
```

To test whether a string contains a substring, use `find` as shown above: `s.find("o") != std::string::npos`. C++23 adds a shorter `s.contains("o")`, but this course targets C++20.

`std::string::npos` is the sentinel value all `find`-family functions return on failure. Always compare against it explicitly.

---

## Extracting parts

```cpp
std::string s = "robotics";

s.substr(0, 5);   // "robot"  (from index 0, take 5 characters)
s.substr(5);      // "ics"    (from index 5 to the end)
```

---

## Converting to and from numbers

```cpp
int    n = std::stoi("42");        // string → int
double d = std::stod("3.14");      // string → double

std::string a = std::to_string(42);    // "42"
std::string b = std::to_string(3.14);  // "3.140000"  (note: 6 decimal places by default)
```

`std::to_string` is fine for quick conversions but its formatting is fixed (and for `double` it always prints 6 decimal places, often more than you want). For precise formatting use `std::format`:

```cpp
std::string a = std::format("{:.2f}", 3.14159);   // "3.14"
std::string b = std::format("{:>8}", 42);         // "      42" (right-aligned)
std::string c = std::format("{:#x}", 255);        // "0xff"
```

`std::stoi` and friends throw if the input is not a number; wrap them in `try`/`catch` or check the input first if that matters.

---

## Comparison

```cpp
std::string a = "apple";
std::string b = "banana";

a == b;     // false
a != b;     // true
a < b;       // true  (lexicographic comparison)
```

The comparison is byte-by-byte. It is case-sensitive (`"Apple" != "apple"`) and locale-naïve (it does not understand language-specific sorting rules). If you need case-insensitive comparison, lowercase both sides first (loop with `std::tolower`).

---

## `std::string` and `const char*`

The C-style "string" is a pointer to a null-terminated array of characters. You will see them in two places:

1. **String literals** in your code. `"hello"` is a `const char*`.
2. **Old C APIs.** Many libraries (especially embedded ones) take `const char*` parameters.

`std::string` converts to and from these freely:

```cpp
const char* literal = "hello";
std::string s = literal;                 // implicit construction

const char* cstr = s.c_str();             // explicit conversion back
```

`s.c_str()` returns a pointer to the string's internal buffer with a null terminator. It is valid only as long as `s` is alive and unmodified.

---

## Common pitfalls

**Modifying through `c_str()`.** The pointer returned by `c_str()` is `const`. Do not cast away the const and write through it; the result is undefined behaviour.

**Comparing with a `const char*` and getting nonsense.**

```cpp
const char* a = "hello";
const char* b = "hello";
if (a == b) { /* this compares POINTERS, not strings */ }
```

Wrap one side in `std::string` to force a value comparison: `if (std::string(a) == b)`.

**Iterating bytes instead of characters.** `std::string` is a sequence of `char`. If your string contains multi-byte UTF-8 characters (Norwegian å, ø, æ for example), `s[3]` may give you a partial byte, not a logical character. For ASCII-only text this is fine; for general text, use a proper Unicode-aware library.

---

## Summary

- `std::string` is the everyday string type. Use it for all text.
- Concatenate with `+` and `+=`; search with `find`; slice with `substr`.
- Convert to and from numbers with `std::to_string` / `std::stoi` / `std::stod`.
- For combining many pieces of mixed types, `std::format` reads cleaner than chained `+=` or `std::ostringstream`.
- `find` returns `std::string::npos` when nothing is found.
- `c_str()` gives you a `const char*` for C APIs.
