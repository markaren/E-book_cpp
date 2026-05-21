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
- A moved-from object is valid but unspecified; assign to it or destroy it.
