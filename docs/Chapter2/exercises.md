# Chapter 2 Exercises

Work through these after reading Chapter 2. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Both exercises are done in a real project and terminal — a `CMakeLists.txt` you write and a sequence of `git` commands you run. There is nothing to "run on Compiler Explorer"; the point is to do them for real on your own machine. (PlatformIO has no paper exercise — it needs a real board, so its practice belongs in the lab with hardware in hand.)

---

## 1. A project with two programs

*Practises: [CMake](cmake_intro.md)*

You want to keep two of your Chapter 1 solutions — `ex1.cpp` and `ex2.cpp` — in a single project, each runnable on its own. Write a `CMakeLists.txt` that builds both as **separate executables**, uses **C++20**, and turns **compiler warnings on** for each.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cmake
    cmake_minimum_required(VERSION 3.15)
    project(chapter1_solutions)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    add_executable(ex1 ex1.cpp)
    target_compile_options(ex1 PRIVATE -Wall -Wextra)

    add_executable(ex2 ex2.cpp)
    target_compile_options(ex2 PRIVATE -Wall -Wextra)
    ```

    One `add_executable` per program gives you two entries in the run-configuration dropdown next to the green ▶ button — exactly the setup the Chapter 1 exercises suggested. `CMAKE_CXX_STANDARD` is set once near the top and applies to every target below it; warnings are switched on per target with `target_compile_options`. (You could instead apply them to everything with `add_compile_options(-Wall -Wextra)` before the targets — either is fine.)

    </div>

---

## 2. Save your work with git

*Practises: [Version Control & Git](version_control.md)*

You have just created a new project folder containing a `CMakeLists.txt` and a `main.cpp`. Using git, (1) turn the folder into a repository, (2) save both files in a first commit with a sensible message, and then (3) start a branch called `experiment` to try a change without disturbing `main`. Write the commands in order.

> Hint: a quick `git status` between steps is always a good way to check what git thinks is going on.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```bash
    git init                                  # turn the folder into a repo
    git status                                # see what is untracked

    git add CMakeLists.txt main.cpp           # stage both files
    git commit -m "Initial project: builds Hello World"

    git switch -c experiment                  # create + move onto a new branch
    ```

    `git add` only *stages* the files — it marks them for the next snapshot. `git commit` is what actually records the snapshot, and its message says what this state is. `git switch -c experiment` creates the branch and moves you onto it in one step; anything you commit now lands on `experiment`, leaving `main` untouched until you choose to merge.

    </div>
