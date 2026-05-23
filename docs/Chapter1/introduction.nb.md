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

Fem linjer, men hver del betyr noe:

- `#include <iostream>` henter inn den delen av standardbiblioteket du trenger for å skrive til skjermen.
- `int main()` angir **startpunktet**. Alle C++-programmer starter her.
- Linjen som slutter med `;` er én **setning**, én ting datamaskinen skal gjøre.
- `return 0` signaliserer til operativsystemet at programmet ble fullført uten feil.

Når du kjører dette, leser kompilatoren kildekoden, sjekker den for feil, oversetter den til instruksjoner for CPU-en din og lager en kjørbar fil. Du kjører så den filen, og teksten vises.

---

## Hvorfor C++?

Du vil høre at C++ er et "vanskelig" språk. Det er noe sant i det: det gir deg direkte kontroll over maskinen, og med den kontrollen følger flere måter å gjøre feil på enn i for eksempel Python. Men det er det rette verktøyet for det automasjonsingeniører faktisk driver med:

- **Innebygde systemer og robotikk.** Arduino, PlatformIO, ROS, industrielle styringssystemer; nesten alt kjører kode skrevet i C++ eller C.
- **Ytelseskritisk numerisk arbeid.** Reguleringssløyfer, signalbehandling, simuleringer.
- **Spillmotorer og grafikk.** Unreal, store deler av kjøretidsmiljøet til Unity.
- **Operativsystemer og drivere.** Kode som snakker direkte med maskinvaren.

Språket har også utviklet seg mye. **Moderne C++** (C++11 og nyere) er langt vennligere enn C++ for tjue år siden. Dette emnet underviser i C++20, som er det du bør skrive i dag.

---

## Kompilert, statisk typet

To egenskaper ved C++ former hvordan du skriver det.

**Kompilert.** Kildekoden din oversettes til maskinkode *én gang*, på forhånd, av kompilatoren. Programmet kjører ikke før kompileringen lykkes. Det betyr at mange feil (skrivefeil, typefeil, manglende semikolon) fanges opp før programmet i det hele tatt kjøres. Sammenlign dette med Python, som kjører koden din linje for linje og først oppdager en skrivefeil på linje 200 når kjøringen når linje 200.

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

Vi skal ikke skrive en klasse i dag. Kapittel 3 dekker dem ordentlig. For nå, hold disse ordene bakerst i tankene.

---

## Hvordan bruke denne boken

Les hvert kapittel, og skriv så kode. Skriv eksemplene for hånd i stedet for å kopiere; skrivefeilene du gjør er måten du lærer hva kompilatoren klager på. Når du får en feil du ikke forstår, se referansen [Lese kompilatorfeil](../compiler_errors.md), og søk så på den nøyaktige feilteksten. Nesten alle kompilatorfeil har blitt spurt om på Stack Overflow.

Hvis du har skrevet litt Python før — det har mange av dere — kartlegger [Fra Python](../python_to_cpp.md) hva som overføres og de "falske vennene" som vil snuble deg.

KI-assistenter skriver gjerne C++ for deg. Les [Bruke KI til koding](../using_ai.md) før du stoler på dem. Kortversjonen: de er utmerkede verktøy og forræderske lærere, og å bruke dem godt krever noen bestemte vaner.

Når denne boken gir en anbefaling, er det den du bør følge med mindre du har en spesifikk grunn til å la være. C++ har mange måter å gjøre de fleste ting på, og en nybegynner som prøver å lære *alle* ender opp forvirret. Lær den ene gode måten først.

Videre: [Grunnstruktur](basic_structure.md) bryter ned et komplett C++-program bit for bit. Hvis du ennå ikke har installert CLion, se [Kom i gang](../getting_started.md) først.
