# Move Semantics

Some operations in C++ involve transferring ownership of data from one object to another. **Move semantics**, introduced in C++11, let you do this *without copying*, which is often dramatically faster.

To see why this matters, you first have to understand what "copying" actually costs.

---

## The cost of a copy

Consider a `std::string` holding the contents of a 10 MB log file:

```cpp
std::string log = readEntireFile("server.log");   // 10 MB of text
```

What is *inside* a `std::string`? Three things:

- a pointer to a heap-allocated character array,
- a `size` (how many characters are in use),
- a `capacity` (how many characters the buffer can hold).

The string object itself is small, typically 24 or 32 bytes on a desktop platform. The 10 MB of actual text lives on the heap.

Now copy the string:

```cpp
std::string copy = log;     // copy
```

C++ must produce a brand-new `std::string` whose state is independent of the original. That means:

1. Allocate a fresh 10 MB buffer on the heap.
2. `memcpy` all 10 MB from the source buffer to the new one.
3. Set the new string's pointer, size, and capacity to match.

For 10 MB this is slow. For a `std::vector<Motor>` holding a thousand motors, you also call a thousand copy constructors. Whenever the data being copied does not need to persist at the source, this work is wasted.

---

## What move does instead

A **move** transfers ownership of the underlying resource, without copying it.

```cpp
std::string log = readEntireFile("server.log");
std::string copy = std::move(log);   // move, not copy
```

Now C++ does this:

1. Copy the three small fields (pointer, size, capacity) from `log` into `copy`.
2. Set `log`'s pointer to `nullptr` and its size and capacity to zero, so that its destructor does nothing harmful.

That is it. No 10 MB allocation, no `memcpy`, no thousand copy constructors. Three pointer-sized writes, regardless of the size of the data.

```text
   before move

       log  ●──►  [ 10 MB of text ]

   after move

       log   (empty)
       copy ●──►  [ 10 MB of text ]   ← same buffer, not copied
```

After the move, `copy` owns the 10 MB and `log` is in a **valid but unspecified state** (usually empty). You may assign to it or destroy it, but you should not assume any particular contents.

---

## When move happens automatically

You very rarely have to type `std::move` yourself. The compiler inserts moves automatically in two important cases:

**1. Returning a local object from a function.**

```cpp
std::vector<int> readSamples() {
    std::vector<int> samples;
    for (int i = 0; i < 1000; ++i) {
        samples.push_back(i);
    }
    return samples;     // moved (or even better, see RVO below)
}

std::vector<int> data = readSamples();   // no copy, no move call needed
```

**2. Passing a temporary into a function.**

```cpp
std::vector<std::string> names;
names.push_back(std::string("Alice"));   // the temporary string is moved in
names.push_back("Bob");                  // same, the temporary is moved
```

The compiler can see that the source value will not be used afterwards, so it moves rather than copies. In modern C++ this happens by default, and the language-level optimisation called **Return Value Optimisation (RVO)** often eliminates even the move: the function builds the return value directly in the caller's variable.

> **Do not write `return std::move(samples);`** on a local variable. It disables RVO and is actually slower than just `return samples;`.

---

## When to write `std::move` yourself

The pattern is: "I have a named variable, I am done with it, and I want its contents to land somewhere else without a copy."

```cpp
class Logger {
public:
    Logger(std::string filename)
        : filename_(std::move(filename)) {}   // move the parameter into the member
private:
    std::string filename_;
};
```

The parameter `filename` is a named local variable, and the compiler will not move it for you automatically. Without `std::move`, the member is *copy-constructed* from it (a needless allocation). With `std::move`, the member adopts the parameter's storage.

Another common case: transferring ownership of a `unique_ptr`.

```cpp
std::unique_ptr<Motor> motor = std::make_unique<Motor>(1);
sim.installMotor(std::move(motor));
// motor is now empty; sim owns the Motor
```

`unique_ptr` cannot be copied (copying would create a second owner), so `std::move` is the *only* way to hand one over.

---

## Move constructors and move assignment

When you copy an object, the compiler calls its **copy constructor**. When you move one, it calls its **move constructor**. For standard library types (`std::string`, `std::vector`, `std::unique_ptr`, `std::map`, etc.) both are already implemented correctly.

