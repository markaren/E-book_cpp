# Ofte stilte spørsmål

Korte svar på spørsmålene som dukker opp oftest i et første C++-kurs. Hvert svar peker til der temaet dekkes i sin helhet, og til en lengre diskusjon på nett der det hjelper.

---

## Oppsett og verktøy

**Hvor bør jeg legge prosjektet mitt, og hvorfor har det noe å si?**
Bruk en kort, enkel sti nær rota av disken (`C:\dev\…`) — uten mellomrom, uten norske bokstaver, og ikke inni en skysynkronisert mappe. Rare stier gir uforståelige byggefeil. Se [Datamaskingrunnlag](computer_basics.md).

**Jeg kan allerede litt Python — hva er annerledes i C++?**
Mye, under overflaten: statiske typer, verdisemantikk (`b = a` *kopierer*), manuelt virkeområde og levetid, heltallsdivisjon. Se [Fra Python](python_to_cpp.md).

**Bør jeg la en KI skrive C++-en min?**
Som veileder og korrekturleser, ja; som erstatning for forståelse, nei — de tar selvsikkert feil ofte nok til at du må sjekke alt. Se [Bruke KI til koding](using_ai.md).

**Hvorfor dele kode i en header og en `.cpp`, i stedet for å `#include`-e en `.cpp`-fil?**
En header deler *deklarasjoner*; å inkludere en `.cpp` kopierer *definisjonene* dens inn i hver fil, noe som gir "multiple definition"-linkerfeil. Se [Klasser](Chapter4/classes.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/1686204/why-should-i-not-include-cpp-files-and-instead-use-a-header).)

**`#include <foo>` kontra `#include "foo"`?**
Vinkelparenteser for standard- og bibliotek-headere; hermetegn for dine egne filer. Se [Grunnstruktur](Chapter1/basic_structure.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/21593/what-is-the-difference-between-include-filename-and-include-filename).)

**Hvorfor `#ifndef`/`#define` (eller `#pragma once`) øverst i headere?**
De hindrer at en header limes inn i én fil to ganger, noe som ville gitt "redefinition"-feil. `#pragma once` er den moderne enlinjeren. Se [Lese kompilatorfeil](compiler_errors.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/1653958/why-are-ifndef-and-define-used-in-c-header-files).)

---

## Når noe går galt

**Programmet mitt vil ikke kompilere — hva betyr feilen?**
Fiks den *første* feilen først (de senere er ofte følgefeil), og start ved `fil:linje` den oppgir. Se [Lese kompilatorfeil](compiler_errors.md).

**Det kompilerer og kjører, men gjør feil ting — hva nå?**
Bruk debuggeren: sett et breakpoint, gå gjennom koden steg for steg, og følg variablene til det som *faktisk* skjer og det du *forventet* spriker. Se [Bruke en debugger](debugger.md).

**Hvorfor kjører `if (x = 5)` alltid?**
`=` *tilordner*; du mente `==`, som *sammenligner*. Skru på advarsler, så flagger kompilatoren det. Se [Operatorer og uttrykk](Chapter1/operators_expressions.md).

---

## Grunnleggende om språket

**Hvorfor gir `10 / 3` `3`, ikke `3.33`?**
Heltallsdivisjon kaster bort resten. Gjør den ene siden til en `double` (`10.0 / 3`) for et desimalresultat. Se [Operatorer og uttrykk](Chapter1/operators_expressions.md).

**`std::endl` eller `"\n"` — hvilken bør jeg bruke?**
Begge avslutter linjen; `std::endl` tømmer også strømmen (flush), som er tregere. Foretrekk `"\n"`. Se [IO og strømmer](Chapter4/io_streams.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/213907/stdendl-vs-n).)

**Trenger jeg virkelig krøllparenteser `{}` på en `if` på én linje?**
Ja — alltid krøllparenteser. Det er én ekstra linje og fjerner en hel klasse feil når noen senere legger til en setning til. Se [Kontrollstrukturer](Chapter1/control_statements.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/2125066/is-it-a-bad-practice-to-use-an-if-statement-without-curly-braces).)

