# Funksjoner

En **funksjon** er en navngitt kodeblokk som utfører en bestemt oppgave. Du skriver den én gang og kaller den når du trenger den oppgaven utført.

Uten funksjoner ville hvert program vært én lang liste med setninger med kopiert-og-limt logikk. Med dem bygger du navngitte biter som kan testes, gjenbrukes og resonneres om én om gangen.

---

## Anatomien til en funksjon

```cpp
int add(int a, int b) {
    return a + b;
}
```

Fire deler:

- **Returtype** (`int`): hvilken type verdi funksjonen gir tilbake. `void` betyr "ingenting".
- **Navn** (`add`): det du kaller den.
- **Parameterliste** (`(int a, int b)`): inndataene, hver med en type og et navn.
- **Kropp** (`{ return a + b; }`): koden som kjører.

Å kalle funksjonen ser slik ut:

```cpp
int result = add(5, 3);   // result er 8
```

Du sender inn **argumenter** (`5` og `3`), og de blir til **parameterne** (`a` og `b`) inne i funksjonen.

---

## Returnere en verdi

`return` avslutter funksjonen og leverer tilbake en verdi:

```cpp
int square(int x) {
    return x * x;
}
```

Hvis returtypen er `void`, returnerer funksjonen ingenting; `return;` (uten verdi) avslutter bare tidlig:

```cpp
void warn(bool overheating) {
    if (!overheating) {
        return;  // avslutt tidlig, ingenting å gjøre
    }
    std::cout << "WARNING: temperature high\n";
}
```

En funksjon som ikke er `void` må returnere en verdi på hver vei. Å glemme det er udefinert oppførsel; moderne kompilatorer vil advare deg, og du bør behandle den advarselen som en feil.

---

## Deklarasjoner vs. definisjoner

I større programmer deler du ofte en funksjon over flere filer. **Deklarasjonen** forteller kompilatoren at funksjonen finnes og hva signaturen dens er; **definisjonen** gir den faktiske koden.

```cpp
// Deklarasjon, vanligvis i en header-fil
int add(int a, int b);

// Definisjon, vanligvis i en .cpp-fil
int add(int a, int b) {
    return a + b;
}
```

For korte programmer som lever i én fil, er deklarasjonen og definisjonen den samme linjen; du bare skriver hele funksjonen og bruker den. Kapittel 2 dekker det å dele kode over flere filer ordentlig.

---

## Overlasting av funksjoner

Du kan ha flere funksjoner med samme navn så lenge de tar ulike parametere. Kompilatoren velger den rette basert på argumenttypene du sender inn.

```cpp
#include <iostream>

int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

int main() {
    int    sum1 = add(5, 3);       // kaller int-versjonen
    double sum2 = add(2.5, 3.7);   // kaller double-versjonen

    std::cout << sum1 << " " << sum2 << "\n";
}
```

Dette kalles **overlasting**. Bruk det når operasjonen begrepsmessig er den samme på tvers av typer (`add` to `int`-er, `add` to `double`-er). Ikke overlast for å bety ulike ting; velg distinkte navn for distinkte operasjoner.

---

## `main`-funksjonen

`main` er funksjonen operativsystemet kaller for å starte programmet ditt. Den er en funksjon som alle andre, med to små spesialregler:

- Den må returnere `int`. Etter konvensjon betyr `0` suksess og noe annet enn null en feil.
- Det må finnes nøyaktig én av dem.

<!-- no-ce -->
```cpp
int main() {
    // ... programmet ditt ...
    return 0;
}
```

Du kan også ta imot kommandolinjeargumenter:

<!-- no-ce -->
```cpp
int main(int argc, char* argv[]) {
    // argc = hvor mange argumenter
    // argv = selve argumentene som strenger
}
```

Du vil ikke trenge dette før du begynner å skrive ekte kommandolinjeverktøy.

---

## Å skrive gode funksjoner

Noen vaner som lønner seg umiddelbart:

