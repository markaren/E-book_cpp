# CMake 

[CMake](https://cmake.org/) is a powerful tool in the world of C++ programming that simplifies the process of building, compiling, and managing complex projects. It helps you create cross-platform, organized, and easily maintainable codebases.

[CLion](https://www.jetbrains.com/clion/) is a powerfull and cross-platform C/C++ IDE that supports CMake projects, which we will use in this course. 
As an NTNU student, you are [eligible for a free license](https://www.jetbrains.com/community/education/#students).  


## What is CMake?

CMake is a widely used open-source build system and project configuration tool. It allows developers to define and manage the build process of their C++ projects in a platform-independent way. CMake generates platform-specific build files, such as Makefiles for Unix-like systems or project files for IDEs like Visual Studio.

### Key Concepts:

- __CMakeLists.txt:__ A CMakeLists.txt file is at the heart of every CMake project. It contains instructions for CMake to configure and generate build files. It specifies project details, source files, dependencies, compiler options, and more.
- __Cross-Platform:__ CMake enables you to write build configurations that work across different platforms, including Windows, macOS, and various Unix-like systems.
- __Generator:__ A generator is a tool that CMake uses to generate platform-specific build files. It can create Makefiles, Visual Studio project files, Xcode project files, and more.
- __Target:__ In CMake, a target represents an output artifact, such as an executable, library, or other build result. Targets can have properties, dependencies, and compile options.
- __Out-of-Source Build:__ CMake encourages an out-of-source build approach, where build files and generated artifacts are kept separate from the source code, reducing clutter and ensuring clean organization.

### Why Use CMake?

CMake offers several benefits for C++ projects:

- __Simplicity:__ CMake simplifies the process of configuring, building, and managing complex projects, abstracting away platform-specific details.
- __Cross-Platform:__ With CMake, you can generate build files that work seamlessly on different platforms without significant modifications.
- __Modularity:__ CMake promotes modular project organization, making it easier to manage larger codebases and libraries.
- __Dependencies:__ CMake simplifies the inclusion of external libraries and dependencies into your project.
- __IDE Integration:__ CMake integrates with various Integrated Development Environments (IDEs), allowing you to work within your preferred coding environment.

#### Going further:

- __Adding Libraries:__ Use `target_link_libraries` to link your executable with external libraries.
- __Multiple Source Files:__ Add all your source files to the `add_executable` line in the `CMakeLists.txt` file.
- __Organizing Code:__ Create subdirectories for different parts of your project and use `add_subdirectory` in your `CMakeLists.txt`.

## Organizing CMake projects

Organizing a CMake project effectively is crucial for maintaining a clean, structured, and manageable codebase. Here's a recommended organization structure for your CMake project:

- __Root Directory:__
The root directory of your project contains the main `CMakeLists.txt` file and any top-level project files. This directory often has a name that reflects your project's purpose.

```scss
MyProject/
├── CMakeLists.txt (Main CMake configuration)
├── README.md
├── LICENSE
├── .gitignore
├── build/ (auto-generated build directory)
├── include/ (Header files)
└── src/ (Source files)
```

Your main `CMakeLists.txt` file should be in the root directory. If you have subdirectories, create additional `CMakeLists.txt` files in those directories to configure the build for their specific contents.

- __Build Directory:__
Create a separate build directory (e.g., `build/`) to keep build-related files separate from the source code. This prevents cluttering your source directory with build artifacts.
- __Include Directory:__
Place header files (.h or .hpp) in the `include/` directory. Organize headers based on their functionality or modules. Use proper directory structure to prevent naming clashes and enhance code readability.
- __Source Directory:__
The `src/` directory is where your source code files (.cpp files) reside. Similar to headers, organize source files by functionality or modules to maintain clarity.
- __Subdirectories__:
Consider creating subdirectories within `include/` and `src/` as your project grows. This helps maintain a well-structured codebase. For example:

```
...
include/
├── math/
│   ├── arithmetic.h
│   └── geometry.h
└── utils/
    ├── string_utils.h
    └── file_utils.h
src/
├── CMakeLists.txt
├── math/
│   ├── arithmetic.cpp
│   └── geometry.cpp
└── utils/
    ├── string_utils.cpp
    └── file_utils.cpp
```

- __Testing:__
For testing purposes, create a separate directory like test/ or tests/ to hold your unit tests. This keeps test code separate from your source code.

- __Documentation:__
Consider having a docs/ directory to store any documentation related to your project.

- __Additional Files:__
  - Include a `README.md` file to provide an overview of your project, its purpose, and how to use it.
  - Include a `.gitignore` file to specify which files and directories should be ignored by version control.
  - Include a `LICENSE` file to state the terms under which your code is shared.

By organizing your CMake project in this manner, you'll make it easier for yourself and other developers to navigate, understand, and maintain your codebase as it grows in complexity.
For more information see [The Pitchfork Layout](https://api.csswg.org/bikeshed/?force=1&url=https://raw.githubusercontent.com/vector-of-bool/pitchfork/develop/data/spec.bs).


## Manually creating a CMake project

In your selected project directory, create a file named `CMakeLists.txt`. This file contains instructions for CMake to configure and generate build files.

> Note: Creating a new Project in CLion will do this for you.

Here's a basic `CMakeLists.txt` example:

```cmake
# Specify the minimum required version of CMake.
cmake_minimum_required(VERSION 3.15)

# Define the project name.
project(MyProject)

# The 'project' command above initializes the project.
# Now, let's add our source files to be compiled into an executable.
# 'add_executable' associates source files with the project and generates the executable.
add_executable(MyExecutable main.cpp)

# Note: You can add more source files by extending the 'add_executable' line.
# For example, 'add_executable(MyExecutable main.cpp another_file.cpp)'
```

### Building from the Command Line

CMake projects can be built using the Command Line using a variation of the commands below.

```
//Windows
cmake . -A x64 -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release

//Linux & Mac
cmake . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

This assumes that `cmake` command is available. That is, CMake is installed and globally available on the system i.e. added to PATH.

## Summary

Mastering CMake will empower you to efficiently manage your C++ projects, create consistent and reliable build systems, and collaborate effectively in the world of software development.

