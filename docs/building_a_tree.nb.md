# Bygge et tre

Standardbiblioteket leveres bevisst uten et generelt tre — hierarkier finnes i for mange former til at én beholder kan passe alle (se [Datastrukturer](Chapter3/data_structures.md)). Du vil sjelden *trenge* å bygge ett. Men når dataene virkelig er treformede, setter du sammen et tre av deler du allerede kjenner: en node eier barna sine, `std::unique_ptr` tar seg av minnet, og rekursjon går gjennom strukturen.

Denne siden bygger et lite, gjenbrukbart tre og bruker det til å modellere et **familietre**. Den fletter sammen [maler](Chapter5/templates.md), [smartpekere](Chapter5/memory.md) og [rekursjon](recursion.md), så den fungerer også som et arbeidseksempel på hvordan disse passer sammen. Har du ikke møtt de kapitlene ennå, så skum gjennom — det er formen som er poenget.

---

## Noden: en verdi og barna sine

Et tre består av **noder**. Hver node holder en verdi og eier en liste med barnenoder:

```cpp
#include <memory>
#include <vector>

template <typename T>
struct TreeNode {
    T value;
    std::vector<std::unique_ptr<TreeNode<T>>> children;

    explicit TreeNode(T v) : value(std::move(v)) {}
};
```

To valg bærer hele designet:

- **`template <typename T>`** lar treet holde hvilken som helst type — `std::string` for familietreet vårt, men like gjerne en `int`, en sensoravlesning eller din egen klasse. (Se [Maler](Chapter5/templates.md).)
- **`std::unique_ptr<TreeNode<T>>` for hvert barn** betyr at en node *eier* barna sine. Når en node ødelegges, ødelegger dens `unique_ptr`-er barna, som ødelegger *sine* barn, og så videre — hele undertreet rydder opp etter seg selv uten et eneste `delete` fra deg. Det er [RAII](Chapter4/raii.md) anvendt på en datastruktur. (Se [Minnehåndtering](Chapter5/memory.md).)

---

## Å legge til barn

En liten hjelpefunksjon fester et barn og gir tilbake en referanse til det, så du kan bygge videre fra noden du nettopp opprettet:

```cpp
template <typename T>
struct TreeNode {
    // ... value og children, som over ...

    TreeNode<T>& addChild(T childValue) {
        children.push_back(std::make_unique<TreeNode<T>>(std::move(childValue)));
        return *children.back();
    }
};
```

`std::make_unique` bygger barnet på heapen og pakker det i en `unique_ptr` i ett steg. At den returnerer `TreeNode<T>&` er det som lar deg legge barnebarn til et barn uten å lete det opp igjen.

---

## Å gå gjennom treet

Et tre er rekursivt av natur — et tre er *en node pluss en liste med mindre trær* — så operasjonene på det er også rekursive (se [Rekursjon](recursion.md)). Å skrive det ut med innrykk per nivå:

```cpp
template <typename T>
void print(const TreeNode<T>& node, int depth = 0) {
    for (int i = 0; i < depth; ++i) {
        std::cout << "  ";
    }
    std::cout << node.value << "\n";
    for (const auto& child : node.children) {
        print(*child, depth + 1);
    }
}
```

Å telle alle er samme form — én for denne noden, pluss antallet i hvert undertre:

```cpp
template <typename T>
int countNodes(const TreeNode<T>& node) {
    int total = 1;
    for (const auto& child : node.children) {
        total += countNodes(*child);
    }
    return total;
}
```

---

## Et familietre

Nå bruker vi det: hver person er en node, og barna deres er — barna deres.

```cpp
TreeNode<std::string> family("Ada");

TreeNode<std::string>& ben = family.addChild("Ben");
ben.addChild("Cara");
ben.addChild("Dan");

TreeNode<std::string>& eve = family.addChild("Eve");
eve.addChild("Finn");

print(family);
std::cout << countNodes(family) << " people in the tree\n";
```

(Navnene er ren ASCII med vilje — se [Datamaskingrunnlag](computer_basics.md#ascii) for hvorfor ikke-engelske bokstaver i kildekode inviterer til trøbbel.)

---

## Det komplette programmet

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <vector>

template <typename T>
struct TreeNode {
    T value;
    std::vector<std::unique_ptr<TreeNode<T>>> children;

    explicit TreeNode(T v) : value(std::move(v)) {}

    TreeNode<T>& addChild(T childValue) {
        children.push_back(std::make_unique<TreeNode<T>>(std::move(childValue)));
        return *children.back();
    }
};

template <typename T>
void print(const TreeNode<T>& node, int depth = 0) {
    for (int i = 0; i < depth; ++i) {
        std::cout << "  ";
    }
    std::cout << node.value << "\n";
    for (const auto& child : node.children) {
        print(*child, depth + 1);
    }
}

template <typename T>
int countNodes(const TreeNode<T>& node) {
    int total = 1;
    for (const auto& child : node.children) {
        total += countNodes(*child);
    }
    return total;
}

int main() {
    TreeNode<std::string> family("Ada");

    TreeNode<std::string>& ben = family.addChild("Ben");
    ben.addChild("Cara");
    ben.addChild("Dan");

    TreeNode<std::string>& eve = family.addChild("Eve");
    eve.addChild("Finn");

    print(family);
    std::cout << countNodes(family) << " people in the tree\n";
}
```

Det skriver ut:

```
Ada
  Ben
    Cara
    Dan
  Eve
    Finn
6 people in the tree
```

Legg merke til hva som *ikke* er der: ingen `delete`, ingen destruktor, ingen oppryddingskode. Når `family` går ut av virkeområdet på slutten av `main`, frigjør dens `unique_ptr`-barn hele treet automatisk.

---

## Når du bør bygge ditt eget

For det meste bør du ikke. En `std::vector` eller `std::map` modellerer flatere data med langt mindre styr; grip etter et håndbygd tre bare når strukturen virkelig er hierarkisk — et filsystem, et organisasjonskart, en scenegraf, et parse-tre. Og når du trenger ekte tre- eller graf-*algoritmer* (balansering, korteste vei), foretrekk et dedikert bibliotek framfor å lage ditt eget.

Men mønsteret som vises her — **noder som eier barna sine gjennom `unique_ptr`, rekursjon for å gå gjennom dem** — er ryggraden under dem alle. Bygg det én gang for hånd, så slutter biblioteksversjonene å se ut som magi.
