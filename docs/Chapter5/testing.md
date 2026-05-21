# Testing

Imagine sending an important email before proof-reading it, only to spot the mistake the moment it lands in someone's inbox. Testing is the habit of checking your work *before* it ships. In software, that means writing small, automated checks that verify individual pieces of code do exactly what they are supposed to do.

A **unit test** is a program that calls your code, gives it specific inputs, and asserts that the output matches what you expect. If it does, the test passes. If not, the test fails, and you know exactly where to look.

Benefits you will notice quickly:

- Catch bugs before they reach other parts of the program.
- Change code confidently, if you break something, a test tells you immediately.
- Tests double as documentation: they show *how* a function is meant to be used.

---

## Introducing Catch2

**Catch2** is a popular C++ testing framework. It lets you write tests in plain C++ without needing to write a `main()` function yourself. Catch2 provides that for you.

Why Catch2?

- Test code reads like plain English: `REQUIRE(result == 5)`.
- Integrates naturally with CMake.
- Widely used in industry and open-source projects.

---

## Project Setup

A project with tests uses a small, standard layout that you already saw in the [CMake introduction](../Chapter2/cmake_intro.md):

```
MyProject/
├── CMakeLists.txt
├── include/
│   └── calculator.hpp
├── src/
│   └── calculator.cpp
└── tests/
    └── test_calculator.cpp
```

### CMakeLists.txt

Catch2 must be downloaded and linked before your tests can use it. The snippet below uses `FetchContent`, a CMake feature that handles this automatically.

> We will cover dependency management in depth in a later chapter. For now, you can use this CMakeLists.txt as a ready-made template for any project that uses Catch2.

```cmake
cmake_minimum_required(VERSION 3.14)
project(MyProject)

set(CMAKE_CXX_STANDARD 20)

# --- Fetch Catch2 from GitHub ---
include(FetchContent)
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

# --- Your library (the code being tested) ---
add_library(calculator src/calculator.cpp)
target_include_directories(calculator PUBLIC include)

# --- Test executable ---
add_executable(tests tests/test_calculator.cpp)
target_link_libraries(tests PRIVATE calculator Catch2::Catch2WithMain)
```

The key line is `target_link_libraries(tests PRIVATE calculator Catch2::Catch2WithMain)`. It links your code and Catch2 (including its built-in `main()`) into a single test binary.

---

## The Class Under Test

Before writing tests, you need something to test. Here is a simple `Calculator` class with four operations. Division throws a `std::invalid_argument` when the divisor is zero, a pattern you saw in the [error handling](error_handling.md) chapter.

**`include/calculator.hpp`**

```cpp
#pragma once
#include <stdexcept>

class Calculator {
public:
    double add(double a, double b);
    double subtract(double a, double b);
    double multiply(double a, double b);
    double divide(double a, double b);
};
```

**`src/calculator.cpp`**

```cpp
#include "calculator.hpp"

double Calculator::add(double a, double b) {
    return a + b;
}

double Calculator::subtract(double a, double b) {
    return a - b;
}

double Calculator::multiply(double a, double b) {
    return a * b;
}

double Calculator::divide(double a, double b) {
    if (b == 0) {
        throw std::invalid_argument("Cannot divide by zero.");
    }
    return a / b;
}
```

---

## Writing Tests with Catch2

Create `tests/test_calculator.cpp`. The only header you need is:

```cpp
#include <catch2/catch_test_macros.hpp>
```

### Core macros

| Macro | Behaviour |
|-------|-----------|
| `TEST_CASE("description")` | Declares a named, independent test |
| `REQUIRE(expression)` | Asserts `expression` is true, stops the test immediately on failure |
| `CHECK(expression)` | Asserts `expression` is true, continues running even on failure |
| `REQUIRE_THROWS(expression)` | Asserts that `expression` throws any exception |

### A complete test file

