# Chapter 1 Exercises

Work through these after reading Chapter 1. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt, and the mistakes along the way, than from reading a finished program. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

## Where to put your code

Each exercise is its own small program with its own `main()`, and a CLion project runs one `main()` at a time. You have two options:

**Simplest** — keep one project open and replace the contents of `main.cpp` for each exercise. Run it, then paste in the next. (You lose the previous attempt, which is fine for quick practice.)

**Keeps every exercise (recommended)** — give each exercise its own file in a single project (`ex1.cpp`, `ex2.cpp`, …) and add one line per file to `CMakeLists.txt`:

```cmake
add_executable(ex1 ex1.cpp)
add_executable(ex2 ex2.cpp)
```

Then choose which program to run from the run-configuration dropdown next to the green ▶ button. You do not need to understand `CMakeLists.txt` yet — [CMake](../Chapter2/cmake_intro.md) explains it in Chapter 2; for now, just copy the pattern.

---

## 1. Introduce yourself

*Practises: [Basic Structure](basic_structure.md), [Variables and Basic Types](variables.md)*

Declare a `std::string` for your name and an `int` for your age (just like the chapter's `int age = 25`). Print one line:

```
My name is Ada and I am 36 years old.
```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>

    int main() {
        std::string name = "Ada";
        int age = 36;

        std::cout << "My name is " << name << " and I am " << age << " years old.\n";
    }
    ```

    Each variable gets the right type and is initialised as it is declared; `<<` chains the pieces into one line.

    </div>

---

## 2. Average score

*Practises: [Operators and Expressions](operators_expressions.md)*

You have three test scores: `7`, `8`, and `10`. Print their average. Make sure it comes out as a decimal — `8.33…`, not a truncated `8`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    int main() {
        int a = 7;
        int b = 8;
        int c = 10;

        double average = (a + b + c) / 3.0;   // 3.0 is a double, so the decimals are kept

        std::cout << "Average: " << average << "\n";
    }
    ```

    Divide by `3` (an `int`) and C++ does integer division — it throws the fraction away and you get `8`. Writing `3.0` makes one side a `double`, so the decimals survive. That is the chapter's `10 / 3` rule in action.

    </div>

---

## 3. Even or odd

*Practises: [Control Statements](control_statements.md)*

Use a `for` loop to print the numbers 1 to 10, labelling each one `even` or `odd`.

> Hint: a number is even when `n % 2 == 0`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    int main() {
        for (int i = 1; i <= 10; ++i) {
            if (i % 2 == 0) {
                std::cout << i << " even\n";
            } else {
                std::cout << i << " odd\n";
            }
        }
    }
    ```

    A counter-based `for` loop like the one in the chapter, with an `if`/`else` inside it deciding what to print.

    </div>

---

## 4. Squares

*Practises: [Functions](functions.md)*

Write a function `int square(int n)` that returns `n * n` (you saw this exact function in the chapter). Then use a `for` loop to print the squares of 1 through 5.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    int square(int n) {
        return n * n;
    }

    int main() {
        for (int i = 1; i <= 5; ++i) {
            std::cout << i << " squared is " << square(i) << "\n";
        }
    }
    ```

    A small function with one clear job, called from a loop. Defining `square` once and reusing it beats writing `i * i` everywhere.

    </div>

---

## 5. Traffic light

*Practises: [Enumerations](enums.md)*

Define an `enum class TrafficLight` with `Red`, `Amber`, and `Green`. Write a function that prints the action for each — `Stop`, `Get ready`, `Go` — using a `switch`, and call it for all three.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    enum class TrafficLight {
        Red,
        Amber,
        Green
    };

    void act(TrafficLight light) {
        switch (light) {
            case TrafficLight::Red:   std::cout << "Stop\n";      break;
            case TrafficLight::Amber: std::cout << "Get ready\n"; break;
            case TrafficLight::Green: std::cout << "Go\n";        break;
        }
    }

    int main() {
        act(TrafficLight::Red);
        act(TrafficLight::Amber);
        act(TrafficLight::Green);
    }
    ```

    A fixed set of named values handled by a `switch`. With no `default`, the compiler warns you if you add a colour later and forget it here.

    </div>
