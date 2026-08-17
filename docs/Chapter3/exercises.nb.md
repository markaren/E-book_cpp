# Oppgaver til kapittel 3

Arbeid deg gjennom disse etter å ha lest kapittel 3. **Prøv hver enkelt selv før du avslører løsningen** — du lærer langt mer av et ærlig forsøk enn av å lese et ferdig svar. Skriv koden inn i CLion og kjør den; ikke bare les den.

Når du åpner en løsning vises den **uskarp** — klikk én gang til for å avsløre den, slik at du ikke ser svaret ved et uhell.

Hver oppgave er et lite program med sin egen `main()`. Nå som du har lest [CMake](../Chapter2/cmake_intro.md), kan du holde dem i ett prosjekt — én `add_executable`-linje per fil — og velge hvilket som skal kjøres fra rullegardinmenyen ved siden av den grønne ▶-knappen.

---

## 1. Sensorstatistikk {#1-sensor-statistics}

*Øver på: [Standardbiblioteket i C++](standard_library.md)*

Legg disse avlesningene i en `std::vector<int>`: `17, 42, 99, 8, 23`. Bruk deretter **algoritmer fra standardbiblioteket**, ikke håndskrevne løkker, til å skrive ut tre ting: avlesningene **sortert** stigende, **summen** deres og den **største** verdien.

> Hint: foretrekk C++20s `std::ranges::`-former — `std::ranges::sort(v)` og `std::ranges::max_element(v)` tar beholderen direkte. `<numeric>` har `std::accumulate`, som ikke har noen ranges-form i C++20, så den tar fortsatt et `.begin(), .end()`-område.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>
    #include <numeric>

    int main() {
        std::vector<int> readings = {17, 42, 99, 8, 23};

        std::ranges::sort(readings);

        int sum = std::accumulate(readings.begin(), readings.end(), 0);
        int largest = *std::ranges::max_element(readings);

        std::cout << "Sorted:";
        for (int r : readings) {
            std::cout << " " << r;
        }
        std::cout << "\n";

        std::cout << "Sum: " << sum << "\n";
        std::cout << "Largest: " << largest << "\n";
    }
    ```

    `std::ranges::`-versjonene tar beholderen direkte — kortere, og du kan ikke ved et uhell blande en `begin()` fra én beholder med en `end()` fra en annen. `std::ranges::max_element` returnerer en *iterator* til det største elementet, så `*`-en foran leser verdien den peker på. `std::accumulate` beholder den klassiske `.begin(), .end()`-formen fordi C++20 ikke gir den noen ranges-versjon (den range-baserte foldingen kom først i C++23). Å la biblioteket sortere og summere for deg er kortere og vanskeligere å gjøre feil enn å skrive løkkene for hånd — kapittelets hovedpoeng.

    </div>

---

## 2. Tell fargene {#2-count-the-colours}

*Øver på: [Datastrukturer](data_structures.md)*

Du får en liste med fargenavn, noen gjentatt — `{"red", "green", "red", "blue", "green", "red"}`. Tell hvor mange ganger hver farge forekommer, og skriv så ut hver farge med antallet sitt. Bruk beholderen kapittelet anbefaler for telling per nøkkel.

> Hint: å slå opp en nøkkel som mangler i en map oppretter den med verdien `0`, så `++counts[colour]` gjør det rette også første gang.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>
    #include <vector>
    #include <map>

    int main() {
        std::vector<std::string> colours = {"red", "green", "red", "blue", "green", "red"};

        std::map<std::string, int> counts;
        for (const std::string& colour : colours) {
            ++counts[colour];
        }

        for (const auto& [colour, count] : counts) {
            std::cout << colour << ": " << count << "\n";
        }
    }
    ```

    `++counts[colour]` virker fordi det første oppslaget av en ny nøkkel setter den inn med en verdi-initialisert `0`, som `++` deretter gjør til `1`. Med `std::map` skrives fargene ut i alfabetisk rekkefølge; `std::unordered_map` ville telt dem like godt, men i ingen bestemt rekkefølge. `[colour, count]` i løkken er en *strukturert binding* — den deler hvert nøkkel/verdi-par i to navngitte biter, akkurat som kapittelet viste.

    </div>

---

