# Chapter 3 Exercises

Work through these after reading Chapter 3. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Each exercise is a small program with its own `main()`. Now that you have read [CMake](../Chapter2/cmake_intro.md), you can keep them in one project — one `add_executable` line per file — and pick which to run from the dropdown next to the green ▶ button.

---

## 1. Sensor statistics

*Practises: [C++ Standard Library](standard_library.md)*

Put these readings in a `std::vector<int>`: `17, 42, 99, 8, 23`. Then, using **standard-library algorithms** rather than hand-written loops, print three things: the readings **sorted** ascending, their **sum**, and the **largest** value.

> Hint: `<algorithm>` has `std::sort` and `std::max_element`; `<numeric>` has `std::accumulate`. Each takes a `.begin(), .end()` range.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>
    #include <numeric>

    int main() {
        std::vector<int> readings = {17, 42, 99, 8, 23};

        std::sort(readings.begin(), readings.end());

        int sum = std::accumulate(readings.begin(), readings.end(), 0);
        int largest = *std::max_element(readings.begin(), readings.end());

        std::cout << "Sorted:";
        for (int r : readings) {
            std::cout << " " << r;
        }
        std::cout << "\n";

        std::cout << "Sum: " << sum << "\n";
        std::cout << "Largest: " << largest << "\n";
    }
    ```

    Each algorithm works on the whole container via the `.begin(), .end()` range. `std::max_element` returns an *iterator* to the largest element, so the `*` in front reads the value it points at. Letting the library sort and sum for you is shorter and harder to get wrong than writing the loops by hand — the chapter's main point.

    </div>

---

## 2. Count the colours

*Practises: [Data Structures](data_structures.md)*

You are given a list of colour names, some repeated — `{"red", "green", "red", "blue", "green", "red"}`. Count how many times each colour appears, then print each colour with its count. Use the container the chapter recommends for counting by key.

> Hint: looking up a missing key in a map creates it with the value `0`, so `++counts[colour]` does the right thing the first time too.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>
    #include <vector>
    #include <map>

    int main() {
        std::vector<std::string> colours = {"red", "green", "red", "blue", "green", "red"};

        std::map<std::string, int> counts;
        for (const std::string& colour : colours) {
            ++counts[colour];
        }

        for (const auto& [colour, count] : counts) {
            std::cout << colour << ": " << count << "\n";
        }
    }
    ```

    `++counts[colour]` works because the first lookup of a new key inserts it with a value-initialised `0`, which the `++` then makes `1`. Using `std::map` prints the colours in alphabetical order; `std::unordered_map` would count them just as well but in no particular order. The `[colour, count]` in the loop is a *structured binding* — it splits each key/value pair into two named pieces, exactly as the chapter showed.

    </div>

---

## 3. Count the distinct IDs

*Practises: [Data Structures](data_structures.md)*

A stream of sensor IDs arrives, with some repeats — `{4, 8, 4, 15, 16, 8, 23, 42, 16}`. Print how many **distinct** IDs there were. Use the container designed for the "have I seen this before?" question.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>
    #include <unordered_set>

    int main() {
        std::vector<int> ids = {4, 8, 4, 15, 16, 8, 23, 42, 16};

        std::unordered_set<int> distinct(ids.begin(), ids.end());

        std::cout << "Distinct IDs: " << distinct.size() << "\n";
    }
    ```

    A set silently discards duplicates, so once every ID has gone in, its `size()` *is* the count of distinct values. Building the set straight from the vector's `begin(), end()` range is the shortest way; inserting in a loop would work too. The chapter's decision table points to a set for exactly this "track which items I have seen" job.

    </div>
