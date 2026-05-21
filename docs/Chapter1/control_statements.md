# Control Statements

By default, a program runs one statement after another from top to bottom. **Control statements** let you change that flow: take one path or another based on a condition, repeat a block of code, or stop a loop early.

Three families:

| Family | Examples | Purpose |
|--------|----------|---------|
| Conditional | `if`, `else`, `else if`, `switch` | Choose between paths |
| Loop        | `while`, `do-while`, `for`, range-based `for` | Repeat code |
| Jump        | `break`, `continue`, `return` | Exit a block or function early |

---

## `if` and `else`

```cpp
if (temperature > 80) {
    std::cout << "Cooling down\n";
}
```

The condition in parentheses must produce a `bool` (or something convertible to one). If it is true, the block runs; otherwise it is skipped.

To handle the other case:

```cpp
if (temperature > 80) {
    std::cout << "Cooling down\n";
} else {
    std::cout << "Normal\n";
}
```

For more than two outcomes, chain with `else if`:

```cpp
if (temperature > 80) {
    std::cout << "Too hot\n";
} else if (temperature < 10) {
    std::cout << "Too cold\n";
} else {
    std::cout << "Fine\n";
}
```

Only the first matching branch runs. Once a branch is taken, the rest are skipped.

> **Use braces even for single-statement bodies.** It is one extra line and avoids a surprising class of bugs when someone adds a second statement later.

---

## `switch`

When you are comparing one value against several constants, `switch` is clearer than a long `else if` chain:

```cpp
switch (gear) {
    case 1: std::cout << "First\n";  break;
    case 2: std::cout << "Second\n"; break;
    case 3: std::cout << "Third\n";  break;
    default: std::cout << "Unknown\n";
}
```

Two things to know:

1. **Always include `break`** at the end of each case unless you specifically want execution to fall through to the next case. Forgetting `break` is a classic bug — execution silently continues into the next case.
2. `switch` only works with integer-like values (`int`, `char`, enumerations). It cannot switch on a `std::string` or a `double`.

If a case needs to declare its own local variables, wrap its body in braces:

```cpp
case 1: {
    int local = 5;
    // ...
    break;
}
```

---

## `while`

Repeat a block as long as a condition is true:

```cpp
int countdown = 5;
while (countdown > 0) {
    std::cout << countdown << "...\n";
    --countdown;
}
std::cout << "Go!\n";
```

The condition is checked *before* each iteration. If it is false at the start, the body runs zero times.

The number-one bug with `while` loops is forgetting to make progress toward the exit condition:

```cpp
int i = 0;
while (i < 10) {
    std::cout << i << "\n";
    // forgot ++i — infinite loop
}
```

If your program hangs, this is the first place to look.

---

## `do-while`

Like `while`, but the condition is checked *after* the first iteration. The body therefore always runs at least once:

```cpp
int input;
do {
    std::cout << "Enter a positive number: ";
    std::cin >> input;
} while (input <= 0);
```

Use this when the work must happen before you know whether to continue. Common pattern: "read input until the user provides something valid."

---

## `for`

When you know how many times to loop, `for` is the cleanest form:

```cpp
for (int i = 0; i < 5; ++i) {
    std::cout << i << "\n";
}
// prints 0, 1, 2, 3, 4
```

The three parts inside the parentheses are:

1. **Initialisation** — `int i = 0` — runs once, before the loop starts.
2. **Condition** — `i < 5` — checked before each iteration. Loop ends when false.
3. **Update** — `++i` — runs after each iteration.

A `for` loop is just a `while` loop with the parts arranged for visibility. Use it whenever you have a counter.

---

## Range-based `for`

For visiting every element of a container, the range-based `for` is shorter and harder to get wrong than a counter-based `for`:

```cpp
std::vector<int> readings{42, 17, 99, 8};

for (int value : readings) {
    std::cout << value << "\n";
}
```

If you do not need to modify the elements, prefer `const auto&` to avoid copying:

```cpp
for (const auto& value : readings) {
    std::cout << value << "\n";
}
```

To modify the elements in place, take a non-const reference:

```cpp
for (auto& value : readings) {
    value *= 2;
}
```

---

## `break`, `continue`, `return`

These three change the flow inside a loop or function.

```cpp
for (int i = 0; i < 100; ++i) {
    if (i == 10) {
        break;     // exit the loop entirely
    }
    if (i % 2 == 0) {
        continue;  // skip the rest of this iteration, go to the next
    }
    std::cout << i << "\n";
}
```

- `break` exits the **innermost** loop or `switch`.
- `continue` skips the rest of the current iteration and moves to the next.
- `return` exits the function entirely (and optionally returns a value).

---

## Choosing the right tool

| Situation | Use |
|-----------|-----|
| Two or three branches based on a condition | `if` / `else if` / `else` |
| Many branches on one integer-like value | `switch` |
| Repeat until a condition becomes false | `while` |
| Loop body must run at least once | `do-while` |
| Fixed number of iterations with a counter | `for` |
| Visit every element of a container | range-based `for` |
| Exit a loop early | `break` |
| Skip to the next iteration | `continue` |
