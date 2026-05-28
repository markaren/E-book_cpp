# Random Numbers

Sooner or later you need randomness — a dice roll, a shuffled list, a noisy sensor reading in a [simulation](tank_control/v1_classes.md). C++ has a correct way to do this and an old, broken way you will see all over the internet. This page shows the correct way.

> **The short version:** `#include <random>`, make one **generator** and seed it once, then draw numbers through a **distribution**. Never use `rand() % n`.

---

## The old way, and why to avoid it

You will see this everywhere:

<!-- no-ce -->
```cpp
#include <cstdlib>
#include <ctime>

std::srand(std::time(nullptr));    // seed once
int roll = std::rand() % 6 + 1;    // a number from 1 to 6... sort of
```

It runs, but it has real problems:

- **`% 6` is biased.** `rand()` returns a value from a fixed range whose size is rarely an exact multiple of 6, so some outcomes come up slightly more often than others. For a die you might not notice; for anything that matters, you will.
- **`rand()` is low quality.** The sequence it produces is poor by modern standards and differs between compilers.
- **It is clumsy to control.** One hidden global generator, shared by everything.

Modern C++ replaced all of this in 2011 with the `<random>` header. Use it.

---

## The right way: `<random>`

Three pieces — a **seed source**, a **generator** (the engine), and a **distribution** (the shape):

<!-- no-ce -->
```cpp
#include <random>

std::random_device rd;                          // 1. a source of a random seed
std::mt19937 gen(rd());                          // 2. the generator, seeded once
std::uniform_int_distribution<int> die(1, 6);    // 3. the shape of the numbers

int roll = die(gen);   // a fair integer in [1, 6]
```

- **`std::random_device`** produces a hard-to-predict number, used once to seed the generator.
- **`std::mt19937`** is the *Mersenne Twister* — the standard, good-quality general-purpose generator. Create it **once** and keep reusing it.
- **The distribution** turns the generator's raw output into the numbers you actually want, in the range you want, with no bias. You draw a value by calling it with the generator: `die(gen)`.

---

## Choosing a distribution

| You want | Distribution | Example |
|----------|--------------|---------|
| A whole number in a range | `std::uniform_int_distribution<int>` | `{1, 6}` — a die |
| A real number in a range | `std::uniform_real_distribution<double>` | `{0.0, 1.0}` |
| A "bell curve" around a mean | `std::normal_distribution<double>` | `{mean, stddev}` — sensor noise |
| A true/false coin flip | `std::bernoulli_distribution` | `{0.3}` — true 30% of the time |

`uniform_int_distribution` includes **both** endpoints: `{1, 6}` can return 1, 6, and everything between.

To **shuffle** a container, use `std::shuffle` (from `<algorithm>`), which takes your generator — not the old `std::random_shuffle`, which was removed in C++17:

<!-- no-ce -->
```cpp
std::shuffle(deck.begin(), deck.end(), gen);
```

---

## Make the generator once

The most common mistake with `<random>` is creating the generator (or worse, a fresh `random_device`) *every time* you need a number:

<!-- no-ce -->
```cpp
int badRoll() {
    std::mt19937 gen(std::random_device{}());      // WRONG: re-created every call
    std::uniform_int_distribution<int> die(1, 6);
    return die(gen);
}
```

That is slow, and on some toolchains it returns nearly the same value every call. Build the generator **once** and reuse it — keep it as a class member, or pass it around by reference:

<!-- no-ce -->
```cpp
class Dice {
    std::mt19937 gen_{std::random_device{}()};    // seeded once, when a Dice is created
    std::uniform_int_distribution<int> die_{1, 6};
public:
    int roll() { return die_(gen_); }             // reuse it on every call
};
```

---

## Reproducible runs

`random_device` gives a different sequence each run. For a **test**, or a **simulation you want to repeat exactly**, seed with a fixed number instead:

<!-- no-ce -->
```cpp
std::mt19937 gen(42);   // same seed → same sequence, every run
```

This is invaluable when debugging: a failing run becomes reproducible. The tank simulation's noisy-sensor extension uses exactly this — a fixed seed makes the "random" noise repeatable while you work on the controller.

> **A MinGW gotcha.** On some toolchains — notably older MinGW, which CLion may bundle on Windows — `std::random_device` is **not actually random**: it returns the same sequence every run. If your program's "random" numbers never change between runs, this is why. Seed from the clock instead: `std::mt19937 gen(std::chrono::steady_clock::now().time_since_epoch().count());` (from `<chrono>`).

---

## A worked example: a noisy sensor

Putting it together — a level reading with Gaussian noise, the kind you would add to the [tank simulation](tank_control/v2_sensors.md):

```cpp
#include <iostream>
#include <random>

int main() {
    std::mt19937 gen(42);                               // fixed seed: repeatable
    std::normal_distribution<double> noise(0.0, 0.05);  // mean 0, std-dev 0.05 m

    double trueLevel = 5.0;
    for (int i = 0; i < 5; ++i) {
        double reading = trueLevel + noise(gen);        // true value + wobble
        std::cout << "reading = " << reading << " m\n";
    }
}
```

Each `noise(gen)` is a small positive or negative wobble around zero; added to the true level, it models a real sensor that is never perfectly precise.

---

## Summary

- `#include <random>`. Forget `rand()` and `srand()`.
- Three pieces: a **seed** (`std::random_device`), a **generator** (`std::mt19937`), and a **distribution**.
- Create the generator **once** and reuse it — never per call.
- Pick a distribution for the shape you want; it handles the range with no bias.
- Seed with a **fixed number** for tests and repeatable simulations.
- If randoms repeat every run on Windows/MinGW, seed from the clock instead.
- Real-valued distributions give `double`s — compare them with care; see [Floating-Point Pitfalls](floating_point.md).
