# Testing

Se for deg at du sender en viktig e-post uten å korrekturlese den, bare for å oppdage feilen i det øyeblikket den lander i innboksen til noen. Testing er vanen med å sjekke arbeidet ditt *før* det leveres. I programvare betyr det å skrive små, automatiserte sjekker som verifiserer at enkeltdeler av koden gjør nøyaktig det de skal.

En **enhetstest** er et program som kaller koden din, gir den bestemte inndata og påstår at utdataene stemmer med det du forventer. Gjør de det, består testen. Hvis ikke, feiler testen, og du vet nøyaktig hvor du skal lete.

Fordeler du raskt vil merke:

- Fang bugs før de når andre deler av programmet.
- Endre kode med trygghet: hvis du ødelegger noe, forteller en test deg det umiddelbart.
- Tester fungerer også som dokumentasjon: de viser *hvordan* en funksjon er ment å brukes.

---

## Introduksjon til Catch2 {#introducing-catch2}

**Catch2** er et populært testrammeverk for C++. Det lar deg skrive tester i vanlig C++ uten at du trenger å skrive en `main()`-funksjon selv. Catch2 stiller med den for deg.

Hvorfor Catch2?

- Testkode leses nesten som vanlig engelsk: `REQUIRE(result == 5)`.
- Integrerer naturlig med CMake.
- Mye brukt i industrien og i åpen kildekode-prosjekter.

---

## Prosjektoppsett {#project-setup}

Et prosjekt med tester bruker et lite, standard oppsett som du allerede så i [CMake-introduksjonen](../Chapter2/cmake_intro.md):

```
MyProject/
├── CMakeLists.txt
├── include/
│   └── calculator.hpp
├── src/
│   └── calculator.cpp
└── tests/
    └── test_calculator.cpp
```

### CMakeLists.txt {#cmakeliststxt}

Catch2 må lastes ned og lenkes inn før testene dine kan bruke det. Utsnittet nedenfor bruker `FetchContent`, en CMake-funksjon som håndterer dette automatisk.

> Å hente inn et bibliotek med `FetchContent` dekkes i [Å konsumere tredjepartsbiblioteker](../Chapter2/cmake_intro.md#consuming-third-party-libraries). Foreløpig kan du bruke denne CMakeLists.txt som en ferdig mal for ethvert prosjekt som bruker Catch2.

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject)

set(CMAKE_CXX_STANDARD 20)

# --- Hent Catch2 fra GitHub ---
include(FetchContent)
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG        v3.5.2
)
FetchContent_MakeAvailable(Catch2)

# --- Biblioteket ditt (koden som testes) ---
add_library(calculator src/calculator.cpp)
target_include_directories(calculator PUBLIC include)

# --- Testprogrammet ---
add_executable(tests tests/test_calculator.cpp)
target_link_libraries(tests PRIVATE calculator Catch2::Catch2WithMain)

# --- Registrer det hos CTest slik at `ctest` kan kjøre testene ---
include(CTest)
add_test(NAME tests COMMAND tests)
```

Nøkkellinjen er `target_link_libraries(tests PRIVATE calculator Catch2::Catch2WithMain)`. Den lenker koden din og Catch2 (inkludert dets innebygde `main()`) sammen til én test-binærfil. De to siste linjene registrerer den binærfilen hos **CTest** (`ctest`-kjøreren som brukes nedenfor), så du slipper å huske dem som et eget steg.

---

## Klassen som testes {#the-class-under-test}

Før du skriver tester, trenger du noe å teste. Her er en enkel `Calculator`-klasse med fire operasjoner. Divisjon kaster en `std::invalid_argument` når divisoren er null, et mønster du så i kapittelet om [feilhåndtering](error_handling.md).

**`include/calculator.hpp`**

```cpp
#pragma once
#include <stdexcept>

class Calculator {
public:
    double add(double a, double b);
    double subtract(double a, double b);
    double multiply(double a, double b);
    double divide(double a, double b);
};
```

**`src/calculator.cpp`**

```cpp
#include "calculator.hpp"

double Calculator::add(double a, double b) {
    return a + b;
}

double Calculator::subtract(double a, double b) {
    return a - b;
}

double Calculator::multiply(double a, double b) {
    return a * b;
}

double Calculator::divide(double a, double b) {
    if (b == 0) {
        throw std::invalid_argument("Cannot divide by zero.");
    }
    return a / b;
}
```

---

## Å skrive tester med Catch2 {#writing-tests-with-catch2}

Opprett `tests/test_calculator.cpp`. Makroene disse testene bruker — `TEST_CASE`, `REQUIRE`, `CHECK`, `REQUIRE_THROWS` — bor alle i én Catch2-header:

```cpp
#include <catch2/catch_test_macros.hpp>
```

I tillegg `#include`-r du det du tester (her `calculator.hpp` — se den komplette filen nedenfor). Catch2 holder mer avanserte verktøy, som matchers og generatorer, i separate headere, men dem trenger du ikke ennå.

