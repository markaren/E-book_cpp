# Feilhåndtering

Programmer kjører sjelden i en perfekt verden. Filer forsvinner, brukere skriver inn ugyldige data, nettverkstilkoblinger faller ut, og aritmetikk kan gi umulige resultater. Å skrive programvare betyr å akseptere at ting _kommer_ til å gå galt, og å bestemme på forhånd hva du skal gjøre med det.

God feilhåndtering skiller to distinkte ansvarsområder:

1. **Oppdagelse:** å innse at noe gikk galt.
2. **Gjenoppretting:** å avgjøre hva som skal gjøres med det.

Å holde disse to ansvarsområdene adskilt, ofte i ulike deler av koden, gir renere programmer som er lettere å vedlikeholde.

---

## Returkoder: den enkle tilnærmingen {#return-codes-the-simple-approach}

Den mest direkte måten å signalisere feil på er å returnere en spesiell verdi fra en funksjon.

```cpp
#include <iostream>

// Returnerer resultatet, eller -1 for å signalisere en feil
int divide(int a, int b) {
    if (b == 0) {
        return -1; // vaktverdi for feil
    }
    return a / b;
}

int main() {
    int result = divide(10, 0);
    if (result == -1) {
        std::cout << "Error: division by zero\n";
    }
    return 0;
}
```

Dette virker i enkle tilfeller, men har reelle begrensninger etter hvert som programmer vokser:

- Kalleren kan **stille ignorere** returverdien, og feilen forsvinner.
- Vaktverdien (`-1` her) kan også være et legitimt resultat i andre sammenhenger.
- Hvert kallsted må sjekke returverdien, noe som roter til koden.
- Det finnes ingen enkel måte å bære en beskrivende feilmelding sammen med resultatet på.

---

## Unntak: C++-tilnærmingen {#exceptions-the-c-approach}

C++ har en dedikert mekanisme for feilhåndtering: **unntak** (exceptions). Tenk på det som en brannalarm: du sjekker ikke hele tiden om det brenner mens du lager mat, men hvis alarmen går, stopper alle det de holder på med og tar tak i det umiddelbart.

Det er tre nøkkelord:

| Nøkkelord | Formål |
|---------|---------|
| `throw` | Signaliser at noe gikk galt (dra i alarmen) |
| `try`   | Marker en kodeblokk som kan feile |
| `catch` | Håndter feilen når den oppstår |

```cpp
#include <iostream>
#include <stdexcept>

int divide(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero is not allowed.");
    }
    return a / b;
}

int main() {
    try {
        int result = divide(10, 0);
        std::cout << "Result: " << result << "\n";
    } catch (const std::invalid_argument& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
```

Når `throw` utføres, slutter programmet umiddelbart å kjøre den gjeldende funksjonen og leter oppover i kallstakken etter en `catch`-blokk som passer. Denne prosessen kalles **stack unwinding** (avvikling av stakken): idet hvert virkeområde mellom `throw` og `catch` forlates, får hvert lokale objekt i det virkeområdet destruktoren sin kalt underveis (se [RAII](../Chapter4/raii.md)).

> Hvis ingen passende `catch` finnes noe sted i kallstakken, kaller programmet `std::terminate()` og avbryter. Fang alltid unntak på et nivå der du kan håndtere dem på en meningsfull måte.

---

## Standard unntakstyper {#standard-exception-types}

C++-standardbiblioteket tilbyr et hierarki av unntakstyper som alle arver fra `std::exception`. Hvert standardunntak har en `.what()`-metode som returnerer en menneskelesbar beskrivelse av feilen.

```cpp
#include <iostream>
#include <stdexcept>

int main() {
    try {
        throw std::runtime_error("Something went wrong at runtime.");
    } catch (const std::exception& e) {
        // Fanger ethvert standardunntak
        std::cout << "Caught: " << e.what() << "\n";
    }
    return 0;
}
```

Ofte brukte standard unntakstyper (de fire første fra `<stdexcept>`):

| Type | Når den brukes |
|------|-------------|
| `std::runtime_error` | Generelle feil oppdaget under kjøring |
| `std::invalid_argument` | En funksjon mottok et argument med en ugyldig verdi |
| `std::out_of_range` | En indeks eller verdi er utenfor det gyldige området |
| `std::logic_error` | En bug i programlogikken (en brutt forutsetning) |
| `std::bad_alloc` | Minneallokering med `new` feilet |

De fire første bor i `<stdexcept>` og arver fra `std::logic_error` eller `std::runtime_error`. `std::bad_alloc` er avvikeren: den bor i `<new>` og arver *direkte* fra `std::exception`. Alle sammen fanges likevel av `catch (const std::exception&)`.

