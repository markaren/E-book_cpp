# Maler

En **mal** er en byggetegning for en funksjon eller klasse som fungerer med *hvilken som helst* type. Kompilatoren stanser ut en spesifikk versjon hver gang du bruker den med en ny type, så `std::vector<int>` og `std::vector<double>` er to genuint forskjellige typer, begge generert fra den samme malen.

Du har allerede brukt maler hele tiden. `std::vector`, `std::array`, `std::unique_ptr`, `std::optional`, `std::map` — hver eneste av dem er en klassemal parametrisert med typen verdi den holder. Dette kapittelet forklarer hvordan mekanismen fungerer og hvordan du skriver dine egne.

---

## Funksjonsmaler {#function-templates}

Anta at du skriver en `add`-funksjon for heltall:

```cpp
int add(int a, int b) { return a + b; }
```

Du vil raskt legge sammen doubles også. Uten maler ville du skrevet en funksjon nummer to (overlasting):

```cpp
int    add(int    a, int    b) { return a + b; }
double add(double a, double b) { return a + b; }
```

Med maler skriver du funksjonen *én gang* og lar kompilatoren generere så mange versjoner du trenger:

```cpp
template <typename T>
T add(T a, T b) {
    return a + b;
}

int    sumInt    = add(5, 3);        // T er int   , instansierer add<int>
double sumDouble = add(2.5, 3.7);    // T er double, instansierer add<double>
```

Linjen `template <typename T>` sier: "det som følger er en byggetegning med en plassholder ved navn `T`." Når du kaller `add(5, 3)`, utleder kompilatoren `T = int`, genererer `add<int>(int, int)` og bruker den. Når du kaller `add(2.5, 3.7)`, genererer og bruker den `add<double>(double, double)`. To genuint forskjellige funksjoner, begge skrevet én gang.

Du kan også være eksplisitt om typen når utledningen ville vært feil eller flertydig:

```cpp
auto x = add<double>(5, 3);   // tvinger double; x er 8.0, ikke 8
```

> `typename` og `class` betyr det samme i denne sammenhengen; `template <class T>` er ekvivalent med `template <typename T>`. `typename` er litt mer moderne og er det denne boka bruker.

---

## Klassemaler {#class-templates}

Den samme ideen gjelder for klasser. En enkel innpakning:

```cpp
template <typename T>
class Box {
public:
    explicit Box(T value) : value_(std::move(value)) {}

    const T& get() const { return value_; }
    void     set(T v)    { value_ = std::move(v); }

private:
    T value_;
};

Box<int>         boxOfInt(42);
Box<std::string> boxOfText("hello");
```

`Box<int>` og `Box<std::string>` er to helt forskjellige typer generert fra den samme malen. Hver av dem er akkurat like effektiv som om du hadde skrevet den for hånd.

Klassemaler kan ha flere parametere. `std::array` er parametrisert med både elementtypen *og* størrelsen, som er fastsatt ved kompilering:

```cpp
template <typename T, std::size_t N>
class array { /* ... */ };

std::array<int, 5>      readings;          // 5 int-er
std::array<double, 100> moreReadings;      // 100 double-er
```

`std::map` er parametrisert med nøkkeltype *og* verditype:

```cpp
std::map<std::string, int> wordCounts;
```

Hver gang du ser vinkelparenteser i C++, ser du på en mal som blir instansiert.

---

## Maler bor i headeren {#templates-live-in-the-header}

