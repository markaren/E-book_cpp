# Testing

Imagine sending an important email before proof-reading it, only to spot the mistake the moment it lands in someone's inbox. Testing is the habit of checking your work *before* it ships. In software, that means writing small, automated checks that verify individual pieces of code do exactly what they are supposed to do.

A **unit test** is a program that calls your code, gives it specific inputs, and asserts that the output matches what you expect. If it does, the test passes. If not, the test fails, and you know exactly where to look.

Benefits you will notice quickly:

- Catch bugs before they reach other parts of the program.
- Change code confidently: if you break something, a test tells you immediately.
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
cmake_minimum_required(VERSION 3.16)
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

Create `tests/test_calculator.cpp`. The macros these tests use — `TEST_CASE`, `REQUIRE`, `CHECK`, `REQUIRE_THROWS` — all live in one Catch2 header:

```cpp
#include <catch2/catch_test_macros.hpp>
```

On top of that you `#include` whatever you are testing (here, `calculator.hpp` — see the complete file below). Catch2 keeps more advanced tools, such as matchers and generators, in separate headers, but you will not need those yet.

### Core macros

| Macro | Behaviour |
|-------|-----------|
| `TEST_CASE("description")` | Declares a named, independent test |
| `REQUIRE(expression)` | Asserts `expression` is true; stops the test immediately on failure |
| `CHECK(expression)` | Asserts `expression` is true; continues running even on failure |
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

Each `TEST_CASE` is independent: it creates its own `Calculator` object and runs from scratch.

---

## Running the Tests

Build and run your tests with CMake the same way you build any project:

```bash
cmake -S . -B build
cmake --build build
```

**Option 1: run the test binary directly.**

```bash
./build/tests
```

Catch2 prints a line per test and a summary at the end:

```
===============================================================================
All tests passed (11 assertions in 5 test cases)
```

If a test fails, it shows the exact line and the values that did not match:

```
test_calculator.cpp:8: FAILED:
  REQUIRE( calc.add(2.0, 3.0) == 6.0 )
with expansion:
  5.0 == 6.0
```

**Option 2: use CTest** (the CMake test runner):

```bash
ctest --test-dir build
```

CTest is the standard way to run tests in CMake projects and what most automated build systems (CI pipelines) use.

> To register your test executable with CTest, add `include(CTest)` and `add_test(NAME tests COMMAND tests)` to your CMakeLists.txt after the `add_executable` line.

---

## `SECTION`: grouping related checks

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

**Test error cases.** If your code is supposed to throw (or return an error), write a test that verifies it actually does.

**Keep tests independent.** No test should rely on another test running first, or on any global state left over from a previous test. Independent tests can run in any order and still give correct results.

**Name tests like sentences.** `"division by zero throws an exception"` is far more useful than `"test3"` when a test fails at 2 a.m. on a deadline.

---

## Test behaviour, not implementation

A test should pin down *what* your code does — its observable behaviour through its public interface — not *how* it does it inside. Test that `divide(10, 2)` returns `5`; do not try to check which private variable it touched along the way.

The reason is that **behaviour is the promise; the internals are free to change.** A test written against behaviour survives a rewrite — you can replace the insides completely, and as long as the result is unchanged, the test still passes and still protects you. A test welded to the internals breaks every time you tidy the code, and a suite that fails on harmless refactors is one people quietly stop trusting.

---

## What about private functions?

This is the question that comes up most: *how do I test a private member function?* You cannot call it from a test — that is what `private` means — and the instinct is to make it public, or reach in with a trick. Resist it. The honest answers, in order of preference:

1. **Test it through the public functions that use it.** A private helper exists to serve the public interface; exercise that interface thoroughly and the private code runs as part of it.
2. **If a private is complex enough to deserve its own tests, that is a signal — extract it into its own unit.** Pull the logic out into a free function (or a small separate class). Now it is public, pure, and trivially testable, and the original class is simpler too:

