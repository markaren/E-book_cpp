# Templates

A **template** is a blueprint for a function or class that works with *any* type. The compiler stamps out a specific version every time you use it with a new type, so `std::vector<int>` and `std::vector<double>` are two genuinely different types, both generated from the same template.

You have already been using templates all along. `std::vector`, `std::array`, `std::unique_ptr`, `std::optional`, `std::map` — every one of them is a class template parameterised by the type of value it holds. This chapter explains how the mechanism works and how to write your own.

---

## Function templates

Suppose you write an `add` function for integers:

```cpp
int add(int a, int b) { return a + b; }
```

You quickly want to add doubles too. Without templates, you would write a second function (overloading):

```cpp
int    add(int    a, int    b) { return a + b; }
double add(double a, double b) { return a + b; }
```

With templates, you write the function *once* and let the compiler generate as many versions as you need:

```cpp
template <typename T>
T add(T a, T b) {
    return a + b;
}

int    sumInt    = add(5, 3);        // T is int   , instantiates add<int>
double sumDouble = add(2.5, 3.7);    // T is double, instantiates add<double>
```

The `template <typename T>` line says: "what follows is a blueprint with a placeholder named `T`." When you call `add(5, 3)`, the compiler deduces `T = int`, generates `add<int>(int, int)`, and uses that. When you call `add(2.5, 3.7)`, it generates and uses `add<double>(double, double)`. Two genuinely different functions, both written once.

You can also be explicit about the type when deduction would be wrong or ambiguous:

```cpp
auto x = add<double>(5, 3);   // forces double; x is 8.0, not 8
```

> `typename` and `class` mean the same thing in this context; `template <class T>` is equivalent to `template <typename T>`. `typename` is slightly more modern and is what this book uses.

---

## Class templates

The same idea applies to classes. A simple wrapper:

```cpp
template <typename T>
class Box {
public:
    explicit Box(T value) : value_(std::move(value)) {}

    const T& get() const { return value_; }
    void     set(T v)    { value_ = std::move(v); }

private:
    T value_;
};

Box<int>         boxOfInt(42);
Box<std::string> boxOfText("hello");
```

`Box<int>` and `Box<std::string>` are two completely different types generated from the same template. Each one is exactly as efficient as if you had written it by hand.

Class templates can have multiple parameters. `std::array` is parameterised by both its element type *and* its compile-time size:

```cpp
template <typename T, std::size_t N>
class array { /* ... */ };

std::array<int, 5>      readings;          // 5 ints
std::array<double, 100> moreReadings;      // 100 doubles
```

`std::map` is parameterised by key type *and* value type:

```cpp
std::map<std::string, int> wordCounts;
```

Whenever you see angle brackets in C++, you are looking at a template being instantiated.

---

## Why use templates?

| Benefit | What it means |
|---------|---------------|
| **Reuse** | Write the algorithm or container once; it works with any type that supports the operations you use. |
| **Performance** | Templates are resolved entirely at compile time. There is no runtime cost; `add<int>` compiles to the same machine code as a hand-written integer `add`. |
| **Type safety** | The compiler still checks every type. `add<int>("hello", 3)` does not compile. |

The cost is compile time: every template instantiation is essentially a fresh round of compilation. Heavy template use makes builds slower.

---

## `auto` and template argument deduction

`auto` is the lightweight cousin of templates. It lets the compiler deduce the type of a variable from its initialiser:

```cpp
auto i = 42;            // int
auto x = 3.14;          // double
auto name = std::string("Alice");

std::vector<int> v{1, 2, 3};
auto it = v.begin();    // std::vector<int>::iterator, saved you a lot of typing
```

For range-based `for` loops, `auto` and `const auto&` are by far the most common forms:

```cpp
for (const auto& value : v) {
    std::cout << value << "\n";
}
```

`auto` does not change anything about how C++ types work; the type is still fixed and checked at compile time, the compiler just figures it out for you. It is the same machinery templates use, applied to one variable at a time.

---

## What template errors look like

The single most intimidating thing about templates is their compile errors. A wrong type passed to `std::sort` can produce a screenful of jargon mentioning iterators, type traits, and SFINAE.

Take a simple mistake:

<!-- no-ce -->
```cpp
template <typename T>
T add(T a, T b) { return a + b; }

int main() {
    std::string s = "x";
    add(s, 5);              // error, T cannot be both std::string and int
}
```

GCC will emit something like:

```
error: no matching function for call to 'add(std::string&, int)'
note:   candidate template ignored: deduced conflicting types for parameter 'T'
        ('std::__cxx11::basic_string<char>' vs. 'int')
```

The wall of text is the compiler listing every candidate it considered and why it rejected each one. Two reading tips that handle 90% of cases:

1. **Read from the top.** The first line is the original error in your code. Everything below is the compiler explaining its reasoning.
2. **Look for `note: candidate template ignored:`.** That line tells you *why* a template was rejected: usually a type mismatch like the one above.

Most "scary" template errors are really just type mismatches with a lot of supporting detail. Once you've decoded a few you stop being afraid of the rest.

---

## Lambdas: templates' close cousin

Many of the algorithms templates power (`std::sort`, `std::find_if`, `std::count_if`) take a function argument. **Lambda expressions** are how you write those function arguments inline:

```cpp
std::vector<int> v = {5, 2, 8, 1, 9, 3};
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });   // descending
```

See the [Lambda Expressions](../lambdas.md) reference for the full story.

---

## When to write a template yourself

For small course projects you mostly *use* templates rather than write them. Two cases where writing one is genuinely the right tool:

- **A container that should hold any type.** A custom ring buffer, a thread-safe queue, a fixed-size matrix — all naturally generic.
- **An algorithm that doesn't care about the element type.** A `sum`, `clamp`, `find_max`, etc.

If you are writing the same function with `int`, then with `double`, then with `float`, you have a template waiting to be written.

---

## Summary

- A template is a blueprint; the compiler stamps out concrete versions for each type you use.
- Function templates eliminate near-identical overloads.
- Class templates are what every standard container is built on.
- `auto` is the everyday face of the same type-deduction machinery.
- Template error messages are long but mechanical: read from the top, look for the "candidate ignored" notes.
- Write your own template when you find yourself duplicating code that differs only in the type involved.
