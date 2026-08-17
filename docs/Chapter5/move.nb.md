# Flyttesemantikk

Noen operasjoner i C++ handler om å overføre eierskapet til data fra ett objekt til et annet. **Flyttesemantikk**, innført i C++11, lar deg gjøre dette *uten å kopiere*, noe som ofte er dramatisk raskere.

For å se hvorfor dette betyr noe, må du først forstå hva "kopiering" faktisk koster.

---

## Hva en kopi koster {#the-cost-of-a-copy}

Ta en `std::string` som holder innholdet i en 10 MB stor loggfil:

```cpp
std::string log = readEntireFile("server.log");   // 10 MB tekst
```

Hva er *inni* en `std::string`? Tre ting:

- en peker til et heap-allokert tegn-array,
- en `size` (hvor mange tegn som er i bruk),
- en `capacity` (hvor mange tegn bufferet har plass til).

Selve strengobjektet er lite, typisk 24 eller 32 byte på en skrivebordsplattform. De 10 MB med faktisk tekst lever på heapen.

Kopier nå strengen:

```cpp
std::string copy = log;     // kopi
```

C++ må produsere en splitter ny `std::string` med en tilstand som er uavhengig av originalen. Det betyr:

1. Allokere et ferskt 10 MB stort buffer på heapen.
2. `memcpy`-e alle 10 MB fra kildebufferet til det nye.
3. Sette den nye strengens peker, størrelse og kapasitet så de stemmer.

For 10 MB er dette tregt. For en `std::vector<Motor>` som holder tusen motorer, kaller du i tillegg tusen kopikonstruktører. Når dataene som kopieres ikke trenger å bestå hos kilden, er dette arbeidet bortkastet.

---

## Hva flytting gjør i stedet {#what-move-does-instead}

En **flytting** overfører eierskapet til den underliggende ressursen, uten å kopiere den.

```cpp
std::string log = readEntireFile("server.log");
std::string copy = std::move(log);   // flytting, ikke kopi
```

Nå gjør C++ dette:

1. Kopierer de tre små feltene (peker, størrelse, kapasitet) fra `log` inn i `copy`.
2. Setter typisk `log` sin peker til `nullptr` og størrelsen og kapasiteten til null, slik at destruktøren dens ikke gjør noe skadelig. (Standarden krever bare at `log` etterlates *gyldig, men uspesifisert* — se nedenfor — så den nøyaktige resttilstanden kan variere; tom er det vanlige resultatet.)

Det er alt. Ingen 10 MB-allokering, ingen `memcpy`, ingen tusen kopikonstruktører. Tre skrivinger på størrelse med en peker, uansett hvor store dataene er.

```text
   før flyttingen

       log  ●──►  [ 10 MB tekst ]

   etter flyttingen

       log   (tom)
       copy ●──►  [ 10 MB tekst ]   ← samme buffer, ikke kopiert
```

Etter flyttingen eier `copy` de 10 MB, og `log` er i en **gyldig, men uspesifisert tilstand** (vanligvis tom). Du kan tilordne til den eller destruere den, men du bør ikke anta noe bestemt om innholdet.

---

## Når flytting skjer automatisk {#when-move-happens-automatically}

Du må svært sjelden skrive `std::move` selv. Kompilatoren setter inn flyttinger automatisk i to viktige tilfeller:

**1. Å returnere et lokalt objekt fra en funksjon.**

```cpp
std::vector<int> readSamples() {
    std::vector<int> samples;
    for (int i = 0; i < 1000; ++i) {
        samples.push_back(i);
    }
    return samples;     // flyttes (eller enda bedre, se RVO nedenfor)
}

std::vector<int> data = readSamples();   // ingen kopi, ikke noe move-kall nødvendig
```

**2. Å sende en midlertidig verdi inn i en funksjon.**

```cpp
std::vector<std::string> names;
names.push_back(std::string("Alice"));   // den midlertidige strengen flyttes inn
names.push_back("Bob");                  // samme, den midlertidige flyttes
```

Kompilatoren kan se at kildeverdien ikke vil bli brukt etterpå, så den flytter i stedet for å kopiere. I moderne C++ skjer dette som standard, og optimaliseringen på språknivå kalt **returverdioptimalisering (Return Value Optimisation, RVO)** fjerner ofte til og med flyttingen: funksjonen bygger returverdien direkte i kallerens variabel.

> **Ikke skriv `return std::move(samples);`** på en lokal variabel. Det slår av RVO og er faktisk tregere enn bare `return samples;`.

---

## Når du skriver `std::move` selv {#when-to-write-stdmove-yourself}

