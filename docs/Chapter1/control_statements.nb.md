# Kontrollstrukturer

Som standard kjører et program én setning etter en annen, ovenfra og ned. **Kontrollstrukturer** lar deg endre den flyten: ta én vei eller en annen basert på en betingelse, gjenta en blokk med kode, eller stoppe en løkke tidlig.

Tre familier:

| Familie | Eksempler | Hensikt |
|--------|----------|---------|
| Betinget | `if`, `else`, `else if`, `switch` | Velge mellom veier |
| Løkke        | `while`, `do-while`, `for`, range-basert `for` | Gjenta kode |
| Hopp        | `break`, `continue`, `return` | Gå tidlig ut av en blokk eller funksjon |

---

## `if` og `else`

```cpp
if (temperature > 80) {
    std::cout << "Cooling down\n";
}
```

Betingelsen i parentes må gi en `bool` (eller noe som kan konverteres til en). Hvis den er sann, kjører blokken; ellers hoppes den over.

For å håndtere det andre tilfellet:

```cpp
if (temperature > 80) {
    std::cout << "Cooling down\n";
} else {
    std::cout << "Normal\n";
}
```

For mer enn to utfall, lenk sammen med `else if`:

```cpp
if (temperature > 80) {
    std::cout << "Too hot\n";
} else if (temperature < 10) {
    std::cout << "Too cold\n";
} else {
    std::cout << "Fine\n";
}
```

Bare den første grenen som passer, kjører. Når en gren først er valgt, hoppes resten over.

> **Bruk krøllparenteser selv for kropper med én enkelt setning.** Det er én ekstra linje og unngår en overraskende klasse av feil når noen legger til en andre setning senere.

---

## `switch`

Når du sammenligner én verdi mot flere konstanter, er `switch` klarere enn en lang `else if`-kjede:

```cpp
switch (gear) {
    case 1: std::cout << "First\n";  break;
    case 2: std::cout << "Second\n"; break;
    case 3: std::cout << "Third\n";  break;
    default: std::cout << "Unknown\n";
}
```

To ting du må vite:

1. **Ta alltid med `break`** på slutten av hver case med mindre du spesifikt vil at kjøringen skal falle gjennom til neste case. Å glemme `break` er en klassisk feil: kjøringen fortsetter stille inn i neste case.
2. `switch` virker bare med heltallslignende verdier (`int`, `char`, enumerasjoner). Den kan ikke switche på en `std::string` eller en `double`.

En subtil felle: alle case-ene deler **ett** virkeområde — den ene blokken etter `switch (...)`. Så en variabel som deklareres i én case, er fortsatt i virkeområde i case-ene under den, og C++ forbyr å hoppe over initialiseringen dens. Denne uskyldig utseende koden kompilerer ikke:

```cpp
switch (gear) {
    case 1:
        int chosen = gear * 10;   // deklarert her
        std::cout << chosen << "\n";
        break;
    case 2:                       // å hoppe hit ville hoppe over
        std::cout << "Second\n";  // linjen som setter opp 'chosen'
        break;
}
```

Kompilatoren avviser den med noe slikt som *"jump to case label crosses initialization of 'int chosen'"*: å nå `case 2` ville hoppe over linjen som setter opp `chosen`, men `chosen` er fortsatt i virkeområde der, så språket nekter.

Gi case-en sitt eget virkeområde med krøllparenteser `{}`, så lever og dør variabelen inni dem:

```cpp
switch (gear) {
    case 1: {
        int chosen = gear * 10;
        std::cout << chosen << "\n";
        break;
    }
    case 2:
        std::cout << "Second\n";
        break;
}
```

Nå finnes `chosen` bare mellom krøllparentesene, så ingenting lekker inn i `case 2`. **Tommelfingerregel: i det øyeblikket en case deklarerer en variabel, pakk den case-en inn i `{}`.**

---

## `while`

Gjenta en blokk så lenge en betingelse er sann:

```cpp
int countdown = 5;
while (countdown > 0) {
    std::cout << countdown << "...\n";
    --countdown;
}
std::cout << "Go!\n";
```

Betingelsen sjekkes *før* hver iterasjon. Hvis den er usann fra start, kjører kroppen null ganger.

Den vanligste feilen med `while`-løkker er å glemme å gjøre fremgang mot avslutningsbetingelsen:

```cpp
int i = 0;
while (i < 10) {
    std::cout << i << "\n";
    // glemte ++i, uendelig løkke
}
```

Hvis programmet ditt henger, er dette det første stedet å se.

---

## `do-while`

Som `while`, men betingelsen sjekkes *etter* den første iterasjonen. Kroppen kjører derfor alltid minst én gang:

```cpp
int input;
do {
    std::cout << "Enter a positive number: ";
    std::cin >> input;
} while (input <= 0);
```

Bruk dette når arbeidet må skje før du vet om du skal fortsette. Vanlig mønster: "les inndata til brukeren oppgir noe gyldig."

---

## `for`

Når du vet hvor mange ganger du skal gå gjennom løkken, er `for` den reneste formen:

```cpp
for (int i = 0; i < 5; ++i) {
    std::cout << i << "\n";
}
// skriver ut 0, 1, 2, 3, 4
```

De tre delene inne i parentesen er:

1. **Initialisering** (`int i = 0`): kjører én gang, før løkken starter.
2. **Betingelse** (`i < 5`): sjekkes før hver iterasjon. Løkken slutter når den er usann.
3. **Oppdatering** (`++i`): kjører etter hver iterasjon.

En `for`-løkke er bare en `while`-løkke med delene ordnet for oversikt. Bruk den når du har en teller.

---

## Range-basert `for`

For å besøke hvert element i en beholder er den range-baserte `for`-løkken kortere og vanskeligere å gjøre feil enn en tellerbasert `for`:

```cpp
std::vector<int> readings{42, 17, 99, 8};

for (int value : readings) {
    std::cout << value << "\n";
}
```

Hvis du ikke trenger å endre elementene, foretrekk `const auto&` for å unngå kopiering:

```cpp
for (const auto& value : readings) {
    std::cout << value << "\n";
}
```

For å endre elementene på stedet, ta en ikke-konstant referanse:

```cpp
for (auto& value : readings) {
    value *= 2;
}
```

---

## `break`, `continue`, `return`

Disse tre endrer flyten inne i en løkke eller funksjon.

```cpp
for (int i = 0; i < 100; ++i) {
    if (i == 10) {
        break;     // gå helt ut av løkken
    }
    if (i % 2 == 0) {
        continue;  // hopp over resten av denne iterasjonen, gå til neste
    }
    std::cout << i << "\n";
}
```

- `break` går ut av den **innerste** løkken eller `switch`.
- `continue` hopper over resten av den gjeldende iterasjonen og går videre til neste.
- `return` går helt ut av funksjonen (og returnerer eventuelt en verdi).

---

## Velge riktig verktøy

| Situasjon | Bruk |
|-----------|-----|
| To eller tre grener basert på en betingelse | `if` / `else if` / `else` |
| Mange grener på én heltallslignende verdi | `switch` |
| Gjenta til en betingelse blir usann | `while` |
| Løkkekroppen må kjøre minst én gang | `do-while` |
| Fast antall iterasjoner med en teller | `for` |
| Besøke hvert element i en beholder | range-basert `for` |
| Gå tidlig ut av en løkke | `break` |
| Hopp til neste iterasjon | `continue` |
