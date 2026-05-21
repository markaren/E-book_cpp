# AIS1003 E-book

Welcome to the E-book for the course [AIS1003](https://www.ntnu.no/studier/emner/AIS1003#tab=omEmnet).

**Read online: [markaren.github.io/E-book_cpp](https://markaren.github.io/E-book_cpp/)**

The book will be updated regularly throughout the semester. Make sure to bookmark it!

> Note. The book is in an early state of development. Consider it a preview.

## Content

| Week | Topic                                                                                                                                                                                                                                                                                                                                                                                                                  |
|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  34    | <ul><li> [Introduction](docs/Chapter1/introduction.md) <ul><li>[Basic Structure](docs/Chapter1/basic_structure.md)</li><li>[Control Statements](docs/Chapter1/control_statements.md)</li><li>[Variables and Basic Types](docs/Chapter1/variables.md)</li><li>[Functions](docs/Chapter1/functions.md)</li><li>[Operators and Expressions](docs/Chapter1/operators_expressions.md)</li></ul> <li>[Getting Started](docs/getting_started.md)</li> </li></ul> |
|  35    | <ul><li>[CMake introduction](docs/Chapter2/cmake_intro.md)</li><li>[Version Control & Git](docs/Chapter2/version_control.md)</li><li>[PlatformIO](docs/Chapter2/platformio.md)</li> </ul>  |
|  36    | <ul><li>[C++ Standard Library](docs/Chapter2/standard_library.md)</li><li>[Data structures](docs/Chapter2/data_structures.md)</li> </ul> |
|  37,38    | <ul><li>[Classes](docs/Chapter3/classes.md)</li> <ul><li>[RAII](docs/Chapter3/raii.md)</li></ul> <li>[Values, References & Pointers](docs/Chapter3/types_refs_ptrs.md)</li> <li>[IO & Streams](docs/Chapter3/io_streams.md)</li></ul> |
|  39,40    | <ul> <li>[Memory Management](docs/Chapter4/memory.md)</li> <li>[Move semantics](docs/Chapter4/move.md)</li> </ul> |
|  41,42    | <ul> <li>[Polymorphism](docs/Chapter4/polymorphism.md)</li><li> [Templates](docs/Chapter4/templates.md) </li> </ul> |
|  43    | <ul> <li>[Separation of Concerns](docs/Chapter5/soc.md)</li><li> [Observer Pattern](docs/Chapter5/observer.md) </li><li> [Testing](docs/Chapter5/testing.md) </li><li> [Error Handling](docs/Chapter5/error_handling.md) </li> </ul> |

### Additional resources

While aimed to support your endeavours, this book should not be treated as a complete reference guide. It is crucial that you supplement with other resources.
Below is a non-exhaustive list of recommended learning resources.

#### Books
- __C++ Primer, Fifth Edition__ - A comprehensive and widely-used introductory book on C++ programming, covering essential concepts and techniques for beginners.
- __A Tour of C++__ - A concise and high-level overview of modern C++ features, focusing on important language elements and programming principles for intermediate programmers.

#### Online

- [__cppreference__](https://en.cppreference.com/w/) - A reliable online reference for C++ programming, providing detailed and up-to-date documentation on C++ language features, libraries, and standard functions.
- [__LearnCpp__](https://www.learncpp.com/) - An online resource offering comprehensive tutorials and guides to help beginners learn C++ programming through step-by-step lessons and practical examples.
- [__Stack Overflow__](https://stackoverflow.com/) - A popular online platform where programmers ask questions, share knowledge, and find solutions to programming-related issues from a community of developers worldwide.

### [Common terms](docs/terms.md)

### [Frequently asked questions (FAQ)](docs/faq.md)

---

## Building the site locally

The site is built with [MkDocs](https://www.mkdocs.org/) and the [Material](https://squidfunk.github.io/mkdocs-material/) theme.

```bash
pip install -r requirements.txt
mkdocs serve     # live preview at http://127.0.0.1:8000
mkdocs build     # produces ./site
```

The site is published automatically to GitHub Pages on every push to `main` via [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).
