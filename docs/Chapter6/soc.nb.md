# Separasjon av ansvar

Når et program er lite (én `main`, noen få hjelpefunksjoner), kan du holde hele greia i hodet. Når det vokser, kan du ikke. Veien ut er **separasjon av ansvar**: å organisere programmet slik at hver del er ansvarlig for én ting, og delene bare kjenner hverandre gjennom smale, bevisste grensesnitt.

Kode skrevet på denne måten er lettere å lese, lettere å teste og lettere å endre. Kode som ignorerer prinsippet, har en tendens til å utvikle en egenskap der hver endring ødelegger noe urelatert.

Dette kapittelet forklarer prinsippet og viser hvordan det ser ut i kode.

> Koden på denne siden er **illustrativ**: den blander maskinvarekall i Arduino-stil (`analogRead`, `digitalWrite`) med skrivebordsfasiliteter (`std::ofstream`, `std::cout`) og utelater `#include`-ene, for å holde søkelyset på *struktur* heller enn på et program du kan lime inn og kompilere.

---

## Lukten av sammenblandede ansvarsområder {#the-smell-of-mixed-concerns}

Her er en funksjon som leser en temperatursensor, avgjør om noe er i ferd med å overopphetes, og skriver ut en advarsel. Alt på ett sted:

```cpp
void monitorLoop() {
    while (true) {
        int raw = analogRead(A0);
        double celsius = (raw * 5.0 / 1023.0 - 0.5) * 100.0;

        if (celsius > 80.0) {
            std::ofstream log("alerts.log", std::ios::app);
            log << "[ALERT] " << celsius << " C at " << millis() << "\n";
            std::cout << "OVERHEAT\n";
            digitalWrite(LED_BUILTIN, HIGH);
        }

        delay(100);
    }
}
```

Hva er galt med den? Ingenting, rent mekanisk — den virker. Men tre ulike ansvarsområder er filtret sammen:

1. **Maskinvaretilgang:** lese sensoren, skrive til LED-en.
2. **Domenelogikk:** konvertere rå ADC-verdier til temperatur, avgjøre hva som regnes som overoppheting.
3. **Rapportering:** skrive til en loggfil, skrive ut til konsollen.

Å teste domenelogikken uten en ekte sensor? Umulig. Å sende varsler et annet sted enn til en fil? Da må du redigere denne funksjonen. Å bruke en annen sensor med en annen konverteringsformel? Samme sak. Hvert ansvarsområde er sveiset fast i alle de andre.

---

## Samme logikk, separert {#the-same-logic-separated}

Samme oppførsel, men hvert ansvarsområde er sin egen del:

```cpp
// --- Ansvarsområde 1: maskinvaretilgang ---
class TemperatureSensor {
public:
    virtual ~TemperatureSensor() = default;
    virtual double readCelsius() = 0;
};

class AnalogTemperatureSensor : public TemperatureSensor {
public:
    explicit AnalogTemperatureSensor(int pin) : pin_(pin) {}
    double readCelsius() override {
        int raw = analogRead(pin_);
        return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    }
private:
    int pin_;
};

// --- Ansvarsområde 2: domenelogikk ---
class OverheatPolicy {
public:
    explicit OverheatPolicy(double threshold) : threshold_(threshold) {}
    bool isOverheating(double celsius) const {
        return celsius > threshold_;
    }
private:
    double threshold_;
};

// --- Ansvarsområde 3: rapportering ---
class AlertSink {
public:
    virtual ~AlertSink() = default;
    virtual void overheatDetected(double celsius) = 0;
};

class FileAlertSink : public AlertSink {
public:
    explicit FileAlertSink(const std::string& path) : out_(path, std::ios::app) {}
    void overheatDetected(double celsius) override {
        out_ << "[ALERT] " << celsius << " C\n";
    }
private:
    std::ofstream out_;
};

// --- Orkestratoren: knytter dem sammen, vet ingenting om detaljer ---
void monitorLoop(TemperatureSensor& sensor,
                 const OverheatPolicy& policy,
                 AlertSink& alerts) {
    while (true) {
        double t = sensor.readCelsius();
        if (policy.isOverheating(t)) {
            alerts.overheatDetected(t);
        }
        delay(100);
    }
}
```

Hver klasse har én jobb. Funksjonen som trekker dem sammen, vet *hva* som må skje, men ingenting om *hvordan*. Den aner ikke om temperaturen kommer fra en analog pinne eller en simulert sensor, aner ikke om varsler går til en fil eller en nettverkssocket, aner ikke hvilken terskel som gjelder. Denne stilen der avhengighetene rekkes inn — `monitorLoop` *får* sensoren, policyen og varselmottakeren i stedet for å opprette dem selv — kalles **dependency injection**; du møter den igjen i [Testing](testing.md), der den er det som lar en test smette inn en fake.

Vil du teste policyen? Konstruer en `OverheatPolicy` og kall `isOverheating` med verdier; ingen maskinvare nødvendig. Vil du bytte fra fil- til konsollvarsel? Skriv en `ConsoleAlertSink` og send den inn i stedet. Vil du teste orkestratoren? Gi den en fake-sensor som returnerer forhåndsbestemte verdier og en fake-mottaker som noterer varslene.

---

## Kohesjon og kobling {#cohesion-and-coupling}

Før-og-etter-bildet du nettopp så, har et navn — to, faktisk — og de er vokabularet du vil høre hver gang folk snakker om design:

- **Kohesjon** er hvor sterkt delene av én bit hører sammen: hvor fokusert den er på én enkelt jobb. `OverheatPolicy` er *høyt kohesiv* — den avgjør én ting, om en temperatur er for høy, og ingenting annet. Den opprinnelige `monitorLoop` hadde *lav* kohesjon: den leste maskinvare, konverterte enheter og skrev filer på én gang.
- **Kobling** er hvor mye én del avhenger av detaljene i en annen. Den separerte `monitorLoop` er *løst koblet*: den når delene sine bare gjennom grensesnittene `TemperatureSensor` og `AlertSink`, så en ekte sensor kan byttes ut med en fake uten å røre den. Den opprinnelige var *tett koblet* — varselet sveiset til en bestemt fil, avlesningen til en bestemt pinne.

Det du alltid sikter mot, er **høy kohesjon, lav kobling**: hver del gjør én jobb godt, og lener seg på de andre så lite den kan, gjennom smale grensesnitt. Nesten hver teknikk i dette kapittelet — å dele opp en funksjon, å skjule en detalj bak et grensesnitt, å gi en klasse ett ansvar — er en måte å skyve i den retningen på.

Av de to gjør tett kobling mest skade: når alt avhenger av alt, forplanter én endring seg overalt, og ingenting kan testes eller byttes ut for seg. Symptomene i neste avsnitt er måten lav kohesjon og tett kobling viser seg på i virkelig kode.

---

## Hva "ansvarsområde" betyr i praksis {#what-concern-means-in-practice}

Et **ansvarsområde** (concern) er én ting et program er ansvarlig for. Noen ansvarsområder er åpenbare:

- snakke med maskinvare
- beregne noe
- presentere resultater for en bruker
- lagre data
- håndtere feil

Andre ansvarsområder er mer subtile og vokser fram over tid. Du kjenner igjen sammenblandede ansvarsområder på symptomene:

- En liten endring i én del tvinger fram redigeringer i urelaterte deler.
- Å skrive en test for én del krever å sette opp ting som ikke har noe med testen å gjøre.
- Navnet på en funksjon trenger ordet "og" (`readSensorAndAlertIfHot`).
- Én enkelt klasse snakker med nettverket, databasen og brukergrensesnittet.
- Flere funksjoner griper inn i og endrer den samme **globale variabelen**, så ingen enkelt del eier den tilstanden.

Når du får øye på disse, har du en kandidat for oppdeling.

---

## Verktøy for å separere ansvarsområder {#tools-for-separating-concerns}

Prinsippet er tidløst; teknikkene er konkrete.

### Funksjoner {#functions}

Det mest grunnleggende verktøyet. Hvis en bit kode inne i en funksjon gjør noe som har et navn, gi den sin egen funksjon:

```cpp
// Før
void run() {
    int raw = analogRead(A0);
    double celsius = (raw * 5.0 / 1023.0 - 0.5) * 100.0;
    /* ... 50 linjer til ... */
}

// Etter
double readTemperature() {
    int raw = analogRead(A0);
    return (raw * 5.0 / 1023.0 - 0.5) * 100.0;
}

void run() {
    double t = readTemperature();
    /* ... */
}
```

Den navngitte funksjonen dokumenterer hensikt, kan testes isolert, og hindrer at funksjonen som kaller den, drukner i detaljer.

### Klasser {#classes}

En klasse grupperer data med operasjonene som virker på dem. Grip etter en klasse når flere beslektede biter av tilstand må utvikle seg sammen (en tilkobling, en parser, en kontroller) og du ser at de samme dataene sendes rundt i følge.

### Grensesnitt (abstrakte basisklasser) {#interfaces-abstract-base-classes}

Når orkestratoren ikke trenger å vite hvilken konkret implementasjon den snakker med, skjul den bak et grensesnitt. Eksempelet ovenfor bruker `TemperatureSensor` og `AlertSink` på nøyaktig denne måten: `monitorLoop` virker med hva som helst som oppfyller de grensesnittene. Bytt implementasjoner uten å røre orkestratoren.

Dette er også det som gjør kode testbar: grensesnittet lar deg sette inn en fake-implementasjon i tester.

### Filer og moduler {#files-and-modules}

Når en logisk del vokser forbi én skjerm, gi den sin egen fil. Et par av header og implementasjon per klasse er en fornuftig standard. Grupper beslektede filer i mapper (`sensors/`, `alerts/`, `policies/`). Mappestrukturen i seg selv blir dokumentasjon på hvilke ansvarsområder prosjektet har.

---

## Hvor langt du skal ta det {#how-far-to-take-it}

Det er mulig å overdrive dette. Et program med tretti klasser for den samme jobben som fem ville klart, er ikke "separert"; det er knust. To tommelfingerregler:

1. **Separer når du har en grunn.** Hvis `readSensor`-funksjonen din aldri endres og du bare kaller den fra ett sted, er det greit å la koden bli stående der den er.
2. **Se etter friksjonen.** Når du merker at du vil teste noe, men ikke får det til, eller vil bytte ut noe, men ikke kan — der er stedet å trekke grensen.

God design er ikke designet med flest klasser. Det er designet der hver klasse har en klar jobb, og der et nytt krav ikke tvinger deg til å skrive om alt.

---

## Oppsummering {#summary}

- **Hver del av koden bør være ansvarlig for én ting.**
- Sikt mot **høy kohesjon** (hver del fokusert på én jobb) og **lav kobling** (deler forbundet bare gjennom smale grensesnitt).
- Når du finner en funksjon som gjør mer enn én ting, del den opp.
- Bruk grensesnitt for å koble "hva" fra "hvordan": `TemperatureSensor` vet ikke hvilken sensor; `monitorLoop` vet det heller ikke.
- Separasjon gjør kode lettere å teste, lettere å endre og lettere å lese.
- Ikke separer bare for å separere. Signalet er friksjon: teste, endre, bytte ut.