Du kan også fange _hvilket som helst_ unntak med `catch (...)`, men bruk dette sparsomt; det kaster bort all informasjon om feilen:

```cpp
try {
    // ...
} catch (const std::exception& e) {
    std::cout << "Standard exception: " << e.what() << "\n";
} catch (...) {
    std::cout << "Unknown exception caught\n";
}
```

---

## Egendefinerte unntak {#custom-exceptions}

For bibliotek- eller applikasjonskode kan du definere dine egne unntakstyper. Å arve fra `std::runtime_error` er den enkleste tilnærmingen: konstruktøren tar en meldingsstreng, og `.what()` virker automatisk.

```cpp
#include <iostream>
#include <stdexcept>
#include <string>

class FileNotFoundError : public std::runtime_error {
public:
    explicit FileNotFoundError(const std::string& filename)
        : std::runtime_error("File not found: " + filename) {}
};

void openFile(const std::string& filename) {
    // Lat som om filen ikke finnes
    throw FileNotFoundError(filename);
}

int main() {
    try {
        openFile("config.txt");
    } catch (const FileNotFoundError& e) {
        std::cout << "Could not open file: " << e.what() << "\n";
    } catch (const std::exception& e) {
        std::cout << "Other error: " << e.what() << "\n";
    }
    return 0;
}
```

Å definere egne unntakstyper lar kallere fange _spesifikke_ feilmodi og håndtere dem ulikt.

---

## RAII og unntakssikkerhet {#raii-and-exception-safety}

Du har allerede lært om [RAII](../Chapter4/raii.md). En av dets største fordeler er at det gjør kode **unntakssikker** automatisk.

Når et unntak kastes, garanterer C++ at destruktorene til alle lokale objekter kjøres mens stakken avvikles. Hvis en ressurs (en fil, en lås, en heap-allokering) forvaltes av en RAII-innpakning, blir den frigitt korrekt selv om et unntak kastes midt i en funksjon.

```cpp
#include <iostream>
#include <fstream>
#include <stdexcept>

void processFile(const std::string& filename) {
    std::ifstream file(filename); // RAII: filen lukkes automatisk når `file` går ut av virkeområdet

    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filename);
    }

    // ... behandle filen ...

} // destruktoren til `file` lukker filen her, selv om et unntak ble kastet ovenfor

int main() {
    try {
        processFile("data.txt");
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
```

> **Ikke** stol på at kode _etter_ en `throw`-setning kjører. Hvis du trenger at opprydding skjer, legg den i en destruktor.

### Å kaste fra en konstruktør {#throwing-from-a-constructor}

Når et [RAII](../Chapter4/raii.md)-objekt ikke klarer å skaffe ressursen det finnes for å forvalte — en fil som ikke lar seg åpne, en tilkobling som avvises — er den kanoniske måten å rapportere det på å **kaste fra konstruktøren**. En konstruktør har ingen returverdi, så å kaste er dens eneste kanal for å signalisere feil. Og regelen som gjør dette trygt, er presis: hvis en konstruktør kaster, regnes objektet som *aldri å ha eksistert*, så destruktoren til objektet vil **ikke** kjøre — men destruktorene til medlemmer som allerede er fullt konstruert *vil* kjøre, så en ressurs skaffet tidligere i den samme konstruktøren blir fortsatt frigitt rent.

---

## `std::optional`: når det å mislykkes er forventet {#stdoptional-when-failure-is-expected}

Noen ganger er fraværet av et resultat ikke en feil. Det er et normalt utfall. For eksempel kan et søk i en liste etter en verdi rett og slett ikke finne noe. Å kaste et unntak i det tilfellet ville vært misvisende, siden ingenting gikk galt.

C++17 introduserte `std::optional<T>`, som holder enten en verdi av type `T` eller ingenting i det hele tatt (`std::nullopt`).

```cpp
#include <iostream>
#include <optional>
#include <vector>
#include <string>

std::optional<int> findIndex(const std::vector<std::string>& items,
                             const std::string& target) {
    for (int i = 0; i < static_cast<int>(items.size()); ++i) {
        if (items[i] == target) {
            return i; // funnet, returner indeksen
        }
    }
    return std::nullopt; // ikke funnet, ingen verdi
}

int main() {
    std::vector<std::string> fruits = {"apple", "banana", "cherry"};

    auto index = findIndex(fruits, "banana");
    if (index) {
        std::cout << "Found at index " << *index << "\n";
    } else {
        std::cout << "Not found\n";
    }

    return 0;
}
```

Du kan sjekke om en `optional` holder en verdi med `if (result)` eller `result.has_value()`, og få tilgang til verdien med `*result` eller `result.value()`.

> Å kalle `.value()` på en tom `optional` kaster `std::bad_optional_access`. Foretrekk å sjekke først med `if (result)` før du henter verdien.