Mønsteret er: "jeg har en navngitt variabel, jeg er ferdig med den, og jeg vil at innholdet skal lande et annet sted uten en kopi."

```cpp
class Logger {
public:
    Logger(std::string filename)
        : filename_(std::move(filename)) {}   // flytt parameteren inn i medlemmet
private:
    std::string filename_;
};
```

Parameteren `filename` er en navngitt lokal variabel, og kompilatoren flytter den ikke automatisk for deg. Uten `std::move` blir medlemmet *kopikonstruert* fra den (en unødvendig allokering). Med `std::move` overtar medlemmet parameterens lagring.

Et annet vanlig tilfelle: å overføre eierskapet til en `unique_ptr`.

```cpp
std::unique_ptr<Motor> motor = std::make_unique<Motor>(1);
sim.installMotor(std::move(motor));
// motor er nå tom; sim eier Motor-en
```

`unique_ptr` kan ikke kopieres (kopiering ville skapt en eier nummer to), så `std::move` er den *eneste* måten å gi en videre på.

---

## Flyttekonstruktører og flyttetilordning {#move-constructors-and-move-assignment}

Når du kopierer et objekt, kaller kompilatoren **kopikonstruktøren** dets. Når du flytter ett, kaller den **flyttekonstruktøren**. For typene i standardbiblioteket (`std::string`, `std::vector`, `std::unique_ptr`, `std::map` osv.) er begge allerede implementert korrekt.

