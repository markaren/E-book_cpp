# AIS1003 E-book

Welcome to the E-book for the course [AIS1003](https://www.ntnu.no/studier/emner/AIS1003#tab=omEmnet).

This book covers an introduction to modern C++ & software engineering fundamentals.

**Read online: [markaren.github.io/E-book_cpp](https://markaren.github.io/E-book_cpp/)**

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
