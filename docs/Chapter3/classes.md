# Classes

A **class** is a user-defined type. Where an `int` holds an integer and a `std::vector` holds a list of values, a class you write holds whatever data your problem needs — a motor, a controller, a sensor reading — together with the operations that make sense on that data.

Classes are the unit of organisation in object-oriented C++. Everything else in this chapter, and most of the rest of the book, hangs off this idea: bundle related data and the operations that work on it into a single type.

---

## A first class

```cpp
class Motor {
public:
    void start()      { running_ = true; }
    void stop()       { running_ = false; }
    bool isRunning() const { return running_; }

private:
    bool running_ = false;
};
```

Three parts to read off:

- **The class name** — `Motor`. Capitalised by convention.
- **Public members** — what code *outside* the class can use. Here: `start`, `stop`, `isRunning`.
- **Private members** — internal state. Here: `running_`. The trailing underscore is a convention for "this is a class data member."

Using it:

```cpp
Motor m;
m.start();
if (m.isRunning()) {
    std::cout << "running\n";
}
m.stop();
```

Outside code can call `m.start()` because `start` is public. Outside code cannot write `m.running_ = true;` directly — `running_` is private. This is the basic shape of **encapsulation**: the class owns its state and decides what the outside world is allowed to do with it.

---

## Members: data and functions

A class has two kinds of members:

- **Data members** (often called fields, attributes, or instance variables) — the data each instance holds.
- **Member functions** (often called methods) — the operations the class supports.

```cpp
class Sensor {
public:
    double read() const { return lastReading_; }
    void   update(double value) { lastReading_ = value; }

private:
    double lastReading_ = 0.0;     // data member
    int    sampleCount_ = 0;       // data member
};
```

A `const` after the parameter list — like `read() const` — means "this function does not modify the object." Mark every member function `const` if it can be. The compiler enforces it, and it tells the reader "calling this is safe; it observes, it does not change."

---

## Access specifiers

Three keywords control what is accessible from where:

| Specifier | Visible from outside the class | Visible from a derived class |
|-----------|--------------------------------|------------------------------|
| `public`    | Yes | Yes |
| `protected` | No  | Yes |
| `private`   | No  | No  |

For everyday classes, `public` is for the interface and `private` is for everything else. `protected` shows up later when you start designing inheritance hierarchies. Default to `private`; relax to `public` only when outside code genuinely needs access.

---

## Constructors

A **constructor** is a special member function that runs when an object is created. It is where you set up the initial state.

```cpp
class Motor {
public:
    Motor(int id, double maxRpm)
        : id_(id), maxRpm_(maxRpm) {}      // member initialiser list

private:
    int    id_;
    double maxRpm_;
    bool   running_ = false;
};

Motor m(1, 3000.0);   // calls the constructor with id=1, maxRpm=3000.0
```

The part after the `:` and before the `{}` is the **member initialiser list**. It initialises the data members directly, before the constructor body runs.

Prefer the member initialiser list over assignment in the constructor body:

```cpp
// Less good — members are default-constructed and then assigned
Motor(int id, double maxRpm) {
    id_     = id;
    maxRpm_ = maxRpm;
}

// Better — members are constructed with the right value in one step
Motor(int id, double maxRpm)
    : id_(id), maxRpm_(maxRpm) {}
```

The difference matters more for non-trivial types (you avoid an extra default construction) and is essential for members that *must* be initialised exactly once (`const` members, references, types without a default constructor).

### Default values for data members

You can give data members default values directly in the class definition:

```cpp
class Motor {
private:
    int    id_      = 0;
    double maxRpm_  = 1000.0;
    bool   running_ = false;
};
```

A constructor that does not mention a member uses the default. If the constructor's initialiser list does mention it, that value wins.

### Multiple constructors

You can have several constructors as long as they take different parameters:

```cpp
class Motor {
public:
    Motor() = default;                            // default constructor
    Motor(int id) : id_(id) {}
    Motor(int id, double maxRpm) : id_(id), maxRpm_(maxRpm) {}
};

Motor a;              // default
Motor b(1);           // id only
Motor c(2, 5000.0);   // id and max RPM
```

`= default` asks the compiler to generate a do-nothing default constructor for you. It is shorter than writing `Motor() {}` and signals intent.

---

## The `this` pointer

Inside any member function, `this` is a pointer to the object the function was called on. You rarely have to write it explicitly because members are accessible by their bare name:

```cpp
void Motor::start() {
    running_ = true;       // means this->running_
}
```

The one case where you *do* need `this`: when a parameter shadows a member.

```cpp
class Motor {
public:
    void setId(int id) {
        this->id_ = id;   // disambiguate — but better to avoid the shadow:
    }
    // Cleaner:
    // void setId(int newId) { id_ = newId; }

private:
    int id_;
};
```

Decorate your data members (the trailing-underscore convention) and shadowing rarely happens in the first place.

---

## Encapsulation in practice

The point of making data private is not paranoia — it is that the class can enforce **invariants**: rules about the data that should never be broken.

