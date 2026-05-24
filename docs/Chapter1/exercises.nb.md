# Oppgaver til kapittel 1

Arbeid deg gjennom disse etter at du har lest kapittel 1. **Prøv hver enkelt selv før du avslører løsningen** — du lærer langt mer av et ærlig forsøk, og feilene underveis, enn av å lese et ferdig program. Skriv koden inn i CLion og kjør den; ikke bare les den.

Når du åpner en løsning vises den **uskarp** — klikk én gang til for å avsløre den, slik at du ikke ser svaret ved et uhell.

## Hvor du skal legge koden din

Hver oppgave er sitt eget lille program med sin egen `main()`, og et CLion-prosjekt kjører én `main()` om gangen. Du har to muligheter:

**Enklest** — hold ett prosjekt åpent og bytt ut innholdet i `main.cpp` for hver oppgave. Kjør det, og lim så inn det neste. (Du mister det forrige forsøket, noe som er greit for rask øving.)

**Beholder hver oppgave (anbefalt)** — gi hver oppgave sin egen fil i ett enkelt prosjekt (`ex1.cpp`, `ex2.cpp`, …) og legg til én linje per fil i `CMakeLists.txt`:

```cmake
add_executable(ex1 ex1.cpp)
add_executable(ex2 ex2.cpp)
```

Velg så hvilket program som skal kjøres fra rullegardinmenyen for kjørekonfigurasjon ved siden av den grønne ▶-knappen. Du trenger ikke forstå `CMakeLists.txt` ennå — [CMake-introduksjon](../Chapter2/cmake_intro.md) forklarer det i kapittel 2; for nå, bare kopier mønsteret.

---

## 1. Presenter deg selv

*Øver på: [Grunnstruktur](basic_structure.md), [Variabler og grunntyper](variables.md)*

Deklarer en `std::string` for navnet ditt og en `int` for alderen din (akkurat som kapittelets `int age = 25`). Skriv ut én linje:

```
My name is Ada and I am 36 years old.
```

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>

    int main() {
        std::string name = "Ada";
        int age = 36;

        std::cout << "My name is " << name << " and I am " << age << " years old.\n";
    }
    ```

    Hver variabel får riktig type og initialiseres idet den deklareres; `<<` kjeder bitene sammen til én linje.

    </div>

---

## 2. Gjennomsnittskarakter

*Øver på: [Operatorer og uttrykk](operators_expressions.md)*

Du har tre prøvekarakterer: `7`, `8` og `10`. Skriv ut gjennomsnittet deres. Sørg for at det kommer ut som et desimaltall — `8.33…`, ikke et avkortet `8`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    int main() {
        int a = 7;
        int b = 8;
        int c = 10;

        double average = (a + b + c) / 3.0;   // 3.0 er en double, så desimalene beholdes

        std::cout << "Average: " << average << "\n";
    }
    ```

    Del på `3` (en `int`) og C++ gjør heltallsdivisjon — den kaster bort brøkdelen og du får `8`. Å skrive `3.0` gjør den ene siden til en `double`, så desimalene overlever. Det er kapittelets `10 / 3`-regel i praksis.

    </div>

---

## 3. Partall eller oddetall

*Øver på: [Kontrollstrukturer](control_statements.md)*

Bruk en `for`-løkke til å skrive ut tallene 1 til 10, og merk hvert enkelt som `even` eller `odd`.

> Hint: et tall er partall når `n % 2 == 0`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    int main() {
        for (int i = 1; i <= 10; ++i) {
            if (i % 2 == 0) {
                std::cout << i << " even\n";
            } else {
                std::cout << i << " odd\n";
            }
        }
    }
    ```

    En tellerbasert `for`-løkke som den i kapittelet, med en `if`/`else` inni som avgjør hva som skal skrives ut.

    </div>

---

## 4. Kvadrater

*Øver på: [Funksjoner](functions.md)*

Skriv en funksjon `int square(int n)` som returnerer `n * n` (du så akkurat denne funksjonen i kapittelet). Bruk så en `for`-løkke til å skrive ut kvadratene av 1 til og med 5.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    int square(int n) {
        return n * n;
    }

    int main() {
        for (int i = 1; i <= 5; ++i) {
            std::cout << i << " squared is " << square(i) << "\n";
        }
    }
    ```

    En liten funksjon med én klar oppgave, kalt fra en løkke. Å definere `square` én gang og gjenbruke den slår å skrive `i * i` overalt.

    </div>

---

## 5. Trafikklys

*Øver på: [Enumerasjoner](enums.md)*

Definer en `enum class TrafficLight` med `Red`, `Amber` og `Green`. Skriv en funksjon som skriver ut handlingen for hver enkelt — `Stop`, `Get ready`, `Go` — ved hjelp av en `switch`, og kall den for alle tre.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    enum class TrafficLight {
        Red,
        Amber,
        Green
    };

    void act(TrafficLight light) {
        switch (light) {
            case TrafficLight::Red:   std::cout << "Stop\n";      break;
            case TrafficLight::Amber: std::cout << "Get ready\n"; break;
            case TrafficLight::Green: std::cout << "Go\n";        break;
        }
    }

    int main() {
        act(TrafficLight::Red);
        act(TrafficLight::Amber);
        act(TrafficLight::Green);
    }
    ```

    Et fast sett med navngitte verdier håndtert av en `switch`. Uten `default` advarer kompilatoren deg hvis du legger til en farge senere og glemmer den her.

    </div>
