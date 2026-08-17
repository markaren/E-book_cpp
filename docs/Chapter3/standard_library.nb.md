# Standardbiblioteket i C++

C++ sitt standardbibliotek er samlingen av beholdere, algoritmer og verktøy som følger med enhver C++-kompilator. Det er det `std::cout`, `std::vector` og `std::string` hører til.

Å kjenne det godt er forskjellen på å skrive flytende, idiomatisk C++ og å finne opp hjulet på nytt. Biblioteket har blitt raffinert i flere tiår; uansett hva du vurderer å skrive, er sjansen svært god for at det allerede finnes der.

Dette kapittelet er en guidet omvisning i delene du kommer til å bruke dette semesteret. Det er ikke et oppslagsverk; til det, se [cppreference.com](https://en.cppreference.com/). Målet her er å vite *hva som finnes*, slik at du kan slå det opp når du trenger det.

---

## `std::`-prefikset {#the-std-prefix}

Alt i standardbiblioteket ligger i navnerommet `std`. Du skriver `std::vector`, ikke `vector`. Prefikset forteller lesere (og kompilatoren) at du mener *den* typen fra standardbiblioteket, ikke noe du har skrevet selv.

Du kan utelate prefikset ved å skrive `using namespace std;` øverst i en fil. Det bør du ikke. I små programmer er det harmløst; i større trekker det hvert eneste navn i standardbiblioteket inn i skopet og skaper navnekollisjoner med din egen kode. Venn deg til å skrive `std::` overalt.

---

## Beholdere: samlinger av verdier {#containers-collections-of-values}

En beholder holder en samling av verdier. Valget mellom dem avhenger av hva du trenger å gjøre med dem.

### `std::vector<T>`: et array som kan endre størrelse {#stdvectort-a-resizable-array}

Beholderen du kommer til å bruke 80 % av tiden. Elementene lagres sammenhengende i minnet, du kan la den vokse og krympe ved kjøring, og indeksert tilgang tar konstant tid.

```cpp
#include <vector>

std::vector<int> readings = {17, 42, 99, 8};

readings.push_back(5);           // legg til på slutten
int first = readings[0];          // indekstilgang (ingen grensesjekk)
int safer = readings.at(0);       // grensesjekket; stopper programmet med en feil hvis den ikke håndteres (kapittel 6)

readings.size();                  // antall elementer
readings.empty();                 // true hvis size == 0
```

Iterer med en range-basert `for`:

```cpp
for (int value : readings) {
    std::cout << value << "\n";
}
```

**Når du bør bruke den:** som standard, for enhver "liste med ting". Grip til noe annet bare hvis målinger sier at du trenger det.

### `std::array<T, N>`: et array med fast størrelse {#stdarrayt-n-a-fixed-size-array}

En tryggere erstatning for C-stil-arrayet. Størrelsen er fast ved kompilering; det er ingen heap-allokering, elementene bor inne i selve objektet.

```cpp
#include <array>

std::array<int, 4> readings = {17, 42, 99, 8};
readings.size();   // 4, kjent ved kompilering
readings[2];        // 99
```

**Når du bør bruke den:** antall elementer er kjent ved kompilering og kommer ikke til å endre seg. Nyttig for sensordata med fast lengde, oppslagstabeller og matrisedimensjoner.

### `std::string`: en streng av tegn {#stdstring-a-string-of-characters}

Tekst. Overalt der du ville brukt `char[]` i C, bruker du `std::string` i C++.

```cpp
#include <string>

std::string name = "Alice";
name += " Smith";           // sammenslåing
name.length();              // 11
name.substr(0, 5);          // "Alice"
name.find("Smith");          // 6, indeksen der "Smith" starter
```

Se [Strenger](../strings.md), senere i dette kapittelet, for en omvisning i operasjonene du oftest vil gripe til.

### `std::map<K, V>`: et sortert nøkkel/verdi-lager {#stdmapk-v-a-sorted-key-value-store}

Kobler nøkler til verdier. Nøklene holdes sortert, så oppslag er O(log n).

```cpp
#include <map>

std::map<std::string, int> wordCount;
wordCount["hello"] = 1;
wordCount["world"] = 2;
++wordCount["hello"];        // nå 2

for (const auto& [word, count] : wordCount) {   // [word, count] deler opp hvert nøkkel/verdi-par
    std::cout << word << ": " << count << "\n";
}
```

`[word, count]` er en *strukturert binding* — den pakker ut paret i to navngitte variabler, slik at du kan skrive `word` og `count` i stedet for `.first` og `.second`.

### `std::unordered_map<K, V>`: et hash-basert nøkkel/verdi-lager {#stdunordered_mapk-v-a-hash-based-key-value-store}

Samme daglige bruk som `std::map`, men usortert og raskere i gjennomsnitt (oppslag i konstant tid). Den dropper de ordnede operasjonene — ingen sortert iterasjon, ingen *range queries* — siden en hashtabell ikke har noe begrep om rekkefølge.

```cpp
#include <unordered_map>

std::unordered_map<std::string, int> fast;
fast["temperature"] = 22;
```

**Å velge mellom map og unordered_map:** unordered er raskere, ordered holder ting sortert (praktisk for iterasjon i sortert rekkefølge eller *range queries*). Trenger du ikke rekkefølge, er `unordered_map` vanligvis det riktige standardvalget.

### `std::set` og `std::unordered_set` {#stdset-and-stdunordered_set}

Som `map` og `unordered_map`, men de lagrer bare *nøkler*, ingen verdier. Bruk dem når du trenger å holde styr på "har jeg sett denne før?" — duplikater forkastes stille.

```cpp
#include <set>

std::set<int> uniqueReadings;
uniqueReadings.insert(42);
uniqueReadings.insert(42);   // ignorert, finnes allerede
uniqueReadings.contains(42); // true
```

### Andre beholdere {#other-containers}

`std::list` (dobbeltlenket liste), `std::deque` (dobbeltendet kø), `std::stack` og `std::queue` finnes for tilfellene der `vector` ikke passer. I et første semester kan du behandle dem som "dette slår jeg opp hvis jeg trenger det"; `vector` og `map` dekker nesten alt.

---

## Algoritmer: gjenbrukbare operasjoner på beholdere {#algorithms-reusable-operations-on-containers}

Headeren `<algorithm>` inneholder dusinvis av frie funksjoner som virker på *enhver* beholder (via iteratorer). En håndfull du kommer til å gripe til gang på gang:

```cpp
#include <algorithm>
#include <numeric>
#include <vector>

std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

std::sort(v.begin(), v.end());            // sorter stigende: 1 1 2 3 4 5 6 9

auto it = std::find(v.begin(), v.end(), 4);
if (it != v.end()) {
    // funnet, *it == 4
}

int ones   = std::count(v.begin(), v.end(), 1);     // 2 (hvor mange 1-ere)
int total  = std::accumulate(v.begin(), v.end(), 0); // 31
int maxVal = *std::max_element(v.begin(), v.end());  // 9
```

Paret `.begin()`/`.end()` dukker opp overalt. Det sier "operer på hele dette området". Det finnes versjoner som tar en egendefinert sammenligningsfunksjon (for `sort`) eller et predikat (for `find_if`, `count_if`), som lar deg bestemme hva "mindre enn" eller "passer" betyr for dine data.

---

## Iteratorer {#iterators}

Du har kanskje lagt merke til at hver algoritme over tok `v.begin()` og `v.end()`, ikke `v` selv. Det er **iteratorer** — standardbibliotekets måte å referere til en *posisjon* i en beholder på.

Se for deg en iterator som et bokmerke:

- `v.begin()` markerer det første elementet.
- `v.end()` markerer *én forbi* det siste — en stoppmarkør, ikke et ekte element.
- `*it` leser elementet på den posisjonen — følg bokmerket til det det markerer.
- `++it` går videre til neste element.

Å gå gjennom en beholder for hånd ser slik ut:

```cpp
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << "\n";
}
```

Det er nøyaktig det den range-baserte `for (int x : v)` du allerede bruker gjør under panseret, så denne løkken skriver du sjelden selv. Men den forklarer *hvorfor* algoritmer tar et `begin, end`-par i stedet for selve beholderen: ved å snakke bare "iterator" virker én og samme `std::sort` på en `vector`, et `array`, en `std::string` eller hva som helst annet som kan dele ut iteratorer. Beholderen og algoritmen trenger aldri å vite om hverandre — iteratorene er limet mellom dem.

---

## Ranges (C++20) {#ranges-c20}

Å sende `v.begin(), v.end()` hver gang er støy; du mener nesten alltid "hele greia". C++20 sine **ranges** lar deg si nettopp det. De fleste algoritmene fra forrige seksjon har en `std::ranges::`-versjon (i den samme `<algorithm>`-headeren) som tar beholderen direkte:

```cpp
std::ranges::sort(v);                  // i stedet for std::sort(v.begin(), v.end())
auto it = std::ranges::find(v, 4);     // i stedet for std::find(v.begin(), v.end(), 4)
```

Én vanlig algoritme har *ingen* ranges-form i C++20: `std::accumulate` (den bor i `<numeric>`, ikke `<algorithm>`). Fortsett å kalle den med `begin(), end()`-paret — den range-baserte foldingen, `std::ranges::fold_left`, kom først i C++23.

Foretrekk disse i ny kode — dette kurset bruker C++20 — fordi de er kortere og tetter en reell felle: du kan ikke lenger ved et uhell pare `begin()` fra én beholder med `end()` fra en annen.

Ranges legger også til **views** (fra `<ranges>`): late, komponerbare steg du kjeder sammen med røret `|`. Ingenting beregnes eller kopieres før du itererer over resultatet.

```cpp
std::vector<int> v = {1, 2, 3, 4, 5, 6};

// kvadratene av bare partallene, beregnet ved behov
for (int n : v | std::views::filter([](int x) { return x % 2 == 0; })
                | std::views::transform([](int x) { return x * x; })) {
    std::cout << n << " ";          // 4 16 36
}
```

De `[](int x) { … }`-bitene er [lambda-uttrykk](../lambdas.md) — små funksjoner skrevet rett i koden, dekket i detalj senere i dette kapittelet. Views er kraftige, og du kommer til å møte dem mer etter hvert; foreløpig holder det å kjenne igjen `|`-stilen når du ser den, og å gripe til `std::ranges::sort(v)` og venner for å slippe `begin()`/`end()`-støyen.

---

## Andre nyttige typer {#other-handy-types}

### `std::optional<T>`: en verdi som kan mangle {#stdoptionalt-a-value-that-might-be-absent}

```cpp
#include <optional>

std::optional<int> findReading(int id) {
    if (id < 0) {
        return std::nullopt;   // ingen avlesning for en ugyldig id
    }
    return 42;                 // lat som om vi fant en avlesning
}

auto r = findReading(7);
if (r) {
    std::cout << *r << "\n";
}
```

Dekkes i detalj i [kapittelet om feilhåndtering](../Chapter6/error_handling.md#stdoptional-when-failure-is-expected).

### `std::chrono`: tid og varigheter {#stdchrono-time-and-durations}

```cpp
#include <chrono>
#include <thread>

auto start = std::chrono::steady_clock::now();
// ... gjør arbeid ...
auto elapsed = std::chrono::steady_clock::now() - start;
auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count();
std::cout << "took " << ms << " ms\n";

std::this_thread::sleep_for(std::chrono::milliseconds(500));
```

### `std::filesystem`: filer og mapper {#stdfilesystem-files-and-directories}

```cpp
#include <filesystem>

namespace fs = std::filesystem;

if (fs::exists("config.txt")) {
    auto size = fs::file_size("config.txt");
}

for (const auto& entry : fs::directory_iterator(".")) {
    std::cout << entry.path() << "\n";
}
```

### `<cmath>`: matematiske funksjoner {#cmath-mathematical-functions}

```cpp
#include <cmath>

double r = std::sqrt(2.0);
double s = std::sin(3.14159);
double e = std::exp(1.0);
```

---

## C-standardbiblioteket {#the-c-standard-library}

`<cmath>` over er én bit av **C-standardbiblioteket**, som C++ arver i sin helhet. Hver C-header finnes i to stavemåter: det opprinnelige C-navnet `<xxx.h>`, og et C++-navn `<cxxx>` som tilbyr de samme tingene gjennom navnerommet `std::`.

| C-header | C++-header | Gir deg |
|----------|------------|-----------|
| `<math.h>`   | `<cmath>`   | `std::sqrt`, `std::sin`, `std::pow` |
| `<stdlib.h>` | `<cstdlib>` | `std::abs`, `std::atoi`, `std::rand` |
| `<string.h>` | `<cstring>` | `std::strlen`, `std::memcpy` |
| `<stdint.h>` | `<cstdint>` | `std::uint8_t`, `std::int32_t` |
| `<stdio.h>`  | `<cstdio>`  | `std::printf`, `std::fopen` |

På skrivebordet, **foretrekk alltid `<cxxx>`-formen** og skriv `std::`-navnene (`std::sqrt`, `std::uint8_t`). Det holder kall til C-biblioteket konsistente med resten av standardbiblioteket; `<xxx.h>`-formen slipper i stedet de samme navnene rett ut i det globale navnerommet.

(Ett unntak: en liten mikrokontroller leveres ofte bare med C-headerne `<xxx.h>` — der bruker du `<stdint.h>` og en naken `uint8_t`. Se [Arduino vs. desktop-C++](../arduino_vs_desktop.md).)

---

## Strømmer {#streams}

Inn- og utdata i C++ gjøres gjennom strømobjekter: `std::cout` for konsollutskrift, `std::cin` for inndata, `std::ifstream` og `std::ofstream` for filer. Disse får sin egen behandling i [Inndata, utdata og filstrømmer](../Chapter4/io_streams.md).

---

## Hvordan lære biblioteket {#how-to-learn-the-library}

Du kommer ikke til å memorere standardbiblioteket. Det har ingen gjort. Det du bygger opp over tid, er **oversikt**: du husker at det finnes *noe* for en gitt oppgave, og du slår opp den nøyaktige stavemåten på cppreference.

To vaner du bør starte med nå:

1. **Hver gang du skal til å skrive en løkke eller en hjelpefunksjon, sjekk om standardbiblioteket allerede har den.** Telle elementer? `std::count`. Fjerne duplikater? `std::unique`. Sortere? `std::sort`. Biblioteket har allerede løst de fleste av de vanlige problemene.
2. **Bokmerk [cppreference.com](https://en.cppreference.com/).** Hvert symbol i standardbiblioteket har en side med signatur, oppførsel, kompleksitet, eksempler og hvilken header som må inkluderes. Det er den nyttigste enkeltressursen i C++.

---

## Oppsummering {#summary}

- Standardbiblioteket ligger i navnerommet `std::`. Skriv alltid prefikset.
- `std::vector` er standardbeholderen din. `std::string` for tekst. `std::map` / `std::unordered_map` for nøkkel/verdi-oppslag.
- `<algorithm>` har dusinvis av funksjoner som virker på enhver beholder: sortere, finne, telle, akkumulere.
- Algoritmer når beholdere gjennom **iteratorer** (`begin()`/`end()`); C++20 sine **ranges** lar deg sende beholderen direkte — `std::ranges::sort(v)`.
- `<optional>`, `<chrono>`, `<filesystem>` og `<cmath>` dekker de fleste dagligdagse behov utover beholdere.
- Hele **C-standardbiblioteket** er tilgjengelig; på skrivebordet, foretrekk `<cXX>`-stavemåten (`<cmath>`, `<cstdint>`, …) slik at navnene dets holder seg bak `std::`.
- Slå ting opp på cppreference i stedet for å memorere signaturer.
