# Fra Python

De fleste av dere har skrevet litt Python før dere kom til C++, og det er et reelt forsprang: selve logikken i programmering — variabler, løkker, funksjoner, betingelser — bæres rett over. Det som endrer seg, er alt *under*. Python skjuler maskinen for deg; C++ gir deg kontrollene. Nesten hver eneste forskjell på denne siden følger av det ene faktumet.

Dette er ikke en syntaksordbok. Målet er å justere den **mentale modellen** din og advare deg om *falske venner* — kode som ser ut som Python, men oppfører seg annerledes. (Når et begrep ikke vil feste seg, er [KI-tipset](using_ai.md) "forklar dette i C++ som om jeg har brukt Python" virkelig nyttig.)

---

## Falske venner

Dette er de som lurer Python-programmerere:

| I Python … | … men i C++ |
|------------|-------------|
| `b = a` lar `b` *referere til* det samme objektet | `b = a` gjør `b` til en **full kopi** |
| `10 / 3` er `3.333…` | `10 / 3` er `3` (heltallsdivisjon) |
| en variabel kan skifte type (`x = 5`, så `x = "hi"`) | en variabels **type er fast** ved deklarasjon |
| innrykk definerer blokker | blokker er `{ }`; setninger avsluttes med `;`; innrykk ignoreres |
| `if xs:` er usann for en tom liste | beholdere har ingen sannhetsverdi — skriv `if (xs.empty())` |
| `None` betyr "ingenting" | `nullptr` (en peker til ingenting) eller [`std::optional`](Chapter6/error_handling.md#stdoptional-when-failure-is-expected) (en manglende verdi) |
| `len(xs)` | `xs.size()` |
| `int` vokser uten grense | `int` har fast bredde og **flyter over stille** |
| `print(obj)` skriver alltid ut *noe* (dine egne typer får en standard plassholder) | `std::cout << obj` **vil ikke kompilere** for dine egne typer før du definerer en [`operator<<`](Chapter4/io_streams.md) |

---

## Den store: tilordning kopierer

I Python er navn etiketter klistret på objekter. `b = a` setter en ny etikett på den *samme* lista, så å endre `b` endrer også `a`. I C++ *er* en variabel verdien sin, og `b = a` **kopierer** den:

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = a;   // en full, uavhengig kopi — ikke et alias

    b.push_back(4);           // endrer bare b

    std::cout << "a has " << a.size() << " elements\n";  // 3
    std::cout << "b has " << b.size() << " elements\n";  // 4
}
```

I Python ville det tilsvarende latt *begge* være på lengde 4. Denne **verdisemantikken** er den enkeltstørste omstillingen. Å la to navn referere til det samme objektet er standarden i Python. I C++ ber du om det eksplisitt, med en referanse (`&`) eller en peker. Se [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md).

---

## Typer er faste, og sjekkes før programmet kjører

Du deklarerer en type, og den endrer seg ikke:

```cpp
int count = 0;
count = "three";   // compile error — not a runtime surprise
```

`auto` lar kompilatoren *utlede* typen, men den er fortsatt fast når den er utledet — `auto` er **ikke** Pythons dynamiske typing:

```cpp
auto name = "Ada";   // type is deduced once, then fixed
```

Gevinsten: en hel kategori av Pythons `TypeError` under kjøring blir **kompileringsfeil** du fikser før programmet i det hele tatt kjører. Se [Kompilert, statisk typet](Chapter1/introduction.md) og [Variabler og grunntyper](Chapter1/variables.md).

---

## Tall oppfører seg annerledes

To overraskelser verdt å kjenne fra dag én:

- **Heltallsdivisjon kutter bort resten.** `10 / 3` er `3`, fordi begge operandene er `int`. Gjør den ene til en `double` (`10.0 / 3`) for å få `3.333…`. Pythons `/` er alltid flyttall; dens `//` ligner mest på C++ sin heltallsdivisjon, men de runder negative tall ulikt (Python runder nedover, C++ kutter mot null). Se [Operatorer og uttrykk](Chapter1/operators_expressions.md).
- **Heltall flyter over.** En C++ `int` rommer omtrent ±2 milliarder; Python-heltall vokser uten grense. Gå forbi området, og en C++ `int` ruller stille rundt. For det meste av automasjonsarbeid er `int` helt greit — bare vit at kanten finnes.

---

## Ingenting ryddes opp "senere"

Python frigjør minne når søppelsamleren kommer rundt til det. C++ ødelegger hvert objekt **deterministisk**, i det øyeblikket det går ut av scope — det er [RAII](Chapter4/raii.md), og det er derfor du aldri kaller "free" selv. Baksiden: en referanse eller peker til noe som *allerede* har gått ut av scope, er en klassisk C++-krasj, uten noe motstykke i Python. Se [levetidsfellen](Chapter4/types_refs_ptrs.md#the-big-lifetime-trap).

---

## Løkker, samlinger og "comprehensions"

| Python | C++ |
|--------|-----|
| `for x in xs:` | `for (int x : xs)` — se [Kontrollstrukturer](Chapter1/control_statements.md) |
| `for i in range(n):` | `for (int i = 0; i < n; ++i)` |
| `list` | [`std::vector`](Chapter3/standard_library.md) |
| `dict` | `std::map` / `std::unordered_map` |
| `[f(x) for x in xs]` | `std::transform`, eller en vanlig løkke — se [Lambda-uttrykk](lambdas.md) |

---

## Ikke skriv Python i C++

Målet er ikke å oversette Python linje for linje; det er å skrive *C++*. Noen vaner markerer overgangen:

- **Omfavn kopier og `const`.** Send og returner etter verdi; ty til referanser eller pekere bare når du mener å dele, eller for å unngå å kopiere noe stort.
- **La scope styre levetider** (RAII) i stedet for å strø om deg med pekere for å gjenskape Pythons aliasing.
- **Bruk ekte typer** — [`enum class`](Chapter1/enums.md) og små klasser — i stedet for å sende rundt på strenger og magiske tall.
- **Len deg på kompilatoren.** Skru på advarsler; feilene den melder *før* programmet kjører, gjør arbeid Python bare gjør under kjøring.

---

## Oppsummering

- Python skjuler maskinen; C++ viser den — de fleste forskjeller følger av det.
- `b = a` **kopierer** i C++; aliasing er noe du ber om eksplisitt, med referanser eller pekere.
- Typer deklareres og er faste, så mange feil Python får under kjøring blir kompileringsfeil i C++.
- `10 / 3` er `3`, og `int` har fast bredde og kan flyte over.
- Objekter ødelegges deterministisk ved slutten av scope sitt (RAII) — men en referanse til et ødelagt objekt krasjer.
- Skriv C++, ikke direkte oversatt Python: verdier og `const` som standard, ekte typer, og kompilatoradvarsler på.
