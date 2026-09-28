# Prosjekt: Se tanken din i aksjon

Alt du har skrevet så langt, har snakket med deg gjennom en konsoll. Dette prosjektet gir det et vindu.

Du tar [tankreguleringssystemet](tank_control/v1_classes.md) — anlegget, sensoren, regulatoren, testene — og bygger en **3D-visning** rundt det med [threepp](https://github.com/markaren/threepp), et C++-bibliotek med samme API som det populære JavaScript-biblioteket *three.js*. Når du trykker Run, dukker en tank opp, vannet stiger i den, en ventil skifter farge når den åpner og lukker, og nivået legger seg på settpunktet foran øynene dine.

Poenget er ikke grafikken. Poenget er hva du må endre i simuleringskoden din for å koble den til: **ingenting.** `Tank`, `Plant`, `PIDController` og testene deres kompilerer uendret, fordi de aldri visste hvor tallene deres tok veien. Det er [separasjon av ansvar](Chapter6/soc.md) som lønner seg, og det er mye lettere å tro på når du ser det. Hva som skjer når simuleringen *kjører* inne i en ekte animasjonsløkke, er en annen historie, og å finne ut av det er en del av prosjektet.

!!! info "Når siden brukes i et emne"

    Milepælene gir deg et fungerende utgangspunkt. Det du bygger utover dem, og hvor godt du viser og forklarer hvordan du jobbet, er prosjektet ditt. Tar du AIS1003, sier mappeoppgaven hva du skal levere og hvordan det vurderes.

Du bygger det i to deler:

- **Del 1** — få opp et vindu med noe som beveger seg i: en ekte tredjepartsavhengighet hentet inn med CMake, en scene, et kamera og en animasjonsløkke. Del 1 trenger ingen tankkode, så du kan starte før tankprosjektet er ferdig.
- **Del 2** — hent inn tankprosjektet ditt fra versjon 5, koble visningen til simuleringen, finn ut hvorfor det ikke virker første gang, bytt regulator mens programmet kjører, og vis tallene på skjermen — med Catch2-testene fortsatt grønne.

Etter det kommer delen som er din: en [utvidelse](#your-extension) du velger og designer selv, og en README som [presenterer det du har laget](#present-your-project).

Ta milepælene i rekkefølge; hver av dem legger til én ting. **Prøv selv før du ser på løsningen** — løsningene er uskarpe; klikk én gang til for å se dem. Ser du på en løsning, skriv den inn i stedet for å lime den inn, og noter i loggen hva du sto fast på.

---

## Dette skal du bygge {#what-youll-build}

En stående tank, en vannsøyle som stiger og synker med nivået i anlegget, et rødt bånd ved settpunktet, og en ventilkloss som går fra grønn (lukket) til rød (helt åpen). Trykk `1`, og regulatoren blir av/på; trykk `2`, og PID-regulatoren tar over. Hvordan forskjellen ser ut med 60 bilder i sekundet, finner du ut i milepæl 6.

En tekstlinje øverst viser:

```
PID | level 4.87 m | setpoint 5.00 m | valve 70%
```

---

## Slik jobber du med prosjektet {#how-to-work-on-this-project}

Veien dit betyr like mye som hvor du ender, og det er lett å ikke etterlate noen spor av den. Fire vaner, fra første milepæl:

- **Commit etter hver milepæl**, og hver gang noe begynner å virke, med en melding som sier *hvorfor* ([Lagre arbeidet ditt](Chapter2/version_control.md#saving-your-work-a-commit)). Historikken er prosjektets dagbok; én enkelt commit med "ferdig versjon" forteller ingen noe. **Push** på slutten av hver økt — **Commit and Push...** i CLions commit-dialog — så historikken er sikkerhetskopiert på GitHub, ikke bare på din egen PC. Når du når et punkt som er verdt å huske — del 1 kjører, kjernen er ferdig, utvidelsen din virker — setter du en [tag](Chapter2/version_control.md#tags-naming-a-commit) på det, med noen linjer om hva som virker, hva som var vanskelig, og hva du planlegger videre.
- **Før logg.** En fil `LOG.md` i prosjektets øverste mappe, ved siden av `CMakeLists.txt` på toppnivå, med en kort føring per arbeidsøkt. Det er et eksempel etter milepæl 4. Denne malen holder:

    ```markdown
    ### <dato> — <hva du jobbet med> (<tid brukt>)
    **Forventet:** <bare hvis du forutså noe før du kjørte>
    **Prøvde:**
    **Skjedde:**
    **Hvorfor tror jeg:**
    **Hvordan jeg sjekket:**
    **Endret:** <hva, og commiten>
    **Neste:**
    ```

- **Forutsi før du kjører.** Der en milepæl har en *Før du kjører*-boks, skriver du forventningen din i loggen og **committer den før du kjører** — da viser historikken hva du forventet før du så hva som skjedde. En feil forventning koster ingenting; det er når du finner ut hvorfor den var feil, at du lærer noe.
- **Ta bilder underveis.** Ta et skjermbilde eller spill inn en kort GIF hver gang noe virker — eller går i stykker på en interessant måte. Du trenger dem til [README-en](#present-your-project), og du kan ikke ta bilde av en feil etter at du har rettet den.

Når du står fast, gå i denne rekkefølgen: de [fire verktøyene for "noe er galt"](debugger.md#four-tools-for-something-is-wrong), så [Lese kompilatorfeil](compiler_errors.md), så [Bruke KI til koding](using_ai.md). Spør du en KI, skriv ned hva du spurte om og hva du beholdt.

---

## Før du begynner {#before-you-start}

- **Del 1** trenger [CMake](Chapter2/cmake_intro.md) og [Git](Chapter2/version_control.md) (kapittel 2), [lambdaer](lambdas.md) (kapittel 3), [klasser](Chapter4/classes.md), [referanser og pekere](Chapter4/types_refs_ptrs.md) og [RAII](Chapter4/raii.md) (kapittel 4), og [smartpekere](Chapter5/memory.md#smart-pointers) (kapittel 5). Den trenger **ikke** tankprosjektet. Noen av forklaringene i løsningene peker framover — til polymorfisme, Observatør-mønsteret og tankprosjektet. Har du ikke kommet dit ennå, hopp over de avsnittene; koden avhenger ikke av dem.
- **Del 2** trenger det ferdige **tankprosjektet**. Det er bokens gjennomgåtte eksempel [Tankreguleringssystem](tank_control/v1_classes.md) (i menyen etter kapittel 6): fem korte sider, *versjon 1* til *versjon 5*, der du bygger en regulator for en vanntank steg for steg, og hver versjon vokser ut av den forrige. Du følger sidene, skriver koden inn i et eget CLion-prosjekt og kjører det. Det denne siden kaller **versjon 5-prosjektet ditt**, er det CLion-prosjektet slik det står etter [versjon 5](tank_control/v5_tests.md): det med mappene `include/`, `src/`, `app/` og `tests/`, et `tank_lib`-bibliotek og grønne Catch2-tester. Tanksidene bygger på resten av kapittel 5 og 6. Har du ikke bygget tankprosjektet ennå, start på [versjon 1](tank_control/v1_classes.md) nå; du kan gjøre del 1 av dette prosjektet mens du jobber deg gjennom det.

!!! warning "Første bygg tar tid"

    Første gang CMake konfigurerer prosjektet, **laster det ned** threepp (rundt 200 MB — du trenger internett), og første bygg **kompilerer** det, noe som tar **flere minutter**. Start bygget og les videre. Det skjer én gang per byggemappe: CLion har én mappe per profil (`cmake-build-debug`, `cmake-build-release`), så en ny profil, **Tools → CMake → Reset Cache and Reload Project**, eller å slette mappen starter det på nytt.

!!! note "Hva maskinen din trenger"

    threepp tegner med **OpenGL 3.3**, som alle grafikkort fra det siste tiåret støtter. Det virker ikke over Remote Desktop eller i en virtuell maskin uten 3D-akselerasjon — kjør dette på din egen maskin.

??? question "Hvis første konfigurering eller bygg feiler"

    - **Nedlastingen feiler** ("could not resolve host", "failed to clone"): du har ikke internett, eller nettet vil at du skal logge inn først — åpne en nettside i nettleseren, og velg så **Reload CMake Project**.
    - **"git not found"**: CMake bruker Git til å laste ned threepp. Installer Git for Windows fra <https://git-scm.com/downloads> (standardvalgene er fine) og start CLion på nytt.
    - **Rare feil om filstier**: prosjektet ligger i OneDrive, eller stien har mellomrom eller `æ`, `ø`, `å` — se [Kom i gang](getting_started.md#2-create-your-first-project).
    - **Et vindu som aldri dukker opp**, eller en feil om OpenGL: du er på Remote Desktop eller i en virtuell maskin (se boksen over).

---

# Del 1 — Et vindu med noe i {#part-1-a-window-with-something-in-it}

## Milepæl 1 — Hent threepp og åpne et vindu {#milestone-1-fetch-threepp-and-open-a-window}

*Øver på: [CMake](Chapter2/cmake_intro.md#consuming-third-party-libraries), [RAII](Chapter4/raii.md), [lambdaer](lambdas.md)*

1. Lag et nytt **C++ Executable**-prosjekt i CLion, kalt `tank-rig`, i en vanlig mappe som `C:\dev\tank-rig` ([Kom i gang](getting_started.md#2-create-your-first-project)).
2. **Legg det under Git** før første bygg: åpne **Terminal**-fanen nederst i CLion (den åpner i prosjektmappen) og skriv `git init` ([Starte et nytt prosjekt](Chapter2/version_control.md#starting-a-new-project)). Høyreklikk så `tank-rig` øverst i **Project**-panelet → **New → File**, kall filen `.gitignore`, og skriv to linjer i den: `cmake-build-*/` og `.idea/` ([Hva du skal legge i `.gitignore`](Chapter2/version_control.md#what-to-put-in-gitignore)). Lag et tomt **privat** repository på GitHub og koble det til over SSH ([Legg et lokalt prosjekt på GitHub](Chapter2/version_control.md#getting-a-project)).
3. Høyreklikk `tank-rig` → **New → Directory**, kall mappen `rig`, og dra `main.cpp` inn i den (bekreft **Move**-dialogen).
4. Åpne `CMakeLists.txt` på toppnivå. **Behold** linjene CLion skrev øverst: `cmake_minimum_required`, `project` og `set(CMAKE_CXX_STANDARD 20)` (viser den linjen et lavere tall, endre det til `20`, og mangler `set(CMAKE_CXX_STANDARD_REQUIRED ON)`, legg den til under, som i [Sette C++-standarden](Chapter2/cmake_intro.md#setting-the-c-standard)). Den siste linjen, `add_executable(...)`, passer ikke lenger, fordi `main.cpp` er flyttet: erstatt den med disse to linjene ([Dele opp bygget over flere mapper](Chapter2/cmake_intro.md#splitting-the-build-across-folders)):

    ```cmake
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    add_subdirectory(rig)
    ```

    Den første linjen legger programmet ditt i samme mappe som threepps DLL-er; løsningen under steg 5 forklarer hvorfor det er viktig.

5. Høyreklikk `rig` → **New → File**, og kall filen `CMakeLists.txt`. I den henter du inn threepp med `FetchContent`, akkurat slik CMake-kapitlet henter Catch2 i [Bruke tredjepartsbiblioteker](Chapter2/cmake_intro.md#consuming-third-party-libraries), og bygger en kjørbar fil `tank_rig` fra `main.cpp` som lenker mot threepp. Bare navnene endres:

    | Det mønsteret trenger | For threepp |
    |---|---|
    | navnet i `FetchContent_Declare` og `FetchContent_MakeAvailable` | `threepp` |
    | `GIT_REPOSITORY` | `https://github.com/markaren/threepp.git` |
    | `GIT_TAG` | `2026-09-28` |
    | targetet du lenker mot | `threepp::threepp` |

    Du kan også legge til `GIT_SHALLOW TRUE` under `GIT_TAG`: da lastes bare den låste versjonen ned, ikke hele historikken til threepp.

    Én ting Catch2 ikke trengte: legg disse tre linjene **før** `FetchContent_Declare`, så threepp bygges som en DLL med CLions MinGW-kompilator. Uten dem bruker hvert nytt bygg nesten et minutt på lenkingen.

    ```cmake
    if(MINGW)
        set(BUILD_SHARED_LIBS ON)
    endif()
    ```

    ??? success "Vis løsning: de to CMake-filene"

        <div class="spoiler" markdown title="Klikk for å avsløre">

        `CMakeLists.txt` (toppnivå; versjonen i `cmake_minimum_required` og navnet i `project` kan være annerledes enn det CLion skrev for deg, og det er helt greit):

        ```cmake
        cmake_minimum_required(VERSION 3.20)
        project(tank_rig)

        set(CMAKE_CXX_STANDARD 20)
        set(CMAKE_CXX_STANDARD_REQUIRED ON)

        set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)   # alle programmer i én mappe, ved siden av threepps DLL-er

        add_subdirectory(rig)      # 3D-visningen
        ```

        `rig/CMakeLists.txt`:

        ```cmake
        include(FetchContent)

        if(MINGW)
            set(BUILD_SHARED_LIBS ON)   # bygg threepp som en DLL, så et nytt bygg lenker på sekunder
        endif()
        FetchContent_Declare(
            threepp
            GIT_REPOSITORY https://github.com/markaren/threepp.git
            GIT_TAG        2026-09-28    # lås til en tag, aldri en bevegelig branch
            GIT_SHALLOW    TRUE          # hent bare de siste commitene, ikke hele historikken
        )
        FetchContent_MakeAvailable(threepp)

        add_executable(tank_rig main.cpp)
        target_link_libraries(tank_rig PRIVATE threepp::threepp)
        ```

        **`BUILD_SHARED_LIBS` og `bin`-mappen hører sammen.** threepp er et svært stort bibliotek. Bygget på vanlig måte — som et *statisk* bibliotek — kopieres det inn i programmet ditt hver gang programmet lenkes, og med MinGW gjør det at hvert nytt bygg tar nesten et minutt. Bygget som et *delt* bibliotek (en DLL på Windows) kompileres det én gang, og programmet ditt bare viser til det, så et nytt bygg lenker på noen sekunder. Haken: Windows finner bare en DLL som ligger ved siden av programmet (eller på `PATH`), så toppnivåfilen sender alle programmer til samme `bin`-mappe, der threepp allerede legger DLL-ene sine. Utelater du den linjen, starter programmet aldri: CLion rapporterer exit code `-1073741515` (`0xC0000135`), som er Windows sin måte å si "fant ikke en DLL". `if(MINGW)` begrenser endringen til CLions MinGW-kompilator, der den statiske lenkingen er tregest; andre kompilatorer beholder standarden.

        </div>

6. **Last inn CMake på nytt** — klikk på reload-ikonet CLion viser over editoren ([CMake i CLion](Chapter2/cmake_intro.md#cmake-in-clion)). Før du gjør det, kan CLion si at `main.cpp` ikke hører til noe target i prosjektet; det er forventet. Det er denne innlastingen som laster ned threepp, og **CMake**-vinduet nederst kan stå uten nye linjer i flere minutter. Vent til det skriver `Build files have been written to`.
7. I `rig/main.cpp` lager du et `Canvas` (vinduet), en `GLRenderer`, en `Scene` med bakgrunnsfarge og et `PerspectiveCamera`, og gir animasjonsløkken en lambda som tegner ett bilde.

> Tips: threepp-navnene — `Canvas`, `Scene`, `canvas.animate` — kan du ikke gjette ut fra noe i denne boken. Se på et av threepps eksempler ([Finn ut av ting selv](#finding-things-out-yourself)), eller åpne løsningen og skriv den inn; i milepæl 1 er det forventet. Én advarsel når du låner fra et eksempel: threepps eksempler har `#include "renderer_factory.hpp"` og lager rendereren med `auto renderer = createRenderer(canvas);`. Den hjelpefunksjonen er ikke en del av biblioteket — den ligger ved siden av eksemplene — og den stopper og **spør i konsollen** hvilken renderer du vil bruke før noe tegnes. Dropp include-linjen, skriv `GLRenderer renderer(canvas);` i stedet, og `renderer.` der eksemplet skriver `renderer->`.

!!! example "Kjør — dette skal du se"

    Et tomt vindu i bakgrunnsfargen du valgte, som du kan endre størrelse på og lukke. Ikke noe annet. Det er milepælen. Commit den — commiten skal bare inneholde `.gitignore`, de to `CMakeLists.txt`-filene og `rig/main.cpp`; ser du filer fra `cmake-build-debug`, virker ikke `.gitignore`-filen din — og push.

??? success "Vis løsning: main.cpp"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    `rig/main.cpp`:

    ```cpp
    #include "threepp/threepp.hpp"

    using namespace threepp;

    int main() {
        Canvas canvas("Tank Rig");
        GLRenderer renderer(canvas);

        auto scene = Scene::create();
        scene->background = Color::aliceblue;

        auto camera = PerspectiveCamera::create(60, canvas.aspect(), 0.1f, 1000);
        camera->position.set(0, 5, 12);

        canvas.onWindowResize([&](WindowSize size) {
            camera->aspect = size.aspect();
            camera->updateProjectionMatrix();
            renderer.setSize(size);
        });

        canvas.animate([&] {
            renderer.render(*scene, *camera);
        });
    }
    ```

    Verdt å merke seg:

    - **`Canvas` eier vinduet.** Når `canvas` ødelegges på slutten av `main`, lukkes vinduet og ressursene frigjøres — du rydder aldri opp for hånd, samme idé som `std::ofstream` i [RAII](Chapter4/raii.md). `GLRenderer` tegner i det vinduet og rydder opp etter seg på samme måte.
    - **Lag `GLRenderer` selv, som her** — ikke med hjelpefunksjonen `createRenderer(canvas)` som threepps eksempler bruker. Den ligger i eksemplenes egen `renderer_factory.hpp`, ikke i biblioteket, og den venter på svar i konsollen før noe tegnes.
    - **`Scene::create()` og `PerspectiveCamera::create()` gir deg smartpekere**, og derfor skriver du `scene->` og `*scene`. Milepæl 2 sier hvilken type, og hvorfor.
    - **`canvas.animate(...)` tar en [lambda](lambdas.md)** og kaller den én gang per bilde til du lukker vinduet. `[&]` fanger `renderer`, `scene` og `camera` by reference — trygt her, fordi alle lever lenger enn løkken.
    - **`onWindowResize` tar en callback**: du gir canvaset en funksjon, og det kaller deg tilbake når noe skjer. Du spør ikke etter endringer i vindusstørrelsen; du abonnerer på dem. (Kapittel 6 kaller dette [Observatør-mønsteret](Chapter6/observer.md).)
    - **`using namespace std;` er fortsatt forbudt; `using namespace threepp;` i denne ene `.cpp`-filen er et bevisst unntak.** threepps namespace er ikke lite — det har hundrevis av navn, mange av dem vanlige ord som `Color`, `Clock` og `Group` — så begrunnelsen i [kapitlet om standardbiblioteket](Chapter3/standard_library.md) gjelder her også. Det er akseptabelt her fordi det står i én kildefil (aldri i en header), du bruker threepp-navn på nesten hver linje, og ingen av dem kolliderer med dine. Skjer det likevel, sier kompilatoren at navnet er *ambiguous*: gi din egen klasse et annet navn, eller fjern `using namespace threepp;` fra den filen og skriv `threepp::` foran threepps navn.

    </div>

## Milepæl 2 — Legg noe i scenen {#milestone-2-put-something-in-the-scene}

*Øver på: [Minnehåndtering](Chapter5/memory.md), [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md)*

En tom scene er ikke mye. Legg til en boks: lag en **geometri** (formen), et **materiale** (hvordan den ser ut), sett dem sammen til en `Mesh`, og `add` den til scenen. Legg til et `DirectionalLight` og et `AmbientLight` også, ellers blir et belyst materiale svart. Til slutt kobler du på `OrbitControls`, så du kan dra med musen for å gå rundt kameraet og scrolle for å zoome.

> Tips: `BoxGeometry::create(w, h, d)`, `MeshStandardMaterial::create()`, `Mesh::create(geometry, material)`. Hold **Ctrl** og klikk på `BoxGeometry::create` for å åpne deklarasjonen: hva annet kunne du gitt den? Og se på hvilken type disse `create`-funksjonene gir deg tilbake — den har du møtt før.

!!! example "Kjør — dette skal du se"

    En belyst blå boks du kan gå rundt ved å dra med musen.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    Inne i `main`, etter kameraet:

    ```cpp
    OrbitControls controls{*camera, canvas};

    auto light = DirectionalLight::create();
    light->position.set(10, 20, 10);
    scene->add(light);
    scene->add(AmbientLight::create(0xffffff, 0.4f));   // hvitt lys med 40 % styrke

    auto geometry = BoxGeometry::create(2, 2, 2);
    auto material = MeshStandardMaterial::create();
    material->color = Color::dodgerblue;
    auto box = Mesh::create(geometry, material);
    scene->add(box);
    ```

    **Hver `create` returnerer en `std::shared_ptr`.** Det er derfor `auto` gjør så mye av jobben her, og derfor du når medlemmer med `->` i stedet for `.` — du holder en [smartpeker](Chapter5/memory.md#smart-pointers), og `box->position` betyr `(*box).position`, akkurat som [kapitlet om pekere](Chapter4/types_refs_ptrs.md#pointers-to-objects) beskrev.

    Det er en `shared_ptr` fordi **threepp valgte delt eierskap**: `scene->add(box)` lagrer en ny `shared_ptr` til den samme meshen, så scenen holder alt du legger i den i live, og `box`-variabelen din er bare en eier til. Ingen av dem bestemmer alene når meshen ødelegges — det gjør den siste eieren som slipper taket, som i [delt eierskap](Chapter5/memory.md#stdshared_ptr-shared-ownership). Du møter et tilfelle der delingen virkelig betyr noe i milepæl 6.

    `OrbitControls controls{*camera, canvas};` tar kameraet **by reference** — legg merke til `*`, som gjør `shared_ptr`-en om til selve kameraet igjen. `controls` låner kameraet og styrer det; den eier det ikke, og den må ikke leve lenger enn det. Her lever begge til slutten av `main`.

    </div>

## Milepæl 3 — Få det til å bevege seg {#milestone-3-make-it-move}

*Øver på: [Lambdaer](lambdas.md), [løkken i versjon 1](tank_control/v1_classes.md)*

Et stillbilde er ingen simulering. Legg til en `Clock`, spør den hvert bilde hvor lang tid som har gått, og roter boksen med en vinkel som er **proporsjonal med den tiden**.

> Tips: `Clock clock;` før løkken, `const float dt = clock.getDelta();` som første linje inne i den. Roter med `speed * dt`, ikke med en fast vinkel per bilde.

!!! question "Før du kjører"

    Tenk deg at du roterte boksen med en fast `0.01f` hvert bilde i stedet. Løkken kjører én gang per skjermoppdatering. Hvor fort ville boksen snudd seg på en 60 Hz-skjerm, og på en 144 Hz-skjerm? Skriv det ned, og les så forklaringen i løsningen.

!!! example "Kjør — dette skal du se"

    Boksen som snur seg jevnt.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    Clock clock;
    canvas.animate([&] {
        const float dt = clock.getDelta();
        box->rotation.y += 0.5f * dt;
        renderer.render(*scene, *camera);
    });
    ```

    **Hvorfor `* dt` og ikke bare `+= 0.01f`?** Fordi bildene ikke kommer i fast takt. Løkken kjører én gang per skjermoppdatering, så en 144 Hz-skjerm gir 144 bilder i sekundet og en 60 Hz-skjerm 60 — og en tung scene på en treg maskin gir færre. Et fast steg per bilde ville snurret mer enn dobbelt så fort på 144 Hz-skjermen. Ganger du med *tiden som har gått*, blir rotasjonen en halv radian per **sekund** på alle maskiner.

    Det er samme grunn til at `Tank::update` og `PIDController::compute` tar en `dt` i stedet for å anta en stegstørrelse — og det er derfor del 2 kan gi `clock.getDelta()` til kode du skrev for flere uker siden. Animasjonsløkken er *måle → bestemme → handle → steg*-løkken fra [versjon 1](tank_control/v1_classes.md), med en ekte klokke som driver den.

    </div>

## Milepæl 4 — Bygg riggen av deler {#milestone-4-build-the-rig-from-parts}

*Øver på: [Funksjoner](Chapter1/functions.md), komposisjon ([versjon 3](tank_control/v3_pid.md#a-plant-composition))*

Bytt ut boksen og rotasjonen med en tankrigg, satt sammen av fire mesher:

| Del | Form | Merknad |
|------|-------|-------|
| Skall | åpen sylinder, 8 m høy | gjennomsiktig, `Side::Double` så du ser innsiden |
| Vann | sylinder med høyde `1` | litt smalere enn skallet |
| Settpunktbånd | tynn, flat boks | ved `y = 5`, målnivået |
| Ventil | liten boks | over tanken |

Skriv én liten funksjon per del som bygger og returnerer meshen. Legg alle fire i en `Group`, og legg *gruppen* til scenen, så hele riggen beveger seg samlet.

Gjør vannet **4 m dypt** foreløpig: en sylinder bygget med høyde `1` blir `level` meter høy når du setter `scale.y = level`.

Kameraet ser fortsatt mot origo — bunnen av tanken. Pek `OrbitControls` mot midten av tanken i stedet: sett `controls.target` og kall `controls.update()`.

> Tips: `CylinderGeometry::create` bygger sylindrene. Skallet trenger *åpne* ender — Ctrl+klikk `create` og finn parameteren som gjør det. Du ser parametere skrevet som `unsigned int heightSegments = 1`: `= 1` er et **default argument**. Stopper kallet ditt før den parameteren, fyller kompilatoren inn verdien etter `=`. Du kan bare utelate argumenter helt til høyre, og C++ har ikke navngitte argumenter, så for å nå en parameter må du gi alle parameterne før den, i rekkefølge. `create(1, 1, 8, 32, true)` kompilerer uten advarsel, men den `true`-en havner ikke der du tror. `Group::create()` gir deg en beholder du kan `add` til, akkurat som scenen.

!!! example "Kjør — dette skal du se"

    En gjennomsiktig tank, 4 m blått vann som står på bunnen, et rødt bånd over den ved 5 m, og en grå kloss over den — alt i bildet, og riggen dreier rundt midten av tanken når du drar.

??? warning "Står du fast? Vannet stikker ut under bunnen"

    Sett `water->scale.y = 4`, og sylinderen vokser ikke opp fra bunnen — den vokser *begge* veier fra sitt eget sentrum, så halvparten synker under tanken og toppen havner på 2 m, ikke 4 m. Flytt den opp med halve høyden også: `water->position.y = 4.f / 2`.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    Mellom `using namespace threepp;` og `main`:

    ```cpp
    constexpr float tankRadius = 1.0f;
    constexpr float tankHeight = 8.0f;
    constexpr double setpoint = 5.0;

    std::shared_ptr<Mesh> createShell() {
        auto geometry = CylinderGeometry::create(tankRadius, tankRadius, tankHeight, 32, 1, true);
        auto material = MeshBasicMaterial::create();
        material->color = Color::lightgray;
        material->transparent = true;
        material->opacity = 0.25f;
        material->side = Side::Double;
        auto shell = Mesh::create(geometry, material);
        shell->position.y = tankHeight / 2;
        return shell;
    }

    std::shared_ptr<Mesh> createWater() {
        // høyde 1, så scale.y leses direkte som meter vann
        auto geometry = CylinderGeometry::create(tankRadius * 0.97f, tankRadius * 0.97f, 1.0f, 32);
        auto material = MeshStandardMaterial::create();
        material->color = Color::dodgerblue;
        return Mesh::create(geometry, material);
    }

    std::shared_ptr<Mesh> createValve() {
        auto geometry = BoxGeometry::create(0.6f, 0.6f, 0.6f);
        auto material = MeshStandardMaterial::create();
        material->color = Color::gray;
        auto valve = Mesh::create(geometry, material);
        valve->position.y = tankHeight + 0.5f;
        return valve;
    }

    std::shared_ptr<Mesh> createMarker() {
        auto geometry = BoxGeometry::create(2.6f, 0.05f, 2.6f);
        auto material = MeshBasicMaterial::create();
        material->color = Color::crimson;
        auto marker = Mesh::create(geometry, material);
        marker->position.y = static_cast<float>(setpoint);
        return marker;
    }
    ```

    `CylinderGeometry::create(radiusTop, radiusBottom, height, radialSegments, heightSegments, openEnded)`: skallet gir `1` for `heightSegments`, slik at `true` havner på `openEnded`. I det fristende `create(1, 1, 8, 32, true)` blir `true` til `heightSegments = 1`, og skallet beholder endelokkene.

    Og i `main` — controls-linjen er der allerede fra milepæl 2; legg til de to linjene etter den:

    ```cpp
    OrbitControls controls{*camera, canvas};
    controls.target.set(0, tankHeight / 2, 0);   // dreie rundt midten av tanken
    controls.update();

    // ...lysene som før...

    auto rig = Group::create();
    auto water = createWater();
    rig->add(createShell());
    rig->add(water);
    rig->add(createValve());
    rig->add(createMarker());
    scene->add(rig);

    water->scale.y = 4.f;         // 4 m vann, foreløpig
    water->position.y = 4.f / 2;  // ...med bunnen på tankbunnen
    ```

    Løkken går tilbake til bare `renderer.render(*scene, *camera);`.

    **En scene er et tre: en gruppe *har* barn.** `rig` har et skall, en vannsøyle og en ventil. Flytt `rig`, og alle barna flytter seg med — sett `rig->position.x = 3`, og hele sammenstillingen glir sidelengs, fortsatt satt sammen, fordi et barns posisjon måles relativt til forelderen. Å "bygge en større ting av mindre ting, der hver beholder sin egen jobb" er akkurat det `Plant` gjorde med `Tank` og `Valve` i [versjon 3](tank_control/v3_pid.md#a-plant-composition) — samme designidé, én gang i fysikk og én gang i geometri.

    Skallet bruker `MeshBasicMaterial` (ignorerer lys — riktig for en gjennomsiktig flate), mens vannet bruker `MeshStandardMaterial` (belyses, så det ser massivt ut). `Mesh` holder materialet sitt gjennom en peker til basisklassen `Material`, så alle slags materialer passer inn — substitusjon gjennom en basisklassepeker, som i [Polymorfisme](Chapter5/polymorphism.md). (Hvilken shader som tegner det, avgjøres så inne i rendereren.)

    Bare `water` trenger en navngitt variabel; de tre andre legges til og glemmes. De holdes i live fordi `Group` holder en `shared_ptr` til hver av dem.

    </div>

### Slik ser en loggføring ut {#what-a-log-entry-looks-like}

Vannfellen over gir en god første loggføring. Noe slikt — rundt hundre ord, med dine egne ord, om hva som skjedde på din maskin:

```markdown
### 14. okt — Milepæl 4, vannsøylen (1,5 t)
**Prøvde:** bygde vannet som en sylinder med høyde 1 og satte `water->scale.y = 4`.
**Skjedde:** vannet stakk ut under bunnen; toppen var på 2 m, ikke 4 m.
Skjermbilde: docs/images/m4_water_below.png
**Hvorfor tror jeg:** sylinderen vokser kanskje fra sentrum, ikke fra bunnen.
**Hvordan jeg sjekket:** prøvde `scale.y = 2`, så `6` — bunnen gikk like langt ned som toppen gikk opp.
**Endret:** `water->position.y = 4.f / 2` (halve høyden) — commit 3f2a9c1
("Løft vannet med halve høyden så det vokser fra bunnen").
**Neste:** styre nivået fra anlegget (milepæl 5).
```

En nøyaktig observasjon, en gjetning, et lite eksperiment som tester gjetningen, og en retting med et *hvorfor* i commit-meldingen. Det er det "å vise prosessen" betyr.

Del 1 er et komplett 3D-program i seg selv — et godt sted å committe, ta et skjermbilde, sette en tag, og se tilbake på det du har bygget.

---

# Del 2 — Styr det med din egen kode {#part-2-drive-it-with-your-own-code}

## Milepæl 5 — Koble til simuleringen {#milestone-5-plug-in-the-simulation}

*Øver på: [Separasjon av ansvar](Chapter6/soc.md), [Polymorfisme](Chapter5/polymorphism.md), [Bruke en debugger](debugger.md)*

Dette er milepælen hele prosjektet finnes for.

1. **Hent inn versjon 5-prosjektet ditt**: CLion-prosjektet du bygget ved å følge bokens sider om [tankreguleringssystemet](tank_control/v1_classes.md) fram til [versjon 5](tank_control/v5_tests.md) (se [Før du begynner](#before-you-start)). Commit del 1 først. Kopier så, i Filutforsker, bare disse fire mappene fra det prosjektets mappe inn i `tank-rig`-mappen, ved siden av `rig/`: `include/`, `src/`, `app/` og `tests/`. La `CMakeLists.txt` på toppnivå fra versjon 5 ligge igjen — `tank-rig` beholder sin egen, og steg 2 utvider den — og la `.git`-, `.idea`- og `cmake-build-*`-mappene ligge igjen også. Commit de fire mappene i en egen commit, uten noe annet i den. Kryss av for **Unversioned Files** i commit-dialogen, så alle de kopierte filene kommer med, og start meldingen med `Import:` — for eksempel `Import: tankprosjektet mitt fra versjon 5 (include, src, app, tests)`. Alt etter den commiten er nytt arbeid, og alle som leser historikken din, ser nøyaktig hvor det starter.
2. **Koble opp bygget.** I `CMakeLists.txt` på toppnivå legger du til `src`, `app` og `tests` ved siden av `rig`. Ikke legg til `include`: den har ingen egen `CMakeLists.txt`, og `src/CMakeLists.txt` peker allerede `tank_lib` dit. Slå på testing med `include(CTest)` *på toppnivå*, så `ctest` finner testene fra byggemappen. I `rig/CMakeLists.txt` lenker du mot `tank_lib` i tillegg til threepp. Last inn CMake på nytt (denne innlastingen laster ned Catch2).
3. **Styr vannet.** Inkluder headerne dine, lag en `Plant`, en `LevelSensor` som leser den, og en `PIDController`, og la en `Controller*` peke på PID-regulatoren — versjon 4 brukte en `Controller&`, men milepæl 6 trenger noe som kan pekes om. Hvert bilde: les sensoren, spør regulatoren om en ventilåpning, steg anlegget, og sett så vannets `scale.y` og `position.y` ut fra nivået i anlegget. De to "foreløpige" vannlinjene fra milepæl 4 kan fjernes; løkken setter vannet fra nå av.

**For å koble det til endrer du ingenting i `src/` eller `include/`.** Merker du at du endrer `Tank` eller `PIDController` for å få dette til å *kompilere*, stopp og les løkken i [versjon 4](tank_control/v4_project.md) på nytt — koden du trenger, er der allerede.

> Tips: løkkekroppen er måle-/bestemme-/handle-linjene fra `main` i versjon 4, med `std::cout` byttet ut med to tilordninger til `water`. Simuleringen din regner i `double`, threepp i `float`; skriv en `static_cast<float>` i overgangen, så innsnevringen blir synlig (kompilatoren ville gjort den i stillhet).

!!! example "Kjør — dette er hva du faktisk vil se"

    Skallet, det røde båndet og ventilen — og **ikke noe vann i det hele tatt**, ikke engang de 2 m tanken starter med. Det kommer ikke tilbake. Er det det du ser, er koden din sannsynligvis riktig. Les videre.

    (Hvis vannet ditt *dukker* opp, takler versjon 5-koden din allerede det som går galt her. Gjør feiljakten under likevel, finn linjen i koden din som redder deg, og skriv det i loggen.)

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    `CMakeLists.txt` (toppnivå):

    ```cmake
    cmake_minimum_required(VERSION 3.20)
    project(tank_rig)

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)   # alle programmer i én mappe, ved siden av threepps DLL-er

    include(CTest)             # på toppnivå, så ctest finner testene fra byggemappen

    add_subdirectory(src)      # tank_lib
    add_subdirectory(app)      # konsollprogrammet fra versjon 5
    add_subdirectory(tests)
    add_subdirectory(rig)      # 3D-visningen
    ```

    I `rig/CMakeLists.txt` blir lenkelinjen:

    ```cmake
    target_link_libraries(tank_rig PRIVATE tank_lib threepp::threepp)
    ```

    Øverst i `rig/main.cpp`, sammen med threepp-includen:

    ```cpp
    #include "level_sensor.hpp"
    #include "pid_controller.hpp"
    #include "plant.hpp"
    ```

    I `main`, før løkken:

    ```cpp
    Plant plant(2.0, 1.0, 0.10, 0.03);       // de samme tallene som i versjon 3
    LevelSensor sensor(plant);
    PIDController pid(0.8, 0.05, 0.0, setpoint);
    Controller* controller = &pid;
    ```

    Og løkken:

    ```cpp
    Clock clock;
    canvas.animate([&] {
        const double dt = clock.getDelta();

        const double measurement = sensor.read();                     // måle
        const double opening = controller->compute(measurement, dt);  // bestemme
        plant.step(opening, dt);                                      // handle

        const auto level = static_cast<float>(plant.level());
        water->scale.y = level;
        water->position.y = level / 2;

        renderer.render(*scene, *camera);
    });
    ```

    **Se hva du slapp å gjøre.** `Plant` aner ikke at den blir tegnet. `PIDController` aner ikke at det finnes et vindu. Ingen av dem fikk en ny `#include`, en ny parameter eller en ny kodelinje. Det eneste som endret seg, er *hvem som bruker tallene* — versjon 4 skrev dem ut; dette skriver ingenting og flytter en sylinder i stedet.

    Det er gevinsten av en beslutning tatt allerede i [versjon 3](tank_control/v3_pid.md#a-plant-composition): anlegget har en `level()` og tar imot en ventilåpning, og stopper der. En `Plant` som skrev ut sin egen status eller skrev sin egen CSV-fil, måtte blitt revet opp nå. Og fordi løkken leser nivået gjennom en `LevelSensor` i stedet for å spørre anlegget direkte, er en støyende eller defekt sensor fortsatt et bytte på én linje — poenget med [versjon 2](tank_control/v2_sensors.md).

    `Controller* controller = &pid;` ser ut som en omvei når det bare finnes én regulator — milepæl 6 er grunnen til at den er der.

    </div>

### Feiljakt: hvor ble det av vannet? {#bug-hunt-where-did-the-water-go}

Simuleringen din besto alle testene fra versjon 5, og du endret ingenting i den. Noe ved den nye brukeren er annerledes. Finn ut hva — hintene går fra forsiktige til konkrete — og **skriv i loggen hvordan du fant det**, med skjermbilder av det du så: den tomme tanken, og debuggeren stoppet i første bilde med verdien av `dt` synlig. Dette er den beste loggføringen i hele prosjektet. Holder ikke hintene, kan du åpne rettingsforslagene — det er lov. Skriv i loggen at du gjorde det, og hva du fortsatt måtte finne ut selv: hvor rettingen skal ligge, og hvorfor.

??? tip "Hint 1 — verktøyet"

    Det bygger og kjører, men gjør feil ting, så grip etter **debuggeren** ([fire verktøy](debugger.md#four-tools-for-something-is-wrong)). Bruk Debug-profilen (CLions standard). Sett et breakpoint på første linje inne i `animate`-lambdaen og start med **Debug**. Ved breakpointet har ingenting under det kjørt ennå, så `measurement` og `opening` viser tilfeldig søppel: trykk **Step Over** og les hver verdi rett etter at linjen dens har kjørt. I det *andre* bildet er `dt` stor, fordi den tar med tiden du sto på pause — det er ikke feilen. Se nøye på det første bildet.

??? tip "Hint 2 — stedet"

    I aller første bilde: **Step Into** `controller->compute` og følg med på alle lokale variabler. To av dem er ikke vanlige tall: den ene er uendelig, og den neste, som regnes ut fra den, er ikke et tall i det hele tatt — Kd er 0, så hva er 0 × uendelig? [Flyttall-fallgruver](floating_point.md#nan-infinity-and-division-by-zero) sier hva det gjør med alt som regnes ut fra den, og hvorfor begrensningene i `PIDController` og `Valve` ikke stopper det.

    Spør deg så hvorfor `dt` var nøyaktig `0` i første bilde. Ctrl+klikk `getDelta`: det åpner bare deklarasjonen i `Clock.hpp`. Ctrl+klikk navnet der igjen for å komme til `Clock.cpp`, der `Clock` gir jobben videre til et skjult hjelpeobjekt (`pimpl_`). Følg `getDelta` én gang til, og les hva den gjør første gang du kaller den. ([Finn ut av ting selv](#finding-things-out-yourself) sier hvor threepps filer ligger.)

??? tip "Hint 3 — beslutningen"

    Rettingen er én eller to linjer. Spørsmålet er *hvor* de skal stå: i løkken i `rig/main.cpp`? I `PIDController::compute`? I `Valve`, eller i hvordan løkken får tidssteget sitt? Hvilket lag bør nekte et tidssteg på null — eller en verdi som ikke er et tall? Hvilket valg beskytter det *neste* programmet som bruker `tank_lib`? Hvilket holder denne milepælens løfte om å "ikke endre noe i `src/`", og er det løftet fortsatt verdt å holde? Legger du rettingen i `tank_lib`, skriv Catch2-testen først og se den feile.

??? success "Rettingsforslag — åpne etter at du har logget forsøket ditt"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    **I appen** — steg bare simuleringen når det faktisk har gått tid:

    ```cpp
    const double dt = clock.getDelta();
    if (dt > 0.0) {
        const double measurement = sensor.read();                     // måle
        const double opening = controller->compute(measurement, dt);  // bestemme
        plant.step(opening, dt);                                      // handle
    }
    ```

    **I biblioteket** — la `PIDController::compute` takle et steg på null, og bevis det med en test. I `src/pid_controller.cpp` blir derivatlinjen:

    ```cpp
    double derivative = (dt > 0.0) ? (error - previousError_) / dt : 0.0;   // et steg på null har ingen endringsrate
    ```

    og i `tests/test_tank.cpp` (legg til `#include <cmath>` øverst):

    ```cpp
    TEST_CASE("PID gives a finite opening for a zero time step") {
        PIDController pid(0.8, 0.05, 0.0, 5.0);
        REQUIRE(std::isfinite(pid.compute(2.0, 0.0)));
    }
    ```

    Dette er ikke de eneste stedene. `Valve::setOpening` kunne avvist en `NaN`; løkken kunne gitt simuleringen et fast steg i stedet for klokkens; threepps egen eksempelregulator (`examples/libs/utility/Regulator.hpp`) bytter ut en `dt` på null med et lite positivt tall, `std::numeric_limits<float>::min()` (omtrent 10⁻³⁸) — er det en god idé? Hvert valg beskytter en annen gruppe kallere. Hvilket som er riktig for prosjektet ditt, er din beslutning, og en god en å forklare i README-en.

    </div>

Med rettingen på plass og bokens forsterkninger (0.8 og 0.05) starter vannet på 2 m og stiger rundt 7 cm i sekundet. Det er kurven fra versjon 3 spilt av i sanntid — ett steg i versjon 3 var ett sekund — så gi det tid: i underkant av 50 sekunder til det røde båndet, et lite oversving til rundt 5,2 m omtrent femten sekunder senere, og rundt to minutter før det legger seg på båndet.

## Milepæl 6 — Bytt regulator mens programmet kjører {#milestone-6-swap-the-controller-while-it-runs}

*Øver på: [Polymorfisme](Chapter5/polymorphism.md), [Observatør-mønsteret](Chapter6/observer.md), [Verdier, referanser og pekere](Chapter4/types_refs_ptrs.md)*

Lag en `OnOffController` *i tillegg til* PID-regulatoren, og la et tastetrykk velge mellom dem mens programmet kjører: `1` for av/på, `2` for PID. Registrer en tastatur-callback hos canvaset; callbacken peker `Controller*` om og gjør ikke noe annet.

For at du skal se hva regulatoren gjør, farger du ventilklossen fra grønn (lukket) til rød (helt åpen). Da trenger du tak i ventilens materiale: lag materialet i `main`, og endre `createValve` så den tar det som parameter.

> Tips: `canvas.onKeyPressed(...)` tar en lambda som får en `KeyEvent`, der du sammenligner `.key` med `Key::NUM_1` og `Key::NUM_2` — talltastene på øverste rad. Taltastaturet virker ikke: i denne versjonen rapporterer threepp de tastene som `Key::UNKNOWN`. Løkken kaller allerede `controller->compute(...)` gjennom basisklassepekeren, så byttet krever ingen endring i den. (Bruker løkken din fortsatt en `Controller&` fra versjon 4, gjør den om til en peker først: `controller = onOff;` på en referanse kompilerer, men referansen refererer fortsatt til PID-regulatoren, så ingenting byttes — se [Referanser](Chapter4/types_refs_ptrs.md#references).)
>
> Til fargen trenger du åpningen *etter* måle-/bestemme-/handle-linjene. Hvis rettingen din for første bilde la dem inne i `if (dt > 0.0) { ... }`, er en `opening` deklarert inne i de klammene borte etter den avsluttende `}`. Deklarer derfor `double opening = 0.0;` før `canvas.animate(...)`, og endre bestemme-linjen til `opening = controller->compute(measurement, dt);` **uten** `const double` foran. Lar du `const double` stå, lager du en ny, separat `opening` inne i klammene: kompilatoren sier ingenting, og ventilen forblir grønn.

!!! question "Før du trykker 1"

    Skriv i loggen — og commit — hva du forventer at **vannet** og **ventilen** gjør med av/på-regulering. [Versjon 1](tank_control/v1_classes.md) beskrev det. La så nivået legge seg, trykk `1`, og følg med på begge i et halvt minutt; trykk `2` og følg med igjen. Er det du ser, ikke det du forutså, spør deg hva som er forskjellig mellom løkken i versjon 1 og denne.

!!! example "Kjør — dette skal du se"

    Fargen på ventilklossen viser åpningen — grønn når den er lukket, rød når den er helt åpen, en blanding imellom — og tastene `1` og `2` bytter regulator mens programmet kjører. Hva vannet og ventilen gjør med hver regulator, er din observasjon å gjøre.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    ```cpp
    #include "controller.hpp"      // Controller-grensesnittet + OnOffController
    ```

    Ventilen får nå materialet sitt fra den som kaller:

    ```cpp
    std::shared_ptr<Mesh> createValve(std::shared_ptr<MeshStandardMaterial> material) {
        auto geometry = BoxGeometry::create(0.6f, 0.6f, 0.6f);
        auto valve = Mesh::create(geometry, material);
        valve->position.y = tankHeight + 0.5f;
        return valve;
    }
    ```

    I `main` får ventilen materialet sitt:

    ```cpp
    auto valveMaterial = MeshStandardMaterial::create();
    rig->add(createValve(valveMaterial));   // i stedet for createValve()
    ```

    Regulatorlinjene fra milepæl 5 blir:

    ```cpp
    OnOffController onOff(setpoint);
    PIDController pid(0.8, 0.05, 0.0, setpoint);
    Controller* controller = &pid;

    canvas.onKeyPressed([&](KeyEvent evt) {
        if (evt.key == Key::NUM_1) {
            controller = &onOff;
        } else if (evt.key == Key::NUM_2) {
            controller = &pid;
        }
    });

    double opening = 0.0;  // ventilen starter lukket
    Clock clock;
    canvas.animate([&] {
        const double dt = clock.getDelta();

        // måle, bestemme, handle: som i milepæl 5, med rettingen din for første bilde,
        // bortsett fra at bestemme-linjen nå tilordner til opening deklarert over:
        //     opening = controller->compute(measurement, dt);   // ingen "const double" foran

        // ...vannet, som før...

        valveMaterial->color.setRGB(static_cast<float>(opening), 1.f - static_cast<float>(opening), 0.f);

        renderer.render(*scene, *camera);
    });
    ```

    **Én linje i render-løkken ble nettopp hele funksjonen.** `controller->compute(measurement, dt)` kjører `OnOffController::compute` eller `PIDController::compute` avhengig av hva `controller` peker på *i dette bildet* — [polymorfisme ved kjøretid](Chapter5/polymorphism.md), avgjort mens programmet kjører i stedet for mens det kompileres. Løkken ble skrevet før noen av regulatorene fantes, og nevner dem ikke.

    `Controller*` er en **ikke-eiende rå peker**: den observerer ett av to objekter som `main` eier. Den må være en peker og ikke en referanse fordi den må kunne **pekes om** — en [referanse](Chapter4/types_refs_ptrs.md#references) bindes én gang og kan aldri referere til noe annet. En `unique_ptr` ville vært feil: pekeren eier ingenting.

    Tastaturhåndtereren er [Observatør-mønsteret](Chapter6/observer.md#watching-out-for-lifetimes) igjen, med levetidsspørsmålet det kapitlet reiser: lambdaen fanger `onOff`, `pid` og `controller` **by reference**, og canvaset lagrer den. Kapitlets tommelfingerregel er at det en callback fanger, bør leve lenger enn subjektet. Her gjør det ikke det — de tre variablene er deklarert etter canvaset, så de ødelegges *før* det — og likevel er det trygt, fordi canvaset bare kaller de lagrede callbackene mens `canvas.animate(...)` kjører, og alle tre lever til `main` slutter, etter at `animate` har returnert. Fanger du noe som dør mens løkken fortsatt kjører, får du en dangling callback.

    **`valveMaterial` er delt eierskap som gjør ekte arbeid.** Materialet eies av variabelen din *og* av ventilmeshen. Endrer du fargen gjennom en av dem, viser meshen det, fordi det bare finnes ett materiale. Fargen er åpningen avbildet på rødt og grønt: `opening = 0` gir `(0, 1, 0)`, ren grønn; `opening = 1` gir `(1, 0, 0)`, ren rød; alt imellom er en blanding.

    </div>

## Milepæl 7 — Vis tallene på skjermen {#milestone-7-put-the-numbers-on-screen}

*Øver på: [Strenger](strings.md), [IO og strømmer](Chapter4/io_streams.md)*

Du ser *at* det legger seg; vis nå *hva* det gjør. Legg til en `TextSprite` i skjermkoordinater som viser regulatorens navn, nivået, settpunktet og ventilåpningen, og bygg teksten på nytt hvert bilde med `std::format`.

> Tips: `TextSprite` er ikke en del av `threepp.hpp` — den har en egen header under `threepp/objects/`. Sier kompilatoren `'TextSprite' has not been declared`, er det det den mener ([Lese kompilatorfeil](compiler_errors.md)). `FontLoader().defaultFont()` gir deg en font uten fil å laste. Sett `screenSpace = true` og `screenAnchor` for å feste teksten til et hjørne av vinduet i stedet for et punkt i verden. Obs: kommentaren over `screenAnchor` i `Sprite.hpp` sier at `(0, 0)` er øverste venstre hjørne. Med `GLRenderer` i denne versjonen er det *nederste* venstre — en kommentar kan være feil, så prøv og se. Hold rede på regulatorens navn i en `std::string` du setter sammen med pekeren.

!!! example "Kjør — dette skal du se"

    En linje som

    ```
    PID | level 4.87 m | setpoint 5.00 m | valve 70%
    ```

    i øverste venstre hjørne, som endrer seg når vannet beveger seg og bytter navn når du trykker `1` eller `2`. (threepps innebygde font tegner `|` som en brutt strek, `¦`.)

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    Nye includer øverst:

    ```cpp
    #include "threepp/objects/TextSprite.hpp"

    #include <format>
    #include <string>
    ```

    HUD-en, etter riggen:

    ```cpp
    FontLoader fontLoader;
    auto hud = TextSprite::create(fontLoader.defaultFont(), 22.f);  // tekst 22 piksler høy
    hud->setColor(Color::black);
    hud->screenSpace = true;               // festet til vinduet, ikke plassert i 3D-verdenen
    hud->screenAnchor.set(0.f, 1.f);       // forankret i øverste venstre hjørne
    hud->position.set(10.f, -10.f, 0.f);   // 10 px til høyre for og under det hjørnet
    scene->add(hud);
    ```

    Sett navnet der du setter pekeren:

    ```cpp
    std::string controllerName = "PID";

    canvas.onKeyPressed([&](KeyEvent evt) {
        if (evt.key == Key::NUM_1) {
            controller = &onOff;
            controllerName = "on/off";
        } else if (evt.key == Key::NUM_2) {
            controller = &pid;
            controllerName = "PID";
        }
    });
    ```

    Og på slutten av løkkekroppen, før tegningen:

    ```cpp
    hud->setText(std::format("{} | level {:.2f} m | setpoint {:.2f} m | valve {:.0f}%",
                             controllerName, plant.level(), setpoint, opening * 100));
    ```

    `std::format` fyller hver `{}` med neste argument, og `{:.2f}` ber om to desimaler — samme formatering som i [IO og strømmer](Chapter4/io_streams.md#formatting). Den gir deg en `std::string`, som er akkurat det `setText` vil ha; med `<iomanip>` måtte du hatt en strengstrøm og en håndfull manipulatorer for å få samme tekst ([Strenger](strings.md)).

    Skjermkoordinatene starter i **nederste venstre** hjørne og vokser oppover, så ankeret `(0, 1)` er øverste venstre hjørne, og forskyvningen `-10` flytter teksten ned fra det. Det er det rendereren gjør (`renderScreenSpaceSprites` i `GLRenderer.cpp`), uansett hva kommentaren i `Sprite.hpp` sier — vanen "sjekk det du antok" fra [Finn ut av ting selv](#finding-things-out-yourself). Headeren kaller også det andre argumentet til `TextSprite::create` for `worldScale`; i skjermkoordinater er én enhet én piksel, og derfor blir teksten 22 piksler høy med `22.f`.

    Legg merke til at denne milepælen **bare** rørte visningskoden. Å presentere tallene er ett ansvar; å produsere dem er et annet, og de ligger fortsatt i forskjellige filer.

    </div>

## Milepæl 8 — Sjekk at testene fortsatt passerer {#milestone-8-check-the-tests-still-pass}

*Øver på: [Testing](Chapter6/testing.md), [CMake](Chapter2/cmake_intro.md#building-libraries), [Git](Chapter2/version_control.md#when-something-goes-wrong)*

Kjør testene: velg `tests`-konfigurasjonen i kjørelisten i CLion og klikk **Run** (listen viser også targets som CTest og threepp legger til — `Continuous…`, `Nightly…`, `glfw`, `threepp` — dem kan du overse), eller skriv `ctest --test-dir cmake-build-debug` (byggemappen til profilen du bruker) i CLions **Terminal**-fane. Alle testene fra [versjon 5](tank_control/v5_tests.md) skal fortsatt være grønne: 3D-visningen endret ingenting de dekker, og en retting for første bilde i `tank_lib` må ikke knekke dem heller. (Gikk rettingen din inn i `tank_lib`, kjører den nye testen din også.)

Bevis så at testene virkelig vokter det du ser på skjermen:

!!! question "Før du ødelegger det"

    Du skal til å endre `+=` i `Tank::update` til `-=`, så nivået *synker* når ventilen åpner. Skriv i loggen — og commit — hvilke tester du forventer feiler, og hvorfor de andre ikke gjør det.

Gjør endringen, bygg på nytt, og kjør testene og riggen. Ta et skjermbilde av den røde testkjøringen. Angre så endringen med `git restore src/tank.cpp` (eller **Rollback** i CLions commit-vindu) — det er derfor du committet først: `git restore` kaster alle endringer i den filen som ikke er committet. Bygg på nytt, og sjekk at alt er grønt igjen.

!!! example "Kjør — dette skal du se"

    Før fortegnsbyttet, fra `ctest`:

    ```
    100% tests passed, 0 tests failed out of 1
    ```

    (`ctest` teller hele `tests`-programmet som én test) eller, fra `tests`-konfigurasjonen, Catch2 sin egen oppsummering: `All tests passed (14 assertions in 8 test cases)` — flere hvis du har lagt til egne tester. Etter endringen: røde tester, og en tank som tømmes foran øynene dine.

??? success "Vis løsning"

    <div class="spoiler" markdown title="Klikk for å avsløre">

    Ingenting å skrive, bortsett fra forventningen din. I CLions **Terminal**-fane peker du `ctest` mot byggemappen du bruker — CLions heter `cmake-build-debug` og `cmake-build-release`:

    ```bash
    ctest --test-dir cmake-build-debug --output-on-failure
    ```

    (Et PowerShell-vindu åpnet fra Start-menyen finner kanskje ikke `ctest`; CLions Terminal-fane gjør det.)

    Med `-=` feiler tre av bokens åtte testtilfeller: *Tank integrates net flow over a step*, *Tank level never goes negative* og *Closed loop: the level ends near the setpoint*. Ventil-, PID- og av/på-testene kaller aldri `Tank::update`, så de forblir grønne — hver test vokter én oppførsel, og de røde peker rett på komponenten som gikk i stykker. Egne tester som steger en `Tank` eller en `Plant`, kan også feile.

    Prosjektet ditt bygger nå tre programmer fra ett kildetre:

    ```mermaid
    %%{init: {'flowchart': {'curve': 'linear'}}}%%
    graph TD
        RIG["tank_rig (3D-visning)"] -->|lenker| LIB["tank_lib"]
        RIG -->|lenker| TPP["threepp::threepp (hentet)"]
        APP["tank_control (konsoll)"] -->|lenker| LIB
        TESTS["tests"] -->|lenker| LIB
        TESTS -->|lenker| C2["Catch2 (hentet)"]
    ```

    `.cpp`-filene i `src/` kompileres **én gang**, til `tank_lib`, og lenkes inn i alle tre, så testene sjekker nøyaktig den samme kompilerte koden som 3D-appen kjører — ikke en kopi som kan ha drevet av gårde. Det er derfor [CMake-kapitlet](Chapter2/cmake_intro.md#building-libraries) sa at du skal bygge felles logikk som et bibliotek i stedet for å liste de samme `.cpp`-filene i flere `add_executable`-linjer.

    Grafikken har ingen tester, og det er med vilje: hold visningen **tynn**. Legg alle beslutninger i `tank_lib`, der de kan testes, og la visningen bare oversette tall til former. Er en bit av den oversettelsen verdt å få riktig — vannets skala og posisjon, for eksempel — trekk den ut i en egen liten funksjon og test den.

    </div>

## Prosjektstruktur {#project-layout}

Etter milepælene ser prosjektet ditt slik ut:

```
tank-rig/
├── CMakeLists.txt      # toppnivå: C++20, bin-mappen, include(CTest), src, app, tests og rig
├── LOG.md              # loggen din
├── README.md           # presentasjonen din
├── include/            # fra versjon 5
├── src/                # fra versjon 5 — bygget som tank_lib
├── app/                # fra versjon 5 — konsollprogrammet
├── tests/              # fra versjon 5 — pluss tester du legger til
├── rig/                # 3D-visningen
│   ├── CMakeLists.txt
│   └── main.cpp
└── docs/
    └── images/         # skjermbilder og GIF-er til README-en
```

De to byggefilene du skrev, er toppnivåfilen fra milepæl 5 og `rig/CMakeLists.txt`:

```cmake
include(FetchContent)

if(MINGW)
    set(BUILD_SHARED_LIBS ON)
endif()
FetchContent_Declare(
    threepp
    GIT_REPOSITORY https://github.com/markaren/threepp.git
    GIT_TAG        2026-09-28
    GIT_SHALLOW    TRUE
)
FetchContent_MakeAvailable(threepp)

add_executable(tank_rig main.cpp)
target_link_libraries(tank_rig PRIVATE tank_lib threepp::threepp)
```

---

## Finn ut av ting selv {#finding-things-out-yourself}

Milepælene er ferdige, og med dem den veiledede delen av prosjektet. Det som gjenstår, er ditt: en [utvidelse](#your-extension) du velger og designer selv, og en README som [presenterer det du har laget](#present-your-project). Herfra er det ingen som gir deg det nøyaktige kallet. Det er normalt: programmerere bruker mye av tiden sin på å finne ut hvordan et bibliotek virker. Slik gjør du det med threepp.

- **Les headerne.** Ctrl+klikk et threepp-navn i CLion for å åpne deklarasjonen. Selve headerne ligger i byggemappen, under `cmake-build-<profil>/_deps/threepp-src/include/threepp/`, og kildefilene under `_deps/threepp-src/src/`. Det er lov å lese `.cpp`-filene, og ofte er de det endelige svaret — feiljakten i milepæl 5 ender i `Clock.cpp`.
- **Les eksemplene.** threepp kommer med over hundre små eksempelprogrammer. Se dem for versjonen du bruker på <https://github.com/markaren/threepp/tree/2026-09-28/examples> — les dem i nettleseren, og kopier bare de få linjene du trenger, med en kommentar om hvor de kommer fra. De starter med `#include "renderer_factory.hpp"` og `createRenderer(canvas)`; dropp include-linjen og bruk `GLRenderer renderer(canvas);` i stedet, som i milepæl 1.
- **Se et eksempel kjøre.** Kopier et eksempels `.cpp` inn i `rig/` under et nytt navn (for eksempel `try_raycast.cpp`), legg til `add_executable(try_raycast try_raycast.cpp)` og `target_link_libraries(try_raycast PRIVATE threepp::threepp)` i `rig/CMakeLists.txt`, bytt inn `GLRenderer` som over, last inn CMake på nytt, og velg det i kjørelisten. Det bruker threepp-versjonen du allerede har bygget. Noen eksempler trenger ekstra filer eller biblioteker og bygger ikke på denne måten — velg et annet.
- **Krymp, og flytt så over.** Finn et eksempel som gjør noe nær det du vil. Finn den minste delen av det som gjør tingen. Flytt den delen inn i riggen din, få den til å virke, og gjør den *så* til din egen.
- **Sjekk det du antok.** Når noe oppfører seg rart, skriv ned hva du forventet, og test antakelsen med den minste endringen du kan komme på — akkurat som loggføringen etter milepæl 4.

---

## Din utvidelse {#your-extension}

Å velge en utvidelse, og å kunne si hvorfor du bygget den som du gjorde, er en del av prosjektet. Regelen fra milepæl 8 gjelder fortsatt: **logikken hører hjemme i et bibliotek, med en test; visningen bare viser den.** Bygg én utvidelse godt — testet, forklart, med avveiningene forstått — før du tenker på en til.

Hvert forslag under sier hva du skal bygge, designspørsmålet du må svare på, og en test som beviser at det virker. Der du trenger noe boken ikke har vist deg, sier det hvor du kan lete. Det finnes ingen løsninger.

Dette er forslag; en egen idé er like god. Uansett hva du velger, start med å skrive planen i loggen: hva den gjør, hvilke nye klasser som skal hvor, hva riggen skal vise, og én ting du ikke vet ennå. Noen av forslagene vokser ut av listen i versjon 5 — har du bygget et av dem der, kommer det med i importen din, så ta det videre her: inn i visningen, med designspørsmålet besvart og testen skrevet.

**Små**

- **Alarm med hysterese.** Skallet blir rødt når nivået stiger over 7,0 m, og går tilbake når det synker under 6,8 m.
    - *Designspørsmål:* hvem bestemmer — render-løkken, anlegget, eller en liten egen klasse? Hvorfor må ikke alarmen slå seg av og på hvert bilde nær grensen?
    - *Test:* alarmen slår seg på én gang når nivået krysser 7,0 m, og av først under 6,8 m.
    - Ingenting i riggen presser nivået så høyt ennå — gi deg selv en måte å gjøre det på (en tast som tvinger ventilen åpen, for eksempel), så du kan se den slå inn.
- **Støyende sensor.** En `NoisyLevelSensor` som legger til litt støy ([Tilfeldige tall](random.md)), med et fast seed så hver kjøring blir lik.
    - *Designspørsmål:* `Sensor::read()` er `const`, men å trekke et tilfeldig tall endrer generatoren. Hvilke muligheter har du, og hvilken skjuler ikke at `read()` endrer noe?
    - *Finn ut:* hva nøkkelordet `mutable` gjør, og hva du ellers kunne gjort.
    - *Test:* to sensorer med samme seed gir de samme målingene. Se så hva støy gjør med hver regulator.
- **Dødbåndregulator.** En av/på-regulator som bare slår om når nivået er mer enn 0,2 m fra settpunktet.
    - *Designspørsmål:* forutsi hva den gjør med det du så i milepæl 6 — og sjekk.
    - *Test:* innenfor båndet endres ikke utgangen.
- **Taster for tidsskala.** Taster som gjør simulert tid raskere og langsommere.
    - *Designspørsmål:* hvor bor skaleringen, og hva skal skje ved 50× fart? Hva gjør en veldig stor `dt` med anlegget ditt?
    - *Test:* det som regner ut det skalerte steget, gir aldri anlegget mer enn grensen du har valgt.

**Design**

- **Historikkgraf.** De siste par hundre nivåene tegnet som en linje ved siden av tanken.
    - *Designspørsmål:* hvilken beholder, hva skjer når den er full, og hvem eier den?
    - *Finn ut:* hvordan du endrer punktene i en linje hvert bilde — `examples/geometries/dynamic.cpp` flytter punktene i en geometri hvert bilde, og `examples/extras/curves/catmull_room_curve3.cpp` bygger en `Line` fra punkter.
    - *Test:* historikken holder høyst N verdier og kaster den eldste først.
- **Tilstandsmaskin.** *Fyller → Holder → Tømmer → Feil*, med fargen på skallet som viser tilstanden ([Enumerasjoner](Chapter1/enums.md) og en `switch`).
    - *Designspørsmål:* anlegget har ingen utløpsventil. Hva legger du til, og hvem eier det?
    - *Test:* én test per overgang, også de som *ikke* skal skje.
- **To tanker i kaskade.** Utløpet fra den første tanken fyller den andre: to anlegg, to rigger, `rig->position.x` fra hverandre.
    - *Designspørsmål:* i din `Plant` er utløpet et fast tall, og `Plant` rapporterer det ikke. Men en tank som fyller en annen, kan ikke renne ut når den er tom (og en ekte tank renner fortere ut jo fullere den er). Hva må endres, hva trenger det andre anlegget å vite, og fra hvem?
    - *Test:* med utløpet fra den første tanken stengt synker nivået i den andre tanken bare.
- **Settpunkt som kan endres mens programmet kjører.** Flytt det røde båndet med taster, eller ved å dra det med musen, og gi den nye verdien til regulatoren.
    - *Designspørsmål:* `Controller` har ingen måte å endre settpunktet sitt på. Hvilket grensesnitt endres, og hvilke tester knekker?
    - *Finn ut:* `examples/misc/raycast.cpp` (hva som er under musen) og `examples/controls/drag.cpp` (dra objekter).
    - *Test:* etter en endring av settpunktet legger lukket sløyfe seg nær den nye verdien.
- **Fast samplingstid for regulatoren.** Regulatoren kjører hvert 0,5 s simulert tid, uansett hvor fort bildene kommer — som scan-syklusen i en PLS.
    - *Designspørsmål:* hvem holder tiden, og hva skjer mellom samplene? Forutsi effekten på milepæl 6.
    - *Test:* over ett simulert sekund, ved hvilken som helst bildefrekvens, kjører regulatoren nøyaktig to ganger.

**Din egen maskin**

Bygg en maskin nummer to *ved siden av* tanken, i samme repository: en heis, et robotledd, et sorteringsbånd, eller din egen idé. Den får sitt eget bibliotek-target som ikke lenker mot threepp, sine egne tester og sin egen visning. Før du begynner, beskriver du den i loggen på samme måte som forslagene over er beskrevet: hva den gjør, designspørsmålet, hva du må finne ut, og den første testen. threepps `examples/projects/MotorControl/` og `examples/libs/utility/Regulator.hpp` viser en motor og en regulator du kan lære av.

Skjelettet fra tanken passer nesten alle regulerte maskiner, fordi det består av fire roller:

- **Tilstand som går framover i tid.** Noe med `step(input, dt)`, som `Plant`. Oppdateringen er samme type linje som i `Tank::update`: den nye verdien er den gamle pluss en rate ganger `dt`. For bevegelse endres posisjonen med hastighet × `dt` og hastigheten med akselerasjon × `dt`.
- **Sensorer** som leser tilstanden, bak et grensesnitt.
- **Aktuatorer med grenser** — en ventil som ikke kan åpne mer enn helt, en motor med en maksimal kraft.
- **Regulatorer** bak et grensesnitt, som kan byttes mens programmet kjører.

To ting å passe på når du går over til en ny maskin:

- **Sjekk hva klassene du gjenbruker, antar.** Bokens PID begrenser utgangen til 0..1 fordi den styrer en ventil ([versjon 3](tank_control/v3_pid.md)). En motor som kan skyve begge veier, trenger −1..+1. Gjenbruk ideen; still spørsmål ved detaljene.
- **Tidssteg betyr mer for ting som beveger seg.** En tank tilgir et langt bilde; en maskin med treghet kan svinge kraftig over etter ett. Bestem hva simuleringen din skal gjøre når et bilde tar mye lengre tid enn vanlig — etter et breakpoint, for eksempel, eller mens du drar i vinduet.

**Beslutninger verdt å skrive ned.** Uansett hva du bygger, noter beslutningene som formet det, noen linjer hver, i loggen eller i README-delen *Hvorfor det er bygget slik*. For eksempel:

```markdown
**Spørsmål:** hvor skal høynivåalarmen ligge?
**Alternativer:** visningen sjekker nivået hvert bilde / anlegget varsler / en AlarmMonitor-klasse som løkken mater.
**Valg:** AlarmMonitor, med 0,2 m hysterese.
**Hvorfor:** kan testes uten vindu, og slår inn én gang per kryssing.
**Test:** "alarm fires once when level crosses 7.0 and clears below 6.8".
```

---

## Presenter prosjektet ditt {#present-your-project}

`README.md` er der du **presenterer** prosjektet — for en lærer, for en framtidig arbeidsgiver, for deg selv om et år. Den er skrevet av deg, om arbeidet ditt, med dine egne ord. Start med [README-fila](readme_guide.md), les avsnittet om [å presentere et større prosjekt](readme_guide.md#presenting-a-bigger-project), og gjør din til en ordentlig presentasjon. (Tar du AIS1003, lister mappeoppgaven delene README-en din må ha, og legger til noen spørsmål i dem; der de to er forskjellige, følger du mappeoppgaven.)

1. **Hva det er** — et avsnitt, og en **GIF av det i gang** øverst. Det første leseren ser, bør være riggen din i bevegelse.
2. **Hvordan bygge og kjøre det** — stegene, hvor lang tid første bygg tar, og kontrollene (hvilke taster som gjør hva).
3. **Hvordan det virker** — løkken, biblioteket og visningen, og et [UML-klassediagram](uml.md) av typene *du* skrev eller endret. En `mermaid`-blokk som de på UML-siden vises som et diagram på GitHub; et bilde av en ryddig håndtegning virker også. Si hvor simuleringen møter visningen.
4. **Hvorfor det er bygget slik** — beslutningene du er fornøyd med, hvorfor de gjør det til en god løsning, og alternativene du valgte bort. Hvor la du rettingen for første bilde, og hvorfor der?
5. **Hva som ikke kom med** — hva du ville bygge, men ikke gjorde, hvorfor ikke, og hva det ville krevd. Å kjenne grensene for din egen løsning er en del av å forstå den.
6. **Hvordan jeg jobbet** — historien om prosjektet, med henvisninger til de beste loggføringene og commitene dine: den vanskeligste feilen, testen som fanget noe, forventningen som viste seg å være feil.
7. **Hvordan jeg brukte KI** — hvilke verktøy og modeller du brukte (navnet og versjonen verktøyet viser deg), hva du brukte dem til, og hvordan: hva du spurte om, hva du beholdt, hva du forkastet og hvorfor. Hvor tok den feil eller hjalp ikke? Hva lærte du av å jobbe på denne måten — om koden, og om å bruke KI? ([Bruke KI til koding](using_ai.md)) Brukte du ikke KI, skriv det, og hvordan du fant svarene i stedet.
8. **Kilder** — alt som ikke startet som ny kode i dette prosjektet: versjon 5-koden du importerte (og tanksidene i boka den bygger på), løsninger fra milepælene du skrev inn fra denne siden, og alt du har lånt fra threepps eksempler eller andre steder, med lenker.

**Bilder og GIF-er.** [README-fila](readme_guide.md#show-it-screenshots-and-gifs) viser hvordan du tar et skjermbilde, spiller inn en kort GIF av vinduet, lagrer begge i `docs/images/` og setter dem inn i README-en. De beste er de du tok underveis: den tomme tanken før rettingen, den røde testkjøringen, første gang utvidelsen din virket — og en GIF av den ferdige riggen øverst på siden.

---

## Oppsummering {#summary}

- En 3D-visning er bare en ny **bruker** av tallene fra simuleringen. Å koble den til krevde ingen endringer i `src/` — simuleringen vet ikke at visningen finnes.
- En ny bruker kan likevel avsløre en antakelse testene dine aldri gjorde. En klokkes første bilde har **ingen tid som har gått**, og en `NaN` som først har kommet inn, flyter gjennom alle utregninger og sniker seg forbi alle begrensninger. Hvor du skal verne mot den, er en designbeslutning.
- Å hente inn en ekte avhengighet er noen få linjer CMake: `include(FetchContent)`, `FetchContent_Declare`, `FetchContent_MakeAvailable`, og så lenke mot targetet den eksporterer. **Lås til en tag**, aldri en bevegelig branch, så alle som bygger prosjektet ditt, får samme threepp.
- En scenegraf er **komposisjon**: en gruppe *har* barn, et barns transformasjon er relativ til forelderen, og flytter du forelderen, flytter alle barna seg.
- threepps `create`-funksjoner returnerer en `shared_ptr` fordi threepp valgte **delt eierskap**: scenen holder det du legger i den i live, og variabelen din er en eier til.
- En basisklassepeker valgt med et tastetrykk er **polymorfisme ved kjøretid** du kan se; løkken som kjører begge regulatorene, endret seg aldri.
- Gang med `dt`, aldri med "per bilde". Bilder er ikke en tidsenhet.
- Biblioteket kompileres én gang og lenkes inn i 3D-riggen, konsollprogrammet og testene, så det du testet, er det du kjørte.
- Etterlat et spor: commits som sier hvorfor, en logg, forventninger skrevet ned før du kjører — og en README som presenterer resultatet med dine egne ord.
