# Bruke KI til koding

KI-assistenter (ChatGPT, Claude, Copilot, Gemini og resten) kan skrive C++. De kan forklare den, debugge den, refaktorere den og svare på spørsmål om den til alle døgnets tider. De er genuint nyttige verktøy, og du kommer til å bruke dem. Alle kommer til det.

Spørsmålet er ikke *om* du skal bruke dem. Spørsmålet er hvordan du bruker dem på en måte som gjør deg til en bedre programmerer, i stedet for en som stille blir dårligere over tid.

Denne siden er den korte, ærlige versjonen av hva de er, hva de er gode og dårlige til, og arbeidsvanene som lar deg få utbyttet uten å miste ferdigheten.

---

## Hva en LLM egentlig er

En **stor språkmodell** (large language model, LLM) er, i én setning, en statistisk motor som forutsier hvilken tekst som sannsynligvis kommer etter teksten så langt. Den ble trent på enorme mengder tekst (bøker, nettsider, kodelagre, forumtråder) og lærte mønstrene inni den. Når du ber den om å "skrive et C++-program som leser en CSV-fil", forstår den ikke CSV-er. Den produserer den typen tekst som, statistisk sett, følger en slik forespørsel.

Tre konsekvenser betyr noe for hvordan du bruker den:

1. **Den har ingen kompilator, ingen debugger og ingen øyne.** Den kan ikke kjøre kode, kan ikke lese skjermen din, kan ikke avgjøre om det den nettopp produserte vil kompilere. Den resonnerer utelukkende ut fra mønstre i tekst.
2. **Den kan ta selvsikkert feil.** Fordi den produserer flytende, plausibel tekst, melder feilene seg ikke selv. Utskriften leses som om en ekspert skrev den, enten en ekspert *ville* skrevet den eller ikke.
3. **C++-kunnskapen dens er skjevt vridd mot det som lå på internett.** Mye C++ på nett er gammel: før `std::unique_ptr`, før `auto`, full av `using namespace std;` og rå `new`/`delete`. Moderne beste praksis er underrepresentert i treningsdataene sammenlignet med hvor ofte den faktisk forekommer i god kode.

Alt dette blir bedre over tid. Ingenting av det har forsvunnet.

---

## Hva KI er genuint god til

Brukt riktig er en KI-assistent et av de beste læringsverktøyene du noensinne har hatt tilgang til. Stedene den glimrer:

- **Forklare begreper med en annen stemme.** Hvis lærebokas forklaring av referanser ikke klikker, hjelper det ofte å spørre "forklar referanser i C++ som om jeg har brukt Python".
- **Lese skumle feilmeldinger.** Lim inn en 200 linjer lang malfeil og spør "hva er det denne klager på?" — den kan som regel oversette tekstveggen til én setning.
- **Generere standardkode (boilerplate).** En `CMakeLists.txt` for et prosjekt med et bibliotek og tester, et grunnleggende klasseskjelett med konstruktører og gettere, et `Makefile`-aktig skript: disse har én åpenbart riktig form, og KI produserer dem raskt og pålitelig.
- **Oversette mellom språk.** "Her er Python-løsningen min; hvordan ville dette sett ut i C++?" er en rask måte å bygge bro fra tidligere erfaring på.
- **Bruke den som badeand (rubber-ducking).** Å beskrive problemet ditt høyt får deg ofte til å innse svaret selv; å gjøre det til en KI virker på samme måte, pluss at den noen ganger legger merke til ting du overså.
- **Kodegjennomgang av din egen kode.** "Her er funksjonen jeg nettopp skrev, ser du noen feil eller ting jeg kunne forenklet?" er en mye bedre ledetekst enn "skriv en funksjon som gjør X."

---

## Hva KI ikke er god til

Den motsatte lista, like viktig:

