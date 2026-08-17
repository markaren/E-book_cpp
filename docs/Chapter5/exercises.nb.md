# Oppgaver til kapittel 5

Det er to slags oppgaver på denne siden.

**Oppvarmingene** kommer først: korte programmer du skal lese, der du forutsier hva som skjer og velger et svar i nettleseren. Ikke noe prosjekt, ingen skriving. Dette kapittelet er der C++ begynner å straffe unøyaktighet — en kopi der du mente en referanse, en basisklasse der du mente en avledet — og dette er feilene som gir *plausibel*, men feil utskrift i stedet for et krasj.

Så kommer **programmene**, fra oppgave 1 og utover. **Prøv hver enkelt selv før du avslører løsningen** — du lærer langt mer av et ærlig forsøk enn av å lese et ferdig svar. Skriv koden inn i CLion og kjør den; ikke bare les den.

Når du åpner en løsning vises den **uskarp** — klikk én gang til for å avsløre den, slik at du ikke ser svaret ved et uhell.

Hver oppgave er et lite program med sin egen `main()`. Hold dem i ett prosjekt med én `add_executable`-linje per fil (se [CMake](../Chapter2/cmake_intro.md)), og velg hvilket som skal kjøres fra rullegardinmenyen ved siden av den grønne ▶-knappen.

---

## Oppvarming: forutsi utskriften {#warm-ups-predict-the-output}

Bestem deg for hva hvert program gjør **før** du svarer. Å svare låser spørsmålet og avslører forklaringen.

### W1. En verdi og en referanse {#w1-a-value-and-a-reference}

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

struct Base {
    virtual ~Base() = default;
    virtual std::string kind() const { return "base"; }
};

struct Derived : Base {
    std::string kind() const override { return "derived"; }
};

int main() {
    Derived d;

    Base  b = d;   // en kopi
    Base& r = d;   // en referanse

    std::cout << b.kind() << " " << r.kind() << "\n";
}
```

````quiz
Hva skriver dette ut?
- `derived derived`
- =`base derived`
- `derived base`
- `base base`
:::
**`base derived`.** Én linje, begge halvdeler av leksjonen.

`Base b = d;` kopierer **bare `Base`-delen** av `d` — en `Base`-variabel er akkurat stor nok for en `Base`, så `Derived`-delen slippes på gulvet. Det er **[objektavskjæring](polymorphism.md#object-slicing)**, og det som overlever er en ekte `Base`, så `b.kind()` returnerer `"base"`. Ingen advarsel: det er en fullt lovlig kopi.

`Base& r = d;` kopierer ingenting. `r` er et annet navn for `d`, som fortsatt er en hel `Derived`, så det virtuelle kallet går til `Derived::kind()`.

Det er regelen på én linje: jobb med polymorfe typer gjennom **referanser eller pekere, aldri som verdi**. I det øyeblikket du tilordner til en basis*verdi*, er det avledede borte — i stillhet, og programmet fortsetter å kjøre med plausibelt utseende utskrift.
````

### W2. En basisklasse uten virtuell destruktør {#w2-a-base-class-without-a-virtual-destructor}

<!-- no-ce -->
```cpp
#include <iostream>
#include <memory>

class Logger {
public:
    ~Logger() { std::cout << "~Logger\n"; }
    virtual void log() = 0;
};

class FileLogger : public Logger {
public:
    ~FileLogger() { std::cout << "~FileLogger\n"; }
    void log() override {}
};

