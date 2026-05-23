# Computer Basics

Programming tools assume you already know a few things about your computer that most people never had to learn: how files and paths really work, what the "terminal" is, and how the system finds the programs you run. Courses rarely teach these, yet they trip up beginners constantly — a build that fails because of a space in a folder name, a `command not found` that is really a PATH problem, a tutorial command that does nothing because it was written for a different shell.

This page covers that taken-for-granted layer: **the filesystem and paths, the terminal and its shells, and the PATH variable.** You do not need to memorise it — skim it now, and come back when something here bites you.

---

## Files, folders, and paths

Your files live in **folders** (also called **directories**), which nest inside one another to form a tree. A **path** is the address of a file or folder: the list of folders you walk through to reach it.

- An **absolute path** starts from the top (the "root") and is unambiguous:
    - Windows: `C:\Users\ada\projects\hello\main.cpp`
    - macOS / Linux: `/home/ada/projects/hello/main.cpp`
- A **relative path** is relative to where you currently are — your *working directory*: `projects/hello/main.cpp`, or `../other` to go up one level.

Your **home directory** is your personal folder: `C:\Users\<you>` on Windows, `/Users/<you>` on macOS, `/home/<you>` on Linux. It is often written `~`.

### The working directory

Your **working directory** (or "current directory") is the folder a program is "in" right now — the folder that relative paths are measured from. In a terminal, `pwd` prints it and `cd` changes it.

It matters for a running program too. When your code opens a file by a plain name — `std::ofstream out("report.txt")` — it does not look in your project folder; it looks in the *working directory of the running program*, and **when you launch from an IDE, that is usually not where you expect.** CLion runs your program from the build folder (e.g. `cmake-build-debug/`), so a `report.txt` your program writes lands *there*, and a `readings.txt` it reads must live *there* too — not beside your source code.

If a program "cannot find" a file that clearly exists, or writes one you then cannot find, the working directory is almost always why. In CLion you can see or change it under **Run → Edit Configurations → Working directory**.

### `/` versus `\`

A classic source of confusion:

- **Windows** separates folders with a **backslash** `\`.
- **macOS and Linux** use a **forward slash** `/`.

This matters in C++, because inside a string a backslash is an *escape character*:

```cpp
std::string bad = "C:\dev\hello";    // WRONG: \d and \h are not valid escapes
std::string a   = "C:\\dev\\hello";  // works: escape each backslash
std::string b   = "C:/dev/hello";    // simpler: forward slashes work on Windows too
```

Windows file functions happily accept `/`, so when you must write a path in code, **prefer forward slashes** and skip the escaping headache. (`std::filesystem::path` also handles separators for you.)

### Keep paths short, simple, and plain

Where you put your projects matters more than beginners expect:

- **Avoid long, deeply-nested paths.** Windows has historically capped a full path at 260 characters, and many tools still break past that. A project buried under `Documents\University\Semester 1\AIS1003\Assignments\…` can hit the wall. Put your code somewhere short, like `C:\dev\`.
- **Avoid spaces.** `My Projects` forces you to quote the path on the command line (`"My Projects"`) and some tools mishandle it. Prefer `my-projects` or `my_projects`.
- **Avoid special and non-English characters.** Norwegian `æ`, `ø`, `å`, accented letters, and symbols like `#`, `&`, `(` confuse compilers, build tools, and scripts in ways that produce baffling errors. Stick to plain letters, digits, `-`, and `_`.
- **Avoid cloud-synced folders** (OneDrive, Dropbox, Google Drive) for code: a build creates thousands of files that sync constantly, and machine-specific build files cause conflicts across computers.

