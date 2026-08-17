# PlatformIO

Når du skriver C++ for en desktop-maskin, følger kompilatoren med IDE-en din, og "bygg" betyr "produser en kjørbar fil for maskinen du sitter ved". Å skrive C++ for en Arduino, en ESP32, en Teensy eller et hvilket som helst annet innebygd kort er mer innviklet: du trenger en **krysskompilator** som produserer kode for en annen CPU, biblioteker skrevet for det spesifikke kortet, og en måte å flashe den resulterende binærfilen over på enheten.

**PlatformIO** er verktøyet som skjuler all denne kompleksiteten bak et enhetlig grensesnitt. Velg kortet ditt, skriv koden din, trykk bygg. PlatformIO vet hvilken verktøykjede som skal brukes, hvilke biblioteker som skal hentes, og hvordan opplastingen til enheten gjøres.

Denne siden handler om *verktøyene*. For hvordan selve C++-en er annerledes på en mikrokontroller — `setup()`/`loop()` i stedet for `main()`, knapt med minne, et i stor grad manglende standardbibliotek — se [Arduino vs. desktop-C++](../arduino_vs_desktop.md).

---

## Hvorfor bruke PlatformIO? {#why-use-platformio}

Du kommer til å se to vanlige måter å programmere et Arduino-aktig kort på:

| Tilnærming | Fordeler | Ulemper |
|----------|------|------|
| **Arduino IDE** | Innebygd, enkel | Begrenset editor, svak prosjektstruktur, vanskelig å håndtere avhengigheter |
| **PlatformIO** | Ordentlig IDE-integrasjon, avhengighetshåndtering, prosjekter med flere kort, skriptbare bygg | Litt mer oppsett |

For alt utover en sketch på én fil er PlatformIO det riktige verktøyet. Det integreres også rent i CLion, IDE-en du allerede bruker til desktop-C++, som betyr at du kan skrive kode for både desktop-simuleringen din og det innebygde målet i samme editor.

---

## Installasjon {#installation}

Følg [installasjonsveiledningen for PlatformIO Core (CLI)](https://docs.platformio.org/en/latest/core/installation/index.html). To ting du må gjøre som veiledningen kanskje underspiller:

1. **Installer shell-kommandoene.** Uten dem kan du ikke kjøre `pio` fra terminalen. Installasjonssiden har en tydelig seksjon merket "Install Shell Commands."
2. **Start maskinen på nytt eller åpne en ny terminal** etter installasjonen, slik at de nye kommandoene er på `PATH`-en din.

For å verifisere installasjonen:

```bash
pio --version
```

---

## Bruke PlatformIO med CLion {#using-platformio-with-clion}

CLion har førsteklasses støtte for PlatformIO via [PlatformIO for CLion-pluginen](https://plugins.jetbrains.com/plugin/13922-platformio-for-clion), bygd i samarbeid med PlatformIO-teamet.

Installer pluginen fra CLions marketplace, og følg deretter CLions [oppsettsveiledning for PlatformIO](https://www.jetbrains.com/help/clion/platformio.html#install). Etter installasjonen kan du opprette nye PlatformIO-prosjekter fra CLions "New Project"-dialog på samme måte som du oppretter desktop-C++-prosjekter.

---

## Anatomien til et PlatformIO-prosjekt {#anatomy-of-a-platformio-project}

Et PlatformIO-prosjekt har en `platformio.ini`-fil i roten som beskriver målkortet og eventuelle biblioteker som trengs:

```ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino

lib_deps =
    arduino-libraries/Servo @ ^1.2.1
```

Hva hver linje gjør:

- `[env:uno]` definerer et byggemiljø kalt `uno`. Du kan ha flere miljøer i ett prosjekt (f.eks. ett for en Uno, ett for en ESP32) og bytte mellom dem.
- `platform` er CPU-familien. `atmelavr` for klassiske Arduinoer, `espressif32` for ESP32, osv.
- `board` er det spesifikke kortet. PlatformIO støtter hundrevis; se deres [kortsøk](https://platformio.org/boards).
- `framework` er hva slags kode du skriver. `arduino` gir deg Arduino-API-et; `espidf` gir deg ESP-IDF; noen kort støtter begge.
- `lib_deps` lister biblioteker som skal hentes automatisk. PlatformIO laster dem ned ved neste bygg.

Kildekoden bor i `src/`. Arduino-sketchen du normalt ville kalt `MyProject.ino`, blir `src/main.cpp`:

```cpp
#include <Arduino.h>

void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}
```

(Den eneste praktiske forskjellen fra en `.ino`-sketch er at du må inkludere `<Arduino.h>` eksplisitt.)

---

## Arbeidsflyten bygg / last opp / overvåk {#the-build-upload-monitor-workflow}

Fra CLion gjør den grønne play-knappen alt. Fra kommandolinjen:

```bash
pio run                    # bygg for standardmiljøet
pio run -t upload          # bygg og last opp til det tilkoblede kortet
pio device monitor         # åpne en seriemonitor (Ctrl+C for å avslutte)
```

Det meste av innebygd utvikling følger syklusen: rediger, bygg, last opp, se på serieutskriften, gjenta.

---

## Videre lesning {#further-reading}

- [PlatformIO-dokumentasjonen](https://docs.platformio.org/): omfattende.
- [Støttede kort](https://platformio.org/boards): søkbar liste.
- [PlatformIOs bibliotekregister](https://registry.platformio.org/): der `lib_deps` løses opp fra.

PlatformIO er sitt eget økosystem; dette kapittelet er bare en døråpning. Når du starter det innebygde prosjektet ditt, regn med å bruke en kveld med PlatformIOs dokumentasjon — det betaler seg for resten av prosjektet.