int main() {
    std::unique_ptr<Logger> p = std::make_unique<FileLogger>();
    p->log();
}
```

````quiz
Hva er galt med dette programmet?
- Ingenting — `unique_ptr` destruerer alltid objektet den holder korrekt
- `Logger` kan ikke være abstrakt og ha en destruktør samtidig
- =`~Logger` er ikke `virtual`, så å destruere en `FileLogger` gjennom en `Logger`-peker er udefinert oppførsel
- `make_unique` kan ikke bygge en `FileLogger` når variabelen er en `unique_ptr<Logger>`
:::
**Destruktøren er ikke `virtual`.**

`unique_ptr`-en holder en `Logger*`. Når den går ut av skop, sletter den gjennom *den* pekeren, og fordi `~Logger` ikke er `virtual`, avgjøres kallet statisk: bare `~Logger` kjører. `~FileLogger` gjør det aldri — så alt den avledede klassen eide (en åpen fil, i en ekte logger), frigjøres aldri. Formelt er det **udefinert oppførsel**, ikke bare en lekkasje.

Kompilatoren advarer faktisk her — MSVC med:

```
warning C5205: delete of an abstract class 'Logger' that has a
non-virtual destructor results in undefined behavior
```

Løsningen er ett ord: `virtual ~Logger() = default;`. Regelen er verdt å lære seg utenat, for ingenting ved kallstedet ser galt ut: **enhver klasse med en `virtual` funksjon trenger en `virtual` destruktør.** Se [Regelen om virtuell destruktør](polymorphism.md#the-virtual-destructor-rule).
````

### W3. Å flytte en unique_ptr {#w3-moving-a-unique_ptr}

<!-- no-ce -->
```cpp
#include <iostream>
#include <memory>

class Valve {
public:
    explicit Valve(int id) : id_(id) { std::cout << "open " << id_ << "\n"; }
    ~Valve() { std::cout << "close " << id_ << "\n"; }

private:
    int id_;
};

int main() {
    auto a = std::make_unique<Valve>(1);
    auto b = std::move(a);

    std::cout << (a ? "a holds it" : "a is empty") << "\n";
    std::cout << "end of main\n";
}
```

````quiz
Hva skriver dette ut?
- `open 1`, `a holds it`, `end of main`, `close 1`
- =`open 1`, `a is empty`, `end of main`, `close 1`
- `open 1`, `a is empty`, `close 1`, `end of main`
- `open 1`, `a is empty`, `end of main`, `close 1`, `close 1`
:::
**`open 1`, `a is empty`, `end of main`, `close 1`.**

`std::move(a)` overfører eierskapet til `b` og etterlater `a` **tom** — en `unique_ptr` det er flyttet fra er garantert null, så `a ? ... : ...` tar den andre grenen. Dette er en av de få flyttet-fra-tilstandene standarden spikrer nøyaktig; for [de fleste typer er den bare "gyldig, men uspesifisert"](move.md#a-note-on-the-moved-from-object).

Ventilen lukkes **én gang**, på slutten av `main`, når `b` destrueres. Ikke to ganger — det fantes bare én `Valve`, og bare én eier av den. Og ikke tidlig — å flytte pekeren rørte ikke objektet den peker på.

Det "nøyaktig én eier, opprydding nøyaktig én gang, ingen `delete` noe sted" er hele grunnen til å bruke `unique_ptr`. Se [`std::unique_ptr`](memory.md#stdunique_ptr-the-default).
````

### W4. Å telle eiere {#w4-counting-owners}

<!-- no-ce -->
```cpp
#include <iostream>
#include <memory>

int main() {
    auto s = std::make_shared<int>(42);
    std::cout << s.use_count() << " ";

    {
        auto t = s;
        std::cout << s.use_count() << " ";
    }

    std::cout << s.use_count() << "\n";
}
```

````quiz
Hva skriver dette ut?
- `1 1 1`
- `1 2 2`
- =`1 2 1`
- `1 3 1`
:::
**`1 2 1`.**

En `shared_ptr` **kan** kopieres, og hver kopi er enda en medeier: `auto t = s;` hever tellingen til `2`. Når `t` går ut av skop ved den avsluttende krøllparentesen, senker destruktøren dens tellingen tilbake til `1`. Selve `int`-en destrueres først når tellingen når **null**, på slutten av `main`.

Det er hele forskjellen fra `unique_ptr`, som forbyr kopiering fullstendig, nettopp for at denne tellingen aldri skal trenges. Strekk deg etter `shared_ptr` bare når eierskapet genuint er delt — det er sjeldnere enn nybegynnere venter, og tellingen er ikke gratis. Se [`std::shared_ptr`](memory.md#stdshared_ptr-shared-ownership).
````

### W5. Én mal, to typer {#w5-one-template-two-types}

<!-- no-ce -->
```cpp
#include <iostream>
#include <string>

