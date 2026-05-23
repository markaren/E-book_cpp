# Observer Pattern

A temperature sensor produces a reading. Several parts of the system care about that reading: a live display, an alarm that trips above a threshold, a logger that records history. The sensor should not have to know about any of them — and certainly should not need editing every time you add one.

The **Observer pattern** solves this. One object (the **subject**) announces when something changes, and any number of interested parties (the **observers**) react — without the subject knowing who they are or what they do. It is [separation of concerns](soc.md) applied to events: the thing that *produces* data does not depend on the things that *consume* it.

This chapter shows the pattern with a small, modern implementation and the one gotcha to watch for.

---

## The problem it solves

Without the pattern, the producer ends up hard-wired to every consumer:

```cpp
void onNewReading(double celsius) {
    updateDisplay(celsius);
    if (celsius > 80.0) {
        soundAlarm();
    }
    logToFile(celsius);
}
```

This works, but the function that produces the reading now knows about the display, the alarm, *and* the log file. Add a fourth consumer — upload the reading to a server — and you must edit this function again. Every consumer is welded to the producer.

What we want instead: the sensor announces "here is a new reading," and whoever is interested reacts on their own.

---

## The idea

- The **subject** is the thing worth watching — here, the sensor. It keeps a list of observers and offers a way to **subscribe**.
- An **observer** is anyone who registered interest. When the subject changes, it notifies every observer on the list.

One subject, many observers — a *one-to-many* relationship where the subject never has to name the observers individually.

---

## A modern implementation

Modern C++ expresses an observer as a **callback**: a function the subject promises to call. A `std::function<void(double)>` can hold anything callable with a `double` — a free function, or most often a [lambda](../lambdas.md) — so the subject keeps a list of them and runs each one whenever a new reading arrives.

Here is the whole thing: a sensor, plus two observers that subscribe to it.

```cpp
#include <functional>
#include <vector>
#include <iostream>

class TemperatureSensor {
public:
    // Register a callback to run on every new reading.
    void subscribe(std::function<void(double)> observer) {
        observers_.push_back(std::move(observer));
    }

    // Called when a fresh reading arrives.
    void setReading(double celsius) {
        reading_ = celsius;
        for (const auto& observer : observers_) {
            observer(celsius);          // notify everyone
        }
    }

    double reading() const { return reading_; }

private:
    double reading_ = 0.0;
    std::vector<std::function<void(double)>> observers_;
};

int main() {
    TemperatureSensor sensor;

    // A live display
    sensor.subscribe([](double t) {
        std::cout << "Display: " << t << " C\n";
    });

    // An alarm that only reacts above a threshold
    sensor.subscribe([](double t) {
        if (t > 80.0) {
            std::cout << "ALARM: too hot!\n";
        }
    });

    sensor.setReading(72.0);   // display fires; alarm stays silent
    sensor.setReading(95.0);   // display fires; alarm fires
}
```

Running this prints:

```
Display: 72 C
Display: 95 C
ALARM: too hot!
```

The sensor knows nothing about displays, alarms, or logs — only that it holds a list of functions to call. `subscribe` adds one; `setReading` calls every one of them in turn. Adding a third observer — say, one that uploads each reading to a server — is just one more `subscribe` call, and the sensor itself never changes.

---

## Watching out for lifetimes

This is the one real hazard. A lambda can [capture](../lambdas.md#captures) variables from around it. If a captured object is destroyed *before* the sensor stops calling the callback, the callback is left referring to something that no longer exists — the same [dangling-reference trap](../Chapter3/types_refs_ptrs.md#the-big-lifetime-trap) from the references chapter.

```cpp
TemperatureSensor sensor;

{
    std::string label = "Reactor core";
    sensor.subscribe([&label](double t) {          // captures label by reference
        std::cout << label << ": " << t << " C\n";
    });
}   // `label` is destroyed here...

sensor.setReading(50.0);   // ...but the callback still refers to it — undefined behaviour
```

Two habits keep you safe:

- **Capture by value** when the callback might outlive the surrounding scope (`[label]` copies it), rather than by reference.
- **Make sure every observer outlives the subject** it subscribed to.

> Capturing by reference (`[&]`) into a callback the subject *stores* is the most common way to create a dangling reference. When in doubt, capture by value.

---

## The classic object-oriented form

You will also meet the Observer pattern written the older "Gang of Four" way: instead of a callback, each observer is an object implementing a shared interface — a direct application of the [polymorphism](../Chapter4/polymorphism.md) you have already seen.

```cpp
class TemperatureObserver {
public:
    virtual ~TemperatureObserver() = default;
    virtual void onReading(double celsius) = 0;
};
```

A `Display`, an `Alarm`, and a `Logger` would each derive from `TemperatureObserver` and override `onReading`. The subject then stores a list of `TemperatureObserver` handles and calls `onReading` on each — the mechanics are identical to the callback version.

The difference is **ownership**. Because polymorphism requires storing observers by pointer or reference (never by value — that would [slice](../Chapter4/polymorphism.md#object-slicing) them), the subject does not own its observers. You must guarantee each one outlives the sensor and is removed before it is destroyed — exactly the bookkeeping the callback version sidesteps.

For new code, prefer the callback form. Reach for the interface form when an observer is already a full-fledged object with several methods, or when a framework you are using expects it.

---

## When to use it

- One source of events, several independent reactions to them (sensor → display, alarm, log).
- You want to add or remove reactions without touching the source.
- The producer should not depend on its consumers.

If there is only ever one consumer, you do not need the pattern — just call it directly. Observer earns its keep when the list of interested parties grows or changes over time.

---

## Summary

- The Observer pattern lets a **subject** notify many **observers** of a change without knowing who they are.
- In modern C++, the simplest form is a list of `std::function` callbacks that observers **subscribe** with — usually lambdas. No manual `attach`/`detach` bookkeeping required.
- It is separation of concerns for events: the producer of data does not depend on its consumers.
- The main hazard is lifetimes — a stored callback that captures by reference can dangle. Capture by value, or ensure observers outlive the subject.
- The classic interface-based form (a virtual `onReading`) is equivalent and reuses polymorphism, but puts the ownership burden back on you.
