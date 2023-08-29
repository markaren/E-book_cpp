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

- __Sets and Maps:__ Sets store unique elements in no particular order, while maps (also known as dictionaries) store key-value pairs. C++ provides std::set, std::unordered_set, std::map, and std::unordered_map as part of the STL.

- __Strings:__ Strings are sequences of characters. C++ provides both C-style strings (character arrays) and the std::string class in the Standard Library for string manipulation.

These are just some of the common data structures in C++. Choosing the right data structure depends on the problem you're trying to solve and the efficiency you require for different operations. 
The C++ Standard Library provides implementations of many of these data structures.

## Arrays

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

### Difference between C Arrays and C++ Arrays:

1. __Declaration and Initialization:__

- In C, you typically declare and initialize arrays separately, like int myArray[5]; followed by assignment of values.
- In C++, you can combine declaration and initialization using the curly braces initializer syntax, like int myArray[5] = {10, 20, 30, 40, 50};.

2. __Bound Checking:__

- C arrays do not perform bounds checking. Accessing an index outside the array's bounds can lead to undefined behavior, like accessing memory that doesn't belong to the array.
- C++ STL containers like `std::array` and `std::vector` (which are similar to arrays) perform bounds checking and throw exceptions when accessing out-of-bounds indices.

3. __Passing to Functions:__

- In C, when you pass an array to a function, you're actually passing a pointer to the first element. There's no inherent mechanism to know the size of the array within the function.
- In C++, you can use Standard Library containers like std::array or reference parameters to pass arrays with size information.

4. __Copying and Assignment:__

- C arrays don't have built-in copy mechanisms or assignment operators.
- C++ arrays (using `std::array`) can be copied directly using the assignment operator, and the copy will contain the same elements.

5. __Dynamic Arrays:__

- In C, dynamic memory allocation using functions like malloc and free is commonly used to create arrays with sizes determined at runtime.
- In C++, std::vector provides dynamic arrays that can grow or shrink dynamically while managing memory automatically.

In summary, while C arrays and C++ arrays share some similarities, C++ introduces improvements and safer alternatives through the Standard Library, like `std::array` and containers such as `std::vector`. 
These improvements help in avoiding common pitfalls associated with C arrays.

#### Vectors


### Linked-list


#### Implementation of a singly-linked list
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

    // Function to insert a new node at the end of the list
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
        std::cout << list[i] << std::endl;
    }

    return 0;
}

```

### Maps

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

- std::map: Stores elements in a sorted order based on the keys.
- std::unordered_map: Does not guarantee any specific order of elements.

2. __Performance:__

- std::map: Provides slower insertion and lookup times compared to std::unordered_map. Insertions and lookups have logarithmic time complexity.
- std::unordered_map: Provides faster insertion and lookup times on average, typically with constant-time complexity.

3. __Underlying Data Structure:__

- std::map: Typically implemented as a balanced binary search tree (such as a red-black tree).
- std::unordered_map: Implemented using a hash table.

4. __Key Type Requirements:__

- std::map: Requires that the key type supports comparison operations (e.g., less than) to maintain order.
- std::unordered_map: Requires that the key type supports hash functions and equality comparisons.

5. __Memory Usage:__

- std::map: Generally uses more memory due to the tree structure and additional pointers.
- std::unordered_map: Memory usage depends on the load factor and hash function quality, but it can be more memory-efficient in some cases.

6. __Use Cases:__

- std::map: Suitable when maintaining order is important or when the keys are naturally ordered.
- std::unordered_map: Suitable for fast data retrieval when order doesn't matter and hash-based lookup is efficient.

When choosing between std::map and std::unordered_map, consider the specific requirements of your application. If you need fast insertion and lookup times and order is not important, std::unordered_map might be a better choice. If you need to maintain elements in a sorted order, then std::map is more appropriate.
