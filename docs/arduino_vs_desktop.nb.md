# Arduino vs. desktop-C++

I dette emnet lærer du C++ for desktop, og i et parallelt emne programmerer du en Arduino. De to kan føles som forskjellige språk. Det er de ikke: **Arduino er C++.** Den samme syntaksen, de samme typene, kontrollflyten, funksjonene, klassene, referansene og `const`-korrektheten du lærer her, overføres direkte.

Det som er forskjellig, er *hvor koden kjører*. En Arduino er en bittesmå datamaskin uten operativsystem og med svært lite minne, så to ting endrer seg: **formen på programmet**, og **hvor mye av standardbiblioteket du kan bruke**. Denne siden kartlegger forskjellene så ingen av emnene forvirrer det andre.

> Detaljene under beskriver et lite 8-bits kort som Arduino Uno eller Nano — det klassiske utgangspunktet. Kraftigere kort (ESP32, Teensy, Raspberry Pi Pico) opphever mange av disse begrensningene; se [Ikke alle kort er like](#ikke-alle-kort-er-like).

---

## Det er det samme språket

Alt i kapittel 1 og 4 gjelder også på en Arduino:

- variabler, `int` / `double` / `bool` / `char`, `if` / `for` / `while`, funksjoner;
- klasser, medlemsfunksjoner, konstruktører, `const`-medlemsfunksjoner;
- referanser og pekere, sending som `const&`;
- kompilatoren er fortsatt GCC — bare en versjon som retter seg mot kortets brikke.

Hvis du kan skrive en klasse på desktop, kan du skrive en på en Arduino. Behold vanene dine.

---

## Hvor er `main()`? — `setup()` og `loop()`

På desktop starter programmet ditt ved `main()` og slutter når `main()` returnerer:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello\n";
    return 0;
}
```

En Arduino-skisse har ingen `main()` som *du* skriver. I stedet skriver du to funksjoner, og Arduino-kjernen leverer en skjult `main()` som kaller dem:

```cpp
void setup() {
    Serial.begin(9600);       // kjører én gang, ved oppstart / reset
    Serial.println("Hello");
}

void loop() {
    // kjører igjen og igjen, for alltid
}
```

- `setup()` kjører **én gang** når kortet slås på — gjør engangskonfigurasjon her.
- `loop()` kjører **om og om igjen, for alltid** — det finnes ingen "slutt." En mikrokontroller er aldri *ferdig*; den fortsetter å svare på verden til strømmen kuttes.

Bak kulissene er Arduino-kjernens `main()` omtrent: initialiser maskinvaren, kall `setup()` én gang, og deretter `for (;;) loop();`.

---

## Dele tilstand mellom `setup()` og `loop()`

`loop()` starter fra toppen hver gang, men dataene dine må overleve fra ett kall til det neste. Siden det ikke finnes noen `main()` med lokale variabler som kan holde på dem, lagrer Arduino-skisser den tilstanden i **globale variabler**, deklarert utenfor begge funksjonene:

```cpp
int  blinkCount = 0;     // global: overlever fra ett loop()-kall til det neste
bool ledOn      = false;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    ledOn = !ledOn;
    digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
    ++blinkCount;
    delay(500);
}
```

På et lite kort er dette normalt og ofte uunngåelig. Men det er den ene desktop-vanen du må **avlære bevisst**: på desktop er [globale variabler en felle](Chapter1/functions.md#global-variables) — enhver funksjon kan endre dem, så du kan ikke lenger se hva som rører tilstanden din. Der holder du tilstanden lokal i `main`, eller — bedre — pakker den inn i en [klasse](Chapter4/classes.md) som eier den.

Den gode nyheten: du kan gjøre nøyaktig det samme på Arduino. Samle beslektede globale variabler i en liten `struct` eller `class` slik at tilstanden har én tydelig eier — språket er identisk; bare betingelsen (den må overleve mellom `loop()`-kall) er ny.

---

## Utskrift: `Serial` i stedet for `std::cout`

Det finnes ingen konsoll og ingen `<iostream>` på et lite kort. For å skrive ut — vanligvis til feilsøking, sendt over USB-kabelen til PC-en din — bruk `Serial`-objektet:

| Desktop | Arduino |
|---------|---------|
| `std::cout << "x = " << x << "\n";` | `Serial.print("x = "); Serial.println(x);` |
| `std::cin >> x;` | `x = Serial.parseInt();` (og lignende) |

Kall `Serial.begin(9600);` én gang i `setup()` før du skriver ut noe.

---

## En mye mindre datamaskin

Dette er roten til nesten alle de andre forskjellene. En desktop har gigabyte med RAM; en Uno har **to kilobyte**.

| | Arduino Uno | Typisk desktop |
|---|---|---|
| RAM | 2 KB | 8–32 GB |
| Programlagring | 32 KB flash | hundrevis av GB |
| CPU | 1 kjerne, 16 MHz | mange kjerner, GHz |
| Operativsystem | ingen | Windows / macOS / Linux |

Med 2 KB RAM kan du ikke ta lett på minne. Det driver de to neste forskjellene.

---

## Standardbiblioteket er stort sett fraværende

På et lite kort er de delene av standardbiblioteket denne boka lener seg på **ikke tilgjengelige, eller ikke tilrådelige**:

- **Ingen `<iostream>`** — skriv ut med `Serial` (over).
- **`std::vector`, `std::map`, `std::string`** er som regel utilgjengelige på AVR, og der de finnes, allokerer de på heap — risikabelt med 2 KB RAM. Foretrekk **vanlige arrayer med fast størrelse** (`int buf[32]`) og **faste buffere**.
- **Unntak og RTTI** (`dynamic_cast`, `typeid`) er vanligvis slått **av** som standard.
- **Unngå `new` / `delete` og dyp rekursjon** — heap-fragmentering og stack-overflyt er reelle farer på en 2 KB-enhet.

### Arduino `String` vs `std::string`

Arduino tilbyr en `String`-klasse (stor **S**) som ser vennlig ut, men som allokerer på heap og fragmenterer minnet på små kort. For alt som kjører lenge, foretrekk C-stil-strenger (`char buf[32]`) eller faste buffere. Dette er det *motsatte* av desktop-rådet ("grip etter `std::string`") — fordi begrensningene er motsatte.

---

## Heltallsstørrelser biter deg

På desktop og på 32-bits kort er `int` 32 bits. **På en 8-bits AVR er `int` bare 16 bits** — dens største verdi er 32767.

```cpp
int x = 40000;   // desktop / ESP32: greit.  Uno: flyter over — int topper ut på 32767
```

Når den eksakte størrelsen betyr noe — og på en mikrokontroller gjør den ofte det — bruk heltallstypene med fast bredde, som betyr det samme på hver brikke. Navnene er identiske på begge sider; bare headeren er forskjellig. På desktop, `#include <cstdint>`. På en Arduino finnes det ingen `<cstdint>` — bruk C-headeren `<stdint.h>` i stedet (og en skisse inkluderer den allerede for deg, så `uint8_t` og venner fungerer uten videre):

