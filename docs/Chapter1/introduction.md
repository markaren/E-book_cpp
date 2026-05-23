# Introduction

Programming is the act of giving a computer step-by-step instructions to follow. You write the steps in a language the computer can be made to understand (in this course, **C++**), and a tool called a **compiler** translates them into something the machine can actually run.

This book is your companion for AIS1003. It will not replace practice. Most of what you learn about programming comes from writing code, making mistakes, and figuring out what went wrong. The chapters here are a reference and a starting point; the keyboard is where the real work happens.

---

## What is a program?

A program is a sequence of operations the computer carries out in order. At its smallest:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world!" << "\n";
    return 0;
}
```

Five lines, but every part matters:

- `#include <iostream>` pulls in the part of the standard library you need to print to the screen.
- `int main()` declares the **entry point**. Every C++ program starts here.
- The line ending in `;` is one **statement**, one thing for the computer to do.
- `return 0` signals to the operating system that the program finished successfully.

When you run this, the compiler reads the source code, checks it for errors, translates it into instructions for your CPU, and produces an executable file. You then run that file, and the text appears.

---

## Why C++?

You will hear that C++ is a "difficult" language. There is truth to that: it gives you direct control over the machine, and with that control comes more ways to make mistakes than in something like Python. But it is the right tool for what automation engineers actually do:

- **Embedded systems and robotics.** Arduino, PlatformIO, ROS, industrial controllers; almost all run code written in C++ or C.
- **High-performance numerical work.** Control loops, signal processing, simulations.
- **Game engines and graphics.** Unreal, large parts of Unity's runtime.
- **Operating systems and drivers.** Code that talks to hardware directly.

The language has also evolved a lot. **Modern C++** (C++11 and later) is far friendlier than the C++ of twenty years ago. This course teaches C++20, which is what you should be writing today.

---

## Compiled, statically typed

Two properties of C++ shape how you write it.

**Compiled.** Your source code is translated to machine code *once*, ahead of time, by the compiler. The program does not run until compilation succeeds. This means many bugs (typos, type mismatches, missing semicolons) are caught before the program ever executes. Compare this to Python, which runs your code line-by-line and only discovers a typo on line 200 when execution reaches line 200.

**Statically typed.** Every variable has a fixed type that you declare up front:

```cpp
int age = 25;         // age holds whole numbers, forever
double price = 19.99; // price holds decimals, forever
```

You cannot later put a string in `age`. The compiler enforces this. Static typing means more typing for you, but in exchange the compiler catches a large class of bugs automatically: you cannot accidentally pass a string where a number is expected.

A short list of consequences you will run into:

| Property                   | What it means for you                                                                            |
|----------------------------|--------------------------------------------------------------------------------------------------|
| Compiled                   | You must rebuild before you can test a change. Read compiler errors carefully.                   |
| Statically typed           | You declare every variable with a type. Mismatches are compile-time errors, not runtime crashes. |
| No garbage collector       | You manage when memory is freed (later chapters cover the modern, painless way).                 |
| Undefined behaviour exists | The language has corners where "anything could happen." We will name them as they appear.        |

---

## Object-oriented programming

OOP is the way C++ is normally written. Instead of one long list of instructions, you organise your code around **objects**: bundles of data together with the operations that work on that data.

A `Motor` object might hold its current speed and its maximum speed, and provide operations like `setSpeed()`, `stop()`, and `getStatus()`. The rest of your program treats the motor as a single unit and does not need to know how the internals work.

The key terms you will meet:

| Term              | Meaning                                                                                          |
|-------------------|--------------------------------------------------------------------------------------------------|
| **Class**         | The blueprint. Describes what data an object holds and what it can do.                           |
| **Object**        | An actual instance of a class; a specific motor, sensor, or controller in memory.                |
| **Member**        | A piece of data or a function that belongs to a class.                                           |
| **Encapsulation** | Hiding the inside of a class behind a clean interface, so outside code cannot break invariants.  |
| **Inheritance**   | Building a new class on top of an existing one.                                                  |
| **Polymorphism**  | Treating different concrete types through a common interface.                                    |

We will not write a class today. Chapter 4 covers them properly. For now, keep these words in the back of your mind.

---

## How to use this book

Read each chapter, then write code. Type the examples by hand rather than copy-pasting; the typos you make are how you learn what the compiler complains about. When you get an error you do not understand, see the [Reading Compiler Errors](../compiler_errors.md) reference, then search the exact error text. Almost every compiler error has been asked about on Stack Overflow.

If you have written some Python before — many of you have — [Coming from Python](../python_to_cpp.md) maps what carries over and the "false friends" that will trip you up.

AI assistants will happily write C++ for you. Read [Using AI for Coding](../using_ai.md) before relying on them. The short version: they are excellent tools and treacherous teachers, and using them well requires a few specific habits.

When this book gives a recommendation, it is the one you should follow unless you have a specific reason not to. C++ has many ways to do most things, and a beginner who tries to learn *all* of them ends up confused. Learn the one good way first.

Up next: [Basic Structure](basic_structure.md) breaks down a complete C++ program piece by piece. If you have not yet installed CLion, see [Getting Started](../getting_started.md) first.
