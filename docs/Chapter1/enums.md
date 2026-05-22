# Enumerations

Some values come from a small, fixed set of named options. A motor is *idle*, *running*, *stopped*, or in *fault*. A traffic light is *red*, *amber*, or *green*. A command is *start*, *stop*, or *reset*.

You *could* store these as plain `int`s — `0` for idle, `1` for running, and so on — but then nothing stops you writing `state = 99`, and every reader has to remember what `1` is supposed to mean. An **enumeration** is a type whose values are a fixed set of names you choose. It makes the options explicit, readable, and checkable by the compiler.

---

## `enum class` — the one to use

Define a scoped enumeration with `enum class`:

```cpp
enum class MotorState {
    Idle,
    Running,
    Stopped,
    Fault
};
```

`MotorState` is now a type, just like `int` or `bool`, and its only values are the four names you listed. You write a value by qualifying it with the type name:

```cpp
MotorState state = MotorState::Idle;

state = MotorState::Running;

if (state == MotorState::Running) {
    // ...
}
```

The `MotorState::` prefix is required. It is a little extra typing, but it means `Running` belongs to `MotorState` and cannot collide with a `Running` defined anywhere else.

---

## Switching on an enum

An enum's natural partner is a [`switch`](control_statements.md): one branch per value.

```cpp
#include <iostream>

enum class MotorState {
    Idle,
    Running,
    Stopped,
    Fault
};

void report(MotorState state) {
    switch (state) {
        case MotorState::Idle:    std::cout << "Motor is idle\n";    break;
        case MotorState::Running: std::cout << "Motor is running\n"; break;
        case MotorState::Stopped: std::cout << "Motor is stopped\n"; break;
        case MotorState::Fault:   std::cout << "Motor fault!\n";     break;
    }
}

int main() {
    MotorState state = MotorState::Idle;
    report(state);

    state = MotorState::Running;
    report(state);

    state = MotorState::Fault;
    report(state);
}
```

Output:

```
Motor is idle
Motor is running
Motor fault!
```

There is a real payoff here. If you leave the `default` case off and later add a fifth state, the compiler — with warnings on (`-Wall`) — points straight at this `switch` and tells you a case is unhandled. That turns "I forgot to update one place" into a build-time reminder, which is exactly why you should leave `default` off a `switch` over an enum.

---

## Why `enum class` and not plain `enum`

You will also meet the older, unscoped form — just `enum`:

```cpp
enum MotorState { Idle, Running, Stopped, Fault };   // unscoped — avoid in new code
```

It has two traps that `enum class` closes:

| | plain `enum` | `enum class` |
|---|--------------|--------------|
| **Names** | leak into the surrounding scope: you write `Idle` bare, and it clashes with any other `Idle` nearby | stay scoped: always `MotorState::Idle` |
| **Type safety** | convert to `int` silently, so `int x = Running;` and `state == 1` both compile | no silent conversion: mixing with `int` is a compile error |

The silent `int` conversion is the dangerous one. With a plain `enum`, comparing two unrelated enums, or storing an out-of-range number, compiles without complaint. `enum class` turns those mistakes into compile errors. **Default to `enum class`.**

---

## The numbers behind the names

Each name has an integer value: `0, 1, 2, …` in declaration order by default. You can set them yourself when the numbers carry meaning — status codes, or values that must match a hardware register:

```cpp
enum class ErrorCode {
    Ok       = 0,
    Timeout  = 4,
    Overheat = 8
};
```

A scoped enum does **not** turn into that integer on its own. When you genuinely need the number — to print it, or to send it to another system — ask for it explicitly with [`static_cast`](operators_expressions.md):

```cpp
ErrorCode code = ErrorCode::Overheat;
int raw = static_cast<int>(code);   // 8
```

> On a microcontroller, where every byte counts, you can pin the size of an enum by naming its underlying type: `enum class ErrorCode : std::uint8_t { ... };` (needs `<cstdint>`). You will not need this on the desktop.

---

## Printing an enum

There is no built-in way to print an `enum class`. `std::cout << state` does **not** compile — at runtime an enum is just a number, and the compiler has no text for the names you chose.

You have already seen one fix: a `switch` that prints a message per value (the `report` function above). When you instead want the name *as a string* — to put in a log message or build up text — write a small `toString`:

```cpp
#include <iostream>
#include <string>

enum class MotorState {
    Idle,
    Running,
    Stopped,
    Fault
};

std::string toString(MotorState state) {
    switch (state) {
        case MotorState::Idle:    return "Idle";
        case MotorState::Running: return "Running";
        case MotorState::Stopped: return "Stopped";
        case MotorState::Fault:   return "Fault";
    }
    return "Unknown";
}

int main() {
    MotorState state = MotorState::Running;
    std::cout << "Motor state: " << toString(state) << "\n";
}
```

Two things about that function:

- The trailing `return "Unknown";` is needed because `toString` must return a `std::string` on *every* path, and the compiler does not treat the four cases as covering all possibilities — an `enum class` can technically hold any value of its underlying type.
- There is deliberately no `default` case. As before, that lets the compiler warn you if you add a fifth state later and forget to give it a name here.

Keeping this in step with the enum by hand is a little tedious — C++20 has no automatic enum-to-string — but a plain `switch` is the dependable, dependency-free way to do it.

---

## Summary

- An enum is a type with a fixed set of named values — reach for one whenever you would otherwise use "magic" `int`s for states, modes, or options.
- **Prefer `enum class`** (scoped and type-safe) over plain `enum`.
- Write values as `Type::Value`, compare them with `==`, and branch on them with `switch`.
- Leave `default` off a `switch` over an enum so the compiler warns you about values you forgot to handle.
- An `enum class` never converts to `int` by itself — use `static_cast` when you really mean to.
- There is no built-in way to print an enum's name — write a small `toString` `switch` for that.
