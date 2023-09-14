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

## File Streams

File streams in C++ allow you to perform I/O operations on files. They provide a way to read data from files (input file streams) or write data to files (output file streams). C++ offers two primary classes for file I/O:

- **`ifstream`**: This class represents an input file stream and is used for reading data from files.
- **`ofstream`**: This class represents an output file stream and is used for writing data to files.

To work with file streams, you need to include the <fstream> header.

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
        inputFile.close();
    } else {
        std::cout << "Unable to open file." << std::endl;
    }
    return 0;
}
```

In this example, we open a file named "example.txt" for reading using ifstream. We then check if the file is open and proceed to read and display its contents line by line.

Similarly, you can use `ofstream` to write data to a file. Just replace `ifstream` with `ofstream` and use the `<<` operator to write data to the file.

C++ provides various methods for manipulating files, including reading and writing binary data. When working with files, 
always ensure proper error handling to deal with potential issues like file not found or permission errors.
