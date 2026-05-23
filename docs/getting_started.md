# Getting Started

To write C++ you need two things: a **compiler** — the program that turns the C++ you type into an *executable*, a file your computer can actually run — and somewhere to write and run your code. This course uses **CLion**, an IDE (Integrated Development Environment: the application you write, build, run, and debug code in). CLion comes with everything you need bundled in, so setup is short.

This page gets you from nothing to a running "Hello, World!". JetBrains' [Quick Start Guide](https://www.jetbrains.com/help/clion/clion-quick-start-guide.html) shows the same steps with screenshots if you would like to follow along visually.

---

## 1. Install CLion

1. Download CLion from [jetbrains.com/clion](https://www.jetbrains.com/clion/) and run the installer with the default options.
2. CLion is **free for students**. The first time it launches it will ask you to sign in — create a free JetBrains account and activate the free licence through the [JetBrains educational program](https://www.jetbrains.com/community/education/#students).

<!-- screenshot: CLion first-run / sign-in screen -->

CLion also bundles **CMake** (the build tool the course uses), so you do not need to install that separately. The only piece that depends on your operating system is the compiler — **click the tab for your OS**:

=== "Windows"

    **Nothing extra to install.** CLion comes with a working compiler (the *MinGW toolchain*) built in. Accept the defaults and you are ready.

    *Advanced, optional:* you can instead use Microsoft's MSVC compiler from [Visual Studio](https://visualstudio.microsoft.com/vs/community/). Skip this unless your instructor specifically asks for it — the bundled compiler is fine for everything in this book.

=== "macOS"

    Install Apple's command-line developer tools, which include the Clang compiler. Open the **Terminal** app and run:

    ```
    xcode-select --install
    ```

    Follow the prompt. CLion then detects the compiler automatically.

=== "Linux"

    Install the GCC compiler and build tools. On Debian/Ubuntu, open a terminal and run:

    ```
    sudo apt-get update && sudo apt-get install build-essential
    ```

    CLion then detects the compiler automatically.

---

## 2. Create your first project

1. On the welcome screen choose **New Project** (or **File → New Project** if CLion is already open).
2. Select **C++ Executable**.
3. If the dialog shows a **Language standard** option, set it to **C++20**. (Some CLion versions don't — the generated `CMakeLists.txt` already sets C++20, so you are covered either way.)
4. Choose a location for the project — but read the warning below first — and click **Create**.

<!-- screenshot: New Project dialog with "C++ Executable" selected -->

> **Where to put your project.** Avoid a folder inside cloud storage (OneDrive, Dropbox, Google Drive). Building generates a large number of files that would sync constantly, and if you use more than one PC the machine-specific build files cause conflicts. Also avoid paths with spaces or special characters — including Norwegian `æ`, `ø`, `å` — which cause confusing errors on Windows. A simple path such as `C:\dev\projects` is ideal. ([Computer Basics](computer_basics.md) explains why paths, spaces, and special characters matter.)

CLion creates a starter "Hello, World!" project for you, with two files:

```cmake
# CMakeLists.txt — tells the build tool how to build your program
cmake_minimum_required(VERSION 3.20)
project(demo)

set(CMAKE_CXX_STANDARD 20)

add_executable(demo main.cpp)
```

```cpp
// main.cpp — your program
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

Do not worry about what each line means yet — [Basic Structure](Chapter1/basic_structure.md) breaks the program down piece by piece, and [CMake Introduction](Chapter2/cmake_intro.md) covers the `CMakeLists.txt`. (You will also learn there why this book usually prefers `'\n'` to `std::endl`; CLion just happens to generate `std::endl`.)

---

## 3. Build and run

C++ has to be **compiled** into an executable before it can run. CLion does both with one click:

- Click the green **▶ Run** button near the top-right corner (or press **Shift+F10**).
- The hammer icon next to it *builds* without running, if you ever want that.

<!-- screenshot: top-right toolbar showing the Run (play) and Build (hammer) buttons -->

---

## 4. Check it worked

The **Run** tool window opens at the bottom of CLion and should show something like:

```
Hello, World!

Process finished with exit code 0
```

`exit code 0` means the program ran successfully. If you see that, your setup is working and you are ready for the [Introduction](Chapter1/introduction.md).

<!-- screenshot: Run tool window showing the output and "exit code 0" -->

---

## If something went wrong

The most common first-run problems:

- **"No toolchain configured" or the compiler is not found.** Open **File → Settings → Build, Execution, Deployment → Toolchains**. On Windows there should be a bundled **MinGW** entry; if it is missing, click **+** and add it. On macOS/Linux, make sure you installed the compiler from the tab in Step 1.
- **A red error appears in the CMake panel at the bottom.** This is almost always a bad project location — a path with spaces or special characters, or a cloud-storage folder. Delete the project and recreate it in a simple path like `C:\dev\projects`.
- **The Run button is greyed out or nothing happens.** CLion is probably still loading the project — wait for the progress bar at the bottom to finish, then try again.
- **Still stuck on an error message.** Read [Reading Compiler Errors](compiler_errors.md), then copy the *exact* error text into a search engine — or into an AI assistant, following [Using AI for Coding](using_ai.md).