---

## Assertions: fange bugs, ikke håndtere feil {#assertions-catching-bugs-not-handling-errors}

Ikke alt som "går galt" er en *feil* du skal komme deg etter. Noen betingelser skal være **umulige** hvis koden din er korrekt — en funksjon som mottar et argument kalleren lovte aldri å sende, en indeks den omkringliggende logikken garanterer er gyldig. Når en av disse brytes, har du ikke en dårlig inndata som skal håndteres pent; du har en **bug** som skal finnes og fikses.

`assert` (fra `<cassert>`) er verktøyet for det. Du gir den en betingelse som må være sann. Hvis den noen gang ikke er det, skriver programmet ut betingelsen som feilet, filen og linjen, og avbryter umiddelbart:

```cpp
#include <cassert>
#include <iostream>

// Forutsetning: percent må være mellom 0 og 100
int dutyCycle(int percent) {
    assert(percent >= 0 && percent <= 100);   // en bug hvis dette noen gang er usant
    return percent * 255 / 100;                // skaler til området 0–255
}

int main() {
    std::cout << dutyCycle(50) << "\n";   // 127
    // dutyCycle(150);  // ville avbrutt i et debug-bygg: assertion feilet
}
```

Poenget er å feile **høylytt og tidlig**, akkurat der feilen er, i stedet for å returnere en stille gal verdi som krasjer mystisk tre funksjoner senere.

Én avgjørende egenskap: **assertions fjernes fra release-bygg.** Når programmet kompileres med `NDEBUG` definert (den vanlige "release"-innstillingen), forsvinner hver `assert` og koster ingenting ved kjøring. To regler følger:

- **Legg aldri kode med sideeffekter inne i en `assert`.** `assert(connect());` ville sluttet å koble til i et release-bygg. Assert *betingelsen*, aldri en handling.
- **Bruk aldri `assert` for feil som skjer i normal bruk** — dårlig brukerinndata, en manglende fil, en tilkobling som faller ut. De er *forventede*; håndter dem med unntak eller `std::optional`. `assert` er bare for "dette kan ikke skje med mindre jeg har gjort en feil".

### `static_assert`: sjekker ved kompilering {#static_assert-checks-at-compile-time}

En nær slektning, `static_assert`, sjekker en betingelse mens programmet *kompileres* i stedet for mens det kjører. Den er for antakelser om typer og størrelser — hendig i portabel eller innebygd kode:

```cpp
static_assert(sizeof(int) >= 4, "this code assumes a 32-bit int");
```

Hvis betingelsen er usann, kompilerer koden rett og slett ikke, og du får meldingen. Det er ingen kjøretidskostnad, fordi det ikke er noen kjøretidssjekk.

---

## Beste praksis {#best-practices}

### Kast som verdi, fang som referanse {#throw-by-value-catch-by-reference}

Kast (`throw`) alltid unntaksobjekter som verdi, og fang (`catch`) dem som `const`-referanse. Dette unngår unødvendige kopier og forhindrer **object slicing**.

```cpp
throw std::runtime_error("something failed"); // kast som verdi

catch (const std::runtime_error& e) { ... }   // fang som const-referanse
```

### Unntak er for unntakstilfeller {#exceptions-are-for-exceptional-situations}

Ikke bruk unntak til å styre normal programflyt (f.eks. å avslutte en løkke). Unntak er for tilstander som representerer en feil — noe kalleren ikke kan forventes å håndtere lokalt. For forventede "ikke noe resultat"-situasjoner, foretrekk `std::optional`.

### Fang på riktig nivå {#catch-at-the-right-level}

Fang et unntak der du kan **gjenopprette på en meningsfull måte**. Å fange et unntak bare for umiddelbart å kaste det videre (uten noen gjenopprettingslogikk) tilfører støy uten gevinst.

### Velg riktig verktøy {#choose-the-right-tool}

| Situasjon | Foretrukket tilnærming |
|-----------|-------------------|
| Funksjonen finner kanskje ikke et resultat (normalt tilfelle) | `std::optional` |
| Noe gikk galt som kalleren må håndtere | Unntak |
| Ytelseskritisk kode, enkel feilsignalisering | Returkode eller `bool` |
| En betingelse som skal være umulig med mindre det finnes en bug | `assert` |

### Bruk RAII for å garantere opprydding {#use-raii-to-guarantee-cleanup}

Kall aldri oppryddingskode (`delete`, `fclose`, osv.) manuelt i en `catch`-blokk. Du kommer til å glemme å duplisere den på hver kodevei. Pakk i stedet ressurser inn i RAII-typer, slik at de rydder opp etter seg selv automatisk, enten et unntak kastes eller ikke.
