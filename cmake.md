# CMake 

CMake is a powerful tool in the world of C++ programming that simplifies the process of building, compiling, and managing complex projects. It helps you create cross-platform, organized, and easily maintainable codebases.

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

- Simplicity: CMake simplifies the process of configuring, building, and managing complex projects, abstracting away platform-specific details.
- Cross-Platform: With CMake, you can generate build files that work seamlessly on different platforms without significant modifications.
- Modularity: CMake promotes modular project organization, making it easier to manage larger codebases and libraries.
- Dependencies: CMake simplifies the inclusion of external libraries and dependencies into your project.
- IDE Integration: CMake integrates with various Integrated Development Environments (IDEs), allowing you to work within your preferred coding environment.

#### Going further:

- __Adding Libraries:__ Use `target_link_libraries` to link your executable with external libraries.
- __Multiple Source Files:__ Add all your source files to the `add_executable` line in the `CMakeLists.txt` file.
- __Organizing Code:__ Create subdirectories for different parts of your project and use `add_subdirectory` in your `CMakeLists.txt`.

## Summary

Mastering CMake will empower you to efficiently manage your C++ projects, create consistent and reliable build systems, and collaborate effectively in the world of software development.

[CLion](https://www.jetbrains.com/clion/) is a powerfull and cross-platform C/C++ IDE that supports CMake projects, which we will use in this course. 
As an NTNU student, you are [eligible for a free license](https://www.jetbrains.com/community/education/#students).  

### Creating a CMake project

In your project directory, create a file named `CMakeLists.txt`. This file contains instructions for CMake to configure and generate build files.
Creating a new Project in CLion will do this for you.

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

