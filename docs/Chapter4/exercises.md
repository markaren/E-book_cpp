# Chapter 4 Exercises

Two kinds of exercise on this page.

The **warm-ups** come first: short programs to read, where you predict what happens and pick an answer in the browser. No project, no typing. Each one is built on a rule this chapter states — `const`-correctness, when a destructor runs, what `static` means, who owns what — where the consequence only becomes obvious once you have been caught by it.

Then come the **programs**, from Exercise 1 onwards. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Each exercise is a small program with its own `main()`. Keep them in one project with one `add_executable` line per file (see [CMake](../Chapter2/cmake_intro.md)), and pick which to run from the dropdown next to the green ▶ button.

---

## Warm-ups: predict the output

Decide what each program does **before** you answer. Answering locks the question and reveals the explanation.

### W1. A const object and a getter

<!-- no-ce -->
```cpp
#include <iostream>

class Sensor {
public:
    double read() { return value_; }
    void set(double v) { value_ = v; }

private:
    double value_ = 21.5;
};

int main() {
    const Sensor s;
    std::cout << s.read() << "\n";
}
```

````quiz
What happens?
- It prints `21.5`
- =It does not compile: `read()` is not `const`
- It prints `0`
- It compiles, but prints a garbage value
:::
**It does not compile.** GCC and MSVC both reject the call, MSVC with:

```
error C2662: 'double Sensor::read(void)': cannot convert 'this'
pointer from 'const Sensor' to 'Sensor &'
```

`s` is a `const Sensor`, and **a `const` object can call only member functions marked `const`**. `read()` does not modify anything, but it never said so, and the compiler goes by the declaration, not by what the body happens to do.

