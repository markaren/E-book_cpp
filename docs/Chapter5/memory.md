# Memory Management

Every value in a C++ program lives somewhere in memory. Most of the time you do not have to think about *where*: the language and compiler handle it for you. But automation code talks to hardware, builds long-lived state machines, and runs for hours; getting memory management wrong here causes real bugs that real users will see.

This chapter walks through the two places values can live (the **stack** and the **heap**), the old C-style way of managing dynamic memory (`new` / `delete`), why it is dangerous, and the modern tools (**smart pointers**) that make it safe again.

---

## Stack vs. heap

Two regions of memory matter to a programmer:

| | Stack | Heap |
|---|-------|------|
| **Allocation** | Automatic; happens when a variable is declared | Manual; you ask for it with `new` (or, better, a smart pointer) |
| **Deallocation** | Automatic; when the variable goes out of scope | Manual; you must release it (or let a smart pointer do it) |
| **Speed** | Very fast; just bump a pointer | Slower; needs a real allocator |
| **Size** | Small (typically a few MB total per thread) | Large (limited by available RAM) |
| **Lifetime** | Tied to the enclosing block | Lives until explicitly freed |

The single most important rule:

> **Prefer the stack.** Only use the heap when the stack will not work.

The stack works as long as:

- the size of the data is known at compile time, and
- the data does not need to outlive the function that created it.

When either condition fails (a vector that grows at runtime, an object that needs to survive the function that built it, an array whose size depends on a sensor reading), you use the heap.

### Stack example

```cpp
#include <iostream>

void demo() {
    int  count = 42;       // on the stack
    double pi    = 3.14;   // on the stack
    std::cout << count << " " << pi << "\n";
}   // both variables destroyed automatically here
```

Nothing to clean up. Each local variable is created when the function is entered and destroyed when the function returns. This is the easy, fast, correct default.

### Heap example (the C way, do not write code like this)

```cpp
#include <iostream>

int main() {
    int* heapInt = new int(42);          // allocate on the heap
    std::cout << *heapInt << "\n";       // dereference to read the value
    delete heapInt;                      // release the memory, required!
    return 0;
}
```

The pointer and the value it points to live in different places — the pointer on the stack, the `int` it was handed on the heap:

```text
   STACK (freed automatically)        HEAP (you must free it)

       heapInt  ●───────────────────────►  [ 42 ]
```

`new` allocates memory on the heap and returns a pointer to it. `delete` releases the memory. You must call `delete` exactly once for every `new`, no matter what, including when an exception is thrown halfway through your function.

This is harder than it sounds.

---

## Why raw `new` / `delete` is dangerous

Three kinds of bug haunt every C codebase and every C++ codebase that uses raw `new` / `delete`:

**1. Memory leaks.** Forget to `delete` and the memory is gone for the lifetime of the program.

```cpp
void process() {
    int* data = new int[1000];
    if (somethingFailed()) {
        return;            // leak, `data` is never freed
    }
    delete[] data;
}
```

**2. Use-after-free.** Use a pointer after the memory has been freed and you get undefined behaviour: usually a crash, sometimes silent data corruption.

```cpp
int* p = new int(5);
delete p;
std::cout << *p << "\n";   // undefined behaviour
```

**3. Double-free.** Calling `delete` twice on the same pointer is also undefined behaviour.

```cpp
int* p = new int(5);
delete p;
delete p;                  // undefined behaviour
```

Every one of these is invisible in the source code; nothing tells the reader "this pointer has already been freed." They show up at runtime, often in production, often after a long random delay.

---

## The trap: classes that own raw pointers

A common beginner pattern: a class allocates something with `new` in its constructor and frees it in its destructor.

```cpp
class Buffer {
public:
    explicit Buffer(int size) : data_(new int[size]) {}
    ~Buffer()        { delete[] data_; }

    int* data() { return data_; }

private:
    int* data_;
};
```

This looks reasonable. It is broken.

Watch what happens when you copy a `Buffer`:

```cpp
Buffer a(100);
Buffer b = a;     // copies the pointer, not the underlying memory
// `a.data_` and `b.data_` now point at the SAME array
```

```text
   STACK                         HEAP

   a.data_  ●─────────┐
                      ├────────►  [  the one int array  ]
   b.data_  ●─────────┘
```

When `a` and `b` are destroyed, the same array is `delete[]`d twice. That is undefined behaviour. The default copy that C++ provides is a shallow copy: it copies the *pointer*, not what the pointer points to.

The classical fix (implementing a copy constructor, a copy assignment operator, and a destructor that all agree on ownership) is called the **Rule of Three**, or in modern C++ the **Rule of Five**, which adds move operations. It is correct, but it is also a lot of error-prone code for what should be a simple type.

There is a better answer: **don't own raw pointers**.

---

## Smart pointers

