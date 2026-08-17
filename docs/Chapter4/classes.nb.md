# Klasser

En **klasse** er en brukerdefinert type. Der en `int` holder et heltall og en `std::vector` holder en liste med verdier, holder en klasse du skriver selv akkurat de dataene problemet ditt trenger (en motor, en styreenhet, en sensoravlesning) sammen med operasjonene som gir mening på de dataene.

Klasser er organiseringsenheten i objektorientert C++. Alt annet i dette kapittelet, og det meste av resten av boken, henger på denne ideen: bunt sammen beslektede data og operasjonene som virker på dem, i én enkelt type.

---

## En første klasse {#a-first-class}

```cpp
class Motor {
public:
    void start()      { running_ = true; }
    void stop()       { running_ = false; }
    bool isRunning() const { return running_; }

private:
    bool running_ = false;
};
```

Tre deler å lese ut:

- **Klassenavnet** (`Motor`). Stor forbokstav etter konvensjon.
- **Offentlige medlemmer:** det kode *utenfor* klassen kan bruke. Her: `start`, `stop`, `isRunning`.
- **Private medlemmer:** intern tilstand. Her: `running_`. Understreken på slutten er en konvensjon for "dette er et datamedlem i en klasse."

Å bruke den:

```cpp
Motor m;
m.start();
if (m.isRunning()) {
    std::cout << "running\n";
}
m.stop();
```

Kode utenfor kan kalle `m.start()` fordi `start` er offentlig. Kode utenfor kan ikke skrive `m.running_ = true;` direkte, fordi `running_` er privat. Dette er grunnformen av **innkapsling**: klassen eier tilstanden sin og bestemmer hva omverdenen får lov til å gjøre med den.

> De tre delene — navnet, de offentlige operasjonene, de private dataene — er nøyaktig det et **UML-klassediagram** tegner som en merket boks. UML er den visuelle stenografien ingeniører bruker til å skissere et design og relasjonene mellom klasser; denne boken bruker det til diagrammene i senere kapitler. Se [UML-klassediagrammer](../uml.md) for hvordan du leser og tegner dem.

---

## Medlemmer: data og funksjoner {#members-data-and-functions}

En klasse har to slags medlemmer:

- **Datamedlemmer** (også kalt felter, attributter eller instansvariabler): dataene hver instans holder.
- **Medlemsfunksjoner** (også kalt metoder): operasjonene klassen støtter.

```cpp
class Sensor {
public:
    double read() const { return lastReading_; }
    void   update(double value) { lastReading_ = value; }

private:
    double lastReading_ = 0.0;     // datamedlem
    int    sampleCount_ = 0;       // datamedlem
};
```

En `const` etter parameterlisten (`read() const`) betyr "denne funksjonen endrer ikke objektet." Merk hver medlemsfunksjon `const` hvis den kan være det. Kompilatoren håndhever det, og det forteller leseren "dette kallet er trygt; det observerer, det endrer ikke."

Hva "håndhever det" betyr i praksis: et `const`-objekt kan kalle **bare** de medlemsfunksjonene som er merket `const`.

```cpp
const Sensor s;        // en skrivebeskyttet Sensor
double r = s.read();   // OK — read() er const
// s.update(2.0);      // kompileringsfeil — update() er ikke const
```

Fordi `s` er `const`, lar kompilatoren deg kalle `read()` (som lover å ikke endre objektet), men avviser `update()` (som ville gjort det). Så hvis du glemmer `const` på en getter som `read()`, kan ingen `const Sensor` kalle den i det hele tatt. Å merke observatører `const` og mutatorer ikke-`const` er disiplinen som kalles **const-korrekthet**. Å sende et objekt ved `const`-referanse — [neste side](types_refs_ptrs.md) — er der dette virkelig gir gevinst.

---

## Tilgangsspesifikatorer {#access-specifiers}

Tre nøkkelord styrer hva som er tilgjengelig hvorfra:

