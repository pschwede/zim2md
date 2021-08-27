# Zim to Markdown conversion

Executable Python module for converting [Zim Wiki](https://zim-wiki.org) to [logseq](https://github.com/logseq/logseq)-compatible Markdown.

#### Requirements

Just have python3 for your default Python engine.

#### Use the scripts

##### Convert single files

**Logseq:**
```bash
./zim2logseq.py <input.file >output.file
```

**Obsidian:**
```bash
./zim2obsidian.py <input.file >output.file
```

**Under windows:**
If you are on Windows, you might be required to explicitely mention your python interpreter in the command line. May be like so:
```cmd
C:\Programs\Python3.8\python3.exe zim2logseq.py <input.file >output.file
```

##### Convert a complete notebook

```bash
./zim2logseq.py /path/to/original/Notes /path/to/new/Notes
```

#### Install it as a Python module

**Clone this Github project as a submodule:**
```bash
git submodule add https://github.com/pschwede/zim2md.git zim2md
```

**Code example:**
```python
from zim2logseq import zim2logseq

with open("input.file", "r") as _f:
	print(zim2logseq.translate(_f.readlines()))
```
