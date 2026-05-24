# Rekursjon

En **rekursiv** funksjon er en som kaller seg selv. Det høres sirkulært ut, men det er bare en måte å løse et problem på ved å løse en *mindre* versjon av samme problem — om og om igjen — helt til versjonen er liten nok til å besvares direkte.

Noen problemer har naturlig denne formen: fakultetet til `n` er `n` ganger fakultetet til `n - 1`; en mappes totale størrelse er dens egne filer pluss størrelsen på hver undermappe; å gå gjennom et familietre betyr å besøke en person, så hvert av barna deres, så *deres* barn.

---

## De to delene

Enhver rekursiv funksjon trenger to ting:

- Et **grunntilfelle** — den minste versjonen, som du kan besvare *uten* å rekursere. Det er dette som stopper rekursjonen.
- Et **rekursivt tilfelle** — som gjør litt arbeid og så kaller seg selv med en *mindre* inndata, og beveger seg mot grunntilfellet.

Det klassiske eksempelet er fakultet (`5! = 5 × 4 × 3 × 2 × 1`):

```cpp
#include <iostream>

int factorial(int n) {
    if (n <= 1) {                   // grunntilfelle: stopp her
        return 1;
    }
    return n * factorial(n - 1);    // rekursivt tilfelle: en mindre n hver gang
}

int main() {
    std::cout << factorial(5) << "\n";   // 120
}
```

`factorial(5)` kan ikke svare på egen hånd, så den ber om `factorial(4)`, som ber om `factorial(3)`, og så videre ned til `factorial(1)` — som *kan* svare (grunntilfellet). Så flyter svarene tilbake oppover.

---

## Hvordan den nøstes opp

Det hjelper å spore kallene. Hvert av dem må vente på kallet det gjorde før det kan fullføre:

```
factorial(5) = 5 * factorial(4)
             = 5 * (4 * factorial(3))
             = 5 * (4 * (3 * factorial(2)))
             = 5 * (4 * (3 * (2 * factorial(1))))
             = 5 * (4 * (3 * (2 * 1)))             <- grunntilfellet nådd
             = 120
```

Datamaskinen holder styr på hvert kall som er underveis, på **kallstacken**. Du kan se dem hope seg opp og nøstes opp, én ramme om gangen, i debuggeren — se [kallstacken](debugger.md#kallstacken).

---

## Feil nummer én: ingen grunntilfelle

Hvis rekursjonen aldri når et grunntilfelle — fordi du glemte det, eller fordi inndataen faktisk ikke blir mindre — kaller funksjonen seg selv i det uendelige. Hvert kall tar litt plass på kallstacken, som er begrenset, så programmet går raskt tom for den og krasjer. Dette kalles en **stack overflow**.

```cpp
int bad(int n) {
    return n + bad(n - 1);   // ingen grunntilfelle — stopper aldri
}
```

Så når du skriver en rekursiv funksjon, sjekk to ting: at det *finnes* et grunntilfelle, og at hvert rekursivt kall beveger seg *mot* det.

---

## Rekursjon eller en løkke?

Alt du kan skrive med rekursjon kan du også skrive med en løkke, og omvendt. For ren telling og oppsamling — som fakultet — er en [løkke](Chapter1/control_statements.md) som regel klarere, og den unngår kostnaden ved kallstacken:

```cpp
int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}
```

Så når er rekursjon det bedre valget? Når *selve dataen* er nøstet — mapper inni mapper, et parse-tre, et familietre — der en løkke er klønete, men "gjør dette med meg, så med hvert av barna mine" er naturlig. For det meste av dagligdags automatiseringskode griper du til en løkke; behold rekursjon i verktøykassa for tilfellene som virkelig er treformede.

---

## Oppsummering

- En rekursiv funksjon kaller seg selv for å løse en mindre versjon av samme problem.
- Den trenger et **grunntilfelle** (som stopper den) og et **rekursivt tilfelle** (som kaller seg selv med en mindre inndata).
- Å glemme grunntilfellet — eller å ikke krympe inndataen — gir uendelig rekursjon og en **stack overflow**-krasj.
- Alt rekursivt kan skrives som en løkke; foretrekk løkka når den er like klar.
- Rekursjon skinner når dataen er naturlig nøstet eller treformet.
