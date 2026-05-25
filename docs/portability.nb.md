# Portabilitet

C++ er definert av en internasjonal standard, så *i prinsippet* bygger og kjører den samme kildekoden likt på ethvert system. **I praksis ikke helt** — og gapet overrasker nybegynnere, fordi det dukker opp selv i små programmer som bare bruker standardbiblioteket.

Denne siden handler om **desktop**-C++ på tvers av **Windows, Linux og macOS**, og de tre kompilatorene du sannsynligvis møter: **GCC**, **Clang** og Microsofts **MSVC**. (På Windows bruker CLion GCC som standard.) For det helt andre tilfellet med en mikrokontroller — samme språk i et bittelite miljø — se [Arduino vs. desktop-C++](arduino_vs_desktop.md).

> **Hvorfor dette angår deg.** Du skriver kode på Windows i CLion; en medstudent bygger det samme prosjektet på en Mac, og foreleseren din bygger det på Linux. "Det bygde på min maskin" er ikke det samme som "det bygger". Å oppdage forskjellen kvelden før en innleveringsfrist er lite morsomt — litt bevissthet nå forhindrer det.

---

## Et kompilert program er ikke portabelt

Husk fra [Introduksjonen](Chapter1/introduction.md) at C++ er *kompilert*: kompilatoren gjør kildekoden din om til **maskinkode** — rå instruksjoner for én bestemt type prosessor, pakket inn i et filformat som ett bestemt operativsystem vet hvordan det skal laste.

Det har en direkte konsekvens: **den kjørbare fila du bygger, er bundet til ett OS og én CPU.**

- En Windows-`.exe` kjører ikke på Linux eller macOS, og omvendt — hvert system bruker et eget filformat for programmer.
- Et program bygget for en 64-bits Intel/AMD-brikke kjører ikke på en ARM-brikke (som Apple Silicon eller en Raspberry Pi) uten å bli bygget på nytt.

For å kjøre programmet ditt på en annen plattform, **kompilerer du det på nytt der**. Dette er normalt og som regel smertefritt — [CMake](Chapter2/cmake_intro.md) finnes nettopp for at du skal kunne beskrive byggingen én gang og kjøre den på en hvilken som helst plattform. Men vær klar over hva CMake gjør: det gjør *byggingen* portabel, ikke det *bygde programmet*. Selve `.exe`-fila blir aldri portabel; du bygger ganske enkelt på nytt på hvert system.

> Dette er prisen for å kompilere til maskinkode. Språk som Python og Java omgår det ved å distribuere kildekoden (eller en portabel bytekode) og kjøre den gjennom en tolk eller en virtuell maskin som er installert på hver plattform. Du bytter ut omkompileringen mot å trenge den kjøretiden til stede — og mot den lavere hastigheten som følger med.

---

## Den samme kildekoden kompilerer kanskje ikke engang

Her er delen som overrasker folk. Du skulle forvente at kode som bruker **bare standardbiblioteket** — ingen Windows-spesifikke kall, ikke noe eksotisk — ville kompilere overalt. Ofte gjør den det. Men ikke alltid, og her er hvorfor.

### Du glemte en `#include` (og slapp unna med det)

En standardheader har lov til å inkludere *andre* standardheadere, og nøyaktig hvilke den drar inn **varierer mellom kompilatorer**. Så dette kan kompilere på Windows, men feile på Linux:

```cpp
#include <vector>          // bare denne — ingen <algorithm>

int main() {
    std::vector<int> v{3, 1, 2};
    std::sort(v.begin(), v.end());   // std::sort hører egentlig hjemme i <algorithm>
}
```

På MSVC drar `<vector>` tilfeldigvis inn `<algorithm>`, så `std::sort` er synlig og det bygger. På Linux med GCC gjør den ikke det, og du får `'sort' is not a member of 'std'` — som peker på en linje du aldri trodde var feil. **Løsningen er en regel, ikke en omvei: inkluder en header for hver standardfasilitet du bruker.** Her: legg til `#include <algorithm>`. ("Inkluder det du bruker.")

### C++20 er ikke ferdig overalt samtidig

En ny standard som **C++20** er et langt dokument, og kompilatorer implementerer den bit for bit over flere år. En funksjon kan være klar i én kompilator og mangle i en annen:

```cpp
#include <format>
#include <iostream>

int main() {
    std::cout << std::format("{} + {} = {}\n", 2, 2, 4);
}
```

`std::format` kom i MSVC og i nyere GCC, men **eldre** versjoner av GCC og Clang har ingen `<format>` i det hele tatt — den samme standardbibliotekskoden vil rett og slett ikke kompilere der. Når du tar i bruk en helt ny funksjon, sjekk at hver kompilator du sikter mot er ny nok til å ha den.

### To som biter i praksis: `or` og `M_PI`

