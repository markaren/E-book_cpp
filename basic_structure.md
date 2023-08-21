# Basic Structure of a C++ Program

Brief description of the structure of a C++ program.

## Preprocessor Directives

Preprocessor directives are instructions to the compiler before actual compilation.
Common directive: `#include` to include header files for library functions.
Example: 
```cpp
#include <iostream>  // to include the input-output stream library.
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

## main() function

Every C++ program must have a `main()` function. It serves as the entry point for execution.
Program execution starts from the first statement in the `main()` function.
```cpp
int main() { /* code here */ return 0; }
```

## Code Blocks:

Sections of code enclosed in curly braces `{}` are called code blocks.
Blocks help organize and group statements together.

Code blocks in C++ also define the scope of variables.

### Scope and Code Blocks

A scope is a region of code where a variable or other named entity can be accessed and manipulated. 
In C++, code blocks, which are enclosed within curly braces {}, play a significant role in defining the scope of variables and other declarations. Here's how it works:

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

## Semicolons

Semicolons indicate the end of a statement in C++.
Missing semicolons can lead to syntax errors.
```cpp
std::cout << "Hello, World!";
```
