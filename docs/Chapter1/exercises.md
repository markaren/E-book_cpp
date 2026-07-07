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