If you write your own class and follow the [Rule of Zero](memory.md#the-rule-of-zero), letting your members manage themselves, the compiler also generates a correct move constructor for free. You almost never have to write one by hand.

---

## Designing a movable class

The Rule of Zero covers almost everything. But occasionally a class owns a **raw resource** that no standard type already wraps — a handle from a C API, a hardware connection, a lock. Then the compiler-generated operations are wrong, and you must write the move operations yourself.

Take the `SensorConnection` from [RAII](../Chapter4/raii.md): it opens a connection in its constructor and closes it in its destructor. A connection is *unique* — there is one physical link, and copying the object cannot duplicate it. So the right design is **move-only**: you can transfer the connection out of one object into another, but you cannot copy it. This is exactly how `std::unique_ptr` behaves.

```cpp
class SensorConnection {
public:
    explicit SensorConnection(int id) : id_(id) {
        std::cout << "Opened connection to sensor " << id_ << "\n";
    }

    ~SensorConnection() {
        if (id_ != -1) {                       // a moved-from object owns nothing
            std::cout << "Closed connection to sensor " << id_ << "\n";
        }
    }

    SensorConnection(SensorConnection&& other) noexcept    // move constructor
        : id_(other.id_) {
        other.id_ = -1;                        // leave the source empty
    }

    SensorConnection& operator=(SensorConnection&& other) noexcept {   // move assignment
        if (this != &other) {                  // guard against `x = std::move(x)`
            if (id_ != -1) {
                std::cout << "Closed connection to sensor " << id_ << "\n";   // release ours first
            }
            id_ = other.id_;                   // steal the other's
            other.id_ = -1;                    // leave it empty
        }
        return *this;
    }

    SensorConnection(const SensorConnection&)            = delete;    // no copying
    SensorConnection& operator=(const SensorConnection&) = delete;

private:
    int id_ = -1;                              // -1 means "owns no connection"
};
```

Four things make it correct:

- **A way to represent "empty."** After being moved from, an object must own nothing, so its destructor does nothing. Here `id_ == -1` is that state, and the destructor checks for it.
- **The move constructor steals.** It takes the handle out of `other` and then sets `other` to empty — no connection is opened or closed, just two integer writes.
- **Move assignment releases, then steals.** It closes the connection it currently holds before taking the other's, and guards against self-assignment (`x = std::move(x)`).
- **Copying is `= delete`d.** That states the move-only intent and turns any attempt to copy into a compile error, rather than a silent, broken duplicate.

**Mark the move operations `noexcept`.** It promises they cannot throw — true here, since they only shuffle a handle around. This matters in practice: `std::vector` will only *move* your objects when it grows (rather than copy them) if their move constructor is `noexcept`.

This is the **Rule of Five** from [Memory Management](memory.md#the-rule-of-zero): once you write a destructor and the move operations, the compiler stops filling in the rest, so you account for all five — here, by deleting the copies.

> **Prefer the Rule of Zero even here.** All of this disappears if the resource lives in a `std::unique_ptr` member (with a custom deleter for a C API) or a standard container: the generated moves are correct, copying is disabled for free, and you write *none* of the five. Hand-write the operations only for a raw resource that nothing else wraps — and keep that wrapper as small as you can.

---

## A note on the moved-from object

After `std::move(x)`, `x` is still a valid object. You can destroy it; you can assign a new value to it. But you should **not** assume anything about its current value.

```cpp
std::string a = "Hello";
std::string b = std::move(a);

std::cout << a << "\n";   // legal, but the result is unspecified
a = "Goodbye";            // legal and well-defined
```

A simple rule of thumb: treat a moved-from variable as if it has been freshly default-constructed. Either assign to it or let it go out of scope.

---

## Summary

- A **copy** duplicates the underlying data; potentially expensive.
- A **move** transfers ownership of the underlying data; cheap (a few pointer writes).
- The compiler inserts moves automatically for returns and temporaries.
- Write `std::move` yourself when you have a named variable whose contents you want to hand off.
- Do **not** `std::move` a return value of a local variable; it disables RVO.
- Use moves when transferring `unique_ptr`s; they cannot be copied.
- Own a **raw resource**? Make the class **move-only** — `noexcept` move operations, copies `= delete`d — or wrap it in a `unique_ptr` and write none of them (Rule of Zero).
- A moved-from object is valid but unspecified; assign to it or destroy it.
