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

A project you are *presenting* — a portfolio piece, like the [capstone](capstone.md) — needs more than this; see [Presenting a bigger project](#presenting-a-bigger-project) below.

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

## Presenting a bigger project

Some projects are not just used but *shown*: a course portfolio, a capstone, something you want a future employer to look at. Then the README is also your presentation, written by you, in your own words, and it has two more jobs: **show** what the project does, and **explain** the thinking behind it.

### Show it: screenshots and GIFs

A reader who sees your program running understands it in seconds; a paragraph takes much longer. Put a picture, or better a short animated GIF, near the top.

- **Screenshot.** On Windows, press **Win + Shift + S**, choose **Window** mode in the bar at the top of the screen, and click the program's window. Windows 11 usually saves the picture in *Pictures\Screenshots*; if it does not, click the notification that pops up and save it from there. Move the file into your project. (On macOS: **Cmd + Shift + 4**, then **Space**, then click the window.)
- **GIF.** Use a free screen-to-GIF recorder — for example [ScreenToGif](https://www.screentogif.com/) on Windows. Record just the program's window, keep it to 5–10 seconds, and keep the file small (a few MB), or the page loads slowly.
- **Store them in the repository**, in a folder such as `docs/images/`, and commit them with the code. Use file names without spaces (`onoff-demo.gif`, not `on off demo.gif`).
- **Show them** with the image syntax — an exclamation mark, a short description of the picture, and the path *relative to the README*:

    ```markdown
    ![The tank under on/off control](docs/images/onoff-demo.gif)
    ```

    The description in square brackets is shown to readers who cannot see the image, so make it say what the picture shows. Check that the image appears in CLion's Markdown preview before you commit, and on GitHub after you push.

Capture as you go. The screenshot of a bug before you fixed it, or of the first run that worked, cannot be taken afterwards.

### Explain it

For a project you present, add sections like these after *what it is* and *how to build and run it*:

- **How it works** — the main parts and how they talk to each other, with a [UML class diagram](uml.md) of the types you wrote.
- **Why it is built this way** — the decisions you made, the alternatives you rejected, and the trade-offs. This is where you argue that it is a good solution.
- **What did not make it** — what you wanted to build but did not, what does not work yet, and what it would take. Knowing the limits of your own solution is part of understanding it, and a README that is honest about them is more convincing than one that claims everything works.
- **How you worked** — the short story of the project, pointing at the commits and notes that show it: the hardest problem, how you found the cause, what you would do differently.
- **How you used AI**, or that you did not — which tools and models, what you used them for, how you worked with them, where they were wrong, and what you learned from it ([Using AI for Coding](using_ai.md)).
- **Credits** — code you did not write, and where it came from.

---

## Summary

- The `README.md` at your repository root is the project's front page; hosting sites render it automatically.
- It is written in **Markdown** — see the [cheat sheet](https://www.markdownguide.org/cheat-sheet/).
- Answer **what is this, how do I build it, how do I run it**, in that order.
- Scale it to the project, lead with usage, and keep it honest and up to date.
- The real test: a stranger should be able to build and run your project from the README alone.
- A project you present also **shows** itself — screenshots and GIFs, stored in the repository — and **explains** itself: how it works, why it is built this way, what did not make it, how you used AI.
