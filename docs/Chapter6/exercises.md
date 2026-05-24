# Chapter 6 Exercises

Work through these after reading Chapter 6. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Most of these are small programs with their own `main()`. Keep them in one project with one `add_executable` line per file (see [CMake](../Chapter2/cmake_intro.md)), and pick which to run from the dropdown next to the green ▶ button. The **last exercise is a test, not a program you run from the dropdown** — build it with the Catch2 template from the [Testing](testing.md) chapter and run it with `ctest`.

---

## 1. One function, three jobs

*Practises: [Separation of Concerns](soc.md)*

Here is a function that does three things at once — it converts a raw sensor value to °C, decides a status, and prints the result:

```cpp
void report(int raw) {
    double celsius = (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    std::string status;
    if (celsius > 80.0)      status = "CRITICAL";
    else if (celsius > 50.0) status = "WARNING";
    else                     status = "OK";
    std::cout << celsius << " C [" << status << "]\n";
}
```

Pull the **computation** apart from the **reporting**. Write two *pure* functions — `double toCelsius(int raw)` and `std::string classify(double celsius)` — that compute and return, with no printing. Keep the printing in `main` (or one small reporting function that calls the two). In `main`, run it on a few raw values.

> Hint: a *pure* function only computes from its arguments and returns a result — no `std::cout`, no files. Printing is a separate concern; it belongs in `main`, not inside the calculation. Once separated, `toCelsius` and `classify` can each be tested and reused on their own.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>

    // --- Concern 1: convert a raw reading to Celsius (pure) ---
    double toCelsius(int raw) {
        return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    }

    // --- Concern 2: decide a status from a temperature (pure) ---
    std::string classify(double celsius) {
        if (celsius > 80.0) return "CRITICAL";
        if (celsius > 50.0) return "WARNING";
        return "OK";
    }

    // --- Concern 3: reporting — the only part that touches the console ---
    int main() {
        for (int raw : {200, 250, 300}) {
            double celsius = toCelsius(raw);
            std::cout << celsius << " C [" << classify(celsius) << "]\n";
        }
    }
    ```

    Output:

    ```
    47.7517 C [OK]
    72.1896 C [WARNING]
    96.6276 C [CRITICAL]
    ```

    The three jobs are now separate. `toCelsius` and `classify` are **pure** — each takes input and returns output, touching nothing else — so you can test them with a value and a check, reuse them to send the status to a file or a network instead of the console, or change the thresholds without ever going near the printing. The original `report` welded all three together: you could not check the classification without also producing console output. Each function now has one job (high **cohesion**), and the I/O lives in exactly one place.

    </div>

---

## 2. One reading, many reactions

*Practises: [Observer Pattern](observer.md)*

Build a subject that several observers watch. Write a class `LevelSensor` that holds a water level and lets observers **subscribe** with a `std::function<void(double)>` callback. A `setLevel(double)` method updates the level and then notifies every observer in turn.

In `main`, subscribe two observers — one that prints the level, and one that prints a warning *only* when the level exceeds a limit — then call `setLevel` twice. The sensor must know nothing about either observer.

> Hint: store the callbacks in a `std::vector<std::function<void(double)>>`. `subscribe` takes a callback by value and `std::move`s it into the vector; `setLevel` stores the new value, then loops calling each callback. The observers are [lambdas](../lambdas.md). Capture the limit **by value** (`[limit]`).

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <functional>
    #include <vector>
    #include <iostream>

    class LevelSensor {
    public:
        // Register a callback to run on every new reading.
        void subscribe(std::function<void(double)> observer) {
            observers_.push_back(std::move(observer));
        }

        // A fresh reading arrives: store it, then notify everyone.
        void setLevel(double metres) {
            level_ = metres;
            for (const auto& observer : observers_) {
                observer(metres);
            }
        }

        double level() const { return level_; }

    private:
        double level_ = 0.0;
        std::vector<std::function<void(double)>> observers_;
    };

    int main() {
        LevelSensor sensor;

        // A display
        sensor.subscribe([](double m) {
            std::cout << "Display: " << m << " m\n";
        });

        // A high-level warning
        double limit = 5.0;
        sensor.subscribe([limit](double m) {
            if (m > limit) {
                std::cout << "WARNING: above " << limit << " m\n";
            }
        });

        sensor.setLevel(3.0);   // display only
        sensor.setLevel(6.0);   // display + warning
    }
    ```

    Output:

    ```
    Display: 3 m
    Display: 6 m
    WARNING: above 5 m
    ```

    `LevelSensor` is the **subject**: it keeps a list of callbacks and calls them all in `setLevel`, never knowing what any of them do. Each observer subscribes a lambda. Adding a third reaction — log every level to a file, say — is just one more `subscribe` call, and the sensor itself never changes; that decoupling is what the pattern buys you. Note the warning captures `limit` **by value** (`[limit]`): if it captured by reference and `limit` were destroyed before `setLevel` ran, the stored callback would dangle — the lifetime hazard the chapter warns about.

    </div>

---

## 3. Refuse the impossible

*Practises: [Error Handling](error_handling.md)*

Model a withdrawal from an account. Write a function `double withdraw(double balance, double amount)` that:

- **throws** `std::invalid_argument` if `amount` is negative (a nonsense request);
- **throws** `std::runtime_error` if `amount` exceeds `balance` (insufficient funds);
- otherwise **returns** the new balance.

In `main`, try a valid withdrawal and each kind of bad one, printing `e.what()` whenever a withdrawal is rejected. Catch by `const` reference.

