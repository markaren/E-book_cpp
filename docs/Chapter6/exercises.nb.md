# Oppgaver til kapittel 6

Jobb deg gjennom disse etter å ha lest kapittel 6. **Prøv hver enkelt selv før du avslører løsningen** — du lærer langt mer av et ærlig forsøk enn av å lese et ferdig svar. Skriv koden inn i CLion og kjør den; ikke bare les den.

Når du åpner en løsning vises den **uskarp** — klikk én gang til for å avsløre den, slik at du ikke ser svaret ved et uhell.

De fleste av disse er små programmer med sin egen `main()`. Hold dem i ett prosjekt med én `add_executable`-linje per fil (se [CMake](../Chapter2/cmake_intro.md)), og velg hvilket som skal kjøres fra rullegardinmenyen ved siden av den grønne ▶-knappen. Den **siste oppgaven er en test, ikke et program du kjører fra rullegardinmenyen** — bygg den med Catch2-malen fra kapittelet om [Testing](testing.md) (som allerede registrerer kjøreren hos CTest via `include(CTest)` + `add_test`, så `ctest` bare virker) og kjør den med `ctest`.

---

## 1. Én funksjon, tre jobber {#1-one-function-three-jobs}

*Øver på: [Separasjon av ansvar](soc.md)*

Her er en funksjon som gjør tre ting på én gang — den konverterer en rå sensorverdi til °C, avgjør en status og skriver ut resultatet:

```cpp
void report(int raw) {
    double celsius = (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    std::string status;
    if (celsius > 80.0)      status = "CRITICAL";
    else if (celsius > 50.0) status = "WARNING";
    else                     status = "OK";
    std::cout << celsius << " C [" << status << "]\n";
}
```

Skill **beregningen** fra **rapporteringen**. Skriv to *rene* funksjoner — `double toCelsius(int raw)` og `std::string classify(double celsius)` — som beregner og returnerer, uten noen utskrift. Behold utskriften i `main` (eller i én liten rapporteringsfunksjon som kaller de to). I `main`, kjør det på noen få råverdier.