[Klasser](../Chapter4/classes.md#splitting-the-declaration-and-the-implementation) lærte deg å dele en vanlig klasse i en `.hpp` (deklarasjoner) og en `.cpp` (definisjoner). **For maler skal du ikke gjøre dette.** En mal er bare en byggetegning: kompilatoren genererer den virkelige koden på stedet der du bruker den med en konkret type, og for å gjøre det må den kunne *se hele definisjonen* akkurat der. Hvis kroppen bor i en separat `.cpp`, kan ikke filen som bruker `Box<int>` se den, og du får en `undefined reference`-feil fra linkeren — for kode som ser helt korrekt ut.

Så hold maler **helt og holdent i headeren**: deklarasjon og definisjon sammen, ingen `.cpp`. Dette er det ene stedet der del-det-opp-vanen ikke gjelder.

---

## Hvorfor bruke maler? {#why-use-templates}

| Fordel | Hva det betyr |
|---------|---------------|
| **Gjenbruk** | Skriv algoritmen eller beholderen én gang; den fungerer med enhver type som støtter operasjonene du bruker. |
| **Ytelse** | Maler avgjøres fullt og helt ved kompilering. Det er ingen kostnad ved kjøring; `add<int>` kompilerer til samme maskinkode som en håndskrevet heltalls-`add`. |
| **Typesikkerhet** | Kompilatoren sjekker fortsatt hver type. `add<int>("hello", 3)` kompilerer ikke. |

Kostnaden er kompileringstid: hver malinstansiering er i praksis en fersk runde med kompilering. Tung bruk av maler gjør byggene tregere.

---

## `auto` og utledning av malargumenter {#auto-and-template-argument-deduction}

`auto` er malenes lettvektsslektning. Den lar kompilatoren utlede typen til en variabel fra initialisereren dens:

```cpp
auto i = 42;            // int
auto x = 3.14;          // double
auto name = std::string("Alice");

std::vector<int> v{1, 2, 3};
auto it = v.begin();    // std::vector<int>::iterator, sparte deg for mye skriving
```

For områdebaserte `for`-løkker er `auto` og `const auto&` de klart vanligste formene:

```cpp
for (const auto& value : v) {
    std::cout << value << "\n";
}
```

`auto` endrer ingenting ved hvordan C++-typer fungerer; typen er fortsatt fast og sjekkes ved kompilering, kompilatoren bare finner den ut for deg. Det er det samme maskineriet malene bruker, anvendt på én variabel om gangen.

---

## Hvordan malfeil ser ut {#what-template-errors-look-like}

Det desidert mest skremmende med maler er kompileringsfeilene deres. En feil type sendt til `std::sort` kan produsere en skjermfull sjargong som nevner iteratorer, type traits og SFINAE.

Ta en enkel feil:

<!-- no-ce -->
```cpp
#include <string>

template <typename T>
T add(T a, T b) { return a + b; }

int main() {
    std::string s = "x";
    add(s, 5);              // feil, T kan ikke være både std::string og int
}
```

GCC vil skrive noe slikt som:

```
error: no matching function for call to 'add(std::string&, int)'
note: candidate: 'template<class T> T add(T, T)'
note:   template argument deduction/substitution failed:
note:   deduced conflicting types for parameter 'T'
        ('std::__cxx11::basic_string<char>' and 'int')
```

Veggen av tekst er kompilatoren som lister opp hver kandidat den vurderte, og hvorfor den forkastet hver av dem. To lesetips som håndterer 90 % av tilfellene:

1. **Les fra toppen.** Den første linjen er den opprinnelige feilen i koden din. Alt under er kompilatoren som forklarer resonnementet sitt.
2. **Se etter `note:`-linjene under hver kandidat.** De forteller deg *hvorfor* en mal ble forkastet — her `deduction/substitution failed` etterfulgt av `deduced conflicting types for parameter 'T'`, altså det enkle typeavviket ovenfor.

De fleste "skumle" malfeil er egentlig bare typeavvik med mye støttende detalj. Når du har dekodet noen få, slutter du å være redd for resten.

---

## Lambdaer: malenes nære slektning {#lambdas-templates-close-cousin}

Mange av algoritmene malene driver (`std::sort`, `std::find_if`, `std::count_if`), tar et funksjonsargument. **Lambdauttrykk** er måten du skriver de funksjonsargumentene inline på:

```cpp
std::vector<int> v = {5, 2, 8, 1, 9, 3};
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });   // synkende
```

Se referansesiden [Lambdauttrykk](../lambdas.md) for hele historien.

---

## Når du skriver en mal selv {#when-to-write-a-template-yourself}

I små kursprosjekter *bruker* du for det meste maler i stedet for å skrive dem. To tilfeller der det å skrive en genuint er riktig verktøy:

- **En beholder som skal holde hvilken som helst type.** En egen ringbuffer, en trådsikker kø, en matrise med fast størrelse — alle er naturlig generiske.
- **En algoritme som ikke bryr seg om elementtypen.** En `sum`, `clamp`, `find_max` og så videre.

Hvis du skriver den samme funksjonen med `int`, så med `double`, så med `float`, har du en mal som venter på å bli skrevet.

---

## Oppsummering {#summary}

- En mal er en byggetegning; kompilatoren stanser ut konkrete versjoner for hver type du bruker.
- Funksjonsmaler fjerner nesten identiske overlastinger.
- Klassemaler er det hver standardbeholder er bygget på.
- `auto` er hverdagsansiktet til det samme typeutledningsmaskineriet.
- Malfeilmeldinger er lange, men mekaniske: les fra toppen, se etter "candidate ignored"-notene.
- Skriv din egen mal når du tar deg selv i å duplisere kode som bare skiller seg i typen som er involvert.
