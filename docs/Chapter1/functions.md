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

- **Return type**, `int`. What type of value the function gives back. `void` means "nothing."
- **Name**, `add`. What you call it.
- **Parameter list**, `(int a, int b)`. The inputs, each with a type and a name.
- **Body**, `{ return a + b; }`. The code that runs.

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

If the return type is `void`, the function returns nothing, `return;` (with no value) just exits early:

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

For short programs that live in one file, the declaration and definition are the same line, you just write the full function and use it. Chapter 2 covers splitting code across files properly.

---

## Function overloading

You can have multiple functions with the same name as long as they take different parameters. The compiler picks the right one based on the argument types you pass.

```cpp
int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

int main() {
    int    sum1 = add(5, 3);       // calls the int version
    double sum2 = add(2.5, 3.7);   // calls the double version
}
```

This is called **overloading**. Use it when the operation is conceptually the same across types, `add` two `int`s, `add` two `double`s. Do not overload to mean different things; pick distinct names for distinct operations.

---

## The `main` function

`main` is the function the operating system calls to start your program. It is a function like any other, with two small special rules:

- It must return `int`. By convention `0` means success and non-zero means an error.
- There must be exactly one of them.

```cpp
int main() {
    // ... your program ...
    return 0;
}
```

You can also accept command-line arguments:

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

## Summary

- A function has a return type, name, parameter list, and body.
- `return` produces the function's output; `void` functions have no output value.
- Overloading lets multiple functions share a name when they take different argument types.
- One job per function, descriptive names, keep them short.
