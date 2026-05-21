# Reading Compiler Errors

The single fastest way to get better at C++ is to learn to read error messages. Beginners freeze at the wall of red text; experienced programmers skim it, find the line, and fix the problem in seconds. The difference is not intelligence — it is knowing what to look for.

This page is a guide to reading typical C++ compiler output, the most common errors you will hit, and what to do about each.

---

## Anatomy of an error message

A typical compiler error has this shape:

```
main.cpp:14:18: error: expected ';' after expression
    std::cout << "Hello"
                ^
                ;
```

Three parts you always want to find:

| Part | What it tells you |
|------|-------------------|
| `main.cpp:14:18` | The file, line number, and column where the compiler got confused |
| `error: expected ';'...` | What the compiler thinks is wrong |
| The caret `^` line | A visual pointer to the spot in the source |

**Always start with the file:line.** Open that file, jump to that line, and read the surrounding code.

---

## Reading multi-error output

A single mistake often generates several error messages, because once the compiler is confused it stays confused for a while. Always **fix the first error first**, then rebuild. Many of the later errors will vanish on their own.

A common pattern:

```
main.cpp:14:18: error: expected ';' after expression
main.cpp:15:5:  error: use of undeclared identifier 'std'
main.cpp:15:23: error: expected ';' after expression
main.cpp:18:1:  error: extraneous closing brace ('}')
```

Four errors, one mistake: a missing semicolon on line 14 cascading into confusion about everything after it. Fix that semicolon and rebuild before doing anything else.

---

## The common errors and what they really mean

### `expected ';' after ...`

You forgot a semicolon. The error usually points at the line *after* the missing one, because the compiler did not realise the previous statement was over until it saw something that could not be a continuation.

```cpp
std::cout << "Hello"        // missing semicolon here
std::cout << "World";       // error reported here
```

### `use of undeclared identifier 'foo'`

You used a name the compiler does not know about. Three usual causes:

1. **Typo.** `std:cout` instead of `std::cout`. `cout` instead of `std::cout`.
2. **Missing `#include`.** You used `std::vector` but did not `#include <vector>`.
3. **Variable declared in another scope.** You declared `x` inside an inner block and tried to use it outside.

### `no matching function for call to 'foo(...)'`

You called a function but the arguments do not match any version of it. The compiler usually lists the candidates it considered:

```
error: no matching function for call to 'add(int, std::string)'
note: candidate function not viable: no known conversion
      from 'std::string' to 'int' for 2nd argument
      int add(int a, int b);
```

The fix is in the `note: candidate ...` line — read it for what the compiler *expected* and compare to what you passed.

### `expected '}' at end of input`

A `{` somewhere does not have a matching `}`. The line number is often the very end of the file, which is not very helpful. Walk back through the file looking for an opening brace without a closing one. Your editor's brace-matching feature is your friend.

### `redefinition of '...'`

You defined the same thing twice. Common causes:

1. Two `.cpp` files implementing the same function.
2. A header included from two places, without `#pragma once` or a header guard.
3. Defining a function in a header without marking it `inline` (it gets compiled into every file that includes the header).

### `'X' was not declared in this scope`

Same as "use of undeclared identifier" — a different compiler's phrasing for the same problem.

### `cannot convert 'X' to 'Y'`

Type mismatch. You assigned, returned, or passed something of one type where another is expected. Read the types carefully:

```
error: cannot convert 'std::string' to 'int' in assignment
```

You tried to put a string into an int variable. Check the types of both sides.

### `member access into incomplete type 'X'`

You used `someObject.field` or `somePtr->field` on a type that has only been forward-declared, not fully defined. Either include the header that defines the type, or move the access to a place where the full type is visible.

### `expression is not assignable`

You tried to write to something that cannot be written to: a `const` variable, the result of a function call, or a temporary value.

```cpp
const int x = 5;
x = 10;                     // expression is not assignable

if (x = 5) { }              // also a warning — see below
```

### Linker errors: `undefined reference to ...`

Different from compile errors — these come from the **linker**, the next stage of the build. The compiler accepted your code, but when it came time to assemble the final program, it could not find the implementation of something:

```
undefined reference to `Motor::start()'
```

Usual causes:

1. **You declared a function but never defined it** (declaration in a header, no implementation in any `.cpp`).
2. **The `.cpp` containing the implementation is not in your `CMakeLists.txt`.**
3. **You forgot to link against a library** (`target_link_libraries` missing).

Linker errors do *not* include line numbers in your source — they refer to symbols.

---

## Warnings

Warnings are not errors — the build succeeds. But warnings almost always indicate a real bug or a smell:

```
warning: control reaches end of non-void function
warning: comparison of integer expressions of different signedness
warning: '=' used in a context where '==' was probably intended
```

**Treat warnings as errors.** Most compilers accept a flag (`-Wall -Wextra -Werror` for GCC and Clang) that promotes them. Once your code compiles warning-free, you will catch a class of bugs that would otherwise survive until runtime.

---

## When the message still does not make sense

Three strategies, in this order:

**1. Read the line above the one the error points to.** Many errors (especially missing-semicolon errors) are actually one line earlier than where the compiler complains.

**2. Comment out the offending line and rebuild.** If the rest of the file then compiles cleanly, you have narrowed the problem.

**3. Search the *exact* error text.** Copy the most specific part — usually starting with `error:` — and paste it into a search engine. Most error messages have been asked about on Stack Overflow several times over.

Template errors are a special case: they can be hundreds of lines long for a single typo. The trick is to read from the top down and look for the line `note: candidate template ignored: ...`, which says *why* a template couldn't be used. That note usually contains the real problem in plain English.

---

## A worked example

You compile this:

```cpp
#include <iostream>

int main() {
    int x = 5
    std::cout << x << "\n";
    return 0;
}
```

And get:

```
main.cpp:5:5: error: use of undeclared identifier 'std'
    std::cout << x << "\n";
    ^
main.cpp:4:13: error: expected ';' after expression
    int x = 5
            ^
            ;
```

Two errors. The first says line 5 has an "undeclared identifier `std`" — which is nonsense because `std` is declared by the `#include`. That is the giveaway: the compiler is so confused that obvious things have stopped making sense. Always look at the *first* error first. The second message points at line 4, which is missing its semicolon. Add the semicolon, recompile, and both errors disappear.

Once you have done this five or six times, you will start fixing missing semicolons before the compiler even finishes complaining about them.
