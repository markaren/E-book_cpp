
# Control statements

Control statements are essential tools in programming that enable you to control the flow of execution within your code. 
They allow you to make decisions, repeat actions, and create logical structures in your programs. 
In C++, there are three main types of control statements: 
[conditional statements](#Conditional-statements), [loop statements](#Loop-statements), and [branching statements](#Branching-statements).

## Conditional statements

Conditional statements in C++ are tools that allow your programs to make decisions and 
execute different blocks of code based on certain conditions. 
They let your program choose between alternative paths, enabling you to create dynamic and responsive applications. 
Here's a concise summary of the main conditional statements you'll encounter in C++:

### `if` statement

The `if` statement is used to execute a block of code if a specified condition is true. It's the simplest form of decision-making in C++.

```cpp
if (condition) {
    // Code to be executed if condition is true
}
```

### `if-else` statement

The `if-else` statement adds an alternative block of code to be executed when the condition is false.

```cpp
if (condition) {
    // Code to be executed if condition is true
} else {
    // Code to be executed if condition is false
}
```

The shorthand if-else statement in C++ is known as the ternary operator (`?:`). 
It provides a compact way to write a simple conditional expression in a single line. The syntax is:

```
condition ? expression_if_true : expression_if_false;
```

For example:

```cpp
int num = 10;
std::string result = (num > 5) ? "Greater than 5" : "Not greater than 5";
```

In this example, if num is greater than 5, the result will be set to "Greater than 5"; otherwise, 
it will be set to "Not greater than 5".


### `else-if` statement

The `else-if` statement allows you to check multiple conditions sequentially. 
It's useful when you have more than two possible outcomes.

```cpp
if (condition1) {
    // Code to be executed if condition1 is true
} else if (condition2) {
    // Code to be executed if condition2 is true
} else {
    // Code to be executed if none of the conditions are true
}
```

### `switch` statement

The `switch` statement is used for multiway branching. It's often used when you have a specific value to compare against.

```cpp
switch (variable) {
    case value1:
        // Code to be executed if variable == value1
        break;
    case value2:
        // Code to be executed if variable == value2
        break;
    // ... more cases ...
    default:
        // Code to be executed if none of the cases match
}
```

In C++, when working with the switch statement, it's a good practice to use braces `{}` 
to define the scope of each case's code block. 
This helps prevent unintended behavior and makes your code more robust. 
Let's modify the switch example to demonstrate the importance of using braces:

```cpp
switch (variable) {
    case value1: {
          // Code to be executed if variable == value1
          break;
    }
    case value2: {
          // Code to be executed if variable == value2
          break;
    }
    // ... more cases ...
    default: {
          // Code to be executed if none of the cases match
          break;
    }
}
```

This allows you to declare a variable with the same name in each of the blocks. 

### Summary

- Conditional statements enable your program to respond to changing conditions and make decisions.
- `if`, `if else`, and `else if` statements allow you to control program flow based on whether conditions are true or false.
- The switch statement provides a way to compare a variable against multiple possible values and execute code accordingly.
- Be mindful of using curly braces `{}` to define the scope of code blocks associated with conditional statements.
- Proper indentation and clear formatting make your code more readable and easier to understand.

Understanding and using conditional statements effectively is crucial for building flexible and interactive programs. 
As you practice, you'll become more adept at creating logical and responsive code that can handle various scenarios.

## Loop statements

Loop statements in C++ provide you with the power to execute a block of code repeatedly, making your programs more efficient and capable of automating tasks. 
Here's a concise summary of the main loop statements you'll encounter in C++:

### `while` loop

The `while` loop repeats a block of code as long as a specified condition remains true. 
It's ideal for situations where you want to repeat an action while a condition is met.

```cpp
while (condition) {
    // Code to be repeated
}
```
### `do-while` loop

The `do-while` loop is similar to the while loop, but it ensures that the code block is executed at least once before checking the condition. 
It's useful when you want to ensure something happens before checking if it should continue happening.

```cpp
do {
    // Code to be repeated
} while (condition);
```

### `for` loop

The for loop provides a structured way to repeat code a specific number of times or over a range of values. 
It's commonly used when you know the exact number of iterations needed.

```cpp
for (initialization; condition; update) {
    // Code to repeat
}
```

- __Initialization:__ This is where you set up your loop, usually by initializing a counter variable.
- __Condition:__ The loop continues as long as this condition is true.
- __Update:__ After each iteration, the update statement is executed, usually incrementing or decrementing the counter.
  
#### Example: Printing numbers from 1 to 5 using a for loop.

```cpp
for (int i = 1; i <= 5; i++) {
    std::cout << i << " ";
}
```

### `for-each` (Range-based for) loop:

The `for-each` loop, also known as the range-based for loop, is used to iterate through each element in a collection, such as an array or a container. 
It simplifies the process of accessing elements and is great for traversing sequences.

```cpp
for (data_type element : collection) {
    // Code to be executed for each element
}
```

#### Example: Printing the values of a `std::vector` container:

```cpp
std::vector<int> v{1, 2, 3};
for (int value : v) {
    std::cout << value << " ";
}
```

### Summary

- Loop statements help you automate repetitive tasks, iterate through data, and execute code multiple times.
- Use the while loop for situations where you need to repeat code based on a condition.
- The do-while loop guarantees the code block runs at least once before checking the condition.
- The for loop offers a structured way to repeat code with clear initialization, condition, and update steps.
- The "for each" loop simplifies iterating through collections by directly accessing each element.
- Be cautious of infinite loops – make sure the loop condition can eventually become false.

## Branching statements

Branching statements in C++ provide you with the ability to control the flow of your program by making decisions and altering the sequence of code execution. 
These statements enable your program to respond dynamically to different situations. Here's a concise summary of the main branching statements you'll encounter in C++:

### `break` statement

The `break` statement is used to exit from a loop or switch statement prematurely. It allows you to immediately terminate the current loop iteration or switch case and continue executing the code after the loop or switch.

```cpp
while (condition) {
    // Code
    if (some_condition) {
        break;  // Exit the loop
    }
    // More code
}
```

### `continue` statement

The `continue` statement is used to skip the rest of the current iteration of a loop and proceed to the next iteration.
It's often used to avoid executing certain code within an iteration.

```cpp
for (int i = 0; i < 5; ++i) {
    if (i == 2) {
        continue;  // Skip iteration when i is 2
    }
    // Code to execute for each iteration
}
```

### `return` statement

The `return` statement is used to exit a function and optionally return a value to the calling code. It immediately stops the function's execution and returns control to the calling context.

```cpp
int square(int x) {
    return x * x;  // Return the square of x
}
```

### Summary

- Branching statements enable your program to change its behavior based on conditions or to exit from a certain block of code.
- The break statement is used to exit loops or switch statements prematurely.
- The continue statement skips the remaining code in the current loop iteration and moves to the next iteration.
- The return statement exits a function and can return a value to the calling code.
