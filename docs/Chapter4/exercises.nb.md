# Oppgaver til kapittel 4

Det er to slags oppgaver på denne siden.

**Oppvarmingene** kommer først: korte programmer du skal lese, der du forutsier hva som skjer og velger et svar i nettleseren. Ikke noe prosjekt, ingen skriving. Hver av dem er bygd på en regel dette kapittelet slår fast — `const`-korrekthet, når en destruktør kjører, hva `static` betyr, hvem som eier hva — der konsekvensen først blir opplagt når du har blitt tatt av den.

Så kommer **programmene**, fra oppgave 1 og utover. **Prøv hver enkelt selv før du avslører løsningen** — du lærer langt mer av et ærlig forsøk enn av å lese et ferdig svar. Skriv koden inn i CLion og kjør den; ikke bare les den.

Når du åpner en løsning vises den **uskarp** — klikk én gang til for å avsløre den, slik at du ikke ser svaret ved et uhell.

Hver oppgave er et lite program med sin egen `main()`. Hold dem i ett prosjekt med én `add_executable`-linje per fil (se [CMake](../Chapter2/cmake_intro.md)), og velg hvilket som skal kjøres fra rullegardinmenyen ved siden av den grønne ▶-knappen.

---

## Oppvarming: forutsi utskriften {#warm-ups-predict-the-output}

Bestem deg for hva hvert program gjør **før** du svarer. Å svare låser spørsmålet og avslører forklaringen.

### W1. Et const-objekt og en getter {#w1-a-const-object-and-a-getter}

<!-- no-ce -->
```cpp
#include <iostream>

class Sensor {
public:
    double read() { return value_; }
    void set(double v) { value_ = v; }

private:
    double value_ = 21.5;
};

int main() {
    const Sensor s;
    std::cout << s.read() << "\n";
}
```

````quiz
Hva skjer?
- Det skriver ut `21.5`
- =Det kompilerer ikke: `read()` er ikke `const`
- Det skriver ut `0`
- Det kompilerer, men skriver ut en søppelverdi
:::
**Det kompilerer ikke.** GCC og MSVC avviser begge kallet, MSVC med:

```
error C2662: 'double Sensor::read(void)': cannot convert 'this'
pointer from 'const Sensor' to 'Sensor &'
```

`s` er en `const Sensor`, og **et `const`-objekt kan bare kalle medlemsfunksjoner som er merket `const`**. `read()` endrer ingenting, men den har aldri sagt det, og kompilatoren går etter deklarasjonen, ikke etter hva kroppen tilfeldigvis gjør.

