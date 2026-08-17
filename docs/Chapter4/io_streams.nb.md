# Inndata, utdata og filstrømmer

En **strøm** i C++ er et objekt som data flyter gjennom. `std::cout` er strømmen som er koblet til konsollen din; `std::cin` er strømmen som leverer det brukeren skriver; `std::ifstream` er en strøm koblet til en fil du leser fra.

Operatorene `<<` og `>>` flytter data inn i og ut av strømmer. Når du først kan mønsteret med `std::cout`, fungerer den samme formen for hver strøm standardbiblioteket tilbyr.

---

## Konsoll-I/O {#console-io}

Tre strømobjekter, alle i `<iostream>`:

| Strøm      | Retning      | Formål                                    |
|-------------|----------------|--------------------------------------------|
| `std::cout` | utdata         | Skrive til konsollen                       |
| `std::cin`  | inndata          | Lese fra konsollen (vanligvis tastaturet)  |
| `std::cerr` | utdata (feil) | Skrive til feilstrømmen                  |

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int number = 0;
    std::cout << "Enter a number: ";
    std::cin  >> number;
    std::cout << "You entered " << number << "\n";
    return 0;
}
```

`<<` leses "putt dette *inn i* strømmen"; `>>` leses "hent ut fra strømmen *inn i* denne variabelen." Du kan kjede dem; operatorene returnerer strømmen selv, slik at den neste kan brukes umiddelbart.

> **En merknad om `std::endl` vs. `"\n"`:** Begge produserer et linjeskift. `std::endl` *flusher* i tillegg strømmen: den tvinger eventuell bufret utdata til å vises umiddelbart. Flushing er dyrt; i tette løkker, foretrekk `"\n"`. Grip til `endl` bare når du spesifikt ønsker å flushe.

---

## Å lese flere verdier {#reading-several-values}

Strømekstraksjon (`>>`) hopper over blanktegn, så å lese flere verdier er bare kjeding:

```cpp
int a = 0;
int b = 0;
std::cout << "Enter two integers separated by a space: ";
std::cin >> a >> b;
std::cout << "Sum: " << (a + b) << "\n";
```

Brukeren kan skrive `3 5`, `3<tab>5`, eller til og med trykke Enter mellom dem; `>>` plukker opp begge.

### Når ekstraksjonen feiler {#when-extraction-fails}

Hvis brukeren skriver `hello` når du ba om et heltall, feiler `>>` i stillhet; strømmen går inn i en feiltilstand, og påfølgende ekstraksjoner feiler også. Du kan sjekke strømmen som en boolsk verdi:

```cpp
int n = 0;
if (!(std::cin >> n)) {
    std::cerr << "That was not a number.\n";
    return 1;
}
```

---

## Å lese hele linjer {#reading-whole-lines}

`>>` stopper ved blanktegn. For å lese en hel linje (inkludert mellomrom), bruk `std::getline`:

```cpp
#include <string>

std::string name;
std::cout << "What is your name? ";
std::getline(std::cin, name);
std::cout << "Hello, " << name << "!\n";
```

!!! warning "Å blande `>>` og `getline`: linjeskiftet som blir igjen"

    Når du leser en verdi med `>>` og deretter leser en linje med `getline`, kommer `getline` ofte tilbake **tom**. Grunnen: `>>` stopper ved det første blanktegnet og lar linjeskiftet du trykket, bli liggende i inndatabufferet. Neste `getline` leser fra gjeldende posisjon frem til det linjeskiftet — og finner ingenting, så den returnerer en tom streng.

    ```cpp
    int age = 0;
    std::cin >> age;                 // du skriver "42<Enter>"; '\n' blir liggende i bufferet
    std::string name;
    std::getline(std::cin, name);    // leser frem til det gjenliggende '\n' → name er tom!
    ```

    Løsningen er å kaste resten av linjen etter `>>`-en, til og med det linjeskiftet:

    ```cpp
    #include <limits>

    std::cin >> age;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');   // kast frem til slutten av linjen
    std::getline(std::cin, name);    // leser nå neste linje riktig
    ```

    Alternativt: les *alt* med `getline` og konverter tallene selv (`std::stoi`, `std::stod`). Velg én stil og hold deg til den, i stedet for å veksle mellom `>>` og `getline` på samme strøm.

---

## Fil-I/O {#file-io}

Filer bruker de samme operatorene. Tre klasser i `<fstream>`:

| Klasse           | Retning | Formål             |
|-----------------|-----------|---------------------|
| `std::ifstream` | inndata     | Lese fra en fil    |
| `std::ofstream` | utdata    | Skrive til en fil     |
| `std::fstream`  | begge      | Lese og skrive      |

### Å lese en fil linje for linje {#reading-a-file-line-by-line}

<!-- no-ce -->
```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ifstream in("readings.txt");
    if (!in) {
        std::cerr << "Could not open readings.txt\n";
        return 1;
    }

    std::string line;
    while (std::getline(in, line)) {
        std::cout << line << "\n";
    }
    // Ingen eksplisitt close trengs, RAII lukker filen når `in` går ut av skop.
}
```

Sjekken `if (!in)` bruker strømmens bool-konvertering: en strøm i god stand regnes som sann; en strøm som ikke fikk åpnet, eller som har truffet en feil, regnes som usann.

`std::ifstream` er et flott eksempel på [RAII](raii.md) i praksis: filen åpnes i konstruktøren og lukkes i destruktøren. Du trenger ikke huske å kalle `close()`; det skjer automatisk, selv om et unntak kastes midt i funksjonen.

### Å skrive en fil {#writing-a-file}

```cpp
#include <fstream>

