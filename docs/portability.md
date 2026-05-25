# Portability

C++ is defined by an international standard, so *in principle* the same source code builds and runs the same on every system. **In practice, not quite** — and the gap catches beginners out, because it shows up even in small programs that use nothing but the standard library.

This page is about **desktop** C++ across **Windows, Linux, and macOS**, and the three compilers you are likely to meet: **GCC**, **Clang**, and Microsoft's **MSVC**. (On Windows, CLion uses GCC by default.) For the very different case of a microcontroller — the same language in a tiny environment — see [Arduino vs. Desktop C++](arduino_vs_desktop.md).

> **Why this matters to you.** You write code on Windows in CLion; a classmate builds the same project on a Mac, and your instructor builds it on Linux. "It built on my machine" is not the same as "it builds." Finding out the difference the night before a deadline is no fun — a little awareness now prevents it.

---

## A compiled program is not portable

Recall from the [Introduction](Chapter1/introduction.md) that C++ is *compiled*: the compiler turns your source into **machine code** — raw instructions for one specific kind of processor, wrapped in a file format that one specific operating system knows how to load.

That has a direct consequence: **the executable you build is tied to one OS and one CPU.**

- A Windows `.exe` will not run on Linux or macOS, and vice versa — each system uses a different file format for programs.
- A program built for a 64-bit Intel/AMD chip will not run on an ARM chip (such as Apple Silicon or a Raspberry Pi) without being rebuilt.

To run your program on another platform, you **recompile it there**. This is normal and usually painless — [CMake](Chapter2/cmake_intro.md) exists precisely so you can describe the build once and run it on any platform. But be clear about what CMake does: it makes *building* portable, not the *built program*. The `.exe` itself never becomes portable; you simply rebuild on each system.

> This is the price of compiling to machine code. Languages like Python and Java sidestep it by shipping the source (or a portable bytecode) and running it through an interpreter or virtual machine installed on each platform. You trade the recompile for needing that runtime present — and for the lower speed that comes with it.

---

## The same source may not even compile

Here is the part that surprises people. You would expect code that uses **only the standard library** — no Windows-specific calls, nothing exotic — to compile anywhere. Often it does. But not always, and here is why.

### You forgot an `#include` (and got away with it)

A standard header is allowed to include *other* standard headers, and exactly which ones it pulls in **differs between compilers**. So this may compile on Windows yet fail on Linux:

```cpp
#include <vector>          // only this — no <algorithm>

int main() {
    std::vector<int> v{3, 1, 2};
    std::sort(v.begin(), v.end());   // std::sort actually lives in <algorithm>
}
```

On MSVC, `<vector>` happens to drag in `<algorithm>`, so `std::sort` is visible and it builds. On Linux with GCC it does not, and you get `'sort' is not a member of 'std'` — pointing at a line you never thought was wrong. **The fix is a rule, not a workaround: include a header for every standard facility you name.** Here, add `#include <algorithm>`. ("Include what you use.")

### C++20 is not finished everywhere at the same time

A new standard like **C++20** is a long document, and compilers implement it piece by piece over several years. A feature can be ready in one compiler and missing in another:

```cpp
#include <format>
#include <iostream>

int main() {
    std::cout << std::format("{} + {} = {}\n", 2, 2, 4);
}
```

`std::format` shipped in MSVC and in recent GCC, but **older** versions of GCC and Clang have no `<format>` at all — the same standard-library code simply will not compile there. When you reach for a brand-new feature, check that every compiler you target is new enough to have it.

### Two that bite in practice: `or` and `M_PI`

Compilers also disagree about what counts as valid in the first place — and the difference is not always "stricter," it can simply be *different*. Two cases turn up constantly.

**Word operators (`or`, `and`, `not`).** C++ lets you spell `||`, `&&`, and `!` as the words `or`, `and`, and `not`. They are standard keywords, and GCC and Clang accept them as-is:

```cpp
if (ready or retry) { /* ... */ }     // identical to: ready || retry
```

But **MSVC, in its default mode, does not** — it reports `'or': undeclared identifier`. (It recognises the word forms only in conformance mode, or if you include `<ciso646>`.) So a line that built on a classmate's Mac can fail in a default Visual Studio project. The robust fix is the simplest one: **use the symbols** `||`, `&&`, `!`. They compile on every compiler, and they are what this book uses throughout.

**`M_PI` for π.** Reach for π and you will find `M_PI` in countless examples:

```cpp
#include <cmath>
double area = M_PI * r * r;     // builds on GCC/Clang...
```

This compiles on Linux and macOS — but `M_PI` is **not part of standard C++** (it is an old POSIX extension). On MSVC it is undefined unless you write `#define _USE_MATH_DEFINES` *before* `#include <cmath>`, so the very same code fails to compile on Windows. In C++20 the portable answer is to drop `M_PI` and use the standard constant:

```cpp
#include <numbers>
double area = std::numbers::pi * r * r;     // standard, works everywhere
```

The pattern behind both: **code that compiled on your machine is not automatically standard, nor available on the next compiler.** When a universal form exists — the operator symbols, `std::numbers::pi` — prefer it.

### Filenames: `Motor.hpp` is not `motor.hpp` on Linux

Windows and macOS filesystems are normally **case-insensitive**: `Motor.hpp` and `motor.hpp` are the same file. Most Linux filesystems are **case-sensitive**: they are two different files. So:

```cpp
#include "Motor.hpp"   // the file on disk is actually motor.hpp
```

builds on Windows and macOS, then fails on Linux with `No such file or directory`. **Match the case exactly** in every `#include` and every filename.

### Do not assume how big a type is

The standard pins down surprisingly little about integer sizes. The one that bites in practice is `long`:

| Type | Windows (MSVC) | Linux / macOS |
|------|----------------|---------------|
| `int` | 32-bit | 32-bit |
| `long` | **32-bit** | **64-bit** |
| `long long` | 64-bit | 64-bit |

Code that assumes `long` holds a 64-bit value is wrong on Windows; code that assumes `long` is the same size as `int` is wrong on Linux. When the exact width matters, use the **fixed-width types** from `<cstdint>` — `std::int32_t`, `std::int64_t`, `std::uint8_t` — which mean the same thing everywhere. (You met the same idea on the [Arduino](arduino_vs_desktop.md), where `int` is only 16 bits; the reasoning is identical.)

> The source-level traps and their fixes, at a glance:
>
> | Trap | Symptom on the other machine | Fix |
> |------|------------------------------|-----|
> | Relying on transitive `#include`s | "`X` is not a member of `std`" | Include a header for everything you use |
> | Using a too-new feature | "`<format>` not found", missing names | Check every target compiler supports it |
> | Compiler-specific spelling or macro (`or`, `M_PI`) | `'or'` / `'M_PI'` undeclared on another compiler | Use symbol operators, not word forms; and `std::numbers::pi`, not `M_PI` |
> | Wrong filename case | "No such file or directory" on Linux | Match case exactly in `#include`s |
> | Assuming type sizes | Wrong results or overflow | Use `<cstdint>` fixed-width types |

---

## Speed, size, and behaviour can differ too

Even when the same source *does* compile everywhere, the program you get is not identical.

**Speed and size.** The machine code is produced by *that* compiler's optimiser, and GCC, Clang, and MSVC optimise differently — one may produce a faster or smaller program than another from the same source. The standard library itself is a *different implementation* on each platform (Microsoft's, GNU's `libstdc++`, LLVM's `libc++`), and these differ in performance: a `std::regex` search or a `std::unordered_map` lookup can be markedly faster under one than another. And a [Release build is far faster than a Debug build](Chapter2/cmake_intro.md#build-configurations-debug-and-release) of the very same code. "How fast is this program?" has no single answer — it depends on the compiler, the standard-library implementation, the build configuration, and the hardware.

**Behaviour.** Most well-written code behaves the same everywhere. The exception is code that leans on things the standard deliberately leaves open:

- **Undefined behaviour** — reading past the end of an array, using an uninitialised variable, signed-integer overflow — may *happen* to work on one platform and crash on another. It is never safe to rely on; this book flags it as it appears.
- **Floating-point** results can differ in the last digits between compilers and optimisation levels. When that can matter, read [Floating-Point Pitfalls](floating_point.md).

The takeaway: portable behaviour comes from writing *correct, standard* C++ — not from code that merely happened to work on the one machine you tested.

---

## Compile times differ

How *long* the build takes is platform- and compiler-dependent too: the same project can compile noticeably faster or slower under GCC, Clang, or MSVC, and on different machines. This is not a correctness problem, just one to expect — do not be alarmed when a project that builds in seconds on one setup takes longer on another. (What you *can* influence: a clean rebuild is slow, but afterwards CMake recompiles only the files you changed, and heavily [templated](Chapter5/templates.md) code is slower to compile than plain code.)

---

## What to do about it

You do not need your coursework to run on five platforms. But a few habits cost nothing and keep your code honest:

- **Include what you use.** One `#include` for every standard facility you name. Never rely on one header dragging in another.
- **Turn warnings on** — `-Wall -Wextra` (GCC/Clang) or `/W4` (MSVC). See [CMake](Chapter2/cmake_intro.md#turn-on-compiler-warnings). Warnings are often the first sign of non-portable code.
- **Stick to the standard library and CMake.** Avoid compiler-specific extensions and OS-specific headers (like `<windows.h>`) unless you truly need them — and when you do, keep them isolated.
- **Use fixed-width integer types** (`<cstdint>`) when the size matters; never assume how big `long` is.
- **Write paths portably** — forward slashes or `std::filesystem::path` — and match filename case exactly. See [Computer Basics](computer_basics.md).
- **The only proof is to build and run it there.** If code must work on another platform, compile and test it on that platform. (Automating that is one job of *continuous integration*.) Reading the source is not enough — "works on my machine" is a statement about your machine.

---

## Summary

- A **compiled executable** targets one OS and one CPU; to run elsewhere you **recompile**. CMake makes rebuilding easy but does not make the binary portable.
- The **same source can fail to compile** on another compiler even using only the standard library — usually from relying on transitive `#include`s, using a too-new C++20 feature, using a compiler-specific spelling or macro (`or`, `M_PI`), wrong filename case, or assuming type sizes.
- **Speed, size, and even behaviour** can differ across compilers, standard-library implementations, build configurations, and hardware; undefined behaviour and floating-point are the usual sources of behaviour differences.
- **Compile times** vary by compiler and machine — expected, not a bug.
- Cheap habits keep code portable: *include what you use*, *warnings on*, *fixed-width types*, *portable paths*, and above all **test on the platform that has to run it.**
