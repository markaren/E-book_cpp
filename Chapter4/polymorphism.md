# Polymorphism 

Polymorphism means many forms, and is one of the fundamental principles of Object-Oriented Programming (OOP).
It allows objects of different classes to be treated as objects of a common superclass. 
It promotes flexibility and reusability in code, enabling you to write more generic 
and extensible programs. 

In C++ we have two types of polymorphism:

1. Compile Time Polymorphism
2. Runtime Polymorphism

## Compile-time polymorphism
Compile-time polymorphism is done by overloading an operator or function. 

### Function overloading

Function overloading allows you to define multiple functions with the same name in the
same scope but with different parameters. 
The appropriate function is called based on the number and types of 
arguments passed during the function call.

```cpp
class Example {
public:
    void display(int num) {
        cout << "Integer: " << num << endl;
    }

    void display(double num) {
        cout << "Double: " << num << endl;
    }
};

int main() {
    Example obj;
    obj.display(5);     // Output: Integer: 5
    obj.display(3.14);  // Output: Double: 3.14
    return 0;
}
```

#### Operator Overloading

Operator overloading allows you to define how operators behave for user-defined data types. 
It enables you to redefine the behavior of operators like `+`, `-`, `*`, etc., 
for objects of a class. I.e., operators can behave differently depending on the type used with them.

```cpp
class Complex {
    
public:
    
    // constructor with default values
    Complex(int real = 0, complex = 0)
        : real_(real), complex_(complex){}
    
    // overloading operator + 
    Complex operator + (const Complex &obj) {
        Complex temp;
        temp.real = real + obj.real;
        temp.imag = imag + obj.imag;
        return temp;
    }
    
private:
    int real_, imag_;
};

int main() {
    Complex num1, num2; // Assume num1 and num2 are initialized with meaningful values
    Complex result = num1 + num2; // Operator + is overloaded for objects of Complex class
    return 0;
}

```

## Runtime polymorphism

Run-time polymorphism in C++ is achieved through virtual functions and inheritance.  

### Inheritance

Inheritance is a fundamental object-oriented programming concept that allows you to create a new class based on an existing class. The new class, known as the derived class, inherits properties and behaviors (data members and member functions) from the existing class, called the base class. This facilitates code reuse and the creation of a hierarchy of classes.

```cpp
class BaseClass {
    // members and methods of BaseClass
};

class DerivedClass : access-specifier BaseClass {
    // members and methods of DerivedClass
};
```

- `access-specifier` can be one of three: `public`, `protected`, or `private`. It specifies the access level for the members inherited from the base class.

##### Example

```cpp
class Animal {
public:
    void eat() {
        cout << "Animal is eating." << endl;
    }
};

class Dog : public Animal {
public:
    void bark() {
        cout << "Dog is barking." << endl;
    }
};
```

In this example, `Dog` is a derived class inheriting publicly from `Animal`. Now, objects of the `Dog` class can access the `eat()` method from the `Animal` class as well as its own `bark()` method.

```cpp
int main() {
    Dog myDog;
    myDog.eat();  // Output: Animal is eating.
    myDog.bark(); // Output: Dog is barking.
    return 0;
}
```

This way, inheritance allows for creating a hierarchy of classes, enabling the creation of more specialized classes based on existing ones, promoting code reuse and modularity.

### Virtual Functions
In C++, you use the `virtual`` keyword to declare a member function of the base class as virtual. 
Virtual functions are resolved at runtime, allowing the appropriate derived class function to be called based on the 
object's actual type rather than the declared type. Virtual functions can have a defualt implementation that gets inherited (and possibly overriden (replaced)) or be defined as pure virtual where some subclass __must__ provide an implementation.

```cpp
class Shape {
public:
    virtual void draw() = 0; //pure virtual
};

class Circle : public Shape {
public:
    void draw() override {
        cout << "Drawing a circle\n";
    }
};

class Square : public Shape {
public:
    void draw() override {
        cout << "Drawing a square\n";
    }
};

```

In this example, the `draw()` function is declared as `virtual` in the Shape class. 
When you have a pointer or reference of the base class type pointing to 
an object of a derived class, the correct `draw()` function is called based on the actual object type.

```cpp

int main() {
    std::unique_ptr<Shape> shape1 = std::make_unique<Circle>();
    std::unique_ptr<Shape> shape2 = std::make_unique<Square>();

    shape1->draw(); // Output: Drawing a circle
    shape2->draw(); // Output: Drawing a square

    return 0;
}

```

In this example, polymorphism allows the `draw()` function to behave differently based on the actual type of the object it's called on.

Polymorphism enables you to write more generic and flexible code, making it easier to extend and modify your programs without altering existing code. 
It's a powerful concept that enhances the maintainability and readability of object-oriented programs in C++.

#### Object slicing

Object slicing in C++ occurs when you assign an object of a derived class to an object of its base class type. In this situation, if the derived class object contains additional member variables or member functions that are not present in the base class, those extra parts of the object are "sliced off." 
This can lead to unexpected behavior and loss of data if you are not careful.

It's important to be aware of object slicing when dealing with inheritance 
and assignments between objects of base and derived classes. 
To avoid object slicing, you can use pointers or references to the base class 
when working with polymorphic behavior, as shown in the previous examples with virtual functions.
Pointers or references allow you to access the derived class's specific members without losing data due to object slicing.

---
### More complex example using runtime-polymorphism 

Imagine we have an application where we want to have some 
logging for debugging or informational purposes.

We could place some `std:cout` calls in our code, but that is not very flexible and would be alot of work to change later. 
What if we wanted to log to a file rather than to the terminal? Let us use inheritance!

We can define an abstract base class `Logger` that declares a (pure) virtual 
function `log(args` like so:

```cpp
class Logger {
public:
    virtual void log(const std::string& str) = 0;
};
```

As `Logger` defines a pure virtual function, it is an abstract type, 
meaning it is not a complete type that we can instantiate. 
We need some other class(es) to subclass it!

Let us create a `FileLogger` and a `ConsoleLogger` like so:

```cpp
class FileLogger: public Logger {

public:
    FileLogger(const std::filesystem::path& outFile)
        : out_(outFile) {}

    void log(const std::string& str) override {
        out_ << str << std::endl;
    }

private:
    std::ofstream out_;
};

class ConsoleLogger: public Logger {
    
public:
    
    void log(const std::string& str) {
        std::cout << str << std::endl;
    }
    
};
```

The `FileLogger` and `ConsoleLogger` both inherits from `Logger` 
and provides an implementation of the `log(...)` function.

Now we can write code that only knows about `Logger` and it's up to the user to
decide whether to log to file or console as shown here:

```cpp
class Simulation {

public:
    void stepSimulation(double dt) {
        // simulate something
        
        if (logger_) {
            logger_->log("Stepping simulation, t=" + std::to_string(t));
        }

        t += dt;
    }

    void setLogger(std::unique_ptr<Logger> logger) {
        logger_ = std::move(logger);
    }

private:
    double t = 0;
    // note that the type is the abstract Logger type
    std::unique_ptr<Logger> logger_;
};

int main() {

    Simulation sim;
    auto logger = std::make_unique<FileLogger>("logfile.txt");
    //        auto logger = std::make_unique<ConsoleLogger>(); // could use this one as well

    sim.setLogger(std::move(logger));

    sim.stepSimulation();
}
```

Now we can remove or add new `Logger` implementations without `Simulation` even knowing!
