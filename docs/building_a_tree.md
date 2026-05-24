# Building a Tree

The standard library deliberately ships no general-purpose tree — hierarchies come in too many shapes for one container to fit them all (see [Data Structures](Chapter3/data_structures.md)). You will rarely *need* to build one. But when the data is genuinely tree-shaped, you assemble a tree from pieces you already know: a node owns its children, `std::unique_ptr` takes care of the memory, and recursion walks the structure.

This page builds a small, reusable tree and uses it to model a **family tree**. It pulls together [templates](Chapter5/templates.md), [smart pointers](Chapter5/memory.md), and [recursion](recursion.md), so it doubles as a worked example of how those fit together. If you have not met those chapters yet, skim — the shape is the point.

---

## The node: a value and its children

A tree is made of **nodes**. Each node holds a value and owns a list of child nodes:

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

Two decisions carry the whole design:

- **`template <typename T>`** lets the tree hold any type — `std::string` for our family tree, but equally an `int`, a sensor reading, or your own class. (See [Templates](Chapter5/templates.md).)
- **`std::unique_ptr<TreeNode<T>>` for each child** means a node *owns* its children. When a node is destroyed, its `unique_ptr`s destroy the children, which destroy *their* children, and so on — the entire subtree cleans itself up with no `delete` from you. That is [RAII](Chapter4/raii.md) applied to a data structure. (See [Memory Management](Chapter5/memory.md).)

---

## Adding children

A small helper attaches a child and hands back a reference to it, so you can keep building from the node you just created:

```cpp
template <typename T>
struct TreeNode {
    // ... value and children, as above ...

    TreeNode<T>& addChild(T childValue) {
        children.push_back(std::make_unique<TreeNode<T>>(std::move(childValue)));
        return *children.back();
    }
};
```

`std::make_unique` builds the child on the heap and wraps it in a `unique_ptr` in one step. Returning `TreeNode<T>&` is what lets you add grandchildren to a child without hunting for it again.

---

## Walking the tree

A tree is recursive by nature — a tree is *a node plus a list of smaller trees* — so the operations on it are recursive too (see [Recursion](recursion.md)). Printing it with indentation per level:

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

Counting everyone is the same shape — one for this node, plus the count of each subtree:

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

## A family tree

Now use it: each person is a node, and their children are — their children.

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

(The names are plain ASCII on purpose — see [Computer Basics](computer_basics.md#ascii) for why non-English letters in source code invite trouble.)

---

## The complete program

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

It prints:

```
Ada
  Ben
    Cara
    Dan
  Eve
    Finn
6 people in the tree
```

Notice what is *not* there: no `delete`, no destructor, no cleanup code. When `family` goes out of scope at the end of `main`, its `unique_ptr` children release the whole tree automatically.

---

## When to build your own

Most of the time you should not. A `std::vector` or `std::map` models flatter data with far less ceremony; reach for a hand-built tree only when the structure is genuinely hierarchical — a file system, an org chart, a scene graph, a parse tree. And when you need real tree or graph *algorithms* (balancing, shortest paths), prefer a dedicated library over rolling your own.

But the pattern shown here — **nodes owning their children through `unique_ptr`, recursion to walk them** — is the backbone underneath all of those. Build it once by hand and the library versions stop looking like magic.
