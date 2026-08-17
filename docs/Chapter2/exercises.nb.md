# Oppgaver til kapittel 2

Jobb deg gjennom disse etter å ha lest kapittel 2. **Prøv hver enkelt selv før du avslører løsningen** — du lærer langt mer av et ærlig forsøk enn av å lese et ferdig svar.

Når du åpner en løsning vises den **uskarp** — klikk én gang til for å avsløre den, slik at du ikke ser svaret ved et uhell.

Disse oppgavene gjøres i et ekte prosjekt og en ekte terminal — en `CMakeLists.txt` du skriver og en sekvens av `git`-kommandoer du kjører. Det er ingenting å "kjøre på Compiler Explorer"; poenget er å gjøre dem på ordentlig på din egen maskin. (PlatformIO har ingen papirøvelse — den trenger et ekte kort, så øvingen på den hører hjemme i laben med maskinvaren i hånden.)

---

## 1. Et prosjekt med to programmer {#1-a-project-with-two-programs}

*Øver på: [CMake](cmake_intro.md)*

Du vil beholde to av kapittel 1-løsningene dine — `ex1.cpp` og `ex2.cpp` — i ett enkelt prosjekt, hver kjørbar for seg. Skriv en `CMakeLists.txt` som bygger begge som **separate kjørbare filer**, bruker **C++20** og slår **kompilator-advarsler på** for hver av dem.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cmake
    cmake_minimum_required(VERSION 3.16)
    project(chapter1_solutions)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    if(MSVC)
        add_compile_options(/W4)
    else()
        add_compile_options(-Wall -Wextra)
    endif()

    add_executable(ex1 ex1.cpp)
    add_executable(ex2 ex2.cpp)
    ```

    Én `add_executable` per program gir deg to oppføringer i rullegardinmenyen for kjørekonfigurasjon ved siden av den grønne ▶-knappen — nøyaktig oppsettet kapittel 1-oppgavene foreslo. `CMAKE_CXX_STANDARD` settes én gang nær toppen og gjelder for hvert target under den. Advarselsflaggene går bak en `if(MSVC)`-gren, akkurat som kapittelet viser: å hardkode `-Wall -Wextra` alene ville røket i det øyeblikket noen bygde dette med Visual Studio, som staver flagget `/W4`. Å legge flaggene i `add_compile_options` *før* targetene gjør at de gjelder begge kjørbare filer på én gang, så det er ingen per-target-linje å gjenta.

    </div>

---

## 2. Lagre arbeidet ditt med git {#2-save-your-work-with-git}

*Øver på: [Versjonskontroll og Git](version_control.md)*

Du har nettopp opprettet en ny prosjektmappe som inneholder en `CMakeLists.txt` og en `main.cpp`. Bruk git til å (1) gjøre mappen om til et repository, (2) lagre begge filene i en første commit med en fornuftig melding, og deretter (3) starte en branch kalt `experiment` for å prøve ut en endring uten å forstyrre `main`. Skriv kommandoene i rekkefølge.

> Hint: en kjapp `git status` mellom stegene er alltid en god måte å sjekke hva git mener foregår.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```bash
    git init                                  # gjør mappen om til et repo
    git status                                # se hva som er usporet

    git add CMakeLists.txt main.cpp           # stage begge filene
    git commit -m "Initial project: builds Hello World"

    git switch -c experiment                  # opprett + flytt over på en ny branch
    ```

    `git add` bare *stager* filene — den markerer dem for neste øyeblikksbilde. `git commit` er det som faktisk registrerer øyeblikksbildet, og meldingen dens sier hva denne tilstanden er. `git switch -c experiment` oppretter branchen og flytter deg over på den i ett steg; alt du committer nå, havner på `experiment` og lar `main` stå urørt til du velger å merge.

    </div>

---

## 3. Del kode mellom to programmer med et bibliotek {#3-share-code-between-two-programs-with-a-library}

*Øver på: [CMake](cmake_intro.md)*

Begge programmene dine trenger den samme hjelperen — si et `motor.cpp` / `motor.hpp`-par med en `motorRpm()`-funksjon. I stedet for å liste `motor.cpp` i *begge* `add_executable`-linjene (og kompilere den to ganger), legg den i et **bibliotek** og link det biblioteket inn i hvert program. Skriv en `CMakeLists.txt` som bygger `motor.cpp` som et bibliotek og linker det inn i to kjørbare filer, `app` og `bench`.

> Hint: `add_library` definerer bibliotek-targetet; `target_link_libraries(<exe> PRIVATE <lib>)` linker det inn i en kjørbar fil. Et program som linker biblioteket, ser også headerne dets.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cmake
    cmake_minimum_required(VERSION 3.16)
    project(motor_tools)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    add_library(motor motor.cpp)          # delt kode, kompilert én gang

    add_executable(app app.cpp)
    target_link_libraries(app PRIVATE motor)

    add_executable(bench bench.cpp)
    target_link_libraries(bench PRIVATE motor)
    ```

    `motor.cpp` kompileres nå én enkelt gang inn i `motor`-biblioteket; hver `target_link_libraries`-linje trekker den kompilerte koden (og `motor` sine headere) inn i én kjørbar fil. Hvis hjelperen hadde sin egen `include/`-mappe, ville du lagt til `target_include_directories(motor PUBLIC include)` slik at begge programmene plukker opp headerne automatisk — `PUBLIC` fordi alt som linker `motor`, også bør se dem. Dette er mønsteret kapittelets seksjon [Bygge biblioteker](cmake_intro.md#building-libraries) beskriver, og det er slik et prosjekt med tester holder produksjonskoden sin på ett sted.

    </div>