| Type | Bits | Område |
|------|------|--------|
| `uint8_t`  | 8  | 0 … 255 |
| `int16_t`  | 16 | −32768 … 32767 |
| `uint16_t` | 16 | 0 … 65535 |
| `int32_t`  | 32 | ±2,1 milliarder |

Også på AVR: `double` er bare 32 bits (det samme som `float`), så den bærer mindre presisjon enn 64-bits `double` du får på desktop.

---

## Intet operativsystem, og det kjører for alltid

- **Ingen filer, ingen kommandolinje, ingen terminal** — kortet snakker med verden gjennom pinnene sine og `Serial`, ikke et filsystem.
- **`delay(1000)` blokkerer** hele programmet i ett sekund. For alt som må holde seg responsivt, les klokka med `millis()` i stedet for å blokkere.
- **Koden din er hele programmet.** Det finnes intet OS å returnere til; `loop()` stopper rett og slett aldri.

```cpp
// Arduino-bibliotekfunksjoner du vil se (deklarert i <Arduino.h>):
pinMode(13, OUTPUT);
digitalWrite(13, HIGH);
int v = analogRead(A0);
delay(500);
unsigned long now = millis();
```

`pinMode`, `digitalWrite`, `analogRead`, `delay` og `millis` er Arduino-*bibliotek*funksjoner, ikke en del av C++ — de finnes ikke på desktop. Hele settet Arduino-kjernen leverer — hver innebygd funksjon, konstant og type — er dokumentert i [Arduino-språkreferansen](https://docs.arduino.cc/language-reference/).

---

## Ikke alle kort er like

"Arduino" spenner over svært forskjellig maskinvare, og begrensningene over letter raskt på mer kapable kort:

| Kort | Brikke | `int` | RAM | Standardbibliotek / STL |
|-------|------|-------|-----|------------------------|
| Uno / Nano / Mega | 8-bits AVR | 16-bits | 2–8 KB | stort sett fraværende |
| ESP32 | 32-bits Xtensa | 32-bits | ~520 KB | mye av STL fungerer |
| Teensy 4.x | 32-bits ARM | 32-bits | ~1 MB | mye av STL fungerer |
| Raspberry Pi Pico | 32-bits ARM | 32-bits | 264 KB | mye av STL fungerer |

På et 32-bits kort med hundrevis av KB RAM ser koden mye mer ut som desktop-C++-en i denne boka — `int` er 32 bits, `std::string` og `std::vector` er brukbare, flyttall har full presisjon. 8-bits Uno er det strenge tilfellet: behandle begrensningene dens som utgangspunktet, og slakk på dem bare når kortet ditt tillater det.

---

## Hva du tar med deg

- **Språket overføres fullstendig.** Din forståelse av typer, kontrollflyt, funksjoner, klasser, referanser og `const` er nøyaktig den samme på begge.
- **Minnedisiplin er den nye vanen.** På et lite kort: unngå heap, foretrekk lagring med fast størrelse, og hold øye med heltallsbredder.
- **Kortet avgjør hvor desktop-aktig det føles.** Sjekk brikken (8-bits AVR vs 32-bits) — det forteller deg hvilke regler som gjelder.
- For verktøykjeden som bygger og laster opp Arduino-kode fra en ekte IDE, se [PlatformIO](Chapter2/platformio.md).

---

## Oppsummering

- Arduino *er* C++ — samme språk, annet miljø.
- Du skriver `setup()` (én gang) og `loop()` (for alltid) i stedet for `main()`.
- Skriv ut med `Serial`, ikke `std::cout`.
- Små 8-bits kort har ~2 KB RAM: unngå heap, `std::string` og `std::vector`; foretrekk faste buffere og vanlige arrayer.
- `int` er 16-bits på AVR — bruk typer med fast bredde (`uint8_t`, `int32_t`, …, fra `<stdint.h>`) når størrelsen betyr noe.
- 32-bits kort (ESP32, Teensy, Pico) opphever de fleste av disse begrensningene og føles mye nærmere desktop-C++.
