# Move semantics

Move semantics is a feature introduced in C++11 that allows you to efficiently transfer the ownership of resources from one object to another without unnecessary copying. This can lead to significant performance improvements in certain situations where copying large amounts of data can be expensive.


```cpp
#include <iostream>
#include <string>

int main() {
    std::string source = "Hello, World!";  // Create a string
    std::string destination = source;       // Copy the string to another variable

    // Output both strings
    std::cout << "Source: " << source << std::endl;
    std::cout << "Destination: " << destination << std::endl;

    return 0;
}
```

In this example, we create a string named source and then copy its content to another string called destination. This copying process can be inefficient, especially if the string is large because it duplicates the data, consuming more memory and time.

Now, let's use move semantics to make this more efficient:

```cpp
#include <iostream>
#include <string>
#include <utility> //std::move

int main() {
    std::string source = "Hello, World!";  // Create a string
    std::string destination = std::move(source);  // Move the string to another variable

    // Output both strings
    std::cout << "Source: " << source << std::endl;
    std::cout << "Destination: " << destination << std::endl;

    return 0;
}
```

In this updated example, we use `std::move` to _transfer_ the contents of source to destination. This means we're not making a copy; instead, we're essentially saying, "You, destination, take ownership of what's in source," which is much faster and uses less memory. After the move, source is still there, but its content is unspecified (usually, it's an empty string in the case of strings). Meanwhile, destination has the original content.

### Summary

Move semantics allows us to efficiently hand over resources (like strings or memory) from one object to another without making unnecessary copies, which can be faster and more memory-efficient. It's like passing a toy car from one child to another without making an extra copy of the car.

Move semantics are particularly useful when working with containers like std::vector or when returning objects from functions, as they can help minimize unnecessary copying and improve performance. However, it's important to be aware of the potential pitfalls, like accessing moved-from objects, to use move semantics effectively in C++.
