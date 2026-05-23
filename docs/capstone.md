# Capstone Project: Sensor Monitor

This project ties the whole book together. You build it in two parts:

- **Part 1** — a single-file program that logs temperature readings, summarises them, classifies each one, and writes a report. The achievable core: classes, a `std::vector`, standard-library algorithms, an `enum`, `const`-correctness, and RAII file output (Chapters 1, 3, 4). If Part 2 feels like too much, Part 1 alone is a complete, working program.
- **Part 2** — you grow it into a **monitoring system**: it reads readings for many named sensors from a file, rejects bad data, raises an alarm on a run of critical readings, is split into a CMake **library + app**, and is backed by an automated **test** (Chapters 2, 3, 6).

Build it as a real **CLion + CMake project**. Work the milestones in order; each adds one capability and shows what the program should print when you run it. **Try each milestone before revealing the solution** — the solutions are blurred; click once more to reveal. Type your own; they are there to check against.

---

## What you'll build

By the end, `monitor` reads `readings.txt`, rejects implausible values, raises an alarm when a sensor logs three critical readings in a row, prints a summary, and writes a full report to `report.txt`:

!!! example "The finished program prints"

    ```
    ambient: mean 22.75, max 23.5 (OK)
    boiler: mean 45.9, max 60 (CRITICAL)  *** ALARM ***
    Rejected: 1
    Report written to report.txt
    ```

A reading over 50 is `CRITICAL`, over 30 is `WARNING`, otherwise `OK`. A value outside −50…150 is rejected as implausible. Three criticals in a row raises the alarm.

---

# Part 1 — A working logger (one file)

## Set up the project

Create a project with a `CMakeLists.txt` (see [CMake](Chapter2/cmake_intro.md)) and an empty `main.cpp`:

```cmake
cmake_minimum_required(VERSION 3.15)
project(sensor_monitor)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(monitor main.cpp)
target_compile_options(monitor PRIVATE -Wall -Wextra)
```

Put it under version control and commit after each milestone (see [Version Control & Git](Chapter2/version_control.md)):

```bash
git init
git add CMakeLists.txt main.cpp
git commit -m "Empty Sensor Monitor project"
```

## Milestone 1 — Store the readings

*Practises: [Classes](Chapter4/classes.md), [Data Structures](Chapter3/data_structures.md)*

Write a class `SensorLog` that stores `double` readings in a private `std::vector<double>`. Give it `add(double)`, a `const` method `count()`, and a `const` method `mean()` (return `0.0` for an empty log). In `main`, add the readings `21.5`, `35.0`, `23.5`, `60.0` and print the count and mean.

> Hint: the vector is the class's private state. Mark `count()` and `mean()` `const` — they only observe.

!!! example "Run it — you should see"

    ```
    Count: 4
    Mean:  35
    ```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>

    class SensorLog {
    public:
        void add(double reading) {
            readings_.push_back(reading);
        }

        int count() const {
            return static_cast<int>(readings_.size());
        }

        double mean() const {
            if (readings_.empty()) {
                return 0.0;
            }
            double sum = 0.0;
            for (double r : readings_) {
                sum += r;
            }
            return sum / readings_.size();
        }

    private:
        std::vector<double> readings_;
    };

    int main() {
        SensorLog log;
        log.add(21.5);
        log.add(35.0);
        log.add(23.5);
        log.add(60.0);

        std::cout << "Count: " << log.count() << "\n";
        std::cout << "Mean:  " << log.mean() << "\n";
    }
    ```

    The readings are private, so they can only change through `add` — the class owns its data. `count()` and `mean()` are `const` because reporting does not modify the log.

    </div>

## Milestone 2 — Summary statistics

*Practises: [C++ Standard Library](Chapter3/standard_library.md)*

Add `const` methods `min()` and `max()` using standard-library algorithms rather than hand-written loops, and print them.

> Hint: `<algorithm>` has `std::min_element` and `std::max_element`. Both return an *iterator*, so dereference with `*` to get the value.

!!! example "Run it — you should see"

    ```
    Count: 4
    Mean:  35
    Min:   21.5
    Max:   60
    ```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Add `#include <algorithm>` and these two methods to `SensorLog`:

    ```cpp
    double min() const {
        if (readings_.empty()) {
            return 0.0;
        }
        return *std::min_element(readings_.begin(), readings_.end());
    }

    double max() const {
        if (readings_.empty()) {
            return 0.0;
        }
        return *std::max_element(readings_.begin(), readings_.end());
    }
    ```

    and these two lines to `main`:

    ```cpp
    std::cout << "Min:   " << log.min() << "\n";
    std::cout << "Max:   " << log.max() << "\n";
    ```

    Letting `<algorithm>` find the smallest and largest is shorter and harder to get wrong than writing the loops yourself.

    </div>