> Hint: en *ren* funksjon beregner bare ut fra argumentene sine og returnerer et resultat — ingen `std::cout`, ingen filer. Utskrift er et eget ansvarsområde; den hører hjemme i `main`, ikke inne i beregningen. Når de først er skilt, kan `toCelsius` og `classify` testes og gjenbrukes hver for seg.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>

    // --- Ansvarsområde 1: konverter en rå avlesning til celsius (ren) ---
    double toCelsius(int raw) {
        return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    }

    // --- Ansvarsområde 2: avgjør en status ut fra en temperatur (ren) ---
    std::string classify(double celsius) {
        if (celsius > 80.0) return "CRITICAL";
        if (celsius > 50.0) return "WARNING";
        return "OK";
    }

    // --- Ansvarsområde 3: rapportering — den eneste delen som rører konsollen ---
    int main() {
        for (int raw : {200, 250, 300}) {
            double celsius = toCelsius(raw);
            std::cout << celsius << " C [" << classify(celsius) << "]\n";
        }
    }
    ```

    Utskrift:

    ```
    47.7517 C [OK]
    72.1896 C [WARNING]
    96.6276 C [CRITICAL]
    ```

    De tre jobbene er nå adskilt. `toCelsius` og `classify` er **rene** — hver tar inndata og returnerer utdata, og rører ingenting annet — så du kan teste dem med en verdi og en sjekk, gjenbruke dem til å sende statusen til en fil eller et nettverk i stedet for konsollen, eller endre tersklene uten å gå i nærheten av utskriften. Den opprinnelige `report` sveiset alle tre sammen: du kunne ikke sjekke klassifiseringen uten også å produsere konsollutskrift. Hver funksjon har nå én jobb (høy **kohesjon**), og I/O-en bor på nøyaktig ett sted.

    </div>

---

## 2. Én avlesning, mange reaksjoner {#2-one-reading-many-reactions}

*Øver på: [Observatør-mønsteret](observer.md)*

Bygg et subjekt som flere observatører følger med på. Skriv en klasse `LevelSensor` som holder et vannivå og lar observatører **abonnere** med en `std::function<void(double)>`-callback. En metode `setLevel(double)` oppdaterer nivået og varsler deretter hver observatør etter tur.

I `main`, abonner to observatører — én som skriver ut nivået, og én som skriver ut en advarsel *bare* når nivået overstiger en grense — og kall så `setLevel` to ganger. Sensoren skal ikke vite noe om noen av observatørene.

> Hint: lagre callbackene i en `std::vector<std::function<void(double)>>`. `subscribe` tar en callback som verdi og `std::move`-r den inn i vektoren; `setLevel` lagrer den nye verdien og løper så gjennom og kaller hver callback. Observatørene er [lambdaer](../lambdas.md). Fang grensen **som verdi** (`[limit]`).

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <functional>
    #include <vector>
    #include <iostream>

    class LevelSensor {
    public:
        // Registrer en callback som kjøres ved hver nye avlesning.
        void subscribe(std::function<void(double)> observer) {
            observers_.push_back(std::move(observer));
        }

        // En fersk avlesning kommer: lagre den, og varsle så alle.
        void setLevel(double metres) {
            level_ = metres;
            for (const auto& observer : observers_) {
                observer(metres);
            }
        }

        double level() const { return level_; }

    private:
        double level_ = 0.0;
        std::vector<std::function<void(double)>> observers_;
    };

    int main() {
        LevelSensor sensor;

        // En visning
        sensor.subscribe([](double m) {
            std::cout << "Display: " << m << " m\n";
        });

        // En advarsel for høyt nivå
        double limit = 5.0;
        sensor.subscribe([limit](double m) {
            if (m > limit) {
                std::cout << "WARNING: above " << limit << " m\n";
            }
        });

        sensor.setLevel(3.0);   // bare visningen
        sensor.setLevel(6.0);   // visningen + advarselen
    }
    ```

    Utskrift:

    ```
    Display: 3 m
    Display: 6 m
    WARNING: above 5 m
    ```

    `LevelSensor` er **subjektet**: det holder en liste med callbacker og kaller dem alle i `setLevel`, uten noen gang å vite hva noen av dem gjør. Hver observatør abonnerer med en lambda. Å legge til en tredje reaksjon — si å logge hvert nivå til en fil — er bare ett `subscribe`-kall til, og sensoren selv endres aldri; den frikoblingen er det mønsteret kjøper deg. Merk at advarselen fanger `limit` **som verdi** (`[limit]`): hvis den fanget som referanse og `limit` ble destruert før `setLevel` kjørte, ville den lagrede callbacken dingle — levetidsfaren kapittelet advarer mot.

    </div>

---

## 3. Avvis det umulige {#3-refuse-the-impossible}

*Øver på: [Feilhåndtering](error_handling.md)*

Modeller et uttak fra en konto. Skriv en funksjon `double withdraw(double balance, double amount)` som:

- **kaster** `std::invalid_argument` hvis `amount` er negativ (en meningsløs forespørsel);
- **kaster** `std::runtime_error` hvis `amount` overstiger `balance` (utilstrekkelige midler);
- ellers **returnerer** den nye saldoen.

I `main`, prøv et gyldig uttak og hver av de ugyldige typene, og skriv ut `e.what()` hver gang et uttak avvises. Fang som `const`-referanse.

