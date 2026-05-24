# Bruke en debugger

Når programmet ditt ikke vil kompilere, [leser du kompilatorfeilen](compiler_errors.md). De vanskeligere problemene er de der programmet *bygger og kjører* — og stille gjør feil ting. Instinktet er å strø `std::cout` overalt for å se hva som skjer. En **debugger** er det bedre verktøyet: den setter det kjørende programmet ditt på pause der du ber om det, og lar deg se innenfra — inspisere hver variabel, gå gjennom én linje av gangen, og følge nøyaktig hvor virkeligheten spriker fra det du forventet.

Denne siden viser debuggeren som er innebygd i CLion. Konseptene — breakpoints, steg for steg, inspeksjon — er de samme i hver IDE og hvert språk, så ferdigheten kan overføres.

---

## Hvorfor ikke bare bruke utskrifter?

Å legge til en utskrift for å se en verdi virker:

```cpp
std::cout << "got here, total = " << total << "\n";
```

Men det er tregt: rediger, bygg på nytt, kjør, les, slett så utskriftene og gjenta. Og det viser bare verdiene du *tenkte på* å skrive ut. En debugger lar deg sette på pause én gang og inspisere *alt* i virkeområdet, uten å røre koden din.

Utskriftsdebugging er ikke feil — det er hendig for et raskt blikk, og noen ganger er det alt du har (en innebygd målplattform uten debugger tilkoblet). Men for de fleste feil på desktop er debuggeren raskere og forteller deg mer.

---

## Breakpoints: sette programmet på pause

Et **breakpoint** sier "pause her". I CLion klikker du i **gutter** — den smale margen rett til venstre for linjenumrene — ved siden av linjen du bryr deg om. En rød prikk dukker opp.

Kjør så i **debug-modus** i stedet for vanlig kjøring:

- Klikk på **bug-ikonet** (ved siden av den grønne kjørepilen), eller trykk **Shift+F9**.

Programmet kjører normalt til det når breakpointet, og **stopper** så — linjen er uthevet og har *ikke kjørt ennå*. Nå kan du se deg rundt.

---

## Se på variabler

Mens programmet er på pause, åpnes verktøyvinduet **Debug** nederst. Ruten **Variables** lister hver variabel som er i virkeområdet akkurat nå, og verdien dens. Du kan også **holde musen over en variabel** i editoren for å se verdien i et verktøytips.

Dette er kjernen i debugging: sammenlign det en variabel *faktisk* holder med det du *forventet*. Det første stedet de spriker er rett ved siden av feilen din.

---

## Gå gjennom koden steg for steg

Når programmet er på pause, fører du det videre én bit av gangen:

| Handling | Tast (CLion) | Hva den gjør |
|--------|-------------|--------------|
| **Step Over** | F8 | Kjør gjeldende linje, pause på den neste. Hvis linjen kaller en funksjon, kjør hele kallet uten å gå inn i det. |
| **Step Into** | F7 | Som Step Over, men hvis linjen kaller *din* funksjon, gå inn i den og pause på dens første linje. |
| **Step Out** | Shift+F8 | Fullfør gjeldende funksjon og pause tilbake i koden som kalte den. |
| **Resume** | F9 | Fortsett til neste breakpoint (eller programmet avsluttes). |
| **Stop** | Ctrl+F2 | Avslutt debug-økten. |

Den daglige rytmen: **Step Over** for å gå nedover en funksjon mens du følger variablene endre seg, **Step Into** når du vil se hva et kall gjør, **Step Out** når du har sett nok.

> CLions [offisielle debugging-veiledning](https://www.jetbrains.com/help/clion/debugging-code.html) har kommenterte skjermbilder av hver av disse knappene hvis du vil se nøyaktig hvor de sitter.

---

## Et gjennomgått eksempel: finne en feil

Dette programmet skal summere tre avlesninger og skrive ut `60`. Det skriver ut `30`:

```cpp
#include <iostream>
#include <vector>

int sumReadings(const std::vector<int>& readings) {
    int total = 0;
    for (int r : readings) {
        total = r;
    }
    return total;
}

int main() {
    std::vector<int> readings = {10, 20, 30};
    std::cout << "sum: " << sumReadings(readings) << "\n";  // expected 60, prints 30
}
```

Slik finner du feilen uten å gjette:

1. Klikk i gutteren på linjen `total = r;` for å sette et breakpoint, og start debugging (**Shift+F9**).
2. Programmet stopper på den linjen første gang gjennom løkken. I ruten **Variables** er `r` lik `10` og `total` lik `0`.
3. Trykk **Step Over** (F8) for å gå rundt løkken et par ganger mens du følger `total`. Den blir `10`, så `20`, så `30` — den blir **overskrevet** hver gang, ikke lagt til. Du forventet `10`, så `30`, så `60`.
4. Der er feilen: `total = r;` *erstatter* totalen. Den skal *akkumulere*:

```cpp
total += r;   // add to the running total, don't overwrite it
```

Bygg på nytt, og den skriver ut `60`. Debuggeren lot deg *se* `total` oppføre seg feil i det øyeblikket det skjedde, i stedet for å stirre på koden og prøve å forestille deg hva den gjør.

---

## Kallstacken

Når programmet er på pause, viser ruten **Frames** (*kallstacken*) kjeden av kall som førte deg hit: funksjonen du er i, den som kalte den, og så videre opp til `main`. Klikk på en hvilken som helst frame for å hoppe til den funksjonen og inspisere *dens* variabler.

Dette svarer på "hvordan kom jeg egentlig hit?" — uvurderlig når en funksjon oppfører seg feil bare når den kalles fra ett bestemt sted.

---

## Noen ting å vokse inn i

Du kommer ikke til å trenge disse på dag én, men det er verdt å vite at de finnes:

- **Betingede breakpoints.** Høyreklikk på et breakpoint og gi det en betingelse som `i == 1000`. Programmet stopper bare når betingelsen er sann — perfekt for en løkke som går galt på én bestemt iterasjon.
- **Watches.** Fest et uttrykk som `readings.size()` til Watches-ruten for å spore det mens du går steg for steg.
- **Evaluate Expression** (Alt+F8). Skriv et hvilket som helst uttrykk mens programmet er på pause og se verdien, uten å legge til kode.

Breakpoints, steg for steg, og Variables-ruten alene vil løse det store flertallet av feilene dine.

---

## Fire verktøy for "noe er galt"

Hvert passer til et ulikt øyeblikk:

| Når | Grip etter |
|------|-----------|
| Programmet vil ikke kompilere | [Les kompilatorfeilen](compiler_errors.md) |
| Det bygger, men gjør feil ting | **Debuggeren** |
| Du vil slå fast "dette kan aldri skje" og få beskjed i det øyeblikket det gjør det | [`assert`](Chapter6/error_handling.md#assertions-catching-bugs-not-handling-errors) |
| Et raskt engangsblikk, eller ingen debugger tilgjengelig (innebygd) | En `std::cout`-utskrift |

---

## Oppsummering

- En debugger setter det kjørende programmet ditt på pause så du kan inspisere det — langt bedre enn å gjette eller strø utskrifter.
- Sett et **breakpoint** (klikk i gutteren), kjør i **debug-modus** (Shift+F9), og programmet stopper der før linjen kjører.
- Les verdier i ruten **Variables** eller ved å holde musen over; det er her du oppdager feilen.
- **Step Over** (F8), **Step Into** (F7) og **Step Out** (Shift+F8) går gjennom koden én bit av gangen.
- Feilen er som regel på det første punktet der en variabels virkelige verdi spriker fra det du forventet at den skulle være.