std::ofstream out("results.txt");
out << "Mean: "      << mean      << "\n";
out << "Std dev: "   << stddev    << "\n";
// lukkes automatisk når `out` går ut av skop
```

Som standard *trunkerer* `std::ofstream` filen; alt tidligere innhold går tapt. For å legge til på slutten i stedet:

```cpp
std::ofstream out("results.txt", std::ios::app);
```

---

## Å skrive ut dine egne typer {#printing-your-own-types}

`std::cout << myObject;` fungerer for innebygde typer og de fleste typene i standardbiblioteket. For dine egne klasser lærer du opp strømmen i hvordan den skal skrive dem ut ved å overlaste `operator<<`:

```cpp
#include <iostream>

struct Vector3 {           // en struct er bare en klasse med offentlige medlemmer som standard
    double x, y, z;
};

std::ostream& operator<<(std::ostream& os, const Vector3& v) {
    os << "Vector3(" << v.x << ", " << v.y << ", " << v.z << ")";
    return os;
}

int main() {
    Vector3 v{1.0, 2.0, 3.0};
    std::cout << v << "\n";   // skriver ut: Vector3(1, 2, 3)
}
```

To ting å legge merke til:

- Den første parameteren er `std::ostream&` — typen til `std::cout`, og fellestypen alle utdatastrømmer deler (`std::ofstream` og resten) — så den samme overlastingen fungerer med enhver utdatastrøm.
- Funksjonen returnerer strømmen slik at `<<`-kall kan kjedes.

Det samme mønsteret med `std::istream&` og `>>` lar deg tolke din egen type fra inndata.

---

## Formatering {#formatting}

For det meste av utdata er standardformateringen god nok. Når den ikke er det, har headeren `<iomanip>` manipulatorer som endrer hvordan påfølgende verdier skrives ut:

```cpp
#include <iomanip>
#include <iostream>

double pi = 3.14159265;

std::cout << std::fixed << std::setprecision(2) << pi << "\n";  // 3.14
std::cout << std::setw(10) << 42 << "\n";                       // "        42"
std::cout << std::hex << 255 << "\n";                            // ff
```

Manipulatorer er "klebrige": når du først har satt dem på en strøm, forblir de satt til du endrer dem. Hvis du bare trenger formatering for én enkelt verdi, må du lagre og gjenopprette — eller, mye renere, bruke `std::format` fra `<format>`:

```cpp
#include <format>

std::cout << std::format("{:.2f}\n", pi);          // 3.14
std::cout << std::format("{:>10}\n", 42);          // høyrejustert i 10 kolonner
std::cout << std::format("{:#x}\n", 255);          // 0xff
```

Formatstrengen følger plassholdere i Python-stil: `{}` for neste argument, med valgfri spesifikasjon etter `:`. Foretrekk dette fremfor manipulatorer når du bare trenger én formatert verdi; ingen klebrig tilstand å rydde opp i.

Formatering i `printf`-stil fra `<cstdio>` er også tilgjengelig, og et vanlig valg i innebygd kode.

---

## Oppsummering {#summary}

- `<<` skriver til en strøm; `>>` leser fra en. Begge kan kjedes.
- `std::cout`, `std::cin`, `std::cerr` er konsollstrømmene; `std::ifstream` / `std::ofstream` er filstrømmer.
- Foretrekk `"\n"` fremfor `std::endl` med mindre du spesifikt vil flushe.
- `std::getline` leser en hel linje, mellomrom inkludert.
- Filstrømmer lukker seg selv automatisk når de går ut av skop (RAII).
- Definer `operator<<` for dine egne klasser for å gjøre dem utskrivbare.
