# Strenger og vektorer

To typer fra standardbiblioteket dukker opp i nesten alle skrivebordsprogrammer: `std::string` for tekst, og `std::vector` for en liste med verdier. De er ikke innebygd i språket slik `int` og `double` er, men på skrivebordet kommer du til å bruke dem hele tiden — uten dem kan du bare holde én verdi om gangen og kan ikke arbeide med ord i det hele tatt. (På små mikrokontrollere er de ofte utilgjengelige; se [Arduino vs. desktop-C++](../arduino_vs_desktop.md).)

Denne siden dekker akkurat nok til å bruke begge. Alle detaljene kommer i kapittel 3 — [Strenger](../strings.md), [Standardbibliotek](../Chapter3/standard_library.md) og [Datastrukturer](../Chapter3/data_structures.md).

---

## `std::string`: tekst

Du har allerede brukt tekst som streng-*literaler* — `"Hello, world!"` i hermetegn. En `std::string` er en *variabel* som holder tekst du kan bygge, endre og undersøke. Inkluder `<string>` for å bruke den:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Ada";
    std::string greeting = "Hello, " + name + "!";   // sett sammen biter med +

    std::cout << greeting << "\n";        // Hello, Ada!
    std::cout << name.length() << "\n";   // 3  — antall tegn
}
```

De dagligdagse operasjonene:

| Operasjon            | Eksempel           | Resultat                        |
|----------------------|--------------------|---------------------------------|
| Sette sammen         | `"Hi " + name`     | en ny streng `"Hi Ada"`         |
| Legge til på slutten | `greeting += "!"`  | føyer til på slutten av `greeting` |
| Lengde               | `name.length()`    | `3` (også `name.size()`)        |
| Ett tegn             | `name[0]`          | `'A'` — en `char`, teller fra 0 |
| Sammenligne          | `name == "Ada"`    | `true`                          |
| Er den tom?          | `name.empty()`     | `false`                         |

### Lese tekst fra brukeren

`std::cin >> word` leser ett enkelt **ord** — den stopper ved første mellomrom. For å lese en hel linje, mellomrom og alt, bruk `std::getline`:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string fullName;

    std::cout << "Enter your full name: ";
    std::getline(std::cin, fullName);   // leser hele linjen

    std::cout << "Hello, " << fullName << "!\n";
}
```

Hadde du skrevet `std::cin >> fullName`, ville det å skrive `Ada Lovelace` lagre bare `Ada` og la `Lovelace` bli igjen — en klassisk nybegynneroverraskelse. Bruk `>>` for enkeltord, `getline` for hele linjer.

---

## `std::vector`: en liste med verdier

En `std::vector` holder en sekvens av verdier **av én type**, og den vokser etter hvert som du legger til. Inkluder `<vector>`, og sett elementtypen i vinkelparenteser:

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings = {42, 17, 99};   // start med tre ints

    readings.push_back(8);                  // legg én til på slutten → {42, 17, 99, 8}

    std::cout << readings.size() << "\n";   // 4  — hvor mange elementer
    std::cout << readings[0]     << "\n";   // 42 — det første (indeks 0)
    std::cout << readings[3]     << "\n";   // 8  — det fjerde (indeks 3)
}
```

Noen ting å huske på:

- Typen i `<...>` er **elementtypen**: `std::vector<int>` holder `int`-er, `std::vector<std::string>` holder strenger. Alle elementene har samme type.
- **Indeksering starter på 0.** Det første elementet er `[0]`, det siste er `[size() - 1]`.
- Å lese eller skrive forbi slutten — `readings[99]` her — er **udefinert oppførsel**: programmet kan krasje eller stille oppføre seg feil. Hold deg mellom `0` og `size() - 1`.
- `push_back` legger til på slutten, og vektoren vokser av seg selv. Du håndterer aldri minnet dens.

> C++ har også lavnivå, innebygde arrays (`int a[4]`), men `std::vector` er den du bør gripe til: den kjenner sin egen størrelse og endrer størrelse selv. Foretrekk den.

For å *gjøre* noe med hvert element — skrive dem alle ut, summere dem, finne det største — bruker du en **løkke**. Det er nettopp det neste side, [Kontrollstrukturer](control_statements.md), handler om; den områdebaserte `for`-en leser spesielt rent over en vektor.

---

## Oppsummering

- `std::string` (fra `<string>`) holder tekst: sett sammen med `+`, mål med `.length()`, les ett tegn med `[i]`, les en hel linje med `std::getline`.
- `std::vector<T>` (fra `<vector>`) holder en voksbar liste med verdier av type `T`: legg til med `push_back`, tell med `.size()`, les med `[i]` (starter på 0).
- Begge rydder opp sitt eget minne — det trenger du aldri gjøre.
- Dette er et fungerende minimum. Kapittel 3 går mye dypere — [Strenger](../strings.md), [Standardbibliotek](../Chapter3/standard_library.md) og [Datastrukturer](../Chapter3/data_structures.md).
