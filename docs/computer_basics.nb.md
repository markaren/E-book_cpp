# Datamaskingrunnlag

Programmeringsverktøy forutsetter at du allerede kan noen ting om datamaskinen din som de fleste aldri har trengt å lære: hvordan filer og stier egentlig fungerer, hva "terminalen" er, og hvordan systemet finner programmene du kjører. Emner underviser sjelden i dette, og likevel snubler nybegynnere stadig i det — en bygging som feiler på grunn av et mellomrom i et mappenavn, et `command not found` som egentlig er et PATH-problem, en kommando fra en veiledning som ikke gjør noe fordi den var skrevet for et annet skall.

Denne siden dekker det laget alle tar for gitt: **hva bits og bytes er, filsystemet og stier, terminalen og skallene dens, og PATH-variabelen.** Du trenger ikke pugge det — skum gjennom nå, og kom tilbake når noe her biter deg.

---

## Bits og bytes

Alt en datamaskin lagrer — tall, tekst, bilder, selve programmet ditt — er til syvende og sist bare **bits**. En bit er den minste informasjonsbiten som finnes: et enkelt `0` eller `1`, som en bryter som er enten av eller på.

Bits grupperes i **byte** på åtte. Åtte av/på-brytere kan settes opp i **256** forskjellige mønstre (2 ganget med seg selv åtte ganger), så én byte kan holde hvilken som helst av 256 ulike verdier — for eksempel et heltall fra 0 til 255, eller ett enkelt teksttegn.

Større verdier bruker bare flere byte:

| Enhet | Størrelse | Omtrent |
|-------|-----------|---------|
| **bit** | `0` eller `1` | én av/på-bryter |
| **byte** | 8 bits | ett tegn, eller et tall 0–255 |
| **kilobyte** (KB) | ~1 000 byte | en side med ren tekst |
| **megabyte** (MB) | ~1 000 KB | et bilde eller en sang |
| **gigabyte** (GB) | ~1 000 MB | en film; datamaskinens RAM måles i disse |

Det er derfor hver type i C++ har en **størrelse**. En `bool` trenger bare én byte; en `int` er vanligvis fire byte (32 bits); en `double` er åtte. Størrelsen setter en hard grense for hva som får plass: en 32-bits `int` kan telle til omtrent ±2 milliarder, og går du forbi det, **renner den over** (overflow) og ruller rundt. Det er også derfor en mikrokontroller med bare noen få **kilobyte** minne (se [Arduino vs. desktop-C++](arduino_vs_desktop.md)) tvinger fram en nøysomhet som en datamaskin med gigabyte ikke gjør. De nøyaktige typestørrelsene står i [Variabler og grunntyper](Chapter1/variables.md).

### Tekst og ASCII {#ascii}

