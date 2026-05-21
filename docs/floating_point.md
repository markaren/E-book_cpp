# Floating-Point Pitfalls

For an automation programme, you will spend a lot of time with `double` and `float` values — sensor readings, control signals, time integrals, transforms. Floating-point numbers are extremely useful, but they have sharp edges that catch every beginner at least once.

This page is the short list of behaviours that will surprise you and how to handle them.

---

## Floating-point is not exact

This is the headline. Floats and doubles cannot represent most decimal fractions exactly. They store the *closest* number their binary representation can hold.

The canonical demo:

```cpp
double a = 0.1;
double b = 0.2;
double c = a + b;

std::cout << c << "\n";        // 0.3
std::cout << (c == 0.3) << "\n"; // 0   (false!)
```

`0.1`, `0.2`, and `0.3` are all rounded when stored. `0.1 + 0.2` lands close to — but not exactly on — the stored representation of `0.3`. The difference is around 5 × 10⁻¹⁷, invisible when printed but very visible when compared with `==`.

This is not a C++ quirk; it is how IEEE 754 floating-point works in every language. Python, Java, JavaScript, MATLAB — same numbers, same behaviour.

---

## Never compare floats with `==`

The most common consequence of the above:

```cpp
if (computedValue == 0.3) { /* almost certainly never runs */ }
if (sensorReading == 0.0) { /* probably wrong */ }
```

Two safer patterns:

### Compare with a tolerance

```cpp
bool approximatelyEqual(double a, double b, double tolerance = 1e-9) {
    return std::abs(a - b) < tolerance;
}

if (approximatelyEqual(computedValue, 0.3)) { /* ... */ }
```

The right tolerance depends on the size of the numbers and how they were computed. For sensor readings calibrated to two decimal places, `1e-3` might be appropriate; for tightly converged numerics, `1e-12`. Pick deliberately.

### Use ranges instead of exact targets

```cpp
if (temperature > 79.95 && temperature < 80.05) {
    // "at 80" — but a range, not a point
}
```

Whenever you find yourself comparing a measured value for *exact* equality, ask whether the question really wants "near this value." It almost always does.

---

## Sums lose precision

Adding many floats produces accumulated error. The classic pitfall:

```cpp
double total = 0.0;
for (int i = 0; i < 10'000'000; ++i) {
    total += 0.1;
}
std::cout << total << "\n";        // 999999.999999...  (not 1,000,000)
```

The error in each addition is tiny; ten million of them add up. For sums of millions of samples, consider:

1. **Use `double`, not `float`.** `double` has roughly 15-16 decimal digits of precision; `float` has 6-7.
2. **Use `std::accumulate` with care** — or look up Kahan summation if accuracy matters more than speed.
3. **Where you can, count in integers** and convert to a float only at the end.

For control loops that integrate over time, drift is something to watch for over long runs.

---

## `NaN`, infinity, and division by zero

Floating-point has special values that integer arithmetic does not:

```cpp
double inf  = 1.0 / 0.0;      // +infinity
double ninf = -1.0 / 0.0;     // -infinity
double nan  = 0.0 / 0.0;      // NaN — "not a number"
double nan2 = std::sqrt(-1.0); // NaN
```

Unlike integer division by zero (which is undefined behaviour and may crash), floating-point division by zero is **well-defined**: it produces infinity or NaN. The program keeps running.

That sounds harmless until you propagate a `NaN` through your math:

```cpp
double x = std::sqrt(-1.0);    // NaN
double y = x + 1.0;             // NaN
double z = std::sin(y);          // NaN
if (z < 1.0) { /* ... */ }       // false! NaN compares false with everything
```

NaN poisons every expression it touches and silently fails every comparison — even `nan == nan` is false. If your sensor pipeline starts producing zeros and you see no errors, suspect a NaN.

To check explicitly:

```cpp
#include <cmath>

if (std::isnan(x)) { /* handle the bad value */ }
if (std::isinf(x)) { /* handle the infinity */ }
if (std::isfinite(x)) { /* x is a regular, usable number */ }
```

---

## Integer division catches people too

Not strictly a floating-point issue, but related and very common:

```cpp
int    a = 10 / 3;        // 3 — fractional part discarded
double b = 10 / 3;        // also 3.0! — division happens in int, then converted
double c = 10.0 / 3;      // 3.333… — at least one operand is a double
```

If you want a floating-point result, make sure at least one operand is `double` (or `float`). Writing the literal as `10.0` is the simplest way.

---

## `float` vs `double`

Default to `double`. Use `float` only when you have a specific reason — typically memory-constrained embedded code where you have lots of values to store, or when interfacing with a library (graphics, ML) that uses `float`.

| | `float` | `double` |
|---|---------|----------|
| Size            | 4 bytes | 8 bytes |
| Significant digits | ~6-7 | ~15-16 |
| Speed           | Often the same on modern CPUs | Often the same on modern CPUs |

On a microcontroller without a hardware FPU, `float` operations may be much faster than `double` (the compiler emulates `double` in software). If you target such a platform, check the datasheet and benchmark.

---

## Measuring time: prefer integers

For timing in control loops, `std::chrono` uses integer types under the hood — durations are exact, no floating-point drift.

```cpp
#include <chrono>

auto start = std::chrono::steady_clock::now();
// ... do work ...
auto elapsed = std::chrono::steady_clock::now() - start;
auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count();
```

Resist the temptation to track simulation time as `double t += dt`. Over a long run, accumulated error in `t` adds up. Use an integer step count and multiply when you need a time value.

---

## When you have to print a float

`std::cout` formats doubles with a default precision of 6 significant digits, which is often misleading:

```cpp
double x = 0.1 + 0.2;
std::cout << x << "\n";                                       // 0.3 — misleading
std::cout << std::setprecision(17) << x << "\n";              // 0.30000000000000004
```

For debugging precision issues, set a high precision explicitly. For user-facing output, `std::fixed << std::setprecision(2)` gives a fixed two-decimal-places display.

---

## Summary

- Floats and doubles are approximations of decimal numbers. They are not exact.
- **Never use `==` to compare floats.** Use a tolerance or a range.
- Long sums accumulate error. Use `double` (not `float`) and consider Kahan summation for high-precision sums.
- Division by zero is well-defined for floats — produces infinity or `NaN`.
- `NaN` poisons every expression it touches and compares unequal to everything, including itself.
- Default to `double`. Use `float` only with reason.
- For timing, use `std::chrono` (integer-based).
