# Verdier, referanser og pekere

C++ gir deg tre måter å referere til data på: ved **verdi** (du har din egen kopi), ved **referanse** (et alias for noen andres data) og ved **peker** (en adresse som kanskje, kanskje ikke, peker på noe).

Hver av dem oppfører seg forskjellig, og hver har sin plass. Å velge riktig avgjør om funksjonen din endrer kallerens data, om den lager en dyr kopi, og om programmet krasjer når noe går galt.

Dette kapittelet forklarer alle tre og gir et klart standardvalg for hver situasjon.

---

## Verdityper {#value-types}

En verditype holder dataene selv. Å tilordne eller sende en verditype **kopierer** den.

```cpp
int a = 25;
int b = a;    // b er en kopi
b = 30;       // a er fortsatt 25
```

Dette er den tryggeste standarden, og slik alle innebygde typer og de fleste klassetyper oppfører seg som standard. Hver variabel har sitt eget uavhengige lager.

Kostnaden er kopien: for en `int` er den i praksis gratis, for en `std::vector` på 10 MB er den en heap-allokering og en `memcpy`. ([Kapittelet om flyttesemantikk](../Chapter5/move.md) forklarer hvordan moderne C++ unngår mange av disse kopiene automatisk.)

---

## Referanser {#references}

En **referanse** er et alias for en eksisterende variabel. Lesing og skriving gjennom referansen går rett til originalen.

```cpp
int age = 42;
int& refAge = age;    // refAge er et annet navn for age
refAge = 10;          // age er nå 10
```

Tre ting gjør referanser forskjellige fra pekere:

- En referanse må initialiseres når den deklareres. Det finnes ingen "uinitialisert" referanse.
- En referanse kan ikke bindes på nytt. Når den først refererer til `age`, refererer den til `age` for alltid.
- Det finnes ingen null-referanse: en referanse starter alltid bundet til et virkelig objekt. Den kan derimot overleve objektet og bli *dangling* — se [Den store levetidsfellen](#the-big-lifetime-trap) nedenfor.

Referanser er arbeidshesten for effektiv parameteroverføring i C++.

### `const`-referanser {#const-references}

En `const`-referanse er skrivebeskyttet. Funksjonen kan se på dataene, men ikke endre dem.

```cpp
void printVector(const std::vector<double>& v) {
    for (double x : v) {
        std::cout << x << "\n";
    }
    // v.push_back(0.0);   // kompileringsfeil, const
}
```

Dette er standardidiomet for å sende store objekter uten å kopiere dem:

```cpp
std::vector<double> data = readSensorBatch();
printVector(data);   // ingen kopi, printVector ser originalen via const&
```

Uten `const&` ville `printVector` mottatt en 10 MB stor kopi ved hvert kall. Med den koster kallet bare arbeidet med å sende én peker.

---

## Pekere {#pointers}

En **peker** er en variabel som holder en *adresse*. Operatoren `*` ser gjennom adressen til verdien som er lagret der:

```cpp
int x = 7;
int* p = &x;     // p holder adressen til x
*p = 42;         // skriver gjennom p, x er nå 42
```

| Symbol | Betydning |
|--------|---------|
| `int*`  | "peker til int"; typen til `p` |
| `&x`    | "adressen til x"; produserer en peker |
| `*p`    | "det `p` peker på"; dereferering  |

En referanse og en peker kan begge referere til samme variabel `x`, men mekanikken er forskjellig — en referanse gir `x` et andre *navn*, mens en peker er en separat celle som lagrer *adressen* til `x`:

<svg viewBox="0 0 500 175" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Å referere til variabelen x: en referanse (int og-tegn r = x) gir cellen til x et andre navn r; en peker (int stjerne p = og-tegn x) er en egen celle som holder adressen til x, og nås ved å følge pilen." style="display:block;margin:1rem auto;max-width:500px;width:100%;height:auto;font-family:var(--md-code-font-family,monospace);font-size:13px;" fill="none" stroke="currentColor" stroke-width="1.5">
  <defs>
    <marker id="rp-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor" stroke="none"/>
    </marker>
  </defs>
  <text x="40" y="28" stroke="none" fill="currentColor" font-weight="bold">int&amp; r = x;</text>
  <rect x="40" y="50" width="120" height="56" rx="4"/>
  <line x1="40" y1="76" x2="160" y2="76"/>
  <text x="100" y="68" stroke="none" fill="currentColor" text-anchor="middle">x &#183; r</text>
  <text x="100" y="97" stroke="none" fill="currentColor" text-anchor="middle" font-size="15">7</text>
  <text x="40" y="140" stroke="none" fill="currentColor" font-size="11" opacity="0.7">r er et annet navn for x</text>
  <text x="280" y="28" stroke="none" fill="currentColor" font-weight="bold">int* p = &amp;x;</text>
  <rect x="280" y="50" width="70" height="56" rx="4"/>
  <line x1="280" y1="76" x2="350" y2="76"/>
  <text x="315" y="68" stroke="none" fill="currentColor" text-anchor="middle">p</text>
  <text x="315" y="97" stroke="none" fill="currentColor" text-anchor="middle">&amp;x</text>
  <rect x="410" y="50" width="70" height="56" rx="4"/>
  <line x1="410" y1="76" x2="480" y2="76"/>
  <text x="445" y="68" stroke="none" fill="currentColor" text-anchor="middle">x</text>
  <text x="445" y="97" stroke="none" fill="currentColor" text-anchor="middle" font-size="15">7</text>
  <line x1="350" y1="92" x2="408" y2="92" marker-end="url(#rp-arrow)"/>
  <text x="280" y="140" stroke="none" fill="currentColor" font-size="11" opacity="0.7">p lagrer adressen til x</text>
</svg>

Pekere skiller seg fra referanser på tre viktige måter:

- En peker kan være `nullptr`, som betyr at den peker på ingenting.
- En peker kan tilordnes på nytt til å peke et annet sted.
- En peker kan være farlig: å dereferere en null-peker eller en ugyldig peker er udefinert oppførsel.

```cpp
int* p = nullptr;   // gyldig peker, peker på ingenting
if (p != nullptr) {
    *p = 5;         // trygt, sjekket først
}
```

Sjekk alltid før du derefererer, eller bruk språkkonstruksjoner som garanterer ikke-null (referanser, smartpekere).

### Pekere til objekter {#pointers-to-objects}

En peker kan peke på et klasseobjekt like lett som på en `int`. For å nå et medlem gjennom pekeren må du først dereferere den. Skrevet helt ut er det `(*p).read()` — parentesene trengs fordi `.` binder sterkere enn `*`. Fordi det er klønete, gir C++ deg pil-snarveien `->`:

```cpp
Sensor s;
Sensor* p = &s;

(*p).read();   // dereferer, kall så read()
p->read();     // nøyaktig det samme, skrevet på den lesbare måten
```

`p->read()` betyr presis `(*p).read()`. Pilen er det du kommer til å se i praksis — nesten ingen skriver `(*p).member`. Du vil møte `->` hele tiden i [kapittel 5](../Chapter5/polymorphism.md), der objekter rutinemessig håndteres gjennom pekere og smartpekere.

---

## Den store levetidsfellen {#the-big-lifetime-trap}

Regelen: en referanse eller peker er bare gyldig så lenge det den refererer til fortsatt lever. Den største enkeltkilden til krasj i C++ er å bruke en referanse eller peker til data som er blitt destruert.

### Å returnere en referanse eller peker til en lokal variabel {#returning-a-reference-or-pointer-to-a-local}

<!-- no-ce -->
```cpp
int& createIntRef() {
    int value = 1;
    return value;     // ille — `value` destrueres når funksjonen returnerer
}

int* createIntPtr() {
    int value = 1;
    return &value;    // ille — samme problem
}

int main() {
    int& bad1 = createIntRef();    // dangling referanse — udefinert oppførsel
    int* bad2 = createIntPtr();    // dangling peker — udefinert oppførsel
}
```

Begge funksjonene returnerer et håndtak til minne som ikke lenger tilhører noen. Å lese fra `bad1` eller `bad2` er udefinert oppførsel. Moderne kompilatorer advarer om nøyaktig dette mønsteret; følg med på advarslene.

Løsningen: returner ved verdi (du får din egen kopi), eller send en referanse *inn* i funksjonen slik at kalleren styrer levetiden.

### Pekere og referanser inn i klassers indre {#pointers-and-references-into-class-internals}

Å returnere en referanse eller peker til en klasses private data bryter også **innkapslingen** du møtte i [Klasser](classes.md):

```cpp
class Demo {
public:
    int  getValue() const   { return value_; }   // trygt — returnerer en kopi
    int& getValueRef()      { return value_; }   // deler ut skrivetilgang
    int* getValuePtr()      { return &value_; }  // deler ut skrivetilgang

private:
    int value_ = 0;
};

Demo obj;
int& ref = obj.getValueRef();
ref = 42;        // obj sine private data er nå 42, invariantene omgått
```

Hvis du må eksponere et medlem ved referanse, returner `const T&` for å holde det skrivebeskyttet. Ellers kan ekstern kode endre din private tilstand uten å gå gjennom metodene som håndhever invariantene dine.

---

## Hvilken skal jeg bruke? {#which-one-should-i-use}

Bruk denne tabellen hver gang en funksjonsparameter eller returtype tvinger frem spørsmålet:

| Situasjon | Bruk |
|-----------|-----|
| Liten type som er billig å kopiere (`int`, `double`, `bool`, en enum) | Send ved **verdi** |
| Funksjonen skal ikke endre inndataene | Send som **`const T&`** |
| Funksjonen endrer inndataene, og kalleren skal se endringen | Send som **`T&`** |
| Funksjonen kan motta "ingen verdi" | Send en **peker** (og sjekk for null), eller `std::optional<T>` |
| Funksjonen returnerer et nyberegnet resultat | Returner ved **verdi** (RVO gjør dette billig) |
| Funksjonen returnerer en av inndataene sine uendret | Returner ved **referanse** (vær forsiktig med levetider) |

For datamedlemmer i en klasse er tommelfingerreglene lignende:

| Situasjon | Bruk |
|-----------|-----|
| Klassen eier dataene | Vanlig verdimedlem (f.eks. `std::vector<int> data_`) |
| Klassen observerer data som eies av noe annet | En **rå peker (ikke-eiende)** — men tenk nøye over hvem som holder den i live |
| Klassen deler eierskap med andre | `std::shared_ptr<T>` (se [Minne](../Chapter5/memory.md)) |

---

## Oppsummering {#summary}

- **Verdityper** kopierer. Trygt, noen ganger dyrt.
- **Referanser** er alias. Kan ikke være null, kan ikke bindes på nytt, må initialiseres.
- **Pekere** er adresser. Kan være null, kan tilordnes på nytt, må sjekkes.
- En referanse eller peker som overlever det den peker på, er udefinert oppførsel — den vanligste enkeltårsaken til krasj.
- For funksjonsparametere: små typer ved verdi, store typer som `const T&`, endre-inndataene-tilfeller som `T&`.
- For eierskap på tvers av klassegrenser, foretrekk smartpekere fremfor rå pekere.