A **smart pointer** is a small class that owns a pointer and automatically deletes it when the smart pointer itself goes out of scope. It is RAII applied to dynamic memory.

The C++ standard library provides three, all in `<memory>`:

| Type                | Ownership | When to use |
|---------------------|-----------|-------------|
| `std::unique_ptr<T>` | Exactly one owner | Almost always |
| `std::shared_ptr<T>` | Multiple co-owners, counted | When ownership genuinely is shared |
| `std::weak_ptr<T>`   | Non-owning observer of a `shared_ptr` | Break reference cycles |

### `std::unique_ptr`: the default

```cpp
#include <iostream>
#include <memory>

class Motor {
public:
    explicit Motor(int id) : id_(id) {
        std::cout << "Motor " << id_ << " constructed\n";
    }
    ~Motor() {
        std::cout << "Motor " << id_ << " destroyed\n";
    }
    void spin() { std::cout << "Motor " << id_ << " spinning\n"; }
private:
    int id_;
};

int main() {
    std::unique_ptr<Motor> m = std::make_unique<Motor>(7);
    m->spin();
    // No delete needed, m's destructor releases the Motor automatically
    return 0;
}
```

Output:

```
Motor 7 constructed
Motor 7 spinning
Motor 7 destroyed
```

`std::make_unique<Motor>(7)` allocates a `Motor` on the heap and hands the pointer to a `unique_ptr` that owns it. When `m` goes out of scope, its destructor runs and the `Motor` is destroyed. No leaks, no use-after-free, no double-delete.

A `unique_ptr` cannot be copied (that would create a second owner), but it can be **moved**:

```cpp
std::unique_ptr<Motor> a = std::make_unique<Motor>(1);
std::unique_ptr<Motor> b = std::move(a);   // ownership transferred to b
// a is now empty (nullptr); b owns the Motor
```

(More on `std::move` in the [next chapter](move.md).)

### `std::shared_ptr`: shared ownership

When several parts of your program legitimately share ownership of one object (and none of them can decide alone when it should be destroyed), use `std::shared_ptr`. It keeps a reference count and deletes the object when the last `shared_ptr` to it goes away.

```cpp
#include <memory>
#include <vector>

void demo() {
    auto motor = std::make_shared<Motor>(42);

    std::vector<std::shared_ptr<Motor>> subscribers;
    subscribers.push_back(motor);    // reference count: 2
    subscribers.push_back(motor);    // reference count: 3

    // Motor is destroyed only after `motor` and both copies in
    // `subscribers` are all gone.
}
```

`shared_ptr` is more expensive than `unique_ptr` (the reference count has to be maintained, atomically, across threads). Reach for it only when shared ownership is really what you need.

### `std::weak_ptr`: non-owning observer

Two `shared_ptr`s that point at each other will keep each other alive forever (a **reference cycle**, and a leak). `std::weak_ptr` is a pointer that can observe a `shared_ptr` without contributing to its reference count, which is how you break such cycles. You will see this in graph and parent/child structures; it is not something to worry about on day one.

---

## The Rule of Zero

Now reconsider the `Buffer` class from earlier, written with a `unique_ptr` instead of a raw pointer:

```cpp
class Buffer {
public:
    explicit Buffer(int size) : data_(std::make_unique<int[]>(size)) {}

    int* data() { return data_.get(); }

private:
    std::unique_ptr<int[]> data_;
};
```

No destructor. No copy constructor. No assignment operator. The compiler-generated defaults are correct, because `unique_ptr` already knows how to manage its memory. It also forbids copying, which is exactly the behaviour we want.

This is the **Rule of Zero**: if all of your class's members manage their own lifetime (via RAII), you do not have to write *any* special member functions. Most well-designed C++ classes are written this way.

Practically: when you find yourself reaching for `new` and `delete`, stop and ask whether `std::vector`, `std::string`, or `std::unique_ptr` already does what you need.

---

## Best practices

- **Prefer the stack.** Use the heap only when the stack will not work.
- **Never write `new` or `delete` in modern C++.** Use `std::make_unique` and `std::make_shared`.
- **Default to `unique_ptr`.** Only use `shared_ptr` when ownership is genuinely shared.
- **Use standard containers** (`std::vector`, `std::string`) instead of hand-rolled dynamic arrays.
- **Aim for the Rule of Zero.** If you do need to write your own special members, write all of them (Rule of Five).
- **Smart pointers are not garbage collection.** They are deterministic: destruction happens at a known, predictable point. This is a feature, especially for embedded code.

---

## Summary

The heap is necessary, but raw heap management is error-prone enough that experienced C++ programmers avoid writing `new` and `delete` directly. Smart pointers and standard containers give you the same capabilities with automatic cleanup, exception safety, and clear ownership semantics. Start with the stack; reach for `std::unique_ptr` when you must; reach for `std::shared_ptr` only when ownership is really shared.
