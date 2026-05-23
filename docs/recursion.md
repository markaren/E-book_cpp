# Recursion

A **recursive** function is one that calls itself. It sounds circular, but it is just a way of solving a problem by solving a *smaller* version of the same problem — over and over — until the version is small enough to answer directly.

Some problems have this shape naturally: the factorial of `n` is `n` times the factorial of `n - 1`; a folder's total size is its own files plus the size of each sub-folder; walking a family tree means visiting a person, then each of their children, then *their* children.

---

## The two parts

Every recursive function needs two things:

- A **base case** — the smallest version, which you can answer *without* recursing. This is what stops the recursion.
- A **recursive case** — which does a little work and then calls itself with a *smaller* input, moving toward the base case.

The classic example is factorial (`5! = 5 × 4 × 3 × 2 × 1`):

```cpp
#include <iostream>

int factorial(int n) {
    if (n <= 1) {                   // base case: stop here
        return 1;
    }
    return n * factorial(n - 1);    // recursive case: a smaller n each time
}

int main() {
    std::cout << factorial(5) << "\n";   // 120
}
```

`factorial(5)` cannot answer on its own, so it asks for `factorial(4)`, which asks for `factorial(3)`, and so on down to `factorial(1)` — which *can* answer (the base case). Then the answers flow back up.

---

## How it unwinds

It helps to trace the calls. Each one has to wait for the call it made before it can finish:

```
factorial(5) = 5 * factorial(4)
             = 5 * (4 * factorial(3))
             = 5 * (4 * (3 * factorial(2)))
             = 5 * (4 * (3 * (2 * factorial(1))))
             = 5 * (4 * (3 * (2 * 1)))             <- base case reached
             = 120
```

The computer tracks every in-progress call on the **call stack**. You can watch them pile up and unwind, one frame at a time, in the debugger — see [the call stack](debugger.md#the-call-stack).

---

## The number-one bug: no base case

If the recursion never reaches a base case — because you forgot it, or because the input does not actually get smaller — the function calls itself forever. Each call takes a little space on the call stack, which is limited, so the program quickly runs out of it and crashes. This is called a **stack overflow**.

```cpp
int bad(int n) {
    return n + bad(n - 1);   // no base case — never stops
}
```

So whenever you write a recursive function, check two things: there *is* a base case, and every recursive call moves *toward* it.

---

## Recursion or a loop?

Anything you can write with recursion you can also write with a loop, and the other way around. For plain counting and accumulating — like factorial — a [loop](Chapter1/control_statements.md) is usually clearer, and it avoids the call-stack cost:

```cpp
int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}
```

So when is recursion the better choice? When the *data itself* is nested — folders inside folders, a parse tree, a family tree — where a loop is awkward but "do this to me, then to each of my children" is natural. For most everyday automation code you will reach for a loop; keep recursion in your toolbox for the cases that are genuinely tree-shaped.

---

## Summary

- A recursive function calls itself to solve a smaller version of the same problem.
- It needs a **base case** (which stops it) and a **recursive case** (which calls itself with a smaller input).
- Forgetting the base case — or not shrinking the input — causes infinite recursion and a **stack overflow** crash.
- Anything recursive can be written as a loop; prefer the loop when it is just as clear.
- Recursion shines when the data is naturally nested or tree-shaped.
