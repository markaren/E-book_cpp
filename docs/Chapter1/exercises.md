# Chapter 1 Exercises

Two kinds of exercise on this page.

The **warm-ups** come first: short programs to read, where you predict what they print and pick an answer in the browser. No project, no typing, about a minute each. Every one of them is built around a mistake Chapter 1 specifically warns about — much cheaper to meet here than at 1 a.m. in your own code.

Then come the **programs**, from Exercise 1 onwards: things to write yourself. **Try each one before revealing the solution** — you learn far more from an honest attempt, and the mistakes along the way, than from reading a finished program. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

---

## Warm-ups: predict the output

Work out what each program prints **before** you pick an option. Answering locks the question and reveals the explanation, so a guess costs you the exercise. If you are unsure, trace the program by hand, line by line, the way a debugger would — that habit is the whole point.

### W1. Divide and print

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int a = 7;
    int b = 8;
    int c = 10;

    double average = (a + b + c) / 3;

    std::cout << average << "\n";
}
```

````quiz
What does this print?
- `8.33333`
- =`8`
- `8.3`
- It does not compile — you cannot put an `int` result in a `double`
:::
**`8`.** The `double` on the left changes nothing about the division on the right.

`a + b + c` is `25`, an `int`. `3` is also an `int`. So `25 / 3` is **integer division**: it computes `8` and throws the remainder away, right there, before anything is assigned. Only then is that `8` converted to `double` and stored in `average`.

The fix is to make one side a `double` so the division itself keeps the fraction: `(a + b + c) / 3.0`. See [Operators and Expressions](operators_expressions.md).
````

### W2. A function that changes nothing

<!-- no-ce -->
```cpp
#include <iostream>

void addTen(int value) {
    value += 10;
}

int main() {
    int count = 5;
    addTen(count);
    std::cout << count << "\n";
}
```

````quiz
What does this print?
- `15`
- =`5`
- `10`
- Nothing — `addTen` returns `void`, so the program has no output
:::
**`5`.** `count` was never touched.

A parameter is a **copy** of the argument. `addTen` received its own `int` holding `5`, added `10` to *that*, and threw it away when it returned. The `count` in `main` is a different variable and never changed.

This is the single most common surprise for beginners, which is why [Functions](functions.md#parameters-are-copies) spends a section on it. To let a function change the caller's variable you pass a **reference** — the tool for that arrives in [Values, References & Pointers](../Chapter4/types_refs_ptrs.md). Until then: if a function needs to hand something back, `return` it.
````

### W3. Two words in, one word out

The user types `Ada Lovelace` and presses Enter.

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

int main() {
    std::string name;

    std::cout << "Name: ";
    std::cin >> name;

    std::cout << "Hello, " << name << "!\n";
}
```

````quiz
What does this print after the prompt?
- `Hello, Ada Lovelace!`
- =`Hello, Ada!`
- `Hello, !`
- It waits forever for more input
:::
**`Hello, Ada!`** — `Lovelace` is left behind.

`>>` reads **one whitespace-separated word**. It stops at the space after `Ada`, so `name` holds just `Ada`; the rest of the line stays in the input buffer, unread.

To read a whole line, spaces included, use `std::getline(std::cin, name)` instead. See [Strings and Vectors](strings_and_vectors.md#reading-text-from-the-user) — and note the warning there about what happens when you *mix* the two on one stream.
````

### W4. A switch without breaks

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int gear = 2;

    switch (gear) {
        case 1: std::cout << "First\n";
        case 2: std::cout << "Second\n";
        case 3: std::cout << "Third\n";
        default: std::cout << "Unknown\n";
    }
}
```

````quiz
What does this print?
- `Second`
- `Second` then `Unknown`
- =`Second`, then `Third`, then `Unknown`
- It does not compile — every `case` needs a `break`
:::
**All three: `Second`, `Third`, `Unknown`.**

A `case` label is an *entry point*, not a self-contained block. Execution jumps to `case 2:` and then keeps running straight through every label below it until it hits a `break` or the closing brace. There is no `break` anywhere here, so it falls all the way through — including into `default`.

It compiles without complaint, because deliberate fall-through is occasionally useful. That is exactly what makes a forgotten `break` such a good hiding place for a bug. See [Control Statements](control_statements.md#switch).
````

### W5. The right branches in the wrong order

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int celsius = -5;

    if (celsius < 25) {
        std::cout << "Comfortable\n";
    } else if (celsius < 15) {
        std::cout << "Cold\n";
    } else if (celsius < 0) {
        std::cout << "Freezing\n";
    } else {
        std::cout << "Hot\n";
    }
}
```

````quiz
Minus five degrees. What does this print?
- `Freezing`
- =`Comfortable`
- `Cold`
- Nothing — no branch matches
:::
**`Comfortable`**, at −5 °C.

Only the **first** matching branch runs; the rest are skipped no matter how much better they fit. `-5 < 25` is true, so the chain stops there and never considers `Cold` or `Freezing` at all. Those two branches are unreachable for *any* value: anything below `15` or `0` is also below `25`.

