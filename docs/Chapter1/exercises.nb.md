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

## 3. Sensoravlesninger

*Øver på: [Strenger og vektorer](strings_and_vectors.md), [Kontrollstrukturer](control_statements.md)*

Lagre fem sensoravlesninger — `42, 17, 99, 8, 56` — i en `std::vector<int>`. Skriv ut hvor mange det er, gjennomsnittet deres (som et desimaltall), og det største.

> Hint: gå gjennom vektoren for å summere verdiene og holde styr på det største; `readings.size()` er antallet.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <vector>

    int main() {
        std::vector<int> readings = {42, 17, 99, 8, 56};

        int sum = 0;
        int largest = readings[0];
        for (int r : readings) {
            sum += r;
            if (r > largest) {
                largest = r;
            }
        }

        double average = static_cast<double>(sum) / readings.size();

        std::cout << "Count:   " << readings.size() << "\n";
        std::cout << "Average: " << average << "\n";
        std::cout << "Largest: " << largest << "\n";
    }
    ```

    En områdebasert `for` besøker hvert element: vi legger hvert til `sum` og beholder det største som er sett så langt. `static_cast<double>` holder divisjonen desimal (heltallsdivisjon-regelen igjen), og `readings.size()` gir antallet elementer.

    </div>

---

## 4. Partall eller oddetall

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

## 5. Kvadrater

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

## 6. Trafikklys

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

---

## 7. Fortsett å spørre

*Øver på: [Kontrollstrukturer](control_statements.md)*

Spør brukeren om et positivt tall, om og om igjen, til de faktisk gir deg et. Skriv det så ut. Bruk en `do-while`-løkke, så du spør minst én gang.

> Hint: dette er `do-while`-mønsteret fra kapittelet — les inne i løkken, og gjenta så lenge verdien ennå ikke er positiv.

Kjør det — du skal se:

```
Enter a positive number: -4
Enter a positive number: 0
Enter a positive number: 12
Thanks — you entered 12
```

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    int main() {
        int number = 0;

        do {
            std::cout << "Enter a positive number: ";
            std::cin >> number;
        } while (number <= 0);

        std::cout << "Thanks — you entered " << number << "\n";
    }
    ```

    En `do-while` kjører kroppen sin *før* den tester betingelsen, så ledeteksten vises alltid minst én gang. Løkken gjentar så lenge `number <= 0`, så den slipper deg først ut når verdien er ekte positiv — nettopp det "fortsett å spørre til det er gyldig" trenger.

    </div>

---

## 8. Hils med fullt navn

*Øver på: [Strenger og vektorer](strings_and_vectors.md)*

Spør om brukerens fulle navn (fornavn *og* etternavn, med mellomrommet), hils på dem, og fortell hvor mange tegn navnet har. Fordi navnet inneholder et mellomrom, trenger du `std::getline`, ikke `std::cin >>`.

> Hint: `std::getline(std::cin, name)` leser hele linjen; `name.length()` teller tegnene.

Kjør det — du skal se:

```
Enter your full name: Ada Lovelace
Hello, Ada Lovelace
Your name has 12 characters.
```

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>

    int main() {
        std::string name;

        std::cout << "Enter your full name: ";
        std::getline(std::cin, name);

        std::cout << "Hello, " << name << "\n";
        std::cout << "Your name has " << name.length() << " characters.\n";
    }
    ```

    `std::getline` leser hele linjen, mellomrom inkludert, så `Ada Lovelace` kommer inn helt — `std::cin >> name` ville stoppet ved mellomrommet og beholdt bare `Ada`. Tallet `12` inkluderer mellomrommet, fordi det er ett av tegnene i strengen.

    </div>

---

## 9. Temperaturklassifisering

*Øver på: [Kontrollstrukturer](control_statements.md)*

Les en temperatur (et helt antall grader Celsius) og skriv ut en beskrivelse ved hjelp av en `if` / `else if` / `else`-kjede: under `0` er `Freezing`, `0` til `14` er `Cold`, `15` til `24` er `Comfortable`, og `25` eller over er `Hot`.

> Hint: test det kaldeste tilfellet først og arbeid oppover, så hver `else if` bare trenger å sjekke sin øvre grense.

Kjør det — du skal se:

```
Enter the temperature in Celsius: 18
Comfortable
```

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    int main() {
        int celsius = 0;

        std::cout << "Enter the temperature in Celsius: ";
        std::cin >> celsius;

        if (celsius < 0) {
            std::cout << "Freezing\n";
        } else if (celsius < 15) {
            std::cout << "Cold\n";
        } else if (celsius < 25) {
            std::cout << "Comfortable\n";
        } else {
            std::cout << "Hot\n";
        }
    }
    ```

    Bare den første grenen som passer kjører, så det å ordne testene fra kaldest og oppover lar hver `else if` anta at alt under den allerede er utelukket: når `celsius < 15` sjekkes, vet vi at den ikke er under `0`, så den grenen betyr `0` til `14`. Den siste `else` fanger alt som er igjen — `25` og over.

    </div>
