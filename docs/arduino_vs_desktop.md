# Arduino vs. Desktop C++

You are learning C++ for the desktop in this course and programming an Arduino in a parallel one. The two can feel like different languages. They are not: **Arduino is C++.** The same syntax, types, control flow, functions, classes, references, and `const`-correctness you learn here all carry straight over.

What differs is *where the code runs*. An Arduino is a tiny computer with no operating system and very little memory, so two things change: the **shape of the program**, and **how much of the standard library you can use**. This page maps the differences so neither course confuses the other.

> The specifics below describe a small 8-bit board like the Arduino Uno or Nano — the classic baseline. More powerful boards (ESP32, Teensy, Raspberry Pi Pico) lift many of these limits; see [Not all boards are equal](#not-all-boards-are-equal).

---

## It's the same language

Everything in Chapters 1 and 4 is true on an Arduino too:

- variables, `int` / `double` / `bool` / `char`, `if` / `for` / `while`, functions;
- classes, member functions, constructors, `const` member functions;
- references and pointers, passing by `const&`;
- the compiler is still GCC — just a version that targets the board's chip.

If you can write a class on the desktop, you can write one on an Arduino. Keep your habits.

---

## Where is `main()`? — `setup()` and `loop()`

On the desktop, your program starts at `main()` and ends when `main()` returns:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello\n";
    return 0;
}
```

An Arduino sketch has no `main()` that *you* write. Instead you write two functions, and the Arduino core supplies a hidden `main()` that calls them:

```cpp
void setup() {
    Serial.begin(9600);       // runs once, at power-on / reset
    Serial.println("Hello");
}

void loop() {
    // runs again and again, forever
}
```

- `setup()` runs **once** when the board powers up — do one-time configuration here.
- `loop()` runs **over and over, forever** — there is no "end." A microcontroller is never *done*; it keeps responding to the world until the power is cut.

Behind the scenes the Arduino core's `main()` is roughly: initialise the hardware, call `setup()` once, then `for (;;) loop();`.

---

## Sharing state between `setup()` and `loop()`

`loop()` runs from the top every time, but your data has to survive from one call to the next. With no `main()` whose local variables could hold it, Arduino sketches keep that state in **global variables**, declared outside both functions:

```cpp
int  blinkCount = 0;     // global: survives from one loop() call to the next
bool ledOn      = false;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    ledOn = !ledOn;
    digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
    ++blinkCount;
    delay(500);
}
```

On a small board this is normal and often unavoidable. But it is the one desktop habit to **un-learn carefully**: on the desktop, [global variables are a trap](Chapter1/functions.md#global-variables) — any function can change them, so you can no longer tell what touches your state. There you keep state local to `main`, or, better, bundle it inside a [class](Chapter4/classes.md) that owns it.

The good news: you can do exactly that on Arduino too. Group related globals into a small `struct` or `class` so the state has one clear owner — the language is identical; only the constraint (it must persist across `loop()`) is new.

---

## Printing: `Serial` instead of `std::cout`

There is no console and no `<iostream>` on a small board. To print — usually for debugging, sent over the USB cable to your PC — use the `Serial` object:

| Desktop | Arduino |
|---------|---------|
| `std::cout << "x = " << x << "\n";` | `Serial.print("x = "); Serial.println(x);` |
| `std::cin >> x;` | `x = Serial.parseInt();` (and similar) |

Call `Serial.begin(9600);` once in `setup()` before you print anything.

---

## A much smaller computer

This is the root of almost every other difference. A desktop has gigabytes of RAM; an Uno has **two kilobytes**.

| | Arduino Uno | Typical desktop |
|---|---|---|
| RAM | 2 KB | 8–32 GB |
| Program storage | 32 KB flash | hundreds of GB |
| CPU | 1 core, 16 MHz | many cores, GHz |
| Operating system | none | Windows / macOS / Linux |

With 2 KB of RAM you cannot be casual about memory. That drives the next two differences.

---

## The standard library is mostly absent

On a small board, the parts of the standard library this book leans on are **not available, or not advisable**:

- **No `<iostream>`** — print with `Serial` (above).
- **`std::vector`, `std::map`, `std::string`** are typically unavailable on AVR, and where they exist they allocate on the heap — risky with 2 KB of RAM. Prefer **plain fixed-size arrays** (`int buf[32]`) and **fixed buffers**.
- **Exceptions and RTTI** (`dynamic_cast`, `typeid`) are usually switched **off** by default.
- **Avoid `new` / `delete` and deep recursion** — heap fragmentation and stack overflow are real hazards on a 2 KB device.

### Arduino `String` vs `std::string`

Arduino offers a `String` class (capital **S**) that looks friendly but allocates on the heap and fragments memory on small boards. For anything long-running, prefer C-style strings (`char buf[32]`) or fixed buffers. This is the *opposite* of the desktop advice ("reach for `std::string`") — because the constraints are opposite.

---

## Integer sizes bite you

On the desktop and on 32-bit boards, `int` is 32 bits. **On an 8-bit AVR, `int` is only 16 bits** — its largest value is 32767.

```cpp
int x = 40000;   // desktop / ESP32: fine.  Uno: overflows — int maxes out at 32767
```

When the exact size matters — and on a microcontroller it often does — use the fixed-width integer types, which mean the same thing on every chip. The names are identical on both sides; only the header differs. On the desktop, `#include <cstdint>`. On an Arduino there is no `<cstdint>` — use the C header `<stdint.h>` instead (and a sketch already includes it for you, so `uint8_t` and friends just work):