Hvis en byte bare er et tall, hvordan kan den holde en *bokstav*? Ved avtale: en **tegnkoding** knytter hvert tegn til et tall. Den eldste og mest universelle er **ASCII**, som tildeler verdiene 0–127 til de engelske bokstavene, sifrene, skilletegnene og noen få kontrolltegn — så `'A'` er 65, `'a'` er 97, og `'0'` er 48 — [hele ASCII-tabellen](https://www.ascii-code.com/) lister alle 128. (Det er også derfor `char` i C++ egentlig bare er et heltall på én byte.)

Men ASCII dekker bare 128 tegn — nok for amerikansk engelsk, men uten plass til `æ`, `ø`, `å`, bokstaver med aksent eller emoji. De hører til det langt større **Unicode**-settet, vanligvis lagret som **UTF-8**, der ett slikt tegn tar *to eller flere* byte.

Det gapet gir et svært praktisk hodebry. ASCII er den minste felles nevneren som alle verktøy, kompilatorer og operativsystemer er enige om; alt utenfor håndteres mindre konsekvent. Et program eller byggeverktøy som forutsetter ren ASCII og møter en løs `ø`, kan skrive ut forvrengt tekst (`Ã¸`) eller feile helt. Det er nettopp derfor stireglene lenger ned ber deg holde filnavn og mapper til ren ASCII — og hvorfor kildekoden holdes på engelsk.

---

## Filer, mapper og stier

Filene dine ligger i **mapper** (også kalt **kataloger**), som ligger inni hverandre og danner et tre. En **sti** er adressen til en fil eller mappe: listen over mapper du går gjennom for å nå den.

- En **absolutt sti** starter fra toppen ("roten") og er entydig:
    - Windows: `C:\Users\ada\projects\hello\main.cpp`
    - macOS / Linux: `/home/ada/projects/hello/main.cpp`
- En **relativ sti** er relativ til der du er nå — din *arbeidskatalog*: `projects/hello/main.cpp`, eller `../other` for å gå opp ett nivå.

**Hjemmemappen** din er din personlige mappe: `C:\Users\<deg>` på Windows, `/Users/<deg>` på macOS, `/home/<deg>` på Linux. Den skrives ofte `~`.

### Arbeidskatalogen

**Arbeidskatalogen** din (eller "gjeldende katalog") er mappa et program er "i" akkurat nå — mappa som relative stier måles fra. I en terminal skriver `pwd` den ut og `cd` endrer den.

Den har betydning for et kjørende program også. Når koden din åpner en fil med bare et navn — `std::ofstream out("report.txt")` — leter den ikke i prosjektmappa di; den leter i *arbeidskatalogen til det kjørende programmet*, og **når du starter programmet fra en IDE, er ikke det der du tror.** CLion kjører programmet ditt fra byggemappa (f.eks. `cmake-build-debug/`), så en `report.txt` programmet skriver havner *der*, og en `readings.txt` det leser må ligge *der* — ikke ved siden av kildekoden.

Hvis et program "ikke finner" en fil som tydeligvis finnes, eller skriver en du så ikke finner igjen, er arbeidskatalogen nesten alltid grunnen. I CLion kan du se eller endre den under **Run → Edit Configurations → Working directory**.

### `/` kontra `\`

En klassisk kilde til forvirring:

- **Windows** skiller mapper med en **omvendt skråstrek** `\`.
- **macOS og Linux** bruker en **vanlig skråstrek** `/`.

Dette har betydning i C++, fordi inni en streng er en omvendt skråstrek et *escape-tegn*:

```cpp
std::string bad = "C:\dev\hello";    // FEIL: \d og \h er ikke gyldige escape-sekvenser
std::string a   = "C:\\dev\\hello";  // virker: escape hver omvendte skråstrek
std::string b   = "C:/dev/hello";    // enklere: vanlige skråstreker virker også på Windows
```

Windows' filfunksjoner godtar gjerne `/`, så når du må skrive en sti i kode, **foretrekk vanlige skråstreker** og slipp escape-hodebryet. (`std::filesystem::path` håndterer også skilletegnene for deg.)

### Hold stier korte, enkle og rene

Hvor du legger prosjektene dine betyr mer enn nybegynnere venter:

- **Unngå lange, dypt nestede stier.** Windows har historisk begrenset en full sti til 260 tegn, og mange verktøy ryker fortsatt forbi det. Et prosjekt begravd under `Documents\University\Semester 1\AIS1003\Assignments\…` kan treffe taket. Legg koden et kort sted, som `C:\dev\`.
- **Unngå mellomrom.** `My Projects` tvinger deg til å sette stien i hermetegn på kommandolinjen (`"My Projects"`), og noen verktøy håndterer det feil. Foretrekk `my-projects` eller `my_projects`.
- **Unngå spesialtegn og ikke-engelske tegn.** Norske `æ`, `ø`, `å`, bokstaver med aksent og symboler som `#`, `&`, `(` forvirrer kompilatorer, byggeverktøy og skript på måter som gir uforståelige feil — de faller utenfor [ASCII](#ascii). Hold deg til vanlige bokstaver, sifre, `-` og `_`.
- **Unngå skysynkroniserte mapper** (OneDrive, Dropbox, Google Drive) for kode: en bygging lager tusenvis av filer som synkroniseres hele tiden, og maskinspesifikke byggefiler skaper konflikter mellom datamaskiner.

Et godt hjem for kursarbeidet ditt: `C:\dev\ais1003\` på Windows, eller `~/dev/ais1003/` på macOS/Linux.

---

## Terminalen

**Terminalen** er et vindu der du styrer datamaskinen ved å *skrive kommandoer* i stedet for å klikke. Du skriver en kommando, trykker Enter, datamaskinen kjører den og skriver ut resultatet, og gir deg så et nytt **ledetegn** (prompt) for neste kommando:

```
C:\dev\hello>          (ledetegnet — her viser det også gjeldende mappe)
```

Hvorfor bry seg, når det finnes et helt greit grafisk grensesnitt?

- **De fleste utviklerverktøy er kommandolinje først** — `git`, CMake, kompilatorer, pakkebehandlere. Knappene i IDE-en din kjører ofte bare disse kommandoene for deg.
- **Det er presist og repeterbart.** En kommando er eksakt; den kan skrives ned, deles, skriptes og kjøres på nytt identisk. "Klikk her, så der, så …" kan ikke det.
- **Det viser deg hva som skjer.** Når noe feiler, er terminalens utskrift der den egentlige feilmeldingen står.
- **Det virker overalt**, også på fjernmaskiner og servere som ikke har noe grafisk grensesnitt i det hele tatt.

Du trenger ikke forlate det grafiske grensesnittet — men en programmerer som nekter å ta i terminalen, jobber med én hånd bundet.

En kommando er som regel et programnavn, eventuelt fulgt av **argumenter** (hva det skal handle på) og **valg** eller **flagg** (hvordan det skal handle). I:

```
git commit -m "Fix the bug"
```

er `git` programmet, `commit` en underkommando, `-m` et valg, og `"Fix the bug"` argumentet til det valget. Merk hermetegnene: hvis noe du skriver inneholder mellomrom, sett det i hermetegn så det behandles som ett element (`cd "My Folder"`).

---

## Skall: PowerShell, cmd, bash, zsh

Folk sier "terminalen" løst, men det er egentlig to forskjellige ting:

- **Terminalen** er *vinduet* — appen som viser tekst og tar imot tastetrykkene dine.
- **Skallet** (shell) er *programmet som kjører inni det* og som faktisk tolker kommandoene du skriver.

Flere skall finnes, og **kommandoene og syntaksen deres er forskjellige** — det er derfor en kommando kopiert fra en Linux-veiledning kan feile på Windows:

| Skall | Hvor du møter det | Merknader |
|-------|-------------------|-----------|
| **Ledetekst (`cmd`)** | Windows (gammelt) | Begrenset; du vil sjelden velge det med vilje. |
| **PowerShell** | Windows (moderne standard) | Kraftig; det du bør bruke på Windows. |
| **bash** | Linux, Git Bash, WSL | Det klassiske Unix-skallet; de fleste eksempler på nett antar det. |
| **zsh** | macOS (moderne standard) | Bash-likt til daglig bruk. |

Noen forskjeller du faktisk vil støte på:

| Oppgave | bash / zsh | PowerShell | cmd |
|---------|------------|------------|-----|
| Liste filer i en mappe | `ls` | `ls` eller `dir` | `dir` |
| Vise gjeldende mappe | `pwd` | `pwd` | `cd` |
| Lese en variabel | `$HOME` | `$env:USERPROFILE` | `%USERPROFILE%` |

Den praktiske regelen: **vit hvilket skall du er i**, og når du kopierer en kommando fra nettet, sjekk at den passer. På Windows, foretrekk **PowerShell** — det er det terminalen innebygd i CLion bruker som standard. På macOS og Linux er standardskallet (zsh eller bash) helt greit.

---

## PATH: hvordan datamaskinen finner programmer

Når du skriver `git` i en terminal, hvordan vet datamaskinen hvor `git` faktisk ligger på disken? Den sjekker en miljøvariabel kalt **`PATH`** — en liste over mapper den skal lete i, i rekkefølge, etter et program med det navnet.

- Hvis `git` finnes i en av de mappene, kjøres det.
- Hvis ikke, får du **`command not found`** (eller, på Windows, `'git' is not recognized…`).

Så den feilen betyr nesten alltid én av to ting: programmet er **ikke installert**, eller det er installert, men **mappen ble aldri lagt til i `PATH`**. Mange installasjonsprogrammer legger seg selv til i `PATH` automatisk; noen — og de fleste manuelle installasjoner — gjør det ikke, og da må du legge til mappen selv.

`PATH` er én av flere **miljøvariabler**: navngitte verdier systemet holder på for at programmer skal lese dem. Som nybegynner vil du mest møte `PATH`, og mest når et nyinstallert verktøy "ikke kan finnes".

> Du vil sjelden trenge å redigere `PATH` for hånd i dette emnet — CLion har med verktøyene den trenger. Men når en veiledning sier "sørg for at X er på `PATH`", er det dette den mener.

---

## Tommelfingerregler

- Hold prosjekter i en **kort, ren sti** nær rota av disken (`C:\dev\…`), ikke en dyp mappe full av mellomrom og norske bokstaver.
- I C++-kode, skriv stier med **vanlige skråstreker** (`"C:/dev"`) eller escape de omvendte skråstrekene (`"C:\\dev"`).
- Et program leser og skriver relative stier (som `"report.txt"`) fra **arbeidskatalogen** sin — som IDE-en ofte setter til byggemappa, ikke prosjektmappa.
- **Terminalen** er verdt å lære: de fleste verktøy bor der, og den viser deg de egentlige feilene.
- Et **skall** (PowerShell, bash, zsh, cmd) tolker kommandoene dine, og de er forskjellige — tilpass kopierte kommandoer til skallet ditt. På Windows, bruk PowerShell.
- **`command not found`** betyr som regel "ikke installert" eller "ikke på `PATH`".
