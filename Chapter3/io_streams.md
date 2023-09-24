# C++ Input/Output and File Streams

In C++, Input/Output (I/O) operations play a crucial role in interacting with the user, reading data from external sources, 
and writing data to files. C++ provides a comprehensive set of tools for performing these operations, 
including standard input and output streams, as well as file streams.

## Standard Input and Output Streams

C++ offers two primary standard I/O streams:

- **`cin`**: This is the standard input stream, often used for reading data from the user via the keyboard. It's connected to the console by default.
- **`cout`**: This is the standard output stream, used for displaying data to the console. You can use `cout` to print information, results, or messages to the screen.

Here's a simple example of using `cin` and `cout`:

```cpp
#include <iostream>

int main() {
    int number;
    std::cout << "Enter a number: ";
    std::cin >> number;
    std::cout << "You entered: " << number << std::endl;
    return 0;
}
```

In this example, we prompt the user for input using `cout` and read their response into the `number` variable with `cin`.

### Writing complex/custom types to `cout`

Standard datatypes like `int`, `double`, `std::string` and similar can be printed by `cout`. 
However, more complex types like `std::vector` and your own classes cannot be represented by default. 
To make these work with std::cout, you can:

1. Create a function that converts the type in question to a string.
2. Overload operator `<<`.

##### Example
```cpp
#include <iostream>
#include <ostream>
#include <string>

struct Vector3 {
    
  float x, y, z;
  
  std::string toString() {
      return "Vector3(x=" + std::to_string(x) + ", y=" + std::to_string(y) + ", z=" + std::to_string(z) + ")"; 
  }
  
  friend std::ostream& operator << (std::ostream& os, const Vector3& v) {
      os << "Vector3(x=" << v.x << ", y=" << v.y << ", z=" << v.z << ")"; 
      return os;
  }
};

std::string toString(const Vector3& v) {
    return "Vector3(x=" + std::to_string(v.x) + ", y=" + std::to_string(v.y) + ", z=" + std::to_string(v.z) + ")"; 
}

int main()
{
    Vector3 v;
    
    std::cout << toString(v) << std::endl;     // free function
    std::cout << v.toString() << std::endl;    // member function
    std::cout << v << std::endl;               // overloading operator <<

    // Prints:
    // Vector3(x=0.000000, y=0.000000, z=0.000000)
    // Vector3(x=0.000000, y=0.000000, z=0.000000)
    // Vector3(x=0, y=0, z=0)

    return 0;
}
```

## File Streams

File streams in C++ allow you to perform I/O operations on files. They provide a way to read data from files (input file streams) or write data to files (output file streams). 
C++ offers two primary classes for file I/O:

- **`ifstream`**: This class represents an input file stream and is used for reading data from files.
- **`ofstream`**: This class represents an output file stream and is used for writing data to files.

To work with file streams, you need to include the `<fstream>` header.

Here's an example of using `ifstream` to read data from a file:

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ifstream inputFile("example.txt");
    if (inputFile.is_open()) {
        std::string line;
        while (std::getline(inputFile, line)) {
            std::cout << line << std::endl;
        }
        inputFile.close(); // Would also have been called implicitly due to RAII
    } else {
        std::cerr << "Unable to open file." << std::endl;
    }
    return 0;
}
```

In this example, we open a file named "example.txt" for reading using `ifstream`. 
We then check if the file is open and proceed to read and display its contents line by line.

Similarly, you can use `ofstream` to write data to a file. Just replace `ifstream` with `ofstream` and use the `<<` operator to write data to the file.

C++ provides various methods for manipulating files, including reading and writing binary data. When working with files, 
always ensure proper error handling to deal with potential issues like file not found or permission errors.
