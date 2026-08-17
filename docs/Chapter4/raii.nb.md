# RAII

Hvert program bruker ressurser som må leveres tilbake: minne som må frigis, filer som må lukkes, enhetstilkoblinger som må slippes. Glem å frigi én, og du har en *lekkasje*; frigi den to ganger, og du ødelegger noe. Å huske å rydde opp for hånd, på hver eneste vei gjennom koden, er nøyaktig den typen bokføring mennesker gjør feil i.

C++ sitt svar er **RAII** — *Resource Acquisition Is Initialization*, et klønete navn på en enkel idé: knytt en ressurs til levetiden til et objekt, slik at oppryddingen skjer **automatisk** når objektet går ut av skop. Det er fundamentet nesten all moderne C++ hviler på.

---

## Destruktøren {#the-destructor}

En konstruktør kjører når et objekt opprettes. Speilbildet dens, **destruktøren**, kjører automatisk når objektet destrueres — som for en lokal variabel er øyeblikket den går ut av skop. En destruktør har navnet `~` etterfulgt av klassenavnet, tar ingen argumenter, og du kaller den aldri selv; kompilatoren setter inn kallet for deg.

RAII er bare dette: **skaff ressursen i konstruktøren, frigi den i destruktøren.**

```cpp
#include <iostream>

class SensorConnection {
public:
    explicit SensorConnection(int id) : id_(id) {
        std::cout << "Opened connection to sensor " << id_ << "\n";   // skaff
    }

    ~SensorConnection() {
        std::cout << "Closed connection to sensor " << id_ << "\n";   // frigi
    }

private:
    int id_;
};

int main() {
    std::cout << "Before block\n";
    {
        SensorConnection sensor(7);
        std::cout << "Using sensor 7\n";
    }   // `sensor` går ut av skop her — destruktøren kjører automatisk
    std::cout << "After block\n";
}
```

Dette skriver ut:

```
Before block
Opened connection to sensor 7
Using sensor 7
Closed connection to sensor 7
After block
```

Legg merke til hva som *ikke* står i `main`: noe kall for å lukke tilkoblingen. Krøllparentesen `}` som avslutter den indre blokken, destruerer `sensor`, og å destruere den lukker tilkoblingen. Oppryddingen er sveiset fast til objektets levetid.

---

## Opprydding som ikke kan hoppes over {#cleanup-that-cannot-be-skipped}

Den virkelige styrken er at destruktøren kjører uansett hvordan kontrollen forlater skopet — enten blokken fullfører normalt, returnerer tidlig eller kaster et [unntak](../Chapter6/error_handling.md) midtveis:

```cpp
void useSensor() {
    SensorConnection sensor(7);

    if (somethingWrong()) {
        return;          // tilkoblingen lukkes fortsatt på veien ut
    }
    // ... normalt arbeid ...
}                        // og lukkes her på den normale veien også
```

Sammenlign dette med opprydding skrevet for hånd på slutten av en funksjon: en tidlig `return` hopper forbi den, og et kastet unntak hopper forbi den. RAII har ingen slik glipe. Når objektet først finnes, er oppryddingen garantert.

> Dette er grunnen til at du bør foretrekke et objekt som eier en ressurs, fremfor et par "åpne den / lukk den"-kall du selv må balansere. Kompilatoren glemmer aldri å kalle destruktøren; det vil du.

---

## Du bruker allerede RAII {#you-are-already-using-raii}

Du har lent deg på RAII siden kapittel 1 uten å sette navn på det. Standardtypene forvalter sine egne ressurser på denne måten:

- `std::vector` og `std::string` allokerer minne og frigir det i destruktøren sin — du har aldri kalt `free`.
- `std::ifstream` og `std::ofstream` åpner en fil og lukker den i destruktøren sin — du kaller aldri `close()` (se [IO og strømmer](io_streams.md)).

```cpp
{
    std::ofstream log("readings.txt");
    log << "started\n";
}   // filen flushes og lukkes automatisk her
```

Dette er grunnen til at du sjelden trenger å skrive en destruktør selv: det riktige grepet er nesten alltid å gripe til en standardtype som allerede forvalter ressursen, og la den gjøre jobben.

---

## RAII og minne {#raii-and-memory}

Den viktigste ressursen er minne. Å allokere det for hånd (`new`) og frigi det for hånd (`delete`) er den klassiske kilden til lekkasjer og doble frigjøringer. Neste kapittels **smartpekere** — `std::unique_ptr` og `std::shared_ptr` — er rett og slett RAII-innpakninger rundt minne: de frigir det de holder når de går ut av skop. Se [Minnehåndtering](../Chapter5/memory.md).

RAII er også grunnen til at C++ ikke trenger en søppelsamler: oppryddingen er *deterministisk* og skjer i det nøyaktige øyeblikket et objekt dør, ikke på et uforutsigbart tidspunkt senere.

Det forklarer også **Rule of Zero** fra kapittelet om [klasser](classes.md): hvis hvert datamedlem allerede er en RAII-type (en `vector`, en `string`, en smartpeker), trenger klassen din ingen egen destruktør — medlemmene rydder opp etter seg selv.

Baksiden er den sjeldnere klassen som eier en *rå* ressurs direkte — en ingen standardtype pakker inn. Den kan ikke lene seg på Rule of Zero, og gjøres vanligvis best **move-only**: du overfører ressursen i stedet for å kopiere den. [Å designe en flyttbar klasse](../Chapter5/move.md#designing-a-movable-class) (neste kapittel) viser hvordan, med nettopp denne `SensorConnection`-klassen.

---

## Oppsummering {#summary}

- RAII knytter en ressurs' levetid til et objekt: **skaff i konstruktøren, frigi i destruktøren.**
- Destruktøren kjører automatisk når objektet går ut av skop — selv ved en tidlig `return` eller et unntak — så oppryddingen kan ikke glemmes eller hoppes over.
- Du er allerede avhengig av RAII: `std::vector`, `std::string` og filstrømmene rydder alle opp etter seg selv.
- Foretrekk en standard RAII-type fremfor å skrive din egen destruktør. Smartpekere (neste kapittel) bringer RAII til rått minne.
- RAII er grunnen til at C++ forvalter ressurser trygt og deterministisk, uten søppelsamler.
