"""MkDocs hook: append a "Run on Compiler Explorer" link to runnable C++ blocks.

For every fenced ```cpp block whose source contains `int main`, generates a
Compiler Explorer URL that opens the code in an editor + executor pane (no
assembly view) and inserts a small link immediately below the block.

Blocks without `int main` are left alone — they are snippets, not standalone
programs, and would not run on their own.

The Compiler Explorer state is encoded directly into the URL via the
documented `/clientstate/<base64-json>` endpoint. No upload, no API call, no
external dependency at build time.
"""

import base64
import json
import re
from typing import Match


# GCC 13.2 with C++20 — matches the course standard. To bump, change here.
COMPILER_ID = "g132"
COMPILER_OPTIONS = "-std=c++20 -O0 -Wall -Wextra -pedantic"


# Match a fenced cpp block, with or without trailing attributes on the opener.
# IMPORTANT: the attributes match uses [ \t]+ rather than \s+ — \s matches \n,
# which would greedily eat the first source line as part of the "attributes".
_CODE_BLOCK_RE = re.compile(
    r"```cpp(?:[ \t]+[^\n]*)?\n(.*?)\n```",
    re.DOTALL,
)


def _make_url(source: str) -> str:
    """Build a Compiler Explorer URL that opens the code in an executor pane.

    The `executors` array (instead of `compilers`) is what hides the assembly
    view — the executor combines build + run into one panel showing program
    output, not disassembly.
    """
    state = {
        "sessions": [
            {
                "id": 1,
                "language": "c++",
                "source": source,
                "compilers": [],
                "executors": [
                    {
                        "arguments": "",
                        "compilerVisible": False,
                        "compilerOutputVisible": False,
                        "argumentsVisible": False,
                        "stdinVisible": False,
                        "stdin": "",
                        "wrap": True,
                        "compiler": {
                            "id": COMPILER_ID,
                            "options": COMPILER_OPTIONS,
                            "libs": [],
                        },
                    }
                ],
            }
        ]
    }
    payload = json.dumps(state, separators=(",", ":"))
    encoded = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("ascii")
    return f"https://godbolt.org/clientstate/{encoded}"


def _replace(match: Match) -> str:
    full_block = match.group(0)
    source = match.group(1)
    if "int main" not in source:
        return full_block
    url = _make_url(source)
    link = (
        f'<a href="{url}" target="_blank" rel="noopener" '
        f'class="ce-run-link">▶ Run on Compiler Explorer</a>'
    )
    return f"{full_block}\n\n{link}\n"


def on_page_markdown(markdown: str, **kwargs) -> str:
    return _CODE_BLOCK_RE.sub(_replace, markdown)
