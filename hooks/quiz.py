"""MkDocs hook: turn a ```quiz fenced block into a multiple-choice question.

Authoring syntax — put it in any `docs/*.md` file, usually just below a code
block the question asks about. Use a **four-backtick** fence, so the
explanation is free to contain an ordinary ```cpp block:

    ````quiz
    What does this print?
    - `8.33333`
    - =`8`
    - It does not compile
    :::
    `(7 + 8 + 10)` is an `int` expression, so `/ 3` is **integer division**...
    ````

* Everything before the first `- ` option is the question stem.
* Each option is a `- ` list item. Exactly one is marked correct by an `=`
  immediately after the dash. Options are shown in the order written, so put
  the tempting wrong answer first as often as not.
* Everything after the `:::` line is the explanation, revealed once the reader
  has committed to an answer.

The block is rewritten to plain HTML carrying `markdown="1"` / `markdown="span"`
attributes, so the normal Markdown pipeline still formats the stem, the options
and the explanation — inline code, emphasis and links all work inside them.
That relies on the `md_in_html` extension, which mkdocs.yml enables.

The correct answer ends up in the page source as a `data-correct` attribute.
That is deliberate and matches the blurred-spoiler precedent: this is a
self-check, not an exam. The point is to make the reader commit to an answer
before seeing the explanation, not to defeat someone reading the HTML.
"""

import re
from typing import Match


# The opening fence is anchored to the start of a line (^ with re.MULTILINE),
# matching the convention in compiler_explorer.py: quizzes are authored at the
# top level, and an unanchored opener paired with a column-0 closer would let
# the lazy `.*?` run past the intended end of the block.
#
# The fence length is captured and back-referenced, so a four-backtick quiz is
# closed only by four backticks. That is what lets an explanation contain an
# ordinary ```cpp block showing the fix — with a fixed three-backtick fence the
# lazy `.*?` would stop at the *inner* opener and mangle the page. Author every
# quiz with four backticks and nesting is never a worry.
_QUIZ_RE = re.compile(
    r"^(?P<fence>`{3,})quiz[ \t]*\n(?P<body>.*?)\n(?P=fence)[ \t]*$",
    re.DOTALL | re.MULTILINE,
)

_OPTION_RE = re.compile(r"^-[ \t]+(?P<correct>=)?(?P<text>.*)$")

_EXPLANATION_SEPARATOR = ":::"


def _render(stem: list, options: list, explanation: list) -> str:
    """Build the HTML for one question."""
    parts = ['<div class="quiz" markdown="1">']

    if stem:
        parts.append('<div class="quiz-stem" markdown="1">')
        parts.append("\n".join(stem))
        parts.append("</div>")

    # The <ul> needs `markdown="1"` of its own: md_in_html only descends into an
    # element that carries the attribute, so without it the <li>s below would be
    # treated as raw HTML and their `markdown="span"` never honoured — options
    # would render with literal backticks. `markdown="span"` on each <li> then
    # runs inline Markdown only, so `` `8` `` becomes <code>8</code> without
    # wrapping the item in a <p>.
    parts.append('<ul class="quiz-options" markdown="1">')
    for is_correct, text in options:
        correct_attr = ' data-correct="1"' if is_correct else ""
        parts.append(
            f'<li class="quiz-option" role="button" tabindex="0"'
            f'{correct_attr} markdown="span">{text}</li>'
        )
    parts.append("</ul>")

    if explanation:
        parts.append('<div class="quiz-answer" markdown="1">')
        parts.append("\n".join(explanation))
        parts.append("</div>")

    parts.append("</div>")
    return "\n".join(parts)


def _replace(match: Match) -> str:
    body = match.group("body")

    stem: list = []
    options: list = []
    explanation: list = []

    in_explanation = False
    for line in body.split("\n"):
        stripped = line.strip()

        if stripped == _EXPLANATION_SEPARATOR:
            in_explanation = True
            continue

        if in_explanation:
            explanation.append(line)
            continue

        option = _OPTION_RE.match(stripped)
        if option:
            options.append((bool(option.group("correct")), option.group("text").strip()))
            continue

        # Anything before the first option belongs to the stem. A blank line
        # after the options (but before `:::`) is just spacing — drop it rather
        # than letting it fall into the stem out of order.
        if not options:
            stem.append(line)

    # A block with no options is malformed; leave it exactly as written so the
    # mistake is visible on the page rather than silently swallowed.
    if not options:
        return match.group(0)

    # Trailing blank lines in the stem would render as an empty paragraph.
    while stem and not stem[-1].strip():
        stem.pop()
    while explanation and not explanation[0].strip():
        explanation.pop(0)

    return _render(stem, options, explanation)


def on_page_markdown(markdown: str, **kwargs) -> str:
    return _QUIZ_RE.sub(_replace, markdown)
