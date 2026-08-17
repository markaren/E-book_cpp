# Minnehåndtering

Hver verdi i et C++-program lever et sted i minnet. Som oftest trenger du ikke tenke på *hvor*: språket og kompilatoren håndterer det for deg. Men automasjonskode snakker med maskinvare, bygger tilstandsmaskiner med lang levetid og kjører i timevis; å håndtere minnet feil her gir ekte feil som ekte brukere får se.

Dette kapittelet går gjennom de to stedene verdier kan leve (**stakken** og **heapen**), den manuelle måten å håndtere dynamisk minne på (`new` / `delete`), hvorfor den er farlig, og de moderne verktøyene (**smarte pekere**) som gjør det trygt igjen.

---

## Stakken vs. heapen {#stack-vs-heap}

To minneområder betyr noe for en programmerer:

| | Stakken | Heapen |
|---|-------|------|
| **Allokering** | Automatisk; skjer når en variabel deklareres | Manuell; du ber om det med `new` (eller, bedre, en smart peker) |
| **Frigjøring** | Automatisk; når variabelen går ut av skop | Manuell; du må frigjøre det (eller la en smart peker gjøre det) |
| **Fart** | Svært rask; bare å flytte en peker | Tregere; trenger en ekte allokator |
| **Størrelse** | Liten (typisk noen få MB totalt per tråd) | Stor (begrenset av tilgjengelig RAM) |
| **Levetid** | Knyttet til blokken rundt | Lever til det eksplisitt frigjøres |

Den aller viktigste regelen:

> **Foretrekk stakken.** Bruk heapen bare når stakken ikke strekker til.

Stakken fungerer så lenge:

- størrelsen på dataene er kjent ved kompilering, og
- dataene ikke trenger å overleve funksjonen som skapte dem.

Når ett av vilkårene ryker (en vektor som vokser ved kjøring, et objekt som må overleve funksjonen som bygde det, et array med en størrelse som avhenger av en sensoravlesning), bruker du heapen.

### Eksempel med stakken {#stack-example}

```cpp
#include <iostream>

void demo() {
    int  count = 42;       // på stakken
    double pi    = 3.14;   // på stakken
    std::cout << count << " " << pi << "\n";
}   // begge variablene destrueres automatisk her
```

Ingenting å rydde opp. Hver lokale variabel opprettes når funksjonen entres og destrueres når funksjonen returnerer. Dette er den enkle, raske, korrekte standarden.

### Eksempel med heapen (den manuelle måten, ikke skriv kode som dette) {#heap-example-the-manual-way-do-not-write-code-like-this}

```cpp
#include <iostream>

int main() {
    int* heapInt = new int(42);          // allokerer på heapen
    std::cout << *heapInt << "\n";       // dereferer for å lese verdien
    delete heapInt;                      // frigjør minnet, obligatorisk!
    return 0;
}
```

Pekeren og verdien den peker på, lever på forskjellige steder — pekeren på stakken, `int`-en den fikk utdelt på heapen:

```text
   STAKKEN (frigjøres automatisk)     HEAPEN (du må frigjøre den)

       heapInt  ●───────────────────────►  [ 42 ]
```

`new` allokerer minne på heapen og returnerer en peker til det. `delete` frigjør minnet. Du må kalle `delete` nøyaktig én gang for hver `new`, uansett hva som skjer, inkludert når et unntak kastes midtveis i funksjonen din.

Dette er vanskeligere enn det høres ut.

---

## Hvorfor rå `new` / `delete` er farlig {#why-raw-new-delete-is-dangerous}

Tre typer feil hjemsøker enhver C-kodebase og enhver C++-kodebase som bruker rå `new` / `delete`:

**1. Minnelekkasjer.** Glem å `delete`, og minnet er tapt for resten av programmets levetid.

```cpp
void process() {
    int* data = new int[1000];
    if (somethingFailed()) {
        return;            // lekkasje, `data` frigjøres aldri
    }
    delete[] data;
}
```

