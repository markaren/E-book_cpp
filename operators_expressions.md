# Operators and Expressions in C++

Operators are symbols that perform operations on one or more operands. 
Operands can be variables, constants, or other expressions. 
Expressions are combinations of operators and operands that produce a value.

## Types of Operators:

1. __Arithmetic Operators:__
Perform basic mathematical operations. <br>
Examples: `+ (addition), - (subtraction), * (multiplication), / (division), % (modulus).`

2.  __Assignment Operators:__
Assign a value to a variable. <br>
Examples: `= (assignment), += (add and assign), -= (subtract and assign), *= (multiply and assign), /= (divide and assign).`

3.  __Comparison Operators:__
Compare two values and return a Boolean result (true or false). <br>
Examples: `== (equal to), != (not equal to), < (less than), > (greater than), <= (less than or equal to), >= (greater than or equal to).`

4.  __Logical Operators:__
Perform logical operations on Boolean values.
Examples: `&& (logical AND), || (logical OR), ! (logical NOT).`

5.  __Increment and Decrement Operators:__
Increase or decrease the value of a variable by 1. <br>
Examples: `++ (increment), -- (decrement).`

6.  __Conditional (Ternary) Operator:__
A shorthand way of writing if-else statements.
Syntax: condition ? expression1 : expression2
Example: `result = (x > y) ? x : y;`

7.  __Bitwise Operators:__
Perform operations on individual bits of values. <br>
Examples: `& (bitwise AND), | (bitwise OR), ^ (bitwise XOR), ~ (bitwise NOT), << (left shift), >> (right shift).`

## Expressions

Expressions are combinations of operators and operands that produce a value. 
They can be as simple as a single variable or complex combinations of operators and functions. 
Expressions are used in assignments, comparisons, calculations, and more.

#### Example: Arithmetic Expression

```cpp
int x = 10;
int y = 5;
int sum = x + y; // An arithmetic expression
```

#### Example: Comparison Expression

```cpp
bool result = x > y; // A comparison expression
```

#### Example: Conditional Expression

```cpp
int max = (x > y) ? x : y; // A conditional expression
```

## Using Operators and Expressions:

Operators and expressions are fundamental to programming. They allow you to manipulate data, make decisions, and perform calculations. 
By combining operators and operands creatively, you can create complex logic and functionality in your programs. 
Just remember to follow operator precedence and use parentheses when necessary to ensure the desired order of operations.
