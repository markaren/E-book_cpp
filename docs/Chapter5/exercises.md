# Chapter 5 Exercises

Two kinds of exercise on this page.

The **warm-ups** come first: short programs to read, where you predict what happens and pick an answer in the browser. No project, no typing. This chapter is where C++ starts punishing imprecision — a copy where you meant a reference, a base class where you meant a derived one — and these are the mistakes that produce *plausible* wrong output rather than a crash.

Then come the **programs**, from Exercise 1 onwards. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Each exercise is a small program with its own `main()`. Keep them in one project with one `add_executable` line per file (see [CMake](../Chapter2/cmake_intro.md)), and pick which to run from the dropdown next to the green ▶ button.

---

## Warm-ups: predict the output

Decide what each program does **before** you answer. Answering locks the question and reveals the explanation.

### W1. A value and a reference

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

struct Base {
    virtual ~Base() = default;
    virtual std::string kind() const { return "base"; }
};

struct Derived : Base {
    std::string kind() const override { return "derived"; }
};

int main() {
    Derived d;

    Base  b = d;   // a copy
    Base& r = d;   // a reference

    std::cout << b.kind() << " " << r.kind() << "\n";
}
```

````quiz
What does this print?
- `derived derived`
- =`base derived`
- `derived base`
- `base base`
:::
**`base derived`.** One line, both halves of the lesson.

`Base b = d;` copies **only the `Base` part** of `d` — a `Base` variable is exactly big enough for a `Base`, so the `Derived` part is dropped on the floor. That is **[object slicing](polymorphism.md#object-slicing)**, and what survives is a genuine `Base`, so `b.kind()` returns `"base"`. No warning: it is a perfectly legal copy.

`Base& r = d;` does not copy anything. `r` is another name for `d`, which is still a whole `Derived`, so the virtual call dispatches to `Derived::kind()`.

That is the rule in one line: work with polymorphic types through **references or pointers, never by value**. The moment you assign to a base *value*, the derived-ness is gone — silently, and the program keeps running with plausible-looking output.
````

### W2. A base class without a virtual destructor

<!-- no-ce -->
```cpp
#include <iostream>
#include <memory>

class Logger {
public:
    ~Logger() { std::cout << "~Logger\n"; }
    virtual void log() = 0;
};

class FileLogger : public Logger {
public:
    ~FileLogger() { std::cout << "~FileLogger\n"; }
    void log() override {}
};

int main() {
    std::unique_ptr<Logger> p = std::make_unique<FileLogger>();
    p->log();
}
```

````quiz
What is wrong with this program?
- Nothing — `unique_ptr` always destroys the object it holds correctly
- `Logger` cannot be abstract and have a destructor at the same time
- =`~Logger` is not `virtual`, so destroying a `FileLogger` through a `Logger` pointer is undefined behaviour
- `make_unique` cannot build a `FileLogger` when the variable is a `unique_ptr<Logger>`
:::
**The destructor is not `virtual`.**

The `unique_ptr` holds a `Logger*`. When it goes out of scope it deletes through *that* pointer, and because `~Logger` is not `virtual` the call is resolved statically: only `~Logger` runs. `~FileLogger` never does — so anything the derived class owned (an open file, in a real logger) is never released. Formally it is **undefined behaviour**, not merely a leak.

The compiler does warn here — MSVC with:

```
warning C5205: delete of an abstract class 'Logger' that has a
non-virtual destructor results in undefined behavior
```

The fix is one word: `virtual ~Logger() = default;`. The rule is worth memorising, because nothing about the call site looks wrong: **any class with a `virtual` function needs a `virtual` destructor.** See [The virtual destructor rule](polymorphism.md#the-virtual-destructor-rule).
````

### W3. Moving a unique_ptr

<!-- no-ce -->
```cpp
#include <iostream>
#include <memory>

class Valve {
public:
    explicit Valve(int id) : id_(id) { std::cout << "open " << id_ << "\n"; }
    ~Valve() { std::cout << "close " << id_ << "\n"; }

private:
    int id_;
};

