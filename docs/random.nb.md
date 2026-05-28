# Tilfeldige tall

Før eller siden trenger du tilfeldighet — et terningkast, en stokket liste, en støyete sensoravlesning i en [simulering](tank_control/v1_classes.md). C++ har en riktig måte å gjøre dette på, og en gammel, ødelagt måte du vil se overalt på nettet. Denne siden viser den riktige måten.

> **Kortversjonen:** `#include <random>`, lag én **generator** og gi den en startverdi én gang, og trekk så tall gjennom en **fordeling**. Bruk aldri `rand() % n`.

---

## Den gamle måten, og hvorfor du bør unngå den

Du vil se dette overalt:

<!-- no-ce -->
```cpp
#include <cstdlib>
#include <ctime>

std::srand(std::time(nullptr));    // gi en startverdi én gang
int roll = std::rand() % 6 + 1;    // et tall fra 1 til 6 ... på et vis
```

Den kjører, men har reelle problemer:

- **`% 6` er skjev.** `rand()` returnerer en verdi fra et fast område hvis størrelse sjelden er et nøyaktig multiplum av 6, så noen utfall dukker opp litt oftere enn andre. For en terning merker du det kanskje ikke; for noe som betyr noe, vil du det.
- **`rand()` er av lav kvalitet.** Sekvensen den lager er dårlig etter moderne målestokk og varierer mellom kompilatorer.
- **Den er klønete å styre.** Én skjult global generator, delt av alt.

Moderne C++ erstattet alt dette i 2011 med `<random>`-headeren. Bruk den.

---

## Den riktige måten: `<random>`

Tre deler — en **kilde til startverdi**, en **generator** (motoren) og en **fordeling** (formen):

<!-- no-ce -->
```cpp
#include <random>

std::random_device rd;                          // 1. en kilde til en tilfeldig startverdi
std::mt19937 gen(rd());                          // 2. generatoren, gitt en startverdi én gang
std::uniform_int_distribution<int> die(1, 6);    // 3. formen på tallene

int roll = die(gen);   // et rettferdig heltall i [1, 6]
```

- **`std::random_device`** lager et tall som er vanskelig å forutsi, brukt én gang til å gi generatoren en startverdi.
- **`std::mt19937`** er *Mersenne Twister* — standardgeneratoren av god kvalitet til generelt bruk. Lag den **én gang** og gjenbruk den.
- **Fordelingen** gjør generatorens rå utdata om til tallene du faktisk vil ha, i området du vil ha, uten skjevhet. Du trekker en verdi ved å kalle den med generatoren: `die(gen)`.

---

## Velge en fordeling

| Du vil ha | Fordeling | Eksempel |
|-----------|-----------|----------|
| Et heltall i et område | `std::uniform_int_distribution<int>` | `{1, 6}` — en terning |
| Et desimaltall i et område | `std::uniform_real_distribution<double>` | `{0.0, 1.0}` |
| En "klokkekurve" rundt et gjennomsnitt | `std::normal_distribution<double>` | `{mean, stddev}` — sensorstøy |
| Et sant/usant myntkast | `std::bernoulli_distribution` | `{0.3}` — sant 30 % av tiden |

`uniform_int_distribution` inkluderer **begge** endepunktene: `{1, 6}` kan returnere 1, 6 og alt imellom.

For å **stokke** en beholder, bruk `std::shuffle` (fra `<algorithm>`), som tar generatoren din — ikke den gamle `std::random_shuffle`, som ble fjernet i C++17:

<!-- no-ce -->
```cpp
std::shuffle(deck.begin(), deck.end(), gen);
```

---

## Lag generatoren én gang

Den vanligste feilen med `<random>` er å lage generatoren (eller verre, en ny `random_device`) *hver gang* du trenger et tall:

<!-- no-ce -->
```cpp
int badRoll() {
    std::mt19937 gen(std::random_device{}());      // FEIL: laget på nytt ved hvert kall
    std::uniform_int_distribution<int> die(1, 6);
    return die(gen);
}
```

Det er tregt, og på noen verktøykjeder returnerer det nesten samme verdi hvert kall. Bygg generatoren **én gang** og gjenbruk den — hold den som et klassemedlem, eller send den rundt ved referanse:

<!-- no-ce -->
```cpp
class Dice {
    std::mt19937 gen_{std::random_device{}()};    // startverdi gitt én gang, når en Dice opprettes
    std::uniform_int_distribution<int> die_{1, 6};
public:
    int roll() { return die_(gen_); }             // gjenbruk den ved hvert kall
};
```

---

## Reproduserbare kjøringer

`random_device` gir en forskjellig sekvens hver kjøring. For en **test**, eller en **simulering du vil gjenta nøyaktig**, gi en fast startverdi i stedet:

<!-- no-ce -->
```cpp
std::mt19937 gen(42);   // samme startverdi → samme sekvens, hver kjøring
```

Dette er uvurderlig ved feilsøking: en kjøring som feiler blir reproduserbar. Tank-simuleringens utvidelse med en støyete sensor bruker nettopp dette — en fast startverdi gjør den "tilfeldige" støyen repeterbar mens du jobber med regulatoren.

> **En MinGW-felle.** På noen verktøykjeder — særlig eldre MinGW, som CLion kan ha med på Windows — er `std::random_device` **ikke faktisk tilfeldig**: den returnerer samme sekvens hver kjøring. Hvis programmets "tilfeldige" tall aldri endrer seg mellom kjøringer, er dette grunnen. Gi en startverdi fra klokken i stedet: `std::mt19937 gen(std::chrono::steady_clock::now().time_since_epoch().count());` (fra `<chrono>`).

---

## Et gjennomgått eksempel: en støyete sensor

Alt satt sammen — en nivåavlesning med gaussisk støy, av typen du ville lagt til [tank-simuleringen](tank_control/v2_sensors.md):

```cpp
#include <iostream>
#include <random>

int main() {
    std::mt19937 gen(42);                               // fast startverdi: repeterbar
    std::normal_distribution<double> noise(0.0, 0.05);  // gjennomsnitt 0, standardavvik 0.05 m

    double trueLevel = 5.0;
    for (int i = 0; i < 5; ++i) {
        double reading = trueLevel + noise(gen);        // sann verdi + vingling
        std::cout << "reading = " << reading << " m\n";
    }
}
```

Hver `noise(gen)` er en liten positiv eller negativ vingling rundt null; lagt til det sanne nivået modellerer den en ekte sensor som aldri er helt presis.

---

## Oppsummering

- `#include <random>`. Glem `rand()` og `srand()`.
- Tre deler: en **startverdi** (`std::random_device`), en **generator** (`std::mt19937`) og en **fordeling**.
- Lag generatoren **én gang** og gjenbruk den — aldri per kall.
- Velg en fordeling for formen du vil ha; den håndterer området uten skjevhet.
- Gi en **fast startverdi** for tester og repeterbare simuleringer.
- Hvis tilfeldige tall gjentar seg hver kjøring på Windows/MinGW, gi en startverdi fra klokken i stedet.
- Reellverdige fordelinger gir `double`-er — sammenlign dem med omhu; se [Flyttall-fallgruver](floating_point.md).
