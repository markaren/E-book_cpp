# Basic Structure of a C++ Program

Every C++ program is built from the same handful of pieces. This chapter walks through them using the smallest program that does something useful.

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
```

---

## `#include`: pulling in code

Lines that start with `#` are **preprocessor directives**. They are handled before the real compilation begins.

`#include <iostream>` tells the compiler: "before you read the rest of this file, paste in the contents of the `iostream` header." That header is what defines `std::cout` and friends. Without it, the compiler will not know what `std::cout` means and your code will not compile.

Angle brackets (`<iostream>`) are used for the standard library and system headers. Quotes (`"my_header.hpp"`) are used for your own files. We will see this distinction in Chapter 2.

---

## `main`: where execution starts

```cpp
int main() {
    // ...
    return 0;
}
```

Every C++ program has exactly one function called `main`. The operating system calls it to start your program. The `int` in front declares that `main` returns an integer: `0` for success, anything non-zero to signal an error.

The body of `main`, between `{` and `}`, is the code that actually runs.

---

## Statements and semicolons

A **statement** is one instruction. In C++, every statement ends with a semicolon:

```cpp
int quantity = 10;
double price = 5.40;
double sum = price * quantity;
std::cout << "Total: " << sum << std::endl;
```

Forgetting a semicolon is the single most common error a beginner gets. The compiler error usually points to the line *after* the missing semicolon, which is confusing the first time. Always check the line above too.

Semicolons also terminate class definitions:

```cpp
class Motor {
    // ...
}; // <-- this semicolon is required
```

---

## Blocks and scope

A **block** is code wrapped in curly braces `{ ... }`. Blocks group statements together and define **scope**: the region of code in which a variable exists.

```cpp
int main() {
    int x = 5;

    {
        int y = 10;
        std::cout << x << " " << y << "\n"; // both visible
    }

    // y no longer exists here
    std::cout << x << "\n"; // x still exists
}
```

Two rules cover almost every case you will meet:

1. A variable declared in a block is destroyed when execution leaves that block.
2. An inner block can see variables from the outer block, but not the reverse.

If an inner block declares a variable with the same name as one outside, the inner one **shadows** the outer one: inside the inner block, the name refers to the new variable. Shadowing is legal but rarely what you want; pick distinct names.

---

## Comments

Comments are notes for human readers. The compiler ignores them.

```cpp
// Single-line comment

/* Multi-line comment
   that spans several lines */
```

A good comment explains *why* the code does something, not what it does. The code already says what; if a future reader can't tell why, that is where a comment helps. Beginner code tends to have too many "this adds two numbers"-style comments. Resist the temptation.

---

## Putting it together

A complete program that reads two numbers from the user and prints their sum:

```cpp
#include <iostream>

int main() {
    int a;
    int b;

    std::cout << "Enter two integers separated by a space: ";
    std::cin >> a >> b;

    int sum = a + b;
    std::cout << "Sum: " << sum << "\n";

    return 0;
}
```

You now know every structural element this program is built from: `#include`, `main`, blocks, statements, semicolons, comments. The remaining chapters of this section fill in what goes *inside* `main`: variables, operators, control flow, and functions.

---

## A note on style

Two stylistic conventions worth adopting from day one:

- **Indent the body of every block by four spaces.** Modern IDEs do this automatically. Keep it consistent.
- **Always use braces, even for one-line `if` and `while` bodies.** It is one line of extra typing and removes a whole class of bugs:

```cpp
// Avoid:
if (ready) doThing();

// Prefer:
if (ready) {
    doThing();
}
```

The second form is harder to break when someone adds a second line later.
