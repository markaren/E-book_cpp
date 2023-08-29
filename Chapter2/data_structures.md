# Data structures

A data structure is a way of organizing and storing data in memory to efficiently perform various operations on that data. 
Data structures provide a way to manage and manipulate data elements, making it easier to perform tasks like insertion, deletion, searching, and sorting.

Here is an overview of common data structures:

- __Arrays:__ An array is a collection of elements of the same data type stored in contiguous memory locations. Elements can be accessed using an index. Arrays have a fixed size that needs to be specified during declaration.

- __Vectors:__ Vectors are a dynamic array implementation provided by the C++ Standard Library (STL). They can dynamically resize themselves, making them more flexible than traditional arrays. Vectors provide methods for adding, removing, and accessing elements.

- __Linked Lists:__ A linked list is a data structure consisting of nodes, where each node contains data and a reference (or pointer) to the next node in the sequence. Linked lists can be singly linked (each node points to the next) or doubly linked (each node points to both the next and previous nodes).

- __Stacks:__ A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. Elements are added and removed from the top of the stack. Common operations include push (add) and pop (remove) operations.

- __Queues:__ A queue is a linear data structure that follows the First-In-First-Out (FIFO) principle. Elements are added at the back (enqueue) and removed from the front (dequeue) of the queue.

- __Trees:__ Trees are hierarchical data structures composed of nodes. Each tree has a root node, and every node can have child nodes. Binary trees, binary search trees, and AVL trees are common variations.

- __Graphs:__ Graphs are a collection of nodes connected by edges. They can be directed (edges have a direction) or undirected. Graphs are used to represent relationships between elements.

- __Sets and Maps:__ Sets store unique elements in no particular order, while maps (also known as dictionaries) store key-value pairs. C++ provides `std::set`, `std::unordered_set`, `std::map`, and `std::unordered_map` as part of the STL.

These are just some of the common data structures in C++. Choosing the right data structure depends on the problem you're trying to solve and the efficiency you require for different operations. 
The C++ Standard Library provides implementations of many of these data structures.

## Sequence containers

Sequence containers refer to a group of container class templates in the standard library of the C++ programming language that implement storage of data elements. 
Being templates, they can be used to store arbitrary elements, such as integers or custom classes.

The following containers are defined in the current revision of the C++ standard: `array`, `vector`, `list`, `forward_list`, `deque`. 
Each of these containers implements different algorithms for data storage, which means that they have different speed guarantees for different operations

### Arrays

As mentioned, Arrays have a fixed size that needs to be specified during declaration. C provides a built-in array type, however, 
the C++ Standard Library provides a better option through its `std::array` type.

#### C-style array
```cpp
#include <iostream>

int main() {
    // Declare and initialize C-style array of integers with a fixed size
    int myArray[5] = {10, 20, 30, 40, 50};

    // Access and print array elements
    for (int i = 0; i < sizeof(myArray) / sizeof(int); ++i) {
        std::cout << "Element at index " << i << ": " << myArray[i] << std::endl;
    }

    return 0;
}
```

#### std::array

```cpp
#include <iostream>
#include <array>

int main() {
    // Declare and initialize an std::array of integers
    std::array<int, 5> myArray = {10, 20, 30, 40, 50};

    // Access and print array elements
    for (int i = 0; i < myArray.size(); ++i) { // alternativly, use for-each 
        std::cout << "Element at index " << i << ": " << myArray[i] << std::endl;
    }

    return 0;
}
```

#### Difference between C Arrays and C++ Arrays:

1. __Declaration and Initialization:__

- In C, you typically declare and initialize arrays separately, like `int myArray[5];` followed by assignment of values.
- In C++, you can combine declaration and initialization using the curly braces initializer syntax, like `int myArray[5] = {10, 20, 30, 40, 50};`.

2. __Bound Checking:__

- C arrays do not perform bounds checking. Accessing an index outside the array's bounds can lead to undefined behavior, like accessing memory that doesn't belong to the array.
- C++ STL containers like `std::array` and `std::vector` (which are similar to arrays) perform bounds checking and throw exceptions when accessing out-of-bounds indices.

3. __Passing to Functions:__

- In C, when you pass an array to a function, you're actually passing a pointer to the first element. There's no inherent mechanism to know the size of the array so you'll need to pass an additional size parameter alongside the array.
- In C++, you can use `std::array` to pass arrays with size information.

4. __Copying and Assignment:__

- C arrays don't have built-in copy mechanisms or assignment operators.
- C++ arrays (using `std::array`) can be copied directly using the assignment operator, and the copy will contain the same elements.

In summary, while C arrays and C++ arrays share some similarities, C++ introduces improvements and safer alternatives through the Standard Library, like `std::array` and containers such as `std::vector`. 
These improvements help in avoiding common pitfalls associated with C arrays.

### Vectors

A vector is essentially a dynamic array. It automatically handles memory allocation and resizing as elements are added or removed. 
This makes vectors more versatile than traditional arrays, which have a fixed size.

```cpp
#include <iostream>
#include <vector>

int main() {
    // Create a vector of integers initialized with some elements
    std::vector<int> myVector {1 ,2 3};

    // Add additional elements to the vector
    myVector.emplace_back(10);
    myVector.emplace_back(20);
    myVector.emplace_back(30);

    // Iterate through the vector using a range-based loop
    for (int element : myVector) {
        std::cout << element << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

Unless you have a very good reason not to, `std::vector` should be used for storing elements in a list-like structure.

### Linked-list

A linked list is a data structure to organize and store a collection of elements, where each element is represented by a node. Unlike arrays or vectors, which use contiguous memory to store elements, a linked list consists of a series of nodes, where each node contains both the actual data and a pointer to the next node in the list. This chain of nodes forms a linear sequence.

##### Implementation of a singly-linked list
```cpp
#include <iostream>

