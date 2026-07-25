# Basic Structure of a C++ Program

Every C++ program is built from the same handful of pieces. This chapter walks through them using the smallest program that does something useful.

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world!" << "\n";
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

<!-- no-ce -->
```cpp
int main() {
    // ...
    return 0;
}
```

Every C++ program has exactly one function called `main`. The operating system calls it to start your program. The `int` in front declares that `main` returns an integer: `0` for success, anything non-zero to signal an error.

The body of `main`, between `{` and `}`, is the code that actually runs.

---

## Escape sequences

Look again at the first program: it prints `"Hello, world!"` followed by `"\n"`. That `\n` is not the two characters backslash and *n*. Inside a string, a backslash starts an **escape sequence** — a stand-in for a character you cannot easily type between quotes. `\n` means "start a new line."

The handful you will meet constantly:

| Escape | Means |
|--------|-------|
| `\n`   | new line |
| `\t`   | tab |
| `\"`   | a double quote (without ending the string) |
| `\\`   | a single backslash |

The last two exist because `"` and `\` already have special jobs — one ends the string, the other starts an escape — so you spell the literal character by escaping it. This is also why a Windows path like `"C:\dev"` misbehaves: `\d` looks like an escape. (More on that in [Computer Basics](../computer_basics.md).)

---

## Statements and semicolons

A **statement** is one instruction. In C++, every *simple* statement — a declaration, an assignment, a function call — ends with a semicolon:

```cpp
int quantity = 10;
double price = 5.40;
double sum = price * quantity;
std::cout << "Total: " << sum << "\n";
```

A **block** (`{ ... }`) and a **control statement** (an `if`, a `for`, a `while`) do *not* take a trailing semicolon — the closing brace ends them. You will meet blocks and control statements in the pages ahead.

Forgetting a semicolon is the single most common error a beginner gets. The compiler error usually points to the line *after* the missing semicolon, which is confusing the first time. Always check the line above too.

---

## Blocks and scope

A **block** is code wrapped in curly braces `{ ... }`. Blocks group statements together and define **scope**: the region of code in which a variable exists.

```cpp
#include <iostream>

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

Comments are notes for human readers; the compiler ignores them. C++ has two forms — `//` runs to the end of the line, and `/* … */` can span several:

```cpp
int retries = 5;          // the sensor often drops its first read, so retry a few times

/* The handshake must finish within one second, or the
   controller treats the device as missing and moves on. */
int timeoutMs = 1000;
```

Notice what those comments do: they explain *why* the values are `5` and `1000` — something the numbers alone cannot tell a future reader. **A good comment explains *why*, not *what*.** The code already says what it does; one that merely restates it — `int retries = 5;  // set retries to 5` — adds nothing. Beginner code collects that kind; resist it, and spend comments on the reasoning, the trade-off, or the surprise.

---

## Putting it together

A complete program that reads two numbers from the user and prints their sum:

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int a = 0;
    int b = 0;

    std::cout << "Enter two integers separated by a space: ";
    std::cin >> a >> b;

    int sum = a + b;
    std::cout << "Sum: " << sum << "\n";

    return 0;
}
```

`std::cin` is the input counterpart of `std::cout`: where `<<` sends values *out* to the screen, `>>` reads a value *in* from the keyboard and stores it in a variable. Here `std::cin >> a >> b` reads two integers.

You now know every structural element this program is built from: `#include`, `main`, blocks, statements, semicolons, comments. The remaining chapters of this section fill in what goes *inside* `main`: variables, operators, strings and vectors, control flow, functions, and enumerations.

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
