# Introduksjon

Programmering er det å gi en datamaskin steg-for-steg-instruksjoner å følge. Du skriver stegene i et språk datamaskinen kan læres å forstå (i dette emnet, **C++**), og et verktøy kalt en **kompilator** oversetter dem til noe maskinen faktisk kan kjøre.

Denne boken er følgesvennen din i AIS1003. Den erstatter ikke øving. Det meste du lærer om programmering kommer fra å skrive kode, gjøre feil og finne ut hva som gikk galt. Kapitlene her er et oppslagsverk og et utgangspunkt; tastaturet er der det egentlige arbeidet skjer.

---

## Hva er et program?

Et program er en sekvens av operasjoner datamaskinen utfører i rekkefølge. På sitt minste:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, world!" << "\n";
    return 0;
}
```

Noen få linjer, men hver del betyr noe:

- `#include <iostream>` henter inn den delen av standardbiblioteket du trenger for å skrive til skjermen.
- `int main()` angir **startpunktet**. Alle C++-programmer starter her.
- Linjen som slutter med `;` er én **setning**, én ting datamaskinen skal gjøre.
- `return 0` signaliserer til operativsystemet at programmet ble fullført uten feil.

Når du kjører dette, leser kompilatoren kildekoden, sjekker den for feil, oversetter den til instruksjoner for CPU-en din og lager en kjørbar fil. Du kjører så den filen, og teksten vises.

---

## En kort historie

Datamaskiner forstår egentlig bare én ting: **maskinkode**, lange rekker med 1-ere og 0-er som svarer til de mest grunnleggende operasjonene prosessoren kan utføre — legg sammen disse to tallene, flytt denne verdien, hopp til den instruksjonen. De første programmererne skrev disse tallene for hånd. Det fungerte, men det var tregt, uleselig og bundet til én bestemt maskin.

Historien om programmeringsspråk er historien om å klatre vekk fra de 1-erne og 0-ene mot noe et menneske kan lese og resonnere om, mens et verktøy tar seg av oversettelsen tilbake ned til maskinen.

- **Maskinkode** (1940-tallet). Rå numeriske instruksjoner. Raskt for datamaskinen, elendig for mennesket.
- **Assembly** (1950-tallet). Korte forkortelser som `ADD` og `MOV` står for tallene. Lettere å lese, men fortsatt én linje per maskininstruksjon og fortsatt bundet til én type prosessor.
- **Høynivåspråk** (fra slutten av 1950-tallet). FORTRAN, og mange etter det, lot deg skrive noe nærmere menneskelige ideer — `x = a + b` i stedet for en sekvens av registeroperasjoner. En **kompilator** oversetter hele programmet ned til maskinkode, så du kunne skrive det én gang og, i prinsippet, kjøre det på ulike maskiner.
- **C** (1972). Dennis Ritchie ved Bell Labs lagde C for å skrive operativsystemet Unix. Det var høynivå nok til å være leselig, men holdt seg samtidig nær maskinvaren, så det produserte raske, kompakte programmer. C ble et av de mest innflytelsesrike språkene som noen gang er skrevet: syntaksen er stamfaren til C++, Java, C# og JavaScript. `{ }`, `;`-ene og `int main()` du så ovenfor kommer alle fra C.

### Fra C til C++

I 1979 ønsket **Bjarne Stroustrup**, også ved Bell Labs, C-ens hastighet og lavnivåkontroll *pluss* en måte å organisere store programmer rundt **klasser** — den objektorienterte ideen, lånt fra et eldre språk kalt Simula. Han begynte med å utvide C og kalte det **"C with Classes."** I 1983 ble det omdøpt til **C++**: `++` er C-operatoren som betyr "legg til én", så navnet er en liten spøk — *én mer enn C*.

C++ ble en internasjonal standard i 1998 (**C++98**), slik at hver kompilator skulle være enig om hva språket betydde. Deretter sto det nokså stille i over et tiår.

Vendepunktet var **C++11**. Det moderniserte språket så grundig at folk nå snakker om "gammel C++" og **"moderne C++"** nærmest som forskjellige språk. Moderne C++ la til funksjoner som gjør språket tryggere og langt mindre tungvint å skrive — du vil møte dem gjennom hele denne boken. Siden C++11 har en ny standard kommet omtrent hvert tredje år:

| Standard      | År          | Merknad                        |
|---------------|-------------|--------------------------------|
| C++98 / C++03 | 1998 / 2003 | Den første standardiserte C++. |
| **C++11**     | 2011        | Spranget til "moderne C++".    |
| C++14 / C++17 | 2014 / 2017 | Jevne forbedringer.            |
| **C++20**     | 2020        | Det dette emnet underviser i.  |
| C++23         | 2023        | Den nåværende nyeste.          |

Du trenger ikke å pugge dette. Lærdommen er enkel: **C++ er gammelt nok til å kjøre nesten alt, og moderne C++ er nytt nok til å være behagelig å skrive — så lenge du holder deg til den moderne stilen denne boken lærer bort.**

---

## Hvorfor C++?