| Spesifikator | Synlig utenfra klassen | Synlig fra en avledet klasse |
|-----------|--------------------------------|------------------------------|
| `public`    | Ja | Ja |
| `protected` | Nei  | Ja |
| `private`   | Nei  | Nei  |

For hverdagsklasser er `public` for grensesnittet og `private` for alt annet. `protected` gir bare mening med arv ([Polymorfisme](../Chapter5/polymorphism.md)) — den eksponerer et medlem for avledede klasser, men ikke for kode utenfor. Du vil sjelden trenge den; ha `private` som standard, og løsne til `public` bare når kode utenfor genuint trenger tilgang.

### `struct` vs. `class` {#struct-vs-class}

En `struct` er det samme som en `class` med én forskjell: medlemmene er **offentlige** som standard i stedet for private.

```cpp
struct Point {     // medlemmene er offentlige som standard
    double x;
    double y;
};
```

Konvensjonen er å bruke `struct` for en liten bunt med data uten invarianter å beskytte — en koordinat, en RGB-farge, et par avlesninger — der medlemmene er ment å leses og skrives direkte. Bruk `class` når typen har oppførsel eller invarianter å håndheve, slik at dataene hører hjemme bak en `private`-vegg. Du vil se `struct` igjen når vi lærer opp strømmen i [IO og strømmer](io_streams.md).

---

## Konstruktører {#constructors}

En **konstruktør** er en spesiell medlemsfunksjon som kjører når et objekt opprettes. Det er der du setter opp starttilstanden.

```cpp
class Motor {
public:
    Motor(int id, double maxRpm)
        : id_(id), maxRpm_(maxRpm) {}      // member initialiser list

private:
    int    id_;
    double maxRpm_;
    bool   running_ = false;
};

Motor m(1, 3000.0);   // kaller konstruktøren med id=1, maxRpm=3000.0
```

Delen etter `:` og før `{}` er konstruktørens **member initialiser list**. Den initialiserer datamedlemmene direkte, før konstruktørkroppen kjører.

Foretrekk *member initialiser list* fremfor tilordning i konstruktørkroppen:

```cpp
// Mindre bra: medlemmene standardkonstrueres og tilordnes etterpå
Motor(int id, double maxRpm) {
    id_     = id;
    maxRpm_ = maxRpm;
}

// Bedre: medlemmene konstrueres med riktig verdi i ett steg
Motor(int id, double maxRpm)
    : id_(id), maxRpm_(maxRpm) {}
```

Forskjellen betyr mer for ikke-trivielle typer (du unngår en ekstra standardkonstruksjon) og er helt nødvendig for medlemmer som *må* initialiseres nøyaktig én gang (`const`-medlemmer, referanser, typer uten standardkonstruktør).

### Standardverdier for datamedlemmer {#default-values-for-data-members}

Du kan gi datamedlemmer standardverdier direkte i klassedefinisjonen:

```cpp
class Motor {
private:
    int    id_      = 0;
    double maxRpm_  = 1000.0;
    bool   running_ = false;
};
```

En konstruktør som ikke nevner et medlem, bruker standardverdien. Hvis konstruktørens initialiseringsliste nevner det, vinner den verdien.

### Flere konstruktører {#multiple-constructors}

Du kan ha flere konstruktører så lenge de tar ulike parametere:

```cpp
class Motor {
public:
    Motor() = default;                            // standardkonstruktør
    Motor(int id) : id_(id) {}
    Motor(int id, double maxRpm) : id_(id), maxRpm_(maxRpm) {}
};

Motor a;              // standard
Motor b(1);           // bare id
Motor c(2, 5000.0);   // id og maks RPM
```

`= default` ber kompilatoren generere en standardkonstruktør for deg som ikke gjør noe. Det er kortere enn å skrive `Motor() {}` og signaliserer intensjon.

### Stoppe stille konverteringer: `explicit` {#stopping-silent-conversions-explicit}

