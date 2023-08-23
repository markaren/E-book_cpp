# Basic Structure of a C++ Program

Brief description of the structure of a C++ program.

## Preprocessor Directives

Preprocessor directives are instructions to the compiler before actual compilation.
Common directive: `#include` to include header files for library functions.
Example: 
```cpp
#include <iostream>  // to include the input-output stream library.
```

### Header guards

All headers you write should contain a _header guard_.
Header guards are a programming technique used to prevent the multiple inclusion of the same header file (.h/.hpp) throughout your project.
When you `#include` a header file in multiple places within your codebase, it can lead to problems like duplicate declarations, redefinitions, and compilation errors. 
Header guards are a way to mitigate these issues and look like this:

##### header.hpp
```cpp
#ifndef HEADER_FILENAME_H
#define HEADER_FILENAME_H

// Content of the header file goes here

#endif
```

 Note that the `HEADER_FILENAME_H` above needs to be unique for every file.

#### Alternative: `#pragma once`
 An alternative to the above is to use the non-stanard `#pragma once` directive, which is supported by all major compilers.

##### header.hpp
 ```cpp
#pragma once

// Content of the header file goes here
```

## Comments

Comments are non-executable lines used for documentation and explanations.
Single-line comments start with two forward slashes (`//`).

```cpp
// This is a comment
std::cout << "Hello World!";
```

```cpp
/* The code below will print the words Hello World!
to the screen, and it is amazing */
std::cout << "Hello World!";
```


## Semicolons

Semicolons indicate the end of a statement in C++.
Missing semicolons can lead to syntax errors.
```cpp
int quantity = 10;
double price = 5.40;
double sum = price * quantity;
std::cout << "Hello there" << std::endl;
```

They are also used to end class definitions.

```cpp
class MyClass {
// class definitions
};
```


## Code Blocks:

Sections of code enclosed in curly braces `{}` are called code blocks.
Blocks help organize and group statements together.

Code blocks in C++ also define the scope of variables.

### Scope and Code Blocks

A scope is a region of code where a variable or other named entity can be accessed and manipulated.
In C++, code blocks, which are enclosed within curly braces {}, play a significant role in defining the 
scope of variables and other declarations. Here's how it works:

1. __Local Scope:__ Variables declared inside a code block are said to have local scope.They can only be accessed and used within that specific code block.Once you move outside the code block, those variables are no longer accessible.
3. __Block Nesting:__ Code blocks can be nested within each other. Variables declared in an outer block are visible to inner blocks, but not vice versa. Inner blocks can "see" variables from outer blocks, but not the other way around.
4. __Shadowing:__ If an inner block declares a variable with the same name as one in an outer block, the inner variable "shadows" the outer one within the inner block's scope. This means that the inner variable takes precedence over the outer one for the duration of that inner block.

```cpp
#include <iostream>

int main() {
    int x = 5;  // x is declared in the main function's scope
    
    {
        int x = 10;  // A new x is declared in this inner code block's scope, which shadows the outer variable x.
        std::cout << "Inner x: " << x << std::endl;  // Outputs 10
    }
    
    std::cout << "Outer x: " << x << std::endl;  // Outputs 5
    
    return 0;
}
```

Understanding scope is crucial for avoiding naming conflicts and making sure that your variables are used where and when they are intended.
It's also a fundamental concept in programming languages, as it allows you to manage the visibility and accessibility of variables throughout your code.

## Statements

A statement in C++ is a complete instruction that performs a specific action.
Here are some common types of statements:

1. __Expression Statements:__
   An expression followed by a semicolon is an expression statement. <br>
   Example: `x = y + z;` or `result = 2 * (x + y);`


2. __Declaration Statements:__
   These declare variables or other entities. <br>
   Example: `int num;` or `double price = 10.99;`

4. __Control Flow Statements:__
   These control the flow of execution in your program. <br>
   Examples: if, else, switch, while, for, do-while. <br>

5. __Jump Statements:__
   These transfer control to a different part of the program. <br>
   Examples: break, continue, return, goto (though rarely used).

See also [Control Statements](control_statements.md)


## main() function

Every C++ program must have a `main()` function. It serves as the entry point for execution.
Program execution starts from the first statement in the `main()` function.
```cpp
int main() { 
    /* code here */ 
    return 0;
}
```

## Header and source files

C++ projects are often split into multiple files to keep things organized and manageable. The two main types of files you'll encounter are header files and source files.
You often pair a header file with a source file. The header file defines the interface of your code, while the source file provides the actual logic and details. 
However, in many cases the header could contain both the definition and implementation of your code. The choice is often yours wether or not you want to split the header or not. 
There are advantages and disadvatages with both alternatives.

You include the header file in your source file using the `#include` directive.

### Header Files:

Header files (usually with a .h or .hpp extension) are used to declare various elements, like classes, functions, and variables, without necessarily providing their implementations. 
These files act as blueprints that describe what something does and how it can be used. Header files contain function prototypes (declarations) and class definitions to be re-used in other files. 
They don't typically contain the actual code for those functions or classes.

Example of a header file named `my_class.h`:

```cpp
#ifndef MY_CLASS_H
#define MY_CLASS_H

class MyClass {
public:
    MyClass();          // Constructor declaration
    void doSomething(); // Method declaration
private:
    int someData;       // Data member declaration
};

#endif
```

### Source Files:

Source files (usually with a .cpp extension) contain the actual implementation of the code you declared in the header files. 
They include the details of how functions are defined, classes are built, and variables are used. Source files provide the "meat" of your program.

Example of a source file named `my_class.cpp` implementing the `MyClass` class:

 ```cpp
#include "my_class.h"

MyClass::MyClass(): someData(0) {} // initialize the value of someData to 0 using member initializer list

void MyClass::doSomething() {
    // Implementation of the method
}
```


#### Alternative approach to splitting header

As an alternative to the split above, we often can provide the header also with the implementation details:

```cpp
#ifndef MY_CLASS_H
#define MY_CLASS_H

class MyClass {
public:
    MyClass(): someData(0){}

    void doSomething() {
       // do something
    }
private:
    int someData; 
};

#endif
```

As you go along, you'll learn to make more informed decisions on which approach to go with.