Du vil høre at C++ er et "vanskelig" språk. Det er noe sant i det: det gir deg direkte kontroll over maskinen, og med den kontrollen følger flere måter å gjøre feil på enn i for eksempel Python. Men det er det rette verktøyet for det automasjonsingeniører faktisk driver med:

- **Innebygde systemer og robotikk.** Arduino, PlatformIO, ROS, industrielle styringssystemer; nesten alt kjører kode skrevet i C++ eller C.
- **Ytelseskritisk numerisk arbeid.** Reguleringssløyfer, signalbehandling, simuleringer.
- **Spillmotorer og grafikk.** Unreal, store deler av kjøretidsmiljøet til Unity.
- **Operativsystemer og drivere.** Kode som snakker direkte med maskinvaren.

---

## Kompilert, statisk typet

To egenskaper ved C++ former hvordan du skriver det.

**Kompilert.** Kildekoden din oversettes til maskinkode *én gang*, på forhånd, av kompilatoren. Programmet kjører ikke før kompileringen lykkes. Det betyr at mange feil (skrivefeil, typefeil, manglende semikolon) fanges opp før programmet i det hele tatt kjøres. Sammenlign dette med Python, der et feilstavet navn eller en typefeil ikke oppdages før programmet faktisk kjører den linjen — så en feil på linje 200 forblir skjult helt til kjøringen kommer dit.

**Statisk typet.** Hver variabel har en fast type som du oppgir på forhånd:

```cpp
int age = 25;         // age holder heltall, for alltid
double price = 19.99; // price holder desimaltall, for alltid
```

Du kan ikke senere legge en streng i `age`. Kompilatoren håndhever dette. Statisk typing betyr mer skriving for deg, men til gjengjeld fanger kompilatoren en stor klasse av feil automatisk: du kan ikke ved et uhell sende en streng der det forventes et tall.

En kort liste over konsekvenser du vil støte på:

| Egenskap | Hva det betyr for deg |
|----------|------------------------|
| Kompilert | Du må bygge på nytt før du kan teste en endring. Les kompilatorfeil nøye. |
| Statisk typet | Du oppgir typen til hver variabel. Mismatch er feil ved kompilering, ikke krasj ved kjøring. |
| Ingen søppelsamler | Du styrer når minne frigjøres (senere kapitler dekker den moderne, smertefrie måten). |
| Udefinert oppførsel finnes | Språket har kroker der "hva som helst kan skje". Vi navngir dem etter hvert som de dukker opp. |

---

## Objektorientert programmering

OOP er måten C++ normalt skrives på. I stedet for én lang liste med instruksjoner organiserer du koden rundt **objekter**: bunter av data sammen med operasjonene som virker på dataene.

Et `Motor`-objekt kan holde gjeldende hastighet og maksimal hastighet, og tilby operasjoner som `setSpeed()`, `stop()` og `getStatus()`. Resten av programmet behandler motoren som én enhet og trenger ikke vite hvordan det indre fungerer.

Sentrale begreper du vil møte:

| Begrep | Betydning |
|--------|-----------|
| **Klasse** | Tegningen. Beskriver hvilke data et objekt holder og hva det kan gjøre. |
| **Objekt** | En faktisk instans av en klasse; en bestemt motor, sensor eller styreenhet i minnet. |
| **Medlem** | En bit data eller en funksjon som hører til en klasse. |
| **Innkapsling** | Å skjule innsiden av en klasse bak et rent grensesnitt, slik at utenforliggende kode ikke kan bryte invariantene. |
| **Arv** | Å bygge en ny klasse oppå en eksisterende. |
| **Polymorfisme** | Å behandle ulike konkrete typer gjennom et felles grensesnitt. |

Vi skal ikke skrive en klasse i dag. Kapittel 4 dekker dem ordentlig. For nå, hold disse ordene bakerst i tankene.

---

## Hvordan bruke denne boken

Les hvert kapittel, og skriv så kode. Skriv eksemplene for hånd i stedet for å kopiere; skrivefeilene du gjør er måten du lærer hva kompilatoren klager på. Når du får en feil du ikke forstår, se referansen [Lese kompilatorfeil](../compiler_errors.md), og søk så på den nøyaktige feilteksten. Nesten alle kompilatorfeil har blitt spurt om på Stack Overflow.

Hvis du har skrevet litt Python før — det har mange av dere — kartlegger [Fra Python](../python_to_cpp.md) hva som overføres og de "falske vennene" som vil snuble deg.

KI-assistenter skriver gjerne C++ for deg. Les [Bruke KI til koding](../using_ai.md) før du stoler på dem. Kortversjonen: de er utmerkede verktøy og forræderske lærere, og å bruke dem godt krever noen bestemte vaner.

Når denne boken gir en anbefaling, er det den du bør følge med mindre du har en spesifikk grunn til å la være. C++ har mange måter å gjøre de fleste ting på, og en nybegynner som prøver å lære *alle* ender opp forvirret. Lær den ene gode måten først.

Videre: [Grunnstruktur](basic_structure.md) bryter ned et komplett C++-program bit for bit. Hvis du ennå ikke har installert CLion, se [Kom i gang](../getting_started.md) først.