### Kjernemakroer {#core-macros}

| Makro | Oppførsel |
|-------|-----------|
| `TEST_CASE("description")` | Deklarerer en navngitt, uavhengig test |
| `REQUIRE(expression)` | Påstår at `expression` er sant; stopper testen umiddelbart ved feil |
| `CHECK(expression)` | Påstår at `expression` er sant; fortsetter å kjøre selv ved feil |
| `REQUIRE_THROWS(expression)` | Påstår at `expression` kaster et eller annet unntak |
| `REQUIRE_THROWS_AS(expression, Type)` | Påstår at `expression` kaster et unntak av nøyaktig typen `Type` |

### En komplett testfil {#a-complete-test-file}

```cpp
#include <catch2/catch_test_macros.hpp>
#include "calculator.hpp"

TEST_CASE("addition returns the correct sum") {
    Calculator calc;
    REQUIRE(calc.add(2.0, 3.0) == 5.0);
    REQUIRE(calc.add(-1.0, 1.0) == 0.0);
    REQUIRE(calc.add(0.0, 0.0) == 0.0);
}

TEST_CASE("subtraction returns the correct difference") {
    Calculator calc;
    REQUIRE(calc.subtract(10.0, 4.0) == 6.0);
    REQUIRE(calc.subtract(0.0, 5.0) == -5.0);
}

TEST_CASE("multiplication returns the correct product") {
    Calculator calc;
    REQUIRE(calc.multiply(3.0, 4.0) == 12.0);
    REQUIRE(calc.multiply(-2.0, 5.0) == -10.0);
    REQUIRE(calc.multiply(0.0, 99.0) == 0.0);
}

TEST_CASE("division returns the correct quotient") {
    Calculator calc;
    REQUIRE(calc.divide(10.0, 2.0) == 5.0);
    REQUIRE(calc.divide(7.0, 2.0) == 3.5);
}

TEST_CASE("division by zero throws an exception") {
    Calculator calc;
    REQUIRE_THROWS(calc.divide(10.0, 0.0));                            // kaster *noe*
    REQUIRE_THROWS_AS(calc.divide(10.0, 0.0), std::invalid_argument);  // ...av den *riktige* typen
}
```

