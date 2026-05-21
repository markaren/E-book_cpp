# Using AI for Coding

AI assistants — ChatGPT, Claude, Copilot, Gemini, and the rest — can write C++. They can explain it, debug it, refactor it, and answer questions about it at any hour of the day. They are genuinely useful tools, and you will use them. Everyone will.

The question is not *whether* to use them. The question is how to use them in a way that makes you a better programmer instead of one that quietly becomes worse over time.

This page is the short, honest version of what they are, what they are good and bad at, and the working habits that let you get the benefit without losing the skill.

---

## What an LLM actually is

A **large language model** is, in one sentence, a statistical engine that predicts what text plausibly comes next given the text so far. It was trained on enormous amounts of text — books, websites, code repositories, forum threads — and learned the patterns inside it. When you ask it to "write a C++ program that reads a CSV file", it does not understand CSVs. It produces the kind of text that, statistically, follows a request like that.

Three consequences matter for using it:

1. **It has no compiler, no debugger, and no eyes.** It cannot run code, cannot read your screen, cannot tell whether what it just produced will compile. It is reasoning entirely from patterns in text.
2. **It can be confidently wrong.** Because it produces fluent, plausible-looking text, mistakes do not announce themselves. The output reads like an expert wrote it whether or not an expert *would* have written it.
3. **Its C++ knowledge is skewed to what was on the internet.** A lot of internet C++ is old — pre-`std::unique_ptr`, pre-`auto`, full of `using namespace std;` and raw `new`/`delete`. Modern best practice is under-represented in training data compared to its actual frequency in good codebases.

All of these are getting better over time. None of them have gone away.

---

## What AI is genuinely good at

Used well, an AI assistant is one of the best learning tools you have ever had access to. The places it shines:

- **Explaining concepts in a different voice.** If the textbook explanation of references doesn't click, asking "explain references in C++ as if I have used Python" often does.
- **Reading scary error messages.** Paste a 200-line template error and ask "what is this complaining about?" — it can usually translate the wall of text into one sentence.
- **Generating boilerplate.** A `CMakeLists.txt` for a project with a library and tests, a basic class skeleton with constructors and getters, a `Makefile`-style script — these have one obvious correct shape and AI produces them quickly and reliably.
- **Translating between languages.** "Here is my Python solution; what would this look like in C++?" is a fast way to bridge prior experience.
- **Rubber-ducking.** Describing your problem out loud often makes you realise the answer; doing it to an AI works the same way, plus it sometimes notices things you missed.
- **Code review on your own code.** "Here's the function I just wrote, do you see any bugs or things I could simplify?" is a much better prompt than "write a function that does X."

---

## What AI is not good at

The reverse list, equally important:

- **Code beyond a screen or two.** Once your problem touches several files or a longer-than-trivial flow, the model starts losing track of context and inventing things.
- **Following your project's conventions.** It doesn't know your naming style, your existing helpers, your team's choices. It will happily write code that contradicts the rest of your codebase.
- **Modern C++ idioms specifically.** This one bites students: ask for "a C++ program that…" and you have a 50/50 chance of getting `using namespace std;`, raw `new`/`delete`, and other anti-patterns this book has taught you to avoid. You usually have to ask explicitly for *modern* C++.
- **Distinguishing true from plausible.** It will invent library functions, parameter names, and standard headers that don't exist, presented in confident prose. The cppreference page for `std::frobnicate` does not exist; the AI's description of it does.
- **Subtle bugs in its own output.** It is much better at writing code than at testing it. Code that "looks right" from the AI is not the same as code that *is* right.

---

## The trap

Here is the bit you should re-read every semester.

The danger of AI is not that it will write your assignments. The danger is that it will write them *well enough* that you never learn to write them yourself, and you will not notice you haven't learned until much later — typically at an exam, an interview, or a job where you are expected to actually program.

There are specific skills that only develop through doing-it-yourself, even when AI could do it faster:

- **Reading a compiler error and knowing what it means.** This skill comes from being confused by hundreds of errors and figuring them out. Outsourcing every error to AI means you never build the pattern recognition.
- **Holding a program in your head.** Real debugging is mostly mental simulation: "if the loop runs three times, then `i` will be…" Skipping straight to "the AI says fix it like this" prevents you from ever building that mental simulator.
- **Knowing what is idiomatic.** You can only recognise a clean solution if you have seen and written messy ones. If your only experience with class design is reading AI output, your taste won't develop.
- **Confidence under pressure.** In a one-hour exam with no internet, your AI is not there. Whatever skill is in your hands is what you have.