Kompilatorer er også uenige om hva som i det hele tatt er gyldig — og forskjellen er ikke alltid "strengere", den kan rett og slett være *annerledes*. To tilfeller dukker opp hele tiden.

**Ord-operatorer (`or`, `and`, `not`).** C++ lar deg skrive `||`, `&&` og `!` som ordene `or`, `and` og `not`. Det er standard nøkkelord, og GCC og Clang godtar dem som de er:

```cpp
if (ready or retry) { /* ... */ }     // identisk med: ready || retry
```

Men **MSVC, i standardmodusen sin, gjør det ikke** — den melder `'or': undeclared identifier`. (Den gjenkjenner ordformene bare i konformansmodus, eller hvis du inkluderer `<ciso646>`.) Så en linje som bygde på en medstudents Mac, kan feile i et standard Visual Studio-prosjekt. Den robuste løsningen er den enkleste: **bruk symbolene** `||`, `&&`, `!`. De kompilerer på alle kompilatorer, og det er dem denne boken bruker gjennomgående.

**`M_PI` for π.** Strekker du deg etter π, finner du `M_PI` i utallige eksempler:

```cpp
#include <cmath>
double area = M_PI * r * r;     // bygger på GCC/Clang ...
```

Dette kompilerer på Linux og macOS — men `M_PI` er **ikke en del av standard-C++** (det er en gammel POSIX-utvidelse). På MSVC er den udefinert med mindre du skriver `#define _USE_MATH_DEFINES` *før* `#include <cmath>`, så nøyaktig samme kode feiler å kompilere på Windows. I C++20 er det portable svaret å droppe `M_PI` og bruke den standardiserte konstanten:

```cpp
#include <numbers>
double area = std::numbers::pi * r * r;     // standard, fungerer overalt
```

Mønsteret bak begge: **kode som kompilerte på din maskin, er ikke automatisk standard, og heller ikke tilgjengelig på neste kompilator.** Når en universell form finnes — operatorsymbolene, `std::numbers::pi` — foretrekk den.

### Filnavn: `Motor.hpp` er ikke `motor.hpp` på Linux

Filsystemer på Windows og macOS er normalt **ufølsomme for store/små bokstaver**: `Motor.hpp` og `motor.hpp` er samme fil. De fleste Linux-filsystemer er **følsomme for store/små bokstaver**: de er to forskjellige filer. Så:

```cpp
#include "Motor.hpp"   // fila på disken heter egentlig motor.hpp
```

bygger på Windows og macOS, men feiler så på Linux med `No such file or directory`. **Match store/små bokstaver nøyaktig** i hver `#include` og hvert filnavn.

### Ikke anta hvor stor en type er

Standarden fastsetter overraskende lite om heltallsstørrelser. Den som biter i praksis, er `long`:

| Type | Windows (MSVC) | Linux / macOS |
|------|----------------|---------------|
| `int` | 32-bit | 32-bit |
| `long` | **32-bit** | **64-bit** |
| `long long` | 64-bit | 64-bit |

Kode som antar at `long` rommer en 64-bits verdi, er feil på Windows; kode som antar at `long` er like stor som `int`, er feil på Linux. Når den nøyaktige bredden betyr noe, bruk **fastbreddetypene** fra `<cstdint>` — `std::int32_t`, `std::int64_t`, `std::uint8_t` — som betyr det samme overalt. (Du møtte den samme ideen på [Arduino](arduino_vs_desktop.md), der `int` bare er 16 bits; resonnementet er identisk.)

> Fellene på kildekodenivå og hvordan du fikser dem, i korthet:
>
> | Felle | Symptom på den andre maskinen | Løsning |
> |-------|-------------------------------|---------|
> | Å stole på transitive `#include`-er | "`X` is not a member of `std`" | Inkluder en header for alt du bruker |
> | Å bruke en for ny funksjon | "`<format>` not found", manglende navn | Sjekk at hver målkompilator støtter den |
> | Kompilatorspesifikk skrivemåte eller makro (`or`, `M_PI`) | `'or'` / `'M_PI'` udefinert på en annen kompilator | Bruk symboloperatorer, ikke ordformer; og `std::numbers::pi`, ikke `M_PI` |
> | Feil bokstavstørrelse i filnavn | "No such file or directory" på Linux | Match store/små bokstaver nøyaktig i `#include`-er |
> | Å anta typestørrelser | Feil resultater eller overflyt | Bruk fastbreddetyper fra `<cstdint>` |

---

## Hastighet, størrelse og oppførsel kan også variere

Selv når den samme kildekoden *faktisk* kompilerer overalt, er ikke programmet du får, identisk.

