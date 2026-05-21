# Variables and Basic Types

A **variable** is a named piece of memory that holds a value. When you write `int age = 25;`, you tell the compiler: "set aside enough memory to hold an integer, call it `age`, and store `25` in it."

In C++ every variable has a **type** that is fixed for its entire lifetime. You declare the type up front; you cannot later store a string in a variable declared `int`. This is what makes C++ a **statically typed** language.

---

## Built-in types

The types you will use day-to-day:

| Type     | Holds                                | Typical size | Example value |
|----------|--------------------------------------|--------------|---------------|
| `bool`   | true or false                        | 1 byte       | `true`        |
| `char`   | a single character                   | 1 byte       | `'A'`         |
| `int`    | whole numbers                        | 4 bytes      | `42`          |
| `double` | decimal numbers (floating point)     | 8 bytes      | `3.14159`     |
| `float`  | decimal numbers, less precision      | 4 bytes      | `3.14f`       |

Prefer `int` for whole numbers and `double` for decimal numbers unless you have a specific reason to do otherwise (`float` for memory-constrained embedded code, for instance). Sizes are typical for desktop platforms — they can differ on microcontrollers.

The standard library adds a few more types you will use constantly. They are not "built in" but they are everywhere:

| Type          | Holds                       | Header        |
|---------------|-----------------------------|---------------|
| `std::string` | text — see [Strings reference](../strings.md) | `<string>`    |
| `std::vector` | a resizable list of values  | `<vector>`    |

For a complete reference, see [cppreference's entry on Fundamental types](https://en.cppreference.com/w/cpp/language/types).

---

## Declaring and initialising

You can declare a variable and assign to it in one step (recommended) or split it into two:

```cpp
int quantity = 10;       // declare and initialise — preferred
double price{5.99};      // braces also work, and are stricter about conversions

int count;               // declare only — `count` now holds a garbage value
count = 5;               // assign later
```

**Always initialise variables when you declare them.** Reading from an uninitialised variable is **undefined behaviour** — the program might print garbage, might crash, might appear to work fine and then break on a different compiler. The compiler will not warn you in every case.

```cpp
int x;                       // uninitialised
std::cout << x * 2 << "\n";  // undefined behaviour — never do this
```

Two extra reasons to initialise eagerly:

- The initial value documents what the variable is *for*. `int retries = 0;` tells the reader something `int retries;` does not.
- If you do not have a sensible initial value yet, that is usually a sign the variable should be declared later — closer to where it is actually used.

### Brace initialisation

You will see two ways to initialise:

```cpp
int a = 10;   // copy initialisation
int b{10};    // brace (uniform) initialisation
```

Both work. Brace initialisation is stricter: it refuses **narrowing conversions** that silently lose information.

```cpp
int    a = 3.7;   // compiles — silently truncates to 3
int    b{3.7};    // compile error — narrowing from double to int
```

For numeric types it is up to you. For class types (which you will meet in Chapter 3) brace initialisation often does the right thing more reliably.

---

## Type inference with `auto`

Sometimes the type is obvious from the right-hand side and writing it out is just noise:

```cpp
std::vector<int> numbers = {1, 2, 3, 4, 5};

// Without auto:
std::vector<int>::iterator it = numbers.begin();

// With auto — the compiler figures out the type from numbers.begin():
auto it = numbers.begin();
```

`auto` lets the compiler deduce the type for you. It is not "dynamic typing" — the type is still fixed and checked at compile time. Use `auto` when the type is verbose or when the exact type does not matter to the reader; spell it out when the explicit type helps clarity.

---

## Naming variables

A name can contain letters, digits, and underscores, and must start with a letter or underscore. Names are case-sensitive: `count` and `Count` are different variables.

Two conventions used throughout this book:

- Local variables and function parameters: `lowerCamelCase` — `maxSpeed`, `sensorIndex`.
- Constants and macros: `UPPER_SNAKE_CASE` — `MAX_RETRIES`.

Pick descriptive names. `int x` is fine for a loop counter; `int maxAllowedTemperature` is far better than `int t` if that is what the variable means.

---

## Constants

If a value should never change after it is set, mark it `const`:

```cpp
const int maxRetries = 5;
maxRetries = 10; // compile error — cannot assign to const
```

The compiler enforces this, which catches a class of bugs and also documents intent: "this is a value, not a setting."

---

## Summary

- Every variable has a type, fixed at declaration.
- Always initialise — uninitialised reads are undefined behaviour.
- Prefer `int` and `double` for arithmetic. Use `bool` for true/false. Use `std::string` for text.
- Use `const` for values that should not change.
- Pick descriptive names.

Scope — the region in which a variable exists — was covered in [Basic Structure](basic_structure.md). The short version: variables declared in a block disappear when the block ends.
