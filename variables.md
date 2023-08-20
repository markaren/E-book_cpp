# Variables and Basic Types

In C++, variables are essential components that allow you to store and manipulate data. 
They act like containers for holding different types of information, such as numbers, text, or even complex structures. 
Understanding variables is fundamental for writing effective and dynamic programs.

## What is a Variable?

Imagine a box where you can put something and give it a name. In programming, a variable is like that box. It's a named storage location in your computer's memory that holds a value. This value can be a number, a piece of text, or something more complex.

### Declaring a Variable:

To use a variable, you need to declare it first. This means giving it a name and specifying its type (what kind of data it will hold). For example:

```cpp
int age;  // Declare an integer variable named 'age'
double price;  // Declare a double (floating-point) variable named 'price'
```

### Assigning a Value:

After declaring a variable, you can assign a value to it using the assignment operator =. The value you assign must match the variable's type:

```cpp
age = 25;  // Assign the value 25 to the 'age' variable
price = 19.99;  // Assign the value 19.99 to the 'price' variable
```

### Initializing a Variable:

You can also declare and assign a value in a single step, known as initialization:

```cpp
int quantity = 10;  // Declare and initialize the 'quantity' variable with the value 10 using direct initialization with assignment.
double sum{5.0};   // Declare and initialize the 'sum' variable with the value 5.0 using uniform initialization.
```

Initializing variables when you declare them is a good programming practice with several benefits. Let's explore why you should make it a habit to initialize variables right from the start:

1. __Prevents Unintended Values:__
When you declare a without initializing it, it contains whatever was previously stored in that memory location.
This could be garbage values, remnants of previous computations, or unpredictable data.
Initializing variables ensures that they start with a known, meaningful value.
3. __Avoids Bugs and Errors:__
Using variables without initializing them can lead to bugs that are difficult to identify and fix.
Unexpected behavior can occur when uninitialized variables interact with other parts of your code.
Initializing variables from the beginning reduces the chances of introducing subtle errors.
5. __Enhances Readability and Intent:__
When you initialize variables at the point of declaration, you make your code more self-explanatory.
Anyone reading your code can immediately understand the initial value and the intended purpose of the variable.
This improves code readability and aids collaboration.
7. __Promotes Good Habits:__
Initializing variables encourages good coding habits. It forces you to think about the initial state and value that your variable should have.
This practice can extend to more complex scenarios where initializing variables becomes essential for proper program behavior.
9. __Makes Debugging Easier:__
If you encounter unexpected behavior in your program, initialized variables help narrow down the scope of the issue.
You can rule out uninitialized variables as a potential cause of bugs, saving time during debugging.
11. __Prevents Undefined Behavior:__
In C++, using uninitialized variables can lead to undefined behavior.
The C++ standard doesn't define the behavior of your program when you read from an uninitialized variable.
This means your program might work differently on different compilers or platforms.

#### Example

```cpp
int main() {
    int age;      // Not initialized
    int salary = 0; // Initialized

    // Using uninitialized variable 'age'
    int doubleAge = age * 2; // Undefined behavior

    // Using initialized variable 'salary'
    int doubleSalary = salary * 2; // Safe and predictable

    return 0;
}
```

### Using Variables:

Once you've declared and assigned a value to a variable, you can use it in your code. For example:

```cpp
int quantity = 3;
//...
int total = quantity * 2;  // Use the 'quantity' variable in an expression
```

### Variable Names:

Variable names can consist of letters, digits, and underscores. They must start with a letter or an underscore. 
Names are case-sensitive (e.g., `age` and `Age` are different variables).

### Scope:

Scope defines the area of your code where a variable is visible and can be accessed. 
Each pair of curly braces `{}` marks a new scope. Variables declared within a scope are usually only accessible within that scope.

#### Local Scope:

Variables declared inside a function are local to that function's scope. 
They can't be accessed from outside the function. This is great for keeping variables separate and preventing unintended interference.

```cpp
void printMessage() {
    std::string message = "Hello!"; // Local variable within the function
    std::cout << message << std::endl;
} // 'message' goes out of scope here and is no longer accessible
```

#### Global Scope:

Variables declared outside any function, at the top of your code, have global scope. 
They can be accessed from anywhere in your program. However, it's recommended to limit global variables as they can make code harder to understand and maintain.

```cpp
#include <iostream>

int globalVariable = 100; // Global variable accessible everywhere

void demoScopes() {
    int localVariable = 50; // Local variable only accessible within this function

    std::cout << "Global variable: " << globalVariable << std::endl;
    std::cout << "Local variable: " << localVariable << std::endl;
}

int main() {
    demoScopes();
    // Uncommenting the next line will cause an error:
    // std::cout << "Local variable: " << localVariable << std::endl;

    return 0;
}
```

## Data Types:

Variables have data types that define the kind of value they can hold. Common data types include:

|Type|Comment|
|----|-------|
| char | Single characters |
| bool | Boolean values (true or false) |
| int | Integers (whole numbers) |
| double | Floating-point numbers (decimal numbers) |
| std::string | Sequences of characters (text) |


Using the `class` or `struct` keyword in C++ you can defines your own custom types.


## Summary

In a nutshell, variables in C++ are like named storage boxes for holding different types of information. 
Variables store data, and scope determines where that data is accessible. 
By understanding how to declare, initialize, and use variables in various scopes, you'll be able to build dynamic and organized programs. 
Keeping variables in appropriate scopes contributes to code clarity, prevents conflicts, and sets the foundation for creating reliable software.
