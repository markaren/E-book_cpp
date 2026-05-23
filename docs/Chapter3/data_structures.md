# Data Structures

A **data structure** is a way of organising data so that the operations you need to perform on it are efficient. The choice of structure shapes how fast your program runs and how clean the code that uses it looks.

This chapter is about *choosing*. C++'s standard library provides solid, well-tested implementations of every data structure you will need this semester; your job is to pick the right one for the job. We will look at what each one is good at and let go of the temptation to implement them from scratch.

---

## The mental model

Every data structure is a trade-off. Adding to one is fast; finding in another is fast; iterating in order through a third is fast. There is no "best" data structure; only the one that fits the operations you actually do.

The questions to ask:

1. **How will I add items?** At the end, at the front, in the middle?
2. **How will I find items?** By index, by key, by scanning?
3. **Do I need them in order?** Insertion order, sorted order, or no order?
4. **Will the size change?** At compile time, at runtime, often, rarely?

The answers usually pick the container for you.

---

## Sequence containers

Containers that store a linear sequence of values.

### `std::vector<T>`: dynamic array

Elements live in **contiguous memory**, like a C array, but the size can grow at runtime.

```cpp
#include <vector>

std::vector<int> readings;
readings.push_back(42);          // add to the end, fast
readings.push_back(17);
readings.push_back(99);

int first = readings[0];         // index access, constant time
readings.size();                 // 3
```

| Operation | Cost |
|-----------|------|
| Index access (`v[i]`) | O(1) |
| `push_back` (append) | O(1) amortised |
| Insert/remove in the middle | O(n), everything after has to shift |
| Find by value (`std::find`) | O(n) |

**Use vector by default.** Only reach for something else if your usage pattern genuinely conflicts with what vector is good at.

### `std::array<T, N>`: fixed-size array

Like `std::vector` but the size is fixed at compile time. Lives on the stack, no heap allocation.

```cpp
#include <array>

std::array<double, 3> position = {0.0, 0.0, 0.0};
position[2] = 1.5;
```

**Use when** the size is known and won't change: fixed-length sensor packets, lookup tables, matrix dimensions.

### `std::deque<T>`: double-ended queue

Like `vector`, but also fast to add or remove at the **front**.

```cpp
#include <deque>

std::deque<int> buffer;
buffer.push_back(1);     // add at the back
buffer.push_front(0);    // add at the front, fast
```

The cost is that elements are not in one contiguous block, so it's slightly less cache-friendly than a vector. **Use when** you need fast inserts at both ends.

### `std::list<T>`: doubly linked list

Each element holds pointers to the next and previous. Insertions and deletions anywhere in the list are O(1) — but you also lose O(1) index access and most of the cache-friendliness of `vector`.

```cpp
#include <list>

std::list<int> jobs;
jobs.push_back(1);
jobs.push_front(0);
// jobs[2] does NOT work, no index access
```

In practice, `std::list` is rarely the right choice. Modern hardware loves contiguous memory; the constant-factor cost of pointer-chasing through a linked list often outweighs the algorithmic advantage. **Use only when** you specifically need to splice items between lists, or remove from the middle while holding an iterator to the item.

---

## Associative containers

Containers that store key-value pairs (or just keys), with fast lookup by key.

### `std::map<K, V>`: sorted key-value store

Keys are kept sorted. Lookup, insertion, and deletion are O(log n).

```cpp
#include <map>

std::map<std::string, double> sensorOffsets;
sensorOffsets["temp"]    = -0.5;
sensorOffsets["voltage"] = 0.01;

double t = sensorOffsets["temp"];       // -0.5
sensorOffsets.contains("temp");          // true

for (const auto& [name, offset] : sensorOffsets) {   // [name, offset] splits each key/value pair
    // iterates in alphabetical order of key
}
```

**Use when** you need fast key lookup *and* you want to iterate in sorted order, *or* you want to do range queries on keys.

### `std::unordered_map<K, V>`: hash-based key-value store

Same interface as `std::map`, but unordered. Backed by a hash table, so lookups are O(1) on average.

```cpp
#include <unordered_map>

std::unordered_map<int, std::string> users;
users[1] = "alice";
users[2] = "bob";
```

| Property | `std::map` | `std::unordered_map` |
|----------|------------|----------------------|
| Underlying structure | Balanced tree | Hash table |
| Lookup | O(log n) | O(1) average |
| Order of iteration | Sorted by key | Unspecified |
| Memory overhead per element | Higher | Lower (usually) |
| Required from the key type | Less-than comparison | Hash + equality |

**Default to `unordered_map`.** Pick `map` when you want ordering.

### `std::set` and `std::unordered_set`

Same as the maps, but storing only keys (no values). Useful for "have I seen this?" and de-duplicating data.

```cpp
#include <unordered_set>

std::unordered_set<int> seen;
if (seen.insert(42).second) {
    std::cout << "first time seeing 42\n";
}
```

---

## Container adapters

Three convenience wrappers built on top of other containers, exposing only the operations of a classic data structure.

| Adapter | Behaviour |
|---------|-----------|
| `std::stack<T>` | LIFO (last in, first out): push, pop, top |
| `std::queue<T>` | FIFO (first in, first out): push, pop, front |
| `std::priority_queue<T>` | Always pops the largest element |

```cpp
#include <stack>

std::stack<int> calls;
calls.push(1);
calls.push(2);
calls.top();   // 2
calls.pop();
calls.top();   // 1
```

These are convenient when the algorithm you are implementing genuinely needs a stack or queue. For most purposes, a `vector` exposes everything they do and more.

---

## Choosing: a decision table

| You need to… | Use |
|--------------|-----|
| Hold a list of values, grow at the end | `std::vector` |
| Hold a fixed-size collection | `std::array` |
| Hold a list, grow at both ends | `std::deque` |
| Map keys to values, lookup fast | `std::unordered_map` |
| Map keys to values, iterate in order | `std::map` |
| Track which items you have seen | `std::unordered_set` |
| LIFO behaviour | `std::stack` |
| FIFO behaviour | `std::queue` |
| Always pop the highest priority | `std::priority_queue` |

When in doubt, start with `std::vector` or `std::unordered_map`. They cover more cases than any other two containers.

---

## Trees, graphs, and "why isn't there a `std::tree`?"

You may notice that the standard library does *not* ship with a general-purpose tree or graph container. That is intentional: trees and graphs come in too many shapes (binary, n-ary, balanced, weighted, directed, …) for one container to fit them all.

When you need a tree, build it out of nodes with `std::unique_ptr` children. (This snippet uses templates and `std::unique_ptr`, both from Chapters 4–5 — skim it for now.)

```cpp
template <typename T>
struct TreeNode {
    T value;
    std::vector<std::unique_ptr<TreeNode<T>>> children;
};
```

When you need a graph, an "adjacency list" — `std::unordered_map<NodeId, std::vector<NodeId>>` — is usually all you need. Specialised libraries exist (Boost.Graph, for example) when the algorithms get serious.

Implementing these from scratch is a fine learning exercise, but for production code, prefer the library where one exists.

---

## Summary

- The standard library covers every basic data structure you need this semester.
- `std::vector` is your default sequence; `std::unordered_map` is your default lookup table.
- Linked lists exist but are usually not what you want; `std::vector` is cache-friendlier.
- Trees and graphs are not in the standard library; build them out of `std::unique_ptr` and `std::vector`.
- Pick a container by asking how you will add, find, and order the elements, not which one sounds clever.