**2. Use-after-free.** Bruk en peker etter at minnet er frigjort, og du får udefinert oppførsel: som regel et krasj, noen ganger stille datakorrupsjon.

```cpp
int* p = new int(5);
delete p;
std::cout << *p << "\n";   // udefinert oppførsel
```

**3. Double-free.** Å kalle `delete` to ganger på samme peker er også udefinert oppførsel.

```cpp
int* p = new int(5);
delete p;
delete p;                  // udefinert oppførsel
```

Hver eneste av disse er usynlig i kildekoden; ingenting forteller leseren at "denne pekeren er allerede frigjort". De viser seg ved kjøring, ofte i produksjon, ofte etter en lang og tilfeldig forsinkelse.

---

## Fella: klasser som eier rå pekere {#the-trap-classes-that-own-raw-pointers}

Et vanlig nybegynnermønster: en klasse allokerer noe med `new` i konstruktøren sin og frigjør det i destruktøren.

```cpp
class Buffer {
public:
    explicit Buffer(int size) : data_(new int[size]) {}
    ~Buffer()        { delete[] data_; }

    int* data() { return data_; }

private:
    int* data_;
};
```

Dette ser fornuftig ut. Det er ødelagt.

Se hva som skjer når du kopierer en `Buffer`:

```cpp
Buffer a(100);
Buffer b = a;     // kopierer pekeren, ikke minnet under
// `a.data_` og `b.data_` peker nå på SAMME array
```

```text
   STAKKEN                       HEAPEN

   a.data_  ●─────────┐
                      ├────────►  [  det ene int-arrayet  ]
   b.data_  ●─────────┘
```

Når `a` og `b` destrueres, blir det samme arrayet `delete[]`-et to ganger. Det er udefinert oppførsel. Standardkopien C++ leverer, er en *shallow copy*: den kopierer *pekeren*, ikke det pekeren peker på.

Den klassiske løsningen (å implementere en kopikonstruktør, en kopitilordningsoperator og en destruktør som alle er enige om eierskapet) kalles **Rule of Three**, eller i moderne C++ **Rule of Five**, som legger til flytteoperasjonene. Den er korrekt, men den er også mye feilutsatt kode for det som burde vært en enkel type.

Det finnes et bedre svar: **ikke ei rå pekere**.

---

## Smarte pekere {#smart-pointers}

En **smart peker** er en liten klasse som eier en peker og automatisk sletter den når den smarte pekeren selv går ut av skop. Det er RAII anvendt på dynamisk minne.

C++-standardbiblioteket tilbyr tre, alle i `<memory>`:

| Type                | Eierskap | Når du bruker den |
|---------------------|-----------|-------------|
| `std::unique_ptr<T>` | Nøyaktig én eier | Nesten alltid |
| `std::shared_ptr<T>` | Flere medeiere, telles | Når eierskapet genuint er delt |
| `std::weak_ptr<T>`   | Ikke-eiende observatør av en `shared_ptr` | Bryte referansesykluser |

### `std::unique_ptr`: standardvalget {#stdunique_ptr-the-default}

```cpp
#include <iostream>
#include <memory>

class Motor {
public:
    explicit Motor(int id) : id_(id) {
        std::cout << "Motor " << id_ << " constructed\n";
    }
    ~Motor() {
        std::cout << "Motor " << id_ << " destroyed\n";
    }
    void spin() { std::cout << "Motor " << id_ << " spinning\n"; }
private:
    int id_;
};

int main() {
    std::unique_ptr<Motor> m = std::make_unique<Motor>(7);
    m->spin();
    // Ingen delete trengs, destruktøren til m frigjør Motor-en automatisk
    return 0;
}
```

Utskrift:

```
Motor 7 constructed
Motor 7 spinning
Motor 7 destroyed
```

