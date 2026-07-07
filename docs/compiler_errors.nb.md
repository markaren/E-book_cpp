# Lese kompilatorfeil

Den raskeste måten å bli bedre i C++ på er å lære å lese feilmeldinger. Nybegynnere stivner foran veggen av rød tekst; erfarne programmerere skummer gjennom den, finner linjen og fikser problemet på sekunder. Forskjellen er ikke intelligens; det er å vite hva man skal se etter.

Denne siden er en veiledning i å lese typisk C++-kompilatorutskrift, de vanligste feilene du kommer til å treffe på, og hva du skal gjøre med hver av dem.

---

## Anatomien til en feilmelding

En typisk kompilatorfeil har denne formen:

```
main.cpp:14:18: error: expected ';' after expression
    std::cout << "Hello"
                ^
                ;
```

Tre deler du alltid vil finne:

| Del | Hva den forteller deg |
|------|-------------------|
| `main.cpp:14:18` | Filen, linjenummeret og kolonnen der kompilatoren ble forvirret |
| `error: expected ';'...` | Hva kompilatoren mener er galt |
| `^`-linjen (caret) | En visuell peker til stedet i kildekoden |

**Start alltid med fil:linje.** Åpne den filen, hopp til den linjen, og les koden rundt.

---

## Lese utskrift med flere feil

Én enkelt feil gir ofte flere feilmeldinger, fordi når kompilatoren først er forvirret, holder den seg forvirret en stund. **Fiks alltid den første feilen først**, og bygg på nytt. Mange av de senere feilene forsvinner av seg selv.

For eksempel: glemmer du `#include <vector>` i et program som bruker `std::vector`, melder GCC tre feil fra den ene forglemmelsen:

```
main.cpp: In function 'int main()':
main.cpp:4:10: error: 'vector' is not a member of 'std'
    4 |     std::vector<int> readings = {10, 20, 30};
      |          ^~~~~~
main.cpp:4:10: note: 'std::vector' is defined in header '<vector>';
                     did you forget to '#include <vector>'?
main.cpp:4:17: error: expected primary-expression before 'int'
    4 |     std::vector<int> readings = {10, 20, 30};
      |                 ^~~
main.cpp:5:5: error: 'readings' was not declared in this scope
    5 |     readings.push_back(40);
      |     ^~~~~~~~
```

Tre feil, én tabbe: den manglende headeren gjør at `std::vector` er ukjent, så `readings` blir aldri deklarert, så linjen som *bruker* `readings` feiler også. Fiks den første feilen — legg til `#include <vector>` — og bygg på nytt; de to andre forsvinner med den. (Legg merke til at `note:`-linjen til og med forteller deg hvilken header du skal legge til — kompilatoren er ofte mer hjelpsom enn veggen av rødt lar det virke.)

---

## De vanlige feilene og hva de egentlig betyr

### `expected ';' after ...`

Du glemte et semikolon. Feilen peker som regel på linjen *etter* den manglende, fordi kompilatoren ikke skjønte at den forrige setningen var slutt før den så noe som ikke kunne være en fortsettelse.

```cpp
std::cout << "Hello"        // missing semicolon here
std::cout << "World";       // error reported here
```

### `use of undeclared identifier 'foo'`

Du brukte et navn kompilatoren ikke kjenner til. Tre vanlige årsaker:

1. **Skrivefeil.** `std:cout` i stedet for `std::cout`. `cout` i stedet for `std::cout`.
2. **Manglende `#include`.** Du brukte `std::vector` men `#include`-et ikke `<vector>`.
3. **Variabel deklarert i et annet virkeområde.** Du deklarerte `x` inni en indre blokk og prøvde å bruke den utenfor.

### `no matching function for call to 'foo(...)'`

Du kalte en funksjon, men argumentene passer ikke til noen versjon av den. Kompilatoren lister vanligvis kandidatene den vurderte:

```
error: no matching function for call to 'add(int, std::string)'
note: candidate function not viable: no known conversion
      from 'std::string' to 'int' for 2nd argument
      int add(int a, int b);
```

Løsningen ligger i `note: candidate ...`-linjen: les den for hva kompilatoren *forventet* og sammenlign med det du sendte inn.

### `expected '}' at end of input`

En `{` et sted har ikke en tilhørende `}`. Linjenummeret er ofte helt på slutten av filen, noe som ikke er særlig nyttig. Gå tilbake gjennom filen og let etter en åpningsparentes uten en lukkende. Editorens parentesmatching er vennen din.

### `redefinition of '...'`