| Type | Bits | Range |
|------|------|-------|
| `uint8_t`  | 8  | 0 … 255 |
| `int16_t`  | 16 | −32768 … 32767 |
| `uint16_t` | 16 | 0 … 65535 |
| `int32_t`  | 32 | ±2.1 billion |

Also on AVR: `double` is only 32 bits (the same as `float`), so it carries less precision than the 64-bit `double` you get on the desktop.

---

## No operating system, and it runs forever

- **No files, no command line, no terminal** — the board talks to the world through its pins and `Serial`, not a filesystem.
- **`delay(1000)` blocks** the whole program for a second. For anything that must stay responsive, read the clock with `millis()` instead of blocking.
- **Your code is the whole program.** There is no OS to return to; `loop()` simply never stops.

```cpp
// Arduino library functions you will see (declared in <Arduino.h>):
pinMode(13, OUTPUT);
digitalWrite(13, HIGH);
int v = analogRead(A0);
delay(500);
unsigned long now = millis();
```

`pinMode`, `digitalWrite`, `analogRead`, `delay`, and `millis` are Arduino *library* functions, not part of C++ — they do not exist on the desktop. The full set the Arduino core provides — every built-in function, constant, and type — is documented in the [Arduino Language Reference](https://docs.arduino.cc/language-reference/).

---

## Not all boards are equal

"Arduino" spans very different hardware, and the limits above ease quickly on more capable boards:

| Board | Chip | `int` | RAM | Standard library / STL |
|-------|------|-------|-----|------------------------|
| Uno / Nano / Mega | 8-bit AVR | 16-bit | 2–8 KB | mostly absent |
| ESP32 | 32-bit Xtensa | 32-bit | ~520 KB | much of the STL works |
| Teensy 4.x | 32-bit ARM | 32-bit | ~1 MB | much of the STL works |
| Raspberry Pi Pico | 32-bit ARM | 32-bit | 264 KB | much of the STL works |

On a 32-bit board with hundreds of KB of RAM, the code looks much more like the desktop C++ in this book — `int` is 32 bits, `std::string` and `std::vector` are usable, floating point is full precision. The 8-bit Uno is the strict case: treat its limits as the baseline and relax them only when your board allows.

---

## What to carry over

- **The language transfers completely.** Your grasp of types, control flow, functions, classes, references, and `const` is exactly the same on both.
- **Memory discipline is the new habit.** On a small board: avoid the heap, prefer fixed-size storage, and watch integer widths.
- **The board decides how desktop-like it feels.** Check its chip (8-bit AVR vs 32-bit) — that tells you which rules apply.
- For the toolchain that builds and uploads Arduino code from a real IDE, see [PlatformIO](Chapter2/platformio.md).

---

## Summary

- Arduino *is* C++ — same language, different environment.
- You write `setup()` (once) and `loop()` (forever) instead of `main()`.
- Print with `Serial`, not `std::cout`.
- Small 8-bit boards have ~2 KB of RAM: avoid the heap, `std::string`, and `std::vector`; prefer fixed buffers and plain arrays.
- `int` is 16-bit on AVR — use fixed-width types (`uint8_t`, `int32_t`, …, from `<stdint.h>`) when size matters.
- 32-bit boards (ESP32, Teensy, Pico) lift most of these limits and feel much closer to desktop C++.
