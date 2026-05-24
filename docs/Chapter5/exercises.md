# Chapter 5 Exercises

Work through these after reading Chapter 5. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Each exercise is a small program with its own `main()`. Keep them in one project with one `add_executable` line per file (see [CMake](../Chapter2/cmake_intro.md)), and pick which to run from the dropdown next to the green ▶ button.

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

*Practises: [Move Semantics](move.md)*

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

    A channel is unique, so `Channel` is **move-only**: it has move operations, and its copy operations are `= delete`d. The move constructor steals the other channel's id and sets the source to the empty state (`-1`); the destructor checks for that state, so a moved-from channel closes nothing. Because copying is deleted, `Channel c = b;` is a *compile error* rather than a silent double-close. The moves are `noexcept`, which is what lets a `std::vector<Channel>` move its elements instead of copying them when it grows. (You wrote a destructor and the move operations — the **Rule of Five** — so you accounted for the copies too. You could avoid all of it by storing the handle in a `std::unique_ptr`: the **Rule of Zero**.)

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
