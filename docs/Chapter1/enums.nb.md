# Enumerasjoner

Noen verdier kommer fra et lite, fast sett med navngitte valg. En motor er *idle*, *running*, *stopped* eller i *fault*. Et trafikklys er *rødt*, *gult* eller *grønt*. En kommando er *start*, *stop* eller *reset*.

Du *kunne* lagret disse som enkle `int`-er — `0` for idle, `1` for running, og så videre — men da er det ingenting som hindrer deg i å skrive `state = 99`, og hver leser må huske hva `1` skal bety. En **enumerasjon** er en type hvis verdier er et fast sett med navn du velger. Den gjør valgene eksplisitte, lesbare og kontrollerbare av kompilatoren.

---

## `enum class` — den du bør bruke

Definer en scoped enumerasjon (med eget skop) med `enum class`:

```cpp
enum class MotorState {
    Idle,
    Running,
    Stopped,
    Fault
};
```

`MotorState` er nå en type, akkurat som `int` eller `bool`, og de eneste verdiene den har er de fire navnene du listet opp. Du skriver en verdi ved å kvalifisere den med typenavnet:

```cpp
MotorState state = MotorState::Idle;

state = MotorState::Running;

if (state == MotorState::Running) {
    // ...
}
```

Prefikset `MotorState::` er påkrevd. Det er litt ekstra skriving, men det betyr at `Running` hører til `MotorState` og ikke kan kollidere med en `Running` definert et annet sted.

---

## Å switche på en enum

En enums naturlige partner er en [`switch`](control_statements.md): én gren per verdi.

```cpp
#include <iostream>

enum class MotorState {
    Idle,
    Running,
    Stopped,
    Fault
};

void report(MotorState state) {
    switch (state) {
        case MotorState::Idle:    std::cout << "Motor is idle\n";    break;
        case MotorState::Running: std::cout << "Motor is running\n"; break;
        case MotorState::Stopped: std::cout << "Motor is stopped\n"; break;
        case MotorState::Fault:   std::cout << "Motor fault!\n";     break;
    }
}

int main() {
    MotorState state = MotorState::Idle;
    report(state);

    state = MotorState::Running;
    report(state);

    state = MotorState::Fault;
    report(state);
}
```

Utskrift:

```
Motor is idle
Motor is running
Motor fault!
```

Det er en reell gevinst her. Hvis du utelater `default`-tilfellet og senere legger til en femte tilstand, vil de fleste kompilatorer — med advarsler på (`-Wall`) — peke på denne `switch`-en og fortelle deg at et case ikke håndteres. Det gjør "jeg glemte å oppdatere ett sted" om til en påminnelse ved bygging, som er nettopp derfor du bør utelate `default` på en `switch` over en enum.

---

## Hvorfor `enum class` og ikke enkel `enum`

Du vil også møte den eldre formen uten eget skop — bare `enum`:

```cpp
enum MotorState { Idle, Running, Stopped, Fault };   // uten eget skop — unngå i ny kode
```

Den har to feller som `enum class` lukker:

| | enkel `enum` | `enum class` |
|---|--------------|--------------|
| **Navn** | lekker ut i det omkringliggende skopet: du skriver `Idle` bart, og det kolliderer med enhver annen `Idle` i nærheten | holder seg i skopet: alltid `MotorState::Idle` |
| **Typesikkerhet** | konverterer til `int` stille, så `int x = Running;` og `state == 1` kompilerer begge | ingen stille konvertering: å blande med `int` er en kompileringsfeil |

Den stille `int`-konverteringen er den farlige. Med en enkel `enum` kompilerer det uten innvendinger å sammenligne to urelaterte enum-er, eller å lagre et tall utenfor gyldig område. `enum class` gjør de feilene om til kompileringsfeil. **Velg `enum class` som standard.**

---

## Tallene bak navnene

Hvert navn har en heltallsverdi: `0, 1, 2, …` i deklarasjonsrekkefølge som standard. Du kan sette dem selv når tallene har betydning — statuskoder, eller verdier som må stemme med et maskinvareregister:

```cpp
enum class ErrorCode {
    Ok       = 0,
    Timeout  = 4,
    Overheat = 8
};
```

En scoped enum blir **ikke** til det heltallet av seg selv. Når du faktisk trenger tallet — for å skrive det ut, eller for å sende det til et annet system — be om det eksplisitt med [`static_cast`](operators_expressions.md):

```cpp
ErrorCode code = ErrorCode::Overheat;
int raw = static_cast<int>(code);   // 8
```

> På en mikrokontroller, der hver byte teller, kan du fastsette størrelsen på en enum ved å navngi dens underliggende type: `enum class ErrorCode : uint8_t { ... };` (typen med fast bredde kommer fra `<stdint.h>`; se [Arduino vs. Desktop C++](../arduino_vs_desktop.md)). Du vil ikke trenge dette på skrivebordsmaskinen.

---

## Å skrive ut en enum

Det finnes ingen innebygd måte å skrive ut en `enum class`. `std::cout << state` kompilerer **ikke** — ved kjøring er en enum bare et tall, og kompilatoren har ingen tekst for navnene du valgte.

Du har allerede sett én løsning: en `switch` som skriver ut en melding per verdi (`report`-funksjonen over). Når du i stedet vil ha navnet *som en streng* — for å legge i en loggmelding eller bygge opp tekst — skriv en liten `toString`:

```cpp
#include <iostream>
#include <string>

enum class MotorState {
    Idle,
    Running,
    Stopped,
    Fault
};

std::string toString(MotorState state) {
    switch (state) {
        case MotorState::Idle:    return "Idle";
        case MotorState::Running: return "Running";
        case MotorState::Stopped: return "Stopped";
        case MotorState::Fault:   return "Fault";
    }
    return "Unknown";
}

int main() {
    MotorState state = MotorState::Running;
    std::cout << "Motor state: " << toString(state) << "\n";
}
```

To ting om den funksjonen:

- Den avsluttende `return "Unknown";` er nødvendig fordi `toString` må returnere en `std::string` på *hver* sti, og kompilatoren behandler ikke de fire tilfellene som om de dekker alle muligheter — en `enum class` kan teknisk sett holde hvilken som helst verdi av sin underliggende type.
- Det er bevisst ikke noe `default`-tilfelle. Som før lar det kompilatoren advare deg hvis du legger til en femte tilstand senere og glemmer å gi den et navn her.

Å holde dette i takt med enum-en for hånd er litt tungvint — C++20 har ingen automatisk enum-til-streng — men en enkel `switch` er den pålitelige, avhengighetsfrie måten å gjøre det på.

---

## Oppsummering

- En enum er en type med et fast sett av navngitte verdier — grip etter en hver gang du ellers ville brukt "magiske" `int`-er for tilstander, moduser eller valg.
- **Foretrekk `enum class`** (scoped, med eget skop, og typesikker) framfor enkel `enum`.
- Skriv verdier som `Type::Value`, sammenlign dem med `==`, og forgren på dem med `switch`.
- Utelat `default` på en `switch` over en enum slik at kompilatoren advarer deg om verdier du glemte å håndtere.
- En `enum class` konverterer aldri til `int` av seg selv — bruk `static_cast` når du virkelig mener det.
- Det finnes ingen innebygd måte å skrive ut en enums navn — skriv en liten `toString`-`switch` for det.