> Hint: both `std::invalid_argument` and `std::runtime_error` live in `<stdexcept>`, and both inherit from `std::exception` — so a single `catch (const std::exception& e)` handles either, and `e.what()` gives the message. A `throw` abandons the rest of the `try` block and jumps to the `catch`, so update the balance only *after* a successful call.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <stdexcept>

    double withdraw(double balance, double amount) {
        if (amount < 0.0) {
            throw std::invalid_argument("amount cannot be negative");
        }
        if (amount > balance) {
            throw std::runtime_error("insufficient funds");
        }
        return balance - amount;
    }

    int main() {
        double balance = 100.0;

        for (double amount : {30.0, -5.0, 500.0}) {
            try {
                double after = withdraw(balance, amount);
                std::cout << "Withdrew " << amount << ", balance now " << after << "\n";
                balance = after;                 // commit only on success
            } catch (const std::exception& e) {
                std::cout << "Rejected " << amount << ": " << e.what() << "\n";
            }
        }
    }
    ```

    Output:

    ```
    Withdrew 30, balance now 70
    Rejected -5: amount cannot be negative
    Rejected 500: insufficient funds
    ```

    `withdraw` **detects** the two failure modes and signals them by throwing; `main` **recovers** by catching — the detection-versus-recovery split the chapter opens with. When a `throw` fires, the rest of the `try` block is abandoned (the balance is never updated on a bad call) and control jumps straight to the `catch`; the loop then carries on to the next amount. Catching `const std::exception&` by reference handles both thrown types through their shared base, with no copy and no slicing. One judgement call worth noting: a negative or oversized amount is a genuine failure the caller must deal with, so an exception fits. If instead you were merely *looking something up* and "not found" were a perfectly normal outcome, you would reach for [`std::optional`](error_handling.md#stdoptional-when-failure-is-expected) rather than throwing.

    </div>

---

## 4. Test it with a fake

*Practises: [Testing](testing.md)*

This one is a **test**, not a program with a `main()` — build it with the Catch2 template from the [Testing](testing.md) chapter and run it with `ctest` (or run the test binary directly).

Here is a `PumpController` that should switch a pump **on** when the water level drops below a minimum. Crucially, it does not read hardware itself — it is *handed* a `LevelSensor`, so a test can supply a fake one:

```cpp
class LevelSensor {
public:
    virtual ~LevelSensor() = default;
    virtual double level() = 0;        // metres
};

class PumpController {
public:
    PumpController(LevelSensor& sensor, double minLevel)
        : sensor_(sensor), minLevel_(minLevel) {}

    bool pumpShouldRun() { return sensor_.level() < minLevel_; }

private:
    LevelSensor& sensor_;
    double minLevel_;
};
```

Write a `FakeLevelSensor` that returns a level you choose, then write Catch2 `TEST_CASE`s proving the pump **runs below** the minimum and **stays off at or above** it. Be sure to test the boundary — *exactly* at the minimum.

> Hint: `FakeLevelSensor` derives from `LevelSensor` and overrides `level()` to return a stored value. Each `TEST_CASE` makes a fake at a chosen level, injects it into a `PumpController`, and `REQUIRE`s the expected `pumpShouldRun()`. Because the test is `level < minLevel`, a level *equal* to the minimum should **not** run the pump.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <catch2/catch_test_macros.hpp>

    // --- The code under test (would normally live in its own header) ---
    class LevelSensor {
    public:
        virtual ~LevelSensor() = default;
        virtual double level() = 0;
    };

    class PumpController {
    public:
        PumpController(LevelSensor& sensor, double minLevel)
            : sensor_(sensor), minLevel_(minLevel) {}
        bool pumpShouldRun() { return sensor_.level() < minLevel_; }
    private:
        LevelSensor& sensor_;
        double minLevel_;
    };

    // --- A fake sensor: returns whatever level the test sets, no hardware ---
    class FakeLevelSensor : public LevelSensor {
    public:
        explicit FakeLevelSensor(double value) : value_(value) {}
        double level() override { return value_; }
    private:
        double value_;
    };

    TEST_CASE("pump runs when the level is below the minimum") {
        FakeLevelSensor low(1.5);
        PumpController pump(low, 2.0);
        REQUIRE(pump.pumpShouldRun());
    }

    TEST_CASE("pump stays off when the level is above the minimum") {
        FakeLevelSensor high(3.0);
        PumpController pump(high, 2.0);
        REQUIRE(!pump.pumpShouldRun());
    }

    TEST_CASE("pump stays off exactly at the minimum") {
        FakeLevelSensor atLimit(2.0);
        PumpController pump(atLimit, 2.0);
        REQUIRE(!pump.pumpShouldRun());   // 2.0 < 2.0 is false
    }
    ```

    Running the tests prints:

    ```
    All tests passed (3 assertions in 3 test cases)
    ```

    Because `PumpController` is **handed** its sensor instead of building one, the test slips in a `FakeLevelSensor` and drives the level to exactly the value each case needs — no water, no waiting, no hardware. That hand-it-in move is **dependency injection**, and the fake is the simplest kind of **test double**. The three cases test *behaviour* (does the pump run?) through the public interface, never the internals — so if you later rewrote `pumpShouldRun` completely, they would still pass as long as the behaviour held. And they probe the **boundary**, exactly at the minimum, because off-by-one mistakes (`<` versus `<=`) hide right there.

    </div>
