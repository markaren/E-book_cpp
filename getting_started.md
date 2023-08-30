# Getting started

In order to get started with C++, you need a compiler. Simply put, a compiler is a software program that processes instructions written in a programming language 
and creates a binary file that the machine’s CPU can understand and execute. Compilers for Windows, Linux and MacOS are typically different. 

You are expected to use [CLion](https://www.jetbrains.com/clion/) in this course. CLion is a cross-platform IDE for C and C++, which is free for students. 
CLion comes bundled with CMake, so you do not have to install that independently. On Windows it also comes with a working compiler that uses the MinGW toolchain. 
However, you might consider using the MSVC compiler, which is tailored to Windows.

## Windows

_Optional:_ Download [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/). 
This is the preferred compiler on Windows, however, you can opt to use the MinGW toolchain that come bundled with CLion.

## MacOS
Apple supports C++ with the Apple Clang compiler (included in Xcode). 

## Linux 
In Debian-based distributions, the most well-known C and C++ compilers are gcc and g++. If your system doesn’t have the build-essential package 
installed in your system by default, you can install the latest available version from the default distribution repositories as follows:

```
sudo apt-get update && sudo apt-get install build-essential
```


## Your first project

With CLion and a working compiler setup:

1. Open CLion and choose `New Project`.
2. Under C++, choose C++ executable.
3. Specify the location of the project and set the language standard to C++17/20.
4. A CMake settings window should appear. If not goto `File->Settings->Build, Execution, Deployment->CMake`. The default settings are likely OK.
   - If you have installed Visual Studio under Windows, however, you might want to go `File->Settings->Build, Execution, Deployment->Toolchains` and add Visual Studio using the `+`. Make sure to select `x86_amd64` under `Architecture`.

> Note. It's not a good idea to specify the location as a folder under cloud storage. This will result a large number of files beeing synchronized during building,
> and of you use multiple PC's you'll end up with synchronization issues as the build files generated are PC specific.
>
> Furthermore, paths with special characters (including Norwegian ones) are likely to lead to hard to understand errors at least on Windows. Also _try_ to avoid paths with spaces. 

With the configuration done, CLion as now created a dummy "Hello world" project for you. It consists of two files:

##### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.15)
project(demo)

set(CMAKE_CXX_STANDARD 17)

add_executable(demo main.cpp)
```

##### main.cpp

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

C++ needs to be compiled prior to execution.

> Click the green "hammer" in the upper right corner to build, or the green "play" button to build & run.
> 
> You may also right click somewhere inside the `main` function to get a "run" context action.

Executing the code should produce `Hello, World!` in the terminal window embedded in CLion (located in the lower panel).
