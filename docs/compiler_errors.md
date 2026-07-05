# Reading Compiler Errors

The single fastest way to get better at C++ is to learn to read error messages. Beginners freeze at the wall of red text; experienced programmers skim it, find the line, and fix the problem in seconds. The difference is not intelligence; it is knowing what to look for.

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

For example, forgetting `#include <vector>` in a program that uses `std::vector` makes GCC report three errors from that one omission:

```
main.cpp: In function 'int main()':
main.cpp:4:10: error: 'vector' is not a member of 'std'
    4 |     std::vector<int> readings = {10, 20, 30};
      |          ^~~~~~
main.cpp:4:10: note: 'std::vector' is defined in header '<vector>';
                     did you forget to '#include <vector>'?
main.cpp:4:17: error: expected primary-expression before 'int'
    4 |     std::vector<int> readings = {10, 20, 30};
      |                 ^~~
main.cpp:5:5: error: 'readings' was not declared in this scope
    5 |     readings.push_back(40);
      |     ^~~~~~~~
```

Three errors, one mistake: the missing header means `std::vector` is unknown, so `readings` never gets declared, so the line that *uses* `readings` fails too. Fix the first error — add `#include <vector>` — and rebuild; the other two vanish with it. (Notice the `note:` line even tells you which header to add — the compiler is often more helpful than the wall of red suggests.)

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

The fix is in the `note: candidate ...` line: read it for what the compiler *expected* and compare to what you passed.

### `expected '}' at end of input`

A `{` somewhere does not have a matching `}`. The line number is often the very end of the file, which is not very helpful. Walk back through the file looking for an opening brace without a closing one. Your editor's brace-matching feature is your friend.

### `redefinition of '...'`

You defined the same thing twice *within one file*, so the **compiler** rejects it. The usual cause is a header, without `#pragma once` or a header guard, being pasted into the same file twice (often because one header `#include`s another that you also include directly). Add `#pragma once` to the header. (Defining the same thing across *different* files is a different, linker-stage error — see [`multiple definition of ...`](#linker-errors-undefined-reference-to-and-multiple-definition-of) below.)

### `'X' was not declared in this scope`

Same as "use of undeclared identifier", a different compiler's phrasing for the same problem.

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

if (x = 5) { }              // also a warning, see below
```

### Linker errors: `undefined reference to ...` and `multiple definition of ...`

Different from compile errors: these come from the **linker**, the next stage of the build. The compiler accepted each file on its own, but when it came time to assemble the final program, the pieces did not fit together — either something is missing, or something is defined too many times.

**`undefined reference to ...`** — the linker cannot find the implementation of something you use:

```
undefined reference to `Motor::start()'
```

Usual causes:

1. **You declared a function but never defined it** (declaration in a header, no implementation in any `.cpp`).
2. **The `.cpp` containing the implementation is not in your `CMakeLists.txt`.**
3. **You forgot to link against a library** (`target_link_libraries` missing).

**`multiple definition of ...`** — the opposite problem: the same thing is defined in more than one `.cpp`, so the linker sees two copies and cannot choose:

```
multiple definition of `add(int, int)'; first defined here
```

Usual causes:

1. **Two `.cpp` files implement the same function.**
2. **A function is *defined* in a header without being marked `inline`** — every `.cpp` that includes the header gets its own copy. Either mark the function `inline`, or move the definition into a single `.cpp` and leave only its declaration in the header.

Linker errors do *not* include line numbers in your source; they refer to symbols.

---

## Warnings

Warnings are not errors; the build succeeds. But warnings almost always indicate a real bug or a smell:

```
warning: control reaches end of non-void function
warning: comparison of integer expressions of different signedness
warning: '=' used in a context where '==' was probably intended
```

**Treat warnings as errors.** Most compilers accept a flag (`-Wall -Wextra -Werror` for GCC and Clang) that promotes them — see [how to switch them on](Chapter2/cmake_intro.md#turn-on-compiler-warnings). Once your code compiles warning-free, you will catch a class of bugs that would otherwise survive until runtime.

---

## When the message still does not make sense

Four strategies, in this order:

**1. Read the line above the one the error points to.** Many errors (especially missing-semicolon errors) are actually one line earlier than where the compiler complains.

**2. Comment out the offending line and rebuild.** If the rest of the file then compiles cleanly, you have narrowed the problem.

**3. Search the *exact* error text.** Copy the most specific part, usually starting with `error:`, and paste it into a search engine. Most error messages have been asked about on Stack Overflow several times over.

**4. Ask an AI to translate the message.** Pasting the *full* compiler output together with the offending code into an AI assistant is one of its best use cases. See [Using AI for Coding](using_ai.md) for the habits that keep this from turning into "the AI does my work."

Template errors are a special case: they can be hundreds of lines long for a single typo. The trick is to read from the top down and look for the line `note: candidate template ignored: ...`, which says *why* a template couldn't be used. That note usually contains the real problem in plain English.

---

## A worked example

You compile this:

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int x = 5
    std::cout << x << "\n";
    return 0;
}
```

And GCC reports:

```
main.cpp: In function 'int main()':
main.cpp:5:5: error: expected ',' or ';' before 'std'
    5 |     std::cout << x << "\n";
      |     ^~~
```

One error — and it points at **line 5**, the `std::cout` line, even though the real mistake is on **line 4**: the `int x = 5` has no semicolon. This is the classic missing-semicolon trap. The compiler read `int x = 5` and kept going, expecting the statement to continue; only when it hit `std` on the next line did it realise something was wrong — so *that* is the line it blames. **Always check the line above the one the error points to.** Add the semicolon after `5`, recompile, and the error disappears.

Once you have done this five or six times, you will start fixing missing semicolons before the compiler even finishes complaining about them.

---

Compiler errors are about code that will not *build*. Once it builds but does the wrong thing when you run it, the tool you want is the [debugger](debugger.md).
