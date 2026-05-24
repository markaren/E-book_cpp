# Terms

Whether you are new to programming or just to C++, you will meet a lot of unfamiliar words. This page gives a short, plain definition of the ones used in this book, with a pointer to where each is explained in full. It is alphabetical — use the search box at the top to jump straight to a term.

| Term | Meaning |
|------|---------|
| **abstract class** | A class with at least one pure virtual function (`= 0`); it cannot be created directly, only inherited from. See [Polymorphism](Chapter5/polymorphism.md). |
| **argument** | A value you pass to a function when you call it. Inside the function it arrives as a *parameter*. See [Functions](Chapter1/functions.md). |
| **assertion** (`assert`) | A check for a condition that must always be true; if it is false the program aborts. A tool for catching bugs, removed in release builds. See [Error Handling](Chapter6/error_handling.md). |
| **assignment** | Replacing a variable's current value with a new one, e.g. `x = 5`. See [Operators](Chapter1/operators_expressions.md). |
| **base case** | The case in a recursive function that can be answered directly, without recursing — it is what stops the recursion. See [Recursion](recursion.md). |
| **block** | A group of statements wrapped in curly braces `{ }`. A block defines a *scope*. See [Basic Structure](Chapter1/basic_structure.md). |
| **breakpoint** | A marker that pauses a running program in the debugger so you can inspect it. See [Using a Debugger](debugger.md). |
| **built-in type** | A type the language provides directly: `int`, `double`, `bool`, `char`. See [Variables](Chapter1/variables.md). |
| **capture** | The `[ ]` part of a lambda that lists which surrounding variables it may use, by value or by reference. See [Lambda Expressions](lambdas.md). |
| **cast** | An explicit type conversion, e.g. `static_cast<int>(x)`. See [Operators](Chapter1/operators_expressions.md). |
| **class** | A user-defined type that bundles data together with the operations that work on it. See [Classes](Chapter4/classes.md). |
| **cohesion** | How strongly the parts of one piece of code belong together — how focused it is on a single job. High cohesion (one clear responsibility) is the goal. See [Separation of Concerns](Chapter6/soc.md). |
| **compiler / compile** | The tool that translates your source code into a runnable program, *before* it runs. See [Introduction](Chapter1/introduction.md). |
| **const** | A promise to the compiler that a value will not change; the compiler enforces it. See [Variables](Chapter1/variables.md). |
| **const-correctness** | The discipline of marking everything that does not change as `const` — member functions that only observe, reference parameters you only read, locals you never reassign — so the compiler enforces what may be modified. A `const` object can call only `const` member functions. See [Classes](Chapter4/classes.md) and [Values, References & Pointers](Chapter4/types_refs_ptrs.md). |
| **constructor** | A special member function that runs when an object is created, to set up its initial state. See [Classes](Chapter4/classes.md). |
| **container** | A standard-library type that holds a collection of values, such as `std::vector`, `std::map`, or `std::set`. See [Data Structures](Chapter3/data_structures.md). |
| **coupling** | How much one piece of code depends on the details of another. Loose (low) coupling — pieces connected only through narrow interfaces — is the goal. See [Separation of Concerns](Chapter6/soc.md). |
| **dangling reference / pointer** | A reference or pointer to something that has already been destroyed; using it is undefined behaviour and a common cause of crashes. See [Values, References & Pointers](Chapter4/types_refs_ptrs.md). |
| **encapsulation** | Hiding a type's inner workings behind a clean interface by making its data `private`. See [Classes](Chapter4/classes.md). |
| **enum class** | A type with a fixed set of named values (a *scoped enumeration*); the modern, type-safe kind of enum. See [Enumerations](Chapter1/enums.md). |
| **exception** | A way to signal and handle errors, using `throw`, `try`, and `catch`. See [Error Handling](Chapter6/error_handling.md). |
| **expression** | Anything that evaluates to a value — a literal, a variable, a function call, or these joined by operators (`i + j`). See [Operators](Chapter1/operators_expressions.md). |
| **function** | A named, reusable piece of code that performs one task. See [Functions](Chapter1/functions.md). |
| **global variable** | A variable declared outside every function, visible everywhere. Shared, mutable globals make code hard to follow and test; prefer locals, parameters, and return values, and keep lasting state inside an object. Global *constants* are fine. See [Functions](Chapter1/functions.md#global-variables). |
| **header** | A file (usually `.hpp`) whose declarations are shared across source files via `#include`. See [Classes](Chapter4/classes.md). |
| **IDE** | Integrated Development Environment — the application you write, build, run, and debug code in. This course uses CLion. See [Getting Started](getting_started.md). |
| **inheritance** | Building a new class on top of an existing one (`class Dog : public Animal`). See [Polymorphism](Chapter5/polymorphism.md). |
| **initialise** | Give a variable a value at the moment it is created. Always do this. See [Variables](Chapter1/variables.md). |
| **iterator** | An object used to walk through the elements of a container. See [C++ Standard Library](Chapter3/standard_library.md). |
| **lambda** | A small, unnamed function written inline, often passed to an algorithm. See [Lambda Expressions](lambdas.md). |
| **linker / linking** | The build stage that combines the compiled pieces and libraries into the final program. "Undefined reference" is a linker error. See [Reading Compiler Errors](compiler_errors.md). |
| **Liskov Substitution Principle** | The design rule that a derived class must be usable anywhere its base type is, without surprising code that relies on the base — an *honest* is-a. See [Polymorphism](Chapter5/polymorphism.md). |
| **LLM / AI assistant** | A large language model (ChatGPT, Claude, …) that can generate code — useful, but confidently wrong often enough that you must check it. See [Using AI for Coding](using_ai.md). |
| **main** | The function the operating system calls to start your program. Each program has exactly one. See [Basic Structure](Chapter1/basic_structure.md). |
| **member function** (method) | An operation defined inside a class and called on an object. "Method" is a synonym. See [Classes](Chapter4/classes.md). |
| **member initialiser list** | The `: a(x), b(y)` part of a constructor that gives data members their values before the body runs. See [Classes](Chapter4/classes.md). |
| **move** | Transferring a resource from one object into another instead of copying it. See [Move Semantics](Chapter5/move.md). |
| **namespace** | A named region that groups names to avoid clashes. The standard library lives in the namespace `std`. See [C++ Standard Library](Chapter3/standard_library.md). |
| **NaN** | "Not a Number" — a floating-point result of invalid maths (e.g. `0.0 / 0.0`). It compares as *false* against everything, even itself. See [Floating-Point Pitfalls](floating_point.md). |
| **operator** | A symbol such as `+`, `==`, or `&&` that performs an action within an expression. See [Operators](Chapter1/operators_expressions.md). |
| **overloading** | Defining several functions with the same name but different parameter types; the compiler picks the right one. See [Functions](Chapter1/functions.md). |
| **parameter** | A named input in a function's definition. The value supplied at the call site is the *argument*. See [Functions](Chapter1/functions.md). |
| **PATH** | The list of folders the shell searches to find a program you run by name. A "command not found" is often a PATH problem. See [Computer Basics](computer_basics.md). |
| **pointer** | A variable that holds a memory address. It can be `nullptr` (pointing at nothing) and must be checked before use. See [Values, References & Pointers](Chapter4/types_refs_ptrs.md). |
| **polymorphism** | Treating different derived types through a common base interface, so the same call runs the right type's code. See [Polymorphism](Chapter5/polymorphism.md). |
| **predicate** | A function (often a lambda) that returns `true` or `false`, used by algorithms like `find_if`. See [Lambda Expressions](lambdas.md). |
| **RAII** | "Resource Acquisition Is Initialisation" — tie a resource to an object so it is released automatically when the object goes out of scope. See [RAII](Chapter4/raii.md). |
| **recursion** | A function that calls itself to solve a smaller version of the same problem, stopping at a *base case*. See [Recursion](recursion.md). |
| **reference** | An alias for an existing variable; it can never be null and never refers to anything else once set. See [Values, References & Pointers](Chapter4/types_refs_ptrs.md). |
| **Rule of Zero** | Design classes whose members manage themselves (containers, smart pointers) so you need write no special member functions. See [Classes](Chapter4/classes.md). |
| **scope** | The region of code in which a name is valid. A variable declared in a block disappears when the block ends. See [Basic Structure](Chapter1/basic_structure.md). |
| **shell** | The program (PowerShell, bash, zsh, cmd) that interprets the commands you type in a terminal. See [Computer Basics](computer_basics.md). |
| **smart pointer** | An RAII wrapper that owns heap memory and frees it automatically — `std::unique_ptr`, `std::shared_ptr`. See [Memory Management](Chapter5/memory.md). |
| **stack overflow** | A crash caused by using up the call stack, for example a recursion with no reachable base case. See [Recursion](recursion.md). |
| **standard library** | The large set of types and functions that ships with C++, all in the `std` namespace. (Its containers and algorithms part is informally called the *STL*.) See [C++ Standard Library](Chapter3/standard_library.md). |
| **statement** | One instruction; in C++ it ends with a semicolon. See [Basic Structure](Chapter1/basic_structure.md). |
| **std** | The namespace of the standard library. `std::cout` means "`cout`, from `std`." See [C++ Standard Library](Chapter3/standard_library.md). |
| **template** | A blueprint that generates functions or classes for whatever type you use, like `std::vector<T>`. See [Templates](Chapter5/templates.md). |
| **terminal** | A text window where you control the computer by typing commands instead of clicking. See [Computer Basics](computer_basics.md). |
| **undefined behaviour** | Code the language makes no promises about: it may crash, print garbage, or seem to work and break later. Avoid it. See [Variables](Chapter1/variables.md). |
| **uninitialised variable** | A variable created without a value. Reading one is undefined behaviour and a rich source of bugs — always initialise. See [Variables](Chapter1/variables.md). |
| **variable** | A named piece of memory that holds a value of a fixed type. See [Variables](Chapter1/variables.md). |
| **vector** | The standard library's resizable array, `std::vector`. The list type you reach for by default. See [C++ Standard Library](Chapter3/standard_library.md). |
| **virtual function** | A member function a derived class can override; a call through a base reference or pointer runs the actual object's version. See [Polymorphism](Chapter5/polymorphism.md). |
