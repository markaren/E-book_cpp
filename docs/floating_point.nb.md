# Flyttall-fallgruver

I et automasjonsstudium vil du tilbringe mye tid med `double`- og `float`-verdier: sensoravlesninger, styringssignaler, tidsintegraler, transformasjoner. Flyttall er ekstremt nyttige, men de har skarpe kanter som tar enhver nybegynner minst én gang.

Denne siden er den korte lista over oppførsler som vil overraske deg, og hvordan du håndterer dem.

---

## Flyttall er ikke nøyaktige

Dette er hovedpoenget. `float` og `double` kan ikke representere de fleste desimalbrøker nøyaktig. De lagrer det *nærmeste* tallet den binære representasjonen deres kan holde.

Den klassiske demonstrasjonen:

```cpp
double a = 0.1;
double b = 0.2;
double c = a + b;

std::cout << c << "\n";        // 0.3
std::cout << (c == 0.3) << "\n"; // 0   (false!)
```

`0.1`, `0.2` og `0.3` blir alle avrundet når de lagres. `0.1 + 0.2` lander nær, men ikke nøyaktig på, den lagrede representasjonen av `0.3`. Forskjellen er rundt 5 × 10⁻¹⁷, usynlig når den skrives ut, men svært synlig når den sammenlignes med `==`.

Dette er ikke en sær C++-detalj; det er slik IEEE 754-flyttall fungerer i alle språk. Python, Java, JavaScript, MATLAB: samme tall, samme oppførsel.

---

## Sammenlign aldri flyttall med `==`

Den vanligste konsekvensen av det ovenstående:

```cpp
if (computedValue == 0.3) { /* almost certainly never runs */ }
if (sensorReading == 0.0) { /* probably wrong */ }
```

To tryggere mønstre:

### Sammenlign med en toleranse

```cpp
bool approximatelyEqual(double a, double b, double tolerance = 1e-9) {
    return std::abs(a - b) < tolerance;
}

if (approximatelyEqual(computedValue, 0.3)) { /* ... */ }
```

Den riktige toleransen avhenger av størrelsen på tallene og hvordan de ble beregnet. For sensoravlesninger kalibrert til to desimaler kan `1e-3` være passende; for tett konvergerte numeriske beregninger, `1e-12`. Velg bevisst.

### Bruk intervaller i stedet for nøyaktige målverdier

```cpp
if (temperature > 79.95 && temperature < 80.05) {
    // "at 80", but a range, not a point
}
```

Når du finner deg selv i å sammenligne en målt verdi for *nøyaktig* likhet, spør om spørsmålet egentlig vil ha "nær denne verdien". Det vil det nesten alltid.

---

## Summer mister presisjon

Å legge sammen mange flyttall gir akkumulert feil. Den klassiske fallgruva:

```cpp
double total = 0.0;
for (int i = 0; i < 10'000'000; ++i) {
    total += 0.1;
}
std::cout << total << "\n";        // 999999.999999...  (not 1,000,000)
```

Feilen i hver addisjon er bittesmå; ti millioner av dem summerer seg opp. For summer av millioner av målepunkter, vurder:

1. **Bruk `double`, ikke `float`.** `double` har omtrent 15–16 desimale siffers presisjon; `float` har 6–7.
2. **Bruk `std::accumulate` med omhu.** Eller slå opp Kahan-summering hvis nøyaktighet betyr mer enn fart.
3. **Der du kan, tell i heltall** og konverter til flyttall bare til slutt.

For styringssløyfer som integrerer over tid, er drift noe å holde øye med over lange kjøringer.

---

## `NaN`, uendelig og divisjon med null

Flyttall har spesialverdier som heltallsaritmetikk ikke har:

```cpp
double inf  = 1.0 / 0.0;      // +infinity
double ninf = -1.0 / 0.0;     // -infinity
double nan  = 0.0 / 0.0;      // NaN, "not a number"
double nan2 = std::sqrt(-1.0); // NaN
```

I motsetning til heltallsdivisjon med null (som er udefinert oppførsel og kan krasje), er flyttallsdivisjon med null **veldefinert**: den gir uendelig eller NaN. Programmet fortsetter å kjøre.