- **Kode utover en skjerm eller to.** Når problemet ditt berører flere filer eller en lengre-enn-triviell flyt, begynner modellen å miste oversikten over konteksten og finne på ting.
- **Følge prosjektets konvensjoner.** Den kjenner ikke navngivningsstilen din, dine eksisterende hjelpefunksjoner, valgene teamet ditt har tatt. Den skriver gjerne kode som motsier resten av kodebasen din.
- **Moderne C++-idiomer spesifikt.** Denne biter studenter: be om "et C++-program som …" og du har 50/50 sjanse for å få `using namespace std;`, rå `new`/`delete` og andre antimønstre denne boka har lært deg å unngå. Du må vanligvis be eksplisitt om *moderne* C++.
- **Skille sant fra plausibelt.** Den finner på bibliotekfunksjoner, parameternavn og standardheadere som ikke finnes, presentert i selvsikker prosa. cppreference-siden for `std::frobnicate` finnes ikke; KI-ens beskrivelse av den gjør det.
- **Subtile feil i sin egen utskrift.** Den er mye bedre til å skrive kode enn til å teste den. Kode som "ser riktig ut" fra KI-en er ikke det samme som kode som *er* riktig.

---

## Fellen

Her er biten du bør lese på nytt hvert semester.

Faren med KI er ikke at den skriver oppgavene dine. Faren er at den skriver dem *godt nok* til at du aldri lærer å skrive dem selv, og du vil ikke merke at du ikke har lært det før mye senere: typisk på en eksamen, et intervju eller en jobb der du forventes å faktisk programmere.

Det finnes spesifikke ferdigheter som bare utvikles ved å gjøre-det-selv, selv når KI kunne gjort det raskere:

- **Lese en kompilatorfeil og vite hva den betyr.** Denne ferdigheten kommer av å ha blitt forvirret av hundrevis av feil og funnet ut av dem. Å sette bort hver eneste feil til KI betyr at du aldri bygger opp mønstergjenkjenningen.
- **Holde et program i hodet.** Ekte debugging er for det meste mental simulering: "hvis løkka kjører tre ganger, så vil `i` være …" Å hoppe rett til "KI-en sier fiks det slik" hindrer deg i noensinne å bygge den mentale simulatoren.
- **Vite hva som er idiomatisk.** Du kan bare gjenkjenne en ren løsning hvis du har sett og skrevet rotete løsninger. Hvis din eneste erfaring med klassedesign er å lese KI-utskrift, vil ikke smaken din utvikle seg.
- **Selvtillit under press.** På en eksamen på én time uten internett er ikke KI-en din der. Det som ligger i hendene dine, er det du har.

En spesifikk feilmodus som nå er vanlig: studenter som kan løse hver eneste ukesoppgave via KI, men ikke kan skrive en `for`-løkke uten den. De føler seg kompetente i løpet av semesteret og oppdager hullet sitt først når de vurderes individuelt under kontrollerte forhold.

---

## Vaner som beskytter læringen

Avveiningen over er reell, men ikke absolutt. Følgende praksiser gir deg det meste av oppsiden uten det meste av nedsiden.

### Prøv først, spør etterpå

Bruk minst ti minutter på å prøve et problem på egen hånd før du spør KI. Selv om du mislykkes, har du bygget et mentalt kart over hva som er vanskelig. Når KI-en så viser deg en løsning, forstår du *hvorfor* valget dens hjelper, i stedet for å hoppe over et problem du aldri engasjerte deg i.

### Skriv koden selv, selv om du ikke fant på den

Å kopiere og lime inn fra KI er den enkeltstående største barrieren for læring. Fingrene dine og den visuelle hukommelsen din bidrar til ferdighet på måter som scrolling ikke gjør. Hvis du godtar en KI-skrevet funksjon, skriv den inn på nytt. Ja, manuelt. Dette er den enkeltstående vanen med høyest verdi på denne siden.

### Spør "hvorfor", ikke bare "hva"

Etter at KI gir deg kode, be den forklare *hvorfor*: hvorfor denne tilnærmingen, hvorfor denne headeren, hvorfor denne signaturen. Sjekk så forklaringen. Hvis forklaringen ikke gir mening for deg, forstår du ikke koden ennå, og du bør ikke levere den inn.

### Verifiser ved å kjøre, ikke ved å lese