int main() {
    auto a = std::make_unique<Valve>(1);
    auto b = std::move(a);

    std::cout << (a ? "a holds it" : "a is empty") << "\n";
    std::cout << "end of main\n";
}
```

````quiz
What does this print?
- `open 1`, `a holds it`, `end of main`, `close 1`
- =`open 1`, `a is empty`, `end of main`, `close 1`
- `open 1`, `a is empty`, `close 1`, `end of main`
- `open 1`, `a is empty`, `end of main`, `close 1`, `close 1`
:::
**`open 1`, `a is empty`, `end of main`, `close 1`.**

`std::move(a)` transfers ownership to `b` and leaves `a` **empty** — a moved-from `unique_ptr` is guaranteed to be null, so `a ? ... : ...` takes the second branch. This is one of the few moved-from states the standard pins down exactly; for [most types it is only "valid but unspecified"](move.md#a-note-on-the-moved-from-object).

The valve is closed **once**, at the end of `main`, when `b` is destroyed. Not twice — there was only ever one `Valve`, and only ever one owner of it. And not early — moving the pointer did not touch the object it points at.

That "exactly one owner, cleanup exactly once, no `delete` anywhere" is the whole reason to use `unique_ptr`. See [`std::unique_ptr`](memory.md#stdunique_ptr-the-default).
````

### W4. Counting owners

<!-- no-ce -->
```cpp
#include <iostream>
#include <memory>

int main() {
    auto s = std::make_shared<int>(42);
    std::cout << s.use_count() << " ";

    {
        auto t = s;
        std::cout << s.use_count() << " ";
    }

    std::cout << s.use_count() << "\n";
}
```

````quiz
What does this print?
- `1 1 1`
- `1 2 2`
- =`1 2 1`
- `1 3 1`
:::
**`1 2 1`.**

A `shared_ptr` **can** be copied, and every copy is another co-owner: `auto t = s;` raises the count to `2`. When `t` goes out of scope at the closing brace its destructor drops the count back to `1`. The `int` itself is destroyed only when the count reaches **zero**, at the end of `main`.

That is the entire difference from `unique_ptr`, which forbids copying outright precisely so this counting is never needed. Reach for `shared_ptr` only when ownership is genuinely shared — it is rarer than beginners expect, and the count is not free. See [`std::shared_ptr`](memory.md#stdshared_ptr-shared-ownership).
````

### W5. One template, two types

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    std::string s = "x";
    std::cout << add(s, 5) << "\n";
}
```

````quiz
What happens?
- It prints `x5`
- It prints `x`
- =It does not compile: `T` cannot be both `std::string` and `int`
- It compiles, and `5` is converted to `std::string`
:::
**It does not compile.**

`add` has **one** type parameter used for **both** arguments, so the compiler must deduce a single `T`. The first argument says `std::string`, the second says `int`, and there is no tie-breaker — deduction fails before any code is generated. MSVC puts it plainly:

```
error C2672: 'add': no matching overloaded function found
note: 'T add(T,T)': template parameter 'T' is ambiguous
note: could be 'int'
note: or       'std::string'
```

Note what does **not** happen: no conversion is attempted. Template argument deduction does not convert to make a match — it deduces from the arguments exactly as written, and gives up if they disagree.

