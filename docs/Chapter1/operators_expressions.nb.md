# Operatorer og uttrykk

Et **uttrykk** er hva som helst som evalueres til en verdi: en literal som `42`, et variabelnavn, et funksjonskall, eller en kombinasjon av disse satt sammen med **operatorer**.

```cpp
int x = 10;
int y = 5;
int sum = x + y;       // uttrykk: x + y → 15
bool ok  = (sum > 10); // uttrykk: sum > 10 → true
```

Dette kapittelet dekker operatorene du vil bruke til daglig, og regelen som avgjør hva som skjer når flere av dem opptrer i samme uttrykk.

---

## Aritmetikk

| Operator | Betydning           | Eksempel         | Resultat |
|----------|---------------------|------------------|--------|
| `+`      | addisjon            | `5 + 3`          | `8`    |
| `-`      | subtraksjon         | `5 - 3`          | `2`    |
| `*`      | multiplikasjon      | `5 * 3`          | `15`   |
| `/`      | divisjon            | `10 / 3`         | `3` (med `int`) eller `3.333…` (med `double`) |
| `%`      | rest (modulo)       | `10 % 3`         | `1`    |

**Heltallsdivisjon avkorter.** Dette er den enkeltvis vanligste aritmetiske overraskelsen:

```cpp
int    a = 10 / 3;        // 3, brøkdelen forkastes
double b = 10 / 3;        // 3.0, ikke 3.333 — delt som int først, så konvertert
double c = 10.0 / 3;      // 3.333…, minst én operand er double
```

Hvis du vil ha et desimalresultat, må minst én operand være en `double` eller `float`.

`%` (modulo) virker bare på heltallstyper. `10 % 3` er `1`; `10.0 % 3` er en kompileringsfeil.

---

## Tilordning og sammensatt tilordning

```cpp
int total = 0;
total = total + 5;    // lang form
total += 5;           // det samme, kortere
```

De sammensatte formene `+=`, `-=`, `*=`, `/=`, `%=` virker alle på samme måte: les den gjeldende verdien, bruk operasjonen, skriv tilbake.

`++` og `--` inkrementerer eller dekrementerer med én:

```cpp
int i = 0;
++i;   // i er nå 1, foretrukket form
i++;   // virker også, foretrekk ++i når den brukes alene
```

For innebygde typer oppfører `++i` og `i++` seg likt når de brukes som en frittstående setning. De er forskjellige når de brukes inne i et større uttrykk (`++i` returnerer den nye verdien, `i++` returnerer den gamle), men å bruke `++` inne i et uttrykk du også tilordner fra er en rask måte å forvirre deg selv på. Ikke gjør det.

---

## Sammenligning

Sammenligningsoperatorer produserer en `bool`:

| Operator | Betydning          |
|----------|--------------------|
| `==`     | lik                |
| `!=`     | ulik               |
| `<`      | mindre enn         |
| `>`      | større enn         |
| `<=`     | mindre enn eller lik |
| `>=`     | større enn eller lik |

```cpp
bool adult = (age >= 18);
```

**Den vanligste feilen her:** å skrive `=` (tilordning) når du mener `==` (sammenligning).

```cpp
if (x = 5) { ... }   // tilordner 5 til x, tester så om 5 er sann, kjører alltid
if (x == 5) { ... }  // tester om x er lik 5
```