Hvis du skriver din egen klasse og følger [Rule of Zero](memory.md#the-rule-of-zero), og lar medlemmene dine håndtere seg selv, genererer kompilatoren også en korrekt flyttekonstruktør gratis. Du trenger nesten aldri å skrive en for hånd.

---

## Å designe en flyttbar klasse {#designing-a-movable-class}

!!! info "Valgfritt — for den nysgjerrige"

    Denne delen er det dypeste stoffet i boka, og du kommer sjelden til å skrive det selv: [Rule of Zero](memory.md#the-rule-of-zero) gjør det unødvendig nesten hver gang. Les den for å forstå *hvordan* en flytting fungerer under panseret, men ikke føl at du må mestre den for å bruke flyttinger. Oppgaven som bygger på den, er likeledes merket som avansert.

Rule of Zero dekker nesten alt. Men av og til eier en klasse en **rå ressurs** som ingen standardtype allerede pakker inn — et håndtak fra et C-API, en maskinvaretilkobling, en lås. Da er de kompilatorgenererte operasjonene feil, og du må skrive flytteoperasjonene selv.

Ta `SensorConnection` fra [RAII](../Chapter4/raii.md): den åpner en tilkobling i konstruktøren og lukker den i destruktøren. En tilkobling er *unik* — det finnes én fysisk forbindelse, og å kopiere objektet kan ikke duplisere den. Så riktig design er **move-only**: du kan overføre tilkoblingen ut av ett objekt og inn i et annet, men du kan ikke kopiere den. Dette er nøyaktig slik `std::unique_ptr` oppfører seg.

!!! note "Først, `&&`-syntaksen: rvalue-referanser"

    En flyttekonstruktør skrives `SensorConnection(SensorConnection&& other)`. Den doble ampersanden `&&` gjør `other` til en **rvalue-referanse** — en referanse som binder seg til *midlertidige verdier* og til verdier du har pakket inn i `std::move`, i stedet for til vanlige navngitte variabler. Les `T&&` som: "denne parameteren er noe du har lov til å stjele fra." Det er nettopp slik kompilatoren skiller en flytting fra en kopi: et argument som er midlertidig (eller pakket inn i `std::move`) matcher `T&&` og velger flyttekonstruktøren, mens en vanlig lvalue matcher kopikonstruktørens `const T&`. Så flyttekonstruktøren tar ressursen ut av `other`, i visshet om at kalleren har lovet å ikke trenge den mer.

```cpp
class SensorConnection {
public:
    explicit SensorConnection(int id) : id_(id) {
        std::cout << "Opened connection to sensor " << id_ << "\n";
    }

    ~SensorConnection() {
        if (id_ != -1) {                       // et objekt det er flyttet fra eier ingenting
            std::cout << "Closed connection to sensor " << id_ << "\n";
        }
    }

    SensorConnection(SensorConnection&& other) noexcept    // flyttekonstruktør
        : id_(other.id_) {
        other.id_ = -1;                        // etterlat kilden tom
    }

    SensorConnection& operator=(SensorConnection&& other) noexcept {   // flyttetilordning
        if (this != &other) {                  // beskytt mot `x = std::move(x)`
            if (id_ != -1) {
                std::cout << "Closed connection to sensor " << id_ << "\n";   // frigjør vår først
            }
            id_ = other.id_;                   // stjel den andres
            other.id_ = -1;                    // etterlat den tom
        }
        return *this;
    }

    SensorConnection(const SensorConnection&)            = delete;    // ingen kopiering
    SensorConnection& operator=(const SensorConnection&) = delete;

private:
    int id_ = -1;                              // -1 betyr "eier ingen tilkobling"
};
```

Fire ting gjør den korrekt:

- **En måte å representere "tom" på.** Etter å ha blitt flyttet fra må et objekt eie ingenting, slik at destruktøren dets ikke gjør noe. Her er `id_ == -1` den tilstanden, og destruktøren sjekker for den.
- **Flyttekonstruktøren stjeler.** Den tar håndtaket ut av `other` og setter deretter `other` til tom — ingen tilkobling åpnes eller lukkes, bare to heltallsskrivinger.
- **Flyttetilordningen frigjør, og stjeler så.** Den lukker tilkoblingen den selv holder før den tar den andres, og beskytter mot selvtilordning (`x = std::move(x)`).
- **Kopiering er `= delete`-et.** Det uttrykker at klassen kun skal flyttes, og gjør ethvert forsøk på å kopiere til en kompileringsfeil, i stedet for et stille, ødelagt duplikat.

**Merk flytteoperasjonene `noexcept`.** Det lover at de ikke kan kaste — sant her, siden de bare flytter et håndtak rundt. Dette betyr noe i praksis når en `std::vector` vokser og må flytte elementene sine til nytt sted. For en type som *også* kan kopieres, flytter vektoren elementene bare hvis flyttekonstruktøren er `noexcept`; ellers kopierer den dem, fordi en flytting som kaster midtveis i relokasjonen kunne etterlatt beholderen ødelagt, og kopiering bevarer den sterke unntaksgarantien (denne avveiningen gjøres av `std::move_if_noexcept`). En **move-only**-type som denne har ingen kopi å falle tilbake på, så vektoren må flytte den uansett — men å merke flyttingene `noexcept` er fortsatt den riktige vanen, og det er det som lar beholdere flytte de *kopierbare* typene dine også.

Dette er **Rule of Five**: når du først skriver en destruktør og flytteoperasjonene, slutter kompilatoren å fylle ut resten, så du må gjøre rede for alle fem — her ved å slette kopiene. ([Rule of Zero](memory.md#the-rule-of-zero) er hvordan du vanligvis unngår alt dette.)

> **Foretrekk Rule of Zero selv her.** Alt dette forsvinner hvis ressursen bor i et `std::unique_ptr`-medlem (med en egendefinert deleter for et C-API) eller en standardbeholder: de genererte flyttingene er korrekte, kopiering er slått av gratis, og du skriver *ingen* av de fem. Håndskriv operasjonene bare for en rå ressurs som ingenting annet pakker inn — og hold den innpakningen så liten du kan.

---

## En merknad om objektet det er flyttet fra {#a-note-on-the-moved-from-object}

Etter `std::move(x)` er `x` fortsatt et gyldig objekt. Du kan destruere det; du kan tilordne det en ny verdi. Men du bør **ikke** anta noe om den nåværende verdien.

```cpp
std::string a = "Hello";
std::string b = std::move(a);

std::cout << a << "\n";   // lovlig, men resultatet er uspesifisert
a = "Goodbye";            // lovlig og veldefinert
```

En enkel tommelfingerregel: behandle en variabel det er flyttet fra som om den nettopp er standardkonstruert. Enten tilordne til den eller la den gå ut av skop.

---

## Oppsummering {#summary}

- En **kopi** dupliserer de underliggende dataene; potensielt dyrt.
- En **flytting** overfører eierskapet til de underliggende dataene; billig (noen få pekerskrivinger).
- Kompilatoren setter inn flyttinger automatisk for returverdier og midlertidige verdier.
- Skriv `std::move` selv når du har en navngitt variabel med innhold du vil gi videre.
- **Ikke** `std::move` en returverdi av en lokal variabel; det slår av RVO.
- Bruk flyttinger når du overfører `unique_ptr`-er; de kan ikke kopieres.
- Eier du en **rå ressurs**? Gjør klassen **move-only** — `noexcept` flytteoperasjoner, kopiene `= delete`-et — eller pakk den inn i en `unique_ptr` og skriv ingen av dem (Rule of Zero).
- Et objekt det er flyttet fra er gyldig, men uspesifisert; tilordne til det eller destruer det.
