# RAII

Every program uses resources that have to be handed back: memory that must be freed, files that must be closed, device connections that must be released. Forget to release one and you get a *leak*; release it twice and you corrupt something. Remembering to clean up by hand, on every path through your code, is exactly the kind of bookkeeping humans get wrong.

C++'s answer is **RAII** — *Resource Acquisition Is Initialization*, an awkward name for a simple idea: tie a resource to the lifetime of an object, so cleanup happens **automatically** when the object goes out of scope. It is the foundation almost all modern C++ rests on.

---

## The problem: cleanup by hand

To see what RAII replaces, here is cleanup done by hand — a pair of "open it / close it" calls you must keep balanced yourself:

```cpp
void logReadings() {
    openSensor(7);                 // acquire

    if (somethingWrong()) {
        return;                    // BUG: the sensor is never closed
    }

    // ... read and log the values ...

    closeSensor(7);                // only reached on the normal path
}
```

The `closeSensor` at the bottom only runs if execution reaches it. The early `return` skips it, and the connection leaks. Every additional exit point — another `return`, a `break`, later an exception — is one more place that must remember the cleanup, and sooner or later one of them is forgotten. The fix is not "be more careful". The fix is to make cleanup impossible to forget.

---

## The destructor

A constructor runs when an object is created. Its mirror image, the **destructor**, runs automatically when the object is destroyed — which, for a local variable, is the moment it goes out of scope. A destructor is named `~` followed by the class name, takes no arguments, and you never call it yourself; the compiler inserts the call for you.

RAII is just this: **acquire the resource in the constructor, release it in the destructor.**

```cpp
#include <iostream>

class SensorConnection {
public:
    explicit SensorConnection(int id) : id_(id) {
        std::cout << "Opened connection to sensor " << id_ << "\n";   // acquire
    }

    ~SensorConnection() {
        std::cout << "Closed connection to sensor " << id_ << "\n";   // release
    }

private:
    int id_;
};

int main() {
    std::cout << "Before block\n";
    {
        SensorConnection sensor(7);
        std::cout << "Using sensor 7\n";
    }   // `sensor` goes out of scope here — the destructor runs automatically
    std::cout << "After block\n";
}
```

This prints:

```
Before block
Opened connection to sensor 7
Using sensor 7
Closed connection to sensor 7
After block
```

Notice what is *not* in `main`: any call to close the connection. The `}` that ends the inner block destroys `sensor`, and destroying it closes the connection. The cleanup is welded to the object's lifetime.

---

## Cleanup that cannot be skipped

The real power is that the destructor runs no matter how control leaves the scope — whether the block finishes normally, returns early, or throws an [exception](../Chapter6/error_handling.md) partway through:

```cpp
void useSensor() {
    SensorConnection sensor(7);

    if (somethingWrong()) {
        return;          // the connection is still closed on the way out
    }
    // ... normal work ...
}                        // and closed here on the normal path too
```

Compare this to cleanup written by hand at the end of a function: an early `return` jumps past it, and a thrown exception jumps past it. RAII has no such gap. Once the object exists, its cleanup is guaranteed.

The exception path even has a name: when a `throw` fires, C++ performs **stack unwinding** — it destroys every local object created so far, in reverse order of construction, on its way out of the scope. `sensor` is among them, so the connection is closed even though execution never reached the end of the function.

> This is why you should prefer an object that owns a resource over a pair of "open it / close it" calls you have to balance yourself. The compiler never forgets to call the destructor; you will.

One further guarantee rounds off the picture: if a **constructor** throws, the object never counts as having existed, and its destructor will not run. Construction either succeeds completely — leaving an object whose cleanup is guaranteed — or fails leaving nothing behind. There is no half-open resource to worry about.

---

## You are already using RAII

You have been relying on RAII since Chapter 1 without naming it. The standard types manage their own resources this way:

- `std::vector` and `std::string` allocate memory and free it in their destructor — you have never called `free`.
- `std::ifstream` and `std::ofstream` open a file and close it in their destructor — you never call `close()` (see [IO & Streams](io_streams.md)).

```cpp
{
    std::ofstream log("readings.txt");
    log << "started\n";
}   // the file is flushed and closed automatically here
```

This is why you rarely need to write a destructor yourself: the right move is almost always to reach for a standard type that already manages the resource, and let it do the work.

---

## RAII and memory

The most important resource is memory. Allocating it by hand (`new`) and freeing it by hand (`delete`) is the classic source of leaks and double-frees. The next chapter's **smart pointers** — `std::unique_ptr` and `std::shared_ptr` — are simply RAII wrappers around memory: they free what they hold when they go out of scope. See [Memory Management](../Chapter5/memory.md).

RAII is also the reason C++ does not need a garbage collector: cleanup is *deterministic*, happening at the exact moment an object dies, not at some unpredictable time later.

It also explains the **Rule of Zero** from the [Classes](classes.md) chapter: if every data member is already an RAII type (a `vector`, a `string`, a smart pointer), your class needs no destructor of its own — the members clean up after themselves.

Here is the rule in one class — a logger whose only member is already an RAII type:

```cpp
class Logger {
public:
    explicit Logger(const std::string& path) : out_(path) {}

    void write(const std::string& line) { out_ << line << '\n'; }

private:
    std::ofstream out_;   // opens in the constructor, closes itself on destruction
};
```

No destructor, no cleanup code, nothing to forget: the `std::ofstream` member owns the file, so the compiler-generated destructor is already correct.

The flip side is the rarer class that owns a *raw* resource directly — one no standard type wraps, like `SensorConnection` above. It cannot lean on the Rule of Zero, and **copying** it is a trap: both copies would own the same connection, and each destructor would release it — a double close. The immediate fix is to forbid copying (`SensorConnection(const SensorConnection&) = delete;`); the full solution is to make the class **move-only**, so the resource is transferred rather than copied. [Designing a movable class](../Chapter5/move.md#designing-a-movable-class) (next chapter) shows how, using this very `SensorConnection`.

---

## Summary

- RAII ties a resource's lifetime to an object: **acquire in the constructor, release in the destructor.**
- The destructor runs automatically when the object goes out of scope — even on an early `return` or an exception (**stack unwinding** destroys locals in reverse order of construction) — so cleanup cannot be forgotten or skipped.
- A constructor that throws leaves nothing behind: no object, no destructor call, no half-open resource.
- You already depend on RAII: `std::vector`, `std::string`, and the file streams all clean up after themselves.
- Prefer a standard RAII type over writing your own destructor (the Rule of Zero). Smart pointers (next chapter) bring RAII to raw memory.
- A class that owns a raw resource must not be blindly copyable — delete its copy operations or make it move-only, so two objects never release the same resource.
- RAII is why C++ manages resources safely and deterministically, without a garbage collector.
