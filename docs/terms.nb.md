# Vanlige begreper

Enten du er ny til programmering eller bare til C++, vil du møte mange ukjente ord. Denne siden gir en kort, enkel definisjon av dem som brukes i denne boka, med en peker til der hvert enkelt forklares i sin helhet. Den er alfabetisk — bruk søkefeltet øverst for å hoppe rett til et begrep.

| Begrep | Betydning |
|------|---------|
| **abstrakt klasse** | En klasse med minst én ren virtuell funksjon (`= 0`); den kan ikke opprettes direkte, bare arves fra. Se [Polymorfisme](Chapter5/polymorphism.md). |
| **argument** | En verdi du sender til en funksjon når du kaller den. Inni funksjonen kommer den fram som en *parameter*. Se [Funksjoner](Chapter1/functions.md). |
| **assertion** (`assert`) | En sjekk av en betingelse som alltid må være sann; hvis den er usann, avbryter programmet. Et verktøy for å fange feil, fjernet i release-bygg. Se [Feilhåndtering](Chapter6/error_handling.md). |
| **tilordning** | Å erstatte en variabels nåværende verdi med en ny, f.eks. `x = 5`. Se [Operatorer og uttrykk](Chapter1/operators_expressions.md). |
| **grunntilfelle** | Tilfellet i en rekursiv funksjon som kan besvares direkte, uten å rekursere — det er det som stopper rekursjonen. Se [Rekursjon](recursion.md). |
| **blokk** | En gruppe setninger pakket inn i krøllparenteser `{ }`. En blokk definerer et *virkeområde*. Se [Grunnstruktur](Chapter1/basic_structure.md). |
| **breakpoint** | En markør som pauser et kjørende program i debuggeren så du kan inspisere det. Se [Bruke en debugger](debugger.md). |
| **innebygd type** | En type språket tilbyr direkte: `int`, `double`, `bool`, `char`. Se [Variabler og grunntyper](Chapter1/variables.md). |
| **capture** | `[ ]`-delen av en lambda som lister hvilke omkringliggende variabler den kan bruke, ved verdi eller ved referanse. Se [Lambda-uttrykk](lambdas.md). |
| **cast** | En eksplisitt typekonvertering, f.eks. `static_cast<int>(x)`. Se [Operatorer og uttrykk](Chapter1/operators_expressions.md). |
| **klasse** | En brukerdefinert type som bunter sammen data med operasjonene som virker på dem. Se [Klasser](Chapter4/classes.md). |
| **kompilator / kompilere** | Verktøyet som oversetter kildekoden din til et kjørbart program, *før* det kjører. Se [Introduksjon](Chapter1/introduction.md). |
| **const** | Et løfte til kompilatoren om at en verdi ikke vil endre seg; kompilatoren håndhever det. Se [Variabler og grunntyper](Chapter1/variables.md). |
| **const-korrekthet** | Vanen med å merke alt som ikke endrer seg som `const` — medlemsfunksjoner som bare observerer, referanseparametere du bare leser, lokale variabler du aldri tilordner på nytt — så kompilatoren håndhever hva som kan endres. Et `const`-objekt kan kalle bare `const`-medlemsfunksjoner. Se [Klasser](Chapter4/classes.md) og [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md). |
| **konstruktør** | En spesiell medlemsfunksjon som kjører når et objekt opprettes, for å sette opp dets opprinnelige tilstand. Se [Klasser](Chapter4/classes.md). |
| **beholder** | En type fra standardbiblioteket som holder en samling verdier, som `std::vector`, `std::map` eller `std::set`. Se [Datastrukturer](Chapter3/data_structures.md). |
| **dinglende referanse / peker** | En referanse eller peker til noe som allerede er ødelagt; å bruke den er udefinert oppførsel og en vanlig årsak til krasj. Se [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md). |
| **innkapsling** | Å skjule en types indre virkemåte bak et rent grensesnitt ved å gjøre dataene dens `private`. Se [Klasser](Chapter4/classes.md). |
| **enum class** | En type med et fast sett navngitte verdier (en *scoped enumerasjon*); den moderne, typesikre varianten av enum. Se [Enumerasjoner](Chapter1/enums.md). |
| **unntak** | En måte å signalisere og håndtere feil på, ved hjelp av `throw`, `try` og `catch`. Se [Feilhåndtering](Chapter6/error_handling.md). |
| **uttrykk** | Alt som evalueres til en verdi — en literal, en variabel, et funksjonskall, eller disse satt sammen med operatorer (`i + j`). Se [Operatorer og uttrykk](Chapter1/operators_expressions.md). |
| **funksjon** | En navngitt, gjenbrukbar kodebit som utfører én oppgave. Se [Funksjoner](Chapter1/functions.md). |
| **global variabel** | En variabel deklarert utenfor alle funksjoner, synlig overalt. Delte, muterbare globale variabler gjør koden vanskelig å følge og teste; foretrekk lokale variabler, parametere og returverdier, og hold varig tilstand inne i et objekt. Globale *konstanter* er greit. Se [Funksjoner](Chapter1/functions.md#global-variables). |
| **header** | En fil (vanligvis `.hpp`) hvis deklarasjoner deles på tvers av kildefiler via `#include`. Se [Klasser](Chapter4/classes.md). |
| **IDE** | Integrert utviklingsmiljø (Integrated Development Environment) — applikasjonen du skriver, bygger, kjører og debugger kode i. Dette emnet bruker CLion. Se [Kom i gang](getting_started.md). |
| **arv** | Å bygge en ny klasse oppå en eksisterende (`class Dog : public Animal`). Se [Polymorfisme](Chapter5/polymorphism.md). |
| **initialisere** | Gi en variabel en verdi i det øyeblikket den opprettes. Gjør alltid dette. Se [Variabler og grunntyper](Chapter1/variables.md). |
| **iterator** | Et objekt som brukes til å gå gjennom elementene i en beholder. Se [C++ standardbibliotek](Chapter3/standard_library.md). |
| **lambda** | En liten, navnløs funksjon skrevet rett i koden, ofte gitt til en algoritme. Se [Lambda-uttrykk](lambdas.md). |
| **linker / linking** | Byggetrinnet som kombinerer de kompilerte delene og bibliotekene til det ferdige programmet. "Undefined reference" er en linkerfeil. Se [Lese kompilatorfeil](compiler_errors.md). |
| **LLM / KI-assistent** | En stor språkmodell (ChatGPT, Claude, …) som kan generere kode — nyttig, men selvsikkert feil ofte nok til at du må sjekke den. Se [Bruke KI til koding](using_ai.md). |
| **main** | Funksjonen operativsystemet kaller for å starte programmet ditt. Hvert program har nøyaktig én. Se [Grunnstruktur](Chapter1/basic_structure.md). |
| **medlemsfunksjon** (metode) | En operasjon definert inni en klasse og kalt på et objekt. "Metode" er et synonym. Se [Klasser](Chapter4/classes.md). |
| **medlemsinitialiseringsliste** | `: a(x), b(y)`-delen av en konstruktør som gir datamedlemmene sine verdier før kroppen kjører. Se [Klasser](Chapter4/classes.md). |
| **move** | Å overføre en ressurs fra ett objekt til et annet i stedet for å kopiere den. Se [Flyttesemantikk](Chapter5/move.md). |
| **namespace** | En navngitt region som grupperer navn for å unngå kollisjoner. Standardbiblioteket bor i navnerommet `std`. Se [C++ standardbibliotek](Chapter3/standard_library.md). |
| **NaN** | "Not a Number" — et flyttallsresultat av ugyldig matematikk (f.eks. `0.0 / 0.0`). Det sammenlignes som *usant* mot alt, til og med seg selv. Se [Flyttall-fallgruver](floating_point.md). |
| **operator** | Et symbol som `+`, `==` eller `&&` som utfører en handling inni et uttrykk. Se [Operatorer og uttrykk](Chapter1/operators_expressions.md). |
| **overlasting** | Å definere flere funksjoner med samme navn, men forskjellige parametertyper; kompilatoren velger den riktige. Se [Funksjoner](Chapter1/functions.md). |
| **parameter** | En navngitt inndata i en funksjons definisjon. Verdien som oppgis på kallstedet, er *argumentet*. Se [Funksjoner](Chapter1/functions.md). |
| **PATH** | Listen over mapper skallet leter gjennom for å finne et program du kjører ved navn. En "command not found" er ofte et PATH-problem. Se [Datamaskingrunnlag](computer_basics.md). |
| **peker** | En variabel som holder en minneadresse. Den kan være `nullptr` (peker på ingenting) og må sjekkes før bruk. Se [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md). |
| **polymorfisme** | Å behandle forskjellige avledede typer gjennom et felles basegrensesnitt, så det samme kallet kjører koden til den riktige typen. Se [Polymorfisme](Chapter5/polymorphism.md). |
| **predikat** | En funksjon (ofte en lambda) som returnerer `true` eller `false`, brukt av algoritmer som `find_if`. Se [Lambda-uttrykk](lambdas.md). |
| **RAII** | "Resource Acquisition Is Initialisation" — knytt en ressurs til et objekt så den frigjøres automatisk når objektet går ut av virkeområdet. Se [RAII](Chapter4/raii.md). |
| **rekursjon** | En funksjon som kaller seg selv for å løse en mindre versjon av det samme problemet, og stopper ved et *grunntilfelle*. Se [Rekursjon](recursion.md). |
| **referanse** | Et alias for en eksisterende variabel; den kan aldri være null og refererer aldri til noe annet når den først er satt. Se [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md). |
| **Regelen om null** (Rule of Zero) | Utform klasser hvis medlemmer styrer seg selv (beholdere, smartpekere) så du ikke trenger å skrive noen spesielle medlemsfunksjoner. Se [Klasser](Chapter4/classes.md). |
| **virkeområde** | Regionen av kode der et navn er gyldig. En variabel deklarert i en blokk forsvinner når blokken slutter. Se [Grunnstruktur](Chapter1/basic_structure.md). |
| **skall** | Programmet (PowerShell, bash, zsh, cmd) som tolker kommandoene du skriver i en terminal. Se [Datamaskingrunnlag](computer_basics.md). |
| **smartpeker** | En RAII-innpakning som eier heap-minne og frigjør det automatisk — `std::unique_ptr`, `std::shared_ptr`. Se [Minnehåndtering](Chapter5/memory.md). |
| **stack overflow** | Et krasj forårsaket av å bruke opp kallstacken, for eksempel en rekursjon uten et nåbart grunntilfelle. Se [Rekursjon](recursion.md). |
| **standardbibliotek** | Det store settet av typer og funksjoner som følger med C++, alle i navnerommet `std`. (Beholder- og algoritmedelen kalles uformelt *STL*.) Se [C++ standardbibliotek](Chapter3/standard_library.md). |
| **setning** | Én instruksjon; i C++ avsluttes den med semikolon. Se [Grunnstruktur](Chapter1/basic_structure.md). |
| **std** | Navnerommet til standardbiblioteket. `std::cout` betyr "`cout`, fra `std`". Se [C++ standardbibliotek](Chapter3/standard_library.md). |
| **template** | En mal som genererer funksjoner eller klasser for hvilken type du enn bruker, som `std::vector<T>`. Se [Maler](Chapter5/templates.md). |
| **terminal** | Et tekstvindu der du styrer datamaskinen ved å skrive kommandoer i stedet for å klikke. Se [Datamaskingrunnlag](computer_basics.md). |
| **udefinert oppførsel** | Kode språket ikke gir noen løfter om: den kan krasje, skrive ut søppel, eller virke og bryte sammen senere. Unngå den. Se [Variabler og grunntyper](Chapter1/variables.md). |
| **uinitialisert variabel** | En variabel opprettet uten en verdi. Å lese en er udefinert oppførsel og en rik kilde til feil — initialiser alltid. Se [Variabler og grunntyper](Chapter1/variables.md). |
| **variabel** | En navngitt minnebit som holder en verdi av en fast type. Se [Variabler og grunntyper](Chapter1/variables.md). |
| **vector** | Standardbibliotekets størrelsesjusterbare array, `std::vector`. Listetypen du griper til som standard. Se [C++ standardbibliotek](Chapter3/standard_library.md). |
| **virtuell funksjon** | En medlemsfunksjon en avledet klasse kan overstyre; et kall gjennom en basereferanse eller -peker kjører versjonen til det faktiske objektet. Se [Polymorfisme](Chapter5/polymorphism.md). |
