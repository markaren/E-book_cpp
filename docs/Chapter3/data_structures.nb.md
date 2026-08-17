# Datastrukturer

En **datastruktur** er en måte å organisere data på slik at operasjonene du trenger å utføre på dem, blir effektive. Valget av struktur former hvor raskt programmet ditt kjører, og hvor ren koden som bruker den, ser ut.

Dette kapittelet handler om å *velge*. Standardbiblioteket i C++ tilbyr solide, gjennomtestede implementasjoner av hver datastruktur du kommer til å trenge dette semesteret; jobben din er å plukke den rette for oppgaven. Vi skal se på hva hver enkelt er god til, og legge fra oss fristelsen til å implementere dem fra bunnen av.

---

## Den mentale modellen {#the-mental-model}

Enhver datastruktur er en avveining. Å legge til i én er raskt; å finne i en annen er raskt; å iterere i rekkefølge gjennom en tredje er raskt. Det finnes ingen "beste" datastruktur; bare den som passer operasjonene du faktisk utfører.

Spørsmålene du bør stille:

1. **Hvordan vil jeg legge til elementer?** På slutten, foran, i midten?
2. **Hvordan vil jeg finne elementer?** Etter indeks, etter nøkkel, ved å lete gjennom?
3. **Trenger jeg dem i rekkefølge?** Innsettingsrekkefølge, sortert rekkefølge, eller ingen rekkefølge?
4. **Kommer størrelsen til å endre seg?** Ved kompilering, ved kjøring, ofte, sjelden?

Svarene plukker som regel beholderen for deg.

---

## Sekvensbeholdere {#sequence-containers}

