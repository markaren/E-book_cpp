# CMake

So far you have run programs through CLion's green play button. That button is calling a build tool behind the scenes, and that tool is **CMake**.

CMake is not a compiler. It is one level above: you describe your project to CMake in a small file called `CMakeLists.txt`, and CMake generates the platform-specific instructions (Makefiles on Linux, Visual Studio project files on Windows, Xcode projects on macOS) that your compiler then follows. Write the project description once; build it anywhere.

You will spend the rest of your career writing C++ inside CMake projects. This chapter teaches the minimum you need today, then shows how it grows as your project does.

---

## The smallest CMake project

A single-file program needs three lines:

```cmake
cmake_minimum_required(VERSION 3.15)
project(hello)

add_executable(hello main.cpp)
```

That is it. Save as `CMakeLists.txt` next to `main.cpp`, and CLion (or `cmake -B build && cmake --build build` on the command line) will compile `main.cpp` into an executable called `hello`.

What each line does:

| Line | Meaning |
|------|---------|
| `cmake_minimum_required(VERSION 3.15)` | The oldest CMake version that can build this project. 3.15 is a sensible floor for modern C++. |
| `project(hello)` | Names the project. Must come before any targets. |
| `add_executable(hello main.cpp)` | Define an executable target named `hello`, built from `main.cpp`. |

You will copy this template into many projects. Get familiar with it.

---

## Setting the C++ standard

The default standard depends on the compiler, and it is rarely the one you want. Set it explicitly:

```cmake
cmake_minimum_required(VERSION 3.15)
project(hello)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(hello main.cpp)
```

`CMAKE_CXX_STANDARD 20` tells the compiler to use C++20 (the standard this course teaches). `CMAKE_CXX_STANDARD_REQUIRED ON` makes it a hard requirement, without it, an older compiler would silently fall back to whatever it supports.

---

## Turn on compiler warnings

Several pages in this book tell you to "turn warnings on." A **warning** is the compiler flagging code that is legal but probably a mistake — `if (x = 5)` instead of `==`, a variable you declared and never used, a function that forgets to `return`. They are some of the most valuable feedback the compiler gives you, and most of them are **off by default**.

Switch them on for your project by adding one line to `CMakeLists.txt`:

```cmake
add_executable(hello main.cpp)
target_compile_options(hello PRIVATE -Wall -Wextra)
```

`-Wall -Wextra` enable the common, worthwhile warnings. (Those are GCC and Clang flag names; CLion's bundled compiler is GCC, so they work out of the box. With Microsoft's MSVC you would write `/W4` instead.) Warnings now appear in CLion's build window every time you compile — read them.

Once your code builds cleanly, you can make warnings **fatal**, so a warning stops the build instead of scrolling past:

```cmake
target_compile_options(hello PRIVATE -Wall -Wextra -Werror)
```

`-Werror` is stricter than you need on your first day, but it is a habit worth growing into: it guarantees you never ignore a warning by accident.

---

## Multiple source files

A real project quickly grows beyond one file. Suppose you have:

```
hello/
├── CMakeLists.txt
├── main.cpp
├── motor.cpp
└── motor.hpp
```

Just list the additional `.cpp` files in `add_executable`:

```cmake
add_executable(hello main.cpp motor.cpp)
```

Header files (`.hpp` / `.h`) are *not* listed, they are pulled in by `#include` lines in the source files. CMake only needs to know which `.cpp` files to compile.

For larger projects you can glob, but glob-based source lists do not pick up new files until CMake re-runs. Explicit lists are clearer:

```cmake
add_executable(hello
    main.cpp
    motor.cpp
    sensor.cpp
    controller.cpp
)
```

---

## Headers in a separate folder

A convention that pays off as projects grow:

```
hello/
├── CMakeLists.txt
├── include/
│   ├── motor.hpp
│   └── sensor.hpp
└── src/
    ├── main.cpp
    ├── motor.cpp
    └── sensor.cpp
```

Tell CMake where the headers live so `#include "motor.hpp"` works from inside any source file:

```cmake
add_executable(hello src/main.cpp src/motor.cpp src/sensor.cpp)
target_include_directories(hello PRIVATE include)
```

`target_include_directories(<target> PRIVATE <path>)` adds `<path>` to the list of folders the compiler searches for `#include`d files when building `<target>`.

`PRIVATE` means "this is only used to build this target." For executables this is always what you want. (You will see `PUBLIC` and `INTERFACE` when you start writing libraries that other code links to.)

---

## Building libraries

Once you have several executables that share code (your tests, your main program, perhaps a quick CLI tool), put the shared code in a **library** so it is compiled once:

```cmake
add_library(motor src/motor.cpp src/sensor.cpp)
target_include_directories(motor PUBLIC include)

add_executable(hello src/main.cpp)
target_link_libraries(hello PRIVATE motor)
```

What changed:

- `add_library` defines a library target. The default is a **static** library, its contents are baked into anything that links it. (You can pass `STATIC`, `SHARED`, or `OBJECT` if you need a specific kind.)
- `target_link_libraries(hello PRIVATE motor)` tells CMake that the `hello` executable uses the `motor` library. The compiler now sees `motor`'s headers, and the linker now combines `motor`'s compiled code into `hello`.
- The library uses `PUBLIC` for its include directory, meaning anyone linking to `motor` *also* gets `motor`'s `include/` folder on their search path. That is what you want for a library's public headers.

---

## Building from the command line

CLion drives CMake for you, but every CMake project can also be built directly:

```bash
# Configure: generate build files in a 'build/' folder
cmake -B build

# Build everything
cmake --build build

# Run the executable (path varies slightly by platform)
./build/hello              # Linux / macOS
./build/Debug/hello.exe    # Windows with MSVC
```

The `-B build` flag puts all generated files into `build/` so they stay out of your source tree. Add `build/` to your `.gitignore` (or use `*/build` if you have nested projects).

For release builds with optimisations on:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

---

## A note on project layout

The layout below scales from one-file scripts to multi-library systems:

```
my_project/
├── CMakeLists.txt
├── README.md
├── .gitignore
├── include/        # public headers
├── src/            # implementation files
└── tests/          # tests (see Chapter 5)
```

You do not need all of these on day one. Start with one `main.cpp` and one `CMakeLists.txt`. Split into `src/` and `include/` when you have more than four or five files. Add `tests/` when you start writing tests. The point is to grow into the structure, not to set it all up before writing any code.

For a more elaborate convention used in larger industry projects, see [the Pitchfork Layout](https://joholl.github.io/pitchfork-website/).

---

## Summary

- `CMakeLists.txt` describes your project; CMake turns the description into platform-specific build files.
- Three lines suffice for a single-file program: `cmake_minimum_required`, `project`, `add_executable`.
- Set `CMAKE_CXX_STANDARD 20` explicitly.
- Add more source files by listing them in `add_executable`. Headers do not need to be listed.
- Use `target_include_directories` when headers live in a separate folder.
- Use `add_library` and `target_link_libraries` once you have code shared between executables.
- Keep build artefacts in a separate `build/` folder; ignore it in git.
