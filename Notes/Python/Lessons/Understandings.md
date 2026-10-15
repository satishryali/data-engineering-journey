# Key Findings

- If you return name directly from a simple python file, We will get like print(__name__) : __main__, that is why whenever we are directly running a python program within the same file, we used to write it like.

```python
if __name__ == '__main__':
    main()
```

- So, whenever you are fetching it from another program lets say you are importing app.py in src.py then the __main__ in src.py.

```python
# app.py
print(__name__)
```

```python
# src.py
import app
print(__name__)
```

```python
#python src.py Output
app
__main__
```
