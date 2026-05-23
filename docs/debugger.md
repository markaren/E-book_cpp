# Using a Debugger

When your program will not compile, you [read the compiler error](compiler_errors.md). The harder problems are the ones where the program *builds and runs* — and quietly does the wrong thing. The instinct is to scatter `std::cout` everywhere to see what is happening. A **debugger** is the better tool: it pauses your running program wherever you ask and lets you look inside — inspect every variable, step through one line at a time, and watch exactly where reality diverges from what you expected.

This page shows the debugger built into CLion. The concepts — breakpoints, stepping, inspecting — are the same in every IDE and every language, so the skill carries over.

---

## Why not just use prints?

Adding a print to see a value works:

```cpp
std::cout << "got here, total = " << total << "\n";
```

But it is slow: edit, rebuild, run, read, then delete the prints and repeat. And it only shows the values you *thought* to print. A debugger lets you pause once and inspect *everything* in scope, without touching your code.

Print debugging is not wrong — it is handy for a quick peek, and sometimes it is all you have (an embedded target with no debugger attached). But for most bugs on the desktop, the debugger is faster and tells you more.

---

## Breakpoints: pausing the program

A **breakpoint** says "pause here." In CLion, click in the **gutter** — the narrow margin just left of the line numbers — next to the line you care about. A red dot appears.

Then run in **debug mode** instead of the normal run:

- Click the **bug icon** (next to the green run arrow), or press **Shift+F9**.

The program runs normally until it reaches the breakpoint, then **pauses** — the line is highlighted and has *not run yet*. Now you can look around.

---

## Looking at variables

While paused, the **Debug** tool window opens at the bottom. Its **Variables** pane lists every variable currently in scope and its value. You can also **hover the mouse over a variable** in the editor to see its value in a tooltip.

This is the heart of debugging: compare what a variable *actually* holds against what you *expected*. The first place those disagree is right next to your bug.

---

## Stepping through code

Once paused, you advance the program one piece at a time:

| Action | Key (CLion) | What it does |
|--------|-------------|--------------|
| **Step Over** | F8 | Run the current line, pause on the next. If the line calls a function, run the whole call without going inside. |
| **Step Into** | F7 | Like Step Over, but if the line calls *your* function, go inside and pause on its first line. |
| **Step Out** | Shift+F8 | Finish the current function and pause back in the code that called it. |
| **Resume** | F9 | Carry on until the next breakpoint (or the program ends). |
| **Stop** | Ctrl+F2 | End the debugging session. |

The everyday rhythm: **Step Over** to walk down a function watching the variables change, **Step Into** when you want to see what a call is doing, **Step Out** when you have seen enough.

> CLion's [official debugging guide](https://www.jetbrains.com/help/clion/debugging-code.html) has annotated screenshots of each of these buttons if you want to see exactly where they sit.

---

## A worked example: finding a bug

This program should add up three readings and print `60`. It prints `30`:

```cpp
#include <iostream>
#include <vector>

int sumReadings(const std::vector<int>& readings) {
    int total = 0;
    for (int r : readings) {
        total = r;
    }
    return total;
}

int main() {
    std::vector<int> readings = {10, 20, 30};
    std::cout << "sum: " << sumReadings(readings) << "\n";  // expected 60, prints 30
}
```

Here is how you find the bug without guessing:

1. Click the gutter on the `total = r;` line to set a breakpoint, and start debugging (**Shift+F9**).
2. The program pauses on that line the first time through the loop. In the **Variables** pane, `r` is `10` and `total` is `0`.
3. Press **Step Over** (F8) to go around the loop a few times, watching `total`. It becomes `10`, then `20`, then `30` — it is being **overwritten** each time, not added to. You expected `10`, then `30`, then `60`.
4. There is the bug: `total = r;` *replaces* the total. It should *accumulate*:

```cpp
total += r;   // add to the running total, don't overwrite it
```

Rebuild and it prints `60`. The debugger let you *watch* `total` misbehave the instant it happened, instead of staring at the code trying to imagine what it does.

---

## The call stack

When the program is paused, the **Frames** pane (the *call stack*) shows the chain of calls that got you here: the function you are in, the one that called it, and so on up to `main`. Click any frame to jump to that function and inspect *its* variables.

This answers "how did I even get here?" — invaluable when a function misbehaves only when it is called from one particular place.

---

## A few things to grow into

You will not need these on day one, but they are worth knowing they exist:

- **Conditional breakpoints.** Right-click a breakpoint and give it a condition like `i == 1000`. The program pauses only when the condition is true — perfect for a loop that goes wrong on one specific iteration.
- **Watches.** Pin an expression such as `readings.size()` to the Watches pane to track it as you step.
- **Evaluate Expression** (Alt+F8). Type any expression while paused and see its value, without adding code.

Breakpoints, stepping, and the Variables pane alone will solve the large majority of your bugs.

---

## Four tools for "something is wrong"

Each fits a different moment:

| When | Reach for |
|------|-----------|
| The program will not compile | [Read the compiler error](compiler_errors.md) |
| It builds but does the wrong thing | The **debugger** |
| You want to state "this can never happen" and be told the instant it does | [`assert`](Chapter6/error_handling.md#assertions-catching-bugs-not-handling-errors) |
| A quick one-off peek, or no debugger available (embedded) | A `std::cout` print |

---

## Summary

- A debugger pauses your running program so you can inspect it — far better than guessing or scattering prints.
- Set a **breakpoint** (click the gutter), run in **debug mode** (Shift+F9), and the program pauses there before the line runs.
- Read values in the **Variables** pane or by hovering; this is where you spot the bug.
- **Step Over** (F8), **Step Into** (F7), and **Step Out** (Shift+F8) walk through the code one piece at a time.
- The bug is usually at the first point where a variable's real value disagrees with what you expected it to be.
