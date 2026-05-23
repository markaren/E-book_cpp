# Kom i gang

For å skrive C++ trenger du to ting: en **kompilator** — programmet som gjør C++-en du skriver om til en *kjørbar fil*, en fil datamaskinen din faktisk kan kjøre — og et sted å skrive og kjøre koden. Dette emnet bruker **CLion**, en IDE (Integrated Development Environment: applikasjonen du skriver, bygger, kjører og feilsøker kode i). CLion kommer med alt du trenger innebygd, så oppsettet er kort.

Denne siden tar deg fra ingenting til et kjørende "Hello, World!". JetBrains' [hurtigstartveiledning](https://www.jetbrains.com/help/clion/clion-quick-start-guide.html) viser de samme stegene med skjermbilder hvis du vil følge med visuelt.

---

## 1. Installer CLion

1. Last ned CLion fra [jetbrains.com/clion](https://www.jetbrains.com/clion/) og kjør installasjonsprogrammet med standardvalgene.
2. CLion er **gratis for studenter**. Første gang det starter, blir du bedt om å logge inn — opprett en gratis JetBrains-konto og aktiver den gratis lisensen via [JetBrains' utdanningsprogram](https://www.jetbrains.com/community/education/#students).

<!-- screenshot: CLion førstegangs-/innloggingsskjerm -->

CLion har også med **CMake** (byggeverktøyet emnet bruker), så det trenger du ikke installere separat. Den eneste delen som avhenger av operativsystemet ditt, er kompilatoren — **klikk fanen for ditt OS**:

=== "Windows"

    **Ingen separat kompilator å installere.** CLion leverer en **MinGW**-verktøykjede og setter den opp ved første oppstart — godta standardvalget den foreslår. (Hvis verktøykjedelisten noen gang er tom, viser avsnittet *Hvis noe gikk galt* nederst hvordan du legger til MinGW.)

    *Avansert, valgfritt:* du kan i stedet bruke Microsofts MSVC-kompilator fra [Visual Studio](https://visualstudio.microsoft.com/vs/community/). Hopp over dette med mindre instruktøren din spesifikt ber om det — den innebygde kompilatoren holder til alt i denne boken.

=== "macOS"

    Installer Apples kommandolinjeverktøy for utviklere, som inkluderer Clang-kompilatoren. Åpne **Terminal**-appen og kjør:

    ```
    xcode-select --install
    ```

    Følg instruksjonen. CLion oppdager så kompilatoren automatisk.

=== "Linux"

    Installer GCC-kompilatoren og byggeverktøyene. På Debian/Ubuntu, åpne en terminal og kjør:

    ```
    sudo apt-get update && sudo apt-get install build-essential
    ```

    CLion oppdager så kompilatoren automatisk.

---

## 2. Lag ditt første prosjekt

1. På velkomstskjermen, velg **New Project** (eller **File → New Project** hvis CLion allerede er åpent).
2. Velg **C++ Executable**.
3. Hvis dialogen tilbyr et **Language standard**-valg, velg **C++20**. (Ikke alle versjoner gjør det — uansett, når prosjektet åpner, sjekk at `CMakeLists.txt` har `set(CMAKE_CXX_STANDARD 20)`; hvis linjen viser et lavere tall som `14` eller `17`, endre det til `20`.)
4. Velg en plassering for prosjektet — men les advarselen nedenfor først — og klikk **Create**.

<!-- screenshot: New Project-dialogen med "C++ Executable" valgt -->

> **Hvor du skal legge prosjektet.** Unngå en mappe inne i skylagring (OneDrive, Dropbox, Google Drive). Bygging lager et stort antall filer som ville synkronisert hele tiden, og hvis du bruker mer enn én PC skaper de maskinspesifikke byggefilene konflikter. Unngå også stier med mellomrom eller spesialtegn — inkludert norske `æ`, `ø`, `å` — som gir forvirrende feil på Windows. En enkel sti som `C:\dev\projects` er ideell. ([Datamaskingrunnlag](computer_basics.md) forklarer hvorfor stier, mellomrom og spesialtegn har betydning.)

CLion lager et "Hello, World!"-startprosjekt for deg, med to filer:

```cmake
# CMakeLists.txt — forteller byggeverktøyet hvordan programmet ditt skal bygges
cmake_minimum_required(VERSION 3.20)
project(demo)

set(CMAKE_CXX_STANDARD 20)

add_executable(demo main.cpp)
```

```cpp
// main.cpp — programmet ditt
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

Ikke bry deg om hva hver linje betyr ennå — [Grunnstruktur](Chapter1/basic_structure.md) bryter programmet ned bit for bit, og [CMake-introduksjon](Chapter2/cmake_intro.md) dekker `CMakeLists.txt`. (CLion genererer `std::endl`; denne boken skriver vanligvis `'\n'` i stedet. Begge avslutter linjen — forskjellen betyr ikke noe ennå.)

---

## 3. Bygg og kjør

C++ må **kompileres** til en kjørbar fil før det kan kjøre. CLion gjør begge deler med ett klikk:

- Klikk den grønne **▶ Run**-knappen øverst til høyre (eller trykk **Shift+F10**).
- Hammerikonet ved siden av *bygger* uten å kjøre, hvis du noen gang vil det.

<!-- screenshot: verktøylinjen øverst til høyre med Run- (play) og Build- (hammer) knappene -->

---

## 4. Sjekk at det virket

**Run**-vinduet åpner seg nederst i CLion og bør vise noe slikt som:

```
Hello, World!

Process finished with exit code 0
```

`exit code 0` betyr at programmet kjørte uten feil. Ser du det, virker oppsettet ditt, og du er klar for [Introduksjonen](Chapter1/introduction.md).

<!-- screenshot: Run-vinduet som viser utskriften og "exit code 0" -->

---

## Hvis noe gikk galt

De vanligste problemene ved første kjøring:

- **"No toolchain configured" eller kompilatoren finnes ikke.** Åpne **File → Settings → Build, Execution, Deployment → Toolchains**. På Windows bør det være en innebygd **MinGW**-oppføring; hvis den mangler, klikk **+** og legg den til. På macOS/Linux, sørg for at du installerte kompilatoren fra fanen i steg 1.
- **En rød feil dukker opp i CMake-panelet nederst.** Dette er nesten alltid en dårlig prosjektplassering — en sti med mellomrom eller spesialtegn, eller en skylagringsmappe. Slett prosjektet og lag det på nytt i en enkel sti som `C:\dev\projects`.
- **Run-knappen er grå eller ingenting skjer.** CLion holder sannsynligvis fortsatt på å laste prosjektet — vent til fremdriftslinjen nederst er ferdig, og prøv igjen.
- **Fortsatt fast på en feilmelding.** Les [Lese kompilatorfeil](compiler_errors.md), og kopier så den *nøyaktige* feilteksten inn i en søkemotor — eller inn i en KI-assistent, og følg [Bruke KI til koding](using_ai.md).
