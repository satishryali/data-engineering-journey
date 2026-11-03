# Paths with pathlib

A path is the address of a file or folder. Python uses paths to find input files and choose where to save output.

`pathlib` is included with Python. `Path` helps us build addresses and work with files and folders.

## Create a path

```python
from pathlib import Path

file = Path("data/orders.csv")
print(file)
```

Expected output on Windows:

```text
data\orders.csv
```

This only builds an address. It does not create the file or check whether it exists.

`Path` creates a **path object**, not an open file object. A path object represents a location. Opening that location is a separate action, such as `file.open()`.

`pathlib` is the module; `Path` is one class inside it:

| Class | Use |
| --- | --- |
| `Path` | Work with paths and actual files/folders using the current operating system |
| `PurePath` | Work with path parts without accessing files/folders |
| `WindowsPath` | Work with actual Windows paths on Windows |
| `PosixPath` | Work with actual Linux/macOS paths on those systems |
| `PureWindowsPath` | Handle Windows-style path parts on any system |
| `PurePosixPath` | Handle Linux/macOS-style path parts on any system |

For now, use `Path`. On Windows, `Path("data")` creates a `WindowsPath` object automatically.

For a Windows address, either form works on Windows:

```python
file = Path("C:/study/data/orders.csv")
file = Path(r"C:\study\data\orders.csv")
```

The `r` makes a raw string, so backslash sequences such as `\n` are not treated as special characters.