`std::make_unique<Motor>(7)` allokerer en `Motor` på heapen og gir pekeren til en `unique_ptr` som eier den. Du når objektets medlemmer gjennom den smarte pekeren med `->`, akkurat som med en rå peker (`m->spin()` betyr `(*m).spin()` — se [pekere til objekter](../Chapter4/types_refs_ptrs.md#pointers-to-objects)). Når `m` går ut av skop, kjører destruktøren dens, og `Motor`-en destrueres. Ingen lekkasjer, ingen use-after-free, ingen double-delete.

En `unique_ptr` kan ikke kopieres (det ville skapt en eier nummer to), men den kan **flyttes**:

```cpp
std::unique_ptr<Motor> a = std::make_unique<Motor>(1);
std::unique_ptr<Motor> b = std::move(a);   // eierskapet overført til b
// a er nå tom (nullptr); b eier Motor-en
```

(Mer om `std::move` på [neste side](move.md).)

### `std::shared_ptr`: delt eierskap {#stdshared_ptr-shared-ownership}

Når flere deler av programmet ditt legitimt deler eierskapet til ett objekt (og ingen av dem alene kan avgjøre når det skal destrueres), bruker du `std::shared_ptr`. Den holder en **referansetelling** og sletter objektet når den siste `shared_ptr`-en til det forsvinner.

Den definerende forskjellen fra `unique_ptr`: en `shared_ptr` **kan kopieres**. Hver kopi er enda en medeier, og hver kopi øker den delte referansetellingen med én; hver destruksjon senker den igjen. (Husk at `unique_ptr` forbyr kopiering fullstendig — den *eneste* måten å gi en videre på er å flytte den.) Objektet destrueres nøyaktig når tellingen når null.

Se for deg en `Sensor` som både en logger og en kontroller trenger å holde i live. Ingen av dem bør være eneeier, og sensoren må leve til *begge* er ferdige med den — et skoleeksempel på delt eierskap:

```cpp
#include <iostream>
#include <memory>
#include <string>

class Sensor {
public:
    explicit Sensor(std::string name) : name_(std::move(name)) {
        std::cout << "Sensor " << name_ << " created\n";
    }
    ~Sensor() { std::cout << "Sensor " << name_ << " destroyed\n"; }
    double read() const { return 21.5; }

private:
    std::string name_;
};

class Controller {
public:
    explicit Controller(std::shared_ptr<Sensor> s) : sensor_(std::move(s)) {}   // tar delt eierskap
    // ... bruker sensor_ ...
private:
    std::shared_ptr<Sensor> sensor_;
};

int main() {
    auto sensor = std::make_shared<Sensor>("outdoor");
    std::cout << sensor.use_count() << "\n";     // 1 — bare main holder den

    Controller ctrl(sensor);                     // ctrl er nå medeier
    std::cout << sensor.use_count() << "\n";     // 2

    {
        Controller ctrl2(sensor);
        std::cout << sensor.use_count() << "\n"; // 3
    }                                            // ctrl2 borte → tellingen tilbake på 2
    std::cout << sensor.use_count() << "\n";     // 2
}   // ctrl og sensor forsvinner → tellingen når 0 → "Sensor outdoor destroyed" skrives ut her
```

`use_count()` rapporterer hvor mange `shared_ptr`-er som eier objektet akkurat nå. Det er et hendig vindu inn i hva som skjer — nyttig for læring og feilsøking — selv om ekte kode sjelden trenger å slå den opp.

**Å sende en `shared_ptr` rundt.** En vanlig feil er å ta imot `shared_ptr<T>` overalt. Ikke gjør det. Parametertypen bør si hva funksjonen gjør med eierskapet:

| Funksjonen… | Parameter å ta |
|---------------|-------------------|
| Bare *bruker* objektet så lenge kallet varer | `const T&` (eller `T&` for å endre det) — ingen eierskap, ingen trafikk på referansetellingen |
| *Lagrer* objektet og blir medeier | `std::shared_ptr<T>` **som verdi** (og deretter `std::move` den inn i medlemmet) |

`logReading(const Sensor&)` bare leser en sensor, så den låner én og rører aldri tellingen. `Controller` holder sensoren sin i live gjennom hele sitt eget liv, så den tar en `shared_ptr` som verdi og lagrer den. Å ta en `shared_ptr` når du bare trengte en referanse, tvinger frem en unødvendig oppdatering av referansetellingen ved hvert kall.

**Polymorfisme fungerer akkurat som med `unique_ptr`.** En `shared_ptr` til en basisklasse sender virtuelle kall til den faktiske avledede typen:

```cpp
std::shared_ptr<Shape> s = std::make_shared<Circle>(2.0);
std::cout << s->area() << "\n";     // kaller Circle::area() — virtuelt kall gjennom shared_ptr-en
```

`shared_ptr` er dyrere enn `unique_ptr` (referansetellingen må vedlikeholdes, atomisk, slik at den er trygg å dele mellom tråder). Strekk deg etter den bare når delt eierskap virkelig er det du trenger — noe som i praksis er sjeldnere enn nybegynnere venter.

### `std::weak_ptr`: ikke-eiende observatør {#stdweak_ptr-non-owning-observer}

To `shared_ptr`-er som peker på hverandre, holder hverandre i live for alltid (en **referansesyklus**, og en lekkasje). `std::weak_ptr` er en peker som kan observere en `shared_ptr` uten å bidra til referansetellingen dens, og det er slik du bryter slike sykluser. Du vil møte dette i graf- og forelder/barn-strukturer; det er ikke noe å bekymre seg for på dag én.

---

## Rule of Zero {#the-rule-of-zero}

Se nå på `Buffer`-klassen fra tidligere igjen, skrevet med en `unique_ptr` i stedet for en rå peker:

```cpp
class Buffer {
public:
    explicit Buffer(int size) : data_(std::make_unique<int[]>(size)) {}

    int* data() { return data_.get(); }

private:
    std::unique_ptr<int[]> data_;
};
```

Ingen destruktør. Ingen kopikonstruktør. Ingen tilordningsoperator. De kompilatorgenererte standardvariantene er korrekte, fordi `unique_ptr` allerede vet hvordan den håndterer minnet sitt. Den forbyr dessuten kopiering, som er nøyaktig oppførselen vi vil ha.

Dette er **Rule of Zero** ("nullregelen"): hvis alle medlemmene i klassen din håndterer sin egen levetid (via RAII), trenger du ikke skrive *noen* spesielle medlemsfunksjoner. De fleste veldesignede C++-klasser er skrevet slik.

I praksis: når du tar deg selv i å strekke deg etter `new` og `delete`, stopp og spør om `std::vector`, `std::string` eller `std::unique_ptr` allerede gjør det du trenger.

---

## Beste praksis {#best-practices}

- **Foretrekk stakken.** Bruk heapen bare når stakken ikke strekker til.
- **Skriv aldri `new` eller `delete` i moderne C++.** Bruk `std::make_unique` og `std::make_shared`.
- **Velg `unique_ptr` som standard.** Bruk `shared_ptr` bare når eierskapet genuint er delt.
- **Bruk standardbeholderne** (`std::vector`, `std::string`) i stedet for hjemmesnekrede dynamiske arrayer.
- **Sikt mot Rule of Zero.** Må du først skrive dine egne spesielle medlemsfunksjoner, skriv alle sammen (Rule of Five).
- **Smarte pekere er ikke søppelsamling.** De er deterministiske: destruksjonen skjer på et kjent, forutsigbart tidspunkt. Det er en styrke, spesielt for innebygd kode.

---

## Oppsummering {#summary}

Heapen er nødvendig, men rå heap-håndtering er feilutsatt nok til at erfarne C++-programmerere unngår å skrive `new` og `delete` direkte. Smarte pekere og standardbeholderne gir deg de samme mulighetene med automatisk opprydding, unntakssikkerhet og tydelig eierskapssemantikk. Start med stakken; strekk deg etter `std::unique_ptr` når du må; strekk deg etter `std::shared_ptr` bare når eierskapet virkelig er delt.