## Milestone 3 — Classify each reading

*Practises: [Enumerations](Chapter1/enums.md), [Functions](Chapter1/functions.md), [Values, References & Pointers](Chapter4/types_refs_ptrs.md)*

Define `enum class Status { Ok, Warning, Critical }` and a free function `classify(double)`. Add `toText(Status)` that turns a status into text with a `switch`. Give `SensorLog` a `const` getter `readings()` returning the vector by `const&`, then loop over it in `main`, printing each reading with its status.

> Hint: returning `const std::vector<double>&` hands out read-only access without copying — the const-correctness idea from Chapter 4.

!!! example "Run it — you should see"

    ```
    Count: 4
    Mean:  35
    Min:   21.5
    Max:   60
    21.5 -> OK
    35 -> WARNING
    23.5 -> OK
    60 -> CRITICAL
    ```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Add `#include <string>` (for `toText`'s return type), then above the class add the enum and two functions:

    ```cpp
    enum class Status { Ok, Warning, Critical };

    Status classify(double reading) {
        if (reading > 50.0) {
            return Status::Critical;
        }
        if (reading > 30.0) {
            return Status::Warning;
        }
        return Status::Ok;
    }

    std::string toText(Status s) {
        switch (s) {
            case Status::Ok:       return "OK";
            case Status::Warning:  return "WARNING";
            case Status::Critical: return "CRITICAL";
        }
        return "UNKNOWN";
    }
    ```

    Add a getter to `SensorLog`:

    ```cpp
    const std::vector<double>& readings() const {
        return readings_;
    }
    ```

    And loop in `main`:

    ```cpp
    for (double r : log.readings()) {
        std::cout << r << " -> " << toText(classify(r)) << "\n";
    }
    ```

    `readings()` returns a `const&`, so the loop reads the vector without copying it and cannot modify the log. The `switch` has no `default`, so if you add a fourth status later the compiler warns you that this function does not handle it.

    </div>

## Milestone 4 — Write a report file

*Practises: [IO & Streams](Chapter4/io_streams.md), [RAII](Chapter4/raii.md)*

Write the per-reading list to `report.txt` with a `std::ofstream`, then print `Report written to report.txt`. You do **not** close the file yourself.

> Hint: an `ofstream` opens the file in its constructor and closes it in its destructor — RAII. When the variable goes out of scope, the file is flushed and closed for you.

!!! example "Run it — you should see"

    ```
    ... (the lines above, then:)
    Report written to report.txt
    ```

!!! warning "Where did `report.txt` go?"

    CLion runs your program from the **build** directory (e.g. `cmake-build-debug/`), not your project folder, so that is where `report.txt` appears. If you cannot find it, that is why. ([Computer Basics](computer_basics.md) explains working directories.)

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Add `#include <fstream>`, and this block at the end of `main`:

    ```cpp
    std::ofstream report("report.txt");
    for (double r : log.readings()) {
        report << r << " -> " << toText(classify(r)) << "\n";
    }
    // `report` is closed automatically when it goes out of scope (RAII)

    std::cout << "Report written to report.txt\n";
    ```

    Writing to a file uses the same `<<` as `std::cout`. There is no `report.close()` — the destructor handles it, even on an early return or an exception.

    </div>

That is a complete, working program. Commit it, then grow it.

---

# Part 2 — Grow it into a monitoring system

Real monitoring reads data from somewhere, watches *many* sensors, guards against bad input, raises alarms, and is backed by tests. Each milestone adds one of those.

## Milestone 5 — Many sensors, read from a file

*Practises: [Data Structures](Chapter3/data_structures.md), [IO & Streams](Chapter4/io_streams.md)*

Real data does not live in your source code. Create a file `readings.txt` with a sensor name and a value per line:

!!! example "readings.txt"

    ```
    boiler 21.5
    boiler 35.0
    boiler 55.0
    boiler 60.0
    boiler 58.0
    ambient 23.5
    ambient 22.0
    ambient 999.0
    ```

Add a `Monitor` class holding a `std::map<std::string, SensorLog>`, with `record(name, value)`, a `const` getter `sensors()`, and a `writeReport(path)` (move the file-writing in here). In `main`, open `readings.txt`, read every `name value` pair into the monitor, and print a one-line summary per sensor.

> Hint: `while (in >> name >> value)` reads pairs until the file ends. `sensors_[name]` creates a `SensorLog` for a new name automatically, then you `.add()` to it.

!!! example "Run it — you should see"

    ```
    ambient: mean 348.167, max 999 (CRITICAL)
    boiler: mean 45.9, max 60 (CRITICAL)
    ```

    That `ambient` max of `999` is a broken-sensor reading polluting the data — you will reject it in the next milestone.

!!! warning "`Could not open readings.txt`?"

    The program looks for `readings.txt` in its **working directory** — the build folder, not your project folder (same trap as `report.txt` above). Put `readings.txt` there, or set the working directory under **Run → Edit Configurations**.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Add `#include <map>` and `#include <string>` to the header includes. Add the `Monitor` class below `SensorLog`:

    ```cpp
    class Monitor {
    public:
        void record(const std::string& sensor, double reading) {
            sensors_[sensor].add(reading);
        }

        const std::map<std::string, SensorLog>& sensors() const {
            return sensors_;
        }

        void writeReport(const std::string& path) const {
            std::ofstream report(path);
            for (const auto& [name, log] : sensors_) {
                report << name << ": count=" << log.count()
                       << " mean=" << log.mean()
                       << " min=" << log.min()
                       << " max=" << log.max() << "\n";
                for (double r : log.readings()) {
                    report << "  " << r << " -> " << toText(classify(r)) << "\n";
                }
            }
        }

    private:
        std::map<std::string, SensorLog> sensors_;
    };
    ```

    Add `#include <fstream>` and `#include <string>`, then replace `main`:

    ```cpp
    int main() {
        std::ifstream in("readings.txt");
        if (!in) {
            std::cerr << "Could not open readings.txt\n";
            return 1;
        }

        Monitor monitor;
        std::string name;
        double value;
        while (in >> name >> value) {
            monitor.record(name, value);
        }

        for (const auto& [sensorName, log] : monitor.sensors()) {
            std::cout << sensorName << ": mean " << log.mean()
                      << ", max " << log.max()
                      << " (" << toText(classify(log.max())) << ")\n";
        }

        monitor.writeReport("report.txt");
    }
    ```

    `Monitor` owns the sensors and is the only thing that touches the map. `std::map` keeps them sorted by name, which is why `ambient` prints before `boiler`. The `if (!in)` check is the stream's bool conversion from the IO chapter: a stream that failed to open is falsy.

    </div>

## Milestone 6 — Reject invalid readings

*Practises: [Error Handling](Chapter6/error_handling.md)*

That `999` should never have entered the data. Add a free function `isValidReading(double)` accepting only plausible temperatures (−50 to 150). Change `Monitor::record` to **return `bool`**: reject and count anything invalid instead of storing it. Expose the count with `rejected()`, print it, and add it to the report.

> Hint: a `bool` return lets the caller see whether the reading was accepted — the simplest form of error reporting.

!!! example "Run it — you should see"

    ```
    ambient: mean 22.75, max 23.5 (OK)
    boiler: mean 45.9, max 60 (CRITICAL)
    Rejected: 1
    ```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Add the validator as a free function:

    ```cpp
    bool isValidReading(double reading) {
        return reading >= -50.0 && reading <= 150.0;
    }
    ```

    Make `record` validate and count rejects, and add `rejected()`:

    ```cpp
    bool record(const std::string& sensor, double reading) {
        if (!isValidReading(reading)) {
            ++rejected_;
            return false;
        }
        sensors_[sensor].add(reading);
        return true;
    }

    int rejected() const {
        return rejected_;
    }
    ```

    Add `int rejected_ = 0;` to the private section, `report << "Rejected readings: " << rejected_ << "\n";` at the end of `writeReport`, and after the per-sensor loop in `main`:

    ```cpp
    std::cout << "Rejected: " << monitor.rejected() << "\n";
    ```

    Returning `bool` is the lightest way to signal "did this work?". For richer failures you would reach for `std::optional` or exceptions, but a yes/no is right here.

    </div>

## Milestone 7 — Raise an alarm

*Practises: [Control Statements](Chapter1/control_statements.md), [Classes](Chapter4/classes.md)*

A single critical reading might be noise; **three in a row** is a real problem. Add a `const` method `SensorLog::inAlarm()` that returns `true` when the log contains three or more *consecutive* `Critical` readings. Flag alarmed sensors in the console output and the report.

> Hint: walk the readings keeping a running count of consecutive criticals. Increment it on a `Critical`, reset it to `0` on anything else, and return `true` if it ever reaches `3`.

!!! example "Run it — you should see"

    ```
    ambient: mean 22.75, max 23.5 (OK)
    boiler: mean 45.9, max 60 (CRITICAL)  *** ALARM ***
    Rejected: 1
    ```

    `boiler`'s last three readings (55, 60, 58) are all critical, so it alarms; `ambient` does not.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Add the method to `SensorLog`:

    ```cpp
    bool inAlarm() const {
        int run = 0;
        for (double r : readings_) {
            if (classify(r) == Status::Critical) {
                ++run;
                if (run >= 3) {
                    return true;
                }
            } else {
                run = 0;
            }
        }
        return false;
    }
    ```

    Flag it in `main`'s loop:

    ```cpp
    std::cout << sensorName << ": mean " << log.mean()
              << ", max " << log.max()
              << " (" << toText(classify(log.max())) << ")";
    if (log.inAlarm()) {
        std::cout << "  *** ALARM ***";
    }
    std::cout << "\n";
    ```

    and append `" ALARM"` to the sensor's line in `writeReport` when `log.inAlarm()`. This is the one piece of real logic in the project: a running counter that resets, exactly the kind of state machine that shows up everywhere in control software.

    </div>

## Milestone 8 — Split into a library

*Practises: [CMake](Chapter2/cmake_intro.md), [Classes](Chapter4/classes.md)*

`main.cpp` now holds two classes, four free functions, and `main` — and you are about to add tests that need the same code. Split the logic into `sensor_log.hpp` (declarations) and `sensor_log.cpp` (definitions, each prefixed with its class), leaving `main.cpp` with only `#include "sensor_log.hpp"` and `main`. Build the logic as a CMake **library** the app links.

> Hint: the header/implementation split from the Classes chapter, plus `add_library` / `target_link_libraries` from CMake. The behaviour does not change — the output is identical to Milestone 7.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    `sensor_log.hpp` is the interface — declarations only (see the full file under *The complete project*). The method bodies move into `sensor_log.cpp`, each prefixed with its class, e.g. `void SensorLog::add(double reading) { ... }`. Update `CMakeLists.txt`:

    ```cmake
    add_library(sensor_log sensor_log.cpp)
    target_compile_options(sensor_log PRIVATE -Wall -Wextra)

    add_executable(monitor main.cpp)
    target_link_libraries(monitor PRIVATE sensor_log)
    ```

    The header is the *contract* — what the types offer. Compiling the library once and linking it is what lets the tests in the next milestone reuse exactly the same code the app runs.

    </div>

## Milestone 9 — Add a test

*Practises: [Testing](Chapter6/testing.md)*

Add `tests.cpp` that checks the logic with **Catch2**, built as a second executable linking your `sensor_log` library. Test the thresholds, the validator, the statistics, and — most importantly — the alarm logic.

> Hint: the Catch2 setup from the testing chapter — `FetchContent` to download it, then `target_link_libraries(... Catch2::Catch2WithMain)`.

!!! example "Run `tests` — you should see"

    ```
    All tests passed (13 assertions in 5 test cases)
    ```

!!! note "The first build downloads Catch2"

    `FetchContent` pulls Catch2 from GitHub the first time you configure, so the initial build needs an internet connection and takes a minute.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    `tests.cpp`:

    ```cpp
    #include <catch2/catch_test_macros.hpp>

    #include "sensor_log.hpp"

    TEST_CASE("classify uses the thresholds") {
        REQUIRE(classify(10.0) == Status::Ok);
        REQUIRE(classify(40.0) == Status::Warning);
        REQUIRE(classify(80.0) == Status::Critical);
    }

    TEST_CASE("isValidReading rejects out-of-range values") {
        REQUIRE(isValidReading(20.0));
        REQUIRE(!isValidReading(999.0));
    }

    TEST_CASE("SensorLog computes statistics") {
        SensorLog log;
        log.add(10.0);
        log.add(20.0);
        REQUIRE(log.count() == 2);
        REQUIRE(log.mean() == 15.0);
        REQUIRE(log.min() == 10.0);
        REQUIRE(log.max() == 20.0);
    }

    TEST_CASE("three consecutive criticals raise the alarm") {
        SensorLog log;
        log.add(60.0);
        log.add(20.0);   // resets the run
        log.add(55.0);
        log.add(60.0);
        log.add(70.0);   // three in a row
        REQUIRE(log.inAlarm());
    }

    TEST_CASE("scattered criticals do not raise the alarm") {
        SensorLog log;
        log.add(60.0);
        log.add(60.0);
        log.add(20.0);   // breaks the run at two
        log.add(60.0);
        REQUIRE(!log.inAlarm());
    }
    ```

    Add Catch2 and the test target to `CMakeLists.txt`:

    ```cmake
    include(FetchContent)
    FetchContent_Declare(
      Catch2
      GIT_REPOSITORY https://github.com/catchorg/Catch2.git
      GIT_TAG        v3.5.2
    )
    FetchContent_MakeAvailable(Catch2)

    add_executable(tests tests.cpp)
    target_link_libraries(tests PRIVATE sensor_log Catch2::Catch2WithMain)
    ```

    **See a test fail.** Tests earn their keep the moment one goes red. Temporarily change `classify`'s `> 50.0` to `> 70.0` and rerun `tests`:

    ```
    tests.cpp:7: FAILED:
      REQUIRE( classify(80.0) == Status::Critical )
    ```

    It points at the exact line and value. Change it back and the tests pass again — that red-to-green loop is the whole point.

    </div>

## The complete project

??? success "Show the complete project"

    <div class="spoiler" markdown title="Click to reveal">

    **`CMakeLists.txt`**

    ```cmake
    cmake_minimum_required(VERSION 3.14)
    project(sensor_monitor)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    add_library(sensor_log sensor_log.cpp)
    target_compile_options(sensor_log PRIVATE -Wall -Wextra)

    add_executable(monitor main.cpp)
    target_link_libraries(monitor PRIVATE sensor_log)

    include(FetchContent)
    FetchContent_Declare(
      Catch2
      GIT_REPOSITORY https://github.com/catchorg/Catch2.git
      GIT_TAG        v3.5.2
    )
    FetchContent_MakeAvailable(Catch2)

    add_executable(tests tests.cpp)
    target_link_libraries(tests PRIVATE sensor_log Catch2::Catch2WithMain)
    ```

    **`sensor_log.hpp`**

    ```cpp
    #pragma once

    #include <map>
    #include <string>
    #include <vector>

    enum class Status { Ok, Warning, Critical };

    Status classify(double reading);
    std::string toText(Status s);
    bool isValidReading(double reading);

    class SensorLog {
    public:
        void add(double reading);
        int count() const;
        double mean() const;
        double min() const;
        double max() const;
        bool inAlarm() const;
        const std::vector<double>& readings() const;

    private:
        std::vector<double> readings_;
    };

    class Monitor {
    public:
        bool record(const std::string& sensor, double reading);
        int rejected() const;
        const std::map<std::string, SensorLog>& sensors() const;
        void writeReport(const std::string& path) const;

    private:
        std::map<std::string, SensorLog> sensors_;
        int rejected_ = 0;
    };
    ```

    **`sensor_log.cpp`**

    ```cpp
    #include "sensor_log.hpp"

    #include <algorithm>
    #include <fstream>
    #include <numeric>

    Status classify(double reading) {
        if (reading > 50.0) {
            return Status::Critical;
        }
        if (reading > 30.0) {
            return Status::Warning;
        }
        return Status::Ok;
    }

    std::string toText(Status s) {
        switch (s) {
            case Status::Ok:       return "OK";
            case Status::Warning:  return "WARNING";
            case Status::Critical: return "CRITICAL";
        }
        return "UNKNOWN";
    }

    bool isValidReading(double reading) {
        return reading >= -50.0 && reading <= 150.0;
    }

    void SensorLog::add(double reading) {
        readings_.push_back(reading);
    }

    int SensorLog::count() const {
        return static_cast<int>(readings_.size());
    }

    double SensorLog::mean() const {
        if (readings_.empty()) {
            return 0.0;
        }
        double sum = std::accumulate(readings_.begin(), readings_.end(), 0.0);
        return sum / readings_.size();
    }

    double SensorLog::min() const {
        if (readings_.empty()) {
            return 0.0;
        }
        return *std::min_element(readings_.begin(), readings_.end());
    }

    double SensorLog::max() const {
        if (readings_.empty()) {
            return 0.0;
        }
        return *std::max_element(readings_.begin(), readings_.end());
    }

    bool SensorLog::inAlarm() const {
        int run = 0;
        for (double r : readings_) {
            if (classify(r) == Status::Critical) {
                ++run;
                if (run >= 3) {
                    return true;
                }
            } else {
                run = 0;
            }
        }
        return false;
    }

    const std::vector<double>& SensorLog::readings() const {
        return readings_;
    }

    bool Monitor::record(const std::string& sensor, double reading) {
        if (!isValidReading(reading)) {
            ++rejected_;
            return false;
        }
        sensors_[sensor].add(reading);
        return true;
    }

    int Monitor::rejected() const {
        return rejected_;
    }

    const std::map<std::string, SensorLog>& Monitor::sensors() const {
        return sensors_;
    }

    void Monitor::writeReport(const std::string& path) const {
        std::ofstream report(path);
        for (const auto& [name, log] : sensors_) {
            report << name << ": count=" << log.count()
                   << " mean=" << log.mean()
                   << " min=" << log.min()
                   << " max=" << log.max();
            if (log.inAlarm()) {
                report << " ALARM";
            }
            report << "\n";
            for (double r : log.readings()) {
                report << "  " << r << " -> " << toText(classify(r)) << "\n";
            }
        }
        report << "Rejected readings: " << rejected_ << "\n";
    }
    ```

    **`main.cpp`**

    ```cpp
    #include <fstream>
    #include <iostream>
    #include <string>

    #include "sensor_log.hpp"

    int main() {
        std::ifstream in("readings.txt");
        if (!in) {
            std::cerr << "Could not open readings.txt\n";
            return 1;
        }

        Monitor monitor;
        std::string name;
        double value;
        while (in >> name >> value) {
            monitor.record(name, value);
        }

        for (const auto& [sensorName, log] : monitor.sensors()) {
            std::cout << sensorName << ": mean " << log.mean()
                      << ", max " << log.max()
                      << " (" << toText(classify(log.max())) << ")";
            if (log.inAlarm()) {
                std::cout << "  *** ALARM ***";
            }
            std::cout << "\n";
        }
        std::cout << "Rejected: " << monitor.rejected() << "\n";

        monitor.writeReport("report.txt");
        std::cout << "Report written to report.txt\n";
    }
    ```

    **`tests.cpp`**

    ```cpp
    #include <catch2/catch_test_macros.hpp>

    #include "sensor_log.hpp"

    TEST_CASE("classify uses the thresholds") {
        REQUIRE(classify(10.0) == Status::Ok);
        REQUIRE(classify(40.0) == Status::Warning);
        REQUIRE(classify(80.0) == Status::Critical);
    }

    TEST_CASE("isValidReading rejects out-of-range values") {
        REQUIRE(isValidReading(20.0));
        REQUIRE(!isValidReading(999.0));
    }

    TEST_CASE("SensorLog computes statistics") {
        SensorLog log;
        log.add(10.0);
        log.add(20.0);
        REQUIRE(log.count() == 2);
        REQUIRE(log.mean() == 15.0);
        REQUIRE(log.min() == 10.0);
        REQUIRE(log.max() == 20.0);
    }

    TEST_CASE("three consecutive criticals raise the alarm") {
        SensorLog log;
        log.add(60.0);
        log.add(20.0);
        log.add(55.0);
        log.add(60.0);
        log.add(70.0);
        REQUIRE(log.inAlarm());
    }

    TEST_CASE("scattered criticals do not raise the alarm") {
        SensorLog log;
        log.add(60.0);
        log.add(60.0);
        log.add(20.0);
        log.add(60.0);
        REQUIRE(!log.inAlarm());
    }
    ```

    **`readings.txt`**

    ```
    boiler 21.5
    boiler 35.0
    boiler 55.0
    boiler 60.0
    boiler 58.0
    ambient 23.5
    ambient 22.0
    ambient 999.0
    ```

    </div>

---

## Make it your own

Each extension reuses something from the book:

- **Make `SensorLog` printable** by overloading `operator<<` so `std::cout << log;` prints its summary (see [IO & Streams](Chapter4/io_streams.md)).
- **Alert live** by having `Monitor::record` call a registered callback the moment a sensor enters alarm (see [Observer Pattern](Chapter6/observer.md)).
- **Support different sensor kinds** — a base `Sensor` with derived `TemperatureSensor` / `PressureSensor` overriding their valid range (see [Polymorphism](Chapter5/polymorphism.md)).
- **Make the thresholds configurable** by passing them to `Monitor`'s constructor instead of hard-coding `30`/`50`.
- **Add more tests** for the edges — an empty log, a single reading, every value rejected (see [Testing](Chapter6/testing.md)).

---

## Summary

- A complete program is the pieces you already know, assembled: a class owning a `std::vector`, algorithms over it, an `enum` and a `switch`, a `const&` getter, file input and RAII file output, a `std::map` of named logs, validation, a bit of real alarm logic, and tests.
- Start single-file (Part 1); split into a **library + app + tests** once it grows and you want to test it (Part 2) — the exact moment the CMake chapter describes.
- `const` runs through the whole design, the `Monitor` owns its sensors, bad input is rejected at the door, and the logic is covered by tests you can trust.
- Pick an extension above and keep going — that is how a capstone becomes your own project.
