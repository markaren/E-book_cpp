# Code Style

Code is read far more often than it is written. A consistent style makes a program easier to read, change, and review — and in group work it stops trivial differences (one person's two-space indent, another's four) from drowning the real changes in every commit.

This page gathers the conventions this book follows in one place, then shows how to let a tool enforce the mechanical parts automatically.

---

## The conventions this book uses

| Convention | Example | Covered in |
|------------|---------|------------|
| Locals, functions, parameters — `lowerCamelCase` | `int maxSpeed`, `readSensor()` | [Variables](Chapter1/variables.md) |
| Types and classes — `PascalCase` | `class SensorLog` | [Classes](Chapter4/classes.md) |
| Constants — `UPPER_SNAKE_CASE` | `const int MAX_RETRIES = 5;` | [Variables](Chapter1/variables.md) |
| Private data members — trailing `_` | `double balance_;` | [Classes](Chapter4/classes.md) |
| Always brace, even one-line bodies | `if (done) { return; }` | [Control Statements](Chapter1/control_statements.md) |
| Prefer `const` for anything you don't reassign | `const double limit = 0.85;` | [Variables](Chapter1/variables.md) |
| Always write `std::`; never `using namespace std;` | `std::vector<int> v;` | [C++ Standard Library](Chapter3/standard_library.md) |
| Prefer `"\n"` over `std::endl` | `std::cout << "done\n";` | [IO & Streams](Chapter4/io_streams.md) |
| Initialise variables where you declare them | `int count = 0;` | [Variables](Chapter1/variables.md) |
| Pass anything bigger than a number by `const&` | `void print(const std::string& s)` | [Values, References & Pointers](Chapter4/types_refs_ptrs.md) |
| Guard every header with `#pragma once` | first line of a `.hpp` | [Classes](Chapter4/classes.md) |

These are conventions, not rules of the language — but following them consistently, and matching the book, means the code you write looks like the examples you read here. When this book makes a recommendation, prefer it unless you have a specific reason not to.

---

## Let a tool format it: clang-format

Indentation, brace placement, spaces around operators, where lines wrap — the *mechanical* parts of style are not worth fixing by hand or arguing over. **clang-format** reformats your C++ to a fixed style automatically, so every file looks the same regardless of who wrote it or on which machine.

That last point is why it matters for **group work and moving between computers**: without a shared format, two people's editors lay code out differently, and every commit fills with formatting churn that hides the real change. With clang-format, layout simply stops being a discussion.

**One shared file.** clang-format takes its rules from a file named `.clang-format` at the root of your project. Commit it to git so every teammate — and every machine you use — formats identically. A small starting point:

```yaml
# .clang-format
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
```

`BasedOnStyle` picks a well-known base (LLVM, Google, Mozilla, …) and the lines below override individual rules. The exact values matter far less than everyone sharing the *same* file.

**In CLion.** CLion bundles clang-format and notices a `.clang-format` file automatically — when you open a project that has one, it offers to use it (or enable it under **Settings → Editor → Code Style → Enable ClangFormat**). Then:

- Reformat the current file with **Ctrl+Alt+L** (**⌥⌘L** on macOS).
- Optionally turn on **Settings → Tools → Actions on Save → Reformat code**, so files are formatted every time you save and you never think about it again.

(clang-format is also a command-line tool — `clang-format -i main.cpp` — and most editors support it, so the same `.clang-format` works outside CLion too.)

See JetBrains' [ClangFormat in CLion](https://www.jetbrains.com/help/clion/clangformat-as-alternative-formatter.html) guide and the full [clang-format style options](https://clang.llvm.org/docs/ClangFormatStyleOptions.html).

> clang-format fixes *layout*, not *meaning*. It will not rename a variable or add a `const` for you — the conventions above are still yours to apply.
