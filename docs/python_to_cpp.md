# Coming from Python

Most of you have written some Python before reaching C++, and that is a real head start: the logic of programming — variables, loops, functions, conditions — carries straight across. What changes is everything *underneath*. Python hides the machine from you; C++ hands you the controls. Almost every difference on this page flows from that one fact.

This is not a syntax dictionary. The aim is to adjust your **mental model** and to warn you about the *false friends* — code that looks like Python but behaves differently. (When a concept will not click, the [AI tip](using_ai.md) "explain this in C++ as if I have used Python" is genuinely useful.)

---

## False friends

These are the ones that catch Python programmers out:

| In Python… | …but in C++ |
|------------|-------------|
| `b = a` makes `b` *refer to* the same object | `b = a` makes `b` a **full copy** |
| `10 / 3` is `3.333…` | `10 / 3` is `3` (integer division) |
| a variable can change type (`x = 5`, then `x = "hi"`) | a variable's **type is fixed** at declaration |
| indentation defines blocks | blocks are `{ }`; statements end in `;`; indentation is ignored |
| `if xs:` is false for an empty list | containers have no truthiness — write `if (xs.empty())` |
| `None` means "nothing" | `nullptr` (a pointer to nothing) or [`std::optional`](Chapter5/error_handling.md#stdoptional-when-failure-is-expected) (a missing value) |
| `len(xs)` | `xs.size()` |
| `int` grows without limit | `int` is fixed-width and **overflows silently** |
| `print(obj)` always prints *something* (your own types get a default placeholder) | `std::cout << obj` **won't compile** for your own types until you define an [`operator<<`](Chapter3/io_streams.md) |

---

## The big one: assignment copies

In Python, names are labels stuck onto objects. `b = a` puts a second label on the *same* list, so changing `b` also changes `a`. In C++, a variable *is* its value, and `b = a` **copies** it:

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = a;   // a full, independent copy — not an alias

    b.push_back(4);           // change b only

    std::cout << "a has " << a.size() << " elements\n";  // 3
    std::cout << "b has " << b.size() << " elements\n";  // 4
}
```

In Python the equivalent would leave *both* at length 4. This **value semantics** is the single biggest adjustment. Having two names refer to the same object is Python's default. In C++ you ask for it explicitly, with a reference (`&`) or a pointer. See [Values, References, and Pointers](Chapter3/types_refs_ptrs.md).

---

## Types are fixed, and checked before the program runs

You declare a type, and it does not change:

```cpp
int count = 0;
count = "three";   // compile error — not a runtime surprise
```

`auto` lets the compiler *deduce* the type, but it is still fixed once deduced — `auto` is **not** Python's dynamic typing:

```cpp
auto name = "Ada";   // type is deduced once, then fixed
```

The payoff: a whole category of Python's runtime `TypeError`s become **compile errors** you fix before the program ever runs. See [Compiled, statically typed](Chapter1/introduction.md) and [Variables](Chapter1/variables.md).

---

## Numbers behave differently

Two surprises worth knowing on day one:

- **Integer division truncates.** `10 / 3` is `3`, because both operands are `int`. Make one a `double` (`10.0 / 3`) to get `3.333…`. Python's `/` is always floating-point; its `//` is the equivalent of C++'s integer division. See [Operators and Expressions](Chapter1/operators_expressions.md).
- **Integers overflow.** A C++ `int` holds roughly ±2 billion; Python integers grow without limit. Go past the range and a C++ `int` silently wraps around. For most automation work `int` is fine — just know the edge exists.

---

## Nothing is cleaned up "later"

Python frees memory whenever its garbage collector gets around to it. C++ destroys each object **deterministically**, the moment it goes out of scope — that is [RAII](Chapter3/raii.md), and it is why you never call a "free" yourself. The flip side: a reference or pointer to something that has *already* gone out of scope is a classic C++ crash, with no Python equivalent. See [the lifetime trap](Chapter3/types_refs_ptrs.md#the-big-lifetime-trap).

---

## Loops, collections, and "comprehensions"

| Python | C++ |
|--------|-----|
| `for x in xs:` | `for (int x : xs)` — see [Control Statements](Chapter1/control_statements.md) |
| `for i in range(n):` | `for (int i = 0; i < n; ++i)` |
| `list` | [`std::vector`](Chapter2/standard_library.md) |
| `dict` | `std::map` / `std::unordered_map` |
| `[f(x) for x in xs]` | `std::transform`, or a plain loop — see [Lambdas](lambdas.md) |

---

## Do not write Python in C++

The goal is not to translate Python line by line; it is to write *C++*. A few habits mark the shift:

- **Embrace copies and `const`.** Pass and return by value; reach for references or pointers only when you mean to share, or to avoid copying something large.
- **Let scope manage lifetimes** (RAII) instead of scattering pointers to recreate Python's aliasing.
- **Use real types** — [`enum class`](Chapter1/enums.md) and small classes — rather than passing around strings and magic numbers.
- **Lean on the compiler.** Turn warnings on; the errors it reports *before* the program runs are doing work Python only does at runtime.

---

## Summary

- Python hides the machine; C++ shows it — most differences follow from that.
- `b = a` **copies** in C++; aliasing is something you ask for explicitly, with references or pointers.
- Types are declared and fixed, so many Python runtime errors become C++ compile errors.
- `10 / 3` is `3`, and `int` is fixed-width and can overflow.
- Objects are destroyed deterministically at the end of their scope (RAII) — but a reference to a destroyed object crashes.
- Write C++, not transliterated Python: values and `const` by default, real types, and compiler warnings on.