Nothing here is a syntax error, so the compiler says nothing. An `else if` chain over a range has to be ordered from one end to the other — coldest first, as [Exercise 9](#9-temperature-classifier) below does it. See [Control Statements](control_statements.md#if-and-else).
````

### W6. Doubling that does not stick

<!-- no-ce -->
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings = {1, 2, 3};

    for (int value : readings) {
        value *= 2;
    }

    for (int value : readings) {
        std::cout << value << " ";
    }
    std::cout << "\n";
}
```

````quiz
What does this print?
- `2 4 6`
- =`1 2 3`
- `1 2 3 2 4 6`
- `6 12 18`
:::
**`1 2 3`.** The vector is untouched.

`for (int value : readings)` hands you a fresh **copy** of each element. `value *= 2` doubles the copy, and the copy is discarded at the end of that iteration — the same pass-by-value rule as [W2](#w2-a-function-that-changes-nothing), in loop clothing.

To modify the elements in place, take a reference so `value` *is* the element rather than a copy of it:

```cpp
for (int& value : readings) {
    value *= 2;
}
```

That one `&` is the whole difference. See [Control Statements](control_statements.md#range-based-for).
````

Once you have answered a question, paste the program into [Compiler Explorer](https://godbolt.org/) and run it — seeing the output confirm (or contradict) your reasoning is what makes it stick.

---

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

## 3. Sensor readings

*Practises: [Strings and Vectors](strings_and_vectors.md), [Control Statements](control_statements.md)*

Store five sensor readings — `42, 17, 99, 8, 56` — in a `std::vector<int>`. Print how many there are, their average (as a decimal), and the largest.

> Hint: loop over the vector to add up the values and track the biggest; `readings.size()` is the count.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> readings = {42, 17, 99, 8, 56};

        int sum = 0;
        int largest = readings[0];
        for (int r : readings) {
            sum += r;
            if (r > largest) {
                largest = r;
            }
        }

        double average = static_cast<double>(sum) / readings.size();

        std::cout << "Count:   " << readings.size() << "\n";
        std::cout << "Average: " << average << "\n";
        std::cout << "Largest: " << largest << "\n";
    }
    ```

    A range-based `for` visits every element: we add each to `sum` and keep the biggest seen so far. `static_cast<double>` keeps the division decimal (the integer-division rule again), and `readings.size()` gives the element count.

    </div>

---

## 4. Even or odd

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

## 5. Squares

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

## 6. Traffic light

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

---

## 7. Keep asking

*Practises: [Control Statements](control_statements.md)*

Ask the user for a positive number, over and over, until they actually give you one. Then print it. Use a `do-while` loop, so you ask at least once.

> Hint: this is the `do-while` pattern from the chapter — read inside the loop, and repeat while the value is not yet positive.

Run it — you should see:

```
Enter a positive number: -4
Enter a positive number: 0
Enter a positive number: 12
Thanks — you entered 12
```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    int main() {
        int number = 0;

        do {
            std::cout << "Enter a positive number: ";
            std::cin >> number;
        } while (number <= 0);

        std::cout << "Thanks — you entered " << number << "\n";
    }
    ```

    A `do-while` runs its body *before* testing the condition, so the prompt always appears at least once. The loop repeats as long as `number <= 0`, so it only lets you out once the value is genuinely positive — exactly what "keep asking until it is valid" needs.

    </div>

---

## 8. Greet by full name

*Practises: [Strings and Vectors](strings_and_vectors.md)*

Ask for the user's full name (first *and* last, with the space), greet them, and report how many characters the name has. Because the name contains a space, you need `std::getline`, not `std::cin >>`.

> Hint: `std::getline(std::cin, name)` reads the whole line; `name.length()` counts its characters.

Run it — you should see:

```
Enter your full name: Ada Lovelace
Hello, Ada Lovelace
Your name has 12 characters.
```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>

    int main() {
        std::string name;

        std::cout << "Enter your full name: ";
        std::getline(std::cin, name);

        std::cout << "Hello, " << name << "\n";
        std::cout << "Your name has " << name.length() << " characters.\n";
    }
    ```

    `std::getline` reads the entire line, spaces included, so `Ada Lovelace` arrives whole — `std::cin >> name` would have stopped at the space and kept only `Ada`. The count of `12` includes the space, because it is one of the characters in the string.

    </div>

---

## 9. Temperature classifier

*Practises: [Control Statements](control_statements.md)*

Read a temperature (a whole number of degrees Celsius) and print a description using an `if` / `else if` / `else` chain: below `0` is `Freezing`, `0` to `14` is `Cold`, `15` to `24` is `Comfortable`, and `25` or above is `Hot`.

> Hint: test the coldest case first and work upward, so each `else if` only has to check its upper bound.

Run it — you should see:

```
Enter the temperature in Celsius: 18
Comfortable
```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    int main() {
        int celsius = 0;

        std::cout << "Enter the temperature in Celsius: ";
        std::cin >> celsius;

        if (celsius < 0) {
            std::cout << "Freezing\n";
        } else if (celsius < 15) {
            std::cout << "Cold\n";
        } else if (celsius < 25) {
            std::cout << "Comfortable\n";
        } else {
            std::cout << "Hot\n";
        }
    }
    ```

    Only the first matching branch runs, so ordering the tests from coldest upward lets each `else if` assume everything below it was already ruled out: by the time `celsius < 15` is checked, we know it is not below `0`, so that branch means `0` to `14`. The final `else` catches everything left — `25` and above.

    </div>
