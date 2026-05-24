# Functions

A **function** is a named block of code that performs a specific task. You write it once and call it whenever you need that task done.

Without functions, every program would be a single long list of statements with copy-pasted logic. With them, you build named pieces that can be tested, reused, and reasoned about one at a time.

---

## Anatomy of a function

```cpp
int add(int a, int b) {
    return a + b;
}
```

Four parts:

- **Return type** (`int`): what type of value the function gives back. `void` means "nothing."
- **Name** (`add`): what you call it.
- **Parameter list** (`(int a, int b)`): the inputs, each with a type and a name.
- **Body** (`{ return a + b; }`): the code that runs.

Calling the function looks like this:

```cpp
int result = add(5, 3);   // result is 8
```

You pass **arguments** (`5` and `3`) and they become the **parameters** (`a` and `b`) inside the function.

---

## Returning a value

`return` exits the function and hands back a value:

```cpp
int square(int x) {
    return x * x;
}
```

If the return type is `void`, the function returns nothing; `return;` (with no value) just exits early:

```cpp
void warn(bool overheating) {
    if (!overheating) {
        return;  // exit early, nothing to do
    }
    std::cout << "WARNING: temperature high\n";
}
```

A non-`void` function must return a value on every path. Forgetting to do so is undefined behaviour; modern compilers will warn you, and you should treat that warning as an error.

---

## Declarations vs. definitions

In larger programs you often split a function across files. The **declaration** tells the compiler the function exists and what its signature is; the **definition** provides the actual code.

```cpp
// Declaration, usually in a header file
int add(int a, int b);

// Definition, usually in a .cpp file
int add(int a, int b) {
    return a + b;
}
```

For short programs that live in one file, the declaration and definition are the same line; you just write the full function and use it. Chapter 2 covers splitting code across files properly.

---

## Function overloading

You can have multiple functions with the same name as long as they take different parameters. The compiler picks the right one based on the argument types you pass.

```cpp
#include <iostream>

int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

int main() {
    int    sum1 = add(5, 3);       // calls the int version
    double sum2 = add(2.5, 3.7);   // calls the double version

    std::cout << sum1 << " " << sum2 << "\n";
}
```

This is called **overloading**. Use it when the operation is conceptually the same across types (`add` two `int`s, `add` two `double`s). Do not overload to mean different things; pick distinct names for distinct operations.

---

## The `main` function

`main` is the function the operating system calls to start your program. It is a function like any other, with two small special rules:

- It must return `int`. By convention `0` means success and non-zero means an error.
- There must be exactly one of them.

<!-- no-ce -->
```cpp
int main() {
    // ... your program ...
    return 0;
}
```

You can also accept command-line arguments:

<!-- no-ce -->
```cpp
int main(int argc, char* argv[]) {
    // argc = how many arguments
    // argv = the arguments themselves as strings
}
```

You will not need this until you start writing real command-line tools.

---

## Writing good functions

A few habits that pay off immediately:

- **One job per function.** If you have to use the word "and" to describe what a function does, it probably needs splitting.
- **Descriptive names.** `computeRpm` is better than `doStuff`. The function name should let a reader skip its body and still understand what your code is doing.
- **Short bodies.** If a function does not fit on one screen, it is doing too much. There is no hard rule, but if you find yourself scrolling to read a single function, consider whether it can be broken up.
- **Avoid side effects.** A function that takes inputs and returns a result is easier to test and reason about than one that quietly changes global state.

---

## Global variables

Every variable so far has lived *inside* a function. You can also declare one **outside** every function, at the top of the file, where every function below can see it. That is a **global variable**:

```cpp
#include <iostream>

int counter = 0;        // global: visible to every function below it

void tick()  { counter++; }    // any function can change it...
void reset() { counter = 0; }  // ...from anywhere

int main() {
    tick();
    tick();
    reset();
    std::cout << counter << "\n";   // to know what prints, you must trace every call
}
```

It compiles, it runs, and it feels convenient. It is also a habit worth breaking early, because shared, mutable state that *any* function can touch causes trouble out of proportion to the convenience:

- **You cannot tell what changes it.** To know `counter`'s value at some point, you have to read *every* function that might write it. The bigger the program, the worse this gets.
- **Bugs depend on order.** Two pieces of code that both write the same global interfere, and the result depends on which ran first — the hardest kind of bug to reproduce.
- **It resists testing.** A function that reads a global has a hidden input you must set up first; one that writes a global leaves a hidden output that leaks into the next test.

The cure is the rest of this chapter, applied on purpose:

- **Declare each variable in the smallest scope that needs it** — normally a local inside the function that uses it.
- **Pass what a function needs as parameters, and return its result** (the no-side-effects habit above). Then a function's inputs and outputs are exactly its parameter list and return value, with nothing hidden:

```cpp
#include <iostream>

int tick(int counter) {     // input in...
    return counter + 1;     // ...result out, nothing hidden
}

int main() {
    int counter = 0;        // lives only as long as main needs it
    counter = tick(counter);
    counter = tick(counter);
    std::cout << counter << "\n";   // prints 2 — everything that changed it is in view
}
```

When several functions genuinely must share state that outlives a single call, the answer is still **not** a global: bundle that state inside an object that owns it and controls how it changes. That is what a [class](../Chapter4/classes.md) is for, and why [separation of concerns](../Chapter6/soc.md) matters.

One exception: a global **constant** is fine. A value that never changes cannot cause any of the problems above.

```cpp
constexpr double gravity = 9.81;   // global, but constant — safe and useful
```

> Coming from Arduino? This is the habit to adjust most consciously. Arduino sketches keep state in globals because it has to survive between `setup()` and `loop()`; on the desktop you have better options. See [Arduino vs. Desktop C++](../arduino_vs_desktop.md).

---

## Summary

- A function has a return type, name, parameter list, and body.
- `return` produces the function's output; `void` functions have no output value.
- Overloading lets multiple functions share a name when they take different argument types.
- One job per function, descriptive names, keep them short.
- Prefer local variables, parameters, and return values over **global state**; reserve globals for constants.

A function may also call *itself* — a technique called **recursion**. See [Recursion](../recursion.md).
