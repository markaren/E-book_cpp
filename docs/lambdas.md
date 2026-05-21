# Lambda Expressions

A **lambda expression** is a function written inline, often used in places where you want to pass behaviour as an argument. They were added in C++11 and are now everywhere, particularly in standard library algorithms, callbacks, and short helper functions that do not deserve their own name.

This page introduces the syntax and the cases where lambdas make code dramatically cleaner.

---

## The motivating example

You have a vector of sensor readings and you want to sort them by absolute value:

```cpp
std::vector<double> readings = {-3.2, 1.0, 4.5, -7.1, 0.5};
```

`std::sort` needs to know what "smaller than" means. The default uses `<`, which would sort `-7.1` first. To sort by *absolute* value, you need to give it a custom comparison.

Without lambdas, you have to write a separate function or a function object:

```cpp
bool compareAbs(double a, double b) {
    return std::abs(a) < std::abs(b);
}

std::sort(readings.begin(), readings.end(), compareAbs);
```

That works, but `compareAbs` is now floating around at namespace scope when it is only used once. With a lambda, the comparison goes right where it is used:

```cpp
std::sort(readings.begin(), readings.end(),
          [](double a, double b) { return std::abs(a) < std::abs(b); });
```

The behaviour you want is right there at the call site. No detour, no naming, no separate function.

---

## Anatomy of a lambda

```cpp
[capture](parameters) -> return_type { body }
```

| Part | What it does |
|------|--------------|
| `[capture]` | Which variables from the enclosing scope the lambda can use |
| `(parameters)` | Like a function's parameter list |
| `-> return_type` | The return type (optional, usually deduced) |
| `{ body }` | The code that runs when the lambda is called |

The simplest form has empty captures and no return type:

```cpp
auto sayHello = []() { std::cout << "Hello\n"; };
sayHello();    // prints Hello
```

The square brackets are what make a lambda a lambda, even an empty `[]` is required.

---

## Captures

Lambdas need a *capture clause* to use variables from the surrounding scope. The clause spells out which variables to bring in and whether to bring them by value or by reference.

```cpp
int threshold = 5;

auto isLarge = [threshold](int x) { return x > threshold; };
//             ^^^^^^^^^^^
//             capture threshold by value, the lambda has its own copy

isLarge(7);   // true
threshold = 100;
isLarge(7);   // still true, the lambda's copy is still 5
```

By reference, with `&`:

```cpp
int count = 0;
auto increment = [&count]() { ++count; };

increment();
increment();
increment();
std::cout << count << "\n";   // 3
```

Two shorthand forms:

| Capture | Meaning |
|---------|---------|
| `[=]` | Capture every used variable by value |
| `[&]` | Capture every used variable by reference |
| `[=, &count]` | Everything by value, but `count` by reference |
| `[&, threshold]` | Everything by reference, but `threshold` by value |

The shorthand forms are convenient but lose precision. Prefer naming the captures explicitly, it documents intent.

> **Beware of `[&]` outliving the captured variables.** A lambda that captures by reference holds references to the variables; if the lambda is stored and called *after* those variables go out of scope, you get a dangling reference. Capture by value when you are not sure.

---

## Where lambdas shine

### Sorting and filtering with `<algorithm>`

```cpp
std::vector<int> v = {5, 2, 8, 1, 9, 3};

// sort descending
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

// count values greater than 4
int n = std::count_if(v.begin(), v.end(), [](int x) { return x > 4; });

// find the first negative reading
auto it = std::find_if(v.begin(), v.end(), [](int x) { return x < 0; });
```

This is the most common use of lambdas in everyday C++. Any algorithm with a `_if` suffix takes a predicate; lambdas make those predicates concise.

### Transforming a container

```cpp
#include <algorithm>

std::vector<double> celsius = { -10, 0, 22, 37 };
std::vector<double> fahrenheit(celsius.size());

std::transform(celsius.begin(), celsius.end(),
               fahrenheit.begin(),
               [](double c) { return c * 9.0 / 5.0 + 32.0; });
```

### Short callbacks

When a library takes a function for you to call back with, a lambda is usually cleaner than a named function:

```cpp
button.setOnClick([&](){ count++; updateDisplay(); });
```

---

## Storing lambdas

Two ways:

**`auto`**, when you store and use the lambda in the same scope:

```cpp
auto add = [](int a, int b) { return a + b; };
int sum = add(2, 3);
```

Each lambda has a unique compiler-generated type. You cannot write the type out by hand, which is why `auto` is the natural fit.

**`std::function<...>`**, when you need to store lambdas of the same call signature in a container, or hand one across an API boundary:

```cpp
#include <functional>

std::vector<std::function<int(int, int)>> ops;
ops.push_back([](int a, int b) { return a + b; });
ops.push_back([](int a, int b) { return a - b; });

for (const auto& op : ops) {
    std::cout << op(10, 3) << "\n";   // 13, then 7
}
```

`std::function` is more flexible but has a small runtime overhead (a virtual call). Reach for it when `auto` does not work; default to `auto`.

---

## A short worked example

Process a list of sensor readings, keeping only the valid ones and computing the mean:

```cpp
#include <algorithm>
#include <numeric>
#include <vector>
#include <iostream>

int main() {
    std::vector<double> readings = {22.5, -999.0, 23.1, 22.9, -999.0, 23.0};
    const double sentinel = -999.0;

    // remove sentinel values
    readings.erase(
        std::remove_if(readings.begin(), readings.end(),
                       [sentinel](double v) { return v == sentinel; }),
        readings.end());

    if (readings.empty()) {
        std::cout << "no valid readings\n";
        return 0;
    }

    double sum  = std::accumulate(readings.begin(), readings.end(), 0.0);
    double mean = sum / static_cast<double>(readings.size());
    std::cout << "mean: " << mean << "\n";
}
```

Both lambdas are tiny and live exactly where they are used. The intent reads top-to-bottom without you having to chase function definitions across the file.

---

## Summary

- A lambda is an inline function with an explicit list of captured variables.
- Syntax: `[captures](params) { body }`, the brackets are what make it a lambda.
- Capture by value (`[x]`), by reference (`[&x]`), or implicitly (`[=]` or `[&]`).
- Pair them with `<algorithm>`, `sort`, `find_if`, `count_if`, `transform`, for clean, expressive code.
- Store small lambdas with `auto`; reach for `std::function` only when you need type erasure.
- Capturing by reference is dangerous if the lambda outlives the captured variables.
