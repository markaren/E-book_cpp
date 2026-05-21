# PlatformIO

When you write C++ for a desktop computer, the compiler ships with your IDE and "build" means "produce an executable for the machine you are sitting at." Writing C++ for an Arduino, an ESP32, a Teensy, or any other embedded board is more involved: you need a **cross-compiler** that produces code for a different CPU, libraries written for that specific board, and a way to flash the resulting binary onto the device.

**PlatformIO** is the tool that hides all of this complexity behind a unified interface. Pick your board, write your code, press build. PlatformIO knows which toolchain to use, which libraries to fetch, and how to upload to the device.

---

## Why use PlatformIO?

You will see two common ways to program an Arduino-style board:

| Approach | Pros | Cons |
|----------|------|------|
| **Arduino IDE** | Built-in, simple | Limited editor, weak project structure, hard to manage dependencies |
| **PlatformIO** | Proper IDE integration, dependency management, multi-board projects, scriptable builds | A bit more setup |

For anything beyond a one-file sketch, PlatformIO is the right tool. It also integrates cleanly into CLion, the IDE you already use for desktop C++, meaning you can write code for both your desktop simulation and the embedded target in the same editor.

---

## Installation

Follow the [PlatformIO Core (CLI) installation guide](https://docs.platformio.org/en/latest/core/installation/index.html). Two things to do that the guide may underplay:

1. **Install the shell commands.** Without them you cannot run `pio` from the terminal. The installation page has a clear section labelled "Install Shell Commands."
2. **Reboot or open a new terminal** after installation so the new commands are on your `PATH`.

To verify the install:

```bash
pio --version
```

---

## Using PlatformIO with CLion

CLion has first-class support for PlatformIO via the [PlatformIO for CLion plugin](https://plugins.jetbrains.com/plugin/13922-platformio-for-clion), built in collaboration with the PlatformIO team.

Install the plugin from CLion's marketplace, then follow CLion's [PlatformIO setup guide](https://www.jetbrains.com/help/clion/platformio.html#install). After installation you can create new PlatformIO projects from CLion's "New Project" dialog the same way you create desktop C++ projects.

---

## Anatomy of a PlatformIO project

A PlatformIO project has a `platformio.ini` file at its root that describes the target board and any libraries needed:

```ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino

lib_deps =
    arduino-libraries/Servo @ ^1.2.1
```

What each line does:

- `[env:uno]` defines a build environment named `uno`. You can have multiple environments in one project (e.g. one for an Uno, one for an ESP32) and switch between them.
- `platform` is the CPU family. `atmelavr` for classic Arduinos, `espressif32` for ESP32, etc.
- `board` is the specific board. PlatformIO supports hundreds; see their [board search](https://platformio.org/boards).
- `framework` is what kind of code you are writing. `arduino` gives you the Arduino API; `espidf` gives you ESP-IDF; some boards support both.
- `lib_deps` lists libraries to fetch automatically. PlatformIO downloads them on the next build.

Source code lives in `src/`. The Arduino sketch you would normally call `MyProject.ino` becomes `src/main.cpp`:

```cpp
#include <Arduino.h>

void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}
```

(The only practical difference from a `.ino` sketch is that you need to include `<Arduino.h>` explicitly.)

---

## The build / upload / monitor workflow

From CLion the green play button does it all. From the command line:

```bash
pio run                    # build for the default environment
pio run -t upload          # build and upload to the connected board
pio device monitor         # open a serial monitor (Ctrl+C to exit)
```

Most embedded development follows the cycle: edit, build, upload, watch the serial output, repeat.

---

## Further reading

- [PlatformIO documentation](https://docs.platformio.org/): comprehensive.
- [Supported boards](https://platformio.org/boards): searchable list.
- [PlatformIO library registry](https://registry.platformio.org/): where `lib_deps` resolves from.

PlatformIO is its own ecosystem; this chapter is just a doorway. When you start your embedded project, expect to spend an evening with PlatformIO's docs, it pays off for the rest of the project.