> Hint: både `std::invalid_argument` og `std::runtime_error` bor i `<stdexcept>`, og begge arver fra `std::exception` — så én enkelt `catch (const std::exception& e)` håndterer begge, og `e.what()` gir meldingen. En `throw` forlater resten av `try`-blokken og hopper til `catch`-en, så oppdater saldoen bare *etter* et vellykket kall.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <stdexcept>

    double withdraw(double balance, double amount) {
        if (amount < 0.0) {
            throw std::invalid_argument("amount cannot be negative");
        }
        if (amount > balance) {
            throw std::runtime_error("insufficient funds");
        }
        return balance - amount;
    }

    int main() {
        double balance = 100.0;

        for (double amount : {30.0, -5.0, 500.0}) {
            try {
                double after = withdraw(balance, amount);
                std::cout << "Withdrew " << amount << ", balance now " << after << "\n";
                balance = after;                 // bekreft bare ved suksess
            } catch (const std::exception& e) {
                std::cout << "Rejected " << amount << ": " << e.what() << "\n";
            }
        }
    }
    ```

    Utskrift:

    ```
    Withdrew 30, balance now 70
    Rejected -5: amount cannot be negative
    Rejected 500: insufficient funds
    ```

    `withdraw` **oppdager** de to feilmodiene og signaliserer dem ved å kaste; `main` **gjenoppretter** ved å fange — skillet mellom oppdagelse og gjenoppretting som kapittelet åpner med. Når en `throw` fyrer av, forlates resten av `try`-blokken (saldoen oppdateres aldri ved et ugyldig kall) og kontrollen hopper rett til `catch`-en; løkka fortsetter så til neste beløp. Å fange `const std::exception&` som referanse håndterer begge de kastede typene gjennom deres felles basisklasse, uten kopi og uten oppskjæring (slicing). Én skjønnsmessig avveining verdt å merke seg: et negativt eller for stort beløp er en genuin feil kalleren må håndtere, så et unntak passer. Hvis du derimot bare skulle *slå opp noe*, og "ikke funnet" var et helt normalt utfall, ville du grepet etter [`std::optional`](error_handling.md#stdoptional-when-failure-is-expected) i stedet for å kaste.

    </div>

---

## 4. Test det med en fake {#4-test-it-with-a-fake}

*Øver på: [Testing](testing.md)*

Denne er en **test**, ikke et program med en `main()` — bygg den med Catch2-malen fra kapittelet om [Testing](testing.md) og kjør den med `ctest` (eller kjør test-binærfilen direkte — de to er likeverdige). Malens `include(CTest)` + `add_test`-linjer er det som lar `ctest` finne kjøreren din; uten dem rapporterer `ctest` *ingen tester*.

Her er en `PumpController` som skal slå en pumpe **på** når vannivået faller under et minimum. Avgjørende nok leser den ikke maskinvare selv — den *får* en `LevelSensor`, slik at en test kan levere en fake:

```cpp
class LevelSensor {
public:
    virtual ~LevelSensor() = default;
    virtual double level() = 0;        // meter
};

class PumpController {
public:
    PumpController(LevelSensor& sensor, double minLevel)
        : sensor_(sensor), minLevel_(minLevel) {}

    bool pumpShouldRun() { return sensor_.level() < minLevel_; }

private:
    LevelSensor& sensor_;
    double minLevel_;
};
```

Skriv en `FakeLevelSensor` som returnerer et nivå du velger, og skriv så Catch2-`TEST_CASE`-er som beviser at pumpa **kjører under** minimum og **holder seg av på eller over** det. Sørg for å teste grensen — *nøyaktig* på minimum.

> Hint: `FakeLevelSensor` arver fra `LevelSensor` og overstyrer `level()` til å returnere en lagret verdi. Hver `TEST_CASE` lager en fake på et valgt nivå, injiserer den i en `PumpController`, og `REQUIRE`-r den forventede `pumpShouldRun()`. Fordi testen er `level < minLevel`, skal et nivå *likt* minimum **ikke** kjøre pumpa.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <catch2/catch_test_macros.hpp>

    // --- Koden som testes (ville normalt bodd i sin egen header) ---
    class LevelSensor {
    public:
        virtual ~LevelSensor() = default;
        virtual double level() = 0;
    };

    class PumpController {
    public:
        PumpController(LevelSensor& sensor, double minLevel)
            : sensor_(sensor), minLevel_(minLevel) {}
        bool pumpShouldRun() { return sensor_.level() < minLevel_; }
    private:
        LevelSensor& sensor_;
        double minLevel_;
    };

    // --- En fake sensor: returnerer det nivået testen setter, ingen maskinvare ---
    class FakeLevelSensor : public LevelSensor {
    public:
        explicit FakeLevelSensor(double value) : value_(value) {}
        double level() override { return value_; }
    private:
        double value_;
    };

    TEST_CASE("pump runs when the level is below the minimum") {
        FakeLevelSensor low(1.5);
        PumpController pump(low, 2.0);
        REQUIRE(pump.pumpShouldRun());
    }

    TEST_CASE("pump stays off when the level is above the minimum") {
        FakeLevelSensor high(3.0);
        PumpController pump(high, 2.0);
        REQUIRE(!pump.pumpShouldRun());
    }

    TEST_CASE("pump stays off exactly at the minimum") {
        FakeLevelSensor atLimit(2.0);
        PumpController pump(atLimit, 2.0);
        REQUIRE(!pump.pumpShouldRun());   // 2.0 < 2.0 er usant
    }
    ```

    Å kjøre testene skriver ut:

    ```
    All tests passed (3 assertions in 3 test cases)
    ```

    Fordi `PumpController` **får** sensoren sin i stedet for å bygge en selv, smetter testen inn en `FakeLevelSensor` og driver nivået til nøyaktig den verdien hvert tilfelle trenger — uten vann, uten venting, uten maskinvare. Det gi-det-inn-grepet er **avhengighetsinjeksjon**, og faken er den enkleste typen **test double**. De tre tilfellene tester *oppførsel* (kjører pumpa?) gjennom det offentlige grensesnittet, aldri innmaten — så hvis du senere skrev om `pumpShouldRun` fullstendig, ville de fortsatt bestå så lenge oppførselen holdt. Og de undersøker **grensen**, nøyaktig på minimum, fordi off-by-one-feil (`<` kontra `<=`) gjemmer seg akkurat der.

    </div>

