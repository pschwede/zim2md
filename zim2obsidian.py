#!/usr/bin/env python3

"""
Converts [Zim Desktop Wiki](https://zim-wiki.org) to Markdown

Usage:
    python zim2md.py <input.file >output.file
"""

import os
from re import sub, fullmatch, findall
from pathlib import Path
from datetime import datetime
from typing import List

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


def translate(text: List[str], path:str="", nbpath:str="") -> List[str]:
    """Discards the first four lines. All other lines are converted."""
    # The first 4 lines usually contain file format info.
    text = text[4:]
    headline_nr = 0
    current_ind = 0
    title = ""
    relpath = "/".join(str(os.path.relpath(path, nbpath)).split(os.sep)[:-1])
    for i, line in enumerate(text):
        # Head lines
        line = sub(r"^(=+)([^=]+)=+$", r"\g<1>\g<2>", line) # removes tailing '='
        line = sub(r"^======", "#", line)
        line = sub(r"^=====", "##", line)
        line = sub(r"^====", "###", line)
        line = sub(r"^===", "####", line)
        line = sub(r"^==", "#####", line)
        line = sub(r"^=", "######", line)

        # Dates
        line = sub(r"\[d:(\d{4}-\d{,2}-\d{,2})](.+)$", r"\g<2>\nDEADLINE: <\g<1> Day>", line)
        line = sub(r"\[d:(\d{,2})\.(\d{,2})\.(\d{4})](.+)$", r"\g<4>\nDEADLINE: <\g<3>-\g<2>-\g<1> Day>", line) # central European date format!
        line = sub(r"\[d:(\d{,2})/(\d{,2})/(\d{4})](.+)$", r"\g<4>\nDEADLINE: <\g<3>-\g<1>-\g<2> Day>", line) # American dates!
        line = sub(r"\[d:(\d{,2}).(\d{,2}).\](.+)$",
                r"\g<3>\nDEADLINE: <" + str(datetime.now().year) + r"-\g<2>-\g<1> Day>",
                line)

        # Links
        for link in findall(r"\[\[:.+?\]\]", line):
            target = link[2:-2]
            # TODO relative to current file
            target = target.replace(":", "/")
            line = line.replace(link, f"[[{target}]]", 1)
        for link in findall(r"\[\[[^+]+?\|?[^\]]+?\]\]", line):
            label, target = None, None
            tokens = link[2:-2].split("|")

            if len(tokens) > 2:
                # probably not a link.
                continue

            if len(tokens) == 2:
                target, label = tokens
            else:
                label = tokens[0]
                target = tokens[0]

            # TODO '~' -> '/home/user'
            target = sub(r"^~", "file://"+str(Path.home()), target)

            if not target.startswith("http://") \
                    and not target.startswith("https://") \
                    and not target.startswith("file://"):
                target = target.replace(" ", "%20")
                target = target.replace(":", "/")
            if not target == label:
                line = line.replace(link, f"[{label}]({target})", 1)
            else:
                line = line.replace(link, f"[[{target}]]", 1)
        line = sub(r"(file://\S+)", r"[\g<1>](\g<1>)", line)

        # Lists
        line = sub(r"^(\s*)\[\*\]", r"\g<1>- [*]", line, count=1)
        line = sub(r"^(\s*)\[x\]", r"\g<1>- [x]", line, count=1)
        line = sub(r"^(\s*)\[>\]", r"\g<1>- [>]", line, count=1)
        line = sub(r"^(\s*)\[ \]", r"\g<1>- [ ]", line, count=1)
        # TODO indented list elements without dots or checkboxes

        # @tags and +SubPageReferences
        line = sub(r"^@(\S+)", r"#\g<1>", line)
        line = sub(r"\s+@(\S+)", r"#\g<1>", line)
        line = sub(r"\[\[\+(\S+?)\]\]", r"[[\g<1>]]", line)

        # rich text formatting
        line = sub(r"~~(.+?)~~", r"~~\g<1>~~", line)
        line = sub(r"(!?<=:)//([^:]+?)//", r"*\g<1>*", line)
        line = sub(r"\*\*(.+?)\*\*", r"**\g<1>**", line)
        line = sub(r"__(.+?)__", r"==\g<1>==", line)

        # footnotes
        line = sub(r"(?!<=\[)\[([0-9]{,4})\](?!=\])", r"[^\g<1>]", line)

        # TODO Images
        line = sub(r"{{(.+?)|(.+?)}}", r"![[\g<1>]]", line)
        line = sub(r"{{(.+?)}}", r"![[\g<1>]]", line)

        text[i] = line

    # TODO more features
    return text

if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 1:
        ls = sys.stdin.readlines()
        if compatible(lines=ls):
            sys.stdout.writelines(translate(text=ls))
        else:
            sys.stderr.writelines(["FATAL: Incompatible file.\n"])
            sys.exit(1)
    else:
        _newpath = sys.argv[2]
        _path = sys.argv[1]
        if not os.path.exists(_newpath):
            os.makedirs(_newpath)
        for _file in Path(_path).rglob("*.txt"):
            with open(_file, 'r') as _f:
                lines = _f.readlines()
                outpath = str(os.path.relpath(_file, _path))
                outpath = os.path.join(_newpath, outpath)
                try:
                    os.makedirs(os.path.dirname(outpath))
                except FileExistsError:
                    pass
                outpath = sub(r"\.txt$", ".md", str(outpath))
                if compatible(lines=lines):
                    print(f"translate {_file} to {outpath}")
                    lines = translate(lines, path=str(_file), nbpath=str(_path))
                else:
                    print(f"WARN: no conversion of {_file} but copy to {outpath}")
                with open(outpath, 'w') as _o:
                    _o.writelines(lines)
        for _file in Path(_path).rglob("*.md"):
            with open(_file, 'r') as _f:
                outpath = str(os.path.relpath(_file, _path))
                outpath = os.path.join(_newpath, outpath)
                try:
                    os.makedirs(os.path.dirname(outpath))
                except FileExistsError:
                    pass
                with open(outpath, 'w') as _o:
                    print(f"Copy {_file} to {outpath}")
                    _o.writelines(_f.readlines())