A specific failure mode that is now common: students who can solve every weekly assignment via AI but cannot write a `for` loop without it. They feel competent during the term and discover their gap only when graded individually under controlled conditions.

---

## Habits that protect the learning

The trade-off above is real but not absolute. The following practices give you most of the upside without most of the downside.

### Try first, ask second

Spend at least ten minutes trying a problem on your own before asking AI. Even if you fail, you have built a mental map of what is hard. When the AI then shows you a solution, you understand *why* its choice helps — instead of skipping over a problem you never engaged with.

### Type the code yourself, even if you didn't write it

Copy-pasting from AI is the single biggest barrier to learning. Your fingers and your visual memory contribute to skill in ways scrolling doesn't. If you accept an AI-written function, retype it. Yes, manually. This is the single highest-value habit on this page.

### Ask "why", not just "what"

After AI gives you code, ask it to explain *why* — why this approach, why this header, why this signature. Then check the explanation. If the explanation doesn't make sense to you, you don't yet understand the code, and you should not turn it in.

### Verify by running, not by reading

AI output reads convincingly even when it's broken. Compile it. Run it on edge cases. Especially run it on the inputs the AI did not mention.

### Be specific about your context

A bare "write me C++ to sort a vector" gets you generic, often dated code. Better:

> "Write modern C++20 code to sort a `std::vector<Reading>` by their `timestamp` field, ascending. I am using GCC 13, no external libraries."

The more constraints you give, the closer the output is to what you actually want. Tell it the language standard, the platform, your level, your style.

### Use it for review, not generation

A surprisingly good prompt:

> "Here's the function I wrote: `[paste]`. What bugs or improvements do you see? Don't rewrite it — just point things out."

This keeps *you* writing the code, with the AI as a second pair of eyes. The code stays yours; the feedback helps.

### Treat its output like Wikipedia

Useful starting point. Possibly wrong. Always verify against a primary source ([cppreference](https://en.cppreference.com/), the standard, the docs of the library you're using) before relying on it for anything that matters.

---

## Working with AI on this course specifically

A few practical tips for getting good C++ out of an assistant in this course's context:

- **State the standard.** "Use C++20" in your prompt. Otherwise expect C++98 idioms.
- **Forbid the bad habits.** "No `using namespace std;`. No raw `new`/`delete` — use `std::unique_ptr` or standard containers. Use RAII." Once stated, most models comply.
- **Ask for the smallest version first.** "Show me the minimum CMakeLists.txt to build one executable" is a better prompt than "set up a full CMake project for me."
- **For errors, paste the whole thing.** Give the AI your code *and* the full compiler output. Don't summarise — the full text often contains the clue.
- **Distinguish concepts from generation.** When you don't understand something — references, RAII, virtual functions — asking AI to explain is great. When you have an assignment problem to solve, write it yourself first.

---

## Academic integrity

This book does not set the rules for what counts as cheating in your specific course — your course staff and the institution do. Find those rules and follow them. If AI use must be disclosed, disclose it. If it is forbidden on a particular assignment, don't use it. The rules apply whether or not the AI is detectable.

Independent of any course rule: if your name is on something and you cannot explain every line of it under questioning, you should treat that as a problem worth fixing before turning it in.

---

## Summary

- LLMs are excellent tools and treacherous teachers. They are both at once.
- They predict plausible text. They do not know things; they do not run things; they can be confidently wrong.
- They are great for explanation, boilerplate, error decoding, and code review.
- They are bad at large programs, your local style, modern idioms, and telling you when they are guessing.
- The risk is not that AI writes your code. The risk is that you never learn to.
- Type code yourself even if AI wrote it. Ask "why", not just "what". Try first, ask second.
- State the C++ standard, forbid raw `new`/`delete`, and verify by running.
- Whatever rules apply to your course: follow them.

The best programmers in 2026 use AI heavily. They are also the people who could write everything they ask AI for, just slower. Be one of those people.
