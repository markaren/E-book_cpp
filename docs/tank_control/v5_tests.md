# Version 5: Tests

[Version 4](v4_project.md) builds and runs, but nothing proves it is *correct*. A real project guards its parts with **tests** — small programs that call your code with known inputs and check the outputs. This version adds a test suite with Catch2 (from [Testing](../Chapter6/testing.md)), and uses the moment to lay the project out the grown-up way: because there are now two things to build — the application *and* the tests, both using the same components — the build itself splits across folders.

---

## A library to share

In Version 4 the components were compiled straight into the application. To run them under test *as well*, compile them once into a **library** that both the app and the tests link — the pattern from [Building libraries](../Chapter2/cmake_intro.md#building-libraries). The tests then exercise the very same code the program runs, not a copy.

## The layout grows a `tests/` folder

Each folder gets its own `CMakeLists.txt`; the top-level file just wires them together with [`add_subdirectory`](../Chapter2/cmake_intro.md#splitting-the-build-across-folders):

```
tank-control/
├── CMakeLists.txt          # top level — wires the folders together
├── include/                # the headers (unchanged from Version 4)
│   └── ...
├── src/                    # the components, built as a library
│   ├── CMakeLists.txt
│   ├── tank.cpp
│   ├── valve.cpp
│   ├── plant.cpp
│   └── pid_controller.cpp
├── app/                    # the application
│   ├── CMakeLists.txt
│   └── main.cpp
└── tests/
    ├── CMakeLists.txt      # builds the test runner
    └── test_tank.cpp
```

## Wiring it together

The top-level file is now a short table of contents:

```cmake
# CMakeLists.txt (top level)
cmake_minimum_required(VERSION 3.16)
project(tank_control)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(src)      # the components, as a library
add_subdirectory(app)      # the application
add_subdirectory(tests)    # the tests
```

`src/` compiles the components once into a library, `tank_lib`:

```cmake
# src/CMakeLists.txt
add_library(tank_lib
    tank.cpp
    valve.cpp
    plant.cpp
    pid_controller.cpp
)
target_include_directories(tank_lib PUBLIC ${CMAKE_SOURCE_DIR}/include)

if(MSVC)
    target_compile_options(tank_lib PRIVATE /W4)
else()
    target_compile_options(tank_lib PRIVATE -Wall -Wextra)
endif()
```

`app/` is a thin consumer — just the application, linked against the library:

```cmake
# app/CMakeLists.txt
add_executable(tank_control main.cpp)
target_link_libraries(tank_control PRIVATE tank_lib)
```

Because `tank_lib`'s include directory is `PUBLIC`, everything that links it — the app *and* the tests — inherits the path to `include/` automatically.

`tests/` fetches Catch2 and builds a test runner that links the same library:

```cmake
# tests/CMakeLists.txt
include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

add_executable(tests test_tank.cpp)
target_link_libraries(tests PRIVATE tank_lib Catch2::Catch2WithMain)
```

---

## The tests

Each component is a small, pure piece of logic, which is exactly what makes it easy to check in isolation. The quantities each test sets up are **named**, and every expected value is a short calculation you can follow in the comment beside it — no bare "magic numbers" to reverse-engineer. Levels and valve openings are floating-point, so the tests compare with `Approx` rather than `==` — see [Floating-Point Pitfalls](../floating_point.md).

<!-- no-ce -->
```cpp
// tests/test_tank.cpp
#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>

#include "tank.hpp"
#include "valve.hpp"
#include "pid_controller.hpp"

using Catch::Approx;

TEST_CASE("Tank integrates net flow over a step") {
    const double area    = 1.0;   // m²
    const double inflow  = 0.5;   // m³/s in
    const double outflow = 0.2;   // m³/s out

    Tank tank(2.0, area);                 // starts at 2 m
    tank.update(inflow, outflow, 1.0);    // one 1-second step

    // level += (inflow - outflow) / area × dt  →  2.0 + 0.3
    REQUIRE(tank.level() == Approx(2.3));
}

TEST_CASE("Tank level never goes negative") {
    Tank tank(0.0, 1.0);
    tank.update(0.0, 5.0, 1.0);           // drained far past empty
    REQUIRE(tank.level() == Approx(0.0));
}

TEST_CASE("Valve clamps its opening to 0..1") {
    const double maxFlow = 2.0;           // flow when fully open
    Valve valve;

    valve.setOpening(1.5);                             // above 1 → clamps fully open
    REQUIRE(valve.flow(maxFlow) == Approx(maxFlow));

    valve.setOpening(-0.5);                            // below 0 → clamps shut
    REQUIRE(valve.flow(maxFlow) == Approx(0.0));

    valve.setOpening(0.25);                            // in range → passes through
    REQUIRE(valve.flow(maxFlow) == Approx(0.5));       // 0.25 × 2.0
}

TEST_CASE("PID opens the valve in proportion to the error") {
    const double setpoint = 5.0;
    const double kp       = 0.5;
    PIDController pid(kp, 0.0, 0.0, setpoint);          // P-only: Kp = kp, no I or D

    const double measured = 4.0;                        // 1 m below setpoint
    REQUIRE(pid.compute(measured, 1.0) == Approx(0.5)); // error 1 × kp 0.5
}

TEST_CASE("PID clamps its output to the valve's 0..1 range") {
    const double setpoint = 5.0;
    PIDController pid(10.0, 0.0, 0.0, setpoint);         // gain large enough to saturate

    REQUIRE(pid.compute(0.0,  1.0) == Approx(1.0));     // far below setpoint → fully open
    REQUIRE(pid.compute(10.0, 1.0) == Approx(0.0));     // far above setpoint → shut
}

TEST_CASE("PID integral accumulates over repeated steps") {
    const double setpoint = 5.0;
    const double ki       = 0.1;
    PIDController pid(0.0, ki, 0.0, setpoint);          // I-only: Ki = ki

    // each step adds (error = 1) × dt = 1 to the running integral
    REQUIRE(pid.compute(4.0, 1.0) == Approx(0.1));      // integral 1 × ki 0.1
    REQUIRE(pid.compute(4.0, 1.0) == Approx(0.2));      // integral 2 × ki 0.1
}
```

Each `TEST_CASE` pins down one behaviour in arithmetic you can check by hand. Flip a sign in `Tank::update`, or forget to clamp the valve, and the matching test goes red the moment you build — the safety net that [Testing](../Chapter6/testing.md) is about.

## Running them

The `tests` target now appears alongside `tank_control` in CLion's run dropdown — select it and click **Run**, and Catch2 reports how many assertions passed. From the command line:

```bash
cmake -B build
cmake --build build
./build/tests/tests      # Linux/macOS;  build\tests\tests.exe on Windows
```

A green run means every behaviour above still holds; a red one points you straight at the component that broke.

## What this version shows

- **Unit testing** — checking each component in isolation with Catch2's `TEST_CASE` and `REQUIRE`, and `Approx` for floating-point. See [Testing](../Chapter6/testing.md).
- **A shared library** — the app and the tests link the *same* compiled code (`tank_lib`), so the tests check the real thing. See [Building libraries](../Chapter2/cmake_intro.md#building-libraries).
- **A multi-folder build** — `add_subdirectory` keeps each folder's build next to its code. See [CMake](../Chapter2/cmake_intro.md#splitting-the-build-across-folders).

---

## Make it your own

You now have a clean, tested skeleton — a plant, a sensor, a controller, a loop, and a suite that proves they behave. That separation is exactly what makes the following *additions* rather than rewrites. Pick a few, and **add a test for each as you go** — that is how the suite, and your confidence, grow:

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

You have built, in miniature, the architecture of real control software — and grown it the way real software grows: one motivated step at a time, each step earning a test of its own.