A good home for your coursework: `C:\dev\ais1003\` on Windows, or `~/dev/ais1003/` on macOS/Linux.

---

## The terminal

The **terminal** is a window where you control the computer by *typing commands* instead of clicking. You type a command, press Enter, the computer runs it and prints the result, then gives you a fresh **prompt** for the next command:

```
C:\dev\hello>          (the prompt — here it also shows your current folder)
```

Why bother, when there is a perfectly good graphical interface?

- **Most developer tools are command-line first** — `git`, CMake, compilers, package managers. The buttons in your IDE are often just running these commands for you.
- **It is precise and repeatable.** A command is exact; it can be written down, shared, scripted, and re-run identically. "Click here, then there, then…" cannot.
- **It shows you what is happening.** When something fails, the terminal's output is where the real error message is.
- **It works everywhere**, including on remote machines and servers that have no graphical interface at all.

You need not abandon the GUI — but a programmer who refuses to touch the terminal is working with one hand tied.

A command is usually a program name, optionally followed by **arguments** (what to act on) and **options** or **flags** (how to act). In:

```
git commit -m "Fix the bug"
```

`git` is the program, `commit` a subcommand, `-m` an option, and `"Fix the bug"` the argument to that option. Note the quotes: if anything you type contains spaces, wrap it in quotes so it is treated as one item (`cd "My Folder"`).

---

## Shells: PowerShell, cmd, bash, zsh

People say "the terminal" loosely, but there are really two separate things:

- The **terminal** is the *window* — the app that shows text and takes your keystrokes.
- The **shell** is the *program running inside it* that actually interprets the commands you type.

Several shells exist, and **their commands and syntax differ** — which is why a command copied from a Linux tutorial may fail on Windows:

| Shell | Where you meet it | Notes |
|-------|-------------------|-------|
| **Command Prompt (`cmd`)** | Windows (old) | Limited; you will rarely choose it on purpose. |
| **PowerShell** | Windows (modern default) | Capable; the one to use on Windows. |
| **bash** | Linux, Git Bash, WSL | The classic Unix shell; most online examples assume it. |
| **zsh** | macOS (modern default) | Bash-like for everyday use. |

A few differences you will actually run into:

| Task | bash / zsh | PowerShell | cmd |
|------|------------|------------|-----|
| List files in a folder | `ls` | `ls` or `dir` | `dir` |
| Show the current folder | `pwd` | `pwd` | `cd` |
| Read a variable | `$HOME` | `$env:USERPROFILE` | `%USERPROFILE%` |

The practical rule: **know which shell you are in**, and when you copy a command off the internet, check it matches. On Windows, prefer **PowerShell** — it is what the terminal built into CLion uses by default. On macOS and Linux, the default shell (zsh or bash) is fine.

---

## PATH: how the computer finds programs

When you type `git` in a terminal, how does the computer know where `git` actually lives on disk? It checks an environment variable called **`PATH`** — a list of folders to search, in order, for a program with that name.

- If `git` is found in one of those folders, it runs.
- If it is not, you get **`command not found`** (or, on Windows, `'git' is not recognized…`).

So that error almost always means one of two things: the program is **not installed**, or it is installed but **its folder was never added to `PATH`**. Many installers add themselves to `PATH` automatically; some — and most manual installs — do not, and then you have to add the folder yourself.

`PATH` is one of several **environment variables**: named values the system keeps for programs to read. As a beginner you will mostly meet `PATH`, and mostly when a freshly-installed tool "cannot be found."

> You will rarely need to edit `PATH` by hand for this course — CLion bundles the tools it needs. But when a tutorial says "make sure X is on your `PATH`," this is what it means.

---

## Rules of thumb

- Keep projects in a **short, plain path** near the drive root (`C:\dev\…`), not a deep folder full of spaces and Norwegian letters.
- In C++ code, write paths with **forward slashes** (`"C:/dev"`) or escape the backslashes (`"C:\\dev"`).
- A program reads and writes relative paths (like `"report.txt"`) from its **working directory** — which your IDE often sets to the build folder, not your project folder.
- The **terminal** is worth learning: most tools live there, and it shows you the real errors.
- A **shell** (PowerShell, bash, zsh, cmd) interprets your commands, and they differ — match copied commands to your shell. On Windows, use PowerShell.
- **`command not found`** usually means "not installed" or "not on `PATH`."
