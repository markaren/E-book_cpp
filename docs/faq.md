# FAQ

Short answers to the questions that come up most in a first C++ course. Each one points to where the topic is covered in full, and to a longer discussion online where that helps.

---

## Setting up and tools

**Where should I put my project, and why does it matter?**
Use a short, plain path near the drive root (`C:\dev\…`) — no spaces, no Norwegian letters, and not inside a cloud-synced folder. Odd paths cause baffling build errors. See [Computer Basics](computer_basics.md).

**I already know some Python — what is different in C++?**
A lot, underneath: static types, value semantics (`b = a` *copies*), manual scope and lifetimes, integer division. See [Coming from Python](python_to_cpp.md).

**Should I let an AI write my C++?**
As a tutor and a reviewer, yes; as a replacement for understanding, no — they are confidently wrong often enough that you must check everything. See [Using AI for Coding](using_ai.md).

**Why split code into a header and a `.cpp`, instead of `#include`-ing a `.cpp` file?**
A header shares *declarations*; including a `.cpp` copies its *definitions* into every file, causing "multiple definition" linker errors. See [Classes](Chapter4/classes.md). (More: [Stack Overflow](https://stackoverflow.com/questions/1686204/why-should-i-not-include-cpp-files-and-instead-use-a-header).)

**`#include <foo>` versus `#include "foo"`?**
Angle brackets for standard and library headers; quotes for your own files. See [Basic Structure](Chapter1/basic_structure.md). (More: [Stack Overflow](https://stackoverflow.com/questions/21593/what-is-the-difference-between-include-filename-and-include-filename).)

**Why the `#ifndef`/`#define` (or `#pragma once`) at the top of headers?**
They stop a header being pasted into one file twice, which would cause "redefinition" errors. `#pragma once` is the modern one-liner. See [Reading Compiler Errors](compiler_errors.md). (More: [Stack Overflow](https://stackoverflow.com/questions/1653958/why-are-ifndef-and-define-used-in-c-header-files).)

---

## When something goes wrong

**My program will not compile — what does the error mean?**
Fix the *first* error first (the later ones are often fallout), starting at the `file:line` it names. See [Reading Compiler Errors](compiler_errors.md).

**It compiles and runs, but does the wrong thing — now what?**
Use the debugger: set a breakpoint, step through, and watch the variables until what *is* happening and what you *expected* diverge. See [Using a Debugger](debugger.md).

**Why does `if (x = 5)` always run?**
`=` *assigns*; you meant `==`, which *compares*. Turn warnings on and the compiler will flag it. See [Operators and Expressions](Chapter1/operators_expressions.md).

---

## Language basics

**Why does `10 / 3` give `3`, not `3.33`?**
Integer division throws the remainder away. Make one side a `double` (`10.0 / 3`) for a decimal result. See [Operators and Expressions](Chapter1/operators_expressions.md).

**`std::endl` or `"\n"` — which should I use?**
Both end the line; `std::endl` also flushes the stream, which is slower. Prefer `"\n"`. See [IO & Streams](Chapter4/io_streams.md). (More: [Stack Overflow](https://stackoverflow.com/questions/213907/stdendl-vs-n).)

**Do I really need braces `{}` on a one-line `if`?**
Yes — always brace. It is one extra line and removes a whole class of bugs when someone later adds a second statement. See [Control Statements](Chapter1/control_statements.md). (More: [Stack Overflow](https://stackoverflow.com/questions/2125066/is-it-a-bad-practice-to-use-an-if-statement-without-curly-braces).)

**Why would I initialise with curly braces, `int x{5}`?**
Mostly for safety: brace initialisation refuses "narrowing" conversions that silently lose data — `int x{3.7}` will not compile, whereas `int x = 3.7;` quietly truncates to `3`. This book uses plain `=` for everyday initialisation and reaches for `{}` when rejecting narrowing matters. See [Variables and Basic Types](Chapter1/variables.md). (More: [Stack Overflow](https://stackoverflow.com/questions/18222926/what-are-the-advantages-of-list-initialization-using-curly-braces).)

**What does `explicit` mean on a constructor?**
It stops that constructor being used for *silent* conversions. A one-argument constructor like `Motor(int)` normally lets the compiler turn a stray `int` into a `Motor` on its own; `explicit` switches that off, so the conversion happens only when you ask for it. Mark single-argument constructors `explicit` unless you want the conversion. See [Classes](Chapter4/classes.md). (More: [Stack Overflow](https://stackoverflow.com/questions/121162/what-does-the-explicit-keyword-mean).)

**Why is `using namespace std;` discouraged?**
It dumps every standard-library name into your scope, inviting clashes and ambiguity. Write the `std::` prefix instead. See [C++ Standard Library](Chapter3/standard_library.md). (More: [Stack Overflow](https://stackoverflow.com/questions/1452721/why-is-using-namespace-std-considered-bad-practice).)

**What does `std::` mean, and why is it everywhere?**
`std` is the namespace that holds the standard library; `std::cout` means "`cout`, from `std`." See [C++ Standard Library](Chapter3/standard_library.md).

**Why isn't `0.1 + 0.2` exactly `0.3`?**
Floating-point numbers are approximations, so tiny errors creep in — never compare them with `==`. See [Floating-Point Pitfalls](floating_point.md).

**What is a lambda?**
A small, unnamed function written inline, usually handed to an algorithm. See [Lambda Expressions](lambdas.md). (More: [Stack Overflow](https://stackoverflow.com/questions/7627098/what-is-a-lambda-expression-in-c11).)

---

## Pointers, references, and memory

**What is the difference between a pointer and a reference?**
A reference is a permanent alias for one variable; a pointer is a reseatable address that can be null. Prefer a reference unless you need null or reassignment. See [Values, References & Pointers](Chapter4/types_refs_ptrs.md). (More: [Stack Overflow](https://stackoverflow.com/questions/57483/what-are-the-differences-between-a-pointer-variable-and-a-reference-variable).)

**When do I use `.` versus `->`?**
`.` on an object; `->` through a pointer to one (`p->x` is shorthand for `(*p).x`). See [Values, References & Pointers](Chapter4/types_refs_ptrs.md).

**Why pass by `const&`?**
It avoids copying a large object while promising not to change it — the standard way to pass anything bigger than a number. See [Values, References & Pointers](Chapter4/types_refs_ptrs.md).

**What is const-correctness?**
The habit of marking everything that does not change as `const`: member functions that only observe (`read() const`), parameters you only read (`const T&`), and locals you never reassign. It matters because a `const` object can call *only* `const` member functions — so consistent `const` lets you pass your own types by `const&` and lets the compiler catch accidental modifications. See [Classes](Chapter4/classes.md) and [Values, References & Pointers](Chapter4/types_refs_ptrs.md).

**Why should I avoid raw `new` and `delete`?**
They are easy to leak or double-free. Let `std::vector`, `std::string`, and smart pointers own memory for you (that is RAII). See [Memory Management](Chapter5/memory.md). (More: [Stack Overflow](https://stackoverflow.com/questions/6500313/why-should-c-programmers-minimize-use-of-new).)

**Which cast should I use?**
Avoid the old C-style cast `(int)x` — it silently does *whatever it takes* to force the conversion, which hides mistakes, and it is impossible to search for. Use a named cast instead: almost always `static_cast`; `dynamic_cast`, `const_cast`, and `reinterpret_cast` are rare and each needs a specific reason. See [Operators and Expressions](Chapter1/operators_expressions.md). (More: [Stack Overflow](https://stackoverflow.com/questions/332030/when-should-static-cast-dynamic-cast-const-cast-and-reinterpret-cast-be-used).)
