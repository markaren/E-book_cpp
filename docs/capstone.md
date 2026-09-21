# Capstone Project: See Your Tank Run

Everything you have written so far talked to you through a console. This project gives it a window.

You take the [Tank Control System](tank_control/v1_classes.md) — the plant, the sensor, the controller, the tests — and put a **3D view** around it, using [threepp](https://github.com/markaren/threepp), a C++ library with the API of the popular JavaScript library *three.js*. When you press Run, a tank appears, water climbs it, a valve changes colour as it opens and shuts, and the level settles on the setpoint in front of you.

The point is not the graphics. The point is what you have to change in your simulation code to plug it in: **nothing.** `Tank`, `Plant`, `PIDController` and their tests compile untouched, because they never knew where their numbers were going. That is [separation of concerns](Chapter6/soc.md) paying off, and it is much easier to believe when you can see it. What happens when the simulation *runs* inside a real animation loop is another story, and finding that out is part of the project.

!!! info "Using this page in a course"

    The milestones get you a working base. What you build beyond them, and how well you show and explain how you worked, is your project. If you are taking AIS1003, your portfolio brief (*mappeoppgaven*) says what to hand in and how it is assessed.

Build it in two parts:

- **Part 1** — get a window open with something moving in it: a real third-party dependency pulled in with CMake, a scene, a camera, and an animation loop. Part 1 needs no tank code at all, so you can start it before the tank project is finished.
- **Part 2** — bring in your Version 5 tank project, wire the view to the simulation, find out why it does not work the first time, swap the controller while it runs, and put the numbers on screen — with the Catch2 suite still green.

After that comes the part that is yours: an [extension](#your-extension) you choose and design, and a README that [presents what you built](#present-your-project).

Work the milestones in order; each adds one capability. **Try each one before revealing the solution** — the solutions are blurred; click once more to reveal. If you do reveal one, type it rather than paste it, and note in your log what you were stuck on.

---

## What you'll build

A vertical tank, a water column that rises and falls with the plant's level, a red band at the setpoint, and a valve block that runs from green (shut) to red (wide open). Press `1` and the controller becomes on/off; press `2` and the PID takes over. What the difference looks like at 60 frames a second is something you will find out in Milestone 6.

A line of text across the top reads:

```
PID | level 4.87 m | setpoint 5.00 m | valve 70%
```

---

## How to work on this project

How you get there matters as much as where you end up, and it is easy to leave no trace of it. Four habits, from the first milestone:

- **Commit after every milestone**, and whenever something starts working, with a message that says *why* ([Saving your work](Chapter2/version_control.md#saving-your-work-a-commit)). Your history is the diary of the project; a single "final version" commit tells nobody anything. **Push** at the end of every session — **Commit and Push...** in CLion's commit dialog — so the history is backed up on GitHub, not only on your laptop. When you reach a point worth remembering — Part 1 running, the core finished, your extension working — put a [tag](Chapter2/version_control.md#tags-naming-a-commit) on it, with a few lines about what works, what was hard, and what you plan next.
- **Keep a log.** A file `LOG.md` in the project's top folder, next to the top-level `CMakeLists.txt`, with one short entry per work session. There is a worked example after Milestone 4. This template is enough:

    ```markdown
    ### <date> — <what you worked on> (<time spent>)
    **Predicted:** <only if you predicted something before running>
    **Tried:**
    **Happened:**
    **Why I think:**
    **How I checked:**
    **Changed:** <what, and the commit>
    **Next:**
    ```

- **Predict before you run.** Where a milestone has a *Before you run* box, write your prediction in your log and **commit it before you run** — then your history shows what you expected before you saw what happened. A wrong prediction costs nothing; working out why it was wrong is where the learning is.
- **Capture as you go.** Take a screenshot, or record a short GIF, whenever something works — or breaks in an interesting way. You will want them for your [README](#present-your-project), and you cannot capture a bug after you have fixed it.

When you are stuck, go in this order: the [four tools for "something is wrong"](debugger.md#four-tools-for-something-is-wrong), then [Reading Compiler Errors](compiler_errors.md), then [Using AI for Coding](using_ai.md). If you ask an AI, write down what you asked and what you kept.

---

## Before you start

- **Part 1** needs [CMake](Chapter2/cmake_intro.md) and [Git](Chapter2/version_control.md) (Chapter 2), [lambdas](lambdas.md) (Chapter 3), [classes](Chapter4/classes.md), [references and pointers](Chapter4/types_refs_ptrs.md) and [RAII](Chapter4/raii.md) (Chapter 4), and [smart pointers](Chapter5/memory.md#smart-pointers) (Chapter 5). It does **not** need the tank project. A few explanations in the solutions point ahead — to polymorphism, the Observer pattern and the tank project. If you have not reached those yet, skip those paragraphs; the code does not depend on them.
- **Part 2** needs the finished **Version 5** tank project — the one with `include/`, `src/`, `app/`, `tests/` and a `tank_lib` library — and so the rest of Chapters 5 and 6. If you have not built it, work through [the five versions](tank_control/v1_classes.md) first.

!!! warning "The first build takes a while"

    The first time CMake configures this project it **downloads** threepp (about 200 MB — you need an internet connection), and the first build **compiles** it, which takes **several minutes**. Start the build, then read on. It happens once per build folder: CLion keeps one folder per profile (`cmake-build-debug`, `cmake-build-release`), so adding a profile, choosing **Tools → CMake → Reset Cache and Reload Project**, or deleting the folder starts it over.

!!! tip "Run the 3D app from a Release profile"

    In the Debug profile, every change to `main.cpp` relinks a very large executable against a very large Debug build of threepp — over a minute each time, long enough to think CLion has hung. A Release build does the same in a few seconds. Add one under **File → Settings → Build, Execution, Deployment → CMake** (click **+**; CLion suggests *Release*), then pick it in the profile switcher next to the Run button. Switch back to Debug when you need the [debugger](debugger.md) — and in Milestone 5, you will ([Debug and Release](Chapter2/cmake_intro.md#build-configurations-debug-and-release)).

!!! note "What your machine needs"

    threepp draws with **OpenGL 3.3**, which every graphics card of the last decade supports. It will not work over a Remote Desktop session or in a virtual machine without 3D acceleration — run this one on your own machine.

??? question "If the first configure or build fails"

    - **The download fails** ("could not resolve host", "failed to clone"): no internet, or a network that wants you to log in first — open a web page in a browser, then **Reload CMake Project**.
    - **"git not found"**: CMake uses Git to download threepp. Install Git for Windows from <https://git-scm.com/downloads> (the default options are fine) and restart CLion.
    - **Strange path errors**: the project is inside OneDrive, or its path has spaces or `æ`, `ø`, `å` — see [Getting Started](getting_started.md#2-create-your-first-project).
    - **A window that never appears**, or an error about OpenGL: you are on Remote Desktop or in a virtual machine (see the box above).

---

# Part 1 — A window with something in it

## Milestone 1 — Fetch threepp and open a window

*Practises: [CMake](Chapter2/cmake_intro.md#consuming-third-party-libraries), [RAII](Chapter4/raii.md), [Lambdas](lambdas.md)*

1. In CLion, create a new **C++ Executable** project called `tank-rig` in a plain folder such as `C:\dev\tank-rig` ([Getting Started](getting_started.md#2-create-your-first-project)).
2. **Put it under Git** before the first build: open the **Terminal** tab at the bottom of CLion (it opens in the project folder) and type `git init` ([Starting a new project](Chapter2/version_control.md#starting-a-new-project)). Then right-click `tank-rig` at the top of the **Project** panel → **New → File**, name it `.gitignore`, and write two lines in it: `cmake-build-*/` and `.idea/` ([What to put in `.gitignore`](Chapter2/version_control.md#what-to-put-in-gitignore)). Create an empty repository on GitHub and connect it over SSH ([Put a local project on GitHub](Chapter2/version_control.md#getting-a-project)).
3. Right-click `tank-rig` → **New → Directory**, name it `rig`, and drag `main.cpp` into it (confirm the **Move** dialog).
4. Replace everything in the top-level `CMakeLists.txt` with a short file that sets C++20 and adds the `rig` folder ([Splitting the build across folders](Chapter2/cmake_intro.md#splitting-the-build-across-folders)). Then right-click `rig` → **New → File**, name it `CMakeLists.txt`, and make it pull threepp in with `FetchContent` and build an executable `tank_rig` from `main.cpp`.
5. **Reload CMake** — click the reload icon CLion shows over the editor ([CMake in CLion](Chapter2/cmake_intro.md#cmake-in-clion)). Until you do, CLion may say `main.cpp` does not belong to any project target; that is expected. This reload is the one that downloads threepp, and the **CMake** window at the bottom can show nothing new for several minutes. Wait until it prints `Build files have been written to`.
6. In `rig/main.cpp`, create a `Canvas` (the window), a `GLRenderer`, a `Scene` with a background colour, and a `PerspectiveCamera`, then hand the animation loop a lambda that renders one frame.

> Hint: the CMake part is the `FetchContent_Declare` / `FetchContent_MakeAvailable` / `target_link_libraries` pattern from the CMake chapter, with `threepp::threepp` as the target threepp exports. Turn threepp's own tests and examples **off** before fetching, or you build those too and download its example assets.
>
> The threepp names — `Canvas`, `Scene`, `canvas.animate`, the option names — you cannot guess from anything in this book. Look at one of threepp's examples ([Finding things out yourself](#finding-things-out-yourself)), or open the solution and type it in; in Milestone 1 that is expected. One warning when you borrow from an example: threepp's examples create their renderer with `auto renderer = createRenderer(canvas);`, which at this version stops and **asks on the console** which renderer to use before anything is drawn. Write `GLRenderer renderer(canvas);` instead, and `renderer.` wherever the example writes `renderer->`.

!!! example "Run it — you should see"

    An empty window in the background colour you chose, that you can resize and close. Nothing else. That is the milestone. Commit it — the commit should hold only `.gitignore`, the two `CMakeLists.txt` files and `rig/main.cpp`; if you see files from `cmake-build-debug`, your `.gitignore` is not working — and push.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    `CMakeLists.txt` (top level):

    ```cmake
    cmake_minimum_required(VERSION 3.20)
    project(tank_rig)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    add_subdirectory(rig)      # the 3D view
    ```

    `rig/CMakeLists.txt`:

    ```cmake
    include(FetchContent)

    set(THREEPP_BUILD_TESTS OFF)
    set(THREEPP_BUILD_EXAMPLES OFF)
    FetchContent_Declare(
        threepp
        GIT_REPOSITORY https://github.com/markaren/threepp.git
        GIT_TAG        2026-06-17    # pin a tag, never a moving branch
        GIT_SHALLOW    TRUE          # fetch only the latest commits, not the whole history
    )
    FetchContent_MakeAvailable(threepp)

    add_executable(tank_rig main.cpp)
    target_link_libraries(tank_rig PRIVATE threepp::threepp)
    ```

    `rig/main.cpp`:

    ```cpp
    #include "threepp/threepp.hpp"

    using namespace threepp;

    int main() {
        Canvas canvas("Tank Rig");
        GLRenderer renderer(canvas);

        auto scene = Scene::create();
        scene->background = Color::aliceblue;

        auto camera = PerspectiveCamera::create(60, canvas.aspect(), 0.1f, 1000);
        camera->position.set(0, 5, 12);

        canvas.onWindowResize([&](WindowSize size) {
            camera->aspect = size.aspect();
            camera->updateProjectionMatrix();
            renderer.setSize(size);
        });

        canvas.animate([&] {
            renderer.render(*scene, *camera);
        });
    }
    ```

    Things worth naming:

    - **`set(THREEPP_BUILD_TESTS OFF)` before `FetchContent_MakeAvailable`** overrides the default of an [`option()`](Chapter2/cmake_intro.md#cmake-options-making-parts-of-the-build-optional) that threepp declares: when threepp's own `CMakeLists.txt` runs, it finds your value already set and uses it.
    - **`Canvas` owns the window.** When `canvas` is destroyed at the end of `main`, the window is closed and its resources released — you never clean up by hand, the same idea as `std::ofstream` in [RAII](Chapter4/raii.md). `GLRenderer` draws into that window and cleans up after itself the same way.
    - **Construct `GLRenderer` yourself, as here** — not with the `createRenderer(canvas)` helper threepp's examples use, which at this version waits for an answer on the console before anything is drawn.
    - **`Scene::create()` and `PerspectiveCamera::create()` hand you smart pointers**, which is why you write `scene->` and `*scene`. Milestone 2 says which kind, and why.
    - **`canvas.animate(...)` takes a [lambda](lambdas.md)** and calls it once per frame until you close the window. `[&]` captures `renderer`, `scene` and `camera` by reference — safe here, because they all outlive the loop.
    - **`onWindowResize` takes a callback**: you hand the canvas a function and it calls you back when something happens. You do not poll for resizes; you subscribe to them. (Chapter 6 calls this the [Observer pattern](Chapter6/observer.md).)
    - **`using namespace std;` is still forbidden; `using namespace threepp;` in this one `.cpp` file is a deliberate exception.** threepp's namespace is not small — it holds hundreds of names, many of them common words like `Color`, `Clock` and `Group` — so the reasoning in [the standard library chapter](Chapter3/standard_library.md) applies to it too. It is acceptable here because it sits in a single source file (never a header), you use threepp names on almost every line, and none of them clash with yours. If one ever does, the compiler says the name is *ambiguous*: rename your own class, or remove the `using namespace threepp;` line from that file and write `threepp::` in front of threepp's names.

    </div>

## Milestone 2 — Put something in the scene

*Practises: [Memory Management](Chapter5/memory.md), [Values, References & Pointers](Chapter4/types_refs_ptrs.md)*

An empty scene is not much. Add a box: build a **geometry** (the shape), a **material** (how it looks), combine them into a `Mesh`, and `add` it to the scene. Add a `DirectionalLight` and an `AmbientLight` too, or a lit material renders black. Finally, attach `OrbitControls` so you can drag to orbit the camera and scroll to zoom.

> Hint: `BoxGeometry::create(w, h, d)`, `MeshStandardMaterial::create()`, `Mesh::create(geometry, material)`. Hold **Ctrl** and click `BoxGeometry::create` to open its declaration: what else could you pass it? And look at what type those `create` functions hand you back — you have met it before.

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
    scene->add(AmbientLight::create(0xffffff, 0.4f));   // white light at 40 % strength

    auto geometry = BoxGeometry::create(2, 2, 2);
    auto material = MeshStandardMaterial::create();
    material->color = Color::dodgerblue;
    auto box = Mesh::create(geometry, material);
    scene->add(box);
    ```

    **Every `create` returns a `std::shared_ptr`.** That is why `auto` is doing so much work here, and why you reach members with `->` rather than `.` — you are holding a [smart pointer](Chapter5/memory.md#smart-pointers), and `box->position` means `(*box).position` exactly as [the pointers chapter](Chapter4/types_refs_ptrs.md#pointers-to-objects) described.

    It is a `shared_ptr` because **threepp chose shared ownership**: `scene->add(box)` stores a second `shared_ptr` to the same mesh, so the scene keeps everything you add to it alive, and your `box` variable is simply another owner. Neither one alone decides when the mesh is destroyed — the last owner to let go does, as in [shared ownership](Chapter5/memory.md#stdshared_ptr-shared-ownership). You will meet a case where the sharing really matters in Milestone 6.

    `OrbitControls controls{*camera, canvas};` takes the camera **by reference** — note the `*` turning the `shared_ptr` back into the camera itself. `controls` borrows the camera and steers it; it does not own it, and it must not outlive it. Here both live until the end of `main`.

    </div>

## Milestone 3 — Make it move

*Practises: [Lambdas](lambdas.md), [Version 1's loop](tank_control/v1_classes.md)*

A still picture is not a simulation. Add a `Clock`, ask it each frame how much time has passed, and rotate the box by an amount **proportional to that elapsed time**.

> Hint: `Clock clock;` before the loop, `const float dt = clock.getDelta();` as the first line inside it. Rotate by `speed * dt`, not by a fixed amount per frame.

!!! question "Before you run"

    Suppose you rotated the box by a fixed `0.01f` every frame instead. The loop runs once per screen refresh. How fast would the box turn on a 60 Hz monitor, and on a 144 Hz one? Write it down, then read the explanation in the solution.

!!! example "Run it — you should see"

    The box turning steadily.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    Clock clock;
    canvas.animate([&] {
        const float dt = clock.getDelta();
        box->rotation.y += 0.5f * dt;
        renderer.render(*scene, *camera);
    });
    ```

    **Why `* dt` and not just `+= 0.01f`?** Because frames do not arrive at a fixed rate. The loop runs once per screen refresh, so a 144 Hz monitor delivers 144 frames a second and a 60 Hz one 60 — and a heavy scene on a slow machine delivers fewer. A fixed step per frame would spin more than twice as fast on the 144 Hz screen. Multiplying by the *elapsed time* makes the rotation half a radian per **second** on any machine.

    That is the same reason `Tank::update` and `PIDController::compute` take a `dt` instead of assuming a step size — and it is why Part 2 can hand `clock.getDelta()` to code you wrote weeks ago. The animation loop is the *sense → decide → act → step* loop from [Version 1](tank_control/v1_classes.md), with a real clock driving it.

    </div>

## Milestone 4 — Build the rig from parts

*Practises: [Functions](Chapter1/functions.md), composition ([Version 3](tank_control/v3_pid.md#a-plant-composition))*

Replace the box and its rotation with a tank rig, assembled from four meshes:

| Part | Shape | Notes |
|------|-------|-------|
| Shell | open-ended cylinder, 8 m tall | transparent, `Side::Double` so you see the inside |
| Water | cylinder of height `1` | slightly narrower than the shell |
| Setpoint band | thin flat box | at `y = 5`, the target level |
| Valve | small box | above the tank |

Write one small function per part that builds and returns its mesh. Put all four in a `Group` and add the *group* to the scene, so the whole rig moves as one.

Make the water **4 m deep** for now: a cylinder built with height `1` becomes `level` metres tall when you set `scale.y = level`.

The camera still looks at the origin — the floor of the tank. Point `OrbitControls` at the middle of the tank instead: set `controls.target` and call `controls.update()`.

> Hint: `CylinderGeometry::create` builds the cylinders. The shell needs its ends *open* — Ctrl+click `create` and find the parameter that does that. You will see parameters written like `unsigned int heightSegments = 1`: that `= 1` is a **default argument**. If your call stops before that parameter, the compiler fills in the value after the `=`. You can only leave arguments off at the right-hand end, and C++ has no named arguments, so to reach a parameter you must pass every parameter before it, in order. `create(1, 1, 8, 32, true)` compiles without a warning, but that `true` does not land where you think. `Group::create()` gives you a container you can `add` to, exactly like the scene.

!!! example "Run it — you should see"

    A see-through tank, 4 m of blue water standing on its floor, a red band across it at 5 m, and a grey block above it — all in view, and orbiting around the middle of the tank when you drag.

??? warning "Stuck? The water pokes out of the bottom"

    Set `water->scale.y = 4` and the cylinder does not rise from the floor — it grows *both* ways from its own centre, so half of it sinks below the tank and its top sits at 2 m, not 4 m. Move it up by half its height as well: `water->position.y = 4.f / 2`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Between `using namespace threepp;` and `main`:

    ```cpp
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
    ```

    `CylinderGeometry::create(radiusTop, radiusBottom, height, radialSegments, heightSegments, openEnded)`: the shell passes `1` for `heightSegments` so that `true` lands on `openEnded`. In the tempting `create(1, 1, 8, 32, true)`, the `true` becomes `heightSegments = 1` and the shell keeps its end caps.

    And in `main` — the controls line is already there from Milestone 2; add the two lines after it:

    ```cpp
    OrbitControls controls{*camera, canvas};
    controls.target.set(0, tankHeight / 2, 0);   // orbit around the middle of the tank
    controls.update();

    // ...lights as before...

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

    The loop goes back to just `renderer.render(*scene, *camera);`.

    **A scene is a tree: a group *has* children.** `rig` has a shell, a water column, a valve. Move `rig` and every child moves with it — set `rig->position.x = 3` and the whole assembly slides sideways, still assembled, because a child's position is measured relative to its parent. That "build a bigger thing out of smaller things, each keeping its own job" is exactly what `Plant` did with `Tank` and `Valve` back in [Version 3](tank_control/v3_pid.md#a-plant-composition) — the same design idea, one in physics and one in geometry.

    The shell uses `MeshBasicMaterial` (ignores lighting — right for a transparent pane) while the water uses `MeshStandardMaterial` (is lit, so it looks solid). `Mesh` holds its material through a pointer to the `Material` base class, so any kind of material plugs in — substitution through a base-class pointer, as in [Polymorphism](Chapter5/polymorphism.md). (Which shader draws it is then decided inside the renderer.)

    Only `water` needs a named variable; the other three are added and forgotten. They stay alive because the `Group` holds a `shared_ptr` to each.

    </div>

### What a log entry looks like

The water trap above makes a good first log entry. Something like this — about a hundred words, in your own words, about what happened on your machine:

```markdown
### 14 Oct — Milestone 4, the water column (1.5 h)
**Tried:** built the water as a height-1 cylinder and set `water->scale.y = 4`.
**Happened:** the water stuck out below the floor; its top was at 2 m, not 4 m.
Screenshot: docs/images/m4_water_below.png
**Why I think:** the cylinder may grow from its centre, not its bottom.
**How I checked:** tried `scale.y = 2`, then `6` — the bottom moved down as far as the top moved up.
**Changed:** `water->position.y = 4.f / 2` (half its height) — commit 3f2a9c1
("Lift water by half its height so it grows from the floor").
**Next:** drive the level from the plant (Milestone 5).
```

An exact observation, a guess, a small experiment that tests the guess, and a fix with a *why* in its commit message. That is what "showing your process" means.

Part 1 is a complete 3D program on its own — a good place to commit, take a screenshot, put a tag on it, and look back at what you have built.

---

# Part 2 — Drive it with your own code

## Milestone 5 — Plug in the simulation

*Practises: [Separation of Concerns](Chapter6/soc.md), [Polymorphism](Chapter5/polymorphism.md), [Using a Debugger](debugger.md)*

Here is the milestone the whole project exists for.

1. **Bring in your Version 5 project.** Commit Part 1 first. Then copy only these four folders from your Version 5 project into `tank-rig`, next to `rig/`: `include/`, `src/`, `app/` and `tests/`. Leave Version 5's own top-level `CMakeLists.txt` behind — `tank-rig` keeps its own, and step 2 extends it — and leave its `.git`, `.idea` and `cmake-build-*` folders behind too. Commit the four folders in a commit of their own, with nothing else in it. In the commit dialog, tick **Unversioned Files** so every copied file goes in, and start the message with `Import:` — for example `Import: my Version 5 tank project (include, src, app, tests)`. Everything after that commit is new work, and anyone reading your history can see exactly where it starts.
2. **Wire up the build.** In the top-level `CMakeLists.txt`, add `src`, `app` and `tests` next to `rig`. Do not add `include`: it has no `CMakeLists.txt` of its own, and `src/CMakeLists.txt` already points `tank_lib` at it. Turn on testing with `include(CTest)` *at the top level*, so `ctest` finds the tests from your build folder. In `rig/CMakeLists.txt`, link `tank_lib` as well as threepp. Reload CMake (this reload downloads Catch2).
3. **Drive the water.** Include your headers, create a `Plant`, a `LevelSensor` reading it, and a `PIDController`, and point a `Controller*` at the PID — Version 4 used a `Controller&`, but Milestone 6 needs something it can re-point. Each frame: read the sensor, ask the controller for a valve opening, step the plant, then set the water's `scale.y` and `position.y` from the plant's level. The two "for now" water lines from Milestone 4 can go; the loop sets the water from now on.

**To plug it in, change nothing in `src/` or `include/`.** If you find yourself editing `Tank` or `PIDController` to make this *compile*, stop and re-read the loop in [Version 4](tank_control/v4_project.md) — the code you need is already there.

> Hint: the loop body is the sense / decide / act lines from Version 4's `main`, with `std::cout` replaced by two assignments to `water`. Your simulation works in `double` and threepp in `float`; write a `static_cast<float>` at the boundary so the narrowing is visible (the compiler would do it silently).

!!! example "Run it — what you will actually see"

    The shell, the red band and the valve — and **no water at all**, not even the 2 m the tank starts with. It does not come back. If that is what you see, your code is probably right. Read on.

    (If your water *does* appear, your Version 5 already copes with what goes wrong here. Do the bug hunt below anyway, find the line in your code that saves you, and write it up in your log.)

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    `CMakeLists.txt` (top level):

    ```cmake
    cmake_minimum_required(VERSION 3.20)
    project(tank_rig)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    include(CTest)             # at the top level, so ctest finds the tests from the build folder

    add_subdirectory(src)      # tank_lib
    add_subdirectory(app)      # the console program from Version 5
    add_subdirectory(tests)
    add_subdirectory(rig)      # the 3D view
    ```

    In `rig/CMakeLists.txt`, the link line becomes:

    ```cmake
    target_link_libraries(tank_rig PRIVATE tank_lib threepp::threepp)
    ```

    At the top of `rig/main.cpp`, alongside the threepp include:

    ```cpp
    #include "level_sensor.hpp"
    #include "pid_controller.hpp"
    #include "plant.hpp"
    ```

    In `main`, before the loop:

    ```cpp
    Plant plant(2.0, 1.0, 0.10, 0.03);       // the same numbers as Version 3
    LevelSensor sensor(plant);
    PIDController pid(0.8, 0.05, 0.0, setpoint);
    Controller* controller = &pid;
    ```

    And the loop:

    ```cpp
    Clock clock;
    canvas.animate([&] {
        const double dt = clock.getDelta();

        const double measurement = sensor.read();                     // sense
        const double opening = controller->compute(measurement, dt);  // decide
        plant.step(opening, dt);                                      // act

        const auto level = static_cast<float>(plant.level());
        water->scale.y = level;
        water->position.y = level / 2;

        renderer.render(*scene, *camera);
    });
    ```

    **Look at what you did not have to do.** `Plant` has no idea it is being drawn. `PIDController` has no idea a window exists. Neither one gained a `#include`, a parameter, or a line of code. All that changed is *who consumes the numbers* — Version 4 printed them; this prints nothing and moves a cylinder instead.

    That is the payoff of a decision made back in [Version 3](tank_control/v3_pid.md#a-plant-composition): the plant exposes a `level()` and takes a valve opening, and stops there. A `Plant` that printed its own status, or wrote its own CSV, would have to be torn open now. And because the loop reads the level through a `LevelSensor` rather than asking the plant directly, a noisy or faulty sensor is still a one-line swap — the point of [Version 2](tank_control/v2_sensors.md).

    `Controller* controller = &pid;` looks like a detour when there is only one controller — Milestone 6 is why it is there.

    </div>

### Bug hunt: where did the water go?

Your simulation passed every Version 5 test, and you changed nothing in it. Something about its new consumer is different. Find out what — the hints go from gentle to specific — and **log how you found it**, with a screenshot of what you saw: this is the best log entry of the whole project. If the hints are not enough, open the fix options — that is allowed. Write in your log that you did, and what you still had to work out yourself: where to put the fix, and why.

??? tip "Hint 1 — the tool"

    It builds and runs but does the wrong thing, so reach for the **debugger** ([four tools](debugger.md#four-tools-for-something-is-wrong)). Switch to the Debug profile — its first build compiles threepp again, which takes several minutes. Put a breakpoint on the first line inside the `animate` lambda and start with **Debug**. At the breakpoint nothing below it has run yet, so `measurement` and `opening` show leftover garbage: press **Step Over** and read each value just after its line has run. On the *second* frame `dt` is large, because it includes the time you spent paused — that is not the bug. Look hard at the first frame.

??? tip "Hint 2 — the place"

    On the very first frame, **Step Into** `controller->compute` and watch every local variable. Two of them are not normal numbers: one is infinite, and the next one computed from it is not a number at all — your Kd is 0, so what is 0 × infinity? [Floating-Point Pitfalls](floating_point.md#nan-infinity-and-division-by-zero) says what that does to everything computed from it, and why the clamps in `PIDController` and `Valve` do not stop it.

    Then ask why `dt` was exactly `0` on the first frame. Ctrl+click `getDelta`: that opens only its declaration in `Clock.hpp`. Ctrl+click the name there again to reach `Clock.cpp`, where `Clock` hands the work to a hidden helper object (`pimpl_`). Follow `getDelta` once more and read what it does the first time you call it. ([Finding things out yourself](#finding-things-out-yourself) says where threepp's files live.)

??? tip "Hint 3 — the decision"

    The fix is one or two lines. The question is *where* they go: in the loop in `rig/main.cpp`? In `PIDController::compute`? In `Valve`, or in how the loop gets its time step? Which layer should refuse a time step of zero — or a value that is not a number? Which choice protects the *next* program that uses `tank_lib`? Which one keeps this milestone's "change nothing in `src/`" promise, and is that promise still worth keeping? If you put the fix in `tank_lib`, write the Catch2 test first and watch it fail.

??? success "Fix options — open after you have logged your attempt"

    <div class="spoiler" markdown title="Click to reveal">

    **In the app** — only step the simulation when time has actually passed:

    ```cpp
    const double dt = clock.getDelta();
    if (dt > 0.0) {
        const double measurement = sensor.read();                     // sense
        const double opening = controller->compute(measurement, dt);  // decide
        plant.step(opening, dt);                                      // act
    }
    ```

    **In the library** — let `PIDController::compute` cope with a zero step, and prove it with a test. In `src/pid_controller.cpp`, the derivative line becomes:

    ```cpp
    double derivative = (dt > 0.0) ? (error - previousError_) / dt : 0.0;   // a zero step has no rate of change
    ```

    and in `tests/test_tank.cpp` (add `#include <cmath>` at the top):

    ```cpp
    TEST_CASE("PID gives a finite opening for a zero time step") {
        PIDController pid(0.8, 0.05, 0.0, 5.0);
        REQUIRE(std::isfinite(pid.compute(2.0, 0.0)));
    }
    ```

    These are not the only places. `Valve::setOpening` could refuse a `NaN`; the loop could hand the simulation a fixed step instead of the clock's; threepp's own example regulator (`examples/libs/utility/Regulator.hpp`) replaces a zero `dt` with a tiny positive number, `std::numeric_limits<float>::min()` (about 10⁻³⁸) — is that a good idea? Each choice protects a different set of callers. Which one is right for your project is your decision, and a good one to explain in your README.

    </div>

With the fix in and the book's gains (0.8 and 0.05), the water starts at 2 m and climbs about 7 cm a second. That is Version 3's curve played in real time — one Version 3 step was one second — so give it time: just under 50 seconds to reach the red band, a small overshoot to about 5.2 m some fifteen seconds later, and roughly two minutes to settle on the band.

## Milestone 6 — Swap the controller while it runs

*Practises: [Polymorphism](Chapter5/polymorphism.md), [Observer Pattern](Chapter6/observer.md), [Values, References & Pointers](Chapter4/types_refs_ptrs.md)*

Create an `OnOffController` *as well* as the PID, and let a key press choose between them at runtime: `1` for on/off, `2` for PID. Register a key callback with the canvas; the callback repoints the `Controller*` and nothing else.

So you can see what the controller is doing, colour the valve block from green (shut) to red (fully open). To do that you need a handle to the valve's material: create the material in `main`, and change `createValve` to take it as a parameter.

> Hint: `canvas.onKeyPressed(...)` takes a lambda receiving a `KeyEvent`, whose `.key` you compare against `Key::NUM_1` and `Key::NUM_2` — the digit keys on the top row. The number pad will not work: at this version threepp reports its keys as `Key::UNKNOWN`. The loop already calls `controller->compute(...)` through the base-class pointer, so the swap needs no change to it. (If your loop still uses a `Controller&` from Version 4, change it to a pointer first: `controller = onOff;` on a reference compiles, but the reference still refers to the PID, so nothing switches — see [References](Chapter4/types_refs_ptrs.md#references).)
>
> For the colour you need the opening *after* the sense / decide / act lines. If your first-frame fix put them inside `if (dt > 0.0) { ... }`, an `opening` declared inside those braces is gone after the closing `}`. So declare `double opening = 0.0;` before `canvas.animate(...)`, and change the decide line to `opening = controller->compute(measurement, dt);` with **no** `const double` in front. Leave `const double` there and you create a second, separate `opening` inside the braces: the compiler says nothing, and the valve stays green.

!!! question "Before you press 1"

    Write down in your log — and commit — what you expect the **water** and the **valve** to do under on/off control. [Version 1](tank_control/v1_classes.md) described it. Then let the level settle, press `1`, and watch both for half a minute; press `2` and watch again. If what you see is not what you predicted, ask what changed between Version 1's loop and this one.

!!! example "Run it — you should see"

    The valve block's colour showing the opening — green when shut, red when wide open, a blend in between — and keys `1` and `2` switching the controller while the program runs. What the water and the valve do under each controller is your observation to make.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include "controller.hpp"      // Controller interface + OnOffController
    ```

    The valve now takes its material from the caller:

    ```cpp
    std::shared_ptr<Mesh> createValve(std::shared_ptr<MeshStandardMaterial> material) {
        auto geometry = BoxGeometry::create(0.6f, 0.6f, 0.6f);
        auto valve = Mesh::create(geometry, material);
        valve->position.y = tankHeight + 0.5f;
        return valve;
    }
    ```

    In `main`, the valve gets its material:

    ```cpp
    auto valveMaterial = MeshStandardMaterial::create();
    rig->add(createValve(valveMaterial));   // instead of createValve()
    ```

    The controller lines from Milestone 5 become:

    ```cpp
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

    double opening = 0.0;  // the valve starts shut
    Clock clock;
    canvas.animate([&] {
        const double dt = clock.getDelta();

        // sense, decide, act: as in Milestone 5, with your first-frame fix,
        // except that the decide line now assigns to the opening declared above:
        //     opening = controller->compute(measurement, dt);   // no "const double" in front

        // ...the water, as before...

        valveMaterial->color.setRGB(static_cast<float>(opening), 1.f - static_cast<float>(opening), 0.f);

        renderer.render(*scene, *camera);
    });
    ```

    **One line of the render loop just became the entire feature.** `controller->compute(measurement, dt)` runs `OnOffController::compute` or `PIDController::compute` depending on what `controller` points at *this frame* — [runtime polymorphism](Chapter5/polymorphism.md), decided while the program is running rather than while it is compiling. The loop was written before either controller existed and does not mention them.

    `Controller*` is a **non-owning raw pointer**: it observes one of two objects that `main` owns. It has to be a pointer rather than a reference because it must be **re-pointed** — a [reference](Chapter4/types_refs_ptrs.md#references) is bound once and can never refer to anything else. A `unique_ptr` would be wrong: the pointer is not doing any owning.

    The key handler is the [Observer pattern](Chapter6/observer.md#watching-out-for-lifetimes) again, with the lifetime question that chapter raises: the lambda captures `onOff`, `pid` and `controller` **by reference**, and the canvas stores it. That chapter's rule of thumb is that whatever a callback captures should outlive the subject. Here it does not — the three variables are declared after the canvas, so they are destroyed *before* it — and it is still safe, because the canvas only calls its stored callbacks while `canvas.animate(...)` is running, and all three live until `main` ends, after `animate` has returned. Capture something that dies while the loop is still running and you would have a dangling callback.

    **`valveMaterial` is shared ownership doing real work.** The material is owned by your variable *and* by the valve mesh. Change its colour through either one and the mesh shows it, because there is only one material. The colour is the opening mapped onto red and green: `opening = 0` gives `(0, 1, 0)`, pure green; `opening = 1` gives `(1, 0, 0)`, pure red; anything between is a blend.

    </div>

## Milestone 7 — Put the numbers on screen

*Practises: [Strings](strings.md), [IO & Streams](Chapter4/io_streams.md)*

You can see *that* it settles; now show *what* it is doing. Add a screen-space `TextSprite` reading the controller's name, the level, the setpoint and the valve opening, and rebuild its text every frame with `std::format`.

> Hint: `TextSprite` is not part of `threepp.hpp` — it has a header of its own under `threepp/objects/`. If the compiler says `'TextSprite' has not been declared`, that is what it means ([Reading Compiler Errors](compiler_errors.md)). `FontLoader().defaultFont()` gives you a font with no file to load. Set `screenSpace = true` and `screenAnchor` to pin the text to a corner of the window rather than a point in the world. Careful: the comment above `screenAnchor` in `Sprite.hpp` says `(0, 0)` is the top-left corner. With `GLRenderer` at this version it is the *bottom*-left — a comment can be wrong, so try it and see. Track the controller's name in a `std::string` you set alongside the pointer.

!!! example "Run it — you should see"

    A line such as

    ```
    PID | level 4.87 m | setpoint 5.00 m | valve 70%
    ```

    in the top-left corner, changing as the water moves and switching name when you press `1` or `2`. (threepp's built-in font draws `|` as a broken bar, `¦`.)

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    New includes at the top:

    ```cpp
    #include "threepp/objects/TextSprite.hpp"

    #include <format>
    #include <string>
    ```

    The HUD, after the rig:

    ```cpp
    FontLoader fontLoader;
    auto hud = TextSprite::create(fontLoader.defaultFont(), 22.f);  // text 22 pixels tall
    hud->setColor(Color::black);
    hud->screenSpace = true;               // pinned to the window, not placed in the 3D world
    hud->screenAnchor.set(0.f, 1.f);       // anchored to the top-left corner
    hud->position.set(10.f, -10.f, 0.f);   // 10 px right of and below that corner
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
    hud->setText(std::format("{} | level {:.2f} m | setpoint {:.2f} m | valve {:.0f}%",
                             controllerName, plant.level(), setpoint, opening * 100));
    ```

    `std::format` fills each `{}` with the next argument, and `{:.2f}` asks for two decimal places — the same formatting as in [IO & Streams](Chapter4/io_streams.md#formatting). It hands you a `std::string`, which is exactly what `setText` wants; with `<iomanip>` you would need a string stream and a handful of manipulators to get the same text ([Strings](strings.md)).

    Screen coordinates start at the **bottom-left** corner and grow upward, so the anchor `(0, 1)` is the top-left corner and the offset `-10` moves the text down from it. That is what the renderer does (`renderScreenSpaceSprites` in `GLRenderer.cpp`), whatever the comment in `Sprite.hpp` says — the "check what you assumed" habit from [Finding things out yourself](#finding-things-out-yourself). The header also calls the second argument of `TextSprite::create` `worldScale`; in screen space one unit is one pixel, which is why `22.f` makes the text 22 pixels tall.

    Notice that this milestone touched **only** the display code. Presenting the numbers is one concern; producing them is another, and they still live in different files.

    </div>

## Milestone 8 — Check the tests still pass

*Practises: [Testing](Chapter6/testing.md), [CMake](Chapter2/cmake_intro.md#building-libraries), [Git](Chapter2/version_control.md#when-something-goes-wrong)*

Run the tests: pick the `tests` configuration in CLion's run dropdown and click **Run** (the dropdown also lists targets that CTest and threepp add — `Continuous…`, `Nightly…`, `glfw`, `threepp` — ignore them), or type `ctest --test-dir cmake-build-release` (or `cmake-build-debug` — whichever profile you built) in CLion's **Terminal** tab. Every test from [Version 5](tank_control/v5_tests.md) should still be green: the 3D view changed nothing they cover, and a first-frame fix in `tank_lib` must not break them either. (If your fix went into `tank_lib`, your new test runs too.)

Then prove the suite is really guarding the thing on screen:

!!! question "Before you break it"

    You are about to change the `+=` in `Tank::update` to `-=`, so that the level *falls* when the valve opens. Write down in your log — and commit — which tests you expect to fail, and why the others will not.

Make the change, rebuild, and run the tests and the rig. Take a screenshot of the red test run. Then undo the change with `git restore src/tank.cpp` (or **Rollback** in CLion's commit window) — which is why you committed first: `git restore` throws away every uncommitted change to that file. Rebuild, and check that everything is green again.

!!! example "Run it — you should see"

    Before the flip, from `ctest`:

    ```
    100% tests passed, 0 tests failed out of 1
    ```

    (`ctest` counts the whole `tests` program as one test) or, from the `tests` configuration, Catch2's own summary: `All tests passed (14 assertions in 8 test cases)` — more if you added tests of your own. After the change: red tests, and a tank draining before your eyes.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    Nothing to write, apart from your prediction. In CLion's **Terminal** tab, point `ctest` at the build folder you are using — CLion's are called `cmake-build-debug` and `cmake-build-release`:

    ```bash
    ctest --test-dir cmake-build-release --output-on-failure
    ```

    (A PowerShell window opened from the Start menu may not find `ctest`; CLion's Terminal tab can.)

    With `-=`, three of the book's eight test cases fail: *Tank integrates net flow over a step*, *Tank level never goes negative* and *Closed loop: the level ends near the setpoint*. The valve, PID and on/off tests never call `Tank::update`, so they stay green — each test guards one behaviour, and the red ones point straight at the component that broke. Tests of your own that step a `Tank` or a `Plant` may fail too.

    Your project now builds three programs from one source tree:

    ```mermaid
    %%{init: {'flowchart': {'curve': 'linear'}}}%%
    graph TD
        RIG["tank_rig (3D view)"] -->|links| LIB["tank_lib"]
        RIG -->|links| TPP["threepp::threepp (fetched)"]
        APP["tank_control (console)"] -->|links| LIB
        TESTS["tests"] -->|links| LIB
        TESTS -->|links| C2["Catch2 (fetched)"]
    ```

    The `.cpp` files in `src/` are compiled **once**, into `tank_lib`, and linked into all three, so the tests check the very same compiled code the 3D app runs — not a copy that might have drifted. That is why [the CMake chapter](Chapter2/cmake_intro.md#building-libraries) told you to build shared logic as a library rather than listing the same `.cpp` files in several `add_executable` lines.

    The graphics have no tests, and that is deliberate: keep the view **thin**. Put every decision in `tank_lib`, where it can be tested, and let the view only translate numbers into shapes. If a piece of that translation is worth getting right — the water's scale and position, say — pull it into a small function of its own and test that.

    </div>

## Project layout

At the end of the milestones your project looks like this:

```
tank-rig/
├── CMakeLists.txt      # top level: C++20, include(CTest), src, app, tests and rig
├── LOG.md              # your log
├── README.md           # your presentation
├── include/            # from Version 5
├── src/                # from Version 5 — built as tank_lib
├── app/                # from Version 5 — the console program
├── tests/              # from Version 5 — plus any tests you add
├── rig/                # the 3D view
│   ├── CMakeLists.txt
│   └── main.cpp
└── docs/
    └── images/         # screenshots and GIFs for the README
```

The two build files you wrote are the top-level one from Milestone 5 and `rig/CMakeLists.txt`:

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

---

## Finding things out yourself

From here on, nobody hands you the exact call. That is normal: working programmers spend much of their time finding out how a library works. Here is how to do it with threepp.

- **Read the headers.** Ctrl+click any threepp name in CLion to open its declaration. The headers themselves are in your build folder, under `cmake-build-<profile>/_deps/threepp-src/include/threepp/`, and the source files under `_deps/threepp-src/src/`. Reading the `.cpp` is allowed, and often the final answer — the bug hunt in Milestone 5 ends in `Clock.cpp`.
- **Read the examples.** threepp comes with around a hundred small example programs. Browse the ones for the version you use at <https://github.com/markaren/threepp/tree/2026-06-17/examples> — read them in the browser, and copy only the few lines you need, with a comment saying where they came from. They start with `createRenderer(canvas)`; use `GLRenderer renderer(canvas);` instead, as in Milestone 1.
- **See one run.** Copy an example's `.cpp` into `rig/` under a new name (say `try_raycast.cpp`), add `add_executable(try_raycast try_raycast.cpp)` and `target_link_libraries(try_raycast PRIVATE threepp::threepp)` to `rig/CMakeLists.txt`, swap in `GLRenderer`, reload CMake, and pick it in the run dropdown. It uses the threepp you have already built. A few examples need extra files or libraries and will not build this way — pick another.
- **Shrink, then port.** Find an example that does something close to what you want. Work out the smallest part of it that does the thing. Move that part into your rig, get it working, *then* make it yours.
- **Check what you assumed.** When something behaves oddly, write down what you expected, then test the assumption with the smallest change you can think of — exactly like the log entry after Milestone 4.

---

## From the tank to your own machine

The tank is one machine. The same skeleton fits almost any controlled machine — a lift, a robot joint, a conveyor — because it is made of four roles:

- **State that steps in time.** Something with `step(input, dt)`, like `Plant`. The update is the same kind of line as in `Tank::update`: the new value is the old value plus a rate times `dt`. For motion, position changes by velocity × `dt` and velocity by acceleration × `dt`.
- **Sensors** that read the state, behind an interface.
- **Actuators with limits** — a valve that cannot open more than fully, a motor with a maximum force.
- **Controllers** behind an interface, swappable at runtime.

Two things to watch when you move to a new machine:

- **Check what the classes you reuse assume.** The book's PID clamps its output to 0..1 because it drives a valve ([Version 3](tank_control/v3_pid.md)). A motor that can push both ways needs −1..+1. Reuse the idea; question the details.
- **Time steps matter more for moving things.** A tank forgives a long frame; a machine with momentum may overshoot badly after one. Decide what your simulation should do when a frame takes far longer than usual — after a breakpoint, say, or while you drag the window.

Keep the machine's logic in a library of its own that does not link threepp, with tests, and let the 3D view only show it — exactly as `tank_lib` and `rig/` do.

---

## Your extension

Choosing an extension, and being able to say why you built it the way you did, is part of the project. The rule from Milestone 8 still holds: **the logic belongs in a library, with a test; the view only shows it.** Build one extension well — tested, explained, with its trade-offs understood — before you think about a second.

Each card below says what to build, the design question you will have to answer, and a test that would prove it works. Where you will need something the book has not shown you, it says where to look. There are no solutions.

These are suggestions; an idea of your own is just as good. Whatever you pick, start by writing its plan in your log: what it does, which new classes go where, what the rig will show, and one thing you do not know yet. Some cards grow out of Version 5's own list — if you built one there, it arrives with your import, so take it further here: into the view, with its design question answered and its test written.

**Small**

- **Alarm with hysteresis.** The shell turns red when the level rises above 7.0 m and back when it falls below 6.8 m.
    - *Design question:* who decides — the render loop, the plant, or a small class of its own? Why must the alarm not switch on and off every frame near the limit?
    - *Test:* the alarm switches on once as the level crosses 7.0 m, and off only below 6.8 m.
    - Nothing in the rig pushes the level that high yet — give yourself a way to (a key that forces the valve open, say) so you can watch it switch.
- **Noisy sensor.** A `NoisyLevelSensor` that adds a small wobble ([Random Numbers](random.md)), with a fixed seed so every run repeats.
    - *Design question:* `Sensor::read()` is `const`, but drawing a random number changes the generator. What are your options, and which one does not hide that `read()` changes something?
    - *Find out:* what the keyword `mutable` does, and what else you could do instead.
    - *Test:* two sensors with the same seed give the same readings. Then watch what noise does to each controller.
- **Deadband controller.** An on/off controller that only switches when the level is more than 0.2 m from the setpoint.
    - *Design question:* predict what it does to what you saw in Milestone 6 — then check.
    - *Test:* inside the band, the output does not change.
- **Time-scale keys.** Keys that speed up and slow down simulated time.
    - *Design question:* where does the scaling live, and what should happen at 50× speed? What does a very large `dt` do to your plant?
    - *Test:* whatever computes the scaled step never hands the plant more than your chosen limit.

**Design**

- **Strip chart.** The last few hundred levels drawn as a line beside the tank.
    - *Design question:* which container, what happens when it is full, and who owns it?
    - *Find out:* how to change a line's points every frame — `examples/geometries/dynamic.cpp` moves a geometry's points each frame, and `examples/extras/curves/catmull_room_curve3.cpp` builds a `Line` from points.
    - *Test:* the history keeps at most N values and drops the oldest first.
- **State machine.** *Filling → Holding → Draining → Fault*, with the shell's colour showing the state ([Enumerations](Chapter1/enums.md) and a `switch`).
    - *Design question:* the plant has no drain valve. What do you add, and who owns it?
    - *Test:* one test per transition, including the ones that must *not* happen.
- **Two tanks in cascade.** The first tank's outflow feeds the second: two plants, two rigs, `rig->position.x` apart.
    - *Design question:* in your `Plant` the outflow is a fixed number, and `Plant` does not report it. But a tank that feeds another cannot drain when it is empty (and a real one drains faster when it is fuller). What has to change, what does the second plant need to know, and from whom?
    - *Test:* with the first tank's outlet shut, the second tank's level only falls.
- **Setpoint at runtime.** Move the red band with keys, or by dragging it with the mouse, and feed the new value to the controller.
    - *Design question:* `Controller` has no way to change its setpoint. Which interface changes, and which tests break?
    - *Find out:* `examples/misc/raycast.cpp` (what is under the mouse) and `examples/controls/drag.cpp` (dragging objects).
    - *Test:* after a setpoint change, the closed loop settles near the new value.
- **Fixed controller sample time.** The controller runs every 0.5 s of simulated time, however fast the frames come — like the scan cycle of a PLC.
    - *Design question:* who keeps time, and what happens between samples? Predict the effect on Milestone 6.
    - *Test:* over one simulated second at any frame rate, the controller runs exactly twice.

**Your own machine**

Build a second machine *next to* the tank, in the same repository: a lift, a robot joint, a conveyor sorter, or your own idea. It gets its own library target that does not link threepp, its own tests, and its own view. Write its card yourself before you start — what it does, the design question, what you need to find out, the first test — using the ones above as the pattern. [From the tank to your own machine](#from-the-tank-to-your-own-machine) lists what to watch for. threepp's `examples/projects/MotorControl/` and `examples/libs/utility/Regulator.hpp` show a motor and a regulator you can learn from.

**Decisions worth writing down.** Whatever you build, record the decisions that shaped it, a few lines each, in your log or in your README's *Why it is built this way* section. For example:

```markdown
**Question:** where does the high-level alarm live?
**Options:** the view checks the level every frame / the plant notifies / an AlarmMonitor class fed by the loop.
**Choice:** AlarmMonitor, with 0.2 m hysteresis.
**Why:** testable without a window, and it fires once per crossing.
**Test:** "alarm fires once when level crosses 7.0 and clears below 6.8".
```

---

## Present your project

Your `README.md` is where you **present** the project — to a teacher, to a future employer, to yourself in a year. It is written by you, about your work, in your own words. Start from [The README](readme_guide.md), read its section on [presenting a bigger project](readme_guide.md#presenting-a-bigger-project), and make yours a proper presentation:

1. **What it is** — a paragraph, and a **GIF of it running** at the top. The first thing a reader sees should be your rig in motion.
2. **How to build and run it** — the steps, how long the first build takes, and the controls (which keys do what).
3. **How it works** — the loop, the library and the view, and a [UML class diagram](uml.md) of the types *you* wrote or changed. A `mermaid` block like the ones on the UML page shows up as a diagram on GitHub; a photo of a tidy hand sketch works too. Say where the simulation meets the view.
4. **Why it is built this way** — the decisions you are proud of, why they make it a good solution, and the alternatives you rejected. Where did your first-frame fix go, and why there?
5. **What did not make it** — what you wanted to build but did not, why not, and what it would take. Knowing the limits of your own solution is part of understanding it.
6. **How you worked** — the story of the project, pointing at your best log entries and commits: the hardest bug, the test that caught something, the prediction that turned out wrong.
7. **How you used AI** — which tools and models you used (the name and version the tool shows you), what you used them for, and how: what you asked, what you kept, what you threw away and why. Where was it wrong or unhelpful? What did you learn from working this way — about the code, and about using AI? ([Using AI for Coding](using_ai.md)) If you did not use AI, say so, and how you found answers instead.
8. **Credits** — everything that did not start as new code in this project: the Version 5 code you imported (and the book's tank pages it grew from), milestone solutions you typed from this page, and anything borrowed from threepp's examples or elsewhere, with links.

**Pictures and GIFs.** [The README](readme_guide.md#show-it-screenshots-and-gifs) shows how to take a screenshot, record a short GIF of the window, store both in `docs/images/`, and put them in the README. The best ones are those you took along the way: the empty tank before your fix, the red test run, the first time your extension worked — and a GIF of the finished rig for the top of the page.

---

## Summary

- A 3D view is just another **consumer** of your simulation's numbers. Plugging it in required no edits to `src/` — the simulation does not know the view exists.
- A new consumer can still expose an assumption your tests never made. A clock's first frame has **no elapsed time**, and a `NaN`, once in, flows through every calculation and slips past every clamp. Where to guard against it is a design decision.
- Pulling in a real dependency is a few lines of CMake: `include(FetchContent)`, `FetchContent_Declare`, `FetchContent_MakeAvailable`, then link the target it exports. **Pin a tag**, and turn off the parts of it you do not need.
- A scene graph is **composition**: a group *has* children, a child's transform is relative to its parent, and moving the parent moves all its children.
- threepp's `create` functions return a `shared_ptr` because threepp chose **shared ownership**: the scene keeps what you add alive, and your variable is another owner.
- A base-class pointer chosen by a key press is **runtime polymorphism** you can watch; the loop that runs both controllers never changed.
- Multiply by `dt`, never by "per frame". Frames are not a unit of time.
- The library is compiled once and linked by the 3D rig, the console program and the tests, so what you tested is what you ran.
- Leave a trail: commits that say why, a log, predictions written down before you run — and a README that presents the result in your own words.