Du definerte det samme to ganger *innenfor én fil*, så **kompilatoren** avviser det. Den vanligste årsaken er en header, uten `#pragma once` eller en header guard, som limes inn i samme fil to ganger (ofte fordi én header `#include`-er en annen som du også inkluderer direkte). Legg til `#pragma once` i headeren. (Å definere det samme på tvers av *forskjellige* filer er en annen feil, på linker-trinnet — se [`multiple definition of ...`](#linker-errors-undefined-reference-to-and-multiple-definition-of) nedenfor.)

### `'X' was not declared in this scope`

Det samme som "use of undeclared identifier", en annen kompilators formulering av det samme problemet.

### `cannot convert 'X' to 'Y'`

Typemismatch. Du tilordnet, returnerte eller sendte noe av én type der en annen forventes. Les typene nøye:

```
error: cannot convert 'std::string' to 'int' in assignment
```

Du prøvde å legge en string inn i en int-variabel. Sjekk typene på begge sider.

### `member access into incomplete type 'X'`

Du brukte `someObject.field` eller `somePtr->field` på en type som bare har blitt forhåndsdeklarert (forward-declared), ikke fullt definert. Enten inkluder headeren som definerer typen, eller flytt tilgangen til et sted der den fulle typen er synlig.

### `expression is not assignable`

Du prøvde å skrive til noe som ikke kan skrives til: en `const`-variabel, resultatet av et funksjonskall, eller en midlertidig verdi.

```cpp
const int x = 5;
x = 10;                     // expression is not assignable

if (x = 5) { }              // also a warning, see below
```

### Linkerfeil: `undefined reference to ...` og `multiple definition of ...` {#linker-errors-undefined-reference-to-and-multiple-definition-of}

Forskjellig fra kompileringsfeil: disse kommer fra **linkeren**, neste trinn i byggingen. Kompilatoren godtok hver fil for seg, men da det ble tid for å sette sammen det endelige programmet, passet ikke bitene sammen — enten mangler noe, eller så er noe definert for mange ganger.

**`undefined reference to ...`** — linkeren finner ikke implementasjonen av noe du bruker:

```
undefined reference to `Motor::start()'
```

Vanlige årsaker:

1. **Du deklarerte en funksjon, men definerte den aldri** (deklarasjon i en header, ingen implementasjon i noen `.cpp`).
2. **`.cpp`-filen som inneholder implementasjonen er ikke med i `CMakeLists.txt`.**
3. **Du glemte å linke mot et bibliotek** (`target_link_libraries` mangler).

**`multiple definition of ...`** — det motsatte problemet: det samme er definert i mer enn én `.cpp`, så linkeren ser to kopier og kan ikke velge:

```
multiple definition of `add(int, int)'; first defined here
```

Vanlige årsaker:

1. **To `.cpp`-filer implementerer den samme funksjonen.**
2. **En funksjon er *definert* i en header uten å være merket `inline`** — hver `.cpp` som inkluderer headeren får sin egen kopi. Enten merk funksjonen `inline`, eller flytt definisjonen inn i én enkelt `.cpp` og la bare deklarasjonen stå i headeren.

Linkerfeil inneholder *ikke* linjenummer i kildekoden din; de viser til symboler.

---

## Advarsler

Advarsler er ikke feil; byggingen lykkes. Men advarsler indikerer nesten alltid en ekte feil eller en kodelukt:

```
warning: control reaches end of non-void function
warning: comparison of integer expressions of different signedness
warning: '=' used in a context where '==' was probably intended
```

**Behandle advarsler som feil.** De fleste kompilatorer godtar et flagg (`-Wall -Wextra -Werror` for GCC og Clang) som forfremmer dem — se [hvordan du slår dem på](Chapter2/cmake_intro.md#turn-on-compiler-warnings). Når koden din kompilerer uten advarsler, fanger du opp en klasse feil som ellers ville overlevd helt til kjøretid.

---

## Når meldingen fortsatt ikke gir mening

Fire strategier, i denne rekkefølgen:

**1. Les linjen over den feilen peker på.** Mange feil (særlig feil om manglende semikolon) er egentlig én linje tidligere enn der kompilatoren klager.

**2. Kommenter ut den problematiske linjen og bygg på nytt.** Hvis resten av filen så kompilerer rent, har du snevret inn problemet.

**3. Søk etter den *eksakte* feilteksten.** Kopier den mest spesifikke delen, vanligvis fra `error:`, og lim den inn i en søkemotor. De fleste feilmeldinger har blitt spurt om på Stack Overflow flere ganger.

**4. Be en KI om å oversette meldingen.** Å lime inn *hele* kompilatorutskriften sammen med den problematiske koden i en KI-assistent er et av dens beste bruksområder. Se [Bruke KI til koding](using_ai.md) for vanene som hindrer at dette blir til "KI-en gjør jobben min".

Malfeil er et spesialtilfelle: de kan være hundrevis av linjer lange for én enkelt skrivefeil. Trikset er å lese ovenfra og ned og se etter linjen `note: candidate template ignored: ...`, som sier *hvorfor* en mal ikke kunne brukes. Den merknaden inneholder som regel det egentlige problemet på rent norsk.

---

## Et gjennomarbeidet eksempel

Du kompilerer dette:

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int x = 5
    std::cout << x << "\n";
    return 0;
}
```

Og GCC melder:

```
main.cpp: In function 'int main()':
main.cpp:5:5: error: expected ',' or ';' before 'std'
    5 |     std::cout << x << "\n";
      |     ^~~
```

Én feil — og den peker på **linje 5**, `std::cout`-linjen, selv om den egentlige tabben er på **linje 4**: `int x = 5` mangler semikolon. Dette er den klassiske fella med manglende semikolon. Kompilatoren leste `int x = 5` og fortsatte, i forventning om at setningen skulle fortsette; først da den traff `std` på neste linje skjønte den at noe var galt — så det er *den* linjen den skylder på. **Sjekk alltid linjen over den feilen peker på.** Legg til semikolonet etter `5`, kompiler på nytt, og feilen forsvinner.

Når du har gjort dette fem eller seks ganger, begynner du å fikse manglende semikolon før kompilatoren engang er ferdig med å klage på dem.

---

Kompilatorfeil handler om kode som ikke vil *bygge*. Når den bygger, men gjør feil ting når du kjører den, er verktøyet du vil ha [debuggeren](debugger.md).
