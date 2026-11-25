#!/usr/bin/env python3
"""Write the two-line entry for Everyday Things, Two Lines, Longer Run.

Deterministic, stdlib only, no network. The entry explains a traffic jam
to a 10-year-old with one concrete, surprising analogy (a ketchup bottle),
then says honestly what the analogy maps and what it leaves out.

The program validates the entry against the sealed gate (UTF-8 text of
1-400 characters, not whitespace-only) and writes it to the output path:
ENTRY_OUT_DIR/entry.txt if ENTRY_OUT_DIR is set, else ENTRY_OUT (if that
path is a directory, entry.txt inside it), else /output/entry.txt.
"""

import os
import sys

ENTRY_LINE_ONE = (
    "A traffic jam is a ketchup bottle tipped upside down: everyone "
    "squeezes, nothing comes out, then suddenly it all rushes at once."
)
ENTRY_LINE_TWO = (
    "It maps the long wait and the sudden rush, but leaves out that no "
    "hand is squeezing the cars, and ketchup never gets angry."
)

FINAL_ENTRY = ENTRY_LINE_ONE + "\n" + ENTRY_LINE_TWO + "\n"

LIMIT_MIN_CHARS = 1
LIMIT_MAX_CHARS = 400


def validate_entry(text):
    """Return an error string if text fails the gate, else None."""
    if not (LIMIT_MIN_CHARS <= len(text) <= LIMIT_MAX_CHARS):
        return "entry must be 1-400 characters, got %d" % len(text)
    if not text.strip():
        return "entry must not be whitespace-only"
    return None


def resolve_destination():
    """Pick the entry.txt path from ENTRY_OUT_DIR / ENTRY_OUT / default."""
    out_dir = os.environ.get("ENTRY_OUT_DIR")
    out_path = os.environ.get("ENTRY_OUT")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if out_path:
        if os.path.isdir(out_path):
            return os.path.join(out_path, "entry.txt")
        return out_path
    return "/output/entry.txt"


def write_entry_text(destination, text):
    """Create parent dirs as needed and write text as UTF-8."""
    parent = os.path.dirname(destination)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(destination, "w", encoding="utf-8") as handle:
        handle.write(text)


def main():
    problem = validate_entry(FINAL_ENTRY)
    if problem is not None:
        print("gate check failed: " + problem, file=sys.stderr)
        return 1

    destination = resolve_destination()
    write_entry_text(destination, FINAL_ENTRY)
    print("wrote %d characters to %s" % (len(FINAL_ENTRY), destination))
    return 0


if __name__ == "__main__":
    sys.exit(main())