```cpp
// Before: a tricky calculation hidden in a private method — awkward to test
class Thermostat {
public:
    void update(int raw) { latest_ = toCelsius(raw); }
private:
    double toCelsius(int raw) const { return (raw * 5.0 / 1023.0 - 0.5) * 100.0; }
    double latest_ = 0.0;
};

// After: the calculation is a free function — public, pure, easy to test
double rawToCelsius(int raw) {
    return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
}

class Thermostat {
public:
    void update(int raw) { latest_ = rawToCelsius(raw); }
private:
    double latest_ = 0.0;
};
```

A test for `rawToCelsius` just passes a number and checks the result — no object, no hidden state. The pull to test a private is usually the code telling you that a piece of it wants to be a unit of its own.

You may have seen tricks for reaching into a class's private members — a `friend` declaration, or `#define private public` before the `#include`. They compile, but they bolt your tests onto the very internals you are trying to keep free to change, so a behaviour-preserving refactor can still break them. Prefer the two options above.

---

## Testable code is well-designed code

Here is the part that surprises people: the hardest thing about testing is usually not writing the test — it is the *code*. When a function is painful to test, that difficulty is information about the **design**, not the test. The common causes:

- **It does too many things at once** — low **cohesion**. A function that reads a sensor, converts units, *and* writes a file forces you to set up all three before you can check any one. Split it.
- **It reaches out to hardware, files, the clock, or the network** — tight **coupling**, with hidden inputs. The fix is **dependency injection**: take those dependencies in (as parameters, or behind an interface) instead of creating them inside, so a test can pass a fake — worth seeing in full, next.
- **It depends on [global state](../Chapter1/functions.md#global-variables).** A global is an invisible input and a shared output: tests of code that touches one interfere with each other and turn fragile.

Code that is easy to test is almost always small, focused, and loosely coupled — the very properties the Separation of Concerns chapter argues for on their own merits. So tests are not only a safety net for catching bugs; **writing them early is a design tool.** When something resists testing, treat it as an alarm and fix the *design*, not the test. Getting the tests right and getting the structure right turn out to be the same job.

---

## Injecting a fake

Take a `FrostAlarm` that decides whether it is freezing. If it reached out and read a real thermometer itself, it would be welded to hardware — untestable without a cold room. So instead it depends on a small interface, and whoever creates it supplies the thermometer:

```cpp
class Thermometer {
public:
    virtual ~Thermometer() = default;
    virtual double celsius() = 0;
};

class FrostAlarm {
public:
    explicit FrostAlarm(Thermometer& thermometer) : thermometer_(thermometer) {}

    bool triggered() { return thermometer_.celsius() < 0.0; }

private:
    Thermometer& thermometer_;
};
```

In the real program you hand `FrostAlarm` a thermometer that reads a pin. In a test you hand it a **fake** — one that returns whatever value the test needs, with no hardware in sight:

```cpp
class FakeThermometer : public Thermometer {
public:
    explicit FakeThermometer(double value) : value_(value) {}
    double celsius() override { return value_; }
private:
    double value_;
};

TEST_CASE("the alarm fires below freezing") {
    FakeThermometer cold(-5.0);
    FrostAlarm alarm(cold);
    REQUIRE(alarm.triggered());
}

TEST_CASE("the alarm stays quiet above freezing") {
    FakeThermometer warm(5.0);
    FrostAlarm alarm(warm);
    REQUIRE(!alarm.triggered());
}
```

Because `FrostAlarm` is *handed* its thermometer instead of building one, the test can slot in a `FakeThermometer` and drive it to any temperature — just below freezing, just above — instantly and repeatably. That hand-it-in move is **dependency injection** (the same technique [Separation of Concerns](soc.md) uses to keep `monitorLoop` independent of any one sensor), and it is what makes hardware-facing code testable at all. A fake that simply returns canned values like this is the simplest kind of *test double*; you will hear "stub" and "mock" for richer ones, but a plain fake covers most of what you need early on.