template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    std::string s = "x";
    std::cout << add(s, 5) << "\n";
}
```

````quiz
Hva skjer?
- Det skriver ut `x5`
- Det skriver ut `x`
- =Det kompilerer ikke: `T` kan ikke være både `std::string` og `int`
- Det kompilerer, og `5` konverteres til `std::string`
:::
**Det kompilerer ikke.**

`add` har **én** typeparameter brukt for **begge** argumentene, så kompilatoren må utlede én enkelt `T`. Det første argumentet sier `std::string`, det andre sier `int`, og ingen regel avgjør konflikten — utledningen feiler før noen kode i det hele tatt genereres. MSVC sier det rett ut:

```
error C2672: 'add': no matching overloaded function found
note: 'T add(T,T)': template parameter 'T' is ambiguous
note: could be 'int'
note: or       'std::string'
```

Merk hva som **ikke** skjer: ingen konvertering forsøkes. Utledning av malargumenter konverterer ikke for å få en match — den utleder fra argumentene nøyaktig slik de står, og gir opp hvis de er uenige.

Lange malfeil leses verre enn denne, men dekodes på samme måte: start på toppen, og se så etter `note:`-linjene som forklarer hvorfor hver kandidat ble forkastet. Se [Hvordan malfeil ser ut](templates.md#what-template-errors-look-like).
````

---

## 1. En ressurs som frigjør seg selv {#1-a-resource-that-frees-itself}

*Øver på: [Minnehåndtering](memory.md)*

Skriv en klasse `Valve` der konstruktøren skriver ut `Valve N opened` og destruktøren skriver ut `Valve N closed` (der `N` er en id som sendes inn). Opprett deretter, i `main`, en `std::unique_ptr<Valve>` med `std::make_unique` og flytt den inn i en *andre* `unique_ptr` med `std::move`. Skriv ut, for hver peker, om den er tom eller fortsatt holder ventilen — etter flyttingen er den første tom og den andre holder den.

Du skal se ventilen lukket **nøyaktig én gang**, automatisk, uten noen `delete` noe sted.

> Hint: `std::make_unique<Valve>(1)` gir deg pekeren; `std::move` overleverer eierskapet; test en peker for tomhet med `if (p)`. En `unique_ptr` kan ikke kopieres — bare flyttes.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <memory>

    class Valve {
    public:
        explicit Valve(int id) : id_(id) { std::cout << "Valve " << id_ << " opened\n"; }
        ~Valve() { std::cout << "Valve " << id_ << " closed\n"; }
    private:
        int id_;
    };

    int main() {
        std::unique_ptr<Valve> a = std::make_unique<Valve>(1);   // "Valve 1 opened"

        std::unique_ptr<Valve> b = std::move(a);   // eierskapet flyttes til b; a etterlates tom
        std::cout << "a is " << (a ? "holding the valve" : "empty") << "\n";  // tom
        std::cout << "b is " << (b ? "holding the valve" : "empty") << "\n";  // holder ventilen
    }   // b går ut av skop her → "Valve 1 closed" (nøyaktig én gang)
    ```

    `std::make_unique<Valve>(1)` allokerer en `Valve` på heapen og gir den til `a`; du skriver aldri `new` eller `delete`. `std::move(a)` overfører eierskapet til `b` og etterlater `a` tom — en `unique_ptr` kan ikke kopieres (det ville skapt to eiere), så flytting er den eneste måten å gi den videre på. Når `b` går ut av skop på slutten av `main`, destruerer den den ene `Valve`-en, så "closed" skrives ut nøyaktig én gang. Ingen lekkasje, ingen dobbel frigjøring, ingen manuell opprydding.

    </div>

---

## 2. Et håndtak du kan flytte, men ikke kopiere {#2-a-handle-you-can-move-but-not-copy}

