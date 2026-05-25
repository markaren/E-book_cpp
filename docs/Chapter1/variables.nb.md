# Variabler og grunnleggende typer

En **variabel** er en navngitt bit minne som holder en verdi. Når du skriver `int age = 25;`, forteller du kompilatoren: "sett av nok minne til å holde et heltall, kall det `age`, og lagre `25` i det."

I C++ har hver variabel en **type** som er fast gjennom hele levetiden. Du deklarerer typen på forhånd; du kan ikke senere lagre en streng i en variabel deklarert `int`. Det er dette som gjør C++ til et **statisk typet** språk.

---

## Innebygde typer

Typene du vil bruke til daglig:

| Type     | Holder                               | Typisk størrelse | Eksempelverdi |
|----------|--------------------------------------|------------------|---------------|
| `bool`   | true eller false                     | 1 byte           | `true`        |
| `char`   | ett enkelt tegn                      | 1 byte           | `'A'`         |
| `int`    | heltall                              | 4 byte           | `42`          |
| `double` | desimaltall (flyttall)               | 8 byte           | `3.14159`     |
| `float`  | desimaltall, mindre presisjon        | 4 byte           | `3.14f`       |

Foretrekk `int` for heltall og `double` for desimaltall med mindre du har en spesifikk grunn til å gjøre noe annet (`float` for minnebegrenset innebygd kode, for eksempel). Størrelsene er typiske for skrivebordsplattformer; de kan være annerledes på mikrokontrollere. For en komplett referanse, se [cppreference sin oppføring om fundamentale typer](https://en.cppreference.com/w/cpp/language/types).

Standardbiblioteket legger til noen flere typer du vil bruke hele tiden på skrivebordet. De er ikke "innebygde", men på skrivebordet er de overalt:

| Type          | Holder                      | Header        |
|---------------|-----------------------------|---------------|
| `std::string` | tekst; se [Strenger](../strings.md)  | `<string>`    |
| `std::vector` | en liste med verdier som kan endre størrelse  | `<vector>`    |

På små mikrokontrollere er disse ofte utilgjengelige; der bruker du arrays med fast størrelse og buffere i stedet (se [Arduino vs. desktop-C++](../arduino_vs_desktop.md)).

---

## Deklarere og initialisere

Du kan deklarere en variabel og tilordne den i ett steg (anbefalt) eller dele det i to:

```cpp
int quantity = 10;       // deklarer og initialiser (foretrukket)
double price{5.99};      // klammer fungerer også, og er strengere på konverteringer

int count;               // bare deklarer; `count` holder nå en søppelverdi
count = 5;               // tilordne senere
```

**Initialiser alltid variabler når du deklarerer dem.** Å lese fra en uinitialisert variabel er **udefinert oppførsel**. Programmet kan skrive ut søppel, kan krasje, kan se ut til å fungere fint og så ryke på en annen kompilator. Kompilatoren vil ikke advare deg i alle tilfeller.

```cpp
int x;                       // uinitialisert
std::cout << x * 2 << "\n";  // udefinert oppførsel; gjør aldri dette
```

To ekstra grunner til å initialisere med en gang:

- Startverdien dokumenterer hva variabelen er *til for*. `int retries = 0;` forteller leseren noe `int retries;` ikke gjør.
- Hvis du ikke har en fornuftig startverdi ennå, er det vanligvis et tegn på at variabelen bør deklareres senere, nærmere der den faktisk brukes.

### Klammeinitialisering

Du vil se to måter å initialisere på:

```cpp
int a = 10;   // kopiinitialisering
int b{10};    // klammeinitialisering (uniform)
```

Begge fungerer. Klammeinitialisering er strengere: den nekter **innsnevrende konverteringer** som stille mister informasjon.

```cpp
int    a = 3.7;   // kompilerer; trunkerer stille til 3
int    b{3.7};    // kompileringsfeil: innsnevring fra double til int
```

For numeriske typer er det opp til deg. For klassetyper (som du vil møte i kapittel 4) gjør klammeinitialisering ofte det riktige mer pålitelig.

---

## Typeinferens med `auto`

Noen ganger er typen åpenbar fra høyresiden, og å skrive den ut er bare støy:

```cpp
std::vector<int> numbers = {1, 2, 3, 4, 5};

// Uten auto:
std::vector<int>::iterator it = numbers.begin();

// Med auto finner kompilatoren ut typen fra numbers.begin():
auto it = numbers.begin();
```

(Du møter `std::vector` snart, i [Strenger og vektorer](strings_and_vectors.md); *iteratorene* dens er stoff fra [kapittel 3](../Chapter3/standard_library.md). Her gir de bare et bevisst langt typenavn, så verdien av `auto` blir åpenbar.)

`auto` lar kompilatoren utlede typen for deg. Det er ikke "dynamisk typing"; typen er fortsatt fast og sjekkes ved kompilering. Bruk `auto` når typen er omstendelig eller når den nøyaktige typen ikke betyr noe for leseren; skriv den ut når den eksplisitte typen hjelper på klarheten.

---

## Navngi variabler

Et navn kan inneholde bokstaver, sifre og understreker, og må starte med en bokstav eller understrek. Navn skiller mellom store og små bokstaver: `count` og `Count` er forskjellige variabler.

To konvensjoner brukt gjennom hele denne boken:

- Lokale variabler og funksjonsparametere: `lowerCamelCase`, som `maxSpeed`, `sensorIndex`.
- Konstanter og makroer: `UPPER_SNAKE_CASE`, som `MAX_RETRIES`.

Velg beskrivende navn. `int x` er greit for en løkketeller; `int maxAllowedTemperature` er langt bedre enn `int t` hvis det er det variabelen betyr.

---

## Konstanter

Hvis en verdi aldri skal endres etter at den er satt, marker den `const`:

```cpp
const int maxRetries = 5;
maxRetries = 10; // kompileringsfeil: kan ikke tilordne til const
```

Kompilatoren håndhever dette, noe som fanger en klasse av feil og også dokumenterer hensikt: "dette er en verdi, ikke en innstilling."

Det samme gjelder vanlige lokale variabler, ikke bare navngitte konstanter som `maxRetries`: hvis du beregner en verdi og aldri endrer den igjen, gjør den `const`. Å gripe etter `const` som standard — og droppe det bare når du virkelig trenger å tilordne på nytt — dokumenterer at verdien er avgjort og lar kompilatoren stoppe deg (eller en fremtidig redaktør) fra å overskrive den ved et uhell.

---

## Oppsummering

- Hver variabel har en type, fast ved deklarasjon.
- Initialiser alltid; uinitialiserte lesinger er udefinert oppførsel.
- Foretrekk `int` og `double` for aritmetikk. Bruk `bool` for true/false. Bruk `std::string` for tekst.
- Foretrekk `const` for alt du ikke tilordner på nytt — ikke bare navngitte konstanter.
- Velg beskrivende navn.

Skop (området der en variabel eksisterer) ble dekket i [Grunnstruktur](basic_structure.md). Kortversjonen: variabler deklarert i en blokk forsvinner når blokken slutter.