Det høres harmløst ut helt til du propagerer en `NaN` gjennom matematikken din:

```cpp
double x = std::sqrt(-1.0);    // NaN
double y = x + 1.0;             // NaN
double z = std::sin(y);          // NaN
if (z < 1.0) { /* ... */ }       // false! NaN compares false with everything
```

NaN forgifter ethvert uttrykk den berører og feiler stille i enhver sammenligning: selv `nan == nan` er false. Hvis sensorrørledningen din begynner å produsere nuller og du ikke ser noen feil, mistenk en NaN.

For å sjekke eksplisitt:

```cpp
#include <cmath>

if (std::isnan(x)) { /* handle the bad value */ }
if (std::isinf(x)) { /* handle the infinity */ }
if (std::isfinite(x)) { /* x is a regular, usable number */ }
```

---

## Heltallsdivisjon tar folk også

Ikke strengt tatt et flyttallsproblem, men beslektet og svært vanlig:

```cpp
int    a = 10 / 3;        // 3, fractional part discarded
double b = 10 / 3;        // also 3.0!, division happens in int, then converted
double c = 10.0 / 3;      // 3.333…, at least one operand is a double
```

Hvis du vil ha et flyttallsresultat, sørg for at minst én operand er `double` (eller `float`). Å skrive literalen som `10.0` er den enkleste måten.

---

## `float` kontra `double`

Bruk `double` som standard. Bruk `float` bare når du har en spesifikk grunn: typisk minnebegrenset innebygd kode der du har mange verdier å lagre, eller når du grensesnitter mot et bibliotek (grafikk, ML) som bruker `float`.

| | `float` | `double` |
|---|---------|----------|
| Størrelse            | 4 byte | 8 byte |
| Signifikante siffer | ~6–7 | ~15–16 |
| Fart           | Ofte den samme på moderne CPU-er | Ofte den samme på moderne CPU-er |

På en mikrokontroller uten en maskinvare-FPU kan `float`-operasjoner være mye raskere enn `double` (kompilatoren emulerer `double` i programvare). Hvis du sikter mot en slik plattform, sjekk databladet og kjør ytelsestester.

---

## Måle tid: foretrekk heltall

For tidtaking i styringssløyfer bruker `std::chrono` heltallstyper under panseret. Varigheter er nøyaktige; ingen flyttallsdrift.

```cpp
#include <chrono>

auto start = std::chrono::steady_clock::now();
// ... do work ...
auto elapsed = std::chrono::steady_clock::now() - start;
auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count();
```

Motstå fristelsen til å spore simuleringstid som `double t += dt`. Over en lang kjøring summerer akkumulert feil i `t` seg opp. Bruk et heltalls stegtall og multipliser når du trenger en tidsverdi.

---

## Når du må skrive ut et flyttall

`std::cout` formaterer `double` med en standardpresisjon på 6 signifikante siffer, noe som ofte er villedende:

```cpp
double x = 0.1 + 0.2;
std::cout << x << "\n";                                       // 0.3, misleading
std::cout << std::setprecision(17) << x << "\n";              // 0.30000000000000004
```

For å feilsøke presisjonsproblemer, sett en høy presisjon eksplisitt. For brukervendt utskrift gir `std::fixed << std::setprecision(2)` en fast visning med to desimaler.

---

## Oppsummering

- `float` og `double` er tilnærminger av desimaltall. De er ikke nøyaktige.
- **Bruk aldri `==` til å sammenligne flyttall.** Bruk en toleranse eller et intervall.
- Lange summer akkumulerer feil. Bruk `double` (ikke `float`) og vurder Kahan-summering for høypresisjonssummer.
- Divisjon med null er veldefinert for flyttall; den gir uendelig eller `NaN`.
- `NaN` forgifter ethvert uttrykk den berører og sammenlignes ulik alt, inkludert seg selv.
- Bruk `double` som standard. Bruk `float` bare med grunn.
- For tidtaking, bruk `std::chrono` (heltallsbasert).