Moderne kompilatorer advarer om dette hvis du slår på advarsler. [Slå dem på](../Chapter2/cmake_intro.md#turn-on-compiler-warnings).

---

## Logiske operatorer

Brukes til å kombinere boolske uttrykk:

| Operator | Betydning |
|----------|---------|
| `&&`     | OG: sann bare hvis begge sider er sanne |
| `\|\|`   | ELLER: sann hvis én av sidene er sann   |
| `!`      | IKKE: snur sann og usann                |

```cpp
if (temperature > 80 && pressure < 5) {
    // begge betingelsene må holde
}

if (!ready) {
    // 'ready' er usann
}
```

`&&` og `||` er **kortsluttende**: de evaluerer høyresiden bare hvis det trengs. Dette er nyttig — og av og til helt nødvendig:

```cpp
if (count != 0 && total / count > threshold) {
    // trygt: total / count kjører bare når count ikke er null
}
```

Hvis `count` er null, kjører høyresiden aldri, så divisjonen hoppes over. Bytt om de to betingelsene, og programmet deler på null.

---

## Den ternære operatoren

En kompakt `if`/`else` som produserer en verdi:

```cpp
int max = (a > b) ? a : b;
```

Leses som: "hvis `a > b`, er verdien `a`; ellers er den `b`." Praktisk for korte valg. For noe mer komplekst, bruk en ekte `if`/`else`-setning; lesbarhet slår korthet.

---

## Presedens: hvorfor parenteser redder deg

Når flere operatorer opptrer i samme uttrykk, avgjør **presedens** hvilken som binder hardere.

```cpp
int x = 2 + 3 * 4;   // 14, ikke 20, * binder hardere enn +
```

Den fullstendige presedenstabellen er lang. Du trenger ikke pugge den. Du trenger å huske **to regler**, så havner du ikke i trøbbel:

1. `*`, `/`, `%` binder hardere enn `+` og `-` (vanlig matematikk).
2. **Når du er i tvil, bruk parenteser.** De koster ingenting og gjør hensikten tydelig.

Operatorer med lik presedens evalueres **fra venstre mot høyre**, noe som kan lure deg:

```cpp
int result = totalSeconds / 60 * 60;
```

Du leser kanskje det som "del på 60, gang så med 60 — tilbake der du startet." Det er det ikke: `/` kjører først, og heltallsdivisjon forkaster resten. Med `totalSeconds = 125` er `125 / 60` lik `2`, og `2 * 60` er `120` — ikke `125`. Nå en annen felle, der *grupperingen* er uklar:

```cpp
double rate = a + b / c + d;
```

Mente du `(a + b) / (c + d)` eller `a + (b/c) + d`? De gir forskjellige svar. Skriv parentesene du mener.

---

## Blanding av typer

Hvis du kombinerer verdier av forskjellige typer, konverterer C++ dem etter veldefinerte regler. To tilfeller verdt å kjenne til:

```cpp
int    i = 5;
double d = 2.0;
double result = i + d;   // i forfremmes til double; result er 7.0
```

Det er den trygge retningen: `int` til `double` mister ingenting.

```cpp
double pi = 3.14;
int    n  = pi;          // avkorter til 3, brøkdelen tapes
```

Den andre retningen (`double` til `int`) mister stille informasjon. Initialisering med krøllparenteser nekter det; vanlig tilordning gjør det ikke. Hvis du *vil* avkorte, gjør det eksplisitt med en **cast** (typekonvertering):

```cpp
int n = static_cast<int>(pi);
```

`static_cast` er den høflige måten å be om en konvertering kompilatoren ellers ville advart om. Den signaliserer også til en leser at avkortingen er tilsiktet.

> **Unngå C-stil-cast.** Du vil også se den eldre formen, `(int)pi`. Foretrekk `static_cast`: en C-stil-cast utfører stille *hvilken som helst* konvertering som trengs — inkludert utrygge som en navngitt cast ville avvist — og en naken `(int)` er nesten umulig å søke etter i koden din. `static_cast<int>(pi)` sier nøyaktig hva du mener og lar kompilatoren holde deg ærlig.

---

## Oppsummering

- Aritmetikk på heltall avkorter; bland inn en `double` for å få desimalresultater.
- `==` sammenligner, `=` tilordner. De er ikke det samme.
- `&&` og `||` kortslutter, noe som er nyttig for å gardere mot null-/ugyldige verdier.
- Presedens finnes, men parenteser er gratis. Bruk dem.
- Konverteringer fra større til mindre typer mister data stille; gjør dem eksplisitte med `static_cast`, ikke den gamle C-stilen `(int)x`.

Flyttallsaritmetikk har sine egne overraskelser: `0.1 + 0.2` er ikke nøyaktig lik `0.3`, og å sammenligne flyttall med `==` er nesten aldri det du vil. Se referansen [Flyttallsfeller](../floating_point.md) for hele listen over fallgruver.