// Define a class for the linked list
template <class T>
class LinkedList {
    
private:
   
    // Define the structure for a singly linked list node
    template <class E>
    struct Node {
        E data;
        Node<E>* next;
    
        Node(E value) : data(value), next(nullptr) {}
    };
    
     size_t size_;
     Node<T>* head_;

public:
    LinkedList() : head_(nullptr) {}
    
    size_t size() const {
        
        return size_;
    }

    T &operator[](size_t index) {
      if (index > size_) {
        throw std::runtime_error("Index out of bounds: " + std::to_string(index));
      }
      
      auto* current = head_;
      for (int i = 0; i < index; i++) {
        current = current->next;
      }
      return current->data;
    }

    void insert(T value) {
        auto newNode = new Node<T>(value);
        if (!head_) {
            head_ = newNode;
        } else {
            auto* current = head_;
            while (current->next) {
                current = current->next;
            }
            current->next = newNode;
        }
        ++size_;
    }

    // Destructor to release memory occupied by nodes
    ~LinkedList() {
        auto* current = head_;
        while (current) {
            auto* temp = current;
            current = current->next;
            delete temp;
        }
    }
};

int main() {
    LinkedList<int> list;

    list.insert(10);
    list.insert(20);
    list.insert(30);
    list.insert(40);
    
    for (int i = 0; i < list.size(); i++) {
        std::cout << list[i] << " ";
    }
    std::cout << std::endl

    return 0;
}
```

## Maps

Maps (also known as dictionaries) store key-value pairs.

```cpp
#include <iostream>
#include <map>
#include <unordered_map>

int main() {
    // Using std::map (ordered map)
    std::map<int, std::string> orderedMap;
    orderedMap[3] = "Apple";
    orderedMap[1] = "Banana";
    orderedMap[2] = "Orange";

    std::cout << "Ordered Map:" << std::endl;
    for (const auto& entry : orderedMap) {
        std::cout << entry.first << ": " << entry.second << std::endl;
    }

    // Using std::unordered_map (unordered hash map)
    std::unordered_map<int, std::string> unorderedMap;
    unorderedMap[3] = "Cat";
    unorderedMap[1] = "Dog";
    unorderedMap[2] = "Elephant";

    std::cout << "Unordered Map:" << std::endl;
    for (const auto& entry : unorderedMap) {
        std::cout << entry.first << ": " << entry.second << std::endl;
    }

    return 0;
}
```

#### Differences between std::map and std::unordered_map:

1. __Ordering:__

- `std::map`: Stores elements in a sorted order based on the keys.
- `std::unordered_map`: Does not guarantee any specific order of elements.

2. __Performance:__

- `std::map`: Provides slower insertion and lookup times compared to std::unordered_map. Insertions and lookups have logarithmic time complexity.
- `std::unordered_map`: Provides faster insertion and lookup times on average, typically with constant-time complexity.

3. __Underlying Data Structure:__

- `std::map`: Typically implemented as a balanced binary search tree (such as a red-black tree).
- `std::unordered_map`: Implemented using a hash table.

4. __Key Type Requirements:__

- `std::map`: Requires that the key type supports comparison operations (e.g., less than) to maintain order.
- `std::unordered_map`: Requires that the key type supports hash functions and equality comparisons.

5. __Memory Usage:__

- `std::map`: Generally uses more memory due to the tree structure and additional pointers.
- `std::unordered_map`: Memory usage depends on the load factor and hash function quality, but it can be more memory-efficient in some cases.

6. __Use Cases:__

- `std::map`: Suitable when maintaining order is important or when the keys are naturally ordered.
- `std::unordered_map`: Suitable for fast data retrieval when order doesn't matter and hash-based lookup is efficient.

When choosing between `std::map` and `std::unordered_map`, consider the specific requirements of your application. 
If you need fast insertion and lookup times and order is not important, `std::unordered_map` might be a better choice. 
If you need to maintain elements in a sorted order, then `std::map` is more appropriate.

### Trees

A tree is a widely used abstract data type that represents a hierarchical tree structure with a set of connected nodes. Each node in the tree can be connected to many children (depending on the type of tree), but must be connected to exactly one parent,[1] except for the root node, which has no parent (i.e., the root node as the top-most node in the tree hierarchy). These constraints mean there are no cycles or "loops" (no node can be its own ancestor), and also that each child can be treated like the root node of its own subtree, making recursion a useful technique for tree traversal.

##### Implementation of a tree in C++

```cpp
template<class T>
class node {

public:
    node(T value) : value_(std::move(value)) {}

    T &value() {
        return value_;
    }

    const T &value() const {
        return value_;
    }

    [[nodiscard]] bool hasParent() const {
        return parent_ != nullptr;
    }

    const node<T> *parent() const {
        return parent_;
    }

    const std::vector<std::unique_ptr<node<T>>> &children() const {
        return children_;
    }

    node<T> &addChild(T child) {
        children_.emplace_back(std::make_unique<node<T>>(child));
        children_.back()->parent_ = this;
        return *(children_.back());
    }

    [[nodiscard]] size_t numChildren() const {
        return children_.size();
    }

    // implementing depth-first traversal using recursion 
    void traverse(const std::function<void(node<T> &)> &f) override {
        f(*this);
        for (auto &child: children_)) {
            child->traverse(f);
        }
    }

private:
    T value_;
    node<T> *parent_ = nullptr;
    std::vector<std::unique_ptr<node<T>>> children_;
};
```

