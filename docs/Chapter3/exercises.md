# Chapter 3 Exercises

Work through these after reading Chapter 3. **Try each one yourself before revealing the solution** — you learn far more from an honest attempt than from reading a finished answer. Type the code into CLion and run it; do not just read it.

When you open a solution it appears **blurred** — click it once more to reveal it, so you do not see the answer by accident.

Each exercise is a small program with its own `main()`. Now that you have read [CMake](../Chapter2/cmake_intro.md), you can keep them in one project — one `add_executable` line per file — and pick which to run from the dropdown next to the green ▶ button.

---

## 1. Sensor statistics

*Practises: [C++ Standard Library](standard_library.md)*

Put these readings in a `std::vector<int>`: `17, 42, 99, 8, 23`. Then, using **standard-library algorithms** rather than hand-written loops, print three things: the readings **sorted** ascending, their **sum**, and the **largest** value.

> Hint: prefer the C++20 `std::ranges::` forms — `std::ranges::sort(v)` and `std::ranges::max_element(v)` take the container directly. `<numeric>` has `std::accumulate`, which has no ranges form in C++20, so it still takes a `.begin(), .end()` range.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>
    #include <numeric>

    int main() {
        std::vector<int> readings = {17, 42, 99, 8, 23};

        std::ranges::sort(readings);

        int sum = std::accumulate(readings.begin(), readings.end(), 0);
        int largest = *std::ranges::max_element(readings);

        std::cout << "Sorted:";
        for (int r : readings) {
            std::cout << " " << r;
        }
        std::cout << "\n";

        std::cout << "Sum: " << sum << "\n";
        std::cout << "Largest: " << largest << "\n";
    }
    ```

    The `std::ranges::` versions take the container directly — shorter, and you cannot accidentally mismatch a `begin()` from one container with an `end()` from another. `std::ranges::max_element` returns an *iterator* to the largest element, so the `*` in front reads the value it points at. `std::accumulate` keeps the classic `.begin(), .end()` form because C++20 gives it no ranges version (the range-based fold arrived only in C++23). Letting the library sort and sum for you is shorter and harder to get wrong than writing the loops by hand — the chapter's main point.

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

        std::unordered_set<int> distinct;
        for (int id : ids) {
            distinct.insert(id);      // a repeat is silently ignored
        }

        std::cout << "Distinct IDs: " << distinct.size() << "\n";
    }
    ```

    A set silently discards duplicates, so once every ID has gone in, its `size()` *is* the count of distinct values. The chapter's decision table points to a set for exactly this "track which items I have seen" job.

    **Shorter alternative:** a set can be built straight from a range of values, so `std::unordered_set<int> distinct(ids.begin(), ids.end());` does the whole loop in one line. Both give the same answer.

    </div>

---

## 4. Split a `name:value` setting

*Practises: [Strings](../strings.md)*

Configuration lines often look like `"speed:120"` — a name, a colon, then a value. Given the string `"speed:120"`, split it at the colon and print the name and the value on their own lines. Then convert the value to an `int` and print double it.

Expected output:

```
name  = speed
value = 120
doubled = 240
```

> Hint: `find(':')` gives you the index of the colon; `substr` takes the part before and the part after. `std::stoi` turns the value text into an `int`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <string>

    int main() {
        std::string line = "speed:120";

        std::size_t colon = line.find(':');
        std::string name  = line.substr(0, colon);   // before the colon
        std::string value = line.substr(colon + 1);  // after the colon

        std::cout << "name  = " << name << "\n";
        std::cout << "value = " << value << "\n";

        int n = std::stoi(value);
        std::cout << "doubled = " << n * 2 << "\n";
    }
    ```

    `find(':')` returns the index of the colon; `substr(0, colon)` takes the `colon` characters before it, and `substr(colon + 1)` takes everything from just after it to the end. `std::stoi` then turns `"120"` into the number `120`. (A robust parser would check `find` did not return `std::string::npos` first — here we know the colon is there.)

    </div>

---

## 5. Count the readings above a threshold

*Practises: [Lambda Expressions](../lambdas.md)*

You have these sensor readings in a `std::vector<double>`: `{22.5, 19.0, 31.2, 18.7, 25.0, 40.1}`. Using `std::ranges::count_if` with a **lambda**, count how many are above `24.0`, and print the count.

Expected output:

```
Above threshold: 3
```

> Hint: `std::ranges::count_if(v, predicate)` counts the elements for which `predicate` returns `true`. The predicate is a lambda taking one `double` and returning a `bool`.

??? success "Show solution"

    <div class="spoiler" markdown title="Click to reveal">

    ```cpp
    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main() {
        std::vector<double> readings = {22.5, 19.0, 31.2, 18.7, 25.0, 40.1};
        const double threshold = 24.0;

        int above = std::ranges::count_if(readings,
                        [threshold](double r) { return r > threshold; });

        std::cout << "Above threshold: " << above << "\n";
    }
    ```

    The lambda `[threshold](double r) { return r > threshold; }` is the test applied to each reading; `std::ranges::count_if` runs it over the whole vector and returns how many times it was `true`. Capturing `threshold` by value lets the lambda use it without it being a global. Three readings — `31.2`, `25.0`, and `40.1` — clear `24.0`.

    </div>
