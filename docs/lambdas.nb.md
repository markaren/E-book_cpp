# Lambda-uttrykk

Et **lambda-uttrykk** er en funksjon skrevet rett i koden, ofte brukt der du vil sende oppførsel som et argument. De ble lagt til i C++11 og er nå overalt, særlig i algoritmer fra standardbiblioteket, i tilbakekall (callbacks) og i korte hjelpefunksjoner som ikke fortjener sitt eget navn.

Denne siden introduserer syntaksen og tilfellene der lambdaer gjør koden dramatisk renere.

---

## Det motiverende eksempelet

Du har en vektor med sensoravlesninger, og du vil sortere dem etter absoluttverdi:

```cpp
std::vector<double> readings = {-3.2, 1.0, 4.5, -7.1, 0.5};
```

`std::sort` trenger å vite hva "mindre enn" betyr. Standarden bruker `<`, som ville sortert `-7.1` først. For å sortere etter *absolutt* verdi må du gi den en egendefinert sammenligning.

Uten lambdaer må du skrive en separat funksjon eller et funksjonsobjekt:

```cpp
bool compareAbs(double a, double b) {
    return std::abs(a) < std::abs(b);
}

std::sort(readings.begin(), readings.end(), compareAbs);
```

Det virker, men `compareAbs` flyter nå rundt i navnerommets virkeområde selv om den bare brukes én gang. Med en lambda havner sammenligningen rett der den brukes:

```cpp
std::sort(readings.begin(), readings.end(),
          [](double a, double b) { return std::abs(a) < std::abs(b); });
```

Oppførselen du vil ha, står rett ved kallstedet. Ingen omvei, ingen navngiving, ingen separat funksjon.

---

## En lambdas anatomi

```cpp
[capture](parameters) -> return_type { body }
```

| Del | Hva den gjør |
|------|--------------|
| `[capture]` | Hvilke variabler fra det omsluttende virkeområdet lambdaen kan bruke |
| `(parameters)` | Som en funksjons parameterliste |
| `-> return_type` | Returtypen (valgfri, vanligvis utledet) |
| `{ body }` | Koden som kjører når lambdaen kalles |

Den enkleste formen har tom fangst og ingen returtype:

```cpp
auto sayHello = []() { std::cout << "Hello\n"; };
sayHello();    // skriver ut Hello
```

Det er hakeparentesene som gjør en lambda til en lambda; selv en tom `[]` er påkrevd.

---

## Fangster {#captures}

Lambdaer trenger en *fangstklausul* for å bruke variabler fra det omkringliggende virkeområdet. Klausulen sier hvilke variabler som skal tas inn, og om de skal tas inn som verdi eller som referanse.

```cpp
int threshold = 5;

auto isLarge = [threshold](int x) { return x > threshold; };
//             ^^^^^^^^^^^
//             fang threshold som verdi, lambdaen har sin egen kopi

isLarge(7);   // true
threshold = 100;
isLarge(7);   // fortsatt true, lambdaens kopi er fortsatt 5
```

Som referanse, med `&`:

```cpp
int count = 0;
auto increment = [&count]() { ++count; };

increment();
increment();
increment();
std::cout << count << "\n";   // 3
```

To kortformer:

| Fangst | Betydning |
|---------|---------|
| `[=]` | Fang hver brukt variabel som verdi |
| `[&]` | Fang hver brukt variabel som referanse |
| `[=, &count]` | Alt som verdi, men `count` som referanse |
| `[&, threshold]` | Alt som referanse, men `threshold` som verdi |

Kortformene er bekvemme, men mister presisjon. Foretrekk å navngi fangstene eksplisitt; det dokumenterer hensikten.

> **Pass på at `[&]` ikke overlever de fangede variablene.** En lambda som fanger som referanse, holder referanser til variablene; hvis lambdaen lagres og kalles *etter* at de variablene har gått ut av virkeområdet, får du en dinglende referanse. Fang som verdi når du er usikker.

