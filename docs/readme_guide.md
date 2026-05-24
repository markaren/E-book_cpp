# The README

Every project has a front door, and it is the `README`. It is the first thing a grader, a teammate, or you-in-six-months opens — before the code, before anything. A good one answers three questions, in order: **what is this, how do I build it, how do I run it.** A project with no README is a locked house with no sign on the door: people have to guess what is inside and how to get in.

---

## Where it lives, and why everyone sees it

The file is called `README.md`, and it sits at the **root** of your repository, next to `CMakeLists.txt`. GitHub, GitLab, and the like render it automatically on the project's front page — so it is, quite literally, the first thing a visitor reads. Commit it from day one and keep it in version control alongside the code (see [Version Control & Git](Chapter2/version_control.md)).

---

## It's just Markdown

The `.md` means **Markdown** — the same lightweight text format this book is written in. A little goes a long way:

```markdown
# A heading

Some text, with **bold** and `inline code`.

- a list item
- another one

[a link](https://example.com)
```

That covers most of what a README needs. For the full syntax — tables, images, quotes, and the rest — keep the [Markdown cheat sheet](https://www.markdownguide.org/cheat-sheet/) within reach.

---

## What to put in it

Scale the README to the project. A small course project needs only the first few of these; do not pad it with sections you do not actually have:

- **Title and one-line description** — what the thing *is*, in a sentence.
- **Build** — the exact commands (for us, the [CMake](Chapter2/cmake_intro.md) ones), so a reader can copy-paste them.
- **Run / usage** — how to start it, with an example and what to expect.
- **Project layout** *(optional)* — a quick map of `src/`, `include/`, `tests/`.
- **Tests** *(optional)* — how to build and run them.
- **Requirements** *(optional)* — compiler and CMake version, any libraries.

The order matters: lead with *what it is* and *how to run it*, because that is what a reader wants first.

---

## A small example

A README for a course project can be as short as this:

````markdown
# Sensor Monitor

Reads temperature samples from a file, flags any that are out of range,
and prints a short report. Course project for AIS1003.

## Build

```bash
cmake -B build
cmake --build build
```

## Run

```bash
./build/monitor readings.txt
```

Example output:

```
temp: 4 readings, max 91.0 (Critical)
```

## Layout

- `src/`     — implementation
- `include/` — headers
- `tests/`   — Catch2 unit tests

## Tests

```bash
cmake -B build -DBUILD_TESTS=ON
ctest --test-dir build
```
````

Short — but a stranger could clone it and be up and running in a minute.

---

## Write it for a stranger

The test of a README is simple: **could someone who has never seen your project clone it, build it, and run it using the README alone?** If not, something is missing — usually a build step you do without thinking, or a dependency you forgot you had installed.

Two habits make the difference:

- **Write for someone who knows nothing about the project** — including future-you, who will have forgotten the details.
- **Keep it current.** A README that lies — a build command that no longer works — is worse than none at all. When the build changes, update the README in the same commit.

---

## Summary

- The `README.md` at your repository root is the project's front page; hosting sites render it automatically.
- It is written in **Markdown** — see the [cheat sheet](https://www.markdownguide.org/cheat-sheet/).
- Answer **what is this, how do I build it, how do I run it**, in that order.
- Scale it to the project, lead with usage, and keep it honest and up to date.
- The real test: a stranger should be able to build and run your project from the README alone.