**Hastighet og størrelse.** Maskinkoden produseres av *den* kompilatorens optimaliserer, og GCC, Clang og MSVC optimaliserer forskjellig — én kan lage et raskere eller mindre program enn en annen fra samme kildekode. Selve standardbiblioteket er en *forskjellig implementasjon* på hver plattform (Microsofts, GNUs `libstdc++`, LLVMs `libc++`), og disse er forskjellige i ytelse: et `std::regex`-søk eller et `std::unordered_map`-oppslag kan være merkbart raskere under én enn under en annen. Og en [Release-bygging er langt raskere enn en Debug-bygging](Chapter2/cmake_intro.md#build-configurations-debug-and-release) av nøyaktig samme kode. "Hvor raskt er dette programmet?" har ikke ett svar — det avhenger av kompilatoren, standardbibliotekimplementasjonen, byggkonfigurasjonen og maskinvaren.

**Oppførsel.** Det meste av velskrevet kode oppfører seg likt overalt. Unntaket er kode som lener seg på ting standarden bevisst lar stå åpent:

- **Udefinert oppførsel** — å lese forbi slutten av et array, å bruke en uinitialisert variabel, fortegnsoverflyt — kan *tilfeldigvis* fungere på én plattform og krasje på en annen. Det er aldri trygt å stole på; denne boken merker det etter hvert som det dukker opp.
- **Flyttall**-resultater kan variere i de siste sifrene mellom kompilatorer og optimaliseringsnivåer. Når det kan ha betydning, les [Flyttall-fallgruver](floating_point.md).

Lærdommen: portabel oppførsel kommer av å skrive *korrekt, standard* C++ — ikke av kode som tilfeldigvis fungerte på den ene maskinen du testet.

---

## Kompileringstider varierer

Hvor *lang* tid byggingen tar, er også plattform- og kompilatoravhengig: det samme prosjektet kan kompilere merkbart raskere eller tregere under GCC, Clang eller MSVC, og på forskjellige maskiner. Dette er ikke et korrekthetsproblem, bare noe å forvente — ikke bli skremt når et prosjekt som bygger på sekunder på ett oppsett, tar lengre tid på et annet. (Det du *kan* påvirke: en ren ombygging er treg, men etterpå rekompilerer CMake bare filene du endret, og tungt [malbasert](Chapter5/templates.md) kode er tregere å kompilere enn vanlig kode.)

---

## Hva du kan gjøre med det

Du trenger ikke at studiearbeidet ditt skal kjøre på fem plattformer. Men noen vaner koster ingenting og holder koden din ærlig:

- **Inkluder det du bruker.** Én `#include` for hver standardfasilitet du nevner. Stol aldri på at én header drar inn en annen.
- **Slå på advarsler** — `-Wall -Wextra` (GCC/Clang) eller `/W4` (MSVC). Se [CMake](Chapter2/cmake_intro.md#turn-on-compiler-warnings). Advarsler er ofte det første tegnet på ikke-portabel kode.
- **Hold deg til standardbiblioteket og CMake.** Unngå kompilatorspesifikke utvidelser og OS-spesifikke headere (som `<windows.h>`) med mindre du virkelig trenger dem — og når du gjør det, isoler dem bak en [CMake-betingelse](Chapter2/cmake_intro.md#treating-compilers-and-platforms-differently).
- **Bruk fastbreddetyper for heltall** (`<cstdint>`) når størrelsen betyr noe; anta aldri hvor stor `long` er.
- **Skriv stier portabelt** — skråstrek forover eller `std::filesystem::path` — og match store/små bokstaver i filnavn nøyaktig. Se [Datamaskingrunnlag](computer_basics.md).
- **Det eneste beviset er å bygge og kjøre det der.** Hvis kode må fungere på en annen plattform, kompiler og test den på den plattformen. (Å automatisere det er én jobb for *kontinuerlig integrasjon*.) Å lese kildekoden er ikke nok — "det funker på min maskin" er en uttalelse om din maskin.

---

## Oppsummering

- En **kompilert kjørbar fil** sikter mot ett OS og én CPU; for å kjøre andre steder **kompilerer du på nytt**. CMake gjør ombygging lett, men gjør ikke binærfila portabel.
- Den **samme kildekoden kan feile å kompilere** på en annen kompilator selv om den bare bruker standardbiblioteket — vanligvis fordi den stoler på transitive `#include`-er, bruker en for ny C++20-funksjon, bruker en kompilatorspesifikk skrivemåte eller makro (`or`, `M_PI`), har feil bokstavstørrelse i filnavn, eller antar typestørrelser.
- **Hastighet, størrelse og til og med oppførsel** kan variere mellom kompilatorer, standardbibliotekimplementasjoner, byggkonfigurasjoner og maskinvare; udefinert oppførsel og flyttall er de vanlige kildene til oppførselsforskjeller.
- **Kompileringstider** varierer med kompilator og maskin — forventet, ikke en feil.
- Billige vaner holder koden portabel: *inkluder det du bruker*, *advarsler på*, *fastbreddetyper*, *portable stier*, og fremfor alt **test på plattformen som må kjøre den.**