Løsningen er ett ord: `double read() const { return value_; }`. Det er derfor [Klasser](classes.md#members-data-and-functions) ber deg merke hver observatør `const` — glem det på en getter, og ikke noe `const`-objekt, og ingen `const&`-parameter, kan kalle den. Det er hele det praktiske poenget med const-korrekthet.
````

### W2. Når kjører destruktøren? {#w2-when-does-the-destructor-run}

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

class Trace {
public:
    explicit Trace(std::string name) : name_(std::move(name)) {
        std::cout << "open " << name_ << "\n";
    }
    ~Trace() { std::cout << "close " << name_ << "\n"; }

private:
    std::string name_;
};

int main() {
    Trace a("A");
    {
        Trace b("B");
        std::cout << "inner\n";
    }
    std::cout << "outer\n";
}
```

````quiz
I hvilken rekkefølge kommer de seks linjene?
- `open A`, `open B`, `inner`, `outer`, `close A`, `close B`
- =`open A`, `open B`, `inner`, `close B`, `outer`, `close A`
- `open A`, `open B`, `inner`, `outer`, `close B`, `close A`
- `open A`, `close A`, `open B`, `close B`, `inner`, `outer`
:::
**`open A`, `open B`, `inner`, `close B`, `outer`, `close A`.**

`b` destrueres ved den avsluttende krøllparentesen til den indre blokken — *før* `outer` skrives ut, ikke ved slutten av `main`. `a` lever til `main` selv avsluttes, så `close A` kommer sist.

To regler gjør alt arbeidet her. Et objekt destrueres **i det øyeblikket skopet det står i, avsluttes**, og objekter i samme skop destrueres i **motsatt rekkefølge av konstruksjonen** (sist bygd, først destruert). Det er det som gjør [RAII](raii.md) til å stole på: oppryddingen er festet til en krøllparentes du kan se, ikke til noe du må huske å kalle.
````

### W3. Én teller, tre objekter {#w3-one-counter-three-objects}

<!-- no-ce -->
```cpp
#include <iostream>

class Motor {
public:
    Motor() : id_(++count_) {}
    int id() const { return id_; }
    static int count() { return count_; }

private:
    int id_;
    static inline int count_ = 0;
};

int main() {
    Motor a;
    Motor b;
    Motor c;

    std::cout << a.id() << " " << c.id() << " " << Motor::count() << "\n";
}
```

````quiz
Hva skriver dette ut?
- `1 1 1`
- `1 3 1`
- =`1 3 3`
- `3 3 3`
:::
**`1 3 3`.**

`id_` er et vanlig datamedlem, så hver `Motor` har sitt eget: `a` fikk `1`, `c` fikk `3`, og de endres aldri. `count_` er **`static`** — det finnes nøyaktig én, delt av hele klassen, og hver konstruktør økte den samme. Etter tre motorer holder den `3`.

`Motor::count()` kalles på *klassen*, ikke på et objekt, og det er derfor det ikke står noen `a.` eller `c.` foran. Se [Statiske medlemmer](classes.md#static-members).
````

### W4. En referanse til noe som er borte {#w4-a-reference-to-something-that-is-gone}

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

const std::string& label() {
    std::string text = "sensor-1";
    return text;
}

int main() {
    std::cout << label() << "\n";
}
```

````quiz
Dette kompilerer. Hva er galt med det?
- Ingenting — å returnere `const&` unngår en kopi, som er den anbefalte stilen
- Det lekker minne, fordi `text` aldri frigis
- =`text` destrueres når `label` returnerer, så kalleren får en referanse til minne som ikke lenger finnes
- Det kompilerer ikke, fordi du ikke kan returnere en lokal variabel ved referanse
:::
**Referansen blir hengende.** `text` er en lokal variabel: den destrueres i det øyeblikket `label` returnerer, så referansen som gis tilbake, refererer til minne som ikke lenger lever. Å lese den er **udefinert oppførsel** — den kan skrive ut `sensor-1`, skrive ut søppel eller krasje, og den kan gjerne oppføre seg annerledes i en Release-bygging enn i Debug.

Det kompilerer, men kompilatoren prøver faktisk å si fra. MSVC advarer:

```
warning C4172: returning address of local variable or temporary : text
```

som er nøyaktig den typen advarsel [CMake-kapittelet](../Chapter2/cmake_intro.md#turn-on-compiler-warnings) slår på for deg, og nøyaktig den typen folk lærer seg å scrolle forbi.

Å returnere `const&` er virkelig den riktige måten å gi tilbake noe som **overlever kallet** — et datamedlem, for eksempel. Det er feil for en lokal variabel. Her returnerer du ved verdi: `std::string label()`. Se [Den store levetidsfellen](types_refs_ptrs.md#the-big-lifetime-trap).
````

### W5. Å skrive til samme fil to ganger {#w5-writing-to-the-same-file-twice}

<!-- no-ce -->
```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    {
        std::ofstream out("log.txt");
        out << "first\n";
    }
    {
        std::ofstream out("log.txt");
        out << "second\n";
    }

    std::ifstream in("log.txt");
    std::string line;
    while (std::getline(in, line)) {
        std::cout << line << "\n";
    }
}
```

````quiz
Hva skriver programmet ut til slutt?
- `first`, så `second`
- =`second`
- `first`
- Ingenting — den andre `ofstream`-en feiler fordi filen allerede er åpen
:::
**Bare `second`.** `first` er borte.

Å åpne en `std::ofstream` **trunkerer** filen som standard: den tømmes i det øyeblikket den åpnes, før du har skrevet en eneste ting. Den andre blokken starter derfor fra en tom `log.txt`, og den første linjen er tapt.

For å legge til i en fil i stedet for å erstatte den, åpne den i append-modus: `std::ofstream out("log.txt", std::ios::app);` Se [Å skrive en fil](io_streams.md#writing-a-file).

Merk at de to blokkene er det som gjør dette trygt å resonnere om: hver `ofstream` lukkes ved sin avsluttende krøllparentes, så filen flushes og slippes før den neste åpner den — [RAII](raii.md) igjen.
````

---

## 1. En vanntank som ikke kan renne over {#1-a-water-tank-that-cannot-overflow}

*Øver på: [Klasser](classes.md)*

Skriv en klasse `WaterTank`. **Kapasiteten** dens fastsettes når tanken opprettes, og den starter tom. Gi den tre operasjoner:

- `fill(amount)` fyller på vann, men nivået kan aldri overstige kapasiteten;
- `drain(amount)` tapper vann, men nivået kan aldri gå under null;
- `level()` rapporterer gjeldende nivå (og endrer ikke tanken).

Hold dataene **private**. Lag så, i `main`, en 100-liters tank, `fill(60)`, `fill(60)` igjen (den skal stoppe på 100, ikke 120), `drain(30)`, og skriv ut nivået.

> Hint: kapasiteten og nivået er tankens private tilstand. Bruk konstruktørens medlemsinitialiseringsliste til å sette kapasiteten, og merk `level()` som `const`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    class WaterTank {
    public:
        explicit WaterTank(double capacity) : capacity_(capacity) {}

        void fill(double amount) {
            level_ += amount;
            if (level_ > capacity_) {
                level_ = capacity_;        // aldri renn over
            }
        }

        void drain(double amount) {
            level_ -= amount;
            if (level_ < 0.0) {
                level_ = 0.0;              // aldri gå i minus
            }
        }

        double level() const { return level_; }

    private:
        double capacity_;
        double level_ = 0.0;
    };

    int main() {
        WaterTank tank(100.0);
        tank.fill(60.0);
        tank.fill(60.0);     // ville nådd 120, begrenses til 100
        tank.drain(30.0);
        std::cout << "Level: " << tank.level() << "\n";   // 70
    }
    ```

    De to invariantene — "aldri over kapasiteten", "aldri under null" — bor inne i `fill` og `drain`, de eneste funksjonene som kan røre `level_`. Fordi dataene er private, kan ingen kode utenfra bryte de reglene. `level()` er `const` fordi det å rapportere nivået ikke endrer tanken. Konstruktøren med ett argument er `explicit` slik at en `int` aldri i det stille blir til en `WaterTank`.

    </div>

---

## 2. Ved verdi, ved referanse, ved const-referanse {#2-by-value-by-reference-by-const-reference}

*Øver på: [Verdier, referanser og pekere](types_refs_ptrs.md)*

Skriv tre funksjoner som hver tar en `std::vector<double>`:

- `tryToScale(data, factor)` tar vektoren **ved verdi** og multipliserer hvert element med `factor`;
- `scale(data, factor)` gjør det samme, men tar vektoren **ved referanse** (`&`);
- `sum(data)` tar vektoren **ved `const`-referanse** og returnerer summen.

I `main`, start med `{1.0, 2.0, 3.0}`, kall `tryToScale(…, 10)` og skriv ut summen, kall så `scale(…, 10)` og skriv ut summen. Forklar for deg selv hvorfor bare én av dem endret resultatet.

> Hint: en parameter som tas ved verdi er en *kopi* — endringer i den når aldri kalleren. En `T&`-parameter *er* kallerens objekt. En `const T&`-parameter lar deg lese et stort objekt uten å kopiere det.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <vector>

    // ved verdi: jobber på en kopi, kallerens vektor røres ikke
    void tryToScale(std::vector<double> data, double factor) {
        for (double& x : data) {
            x *= factor;
        }
    }

    // ved referanse: jobber på kallerens egen vektor
    void scale(std::vector<double>& data, double factor) {
        for (double& x : data) {
            x *= factor;
        }
    }

    // ved const-referanse: leser kallerens vektor uten å kopiere den
    double sum(const std::vector<double>& data) {
        double total = 0.0;
        for (double x : data) {
            total += x;
        }
        return total;
    }

    int main() {
        std::vector<double> readings = {1.0, 2.0, 3.0};

        tryToScale(readings, 10.0);
        std::cout << "After tryToScale (by value): sum = " << sum(readings) << "\n";  // 6

        scale(readings, 10.0);
        std::cout << "After scale (by reference):  sum = " << sum(readings) << "\n";  // 60
    }
    ```

    `tryToScale` mottar en *kopi*; den skalerer den kopien og kaster den når den returnerer, så kallerens `readings` er uendret og summen er fortsatt `6`. `scale` mottar en referanse — et alias for kallerens vektor — så endringene dens består, og summen blir `60`. `sum` leser bare, så den tar `const std::vector<double>&`: det lages ingen kopi av vektoren, og `const`-en garanterer at funksjonen ikke kan endre den.

    </div>

---

## 3. En destruktør du kan se på {#3-a-destructor-you-can-watch}

*Øver på: [RAII](raii.md)*

Skriv en klasse `Task` som skriver ut `Begin <name>` fra **konstruktøren** sin og `End <name>` fra **destruktøren** sin. I `main`, konstruer en `Task` kalt `outer`; konstruer så, inne i en indre `{ }`-blokk, en som heter `inner`, og skriv ut `working`. Etter blokken, skriv ut `back in main`.

**Forutsi rekkefølgen på alle linjene før du kjører det**, og sjekk så.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>

    class Task {
    public:
        explicit Task(std::string name) : name_(name) {
            std::cout << "Begin " << name_ << "\n";
        }
        ~Task() {
            std::cout << "End " << name_ << "\n";
        }

    private:
        std::string name_;
    };

    int main() {
        Task outer("outer");
        {
            Task inner("inner");
            std::cout << "working\n";
        }   // inner går ut av skop her — destruktøren dens kjører
        std::cout << "back in main\n";
    }
    ```

    Utskriften er:

    ```
    Begin outer
    Begin inner
    working
    End inner
    back in main
    End outer
    ```

    `inner` destrueres ved den avsluttende `}` i den indre blokken, *før* `back in main` skrives ut — du skrev aldri noe kall for å destruere den. `outer` destrueres sist, ved slutten av `main`. Objekter destrueres i motsatt rekkefølge av konstruksjonen, hvert av dem nøyaktig når skopet dets avsluttes. Den automatiske, garanterte oppryddingen er hele poenget med RAII.

    </div>

---

## 4. Lær en strøm å skrive ut typen din {#4-teach-a-stream-to-print-your-type}

*Øver på: [IO og strømmer](io_streams.md)*

Definer en `struct Point` med `int`-medlemmene `x` og `y`. Overlast `operator<<` slik at `std::cout << p` skriver ut et punkt som `(x, y)`. Skriv så ut to punkter, for eksempel `(3, 4)` og `(-1, 7)`.

> Hint: signaturen er `std::ostream& operator<<(std::ostream& os, const Point& p)`. Skriv inn i `os`, og deretter `return os;` slik at `<<`-kallene kan kjedes.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    struct Point {        // en struct er en klasse med offentlige medlemmer som standard
        int x;
        int y;
    };

    std::ostream& operator<<(std::ostream& os, const Point& p) {
        os << "(" << p.x << ", " << p.y << ")";
        return os;
    }

    int main() {
        Point a{3, 4};
        Point b{-1, 7};
        std::cout << "a = " << a << "\n";   // a = (3, 4)
        std::cout << "b = " << b << "\n";   // b = (-1, 7)
    }
    ```

    Overlastingen tar strømmen ved referanse som `std::ostream&` — typen til `std::cout` og fellestypen alle utdatastrømmer deler (`std::ofstream` og resten) — så den samme funksjonen skriver til konsollen eller til en fil. Den returnerer den strømmen slik at neste `<<` i kjeden har noe å skrive til; det er derfor `std::cout << "a = " << a << "\n"` fungerer fra venstre mot høyre. Å ta `const Point&` unngår kopiering og lover å ikke endre punktet.

    </div>

---

## 5. Tre måter å bygge et rektangel på {#5-three-ways-to-build-a-rectangle}

*Øver på: [Klasser](classes.md)*

Skriv en klasse `Rectangle` med en `width` og en `height`. Gi den **tre** konstruktører og én spørring:

- en standardkonstruktør, som lager et `0 × 0`-rektangel;
- en konstruktør med ett argument, `Rectangle(side)`, som lager et **kvadrat**;
- en konstruktør med to argumenter, `Rectangle(width, height)`;
- `area() const`, som returnerer `width × height`.

Merk konstruktøren med ett argument `explicit`. I `main`, bygg ett av hvert, skriv ut arealene deres, og finn ut hvorfor `Rectangle r = 4.0;` ikke ville kompilert.

> Hint: gi medlemmene standardverdier (`= 0.0`) slik at standardkonstruktøren kan være `= default`. Kompilatoren velger riktig konstruktør ut fra antallet og typen argumenter du sender.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    class Rectangle {
    public:
        Rectangle() = default;                                            // 0 x 0
        explicit Rectangle(double side) : width_(side), height_(side) {}  // et kvadrat
        Rectangle(double width, double height) : width_(width), height_(height) {}

        double area() const { return width_ * height_; }

    private:
        double width_  = 0.0;
        double height_ = 0.0;
    };

    int main() {
        Rectangle empty;            // 0 x 0
        Rectangle square(4.0);      // 4 x 4
        Rectangle rect(3.0, 5.0);   // 3 x 5
        // Rectangle bad = 4.0;      // kompileringsfeil: konstruktøren med ett argument er explicit

        std::cout << empty.area()  << "\n";   // 0
        std::cout << square.area() << "\n";   // 16
        std::cout << rect.area()   << "\n";   // 15
    }
    ```

    De tre konstruktørene deler navnet `Rectangle`; kompilatoren velger én ut fra argumentene du sender. `Rectangle() = default` ber om standardkonstruktøren som ikke gjør noe — medlemsstandardene på `0.0` blir stående. Konstruktøren med ett argument bygger et kvadrat og er `explicit`, så `Rectangle bad = 4.0;` avvises: du må skrive `Rectangle square(4.0)`, som uttrykker intensjonen. `area()` er `const` fordi det å måle et rektangel ikke endrer det.

    </div>

---

## 6. Rule of Zero i praksis {#6-the-rule-of-zero-in-action}

*Øver på: [Klasser](classes.md)*

Skriv en klasse `Recording` som lagrer en `std::string name` og en `std::vector<double> samples`. Gi den `add(sample)`, `name() const` og `count() const`. Skriv **ingen** destruktør, kopikonstruktør eller tilordningsoperator.

I `main`, lag et opptak og legg til to målinger. Lag så en **kopi** av det, legg en tredje måling til *bare kopien*, og skriv ut begge antallene. De skal være forskjellige — noe som beviser at kopien er uavhengig, selv om du ikke skrev noen kopieringskode.

> Hint: bare deklarer de to medlemmene og de tre små funksjonene. *Ikke* skriv `~Recording`, en kopikonstruktør eller `operator=` — det er hele poenget.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>
    #include <vector>

    class Recording {
    public:
        explicit Recording(const std::string& name) : name_(name) {}

        void add(double sample) { samples_.push_back(sample); }

        const std::string& name() const { return name_; }
        int count() const { return static_cast<int>(samples_.size()); }

    private:
        std::string         name_;
        std::vector<double> samples_;
    };

    int main() {
        Recording original("run-1");
        original.add(1.0);
        original.add(2.0);

        Recording copy = original;   // en kopi — likevel skrev du ingen kopikonstruktør
        copy.add(3.0);               // bare kopien får en tredje måling

        std::cout << original.name() << ": " << original.count() << "\n";  // run-1: 2
        std::cout << copy.name()     << ": " << copy.count()     << "\n";  // run-1: 3
    }
    ```

    Du skrev ingen spesielle medlemsfunksjoner, likevel produserer `Recording copy = original;` en ekte, uavhengig kopi: den tredje målingen lander bare i `copy`, og `original` rapporterer fortsatt to. Det fungerer fordi *medlemmene* gjør kopieringen — `std::string` og `std::vector` vet hver især hvordan de kopierer seg selv, så den kompilatorgenererte kopien av `Recording` kopierer rett og slett hvert medlem. Det er **Rule of Zero**: når hvert medlem forvalter sine egne ressurser, er kompilatorens standardversjoner korrekte, og du skriver ingen av de spesielle medlemmene selv.

    </div>

---

## 7. const-korrekthet {#7-const-correctness}

*Øver på: [Klasser](classes.md)*

Skriv en klasse `Thermometer` som holder en avlesning i °C, med start på `20.0`. Gi den `celsius()` (rapporterer avlesningen) og `calibrate(offset)` (forskyver avlesningen med `offset`). Skriv så en fri funksjon `void report(const Thermometer& t)` som skriver ut `t.celsius()`.

I `main`, bygg et termometer, `report` det, `calibrate(-1.5)`, og `report` det igjen. Spørsmålet du skal besvare: hvilken metode *må* være `const`, og hvorfor tvinger `report` sin `const&`-parameter det frem?

> Hint: gjennom en `const`-referanse kan du kalle **bare** `const`-medlemsfunksjoner. `report` tar `const Thermometer&`, så hver metode den kaller må være `const`. Hvilken av `celsius()` og `calibrate()` bare observerer?

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>

    class Thermometer {
    public:
        double celsius() const { return celsius_; }               // observatør → const
        void   calibrate(double offset) { celsius_ += offset; }   // mutator → ikke const

    private:
        double celsius_ = 20.0;
    };

    void report(const Thermometer& t) {      // const& → kan bare kalle const-metoder
        std::cout << t.celsius() << " C\n";  // OK: celsius() er const
        // t.calibrate(1.0);                  // ville IKKE kompilert: calibrate er ikke const
    }

    int main() {
        Thermometer t;
        report(t);            // 20 C
        t.calibrate(-1.5);
        report(t);            // 18.5 C
    }
    ```

    `report` tar argumentet sitt som `const Thermometer&` — den vanlige måten å sende et objekt du bare vil lese, uten kopi. Men en `const`-referanse kan bare kalle `const`-medlemsfunksjoner, så `celsius()` **må** være merket `const` (den bare observerer) for at `report` skal kompilere. `calibrate` endrer avlesningen, så den er med vilje *ikke* `const` — og det utkommenterte kallet inne i `report` ville vært en kompileringsfeil, som er akkurat det sikkerhetsnettet const-korrekthet gir deg. Tommelfingerregelen: merk hver observatør `const`, så blir klassen din brukbar gjennom en `const`-referanse.

    </div>

---

## 8. En peker som kan peke på ingenting {#8-a-pointer-that-may-point-to-nothing}

*Øver på: [Verdier, referanser og pekere](types_refs_ptrs.md)*

Skriv en funksjon `const int* largest(const std::vector<int>& v)` som returnerer en **peker** til det største elementet i `v` — eller `nullptr` hvis `v` er tom. I `main`, kall den på `{3, 9, 2, 7}` og skriv ut verdien den peker på, men bare hvis den returnerte pekeren ikke er null. Kall den så på en **tom** vektor og bekreft at du får `nullptr` og ikke skriver ut noe farlig.

Poenget med oppgaven: en peker kan legitimt bety "ikke noe resultat", og du må **sjekke for `nullptr` før du derefererer**.

> Hint: ta adressen til et element med `&`. Start "størst så langt" som `&v.at(0)` (men først etter å ha sjekket at vektoren ikke er tom), gå så gjennom resten og tilordne pekeren på nytt når du finner et større element. Les verdien det pekes på med `*p`, og medlemmene dens — hvis den hadde pekt på en klasse — med `p->` ([pekere til objekter](types_refs_ptrs.md#pointers-to-objects)).

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <vector>

    // returnerer en peker til det største elementet, eller nullptr hvis v er tom
    const int* largest(const std::vector<int>& v) {
        if (v.empty()) {
            return nullptr;             // ikke noe element å peke på
        }
        const int* biggest = &v.at(0);
        for (const int& x : v) {
            if (x > *biggest) {
                biggest = &x;           // pek på den nye lederen
            }
        }
        return biggest;
    }

    int main() {
        std::vector<int> readings = {3, 9, 2, 7};
        const int* p = largest(readings);
        if (p != nullptr) {                       // sjekk før du derefererer
            std::cout << "largest = " << *p << "\n";   // largest = 9
        }

        std::vector<int> empty;
        const int* q = largest(empty);
        if (q == nullptr) {
            std::cout << "empty: no largest\n";   // empty: no largest
        }
    }
    ```

    En peker kan holde `nullptr` for å bety "her er det ingenting" — noe en referanse aldri kan. Derfor returnerer `largest` en peker: adressen til et virkelig element når det finnes ett, `nullptr` når vektoren er tom. Kalleren **må** sjekke `p != nullptr` før den skriver `*p`; å dereferere en null-peker er udefinert oppførsel. Merk at pekeren er `const int*` — den peker på data som eies av kallerens vektor, og å returnere den er trygt *fordi den vektoren overlever kallet*. (Hadde `largest` i stedet returnert adressen til en lokal variabel, ville pekeren blitt hengende i det øyeblikket funksjonen returnerte — fellen fra [siden om pekere](types_refs_ptrs.md#the-big-lifetime-trap).)

    </div>
