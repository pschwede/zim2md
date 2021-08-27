# Zim to Markdown conversion

Executable Python module for converting [Zim Wiki](https://zim-wiki.org) to [logseq](https://github.com/logseq/logseq)-compatible Markdown.

#### Requirements

Just have python3 for your default Python engine.

#### Usage of the scripts

##### Logseq
```bash
./zim2logseq.py <input.file >output.file
```

##### Obsidian
```bash
./zim2obsidian.py <input.file >output.file
```

If you are on Windows, you might be required to explicitely mention your python interpreter in the command line. May be like so:
```cmd
C:\Programs\Python3.8\python3.exe zim2md.py <input.file >output.file
```

#### Installing the python module

Clone this Github project as a submodule:
```bash
git submodule add https://github.com/pschwede/zim2md.git zim2md
```

#### Usage of the python module

Example:

```python
from zim2md import zim2md

with open("input.file", "r") as _f:
	print(zim2md.translate(_f.readlines()))
```
