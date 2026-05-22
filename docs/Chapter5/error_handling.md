# Error Handling

Programs rarely run in a perfect world. Files go missing, users enter invalid data, network connections drop, and arithmetic can produce impossible results. Writing software means accepting that things _will_ go wrong and deciding in advance what to do about it.

Good error handling separates two distinct responsibilities:

1. **Detection:** recognising that something went wrong.
2. **Recovery:** deciding what to do about it.

Keeping these two concerns separate, often in different parts of your code, leads to cleaner and more maintainable programs.

---

## Return codes: the simple approach

The most straightforward way to signal failure is to return a special value from a function.

```cpp
#include <iostream>

// Returns the result, or -1 to signal an error
int divide(int a, int b) {
    if (b == 0) {
        return -1; // error sentinel
    }
    return a / b;
}

int main() {
    int result = divide(10, 0);
    if (result == -1) {
        std::cout << "Error: division by zero\n";
    }
    return 0;
}
```

This works for simple cases, but has real limitations as programs grow:

- The caller can **silently ignore** the return value, and the error disappears.
- The sentinel value (`-1` here) might also be a legitimate result in other contexts.
- Every call site must check the return value, cluttering the code.
- There is no easy way to carry a descriptive error message alongside the result.

---

## Exceptions: the C++ approach

C++ provides a dedicated mechanism for error handling: **exceptions**. Think of it like a fire alarm: you don't constantly check for fire while cooking, but if the alarm goes off, everyone stops what they are doing and deals with it immediately.

There are three keywords:

| Keyword | Purpose |
|---------|---------|
| `throw` | Signal that something went wrong (pull the alarm) |
| `try`   | Mark a block of code that might fail |
| `catch` | Handle the error when it occurs |

```cpp
#include <iostream>
#include <stdexcept>

int divide(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero is not allowed.");
    }
    return a / b;
}

int main() {
    try {
        int result = divide(10, 0);
        std::cout << "Result: " << result << "\n";
    } catch (const std::invalid_argument& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
```

When `throw` executes, the program immediately stops running the current function and searches up the call stack for a matching `catch` block. This process is called **stack unwinding**: every local object that has gone out of scope has its destructor called along the way (see [RAII](../Chapter3/raii.md)).

> If no matching `catch` is found anywhere in the call stack, the program calls `std::terminate()` and aborts. Always catch exceptions at a level where you can meaningfully handle them.

---

## Standard Exception Types

The C++ Standard Library provides a hierarchy of exception types, all inheriting from `std::exception`. Every standard exception has a `.what()` method that returns a human-readable description of the error.

```cpp
#include <iostream>
#include <stdexcept>

int main() {
    try {
        throw std::runtime_error("Something went wrong at runtime.");
    } catch (const std::exception& e) {
        // Catches any standard exception
        std::cout << "Caught: " << e.what() << "\n";
    }
    return 0;
}
```

Commonly used types from `<stdexcept>`:

| Type | When to use |
|------|-------------|
| `std::runtime_error` | General errors detected during execution |
| `std::invalid_argument` | A function received an argument with an invalid value |
| `std::out_of_range` | An index or value is outside the valid range |
| `std::logic_error` | A bug in program logic (precondition violated) |
| `std::bad_alloc` | Memory allocation with `new` failed |

You can also catch _any_ exception with `catch (...)`, but use this sparingly; it discards all information about the error:

```cpp
try {
    // ...
} catch (const std::exception& e) {
    std::cout << "Standard exception: " << e.what() << "\n";
} catch (...) {
    std::cout << "Unknown exception caught\n";
}
```

---

## Custom Exceptions

For library or application code, you can define your own exception types. Inheriting from `std::runtime_error` is the easiest approach: the constructor takes a message string and `.what()` works automatically.

```cpp
#include <iostream>
#include <stdexcept>
#include <string>

class FileNotFoundError : public std::runtime_error {
public:
    explicit FileNotFoundError(const std::string& filename)
        : std::runtime_error("File not found: " + filename) {}
};

void openFile(const std::string& filename) {
    // Pretend the file does not exist
    throw FileNotFoundError(filename);
}

int main() {
    try {
        openFile("config.txt");
    } catch (const FileNotFoundError& e) {
        std::cout << "Could not open file: " << e.what() << "\n";
    } catch (const std::exception& e) {
        std::cout << "Other error: " << e.what() << "\n";
    }
    return 0;
}
```

Defining your own exception types lets callers catch _specific_ failure modes and handle them differently.

---

## RAII and Exception Safety

You already learned about [RAII](../Chapter3/raii.md). One of its greatest benefits is that it makes code **exception-safe** automatically.

When an exception is thrown, C++ guarantees that the destructors of all local objects are run as the stack unwinds. If a resource (a file, a lock, a heap allocation) is managed by an RAII wrapper, it will be released correctly even if an exception is thrown mid-function.

