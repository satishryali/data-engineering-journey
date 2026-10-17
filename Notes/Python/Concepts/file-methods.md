# Work with an open file

An open file gives us methods to read its contents and move through it. A method is a function attached to an object, such as `file.read()`.

## Read and return to the start

Run this small example in a scratch folder.

```python
with open("read_example.txt", "w", encoding="utf-8", newline="") as file:
    file.write("hello\n")

with open("read_example.txt", "r", encoding="utf-8") as file:
    print(file.tell())
    print(repr(file.read()))
    print(repr(file.read()))
    file.seek(0)
    print(repr(file.read()))

print(file.closed)
```

Expected output:

```text
0
'hello\n'
''
'hello\n'
True
```

- `read()` reads from the current position to the end when no size is supplied.
- A second `read()` at the end returns an empty string.
- `seek(0)` moves back to the start of this file.
- `tell()` reports the current position. In text mode, treat it as a position marker, not a general character count. The notebook's final value `66` belongs to that file and environment.
- `repr()` makes the newline visible as `\n` in this example.
- A file's `with` block closes it on exit. The variable can still exist, but the file is closed.

Related: [context managers](with\(Context_Manager\).md).

## A method versus a method call

```python
with open("read_example.txt", "r", encoding="utf-8") as file:
    read_again = file.read
    print(file.tell())
    print(repr(read_again()))
```

Expected output, after creating the file above:

```text
0
'hello\n'
```

- `file.read` refers to the method. It does not read the file yet.
- `file.read()` calls the method and returns text.
- `read_again = file.read` keeps a reference to the method; `read_again()` calls it while the file is open.
- `print(file)` displays a description of the file object. Use `read()` or a loop to get its contents.

## Look up available methods

```python
with open("read_example.txt", "r", encoding="utf-8") as file:
    print("read" in dir(file))
    help(file.read)
```

Expected behaviour: the first line prints `True`; `help()` displays information about `read`.
`dir()` lists available names; it does not explain all of them. `help()` prints help and returns `None`, so `print(help(file.read))` also prints `None` afterwards.

## Read bytes and control printed newlines

```python
with open("read_example.txt", "rb") as file:
    print(file.read())

print("Hello", end="\r\n")
print("World")
```

Expected output:

```text
b'hello\n'
Hello
World
```

`"rb"` reads bytes rather than decoded text; the `b` marks a bytes value. `end` controls what `print()` adds after its value. In the notebook, `time.sleep(1)` pauses execution between the two prints; it does not change their text.

Source: [csv-module.ipynb](../../../practice/Modules/csv-module.ipynb), cells 10-14, 16-18, 21-25 and 30-32. Saved outputs show these experiments; no independent assessment was performed.
References: [Python I/O](https://docs.python.org/3/library/io.html), [built-in functions](https://docs.python.org/3/library/functions.html).
