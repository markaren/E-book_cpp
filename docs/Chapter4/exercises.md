# Chapter 4 Exercises

Work through these after reading Chapter 4. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Each exercise is a small program with its own `main()`. Keep them in one project with one `add_executable` line per file (see [CMake](../Chapter2/cmake_intro.md)), and pick which to run from the dropdown next to the green ▶ button.

---

## 1. A water tank that cannot overflow

*Practises: [Classes](classes.md)*

Write a class `WaterTank`. Its **capacity** is fixed when the tank is created, and it starts empty. Give it three operations:

- `fill(amount)` adds water, but the level can never exceed the capacity;
- `drain(amount)` removes water, but the level can never drop below zero;
- `level()` reports the current level (and does not modify the tank).

Keep the data **private**. Then in `main`, make a 100-litre tank, `fill(60)`, `fill(60)` again (it should clamp to 100, not 120), `drain(30)`, and print the level.

> Hint: the capacity and level are the tank's private state. Use the constructor's member-initialiser list to set the capacity, and mark `level()` as `const`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    class WaterTank {
    public:
        explicit WaterTank(double capacity) : capacity_(capacity) {}

        void fill(double amount) {
            level_ += amount;
            if (level_ > capacity_) {
                level_ = capacity_;        // never overflow
            }
        }

        void drain(double amount) {
            level_ -= amount;
            if (level_ < 0.0) {
                level_ = 0.0;              // never go negative
            }
        }

        double level() const { return level_; }

    private:
        double capacity_;
        double level_ = 0.0;
    };

    int main() {
        WaterTank tank(100.0);
        tank.fill(60.0);
        tank.fill(60.0);     // would reach 120, clamped to 100
        tank.drain(30.0);
        std::cout << "Level: " << tank.level() << "\n";   // 70
    }
    ```

    The two invariants — "never above capacity", "never below zero" — live inside `fill` and `drain`, the only functions that can touch `level_`. Because the data is private, no outside code can break those rules. `level()` is `const` because reporting the level does not change the tank. The single-argument constructor is `explicit` so an `int` never silently turns into a `WaterTank`.

    </div>

---

## 2. By value, by reference, by const reference

*Practises: [Values, References & Pointers](types_refs_ptrs.md)*

Write three functions that each take a `std::vector<double>`:

- `tryToScale(data, factor)` takes the vector **by value** and multiplies every element by `factor`;
- `scale(data, factor)` does the same but takes the vector **by reference** (`&`);
- `sum(data)` takes the vector **by `const` reference** and returns the total.

In `main`, start with `{1.0, 2.0, 3.0}`, call `tryToScale(…, 10)` and print the sum, then call `scale(…, 10)` and print the sum. Explain to yourself why only one of them changed the result.

> Hint: a by-value parameter is a *copy* — changes to it never reach the caller. A `T&` parameter *is* the caller's object. A `const T&` parameter lets you read a big object without copying it.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>

    // by value: works on a copy, the caller's vector is untouched
    void tryToScale(std::vector<double> data, double factor) {
        for (double& x : data) {
            x *= factor;
        }
    }

    // by reference: works on the caller's own vector
    void scale(std::vector<double>& data, double factor) {
        for (double& x : data) {
            x *= factor;
        }
    }

    // by const reference: reads the caller's vector without copying it
    double sum(const std::vector<double>& data) {
        double total = 0.0;
        for (double x : data) {
            total += x;
        }
        return total;
    }

    int main() {
        std::vector<double> readings = {1.0, 2.0, 3.0};

        tryToScale(readings, 10.0);
        std::cout << "After tryToScale (by value): sum = " << sum(readings) << "\n";  // 6

        scale(readings, 10.0);
        std::cout << "After scale (by reference):  sum = " << sum(readings) << "\n";  // 60
    }
    ```

    `tryToScale` receives a *copy*; it scales that copy and throws it away when it returns, so the caller's `readings` is unchanged and the sum is still `6`. `scale` receives a reference — an alias for the caller's vector — so its changes stick, and the sum becomes `60`. `sum` only reads, so it takes `const std::vector<double>&`: no copy of the vector is made, and the `const` guarantees the function cannot modify it.

    </div>

---

## 3. A destructor you can watch

*Practises: [RAII](raii.md)*

Write a class `Task` that prints `Begin <name>` from its **constructor** and `End <name>` from its **destructor**. In `main`, construct a `Task` called `outer`; then, inside an inner `{ }` block, construct one called `inner` and print `working`. After the block, print `back in main`.

**Predict the order of all the lines before you run it**, then check.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>

    class Task {
    public:
        explicit Task(std::string name) : name_(name) {
            std::cout << "Begin " << name_ << "\n";
        }
        ~Task() {
            std::cout << "End " << name_ << "\n";
        }

    private:
        std::string name_;
    };

    int main() {
        Task outer("outer");
        {
            Task inner("inner");
            std::cout << "working\n";
        }   // inner goes out of scope here — its destructor runs
        std::cout << "back in main\n";
    }
    ```

    The output is:

    ```
    Begin outer
    Begin inner
    working
    End inner
    back in main
    End outer
    ```

    `inner` is destroyed at the closing `}` of the inner block, *before* `back in main` prints — you never wrote a call to destroy it. `outer` is destroyed last, at the end of `main`. Objects are destroyed in reverse order of construction, each exactly when its scope ends. That automatic, guaranteed cleanup is the whole point of RAII.

    </div>

---

## 4. Teach a stream to print your type

*Practises: [IO & Streams](io_streams.md)*

Define a `struct Point` with `int` members `x` and `y`. Overload `operator<<` so that `std::cout << p` prints a point as `(x, y)`. Then print two points, for example `(3, 4)` and `(-1, 7)`.

> Hint: the signature is `std::ostream& operator<<(std::ostream& os, const Point& p)`. Write into `os`, then `return os;` so the `<<` calls can chain.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    struct Point {        // a struct is a class with public members by default
        int x;
        int y;
    };

    std::ostream& operator<<(std::ostream& os, const Point& p) {
        os << "(" << p.x << ", " << p.y << ")";
        return os;
    }

    int main() {
        Point a{3, 4};
        Point b{-1, 7};
        std::cout << "a = " << a << "\n";   // a = (3, 4)
        std::cout << "b = " << b << "\n";   // b = (-1, 7)
    }
    ```

    The overload takes the stream by reference as `std::ostream&` — the base type of `std::cout`, `std::ofstream`, and the rest — so the same function prints to the console or to a file. It returns that stream so the next `<<` in the chain has something to write to; that is why `std::cout << "a = " << a << "\n"` works left to right. Taking `const Point&` avoids copying and promises not to change the point.

    </div>
