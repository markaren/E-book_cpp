# Grunnstruktur i et C++-program

Alle C++-programmer er bygd opp av den samme håndfullen med biter. Dette kapittelet går gjennom dem ved hjelp av det minste programmet som gjør noe nyttig.

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world!" << "\n";
    return 0;
}
```

---

## `#include`: hente inn kode

Linjer som starter med `#` er **preprosessordirektiver**. De håndteres før den egentlige kompileringen begynner.

`#include <iostream>` sier til kompilatoren: "før du leser resten av denne filen, lim inn innholdet i `iostream`-headeren." Den headeren er det som definerer `std::cout` og venner. Uten den vet ikke kompilatoren hva `std::cout` betyr, og koden din vil ikke kompilere.

Vinkelparenteser (`<iostream>`) brukes for standardbiblioteket og systemheadere. Hermetegn (`"my_header.hpp"`) brukes for dine egne filer. Vi ser dette skillet i kapittel 2.

---

## `main`: der kjøringen starter

<!-- no-ce -->
```cpp
int main() {
    // ...
    return 0;
}
```

Alle C++-programmer har nøyaktig én funksjon kalt `main`. Operativsystemet kaller den for å starte programmet ditt. `int` foran angir at `main` returnerer et heltall: `0` for suksess, hva som helst som ikke er null for å signalisere en feil.

Kroppen til `main`, mellom `{` og `}`, er koden som faktisk kjører.

---

## Setninger og semikolon

En **setning** er én instruksjon. I C++ slutter hver setning med et semikolon:

```cpp
int quantity = 10;
double price = 5.40;
double sum = price * quantity;
std::cout << "Total: " << sum << "\n";
```

Å glemme et semikolon er den aller vanligste feilen en nybegynner gjør. Kompilatorfeilen peker som regel på linjen *etter* det manglende semikolonet, noe som er forvirrende første gang. Sjekk alltid linjen over også.

Semikolon avslutter også klassedefinisjoner:

```cpp
class Motor {
    // ...
}; // <-- dette semikolonet er påkrevd
```

---

## Blokker og skop

En **blokk** er kode pakket inn i krøllparenteser `{ ... }`. Blokker grupperer setninger sammen og definerer **skop**: området av koden der en variabel finnes.

```cpp
#include <iostream>

int main() {
    int x = 5;

    {
        int y = 10;
        std::cout << x << " " << y << "\n"; // begge synlige
    }

    // y finnes ikke lenger her
    std::cout << x << "\n"; // x finnes fortsatt
}
```

To regler dekker nesten alle tilfellene du vil møte:

1. En variabel deklarert i en blokk ødelegges når kjøringen forlater den blokken.
2. En indre blokk kan se variabler fra den ytre blokken, men ikke omvendt.

Hvis en indre blokk deklarerer en variabel med samme navn som en utenfor, **skygger** den indre for den ytre: inne i den indre blokken refererer navnet til den nye variabelen. Skygging er lovlig, men sjelden det du vil ha; velg ulike navn.

---

## Kommentarer

Kommentarer er notater for menneskelige lesere; kompilatoren ignorerer dem. C++ har to former — `//` går til slutten av linjen, og `/* … */` kan spenne over flere:

```cpp
int retries = 5;          // sensoren mister ofte sin første avlesning, så prøv på nytt noen ganger

/* Håndtrykket må fullføres innen ett sekund, ellers
   behandler styreenheten enheten som fraværende og går videre. */
int timeoutMs = 1000;
```

Legg merke til hva de kommentarene gjør: de forklarer *hvorfor* verdiene er `5` og `1000` — noe tallene alene ikke kan fortelle en fremtidig leser. **En god kommentar forklarer *hvorfor*, ikke *hva*.** Koden sier allerede hva den gjør; en som bare gjentar det — `int retries = 5;  // sett retries til 5` — tilfører ingenting. Nybegynnerkode samler den typen; motstå det, og bruk kommentarer på resonnementet, avveiingen eller overraskelsen.

---

## Sette det sammen

Et komplett program som leser to tall fra brukeren og skriver ut summen deres:

<!-- no-ce -->
```cpp
#include <iostream>

int main() {
    int a;
    int b;

    std::cout << "Enter two integers separated by a space: ";
    std::cin >> a >> b;

    int sum = a + b;
    std::cout << "Sum: " << sum << "\n";

    return 0;
}
```

Du kjenner nå alle de strukturelle elementene dette programmet er bygd av: `#include`, `main`, blokker, setninger, semikolon, kommentarer. De gjenværende kapitlene i denne delen fyller inn det som går *inni* `main`: variabler, operatorer, kontrollflyt og funksjoner.

---

## En merknad om stil

To stilistiske konvensjoner verdt å ta i bruk fra dag én:

- **Rykk inn kroppen til hver blokk med fire mellomrom.** Moderne IDE-er gjør dette automatisk. Hold det konsekvent.
- **Bruk alltid krøllparenteser, selv for `if`- og `while`-kropper på én linje.** Det er én linje ekstra å skrive og fjerner en hel klasse av feil:

```cpp
// Unngå:
if (ready) doThing();

// Foretrekk:
if (ready) {
    doThing();
}
```

Den andre formen er vanskeligere å ødelegge når noen legger til en andre linje senere.
