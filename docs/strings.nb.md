# Strenger

Tekst i C++ håndteres av `std::string`. Du vil bruke den overalt: til filnavn, sensor-ID-er, loggmeldinger, kommandotolking, feilbeskrivelser. Den oppfører seg som enhver annen verditype: kopiering lager en ekte kopi; å sende den som verdi er trygt, men potensielt dyrt.

Denne siden er en rask oppslagstabell for operasjonene du vil ty til oftest. Hele API-et finner du på [cppreference sin std::string-side](https://en.cppreference.com/w/cpp/string/basic_string).

---

## Lage strenger

```cpp
#include <string>

std::string a;                          // empty
std::string b = "hello";                // from a string literal
std::string c{"hello"};                 // same, brace form
std::string d(5, 'a');                  // "aaaaa"
std::string e = std::to_string(42);     // "42" (convert a number)
```

En naken strengliteral i kildekoden din (`"hello"`) er teknisk sett en `const char[]`, ikke en `std::string`. I de fleste sammenhenger konverteres den implisitt, men for tilfellene der den ikke gjør det, kan du tvinge det:

```cpp
auto x = std::string{"hello"};      // explicit construction
```

---

## Lengde, tomhet og tilgang

```cpp
std::string s = "robotics";

s.length();          // 8 (same as s.size())
s.empty();           // false
s[0];                 // 'r' (no bounds check)
s.at(0);              // 'r' (bounds-checked, throws if out of range)
s.front();            // 'r'
s.back();             // 's'
```

`length()` og `size()` er identiske; `std::string` bærer begge navnene av historiske grunner. Bruk den som leses best.

---

## Sammenslåing

`+` og `+=` virker slik du forventer:

```cpp
std::string greeting = "Hello, ";
std::string name     = "Alice";

std::string out = greeting + name + "!";   // "Hello, Alice!"
greeting += name;                            // greeting is now "Hello, Alice"
greeting += '!';                             // appending a single char also works
```

For å bygge opp lange strenger bit for bit er gjentatt `+=` helt greit. For å kombinere flere små biter, særlig med ikke-streng-typer blandet inn, er `std::format` det reneste alternativet:

```cpp
#include <format>

std::string message = std::format("Motor {} at {} RPM", id, rpm);
```

Plassholderne (`{}`) tar argumentene i rekkefølge og konverterer hvert av dem til tekst automatisk. Ingen strengsammenslåing, ingen `std::to_string`, ingen midlertidige strømmer.

To eldre alternativer du fremdeles vil se i eksisterende kode:

```cpp
// std::ostringstream (pre-C++20 idiom)
#include <sstream>
std::ostringstream out;
out << "Motor " << id << " at " << rpm << " RPM";
std::string message = out.str();

// Concatenation with std::to_string (works but reads poorly)
std::string message = "Motor " + std::to_string(id)
                    + " at "    + std::to_string(rpm) + " RPM";
```

Foretrekk `std::format` i ny kode.

---

## Søking

```cpp
std::string s = "hello world";

s.find("world");      // 6
s.find("xyz");        // std::string::npos, meaning "not found"

if (s.find("world") != std::string::npos) {
    // found
}

s.starts_with("hello"); // true   (C++20)
s.ends_with("world");   // true   (C++20)
```

For å teste om en streng inneholder en delstreng, bruk `find` som vist over: `s.find("o") != std::string::npos`. C++23 legger til en kortere `s.contains("o")`, men dette kurset retter seg mot C++20.

`std::string::npos` er vaktverdien alle funksjoner i `find`-familien returnerer ved feil. Sammenlign alltid eksplisitt mot den.

---

## Hente ut deler

```cpp
std::string s = "robotics";

s.substr(0, 5);   // "robot"  (from index 0, take 5 characters)
s.substr(5);      // "ics"    (from index 5 to the end)
```

---

## Konvertere til og fra tall

```cpp
int    n = std::stoi("42");        // string → int
double d = std::stod("3.14");      // string → double

std::string a = std::to_string(42);    // "42"
std::string b = std::to_string(3.14);  // "3.140000"  (note: 6 decimal places by default)
```

`std::to_string` er grei for raske konverteringer, men formateringen er fast (og for `double` skriver den alltid ut 6 desimaler, ofte flere enn du vil ha). For presis formatering, bruk `std::format`:

```cpp
std::string a = std::format("{:.2f}", 3.14159);   // "3.14"
std::string b = std::format("{:>8}", 42);         // "      42" (right-aligned)
std::string c = std::format("{:#x}", 255);        // "0xff"
```

`std::stoi` og slektningene kaster et *unntak* hvis inndataen ikke er et tall. Inntil du har møtt [Feilhåndtering](Chapter6/error_handling.md), sjekk at inndataen er gyldig først; etterpå kan du pakke kallet inn i `try`/`catch`.

---

## Sammenligning

```cpp
std::string a = "apple";
std::string b = "banana";

a == b;     // false
a != b;     // true
a < b;       // true  (lexicographic comparison)
```

Sammenligningen er tegn for tegn. Den skiller mellom store og små bokstaver (`"Apple" != "apple"`) og er språknaiv (den forstår ikke språkspesifikke sorteringsregler). Hvis du trenger sammenligning uten å skille mellom store og små bokstaver, gjør begge sider om til små bokstaver først (løkke med `std::tolower`).

---

## `std::string` og `const char*`

C-stil-"strengen" er en peker til et nullterminert tegnarray. Du vil se dem to steder:

1. **Strengliteraler** i koden din. `"hello"` er en `const char*`.
2. **Gamle C-API-er.** Mange biblioteker (særlig innebygde) tar `const char*`-parametere.

`std::string` konverterer fritt til og fra disse:

```cpp
const char* literal = "hello";
std::string s = literal;                 // implicit construction

const char* cstr = s.c_str();             // explicit conversion back
```

`s.c_str()` returnerer en peker til strengens interne buffer med en nullterminator. Den er gyldig bare så lenge `s` er i live og uendret.

---

## Vanlige fallgruver

**Endre gjennom `c_str()`.** Pekeren som `c_str()` returnerer er `const`. Ikke cast bort const-en og skriv gjennom den; resultatet er udefinert oppførsel.

**Sammenligne med en `const char*` og få tull.**

```cpp
const char* a = "hello";
const char* b = "hello";
if (a == b) { /* this compares POINTERS, not strings */ }
```

Pakk den ene siden inn i `std::string` for å tvinge fram en verdisammenligning: `if (std::string(a) == b)`.

**Iterere over byte i stedet for tegn.** `std::string` er en sekvens av `char`. Hvis strengen din inneholder UTF-8-tegn på flere byte (norske å, ø, æ for eksempel), kan `s[3]` gi deg en delvis byte, ikke et logisk tegn. For ren ASCII-tekst er dette greit; for tekst generelt, bruk et skikkelig Unicode-bevisst bibliotek.

---

## Oppsummering

- `std::string` er den dagligdagse strengtypen. Bruk den til all tekst.
- Slå sammen med `+` og `+=`; søk med `find`; del opp med `substr`.
- Konverter til og fra tall med `std::to_string` / `std::stoi` / `std::stod`.
- For å kombinere mange biter av blandede typer leses `std::format` renere enn kjedet `+=` eller `std::ostringstream`.
- `find` returnerer `std::string::npos` når ingenting blir funnet.
- `c_str()` gir deg en `const char*` for C-API-er.