## 3. Tell de distinkte ID-ene {#3-count-the-distinct-ids}

*Øver på: [Datastrukturer](data_structures.md)*

En strøm av sensor-ID-er kommer inn, med noen gjentakelser — `{4, 8, 4, 15, 16, 8, 23, 42, 16}`. Skriv ut hvor mange **distinkte** ID-er det var. Bruk beholderen som er laget for spørsmålet "har jeg sett denne før?".

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <vector>
    #include <unordered_set>

    int main() {
        std::vector<int> ids = {4, 8, 4, 15, 16, 8, 23, 42, 16};

        std::unordered_set<int> distinct;
        for (int id : ids) {
            distinct.insert(id);      // en gjentakelse ignoreres stille
        }

        std::cout << "Distinct IDs: " << distinct.size() << "\n";
    }
    ```

    En mengde forkaster duplikater stille, så når hver ID har gått inn, *er* dens `size()` antallet distinkte verdier. Kapittelets beslutningstabell peker på en `set` for nettopp denne "holde styr på hvilke elementer jeg har sett"-jobben.

    **Kortere alternativ:** en mengde kan bygges rett fra et område med verdier, så `std::unordered_set<int> distinct(ids.begin(), ids.end());` gjør hele løkken på én linje. Begge gir samme svar.

    </div>

---

## 4. Del opp en `name:value`-innstilling {#4-split-a-namevalue-setting}

*Øver på: [Strenger](../strings.md)*

Konfigurasjonslinjer ser ofte slik ut: `"speed:120"` — et navn, et kolon, så en verdi. Gitt strengen `"speed:120"`, del den ved kolonet og skriv ut navnet og verdien på hver sin linje. Konverter deretter verdien til en `int` og skriv ut det dobbelte av den.

Forventet utskrift:

```
name  = speed
value = 120
doubled = 240
```

> Hint: `find(':')` gir deg indeksen til kolonet; `substr` tar delen før og delen etter. `std::stoi` gjør verditeksten om til en `int`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>

    int main() {
        std::string line = "speed:120";

        std::size_t colon = line.find(':');
        std::string name  = line.substr(0, colon);   // før kolonet
        std::string value = line.substr(colon + 1);  // etter kolonet

        std::cout << "name  = " << name << "\n";
        std::cout << "value = " << value << "\n";

        int n = std::stoi(value);
        std::cout << "doubled = " << n * 2 << "\n";
    }
    ```

    `find(':')` returnerer indeksen til kolonet; `substr(0, colon)` tar de `colon` tegnene før det, og `substr(colon + 1)` tar alt fra rett etter det og til slutten. `std::stoi` gjør deretter `"120"` om til tallet `120`. (En robust tolker ville først sjekket at `find` ikke returnerte `std::string::npos` — her vet vi at kolonet er der.)

    </div>

---

## 5. Tell avlesningene over en terskel {#5-count-the-readings-above-a-threshold}

*Øver på: [Lambda-uttrykk](../lambdas.md)*

Du har disse sensoravlesningene i en `std::vector<double>`: `{22.5, 19.0, 31.2, 18.7, 25.0, 40.1}`. Bruk `std::ranges::count_if` med et **lambda-uttrykk** til å telle hvor mange som er over `24.0`, og skriv ut antallet.

Forventet utskrift:

```
Above threshold: 3
```

> Hint: `std::ranges::count_if(v, predicate)` teller elementene som `predicate` returnerer `true` for. Predikatet er et lambda-uttrykk som tar én `double` og returnerer en `bool`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main() {
        std::vector<double> readings = {22.5, 19.0, 31.2, 18.7, 25.0, 40.1};
        const double threshold = 24.0;

        int above = std::ranges::count_if(readings,
                        [threshold](double r) { return r > threshold; });

        std::cout << "Above threshold: " << above << "\n";
    }
    ```

    Lambda-uttrykket `[threshold](double r) { return r > threshold; }` er testen som anvendes på hver avlesning; `std::ranges::count_if` kjører den over hele vektoren og returnerer hvor mange ganger den var `true`. Å fange `threshold` som verdi lar lambdaen bruke den uten at den må være global. Tre avlesninger — `31.2`, `25.0` og `40.1` — er over `24.0`.

    </div>