The fix is one word: `double read() const { return value_; }`. This is why [Classes](classes.md#members-data-and-functions) tells you to mark every observer `const` — forget it on a getter and no `const` object, and no `const&` parameter, can call it. That is the whole practical point of const-correctness.
````

### W2. When does the destructor run?

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

class Trace {
public:
    explicit Trace(std::string name) : name_(std::move(name)) {
        std::cout << "open " << name_ << "\n";
    }
    ~Trace() { std::cout << "close " << name_ << "\n"; }

private:
    std::string name_;
};

int main() {
    Trace a("A");
    {
        Trace b("B");
        std::cout << "inner\n";
    }
    std::cout << "outer\n";
}
```

````quiz
In what order do the six lines appear?
- `open A`, `open B`, `inner`, `outer`, `close A`, `close B`
- =`open A`, `open B`, `inner`, `close B`, `outer`, `close A`
- `open A`, `open B`, `inner`, `outer`, `close B`, `close A`
- `open A`, `close A`, `open B`, `close B`, `inner`, `outer`
:::
**`open A`, `open B`, `inner`, `close B`, `outer`, `close A`.**

`b` is destroyed at the closing brace of the inner block — *before* `outer` prints, not at the end of `main`. `a` lives until `main` itself ends, so `close A` comes last.

Two rules do all the work here. An object is destroyed **the moment its enclosing scope ends**, and objects in the same scope are destroyed in **reverse order of construction** (last built, first destroyed). That is what makes [RAII](raii.md) trustworthy: cleanup is pinned to a brace you can see, not to something you have to remember to call.
````

### W3. One counter, three objects

<!-- no-ce -->
```cpp
#include <iostream>

class Motor {
public:
    Motor() : id_(++count_) {}
    int id() const { return id_; }
    static int count() { return count_; }

private:
    int id_;
    static inline int count_ = 0;
};

int main() {
    Motor a;
    Motor b;
    Motor c;

    std::cout << a.id() << " " << c.id() << " " << Motor::count() << "\n";
}
```

````quiz
What does this print?
- `1 1 1`
- `1 3 1`
- =`1 3 3`
- `3 3 3`
:::
**`1 3 3`.**

`id_` is an ordinary data member, so every `Motor` has its own: `a` got `1`, `c` got `3`, and those never change. `count_` is **`static`** — there is exactly one, shared by the whole class, and each constructor incremented that same one. After three motors it holds `3`.

`Motor::count()` is called on the *class*, not on an object, which is why there is no `a.` or `c.` in front of it. See [Static members](classes.md#static-members).
````

### W4. A reference to something that is gone

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

const std::string& label() {
    std::string text = "sensor-1";
    return text;
}

int main() {
    std::cout << label() << "\n";
}
```

````quiz
This compiles. What is wrong with it?
- Nothing — returning `const&` avoids a copy, which is the recommended style
- It leaks memory, because `text` is never freed
- =`text` is destroyed when `label` returns, so the caller is handed a reference to memory that no longer exists
- It does not compile, because you cannot return a local by reference
:::
**The reference dangles.** `text` is a local: it is destroyed the instant `label` returns, so the reference handed back refers to memory that is no longer alive. Reading it is **undefined behaviour** — it might print `sensor-1`, print rubbish, or crash, and it may well behave differently in a Release build than in Debug.

It compiles, though the compiler does try to tell you. MSVC warns:

```
warning C4172: returning address of local variable or temporary : text
```

which is exactly the kind of warning [the CMake chapter](../Chapter2/cmake_intro.md#turn-on-compiler-warnings) turns on for you, and exactly the kind people learn to scroll past.

Returning `const&` really is the right way to hand back something that **outlives the call** — a data member, say. It is wrong for a local. Here you return by value: `std::string label()`. See [The big lifetime trap](types_refs_ptrs.md#the-big-lifetime-trap).
````

### W5. Writing to the same file twice

<!-- no-ce -->
```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    {
        std::ofstream out("log.txt");
        out << "first\n";
    }
    {
        std::ofstream out("log.txt");
        out << "second\n";
    }

    std::ifstream in("log.txt");
    std::string line;
    while (std::getline(in, line)) {
        std::cout << line << "\n";
    }
}
```

````quiz
What does the program print at the end?
- `first` then `second`
- =`second`
- `first`
- Nothing — the second `ofstream` fails because the file is already open
:::
**Just `second`.** `first` is gone.

Opening an `std::ofstream` **truncates** the file by default: it is emptied the moment it is opened, before you write a thing. The second block therefore starts from an empty `log.txt` and the first line is lost.

To add to a file instead of replacing it, open it in append mode: `std::ofstream out("log.txt", std::ios::app);` See [Writing a file](io_streams.md#writing-a-file).

Note that the two blocks are what make this safe to reason about: each `ofstream` is closed at its closing brace, so the file is flushed and released before the next one opens it — [RAII](raii.md) again.
````

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

    The overload takes the stream by reference as `std::ostream&` — the type of `std::cout` and the common type all output streams share (`std::ofstream` and the rest) — so the same function prints to the console or to a file. It returns that stream so the next `<<` in the chain has something to write to; that is why `std::cout << "a = " << a << "\n"` works left to right. Taking `const Point&` avoids copying and promises not to change the point.

    </div>

---

## 5. Three ways to build a rectangle

*Practises: [Classes](classes.md)*

Write a class `Rectangle` with a `width` and a `height`. Give it **three** constructors and one query:

- a default constructor, making a `0 × 0` rectangle;
- a single-argument constructor `Rectangle(side)` that makes a **square**;
- a two-argument constructor `Rectangle(width, height)`;
- `area() const`, returning `width × height`.

Mark the single-argument constructor `explicit`. In `main`, build one of each, print their areas, and work out why `Rectangle r = 4.0;` would not compile.

> Hint: give the members default values (`= 0.0`) so the default constructor can be `= default`. The compiler picks the right constructor from the number and type of arguments you pass.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    class Rectangle {
    public:
        Rectangle() = default;                                            // 0 x 0
        explicit Rectangle(double side) : width_(side), height_(side) {}  // a square
        Rectangle(double width, double height) : width_(width), height_(height) {}

        double area() const { return width_ * height_; }

    private:
        double width_  = 0.0;
        double height_ = 0.0;
    };

    int main() {
        Rectangle empty;            // 0 x 0
        Rectangle square(4.0);      // 4 x 4
        Rectangle rect(3.0, 5.0);   // 3 x 5
        // Rectangle bad = 4.0;      // compile error: the 1-arg constructor is explicit

        std::cout << empty.area()  << "\n";   // 0
        std::cout << square.area() << "\n";   // 16
        std::cout << rect.area()   << "\n";   // 15
    }
    ```

    The three constructors share the name `Rectangle`; the compiler chooses one from the arguments you pass. `Rectangle() = default` asks for the do-nothing default constructor — the `0.0` member defaults stand. The single-argument constructor builds a square and is `explicit`, so `Rectangle bad = 4.0;` is rejected: you must write `Rectangle square(4.0)`, which states the intent. `area()` is `const` because measuring a rectangle does not change it.

    </div>

---

## 6. The Rule of Zero in action

*Practises: [Classes](classes.md)*

Write a class `Recording` that stores a `std::string name` and a `std::vector<double> samples`. Give it `add(sample)`, `name() const`, and `count() const`. Write **no** destructor, copy constructor, or assignment operator.

In `main`, make a recording and add two samples. Then make a **copy** of it, add a third sample to the *copy only*, and print both counts. They should differ — proving the copy is independent, even though you wrote no copying code.

> Hint: just declare the two members and the three small functions. Do *not* write `~Recording`, a copy constructor, or `operator=` — that is the whole point.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>
    #include <vector>

    class Recording {
    public:
        explicit Recording(const std::string& name) : name_(name) {}

        void add(double sample) { samples_.push_back(sample); }

        const std::string& name() const { return name_; }
        int count() const { return static_cast<int>(samples_.size()); }

    private:
        std::string         name_;
        std::vector<double> samples_;
    };

    int main() {
        Recording original("run-1");
        original.add(1.0);
        original.add(2.0);

        Recording copy = original;   // a copy — yet you wrote no copy constructor
        copy.add(3.0);               // only the copy gets a third sample

        std::cout << original.name() << ": " << original.count() << "\n";  // run-1: 2
        std::cout << copy.name()     << ": " << copy.count()     << "\n";  // run-1: 3
    }
    ```

    You wrote no special member functions, yet `Recording copy = original;` produces a genuine, independent copy: the third sample lands only in `copy`, and `original` still reports two. It works because the *members* do the copying — `std::string` and `std::vector` each know how to copy themselves, so the compiler-generated copy of `Recording` simply copies each member. That is the **Rule of Zero**: when every member manages its own resources, the compiler's defaults are correct and you write none of the special members yourself.

    </div>

---

## 7. const-correctness

*Practises: [Classes](classes.md)*

Write a class `Thermometer` holding a reading in °C, starting at `20.0`. Give it `celsius()` (reports the reading) and `calibrate(offset)` (shifts the reading by `offset`). Then write a free function `void report(const Thermometer& t)` that prints `t.celsius()`.

In `main`, build a thermometer, `report` it, `calibrate(-1.5)`, and `report` it again. The question to answer: which method *must* be `const`, and why does `report`'s `const&` parameter force it?

> Hint: through a `const` reference you may call **only** `const` member functions. `report` takes `const Thermometer&`, so every method it calls must be `const`. Which of `celsius()` and `calibrate()` only observes?

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>

    class Thermometer {
    public:
        double celsius() const { return celsius_; }               // observer → const
        void   calibrate(double offset) { celsius_ += offset; }   // mutator → not const

    private:
        double celsius_ = 20.0;
    };

    void report(const Thermometer& t) {      // const& → may call only const methods
        std::cout << t.celsius() << " C\n";  // OK: celsius() is const
        // t.calibrate(1.0);                  // would NOT compile: calibrate is not const
    }

    int main() {
        Thermometer t;
        report(t);            // 20 C
        t.calibrate(-1.5);
        report(t);            // 18.5 C
    }
    ```

    `report` takes its argument by `const Thermometer&` — the usual way to pass an object you only want to read, with no copy. But a `const` reference can call only `const` member functions, so `celsius()` **must** be marked `const` (it merely observes) for `report` to compile. `calibrate` changes the reading, so it is deliberately *not* `const` — and the commented-out call inside `report` would be a compile error, which is exactly the safety net const-correctness gives you. The rule of thumb: mark every observer `const`, and your class becomes usable through a `const` reference.

    </div>

---

## 8. A pointer that may point to nothing

*Practises: [Values, References & Pointers](types_refs_ptrs.md)*

Write a function `const int* largest(const std::vector<int>& v)` that returns a **pointer** to the biggest element of `v` — or `nullptr` if `v` is empty. In `main`, call it on `{3, 9, 2, 7}` and, only if the returned pointer is not null, print the value it points to. Then call it on an **empty** vector and confirm you get `nullptr` and print nothing dangerous.

The point of the exercise: a pointer can legitimately mean "no result", and you must **check for `nullptr` before dereferencing**.

> Hint: take the address of an element with `&`. Start "biggest so far" as `&v.at(0)` (but only after checking the vector is not empty), then walk the rest, reassigning the pointer when you find a larger element. Read the pointed-to value with `*p`, and its members — if it pointed to a class — with `p->` ([pointers to objects](types_refs_ptrs.md#pointers-to-objects)).

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>

    // returns a pointer to the largest element, or nullptr if v is empty
    const int* largest(const std::vector<int>& v) {
        if (v.empty()) {
            return nullptr;             // no element to point at
        }
        const int* biggest = &v.at(0);
        for (const int& x : v) {
            if (x > *biggest) {
                biggest = &x;           // point at the new champion
            }
        }
        return biggest;
    }

    int main() {
        std::vector<int> readings = {3, 9, 2, 7};
        const int* p = largest(readings);
        if (p != nullptr) {                       // check before dereferencing
            std::cout << "largest = " << *p << "\n";   // largest = 9
        }

        std::vector<int> empty;
        const int* q = largest(empty);
        if (q == nullptr) {
            std::cout << "empty: no largest\n";   // empty: no largest
        }
    }
    ```

    A pointer can hold `nullptr` to mean "there is nothing here" — something a reference can never do. So `largest` returns a pointer: a real element's address when there is one, `nullptr` when the vector is empty. The caller **must** check `p != nullptr` before writing `*p`; dereferencing a null pointer is undefined behaviour. Note the pointer is `const int*` — it points at data owned by the caller's vector, and returning it is safe *because that vector outlives the call*. (Had `largest` returned the address of a local variable instead, the pointer would dangle the moment the function returned — the trap from [the pointers page](types_refs_ptrs.md#the-big-lifetime-trap).)

    </div>
