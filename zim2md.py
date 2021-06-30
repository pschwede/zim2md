#!/usr/bin/env python3

"""
Converts [Zim Desktop Wiki](https://zim-wiki.org) to Markdown

Usage:
    python zim2md.py <input.file >output.file
"""

from typing import List
from re import sub, fullmatch, findall


def __compatible(lines):
    """Return True iff the first two lines of a file allute to it being
    convertible or not."""
    if len(lines) < 2:
        return False
    if not fullmatch(r"^Content-Type: text/x-zim-wiki$", lines[0].strip()):
        return False
    if not fullmatch(r"^Wiki-Format: zim 0\.[0-6]$", lines[1].strip()) is not None:
        return False
    return True


def compatible(path=None, infile=None, lines=None):
    """Return True iff the given path points to a Zim Wiki file."""
    if path is not None:
        with open(path, "r") as _f:
            return __compatible(_f.readlines()[:4])
    elif infile is not None:
        return __compatible(infile.readlines()[:4])
    elif lines is not None:
        return __compatible(lines[:4])
    return True


def translate(text: List[str], path:str = "") -> List[str]:
    """Discards the first four lines. All other lines are converted."""
    # The first 4 lines usually contain file format info.
    text = text[4:]
    for i, line in enumerate(text):
        # Head lines
        line = sub(r"^(=+)([^=]+)=+$", r"\g<1>\g<2>", line)
        line = sub(r"^======", "#", line)
        line = sub(r"^=====", "##", line)
        line = sub(r"^====", "###", line)
        line = sub(r"^===", "####", line)
        line = sub(r"^==", "#####", line)
        line = sub(r"^=", "######", line)

        # Links
        for link in findall(r"\[\[.+?\]\]", line):
            label, target = None, None
            tokens = link[2:-2].split("|")

            if len(tokens) > 2:
                # probably not a link.
                continue

            if len(tokens) == 2:
                label, target = tokens
            else:
                label = tokens[0]
                target = tokens[0]

            if target[0] == '+':
                target = path + "/" + target[1:] if path else target[1:]
            target = target.replace(" ", "_")
            target = target.replace(":", "/")
            if not target.endswith(".txt") and not target.endswith(".md"):
                target += ".txt" # txt is zim
            line = line.replace(link, f"[{label}]({target})", 1)
        line = sub(r"\+([A-Z]\s+)", r"[\g<1>](\g<1>)", line)

        # Lists
        line = sub(r"^(\s*)\[[*]\]", r"\g<1>- [x]", line, count=1)
        line = sub(r"^(\s*)\[[x]\]", r"\g<1>- [-]", line, count=1)
        line = sub(r"^(\s*)\[[>]\]", r"\g<1>- [>]", line, count=1)
        line = sub(r"^(\s*)\[[ ]\]", r"\g<1>- [ ]", line, count=1)
        # TODO indented list elements without dots or checkboxes

        text[i] = line

    # TODO more features
    return text


if __name__ == "__main__":
    import sys
    ls = sys.stdin.readlines()
    if compatible(lines=ls):
        sys.stdout.writelines(translate(text=ls))
    else:
        sys.stderr.writelines(["FATAL: Incompatible file.\n"])
        sys.exit(1)