`REQUIRE_THROWS_AS` fastslår ikke bare *at* det kastes, men *hva* som kastes — den samme "fang en spesifikk feilmodus"-ideen fra [Feilhåndtering](error_handling.md#custom-exceptions). Hvis noen senere endret `divide` til å kaste en ren `std::runtime_error`, ville den løse `REQUIRE_THROWS` fortsatt bestå, men denne strengere sjekken ville slått rødt.

Hver `TEST_CASE` er uavhengig: den oppretter sitt eget `Calculator`-objekt og kjører fra bunnen av.

> Disse testene sammenligner `double`-verdier med `==`, noe som virker *her* bare fordi hver valgt verdi (`5.0`, `3.5`, `-10.0`, …) er eksakt representerbar binært. Generelt må du **ikke** sammenligne flyttallsresultater med `==` — avrunding gjør at `0.1 + 0.2 != 0.3` — så sammenlign innenfor en toleranse i stedet: Catch2s `Approx` (brukt gjennomgående i [versjon 5 av tankreguleringen](../tank_control/v5_tests.md)) eller teknikkene i [Flyttall-fallgruver](../floating_point.md#compare-with-a-tolerance).

---

## Å kjøre testene {#running-the-tests}

Bygg og kjør testene dine med CMake på samme måte som du bygger ethvert prosjekt:

```bash
cmake -S . -B build
cmake --build build
```

**Alternativ 1: kjør test-binærfilen direkte.**

```bash
./build/tests
```

Catch2 skriver ut én linje per test og en oppsummering til slutt:

```
===============================================================================
All tests passed (12 assertions in 5 test cases)
```

Hvis en test feiler, viser den nøyaktig linje og verdiene som ikke stemte:

```
test_calculator.cpp:8: FAILED:
  REQUIRE( calc.add(2.0, 3.0) == 6.0 )
with expansion:
  5.0 == 6.0
```

**Alternativ 2: bruk CTest** (CMakes testkjører):

```bash
ctest --test-dir build
```

Dette virker fordi malen allerede registrerte kjøreren (`include(CTest)` + `add_test`); `ctest` finner den og rapporterer bestått/feilet. CTest er standardmåten å kjøre tester på i CMake-prosjekter og det de fleste automatiserte byggesystemer (CI-pipelines) bruker. (`--test-dir` krever CMake 3.20 eller nyere, og det er derfor malen ber om nettopp det; på en eldre CMake, kjør `cd build` først og deretter bare `ctest`.)

---

## `SECTION`: gruppere beslektede sjekker {#section-grouping-related-checks}

Når flere sjekker deler oppsettkode, kan du gruppere dem med `SECTION`. Hver `SECTION` kjører uavhengig, men alle deler det samme `TEST_CASE`-oppsettet øverst.

```cpp
TEST_CASE("multiplication handles various inputs") {
    Calculator calc;

    SECTION("positive numbers") {
        REQUIRE(calc.multiply(2.0, 3.0) == 6.0);
        REQUIRE(calc.multiply(10.0, 10.0) == 100.0);
    }

    SECTION("one factor is zero") {
        REQUIRE(calc.multiply(0.0, 42.0) == 0.0);
        REQUIRE(calc.multiply(42.0, 0.0) == 0.0);
    }

    SECTION("negative numbers") {
        REQUIRE(calc.multiply(-2.0, 3.0) == -6.0);
        REQUIRE(calc.multiply(-2.0, -3.0) == 6.0);
    }
}
```

Linjen `Calculator calc;` kjører én gang for hver seksjon, slik at hver seksjon får et ferskt objekt.

---

## Hva kjennetegner en god test? {#what-makes-a-good-test}

**Test én ting per `TEST_CASE`.** En test som heter `"addition returns the correct sum"`, bør bare teste addisjon. Hvis den feiler, vet du nøyaktig hva som røk.

**Test grensene, ikke bare midten.** Null, negative tall, tomme strenger og maksimumsverdier er der bugs gjemmer seg. Tester som bare dekker normaltilfellet — "happy path" — overser de fleste virkelige problemer.

**Test feiltilfellene.** Hvis koden din skal kaste (eller returnere en feil), skriv en test som verifiserer at den faktisk gjør det.

**Hold testene uavhengige.** Ingen test bør avhenge av at en annen test kjører først, eller av global tilstand som ligger igjen etter en tidligere test. Uavhengige tester kan kjøre i hvilken som helst rekkefølge og fortsatt gi riktige resultater.

**Navngi tester som setninger.** `"division by zero throws an exception"` er langt mer nyttig enn `"test3"` når en test feiler klokka to om natta før en frist.

---

## Test oppførsel, ikke implementasjon {#test-behaviour-not-implementation}

En test bør spikre fast *hva* koden din gjør — dens observerbare oppførsel gjennom det offentlige grensesnittet — ikke *hvordan* den gjør det innvendig. Test at `divide(10, 2)` returnerer `5`; ikke prøv å sjekke hvilken privat variabel den rørte underveis.

Grunnen er at **oppførselen er løftet; innmaten står fritt til å endres.** En test skrevet mot oppførsel overlever en omskriving — du kan bytte ut innsiden fullstendig, og så lenge resultatet er uendret, består testen fortsatt og beskytter deg fortsatt. En test sveiset fast i innmaten ryker hver gang du rydder i koden, og en testsuite som feiler på harmløse refaktoreringer, er en folk i det stille slutter å stole på.

---

## Hva med private funksjoner? {#what-about-private-functions}

Dette er spørsmålet som dukker opp oftest: *hvordan tester jeg en privat medlemsfunksjon?* Du kan ikke kalle den fra en test — det er det `private` betyr — og instinktet er å gjøre den offentlig, eller å nå inn med et triks. Stå imot. De ærlige svarene, i prioritert rekkefølge:

1. **Test den gjennom de offentlige funksjonene som bruker den.** En privat hjelpefunksjon finnes for å tjene det offentlige grensesnittet; tren det grensesnittet grundig, og den private koden kjører som en del av det.
2. **Hvis noe privat er komplekst nok til å fortjene egne tester, er det et signal — trekk det ut i sin egen enhet.** Løft logikken ut i en frittstående funksjon (eller en liten egen klasse). Nå er den offentlig, ren og trivielt testbar, og den opprinnelige klassen er enklere også:

```cpp
// Før: en vrien beregning gjemt i en privat metode — vanskelig å teste
class Thermostat {
public:
    void update(int raw) { latest_ = toCelsius(raw); }
private:
    double toCelsius(int raw) const { return (raw * 5.0 / 1023.0 - 0.5) * 100.0; }
    double latest_ = 0.0;
};

// Etter: beregningen er en frittstående funksjon — offentlig, ren, lett å teste
double rawToCelsius(int raw) {
    return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
}

class Thermostat {
public:
    void update(int raw) { latest_ = rawToCelsius(raw); }
private:
    double latest_ = 0.0;
};
```

En test for `rawToCelsius` sender bare inn et tall og sjekker resultatet — ingen objekter, ingen skjult tilstand. Trangen til å teste noe privat er vanligvis koden som forteller deg at en bit av den vil være sin egen enhet.

Du kan ha sett triks for å nå inn i en klasses private medlemmer — en `friend`-deklarasjon, eller `#define private public` før `#include`-en. De kompilerer, men de bolter testene dine fast i akkurat den innmaten du prøver å holde fri til å endres, så en refaktorering som bevarer oppførselen, kan fortsatt knekke dem. Foretrekk de to alternativene ovenfor.

---

## Testbar kode er godt designet kode {#testable-code-is-well-designed-code}

Her er delen som overrasker folk: det vanskeligste med testing er vanligvis ikke å skrive testen — det er *koden*. Når en funksjon er smertefull å teste, er den vanskeligheten informasjon om **designet**, ikke om testen. De vanlige årsakene:

- **Den gjør for mange ting på én gang** — lav **kohesjon**. En funksjon som leser en sensor, konverterer enheter *og* skriver en fil, tvinger deg til å sette opp alle tre før du kan sjekke én av dem. Del den opp.
- **Den strekker seg ut mot maskinvare, filer, klokka eller nettverket** — tett **kobling**, med skjulte inndata. Løsningen er **dependency injection**: ta imot de avhengighetene (som parametere, eller bak et grensesnitt) i stedet for å opprette dem innvendig, slik at en test kan sende inn en fake — verdt å se i sin helhet, straks.
- **Den avhenger av [global tilstand](../Chapter1/functions.md#global-variables).** En global variabel er en usynlig inndata og en delt utdata: tester av kode som rører en, forstyrrer hverandre og blir skjøre.

Kode som er lett å teste, er nesten alltid liten, fokusert og løst koblet — nøyaktig de egenskapene kapittelet om separasjon av ansvar argumenterer for på selvstendig grunnlag. Så tester er ikke bare et sikkerhetsnett for å fange bugs; **å skrive dem tidlig er et designverktøy.** Når noe stritter imot testing, behandle det som en alarm og fiks *designet*, ikke testen. Å få testene riktige og å få strukturen riktig viser seg å være samme jobb.

---

## Å injisere en fake {#injecting-a-fake}

Ta en `FrostAlarm` som avgjør om det er frost. Hvis den selv strakte seg ut og leste et ekte termometer, ville den vært sveiset fast i maskinvare — utestbar uten et kjølerom. Så i stedet avhenger den av et lite grensesnitt, og den som oppretter den, leverer termometeret:

```cpp
class Thermometer {
public:
    virtual ~Thermometer() = default;
    virtual double celsius() = 0;
};

class FrostAlarm {
public:
    explicit FrostAlarm(Thermometer& thermometer) : thermometer_(thermometer) {}

    bool triggered() { return thermometer_.celsius() < 0.0; }

private:
    Thermometer& thermometer_;
};
```

I det virkelige programmet gir du `FrostAlarm` et termometer som leser en pinne. I en test gir du den en **fake** — en som returnerer akkurat den verdien testen trenger, uten maskinvare i sikte:

```cpp
class FakeThermometer : public Thermometer {
public:
    explicit FakeThermometer(double value) : value_(value) {}
    double celsius() override { return value_; }
private:
    double value_;
};

TEST_CASE("the alarm fires below freezing") {
    FakeThermometer cold(-5.0);
    FrostAlarm alarm(cold);
    REQUIRE(alarm.triggered());
}

TEST_CASE("the alarm stays quiet above freezing") {
    FakeThermometer warm(5.0);
    FrostAlarm alarm(warm);
    REQUIRE(!alarm.triggered());
}
```

Fordi `FrostAlarm` *får* termometeret sitt i stedet for å bygge et selv, kan testen smette inn et `FakeThermometer` og drive det til hvilken som helst temperatur — så vidt under frysepunktet, så vidt over — umiddelbart og repeterbart. Det gi-det-inn-grepet er **dependency injection** (den samme teknikken [separasjon av ansvar](soc.md) bruker for å holde `monitorLoop` uavhengig av én bestemt sensor), og det er det som i det hele tatt gjør maskinvarenær kode testbar. En fake som bare returnerer forhåndsbestemte verdier som dette, er den enkleste typen *test double*; du vil høre "stub" og "mock" om rikere varianter, men en enkel fake dekker det meste av det du trenger i starten.
