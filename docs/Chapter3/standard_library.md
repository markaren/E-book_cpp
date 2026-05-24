# The C++ Standard Library

The C++ Standard Library is the set of containers, algorithms, and utilities that ship with every C++ compiler. It is what `std::cout`, `std::vector`, and `std::string` belong to.

Knowing it well is the difference between writing fluent, idiomatic C++ and reinventing the wheel. The library has been refined for decades; whatever you are thinking of writing, there is a very good chance it is already there.

This chapter is a guided tour of the parts you will use this semester. It is not a reference; for that, see [cppreference.com](https://en.cppreference.com/). The aim here is to know *what exists* so that you can look it up when you need it.

---

## The `std::` prefix

Everything in the standard library lives in the `std` namespace. You write `std::vector`, not `vector`. The prefix tells readers (and the compiler) that you mean *the* standard library type, not something you wrote yourself.

You can omit the prefix by writing `using namespace std;` at the top of a file. You should not. In small programs it is harmless; in larger ones it brings every standard-library name into scope and creates name clashes with your own code. Get used to writing `std::` everywhere.

---

## Containers: collections of values

A container holds a collection of values. The choice between them depends on what you need to do with them.

### `std::vector<T>`: a resizable array

The container you will use 80% of the time. Elements are stored contiguously in memory, you can grow and shrink it at runtime, and indexed access is constant-time.

```cpp
#include <vector>

std::vector<int> readings = {17, 42, 99, 8};

readings.push_back(5);           // append
int first = readings[0];          // index access (no bounds check)
int safer = readings.at(0);       // bounds-checked, throws if out of range

readings.size();                  // number of elements
readings.empty();                 // true if size == 0
```

Iterate with a range-based `for`:

```cpp
for (int value : readings) {
    std::cout << value << "\n";
}
```

**When to use:** by default, for any "list of things." Reach for something else only if measurement says you need to.

### `std::array<T, N>`: a fixed-size array

A safer replacement for the C-style array. Size is fixed at compile time, so it lives on the stack.

```cpp
#include <array>

std::array<int, 4> readings = {17, 42, 99, 8};
readings.size();   // 4, known at compile time
readings[2];        // 99
```

**When to use:** the number of elements is known at compile time and won't change. Useful for fixed-length sensor data, lookup tables, and matrix dimensions.

### `std::string`: a string of characters

Text. Everywhere you would have used `char[]` in C, use `std::string` in C++.

```cpp
#include <string>

std::string name = "Alice";
name += " Smith";           // concatenation
name.length();              // 11
name.substr(0, 5);          // "Alice"
name.find("Smith");          // 6, the index where "Smith" starts
```

See [Strings](../strings.md), later in this chapter, for a tour of the operations you will reach for most.

### `std::map<K, V>`: a sorted key-value store

Maps keys to values. Keys are kept sorted, so lookup is O(log n).

```cpp
#include <map>

std::map<std::string, int> wordCount;
wordCount["hello"] = 1;
wordCount["world"] = 2;
++wordCount["hello"];        // now 2

for (const auto& [word, count] : wordCount) {   // [word, count] splits each key/value pair
    std::cout << word << ": " << count << "\n";
}
```

### `std::unordered_map<K, V>`: a hash-based key-value store

Same interface as `std::map`, but unsorted and faster on average (constant-time lookup).

```cpp
#include <unordered_map>

std::unordered_map<std::string, int> fast;
fast["temperature"] = 22;
```

**Choosing between map and unordered_map:** unordered is faster, ordered keeps things sorted (handy for ordered iteration or range queries). If you do not need order, `unordered_map` is usually the right default.

### `std::set` and `std::unordered_set`

Like `map` and `unordered_map`, but storing just *keys*, no values. Use when you need to keep track of "have I seen this before?" — duplicates are silently discarded.

```cpp
#include <set>

std::set<int> uniqueReadings;
uniqueReadings.insert(42);
uniqueReadings.insert(42);   // ignored, already present
uniqueReadings.contains(42); // true
```

### Other containers

`std::list` (doubly linked list), `std::deque` (double-ended queue), `std::stack`, and `std::queue` exist for the cases where `vector` does not fit. For a first semester, treat them as "I will look this up if I need it"; `vector` and `map` cover almost everything.

---

## Algorithms: reusable operations on containers

The `<algorithm>` header contains dozens of free functions that work on *any* container (via iterators). A handful you will reach for repeatedly:

```cpp
#include <algorithm>
#include <numeric>
#include <vector>

std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

std::sort(v.begin(), v.end());            // sort ascending: 1 1 2 3 4 5 6 9

auto it = std::find(v.begin(), v.end(), 4);
if (it != v.end()) {
    // found, *it == 4
}

int count4 = std::count(v.begin(), v.end(), 1);     // 2
int total  = std::accumulate(v.begin(), v.end(), 0); // 31
int maxVal = *std::max_element(v.begin(), v.end());  // 9
```

The `.begin()`/`.end()` pair appears everywhere. It says "operate on this whole range." There are versions that take a custom comparator (for `sort`) or predicate (for `find_if`, `count_if`), letting you decide what "less than" or "matches" means for your data.

---

## Iterators

You may have noticed that every algorithm above took `v.begin()` and `v.end()`, not `v` itself. Those are **iterators** — the standard library's way of referring to a *position* in a container.

Picture an iterator as a bookmark:

- `v.begin()` marks the first element.
- `v.end()` marks *one past* the last — a stop marker, not a real element.
- `*it` reads the element at that position (just like dereferencing a pointer).
- `++it` advances to the next element.

Walking a container by hand looks like this:

```cpp
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << "\n";
}
```

That is exactly what the range-based `for (int x : v)` you already use does under the hood, so you rarely write this loop yourself. But it explains *why* algorithms take a `begin, end` pair rather than the container itself: by speaking only "iterator," one `std::sort` works on a `vector`, an `array`, a `std::string`, or anything that can hand out iterators. The container and the algorithm never have to know about each other — iterators are the glue between them.

---

## Ranges (C++20)

Passing `v.begin(), v.end()` every time is noise; you almost always mean "the whole thing." C++20's **ranges** let you say exactly that. Every algorithm from the previous section has a `std::ranges::` version (in the same `<algorithm>` header) that takes the container directly:

```cpp
std::ranges::sort(v);                  // instead of std::sort(v.begin(), v.end())
auto it = std::ranges::find(v, 4);     // instead of std::find(v.begin(), v.end(), 4)
```

Prefer these in new code — this course uses C++20 — because they are shorter and close a real footgun: you can no longer accidentally pair `begin()` from one container with `end()` from another.

Ranges also add **views** (from `<ranges>`): lazy, composable steps you chain with the `|` pipe. Nothing is computed or copied until you iterate the result.

```cpp
std::vector<int> v = {1, 2, 3, 4, 5, 6};

// the squares of just the even numbers, computed on demand
for (int n : v | std::views::filter([](int x) { return x % 2 == 0; })
                | std::views::transform([](int x) { return x * x; })) {
    std::cout << n << " ";          // 4 16 36
}
```

Those `[](int x) { … }` pieces are [lambdas](../lambdas.md) — small inline functions, covered in detail later in this chapter. Views are powerful and you will meet them more as you go; for now, just recognise the `|` style when you see it, and reach for `std::ranges::sort(v)` and friends to skip the `begin()`/`end()` boilerplate.

---

## Other handy types

### `std::optional<T>`: a value that might be absent

```cpp
#include <optional>

std::optional<int> findReading(int id) {
    if (id < 0) {
        return std::nullopt;   // no reading for an invalid id
    }
    return 42;                 // pretend we found a reading
}

auto r = findReading(7);
if (r) {
    std::cout << *r << "\n";
}
```

Covered in detail in the [error handling chapter](../Chapter6/error_handling.md#stdoptional-when-failure-is-expected).

### `std::chrono`: time and durations

```cpp
#include <chrono>
#include <thread>

auto start = std::chrono::steady_clock::now();
// ... do work ...
auto elapsed = std::chrono::steady_clock::now() - start;
auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count();
std::cout << "took " << ms << " ms\n";

std::this_thread::sleep_for(std::chrono::milliseconds(500));
```

### `std::filesystem`: files and directories

```cpp
#include <filesystem>

namespace fs = std::filesystem;

if (fs::exists("config.txt")) {
    auto size = fs::file_size("config.txt");
}

for (const auto& entry : fs::directory_iterator(".")) {
    std::cout << entry.path() << "\n";
}
```

### `<cmath>`: mathematical functions

```cpp
#include <cmath>

double r = std::sqrt(2.0);
double s = std::sin(3.14159);
double e = std::exp(1.0);
```

---

## The C standard library

`<cmath>` above is one slice of the **C standard library**, which C++ inherits in full. Each C header comes in two spellings: the original C name `<xxx.h>`, and a C++ name `<cxxx>` that provides the same things through the `std::` namespace.

| C header | C++ header | Gives you |
|----------|------------|-----------|
| `<math.h>`   | `<cmath>`   | `std::sqrt`, `std::sin`, `std::pow` |
| `<stdlib.h>` | `<cstdlib>` | `std::abs`, `std::atoi`, `std::rand` |
| `<string.h>` | `<cstring>` | `std::strlen`, `std::memcpy` |
| `<stdint.h>` | `<cstdint>` | `std::uint8_t`, `std::int32_t` |
| `<stdio.h>`  | `<cstdio>`  | `std::printf`, `std::fopen` |

On the desktop, **always prefer the `<cxxx>` form** and write the `std::` names (`std::sqrt`, `std::uint8_t`). It keeps C-library calls consistent with the rest of the standard library; the `<xxx.h>` form drops the same names into the global namespace instead.

(One exception: a small microcontroller often ships only the C `<xxx.h>` headers — there you use `<stdint.h>` and a bare `uint8_t`. See [Arduino vs. Desktop C++](../arduino_vs_desktop.md).)

---

## Streams

C++ I/O is done through stream objects: `std::cout` for console output, `std::cin` for input, `std::ifstream` and `std::ofstream` for files. These get their own treatment in [IO & Streams](../Chapter4/io_streams.md).

---

## How to learn the library

You will not memorise the standard library. Nobody has. What you build over time is **awareness**: you remember that *something* exists for a given task, and you look up the exact spelling on cppreference.

Two habits to start now:

1. **Whenever you are about to write a loop or a utility, check if the standard library already has it.** Counting elements? `std::count`. Removing duplicates? `std::unique`. Sorting? `std::sort`. The library has solved most of the common problems already.
2. **Bookmark [cppreference.com](https://en.cppreference.com/).** Every standard library symbol has a page with signature, behaviour, complexity, examples, and what header to include. It is the most useful single resource in C++.

---

## Summary

- The standard library lives in the `std::` namespace. Always write the prefix.
- `std::vector` is your default container. `std::string` for text. `std::map` / `std::unordered_map` for key-value lookups.
- `<algorithm>` has dozens of functions that work on any container: sort, find, count, accumulate.
- Algorithms reach containers through **iterators** (`begin()`/`end()`); C++20 **ranges** let you pass the container directly — `std::ranges::sort(v)`.
- `<optional>`, `<chrono>`, `<filesystem>`, `<cmath>` cover most everyday needs beyond containers.
- The whole **C standard library** is available; on the desktop prefer the `<cXX>` spelling (`<cmath>`, `<cstdint>`, …) so its names stay behind `std::`.
- Look things up on cppreference instead of memorising signatures.