Windows normally displays backslashes (`\`); Linux/macOS use forward slashes (`/`). Python file operations on Windows also accept forward slashes, so `Path("C:/study/data/orders.csv")` is convenient.

Compare these strings:

```python
normal = "C:\new\test"      # Contains a newline (\n) and a tab (\t)
raw = r"C:\new\test"       # Keeps the backslashes literal
forward = "C:/new/test"    # No special backslash sequences; no r needed

print(raw)
print(forward)
```

Expected output:

```text
C:\new\test
C:/new/test
```

Raw strings have limits: they cannot end with an odd number of backslashes. Use `Path("C:/study")` rather than adding a final backslash.

## Absolute and relative paths

- Absolute path: the full address, such as `C:/study/data/orders.csv` on Windows.
- Relative path: an address starting from Python's current working folder, such as `data/orders.csv`.

Imagine this structure:

```text
C:/study/
    practice.ipynb
    data/
        orders.csv
```

```python
from pathlib import Path

print(Path.cwd())
print(Path("data/orders.csv").resolve())
```

Expected output on Windows, **if the working folder is C:/study**:

```text
C:\study
C:\study\data\orders.csv
```

`cwd()` means current working directory. A directory is a folder. The working folder is not always the folder containing the notebook.

`cwd()` returns the full address of the **working folder only**. It does not add the filename.

For the simple example above, `resolve()` starts from `C:/study` and adds `data/orders.csv`. It does **not search the computer** for a matching file.

You can define and print a relative path without knowing its full address:

```python
from pathlib import Path

file = Path("data/orders.csv")
print(file)
```

Expected output on Windows:

```text
data\orders.csv
```

Absolute and relative describe how an address is written, not who creates it. Both humans and Python can create either form. Python needs a target path; it cannot guess which file you mean.

Use an absolute path for a specific location on your computer. Use relative paths for project files so the project can move together, provided you run from the intended working folder. Changing the working folder changes where the same relative path points.

`resolve()` makes the path absolute and resolves symbolic links (filesystem shortcuts). Its default is `strict=False`, so a missing file does not by itself cause an error. It does not create that file. `resolve(strict=True)` raises `FileNotFoundError` for a missing path.

`Path.home()` gives the current user's home folder. Both `cwd()` and `home()` depend on the computer/session.

## Join folders and filenames

```python
from pathlib import Path

folder = Path("data")
file = folder / "orders.csv"
print(file)
```

Expected output on Windows:

```text
data\orders.csv
```

Use `/` between a `Path` and the next part. A standalone `\` is not a Python path-joining operator.

Joining paths does not check whether the first part is a folder:

```python
notebook = Path("practice/path.ipynb")
print((notebook / "analysis").as_posix())
print((notebook.parent / "analysis").as_posix())
```

Expected output:

```text
practice/path.ipynb/analysis
practice/analysis
```

The second path puts `analysis` beside the notebook. `as_posix()` displays forward slashes so this example reads the same on Windows and Linux. Neither line creates a folder.

## Get parts of a path

```python
from pathlib import Path

file = Path("data/orders.csv")
print(file.name)
print(file.stem)
print(file.suffix)
print(file.parent)
```

Expected output:

```text
orders.csv
orders
.csv
data
```

| Property | Meaning |
| --- | --- |
| `name` | Filename including extension |
| `stem` | Filename without its final extension |
| `suffix` | Final extension, including the dot |
| `parent` | Containing folder |

For `orders.backup.csv`, `stem` is `orders.backup` and `suffix` is `.csv`.

Properties do not use parentheses: `file.name`. Methods do: `file.exists()`.

## Check what exists

```python
from pathlib import Path

file = Path("data/orders.csv")
print(file.exists())
print(file.is_file())
print(file.is_dir())
```

Expected output **if this CSV exists as a regular file**:

```text
True
True
False
```

`exists()` checks for a file or folder. `is_file()` checks for a file; `is_dir()` checks for a folder. Results depend on the actual address and filesystem.

## Create folders with mkdir

```python
from pathlib import Path

folder = Path("reports/2026/november")
folder.mkdir(parents=True, exist_ok=True)
```

This creates the folder and any missing parent folders. It has no printed output.

The full parameter list is:

```python
folder.mkdir(mode=0o777, parents=False, exist_ok=False)
```

| Parameter | Default | Meaning |
| --- | --- | --- |
| `parents` | `False` | With `True`, create missing parent folders |
| `exist_ok` | `False` | With `True`, allow the target folder to exist already |
| `mode` | `0o777` | Requested permissions, mainly useful on Linux/macOS; system settings can reduce them |

`0o` means an octal number. You can usually leave `mode` at its default for this practice. Its treatment depends on the operating system. It does not set permissions on parents created through `parents=True`.

| Situation | Option | Behaviour |
| --- | --- | --- |
| Parent folder is missing | `parents=False` | `FileNotFoundError` |
| Parent folder is missing | `parents=True` | Creates missing parents and the target folder |
| Target folder already exists | `exist_ok=False` | `FileExistsError` |
| Target folder already exists | `exist_ok=True` | Allows the existing folder |

`exist_ok=True` does not empty a folder. If the target is an existing file, it still raises an error. Each method has its own parameters; these belong to `mkdir()`.

For example, running this twice is fine:

```python
from pathlib import Path

folder = Path("reports/daily")
folder.mkdir(parents=True, exist_ok=True)
folder.mkdir(parents=True, exist_ok=True)
```

Expected behaviour: the first call creates any missing folders. The second accepts the existing folder and leaves its contents alone.

**A file inside the folder is a different location:**

```text
reports/
    daily/          <- folder: reports/daily
        daily       <- file: reports/daily/daily
```

This is allowed. The names match, but the full paths differ.

**A file at the exact target location blocks folder creation.** A file can have no extension. To see the error, run this in a location where `path_collision_demo` does not already exist:

```python
from pathlib import Path

Path("path_collision_demo").mkdir()
Path("path_collision_demo/daily").write_text("Hello", encoding="utf-8")

# daily is already a FILE. Requesting a FOLDER here fails.
Path("path_collision_demo/daily").mkdir(exist_ok=True)
```

Expected error on Windows at the last line: `FileExistsError` (the exact message depends on the system).

At that point the structure is:

```text
path_collision_demo/
    daily           <- file containing Hello
```

`exist_ok=True` accepts an existing **folder**, not an existing file at the same path. It does not turn a file into a folder. If you rerun the whole example, the first line also raises an error because the demo folder now exists.

## Write and read text

Goal: save a short message and read it back.

```python
from pathlib import Path

folder = Path("path_demo")
folder.mkdir(exist_ok=True)
file = folder / "daily.txt"
count = file.write_text("Hello", encoding="utf-8")
print(count)
print(file.read_text(encoding="utf-8"))
```

Expected output:

```text
5
Hello
```

- `write_text()` creates the file or replaces its existing contents. It does not create missing parent folders.
- It returns the number of characters written. That is why a notebook can display `5` after writing `"Hello"` even without `print()`.
- `read_text()` returns the file contents as a string.
- `encoding="utf-8"` chooses how text is stored and read.

Your working notebook uses `Path("path_demo/daily").write_text("Hello", encoding="utf-8")` and has saved output `5`. Here, `daily` is a file with no extension. A file does not need `.txt`; the operation determines what is created.

## List files and folders

Assume `data` exists and contains the input files.

```python
from pathlib import Path

for item in Path("data").iterdir():
    print(item)

for file in Path("data").glob("*.csv"):
    print(file)

for file in Path("data").rglob("*.csv"):
    print(file)
```

- `iterdir()`: direct children, including files and folders.
- `glob("*.csv")`: matching names directly inside this folder.
- `rglob("*.csv")`: matching names in this folder and its subfolders.
- `*` means any sequence of characters in this pattern. Matching paths can include folders; add `is_file()` when only files are wanted.
- The printed paths depend on actual contents; do not rely on their order.

## Change an address without changing the file

```python
from pathlib import Path

file = Path("data/orders.csv")
print(file.with_name("backup.csv").as_posix())
print(file.with_suffix(".json").as_posix())
```

Expected output:

```text
data/backup.csv
data/orders.json
```

Both return new path objects. They do not rename the file or convert CSV data to JSON.

## Show a path relative to another folder

```python
from pathlib import Path

folder = Path("project")
file = folder / "data" / "orders.csv"
print(file.relative_to(folder).as_posix())
print(folder.relative_to(folder))
```

Expected output:

```text
data/orders.csv
.
```

The first line removes the starting `project` part. The second compares the same path with itself, so the result is `.`. This matches the same-path example in your working notebook. `relative_to()` does not move anything; with its default options, a path outside the given starting folder raises `ValueError`.

## Sources and practice

These are explanations and guided practice, not an independent assessment. Notebook outputs were inspected; examples above are labelled expected output, not learner execution results.

- [Official Python pathlib documentation](https://docs.python.org/3.14/library/pathlib.html)
- [Saved session evidence](../../../progress/pathlib/2026-11-03-session.md)
- [Practice questions without answers](../../revision/pathlib-questions.md)
- [File reading methods](file-methods.md)
