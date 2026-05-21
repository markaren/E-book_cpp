# Separation of Concerns

When a program is small — one `main`, a few helper functions — you can keep the whole thing in your head. As it grows, you cannot. The way out is **separation of concerns**: organising the program so each piece is responsible for one thing, and pieces only know about each other through narrow, deliberate interfaces.

Code written this way is easier to read, easier to test, and easier to change. Code that ignores it tends to develop a quality where every change breaks something unrelated.

This chapter explains the principle and shows what it looks like in code.

---

## The smell of mixed concerns

Here is a function that reads a temperature sensor, decides whether it is overheating, and prints a warning. All in one place:

```cpp
void monitorLoop() {
    while (true) {
        int raw = analogRead(A0);
        double celsius = (raw * 5.0 / 1023.0 - 0.5) * 100.0;

        if (celsius > 80.0) {
            std::ofstream log("alerts.log", std::ios::app);
            log << "[ALERT] " << celsius << " C at " << millis() << "\n";
            std::cout << "OVERHEAT\n";
            digitalWrite(LED_BUILTIN, HIGH);
        }

        delay(100);
    }
}
```

What is wrong with it? Nothing, mechanically — it works. But three different concerns are tangled together:

1. **Hardware access** — reading the sensor, writing to the LED.
2. **Domain logic** — converting raw ADC values to temperature, deciding what counts as overheating.
3. **Reporting** — writing to a log file, printing to the console.

To test the domain logic without a real sensor, you cannot. To send alerts somewhere other than a file, you have to edit this function. To use a different sensor with a different conversion formula, ditto. Every concern is welded to every other.

---

## The same logic, separated

The same behaviour, but each concern is its own piece:

```cpp
// --- Concern 1: hardware access ---
class TemperatureSensor {
public:
    virtual ~TemperatureSensor() = default;
    virtual double readCelsius() = 0;
};

class AnalogTemperatureSensor : public TemperatureSensor {
public:
    AnalogTemperatureSensor(int pin) : pin_(pin) {}
    double readCelsius() override {
        int raw = analogRead(pin_);
        return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    }
private:
    int pin_;
};

// --- Concern 2: domain logic ---
class OverheatPolicy {
public:
    OverheatPolicy(double threshold) : threshold_(threshold) {}
    bool isOverheating(double celsius) const {
        return celsius > threshold_;
    }
private:
    double threshold_;
};

// --- Concern 3: reporting ---
class AlertSink {
public:
    virtual ~AlertSink() = default;
    virtual void overheatDetected(double celsius) = 0;
};

class FileAlertSink : public AlertSink {
public:
    FileAlertSink(const std::filesystem::path& path) : out_(path, std::ios::app) {}
    void overheatDetected(double celsius) override {
        out_ << "[ALERT] " << celsius << " C\n";
    }
private:
    std::ofstream out_;
};

// --- The orchestrator: ties them together, knows nothing about details ---
void monitorLoop(TemperatureSensor& sensor,
                 const OverheatPolicy& policy,
                 AlertSink& alerts) {
    while (true) {
        double t = sensor.readCelsius();
        if (policy.isOverheating(t)) {
            alerts.overheatDetected(t);
        }
        delay(100);
    }
}
```

Each class has one job. The function that pulls them together knows about *what* must happen but nothing about *how* — it has no idea whether the temperature comes from an analog pin or a simulated sensor, no idea whether alerts go to a file or a network socket, no idea what threshold is in effect.

Want to test the policy? Construct an `OverheatPolicy` and call `isOverheating` with values — no hardware required. Want to switch from a file to a console alert? Write a `ConsoleAlertSink` and pass it in instead. Want to test the orchestrator? Pass it a fake sensor that returns scripted values and a fake sink that records the alerts.

---

## What "concern" means in practice

A **concern** is one thing a program is responsible for. Some concerns are obvious:

- talking to hardware
- computing something
- presenting results to a user
- storing data
- handling errors

Other concerns are more subtle and emerge over time. You will recognise mixed concerns by the symptoms:

- A small change to one part forces edits in unrelated parts.
- Writing a test for one piece requires setting up things that have nothing to do with the test.
- A function's name needs the word "and" — `readSensorAndAlertIfHot`.
- A single class talks to the network, the database, and the user interface.

When you spot these, you have a candidate for splitting.

---

## Tools for separating concerns

The principle is timeless; the techniques are concrete.

### Functions

The most basic tool. If a chunk of code inside a function does something with a name, give it its own function:

```cpp
// Before
void run() {
    int raw = analogRead(A0);
    double celsius = (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    /* ... 50 more lines ... */
}

// After
double readTemperature() {
    int raw = analogRead(A0);
    return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
}

void run() {
    double t = readTemperature();
    /* ... */
}
```

The named function documents intent, can be tested in isolation, and stops the calling function from drowning in detail.

### Classes

A class groups data with the operations that act on it. Reach for a class when several related pieces of state need to evolve together — a connection, a parser, a controller — and you find the same data being passed around in tandem.

### Interfaces (abstract base classes)

When the orchestrator does not need to know which concrete implementation it is talking to, hide it behind an interface. The example above uses `TemperatureSensor` and `AlertSink` exactly this way — `monitorLoop` works with anything that fulfils those interfaces. Swap implementations without touching the orchestrator.

This is also what makes code testable: the interface lets you substitute a fake implementation in tests.

### Files and modules

Once a logical piece grows beyond a screen, give it its own file. Header + implementation pair per class is a reasonable default. Group related files into folders (`sensors/`, `alerts/`, `policies/`). The folder structure itself becomes documentation of what concerns the project has.

---

## How far to take it

It is possible to over-do this. A program with thirty classes for the same job five would handle is not "separated"; it is shattered. Two rules of thumb:

1. **Separate when you have a reason.** If your `readSensor` function never changes and you only call it from one place, leaving it inline is fine.
2. **Look for the friction.** When you find yourself wanting to test something but not being able to, or wanting to swap something out and not being able to — that is where to draw the line.

Good design is not the design with the most classes. It is the design where each class has a clear job, and where introducing a new requirement does not force you to rewrite everything.

---

## Summary

- **Each piece of code should be responsible for one thing.**
- When you find a function doing more than one thing, split it.
- Use interfaces to decouple "what" from "how" — `TemperatureSensor` does not know which sensor; `monitorLoop` does not know which sensor either.
- Separation makes code easier to test, easier to change, and easier to read.
- Do not separate just for the sake of it. The signal is friction — testing, changing, swapping.