KI-utskrift leses overbevisende selv når den er ødelagt. Kompiler den. Kjør den på grensetilfeller. Kjør den spesielt på inndataene KI-en ikke nevnte.

### Vær spesifikk om konteksten din

En naken "skriv C++ til meg som sorterer en vector" gir deg generisk, ofte foreldet kode. Bedre:

> "Skriv moderne C++20-kode som sorterer en `std::vector<Reading>` etter `timestamp`-feltet, stigende. Jeg bruker GCC 13, ingen eksterne biblioteker."

Jo flere føringer du gir, desto nærmere er utskriften det du faktisk vil ha. Fortell den språkstandarden, plattformen, nivået ditt, stilen din.

### Bruk den til gjennomgang, ikke generering

En overraskende god ledetekst:

> "Her er funksjonen jeg skrev: `[lim inn]`. Hvilke feil eller forbedringer ser du? Ikke skriv den om; bare påpek ting."

Dette holder *deg* skrivende koden, med KI-en som et ekstra par øyne. Koden forblir din; tilbakemeldingen hjelper.

### Behandle utskriften som Wikipedia

Nyttig utgangspunkt. Muligens feil. Verifiser alltid mot en primærkilde ([cppreference](https://en.cppreference.com/), standarden, dokumentasjonen til biblioteket du bruker) før du stoler på den til noe som betyr noe.

---

## Å jobbe med KI i akkurat dette emnet

Noen praktiske tips for å få god C++ ut av en assistent i konteksten til dette emnet:

- **Oppgi standarden.** "Bruk C++20" i ledeteksten din. Ellers kan du forvente C++98-idiomer.
- **Forby de dårlige vanene.** "Ingen `using namespace std;`. Ingen rå `new`/`delete`; bruk `std::unique_ptr` eller standardbeholdere. Bruk RAII." Når det er sagt, retter de fleste modeller seg etter det.
- **Be om den minste versjonen først.** "Vis meg den minimale CMakeLists.txt som bygger én kjørbar fil" er en bedre ledetekst enn "sett opp et fullt CMake-prosjekt for meg."
- **For feil, lim inn det hele.** Gi KI-en koden din *og* hele kompilatorutskriften. Ikke oppsummer; den fulle teksten inneholder ofte ledetråden.
- **Skill begreper fra generering.** Når du ikke forstår noe (referanser, RAII, virtuelle funksjoner), er det flott å be KI forklare. Når du har en oppgave å løse, skriv den selv først.

---

## Akademisk redelighet

Denne boka setter ikke reglene for hva som teller som juks i akkurat ditt emne; det gjør emneansvarlige og institusjonen. Finn de reglene og følg dem. Hvis KI-bruk må oppgis, oppgi den. Hvis den er forbudt på en bestemt oppgave, ikke bruk den. Reglene gjelder enten KI-en er oppdagbar eller ikke.

Uavhengig av enhver emneregel: hvis navnet ditt står på noe og du ikke kan forklare hver linje av det under utspørring, bør du behandle det som et problem verdt å fikse før du leverer det inn.

---

## Oppsummering

- LLM-er er utmerkede verktøy og forræderske lærere. De er begge deler samtidig.
- De forutsier plausibel tekst. De vet ikke ting; de kjører ikke ting; de kan ta selvsikkert feil.
- De er gode til forklaring, standardkode, feiltyding og kodegjennomgang.
- De er dårlige på store programmer, din lokale stil, moderne idiomer, og på å fortelle deg når de gjetter.
- Risikoen er ikke at KI skriver koden din. Risikoen er at du aldri lærer å gjøre det.
- Skriv koden selv, selv om KI fant på den. Spør "hvorfor", ikke bare "hva". Prøv først, spør etterpå.
- Oppgi C++-standarden, forby rå `new`/`delete`, og verifiser ved å kjøre.
- Uansett hvilke regler som gjelder for emnet ditt: følg dem.

De beste programmererne i 2026 bruker KI mye. De er også de som kunne skrevet alt de ber KI-en om, bare langsommere. Vær en av de menneskene.
