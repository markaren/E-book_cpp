# Introducing Classes in C++

Classes are a fundamental concept in C++ and form the basis of 
object-oriented programming (OOP). They allow you to define custom data 
types that represent real-world objects or concepts in your program.

## What is a Class?

A class in C++ serves as a blueprint or template for creating objects. 
It defines the properties (data members) and behaviors (member functions or methods) 
that objects of that class will have. Essentially, a class helps you model
real-world entities or concepts in your program.

## Class Declaration

To declare a class, you use the `class` keyword followed by the class name. 
Here's a simple example of a class declaration for a "Car":

```cpp
class Car {
    
public:
    // Data members (properties)
    std::string brand;
    std::string model;
    int year;

    // Member functions (methods)
    void startEngine();
    void stopEngine();
    void accelerate();
    void brake();
}; // <--- NOTE the ;
```

In this example: 

- `Car` is the class name
- `brand`, `model`, and `year` are data members representing the car`s properties.
- `startEngine`, `stopEngine`, `accelerate`, and `brake` are member functions 
representing the car's behaviour.
- In this example, the header only provides the declaration. 
The actual implementation code (what happens when the functions are called) 
would be defined in a separate source file (.cpp). This is known as splitting the header.

## Creating objects

Once you've defined a class, you can create objects (instances) of that class. 
Objects are actual instances of the class that can hold data and perform actions. 
Here's how you create a `Car` object:

```cpp
Car myCar; // Creating a Car object named "myCar"
```

## Accessing members

You can access the data members (fields) and member functions of an object 
using the dot (`.`) operator:

```cpp
Car myCar;
myCar.brand = "Toyota";
myCar.model = "Camry";
myCar.year = 2020;

myCar.startEngine();
myCar.accelerate();
```

In the above, the fields and functions are accessible outside the class 
as they are declared under a `public` access specifier. Typically, we would employ [encapsulation](#encapsulation) 
and disallow access to internal data fields as well as initializing key data fields directly using a [constructor](#constructor).

## Member Functions

Member functions are used to define the actions that objects of the class can perform. 
They are defined inside the class and may be implemented outside the class. 
For example:

```cpp
void Car::startEngine() { 
    cout << "Engine started." << endl;
}

void Car::accelerate() {
    cout << "Car is accelerating." << endl;
}
```

> Note: [ClassName::] (i.e Car:: above) is only used when functions are implemented outside the class body.

## Constructor

A constructor is a special member function that is called when an object is created. 
It initializes the object's data members. 
Here's an example of a constructor for the `Car` class:

```cpp
Car::Car(std::string brand, std::string model, int year) {
    this->brand = brand;
    this->model = model;
    this->year = year;
}
```

The above is allowed and is similar to how member attributes in other languages are set. However, you __ought__ to be using [member initializer lists](https://en.cppreference.com/w/cpp/language/constructor):

```cpp
Car::Car(std::string brand, std::string model, int year)
    : brand(brand), 
      model(model), 
      year(year) {}
```

## Using Constructors

You can use constructors to initialize objects when they are created:

```cpp
Car myCar("Ford", "Mustang", 2022);
```

The type and number of parameters provided as input to the constructor must match. 
A class can have multiple constructors. In the example above, 
if `Car(std::string brand, std::string model, int year)` is the only constructor defined, 
you are not allowed to do:

```cpp
Car myCar1;                          // compile error - no matching constructor
Car myCar2("Ford", "Mustang");       // compile error - still no matching constructor
Car myCar3("Ford", "Mustang", 2022); // valid code
```

## Encapsulation
Encapsulation is a key principle of OOP, and it involves bundling data and methods that operate on that data into a single unit (the class). 
In C++, you can control access to the data members using access specifiers like `public`, `private`, and `protected`.

- `public`: Members declared as public are accessible from outside the class.
- `private`: Members declared as private are only accessible from within the class.
- `protected`: Members declared as protected are accessible from within the class and derived classes (inheritance).

Encapsulation is like putting your data and the code that works with that data into a box and allowing controlled access to the box. 
This helps in hiding the internal details of how a class works and provides a well-defined interface for interacting with it.

### Why Encapsulation?
- __Data Protection:__ Encapsulation helps protect data from unauthorized access or modification. By defining data members as private or protected, you can control who or what can change the internal state of an object.

- __Abstraction:__ It allows you to provide a simplified view of an object to the outside world. Users of a class don't need to know the intricate details of how it works internally; they only need to interact with its public interface.

- __Code Organization:__ Encapsulation promotes clean and organized code. Data and related functions are grouped together within a class, making the codebase more maintainable.

Here's an example demonstrating encapsulation in C++:

```cpp
class BankAccount {
    
private:
    double balance_;            // Private data member

public:
    // Constructor
    BankAccount(double initialBalance)
        : balance_(initialBalance){}

    // Public member functions
    void deposit(double amount) {
        if (amount > 0) {
            balance_ += amount;
        }
    }

    void withdraw(double amount) {
        if (amount > 0 && balance_ >= amount) {
            balance_ -= amount;
        }
    }

    double getBalance() {
        return balance_;
    }
};
```

The private data is encapsulated within the class, and external code can interact with the object only through the public functions, 
ensuring controlled and safe access to the data.

By following the principles of encapsulation, you can build robust and maintainable code while protecting your data from unintended modifications. 
It's a foundational concept in OOP and is widely used in programming to create organized and secure software systems.
---
Note the added trailing `_` to the private attributes in the example above. 
It is common to add _some_ special decoration to class member attributes in C++ in order to avoid variable shadowing. 
That is, to distinguish between local variables and class attributes. Example:

```cpp
class Car {
    
private:
    string model;

public:
    void setModel(std::string model) {
        model = model; // what happens here? Answer: We assign the input parameter to itself. NOT what we intended.
        // this->model = model; // (1) We fix it by using the special `this` pointer.
        // model_ = model;      // (2) Better. We solve the issue by decorating the field.
    }
};
```