```cpp
#include <catch2/catch_test_macros.hpp>
#include "calculator.hpp"

TEST_CASE("addition returns the correct sum") {
    Calculator calc;
    REQUIRE(calc.add(2.0, 3.0) == 5.0);
    REQUIRE(calc.add(-1.0, 1.0) == 0.0);
    REQUIRE(calc.add(0.0, 0.0) == 0.0);
}

TEST_CASE("subtraction returns the correct difference") {
    Calculator calc;
    REQUIRE(calc.subtract(10.0, 4.0) == 6.0);
    REQUIRE(calc.subtract(0.0, 5.0) == -5.0);
}

TEST_CASE("multiplication returns the correct product") {
    Calculator calc;
    REQUIRE(calc.multiply(3.0, 4.0) == 12.0);
    REQUIRE(calc.multiply(-2.0, 5.0) == -10.0);
    REQUIRE(calc.multiply(0.0, 99.0) == 0.0);
}

TEST_CASE("division returns the correct quotient") {
    Calculator calc;
    REQUIRE(calc.divide(10.0, 2.0) == 5.0);
    REQUIRE(calc.divide(7.0, 2.0) == 3.5);
}

TEST_CASE("division by zero throws an exception") {
    Calculator calc;
    REQUIRE_THROWS(calc.divide(10.0, 0.0));
}
```

Each `TEST_CASE` is independent, it creates its own `Calculator` object and runs from scratch.

---

## Running the Tests

Build and run your tests with CMake the same way you build any project:

```bash
cmake -S . -B build
cmake --build build
```

**Option 1, run the test binary directly:**

```bash
./build/tests
```

Catch2 prints a line per test and a summary at the end:

```
===============================================================================
All tests passed (9 assertions in 5 test cases)
```

If a test fails, it shows the exact line and the values that did not match:

```
test_calculator.cpp:8: FAILED:
  REQUIRE( calc.add(2.0, 3.0) == 6.0 )
with expansion:
  5.0 == 6.0
```

**Option 2, use CTest** (the CMake test runner):

```bash
ctest --test-dir build
```

CTest is the standard way to run tests in CMake projects and what most automated build systems (CI pipelines) use.

> To register your test executable with CTest, add `include(CTest)` and `add_test(NAME tests COMMAND tests)` to your CMakeLists.txt after the `add_executable` line.

---

## SECTION. Grouping Related Checks

When multiple checks share setup code, you can group them using `SECTION`. Each `SECTION` runs independently, but all share the same `TEST_CASE` setup at the top.

```cpp
TEST_CASE("multiplication handles various inputs") {
    Calculator calc;

    SECTION("positive numbers") {
        REQUIRE(calc.multiply(2.0, 3.0) == 6.0);
        REQUIRE(calc.multiply(10.0, 10.0) == 100.0);
    }

    SECTION("one factor is zero") {
        REQUIRE(calc.multiply(0.0, 42.0) == 0.0);
        REQUIRE(calc.multiply(42.0, 0.0) == 0.0);
    }

    SECTION("negative numbers") {
        REQUIRE(calc.multiply(-2.0, 3.0) == -6.0);
        REQUIRE(calc.multiply(-2.0, -3.0) == 6.0);
    }
}
```

The `Calculator calc;` line runs once for each section, giving every section a fresh object.

---

## What Makes a Good Test?

**Test one thing per `TEST_CASE`.** A test named `"addition returns the correct sum"` should only test addition. If it fails, you know exactly what broke.

**Test the edges, not just the middle.** Zero, negative numbers, empty strings, and maximum values are where bugs hide. Happy-path tests alone miss most real problems.

**Test error cases.** If your code is supposed to throw, or return an error, write a test that verifies it actually does.

**Keep tests independent.** No test should rely on another test running first, or on any global state left over from a previous test. Independent tests can run in any order and still give correct results.

**Name tests like sentences.** `"division by zero throws an exception"` is far more useful than `"test3"` when a test fails at 2 a.m. on a deadline.
