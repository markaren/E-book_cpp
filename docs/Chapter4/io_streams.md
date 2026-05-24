# Input, Output, and File Streams

A **stream** in C++ is an object that data flows through. `std::cout` is the stream connected to your console; `std::cin` is the stream that delivers what the user types; `std::ifstream` is a stream connected to a file you are reading.

The operators `<<` and `>>` move data into and out of streams. Once you know the pattern with `std::cout`, the same shape works for every stream the standard library provides.

---

## Console I/O

Three stream objects, all in `<iostream>`:

| Stream      | Direction      | Purpose                                    |
|-------------|----------------|--------------------------------------------|
| `std::cout` | output         | Print to the console                       |
| `std::cin`  | input          | Read from the console (keyboard, usually)  |
| `std::cerr` | output (error) | Print to the error stream                  |

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int number;
    std::cout << "Enter a number: ";
    std::cin  >> number;
    std::cout << "You entered " << number << "\n";
    return 0;
}
```

`<<` reads "put this *into* the stream"; `>>` reads "extract from the stream *into* this variable." You can chain them; the operators return the stream itself so the next one can be applied immediately.

> **A note on `std::endl` vs `"\n"`:** Both produce a newline. `std::endl` also *flushes* the stream, forcing any buffered output to appear immediately. Flushing is expensive; in tight loops, prefer `"\n"`. Reach for `endl` only when you specifically want to flush.

---

## Reading several values

Stream extraction (`>>`) skips whitespace, so reading several values is just chaining:

```cpp
int a, b;
std::cout << "Enter two integers separated by a space: ";
std::cin >> a >> b;
std::cout << "Sum: " << (a + b) << "\n";
```

The user can type `3 5`, `3<tab>5`, or even press Enter between them; `>>` will pick up both.

### When extraction fails

If the user types `hello` when you asked for an integer, `>>` fails silently; the stream enters an error state and subsequent extractions also fail. You can check the stream like a boolean:

```cpp
int n;
if (!(std::cin >> n)) {
    std::cerr << "That was not a number.\n";
    return 1;
}
```

---

## Reading whole lines

`>>` stops at whitespace. To read an entire line (including spaces) use `std::getline`:

```cpp
#include <string>

std::string name;
std::cout << "What is your name? ";
std::getline(std::cin, name);
std::cout << "Hello, " << name << "!\n";
```

---

## File I/O

Files use the same operators. Three classes in `<fstream>`:

| Class           | Direction | Purpose             |
|-----------------|-----------|---------------------|
| `std::ifstream` | input     | Read from a file    |
| `std::ofstream` | output    | Write to a file     |
| `std::fstream`  | both      | Read and write      |

### Reading a file line by line

<!-- no-ce -->
```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ifstream in("readings.txt");
    if (!in) {
        std::cerr << "Could not open readings.txt\n";
        return 1;
    }

    std::string line;
    while (std::getline(in, line)) {
        std::cout << line << "\n";
    }
    // No explicit close needed, RAII closes the file when `in` goes out of scope.
}
```

The `if (!in)` check uses the stream's bool conversion: a "good" stream is truthy, a stream that failed to open or has hit an error is falsy.

`std::ifstream` is a great example of [RAII](raii.md) in action: opening the file in the constructor, closing it in the destructor. You do not have to remember to call `close()`; it happens automatically, even if an exception is thrown mid-function.

### Writing a file

```cpp
#include <fstream>

std::ofstream out("results.txt");
out << "Mean: "      << mean      << "\n";
out << "Std dev: "   << stddev    << "\n";
// closed automatically when `out` goes out of scope
```

By default `std::ofstream` *truncates* the file; any previous contents are lost. To append instead:

```cpp
std::ofstream out("results.txt", std::ios::app);
```

---

## Printing your own types

`std::cout << myObject;` works for built-in types and most standard library types. For your own classes, you teach the stream how to print them by overloading `operator<<`:

```cpp
#include <iostream>

struct Vector3 {           // a struct is just a class with public members by default
    double x, y, z;
};

std::ostream& operator<<(std::ostream& os, const Vector3& v) {
    os << "Vector3(" << v.x << ", " << v.y << ", " << v.z << ")";
    return os;
}

int main() {
    Vector3 v{1.0, 2.0, 3.0};
    std::cout << v << "\n";   // prints: Vector3(1, 2, 3)
}
```

Two things to notice:

- The first parameter is `std::ostream&` (the base class of `std::cout`, `std::ofstream`, etc.); so the same overload works with any output stream.
- The function returns the stream so that `<<` calls can be chained.

The same pattern with `std::istream&` and `>>` lets you parse your own type from input.

---

## Formatting

For most output, default formatting is fine. When it is not, the `<iomanip>` header has manipulators that change how subsequent values are printed:

```cpp
#include <iomanip>
#include <iostream>

double pi = 3.14159265;

std::cout << std::fixed << std::setprecision(2) << pi << "\n";  // 3.14
std::cout << std::setw(10) << 42 << "\n";                       // "        42"
std::cout << std::hex << 255 << "\n";                            // ff
```

Manipulators are "sticky": once you set them on a stream, they stay set until you change them. If you only need formatting for a single value, save and restore — or, much more cleanly, use `std::format` from `<format>`:

```cpp
#include <format>

std::cout << std::format("{:.2f}\n", pi);          // 3.14
std::cout << std::format("{:>10}\n", 42);          // right-aligned in 10 columns
std::cout << std::format("{:#x}\n", 255);          // 0xff
```

The format string follows Python-style placeholders: `{}` for the next argument, with optional spec after `:`. Prefer this over manipulators when you only need one formatted value; no sticky state to clean up.

`printf`-style formatting from `<cstdio>` is also available, and a common choice in embedded code.

---

## Summary

- `<<` writes to a stream; `>>` reads from one. Both chain.
- `std::cout`, `std::cin`, `std::cerr` are the console streams; `std::ifstream` / `std::ofstream` are file streams.
- Prefer `"\n"` to `std::endl` unless you specifically want to flush.
- `std::getline` reads a whole line including spaces.
- File streams close themselves automatically when they go out of scope (RAII).
- Define `operator<<` for your own classes to make them printable.