Beholdere som lagrer en lineær sekvens av verdier. [Standardbiblioteket](standard_library.md#containers-collections-of-values) viser API-et til hver av dem — hvordan du legger til, indekserer og itererer. Denne siden handler om *når du bør velge hvilken*, og kostnadene bak det valget.

### `std::vector<T>`: dynamisk array {#stdvectort-dynamic-array}

Elementene bor i **sammenhengende minne**, som i et C-array, men størrelsen kan vokse ved kjøring. Kostnadene dens er det som gjør den til standardvalget:

| Operasjon | Kostnad |
|-----------|------|
| Indekstilgang (`v[i]`) | O(1) |
| `push_back` (legge til på slutten) | O(1) amortisert |
| Sette inn / fjerne i midten | O(n), alt etter må flyttes |
| Finne etter verdi (`std::find`) | O(n) |

**Bruk vector som standard.** Grip til noe annet bare hvis bruksmønsteret ditt genuint er i konflikt med det vector er god til — mye innsetting foran, for eksempel, eller et behov for garantert O(1) fjerning i midten.

### `std::array<T, N>`: array med fast størrelse {#stdarrayt-n-fixed-size-array}

Som `std::vector`, men størrelsen er fast ved kompilering; det er ingen heap-allokering, elementene bor inne i selve objektet. **Bruk når** størrelsen er kjent og ikke kommer til å endre seg: sensorpakker med fast lengde, oppslagstabeller, matrisedimensjoner.

### `std::deque<T>`: dobbeltendet kø {#stddequet-double-ended-queue}

Som `vector`, men også rask til å legge til eller fjerne **foran** (O(1) i begge ender). Kostnaden er at elementene ikke ligger i én sammenhengende blokk, så den er litt mindre cache-vennlig enn en vector. **Bruk når** du trenger raske innsettinger i begge ender.

### `std::list<T>`: dobbeltlenket liste {#stdlistt-doubly-linked-list}

Hvert element holder en peker (adressen til et annet element; pekere er [kapittel 4](../Chapter4/types_refs_ptrs.md)) til neste og forrige element i listen. Innsettinger og slettinger hvor som helst i listen er O(1), men du mister også O(1) indekstilgang og det meste av cache-vennligheten til `vector`.

I praksis er `std::list` sjelden det rette valget. Moderne maskinvare elsker sammenhengende minne; konstantfaktor-kostnaden ved å jage pekere gjennom en lenket liste veier ofte tyngre enn den algoritmiske fordelen. **Bruk bare når** du spesifikt trenger å flytte (splice) elementer mellom lister, eller å fjerne fra midten mens du holder en iterator til elementet.

Forskjellen er *formen* i minnet: en `vector` pakker elementene sine side om side i én blokk, mens en `list` sprer dem utover og lenker hvert element til det neste med en peker (en adresse som peker på hvor neste node bor):

<svg viewBox="0 0 300 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="En vector lagrer elementene sine i én sammenhengende blokk som nås med indeks; en list lagrer dem som separate noder lenket med pekere, som nås ved å følge lenkene." style="display:block;margin:1rem auto;max-width:320px;width:100%;height:auto;font-family:var(--md-code-font-family,monospace);font-size:13px;" fill="none" stroke="currentColor" stroke-width="1.5">
  <defs>
    <marker id="cs-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor" stroke="none"/>
    </marker>
  </defs>
  <text x="20" y="22" stroke="none" fill="currentColor" font-weight="bold">vector</text>
  <rect x="20" y="36" width="156" height="40" rx="2"/>
  <line x1="72" y1="36" x2="72" y2="76"/>
  <line x1="124" y1="36" x2="124" y2="76"/>
  <text x="46" y="61" stroke="none" fill="currentColor" text-anchor="middle">3</text>
  <text x="98" y="61" stroke="none" fill="currentColor" text-anchor="middle">1</text>
  <text x="150" y="61" stroke="none" fill="currentColor" text-anchor="middle">4</text>
  <text x="20" y="98" stroke="none" fill="currentColor" font-size="11" opacity="0.7">sammenhengende — nå ethvert element i ett steg</text>
  <text x="20" y="130" stroke="none" fill="currentColor" font-weight="bold">list</text>
  <rect x="20" y="144" width="52" height="40" rx="4"/>
  <rect x="110" y="144" width="52" height="40" rx="4"/>
  <rect x="200" y="144" width="52" height="40" rx="4"/>
  <text x="46" y="169" stroke="none" fill="currentColor" text-anchor="middle">3</text>
  <text x="136" y="169" stroke="none" fill="currentColor" text-anchor="middle">1</text>
  <text x="226" y="169" stroke="none" fill="currentColor" text-anchor="middle">4</text>
  <line x1="72" y1="164" x2="108" y2="164" marker-end="url(#cs-arrow)"/>
  <line x1="162" y1="164" x2="198" y2="164" marker-end="url(#cs-arrow)"/>
  <text x="20" y="206" stroke="none" fill="currentColor" font-size="11" opacity="0.7">lenket — følg en peker til neste node</text>
</svg>

---

## Assosiative beholdere {#associative-containers}

Beholdere som lagrer nøkkel/verdi-par (eller bare nøkler), med raskt oppslag etter nøkkel. Igjen: [Standardbiblioteket](standard_library.md#stdmapk-v-a-sorted-key-value-store) dekker hvordan du setter inn og slår opp; her sammenligner vi de to du faktisk kommer til å velge mellom.

Valget står nesten alltid mellom `std::map` og `std::unordered_map`, og det koker ned til ett spørsmål: **trenger du nøklene i sortert rekkefølge?**

| Egenskap | `std::map` | `std::unordered_map` |
|----------|------------|----------------------|
| Underliggende struktur | Balansert tre | Hashtabell |
| Oppslag | O(log n) | O(1) i gjennomsnitt |
| Rekkefølge ved iterasjon | Sortert etter nøkkel | Uspesifisert |
| Minneoverhead per element | Høyere | Lavere (vanligvis) |
| Krav til nøkkeltypen | Mindre-enn-sammenligning | Hash + likhet |

**Bruk `unordered_map` som standard** — den er raskere i gjennomsnitt og krever mindre av deg i det daglige. Velg `map` bare når du trenger det ekstra den tilbyr: å iterere nøklene i sortert rekkefølge, eller intervallspørringer over et spenn av nøkler. Den ordnede oppførselen er nøyaktig det hashtabellen gir opp for farten sin.

### `std::set` og `std::unordered_set` {#stdset-and-stdunordered_set}

Samme avveining som de to map-ene, men de lagrer bare nøkler (ingen verdier). Nyttige for "har jeg sett denne?" og for å fjerne duplikater fra data. `set` holder nøklene sortert; `unordered_set` er raskere og usortert — bruk `unordered_set` som standard med mindre du trenger rekkefølgen. Test medlemskap med `contains()`:

```cpp
#include <unordered_set>

std::unordered_set<int> seen;
if (!seen.contains(42)) {
    seen.insert(42);
    // første gang vi ser 42 — gjør engangsarbeidet her
}
```

Det slår opp i mengden to ganger. `insert()` forteller deg allerede hva som skjedde: den returnerer et par der `.second` er `true` bare hvis verdien var ny, så ett kall gjør begge jobbene:

```cpp
if (seen.insert(42).second) {
    // første gang vi ser 42 — gjør engangsarbeidet her
}
```

---

## Beholderadaptere {#container-adapters}

Tre bekvemmelighetsinnpakninger bygd oppå andre beholdere, som bare eksponerer operasjonene til en klassisk datastruktur.

| Adapter | Oppførsel |
|---------|-----------|
| `std::stack<T>` | LIFO (sist inn, først ut): push, pop, top |
| `std::queue<T>` | FIFO (først inn, først ut): push, pop, front |
| `std::priority_queue<T>` | Tar alltid ut det største elementet |

Grip til disse når algoritmen du implementerer genuint trenger en stakk eller en kø: det begrensede grensesnittet sier "dette er en stakk" tydeligere enn en naken `vector` ville gjort, og hindrer deg i å gripe til operasjoner algoritmen ikke burde bruke.

En `vector` kan gjøre jobben til en `std::stack` — push og pop bakerst er begge O(1), så den gjør alt en stakk trenger, og mer til. En `std::queue` er en annen historie: en kø fjerner *forrest*, som er O(n) på en vector (hvert gjenværende element flyttes ned). Det er derfor `std::queue` er bygd på en `std::deque`, ikke en vector. Så "bare bruk en vector" holder for stakker, ikke for køer.

---

## Å velge: en beslutningstabell {#choosing-a-decision-table}

| Du trenger å… | Bruk |
|--------------|-----|
| Holde en liste med verdier, vokse på slutten | `std::vector` |
| Holde en samling med fast størrelse | `std::array` |
| Holde en liste, vokse i begge ender | `std::deque` |
| Koble nøkler til verdier, raskt oppslag | `std::unordered_map` |
| Koble nøkler til verdier, iterere i rekkefølge | `std::map` |
| Holde styr på hvilke elementer du har sett | `std::unordered_set` |
| LIFO-oppførsel | `std::stack` |
| FIFO-oppførsel | `std::queue` |
| Alltid ta ut høyeste prioritet | `std::priority_queue` |

Når du er i tvil, start med `std::vector` eller `std::unordered_map`. De dekker flere tilfeller enn noe annet par av beholdere.

---

## Trær, grafer og "hvorfor finnes det ingen `std::tree`?" {#trees-graphs-and-why-isnt-there-a-stdtree}

Du legger kanskje merke til at standardbiblioteket *ikke* leveres med en generell tre- eller grafbeholder. Det er med vilje: trær og grafer kommer i for mange former (binære, n-ære, balanserte, vektede, rettede, …) til at én beholder kan passe dem alle.

Når du trenger et tre, bygger du det selv av **noder**: hver node holder en verdi og lenker til barnenodene sine. Lenkene bruker verktøy fra senere kapitler (referanser og smartpekere i kapittel 4, maler for å få noden til å virke for enhver verditype i kapittel 5), så den fulle konstruksjonen venter til da.

Når du trenger en graf, er en "naboliste" (adjacency list) — `std::unordered_map<NodeId, std::vector<NodeId>>`, som kobler hver node til listen over noder den er koblet til — vanligvis alt du trenger, og den bruker bare beholderne fra dette kapittelet. Spesialiserte biblioteker finnes (Boost.Graph, for eksempel) når algoritmene blir seriøse.

Å implementere disse fra bunnen av er en fin læringsøvelse, men i produksjonskode bør du foretrekke biblioteket der ett finnes. Fortsatt nysgjerrig? [Bygge et tre](../building_a_tree.md) bygger en liten, gjenbrukbar trebeholder steg for steg og demonstrerer den med et familietre.

---

## Oppsummering {#summary}

- Standardbiblioteket dekker hver grunnleggende datastruktur du trenger dette semesteret.
- `std::vector` er standardsekvensen din; `std::unordered_map` er standard-oppslagstabellen din.
- Lenkede lister finnes, men er vanligvis ikke det du vil ha; `std::vector` er mer cache-vennlig.
- Trær og grafer er ikke i standardbiblioteket; en graf er bare en naboliste (`std::unordered_map` av `std::vector`), og trær bygger du av noder når du har verktøyene fra kapittel 4–5.
- Velg en beholder ved å spørre hvordan du skal legge til, finne og ordne elementene, ikke hvilken som høres smart ut.