- **Én jobb per funksjon.** Hvis du må bruke ordet "og" for å beskrive hva en funksjon gjør, trenger den sannsynligvis å deles opp.
- **Beskrivende navn.** `computeRpm` er bedre enn `doStuff`. Funksjonsnavnet bør la en leser hoppe over kroppen og likevel forstå hva koden din gjør.
- **Korte kropper.** Hvis en funksjon ikke får plass på én skjerm, gjør den for mye. Det finnes ingen hard regel, men hvis du må scrolle for å lese en enkelt funksjon, vurder om den kan brytes opp.
- **Unngå sideeffekter.** En funksjon som tar inndata og returnerer et resultat er lettere å teste og resonnere om enn en som stille endrer global tilstand.

---

## Globale variabler {#global-variables}

Hver variabel så langt har levd *inne i* en funksjon. Du kan også deklarere en **utenfor** alle funksjoner, øverst i filen, der hver funksjon under kan se den. Det er en **global variabel**:

```cpp
#include <iostream>

int counter = 0;        // global: synlig for hver funksjon under den

void tick()  { counter++; }    // hvilken som helst funksjon kan endre den...
void reset() { counter = 0; }  // ...fra hvor som helst

int main() {
    tick();
    tick();
    reset();
    std::cout << counter << "\n";   // for å vite hva som skrives ut, må du spore hvert kall
}
```

Det kompilerer, det kjører, og det føles praktisk. Det er også en vane verdt å bryte tidlig, fordi delt, endrbar tilstand som *hvilken som helst* funksjon kan røre, skaper problemer ute av proporsjon med bekvemmeligheten:

- **Du kan ikke si hva som endrer den.** For å vite verdien til `counter` på et tidspunkt, må du lese *hver* funksjon som kan skrive til den. Jo større programmet er, jo verre blir dette.
- **Feil avhenger av rekkefølge.** To kodebiter som begge skriver til den samme globale variabelen forstyrrer hverandre, og resultatet avhenger av hvilken som kjørte først — den vanskeligste typen feil å reprodusere.
- **Den motsetter seg testing.** En funksjon som leser en global variabel har en skjult inndata du må sette opp først; en som skriver til en global variabel etterlater en skjult utdata som lekker inn i neste test.

Kuren er resten av dette kapittelet, brukt med vilje:

- **Deklarer hver variabel i det minste skopet som trenger den** — normalt en lokal variabel inne i funksjonen som bruker den.
- **Send det en funksjon trenger som parametere, og returner resultatet** (vanen uten sideeffekter ovenfor). Da er en funksjons inndata og utdata nøyaktig parameterlisten og returverdien, uten noe skjult:

```cpp
#include <iostream>

int tick(int counter) {     // inndata inn...
    return counter + 1;     // ...resultat ut, ingenting skjult
}

int main() {
    int counter = 0;        // lever bare så lenge main trenger den
    counter = tick(counter);
    counter = tick(counter);
    std::cout << counter << "\n";   // skriver ut 2 — alt som endret den er synlig
}
```

Når flere funksjoner virkelig må dele tilstand som overlever et enkelt kall, er svaret fortsatt **ikke** en global variabel: bunt den tilstanden inne i et objekt som eier den og styrer hvordan den endres. Det er det en [klasse](../Chapter4/classes.md) er til for, og hvorfor [separasjon av ansvarsområder](../Chapter6/soc.md) betyr noe.

Ett unntak: en global **konstant** er greit. En verdi som aldri endres kan ikke forårsake noen av problemene ovenfor.

```cpp
constexpr double gravity = 9.81;   // global, men konstant — trygg og nyttig
```

> Kommer du fra Arduino? Dette er vanen du må justere mest bevisst. Arduino-skisser holder tilstand i globale variabler fordi den må overleve mellom `setup()` og `loop()`; på skrivebordet har du bedre alternativer. Se [Arduino vs. skrivebords-C++](../arduino_vs_desktop.md).

---

## Oppsummering

- En funksjon har en returtype, et navn, en parameterliste og en kropp.
- `return` produserer funksjonens utdata; `void`-funksjoner har ingen utdataverdi.
- Overlasting lar flere funksjoner dele et navn når de tar ulike argumenttyper.
- Én jobb per funksjon, beskrivende navn, hold dem korte.
- Foretrekk lokale variabler, parametere og returverdier fremfor **global tilstand**; reserver globale variabler for konstanter.

En funksjon kan også kalle *seg selv* — en teknikk kalt **rekursjon**. Se [Rekursjon](../recursion.md).
