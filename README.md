# zim2md

Executable Python module for converting [Zim Wiki](https://zim-wiki.org) to Markdown.

## Command Line Interface

### Install

Just have python3 for your default Python engine.

### Usage

```bash
./zim2md.py <input.file >output.file
```

If you are on Windows, you might be required to mention your python interpreter in the command line explicitly. May be like so:
```cmd
C:\Programs\Python3.8\python3.exe zim2md.py <input.file >output.file
```

## Python module

### Install

Clone this Github project as a submodule:
```bash
git submodule add https://github.com/pschwede/zim2md.git zim2md
```

### Usage

Example:

```python
from zim2md import zim2md

with open("input.file", "r") as _f:
	print(zim2md.translate(_f.readlines()))
```