Long template errors read worse than this one, but decode the same way: start at the top, then look for the `note:` lines explaining why each candidate was rejected. See [What template errors look like](templates.md#what-template-errors-look-like).
````

---

## 1. A resource that frees itself

*Practises: [Memory Management](memory.md)*

Write a class `Valve` whose constructor prints `Valve N opened` and whose destructor prints `Valve N closed` (where `N` is an id passed in). Then, in `main`, create a `std::unique_ptr<Valve>` with `std::make_unique` and move it into a *second* `unique_ptr` using `std::move`. Print, for each pointer, whether it is empty or still holds the valve — after the move, the first is empty and the second holds it.

You should see the valve closed **exactly once**, automatically, with no `delete` anywhere.

> Hint: `std::make_unique<Valve>(1)` gives you the pointer; `std::move` hands ownership over; test a pointer for emptiness with `if (p)`. A `unique_ptr` cannot be copied — only moved.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <memory>

    class Valve {
    public:
        explicit Valve(int id) : id_(id) { std::cout << "Valve " << id_ << " opened\n"; }
        ~Valve() { std::cout << "Valve " << id_ << " closed\n"; }
    private:
        int id_;
    };

    int main() {
        std::unique_ptr<Valve> a = std::make_unique<Valve>(1);   // "Valve 1 opened"

        std::unique_ptr<Valve> b = std::move(a);   // ownership moves to b; a is left empty
        std::cout << "a is " << (a ? "holding the valve" : "empty") << "\n";  // empty
        std::cout << "b is " << (b ? "holding the valve" : "empty") << "\n";  // holding the valve
    }   // b goes out of scope here → "Valve 1 closed" (exactly once)
    ```

    `std::make_unique<Valve>(1)` allocates a `Valve` on the heap and hands it to `a`; you never write `new` or `delete`. `std::move(a)` transfers ownership to `b`, leaving `a` empty — a `unique_ptr` cannot be copied (that would create two owners), so moving is the only way to hand it over. When `b` goes out of scope at the end of `main`, it destroys the one `Valve`, so "closed" prints exactly once. No leak, no double-free, no manual cleanup.

    </div>

---

## 2. A handle you can move but not copy

*Practises: [Move Semantics](move.md)* — **advanced / optional**

> This one builds on the [Designing a movable class](move.md#designing-a-movable-class) section, the deepest material in the chapter. It is here for the curious; you can skip it without missing anything the later chapters rely on.

A data-acquisition `Channel` is a *unique* resource: there is one physical channel, so the object should be **movable but not copyable**. Write a class `Channel` that prints `Channel N open` in its constructor and `Channel N closed` in its destructor. Make it move-only: write the move constructor and move assignment (transfer the id and leave the source empty), `= delete` the copy operations, and have the destructor skip a moved-from channel.

In `main`, open channel `1`, move it into a second variable, and confirm it closes exactly once.

> Hint: use `-1` to mean "owns nothing". The destructor checks `if (id_ != -1)`; the move constructor steals `other.id_` then sets it to `-1`; the move assignment releases what it holds first, then steals, then empties the source (and guards against self-assignment). Mark both moves `noexcept`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <utility>   // std::move

    class Channel {
    public:
        explicit Channel(int id) : id_(id) { std::cout << "Channel " << id_ << " open\n"; }

        ~Channel() {
            if (id_ != -1) { std::cout << "Channel " << id_ << " closed\n"; }
        }

        Channel(Channel&& other) noexcept : id_(other.id_) {   // move constructor
            other.id_ = -1;
        }

        Channel& operator=(Channel&& other) noexcept {         // move assignment
            if (this != &other) {
                if (id_ != -1) { std::cout << "Channel " << id_ << " closed\n"; }
                id_ = other.id_;
                other.id_ = -1;
            }
            return *this;
        }

        Channel(const Channel&)            = delete;           // no copying
        Channel& operator=(const Channel&) = delete;

    private:
        int id_ = -1;     // -1 means "owns no channel"
    };

    int main() {
        Channel a(1);                  // "Channel 1 open"
        Channel b = std::move(a);      // ownership moves to b; a is now empty
        // Channel c = b;              // compile error: Channel cannot be copied
    }   // b closes channel 1 (once); a is empty and closes nothing
    ```

    A channel is unique, so `Channel` is **move-only**: it has move operations, and its copy operations are `= delete`d. The move constructor steals the other channel's id and sets the source to the empty state (`-1`); the destructor checks for that state, so a moved-from channel closes nothing. Because copying is deleted, `Channel c = b;` is a *compile error* rather than a silent double-close. The moves are `noexcept`; since `Channel` is move-only a `std::vector<Channel>` must move it when it grows in any case, but `noexcept` is the right habit — it is what lets a vector move *copyable* types instead of copying them, and preserves the container's exception guarantees. (You wrote a destructor and the move operations — the **Rule of Five** — so you accounted for the copies too. You could avoid all of it by storing the handle in a `std::unique_ptr`: the **Rule of Zero**.)

    </div>

---

## 3. One interface, many shapes

*Practises: [Polymorphism](polymorphism.md)*

Write an abstract base class `Shape` with a pure virtual `double area() const` and a `virtual` destructor. Derive `Circle` (from a radius) and `Square` (from a side), each `override`-ing `area()`. Write a free function `void printArea(const Shape& s)` that prints `s.area()`.

In `main`, call `printArea` on a `Circle` and a `Square` through that single function. Then store a mix of shapes in a `std::vector<std::unique_ptr<Shape>>` and print every area in a loop.

> Hint: `virtual double area() const = 0;` makes `Shape` abstract; `virtual ~Shape() = default;` is essential. Add shapes with `std::make_unique<Circle>(2.0)`. Use `3.14159` for π.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <memory>
    #include <vector>

    class Shape {
    public:
        virtual ~Shape() = default;          // a polymorphic base needs a virtual destructor
        virtual double area() const = 0;     // pure virtual → Shape is abstract
    };

    class Circle : public Shape {
    public:
        explicit Circle(double radius) : radius_(radius) {}
        double area() const override { return 3.14159 * radius_ * radius_; }
    private:
        double radius_;
    };

    class Square : public Shape {
    public:
        explicit Square(double side) : side_(side) {}
        double area() const override { return side_ * side_; }
    private:
        double side_;
    };

    void printArea(const Shape& s) {         // works for any Shape
        std::cout << "area = " << s.area() << "\n";
    }

    int main() {
        Circle c(2.0);
        Square s(3.0);
        printArea(c);     // area = 12.566...
        printArea(s);     // area = 9

        std::vector<std::unique_ptr<Shape>> shapes;
        shapes.push_back(std::make_unique<Circle>(1.0));
        shapes.push_back(std::make_unique<Square>(5.0));
        for (const auto& shape : shapes) {
            printArea(*shape);               // area = 3.14159, then area = 25
        }
    }
    ```

    `Shape` is **abstract** — its `area()` is pure virtual (`= 0`), so you cannot create a bare `Shape`, only something that *is* a `Shape`. `Circle` and `Square` each `override` `area()`. `printArea` takes `const Shape&` and calls `area()`; because `area` is `virtual`, the call dispatches to the real type at run time — that is polymorphism. `std::vector<std::unique_ptr<Shape>>` is the standard way to hold a mixed collection of polymorphic objects: each `unique_ptr` owns its object and frees it automatically. The `virtual` destructor is what makes that safe — deleting a `Circle` through a `Shape` pointer (which is exactly what the `unique_ptr` does) would be undefined behaviour without it.

    </div>

---

## 4. A function that works for any type

*Practises: [Templates](templates.md)*

Write a function template `largest` that takes a `std::vector<T>` and returns its biggest element, for any type `T` that supports `>`. In `main`, call it on a vector of `int`, a vector of `double`, and a vector of `std::string`, and print each result.

Notice that the *same* function works for all three — including strings, which compare alphabetically.

> Hint: `template <typename T>` goes above the function; the return type and the parameter both use `T`. Start your "biggest so far" from the first element (`values.at(0)`) and walk the rest. You do not write the type at the call site — the compiler deduces `T` from the argument.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>
    #include <vector>

    template <typename T>
    T largest(const std::vector<T>& values) {
        T biggest = values.at(0);            // assumes at least one element
        for (const T& v : values) {
            if (v > biggest) {
                biggest = v;
            }
        }
        return biggest;
    }

    int main() {
        std::vector<int>         ints    = {3, 9, 2, 7};
        std::vector<double>      doubles = {1.5, 0.5, 2.25};
        std::vector<std::string> words   = {"apple", "pear", "fig"};

        std::cout << largest(ints)    << "\n";   // 9
        std::cout << largest(doubles) << "\n";   // 2.25
        std::cout << largest(words)   << "\n";   // pear
    }
    ```

    `largest` is written once but works for any type `T` with a `>` operator. The compiler generates a separate version for each type you actually use — `largest<int>`, `largest<double>`, `largest<std::string>` — each as efficient as if you had written it by hand. You never spell out the type at the call site: the compiler deduces `T` from the argument, so `largest(ints)` gives `T = int`. That is the whole point of a template — write the logic once, and it applies to every type that fits. (`std::string`'s `>` compares alphabetically, so `"pear"` wins.)

    </div>

---

## 5. A sensor shared by two owners

*Practises: [Memory Management](memory.md)*

One `Sensor` is used by both a `Logger` and a `Controller`; neither should own it alone, and it must live until *both* are done with it. Model this with `std::shared_ptr`.

Write a `Sensor` that prints `Sensor N created` in its constructor and `Sensor N destroyed` in its destructor. Write a `Logger` and a `Controller` that each store a `std::shared_ptr<Sensor>` (take it by value in the constructor and `std::move` it into the member). In `main`, make one sensor with `std::make_shared`, print `use_count()`, hand it to a `Logger`, print the count again, then hand it to a `Controller` **inside an inner `{ }` block** and print the count once more. After the block, print the count again.

Watch the count rise to 3 and fall back to 2 as the `Controller` is destroyed, and confirm the sensor is destroyed only at the very end — when the *last* owner goes away.

> Hint: `use_count()` reports how many `shared_ptr`s own the object. Copying a `shared_ptr` (which is what handing it to a constructor does) bumps the count; destroying one drops it. The sensor's destructor runs when the count hits zero.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <memory>
    #include <string>

    class Sensor {
    public:
        explicit Sensor(std::string name) : name_(std::move(name)) {
            std::cout << "Sensor " << name_ << " created\n";
        }
        ~Sensor() { std::cout << "Sensor " << name_ << " destroyed\n"; }
    private:
        std::string name_;
    };

    class Logger {
    public:
        explicit Logger(std::shared_ptr<Sensor> s) : sensor_(std::move(s)) {}
    private:
        std::shared_ptr<Sensor> sensor_;
    };

    class Controller {
    public:
        explicit Controller(std::shared_ptr<Sensor> s) : sensor_(std::move(s)) {}
    private:
        std::shared_ptr<Sensor> sensor_;
    };

    int main() {
        auto sensor = std::make_shared<Sensor>("outdoor");
        std::cout << "owners: " << sensor.use_count() << "\n";   // 1

        Logger logger(sensor);
        std::cout << "owners: " << sensor.use_count() << "\n";   // 2

        {
            Controller controller(sensor);
            std::cout << "owners: " << sensor.use_count() << "\n";   // 3
        }   // controller destroyed → count drops back to 2

        std::cout << "owners: " << sensor.use_count() << "\n";   // 2
        std::cout << "leaving main\n";
    }   // logger and sensor go → count hits 0 → sensor destroyed here
    ```

    The output is:

    ```
    Sensor outdoor created
    owners: 1
    owners: 2
    owners: 3
    owners: 2
    leaving main
    Sensor outdoor destroyed
    ```

    Each `shared_ptr` that owns the sensor counts as one owner, and copying one (which is what passing it to `Logger`/`Controller` does) raises the count. Unlike a `unique_ptr` — which cannot be copied at all — a `shared_ptr` is *meant* to be copied, and the reference count is how it knows when the last owner is gone. The `Controller` inside the block drops the count from 3 back to 2 when it is destroyed; the sensor itself is not destroyed until `leaving main` has printed and both remaining owners (`logger` and `sensor`) disappear at the end of `main`. That "destroy exactly when the last owner dies" behaviour is the whole reason `shared_ptr` exists.

    </div>

---

## 6. A base class that needs arguments

*Practises: [Polymorphism](polymorphism.md)*

Every `Sensor` has a **name**, fixed when it is built, so the base class has a constructor `Sensor(std::string name)` and *no* default constructor. Derive two concrete sensors from it and make each forward the name up to the base.

Write an abstract `Sensor` with a `std::string name_` (set via `Sensor(std::string name)`), a `name()` getter, a **pure virtual** `double read() const`, and a virtual destructor. Derive `Thermometer` (constructed from a name and a temperature) and `Barometer` (a name and a pressure); each forwards the name to `Sensor` in its initialiser list and `override`s `read()`. Write `void report(const Sensor& s)` that prints the name and reading, store a mix in a `std::vector<std::unique_ptr<Sensor>>`, and report each.

The lesson: because `Sensor` has no default constructor, a derived constructor that forgets `: Sensor(...)` **will not compile** — try it and read the error.

> Hint: the derived initialiser list runs the base constructor first: `Thermometer(std::string name, double c) : Sensor(std::move(name)), celsius_(c) {}`. Add sensors with `std::make_unique<Thermometer>("outdoor", 21.5)`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <memory>
    #include <string>
    #include <vector>

    class Sensor {
    public:
        explicit Sensor(std::string name) : name_(std::move(name)) {}
        virtual ~Sensor() = default;

        virtual double read() const = 0;              // pure virtual → Sensor is abstract
        const std::string& name() const { return name_; }

    private:
        std::string name_;
    };

    class Thermometer : public Sensor {
    public:
        Thermometer(std::string name, double celsius)
            : Sensor(std::move(name)),   // forward the name to the base constructor
              celsius_(celsius) {}
        double read() const override { return celsius_; }
    private:
        double celsius_;
    };

    class Barometer : public Sensor {
    public:
        Barometer(std::string name, double kPa)
            : Sensor(std::move(name)),
              kPa_(kPa) {}
        double read() const override { return kPa_; }
    private:
        double kPa_;
    };

    void report(const Sensor& s) {
        std::cout << s.name() << " = " << s.read() << "\n";
    }

    int main() {
        std::vector<std::unique_ptr<Sensor>> sensors;
        sensors.push_back(std::make_unique<Thermometer>("outdoor", 21.5));
        sensors.push_back(std::make_unique<Barometer>("roof", 101.3));

        for (const auto& s : sensors) {
            report(*s);        // outdoor = 21.5, then roof = 101.3
        }
    }
    ```

    `Sensor` has only the one constructor, `Sensor(std::string)`, so it has **no default constructor**. That means each derived constructor *must* name `Sensor(...)` in its initialiser list to build the base part — `Thermometer(std::string, double) : Sensor(std::move(name)), celsius_(celsius) {}`. Leave the `: Sensor(...)` off and the compiler refuses with an error about `Sensor::Sensor()`, the default constructor that does not exist. The base part is always constructed first, then the derived members. Everything else is ordinary polymorphism: `read()` is pure virtual, so `Sensor` is abstract; `report` takes `const Sensor&` and dispatches to the real type at run time; and the `std::vector<std::unique_ptr<Sensor>>` holds the mixed collection, each object freed automatically through the virtual destructor.

    </div>