En konstruktør du kan kalle med et *enkelt* argument — som `Motor(int id)` ovenfor — fungerer også som en implisitt konvertering: kompilatoren vil i det stille gjøre en `int` om til en `Motor` overalt der en forventes. Det er av og til hendig og ofte en kilde til overraskende feil. Sett `explicit` foran for å slå det av:

```cpp
class Motor {
public:
    explicit Motor(int id) : id_(id) {}
private:
    int id_ = 0;
};

Motor a(7);     // greit — du ba eksplisitt om en Motor
Motor b = 7;    // kompileringsfeil: ingen stille int-til-Motor-konvertering
```

Vanen: merk konstruktører med ett argument `explicit` med mindre du spesifikt ønsker konverteringen.

---

## Nøkkelordet `this` {#the-this-keyword}

Inne i enhver medlemsfunksjon refererer `this` til objektet funksjonen ble kalt på — teknisk sett er det en *peker*, som [neste seksjon](types_refs_ptrs.md) forklarer. Du trenger sjelden å skrive `this`, fordi medlemmene er tilgjengelige med sitt bare navn:

```cpp
void Motor::start() {
    running_ = true;       // betyr this->running_
}
```

Det ene tilfellet der du *må* bruke `this`: når en parameter skygger for et medlem.

```cpp
class Motor {
public:
    void setId(int id) {
        this->id_ = id;   // skiller dem, men bedre å unngå skyggen:
    }
    // Renere:
    // void setId(int newId) { id_ = newId; }

private:
    int id_;
};
```

Dekorer datamedlemmene dine (konvensjonen med understrek på slutten), så oppstår skygging sjelden i utgangspunktet.

---

## Statiske medlemmer {#static-members}

Hvert medlem så langt har tilhørt et *objekt*: hver `Motor` har sin egen `id_`, sin egen `running_`. Et **statisk** medlem tilhører **selve klassen** — det finnes bare ett, delt av alle instanser.

En vanlig bruk er å gi hvert nytt objekt en unik id fra en delt teller:

```cpp
class Motor {
public:
    Motor() : id_(++count_) {}              // hver ny Motor tar neste nummer
    int id() const { return id_; }

    static int count() { return count_; }   // hvor mange Motor-er som er opprettet

private:
    int id_;
    static inline int count_ = 0;           // ÉN teller, delt av alle Motor-er
};

Motor a;   // id 1
Motor b;   // id 2
std::cout << a.id() << ", " << b.id() << "\n";   // 1, 2
std::cout << Motor::count() << "\n";              // 2
```

To statiske ting skjer her:

- **`count_` er et statisk datamedlem** — det er ikke en del av noen enkelt `Motor`; det finnes nøyaktig ett, og hver konstruktør øker det samme. (`inline` lar deg gi det verdien rett her i klassen; uten den måtte du ha definert det separat i en `.cpp`.)
- **`count()` er en statisk medlemsfunksjon** — du kaller den på klassen, `Motor::count()`, helt uten objekt. Uten et objekt har den ingen `this` og kan ikke røre per-objekt-medlemmene som `id_`; den kan bare bruke de statiske medlemmene. Statiske funksjoner er hendige for klasseomfattende spørringer som denne, og for *fabrikkfunksjoner* — statiske funksjoner som bygger og returnerer et ferdig objekt av klassen.

Det tryggeste og vanligste statiske medlemmet er en **konstant** som tilhører typen:

```cpp
class Motor {
public:
    static constexpr double maxRpm = 10000.0;     // delt, og endres aldri
};

double limit = Motor::maxRpm;
```

