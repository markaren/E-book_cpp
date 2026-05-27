# Version 2: Sensors and Polymorphism

In [Version 1](v1_classes.md) the controller read the tank directly:

<!-- no-ce -->
```cpp
double opening = controller.compute(tank.level());
```

That hides an assumption: *the level always comes from this tank, exactly.* Reality is messier — the reading comes from a **sensor** that might be one of several types, and when you [test](../Chapter6/testing.md) the controller you will want to feed it readings from a stand-in instead of a real tank. The fix is to depend on an **interface** rather than a concrete source. That is what [polymorphism](../Chapter5/polymorphism.md) is for.

---

## A sensor interface

<!-- no-ce -->
```cpp
class Sensor {
public:
    virtual ~Sensor() = default;
    virtual double read() const = 0;   // pure virtual: every sensor must provide this
};
```

`Sensor` is an **abstract class**: it has no `read()` of its own, only the *promise* that every sensor has one. You cannot create a bare `Sensor` — you create one of its concrete kinds. The `virtual` destructor is the rule for any class meant to be inherited from.

---

## Two kinds of sensor

A real sensor reports the tank's actual level. It holds a **reference** to the tank it watches:

<!-- no-ce -->
```cpp
class LevelSensor : public Sensor {
    const Tank& tank_;
public:
    explicit LevelSensor(const Tank& tank) : tank_(tank) {}

    double read() const override { return tank_.level(); }
};
```

A second kind reports a fixed value, with no tank at all — exactly what you want when testing a controller in isolation:

<!-- no-ce -->
```cpp
class FixedSensor : public Sensor {
    double value_;
public:
    explicit FixedSensor(double value) : value_(value) {}

    double read() const override { return value_; }
};
```

Both say `override`, because both replace the `Sensor`'s promised `read()`. The `const Tank&` member is a deliberate choice from [Values, References & Pointers](../Chapter4/types_refs_ptrs.md): the sensor *observes* the tank, it does not own or copy it.

---

## Programming to the interface

Any code that needs a reading takes a `Sensor&` and stops caring which kind it got:

<!-- no-ce -->
```cpp
// Works with ANY sensor — it knows only the Sensor interface.
void report(const Sensor& sensor) {
    std::cout << "level reads " << sensor.read() << " m\n";
}
```

`report(realSensor)` and `report(fakeSensor)` both compile and both run — the function never changes. That is the whole point of the interface.

The simulation loop does the same: it reaches the level through a `Sensor&`, so the source is now a single line you can change.

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    Tank tank(2.0, 1.0);
    Valve inlet;
    OnOffController controller(5.0);

    LevelSensor levelSensor(tank);
    Sensor& sensor = levelSensor;     // refer to it through the interface
    // FixedSensor fake(4.0);         // ...or, to test the controller alone:
    // Sensor& sensor = fake;

    const double maxInflow = 0.10;
    const double outflow   = 0.03;
    const double dt        = 1.0;

    for (int step = 0; step < 60; ++step) {
        double reading = sensor.read();                  // sense (through the interface)
        inlet.setOpening(controller.compute(reading));   // decide + act
        tank.update(inlet.flow(maxInflow), outflow, dt); // step
    }
}
```

Swap the two commented lines in for the two above them and the controller now runs against a fake reading of `4.0` m — with no tank and no change to the loop. When the call `sensor.read()` runs the *right* `read()` for the object it actually points at, that is **runtime polymorphism** in action.

---

## What this version shows

- **Abstraction / interfaces** — `Sensor` defines *what* a sensor does; `LevelSensor` and `FixedSensor` decide *how*. See [Polymorphism](../Chapter5/polymorphism.md).
- **Pure virtual functions and `override`** — the mechanics that make the swap work.
- **Depend on interfaces, not concrete types** — the controller and loop work with any `Sensor`, which is what makes the system testable and extensible.

## What's still awkward → Version 3

Two things nag now. First, `main` is juggling a tank, a valve, a sensor, a controller, and a fistful of loose constants — the "plant" (the physical kit) and the controller are tangled together. Second, on/off control still chatters. [Version 3](v3_pid.md) bundles the hardware into a `Plant` (composition), keeps the controller cleanly separate (separation of concerns), and swaps the bang-bang logic for a **PID controller** — itself made swappable through the same interface trick you just learned.