---

## 5. Test funksjonene du allerede har separert {#5-test-the-functions-you-already-separated}

*Øver på: [Separasjon av ansvar](soc.md) → [Testing](testing.md)*

Denne bygger videre på oppgave 1. Der trakk du `report` fra hverandre til to **rene** funksjoner — `double toCelsius(int raw)` og `std::string classify(double celsius)`. Hele poenget med å gjøre dem rene var at hver av dem nå kan testes med en verdi og en sjekk. Så gjør nøyaktig det: skriv Catch2-`TEST_CASE`-er for begge.

For `toCelsius`, velg et par råverdier og sjekk resultatet innenfor en toleranse (det er `double`, så sammenlign med `Approx`, ikke `==`). For `classify`, sjekk hvert bånd — en temperatur som er `OK`, en som er `WARNING`, en som er `CRITICAL` — og sørg for å undersøke en **grense**: `classify(80.0)` er `WARNING`, ikke `CRITICAL`, fordi testen er `> 80.0`.

> Hint: dette er den samme Catch2-malen som i oppgave 4 — ingen `main()`, kjør den med `ctest`. Legg `toCelsius`/`classify` i en header testen inkluderer. En ren funksjon er det enkleste som finnes å teste: ingen objekter å bygge, ingen fake å injisere, bare inndata inn og utdata ut. Den lettheten er gevinsten for at du separerte ansvarsområdene i utgangspunktet.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <catch2/catch_test_macros.hpp>
    #include <catch2/catch_approx.hpp>
    #include <string>

    using Catch::Approx;

    // --- De rene funksjonene fra oppgave 1 (ville bodd i sin egen header) ---
    double toCelsius(int raw) {
        return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    }

    std::string classify(double celsius) {
        if (celsius > 80.0) return "CRITICAL";
        if (celsius > 50.0) return "WARNING";
        return "OK";
    }

    TEST_CASE("toCelsius converts a raw reading") {
        // raw 0 → (0 - 0.5) × 100 = -50 ; raw 1023 → (5 - 0.5) × 100 = 450
        REQUIRE(toCelsius(0)    == Approx(-50.0));
        REQUIRE(toCelsius(1023) == Approx(450.0));
        REQUIRE(toCelsius(250)  == Approx(72.1896).epsilon(0.001));
    }

    TEST_CASE("classify names the right band") {
        REQUIRE(classify(20.0)  == "OK");
        REQUIRE(classify(60.0)  == "WARNING");
        REQUIRE(classify(90.0)  == "CRITICAL");
    }

    TEST_CASE("classify handles the band boundaries") {
        REQUIRE(classify(80.0) == "WARNING");    // 80 er ikke > 80, så ikke CRITICAL
        REQUIRE(classify(50.0) == "OK");         // 50 er ikke > 50, så ikke WARNING
    }
    ```

    Å kjøre testene skriver ut:

    ```
    All tests passed (8 assertions in 3 test cases)
    ```

    Ingenting her trengte et `FakeThermometer` eller en `PumpController` — fordi `toCelsius` og `classify` er **rene**, er det å teste dem bare "putt et tall inn, sjekk tallet (eller strengen) ut". Det er belønningen for separasjonen du gjorde i oppgave 1: i det øyeblikket beregningen sluttet å være viklet inn i `std::cout`, ble den trivielt testbar. Grensetilfellene (`80.0`, `50.0`) betyr noe av samme grunn som ved pumpa — `>`-kontra-`>=`-bugs bor nøyaktig på grensen.

    </div>