```cpp
#include <iostream>
#include <fstream>
#include <stdexcept>

void processFile(const std::string& filename) {
    std::ifstream file(filename); // RAII: file closes automatically when `file` leaves scope

    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filename);
    }

    // ... process the file ...

} // `file` destructor closes the file here, even if an exception was thrown above

int main() {
    try {
        processFile("data.txt");
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
```

> **Do not** rely on code _after_ a `throw` statement running. If you need cleanup to happen, put it in a destructor.

---

## `std::optional`: when failure is expected

Sometimes the absence of a result is not an error. It is a normal outcome. For example, searching a list for a value might simply find nothing. Throwing an exception in this case would be misleading, since nothing went wrong.

C++17 introduced `std::optional<T>`, which holds either a value of type `T` or nothing at all (`std::nullopt`).

```cpp
#include <iostream>
#include <optional>
#include <vector>
#include <string>

std::optional<int> findIndex(const std::vector<std::string>& items,
                             const std::string& target) {
    for (int i = 0; i < static_cast<int>(items.size()); ++i) {
        if (items[i] == target) {
            return i; // found, return the index
        }
    }
    return std::nullopt; // not found, no value
}

int main() {
    std::vector<std::string> fruits = {"apple", "banana", "cherry"};

    auto index = findIndex(fruits, "banana");
    if (index) {
        std::cout << "Found at index " << *index << "\n";
    } else {
        std::cout << "Not found\n";
    }

    return 0;
}
```

You can check whether an `optional` holds a value using `if (result)` or `result.has_value()`, and access the value with `*result` or `result.value()`.

> Calling `.value()` on an empty `optional` throws `std::bad_optional_access`. Prefer checking first with `if (result)` before accessing.

---

## Assertions: catching bugs, not handling errors

Not everything that "goes wrong" is an *error* to recover from. Some conditions should be **impossible** if your code is correct — a function receiving an argument the caller promised never to pass, an index the surrounding logic guarantees is valid. When one of those is violated you do not have a bad input to handle gracefully; you have a **bug** to find and fix.

`assert` (from `<cassert>`) is the tool for that. You give it a condition that must be true. If it ever is not, the program prints the failing condition, file, and line, and aborts immediately:

```cpp
#include <cassert>
#include <iostream>

// Precondition: percent must be between 0 and 100
int dutyCycle(int percent) {
    assert(percent >= 0 && percent <= 100);   // a bug if this is ever false
    return percent * 255 / 100;                // scale to the 0–255 range
}

int main() {
    std::cout << dutyCycle(50) << "\n";   // 127
    // dutyCycle(150);  // would abort in a debug build: assertion failed
}
```

The point is to fail **loudly and early**, right where the mistake is, instead of returning a silently wrong value that crashes mysteriously three functions later.

One crucial property: **assertions are removed from release builds.** When the program is compiled with `NDEBUG` defined (the standard "release" setting), every `assert` disappears and costs nothing at runtime. Two rules follow:

- **Never put code with side effects inside an `assert`.** `assert(connect());` would stop connecting in a release build. Assert the *condition*, never an action.
- **Never use `assert` for failures that happen in normal use** — bad user input, a missing file, a dropped connection. Those are *expected*; handle them with exceptions or `std::optional`. `assert` is only for "this cannot happen unless I made a mistake."

### `static_assert`: checks at compile time

A close relative, `static_assert`, checks a condition while the program is *compiling* rather than running. It is for assumptions about types and sizes — handy in portable or embedded code:

```cpp
static_assert(sizeof(int) >= 4, "this code assumes a 32-bit int");
```

If the condition is false the code simply does not compile, and you get the message. There is no runtime cost, because there is no runtime check.

---

## Best Practices

### Throw by value, catch by reference

Always `throw` exception objects by value and `catch` them by `const` reference. This avoids unnecessary copies and prevents object slicing.

```cpp
throw std::runtime_error("something failed"); // throw by value

catch (const std::runtime_error& e) { ... }   // catch by const reference
```

### Exceptions are for exceptional situations

Do not use exceptions to control normal program flow (e.g. exiting a loop). Exceptions are for conditions that represent a failure — something the caller cannot be expected to deal with locally. For expected "no result" situations, prefer `std::optional`.

### Catch at the right level

Catch an exception where you can **meaningfully recover** from it. Catching an exception only to immediately rethrow it (with no recovery logic) adds noise without benefit.

### Choose the right tool

| Situation | Preferred approach |
|-----------|-------------------|
| Function might not find a result (normal case) | `std::optional` |
| Something went wrong that the caller must deal with | Exception |
| Performance-critical code, simple error signaling | Return code or `bool` |
| A condition that should be impossible unless there is a bug | `assert` |

### Use RAII to guarantee cleanup

Never manually call cleanup code (`delete`, `fclose`, etc.) in a `catch` block. You will forget to duplicate it on every code path. Instead, wrap resources in RAII types so they clean themselves up automatically, whether or not an exception is thrown.