**Hvorfor skulle jeg initialisere med krøllparenteser, `int x{5}`?**
Mest for sikkerhet: krøllparentes-initialisering nekter "innsnevrende" (narrowing) konverteringer som stille mister data — `int x{3.7}` vil ikke kompilere, mens `int x = 3.7;` stille kutter til `3`. Denne boka bruker vanlig `=` til daglig initialisering og griper til `{}` når det å avvise narrowing er viktig. Se [Variabler og grunntyper](Chapter1/variables.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/18222926/what-are-the-advantages-of-list-initialization-using-curly-braces).)

**Hva betyr `explicit` på en konstruktør?**
Den hindrer at konstruktøren brukes til *stille* konverteringer. En konstruktør med ett argument som `Motor(int)` lar normalt kompilatoren gjøre en løs `int` om til en `Motor` på egen hånd; `explicit` slår det av, så konverteringen skjer bare når du ber om den. Merk konstruktører med ett argument `explicit` med mindre du ønsker konverteringen. Se [Klasser](Chapter4/classes.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/121162/what-does-the-explicit-keyword-mean).)

**Hvorfor frarådes `using namespace std;`?**
Den dumper alle navn fra standardbiblioteket inn i ditt virkeområde, og inviterer til kollisjoner og tvetydighet. Skriv `std::`-prefikset i stedet. Se [C++ standardbibliotek](Chapter3/standard_library.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/1452721/why-is-using-namespace-std-considered-bad-practice).)

**Hva betyr `std::`, og hvorfor er det overalt?**
`std` er navnerommet som inneholder standardbiblioteket; `std::cout` betyr "`cout`, fra `std`". Se [C++ standardbibliotek](Chapter3/standard_library.md).

**Hvorfor er `0.1 + 0.2` ikke nøyaktig `0.3`?**
Flyttall er tilnærminger, så bittesmå feil sniker seg inn — sammenlign dem aldri med `==`. Se [Flyttall-fallgruver](floating_point.md).

**Hva er en lambda?**
En liten, navnløs funksjon skrevet rett i koden, vanligvis gitt til en algoritme. Se [Lambda-uttrykk](lambdas.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/7627098/what-is-a-lambda-expression-in-c11).)

---

## Pekere, referanser og minne

**Hva er forskjellen på en peker og en referanse?**
En referanse er et permanent alias for én variabel; en peker er en adresse som kan flyttes til et nytt sted og kan være null. Foretrekk en referanse med mindre du trenger null eller å peke et nytt sted. Se [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/57483/what-are-the-differences-between-a-pointer-variable-and-a-reference-variable).)

**Når bruker jeg `.` kontra `->`?**
`.` på et objekt; `->` gjennom en peker til ett (`p->x` er kortform for `(*p).x`). Se [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md).

**Hvorfor sende som `const&`?**
Det unngår å kopiere et stort objekt samtidig som det lover å ikke endre det — standardmåten å sende alt større enn et tall på. Se [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md).

**Hva er const-korrekthet?**
Vanen med å merke alt som ikke endrer seg som `const`: medlemsfunksjoner som bare observerer (`read() const`), parametere du bare leser (`const T&`), og lokale variabler du aldri tilordner på nytt. Det betyr noe fordi et `const`-objekt kan kalle *bare* `const`-medlemsfunksjoner — så konsekvent `const` lar deg sende dine egne typer som `const&` og lar kompilatoren fange opp utilsiktede endringer. Se [Klasser](Chapter4/classes.md) og [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md).

**Hvorfor bør jeg unngå rå `new` og `delete`?**
Det er lett å lekke dem eller frigjøre dem dobbelt. La `std::vector`, `std::string` og smartpekere eie minnet for deg (det er RAII). Se [Minnehåndtering](Chapter5/memory.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/6500313/why-should-c-programmers-minimize-use-of-new).)

**Hvilken cast bør jeg bruke?**
Unngå den gamle C-stil-casten `(int)x` — den gjør stille *hva som helst* for å tvinge gjennom konverteringen, noe som skjuler feil, og den er umulig å søke etter. Bruk en navngitt cast i stedet: nesten alltid `static_cast`; `dynamic_cast`, `const_cast` og `reinterpret_cast` er sjeldne og trenger hver sin spesifikke grunn. Se [Operatorer og uttrykk](Chapter1/operators_expressions.md). (Mer: [Stack Overflow](https://stackoverflow.com/questions/332030/when-should-static-cast-dynamic-cast-const-cast-and-reinterpret-cast-be-used).)
