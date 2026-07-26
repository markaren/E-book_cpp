#!/usr/bin/env python3
"""Prove that the checkers in this folder actually catch things.

    python tools/selftest.py site

A checker that only ever passes is worse than no checker: it buys confidence
without earning it. This plants a known defect in a *copy* of the built site,
runs the relevant checker, and asserts it fails — then checks that an untouched
copy still passes.

Both of these were caught by writing this file: `check_links.py` ignores the
theme's navigation (so a test that mutates a nav link proves nothing), and
`check_quizzes.py` originally looked for leaked authoring syntax only on pages
where a quiz had parsed successfully — skipping the check in precisely the case
where the hook had failed.

Exits non-zero if any planted defect goes undetected.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
ARTICLE_RE = re.compile(r"<article\b.*?</article>", re.DOTALL)
PAGE = "Chapter1/exercises/index.html"


def run_checker(script, site):
    r = subprocess.run(
        [sys.executable, os.path.join(TOOLS, script), site],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return r.returncode, r.stdout + r.stderr


def patch_article(site, rel, fn):
    """Rewrite the article body of one page. The nav is not under test."""
    path = os.path.join(site, rel.replace("/", os.sep))
    html = open(path, encoding="utf-8").read()
    m = ARTICLE_RE.search(html)
    if not m:
        raise RuntimeError(f"no <article> in {rel}")
    open(path, "w", encoding="utf-8").write(html[: m.start()] + fn(m.group(0)) + html[m.end():])


CASES = [
    ("broken link", "check_links.py", "BROKEN LINK",
     lambda a: a.replace('href="../variables/"', 'href="../nope/"', 1)),
    ("broken anchor", "check_links.py", "BROKEN ANCHOR",
     lambda a: a.replace('href="../functions/#parameters-are-copies"',
                         'href="../functions/#no-such-heading"', 1)),
    ("no correct option", "check_quizzes.py", "0 correct options",
     lambda a: a.replace(' data-correct="1"', "", 1)),
    ("two correct options", "check_quizzes.py", "2 correct options",
     lambda a: a.replace('<li class="quiz-option" role="button"',
                         '<li class="quiz-option" data-correct="1" role="button"', 1)),
    ("leaked quiz syntax", "check_quizzes.py", "leaked",
     lambda a: a.replace("</article>", ":::</article>", 1)),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", nargs="?", default="site", help="built site directory")
    args = ap.parse_args()

    if not os.path.isdir(args.site):
        sys.exit(f"error: '{args.site}' is not a directory — run `mkdocs build` first")

    rows, ok = [], True

    for name, script, expect, mutate in CASES:
        tmp = tempfile.mkdtemp(prefix="selftest-")
        try:
            site = os.path.join(tmp, "site")
            shutil.copytree(args.site, site)
            patch_article(site, PAGE, mutate)
            code, out = run_checker(script, site)
            caught = code != 0 and expect.lower() in out.lower()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        ok &= caught
        rows.append((name, script, caught))

    # And the control: an unmodified site must pass both.
    clean = all(run_checker(s, args.site)[0] == 0
                for s in ("check_links.py", "check_quizzes.py"))
    ok &= clean
    rows.append(("clean site passes", "both", clean))

    width = max(len(r[0]) for r in rows)
    for name, script, good in rows:
        print(f"  {'ok  ' if good else 'FAIL'}  {name:{width}}  ({script})")

    if not ok:
        print("\nFAILED: a planted defect was not detected")
        return 1
    print(f"\nOK: {len(rows)} self-tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
