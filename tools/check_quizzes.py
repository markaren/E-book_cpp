#!/usr/bin/env python3
"""Check the multiple-choice questions in the built site.

Run it against the output of `mkdocs build`:

    python tools/check_quizzes.py site

A quiz is authored as a ````quiz block (see hooks/quiz.py) and rendered to
HTML. Three things can go wrong silently, and all three survive a clean build:

* **No correct option**, or more than one. `quiz.js` marks whichever options
  carry `data-correct`, so a missing `=` in the source produces a question that
  is simply unanswerable — it goes red whatever the reader picks.
* **Too few options.** A question with one or two is not worth asking.
* **A malformed block.** If the fence or the `:::` separator is wrong, the hook
  leaves the block alone and the raw authoring syntax renders as literal text.

Exits non-zero on any of them, so CI fails rather than shipping a broken quiz.
"""

import argparse
import os
import re
import sys

QUIZ_RE = re.compile(r'<div class="quiz">.*?</ul>', re.DOTALL)
OPTION_RE = re.compile(r'<li class="quiz-option"([^>]*)>')
ARTICLE_RE = re.compile(r"<article\b.*?</article>", re.DOTALL)

MIN_OPTIONS = 3

# Authoring syntax that must never reach the page. If any of these show up, the
# hook did not process a block it should have.
LEAKED = [
    (":::", "the quiz explanation separator"),
    ("````", "a four-backtick quiz fence"),
    ('markdown="', "an md_in_html attribute"),
]


def check_page(rel, html):
    problems = []
    match = ARTICLE_RE.search(html)
    article = match.group(0) if match else html

    quizzes = QUIZ_RE.findall(article)
    for index, block in enumerate(quizzes, start=1):
        options = OPTION_RE.findall(block)
        correct = sum(1 for attrs in options if 'data-correct="1"' in attrs)
        if correct != 1:
            problems.append(
                f"{rel} quiz {index}: {correct} correct options, expected exactly 1"
            )
        if len(options) < MIN_OPTIONS:
            problems.append(
                f"{rel} quiz {index}: only {len(options)} options, expected at least {MIN_OPTIONS}"
            )

    # Deliberately NOT guarded by `if quizzes:`. When the hook fails to parse a
    # block, no `.quiz` div is produced at all — so guarding on a successful
    # parse would skip the check in exactly the case it exists to catch. None of
    # these markers appear anywhere in the built site legitimately.
    for needle, what in LEAKED:
        if needle in article:
            problems.append(f"{rel}: {what} leaked into the rendered page ({needle!r})")

    return len(quizzes), problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", nargs="?", default="site", help="built site directory")
    args = ap.parse_args()

    if not os.path.isdir(args.site):
        sys.exit(f"error: '{args.site}' is not a directory — run `mkdocs build` first")

    total, pages_with_quizzes, problems = 0, 0, []
    for root, _dirs, files in os.walk(args.site):
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, args.site).replace(os.sep, "/")
            count, found = check_page(rel, open(full, encoding="utf-8").read())
            total += count
            pages_with_quizzes += 1 if count else 0
            problems.extend(found)

    print(f"quizzes found : {total} across {pages_with_quizzes} page(s)")
    for p in problems:
        print(f"  PROBLEM: {p}")

    if problems:
        print(f"\nFAILED: {len(problems)} problem(s)")
        return 1
    if total == 0:
        print("OK: no quizzes to check")
        return 0
    print("OK: every question has exactly one correct option")
    return 0


if __name__ == "__main__":
    sys.exit(main())
