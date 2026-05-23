# RAII

Every program uses resources that have to be handed back: memory that must be freed, files that must be closed, device connections that must be released. Forget to release one and you get a *leak*; release it twice and you corrupt something. Remembering to clean up by hand, on every path through your code, is exactly the kind of bookkeeping humans get wrong.

C++'s answer is **RAII** — *Resource Acquisition Is Initialization*, an awkward name for a simple idea: tie a resource to the lifetime of an object, so cleanup happens **automatically** when the object goes out of scope. It is the foundation almost all modern C++ rests on.

---

## The destructor

A constructor runs when an object is created. Its mirror image, the **destructor**, runs automatically when the object is destroyed — which, for a local variable, is the moment it goes out of scope. A destructor is named `~` followed by the class name, takes no arguments, and you never call it yourself; the compiler inserts the call for you.

RAII is just this: **acquire the resource in the constructor, release it in the destructor.**

```cpp
#include <iostream>

class SensorConnection {
public:
    SensorConnection(int id) : id_(id) {
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

> This is why you should prefer an object that owns a resource over a pair of "open it / close it" calls you have to balance yourself. The compiler never forgets to call the destructor; you will.

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

---

## Summary

- RAII ties a resource's lifetime to an object: **acquire in the constructor, release in the destructor.**
- The destructor runs automatically when the object goes out of scope — even on an early `return` or an exception — so cleanup cannot be forgotten or skipped.
- You already depend on RAII: `std::vector`, `std::string`, and the file streams all clean up after themselves.
- Prefer a standard RAII type over writing your own destructor. Smart pointers (next chapter) bring RAII to raw memory.
- RAII is why C++ manages resources safely and deterministically, without a garbage collector.
