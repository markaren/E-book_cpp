# Operators and Expressions

An **expression** is anything that evaluates to a value: a literal like `42`, a variable name, a function call, or some combination of these joined by **operators**.

```cpp
int x = 10;
int y = 5;
int sum = x + y;       // expression: x + y → 15
bool ok  = (sum > 10); // expression: sum > 10 → true
```

This chapter covers the operators you will use day-to-day, and the rule that decides what happens when several of them appear in the same expression.

---

## Arithmetic

| Operator | Meaning             | Example          | Result |
|----------|---------------------|------------------|--------|
| `+`      | addition            | `5 + 3`          | `8`    |
| `-`      | subtraction         | `5 - 3`          | `2`    |
| `*`      | multiplication      | `5 * 3`          | `15`   |
| `/`      | division            | `10 / 3`         | `3` (with `int`) or `3.333…` (with `double`) |
| `%`      | remainder (modulo)  | `10 % 3`         | `1`    |

**Integer division truncates.** This is the single most common arithmetic surprise:

```cpp
int    a = 10 / 3;        // 3, fractional part discarded
double b = 10 / 3;        // still 3.0!, division happens in int, then converted
double c = 10.0 / 3;      // 3.333…, at least one operand is double
```

If you want a decimal result, at least one operand must be a `double` or `float`.

`%` (modulo) only works on integer types. `10 % 3` is `1`; `10.0 % 3` is a compile error.

---

## Assignment and compound assignment

```cpp
int total = 0;
total = total + 5;    // long form
total += 5;           // same thing, shorter
```

The compound forms `+=`, `-=`, `*=`, `/=`, `%=` all work the same way: read the current value, apply the operation, write back.

`++` and `--` increment or decrement by one:

```cpp
int i = 0;
++i;   // i is now 1, preferred form
i++;   // also works, prefer ++i when used on its own
```

For built-in types `++i` and `i++` behave identically when used as a standalone statement. They differ when used inside a larger expression (`++i` returns the new value, `i++` returns the old one), but using `++` inside an expression you also assign from is a quick way to confuse yourself. Don't.

---

## Comparison

Comparison operators produce a `bool`:

| Operator | Meaning            |
|----------|--------------------|
| `==`     | equal              |
| `!=`     | not equal          |
| `<`      | less than          |
| `>`      | greater than       |
| `<=`     | less than or equal |
| `>=`     | greater than or equal |

```cpp
bool adult = (age >= 18);
```

**The most common bug here:** writing `=` (assignment) when you mean `==` (comparison).

```cpp
if (x = 5) { ... }   // assigns 5 to x, then tests if 5 is true, always runs
if (x == 5) { ... }  // tests whether x equals 5
```

Modern compilers warn about this if you enable warnings. Turn them on.

---

## Logical operators

Used to combine boolean expressions:

| Operator | Meaning |
|----------|---------|
| `&&`     | AND: true only if both sides are true |
| `\|\|`   | OR: true if either side is true       |
| `!`      | NOT: flips true and false             |

```cpp
if (temperature > 80 && pressure < 5) {
    // both conditions must hold
}

if (!ready) {
    // 'ready' is false
}
```

`&&` and `||` are **short-circuiting**: they evaluate the right-hand side only if needed. This is useful — and occasionally essential:

```cpp
if (count != 0 && total / count > threshold) {
    // safe: total / count runs only when count is not zero
}
```

If `count` is zero, the right side never runs, so the division is skipped. Swap the two conditions and the program divides by zero.

---

## The ternary operator

A compact `if`/`else` that produces a value:

```cpp
int max = (a > b) ? a : b;
```

Reads as: "if `a > b`, the value is `a`; otherwise it is `b`." Convenient for short choices. For anything more complex, use a real `if`/`else` statement; readability beats brevity.

---

## Precedence: why parentheses save you

When several operators appear in the same expression, **precedence** decides which binds tighter.

```cpp
int x = 2 + 3 * 4;   // 14, not 20, * binds tighter than +
```

The full precedence table is long. You do not need to memorise it. You need to remember **two rules** and you will not get in trouble:

1. `*`, `/`, `%` bind tighter than `+` and `-` (standard maths).
2. **When in doubt, use parentheses.** They cost nothing and make intent explicit.

Operators of equal precedence evaluate **left to right**, which can catch you out:

```cpp
int result = totalSeconds / 60 * 60;
```

You might read that as "divide by 60, then multiply by 60 — back where you started." It is not: the `/` runs first, and integer division discards the remainder. With `totalSeconds = 125`, `125 / 60` is `2`, and `2 * 60` is `120` — not `125`. Now a different trap, where the *grouping* is unclear:

```cpp
double rate = a + b / c + d;
```

Did you mean `(a + b) / (c + d)` or `a + (b/c) + d`? They give different answers. Write the parentheses you mean.

---

## Mixing types

If you combine values of different types, C++ converts them following well-defined rules. Two cases worth knowing:

```cpp
int    i = 5;
double d = 2.0;
double result = i + d;   // i is promoted to double; result is 7.0
```

That is the safe direction: `int` to `double` loses nothing.

```cpp
double pi = 3.14;
int    n  = pi;          // truncates to 3, fractional part lost
```

Going the other direction (`double` to `int`) silently loses information. Brace initialisation refuses it; ordinary assignment does not. If you *want* to truncate, make it explicit with a **cast**:

```cpp
int n = static_cast<int>(pi);
```

`static_cast` is the polite way to ask for a conversion the compiler would otherwise warn about. It also flags to a reader that the truncation is intentional.

---

## Summary

- Arithmetic on integers truncates; mix in a `double` to get decimal results.
- `==` compares, `=` assigns. They are not the same.
- `&&` and `||` short-circuit, which is useful for guarding against null/invalid values.
- Precedence exists, but parentheses are free. Use them.
- Conversions from larger to smaller types lose data silently; make casts explicit.

Floating-point arithmetic has surprises of its own: `0.1 + 0.2` does not exactly equal `0.3`, and comparing floats with `==` is almost never what you want. See the [Floating-Point Pitfalls](../floating_point.md) reference for the full list of gotchas.