A bank account whose balance must never go negative; a sensor whose timestamp must never decrease; a motor whose RPM cannot exceed its rated maximum. If the data is public, every caller has to remember to check. If the data is private and only updated via member functions, the check lives in one place.

```cpp
class BankAccount {
public:
    BankAccount(double initialBalance)
        : balance_(initialBalance) {}

    void deposit(double amount) {
        if (amount <= 0) {
            return;                  // refuse nonsense
        }
        balance_ += amount;
    }

    bool withdraw(double amount) {
        if (amount <= 0 || amount > balance_) {
            return false;            // can't go negative
        }
        balance_ -= amount;
        return true;
    }

    double balance() const { return balance_; }

private:
    double balance_;
};
```

`balance_` is private, so it can only change through `deposit` and `withdraw` — both of which check the operation before they apply it. The invariant "balance is never negative" is enforced in one place.

---

## Special member functions: the Rule of Zero, Three, and Five

When you create or copy or destroy an object, C++ may call up to six special member functions:

| Function | When it runs |
|----------|--------------|
| Default constructor    | Creating an object with no arguments |
| Destructor             | When the object is destroyed |
| Copy constructor       | Initialising a new object from an existing one (`B b = a;`) |
| Copy assignment        | Assigning to an existing object (`b = a;`) |
| Move constructor       | Initialising from a temporary or `std::move`d value |
| Move assignment        | Assigning from a temporary or `std::move`d value |

If you do not write any of these, the compiler generates them for you. The generated versions do the obvious thing: copy or move each member. For *most* classes, that is exactly what you want.

The rules of thumb are well-known:

### Rule of Zero (the modern default)

> If your class's data members can manage themselves (via standard containers or smart pointers), do not write any special member functions. The compiler-generated defaults are correct.

```cpp
class Telemetry {
public:
    Telemetry(std::string deviceId)
        : deviceId_(std::move(deviceId)) {}

    void record(double value) { samples_.push_back(value); }

private:
    std::string         deviceId_;
    std::vector<double> samples_;
};
```

No destructor. No copy or move operations. The defaults work because `std::string` and `std::vector` already know how to copy, move, and destroy themselves correctly. This is the cleanest possible class design and the goal for almost all your classes.

### Rule of Three (the C++03 rule)

> If you write a destructor, you almost certainly also need a copy constructor and a copy assignment operator — and vice versa.

The classical reason: a class with a destructor probably manages a resource (memory, a file, a lock). The compiler-generated copy operations just shallow-copy the resource handle, which means two objects now think they own the same thing. Disaster on destruction.

```cpp
class BadBuffer {
public:
    BadBuffer(int size) : data_(new int[size]) {}
    ~BadBuffer()        { delete[] data_; }
    // no copy constructor, no copy assignment — compiler generates broken ones

private:
    int* data_;
};

BadBuffer a(100);
BadBuffer b = a;     // SAME pointer in both! double-delete on destruction
```

**Better solution:** don't own raw resources. Use `std::unique_ptr`, `std::vector`, or `std::string` for the resource, and you are back to the Rule of Zero.

### Rule of Five (C++11 and later)

> If you write any of the five (destructor, copy ctor, copy assignment, move ctor, move assignment), you probably need to think about all five.

Modern C++ added move operations. If you write a destructor and copy operations, the compiler stops generating move operations for you — which can quietly make your class slower than it should be.

The practical advice for this course: **aim for the Rule of Zero**. If you can't, write all five explicitly. If you find yourself implementing a destructor, ask whether you can replace the raw resource with a smart pointer or a standard container instead.

---

## Splitting the declaration and the implementation

Everything we have written so far has had the implementation inside the class body. For longer functions, you usually split them out:

**motor.hpp** — the declaration:

```cpp
#pragma once
#include <string>

class Motor {
public:
    Motor(int id, double maxRpm);

    void start();
    void stop();
    bool isRunning() const;

    std::string describe() const;

private:
    int    id_;
    double maxRpm_;
    bool   running_ = false;
};
```

**motor.cpp** — the implementation:

```cpp
#include "motor.hpp"
#include <format>

Motor::Motor(int id, double maxRpm)
    : id_(id), maxRpm_(maxRpm) {}

void Motor::start() {
    running_ = true;
}

void Motor::stop() {
    running_ = false;
}

bool Motor::isRunning() const {
    return running_;
}

std::string Motor::describe() const {
    return std::format("Motor {} (max {} RPM)", id_, maxRpm_);
}
```

`Motor::` in front of each function name says "this function belongs to the `Motor` class." The header is what other files `#include`; the implementation file is compiled separately.

For short functions — one-liners, simple getters — it is fine to keep them inside the class. For anything bigger, split. Compile times improve and the header stays readable.

---

## Summary

- A class bundles data with the operations that work on it.
- Default data to `private` and expose only the operations callers need (`public`).
- Use the **member initialiser list** for constructors.
- Decorate data members (`balance_`, `id_`) to avoid name conflicts with parameters.
- Mark member functions `const` whenever they don't modify the object.
- **Aim for the Rule of Zero**: design classes whose members manage themselves, and let the compiler generate the special members.
- Split long classes into a header (`.hpp`) and an implementation (`.cpp`).
