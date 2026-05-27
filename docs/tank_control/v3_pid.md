# Version 3: A PID Controller, Composition, and Logging

[Version 2](v2_sensors.md) left two things nagging: `main` was juggling every component and a pile of loose constants, and on/off control still chatters. This version fixes both. It bundles the hardware into a **`Plant`** (composition), keeps the controller cleanly separate (separation of concerns), and replaces bang-bang control with a **PID controller** — made swappable through the same interface trick you used for sensors.

It reuses `Tank`, `Valve`, and the `Sensor` interface unchanged from the earlier versions.

---

## A plant: composition

A real system groups its physical kit together. A `Plant` **has a** tank and **has a** valve — it does not *inherit* from them; it *contains* them. That is [composition](../Chapter5/polymorphism.md#composition-over-inheritance):

<!-- no-ce -->
```cpp
class Plant {
    Tank tank_;
    Valve inlet_;
    double maxInflow_;
    double outflow_;
public:
    Plant(double initialLevel, double area, double maxInflow, double outflow)
        : tank_(initialLevel, area), maxInflow_(maxInflow), outflow_(outflow) {}

    // Apply a valve opening (0..1) and let one time step pass.
    void step(double valveOpening, double dt) {
        inlet_.setOpening(valveOpening);
        tank_.update(inlet_.flow(maxInflow_), outflow_, dt);
    }

    double level() const { return tank_.level(); }
};
```

`Plant` now exposes exactly two things — *give it a valve opening and a time step* (`step`) and *what is the level* (`level`). The tank and valve are sealed inside. The sensor reads the plant:

<!-- no-ce -->
```cpp
class LevelSensor : public Sensor {
    const Plant& plant_;
public:
    explicit LevelSensor(const Plant& plant) : plant_(plant) {}

    double read() const override { return plant_.level(); }
};
```

---

## A controller interface

You met polymorphism for sensors; the same move makes controllers interchangeable. A `Controller` promises one thing — turn a measurement into a valve opening:

<!-- no-ce -->
```cpp
class Controller {
public:
    virtual ~Controller() = default;
    // Given the latest measurement and the time step, return a valve opening (0..1).
    virtual double compute(double measurement, double dt) = 0;
};
```

The on/off controller from Version 1 becomes one implementation (it simply ignores `dt`):

<!-- no-ce -->
```cpp
class OnOffController : public Controller {
    double setpoint_;
public:
    explicit OnOffController(double setpoint) : setpoint_(setpoint) {}

    double compute(double measurement, double /*dt*/) override {
        return (measurement < setpoint_) ? 1.0 : 0.0;
    }
};
```

## The PID controller

A PID controller steers smoothly by combining three terms: the **P**roportional (how far off we are now), the **I**ntegral (how much error has built up over time), and the **D**erivative (how fast the error is changing):

<!-- no-ce -->
```cpp
class PIDController : public Controller {
    double kp_, ki_, kd_;
    double setpoint_;
    double integral_ = 0.0;
    double previousError_ = 0.0;
public:
    PIDController(double kp, double ki, double kd, double setpoint)
        : kp_(kp), ki_(ki), kd_(kd), setpoint_(setpoint) {}

    double compute(double measurement, double dt) override {
        double error = setpoint_ - measurement;
        integral_ += error * dt;
        double derivative = (error - previousError_) / dt;
        previousError_ = error;

        double output = kp_ * error + ki_ * integral_ + kd_ * derivative;
        if (output < 0.0) { output = 0.0; }   // a valve cannot open less than shut
        if (output > 1.0) { output = 1.0; }   // ...or more than fully open
        return output;
    }
};
```

The gains `kp_`, `ki_`, `kd_` are kept as private state, along with the running `integral_` and the last error. (Tuning those gains well is an engineering field of its own; the values below are just sensible starting numbers.)

---

## Putting it together, with logging

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    Plant plant(2.0, 1.0, 0.10, 0.03);
    LevelSensor sensor(plant);

    PIDController pid(0.8, 0.05, 0.0, 5.0);   // Kp, Ki, Kd, setpoint = 5 m
    Controller& controller = pid;             // swap in OnOffController and nothing else changes

    const double dt = 1.0;

    std::cout << "time,level,setpoint\n";      // CSV header
    for (int step = 0; step < 80; ++step) {
        double measurement = sensor.read();                    // sense
        double opening     = controller.compute(measurement, dt);  // decide
        plant.step(opening, dt);                               // act + step

        std::cout << step << "," << measurement << ",5\n";     // log a row
    }
}
```

Run it and the level rises and **settles** at 5 m instead of chattering: as it nears the setpoint the PID eases the valve toward the ~30% opening that exactly matches the outflow, and the integral term trims away the last bit of offset. That is the difference between bang-bang and proportional control, on your screen.

The output is **CSV** — `time,level,setpoint` — so you can redirect it to a file (`./tank_control > run.csv`) and open it in a spreadsheet to plot the curve. To write the file from inside the program instead, swap `std::cout` for a `std::ofstream`; see [IO & Streams](../Chapter4/io_streams.md).

---

## What this version shows

- **Composition** — `Plant` *has a* `Tank` and a `Valve`; it owns them and exposes a small interface. See [Composition over inheritance](../Chapter5/polymorphism.md#composition-over-inheritance).
- **Separation of concerns** — the plant knows physics, the controller knows control, the sensor knows measurement. None reaches into another. See [Separation of Concerns](../Chapter6/soc.md).
- **Polymorphism, again** — the loop runs against a `Controller&`, so on/off and PID are drop-in swaps. See [Polymorphism](../Chapter5/polymorphism.md).
- **A real control law** — PID is what actually runs in pumps, ovens, drones, and process plants.

## What's still awkward → Version 4

Everything now lives in one steadily growing file. Real projects split into headers and source files, organised by component and built with CMake. [Version 4](v4_project.md) does exactly that — turning this example into a project laid out the way an industrial one would be.
