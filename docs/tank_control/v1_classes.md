# Version 1: A Tank, a Valve, and a Loop

Almost all automation software has the same shape: **read the world, decide, act, repeat.** Over four short versions we will build that shape around a problem every automation engineer recognises — keeping the level of a water tank at a target — and grow it into a small but real piece of control software.

This is a *worked example*, not new language material. It assumes you have read Chapters 1–6; each version points back to where its ideas are taught. Read it, type it, run it, then take it further with the [project ideas](v4_project.md#make-it-your-own) at the end.

The physical system and its software counterparts — this direct mapping is what makes object-oriented code feel useful rather than abstract:

| Physical part | C++ class |
|---------------|-----------|
| The water tank | `Tank` |
| The inlet valve | `Valve` |
| The level controller | `OnOffController` |

This version introduces the three as plain [classes](../Chapter4/classes.md) and wires them together in a **simulation loop**.

---

## The tank

A tank holds water; its level rises with inflow and falls with outflow. We keep the level **private** so the outside world can read it and step it forward in time, but never scribble on it directly — that is [encapsulation](../Chapter4/classes.md).

<!-- no-ce -->
```cpp
class Tank {
    double level_;   // metres of water
    double area_;    // m², the tank's footprint
public:
    Tank(double initialLevel, double area)
        : level_(initialLevel), area_(area) {}

    // Advance the level by one step of dt seconds.
    void update(double inflow, double outflow, double dt) {
        level_ += (inflow - outflow) / area_ * dt;
        if (level_ < 0.0) {
            level_ = 0.0;   // a tank cannot hold less than nothing
        }
    }

    double level() const { return level_; }
};
```

The physics is one line: the level changes by the *net* flow (in minus out), spread over the tank's area, across the time step. The clamp keeps the simulation honest.

---

## The valve

The inlet valve controls how much water flows in. Its opening runs from `0.0` (shut) to `1.0` (fully open):

<!-- no-ce -->
```cpp
class Valve {
    double opening_ = 0.0;   // 0.0 = shut, 1.0 = fully open
public:
    void setOpening(double fraction) {
        if (fraction < 0.0) { fraction = 0.0; }
        if (fraction > 1.0) { fraction = 1.0; }
        opening_ = fraction;
    }

    // The flow through the valve, given the flow when fully open.
    double flow(double maxFlow) const { return opening_ * maxFlow; }
};
```

`setOpening` refuses nonsense values — another small invariant the class protects on its own.

---

## The controller

The simplest controller there is: if we are below target, open the valve; otherwise shut it. This is **on/off** (bang-bang) control — what a basic thermostat does.

<!-- no-ce -->
```cpp
class OnOffController {
    double setpoint_;
public:
    explicit OnOffController(double setpoint) : setpoint_(setpoint) {}

    // Given the measured level, return the valve opening to use.
    double compute(double level) const {
        return (level < setpoint_) ? 1.0 : 0.0;
    }
};
```

---

## The simulation loop

Here is the part that makes it automation. Each step we **sense** the level, **decide** the valve opening, **act** by setting the valve, and **step** time forward:

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    Tank tank(2.0, 1.0);              // start at 2 m, 1 m² footprint
    Valve inlet;
    OnOffController controller(5.0);  // hold the level at 5 m

    const double maxInflow = 0.10;    // m³/s with the valve fully open
    const double outflow   = 0.03;    // m³/s drawn off by the process
    const double dt        = 1.0;     // seconds per step

    for (int step = 0; step < 60; ++step) {
        double level   = tank.level();               // sense
        double opening = controller.compute(level);  // decide
        inlet.setOpening(opening);                   // act
        tank.update(inlet.flow(maxInflow), outflow, dt);  // step the world forward

        std::cout << "t=" << step << "s  level=" << level << " m\n";
    }
}
```

Run it and watch the level climb from 2 m: while it is below 5 m the valve is wide open, so the level rises by the net flow (`0.10 − 0.03 = 0.07` m per step). The moment it crosses 5 m the valve slams shut, the level falls by `0.03` m per step, drops back below 5 m, and the valve slams open again. The level **chatters** around the setpoint forever. That endless on/off switching is the classic weakness of bang-bang control — and the reason [Version 3](v3_pid.md) reaches for a PID controller.

---

## What this version shows

- **Encapsulation** — `Tank` owns `level_`; the loop reads it and steps it, but never assigns it. See [Classes](../Chapter4/classes.md).
- **One job per object** — tank, valve, controller. The loop is the only place that knows about all three.
- **The control loop** — *sense → decide → act → step* is the heartbeat of every PLC scan cycle, real-time controller, and digital twin. See [Control Statements](../Chapter1/control_statements.md).

## What's still awkward → Version 2

The controller reads the level straight out of the tank: `controller.compute(tank.level())`. Real systems read it through a **sensor**, which can be noisy, can be one of several types, and which you will want to replace with a stand-in when [testing](../Chapter6/testing.md). Hard-wiring `tank.level()` makes none of that possible. [Version 2](v2_sensors.md) puts a `Sensor` interface in the middle and lets *polymorphism* decouple the controller from where the reading comes from.