*Øver på: [Flyttesemantikk](move.md)* — **avansert / valgfri**

> Denne bygger på delen [Å designe en flyttbar klasse](move.md#designing-a-movable-class), det dypeste stoffet i kapittelet. Den er her for den nysgjerrige; du kan hoppe over den uten å gå glipp av noe de senere kapitlene er avhengige av.

En datainnsamlings-`Channel` er en *unik* ressurs: det finnes én fysisk kanal, så objektet skal være **flyttbart, men ikke kopierbart**. Skriv en klasse `Channel` som skriver ut `Channel N open` i konstruktøren og `Channel N closed` i destruktøren. Gjør den kun flyttbar: skriv flyttekonstruktøren og flyttetilordningen (overfør id-en og etterlat kilden tom), `= delete` kopioperasjonene, og la destruktøren hoppe over en kanal det er flyttet fra.

I `main`, åpne kanal `1`, flytt den inn i en andre variabel, og bekreft at den lukkes nøyaktig én gang.

> Hint: bruk `-1` for å bety "eier ingenting". Destruktøren sjekker `if (id_ != -1)`; flyttekonstruktøren stjeler `other.id_` og setter den så til `-1`; flyttetilordningen frigjør det den selv holder først, stjeler så, og tømmer så kilden (og beskytter mot selvtilordning). Merk begge flytteoperasjonene `noexcept`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <utility>   // std::move

    class Channel {
    public:
        explicit Channel(int id) : id_(id) { std::cout << "Channel " << id_ << " open\n"; }

        ~Channel() {
            if (id_ != -1) { std::cout << "Channel " << id_ << " closed\n"; }
        }

        Channel(Channel&& other) noexcept : id_(other.id_) {   // flyttekonstruktør
            other.id_ = -1;
        }

        Channel& operator=(Channel&& other) noexcept {         // flyttetilordning
            if (this != &other) {
                if (id_ != -1) { std::cout << "Channel " << id_ << " closed\n"; }
                id_ = other.id_;
                other.id_ = -1;
            }
            return *this;
        }

        Channel(const Channel&)            = delete;           // ingen kopiering
        Channel& operator=(const Channel&) = delete;

    private:
        int id_ = -1;     // -1 betyr "eier ingen kanal"
    };

    int main() {
        Channel a(1);                  // "Channel 1 open"
        Channel b = std::move(a);      // eierskapet flyttes til b; a er nå tom
        // Channel c = b;              // kompileringsfeil: Channel kan ikke kopieres
    }   // b lukker kanal 1 (én gang); a er tom og lukker ingenting
    ```

    En kanal er unik, så `Channel` er **kun flyttbar**: den har flytteoperasjoner, og kopioperasjonene dens er `= delete`-et. Flyttekonstruktøren stjeler den andre kanalens id og setter kilden til den tomme tilstanden (`-1`); destruktøren sjekker for den tilstanden, så en kanal det er flyttet fra lukker ingenting. Fordi kopiering er slettet, er `Channel c = b;` en *kompileringsfeil* i stedet for en stille dobbel lukking. Flyttingene er `noexcept`; siden `Channel` er kun flyttbar, må en `std::vector<Channel>` uansett flytte den når den vokser, men `noexcept` er den riktige vanen — det er det som lar en vektor flytte *kopierbare* typer i stedet for å kopiere dem, og som bevarer beholderens unntaksgarantier. (Du skrev en destruktør og flytteoperasjonene — **Rule of Five** — så du gjorde rede for kopiene også. Du kunne unngått alt sammen ved å lagre håndtaket i en `std::unique_ptr`: **Rule of Zero**.)

    </div>

---

## 3. Ett grensesnitt, mange former {#3-one-interface-many-shapes}

*Øver på: [Polymorfisme](polymorphism.md)*

Skriv en abstrakt basisklasse `Shape` med en ren virtuell `double area() const` og en `virtual` destruktør. Avled `Circle` (fra en radius) og `Square` (fra en side), som hver `override`-er `area()`. Skriv en fri funksjon `void printArea(const Shape& s)` som skriver ut `s.area()`.

I `main`, kall `printArea` på en `Circle` og en `Square` gjennom den ene funksjonen. Lagre deretter en blanding av former i en `std::vector<std::unique_ptr<Shape>>` og skriv ut hvert areal i en løkke.

> Hint: `virtual double area() const = 0;` gjør `Shape` abstrakt; `virtual ~Shape() = default;` er essensiell. Legg til former med `std::make_unique<Circle>(2.0)`. Bruk `3.14159` for π.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <memory>
    #include <vector>

    class Shape {
    public:
        virtual ~Shape() = default;          // en polymorf basisklasse trenger en virtuell destruktør
        virtual double area() const = 0;     // ren virtuell → Shape er abstrakt
    };

    class Circle : public Shape {
    public:
        explicit Circle(double radius) : radius_(radius) {}
        double area() const override { return 3.14159 * radius_ * radius_; }
    private:
        double radius_;
    };

    class Square : public Shape {
    public:
        explicit Square(double side) : side_(side) {}
        double area() const override { return side_ * side_; }
    private:
        double side_;
    };

    void printArea(const Shape& s) {         // fungerer for enhver Shape
        std::cout << "area = " << s.area() << "\n";
    }

    int main() {
        Circle c(2.0);
        Square s(3.0);
        printArea(c);     // area = 12.566...
        printArea(s);     // area = 9

        std::vector<std::unique_ptr<Shape>> shapes;
        shapes.push_back(std::make_unique<Circle>(1.0));
        shapes.push_back(std::make_unique<Square>(5.0));
        for (const auto& shape : shapes) {
            printArea(*shape);               // area = 3.14159, deretter area = 25
        }
    }
    ```

    `Shape` er **abstrakt** — dens `area()` er ren virtuell (`= 0`), så du kan ikke opprette en naken `Shape`, bare noe som *er* en `Shape`. `Circle` og `Square` `override`-er hver sin `area()`. `printArea` tar `const Shape&` og kaller `area()`; fordi `area` er `virtual`, går kallet til den virkelige typen ved kjøring — det er polymorfisme. `std::vector<std::unique_ptr<Shape>>` er standardmåten å holde en blandet samling polymorfe objekter på: hver `unique_ptr` eier objektet sitt og frigjør det automatisk. Den `virtual` destruktøren er det som gjør det trygt — å slette en `Circle` gjennom en `Shape`-peker (som er nøyaktig det `unique_ptr`-en gjør) ville vært udefinert oppførsel uten den.

    </div>

---

## 4. En funksjon som fungerer for enhver type {#4-a-function-that-works-for-any-type}

*Øver på: [Maler](templates.md)*

Skriv en funksjonsmal `largest` som tar en `std::vector<T>` og returnerer det største elementet, for enhver type `T` som støtter `>`. I `main`, kall den på en vektor av `int`, en vektor av `double` og en vektor av `std::string`, og skriv ut hvert resultat.

Legg merke til at den *samme* funksjonen fungerer for alle tre — inkludert strenger, som sammenlignes alfabetisk.

> Hint: `template <typename T>` står over funksjonen; returtypen og parameteren bruker begge `T`. Start "størst så langt" fra det første elementet (`values.at(0)`) og gå gjennom resten. Du skriver ikke typen på kallstedet — kompilatoren utleder `T` fra argumentet.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <string>
    #include <vector>

    template <typename T>
    T largest(const std::vector<T>& values) {
        T biggest = values.at(0);            // antar minst ett element
        for (const T& v : values) {
            if (v > biggest) {
                biggest = v;
            }
        }
        return biggest;
    }

    int main() {
        std::vector<int>         ints    = {3, 9, 2, 7};
        std::vector<double>      doubles = {1.5, 0.5, 2.25};
        std::vector<std::string> words   = {"apple", "pear", "fig"};

        std::cout << largest(ints)    << "\n";   // 9
        std::cout << largest(doubles) << "\n";   // 2.25
        std::cout << largest(words)   << "\n";   // pear
    }
    ```

    `largest` er skrevet én gang, men fungerer for enhver type `T` med en `>`-operator. Kompilatoren genererer en egen versjon for hver type du faktisk bruker — `largest<int>`, `largest<double>`, `largest<std::string>` — hver like effektiv som om du hadde skrevet den for hånd. Du staver aldri ut typen på kallstedet: kompilatoren utleder `T` fra argumentet, så `largest(ints)` gir `T = int`. Det er hele poenget med en mal — skriv logikken én gang, og den gjelder for hver type som passer. (`std::string` sin `>` sammenligner alfabetisk, så `"pear"` vinner.)

    </div>

---

## 5. En sensor delt av to eiere {#5-a-sensor-shared-by-two-owners}

*Øver på: [Minnehåndtering](memory.md)*

Én `Sensor` brukes av både en `Logger` og en `Controller`; ingen av dem bør eie den alene, og den må leve til *begge* er ferdige med den. Modeller dette med `std::shared_ptr`.

Skriv en `Sensor` som skriver ut `Sensor N created` i konstruktøren og `Sensor N destroyed` i destruktøren. Skriv en `Logger` og en `Controller` som hver lagrer en `std::shared_ptr<Sensor>` (ta den som verdi i konstruktøren og `std::move` den inn i medlemmet). I `main`, lag én sensor med `std::make_shared`, skriv ut `use_count()`, gi den til en `Logger`, skriv ut tellingen igjen, gi den så til en `Controller` **inne i en indre `{ }`-blokk** og skriv ut tellingen en gang til. Etter blokken, skriv ut tellingen igjen.

Se tellingen stige til 3 og falle tilbake til 2 når `Controller`-en destrueres, og bekreft at sensoren destrueres først helt til slutt — når den *siste* eieren forsvinner.

> Hint: `use_count()` rapporterer hvor mange `shared_ptr`-er som eier objektet. Å kopiere en `shared_ptr` (som er det å gi den til en konstruktør gjør) øker tellingen; å destruere en senker den. Sensorens destruktør kjører når tellingen når null.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

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
    private:
        std::string name_;
    };

    class Logger {
    public:
        explicit Logger(std::shared_ptr<Sensor> s) : sensor_(std::move(s)) {}
    private:
        std::shared_ptr<Sensor> sensor_;
    };

    class Controller {
    public:
        explicit Controller(std::shared_ptr<Sensor> s) : sensor_(std::move(s)) {}
    private:
        std::shared_ptr<Sensor> sensor_;
    };

    int main() {
        auto sensor = std::make_shared<Sensor>("outdoor");
        std::cout << "owners: " << sensor.use_count() << "\n";   // 1

        Logger logger(sensor);
        std::cout << "owners: " << sensor.use_count() << "\n";   // 2

        {
            Controller controller(sensor);
            std::cout << "owners: " << sensor.use_count() << "\n";   // 3
        }   // controller destruert → tellingen faller tilbake til 2

        std::cout << "owners: " << sensor.use_count() << "\n";   // 2
        std::cout << "leaving main\n";
    }   // logger og sensor forsvinner → tellingen når 0 → sensoren destrueres her
    ```

    Utskriften er:

    ```
    Sensor outdoor created
    owners: 1
    owners: 2
    owners: 3
    owners: 2
    leaving main
    Sensor outdoor destroyed
    ```

    Hver `shared_ptr` som eier sensoren teller som én eier, og å kopiere en (som er det å sende den til `Logger`/`Controller` gjør) hever tellingen. I motsetning til en `unique_ptr` — som ikke kan kopieres i det hele tatt — er en `shared_ptr` *ment* å kopieres, og referansetellingen er hvordan den vet når den siste eieren er borte. `Controller`-en inne i blokken senker tellingen fra 3 tilbake til 2 når den destrueres; selve sensoren destrueres ikke før `leaving main` er skrevet ut og begge de gjenværende eierne (`logger` og `sensor`) forsvinner på slutten av `main`. Den "destruer nøyaktig når den siste eieren dør"-oppførselen er hele grunnen til at `shared_ptr` finnes.

    </div>

---

## 6. En basisklasse som trenger argumenter {#6-a-base-class-that-needs-arguments}

*Øver på: [Polymorfisme](polymorphism.md)*

Hver `Sensor` har et **navn**, fastsatt når den bygges, så basisklassen har en konstruktør `Sensor(std::string name)` og *ingen* standardkonstruktør. Avled to konkrete sensorer fra den, og la hver av dem videresende navnet opp til basisklassen.

Skriv en abstrakt `Sensor` med en `std::string name_` (satt via `Sensor(std::string name)`), en `name()`-getter, en **ren virtuell** `double read() const` og en virtuell destruktør. Avled `Thermometer` (konstruert fra et navn og en temperatur) og `Barometer` (et navn og et trykk); hver videresender navnet til `Sensor` i initialiseringslisten sin og `override`-er `read()`. Skriv `void report(const Sensor& s)` som skriver ut navnet og avlesningen, lagre en blanding i en `std::vector<std::unique_ptr<Sensor>>`, og rapporter hver enkelt.

Leksjonen: fordi `Sensor` ikke har noen standardkonstruktør, vil en avledet konstruktør som glemmer `: Sensor(...)` **ikke kompilere** — prøv det og les feilmeldingen.

> Hint: den avledede initialiseringslisten kjører basiskonstruktøren først: `Thermometer(std::string name, double c) : Sensor(std::move(name)), celsius_(c) {}`. Legg til sensorer med `std::make_unique<Thermometer>("outdoor", 21.5)`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include <iostream>
    #include <memory>
    #include <string>
    #include <vector>

    class Sensor {
    public:
        explicit Sensor(std::string name) : name_(std::move(name)) {}
        virtual ~Sensor() = default;

        virtual double read() const = 0;              // ren virtuell → Sensor er abstrakt
        const std::string& name() const { return name_; }

    private:
        std::string name_;
    };

    class Thermometer : public Sensor {
    public:
        Thermometer(std::string name, double celsius)
            : Sensor(std::move(name)),   // videresend navnet til basiskonstruktøren
              celsius_(celsius) {}
        double read() const override { return celsius_; }
    private:
        double celsius_;
    };

    class Barometer : public Sensor {
    public:
        Barometer(std::string name, double kPa)
            : Sensor(std::move(name)),
              kPa_(kPa) {}
        double read() const override { return kPa_; }
    private:
        double kPa_;
    };

    void report(const Sensor& s) {
        std::cout << s.name() << " = " << s.read() << "\n";
    }

    int main() {
        std::vector<std::unique_ptr<Sensor>> sensors;
        sensors.push_back(std::make_unique<Thermometer>("outdoor", 21.5));
        sensors.push_back(std::make_unique<Barometer>("roof", 101.3));

        for (const auto& s : sensors) {
            report(*s);        // outdoor = 21.5, deretter roof = 101.3
        }
    }
    ```

    `Sensor` har bare den ene konstruktøren, `Sensor(std::string)`, så den har **ingen standardkonstruktør**. Det betyr at hver avledet konstruktør *må* navngi `Sensor(...)` i initialiseringslisten sin for å bygge basisdelen — `Thermometer(std::string, double) : Sensor(std::move(name)), celsius_(celsius) {}`. Dropp `: Sensor(...)`, og kompilatoren nekter med en feilmelding om `Sensor::Sensor()`, standardkonstruktøren som ikke finnes. Basisdelen konstrueres alltid først, deretter de avledede medlemmene. Alt annet er ordinær polymorfisme: `read()` er ren virtuell, så `Sensor` er abstrakt; `report` tar `const Sensor&` og sender kallet til den virkelige typen ved kjøring; og `std::vector<std::unique_ptr<Sensor>>`-en holder den blandede samlingen, hvert objekt frigjort automatisk gjennom den virtuelle destruktøren.

    </div>