> **Et endrbart statisk medlem er en global variabel i forkledning.** Delt, klasseomfattende, endrbar tilstand bærer alle farene til en [global variabel](../Chapter1/functions.md#global-variables): hvilken som helst kode kan endre den, og den gjør klassen vanskeligere å resonnere om og å teste. Grip sjelden til endrbare statiske data; en `static constexpr`-konstant, som aldri endres, er det trygge hverdagstilfellet.

---

## Innkapsling i praksis {#encapsulation-in-practice}

Poenget med å gjøre data private er ikke paranoia. Det er at klassen kan håndheve **invarianter**: regler om dataene som aldri skal brytes.

En bankkonto der saldoen aldri må bli negativ; en sensor der tidsstempelet aldri må avta; en motor der turtallet ikke kan overstige det oppgitte maksimumet. Hvis dataene er offentlige, må hver kaller huske å sjekke. Hvis dataene er private og bare oppdateres via medlemsfunksjoner, bor sjekken på ett sted.

```cpp
class BankAccount {
public:
    explicit BankAccount(double initialBalance)
        : balance_(initialBalance) {}

    void deposit(double amount) {
        if (amount <= 0) {
            return;                  // avvis tull
        }
        balance_ += amount;
    }

    bool withdraw(double amount) {
        if (amount <= 0 || amount > balance_) {
            return false;            // kan ikke gå i minus
        }
        balance_ -= amount;
        return true;
    }

    double balance() const { return balance_; }

private:
    double balance_;
};
```

`balance_` er privat, så den kan bare endres gjennom `deposit` og `withdraw`. Begge sjekker operasjonen før de utfører den. Invarianten "saldoen er aldri negativ" håndheves på ett sted.

---

## Spesielle medlemsfunksjoner: Rule of Zero, Three og Five {#special-member-functions-the-rule-of-zero-three-and-five}

Når du oppretter, kopierer eller destruerer et objekt, kan C++ kalle opptil seks spesielle medlemsfunksjoner:

| Funksjon | Når den kjører |
|----------|--------------|
| Standardkonstruktør    | Når et objekt opprettes uten argumenter |
| Destruktør             | Når objektet destrueres |
| Kopikonstruktør       | Når et nytt objekt initialiseres fra et eksisterende (`B b = a;`) |
| Kopitilordning        | Når det tilordnes til et eksisterende objekt (`b = a;`) |
| Flyttekonstruktør       | Når det initialiseres fra et midlertidig objekt ([kapittel 5](../Chapter5/move.md) forklarer flytting) |
| Flyttetilordning        | Når det tilordnes fra et midlertidig objekt ([kapittel 5](../Chapter5/move.md) forklarer flytting) |

Hvis du ikke skriver noen av disse, genererer kompilatoren dem for deg. De genererte versjonene gjør det opplagte: kopierer eller flytter hvert medlem. For de *fleste* klasser er det akkurat det du vil ha.

Tommelfingerreglene er velkjente:

### Rule of Zero (den moderne standarden) {#rule-of-zero-the-modern-default}

> Hvis klassens datamedlemmer kan forvalte seg selv (via standardbeholderne eller smartpekere), så ikke skriv noen spesielle medlemsfunksjoner. De kompilatorgenererte standardversjonene er korrekte.

```cpp
class Telemetry {
public:
    Telemetry(std::string deviceId)
        : deviceId_(deviceId) {}

    void record(double value) { samples_.push_back(value); }

private:
    std::string         deviceId_;
    std::vector<double> samples_;
};
```

Ingen destruktør. Ingen kopi- eller flytteoperasjoner. Standardversjonene fungerer fordi `std::string` og `std::vector` allerede vet hvordan de skal kopiere, flytte og destruere seg selv korrekt. Dette er det renest mulige klassedesignet og målet for nesten alle klassene dine.

### Når du ikke kan bruke Rule of Zero {#when-you-cant-use-the-rule-of-zero}

Av og til forvalter en klasse en *rå* ressurs direkte — en minneblokk, et filhåndtak, en lås. Da er de kompilatorgenererte kopi- og destruksjonsoperasjonene som regel feil: to objekter ender opp med å eie samme ting, og programmet krasjer når begge prøver å frigi den. Å håndtere det korrekt betyr å skrive flere av de spesielle medlemmene sammen — de klassiske **Rule of Three** og **Rule of Five**.

Det vil du sjelden trenge. Den bedre løsningen er nesten alltid å la en standardtype eie ressursen for deg — en `std::vector`, en `std::string` eller en smartpeker — noe som setter deg rett tilbake til Rule of Zero. [Minnehåndtering](../Chapter5/memory.md) og [Flyttesemantikk](../Chapter5/move.md) dekker rå ressurser, kopiering og flytting fullt ut, når du først har møtt pekere og heap-en.

Det praktiske rådet for dette emnet: **sikt mot Rule of Zero.**

---

## Å dele opp deklarasjonen og implementasjonen {#splitting-the-declaration-and-the-implementation}

Alt vi har skrevet så langt har hatt implementasjonen inne i klassekroppen. For lengre funksjoner deler du dem vanligvis ut:

**motor.hpp** — deklarasjonen:

```cpp
#pragma once
#include <string>

class Motor {
public:
    Motor(int id, double maxRpm);

    void start();
    void stop();
    bool isRunning() const;

    std::string describe() const;

private:
    int    id_;
    double maxRpm_;
    bool   running_ = false;
};
```

**motor.cpp** — implementasjonen:

```cpp
#include "motor.hpp"
#include <format>

Motor::Motor(int id, double maxRpm)
    : id_(id), maxRpm_(maxRpm) {}

void Motor::start() {
    running_ = true;
}

void Motor::stop() {
    running_ = false;
}

bool Motor::isRunning() const {
    return running_;
}

std::string Motor::describe() const {
    return std::format("Motor {} (max {} RPM)", id_, maxRpm_);  // std::format fyller hver {} med et argument, i rekkefølge
}
```

`Motor::` foran hvert funksjonsnavn sier "denne funksjonen tilhører klassen `Motor`." Headeren er det andre filer `#include`-er; implementasjonsfilen kompileres separat.

`#pragma once` på headerens første linje er den **include-guarden** du møtte i [CMake](../Chapter2/cmake_intro.md#headers). En header blir *limt inn* overalt der den `#include`-es, og det er lett for én fil å ende opp med å inkludere samme header to ganger (direkte, og igjen gjennom en annen header). Uten guarden ville klassen blitt definert to ganger i den filen, og kompilatoren ville avvist det. `#pragma once` forteller kompilatoren "uansett hvor mange ganger du blir bedt, lim denne filen inn bare én gang." Sett den øverst i hver header du skriver.

(`describe` bruker `std::format`, som bygger en streng ved å fylle hver `{}` med neste argument — den moderne måten å sette sammen tekst på. Se [Strenger](../strings.md).)

For korte funksjoner (enlinjere, enkle gettere) er det greit å beholde dem inne i klassen. For alt som er større, del det ut: headeren forblir lesbar, og kompileringstidene bedres.

**Hvorfor kompileringstidene bedres.** En header limes inn i *hver* `.cpp` som `#include`-er den. En funksjonskropp som blir liggende i headeren, kompileres derfor på nytt i hver av de filene — og, verre, hver gang du redigerer den kroppen regnes headeren som endret, så alle sammen må rekompileres. Flytt kroppen inn i `motor.cpp`, og den kompileres bare én gang; redigerer du den senere, bygges bare `motor.cpp` på nytt, ikke hver fil som inkluderer headeren.

---

## Oppsummering {#summary}

- En klasse bunter data sammen med operasjonene som virker på dem.
- La data være `private` som standard, og eksponer bare operasjonene kallerne trenger (`public`).
- Bruk **member initialiser list** i konstruktører.
- Dekorer datamedlemmer (`balance_`, `id_`) for å unngå navnekonflikter med parametere.
- Merk medlemsfunksjoner `const` når de ikke endrer objektet.
- **Sikt mot Rule of Zero**: design klasser der medlemmene forvalter seg selv, og la kompilatoren generere de spesielle medlemmene.
- Del lange klasser i en header (`.hpp`) og en implementasjon (`.cpp`).
