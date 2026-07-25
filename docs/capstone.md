# Capstone Project: See Your Tank Run

Everything you have written so far talked to you through a console. This project gives it a window.

You take the [Tank Control System](tank_control/v1_classes.md) — the plant, the sensor, the controller, the tests — and put a **3D view** around it, using [threepp](https://github.com/markaren/threepp), a C++ library with the API of the popular JavaScript library *three.js*. When you press Run, a tank appears, water climbs it, a valve changes colour as it opens and shuts, and the level settles on the setpoint in front of you.

The point is not the graphics. The point is what happens to your simulation code when you do this: **nothing.** `Tank`, `Plant`, `PIDController` and their tests compile untouched, because they never knew where their numbers were going. That is [separation of concerns](Chapter6/soc.md) collecting on its promise, and it is much easier to believe when you can see it.

Build it in two parts:

- **Part 1** — get a window open with something moving in it: a real third-party dependency pulled in with CMake, a scene, a camera, and an animation loop (Chapters 2, 4, 5). If Part 2 feels like too much, Part 1 alone is a complete, working 3D program.
- **Part 2** — wire the view to your simulation, swap the controller while it runs, and put the numbers on screen — with the Catch2 suite from Chapter 6 still green (Chapters 5, 6).

Work the milestones in order; each adds one capability. **Try each one before revealing the solution** — the solutions are blurred; click once more to reveal.

---

## What you'll build

A vertical tank, a water column that rises and falls with `plant.level()`, a red band at the setpoint, and a valve block that runs from green (shut) to red (wide open). Press `1` and the controller becomes bang-bang, and the water visibly *chatters* around the setpoint; press `2` and the PID takes over and it glides in and settles.

A line of text across the top reads:

```
PID | level 4.87 m | setpoint 5.00 m | valve 42%
```

---

## Before you start

You need the **Version 5** tank project — the one with `include/`, `src/`, `tests/` and a `tank_lib` library. If you have not built it, work through [the five versions](tank_control/v1_classes.md) first; this project starts where that one stops.

!!! warning "The first build takes a while"

    Configuring this project downloads and compiles threepp. That needs an internet connection and takes **several minutes** the first time — far longer than the Catch2 download in Chapter 6. It is cached in your `build/` folder afterwards, so it happens once. Start the build, then read on.

!!! note "What your machine needs"

    threepp draws with **OpenGL 3.3**, which every graphics card of the last decade supports. It will not work over a Remote Desktop session or in a virtual machine without 3D acceleration — run this one on your own machine.

---

# Part 1 — A window with something in it

## Milestone 1 — Fetch threepp and open a window

*Practises: [CMake](Chapter2/cmake_intro.md#consuming-third-party-libraries), [RAII](Chapter4/raii.md)*

Add an `app/` folder next to `src/` and `tests/`, holding a `CMakeLists.txt` and a `main.cpp`. The `CMakeLists.txt` pulls threepp in with `FetchContent` and links it alongside your `tank_lib`. In `main.cpp`, create a `Canvas` (the window), a renderer, a `Scene`, and a `PerspectiveCamera`, then hand the animation loop a lambda that renders one frame.

Add `add_subdirectory(app)` to the top-level `CMakeLists.txt`.

> Hint: this is the `FetchContent_Declare` / `FetchContent_MakeAvailable` / `target_link_libraries` pattern from the CMake chapter, with `threepp::threepp` as the exported target. Turn threepp's own tests and examples **off** before fetching, or you also download its example assets.

!!! example "Run it — you should see"

    An empty window, in the colour you set as the background, that you can resize and close. Nothing else. That is the milestone.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    `app/CMakeLists.txt`:

    ```cmake
    include(FetchContent)

    set(THREEPP_BUILD_TESTS OFF)
    set(THREEPP_BUILD_EXAMPLES OFF)
    FetchContent_Declare(
        threepp
        GIT_REPOSITORY https://github.com/markaren/threepp.git
        GIT_TAG        2026-06-17    # pin a tag, never a moving branch
        GIT_SHALLOW    TRUE          # fetch only the tip — a much smaller download
    )
    FetchContent_MakeAvailable(threepp)

    add_executable(tank_rig main.cpp)
    target_link_libraries(tank_rig PRIVATE tank_lib threepp::threepp)
    ```

    `app/main.cpp`:

    ```cpp
    #include "threepp/threepp.hpp"

    using namespace threepp;

    int main() {
        Canvas canvas("Tank Rig", {{"aa", 4}});
        auto renderer = createRenderer(canvas);

        auto scene = Scene::create();
        scene->background = Color::aliceblue;

        auto camera = PerspectiveCamera::create(60, canvas.aspect(), 0.1f, 1000);
        camera->position.set(0, 5, 15);

        canvas.onWindowResize([&](WindowSize size) {
            camera->aspect = size.aspect();
            camera->updateProjectionMatrix();
            renderer->setSize(size);
        });

        canvas.animate([&] {
            renderer->render(*scene, *camera);
        });
    }
    ```

    Four things worth naming:

    - **`Canvas` is an RAII type.** It opens the window in its constructor and closes it in its destructor. There is no `canvas.close()` at the end of `main` — the same idea as `std::ofstream` in [RAII](Chapter4/raii.md).
    - **`canvas.animate(...)` takes a [lambda](lambdas.md)** and calls it once per frame until you close the window. `[&]` captures `renderer`, `scene` and `camera` by reference — safe here, because they all outlive the loop.
    - **`onWindowResize` is the [Observer pattern](Chapter6/observer.md)** in the wild: you hand the canvas a callback and it calls you back when something happens. You do not poll for resizes; you subscribe to them.
    - **`using namespace std;` is still forbidden — `using namespace threepp;` is not.** The rule from [the standard library chapter](Chapter3/standard_library.md) is about `std`, which is enormous and full of common words. A small, focused library namespace at the top of one file is normal practice.

    </div>

## Milestone 2 — Put something in the scene

*Practises: [Memory Management](Chapter5/memory.md), [Values, References & Pointers](Chapter4/types_refs_ptrs.md)*

An empty scene is not much. Add a box: build a **geometry** (the shape), a **material** (how it looks), combine them into a `Mesh`, and `add` it to the scene. Add a `DirectionalLight` and an `AmbientLight` too, or a lit material renders black. Finally, attach `OrbitControls` so you can drag to orbit the camera and scroll to zoom.

> Hint: `BoxGeometry::create(w, h, d)`, `MeshStandardMaterial::create()`, `Mesh::create(geometry, material)`. Look at what type those `create` functions hand you back — you have met it before.

!!! example "Run it — you should see"

    A lit blue box you can orbit around by dragging with the mouse.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Inside `main`, after the camera:

    ```cpp
    OrbitControls controls{*camera, canvas};

    auto light = DirectionalLight::create();
    light->position.set(10, 20, 10);
    scene->add(light);
    scene->add(AmbientLight::create(0xffffff, 0.4f));

    auto geometry = BoxGeometry::create(2, 2, 2);
    auto material = MeshStandardMaterial::create();
    material->color = Color::dodgerblue;
    auto box = Mesh::create(geometry, material);
    scene->add(box);
    ```

    **Every `create` returns a `std::shared_ptr`.** That is why `auto` is doing so much work here, and why you reach members with `->` rather than `.` — you are holding a [smart pointer](Chapter5/memory.md#smart-pointers), and `box->position` means `(*box).position` exactly as [the pointers chapter](Chapter4/types_refs_ptrs.md#pointers-to-objects) described.

    And it is a `shared_ptr`, not a `unique_ptr`, for a real reason: ownership genuinely *is* shared. Your `box` variable owns the mesh, and so does the scene you added it to. Neither can decide alone when it should be destroyed. That is the [textbook case for `shared_ptr`](Chapter5/memory.md#stdshared_ptr-shared-ownership) — and the first time in this book you have needed one rather than been shown one.

    `OrbitControls controls{*camera, canvas};` takes the camera **by reference** — note the `*` turning the `shared_ptr` back into a reference to the camera itself. `controls` does not own the camera; it steers one that lives elsewhere, which is precisely the "class observes data owned by something else" row in the [table of which to use](Chapter4/types_refs_ptrs.md#which-one-should-i-use).

    </div>

## Milestone 3 — Make it move

*Practises: [Control Statements](Chapter1/control_statements.md), [Classes](Chapter4/classes.md)*

A still picture is not a simulation. Add a `Clock`, ask it each frame how much time has passed, and rotate the box by an amount **proportional to that elapsed time**.

> Hint: `Clock clock;` before the loop, `const float dt = clock.getDelta();` as the first line inside it. Rotate by `speed * dt`, not by a fixed amount per frame.

!!! example "Run it — you should see"

    The box turning steadily.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    Clock clock;
    canvas.animate([&] {
        const float dt = clock.getDelta();
        box->rotation.y += 0.5f * dt;
        renderer->render(*scene, *camera);
    });
    ```

    **Why `* dt` and not just `+= 0.01f`?** Because frames do not arrive at a fixed rate. A fast machine might render 300 frames a second and a slow one 30, so a fixed step per frame would spin ten times faster on the fast machine. Multiplying by the *elapsed time* makes the rotation half a radian per **second** on any machine.

    That is the same reason `Tank::update` and `PIDController::compute` take a `dt` instead of assuming a step size — and it is why the next milestones can hand `clock.getDelta()` straight to code you wrote weeks ago. The animation loop is the *sense → decide → act → step* loop from [Version 1](tank_control/v1_classes.md), with a real clock driving it.

    </div>

## Milestone 4 — Build the rig from parts

*Practises: [Composition over inheritance](Chapter5/polymorphism.md#composition-over-inheritance)*

Replace the box with a tank rig, assembled from four meshes:

| Part | Shape | Notes |
|------|-------|-------|
| Shell | open-ended cylinder | transparent, `Side::Double` so you see the inside |
| Water | cylinder of height `1` | slightly narrower than the shell |
| Setpoint band | thin flat box | at `y = 5`, the target level |
| Valve | small box | above the tank |

Put all four in a `Group` and add the *group* to the scene, so the whole rig moves as one.

Make the water column **half full** for now: a cylinder built with height `1` becomes `level` metres tall when you set `scale.y = level`.

> Hint: `CylinderGeometry::create(radiusTop, radiusBottom, height, radialSegments)`; pass `openEnded = true` for the shell. `Group::create()` gives you a container you can `add` to, exactly like the scene.

!!! warning "The trap: scaling grows a shape from its middle"

    Set `water->scale.y = 4` and the cylinder does not rise from the floor — it grows *both* ways from its own centre, so half of it sinks below the tank. You have to move it up by half its height as well: `water->position.y = 4 / 2`. Get this wrong and the symptom is unmistakable: the water level moves at half speed and pokes out the bottom.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Above `main`, in an anonymous namespace so the helpers stay private to this file:

    ```cpp
    namespace {

        constexpr float tankRadius = 1.0f;
        constexpr float tankHeight = 8.0f;
        constexpr double setpoint = 5.0;

        std::shared_ptr<Mesh> createShell() {
            auto geometry = CylinderGeometry::create(tankRadius, tankRadius, tankHeight, 32, 1, true);
            auto material = MeshBasicMaterial::create();
            material->color = Color::lightgray;
            material->transparent = true;
            material->opacity = 0.25f;
            material->side = Side::Double;
            auto shell = Mesh::create(geometry, material);
            shell->position.y = tankHeight / 2;
            return shell;
        }

        std::shared_ptr<Mesh> createWater() {
            // height 1, so scale.y reads directly as metres of water
            auto geometry = CylinderGeometry::create(tankRadius * 0.97f, tankRadius * 0.97f, 1.0f, 32);
            auto material = MeshStandardMaterial::create();
            material->color = Color::dodgerblue;
            return Mesh::create(geometry, material);
        }

        std::shared_ptr<Mesh> createValve() {
            auto geometry = BoxGeometry::create(0.6f, 0.6f, 0.6f);
            auto material = MeshStandardMaterial::create();
            material->color = Color::gray;
            auto valve = Mesh::create(geometry, material);
            valve->position.y = tankHeight + 0.5f;
            return valve;
        }

        std::shared_ptr<Mesh> createMarker() {
            auto geometry = BoxGeometry::create(2.6f, 0.05f, 2.6f);
            auto material = MeshBasicMaterial::create();
            material->color = Color::crimson;
            auto marker = Mesh::create(geometry, material);
            marker->position.y = static_cast<float>(setpoint);
            return marker;
        }

    }// namespace
    ```

    And in `main`:

    ```cpp
    auto rig = Group::create();
    auto water = createWater();
    rig->add(createShell());
    rig->add(water);
    rig->add(createValve());
    rig->add(createMarker());
    scene->add(rig);

    water->scale.y = 4.f;         // 4 m of water, for now
    water->position.y = 4.f / 2;  // ...with its base on the floor
    ```

    **A scene is a tree, and that tree is composition.** `rig` *has a* shell, *has a* water column, *has a* valve. Move `rig` and every child moves with it — set `rig->position.x = 3` and the whole assembly slides sideways, still assembled, because a child's position is measured relative to its parent. That "build a bigger thing out of smaller things, each keeping its own job" is exactly what `Plant` did to `Tank` and `Valve` back in [Version 3](tank_control/v3_pid.md#a-plant-composition) — the same design idea, one in physics and one in geometry.

    The shell uses `MeshBasicMaterial` (ignores lighting — right for a transparent pane) while the water uses `MeshStandardMaterial` (is lit, so it looks solid). One `Mesh` type, different materials: [polymorphism](Chapter5/polymorphism.md) doing its job under the surface.

    Only `water` needs a named variable; the other three are added and forgotten. They stay alive because the `Group` holds a `shared_ptr` to each — the count never reaches zero.

    </div>

That is a complete, working 3D program. Commit it, then give it a brain.

---

# Part 2 — Drive it with your own code

## Milestone 5 — Plug in the simulation

*Practises: [Separation of Concerns](Chapter6/soc.md), [Polymorphism](Chapter5/polymorphism.md)*

Here is the milestone the whole project exists for. Include your own headers, create a `Plant` and a `PIDController`, and each frame: read the level, ask the controller for a valve opening, step the plant, then set the water's `scale.y` and `position.y` from the new level.

**Change nothing in `src/` or `include/`.** If you find yourself editing `Tank` or `PIDController` to make this work, stop and re-read the loop in [Version 3](tank_control/v3_pid.md) — the code you need is already there.

> Hint: the loop body is the four lines from Version 3's `main`, with `std::cout` replaced by two assignments to `water`. Your simulation works in `double` and threepp in `float`, so a `static_cast<float>` is needed at the boundary.

!!! example "Run it — you should see"

    The water starting at 2 m and climbing, easing off as it nears the red band, drifting a little past it, then settling on it — the curve you plotted from CSV in Version 3, now happening in front of you.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    At the top of `main.cpp`, alongside the threepp include:

    ```cpp
    #include "plant.hpp"
    #include "pid_controller.hpp"
    ```

    In `main`, before the loop:

    ```cpp
    Plant plant(2.0, 1.0, 0.10, 0.03);      // the same numbers as Version 3
    PIDController pid(0.8, 0.05, 0.0, setpoint);
    Controller* controller = &pid;
    ```

    And the loop:

    ```cpp
    Clock clock;
    canvas.animate([&] {
        const double dt = clock.getDelta();

        const double level = plant.level();                     // sense
        const double opening = controller->compute(level, dt);  // decide
        plant.step(opening, dt);                                // act

        water->scale.y = static_cast<float>(level);
        water->position.y = static_cast<float>(level) / 2;

        renderer->render(*scene, *camera);
    });
    ```

    **Look at what you did not have to do.** `Plant` has no idea it is being drawn. `PIDController` has no idea a window exists. Neither one gained a `#include`, a parameter, or a line of code. All that changed is *who consumes the numbers* — Version 3 printed them, this prints nothing and moves a cylinder instead.

    That is not luck. It is the payoff for a decision made back in [Version 2](tank_control/v2_sensors.md): the plant exposes a `level()` and takes a valve opening, and stops there. A `Plant` that had printed its own status, or written its own CSV, would have to be torn open now. Every time this book said "one job per class," this is the invoice being paid.

    `Controller* controller = &pid;` looks like a detour when there is only one controller — the next milestone is why it is there.

    </div>

## Milestone 6 — Swap the controller while it runs

*Practises: [Polymorphism](Chapter5/polymorphism.md), [Observer Pattern](Chapter6/observer.md)*

Create an `OnOffController` *as well* as the PID, and let a key press choose between them at runtime: `1` for on/off, `2` for PID. Register a key callback with the canvas; the callback repoints the `Controller*` and nothing else.

> Hint: `canvas.onKeyPressed(...)` takes a lambda receiving a `KeyEvent`, whose `.key` you compare against `Key::NUM_1` and `Key::NUM_2`. The loop already calls `controller->compute(...)` through the base-class pointer, so it needs no changes at all.

!!! example "Run it — you should see"

    Press `1` and the water starts sawing up and down across the red band — the valve slams fully open, fully shut, open, shut. Press `2` and the sawing damps out and the level glides back onto the setpoint.

    That chatter is the weakness [Version 1](tank_control/v1_classes.md) described in words. Here it is a thing you watch happen.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include "controller.hpp"      // Controller interface + OnOffController

    // ...

    OnOffController onOff(setpoint);
    PIDController pid(0.8, 0.05, 0.0, setpoint);
    Controller* controller = &pid;

    canvas.onKeyPressed([&](KeyEvent evt) {
        if (evt.key == Key::NUM_1) {
            controller = &onOff;
        } else if (evt.key == Key::NUM_2) {
            controller = &pid;
        }
    });
    ```

    **One line of the render loop just became the entire feature.** `controller->compute(level, dt)` runs `OnOffController::compute` or `PIDController::compute` depending on what `controller` points at *this frame* — [runtime polymorphism](Chapter5/polymorphism.md#virtual-functions), decided while the program is running rather than while it is compiling. The loop was written before either controller existed and does not mention them.

    `Controller*` is a **non-owning raw pointer**: it observes one of two objects that `main` owns and outlive it. That is the one everyday use for a raw pointer the [pointers chapter](Chapter4/types_refs_ptrs.md#which-one-should-i-use) endorses — a `unique_ptr` here would be wrong, because the pointer is not doing any owning.

    The key handler is the [Observer pattern](Chapter6/observer.md) again, and it comes with the lifetime hazard that chapter warns about: the lambda captures `onOff`, `pid` and `controller` **by reference**, and the canvas stores it. That is safe *only* because all three are locals of `main` that outlive the canvas. Capture something shorter-lived by reference and you would have a dangling callback.

    </div>

## Milestone 7 — Put the numbers on screen

*Practises: [Strings](strings.md), [IO & Streams](Chapter4/io_streams.md)*

You can see *that* it settles; now show *what* it is doing. Add a screen-space `TextSprite` reading the controller name, the level, the setpoint and the valve opening, and rebuild its text every frame with `std::format`. Colour the valve block from green (shut) to red (fully open) so it reports its own state.

> Hint: `FontLoader().defaultFont()` gives you a font with no file to load. Set `screenSpace = true` and `screenAnchor` to pin the text to a corner of the window rather than a point in the world. Track the controller's name in a `std::string` you set alongside the pointer.

!!! example "Run it — you should see"

    ```
    PID | level 4.87 m | setpoint 5.00 m | valve 42%
    ```

    and the valve block shading from green toward red as it opens.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Keep a handle to the valve mesh (`auto valve = createValve();`) so you can recolour it, and add the HUD:

    ```cpp
    FontLoader fontLoader;
    auto hud = TextSprite::create(fontLoader.defaultFont(), 22.f);
    hud->setColor(Color::black);
    hud->setVerticalAlignment(TextSprite::VerticalAlignment::Below);
    hud->screenSpace = true;
    hud->screenAnchor.set(0.f, 1.f);      // top-left of the window
    hud->position.set(10.f, -10.f, 0.f);  // 10 px in from that corner
    scene->add(hud);
    ```

    Set the name where you set the pointer:

    ```cpp
    std::string controllerName = "PID";

    canvas.onKeyPressed([&](KeyEvent evt) {
        if (evt.key == Key::NUM_1) {
            controller = &onOff;
            controllerName = "on/off";
        } else if (evt.key == Key::NUM_2) {
            controller = &pid;
            controllerName = "PID";
        }
    });
    ```

    And at the end of the loop body, before rendering:

    ```cpp
    valve->materialAs<MeshStandardMaterial>()->color.setRGB(
            static_cast<float>(opening), 1.f - static_cast<float>(opening), 0.f);

    hud->setText(std::format("{} | level {:.2f} m | setpoint {:.2f} m | valve {:.0f}%",
                             controllerName, level, setpoint, opening * 100));
    ```

    `std::format` fills each `{}` with the next argument, and `{:.2f}` asks for two decimal places — the same formatting from [IO & Streams](Chapter4/io_streams.md#formatting), and much easier here than `<iomanip>`, whose manipulators are *sticky* and would leak their settings into everything printed afterwards.

    The valve's colour is the opening, mapped onto red and green: `opening = 0` gives `(0, 1, 0)`, pure green; `opening = 1` gives `(1, 0, 0)`, pure red; anything between is a blend. One `double` you already had, turned into something you can read at a glance without looking at the text at all.

    Notice that this milestone touched **only** the display code. Presenting the numbers is one concern; producing them is another, and they still live in different files.

    </div>

## Milestone 8 — Check the tests still pass

*Practises: [Testing](Chapter6/testing.md), [CMake](Chapter2/cmake_intro.md#building-libraries)*

Run `ctest`. Every test from [Version 5](tank_control/v5_tests.md) should still be green — you have not touched the code they cover.

Then prove the suite is really guarding the thing on screen: flip the sign in `Tank::update` so the level falls when the valve opens. Rebuild. The tests go red **and** the tank drains before your eyes.

!!! example "Run it — you should see"

    ```
    100% tests passed, 0 tests failed out of 1
    ```

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Nothing to write. That is the milestone.

    ```bash
    ctest --test-dir build
    ```

    Your project now builds three targets from one source tree:

    ```mermaid
    %%{init: {'flowchart': {'curve': 'linear'}}}%%
    graph TD
        APP["tank_rig (3D app)"] -->|links| LIB["tank_lib"]
        APP -->|links| TPP["threepp::threepp (fetched)"]
        TESTS["tests"] -->|links| LIB
        TESTS -->|links| C2["Catch2 (fetched)"]
    ```

    `tank_lib` is compiled **once** and linked by both, so the tests check the very same machine code the 3D app runs — not a copy that might have drifted. That is the whole reason [the CMake chapter](Chapter2/cmake_intro.md#building-libraries) told you to build shared logic as a library rather than listing the same `.cpp` files in two `add_executable` lines.

    It also explains why the graphics never got a test. There is nothing to test: the app contains no logic worth checking, only translation from numbers to shapes. Everything that *could* be wrong lives in `tank_lib`, and `tank_lib` is covered. Push the decisions into testable code and the untestable layer becomes too thin to hurt you.

    </div>

## The complete project

??? success "Show the complete project"

    <div class="spoiler" markdown title="Click to reveal">

    **Layout** — Version 5's project, plus one folder:

    ```
    tank-rig/
    ├── CMakeLists.txt
    ├── include/            # unchanged from Version 5
    ├── src/                # unchanged from Version 5 — built as tank_lib
    ├── app/                # NEW
    │   ├── CMakeLists.txt
    │   └── main.cpp
    └── tests/              # unchanged from Version 5
    ```

    **Top-level `CMakeLists.txt`** — one new line:

    ```cmake
    cmake_minimum_required(VERSION 3.20)
    project(tank_rig)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    add_subdirectory(src)
    add_subdirectory(app)      # <-- the 3D application
    add_subdirectory(tests)
    ```

    **`app/CMakeLists.txt`**

    ```cmake
    include(FetchContent)

    set(THREEPP_BUILD_TESTS OFF)
    set(THREEPP_BUILD_EXAMPLES OFF)
    FetchContent_Declare(
        threepp
        GIT_REPOSITORY https://github.com/markaren/threepp.git
        GIT_TAG        2026-06-17
        GIT_SHALLOW    TRUE
    )
    FetchContent_MakeAvailable(threepp)

    add_executable(tank_rig main.cpp)
    target_link_libraries(tank_rig PRIVATE tank_lib threepp::threepp)
    ```

    **`app/main.cpp`**

    ```cpp
    #include "threepp/threepp.hpp"
    #include "threepp/objects/TextSprite.hpp"

    #include "controller.hpp"        // Controller interface + OnOffController
    #include "pid_controller.hpp"
    #include "plant.hpp"

    #include <format>
    #include <memory>
    #include <string>

    using namespace threepp;

    namespace {

        constexpr float tankRadius = 1.0f;
        constexpr float tankHeight = 8.0f;
        constexpr double setpoint = 5.0;

        std::shared_ptr<Mesh> createShell() {
            auto geometry = CylinderGeometry::create(tankRadius, tankRadius, tankHeight, 32, 1, true);
            auto material = MeshBasicMaterial::create();
            material->color = Color::lightgray;
            material->transparent = true;
            material->opacity = 0.25f;
            material->side = Side::Double;
            auto shell = Mesh::create(geometry, material);
            shell->position.y = tankHeight / 2;
            return shell;
        }

        std::shared_ptr<Mesh> createWater() {
            // height 1, so scale.y reads directly as metres of water
            auto geometry = CylinderGeometry::create(tankRadius * 0.97f, tankRadius * 0.97f, 1.0f, 32);
            auto material = MeshStandardMaterial::create();
            material->color = Color::dodgerblue;
            return Mesh::create(geometry, material);
        }

        std::shared_ptr<Mesh> createValve() {
            auto geometry = BoxGeometry::create(0.6f, 0.6f, 0.6f);
            auto material = MeshStandardMaterial::create();
            material->color = Color::gray;
            auto valve = Mesh::create(geometry, material);
            valve->position.y = tankHeight + 0.5f;
            return valve;
        }

        std::shared_ptr<Mesh> createMarker() {
            auto geometry = BoxGeometry::create(2.6f, 0.05f, 2.6f);
            auto material = MeshBasicMaterial::create();
            material->color = Color::crimson;
            auto marker = Mesh::create(geometry, material);
            marker->position.y = static_cast<float>(setpoint);
            return marker;
        }

    }// namespace

    int main() {

        Canvas canvas("Tank Rig", {{"aa", 4}});
        auto renderer = createRenderer(canvas);

        auto scene = Scene::create();
        scene->background = Color::aliceblue;

        auto camera = PerspectiveCamera::create(60, canvas.aspect(), 0.1f, 1000);
        camera->position.set(0, 6, 16);

        OrbitControls controls{*camera, canvas};

        auto light = DirectionalLight::create();
        light->position.set(10, 20, 10);
        scene->add(light);
        scene->add(AmbientLight::create(0xffffff, 0.4f));

        auto rig = Group::create();
        auto water = createWater();
        auto valve = createValve();
        rig->add(createShell());
        rig->add(water);
        rig->add(valve);
        rig->add(createMarker());
        scene->add(rig);

        FontLoader fontLoader;
        auto hud = TextSprite::create(fontLoader.defaultFont(), 22.f);
        hud->setColor(Color::black);
        hud->setVerticalAlignment(TextSprite::VerticalAlignment::Below);
        hud->screenSpace = true;
        hud->screenAnchor.set(0.f, 1.f);
        hud->position.set(10.f, -10.f, 0.f);
        scene->add(hud);

        canvas.onWindowResize([&](WindowSize size) {
            camera->aspect = size.aspect();
            camera->updateProjectionMatrix();
            renderer->setSize(size);
        });

        Plant plant(2.0, 1.0, 0.10, 0.03);
        OnOffController onOff(setpoint);
        PIDController pid(0.8, 0.05, 0.0, setpoint);
        Controller* controller = &pid;
        std::string controllerName = "PID";

        canvas.onKeyPressed([&](KeyEvent evt) {
            if (evt.key == Key::NUM_1) {
                controller = &onOff;
                controllerName = "on/off";
            } else if (evt.key == Key::NUM_2) {
                controller = &pid;
                controllerName = "PID";
            }
        });

        Clock clock;
        canvas.animate([&] {
            const double dt = clock.getDelta();

            const double level = plant.level();                     // sense
            const double opening = controller->compute(level, dt);  // decide
            plant.step(opening, dt);                                // act

            water->scale.y = static_cast<float>(level);
            water->position.y = static_cast<float>(level) / 2;

            valve->materialAs<MeshStandardMaterial>()->color.setRGB(
                    static_cast<float>(opening), 1.f - static_cast<float>(opening), 0.f);

            hud->setText(std::format("{} | level {:.2f} m | setpoint {:.2f} m | valve {:.0f}%",
                                     controllerName, level, setpoint, opening * 100));

            renderer->render(*scene, *camera);
        });
    }
    ```

    `Plant::valveOpening()` is not needed — the loop already has `opening` in hand, because it is the value it just computed.

    </div>

---

## Make it your own

Every extension below reuses something from the book, and every one of them belongs in `tank_lib` — with a test — rather than in `main.cpp`:

- **Show the alarm.** Flash the shell red while the level is above a limit (see [Observer Pattern](Chapter6/observer.md) — have the plant notify a callback rather than having the render loop poll it).
- **Add sensor noise.** Draw the level through a `NoisySensor` that adds a small wobble ([Random Numbers](random.md)) and watch the controller fight it. Use a fixed seed so the run repeats.
- **Draw the history.** Keep the last few hundred levels in a `std::vector` and draw them as a `Line` — a live strip chart beside the tank.
- **Cascade a second tank.** The first tank's outflow feeds the second. Two `Plant`s, two rigs, `rig->position.x` apart.
- **Add a state machine.** *Filling → Holding → Draining → Fault*, with the shell's colour showing the state ([Enumerations](Chapter1/enums.md) and a `switch`).
- **Drag the setpoint.** Let the mouse move the red band and feed the new value to the controller.

For a bigger jump, keep the architecture and change the machine: a **robot arm** (a chain of `Group`s, each rotating about its own joint — the scene graph doing the work), a **conveyor sorter**, or a **lift**. The plant–controller–loop skeleton does not change; only the physics and the shapes do.

---

## Summary

- A 3D view is just another **consumer** of your simulation's numbers. The simulation should not know it exists, and if you built it as this book taught, it does not — that is why Milestone 5 required no edits to `src/`.
- Pulling in a real dependency is four lines of CMake: `FetchContent_Declare`, `FetchContent_MakeAvailable`, then link the target it exports. **Pin a tag**, and turn off the parts of it you do not need.
- A scene graph is **composition**: a group *has* children, a child's transform is relative to its parent, and moving the parent moves the lot.
- `create` returning a `shared_ptr` is genuine shared ownership — your variable and the scene are both owners, and neither decides alone when the object dies.
- A base-class pointer chosen by a key press is **runtime polymorphism** you can watch: on/off chatters, PID settles, and the loop that runs them both never changed.
- Multiply by `dt`, never by "per frame." Frames are not a unit of time.
- The library is compiled once and linked by both the app and the tests, so what you tested is what you ran.