---

## Der lambdaer skinner

### Sortering og filtrering med `<algorithm>`

```cpp
std::vector<int> v = {5, 2, 8, 1, 9, 3};

// sorter synkende
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

// tell verdier større enn 4
int n = std::count_if(v.begin(), v.end(), [](int x) { return x > 4; });

// finn den første verdien større enn 7
auto it = std::find_if(v.begin(), v.end(), [](int x) { return x > 7; });
```

Dette er den vanligste bruken av lambdaer i dagligdags C++. Enhver algoritme med en `_if`-endelse tar et predikat; lambdaer gjør de predikatene konsise.

### Transformere en beholder

```cpp
#include <algorithm>

std::vector<double> celsius = { -10, 0, 22, 37 };
std::vector<double> fahrenheit(celsius.size());

std::transform(celsius.begin(), celsius.end(),
               fahrenheit.begin(),
               [](double c) { return c * 9.0 / 5.0 + 32.0; });
```

### Korte tilbakekall

Når et bibliotek tar en funksjon som det kaller deg tilbake med, er en lambda vanligvis renere enn en navngitt funksjon:

```cpp
button.setOnClick([&](){ count++; updateDisplay(); });
```

---

## Lagre lambdaer

To måter:

**`auto`** når du lagrer og bruker lambdaen i samme virkeområde:

```cpp
auto add = [](int a, int b) { return a + b; };
int sum = add(2, 3);
```

Hver lambda har en unik, kompilatorgenerert type. Du kan ikke skrive ut typen for hånd, og det er derfor `auto` passer naturlig.

**`std::function<...>`** når du trenger å lagre lambdaer med samme kallsignatur i en beholder, eller sende en over en API-grense:

```cpp
#include <functional>

std::vector<std::function<int(int, int)>> ops;
ops.push_back([](int a, int b) { return a + b; });
ops.push_back([](int a, int b) { return a - b; });

for (const auto& op : ops) {
    std::cout << op(10, 3) << "\n";   // 13, deretter 7
}
```

`std::function` er mer fleksibel, men har en liten kjøretidskostnad (et virtuelt kall). Grip etter den når `auto` ikke fungerer; bruk `auto` som standard.

---

## Et kort gjennomarbeidet eksempel

Behandle en liste med sensoravlesninger, behold bare de gyldige og regn ut gjennomsnittet:

```cpp
#include <algorithm>
#include <numeric>
#include <vector>
#include <iostream>

int main() {
    std::vector<double> readings = {22.5, -999.0, 23.1, 22.9, -999.0, 23.0};
    const double sentinel = -999.0;

    // fjern sentinel-verdier
    readings.erase(
        std::remove_if(readings.begin(), readings.end(),
                       [sentinel](double v) { return v == sentinel; }),
        readings.end());

    if (readings.empty()) {
        std::cout << "no valid readings\n";
        return 0;
    }

    double sum  = std::accumulate(readings.begin(), readings.end(), 0.0);
    double mean = sum / static_cast<double>(readings.size());
    std::cout << "mean: " << mean << "\n";
}
```

Begge lambdaene er bittesmå og lever akkurat der de brukes. Hensikten leses ovenfra og ned uten at du må jakte på funksjonsdefinisjoner rundt om i fila.

---

## Oppsummering

- En lambda er en funksjon skrevet rett i koden med en eksplisitt liste over fangede variabler.
- Syntaks: `[captures](params) { body }`; det er parentesene som gjør den til en lambda.
- Fang som verdi (`[x]`), som referanse (`[&x]`), eller implisitt (`[=]` eller `[&]`).
- Par dem med `<algorithm>` (`sort`, `find_if`, `count_if`, `transform`) for ren, uttrykksfull kode.
- Lagre små lambdaer med `auto`; grip etter `std::function` bare når du trenger typeutvisking (type erasure).
- Å fange som referanse er farlig hvis lambdaen overlever de fangede variablene.
