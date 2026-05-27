# Version 4: Splitting into a Real Project

[Version 3](v3_pid.md) is complete, but it all lives in one file that keeps growing. That is fine for a sketch and wrong for anything you maintain. Real projects split the code into **headers** (declarations — *what* exists) and **source files** (definitions — *how* it works), organised by component and built with [CMake](../Chapter2/cmake_intro.md). This version reorganises the exact same code into that shape.

---

## The layout

One file per component, headers separated from sources — the convention from [CMake](../Chapter2/cmake_intro.md#a-note-on-project-layout):

```
tank-control/
├── CMakeLists.txt
├── include/
│   ├── tank.hpp
│   ├── valve.hpp
│   ├── sensor.hpp          # Sensor interface + FixedSensor (header-only)
│   ├── level_sensor.hpp
│   ├── controller.hpp      # Controller interface (header-only)
│   ├── pid_controller.hpp
│   └── plant.hpp
└── src/
    ├── main.cpp
    ├── tank.cpp
    ├── valve.cpp
    ├── plant.cpp
    └── pid_controller.cpp
```

---

## Splitting a class

`Tank` shows the pattern. The header **declares** it; short functions (the getter) stay inline, the longer one moves to the source file:

```cpp
// include/tank.hpp
#pragma once

class Tank {
    double level_;
    double area_;
public:
    Tank(double initialLevel, double area);
    void update(double inflow, double outflow, double dt);
    double level() const { return level_; }   // one-liner: fine to leave here
};
```

```cpp
// src/tank.cpp
#include "tank.hpp"

Tank::Tank(double initialLevel, double area)
    : level_(initialLevel), area_(area) {}

void Tank::update(double inflow, double outflow, double dt) {
    level_ += (inflow - outflow) / area_ * dt;
    if (level_ < 0.0) {
        level_ = 0.0;
    }
}
```

The `#pragma once` at the top of the header stops it being pasted in twice. Why the getter stays in the header but `update` moves out — and what it does to compile times — is covered in [Classes](../Chapter4/classes.md#splitting-the-declaration-and-the-implementation).

The **interfaces** (`Sensor`, `Controller`) are pure declarations with no bodies to compile, so they live entirely in headers — no `.cpp` needed. Each remaining class follows the `Tank` pattern:

| Class | Header | Source |
|-------|--------|--------|
| `Tank` | `tank.hpp` | `tank.cpp` |
| `Valve` | `valve.hpp` | `valve.cpp` |
| `Sensor`, `FixedSensor` | `sensor.hpp` | — (header-only) |
| `LevelSensor` | `level_sensor.hpp` | — (one-liner) |
| `Controller` | `controller.hpp` | — (interface) |
| `PIDController` | `pid_controller.hpp` | `pid_controller.cpp` |
| `Plant` | `plant.hpp` | `plant.cpp` |

`main.cpp` includes the headers it needs and is otherwise the loop from Version 3:

```cpp
// src/main.cpp
#include <iostream>
#include "plant.hpp"
#include "level_sensor.hpp"
#include "pid_controller.hpp"

int main() {
    Plant plant(2.0, 1.0, 0.10, 0.03);
    LevelSensor sensor(plant);
    PIDController pid(0.8, 0.05, 0.0, 5.0);
    Controller& controller = pid;

    const double dt = 1.0;
    std::cout << "time,level,setpoint\n";
    for (int step = 0; step < 80; ++step) {
        double measurement = sensor.read();
        double opening     = controller.compute(measurement, dt);
        plant.step(opening, dt);
        std::cout << step << "," << measurement << ",5\n";
    }
}
```

---

## The build file

`CMakeLists.txt` lists the sources, points the compiler at `include/`, fixes the standard at C++20, and turns warnings on for both compiler families — the cross-compiler pattern from [CMake](../Chapter2/cmake_intro.md#turn-on-compiler-warnings):

```cmake
cmake_minimum_required(VERSION 3.16)
project(tank_control)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(tank_control
    src/main.cpp
    src/tank.cpp
    src/valve.cpp
    src/plant.cpp
    src/pid_controller.cpp
)
target_include_directories(tank_control PRIVATE include)

if(MSVC)
    target_compile_options(tank_control PRIVATE /W4)
else()
    target_compile_options(tank_control PRIVATE -Wall -Wextra)
endif()
```

Header-only classes are not listed in `add_executable` — only `.cpp` files are compiled; headers come along through `#include`. Build it the usual way (`cmake -B build && cmake --build build`, or just open the folder in CLion), and the same program runs — now as a project that builds cleanly on Windows, Linux, and macOS. See [Portability](../portability.md).

## What this version shows

- **Declarations vs definitions** — headers say what exists, sources say how. See [Classes](../Chapter4/classes.md#splitting-the-declaration-and-the-implementation).
- **One component per file**, headers in `include/`, sources in `src/`.
- **A real CMake project** — the layout an industrial codebase uses, scaled down. See [CMake](../Chapter2/cmake_intro.md).

---

## Make it your own

You now have a clean skeleton — a plant, a sensor, a controller, and a loop, separated well enough that any one can change without disturbing the others. That is exactly what makes the following additions *additions* rather than rewrites. Pick a few:

**Beginner**

- A high-level **alarm** that warns when the level crosses a limit.
- **Overflow protection** — cap the tank and report when it would have spilled.
- **Sensor noise** — a `NoisyLevelSensor` that adds a small wobble, to see how the controller copes.
- A **manual mode** — a controller that follows a fixed opening you set, ignoring the level.

**Intermediate**

- **Tune the PID** and compare the curves you logged.
- A **second tank**, fed by the first (cascaded levels).
- A **state machine** for the process: *Filling → Holding → Draining → Fault*.
- **Log to a file** with `std::ofstream` instead of the console.

The same plant–sensor–controller–loop skeleton fits other systems too: an **elevator** (with a state machine and a request queue) or a **conveyor sorter** (event-driven, with detectors and actuators) make natural next projects.

You have built, in miniature, the architecture of real control software — and grown it the way real software grows: one motivated step at a time.
